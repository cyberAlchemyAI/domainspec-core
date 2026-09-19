import {createDurableOidcBoundary} from "../auth/oidc-durable.js";
import {createOidcBoundary,OIDC_POLICY,SESSION_COOKIE} from "../auth/oidc.js";
import {readQuery} from "../application/query.js";
import {readRequest} from "../application/request.js";
import { project } from "../application/domain.js";
import { evidenceConsentRequired } from "../compiled/generated/src/domainspec/typescript/body-war-pilot/evidence-consent-required.js";
import {
  createDrizzleAuthRepositories,
  createHmacTokenCodec,
  createMemoryAuthRepositories,
  type AuthContext,
} from "@domainspec/auth-user-management"
import { createServer, type IncomingMessage, type ServerResponse } from "node:http"
import { readFile } from "node:fs/promises"
import { existsSync, readFileSync } from "node:fs"
import { extname, resolve } from "node:path"
import { createBrowserSessionAdapter } from "../auth/browser-session.js"
import { parseCookieHeader } from "../auth/cookies.js"
import { createDrizzleBodyWarAuthRepository } from "../auth/drizzle-repository.js"
import { createMemoryBodyWarAuthRepository } from "../auth/memory-repository.js"
import {
  DEFAULT_STRAVA_SCOPE,
  createStravaOAuthAdapter,
  stravaPrincipalPlaceholder,
} from "../auth/strava-oauth.js"
import {
  appError,
  type ActivityEvidenceCandidate,
  type ActivitySummary,
  type AppError,
  type CookieMap,
  type JsonRecord,
  type ProviderAccount,
  type RunnerProfile,
  type SuggestedTrack,
} from "../auth/types.js"
import { createBodyWarDatabase, createBodyWarSqlClient } from "../infrastructure/postgres/database.js"

const APP_ROOT = resolve(process.env.BODY_WAR_APP_ROOT ?? process.cwd())
const STATIC_DIR = resolve(APP_ROOT, "static")

function loadDotenv(): void {
  const envPath = resolve(APP_ROOT, ".env")
  if (!existsSync(envPath)) return
  const text = readFileSync(envPath, "utf8")
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim()
    if (!line || line.startsWith("#") || !line.includes("=")) continue
    const [key, ...rest] = line.split("=")
    if (!key) continue
    process.env[key.trim()] ??= rest.join("=").trim().replace(/^['"]|['"]$/g, "")
  }
}

loadDotenv()

function env(name: string, fallback = ""): string {
  return process.env[name] ?? fallback
}

export const HOST = env("BODY_WAR_HOST", "127.0.0.1")
export const PORT = Number(env("BODY_WAR_PORT", "5174"))
export const PUBLIC_BASE_URL = env("BODY_WAR_PUBLIC_BASE_URL", `http://${HOST}:${PORT}`)
export const STRAVA_REDIRECT_URI = env(
  "STRAVA_REDIRECT_URI",
  `${PUBLIC_BASE_URL}/api/auth/strava/callback`,
)
const SESSION_SECRET = env("BODY_WAR_SESSION_SECRET") || env("SESSION_SECRET") || "dev-secret-change-me"
export const IDENTITY_MODE=env("BODY_WAR_IDENTITY_MODE","strava-pilot");
if(!["strava-pilot","oidc","oidc-durable"].includes(IDENTITY_MODE))throw Error("Unknown identity profile");
const OIDC_ENABLED=IDENTITY_MODE!=="strava-pilot";
const oidcFactory=IDENTITY_MODE==="oidc-durable"?createDurableOidcBoundary:createOidcBoundary;
if(OIDC_ENABLED&&(PUBLIC_BASE_URL!==OIDC_POLICY.origin||!env("BODY_WAR_OIDC_CLIENT_SECRET")))throw Error("OIDC profile configuration required");
const SESSION_TTL_SECONDS = OIDC_ENABLED?OIDC_POLICY.max:60 * 60 * 24 * 30
const TOKEN_PROTECTION_SECRET = env("BODY_WAR_TOKEN_PROTECTION_SECRET", SESSION_SECRET)
const USE_POSTGRES = env("BODY_WAR_AUTH_BACKEND", env("BODY_WAR_DATABASE_URL") ? "postgres" : "memory") === "postgres"
export const STRAVA_FAKE_GATEWAY = env("BODY_WAR_STRAVA_FAKE", process.env.NODE_ENV === "test" ? "1" : "0") === "1"
export const SECURE_COOKIES = env(
  "BODY_WAR_SECURE_COOKIES",
  process.env.NODE_ENV === "production" || PUBLIC_BASE_URL.startsWith("https://") ? "1" : "0",
) !== "0"

function configuredAllowedOrigins(): Set<string> {
  const configured = env("BODY_WAR_ALLOWED_ORIGINS")
  if (configured) {
    return new Set(configured.split(",").map((origin) => origin.trim()).filter(Boolean))
  }
  const origins = new Set([PUBLIC_BASE_URL])
  if (process.env.NODE_ENV !== "production") origins.add(`http://${HOST}:${PORT}`)
  return origins
}

export const ALLOWED_ORIGINS = configuredAllowedOrigins()

const CONTENT_TYPES: Record<string, string> = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
}

