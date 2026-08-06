const SERVER = "projects/body-war/app/server.ts"
const STATIC_UI = "projects/body-war/app/static/app.js"
const TYPES = "projects/body-war/app/src/auth/types.ts"
const REPOSITORY = "projects/body-war/app/src/auth/body-war-repository.ts"
const STRAVA = "projects/body-war/app/src/auth/strava-oauth.ts"
const SESSION = "projects/body-war/app/src/auth/browser-session.ts"
const MEMORY = "projects/body-war/app/src/auth/memory-repository.ts"
const DRIZZLE = "projects/body-war/app/src/auth/drizzle-repository.ts"
const DATABASE = "projects/body-war/app/src/infrastructure/postgres/database.ts"
const MIGRATIONS = "projects/body-war/app/src/infrastructure/postgres/migrations.ts"
const SCHEMA = "projects/body-war/app/src/infrastructure/postgres/schema.ts"
const APP_PACKAGE = "projects/body-war/app/package.json"
const UNIT_TEST = "projects/body-war/app/tests/auth-consumer.test.ts"
const API_E2E = "projects/body-war/app/e2e/body-war-auth.e2e.ts"
const UI_E2E = "projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts"
const COMPOSE = "projects/body-war/infra/docker-compose.direct.yml"
const CADDY = "projects/body-war/infra/Caddyfile"

const ref = (path, selector) => ({ path, selector })
const node = (slug, label, definition, systemKind, sourceRefs, options = {}) => ({
  concept_id: `body-war.system.${systemKind}.${slug}`,
  label,
  definition,
  concept_role: options.concept_role ?? "workflow object",
  system_kind: systemKind,
  observation_status: options.observation_status ?? "observed",
  source_refs: sourceRefs,
  confidence: options.confidence ?? "high",
  residue: options.residue ?? [],
})

