const S = {
  overview: "projects/body-war/docs/PROJECT-OVERVIEW.md",
  definitions: "projects/body-war/docs/INITIAL-DEFINITIONS.md",
  hypotheses: "projects/body-war/docs/HYPOTHESES.md",
  decisions: "projects/body-war/docs/PROJECT-DECISIONS.md",
  glossary: "projects/body-war/docs/glossary.md",
  registry: "projects/body-war/docs/registry.md",
  game: "projects/body-war/docs/features/game-rules/SPEC.md",
  architecture:
    "projects/body-war/docs/features/troqar-product-architecture/SPEC.md",
  capabilities:
    "projects/body-war/docs/features/troqar-product-architecture/OPERATIONS-CAPABILITIES.md",
  domain:
    "projects/body-war/docs/features/troqar-product-architecture/domain.md",
  operations:
    "projects/body-war/docs/features/troqar-product-architecture/operations.md",
  queries:
    "projects/body-war/docs/features/troqar-product-architecture/queries.md",
  states:
    "projects/body-war/docs/features/troqar-product-architecture/states.md",
  events:
    "projects/body-war/docs/features/troqar-product-architecture/events.md",
  interfaces:
    "projects/body-war/docs/features/troqar-product-architecture/interfaces.md",
  mappings:
    "projects/body-war/docs/features/troqar-product-architecture/mappings.md",
  strava:
    "projects/body-war/docs/features/strava-linked-pilot/SPEC.md",
  suggestedSpec:
    "projects/body-war/docs/features/parque-taquaral-online-mvp/SPEC.md",
  suggestedDomain:
    "projects/body-war/docs/features/parque-taquaral-online-mvp/domain.md",
  suggestedOperations:
    "projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md",
  suggestedQueries:
    "projects/body-war/docs/features/parque-taquaral-online-mvp/queries.md",
  suggestedStates:
    "projects/body-war/docs/features/parque-taquaral-online-mvp/states.md",
  suggestedInterfaces:
    "projects/body-war/docs/features/parque-taquaral-online-mvp/interfaces.md",
  journeySpec:
    "projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/SPEC.md",
  journeyMap:
    "projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/ONTOLOGY-MAP.md",
  journeyGlossary:
    "projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/GLOSSARY.md",
};

function n(
  suffix,
  label,
  definition,
  businessKind,
  conceptRole,
  source,
  selector,
  options = {},
) {
  const status = options.status ?? "reviewed-candidate";
  const owner = options.owner ?? "body-war.product-ontology-owner";
  const evidenceConfidence = options.evidenceConfidence ?? "high";
  const commitmentConfidence =
    options.commitmentConfidence ??
    (status === "blocked" || status === "deferred" ? "low" : "high");
  const blockingQuestions = options.blockingQuestions ?? [];
  const residue = options.residue ?? [];
  const nextGate =
    options.nextGate ??
    (status === "blocked"
      ? "decision-gate"
      : status === "deferred"
        ? "body-war.product-scope-review"
        : "body-war.product-ontology-review");

  return {
    suffix,
    label,
    definition,
    businessKind,
    conceptRole,
    source,
    selector,
    status,
    owner,
    evidenceConfidence,
    commitmentConfidence,
    basis:
      options.basis ??
      `The named Body War source explicitly declares ${label}; ontology status does not add runtime or authority evidence.`,
    challengeResponse:
      options.challengeResponse ??
      "Re-open the cited selector, compare the claim with current product decisions and receipts, then route any semantic or ownership conflict to the named owner.",
    blockingQuestions,
    nextGate,
    residue,
    forbidden:
      options.forbidden ??
      `Do not collapse ${label} into implementation, runtime proof, lifecycle promotion, or release authority.`,
  };
}

const actors = [
  n("actor.anonymous-visitor", "Anonymous Visitor", "A person without a Body War session who may understand the entry point and begin Strava authorization.", "actor", "authority object", S.journeySpec, "Actors"),
  n("actor.runner", "Runner", "A person using Body War to turn running activity into game evidence, progression, and community participation.", "actor", "authority object", S.definitions, "Runner"),
  n("actor.connected-runner", "Connected Runner", "A runner with an active Body War browser session and a linked Strava provider account.", "actor", "authority object", S.journeyGlossary, "Connected Runner"),
  n("actor.zone-owner", "Zone Owner", "A runner or eligible clan currently represented as controlling a territory under a declared controller basis.", "actor", "authority object", S.game, "Ownership and invasion"),
  n("actor.invader", "Invader", "A runner submitting eligible evidence to challenge current territory control.", "actor", "authority object", S.game, "Invasion"),
  n("actor.clan-member", "Clan Member", "A runner with one active clan membership who may contribute or defend under clan policy.", "actor", "authority object", S.operations, "OP-CLAN-JOIN"),
  n("actor.prototype-operator", "Prototype Operator", "An operator who configures prototype fixtures and witnesses without gaining route or score promotion authority.", "actor", "workflow object", S.journeySpec, "Actors"),
  n("actor.track-policy-owner", "Track and Policy Owner", "The owner required to ratify score normalization and later route promotion rules.", "actor", "authority object", S.journeySpec, "Actors", { owner: "body-war.track-policy-owner" }),
  n("actor.anti-cheat-reviewer", "Anti-Cheat Reviewer", "An operator role that reviews evidence anomalies and validation residue before verified use.", "actor", "workflow object", S.definitions, "Run Validation and Anti-Cheat"),
  n("actor.sponsor-partner", "Sponsor Partner", "A deferred partner role associated with sponsored zones and activation rules.", "actor", "authority object", S.capabilities, "CAP-SPONSOR", { status: "deferred" }),
  n("actor.city-community-operator", "City or Community Operator", "A deferred local operator role for city rollout, community governance, or park operations.", "actor", "authority object", S.definitions, "Pilot Operations", { status: "deferred" }),
  n("actor.product-team", "Body War Product Team", "The team that owns product scope, declared contracts, and the route to implementation decisions.", "actor", "authority object", S.overview, "Project Shape"),
  n("external.strava", "Strava", "The external provider of identity, redacted activity data, detailed activity, and permitted streams; it is not Body War lifecycle authority.", "external_system", "evidence object", S.journeySpec, "Actors", { forbidden: "Do not treat Strava provider data as Body War route, score, control, or promotion authority." }),
];