type AuthComponents = ReturnType<typeof createAuthComponents>
let singletonAuthComponents: AuthComponents | null = null

export function createAuthComponents(clock?:()=>number) {
  const tokenCodec = createHmacTokenCodec(SESSION_SECRET)
  if (USE_POSTGRES) {
    const sql = createBodyWarSqlClient()
    const database = createBodyWarDatabase(sql)
    const repos = createDrizzleAuthRepositories(database)
    const bodyWarRepo = createDrizzleBodyWarAuthRepository(database)
    const browser = createBrowserSessionAdapter({
      repos,
      tokenCodec,
      config: {
        sessionCookieName: OIDC_ENABLED?SESSION_COOKIE:"bw_session",
        csrfCookieName: "bw_csrf",
        csrfHeaderName: "x-csrf-token",
        allowedOrigins: ALLOWED_ORIGINS,
        secureCookies: SECURE_COOKIES,
        sessionTtlSeconds: SESSION_TTL_SECONDS,
      },
    })
    const strava = createStravaOAuthAdapter({
      authRepos: repos,
      bodyWarRepo,
      config: {
        clientId: env("STRAVA_CLIENT_ID"),
        clientSecret: env("STRAVA_CLIENT_SECRET"),
        redirectUri: STRAVA_REDIRECT_URI,
        publicBaseUrl: PUBLIC_BASE_URL,
        fakeGateway: STRAVA_FAKE_GATEWAY,
        tokenProtectionSecret: TOKEN_PROTECTION_SECRET,
      },
    })
    const oidc=OIDC_ENABLED?oidcFactory({browser,repos,bodyWarRepo,secret:env("BODY_WAR_OIDC_CLIENT_SECRET"),clock}):null;
    return { repos, bodyWarRepo, browser:oidc?.browser??browser, strava, sql, oidc }
  }

  const repos = createMemoryAuthRepositories()
  const bodyWarRepo = createMemoryBodyWarAuthRepository()
  const browser = createBrowserSessionAdapter({
    repos,
    tokenCodec,
    config: {
      sessionCookieName: OIDC_ENABLED?SESSION_COOKIE:"bw_session",
      csrfCookieName: "bw_csrf",
      csrfHeaderName: "x-csrf-token",
      allowedOrigins: ALLOWED_ORIGINS,
      secureCookies: SECURE_COOKIES,
      sessionTtlSeconds: SESSION_TTL_SECONDS,
    },
  })
  const strava = createStravaOAuthAdapter({
    authRepos: repos,
    bodyWarRepo,
    config: {
      clientId: env("STRAVA_CLIENT_ID"),
      clientSecret: env("STRAVA_CLIENT_SECRET"),
      redirectUri: STRAVA_REDIRECT_URI,
      publicBaseUrl: PUBLIC_BASE_URL,
      fakeGateway: STRAVA_FAKE_GATEWAY,
      tokenProtectionSecret: TOKEN_PROTECTION_SECRET,
    },
  })
  const oidc=OIDC_ENABLED?oidcFactory({browser,repos,bodyWarRepo,secret:env("BODY_WAR_OIDC_CLIENT_SECRET"),clock}):null;
  return { repos, bodyWarRepo, browser:oidc?.browser??browser, strava, sql: null, oidc }
}

export function authComponents() {
  singletonAuthComponents ??= createAuthComponents()
  return singletonAuthComponents
}

