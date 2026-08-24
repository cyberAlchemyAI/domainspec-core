import { randomBytes, timingSafeEqual } from "node:crypto"
import { chmod, lstat, mkdir, readFile, rename, unlink, writeFile } from "node:fs/promises"
import { createServer, type Server, type ServerResponse } from "node:http"
import { dirname, resolve } from "node:path"

const STRAVA_AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
const STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
const DEFAULT_TIMEOUT_MS = 10 * 60 * 1000

type JsonObject = Record<string, unknown>

type AuthorizationTokenResponse = {
  access_token: string
  refresh_token: string
  expires_at: number
  token_type: string
  scope: string
  athlete: JsonObject & { id: string | number }
}

type TokenStore = {
  athletes: Record<string, JsonObject>
}

export type StravaReconnectOptions = {
  clientId: string
  clientSecret: string
  redirectUri: string
  publicRedirectUri?: string | undefined
  tokensPath: string
  includePrivate: boolean
  addAthlete?: boolean | undefined
  athleteKey?: string | undefined
  fetchImpl?: typeof fetch | undefined
  state?: string | undefined
  timeoutMs?: number | undefined
  tokenUrl?: string | undefined
  authorizeUrl?: string | undefined
  now?: Date | undefined
}

export type StravaReconnectSession = {
  authorizationUrl: string
  requestedScope: string
  completion: Promise<{ acceptedScope: string; tokenStored: true }>
  close: () => Promise<void>
}

export class StravaReconnectError extends Error {
  constructor(readonly code: string, message: string) {
    super(message)
    this.name = "StravaReconnectError"
  }
}

export function validateLoopbackRedirectUri(value: string): URL {
  let redirect: URL
  try {
    redirect = new URL(value)
  } catch {
    throw new StravaReconnectError(
      "invalid_redirect_uri",
      "STRAVA_REDIRECT_URI must be a valid loopback URL",
    )
  }
  if (
    redirect.protocol !== "http:" ||
    redirect.hostname !== "127.0.0.1"
  ) {
    throw new StravaReconnectError(
      "non_loopback_redirect_uri",
      "Geometry reconnect requires an http://127.0.0.1 callback",
    )
  }
  const port = Number(redirect.port)
  if (!Number.isInteger(port) || port < 1024 || port > 65_535) {
    throw new StravaReconnectError(
      "invalid_redirect_port",
      "Geometry reconnect requires an explicit unprivileged loopback port",
    )
  }
  validateCallbackPathAndComponents(redirect)
  return redirect
}

function validateCallbackPathAndComponents(redirect: URL): void {
  if (redirect.pathname !== "/api/auth/strava/callback") {
    throw new StravaReconnectError(
      "invalid_redirect_path",
      "Geometry reconnect requires the /api/auth/strava/callback path",
    )
  }
  if (redirect.username || redirect.password || redirect.search || redirect.hash) {
    throw new StravaReconnectError(
      "invalid_redirect_components",
      "Geometry reconnect callback cannot contain credentials, a query, or a fragment",
    )
  }
}

export function validatePublicRedirectUri(value: string): URL {
  let redirect: URL
  try {
    redirect = new URL(value)
  } catch {
    throw new StravaReconnectError(
      "invalid_public_redirect_uri",
      "Public OAuth redirect must be a valid HTTPS URL",
    )
  }
  if (redirect.protocol !== "https:" || redirect.port) {
    throw new StravaReconnectError(
      "invalid_public_redirect_uri",
      "Public OAuth redirect must use standard-port HTTPS",
    )
  }
  if (
    redirect.hostname === "localhost" ||
    redirect.hostname === "127.0.0.1" ||
    !redirect.hostname.includes(".")
  ) {
    throw new StravaReconnectError(
      "invalid_public_redirect_host",
      "Public OAuth redirect requires a public DNS hostname",
    )
  }
  validateCallbackPathAndComponents(redirect)
  return redirect
}