export const systemNodes = [
  node("http-server", "Body War HTTP Server", "Node HTTP composition root that constructs adapters, routes API requests, and serves the browser application.", "component", [ref(SERVER, "export async function handleRequest")]),
  node("browser-ui", "TROQAR Browser UI", "Browser-side interface for Strava connection, safe profile display, suggested tracks, activities, and preview evidence submission.", "component", [ref(STATIC_UI, "createSuggestedTrack")]),
  node("http-api", "Body War HTTP API", "Request boundary exposing the currently implemented Body War JSON endpoints.", "interface", [ref(SERVER, "if (url.pathname.startsWith(\"/api/\"))")]),
  node("browser-session-adapter", "Browser Session Adapter", "Adapter that binds package authentication to secure cookies, CSRF checks, origin checks, session creation, authentication, and logout.", "module", [ref(SESSION, "export function createBrowserSessionAdapter")]),
  node("strava-oauth-adapter", "Strava OAuth Adapter", "Body War-owned provider adapter for OAuth state, token exchange and custody, provider profile, and redacted activity summaries.", "module", [ref(STRAVA, "export function createStravaOAuthAdapter")]),
  node("body-war-repository-port", "Body War Repository Port", "Application-owned persistence interface for profiles, provider records, suggested tracks, and activity evidence candidates.", "interface", [ref(REPOSITORY, "export type BodyWarAuthRepository")]),
  node("memory-repository", "Memory Repository", "In-process repository used by the local prototype and fake-provider test path.", "data_store", [ref(MEMORY, "export function createMemoryBodyWarAuthRepository")]),
  node("postgres-repository", "Postgres Repository", "Drizzle-backed implementation of the Body War repository port.", "data_store", [ref(DRIZZLE, "export function createDrizzleBodyWarAuthRepository")]),
  node("postgres-database", "Postgres Database Adapter", "SQL client and Drizzle database construction boundary selected by runtime configuration.", "module", [ref(DATABASE, "export function createBodyWarDatabase")]),
  node("migration-runner", "Migration Runner", "Checksum-bound migration runner for shared authentication and Body War database schemas.", "job", [ref(MIGRATIONS, "export async function applyBodyWarMigrations")]),
  node("shared-auth-package", "DomainSpec Auth User Management", "Imported shared package supplying principal, permission, session, access-token, and authorization use cases.", "external_dependency", [ref(APP_PACKAGE, "@domainspec/auth-user-management")], { concept_role: "authority object" }),
  node("strava-api", "Strava API", "External activity provider reached only through the server-side Strava adapter.", "external_dependency", [ref(STRAVA, "DEFAULT_STRAVA_SCOPE")], { concept_role: "authority object" }),
  node("static-asset-server", "Static Asset Server", "Server path that publishes the Body War browser shell and its local assets.", "module", [ref(SERVER, "async function serveStatic")]),
  node("json-prototype-store", "Prototype JSON Store", "Local JSON files used for track and submission fixture persistence outside the auth repositories.", "data_store", [ref(SERVER, "SUBMISSION_STORE")]),
  node("runtime-configuration", "Runtime Configuration", "Environment-selected host, origin, session, provider, persistence, cookie, and redirect configuration.", "configuration", [ref(SERVER, "BODY_WAR_AUTH_BACKEND")]),
  node("status", "GET /api/status", "Returns configuration-safe authentication and provider connection status.", "endpoint", [ref(SERVER, "url.pathname === \"/api/status\"")]),
  node("profile", "GET /api/profile", "Returns the authenticated runner's safe Body War profile projection.", "endpoint", [ref(SERVER, "url.pathname === \"/api/profile\"")]),
  node("strava-start", "GET /api/auth/strava/start", "Starts the Strava OAuth flow and sets bounded state.", "endpoint", [ref(SERVER, "url.pathname === \"/api/auth/strava/start\"")]),
  node("strava-callback", "GET /api/auth/strava/callback", "Completes Strava OAuth and creates the browser session binding.", "endpoint", [ref(SERVER, "url.pathname === \"/api/auth/strava/callback\"")]),
  node("logout", "POST /api/auth/logout", "Revokes the active session and clears browser authentication cookies.", "endpoint", [ref(SERVER, "url.pathname === \"/api/auth/logout\"")]),
  node("activities", "GET /api/activities", "Lists redacted Strava activity summaries for an authenticated connected runner.", "endpoint", [ref(SERVER, "url.pathname === \"/api/activities\"")]),
  node("suggested-tracks", "GET/POST /api/suggested-tracks", "Lists suggested tracks or creates a runner suggestion in needs-evidence state.", "endpoint", [ref(SERVER, "url.pathname === \"/api/suggested-tracks\"")]),
  node("suggested-track-detail", "GET /api/suggested-tracks/:id", "Returns one suggested track and its current evidence summary.", "endpoint", [ref(SERVER, "suggestedTrackDetailMatch")]),
  node("suggested-track-evidence", "POST /api/suggested-tracks/:id/evidence-candidates", "Attaches a consent-acknowledged redacted activity candidate to a suggested track.", "endpoint", [ref(SERVER, "suggestedTrackEvidenceMatch")]),
  node("tracks", "GET /api/tracks", "Returns the prototype track catalog from the local JSON store.", "endpoint", [ref(SERVER, "url.pathname === \"/api/tracks\"")]),
  node("submissions", "GET/POST /api/submissions", "Lists fixture submissions or creates authenticated preview evidence submissions guarded by CSRF and origin checks.", "endpoint", [ref(SERVER, "url.pathname === \"/api/submissions\"")]),
  node("runner-profiles", "Runner Profiles Table", "Stores Body War runner display/profile data keyed to the shared principal.", "table", [ref(SCHEMA, "body_war_runner_profiles")]),
  node("oauth-states", "OAuth States Table", "Stores single-use expiring provider OAuth state.", "table", [ref(SCHEMA, "body_war_oauth_states")]),
  node("provider-accounts", "Provider Accounts Table", "Stores provider identity and connection status without exposing provider tokens to the browser.", "table", [ref(SCHEMA, "body_war_provider_accounts")]),
  node("provider-tokens", "Provider Tokens Table", "Stores protected provider access and refresh token ciphertext on the server.", "table", [ref(SCHEMA, "body_war_provider_tokens")]),
  node("suggested-tracks", "Suggested Tracks Table", "Stores suggestion metadata, workflow status, and geometry authority marker.", "table", [ref(SCHEMA, "body_war_suggested_tracks")]),
  node("activity-evidence-candidates", "Activity Evidence Candidates Table", "Stores consent-bound redacted activity evidence candidate records for suggested tracks.", "table", [ref(SCHEMA, "body_war_activity_evidence_candidates")]),
  node("app-container", "Body War App Container", "Production application service with explicit runtime configuration and health check.", "deployment_unit", [ref(COMPOSE, "services:")]),
  node("postgres-service", "Postgres Service", "Internal persistent database service with a health check and durable volume.", "deployment_unit", [ref(COMPOSE, "postgres:")]),
  node("caddy-edge", "Caddy Edge Proxy", "TLS-capable reverse proxy forwarding the public origin to the Body War application service.", "deployment_unit", [ref(CADDY, "reverse_proxy app:5174")]),
  node("auth-consumer-tests", "Auth Consumer Tests", "Node tests covering fake-Strava authentication, cookie safety, profile projection, activity authority ceiling, and suggested-track behavior.", "test", [ref(UNIT_TEST, "Body War local fake-Strava auth flow creates safe profile and cookies")], { concept_role: "evidence object" }),
  node("api-e2e-tests", "Body War API E2E Tests", "End-to-end HTTP test of login, activities, suggested tracks, evidence candidates, submissions, and logout.", "test", [ref(API_E2E, "suggested_track")], { concept_role: "evidence object" }),
  node("browser-e2e-tests", "TROQAR Browser E2E Tests", "Playwright tests for anonymous login, safe connected profile, suggested-track creation, preview evidence submission, logout, and narrow viewports.", "test", [ref(UI_E2E, "TROQAR production login and runner profile")], { concept_role: "evidence object" }),
  node("geometry-score-gap", "Geometry And Score Runtime Gap", "The current runtime deliberately reports route geometry as deferred or not claimed and does not calculate the business score preview.", "gap", [ref(SERVER, "route_geometry: \"deferred\"")], { concept_role: "residue object", observation_status: "gap", confidence: "high", residue: ["Implement source-authorized activity geometry acquisition, geometry candidate derivation, policy snapshot, explained score calculation, and projection before closing this gap."] }),
]