export function resetAuthComponentsForTests(clock?:()=>number): void {
  singletonAuthComponents = clock?createAuthComponents(clock):null
}

function headerRecord(request: IncomingMessage): Record<string, string | undefined> {
  const headers: Record<string, string | undefined> = {}
  for (const [key, value] of Object.entries(request.headers)) {
    headers[key] = Array.isArray(value) ? value.join(", ") : value
  }
  return headers
}

function cookies(request: IncomingMessage): CookieMap {
  return parseCookieHeader(request.headers.cookie)
}

export function sendJson(response: ServerResponse, status: number, payload: unknown, setCookies: string[] = []): void {
  const body = Buffer.from(`${JSON.stringify(payload, null, 2)}\n`, "utf8")
  response.statusCode = status
  response.setHeader("content-type", "application/json; charset=utf-8")
  response.setHeader("content-length", body.byteLength)
  for (const cookie of setCookies) response.appendHeader("set-cookie", cookie)
  response.end(body)
}

function sendError(response: ServerResponse, error: AppError): void {
  sendJson(response, error.status, { error: error.code, message: error.message, details: error.details })
}

function redirect(response: ServerResponse, location: string, setCookies: string[] = []): void {
  response.statusCode = 302
  response.setHeader("location", location)
  for (const cookie of setCookies) response.appendHeader("set-cookie", cookie)
  response.end()
}

export function stravaProfileUrl(providerUserId: unknown): string | null {
  const id = typeof providerUserId === "number"
    ? String(providerUserId)
    : typeof providerUserId === "string"
      ? providerUserId.trim()
      : ""
  if (!/^\d+$/.test(id)) return null
  return `https://www.strava.com/athletes/${id}`
}

function publicBodyWarAthlete(account: ProviderAccount | null): JsonRecord | null {
  if (!account) return null
  const athlete = account.metadata?.athlete
  const athleteRecord = athlete && typeof athlete === "object" && !Array.isArray(athlete)
    ? (athlete as JsonRecord)
    : {}
  const providerUserId = athleteRecord.id ?? account.providerUserId
  return {
    id: providerUserId,
    firstname: athleteRecord.firstname,
    lastname: athleteRecord.lastname,
    profile: athleteRecord.profile,
    strava_profile_url: stravaProfileUrl(providerUserId),
    scope: account.scope,
    provider: account.provider,
    status: account.status,
  }
}

export function publicRunnerProfile(input: {
  auth: AuthContext
  profile: RunnerProfile | null
  account: ProviderAccount | null
}): JsonRecord {
  const athlete = publicBodyWarAthlete(input.account)
  const athleteName = athlete
    ? [athlete.firstname, athlete.lastname].filter(Boolean).join(" ").trim()
    : ""
  return {
    principal_id: input.auth.principalId,
    display_name: (input.profile?.displayName ?? athleteName) || input.auth.principalId,
    principal_status: "active",
    session: {
      expires_at: input.auth.expiresAt,
    },
    strava: {
      connected: !!input.account && input.account.status === "linked",
      account: athlete,
      profile_url: athlete?.strava_profile_url ?? null,
    },
    privacy: {
      provider_tokens: "server_only",
      activity_import: "redacted_summaries",
      csrf: "required_for_unsafe_methods",
    },
    validation: {
      taquaral_activity: "consent_required",
      route_geometry: "deferred",
      scoring: "deferred",
    },
  }
}

export function publicActivityImportReceipt(input: {
  principalId: string
  summaryCount: number
  importedAt?: string
}): JsonRecord {
  return {
    source: "strava",
    principal_id: input.principalId,
    imported_at: input.importedAt ?? new Date().toISOString(),
    summary_count: input.summaryCount,
    redaction: {
      provider_tokens: "server_only",
      raw_private_payload: "omitted",
      maps: "omitted",
      notes: "omitted",
    },
    consent: {
      friend_fixture: "required_before_real_friend_activity",
    },
    authority: {
      activity_summary: "imported",
      route_geometry: "not_claimed",
      scoring: "not_claimed",
    },
  }
}