function validateAuthorizationRedirectUri(value: string): URL {
  let redirect: URL
  try {
    redirect = new URL(value)
  } catch {
    throw new StravaReconnectError(
      "invalid_redirect_uri",
      "OAuth redirect must be a valid URL",
    )
  }
  return redirect.protocol === "http:"
    ? validateLoopbackRedirectUri(value)
    : validatePublicRedirectUri(value)
}

export function buildStravaAuthorizationUrl(input: {
  authorizeUrl?: string | undefined
  clientId: string
  redirectUri: string
  includePrivate: boolean
  state: string
}): { url: string; requestedScope: string } {
  const clientId = requiredNonEmpty(input.clientId, "STRAVA_CLIENT_ID")
  const state = requiredNonEmpty(input.state, "OAuth state")
  validateAuthorizationRedirectUri(input.redirectUri)
  const requestedScope = input.includePrivate
    ? "read,activity:read_all"
    : "read,activity:read"
  const url = new URL(input.authorizeUrl ?? STRAVA_AUTHORIZE_URL)
  url.searchParams.set("client_id", clientId)
  url.searchParams.set("redirect_uri", input.redirectUri)
  url.searchParams.set("response_type", "code")
  url.searchParams.set("approval_prompt", "force")
  url.searchParams.set("scope", requestedScope)
  url.searchParams.set("state", state)
  return { url: url.toString(), requestedScope }
}

export async function exchangeAndPersistAuthorization(input: {
  code: string
  clientId: string
  clientSecret: string
  redirectUri: string
  requestedScope: string
  tokensPath: string
  addAthlete?: boolean | undefined
  athleteKey?: string | undefined
  fetchImpl?: typeof fetch | undefined
  tokenUrl?: string | undefined
  now?: Date | undefined
}): Promise<{ acceptedScope: string; tokenStored: true }> {
  const fetchImpl = input.fetchImpl ?? fetch
  const existingStore = await readAndSecureTokenStore(input.tokensPath)
  const expectedAthleteId = expectedStoredAthleteId(
    existingStore,
    input.addAthlete ?? false,
    input.athleteKey,
  )
  const response = await fetchImpl(input.tokenUrl ?? STRAVA_TOKEN_URL, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: requiredNonEmpty(input.clientId, "STRAVA_CLIENT_ID"),
      client_secret: requiredNonEmpty(input.clientSecret, "STRAVA_CLIENT_SECRET"),
      code: requiredNonEmpty(input.code, "authorization code"),
      grant_type: "authorization_code",
      redirect_uri: input.redirectUri,
    }),
  })
  if (!response.ok) {
    throw new StravaReconnectError(
      `strava_exchange_http_${response.status}`,
      `Strava authorization-code exchange failed with HTTP ${response.status}`,
    )
  }
  const tokenResponse = parseTokenResponse(await response.json())
  const nowSeconds = Math.floor((input.now ?? new Date()).getTime() / 1000)
  if (tokenResponse.expires_at <= nowSeconds) {
    throw new StravaReconnectError(
      "invalid_token_response",
      "Strava token response contains an expired access token",
    )
  }
  requireAcceptedScope(tokenResponse.scope, input.requestedScope)
  const athleteId = String(tokenResponse.athlete.id)
  if (input.addAthlete && existingStore.athletes[athleteId]) {
    throw new StravaReconnectError(
      "athlete_already_present",
      "Add-athlete authorization used an athlete account that is already stored; the token store was not changed",
    )
  }
  if (expectedAthleteId && expectedAthleteId !== athleteId) {
    throw new StravaReconnectError(
      "athlete_mismatch",
      "Strava reconnect used a different athlete account; the token store was not changed",
    )
  }

  existingStore.athletes[athleteId] = {
    athlete: tokenResponse.athlete,
    scope: tokenResponse.scope,
    token_type: tokenResponse.token_type,
    access_token: tokenResponse.access_token,
    refresh_token: tokenResponse.refresh_token,
    expires_at: tokenResponse.expires_at,
    updated_at: nowSeconds,
  }
  await writeJsonAtomic(input.tokensPath, existingStore, 0o600)
  return { acceptedScope: tokenResponse.scope, tokenStored: true }
}