const relation = (slug, predicate, source, target, sourceRefs, options = {}) => ({
  relation_id: `body-war.system-relation.${slug}`,
  predicate,
  source_concept: source,
  target_concept: target,
  evidence_refs: sourceRefs,
  observation_status: options.observation_status ?? "observed",
})

export const systemRelations = [
  relation("server-exposes-api", "exposes", "body-war.system.component.http-server", "body-war.system.interface.http-api", [ref(SERVER, "export async function handleRequest")]),
  relation("server-serves-ui", "serves", "body-war.system.component.http-server", "body-war.system.component.browser-ui", [ref(SERVER, "async function serveStatic")]),
  relation("server-uses-static-assets", "uses", "body-war.system.component.http-server", "body-war.system.module.static-asset-server", [ref(SERVER, "async function serveStatic")]),
  relation("static-assets-serve-ui", "serves", "body-war.system.module.static-asset-server", "body-war.system.component.browser-ui", [ref(SERVER, "STATIC_DIR")]),
  relation("server-uses-session", "uses", "body-war.system.component.http-server", "body-war.system.module.browser-session-adapter", [ref(SERVER, "createBrowserSessionAdapter")]),
  relation("server-uses-strava", "uses", "body-war.system.component.http-server", "body-war.system.module.strava-oauth-adapter", [ref(SERVER, "createStravaOAuthAdapter")]),
  relation("server-uses-repository", "uses", "body-war.system.component.http-server", "body-war.system.interface.body-war-repository-port", [ref(SERVER, "bodyWarRepo")]),
  relation("memory-implements-repository", "implements", "body-war.system.data_store.memory-repository", "body-war.system.interface.body-war-repository-port", [ref(MEMORY, "createMemoryBodyWarAuthRepository")]),
  relation("postgres-implements-repository", "implements", "body-war.system.data_store.postgres-repository", "body-war.system.interface.body-war-repository-port", [ref(DRIZZLE, "createDrizzleBodyWarAuthRepository")]),
  relation("postgres-repository-uses-database", "uses", "body-war.system.data_store.postgres-repository", "body-war.system.module.postgres-database", [ref(DRIZZLE, "BodyWarDrizzleDatabase")]),
  relation("session-depends-auth", "depends_on", "body-war.system.module.browser-session-adapter", "body-war.system.external_dependency.shared-auth-package", [ref(SESSION, "@domainspec/auth-user-management")]),
  relation("strava-depends-auth", "depends_on", "body-war.system.module.strava-oauth-adapter", "body-war.system.external_dependency.shared-auth-package", [ref(STRAVA, "@domainspec/auth-user-management")]),
  relation("strava-calls-api", "calls", "body-war.system.module.strava-oauth-adapter", "body-war.system.external_dependency.strava-api", [ref(STRAVA, "https://www.strava.com/oauth/token")]),
  ...["status", "profile", "strava-start", "strava-callback", "logout", "activities", "suggested-tracks", "suggested-track-detail", "suggested-track-evidence", "tracks", "submissions"].map((slug) => relation(`api-contains-${slug}`, "contains", "body-war.system.interface.http-api", `body-war.system.endpoint.${slug}`, [ref(SERVER, "/api/")])),
  relation("strava-start-calls-adapter", "calls", "body-war.system.endpoint.strava-start", "body-war.system.module.strava-oauth-adapter", [ref(SERVER, "handleStravaStart")]),
  relation("strava-callback-calls-adapter", "calls", "body-war.system.endpoint.strava-callback", "body-war.system.module.strava-oauth-adapter", [ref(SERVER, "handleStravaCallback")]),
  relation("activities-calls-strava", "calls", "body-war.system.endpoint.activities", "body-war.system.module.strava-oauth-adapter", [ref(SERVER, "handleActivities")]),
  relation("unsafe-endpoints-protected", "protects_with", "body-war.system.interface.http-api", "body-war.system.module.browser-session-adapter", [ref(SESSION, "validateBrowserGuards")]),
  relation("repository-writes-profiles", "writes", "body-war.system.interface.body-war-repository-port", "body-war.system.table.runner-profiles", [ref(REPOSITORY, "upsertRunnerProfile")]),
  relation("repository-writes-oauth-states", "writes", "body-war.system.interface.body-war-repository-port", "body-war.system.table.oauth-states", [ref(REPOSITORY, "createOAuthState")]),
  relation("repository-writes-provider-accounts", "writes", "body-war.system.interface.body-war-repository-port", "body-war.system.table.provider-accounts", [ref(REPOSITORY, "upsertProviderAccount")]),
  relation("repository-writes-provider-tokens", "writes", "body-war.system.interface.body-war-repository-port", "body-war.system.table.provider-tokens", [ref(REPOSITORY, "storeProviderToken")]),
  relation("repository-writes-suggested-tracks", "writes", "body-war.system.interface.body-war-repository-port", "body-war.system.table.suggested-tracks", [ref(REPOSITORY, "createSuggestedTrack")]),
  relation("repository-writes-evidence-candidates", "writes", "body-war.system.interface.body-war-repository-port", "body-war.system.table.activity-evidence-candidates", [ref(REPOSITORY, "addActivityEvidenceCandidate")]),
  relation("migrations-migrate-database", "migrates", "body-war.system.job.migration-runner", "body-war.system.module.postgres-database", [ref(MIGRATIONS, "applyBodyWarMigrations")]),
  relation("submissions-use-json", "persists_to", "body-war.system.endpoint.submissions", "body-war.system.data_store.json-prototype-store", [ref(SERVER, "SUBMISSION_STORE")]),
  relation("tracks-use-json", "reads", "body-war.system.endpoint.tracks", "body-war.system.data_store.json-prototype-store", [ref(SERVER, "TRACK_STORE")]),
  relation("server-configured-by-runtime", "configured_by", "body-war.system.component.http-server", "body-war.system.configuration.runtime-configuration", [ref(SERVER, "BODY_WAR_HOST")]),
  relation("app-container-runs-server", "runs", "body-war.system.deployment_unit.app-container", "body-war.system.component.http-server", [ref(COMPOSE, "BODY_WAR_PORT")]),
  relation("app-container-depends-postgres", "depends_on", "body-war.system.deployment_unit.app-container", "body-war.system.deployment_unit.postgres-service", [ref(COMPOSE, "condition: service_healthy")]),
  relation("edge-routes-app", "routes_to", "body-war.system.deployment_unit.caddy-edge", "body-war.system.deployment_unit.app-container", [ref(CADDY, "reverse_proxy app:5174")]),
  relation("unit-tests-observe-server", "tests", "body-war.system.test.auth-consumer-tests", "body-war.system.component.http-server", [ref(UNIT_TEST, "withServer")]),
  relation("api-e2e-observes-api", "tests", "body-war.system.test.api-e2e-tests", "body-war.system.interface.http-api", [ref(API_E2E, "handleRequest")]),
  relation("browser-e2e-observes-ui", "tests", "body-war.system.test.browser-e2e-tests", "body-war.system.component.browser-ui", [ref(UI_E2E, "page.goto(\"/\")")]),
  relation("gap-constrains-server", "constrains", "body-war.system.gap.geometry-score-gap", "body-war.system.component.http-server", [ref(SERVER, "route_geometry: \"deferred\"")], { observation_status: "gap" }),
]