function publicSuggestedTrack(track: SuggestedTrack): JsonRecord {
  return {
    id: track.id,
    slug: track.slug,
    name: track.name,
    place_label: track.placeLabel,
    city: track.city,
    country: track.country,
    distance_hint_meters: track.distanceHintMeters,
    status: track.status,
    geometry_authority: track.geometryAuthority,
    suggested_by: track.suggestedByPrincipalId ? "connected_runner" : "seed",
    public_note: track.publicNote,
    created_at: track.createdAt,
    updated_at: track.updatedAt,
    authority: {
      route_geometry: track.geometryAuthority === "source_backed" ? "source_backed" : "not_claimed",
      scoring: "not_claimed",
      pilot_ready: "not_claimed",
    },
  }
}

function publicActivityEvidenceCandidate(candidate: ActivityEvidenceCandidate): JsonRecord {
  return {
    id: candidate.id,
    suggested_track_id: candidate.suggestedTrackId,
    provider: candidate.provider,
    provider_activity_id: candidate.providerActivityId,
    redacted_summary: candidate.redactedSummary,
    consented_at: candidate.consentedAt,
    status: candidate.status,
    created_at: candidate.createdAt,
    updated_at: candidate.updatedAt,
    authority: {
      activity_summary: "redacted_candidate",
      route_geometry: "not_claimed",
      scoring: "not_claimed",
    },
  }
}

function publicSuggestedTrackEvidenceSummary(candidates: ActivityEvidenceCandidate[]): JsonRecord {
  return {
    candidate_count: candidates.length,
    redaction: {
      provider_tokens: "server_only",
      raw_private_payload: "omitted",
      maps: "omitted",
      notes: "omitted",
    },
    authority: {
      activity_summary: candidates.length > 0 ? "candidate_submitted" : "none",
      route_geometry: "not_claimed",
      scoring: "not_claimed",
      pilot_ready: "not_claimed",
    },
  }
}

function redactedActivitySummary(activity: ActivitySummary): JsonRecord {
  return project("RedactedActivity", activity);
}

export async function handleStatus(response: ServerResponse, request: IncomingMessage): Promise<void> {
  const { browser, strava } = authComponents()
  let authenticated = false
  let connected = false
  let account: ProviderAccount | null = null
  const auth = await browser.authenticate({
    cookies: cookies(request),
    method: "GET",
    headers: headerRecord(request),
  })
  if (auth.ok) {
    authenticated = true
    const connection = await strava.connectionStatus(auth.value.principalId)
    connected = connection.connected
    account = connection.account
  }
  sendJson(response, 200, {
    ...(OIDC_ENABLED?{identity_mode:"oidc",security_available:IDENTITY_MODE==="oidc-durable",login_uri:"/api/auth/oidc/start",session_state:auth.ok?"active":auth.error.code}:{}),
    configured: strava.configured(),
    authenticated,
    connected,
    athlete: publicBodyWarAthlete(account),
    redirect_uri: STRAVA_REDIRECT_URI,
    scope: DEFAULT_STRAVA_SCOPE,
  })
}

export async function handleProfile(response: ServerResponse, request: IncomingMessage): Promise<void> {
  const { bodyWarRepo, browser, strava } = authComponents()
  const auth = await browser.authenticate({
    cookies: cookies(request),
    method: "GET",
    headers: headerRecord(request),
    route: "GET /api/profile",
  })
  if (!auth.ok) {
    sendError(response, auth.error)
    return
  }
  const [profile, connection] = await Promise.all([
    bodyWarRepo.findRunnerProfile(auth.value.principalId),
    strava.connectionStatus(auth.value.principalId),
  ])
  sendJson(response, 200, {
    profile: publicRunnerProfile({
      auth: auth.value,
      profile,
      account: connection.account,
    }),
  })
}