export async function startStravaReconnect(
  options: StravaReconnectOptions,
): Promise<StravaReconnectSession> {
  const listenerRedirect = validateLoopbackRedirectUri(options.redirectUri)
  const authorizationRedirect = options.publicRedirectUri
    ? validatePublicRedirectUri(options.publicRedirectUri)
    : listenerRedirect
  const state = options.state ?? randomBytes(32).toString("base64url")
  const authorization = buildStravaAuthorizationUrl({
    authorizeUrl: options.authorizeUrl,
    clientId: options.clientId,
    redirectUri: authorizationRedirect.toString(),
    includePrivate: options.includePrivate,
    state,
  })
  let server: Server | null = null
  let settled = false
  let processing = false
  let timer: ReturnType<typeof setTimeout> | null = null
  let resolveCompletion: ((value: { acceptedScope: string; tokenStored: true }) => void) | null = null
  let rejectCompletion: ((reason: unknown) => void) | null = null
  const completion = new Promise<{ acceptedScope: string; tokenStored: true }>((resolve, reject) => {
    resolveCompletion = resolve
    rejectCompletion = reject
  })

  const close = async (): Promise<void> => {
    if (timer) clearTimeout(timer)
    timer = null
    if (!server?.listening) return
    await new Promise<void>((resolveClose, rejectClose) => {
      server?.close((error) => error ? rejectClose(error) : resolveClose())
    })
  }

  const finish = async (
    result: { acceptedScope: string; tokenStored: true } | null,
    error: unknown,
  ): Promise<void> => {
    if (settled) return
    settled = true
    if (timer) clearTimeout(timer)
    timer = null
    await close().catch(() => undefined)
    if (error) rejectCompletion?.(error)
    else if (result) resolveCompletion?.(result)
  }

  server = createServer((request, response) => {
    void (async () => {
      const requestUrl = new URL(request.url ?? "/", authorizationRedirect.origin)
      if (
        request.method !== "GET" ||
        requestUrl.pathname !== authorizationRedirect.pathname ||
        request.headers.host !== authorizationRedirect.host
      ) {
        sendText(response, 404, "Not found")
        return
      }
      const returnedStates = requestUrl.searchParams.getAll("state")
      const returnedState = returnedStates.length === 1 ? returnedStates[0] ?? "" : ""
      if (!constantTimeEqual(returnedState, state)) {
        sendText(response, 400, "Invalid OAuth state. This reconnect session is still waiting.")
        return
      }
      if (processing || settled) {
        sendText(response, 409, "This reconnect callback is already being processed.")
        return
      }
      processing = true
      const providerErrors = requestUrl.searchParams.getAll("error")
      const providerError = providerErrors.length === 1 ? providerErrors[0] : null
      if (providerError) {
        sendText(response, 400, "Strava authorization was not granted. You may close this tab.")
        await finish(
          null,
          new StravaReconnectError("authorization_not_granted", "Strava authorization was not granted"),
        )
        return
      }
      const codes = requestUrl.searchParams.getAll("code")
      const code = codes.length === 1 ? codes[0] ?? "" : ""
      if (!code) {
        sendText(response, 400, "Strava callback did not include an authorization code.")
        await finish(
          null,
          new StravaReconnectError("missing_authorization_code", "Strava callback did not include a code"),
        )
        return
      }
      try {
        const result = await exchangeAndPersistAuthorization({
          code,
          clientId: options.clientId,
          clientSecret: options.clientSecret,
          redirectUri: authorizationRedirect.toString(),
          requestedScope: authorization.requestedScope,
          tokensPath: options.tokensPath,
          addAthlete: options.addAthlete,
          athleteKey: options.athleteKey,
          fetchImpl: options.fetchImpl,
          tokenUrl: options.tokenUrl,
          now: options.now,
        })
        sendHtml(
          response,
          200,
          "<h1>Body War reconnect complete</h1><p>The private token store was updated. You may close this tab.</p>",
        )
        await finish(result, null)
      } catch (error) {
        sendText(response, 502, "Strava reconnect failed without changing the token store.")
        await finish(null, error)
      }
    })()
  })

  await new Promise<void>((resolveListen, rejectListen) => {
    server?.once("error", (error) => rejectListen(error))
    server?.listen(Number(listenerRedirect.port), "127.0.0.1", resolveListen)
  }).catch((error: unknown) => {
    throw new StravaReconnectError(
      "callback_listener_unavailable",
      error instanceof Error
        ? `Could not start the loopback callback listener: ${error.message}`
        : "Could not start the loopback callback listener",
    )
  })

  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS
  timer = setTimeout(() => {
    void finish(
      null,
      new StravaReconnectError("authorization_timeout", "Strava authorization timed out"),
    )
  }, timeoutMs)

  return {
    authorizationUrl: authorization.url,
    requestedScope: authorization.requestedScope,
    completion,
    close,
  }
}

