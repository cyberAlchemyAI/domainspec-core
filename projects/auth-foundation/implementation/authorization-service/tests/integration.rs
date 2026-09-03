use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

use auth_foundation_authorization_service::SqliteAuthService;
use auth_foundation_runtime_adapter::{BinaryAuthorizationDecision, DecisionClock, PortFailure};
use auth_foundation_trusted_boundary::InboundAuthorizationRequest;
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

fn fixture() -> PathBuf {
    let path = unique_database_path();
    drop(SqliteAuthService::open(&path, FixedClock(100)).expect("prepare unified schema"));
    Connection::open(&path)
        .expect("open fixture")
        .execute_batch(
            "INSERT INTO auth_authentication_evidence
             (evidence_row_id, evidence_ref, session_id, trusted, revoked, expires_at,
              evidence_revision, authenticated_subject_id)
         VALUES (1, 'auth-1', 'session-1', 1, 0, 101, 3, 'user-1');
         INSERT INTO auth_route_authorization_bindings
             (binding_row_id, route_id, resource, action, scope, scope_evidence_ref,
              complete, enabled, binding_revision)
         VALUES (1, 'documents.read', 'documents', 'read', 'tenant-7', 'scope-1', 1, 1, 5);
         INSERT INTO auth_roles (role_id) VALUES ('reader');
         INSERT INTO auth_role_permissions
             (role_id, resource, action, scope, authorization_revision)
         VALUES ('reader', 'documents', 'read', 'tenant-7', 7);
         INSERT INTO auth_sessions
             (session_row_id, session_id, user_id, status, authorization_revision, expires_at)
         VALUES (1, 'session-1', 'user-1', 'active', 7, 101);
         INSERT INTO auth_session_active_roles
             (session_row_id, role_id, authorization_revision)
         VALUES (1, 'reader', 7);
         INSERT INTO auth_authorization_revisions (session_id, revision)
         VALUES ('session-1', 7);
         INSERT INTO auth_scope_evidence (evidence_ref, resource, action, scope, trusted)
         VALUES ('scope-1', 'documents', 'read', 'tenant-7', 1);",
        )
        .expect("seed unified auth database");
    path
}

fn run(mutation: &str, time: u64) -> BinaryAuthorizationDecision {
    let path = fixture();
    if !mutation.is_empty() {
        Connection::open(&path)
            .expect("open mutation connection")
            .execute_batch(mutation)
            .expect("apply mutation");
    }
    let decision = SqliteAuthService::open(&path, FixedClock(time))
        .expect("open service")
        .authorize(request());
    std::fs::remove_file(path).expect("remove fixture");
    decision
}

#[test]
fn one_complete_epoch_allows() {
    assert_eq!(run("", 100), BinaryAuthorizationDecision::Allow);
}

#[test]
fn trusted_input_failures_deny() {
    for mutation in [
        "DELETE FROM auth_authentication_evidence;",
        "UPDATE auth_authentication_evidence SET authenticated_subject_id = '';",
        "UPDATE auth_authentication_evidence SET revoked = 1;",
        "UPDATE auth_route_authorization_bindings SET enabled = 0;",
    ] {
        assert_eq!(run(mutation, 100), BinaryAuthorizationDecision::Deny);
    }
    assert_eq!(run("", 101), BinaryAuthorizationDecision::Deny);
}

#[test]
fn identity_and_revision_join_failures_deny() {
    for mutation in [
        "UPDATE auth_sessions SET user_id = 'user-2';",
        "UPDATE auth_authorization_revisions SET revision = 8;",
        "UPDATE auth_session_active_roles SET authorization_revision = 6;",
        "UPDATE auth_role_permissions SET authorization_revision = 6;",
    ] {
        assert_eq!(run(mutation, 100), BinaryAuthorizationDecision::Deny);
    }
}

#[test]
fn permission_mismatch_denies() {
    assert_eq!(
        run("UPDATE auth_role_permissions SET action = 'write';", 100),
        BinaryAuthorizationDecision::Deny
    );
}

fn unique_database_path() -> PathBuf {
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("time")
        .as_nanos();
    std::env::temp_dir().join(format!(
        "auth-service-{}-{nonce}.sqlite",
        std::process::id()
    ))
}
