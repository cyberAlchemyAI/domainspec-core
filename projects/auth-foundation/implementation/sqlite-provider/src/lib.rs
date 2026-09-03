use std::collections::BTreeSet;
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};

use auth_foundation_runtime_adapter::{
    AuthorizationAdapter, AuthorizationCommand, AuthorizationRevisionSource,
    BinaryAuthorizationDecision, DecisionClock, PortFailure, RolePermission, RoleRecord,
    RoleResolution, RoleResolver, ScopeEvidenceVerifier, SessionRecord, SessionResolver,
    SessionStatus,
};
use rusqlite::{Connection, OptionalExtension, Transaction, TransactionBehavior};

pub const SCHEMA_V1: &str = include_str!("../migrations/0001_auth_state.sql");
const SCHEMA_VERSION: i64 = 1;

#[derive(Clone, Copy, Debug, Default)]
pub struct SystemClock;

impl DecisionClock for SystemClock {
    fn decision_time(&self) -> Result<u64, PortFailure> {
        let duration = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_err(|_| PortFailure)?;
        Ok(duration.as_secs())
    }
}

pub struct SqliteAuthorizationService<C> {
    connection: Connection,
    clock: C,
}

impl<C> SqliteAuthorizationService<C>
where
    C: DecisionClock,
{
    pub fn open(path: impl AsRef<Path>, clock: C) -> Result<Self, PortFailure> {
        let connection = Connection::open(path).map_err(|_| PortFailure)?;
        Self::from_connection(connection, clock)
    }

    pub fn open_in_memory(clock: C) -> Result<Self, PortFailure> {
        let connection = Connection::open_in_memory().map_err(|_| PortFailure)?;
        Self::from_connection(connection, clock)
    }

    pub fn from_connection(connection: Connection, clock: C) -> Result<Self, PortFailure> {
        connection
            .execute_batch("PRAGMA foreign_keys = ON;")
            .map_err(|_| PortFailure)?;
        let current_version = schema_version(&connection)?;
        if current_version > SCHEMA_VERSION {
            return Err(PortFailure);
        }
        connection
            .execute_batch(SCHEMA_V1)
            .map_err(|_| PortFailure)?;
        if schema_version(&connection)? != SCHEMA_VERSION {
            return Err(PortFailure);
        }
        Ok(Self { connection, clock })
    }

    pub fn authorize(&mut self, command: AuthorizationCommand) -> BinaryAuthorizationDecision {
        let transaction = match self
            .connection
            .transaction_with_behavior(TransactionBehavior::Deferred)
        {
            Ok(transaction) => transaction,
            Err(_) => return authorize_with_failed_ports(&self.clock, command),
        };
        let decision = authorize_in_transaction(
            &transaction,
            command,
            match self.clock.decision_time() {
                Ok(value) => value,
                Err(_) => return BinaryAuthorizationDecision::Deny,
            },
        );

        match transaction.commit() {
            Ok(()) => decision,
            Err(_) => BinaryAuthorizationDecision::Deny,
        }
    }
}

/// Evaluate authorization through a caller-owned SQLite transaction and a
/// decision time captured by that caller. This is the service-composition
/// entrypoint for keeping trusted-input and authorization-state reads in one
/// evaluation epoch.
pub fn authorize_in_transaction(
    transaction: &Transaction<'_>,
    command: AuthorizationCommand,
    decision_time: u64,
) -> BinaryAuthorizationDecision {
    let snapshot = SqliteSnapshot { transaction };
    AuthorizationAdapter::new(
        &snapshot,
        &snapshot,
        &snapshot,
        &snapshot,
        FixedClock(decision_time),
    )
    .authorize(command)
}

#[derive(Clone, Copy)]
struct FixedClock(u64);

impl DecisionClock for FixedClock {
    fn decision_time(&self) -> Result<u64, PortFailure> {
        Ok(self.0)
    }
}

fn schema_version(connection: &Connection) -> Result<i64, PortFailure> {
    connection
        .query_row("PRAGMA user_version", [], |row| row.get(0))
        .map_err(|_| PortFailure)
}

struct ClockRef<'a, C>(&'a C);

impl<C> DecisionClock for ClockRef<'_, C>
where
    C: DecisionClock,
{
    fn decision_time(&self) -> Result<u64, PortFailure> {
        self.0.decision_time()
    }
}