const contexts = [
  ["identity-consent", "Identity and Consent", "Owns runner identity, provider connection, browser session, consent, and privacy boundaries."],
  ["activity-evidence", "Activity Evidence", "Owns redacted run summaries and submitted activity evidence."],
  ["territory-catalog", "Territory Catalog", "Owns tracks, territory metadata, geometry posture, and route discovery."],
  ["control-competition", "Control and Competition", "Owns controller projections, invasion, defense, and control basis."],
  ["progression", "Progression", "Owns profile XP, leagues, badges, streaks, and ranking contributions."],
  ["community", "Community", "Owns clans, memberships, community contribution, and social competition."],
  ["pilot-operations", "Pilot Operations", "Owns operator review, prototype health, and supervised pilot workflows."],
  ["run-validation-anti-cheat", "Run Validation and Anti-Cheat", "Owns evidence eligibility, review, rejection, and anti-cheat policy."],
  ["monetization-sponsored-zones", "Monetization and Sponsored Zones", "Deferred context for RunCoins, premium, sponsor activation, and sponsored territory.", { status: "deferred" }],
  ["route-expansion", "Suggested Track Route Expansion", "Owns runner-created route suggestions and consented candidate evidence without source-backed promotion.", { source: S.suggestedSpec }],
  ["geometry-evidence", "Candidate Geometry Evidence", "Candidate context for ephemeral provider streams and private activity-derived geometry.", { source: S.journeySpec, status: "candidate", evidenceConfidence: "medium", commitmentConfidence: "medium" }],
  ["score-preview", "Score Preview", "Candidate context for canonical score inputs and non-authoritative explained score projections.", { source: S.journeySpec, status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["Which complete ScorePolicy normalizers, window identity, eligibility, aggregation, and rounding rules does the owner ratify?"] }],
].map(([id, label, definition, options = {}]) =>
  n(`context.${id}`, label, definition, "bounded_context", "authority object", options.source ?? S.definitions, label, options),
);

const capabilities = [
  ["auth-consent", "Authentication and Consent", "Connect a runner, preserve provider token custody, establish session/CSRF, and expose privacy state.", "Identity and Consent"],
  ["activity-import", "Activity Import", "Fetch UI-safe redacted run activity summaries under the connected runner session.", "Activity Evidence"],
  ["track-territory-catalog", "Track and Territory Catalog", "Publish and query territory metadata with honest geometry posture.", "Territory Catalog"],
  ["evidence-submission", "Evidence Submission", "Submit one owned run activity as evidence for one territory.", "Activity Evidence"],
  ["control-ownership", "Control and Ownership", "Compute controller state and manage invasion/defense transitions.", "Control and Competition"],
  ["score-xp", "Score and XP", "Calculate score under declared rules and append progression awards.", "Progression"],
  ["challenges-missions", "Challenges and Missions", "Enroll runners, track criteria, complete missions, and grant rewards.", "Community"],
  ["community-clans", "Community and Clans", "Create clans, manage membership, and project group contribution.", "Community"],
  ["rankings-seasons", "Rankings and Seasons", "Project rankings and close immutable seasonal snapshots.", "Progression"],
  ["notifications", "Notifications", "Dispatch privacy-safe domain-event notifications.", "Pilot Operations"],
  ["pilot-operations", "Pilot Operations Capability", "Review evidence and monitor pilot health without inflating preview evidence.", "Pilot Operations"],
  ["sponsored-zones", "Sponsored Zones", "Activate sponsored territory and sponsor-specific rules.", "Monetization", { status: "deferred" }],
  ["economy", "RunCoin and Premium Economy", "Purchase or spend game currency and premium benefits.", "Monetization", { status: "deferred" }],
].map(([id, label, definition, selector, options = {}]) =>
  n(`capability.${id}`, label, definition, "capability", "authority object", S.capabilities, selector, options),
);

capabilities.push(
  n("capability.suggested-track-discovery", "Suggested Track Discovery", "Show active route suggestions to connected runners with honest evidence and geometry posture.", "capability", "authority object", S.suggestedSpec, "Capabilities"),
  n("capability.suggested-track-creation", "Suggested Track Creation", "Allow a connected runner to propose a route that begins in needs_evidence.", "capability", "authority object", S.suggestedSpec, "Capabilities"),
  n("capability.evidence-candidate-attach", "Evidence Candidate Attachment", "Attach one consented redacted activity summary to one SuggestedTrack for later review.", "capability", "authority object", S.suggestedSpec, "Capabilities"),
  n("capability.activity-geometry", "Selected Activity Geometry", "Fetch one confirmed activity's streams ephemerally and derive private candidate geometry.", "capability", "workflow object", S.journeySpec, "FetchSelectedActivityGeometry", { status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["Which private-geometry filter, precision, retention, and deletion policy is ratified?"] }),
  n("capability.score-preview", "Explained Score Preview", "Build a canonical score input and calculate an explained preview under an exact policy.", "capability", "projection object", S.journeySpec, "CalculateScorePreview", { status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["Which complete ScorePolicy is ratified?"] }),
);