function parseTokenResponse(value: unknown): AuthorizationTokenResponse {
  if (!isObject(value) || !isObject(value.athlete)) {
    throw new StravaReconnectError(
      "invalid_token_response",
      "Strava token response is missing the athlete record",
    )
  }
  const athleteId = value.athlete.id
  if ((typeof athleteId !== "string" && typeof athleteId !== "number") || String(athleteId).length === 0) {
    throw new StravaReconnectError(
      "invalid_token_response",
      "Strava token response is missing athlete.id",
    )
  }
  return {
    access_token: requiredStringField(value, "access_token"),
    refresh_token: requiredStringField(value, "refresh_token"),
    expires_at: requiredNumberField(value, "expires_at"),
    token_type: parseTokenType(value.token_type),
    scope: requiredStringField(value, "scope"),
    athlete: { ...value.athlete, id: athleteId },
  }
}

function requireAcceptedScope(accepted: string, requested: string): void {
  const acceptedScopes = new Set(accepted.split(/[ ,]+/).filter(Boolean))
  const requestedScopes = requested.split(/[ ,]+/).filter(Boolean)
  const missing = requestedScopes.filter((scope) => {
    if (scope === "activity:read" && acceptedScopes.has("activity:read_all")) return false
    return !acceptedScopes.has(scope)
  })
  if (missing.length > 0) {
    throw new StravaReconnectError(
      "required_scope_not_granted",
      "Strava did not grant every scope required by this reconnect",
    )
  }
}

async function readAndSecureTokenStore(path: string): Promise<TokenStore> {
  let parsed: unknown
  try {
    const metadata = await lstat(path)
    if (!metadata.isFile() || metadata.isSymbolicLink()) {
      throw new Error("token target is not a regular file")
    }
    await chmod(path, 0o600)
    parsed = JSON.parse(await readFile(path, "utf8")) as unknown
  } catch {
    throw new StravaReconnectError(
      "token_store_unavailable",
      "The existing private token store could not be secured and read",
    )
  }
  if (!isObject(parsed) || !isObject(parsed.athletes)) {
    throw new StravaReconnectError(
      "invalid_token_store",
      "The existing token store must contain an athletes object",
    )
  }
  const athletes: Record<string, JsonObject> = {}
  for (const [key, value] of Object.entries(parsed.athletes)) {
    if (!isObject(value)) {
      throw new StravaReconnectError(
        "invalid_token_store",
        "Every token-store athlete entry must be an object",
      )
    }
    athletes[key] = value
  }
  return { athletes }
}