const businessNodeRef = (filename, conceptId) => ref(`projects/body-war/ontology/business/nodes/${filename}.json`, conceptId)
const bridge = (slug, predicate, businessConcept, systemConcept, businessRef, systemRef, alignmentStatus, note) => ({
  relation_id: `body-war.bridge.${slug}`,
  predicate,
  business_concept: businessConcept,
  system_concept: systemConcept,
  business_evidence_refs: [businessRef],
  system_evidence_refs: [systemRef],
  alignment_status: alignmentStatus,
  note,
})

export const bridgeRelations = [
  bridge("http-api-realized", "realized_by", "body-war.business.interface.http-api", "body-war.system.interface.http-api", businessNodeRef("interface.http-api", "body-war.business.interface.http-api"), ref(SERVER, "export async function handleRequest"), "supported", "The current server exposes the implemented HTTP boundary, not every design-time route."),
  bridge("strava-boundary-realized", "realized_by", "body-war.business.interface.strava-provider-boundary", "body-war.system.module.strava-oauth-adapter", businessNodeRef("interface.strava-provider-boundary", "body-war.business.interface.strava-provider-boundary"), ref(STRAVA, "export function createStravaOAuthAdapter"), "supported", "Provider tokens remain in the server-side adapter and repositories."),
  bridge("auth-capability-realized", "realized_by", "body-war.business.capability.auth-consent", "body-war.system.module.browser-session-adapter", businessNodeRef("capability.auth-consent", "body-war.business.capability.auth-consent"), ref(SESSION, "export function createBrowserSessionAdapter"), "supported", "The adapter implements browser-session and request guard concerns for the prototype."),
  bridge("oauth-start-realized", "realized_by", "body-war.business.operation.start-strava-oauth", "body-war.system.endpoint.strava-start", businessNodeRef("operation.start-strava-oauth", "body-war.business.operation.start-strava-oauth"), ref(SERVER, "handleStravaStart"), "supported", "The endpoint starts the provider flow."),
  bridge("oauth-complete-realized", "realized_by", "body-war.business.operation.complete-strava-oauth", "body-war.system.endpoint.strava-callback", businessNodeRef("operation.complete-strava-oauth", "body-war.business.operation.complete-strava-oauth"), ref(SERVER, "handleStravaCallback"), "supported", "The endpoint completes the fake or configured provider callback and binds a session."),
  bridge("auth-status-realized", "realized_by", "body-war.business.query.auth-status", "body-war.system.endpoint.status", businessNodeRef("query.auth-status", "body-war.business.query.auth-status"), ref(SERVER, "handleStatus"), "supported", "The runtime provides a configuration-safe status projection."),
  bridge("profile-summary-realized", "realized_by", "body-war.business.query.profile-summary", "body-war.system.endpoint.profile", businessNodeRef("query.profile-summary", "body-war.business.query.profile-summary"), ref(SERVER, "handleProfile"), "partial", "The current profile endpoint is safe but does not yet project full score, XP, league, badge, or streak state."),
  bridge("activity-import-realized", "realized_by", "body-war.business.operation.import-activities", "body-war.system.endpoint.activities", businessNodeRef("operation.import-activities", "body-war.business.operation.import-activities"), ref(SERVER, "handleActivities"), "supported", "The endpoint returns redacted activity summaries for a connected runner."),
  bridge("activity-list-realized", "realized_by", "body-war.business.query.activity-list", "body-war.system.endpoint.activities", businessNodeRef("query.activity-list", "body-war.business.query.activity-list"), ref(SERVER, "handleActivities"), "supported", "The activity query is implemented through the same endpoint."),
  bridge("suggested-track-create-realized", "realized_by", "body-war.business.operation.create-suggested-track", "body-war.system.endpoint.suggested-tracks", businessNodeRef("operation.create-suggested-track", "body-war.business.operation.create-suggested-track"), ref(SERVER, "handleSuggestedTrackCreate"), "supported", "The endpoint creates a needs-evidence candidate only."),
  bridge("suggested-track-list-realized", "realized_by", "body-war.business.query.list-suggested-tracks", "body-war.system.endpoint.suggested-tracks", businessNodeRef("query.list-suggested-tracks", "body-war.business.query.list-suggested-tracks"), ref(SERVER, "handleSuggestedTracksList"), "supported", "The endpoint returns default and runner-created suggestions."),
  bridge("suggested-track-detail-realized", "realized_by", "body-war.business.query.get-suggested-track-detail", "body-war.system.endpoint.suggested-track-detail", businessNodeRef("query.get-suggested-track-detail", "body-war.business.query.get-suggested-track-detail"), ref(SERVER, "handleSuggestedTrackDetail"), "supported", "The endpoint joins one suggestion to its evidence summary."),
  bridge("candidate-attach-realized", "realized_by", "body-war.business.operation.attach-activity-evidence-candidate", "body-war.system.endpoint.suggested-track-evidence", businessNodeRef("operation.attach-activity-evidence-candidate", "body-war.business.operation.attach-activity-evidence-candidate"), ref(SERVER, "handleSuggestedTrackEvidenceCreate"), "supported", "The endpoint records explicit consent and a redacted evidence candidate."),
  bridge("evidence-submit-realized", "realized_by", "body-war.business.operation.submit-evidence", "body-war.system.endpoint.submissions", businessNodeRef("operation.submit-evidence", "body-war.business.operation.submit-evidence"), ref(SERVER, "handleSubmission"), "partial", "Submission is implemented as prototype evidence and does not become verified evidence or territory authority."),
  bridge("track-list-realized", "realized_by", "body-war.business.query.track-list", "body-war.system.endpoint.tracks", businessNodeRef("query.track-list", "body-war.business.query.track-list"), ref(SERVER, "TRACK_STORE"), "partial", "The current catalog is a JSON-backed prototype fixture."),
  bridge("auth-tested", "tested_by", "body-war.business.capability.auth-consent", "body-war.system.test.auth-consumer-tests", businessNodeRef("capability.auth-consent", "body-war.business.capability.auth-consent"), ref(UNIT_TEST, "Body War local fake-Strava auth flow creates safe profile and cookies"), "supported", "The unit/consumer suite tests the fake-provider authentication boundary."),
  bridge("suggestion-tested", "tested_by", "body-war.business.workflow.suggested-track-expansion", "body-war.system.test.api-e2e-tests", businessNodeRef("workflow.suggested-track-expansion", "body-war.business.workflow.suggested-track-expansion"), ref(API_E2E, "evidence-candidates"), "supported", "The HTTP E2E flow exercises suggestion creation and candidate attachment."),
  bridge("browser-workflow-tested", "tested_by", "body-war.business.workflow.suggested-track-expansion", "body-war.system.test.browser-e2e-tests", businessNodeRef("workflow.suggested-track-expansion", "body-war.business.workflow.suggested-track-expansion"), ref(UI_E2E, "submits one activity as preview evidence through visible controls"), "supported", "The browser test covers the user-visible candidate flow."),
  bridge("geometry-fetch-gap", "drifts_from", "body-war.business.operation.fetch-selected-activity-geometry", "body-war.system.gap.geometry-score-gap", businessNodeRef("operation.fetch-selected-activity-geometry", "body-war.business.operation.fetch-selected-activity-geometry"), ref(SERVER, "route_geometry: \"deferred\""), "gap", "No source-authorized route geometry acquisition is present in the current runtime."),
  bridge("geometry-derive-gap", "drifts_from", "body-war.business.operation.derive-geometry-candidate", "body-war.system.gap.geometry-score-gap", businessNodeRef("operation.derive-geometry-candidate", "body-war.business.operation.derive-geometry-candidate"), ref(SERVER, "route_geometry: \"not_claimed\""), "gap", "Attaching activity evidence does not derive or promote geometry."),
  bridge("score-preview-gap", "drifts_from", "body-war.business.operation.calculate-score-preview", "body-war.system.gap.geometry-score-gap", businessNodeRef("operation.calculate-score-preview", "body-war.business.operation.calculate-score-preview"), ref(SERVER, "composite_score_pending"), "gap", "The runtime explicitly leaves composite scoring pending."),
  bridge("login-score-workflow-partial", "realized_by", "body-war.business.workflow.login-to-score-preview", "body-war.system.component.browser-ui", businessNodeRef("workflow.login-to-score-preview", "body-war.business.workflow.login-to-score-preview"), ref(UI_E2E, "connects fake Strava and renders safe profile, activity, and evidence UI"), "partial", "Login through evidence candidate submission is visible; geometry derivation and explained score projection remain absent."),
  bridge("provider-account-persisted", "realized_by", "body-war.business.entity.provider-account", "body-war.system.table.provider-accounts", businessNodeRef("entity.provider-account", "body-war.business.entity.provider-account"), ref(SCHEMA, "body_war_provider_accounts"), "supported", "Provider identity and connection status have a durable schema."),
  bridge("suggested-track-persisted", "realized_by", "body-war.business.entity.suggested-track", "body-war.system.table.suggested-tracks", businessNodeRef("entity.suggested-track", "body-war.business.entity.suggested-track"), ref(SCHEMA, "body_war_suggested_tracks"), "supported", "Suggested-track candidates have a durable schema."),
  bridge("candidate-persisted", "realized_by", "body-war.business.entity.activity-evidence-candidate", "body-war.system.table.activity-evidence-candidates", businessNodeRef("entity.activity-evidence-candidate", "body-war.business.entity.activity-evidence-candidate"), ref(SCHEMA, "body_war_activity_evidence_candidates"), "supported", "Candidate evidence and consent fields have a durable schema."),
]

