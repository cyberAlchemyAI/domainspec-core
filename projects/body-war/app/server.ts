import {
  createDrizzleAuthRepositories,
  createHmacTokenCodec,
  createMemoryAuthRepositories,
  type AuthContext,
} from "@domainspec/auth-user-management"
import { createServer, type IncomingMessage, type ServerResponse } from "node:http"
import { mkdir, readFile, writeFile } from "node:fs/promises"
import { existsSync, readFileSync } from "node:fs"
import { dirname, extname, resolve } from "node:path"
import { createBrowserSessionAdapter } from "./src/auth/browser-session.js"
import { parseCookieHeader } from "./src/auth/cookies.js"
import { createDrizzleBodyWarAuthRepository } from "./src/auth/drizzle-repository.js"
import { createMemoryBodyWarAuthRepository } from "./src/auth/memory-repository.js"
import {
  DEFAULT_STRAVA_SCOPE,
  createStravaOAuthAdapter,
  stravaPrincipalPlaceholder,
} from "./src/auth/strava-oauth.js"
import type { AppError, CookieMap, JsonRecord, ProviderAccount, RunnerProfile } from "./src/auth/types.js"
import { createBodyWarDatabase, createBodyWarSqlClient } from "./src/infrastructure/postgres/database.js"

const APP_ROOT = resolve(process.env.BODY_WAR_APP_ROOT ?? process.cwd())
const STATIC_DIR = resolve(APP_ROOT, "static")
const DATA_DIR = resolve(APP_ROOT, "data")
const SUBMISSION_STORE = resolve(DATA_DIR, "track-submissions.json")
const TRACK_STORE = resolve(DATA_DIR, "tracks.json")

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
const SESSION_TTL_SECONDS = 60 * 60 * 24 * 30
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

async function writeJson(path: string, value: unknown): Promise<void> {
  await mkdir(dirname(path), { recursive: true })
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, "utf8")
}

async function readJson<T>(path: string, fallback: T): Promise<T> {
  try {
    return JSON.parse(await readFile(path, "utf8")) as T
  } catch {
    return fallback
  }
}

export async function ensureDefaultFiles(): Promise<void> {
  await mkdir(DATA_DIR, { recursive: true })
  if (!existsSync(SUBMISSION_STORE)) {
    await writeJson(SUBMISSION_STORE, { submissions: [] })
  }
  if (!existsSync(TRACK_STORE)) {
    await writeJson(TRACK_STORE, {
      tracks: [
        {
          id: "craft-distill-blocker",
          name: "Craft Distill Blocker",
          pilot: "internal",
          description: "Aggregate Refine receipt status, grounded by recursive ledger evidence.",
          controller_metric: "aggregate_refine_receipt_status",
        },
        {
          id: "park-track-alpha",
          name: "Park Track Alpha",
          pilot: "body-war",
          description: "Placeholder physical track for the later real-world runner pilot.",
          controller_metric: "fastest_verified_time",
        },
      ],
    })
  }
}

type AuthComponents = ReturnType<typeof createAuthComponents>
let singletonAuthComponents: AuthComponents | null = null