function expectedStoredAthleteId(
  store: TokenStore,
  addAthlete: boolean,
  athleteKey: string | undefined,
): string | null {
  if (addAthlete && athleteKey) {
    throw new StravaReconnectError(
      "conflicting_athlete_selection",
      "--add-athlete and --athlete-key cannot be used together",
    )
  }
  if (addAthlete) return null
  if (athleteKey) {
    const record = store.athletes[athleteKey]
    if (!record) {
      throw new StravaReconnectError(
        "unknown_token_athlete",
        "The selected token athlete key does not exist",
      )
    }
    return storedAthleteId(athleteKey, record)
  }
  const entries = Object.entries(store.athletes)
  if (entries.length > 1) {
    throw new StravaReconnectError(
      "ambiguous_token_store",
      "The token store contains multiple athletes; pass --athlete-key or --add-athlete explicitly",
    )
  }
  const entry = entries[0]
  if (!entry) return null
  return storedAthleteId(entry[0], entry[1])
}

function storedAthleteId(key: string, record: JsonObject): string {
  const embeddedId = isObject(record.athlete) ? record.athlete.id : null
  return embeddedId === null || embeddedId === undefined ? key : String(embeddedId)
}

async function writeJsonAtomic(path: string, value: unknown, mode: number): Promise<void> {
  const absolutePath = resolve(path)
  const parent = dirname(absolutePath)
  await mkdir(parent, { recursive: true, mode: 0o700 })
  await chmod(parent, 0o700)
  const temporaryPath = `${absolutePath}.tmp-${process.pid}`
  try {
    await writeFile(temporaryPath, `${JSON.stringify(value, null, 2)}\n`, { mode })
    await chmod(temporaryPath, mode)
    await rename(temporaryPath, absolutePath)
  } catch (error) {
    await unlink(temporaryPath).catch(() => undefined)
    throw error
  }
}

function sendText(
  response: ServerResponse,
  status: number,
  text: string,
): void {
  response.writeHead(status, securityHeaders("text/plain; charset=utf-8"))
  response.end(text)
}

function sendHtml(
  response: ServerResponse,
  status: number,
  html: string,
): void {
  response.writeHead(status, securityHeaders("text/html; charset=utf-8"))
  response.end(`<!doctype html><meta charset="utf-8"><title>Body War</title>${html}`)
}

function securityHeaders(contentType: string): Record<string, string> {
  return {
    "content-type": contentType,
    "cache-control": "no-store",
    "content-security-policy": "default-src 'none'; style-src 'unsafe-inline'",
    "referrer-policy": "no-referrer",
    "x-content-type-options": "nosniff",
  }
}

function constantTimeEqual(left: string, right: string): boolean {
  const leftBytes = Buffer.from(left)
  const rightBytes = Buffer.from(right)
  return leftBytes.length === rightBytes.length && timingSafeEqual(leftBytes, rightBytes)
}

function requiredNonEmpty(value: string, name: string): string {
  const trimmed = value.trim()
  if (!trimmed) throw new StravaReconnectError("missing_configuration", `${name} is required`)
  return trimmed
}

function requiredStringField(value: JsonObject, key: string): string {
  const candidate = value[key]
  if (typeof candidate !== "string" || !candidate.trim()) {
    throw new StravaReconnectError("invalid_token_response", `Strava token response is missing ${key}`)
  }
  return candidate.trim()
}

function requiredNumberField(value: JsonObject, key: string): number {
  const candidate = value[key]
  if (typeof candidate !== "number" || !Number.isFinite(candidate)) {
    throw new StravaReconnectError("invalid_token_response", `Strava token response is missing ${key}`)
  }
  return candidate
}

function parseTokenType(value: unknown): string {
  if (typeof value !== "string" || value.toLowerCase() !== "bearer") {
    throw new StravaReconnectError(
      "invalid_token_response",
      "Strava token response contains an unsupported token type",
    )
  }
  return "Bearer"
}

function isObject(value: unknown): value is JsonObject {
  return typeof value === "object" && value !== null && !Array.isArray(value)
}