const objects = [
  n("entity.provider-account", "ProviderAccount", "A server-custodied link between a Runner and an external provider account.", "entity", "authority object", S.domain, "ProviderAccount"),
  n("entity.run-activity", "RunActivity", "A UI-safe redacted summary of one provider activity that may be evaluated for evidence eligibility.", "entity", "evidence object", S.domain, "RunActivity"),
  n("entity.territory-unit", "TerritoryUnit", "A controllable route, loop, segment, or later zone with metadata and geometry posture.", "entity", "authority object", S.domain, "TerritoryUnit"),
  n("value.track-geometry", "TrackGeometry", "A route shape plus provenance and validation posture; its authority must be stated independently.", "value_object", "evidence object", S.domain, "TrackGeometry"),
  n("entity.evidence-submission", "EvidenceSubmission", "One runner-owned activity submitted as evidence for one territory with an auditable status.", "entity", "evidence object", S.domain, "EvidenceSubmission"),
  n("value.controller-state", "ControllerState", "A read model naming current controller, basis, metric, and source submission for one territory.", "value_object", "projection object", S.domain, "ControllerState"),
  n("metric.zone-score", "Zone Score", "The broader draft game metric weighted by pace, distance, and frequency with a displayed cap of 550.", "metric", "authority object", S.game, "Zone Score", { status: "blocked", owner: "body-war.score-policy-owner", blockingQuestions: ["What normalizers and aggregation rules define each component?", "Does Zone Score or fastest verified time decide control?"] }),
  n("ledger.xp-ledger", "XP Ledger", "An append-oriented record of profile XP grants tied to source domain events.", "ledger", "evidence object", S.domain, "XPLedger"),
  n("entity.clan", "Clan", "A named active community group with leadership, membership, and contribution rules.", "entity", "authority object", S.domain, "Clan"),
  n("entity.season", "Season", "A bounded ranking period whose closed snapshot is immutable while permanent progression persists.", "entity", "authority object", S.domain, "Season"),
  n("entity.challenge", "Challenge", "An eligibility-bound mission with enrollment, progress, completion evidence, and rewards.", "entity", "authority object", S.operations, "OP-CHALLENGE-JOIN"),
  n("entity.notification", "Notification", "A privacy-safe message caused by a cited domain event and routed to an eligible recipient.", "entity", "projection object", S.operations, "OP-NOTIFY-DISPATCH"),
  n("entity.ranking-snapshot", "Ranking Snapshot", "An immutable closing record of runner and clan standings for a season.", "entity", "evidence object", S.operations, "OP-SEASON-SNAPSHOT"),
  n("entity.suggested-track", "SuggestedTrack", "A runner-visible proposed route awaiting evidence and separate source-backed promotion.", "entity", "authority object", S.suggestedDomain, "SuggestedTrack", { forbidden: "Do not collapse SuggestedTrack existence or attached evidence into source-backed geometry, pilot readiness, or territory authority." }),
  n("entity.activity-evidence-candidate", "ActivityEvidenceCandidate", "A consenting runner's redacted Strava activity summary attached to one SuggestedTrack for later review.", "entity", "evidence object", S.suggestedDomain, "ActivityEvidenceCandidate"),
  n("entity.runner-confirmation", "RunnerConfirmation", "The affirmative binding of one authenticated runner, one SuggestedTrack, one owned activity, and one exact geometry-use consent contract.", "entity", "evidence object", S.journeySpec, "RunnerConfirmation", { status: "candidate", evidenceConfidence: "medium", commitmentConfidence: "medium", forbidden: "Do not collapse runner confirmation into operator acceptance, route promotion, or verified evidence." }),
  n("value.activity-geometry-sample", "ActivityGeometrySample", "Ephemeral aligned latlng, distance, and time streams fetched for one confirmed owned activity.", "value_object", "evidence object", S.journeySpec, "ActivityGeometrySample", { status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["Is the selected Strava scope and geometry-use consent contract ratified?"] }),
  n("entity.geometry-candidate", "GeometryCandidate", "A normalized privacy-filtered route geometry derived from consented activity data and retained as principal-private candidate evidence.", "entity", "evidence object", S.journeySpec, "GeometryCandidate", { status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["Which privacy filter, precision, retention, and deletion policy is ratified?"], forbidden: "Do not collapse candidate_from_activity into source-backed or public route geometry." }),
  n("policy.score-policy", "ScorePolicy", "A versioned calculation contract for component maxima, normalizers, caps, window, eligibility, aggregation, rounding, and missing data.", "policy", "authority object", S.journeySpec, "ScorePolicy", { status: "blocked", owner: "body-war.score-policy-owner", evidenceConfidence: "medium", blockingQuestions: ["Which ScorePolicy version and complete parameters does the owner ratify?"], forbidden: "Do not implement numeric score output from weights alone or treat a candidate policy as adopted." }),
  n("value.score-input-snapshot", "ScoreInputSnapshot", "An immutable canonical policy-window input binding derived activity metrics, geometry, policy, provenance, and history completeness.", "value_object", "evidence object", S.journeySpec, "ScoreInputSnapshot", { status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["What is the ratified real-history acquisition and consent scope?"] }),
  n("outcome.score-preview", "ScorePreview", "An explained non-authoritative numeric or partial projection produced from one exact policy and canonical score input.", "outcome", "projection object", S.journeySpec, "ScorePreview", { status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["Is a complete ScorePolicy available?", "Is the ScoreInputSnapshot complete_window or single_activity_projection?"], forbidden: "Do not collapse ScorePreview into Zone Score authority, verified scoring, controller verdict, or conquest." }),
  n("outcome.source-backed-track", "Source-Backed Track", "A SuggestedTrack whose source or geometry evidence has been accepted by an operator-owned promotion path.", "outcome", "authority object", S.journeyGlossary, "Source-backed", { status: "deferred", owner: "body-war.track-policy-owner" }),
  n("value.redacted-activity-summary", "Redacted Activity Summary", "Provider activity identity and performance summary excluding tokens, raw maps, notes, and private payloads.", "value_object", "evidence object", S.mappings, "Strava Activity To RunActivity"),
  n("value.submission-status", "Submission Status", "The independent lifecycle status draft, submitted, preview-accepted, verified, or rejected.", "value_object", "authority object", S.states, "Submission State"),
  n("value.geometry-status", "Geometry Status", "The independent geometry evidence posture missing, placeholder, draft, source-backed, or validated.", "value_object", "authority object", S.states, "Geometry State"),
  n("value.controller-metric", "Controller Metric", "The named comparison metric used to choose a controller, with its basis recorded.", "value_object", "authority object", S.domain, "ControllerState", { status: "blocked", blockingQuestions: ["Does the pilot use fastest verified time or a ratified Zone Score for control?"] }),
  n("value.control-basis", "Control Basis", "The declared evidence basis preview, verified, or manual attached to public controller projections.", "value_object", "evidence object", S.events, "Event Payload Rules"),
  n("value.zone-type", "Zone Type", "A classification such as common or strategic that may affect defense windows and game rules.", "value_object", "authority object", S.game, "Zone types"),
  n("value.reference-time", "Reference Time", "A route time used as a declared comparison reference under the selected validation policy.", "value_object", "authority object", S.game, "Reference time"),
  n("entity.invasion", "Invasion", "A contested-control episode opened by eligible evidence against an owned territory.", "entity", "workflow object", S.operations, "OP-CONTROL-OPEN-INVASION"),
  n("entity.ownership-record", "Ownership Record", "An auditable event-backed statement of territory controller, basis, and effective period.", "entity", "evidence object", S.game, "Ownership and invasion"),
  n("value.defense-window", "Defense Window", "The bounded response interval for an owner or eligible clan member after an invasion opens.", "value_object", "authority object", S.operations, "OP-CONTROL-OPEN-INVASION"),
  n("value.activity-sport-type", "Activity Sport Type", "The provider activity type used to admit only run-like evidence under policy.", "value_object", "authority object", S.mappings, "Strava Activity To RunActivity"),
  n("value.privacy-consent", "Privacy Consent", "A versioned exact statement affirmatively accepted before redacted evidence or geometry use.", "value_object", "authority object", S.journeySpec, "RunnerConfirmation", { status: "candidate", evidenceConfidence: "medium", commitmentConfidence: "medium" }),
  n("value.league", "League", "A progression tier used to group or display runner ranking.", "value_object", "projection object", S.game, "League"),
  n("value.badge", "Badge", "A persistent progression reward earned through declared conditions.", "value_object", "projection object", S.game, "Badge"),
  n("value.runcoin", "RunCoin", "A deferred game currency whose earning, spending, and purchase rules are unresolved.", "value_object", "authority object", S.game, "RunCoins", { status: "deferred" }),
  n("entity.sponsored-zone", "Sponsored Zone", "A deferred territory with sponsor-specific activation and rules.", "entity", "authority object", S.game, "Sponsored zones", { status: "deferred" }),
  n("metric.profile-xp", "Profile XP", "Permanent profile progression points awarded from cited domain events.", "metric", "projection object", S.operations, "OP-XP-AWARD"),
  n("metric.seasonal-ranking", "Seasonal Ranking", "A season-bounded ordering derived from declared runner and clan contributions.", "metric", "projection object", S.queries, "Q-RANKINGS"),
];