export const systemLayers = [
  { id: "presentation", label: "Presentation", concepts: ["body-war.system.component.browser-ui"] },
  { id: "interface", label: "HTTP Interface", concepts: ["body-war.system.component.http-server", "body-war.system.interface.http-api", ...systemNodes.filter((entry) => entry.system_kind === "endpoint").map((entry) => entry.concept_id)] },
  { id: "application-adapters", label: "Application Adapters", concepts: ["body-war.system.module.browser-session-adapter", "body-war.system.module.strava-oauth-adapter", "body-war.system.interface.body-war-repository-port"] },
  { id: "persistence", label: "Persistence", concepts: systemNodes.filter((entry) => ["data_store", "table", "job"].includes(entry.system_kind)).map((entry) => entry.concept_id) },
  { id: "external", label: "External Dependencies", concepts: systemNodes.filter((entry) => entry.system_kind === "external_dependency").map((entry) => entry.concept_id) },
  { id: "deployment", label: "Deployment", concepts: systemNodes.filter((entry) => entry.system_kind === "deployment_unit").map((entry) => entry.concept_id) },
  { id: "verification", label: "Verification And Gaps", concepts: systemNodes.filter((entry) => ["test", "gap"].includes(entry.system_kind)).map((entry) => entry.concept_id) },
]
