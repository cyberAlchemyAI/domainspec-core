use std::collections::BTreeSet;

use auth_foundation_kernel::{
    AuthorizationDecision, AuthorizationRequest, DenyReason, EvaluationContext, Permission, Role,
    Session, SessionStatus, authorize,
};

fn set<T: Ord>(values: impl IntoIterator<Item = T>) -> BTreeSet<T> {
    values.into_iter().collect()
}

struct Fixture {
    request: AuthorizationRequest,
    sessions: Vec<Session>,
    roles: Vec<Role>,
    trusted_scope_evidence: bool,
    role_relation_complete: bool,
}

impl Fixture {
    fn valid() -> Self {
        let permission = Permission::new("invoice", "read", "tenant-7");
        Self {
            request: AuthorizationRequest {
                request_id: "request-1".into(),
                session_id: "session-1".into(),
                required_permission: permission.clone(),
                scope_evidence_ref: "scope-evidence-1".into(),
                decision_time: 100,
                current_authorization_revision: 7,
            },
            sessions: vec![Session {
                session_id: "session-1".into(),
                user_id: "user-1".into(),
                status: SessionStatus::Active,
                active_role_ids: set(["reader".into()]),
                authorization_revision: 7,
                expires_at: 101,
            }],
            roles: vec![Role {
                role_id: "reader".into(),
                permissions: set([permission]),
            }],
            trusted_scope_evidence: true,
            role_relation_complete: true,
        }
    }

    fn evaluate(&self) -> AuthorizationDecision {
        authorize(EvaluationContext {
            request: &self.request,
            resolved_sessions: &self.sessions,
            resolved_roles: &self.roles,
            trusted_scope_evidence: self.trusted_scope_evidence,
            role_relation_complete: self.role_relation_complete,
        })
    }
}

#[test]
fn permitted_case_exact_active_role_grant_allows() {
    assert_eq!(Fixture::valid().evaluate(), AuthorizationDecision::Allow);
}

#[test]
fn inadmissible_missing_session_denies() {
    let mut fixture = Fixture::valid();
    fixture.sessions.clear();
    assert_eq!(
        fixture.evaluate(),
        AuthorizationDecision::Deny(DenyReason::MissingSession)
    );
}

#[test]
fn ambiguous_session_resolution_denies() {
    let mut fixture = Fixture::valid();
    fixture.sessions.push(fixture.sessions[0].clone());
    assert_eq!(
        fixture.evaluate(),
        AuthorizationDecision::Deny(DenyReason::AmbiguousSession)
    );
}

#[test]
fn inactive_or_revoked_session_denies() {
    for status in [SessionStatus::Inactive, SessionStatus::Revoked] {
        let mut fixture = Fixture::valid();
        fixture.sessions[0].status = status;
        assert_eq!(
            fixture.evaluate(),
            AuthorizationDecision::Deny(DenyReason::InactiveSession)
        );
    }
}

#[test]
fn expiry_boundary_is_fail_closed() {
    let mut fixture = Fixture::valid();
    fixture.sessions[0].expires_at = fixture.request.decision_time;
    assert_eq!(
        fixture.evaluate(),
        AuthorizationDecision::Deny(DenyReason::ExpiredSession)
    );
}

#[test]
fn stale_authorization_revision_denies() {
    let mut fixture = Fixture::valid();
    fixture.request.current_authorization_revision += 1;
    assert_eq!(
        fixture.evaluate(),
        AuthorizationDecision::Deny(DenyReason::StaleAuthorizationRevision)
    );
}

#[test]
fn missing_or_untrusted_scope_evidence_denies() {
    let mut fixture = Fixture::valid();
    fixture.trusted_scope_evidence = false;
    assert_eq!(
        fixture.evaluate(),
        AuthorizationDecision::Deny(DenyReason::UntrustedScopeEvidence)
    );
    let mut fixture = Fixture::valid();
    fixture.request.scope_evidence_ref.clear();
    assert_eq!(
        fixture.evaluate(),
        AuthorizationDecision::Deny(DenyReason::UntrustedScopeEvidence)
    );
}

#[test]
fn incomplete_active_role_relation_denies() {
    let mut fixture = Fixture::valid();
    fixture.role_relation_complete = false;
    assert_eq!(
        fixture.evaluate(),
        AuthorizationDecision::Deny(DenyReason::IncompleteRoleRelation)
    );
}

#[test]
fn missing_extra_or_duplicate_resolved_roles_deny() {
    let mut missing = Fixture::valid();
    missing.roles.clear();
    assert_eq!(
        missing.evaluate(),
        AuthorizationDecision::Deny(DenyReason::RoleRelationMismatch)
    );

    let mut extra = Fixture::valid();
    extra.roles.push(Role {
        role_id: "extra".into(),
        permissions: BTreeSet::new(),
    });
    assert_eq!(
        extra.evaluate(),
        AuthorizationDecision::Deny(DenyReason::RoleRelationMismatch)
    );

    let mut duplicate = Fixture::valid();
    duplicate.roles.push(duplicate.roles[0].clone());
    assert_eq!(
        duplicate.evaluate(),
        AuthorizationDecision::Deny(DenyReason::DuplicateResolvedRole)
    );
}

#[test]
fn active_role_without_grant_denies() {
    let mut fixture = Fixture::valid();
    fixture.sessions[0].active_role_ids = set(["other".into()]);
    fixture.roles[0].role_id = "other".into();
    fixture.roles[0].permissions.clear();
    assert_eq!(
        fixture.evaluate(),
        AuthorizationDecision::Deny(DenyReason::NoExactActiveRoleGrant)
    );
}

#[test]
fn resource_action_or_scope_mismatch_denies() {
    for permission in [
        Permission::new("other", "read", "tenant-7"),
        Permission::new("invoice", "write", "tenant-7"),
        Permission::new("invoice", "read", "tenant-8"),
    ] {
        let mut fixture = Fixture::valid();
        fixture.roles[0].permissions = set([permission]);
        assert_eq!(
            fixture.evaluate(),
            AuthorizationDecision::Deny(DenyReason::NoExactActiveRoleGrant)
        );
    }
}

#[test]
fn any_one_exact_active_role_grant_is_sufficient() {
    let mut fixture = Fixture::valid();
    fixture.sessions[0].active_role_ids.insert("empty".into());
    fixture.roles.insert(
        0,
        Role {
            role_id: "empty".into(),
            permissions: BTreeSet::new(),
        },
    );
    assert_eq!(fixture.evaluate(), AuthorizationDecision::Allow);
}

#[test]
fn decision_is_total_and_default_deny_for_near_matches() {
    let resources = ["invoice", "other"];
    let actions = ["read", "write"];
    let scopes = ["tenant-7", "tenant-8"];
    for resource in resources {
        for action in actions {
            for scope in scopes {
                let mut fixture = Fixture::valid();
                fixture.roles[0].permissions = set([Permission::new(resource, action, scope)]);
                let exact = resource == "invoice" && action == "read" && scope == "tenant-7";
                assert_eq!(fixture.evaluate() == AuthorizationDecision::Allow, exact);
            }
        }
    }
}
