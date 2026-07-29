import { sourceAliases as S } from "./catalog.mjs";

function r(
  suffix,
  predicate,
  sourceSuffix,
  targetSuffix,
  source,
  selector,
  options = {},
) {
  return {
    suffix,
    predicate,
    sourceSuffix,
    targetSuffix,
    source,
    selector,
    direction: options.direction ?? "directed",
    owner: options.owner ?? "body-war.product-ontology-owner",
    authorityEffect: options.authorityEffect ?? "none",
    valueEffect: options.valueEffect ?? "value-free",
    cyclePolicy: options.cyclePolicy ?? "acyclic",
    forbidden:
      options.forbidden ??
      `Do not treat ${predicate} as implementation, runtime proof, lifecycle promotion, or authority transfer.`,
  };
}

const contextCapabilities = [
  ["identity-consent", "auth-consent"],
  ["activity-evidence", "activity-import"],
  ["activity-evidence", "evidence-submission"],
  ["territory-catalog", "track-territory-catalog"],
  ["control-competition", "control-ownership"],
  ["progression", "score-xp"],
  ["progression", "rankings-seasons"],
  ["community", "challenges-missions"],
  ["community", "community-clans"],
  ["pilot-operations", "notifications"],
  ["pilot-operations", "pilot-operations"],
  ["monetization-sponsored-zones", "sponsored-zones"],
  ["monetization-sponsored-zones", "economy"],
  ["route-expansion", "suggested-track-discovery"],
  ["route-expansion", "suggested-track-creation"],
  ["route-expansion", "evidence-candidate-attach"],
  ["geometry-evidence", "activity-geometry"],
  ["score-preview", "score-preview"],
].map(([context, capability], index) =>
  r(
    `context-${index + 1}`,
    "owns",
    `context.${context}`,
    `capability.${capability}`,
    S.capabilities,
    "Context-to-capability ownership",
  ),
);

const actorRelations = [
  r("runner-owns-provider", "owns", "actor.runner", "entity.provider-account", S.domain, "Runner and ProviderAccount"),
  r("runner-participates-community", "participates_in", "actor.runner", "context.community", S.definitions, "Runner"),
  r("runner-becomes-connected", "becomes", "actor.runner", "actor.connected-runner", S.journeyMap, "Business Relationships", { valueEffect: "value-constraining" }),
  r("visitor-authenticates", "participates_in", "actor.anonymous-visitor", "workflow.login-to-score-preview", S.journeySpec, "End-to-End Capability Map"),
  r("connected-proposes-track", "produces", "actor.connected-runner", "entity.suggested-track", S.journeyMap, "Business Relationships"),
  r("connected-confirms", "produces", "actor.connected-runner", "entity.runner-confirmation", S.journeyMap, "Business Relationships"),
  r("operator-reviews-evidence", "participates_in", "actor.prototype-operator", "operation.review-evidence", S.journeySpec, "Actors"),
  r("policy-owner-owns-score-policy", "owns", "actor.track-policy-owner", "policy.score-policy", S.journeySpec, "Actors", { valueEffect: "value-constraining" }),
  r("reviewer-validates-submission", "validates", "actor.anti-cheat-reviewer", "entity.evidence-submission", S.definitions, "Run Validation and Anti-Cheat"),
  r("owner-controls-territory", "controls", "actor.zone-owner", "entity.territory-unit", S.game, "Ownership and invasion", { valueEffect: "value-constraining" }),
  r("invader-contests-territory", "contests", "actor.invader", "entity.territory-unit", S.game, "Invasion", { valueEffect: "value-constraining" }),
  r("clan-member-defends", "defends", "actor.clan-member", "entity.territory-unit", S.operations, "OP-CONTROL-DEFEND", { valueEffect: "value-constraining" }),
  r("sponsor-participates-zone", "participates_in", "actor.sponsor-partner", "entity.sponsored-zone", S.game, "Sponsored zones"),
  r("strava-provides-activity", "provides", "external.strava", "entity.run-activity", S.journeySpec, "Actors"),
  r("strava-provides-geometry", "provides", "external.strava", "value.activity-geometry-sample", S.journeySpec, "ActivityGeometrySample", { authorityEffect: "blocked" }),
];