export async function handleOidcStart(response:ServerResponse,request:IncomingMessage):Promise<void>{const oidc=authComponents().oidc;if(!oidc){sendJson(response,404,{error:"oidc_disabled"});return;}await oidc.start(request,response);}
export async function handleOidcCallback(response:ServerResponse,url:URL,request:IncomingMessage):Promise<void>{const oidc=authComponents().oidc;if(!oidc){sendJson(response,404,{error:"oidc_disabled"});return;}await oidc.callback(request,response,new URL(url.pathname+url.search,OIDC_POLICY.origin));}
export async function handleStravaStart(response: ServerResponse,request?:IncomingMessage): Promise<void> {
  const { strava,browser,oidc } = authComponents()
  let pending=stravaPrincipalPlaceholder();
  if(oidc){
   if(!request||request.method!=="POST"){sendJson(response,405,{error:"use_authenticated_provider_link"});return;}
   const auth=await browser.authenticate({cookies:cookies(request),method:"POST",headers:headerRecord(request)});
   if(!auth.ok){sendError(response,auth.error);return;}
   pending=(await oidc.linkBinding(cookies(request))).nonce;
  }
  if (!strava.configured()) {
    sendJson(response, 400, {
      error: "strava_not_configured",
      message: "Set STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET in projects/body-war/app/.env.",
    })
    return
  }
  const started = await strava.start(pending, DEFAULT_STRAVA_SCOPE)
  if (!started.ok) {
    sendError(response, started.error)
    return
  }
  const stateCookie=`bw_state=${encodeURIComponent(started.value.state)}; ${SECURE_COOKIES?"Secure; ":""}HttpOnly; SameSite=Lax; Path=/; Max-Age=600`;
  if(oidc)sendJson(response,200,{url:started.value.url},[stateCookie]);
  else redirect(response,started.value.url,[stateCookie]);
}

export async function handleStravaCallback(response: ServerResponse, url: URL, request: IncomingMessage): Promise<void> {
  const providerError = url.searchParams.get("error")
  if (providerError) {
    redirect(response, `/?auth_error=${encodeURIComponent(providerError)}`)
    return
  }
  const code = url.searchParams.get("code") ?? ""
  const state = url.searchParams.get("state") ?? ""
  if (!code || !state || cookies(request).bw_state !== state) {
    redirect(response, "/?auth_error=invalid_state")
    return
  }

  const { browser, strava,oidc } = authComponents()
  let link;try{link=oidc?await oidc.linkBinding(cookies(request)):undefined;}catch{redirect(response,"/?auth_error=provider_link_session_expired");return;}
  const completed = await strava.callback(code, state,link)
  if (!completed.ok) {
    redirect(response, `/?auth_error=${encodeURIComponent(completed.error.code)}`)
    return
  }
  if(oidc){redirect(response,"/?connected=1",["bw_state=; Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age=0"]);return;}
  const created = await browser.createSession({
    principalId: completed.value.principalId,
    metadata: { provider: "strava" },
  })
  if (!created.ok) {
    redirect(response, `/?auth_error=${encodeURIComponent(created.error.code)}`)
    return
  }
  redirect(response, "/?connected=1", [
    browser.sessionCookieHeader(created.value.binding, SESSION_TTL_SECONDS),
    browser.csrfCookieHeader(created.value.binding, SESSION_TTL_SECONDS),
    "bw_state=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0",
  ])
}

export async function handleActivities(response: ServerResponse, request: IncomingMessage, url: URL): Promise<void> {
  const { browser, strava } = authComponents()
  const auth = await browser.authenticate({
    cookies: cookies(request),
    method: "GET",
    headers: headerRecord(request),
    requiredPermission: "body-war.activity.read",
    route: "GET /api/activities",
  })
  if (!auth.ok) {
    sendError(response, auth.error)
    return
  }
  const query = readQuery(url,"ListActivities")
  const activities = await strava.listActivitySummaries(
    auth.value.principalId,
    query.page!,
    query.per_page!,
  )
  if (!activities.ok) {
    sendError(response, activities.error)
    return
  }
  sendJson(response, 200, {
    activities: activities.value,
    receipt: publicActivityImportReceipt({
      principalId: auth.value.principalId,
      summaryCount: activities.value.length,
    }),
  })
}

async function authenticateSuggestedTrackRunner(
  request: IncomingMessage,
  response: ServerResponse,
  method: string,
  route: string,
  requiredPermission: string,
): Promise<AuthContext | null> {
  const { browser, strava } = authComponents()
  const auth = await browser.authenticate({
    cookies: cookies(request),
    method,
    headers: headerRecord(request),
    requiredPermission,
    route,
  })
  if (!auth.ok) {
    sendError(response, auth.error)
    return null
  }

  const connection = await strava.connectionStatus(auth.value.principalId)
  if (!connection.connected) {
    sendError(response, appError("strava_not_connected", 409, "Strava account is not connected"))
    return null
  }

  return auth.value
}