function parseCliArgs(args: string[]): {
  includePrivate: boolean
  addAthlete: boolean
  tokensPath: string
  athleteKey?: string | undefined
  publicRedirectUri?: string | undefined
} {
  let includePrivate = false
  let addAthlete = false
  let tokensPath = resolve("data/strava-tokens.json")
  let athleteKey: string | undefined
  let publicRedirectUri: string | undefined
  for (let index = 0; index < args.length; index += 1) {
    const argument = args[index]
    if (argument === "--help") {
      printHelp()
      process.exit(0)
    }
    if (argument === "--include-private") {
      includePrivate = true
      continue
    }
    if (argument === "--add-athlete") {
      addAthlete = true
      continue
    }
    if (argument === "--tokens") {
      const value = args[index + 1]
      if (!value || value.startsWith("--")) {
        throw new StravaReconnectError("missing_cli_value", "--tokens requires a path")
      }
      tokensPath = resolve(value)
      index += 1
      continue
    }
    if (argument === "--public-callback-url") {
      const value = args[index + 1]
      if (!value || value.startsWith("--")) {
        throw new StravaReconnectError(
          "missing_cli_value",
          "--public-callback-url requires an HTTPS callback URL",
        )
      }
      publicRedirectUri = validatePublicRedirectUri(value).toString()
      index += 1
      continue
    }
    if (argument === "--athlete-key") {
      const value = args[index + 1]
      if (!value || value.startsWith("--")) {
        throw new StravaReconnectError("missing_cli_value", "--athlete-key requires a value")
      }
      athleteKey = value
      index += 1
      continue
    }
    throw new StravaReconnectError("unknown_cli_argument", `Unknown argument: ${argument}`)
  }
  if (addAthlete && athleteKey) {
    throw new StravaReconnectError(
      "conflicting_athlete_selection",
      "--add-athlete and --athlete-key cannot be used together",
    )
  }
  return {
    includePrivate,
    addAthlete,
    tokensPath,
    ...(athleteKey ? { athleteKey } : {}),
    ...(publicRedirectUri ? { publicRedirectUri } : {}),
  }
}

function printHelp(): void {
  process.stdout.write(`Usage: npm run geometry:reconnect -- [options]\n\n`)
  process.stdout.write(`Options:\n`)
  process.stdout.write(`  --include-private     Request activity:read_all for Only Me activities\n`)
  process.stdout.write(`  --add-athlete         Add a separately consenting athlete without replacing others\n`)
  process.stdout.write(`  --athlete-key <key>   Reauthorize one existing athlete in a multi-athlete store\n`)
  process.stdout.write(`  --tokens <path>       Legacy private token store path\n`)
  process.stdout.write(`  --public-callback-url <url>  Public HTTPS tunnel callback URL\n`)
}

async function main(): Promise<void> {
  const cli = parseCliArgs(process.argv.slice(2))
  const session = await startStravaReconnect({
    ...cli,
    clientId: process.env.STRAVA_CLIENT_ID ?? "",
    clientSecret: process.env.STRAVA_CLIENT_SECRET ?? "",
    redirectUri: process.env.STRAVA_REDIRECT_URI ?? "",
  })
  process.stdout.write(`Requested scope: ${session.requestedScope}\n`)
  process.stdout.write(`Open this URL in your browser:\n${session.authorizationUrl}\n`)
  process.stdout.write(`Waiting up to ten minutes for the loopback callback...\n`)
  const result = await session.completion
  process.stdout.write(`Strava reconnect complete. Accepted scope: ${result.acceptedScope}\n`)
}

if (process.argv[1]?.endsWith("reconnect-strava.js")) {
  main().catch((error: unknown) => {
    const code = error instanceof StravaReconnectError ? error.code : "unexpected_reconnect_error"
    const message = error instanceof Error ? error.message : "Strava reconnect failed"
    process.stderr.write(`Strava reconnect failed (${code}): ${message}\n`)
    process.exitCode = 1
  })
}