struct FailedPorts;

impl SessionResolver for FailedPorts {
    fn resolve_sessions(&self, _session_id: &str) -> Result<Vec<SessionRecord>, PortFailure> {
        Err(PortFailure)
    }
}

impl RoleResolver for FailedPorts {
    fn resolve_active_roles(
        &self,
        _session: &SessionRecord,
    ) -> Result<RoleResolution, PortFailure> {
        Err(PortFailure)
    }
}

impl ScopeEvidenceVerifier for FailedPorts {
    fn verify_scope_evidence(&self, _command: &AuthorizationCommand) -> Result<bool, PortFailure> {
        Err(PortFailure)
    }
}

impl AuthorizationRevisionSource for FailedPorts {
    fn current_authorization_revision(&self, _session_id: &str) -> Result<u64, PortFailure> {
        Err(PortFailure)
    }
}

fn authorize_with_failed_ports<C>(
    clock: &C,
    command: AuthorizationCommand,
) -> BinaryAuthorizationDecision
where
    C: DecisionClock,
{
    AuthorizationAdapter::new(
        FailedPorts,
        FailedPorts,
        FailedPorts,
        FailedPorts,
        ClockRef(clock),
    )
    .authorize(command)
}

struct SqliteSnapshot<'transaction, 'connection> {
    transaction: &'transaction Transaction<'connection>,
}

impl SessionResolver for &SqliteSnapshot<'_, '_> {
    fn resolve_sessions(&self, session_id: &str) -> Result<Vec<SessionRecord>, PortFailure> {
        let mut statement = self
            .transaction
            .prepare(
                "SELECT session_row_id, session_id, user_id, status, authorization_revision, expires_at
                 FROM auth_sessions
                 WHERE session_id = ?1
                 ORDER BY session_row_id",
            )
            .map_err(|_| PortFailure)?;
        let rows = statement
            .query_map([session_id], |row| {
                Ok((
                    row.get::<_, i64>(0)?,
                    row.get::<_, String>(1)?,
                    row.get::<_, String>(2)?,
                    row.get::<_, String>(3)?,
                    row.get::<_, i64>(4)?,
                    row.get::<_, i64>(5)?,
                ))
            })
            .map_err(|_| PortFailure)?
            .collect::<Result<Vec<_>, _>>()
            .map_err(|_| PortFailure)?;
        drop(statement);

        rows.into_iter()
            .map(
                |(row_id, resolved_session_id, user_id, status, revision, expires_at)| {
                    let active_role_ids = active_role_ids(&self.transaction, row_id)?;
                    Ok(SessionRecord {
                        session_id: resolved_session_id,
                        user_id,
                        status: parse_status(&status)?,
                        active_role_ids,
                        authorization_revision: to_u64(revision)?,
                        expires_at: to_u64(expires_at)?,
                    })
                },
            )
            .collect()
    }
}

impl RoleResolver for &SqliteSnapshot<'_, '_> {
    fn resolve_active_roles(&self, session: &SessionRecord) -> Result<RoleResolution, PortFailure> {
        let status = status_text(session.status);
        let revision = to_i64(session.authorization_revision)?;
        let expires_at = to_i64(session.expires_at)?;
        let mut statement = self
            .transaction
            .prepare(
                "SELECT session_row_id
                 FROM auth_sessions
                 WHERE session_id = ?1
                   AND user_id = ?2
                   AND status = ?3
                   AND authorization_revision = ?4
                   AND expires_at = ?5
                 ORDER BY session_row_id",
            )
            .map_err(|_| PortFailure)?;
        let row_ids = statement
            .query_map(
                rusqlite::params![
                    session.session_id,
                    session.user_id,
                    status,
                    revision,
                    expires_at
                ],
                |row| row.get::<_, i64>(0),
            )
            .map_err(|_| PortFailure)?
            .collect::<Result<Vec<_>, _>>()
            .map_err(|_| PortFailure)?;
        drop(statement);

        if row_ids.len() != 1 {
            return Ok(RoleResolution {
                roles: Vec::new(),
                complete: false,
            });
        }

        let resolved_role_ids = active_role_ids(&self.transaction, row_ids[0])?;
        if resolved_role_ids != session.active_role_ids {
            return Ok(RoleResolution {
                roles: Vec::new(),
                complete: false,
            });
        }

        let mut roles = Vec::with_capacity(resolved_role_ids.len());
        for role_id in &resolved_role_ids {
            let exists = self
                .transaction
                .query_row(
                    "SELECT role_id FROM auth_roles WHERE role_id = ?1",
                    [role_id],
                    |row| row.get::<_, String>(0),
                )
                .optional()
                .map_err(|_| PortFailure)?;
            if exists.is_none() {
                return Ok(RoleResolution {
                    roles: Vec::new(),
                    complete: false,
                });
            }
            roles.push(RoleRecord {
                role_id: role_id.clone(),
                permissions: role_permissions(&self.transaction, role_id)?,
            });
        }

        Ok(RoleResolution {
            roles,
            complete: true,
        })
    }
}