export async function handleSuggestedTracksList(response: ServerResponse, request: IncomingMessage): Promise<void> {
  const auth = await authenticateSuggestedTrackRunner(
    request,
    response,
    "GET",
    "GET /api/suggested-tracks",
    "body-war.suggested-track.read",
  )
  if (!auth) return

  const { bodyWarRepo } = authComponents()
  const tracks = await bodyWarRepo.listSuggestedTracks()
  sendJson(response, 200, {
    suggested_tracks: tracks.map(publicSuggestedTrack),
  })
}

export async function handleSuggestedTrackCreate(response: ServerResponse, request: IncomingMessage): Promise<void> {
  const payload = await readRequest(request,"CreateTrack")
  const auth = await authenticateSuggestedTrackRunner(
    request,
    response,
    "POST",
    "POST /api/suggested-tracks",
    "body-war.suggested-track.create",
  )
  if (!auth) return

  const name = payload.name as string
  const placeLabel = payload.place_label as string
  const city = payload.city as string
  const publicNote = payload.public_note as string
  const distanceHintMeters = payload.distance_hint_meters as number | null

  const { bodyWarRepo } = authComponents()
  const track = await bodyWarRepo.createSuggestedTrack({
    principalId: auth.principalId,
    name,
    placeLabel,
    city,
    country: "BR",
    distanceHintMeters,
    publicNote,
  })
  sendJson(response, 201, { suggested_track: publicSuggestedTrack(track) })
}

export async function handleSuggestedTrackDetail(
  response: ServerResponse,
  request: IncomingMessage,
  idOrSlug: string,
): Promise<void> {
  const auth = await authenticateSuggestedTrackRunner(
    request,
    response,
    "GET",
    "GET /api/suggested-tracks/:id",
    "body-war.suggested-track.read",
  )
  if (!auth) return

  const { bodyWarRepo } = authComponents()
  const track = await bodyWarRepo.findSuggestedTrack(idOrSlug)
  if (!track) {
    sendError(response, appError("suggested_track_not_found", 404, "Suggested track was not found"))
    return
  }

  const [allCandidates, myCandidates] = await Promise.all([
    bodyWarRepo.listActivityEvidenceCandidates(track.id),
    bodyWarRepo.listActivityEvidenceCandidates(track.id, auth.principalId),
  ])
  sendJson(response, 200, {
    suggested_track: publicSuggestedTrack(track),
    my_evidence_candidates: myCandidates.map(publicActivityEvidenceCandidate),
    evidence_summary: publicSuggestedTrackEvidenceSummary(allCandidates),
  })
}

export async function handleSuggestedTrackEvidenceCreate(
  response: ServerResponse,
  request: IncomingMessage,
  idOrSlug: string,
): Promise<void> {
  const payload = await readRequest(request,"AttachEvidence")
  const auth = await authenticateSuggestedTrackRunner(
    request,
    response,
    "POST",
    "POST /api/suggested-tracks/:id/evidence-candidates",
    "body-war.suggested-track-evidence.create",
  )
  if (!auth) return

  const activityId = payload.activity_id as string
  const consentText = payload.consent_text as string
  const consentAcknowledged = payload.consent_acknowledged === true
  if (!evidenceConsentRequired({ consent_acknowledged: consentAcknowledged, activity_present: Boolean(activityId), consent_text_present: Boolean(consentText) })) {
    sendError(response, appError("consent_required", 400, "Explicit consent and activity_id are required"))
    return
  }

  const { bodyWarRepo, strava } = authComponents()
  const track = await bodyWarRepo.findSuggestedTrack(idOrSlug)
  if (!track) {
    sendError(response, appError("suggested_track_not_found", 404, "Suggested track was not found"))
    return
  }

  const existingCandidates = await bodyWarRepo.listActivityEvidenceCandidates(
    track.id,
    auth.principalId,
  )
  if (existingCandidates.some((candidate) => candidate.providerActivityId === activityId)) {
    sendError(response, appError(
      "evidence_candidate_replay",
      409,
      "This activity already has evidence for this suggested track",
    ))
    return
  }

  const activities=await strava.listActivitySummaries(auth.principalId,"1","50");
  if(!activities.ok){sendError(response,activities.error);return;}
  const activity=activities.value.find(candidate=>String(candidate.id)===activityId);
  if(!activity){sendError(response,appError("invalid_activity",400,"Activity is not available for this runner"));return;}

  let candidate;
  try { candidate = await bodyWarRepo.addActivityEvidenceCandidate({
    suggestedTrackId: track.id,
    principalId: auth.principalId,
    providerActivityId: activity.id,
    redactedSummary: redactedActivitySummary(activity),
    consentText,
    consentedAt: new Date().toISOString(),
  })
  } catch(error) {
    if((error as {code?:string}).code === "evidence_candidate_replay") {sendError(response,appError("evidence_candidate_replay",409,"This activity already has evidence for this suggested track"));return;}
    throw error;
  }
  const updatedTrack = await bodyWarRepo.findSuggestedTrack(track.id) ?? track
  sendJson(response, 201, {
    evidence_candidate: publicActivityEvidenceCandidate(candidate),
    suggested_track: publicSuggestedTrack(updatedTrack),
  })
}