const operationSpecs = [
  ["start-strava-oauth", "Start Strava OAuth", "Begins provider authorization and records a signed one-use state.", "OP-AUTH-START-STRAVA"],
  ["complete-strava-oauth", "Complete Strava OAuth", "Verifies callback state, exchanges code server-side, links provider account, and establishes session/CSRF.", "OP-AUTH-CALLBACK"],
  ["logout", "Logout", "Revokes the Body War session and records provider-access or privacy state as applicable.", "OP-AUTH-LOGOUT"],
  ["import-activities", "Import Activities", "Fetches recent redacted run-like activity summaries with token refresh and honest empty/error states.", "OP-ACT-REFRESH"],
  ["upsert-territory", "Upsert Territory", "Publishes territory metadata and geometry status with audit notes and honest claims.", "OP-TRACK-UPSERT"],
  ["submit-evidence", "Submit Evidence", "Submits one runner-owned activity as evidence for one existing territory.", "OP-EVIDENCE-SUBMIT"],
  ["auto-accept-preview-evidence", "Auto-Accept Preview Evidence", "Marks submitted evidence preview-accepted without writing verified.", "OP-EVIDENCE-AUTO-ACCEPT"],
  ["review-evidence", "Review Evidence", "Allows an operator to verify or reject submitted evidence with basis, reviewer, and reason.", "OP-OPERATOR-REVIEW"],
  ["compute-controller", "Compute Controller", "Computes the current controller projection with named metric, basis, and source submission.", "OP-CONTROL-COMPUTE"],
  ["open-invasion", "Open Invasion", "Opens contested state for an owned territory after eligible evidence.", "OP-CONTROL-OPEN-INVASION"],
  ["defend-territory", "Defend Territory", "Allows an eligible owner or clan member to respond during the defense window.", "OP-CONTROL-DEFEND"],
  ["calculate-zone-score", "Calculate Zone Score", "Calculates the broader game score once the complete policy is ratified.", "OP-SCORE-CALCULATE", { status: "blocked", owner: "body-war.score-policy-owner", blockingQuestions: ["What complete Zone Score normalizers and authority rule are ratified?"] }],
  ["award-xp", "Award XP", "Appends profile XP tied to a cited source domain event.", "OP-XP-AWARD"],
  ["join-challenge", "Join Challenge", "Enrolls an eligible runner in an active challenge.", "OP-CHALLENGE-JOIN"],
  ["complete-challenge", "Complete Challenge", "Accepts completion evidence and emits progression or reward events.", "OP-CHALLENGE-COMPLETE"],
  ["create-clan", "Create Clan", "Creates a unique active clan and assigns its creator as leader.", "OP-CLAN-CREATE"],
  ["join-clan", "Join Clan", "Adds a runner to one active clan subject to capacity policy.", "OP-CLAN-JOIN"],
  ["snapshot-season", "Snapshot Season", "Closes a ranking cycle into an immutable season snapshot.", "OP-SEASON-SNAPSHOT"],
  ["dispatch-notification", "Dispatch Notification", "Sends a privacy-safe message citing its source domain event.", "OP-NOTIFY-DISPATCH"],
  ["activate-sponsored-zone", "Activate Sponsored Zone", "Activates sponsor-specific territory rules.", "OP-SPONSOR-ACTIVATE", { status: "deferred" }],
  ["purchase-economy-item", "Purchase Economy Item", "Purchases RunCoin or premium value under an adopted economy policy.", "OP-ECONOMY-PURCHASE", { status: "deferred" }],
].map(([id, label, definition, selector, options = {}]) =>
  n(`operation.${id}`, label, definition, "operation", "workflow object", S.operations, selector, options),
);

