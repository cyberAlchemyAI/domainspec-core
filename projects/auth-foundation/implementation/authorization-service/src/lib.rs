//! In-process Auth service composition with concrete SQLite trusted-input and authorization providers.

use std::path::Path;

use auth_foundation_runtime_adapter::{BinaryAuthorizationDecision, DecisionClock, PortFailure};
use auth_foundation_sqlite_provider::SqliteAuthorizationService;
use auth_foundation_trusted_boundary::{
    AuthenticatedSessionEvidence, AuthenticationEvidenceResolver, AuthorizationCommand,
    AuthorizationDecisionService, InboundAuthorizationRequest, RouteAuthorizationBinding,
    RouteAuthorizationBindingResolver, TrustedAuthorizationBoundary,
};
use auth_foundation_trusted_input_provider::{SqliteTrustedInputResolver, TrustedInputResolution};

pub struct SqliteAuthService<C>
where
    C: DecisionClock,
{
    trusted_inputs: SqliteTrustedInputResolver<C>,
    downstream: SqliteAuthorizationService<C>,
}

impl<C> SqliteAuthService<C>
where
    C: DecisionClock + Clone,
{
    pub fn open(
        trusted_input_path: impl AsRef<Path>,
        authorization_state_path: impl AsRef<Path>,
        clock: C,
    ) -> Result<Self, PortFailure> {
        let trusted_inputs = SqliteTrustedInputResolver::open(&trusted_input_path, clock.clone())?;
        let downstream = SqliteAuthorizationService::open(authorization_state_path, clock)?;
        Ok(Self {
            trusted_inputs,
            downstream,
        })
    }

    pub fn authorize(
        &mut self,
        request: InboundAuthorizationRequest,
    ) -> BinaryAuthorizationDecision {
        let Ok((query, resolution)) = self
            .trusted_inputs
            .resolve(&request.authentication_evidence_ref, &request.route_id)
        else {
            return BinaryAuthorizationDecision::Deny;
        };
        let TrustedInputResolution::Resolved(snapshot) = resolution else {
            return BinaryAuthorizationDecision::Deny;
        };
        let authentication = ResolvedAuthenticationEvidence(
            snapshot
                .authentication_evidence
                .into_iter()
                .map(|evidence| AuthenticatedSessionEvidence {
                    evidence_ref: evidence.evidence_ref,
                    session_id: evidence.session_id,
                    trusted: evidence.trusted
                        && !evidence.revoked
                        && query.decision_time < evidence.expires_at,
                })
                .collect(),
        );
        let route_bindings = ResolvedRouteBindings(
            snapshot
                .route_bindings
                .into_iter()
                .map(|binding| RouteAuthorizationBinding {
                    route_id: binding.route_id,
                    required_permission: auth_foundation_runtime_adapter::Permission {
                        resource: binding.resource,
                        action: binding.action,
                        scope: binding.scope,
                    },
                    scope_evidence_ref: binding.scope_evidence_ref,
                    complete: binding.complete && binding.enabled,
                })
                .collect(),
        );
        TrustedAuthorizationBoundary::new(
            authentication,
            route_bindings,
            Downstream(&mut self.downstream),
        )
        .authorize(request)
    }
}

struct ResolvedAuthenticationEvidence(Vec<AuthenticatedSessionEvidence>);

impl AuthenticationEvidenceResolver for ResolvedAuthenticationEvidence {
    fn resolve_authentication_evidence(
        &self,
        _evidence_ref: &str,
    ) -> Result<Vec<AuthenticatedSessionEvidence>, PortFailure> {
        Ok(self.0.clone())
    }
}

struct ResolvedRouteBindings(Vec<RouteAuthorizationBinding>);

impl RouteAuthorizationBindingResolver for ResolvedRouteBindings {
    fn resolve_route_authorization_bindings(
        &self,
        _route_id: &str,
    ) -> Result<Vec<RouteAuthorizationBinding>, PortFailure> {
        Ok(self.0.clone())
    }
}

struct Downstream<'a, C>(&'a mut SqliteAuthorizationService<C>);

impl<C> AuthorizationDecisionService for Downstream<'_, C>
where
    C: DecisionClock,
{
    fn authorize(&mut self, command: AuthorizationCommand) -> BinaryAuthorizationDecision {
        self.0.authorize(command)
    }
}