export async function handleLogout(response: ServerResponse, request: IncomingMessage): Promise<void> {
  const { browser } = authComponents()
  const auth = await browser.authenticate({
    cookies: cookies(request),
    method: "POST",
    headers: headerRecord(request),
    route: "POST /api/auth/logout",
  })
  if (!auth.ok && !["auth_required", "invalid_session", "session_expired"].includes(auth.error.code)) {
    sendError(response, auth.error)
    return
  }
  await browser.logout(cookies(request))
  sendJson(response, 200, { ok: true }, browser.clearCookieHeaders())
}

export async function serveStatic(response: ServerResponse, pathname: string): Promise<void> {
  const requested = resolve(STATIC_DIR, pathname.replace(/^\/+/, "") || "index.html")
  const target = requested.startsWith(STATIC_DIR) && existsSync(requested)
    ? requested
    : resolve(STATIC_DIR, "index.html")
  const body = await readFile(target)
  response.statusCode = 200
  response.setHeader("content-type", CONTENT_TYPES[extname(target)] ?? "application/octet-stream")
  response.setHeader("content-length", body.byteLength)
  response.end(body)
}


export async function authorizeOperation(request: IncomingMessage, response: ServerResponse, contract: {
  authentication: string; permission: string | null; method: string; route: string;
}): Promise<boolean> {
  if(OIDC_ENABLED&&contract.authentication!=="public"&&request.method!=="OPTIONS"){
   response.once("finish",()=>{if(response.statusCode<400&&!contract.route.includes("/api/status")&&!contract.route.includes("/api/auth/"))authComponents().oidc?.touch(cookies(request));});
  }
  if (contract.authentication === "public") return true;
  if (!["session", "connected", "optional-session"].includes(contract.authentication)) throw Error("UNKNOWN_AUTHENTICATION_CONTRACT");
  const { browser, strava } = authComponents();
  const result = await browser.authenticate({cookies:cookies(request), method:contract.method, headers:headerRecord(request), route:contract.route,
    ...(contract.permission ? {requiredPermission:contract.permission} : {})});
  if (!result.ok) {
    if (contract.authentication === "optional-session" && ["auth_required", "invalid_session", "session_expired"].includes(result.error.code)) return true;
    sendError(response, result.error); return false;
  }
  if (contract.authentication === "connected" && !(await strava.connectionStatus(result.value.principalId)).connected) {
    sendError(response, appError("strava_not_connected",409,"Strava account is not connected")); return false;
  }
  return true;
}

export async function handleSecurity(response:ServerResponse,request:IncomingMessage):Promise<void>{const oidc=authComponents().oidc;if(!oidc||!("security" in oidc)||typeof oidc.security!=="function"){sendJson(response,404,{error:"security_unavailable"});return;}await oidc.security(request,response);}

export async function handleEvidenceWithdraw(response: ServerResponse, request: IncomingMessage, id: string): Promise<void> {
  await readRequest(request, "WithdrawEvidence");
  const { browser, bodyWarRepo } = authComponents();
  const auth = await browser.authenticate({cookies: cookies(request), method: "POST", headers: headerRecord(request), route: "POST /api/evidence-candidates/:id/withdraw"});
  if (!auth.ok) { sendError(response, auth.error); return; }
  // PostgreSQL UUID columns must not turn an arbitrary public ID into a 500.
  if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) {
    await bodyWarRepo.disposeActivityEvidenceCandidate({candidateId: id, principalId: auth.value.principalId, reason: "consent_revocation"});
  }
  sendJson(response, 200, {withdrawn: true});
}