operationSpecs.push(
  n("operation.create-suggested-track", "Create SuggestedTrack", "Creates a connected-runner route suggestion in needs_evidence without geometry or pilot-ready claims.", "operation", "workflow object", S.suggestedOperations, "CreateSuggestedTrack"),
  n("operation.attach-activity-evidence-candidate", "Attach ActivityEvidenceCandidate", "Validates explicit consent and persists one redacted activity summary against one SuggestedTrack.", "operation", "workflow object", S.suggestedOperations, "AttachActivityEvidenceCandidate"),
  n("operation.ensure-default-suggested-tracks", "Ensure Default SuggestedTracks", "Idempotently seeds the Volta do Taquaral candidate as data rather than a UI branch.", "operation", "workflow object", S.suggestedOperations, "EnsureDefaultSuggestedTracks"),
  n("operation.authenticate-via-strava", "Authenticate Via Strava", "Orchestrates OAuth start/callback, accepted scope, provider binding, session, and CSRF for the prototype.", "operation", "workflow object", S.journeySpec, "AuthenticateViaStrava"),
  n("operation.select-suggested-track", "Select SuggestedTrack", "Carries one exact runner-selected suggestion into activity selection and consent.", "operation", "workflow object", S.journeySpec, "SelectSuggestedTrack", { status: "candidate", evidenceConfidence: "medium", commitmentConfidence: "medium" }),
  n("operation.confirm-track-with-activity", "Confirm Track With Activity", "Validates exact track, current owned activity, consent version/text, and geometry-use affirmation before attaching evidence.", "operation", "workflow object", S.journeySpec, "ConfirmTrackWithActivity", { status: "candidate", evidenceConfidence: "medium", commitmentConfidence: "medium" }),
  n("operation.fetch-selected-activity-geometry", "Fetch Selected Activity Geometry", "Fetches aligned latlng, distance, and time streams for one confirmed owned activity and keeps raw data ephemeral.", "operation", "workflow object", S.journeySpec, "FetchSelectedActivityGeometry", { status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["Is geometry-use scope and privacy policy ratified?"] }),
  n("operation.derive-geometry-candidate", "Derive GeometryCandidate", "Validates, privacy-filters, simplifies, digests, and persists principal-private candidate geometry.", "operation", "workflow object", S.journeySpec, "DeriveGeometryCandidate", { status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["Which geometry filter, precision, retention, and deletion rules apply?"] }),
  n("operation.build-score-input-snapshot", "Build ScoreInputSnapshot", "Canonically orders policy-eligible derived metrics and binds geometry, policy, provenance, and history completeness.", "operation", "workflow object", S.journeySpec, "BuildScoreInputSnapshot", { status: "blocked", evidenceConfidence: "medium", owner: "body-war.score-policy-owner", blockingQuestions: ["Which complete policy and history contract apply?"] }),
  n("operation.calculate-score-preview", "Calculate ScorePreview", "Consumes one canonical snapshot and one exact ratified policy to emit comparable or explicitly partial components.", "operation", "workflow object", S.journeySpec, "CalculateScorePreview", { status: "blocked", evidenceConfidence: "medium", owner: "body-war.score-policy-owner", blockingQuestions: ["Is ScorePolicy ratified and snapshot history complete?"] }),
  n("operation.project-score-preview", "Project ScorePreview", "Shows an authenticated runner preliminary components, policy, evidence mode, geometry posture, and limitations.", "operation", "projection object", S.journeySpec, "ProjectScorePreview", { status: "blocked", evidenceConfidence: "medium" }),
);

const querySpecs = [
  ["auth-status", "Auth Status Query", "Returns provider configuration, authentication, connection, athlete summary, and scope.", "Q-AUTH-STATUS"],
  ["home-summary", "Home Summary Query", "Composes auth, weekly distance, challenge, featured route, controller, and next action.", "Q-HOME-SUMMARY"],
  ["activity-list", "Activity List Query", "Returns redacted activity summaries, provider status, and honest empty reason.", "Q-ACT-LIST"],
  ["track-list", "Track List Query", "Returns track cards, geometry status, and controller metric.", "Q-TRACK-LIST"],
  ["track-detail", "Track Detail Query", "Returns territory, geometry, controller, leaderboard, eligible activities, and submit state.", "Q-TRACK-DETAIL"],
  ["current-controller", "Current Controller Query", "Returns controller, basis, metric, and last accepted evidence.", "Q-CONTROL-CURRENT"],
  ["evidence-list", "Evidence List Query", "Returns submissions, status, and audit state to authorized consumers.", "Q-EVIDENCE-LIST"],
  ["profile-summary", "Profile Summary Query", "Returns XP, league, badges, streak, clan, privacy, and provider state.", "Q-PROFILE-SUMMARY"],
  ["active-challenges", "Active Challenges Query", "Returns missions, progress, rewards, and enrollment.", "Q-CHALLENGE-ACTIVE"],
  ["clan-summary", "Clan Summary Query", "Returns current clan, members, contribution, and alerts.", "Q-CLAN-SUMMARY"],
  ["rankings", "Rankings Query", "Returns season and league runner/clan rankings.", "Q-RANKINGS"],
  ["notifications", "Notifications Query", "Returns privacy-safe messages, unread count, and action links.", "Q-NOTIFICATIONS"],
  ["operator-queue", "Operator Queue Query", "Returns pending submissions, review decisions, and health warnings.", "Q-OPERATOR-QUEUE"],
].map(([id, label, definition, selector]) =>
  n(`query.${id}`, label, definition, "query", "projection object", S.queries, selector),
);