export function createAuthComponents() {
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
        sessionCookieName: "bw_session",
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
    return { repos, bodyWarRepo, browser, strava, sql }
  }

  const repos = createMemoryAuthRepositories()
  const bodyWarRepo = createMemoryBodyWarAuthRepository()
  const browser = createBrowserSessionAdapter({
    repos,
    tokenCodec,
    config: {
      sessionCookieName: "bw_session",
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
  return { repos, bodyWarRepo, browser, strava, sql: null }
}

export function authComponents() {
  singletonAuthComponents ??= createAuthComponents()
  return singletonAuthComponents
}

export function resetAuthComponentsForTests(): void {
  singletonAuthComponents = null
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

function sendJson(response: ServerResponse, status: number, payload: unknown, setCookies: string[] = []): void {
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

async function readBodyJson(request: IncomingMessage): Promise<JsonRecord> {
  const chunks: Buffer[] = []
  for await (const chunk of request) chunks.push(Buffer.from(chunk))
  if (!chunks.length) return {}
  const text = Buffer.concat(chunks).toString("utf8")
  return text ? (JSON.parse(text) as JsonRecord) : {}
}

async function handleStatus(response: ServerResponse, request: IncomingMessage): Promise<void> {
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
    configured: strava.configured(),
    authenticated,
    connected,
    athlete: publicBodyWarAthlete(account),
    redirect_uri: STRAVA_REDIRECT_URI,
    scope: DEFAULT_STRAVA_SCOPE,
  })
}

async function handleProfile(response: ServerResponse, request: IncomingMessage): Promise<void> {
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

async function handleStravaStart(response: ServerResponse): Promise<void> {
  const { strava } = authComponents()
  if (!strava.configured()) {
    sendJson(response, 400, {
      error: "strava_not_configured",
      message: "Set STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET in projects/body-war/app/.env.",
    })
    return
  }
  const started = await strava.start(stravaPrincipalPlaceholder(), DEFAULT_STRAVA_SCOPE)
  if (!started.ok) {
    sendError(response, started.error)
    return
  }
  redirect(response, started.value.url, [
    `bw_state=${encodeURIComponent(started.value.state)}; HttpOnly; SameSite=Lax; Path=/; Max-Age=600`,
  ])
}

async function handleStravaCallback(response: ServerResponse, url: URL, request: IncomingMessage): Promise<void> {
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

  const { browser, strava } = authComponents()
  const completed = await strava.callback(code, state)
  if (!completed.ok) {
    redirect(response, `/?auth_error=${encodeURIComponent(completed.error.code)}`)
    return
  }
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

async function handleActivities(response: ServerResponse, request: IncomingMessage, url: URL): Promise<void> {
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
  const activities = await strava.listActivitySummaries(
    auth.value.principalId,
    url.searchParams.get("page") ?? "1",
    url.searchParams.get("per_page") ?? "20",
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

async function handleLogout(response: ServerResponse, request: IncomingMessage): Promise<void> {
  const { browser } = authComponents()
  const auth = await browser.authenticate({
    cookies: cookies(request),
    method: "POST",
    headers: headerRecord(request),
    route: "POST /api/auth/logout",
  })
  if (!auth.ok && !["auth_required", "invalid_session"].includes(auth.error.code)) {
    sendError(response, auth.error)
    return
  }
  await browser.logout(cookies(request))
  sendJson(response, 200, { ok: true }, browser.clearCookieHeaders())
}

async function handleSubmission(response: ServerResponse, request: IncomingMessage): Promise<void> {
  const payload = await readBodyJson(request)
  const trackId = typeof payload.track_id === "string" ? payload.track_id : ""
  const { browser, strava } = authComponents()
  const auth = await browser.authenticate({
    cookies: cookies(request),
    method: "POST",
    headers: headerRecord(request),
    requiredPermission: "body-war.submission.create",
    route: "POST /api/submissions",
  })
  if (!auth.ok) {
    sendError(response, auth.error)
    return
  }

  const connection = await strava.connectionStatus(auth.value.principalId)
  const athlete = publicBodyWarAthlete(connection.account) ?? {}
  const submission = {
    id: globalThis.crypto.randomUUID(),
    created_at: Math.floor(Date.now() / 1000),
    athlete_id: athlete.id ?? auth.value.principalId,
    athlete_name: [athlete.firstname, athlete.lastname].filter(Boolean).join(" "),
    track_id: trackId,
    activity_id: payload.activity_id,
    activity_name: payload.activity_name,
    moving_time: payload.moving_time,
    distance: payload.distance,
    average_speed: payload.average_speed,
    status: "submitted",
    authority: "hybrid",
    public_controller_metric: "fastest_verified_time",
    parallel_evidence: "composite_score_pending",
  }
  const store = await readJson<{ submissions: unknown[] }>(SUBMISSION_STORE, { submissions: [] })
  store.submissions.push(submission)
  await writeJson(SUBMISSION_STORE, store)
  sendJson(response, 201, { submission })
}

async function serveStatic(response: ServerResponse, pathname: string): Promise<void> {
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

export async function handleRequest(request: IncomingMessage, response: ServerResponse): Promise<void> {
  const url = new URL(request.url ?? "/", PUBLIC_BASE_URL)
  try {
    if (request.method === "GET" && url.pathname === "/api/status") return handleStatus(response, request)
    if (request.method === "GET" && url.pathname === "/api/profile") return handleProfile(response, request)
    if (request.method === "GET" && url.pathname === "/api/auth/strava/start") return handleStravaStart(response)
    if (request.method === "GET" && url.pathname === "/api/auth/strava/callback") return handleStravaCallback(response, url, request)
    if (request.method === "GET" && url.pathname === "/api/activities") return handleActivities(response, request, url)
    if (request.method === "GET" && url.pathname === "/api/tracks") return sendJson(response, 200, await readJson(TRACK_STORE, { tracks: [] }))
    if (request.method === "GET" && url.pathname === "/api/submissions") return sendJson(response, 200, await readJson(SUBMISSION_STORE, { submissions: [] }))
    if (request.method === "POST" && url.pathname === "/api/auth/logout") return handleLogout(response, request)
    if (request.method === "POST" && url.pathname === "/api/submissions") return handleSubmission(response, request)
    if (url.pathname.startsWith("/api/")) return sendJson(response, 404, { error: "not_found" })
    return serveStatic(response, url.pathname)
  } catch (error) {
    sendJson(response, 500, { error: "internal_error", message: error instanceof Error ? error.message : "Unknown error" })
  }
}

export async function main(): Promise<void> {
  await ensureDefaultFiles()
  const server = createServer((request, response) => {
    void handleRequest(request, response)
  })
  server.listen(PORT, HOST, () => {
    console.log(`Body War pilot app: http://${HOST}:${PORT}`)
    console.log(`Strava callback URL: ${STRAVA_REDIRECT_URI}`)
  })
}

if (process.argv[1]?.endsWith("server.js")) {
  void main()
}