impl ScopeEvidenceVerifier for &SqliteSnapshot<'_, '_> {
    fn verify_scope_evidence(&self, command: &AuthorizationCommand) -> Result<bool, PortFailure> {
        let count = self
            .transaction
            .query_row(
                "SELECT COUNT(*)
                 FROM auth_scope_evidence
                 WHERE evidence_ref = ?1
                   AND resource = ?2
                   AND action = ?3
                   AND scope = ?4
                   AND trusted = 1",
                rusqlite::params![
                    command.scope_evidence_ref,
                    command.required_permission.resource,
                    command.required_permission.action,
                    command.required_permission.scope
                ],
                |row| row.get::<_, i64>(0),
            )
            .map_err(|_| PortFailure)?;
        Ok(count == 1)
    }
}

impl AuthorizationRevisionSource for &SqliteSnapshot<'_, '_> {
    fn current_authorization_revision(&self, session_id: &str) -> Result<u64, PortFailure> {
        let revision = self
            .transaction
            .query_row(
                "SELECT revision
                 FROM auth_authorization_revisions
                 WHERE session_id = ?1",
                [session_id],
                |row| row.get::<_, i64>(0),
            )
            .optional()
            .map_err(|_| PortFailure)?
            .ok_or(PortFailure)?;
        to_u64(revision)
    }
}

fn active_role_ids(
    transaction: &Transaction<'_>,
    session_row_id: i64,
) -> Result<BTreeSet<String>, PortFailure> {
    let mut statement = transaction
        .prepare(
            "SELECT role_id
             FROM auth_session_active_roles
             WHERE session_row_id = ?1
             ORDER BY role_id",
        )
        .map_err(|_| PortFailure)?;
    statement
        .query_map([session_row_id], |row| row.get::<_, String>(0))
        .map_err(|_| PortFailure)?
        .collect::<Result<BTreeSet<_>, _>>()
        .map_err(|_| PortFailure)
}

fn role_permissions(
    transaction: &Transaction<'_>,
    role_id: &str,
) -> Result<BTreeSet<RolePermission>, PortFailure> {
    let mut statement = transaction
        .prepare(
            "SELECT resource, action, scope
             FROM auth_role_permissions
             WHERE role_id = ?1
             ORDER BY resource, action, scope",
        )
        .map_err(|_| PortFailure)?;
    statement
        .query_map([role_id], |row| {
            Ok(RolePermission {
                resource: row.get(0)?,
                action: row.get(1)?,
                scope: row.get(2)?,
            })
        })
        .map_err(|_| PortFailure)?
        .collect::<Result<BTreeSet<_>, _>>()
        .map_err(|_| PortFailure)
}

fn parse_status(value: &str) -> Result<SessionStatus, PortFailure> {
    match value {
        "active" => Ok(SessionStatus::Active),
        "inactive" => Ok(SessionStatus::Inactive),
        "revoked" => Ok(SessionStatus::Revoked),
        _ => Err(PortFailure),
    }
}

fn status_text(value: SessionStatus) -> &'static str {
    match value {
        SessionStatus::Active => "active",
        SessionStatus::Inactive => "inactive",
        SessionStatus::Revoked => "revoked",
    }
}

fn to_u64(value: i64) -> Result<u64, PortFailure> {
    value.try_into().map_err(|_| PortFailure)
}

fn to_i64(value: u64) -> Result<i64, PortFailure> {
    value.try_into().map_err(|_| PortFailure)
}