querySpecs.push(
  n("query.list-suggested-tracks", "List SuggestedTracks", "Returns active route suggestions with honest evidence and geometry posture to a connected runner.", "query", "projection object", S.suggestedQueries, "ListSuggestedTracks"),
  n("query.get-suggested-track-detail", "Get SuggestedTrack Detail", "Returns one suggestion, the current runner's redacted candidates, and non-authoritative evidence summary.", "query", "projection object", S.suggestedQueries, "GetSuggestedTrackDetail"),
  n("query.score-preview-journey", "Score Preview Journey Query", "Returns the accepted/resumable stage, recovery state, geometry candidate, and preview for the current runner.", "query", "projection object", S.journeySpec, "API Surface", { status: "blocked", evidenceConfidence: "medium" }),
  n("query.latest-score-preview", "Latest ScorePreview Query", "Returns the current runner's latest completed or partial preview for one SuggestedTrack.", "query", "projection object", S.journeySpec, "API Surface", { status: "blocked", evidenceConfidence: "medium" }),
);

const eventSpecs = [
  ["provider-connected", "ProviderConnected", "A provider account was linked and a connected runner session established.", "EVT-AUTH-CONNECTED"],
  ["provider-access-revoked", "ProviderAccessRevoked", "Provider or session consent was revoked.", "EVT-AUTH-REVOKED"],
  ["activities-imported", "ActivitiesImported", "A redacted activity import completed.", "EVT-ACT-IMPORTED"],
  ["territory-published", "TerritoryPublished", "Territory metadata and geometry posture were published.", "EVT-TRACK-PUBLISHED"],
  ["evidence-submitted", "EvidenceSubmitted", "A runner-owned activity was submitted as territory evidence.", "EVT-EVIDENCE-SUBMITTED"],
  ["evidence-preview-accepted", "EvidencePreviewAccepted", "Evidence was accepted only for preview projection.", "EVT-EVIDENCE-PREVIEW-ACCEPTED"],
  ["evidence-verified", "EvidenceVerified", "An operator or validation system accepted evidence as verified.", "EVT-EVIDENCE-VERIFIED"],
  ["evidence-rejected", "EvidenceRejected", "Evidence was rejected with an auditable reason.", "EVT-EVIDENCE-REJECTED"],
  ["controller-updated", "ControllerUpdated", "The current controller projection changed with a named basis.", "EVT-CONTROLLER-UPDATED"],
  ["invasion-opened", "InvasionOpened", "A territory entered contested state.", "EVT-INVASION-OPENED"],
  ["defense-succeeded", "DefenseSucceeded", "An eligible defense completed successfully.", "EVT-DEFENSE-SUCCEEDED"],
  ["xp-awarded", "XPAwarded", "Profile XP was appended from a cited event.", "EVT-XP-AWARDED"],
  ["challenge-completed", "ChallengeCompleted", "Challenge completion evidence was accepted.", "EVT-CHALLENGE-COMPLETED"],
  ["season-snapshot-closed", "SeasonSnapshotClosed", "A ranking cycle was closed into an immutable snapshot.", "EVT-SEASON-SNAPSHOT"],
].map(([id, label, definition, selector]) =>
  n(`event.${id}`, label, definition, "event", "evidence object", S.events, selector),
);

eventSpecs.push(
  n("event.runner-confirmed-track-activity", "Runner Confirmed Track Activity", "A runner affirmatively bound one track, owned activity, consent text, and geometry use.", "event", "evidence object", S.journeySpec, "ConfirmTrackWithActivity", { status: "candidate", evidenceConfidence: "medium", commitmentConfidence: "medium" }),
  n("event.geometry-derived", "Geometry Derived", "A privacy-filtered candidate geometry was derived from one confirmed activity.", "event", "evidence object", S.journeySpec, "End-to-End Capability Map", { status: "blocked", evidenceConfidence: "medium" }),
  n("event.score-input-snapshotted", "Score Input Snapshotted", "A canonical score input was persisted with exact policy, geometry, provenance, and history state.", "event", "evidence object", S.journeySpec, "BuildScoreInputSnapshot", { status: "blocked", evidenceConfidence: "medium" }),
  n("event.score-preview-calculated", "Score Preview Calculated", "An explained preview was calculated from one exact policy and canonical snapshot.", "event", "evidence object", S.journeySpec, "CalculateScorePreview", { status: "blocked", evidenceConfidence: "medium" }),
);