const capabilityDependencies = [
  ["activity-import", "auth-consent"],
  ["evidence-submission", "auth-consent"],
  ["evidence-submission", "activity-import"],
  ["control-ownership", "evidence-submission"],
  ["score-xp", "evidence-submission"],
  ["rankings-seasons", "score-xp"],
  ["notifications", "control-ownership"],
  ["pilot-operations", "evidence-submission"],
  ["suggested-track-discovery", "auth-consent"],
  ["suggested-track-creation", "auth-consent"],
  ["evidence-candidate-attach", "suggested-track-discovery"],
  ["evidence-candidate-attach", "activity-import"],
  ["activity-geometry", "evidence-candidate-attach"],
  ["activity-geometry", "auth-consent"],
  ["score-preview", "activity-geometry"],
  ["score-preview", "score-xp"],
].map(([source, target], index) =>
  r(
    `capability-dependency-${index + 1}`,
    "depends_on",
    `capability.${source}`,
    `capability.${target}`,
    S.capabilities,
    "Capability dependencies",
  ),
);

const objectRelations = [
  r("provider-belongs-runner", "owns", "actor.runner", "entity.provider-account", S.domain, "ProviderAccount"),
  r("provider-supports-activity", "supports", "entity.provider-account", "entity.run-activity", S.domain, "RunActivity"),
  r("activity-maps-redacted", "maps_to", "entity.run-activity", "value.redacted-activity-summary", S.mappings, "Strava Activity To RunActivity"),
  r("territory-contains-geometry", "contains", "entity.territory-unit", "value.track-geometry", S.domain, "TerritoryUnit"),
  r("submission-supports-territory", "supports", "entity.evidence-submission", "entity.territory-unit", S.domain, "EvidenceSubmission"),
  r("submission-records-status", "records", "entity.evidence-submission", "value.submission-status", S.states, "Submission State"),
  r("controller-projects-territory", "projects", "value.controller-state", "entity.territory-unit", S.domain, "ControllerState"),
  r("controller-governed-metric", "governed_by", "value.controller-state", "value.controller-metric", S.domain, "ControllerState", { valueEffect: "value-constraining" }),
  r("controller-records-basis", "records", "value.controller-state", "value.control-basis", S.domain, "ControllerState"),
  r("xp-ledger-records-xp", "records", "ledger.xp-ledger", "metric.profile-xp", S.domain, "XPLedger"),
  r("season-contains-ranking", "contains", "entity.season", "metric.seasonal-ranking", S.queries, "Q-RANKINGS"),
  r("challenge-awards-xp", "awards", "entity.challenge", "metric.profile-xp", S.operations, "OP-CHALLENGE-COMPLETE", { valueEffect: "value-constraining" }),
  r("clan-contains-member", "contains", "entity.clan", "actor.clan-member", S.operations, "OP-CLAN-JOIN"),
  r("invasion-contests-ownership", "contests", "entity.invasion", "entity.ownership-record", S.game, "Ownership and invasion", { valueEffect: "value-constraining" }),
  r("invasion-governed-defense-window", "governed_by", "entity.invasion", "value.defense-window", S.operations, "OP-CONTROL-OPEN-INVASION", { valueEffect: "value-constraining" }),
  r("sponsored-zone-maps-territory", "maps_to", "entity.sponsored-zone", "entity.territory-unit", S.game, "Sponsored zones"),
  r("suggested-track-supports-territory", "supports", "entity.suggested-track", "entity.territory-unit", S.suggestedSpec, "What This Module Owns"),
  r("candidate-supports-suggestion", "supports", "entity.activity-evidence-candidate", "entity.suggested-track", S.suggestedDomain, "ActivityEvidenceCandidate"),
  r("confirmation-produces-candidate", "produces", "entity.runner-confirmation", "entity.activity-evidence-candidate", S.journeyMap, "Business Relationships"),
  r("confirmation-governed-consent", "governed_by", "entity.runner-confirmation", "policy.consent-contract", S.journeySpec, "RunnerConfirmation", { valueEffect: "value-constraining" }),
  r("candidate-supports-geometry", "supports", "entity.activity-evidence-candidate", "entity.geometry-candidate", S.journeyMap, "Business Relationships"),
  r("geometry-consumes-sample", "consumes", "entity.geometry-candidate", "value.activity-geometry-sample", S.journeySpec, "GeometryCandidate"),
  r("geometry-supports-snapshot", "supports", "entity.geometry-candidate", "value.score-input-snapshot", S.journeyMap, "Business Relationships"),
  r("snapshot-governed-policy", "governed_by", "value.score-input-snapshot", "policy.score-policy", S.journeySpec, "ScoreInputSnapshot", { valueEffect: "value-constraining" }),
  r("snapshot-produces-preview", "produces", "value.score-input-snapshot", "outcome.score-preview", S.journeyMap, "Business Relationships"),
  r("preview-governed-policy", "governed_by", "outcome.score-preview", "policy.score-policy", S.journeyMap, "Business Relationships", { valueEffect: "value-constraining" }),
  r("preview-does-not-promote", "does_not_promote", "outcome.score-preview", "outcome.source-backed-track", S.journeyMap, "Business Relationships", { authorityEffect: "blocked", valueEffect: "value-constraining", forbidden: "A score preview cannot promote a SuggestedTrack, geometry, controller, or game authority." }),
  r("geometry-does-not-promote", "does_not_promote", "entity.geometry-candidate", "outcome.source-backed-track", S.journeyGlossary, "Source-backed", { authorityEffect: "blocked", valueEffect: "value-constraining", forbidden: "Candidate geometry cannot become source-backed without the operator-owned promotion path." }),
  r("zone-score-governed-policy", "governed_by", "metric.zone-score", "policy.score-policy", S.journeyGlossary, "Zone Score", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
  r("score-preview-projects-zone-score", "projects", "outcome.score-preview", "metric.zone-score", S.journeyGlossary, "ScorePreview", { authorityEffect: "projection", forbidden: "The preview may project score components but cannot assert Zone Score authority." }),
];

const operationRelations = [
  ["start-strava-oauth", "consumes", "actor.anonymous-visitor"],
  ["start-strava-oauth", "produces", "state.auth.anonymous"],
  ["complete-strava-oauth", "consumes", "entity.provider-account"],
  ["complete-strava-oauth", "produces", "event.provider-connected"],
  ["complete-strava-oauth", "changes_state_of", "state.auth.connected"],
  ["logout", "produces", "event.provider-access-revoked"],
  ["import-activities", "consumes", "entity.provider-account"],
  ["import-activities", "produces", "entity.run-activity"],
  ["import-activities", "produces", "event.activities-imported"],
  ["upsert-territory", "produces", "entity.territory-unit"],
  ["upsert-territory", "produces", "event.territory-published"],
  ["submit-evidence", "consumes", "entity.run-activity"],
  ["submit-evidence", "consumes", "entity.territory-unit"],
  ["submit-evidence", "produces", "entity.evidence-submission"],
  ["submit-evidence", "produces", "event.evidence-submitted"],
  ["auto-accept-preview-evidence", "consumes", "entity.evidence-submission"],
  ["auto-accept-preview-evidence", "produces", "event.evidence-preview-accepted"],
  ["review-evidence", "consumes", "entity.evidence-submission"],
  ["review-evidence", "produces", "event.evidence-verified"],
  ["review-evidence", "produces", "event.evidence-rejected"],
  ["compute-controller", "consumes", "entity.evidence-submission"],
  ["compute-controller", "produces", "value.controller-state"],
  ["compute-controller", "produces", "event.controller-updated"],
  ["open-invasion", "consumes", "entity.ownership-record"],
  ["open-invasion", "produces", "entity.invasion"],
  ["open-invasion", "produces", "event.invasion-opened"],
  ["defend-territory", "consumes", "entity.invasion"],
  ["defend-territory", "produces", "event.defense-succeeded"],
  ["calculate-zone-score", "consumes", "policy.score-policy"],
  ["calculate-zone-score", "produces", "metric.zone-score"],
  ["award-xp", "produces", "event.xp-awarded"],
  ["award-xp", "records", "ledger.xp-ledger"],
  ["join-challenge", "consumes", "entity.challenge"],
  ["complete-challenge", "produces", "event.challenge-completed"],
  ["create-clan", "produces", "entity.clan"],
  ["join-clan", "consumes", "entity.clan"],
  ["snapshot-season", "produces", "entity.ranking-snapshot"],
  ["snapshot-season", "produces", "event.season-snapshot-closed"],
  ["dispatch-notification", "produces", "entity.notification"],
  ["activate-sponsored-zone", "produces", "entity.sponsored-zone"],
  ["purchase-economy-item", "consumes", "value.runcoin"],
].map(([operation, predicate, target], index) =>
  r(
    `operation-${index + 1}`,
    predicate,
    `operation.${operation}`,
    target,
    S.operations,
    operation,
    {
      authorityEffect:
        operation === "calculate-zone-score" ||
        operation === "activate-sponsored-zone" ||
        operation === "purchase-economy-item"
          ? "blocked"
          : "none",
      valueEffect:
        ["changes_state_of", "records", "awards"].includes(predicate)
          ? "value-constraining"
          : "value-free",
    },
  ),
);

const suggestedAndJourneyOperations = [
  r("create-suggested-produces-track", "produces", "operation.create-suggested-track", "entity.suggested-track", S.suggestedOperations, "CreateSuggestedTrack"),
  r("attach-candidate-consumes-track", "consumes", "operation.attach-activity-evidence-candidate", "entity.suggested-track", S.suggestedOperations, "AttachActivityEvidenceCandidate"),
  r("attach-candidate-produces-candidate", "produces", "operation.attach-activity-evidence-candidate", "entity.activity-evidence-candidate", S.suggestedOperations, "AttachActivityEvidenceCandidate"),
  r("seed-produces-track", "produces", "operation.ensure-default-suggested-tracks", "entity.suggested-track", S.suggestedOperations, "EnsureDefaultSuggestedTracks"),
  r("authenticate-contains-start", "contains", "operation.authenticate-via-strava", "operation.start-strava-oauth", S.journeySpec, "AuthenticateViaStrava"),
  r("authenticate-contains-callback", "contains", "operation.authenticate-via-strava", "operation.complete-strava-oauth", S.journeySpec, "AuthenticateViaStrava"),
  r("select-reads-track", "reads", "operation.select-suggested-track", "entity.suggested-track", S.journeySpec, "SelectSuggestedTrack"),
  r("confirm-consumes-track", "consumes", "operation.confirm-track-with-activity", "entity.suggested-track", S.journeySpec, "ConfirmTrackWithActivity"),
  r("confirm-consumes-activity", "consumes", "operation.confirm-track-with-activity", "entity.run-activity", S.journeySpec, "ConfirmTrackWithActivity"),
  r("confirm-produces-confirmation", "produces", "operation.confirm-track-with-activity", "entity.runner-confirmation", S.journeySpec, "ConfirmTrackWithActivity"),
  r("confirm-produces-event", "produces", "operation.confirm-track-with-activity", "event.runner-confirmed-track-activity", S.journeySpec, "ConfirmTrackWithActivity"),
  r("fetch-geometry-consumes-confirmation", "consumes", "operation.fetch-selected-activity-geometry", "entity.runner-confirmation", S.journeySpec, "FetchSelectedActivityGeometry", { authorityEffect: "blocked" }),
  r("fetch-geometry-produces-sample", "produces", "operation.fetch-selected-activity-geometry", "value.activity-geometry-sample", S.journeySpec, "FetchSelectedActivityGeometry", { authorityEffect: "blocked" }),
  r("derive-consumes-sample", "consumes", "operation.derive-geometry-candidate", "value.activity-geometry-sample", S.journeySpec, "DeriveGeometryCandidate", { authorityEffect: "blocked" }),
  r("derive-produces-geometry", "produces", "operation.derive-geometry-candidate", "entity.geometry-candidate", S.journeySpec, "DeriveGeometryCandidate", { authorityEffect: "blocked" }),
  r("derive-produces-event", "produces", "operation.derive-geometry-candidate", "event.geometry-derived", S.journeySpec, "DeriveGeometryCandidate", { authorityEffect: "blocked" }),
  r("snapshot-consumes-geometry", "consumes", "operation.build-score-input-snapshot", "entity.geometry-candidate", S.journeySpec, "BuildScoreInputSnapshot", { authorityEffect: "blocked" }),
  r("snapshot-consumes-policy", "consumes", "operation.build-score-input-snapshot", "policy.score-policy", S.journeySpec, "BuildScoreInputSnapshot", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
  r("snapshot-produces-snapshot", "produces", "operation.build-score-input-snapshot", "value.score-input-snapshot", S.journeySpec, "BuildScoreInputSnapshot", { authorityEffect: "blocked" }),
  r("snapshot-produces-event", "produces", "operation.build-score-input-snapshot", "event.score-input-snapshotted", S.journeySpec, "BuildScoreInputSnapshot", { authorityEffect: "blocked" }),
  r("calculate-preview-consumes-snapshot", "consumes", "operation.calculate-score-preview", "value.score-input-snapshot", S.journeySpec, "CalculateScorePreview", { authorityEffect: "blocked" }),
  r("calculate-preview-consumes-policy", "consumes", "operation.calculate-score-preview", "policy.score-policy", S.journeySpec, "CalculateScorePreview", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
  r("calculate-preview-produces-preview", "produces", "operation.calculate-score-preview", "outcome.score-preview", S.journeySpec, "CalculateScorePreview", { authorityEffect: "blocked" }),
  r("calculate-preview-produces-event", "produces", "operation.calculate-score-preview", "event.score-preview-calculated", S.journeySpec, "CalculateScorePreview", { authorityEffect: "blocked" }),
  r("project-preview-reads-preview", "reads", "operation.project-score-preview", "outcome.score-preview", S.journeySpec, "ProjectScorePreview", { authorityEffect: "projection" }),
];

const queryTargets = [
  ["auth-status", "actor.connected-runner"],
  ["home-summary", "value.controller-state"],
  ["activity-list", "entity.run-activity"],
  ["track-list", "entity.territory-unit"],
  ["track-detail", "entity.territory-unit"],
  ["current-controller", "value.controller-state"],
  ["evidence-list", "entity.evidence-submission"],
  ["profile-summary", "metric.profile-xp"],
  ["active-challenges", "entity.challenge"],
  ["clan-summary", "entity.clan"],
  ["rankings", "metric.seasonal-ranking"],
  ["notifications", "entity.notification"],
  ["operator-queue", "entity.evidence-submission"],
].map(([query, target], index) =>
  r(`query-${index + 1}`, "reads", `query.${query}`, target, S.queries, query),
);

queryTargets.push(
  r("list-suggested-reads-track", "reads", "query.list-suggested-tracks", "entity.suggested-track", S.suggestedQueries, "ListSuggestedTracks"),
  r("detail-suggested-reads-track", "reads", "query.get-suggested-track-detail", "entity.suggested-track", S.suggestedQueries, "GetSuggestedTrackDetail"),
  r("detail-suggested-reads-candidate", "reads", "query.get-suggested-track-detail", "entity.activity-evidence-candidate", S.suggestedQueries, "GetSuggestedTrackDetail"),
  r("journey-query-reads-confirmation", "reads", "query.score-preview-journey", "entity.runner-confirmation", S.journeySpec, "API Surface", { authorityEffect: "projection" }),
  r("journey-query-reads-geometry", "reads", "query.score-preview-journey", "entity.geometry-candidate", S.journeySpec, "API Surface", { authorityEffect: "projection" }),
  r("journey-query-reads-preview", "reads", "query.score-preview-journey", "outcome.score-preview", S.journeySpec, "API Surface", { authorityEffect: "projection" }),
  r("latest-query-reads-preview", "reads", "query.latest-score-preview", "outcome.score-preview", S.journeySpec, "API Surface", { authorityEffect: "projection" }),
);

const workflowRelations = [
  ["run-to-control", "import-activities"],
  ["run-to-control", "submit-evidence"],
  ["run-to-control", "auto-accept-preview-evidence"],
  ["run-to-control", "review-evidence"],
  ["run-to-control", "compute-controller"],
  ["invasion-defense", "open-invasion"],
  ["invasion-defense", "defend-territory"],
  ["invasion-defense", "dispatch-notification"],
  ["seasonal-progression", "award-xp"],
  ["seasonal-progression", "snapshot-season"],
  ["suggested-track-expansion", "create-suggested-track"],
  ["suggested-track-expansion", "attach-activity-evidence-candidate"],
  ["login-to-score-preview", "authenticate-via-strava"],
  ["login-to-score-preview", "select-suggested-track"],
  ["login-to-score-preview", "confirm-track-with-activity"],
  ["login-to-score-preview", "fetch-selected-activity-geometry"],
  ["login-to-score-preview", "derive-geometry-candidate"],
  ["login-to-score-preview", "build-score-input-snapshot"],
  ["login-to-score-preview", "calculate-score-preview"],
  ["login-to-score-preview", "project-score-preview"],
].map(([workflow, operation], index) =>
  r(
    `workflow-${index + 1}`,
    "contains",
    `workflow.${workflow}`,
    `operation.${operation}`,
    workflow === "login-to-score-preview"
      ? S.journeySpec
      : workflow === "suggested-track-expansion"
        ? S.suggestedSpec
        : S.operations,
    workflow,
    {
      authorityEffect:
        workflow === "login-to-score-preview" &&
        [
          "fetch-selected-activity-geometry",
          "derive-geometry-candidate",
          "build-score-input-snapshot",
          "calculate-score-preview",
          "project-score-preview",
        ].includes(operation)
          ? "blocked"
          : "none",
    },
  ),
);

const stateTransitions = [
  ["auth-anonymous-connected", "state.auth.anonymous", "state.auth.connected", S.states],
  ["auth-connected-revoked", "state.auth.connected", "state.auth.revoked", S.states],
  ["submission-draft-submitted", "state.submission.draft", "state.submission.submitted", S.states],
  ["submission-submitted-preview", "state.submission.submitted", "state.submission.preview-accepted", S.states],
  ["submission-submitted-verified", "state.submission.submitted", "state.submission.verified", S.states],
  ["submission-submitted-rejected", "state.submission.submitted", "state.submission.rejected", S.states],
  ["controller-neutral-preview", "state.controller.neutral", "state.controller.preview-controlled", S.states],
  ["controller-neutral-verified", "state.controller.neutral", "state.controller.verified-controlled", S.states],
  ["controller-controlled-contested", "state.controller.verified-controlled", "state.controller.contested", S.states],
  ["challenge-available-active", "state.challenge.available", "state.challenge.active", S.states],
  ["challenge-active-complete", "state.challenge.active", "state.challenge.complete", S.states],
  ["challenge-complete-rewarded", "state.challenge.complete", "state.challenge.rewarded", S.states],
  ["season-preseason-active", "state.season.preseason", "state.season.active", S.states],
  ["season-active-closing", "state.season.active", "state.season.closing", S.states],
  ["season-closing-closed", "state.season.closing", "state.season.closed", S.states],
  ["suggested-needs-submitted", "state.suggested-track.needs-evidence", "state.suggested-track.evidence-submitted", S.suggestedStates],
  ["suggested-submitted-review", "state.suggested-track.evidence-submitted", "state.suggested-track.operator-review", S.suggestedStates],
  ["suggested-review-source-backed", "state.suggested-track.operator-review", "state.suggested-track.source-backed", S.suggestedStates],
  ["geometry-absent-fetch", "state.geometry-candidate.absent", "state.geometry-candidate.fetch-pending", S.journeyMap],
  ["geometry-fetch-derived", "state.geometry-candidate.fetch-pending", "state.geometry-candidate.derived-candidate", S.journeyMap],
  ["geometry-fetch-unavailable", "state.geometry-candidate.fetch-pending", "state.geometry-candidate.unavailable", S.journeyMap],
  ["score-unavailable-snapshot", "state.score-preview.unavailable", "state.score-preview.snapshot-pending", S.journeyMap],
  ["score-snapshot-calculation", "state.score-preview.snapshot-pending", "state.score-preview.calculation-pending", S.journeyMap],
  ["score-snapshot-incomplete", "state.score-preview.snapshot-pending", "state.score-preview.incomplete-projection", S.journeyMap],
  ["score-calculation-available", "state.score-preview.calculation-pending", "state.score-preview.available", S.journeyMap],
  ["score-calculation-failed", "state.score-preview.calculation-pending", "state.score-preview.failed", S.journeyMap],
].map(([id, source, target, ref]) =>
  r(id, "transitions_to", source, target, ref, "State transitions", {
    valueEffect: "value-constraining",
  }),
);

const interfaceRelations = [
  r("strava-interface-exposes-auth", "exposes", "interface.strava-provider-boundary", "operation.authenticate-via-strava", S.interfaces, "Strava Provider Boundary"),
  r("strava-interface-exposes-import", "exposes", "interface.strava-provider-boundary", "operation.import-activities", S.interfaces, "Strava Provider Boundary"),
  r("http-exposes-auth-query", "exposes", "interface.http-api", "query.auth-status", S.interfaces, "HTTP Interface Table"),
  r("http-exposes-track-query", "exposes", "interface.http-api", "query.track-list", S.interfaces, "HTTP Interface Table"),
  r("http-exposes-submit", "exposes", "interface.http-api", "operation.submit-evidence", S.interfaces, "HTTP Interface Table"),
  r("suggested-api-exposes-list", "exposes", "interface.suggested-track-api", "query.list-suggested-tracks", S.suggestedInterfaces, "SuggestedTrack API"),
  r("suggested-api-exposes-create", "exposes", "interface.suggested-track-api", "operation.create-suggested-track", S.suggestedInterfaces, "SuggestedTrack API"),
  r("suggested-api-exposes-attach", "exposes", "interface.suggested-track-api", "operation.attach-activity-evidence-candidate", S.suggestedInterfaces, "SuggestedTrack API"),
  r("journey-api-exposes-workflow", "exposes", "interface.score-preview-journey-api", "workflow.login-to-score-preview", S.journeySpec, "API Surface", { authorityEffect: "blocked" }),
  r("journey-api-exposes-query", "exposes", "interface.score-preview-journey-api", "query.score-preview-journey", S.journeySpec, "API Surface", { authorityEffect: "projection" }),
];

const policyRelations = [
  r("preview-policy-governs-autoaccept", "governed_by", "operation.auto-accept-preview-evidence", "policy.preview-evidence", S.operations, "OP-EVIDENCE-AUTO-ACCEPT", { valueEffect: "value-constraining" }),
  r("controller-governed-selection", "governed_by", "operation.compute-controller", "policy.controller-selection", S.operations, "OP-CONTROL-COMPUTE", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
  r("geometry-governed-privacy", "governed_by", "operation.derive-geometry-candidate", "policy.geometry-privacy", S.journeySpec, "DeriveGeometryCandidate", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
  r("confirm-operation-governed-consent", "governed_by", "operation.confirm-track-with-activity", "policy.consent-contract", S.journeySpec, "ConfirmTrackWithActivity", { valueEffect: "value-constraining" }),
  r("submission-governed-anticheat", "governed_by", "operation.review-evidence", "policy.anti-cheat", S.game, "Anti-cheat", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
  r("ownership-governed-caducity", "governed_by", "entity.ownership-record", "policy.caducity", S.game, "Caducity", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
  r("invasion-governed-eligibility", "governed_by", "entity.invasion", "policy.ownership-eligibility", S.game, "Ownership and invasion", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
  r("notification-governed-privacy", "governed_by", "operation.dispatch-notification", "policy.notification-privacy", S.operations, "OP-NOTIFY-DISPATCH", { valueEffect: "value-constraining" }),
  r("snapshot-governed-history", "governed_by", "operation.build-score-input-snapshot", "policy.score-history", S.journeySpec, "BuildScoreInputSnapshot", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
  r("snapshot-governed-eligibility", "governed_by", "operation.build-score-input-snapshot", "policy.activity-eligibility", S.journeySpec, "BuildScoreInputSnapshot", { authorityEffect: "blocked", valueEffect: "value-constraining" }),
];

export const relations = [
  ...contextCapabilities,
  ...actorRelations,
  ...capabilityDependencies,
  ...objectRelations,
  ...operationRelations,
  ...suggestedAndJourneyOperations,
  ...queryTargets,
  ...workflowRelations,
  ...stateTransitions,
  ...interfaceRelations,
  ...policyRelations,
];
