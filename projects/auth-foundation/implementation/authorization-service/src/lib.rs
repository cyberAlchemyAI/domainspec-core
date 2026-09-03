//! In-process Auth service composition with one transaction-scoped SQLite evaluation epoch.

use std::path::Path;

use auth_foundation_runtime_adapter::{
    BinaryAuthorizationDecision, DecisionClock, Permission, PortFailure,
};
use auth_foundation_sqlite_provider::{
    SCHEMA_V1 as AUTHORIZATION_SCHEMA_V1, authorize_in_transaction,
};
use auth_foundation_trusted_boundary::{
    AuthenticatedSessionEvidence, AuthenticationEvidenceResolver, AuthorizationCommand,
    AuthorizationDecisionService, InboundAuthorizationRequest, RouteAuthorizationBinding,
    RouteAuthorizationBindingResolver, TrustedAuthorizationBoundary,
};
use auth_foundation_trusted_input_provider::{
    SCHEMA_V1 as TRUSTED_INPUT_SCHEMA_V1, TrustedInputResolution, resolve_in_transaction,
};
use rusqlite::{Connection, OptionalExtension, Transaction, TransactionBehavior};

pub const SCHEMA_V2: &str = include_str!("../migrations/0002_auth_service_epoch.sql");

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AuthorizationEvaluationEpoch {
    pub evaluation_epoch_id: u64,
    pub decision_time: u64,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ExactTrustedInputSnapshot {
    pub evaluation_epoch_id: u64,
    pub decision_time: u64,
    pub authentication_evidence_ref: String,
    pub authentication_evidence_revision: u64,
    pub authenticated_subject_id: String,
    pub session_id: String,
    pub authentication_expires_at: u64,
    pub route_ref: String,
    pub route_binding_revision: u64,
    pub required_permission: Permission,
    pub scope_evidence_ref: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ExactTrustedAuthorizationCommand {
    pub evaluation_epoch_id: u64,
    pub decision_time: u64,
    pub session_id: String,
    pub authenticated_subject_id: String,
    pub required_permission: Permission,
    pub scope_evidence_ref: String,
    pub authentication_evidence_revision: u64,
    pub route_binding_revision: u64,
}

pub struct SqliteAuthService<C: DecisionClock> {
    connection: Connection,
    clock: C,
    next_epoch_id: u64,
}

impl<C: DecisionClock> SqliteAuthService<C> {
    pub fn open(path: impl AsRef<Path>, clock: C) -> Result<Self, PortFailure> {
        Self::from_connection(Connection::open(path).map_err(|_| PortFailure)?, clock)
    }

    pub fn open_in_memory(clock: C) -> Result<Self, PortFailure> {
        Self::from_connection(
            Connection::open_in_memory().map_err(|_| PortFailure)?,
            clock,
        )
    }

    pub fn from_connection(connection: Connection, clock: C) -> Result<Self, PortFailure> {
        connection
            .execute_batch(AUTHORIZATION_SCHEMA_V1)
            .map_err(|_| PortFailure)?;
        connection
            .execute_batch(TRUSTED_INPUT_SCHEMA_V1)
            .map_err(|_| PortFailure)?;
        apply_epoch_schema(&connection)?;
        Ok(Self {
            connection,
            clock,
            next_epoch_id: 1,
        })
    }

    pub fn authorize(
        &mut self,
        request: InboundAuthorizationRequest,
    ) -> BinaryAuthorizationDecision {
        let decision_time = match self.clock.decision_time() {
            Ok(value) => value,
            Err(_) => return BinaryAuthorizationDecision::Deny,
        };
        let epoch = AuthorizationEvaluationEpoch {
            evaluation_epoch_id: self.next_epoch_id,
            decision_time,
        };
        self.next_epoch_id = self.next_epoch_id.saturating_add(1);
        let transaction = match self
            .connection
            .transaction_with_behavior(TransactionBehavior::Deferred)
        {
            Ok(value) => value,
            Err(_) => return BinaryAuthorizationDecision::Deny,
        };
        let decision = authorize_in_epoch(&transaction, &epoch, request);
        match transaction.commit() {
            Ok(()) => decision,
            Err(_) => BinaryAuthorizationDecision::Deny,
        }
    }
}

fn authorize_in_epoch(
    transaction: &Transaction<'_>,
    epoch: &AuthorizationEvaluationEpoch,
    request: InboundAuthorizationRequest,
) -> BinaryAuthorizationDecision {
    let Ok((query, resolution)) = resolve_in_transaction(
        transaction,
        &request.authentication_evidence_ref,
        &request.route_id,
        epoch.decision_time,
    ) else {
        return BinaryAuthorizationDecision::Deny;
    };
    let TrustedInputResolution::Resolved(snapshot) = resolution else {
        return BinaryAuthorizationDecision::Deny;
    };
    if query.decision_time != epoch.decision_time
        || snapshot.authentication_evidence.len() != 1
        || snapshot.route_bindings.len() != 1
    {
        return BinaryAuthorizationDecision::Deny;
    }

    let evidence = &snapshot.authentication_evidence[0];
    let binding = &snapshot.route_bindings[0];
    if evidence.evidence_ref != request.authentication_evidence_ref
        || !evidence.trusted
        || evidence.revoked
        || epoch.decision_time >= evidence.expires_at
        || binding.route_id != request.route_id
        || !binding.complete
        || !binding.enabled
    {
        return BinaryAuthorizationDecision::Deny;
    }

    let Some((evidence_revision, subject_id)) =
        authentication_metadata(transaction, evidence.evidence_identity)
    else {
        return BinaryAuthorizationDecision::Deny;
    };
    let Some(route_binding_revision) = route_revision(transaction, binding.binding_identity) else {
        return BinaryAuthorizationDecision::Deny;
    };
    let exact_snapshot = ExactTrustedInputSnapshot {
        evaluation_epoch_id: epoch.evaluation_epoch_id,
        decision_time: epoch.decision_time,
        authentication_evidence_ref: evidence.evidence_ref.clone(),
        authentication_evidence_revision: evidence_revision,
        authenticated_subject_id: subject_id,
        session_id: evidence.session_id.clone(),
        authentication_expires_at: evidence.expires_at,
        route_ref: binding.route_id.clone(),
        route_binding_revision,
        required_permission: Permission {
            resource: binding.resource.clone(),
            action: binding.action.clone(),
            scope: binding.scope.clone(),
        },
        scope_evidence_ref: binding.scope_evidence_ref.clone(),
    };
    let command = command_from_snapshot(&exact_snapshot);
    if !authorization_state_joins_hold(transaction, epoch, &command) {
        return BinaryAuthorizationDecision::Deny;
    }

    let authentication = ResolvedAuthenticationEvidence(vec![AuthenticatedSessionEvidence {
        evidence_ref: exact_snapshot.authentication_evidence_ref,
        session_id: exact_snapshot.session_id,
        trusted: true,
    }]);
    let routes = ResolvedRouteBindings(vec![RouteAuthorizationBinding {
        route_id: exact_snapshot.route_ref,
        required_permission: command.required_permission.clone(),
        scope_evidence_ref: command.scope_evidence_ref.clone(),
        complete: true,
    }]);
    TrustedAuthorizationBoundary::new(
        authentication,
        routes,
        TransactionDecisionService {
            transaction,
            decision_time: epoch.decision_time,
        },
    )
    .authorize(request)
}

fn command_from_snapshot(snapshot: &ExactTrustedInputSnapshot) -> ExactTrustedAuthorizationCommand {
    ExactTrustedAuthorizationCommand {
        evaluation_epoch_id: snapshot.evaluation_epoch_id,
        decision_time: snapshot.decision_time,
        session_id: snapshot.session_id.clone(),
        authenticated_subject_id: snapshot.authenticated_subject_id.clone(),
        required_permission: snapshot.required_permission.clone(),
        scope_evidence_ref: snapshot.scope_evidence_ref.clone(),
        authentication_evidence_revision: snapshot.authentication_evidence_revision,
        route_binding_revision: snapshot.route_binding_revision,
    }
}

fn authentication_metadata(transaction: &Transaction<'_>, row_id: u64) -> Option<(u64, String)> {
    let row_id = i64::try_from(row_id).ok()?;
    let rows = transaction.prepare(
        "SELECT evidence_revision, authenticated_subject_id FROM auth_authentication_evidence WHERE evidence_row_id = ?1"
    ).ok()?.query_map([row_id], |row| Ok((row.get::<_, i64>(0)?, row.get::<_, String>(1)?)))
        .ok()?.collect::<Result<Vec<_>, _>>().ok()?;
    match rows.as_slice() {
        [(revision, subject)] if *revision >= 0 && !subject.is_empty() => {
            Some((*revision as u64, subject.clone()))
        }
        _ => None,
    }
}

fn route_revision(transaction: &Transaction<'_>, row_id: u64) -> Option<u64> {
    let value = transaction.query_row(
        "SELECT binding_revision FROM auth_route_authorization_bindings WHERE binding_row_id = ?1",
        [i64::try_from(row_id).ok()?], |row| row.get::<_, i64>(0),
    ).optional().ok()??;
    value.try_into().ok()
}

fn authorization_state_joins_hold(
    transaction: &Transaction<'_>,
    epoch: &AuthorizationEvaluationEpoch,
    command: &ExactTrustedAuthorizationCommand,
) -> bool {
    if command.evaluation_epoch_id != epoch.evaluation_epoch_id
        || command.decision_time != epoch.decision_time
    {
        return false;
    }
    let sessions = match transaction.prepare(
        "SELECT session_row_id, user_id, authorization_revision FROM auth_sessions WHERE session_id = ?1 ORDER BY session_row_id"
    ) {
        Ok(mut statement) => match statement.query_map([&command.session_id], |row| {
            Ok((row.get::<_, i64>(0)?, row.get::<_, String>(1)?, row.get::<_, i64>(2)?))
        }) {
            Ok(rows) => match rows.collect::<Result<Vec<_>, _>>() { Ok(rows) => rows, Err(_) => return false },
            Err(_) => return false,
        }, Err(_) => return false,
    };
    let [(session_row_id, subject_id, session_revision)] = sessions.as_slice() else {
        return false;
    };
    if subject_id != &command.authenticated_subject_id || *session_revision < 0 {
        return false;
    }
    let current_revision = match transaction.query_row(
        "SELECT revision FROM auth_authorization_revisions WHERE session_id = ?1",
        [&command.session_id],
        |row| row.get::<_, i64>(0),
    ) {
        Ok(value) => value,
        Err(_) => return false,
    };
    if *session_revision != current_revision {
        return false;
    }
    let stale_roles: i64 = match transaction.query_row(
        "SELECT COUNT(*) FROM auth_session_active_roles WHERE session_row_id = ?1 AND authorization_revision != ?2",
        rusqlite::params![session_row_id, current_revision], |row| row.get(0),
    ) { Ok(value) => value, Err(_) => return false };
    let stale_grants: i64 = match transaction.query_row(
        "SELECT COUNT(*) FROM auth_role_permissions WHERE role_id IN
         (SELECT role_id FROM auth_session_active_roles WHERE session_row_id = ?1)
         AND authorization_revision != ?2",
        rusqlite::params![session_row_id, current_revision],
        |row| row.get(0),
    ) {
        Ok(value) => value,
        Err(_) => return false,
    };
    stale_roles == 0 && stale_grants == 0
}

fn apply_epoch_schema(connection: &Connection) -> Result<(), PortFailure> {
    for (table, column, definition) in [
        (
            "auth_authentication_evidence",
            "evidence_revision",
            "INTEGER NOT NULL DEFAULT 0 CHECK (evidence_revision >= 0)",
        ),
        (
            "auth_authentication_evidence",
            "authenticated_subject_id",
            "TEXT NOT NULL DEFAULT ''",
        ),
        (
            "auth_route_authorization_bindings",
            "binding_revision",
            "INTEGER NOT NULL DEFAULT 0 CHECK (binding_revision >= 0)",
        ),
        (
            "auth_session_active_roles",
            "authorization_revision",
            "INTEGER NOT NULL DEFAULT 0 CHECK (authorization_revision >= 0)",
        ),
        (
            "auth_role_permissions",
            "authorization_revision",
            "INTEGER NOT NULL DEFAULT 0 CHECK (authorization_revision >= 0)",
        ),
    ] {
        if !has_column(connection, table, column)? {
            connection
                .execute_batch(&format!(
                    "ALTER TABLE {table} ADD COLUMN {column} {definition};"
                ))
                .map_err(|_| PortFailure)?;
        }
    }
    connection.execute_batch(SCHEMA_V2).map_err(|_| PortFailure)
}

fn has_column(connection: &Connection, table: &str, column: &str) -> Result<bool, PortFailure> {
    let mut statement = connection
        .prepare(&format!("PRAGMA table_info({table})"))
        .map_err(|_| PortFailure)?;
    let names = statement
        .query_map([], |row| row.get::<_, String>(1))
        .map_err(|_| PortFailure)?
        .collect::<Result<Vec<_>, _>>()
        .map_err(|_| PortFailure)?;
    Ok(names.iter().any(|name| name == column))
}

struct ResolvedAuthenticationEvidence(Vec<AuthenticatedSessionEvidence>);
impl AuthenticationEvidenceResolver for ResolvedAuthenticationEvidence {
    fn resolve_authentication_evidence(
        &self,
        _: &str,
    ) -> Result<Vec<AuthenticatedSessionEvidence>, PortFailure> {
        Ok(self.0.clone())
    }
}
struct ResolvedRouteBindings(Vec<RouteAuthorizationBinding>);
impl RouteAuthorizationBindingResolver for ResolvedRouteBindings {
    fn resolve_route_authorization_bindings(
        &self,
        _: &str,
    ) -> Result<Vec<RouteAuthorizationBinding>, PortFailure> {
        Ok(self.0.clone())
    }
}
struct TransactionDecisionService<'a, 'connection> {
    transaction: &'a Transaction<'connection>,
    decision_time: u64,
}
impl AuthorizationDecisionService for TransactionDecisionService<'_, '_> {
    fn authorize(&mut self, command: AuthorizationCommand) -> BinaryAuthorizationDecision {
        authorize_in_transaction(self.transaction, command, self.decision_time)
    }
}