const stateGroups = [
  ["auth", S.states, [
    ["unconfigured", "Auth Unconfigured", "Provider configuration is absent."],
    ["anonymous", "Auth Anonymous", "No server session exists."],
    ["connected", "Auth Connected", "Session and provider account are active."],
    ["revoked", "Auth Revoked", "Session or provider consent was revoked."],
    ["error", "Auth Error", "Callback, session, or provider interaction failed."]
  ]],
  ["activity", S.states, [
    ["not-loaded", "Activities Not Loaded", "No activity query has been attempted."],
    ["loading", "Activities Loading", "Activity query is in flight."],
    ["empty", "Activities Empty", "Provider returned no run-like activity summaries."],
    ["ready", "Activities Ready", "Redacted run-like activity summaries are available."],
    ["provider-error", "Activity Provider Error", "Provider activity query failed."]
  ]],
  ["geometry", S.states, [
    ["missing", "Geometry Missing", "No geometry artifact exists."],
    ["placeholder", "Geometry Placeholder", "Only prototype metadata exists; no GPS claim is allowed."],
    ["draft", "Geometry Draft", "A draft route artifact exists."],
    ["source-backed", "Geometry Source-Backed", "A source-backed route geometry exists."],
    ["validated", "Geometry Validated", "Geometry has validation evidence sufficient for the stated use."]
  ]],
  ["submission", S.states, [
    ["draft", "Submission Draft", "The browser has not submitted evidence."],
    ["submitted", "Submission Submitted", "The backend received evidence."],
    ["preview-accepted", "Submission Preview-Accepted", "Evidence may affect preview projection only."],
    ["verified", "Submission Verified", "Operator or validation evidence accepted the submission as verified."],
    ["rejected", "Submission Rejected", "Evidence cannot count under the applied review policy."]
  ]],
  ["controller", S.states, [
    ["neutral", "Controller Neutral", "No accepted evidence controls the territory."],
    ["preview-controlled", "Controller Preview-Controlled", "Preview-accepted evidence controls only the preview projection."],
    ["verified-controlled", "Controller Verified-Controlled", "Verified evidence controls the territory projection."],
    ["contested", "Controller Contested", "An invasion and defense window are active."],
    ["expired", "Controller Expired", "Ownership lapsed under caducity policy."]
  ]],
  ["challenge", S.states, [
    ["available", "Challenge Available", "An eligible runner may join."],
    ["active", "Challenge Active", "The runner is enrolled and progress is open."],
    ["complete", "Challenge Complete", "Completion evidence was accepted."],
    ["rewarded", "Challenge Rewarded", "Declared rewards were issued."],
    ["expired", "Challenge Expired", "The challenge window closed."]
  ]],
  ["season", S.states, [
    ["preseason", "Season Preseason", "Rankings are not open."],
    ["active", "Season Active", "Eligible runs affect seasonal ranking."],
    ["closing", "Season Closing", "The immutable snapshot is being produced."],
    ["closed", "Season Closed", "The snapshot is final and rewards are issued."]
  ]],
  ["suggested-track", S.suggestedStates, [
    ["needs-evidence", "SuggestedTrack Needs Evidence", "The suggestion exists without accepted source-backed evidence."],
    ["evidence-submitted", "SuggestedTrack Evidence Submitted", "At least one redacted candidate was attached."],
    ["operator-review", "SuggestedTrack Operator Review", "An operator is reviewing candidate evidence."],
    ["source-backed", "SuggestedTrack Source-Backed", "An operator accepted source or geometry evidence."],
    ["retired", "SuggestedTrack Retired", "The suggestion is no longer active."]
  ]],
  ["evidence-candidate", S.suggestedStates, [
    ["submitted", "Evidence Candidate Submitted", "A consented redacted candidate is stored."],
    ["operator-review", "Evidence Candidate Operator Review", "An operator is reviewing the candidate."],
    ["accepted", "Evidence Candidate Accepted", "An operator accepted it as useful candidate evidence."],
    ["rejected", "Evidence Candidate Rejected", "An operator rejected the candidate."]
  ]],
  ["geometry-candidate", S.journeyMap, [
    ["absent", "Geometry Candidate Absent", "No geometry derivation has started."],
    ["fetch-pending", "Geometry Fetch Pending", "The confirmed activity's geometry is being acquired."],
    ["derived-candidate", "Geometry Derived Candidate", "A private candidate geometry exists."],
    ["unavailable", "Geometry Unavailable", "Provider, scope, stream, or validation failure prevented derivation."],
    ["rejected", "Geometry Candidate Rejected", "The candidate failed validation or owner review."],
    ["superseded", "Geometry Candidate Superseded", "A newer candidate replaced this candidate without promoting it."]
  ]],
  ["score-preview", S.journeyMap, [
    ["unavailable", "Score Preview Unavailable", "No score-preview path is currently available."],
    ["snapshot-pending", "Score Snapshot Pending", "A canonical ScoreInputSnapshot is being assembled."],
    ["calculation-pending", "Score Calculation Pending", "A complete snapshot and policy await calculation."],
    ["available", "Score Preview Available", "An explained preview result exists."],
    ["incomplete-projection", "Score Incomplete Projection", "Only evidence-satisfied components are shown; total is null."],
    ["blocked-policy", "Score Blocked By Policy", "No ratified complete ScorePolicy is available."],
    ["blocked-geometry", "Score Blocked By Geometry", "No admissible GeometryCandidate is available."],
    ["failed", "Score Calculation Failed", "A calculation invariant failed."],
    ["superseded", "Score Preview Superseded", "A newer policy/snapshot result replaced this preview."]
  ]]
];

const states = stateGroups.flatMap(([group, source, values]) =>
  values.map(([id, label, definition]) =>
    n(`state.${group}.${id}`, label, definition, "lifecycle_state", "authority object", source, `${group} state: ${id}`, {
      status: group === "geometry-candidate" || group === "score-preview" ? "candidate" : "reviewed-candidate",
      evidenceConfidence: group === "geometry-candidate" || group === "score-preview" ? "medium" : "high",
      commitmentConfidence: group === "score-preview" ? "low" : "high",
    }),
  ),
);

