use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

use auth_foundation_authorization_service::SqliteAuthService;
use auth_foundation_runtime_adapter::{BinaryAuthorizationDecision, DecisionClock, PortFailure};
use auth_foundation_sqlite_provider::SCHEMA_V1 as AUTHORIZATION_SCHEMA_V1;
use auth_foundation_trusted_boundary::InboundAuthorizationRequest;
use auth_foundation_trusted_input_provider::SCHEMA_V1 as TRUSTED_INPUT_SCHEMA_V1;
use rusqlite::Connection;

#[derive(Clone, Copy)]
struct FixedClock(u64);

impl DecisionClock for FixedClock {
    fn decision_time(&self) -> Result<u64, PortFailure> {
        Ok(self.0)
    }
}

fn request() -> InboundAuthorizationRequest {
    InboundAuthorizationRequest {
        request_id: "request-1".into(),
        authentication_evidence_ref: "auth-1".into(),
        route_id: "documents.read".into(),
    }
}

fn seed_trusted_inputs(path: &Path) {
    let connection = Connection::open(path).expect("open trusted input database");
    connection
        .execute_batch(TRUSTED_INPUT_SCHEMA_V1)
        .expect("apply trusted input schema");
    connection
        .execute_batch(
            "INSERT INTO auth_authentication_evidence
                 (evidence_row_id, evidence_ref, session_id, trusted, revoked, expires_at)
             VALUES (1, 'auth-1', 'session-1', 1, 0, 101);
             INSERT INTO auth_route_authorization_bindings
                 (binding_row_id, route_id, resource, action, scope, scope_evidence_ref, complete, enabled)
             VALUES (1, 'documents.read', 'documents', 'read', 'tenant-7', 'scope-1', 1, 1);",
        )
        .expect("seed trusted inputs");
}

fn seed_authorization_state(path: &Path) {
    let connection = Connection::open(path).expect("open authorization database");
    connection
        .execute_batch(AUTHORIZATION_SCHEMA_V1)
        .expect("apply authorization schema");
    connection
        .execute_batch(
            "INSERT INTO auth_roles (role_id) VALUES ('reader');
             INSERT INTO auth_role_permissions (role_id, resource, action, scope)
             VALUES ('reader', 'documents', 'read', 'tenant-7');
             INSERT INTO auth_sessions
                 (session_row_id, session_id, user_id, status, authorization_revision, expires_at)
             VALUES (1, 'session-1', 'user-1', 'active', 7, 101);
             INSERT INTO auth_session_active_roles (session_row_id, role_id)
             VALUES (1, 'reader');
             INSERT INTO auth_authorization_revisions (session_id, revision)
             VALUES ('session-1', 7);
             INSERT INTO auth_scope_evidence
                 (evidence_ref, resource, action, scope, trusted)
             VALUES ('scope-1', 'documents', 'read', 'tenant-7', 1);",
        )
        .expect("seed authorization state");
}

fn fixture() -> (PathBuf, PathBuf) {
    let trusted = unique_database_path("trusted-input");
    let authorization = unique_database_path("authorization-state");
    seed_trusted_inputs(&trusted);
    seed_authorization_state(&authorization);
    (trusted, authorization)
}

fn run_with_trusted_mutation(mutation: &str, time: u64) -> BinaryAuthorizationDecision {
    let (trusted, authorization) = fixture();
    if !mutation.is_empty() {
        Connection::open(&trusted)
            .expect("reopen trusted inputs")
            .execute_batch(mutation)
            .expect("mutate trusted inputs");
    }
    let mut service = SqliteAuthService::open(&trusted, &authorization, FixedClock(time))
        .expect("open composed service");
    let decision = service.authorize(request());
    drop(service);
    remove_fixture(trusted, authorization);
    decision
}

#[test]
fn complete_current_server_owned_evidence_allows_end_to_end() {
    assert_eq!(
        run_with_trusted_mutation("", 100),
        BinaryAuthorizationDecision::Allow
    );
}

#[test]
fn authentication_evidence_failures_deny_end_to_end() {
    for mutation in [
        "DELETE FROM auth_authentication_evidence;",
        "INSERT INTO auth_authentication_evidence
             (evidence_row_id, evidence_ref, session_id, trusted, revoked, expires_at)
         VALUES (2, 'auth-1', 'session-2', 1, 0, 101);",
        "UPDATE auth_authentication_evidence SET trusted = 0;",
        "UPDATE auth_authentication_evidence SET revoked = 1;",
    ] {
        assert_eq!(
            run_with_trusted_mutation(mutation, 100),
            BinaryAuthorizationDecision::Deny
        );
    }
    assert_eq!(
        run_with_trusted_mutation("", 101),
        BinaryAuthorizationDecision::Deny
    );
}

#[test]
fn route_binding_failures_deny_end_to_end() {
    for mutation in [
        "DELETE FROM auth_route_authorization_bindings;",
        "INSERT INTO auth_route_authorization_bindings
             (binding_row_id, route_id, resource, action, scope, scope_evidence_ref, complete, enabled)
         VALUES (2, 'documents.read', 'documents', 'read', 'tenant-7', 'scope-1', 1, 1);",
        "UPDATE auth_route_authorization_bindings SET complete = 0;",
        "UPDATE auth_route_authorization_bindings SET enabled = 0;",
    ] {
        assert_eq!(
            run_with_trusted_mutation(mutation, 100),
            BinaryAuthorizationDecision::Deny
        );
    }
}

#[test]
fn downstream_permission_mismatch_preserves_deny() {
    let (trusted, authorization) = fixture();
    Connection::open(&authorization)
        .expect("reopen authorization state")
        .execute("UPDATE auth_role_permissions SET action = 'write'", [])
        .expect("mutate permission");
    let mut service = SqliteAuthService::open(&trusted, &authorization, FixedClock(100))
        .expect("open composed service");
    assert_eq!(
        service.authorize(request()),
        BinaryAuthorizationDecision::Deny
    );
    drop(service);
    remove_fixture(trusted, authorization);
}

fn unique_database_path(label: &str) -> PathBuf {
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("system time")
        .as_nanos();
    std::env::temp_dir().join(format!(
        "auth-foundation-{label}-{}-{nonce}.sqlite",
        std::process::id()
    ))
}

fn remove_fixture(trusted: PathBuf, authorization: PathBuf) {
    std::fs::remove_file(trusted).expect("remove trusted input database");
    std::fs::remove_file(authorization).expect("remove authorization database");
}