const policies = [
  n("policy.controller-selection", "Controller Selection Policy", "Selects current controller from eligible evidence while recording metric and basis.", "policy", "authority object", S.operations, "OP-CONTROL-COMPUTE", { status: "blocked", blockingQuestions: ["When does fastest verified time yield to Zone Score?"] }),
  n("policy.preview-evidence", "Preview Evidence Policy", "Allows submitted evidence to affect preview controller state while forbidding verified language.", "policy", "authority object", S.operations, "OP-EVIDENCE-AUTO-ACCEPT"),
  n("policy.geometry-privacy", "Geometry Privacy Policy", "Defines filtering, precision, retention, visibility, and deletion for activity-derived candidate geometry.", "policy", "authority object", S.journeySpec, "GeometryCandidate", { status: "blocked", owner: "body-war.data-privacy-owner", evidenceConfidence: "medium", blockingQuestions: ["What filter, precision, retention, and deletion behavior is ratified?"] }),
  n("policy.consent-contract", "Consent Contract", "Binds displayed, affirmed, transmitted, and persisted consent text and version to one exact activity and track.", "policy", "authority object", S.journeySpec, "RunnerConfirmation", { status: "candidate", evidenceConfidence: "medium", commitmentConfidence: "medium" }),
  n("policy.anti-cheat", "Anti-Cheat Policy", "Defines anomaly detection, evidence rejection, escalation, and review standards.", "policy", "authority object", S.game, "Anti-cheat", { status: "deferred", blockingQuestions: ["What strictness and automated validation are adopted?"] }),
  n("policy.caducity", "Ownership Caducity Policy", "Defines when territory ownership expires or requires renewal.", "policy", "authority object", S.game, "Caducity", { status: "blocked", blockingQuestions: ["What expiry interval and renewal evidence apply?"] }),
  n("policy.ownership-eligibility", "Ownership Eligibility Policy", "Defines who may invade, control, or defend and which evidence counts.", "policy", "authority object", S.game, "Ownership and invasion", { status: "blocked", blockingQuestions: ["Which evidence authority and clan eligibility rules apply?"] }),
  n("policy.notification-privacy", "Notification Privacy Policy", "Forbids private activity details in push payloads and requires source event identity.", "policy", "authority object", S.operations, "OP-NOTIFY-DISPATCH"),
  n("policy.activity-eligibility", "Activity Eligibility Policy", "Admits run-like activity types and declared visibility/geometry/history rules for evidence or score input.", "policy", "authority object", S.journeySpec, "ScorePolicy", { status: "blocked", owner: "body-war.score-policy-owner" }),
  n("policy.score-history", "Score History Policy", "Defines complete-window acquisition, timezone, consent scope, same-day collapse, and incomplete-history behavior.", "policy", "authority object", S.journeySpec, "ScoreInputSnapshot", { status: "blocked", owner: "body-war.score-policy-owner" }),
];

const premises = [
  ["h-001", "H-001 Physical Activity Motivation", "Gamifying neighborhood running can increase motivation and repeat physical activity."],
  ["h-002", "H-002 Territory Competition", "Visible local territory competition can create repeated engagement."],
  ["h-003", "H-003 Strava Trust", "Strava-linked activity evidence can improve participant trust in pilot results."],
  ["h-004", "H-004 Park Pilot", "A bounded park-track pilot can test core behavior before city-wide zoning."],
  ["h-005", "H-005 Composite Score", "A composite of pace, distance, and frequency can feel fairer than a single metric."],
  ["h-006", "H-006 Defense Window", "Time-bounded defense can create urgency without requiring real-time play."],
  ["h-007", "H-007 Progression", "Persistent XP, leagues, and badges can support long-term engagement."],
  ["h-008", "H-008 Clan Sociality", "Clan membership can increase social commitment and retention."],
  ["h-009", "H-009 Sponsor Value", "Sponsored zones may create value for local partners without harming play.", { status: "deferred" }],
  ["h-010", "H-010 Local Operator", "A local operator can review evidence and support safe pilot learning."]
].map(([id, label, definition, options = {}]) =>
  n(`premise.${id}`, label, definition, "premise", "authority object", S.hypotheses, id.toUpperCase(), {
    status: options.status ?? "candidate",
    evidenceConfidence: "low",
    commitmentConfidence: "low",
    nextGate: "body-war.experiment-design",
    forbidden: "Do not collapse a product premise into validated human outcome, causal proof, or adopted rule.",
  }),
);

const interfacesAndWorkflows = [
  n("interface.strava-provider-boundary", "Strava Provider Boundary", "The server-side interface for OAuth, token custody/refresh, and redacted activity acquisition.", "interface", "workflow object", S.interfaces, "Strava Provider Boundary"),
  n("interface.http-api", "Body War HTTP API", "The authenticated and public HTTP routes exposing queries and controlled mutations.", "interface", "workflow object", S.interfaces, "HTTP Interface Table"),
  n("interface.suggested-track-api", "SuggestedTrack API", "Authenticated routes for listing, creating, detailing, and attaching candidate evidence.", "interface", "workflow object", S.suggestedInterfaces, "SuggestedTrack API"),
  n("interface.score-preview-journey-api", "Score Preview Journey API", "A durable command/read boundary for resumable confirmation, geometry, snapshot, and preview stages.", "interface", "workflow object", S.journeySpec, "API Surface", { status: "blocked", evidenceConfidence: "medium" }),
  n("workflow.run-to-control", "Run To Control Workflow", "Import activity, submit evidence, review or preview-accept it, and recompute controller projection.", "workflow", "workflow object", S.events, "Event Ordering"),
  n("workflow.invasion-defense", "Invasion and Defense Workflow", "Open contested state, notify eligible defenders, record defense result, and update ownership.", "workflow", "workflow object", S.operations, "OP-CONTROL-OPEN-INVASION"),
  n("workflow.seasonal-progression", "Seasonal Progression Workflow", "Award XP, project rankings, close a season, and preserve permanent progression.", "workflow", "workflow object", S.operations, "OP-SEASON-SNAPSHOT"),
  n("workflow.suggested-track-expansion", "SuggestedTrack Expansion Workflow", "Create or select a route suggestion and attach consented redacted candidate evidence.", "workflow", "workflow object", S.suggestedSpec, "Module Map"),
  n("workflow.login-to-score-preview", "Login To ScorePreview Workflow", "Connect Strava, select an exact track/activity, consent, derive candidate geometry, snapshot inputs, calculate, and project a preview.", "workflow", "workflow object", S.journeySpec, "End-to-End Capability Map", { status: "blocked", evidenceConfidence: "medium", blockingQuestions: ["Are score and geometry policies ratified for the selected evidence lane?"] }),
];

export const catalog = [
  ...actors,
  ...contexts,
  ...capabilities,
  ...objects,
  ...operationSpecs,
  ...querySpecs,
  ...eventSpecs,
  ...states,
  ...policies,
  ...premises,
  ...interfacesAndWorkflows,
];

export const sourceAliases = S;
