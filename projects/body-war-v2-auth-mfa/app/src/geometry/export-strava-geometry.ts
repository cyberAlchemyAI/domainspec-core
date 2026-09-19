import { createHash } from "node:crypto"
import { chmod, mkdir, readFile, rename, unlink, writeFile } from "node:fs/promises"
import { dirname, resolve } from "node:path"

const DEFAULT_STRAVA_API_BASE_URL = "https://www.strava.com/api/v3"
const STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
const EXPORT_SCHEMA = "body-war-strava-geometry-export/v1"

type JsonObject = Record<string, unknown>
type GeometrySource = "athlete-activities" | "submitted"

type LegacyTokenRecord = {
  access_token: string
  refresh_token: string
  expires_at: number
  updated_at: number
  scope?: string | undefined
  athlete?: JsonObject | undefined
  [key: string]: unknown
}

type LegacyTokenStore = {
  athletes: Record<string, LegacyTokenRecord>
}

type ActivityCandidate = {
  activityId: string
  source: GeometrySource | "explicit"
  sportType: string | null
  activityDistanceMeters: number | null
  trackIds: string[]
  submissionCount: number
}

type Stream = {
  data: unknown[]
  resolution?: string | undefined
}

type GeoJsonFeature = {
  type: "Feature"
  id: string
  properties: {
    authority: "exploratory_evidence"
    provider: "strava"
    source_activity_ref: string
    discovery_source: ActivityCandidate["source"]
    sport_type: string | null
    track_ids: string[]
    submission_count: number
    point_count: number
    activity_distance_meters: number | null
    stream_distance_meters: number
    elapsed_seconds: number
    stream_resolution: string | null
    coordinate_distances_meters: number[]
    coordinate_times_seconds: number[]
  }
  geometry: {
    type: "LineString"
    coordinates: Array<[number, number]>
  }
}

type ExportOutcome = {
  source_activity_ref: string
  status: "exported" | "failed" | "not_attempted"
  point_count?: number | undefined
  reason?: string | undefined
}

export type GeometryExportOptions = {
  tokensPath: string
  outputPath: string
  reportPath: string
  clientId: string
  clientSecret: string
  source?: GeometrySource | undefined
  submissionsPath?: string | undefined
  athleteKey?: string | undefined
  pages?: number | undefined
  perPage?: number | undefined
  limit?: number | undefined
  activityIds?: string[] | undefined
  fetchImpl?: typeof fetch | undefined
  now?: Date | undefined
  apiBaseUrl?: string | undefined
  tokenUrl?: string | undefined
}

export type GeometryExportResult = {
  discovered: number
  requested: number
  exported: number
  failed: number
  outputPath: string
  reportPath: string
  tokenRefreshed: boolean
  rateLimited: boolean
}

export class GeometryExportError extends Error {
  constructor(readonly code: string, message: string) {
    super(message)
    this.name = "GeometryExportError"
  }
}

export async function exportStravaGeometry(
  options: GeometryExportOptions,
): Promise<GeometryExportResult> {
  const fetchImpl = options.fetchImpl ?? fetch
  const now = options.now ?? new Date()
  const source = options.source ?? "athlete-activities"
  const pages = boundedInteger(options.pages ?? 1, "pages", 1, 10)
  const perPage = boundedInteger(options.perPage ?? 30, "per-page", 1, 100)
  const limit = options.limit === undefined
    ? undefined
    : boundedInteger(options.limit, "limit", 1, 1000)

  const localCandidates = await selectLocalCandidates({
    activityIds: options.activityIds,
    source,
    submissionsPath: options.submissionsPath,
  })

  await secureExistingFile(options.tokensPath)
  const tokenStore = parseTokenStore(await readJson(options.tokensPath))
  const selectedToken = selectTokenRecord(tokenStore, options.athleteKey)
  const access = await ensureAccessToken({
    clientId: requiredNonEmpty(options.clientId, "STRAVA_CLIENT_ID"),
    clientSecret: requiredNonEmpty(options.clientSecret, "STRAVA_CLIENT_SECRET"),
    fetchImpl,
    now,
    tokenRecord: selectedToken.record,
    tokenUrl: options.tokenUrl ?? STRAVA_TOKEN_URL,
  })

  if (access.refreshed) {
    tokenStore.athletes[selectedToken.key] = access.tokenRecord
    await writeJsonAtomic(options.tokensPath, tokenStore, 0o600)
  }

  const discoveredActivities = localCandidates ?? await discoverAthleteActivities({
    accessToken: access.tokenRecord.access_token,
    apiBaseUrl: options.apiBaseUrl ?? DEFAULT_STRAVA_API_BASE_URL,
    fetchImpl,
    pages,
    perPage,
  })
  if (discoveredActivities.length === 0) {
    const hasPrivateActivityScope = access.tokenRecord.scope
      ?.split(/[ ,]+/)
      .includes("activity:read_all") ?? false
    throw new GeometryExportError(
      hasPrivateActivityScope
        ? "no_activities_discovered"
        : "no_activities_accessible_with_scope",
      hasPrivateActivityScope
        ? "No retrievable Strava activities were discovered"
        : "No activities are visible to the stored authorization; review activity visibility and explicitly authorize a suitable scope before retrying",
    )
  }
  const selectedActivities = limit === undefined
    ? discoveredActivities
    : discoveredActivities.slice(0, limit)

  const features: GeoJsonFeature[] = []
  const outcomes: ExportOutcome[] = []
  let rateLimited = false
  for (let index = 0; index < selectedActivities.length; index += 1) {
    const activity = selectedActivities[index]
    if (!activity) continue
    const activityRef = sourceActivityRef(activity.activityId)
    try {
      const feature = await fetchActivityFeature({
        accessToken: access.tokenRecord.access_token,
        activity,
        apiBaseUrl: options.apiBaseUrl ?? DEFAULT_STRAVA_API_BASE_URL,
        fetchImpl,
      })
      features.push(feature)
      outcomes.push({
        source_activity_ref: activityRef,
        status: "exported",
        point_count: feature.properties.point_count,
      })
    } catch (error) {
      const reason = safeErrorCode(error)
      outcomes.push({
        source_activity_ref: activityRef,
        status: "failed",
        reason,
      })
      if (reason === "strava_stream_http_429") {
        rateLimited = true
        for (const pending of selectedActivities.slice(index + 1)) {
          outcomes.push({
            source_activity_ref: sourceActivityRef(pending.activityId),
            status: "not_attempted",
            reason: "rate_limited",
          })
        }
        break
      }
    }
  }

  const generatedAt = now.toISOString()
  const featureCollection = {
    type: "FeatureCollection",
    name: "body-war-strava-geometry-evidence",
    body_war_export: {
      schema: EXPORT_SCHEMA,
      generated_at: generatedAt,
      source: "strava_activity_streams",
      discovery_source: localCandidates === null ? "athlete-activities" : source,
      authority: "exploratory_evidence",
      geometry_status: "candidate_input_only",
      privacy: "private_location_data",
      discovered_activity_count: discoveredActivities.length,
      requested_activity_count: selectedActivities.length,
      exported_activity_count: features.length,
    },
    features,
  }
  const report = {
    schema: EXPORT_SCHEMA,
    generated_at: generatedAt,
    source: "strava_activity_streams",
    discovery_source: localCandidates === null ? "athlete-activities" : source,
    authority: "exploratory_evidence",
    geometry_status: "candidate_input_only",
    discovered_activity_count: discoveredActivities.length,
    requested_activity_count: selectedActivities.length,
    exported_activity_count: features.length,
    failed_activity_count: outcomes.length - features.length,
    token_refreshed: access.refreshed,
    rate_limited: rateLimited,
    outcomes,
  }

  await writeJsonAtomic(options.outputPath, featureCollection, 0o600)
  await writeJsonAtomic(options.reportPath, report, 0o600)

  return {
    discovered: discoveredActivities.length,
    requested: selectedActivities.length,
    exported: features.length,
    failed: outcomes.length - features.length,
    outputPath: options.outputPath,
    reportPath: options.reportPath,
    tokenRefreshed: access.refreshed,
    rateLimited,
  }
}

async function selectLocalCandidates(input: {
  activityIds: string[] | undefined
  source: GeometrySource
  submissionsPath: string | undefined
}): Promise<ActivityCandidate[] | null> {
  if (input.activityIds && input.activityIds.length > 0) {
    const unique = [...new Set(input.activityIds)]
    for (const id of unique) requireNumericActivityId(id, "--activity-id")
    return unique.map((activityId) => ({
      activityId,
      source: "explicit",
      sportType: null,
      activityDistanceMeters: null,
      trackIds: [],
      submissionCount: 0,
    }))
  }
  if (input.source === "athlete-activities") return null
  if (!input.submissionsPath) {
    throw new GeometryExportError(
      "missing_submissions_path",
      "A submission store path is required for --source submitted",
    )
  }
  return parseSubmittedCandidates(await readJson(input.submissionsPath))
}

function parseSubmittedCandidates(value: unknown): ActivityCandidate[] {
  if (!isObject(value) || !Array.isArray(value.submissions)) {
    throw new GeometryExportError(
      "invalid_submissions_store",
      "Submission store must contain a submissions array",
    )
  }
  const candidates = new Map<string, ActivityCandidate>()
  for (const item of value.submissions) {
    if (!isObject(item) || typeof item.activity_id !== "string") continue
    const activityId = item.activity_id.trim()
    if (!/^\d+$/.test(activityId)) continue
    const trackId = typeof item.track_id === "string" && item.track_id.trim()
      ? item.track_id.trim()
      : null
    const existing = candidates.get(activityId)
    if (existing) {
      existing.submissionCount += 1
      if (trackId && !existing.trackIds.includes(trackId)) existing.trackIds.push(trackId)
      continue
    }
    candidates.set(activityId, {
      activityId,
      source: "submitted",
      sportType: null,
      activityDistanceMeters: null,
      trackIds: trackId ? [trackId] : [],
      submissionCount: 1,
    })
  }
  if (candidates.size === 0) {
    throw new GeometryExportError(
      "no_usable_provider_activity_ids",
      "The submission store contains no numeric Strava activity IDs",
    )
  }
  return [...candidates.values()]
}

async function discoverAthleteActivities(input: {
  accessToken: string
  apiBaseUrl: string
  fetchImpl: typeof fetch
  pages: number
  perPage: number
}): Promise<ActivityCandidate[]> {
  const activities = new Map<string, ActivityCandidate>()
  const baseUrl = input.apiBaseUrl.replace(/\/+$/, "")
  for (let page = 1; page <= input.pages; page += 1) {
    const url = new URL(`${baseUrl}/athlete/activities`)
    url.searchParams.set("page", String(page))
    url.searchParams.set("per_page", String(input.perPage))
    const response = await input.fetchImpl(url, {
      headers: { authorization: `Bearer ${input.accessToken}` },
    })
    if (!response.ok) {
      throw new GeometryExportError(
        `strava_activities_http_${response.status}`,
        `Strava activity discovery failed with HTTP ${response.status}`,
      )
    }
    const payload: unknown = await response.json()
    if (!Array.isArray(payload)) {
      throw new GeometryExportError(
        "invalid_activities_response",
        "Strava activity discovery response is not an array",
      )
    }
    for (const rawActivity of payload) {
      const activity = parseDiscoveredActivity(rawActivity)
      if (activity) activities.set(activity.activityId, activity)
    }
    if (payload.length < input.perPage) break
  }
  return [...activities.values()]
}

function parseDiscoveredActivity(value: unknown): ActivityCandidate | null {
  if (!isObject(value)) return null
  const rawId = value.id
  const activityId = typeof rawId === "number" && Number.isSafeInteger(rawId)
    ? String(rawId)
    : typeof rawId === "string"
      ? rawId.trim()
      : ""
  if (!/^\d+$/.test(activityId)) return null
  const sportType = typeof value.sport_type === "string"
    ? value.sport_type
    : typeof value.type === "string"
      ? value.type
      : null
  const distance = typeof value.distance === "number" && Number.isFinite(value.distance)
    ? value.distance
    : null
  return {
    activityId,
    source: "athlete-activities",
    sportType,
    activityDistanceMeters: distance,
    trackIds: [],
    submissionCount: 0,
  }
}

function parseTokenStore(value: unknown): LegacyTokenStore {
  if (!isObject(value) || !isObject(value.athletes)) {
    throw new GeometryExportError(
      "invalid_token_store",
      "Token store must contain an athletes object",
    )
  }

  const athletes: Record<string, LegacyTokenRecord> = {}
  for (const [key, rawRecord] of Object.entries(value.athletes)) {
    if (!isObject(rawRecord)) {
      throw new GeometryExportError("invalid_token_record", "Token record is not an object")
    }
    const accessToken = requiredStringField(rawRecord, "access_token")
    const refreshToken = requiredStringField(rawRecord, "refresh_token")
    const expiresAt = requiredFiniteNumberField(rawRecord, "expires_at")
    const updatedAt = typeof rawRecord.updated_at === "number" && Number.isFinite(rawRecord.updated_at)
      ? rawRecord.updated_at
      : 0
    athletes[key] = {
      ...rawRecord,
      access_token: accessToken,
      refresh_token: refreshToken,
      expires_at: expiresAt,
      updated_at: updatedAt,
      ...(typeof rawRecord.scope === "string" ? { scope: rawRecord.scope } : {}),
      ...(isObject(rawRecord.athlete) ? { athlete: rawRecord.athlete } : {}),
    }
  }
  if (Object.keys(athletes).length === 0) {
    throw new GeometryExportError("missing_token_record", "Token store has no athlete records")
  }
  return { athletes }
}

function selectTokenRecord(
  store: LegacyTokenStore,
  athleteKey: string | undefined,
): { key: string; record: LegacyTokenRecord } {
  if (athleteKey) {
    const record = store.athletes[athleteKey]
    if (!record) {
      throw new GeometryExportError(
        "unknown_token_athlete",
        "The selected token athlete key does not exist",
      )
    }
    return { key: athleteKey, record }
  }

  const entries = Object.entries(store.athletes)
  if (entries.length !== 1) {
    throw new GeometryExportError(
      "ambiguous_token_athlete",
      "Token store contains multiple athletes; pass --athlete-key explicitly",
    )
  }
  const entry = entries[0]
  if (!entry) {
    throw new GeometryExportError("missing_token_record", "Token store has no athlete records")
  }
  return { key: entry[0], record: entry[1] }
}

async function ensureAccessToken(input: {
  clientId: string
  clientSecret: string
  fetchImpl: typeof fetch
  now: Date
  tokenRecord: LegacyTokenRecord
  tokenUrl: string
}): Promise<{ tokenRecord: LegacyTokenRecord; refreshed: boolean }> {
  const nowSeconds = Math.floor(input.now.getTime() / 1000)
  if (input.tokenRecord.expires_at > nowSeconds + 3600) {
    return { tokenRecord: input.tokenRecord, refreshed: false }
  }

  const response = await input.fetchImpl(input.tokenUrl, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: input.clientId,
      client_secret: input.clientSecret,
      grant_type: "refresh_token",
      refresh_token: input.tokenRecord.refresh_token,
    }),
  })
  if (!response.ok) {
    throw new GeometryExportError(
      `strava_refresh_http_${response.status}`,
      `Strava token refresh failed with HTTP ${response.status}`,
    )
  }
  const payload: unknown = await response.json()
  if (!isObject(payload)) {
    throw new GeometryExportError("invalid_refresh_response", "Strava refresh response is not an object")
  }
  const accessToken = requiredStringField(payload, "access_token")
  const refreshToken = requiredStringField(payload, "refresh_token")
  const expiresAt = requiredFiniteNumberField(payload, "expires_at")

  return {
    refreshed: true,
    tokenRecord: {
      ...input.tokenRecord,
      access_token: accessToken,
      refresh_token: refreshToken,
      expires_at: expiresAt,
      updated_at: nowSeconds,
    },
  }
}

async function fetchActivityFeature(input: {
  accessToken: string
  activity: ActivityCandidate
  apiBaseUrl: string
  fetchImpl: typeof fetch
}): Promise<GeoJsonFeature> {
  const baseUrl = input.apiBaseUrl.replace(/\/+$/, "")
  const url = new URL(`${baseUrl}/activities/${encodeURIComponent(input.activity.activityId)}/streams`)
  url.searchParams.set("keys", "latlng,distance,time")
  url.searchParams.set("key_by_type", "true")
  const response = await input.fetchImpl(url, {
    headers: { authorization: `Bearer ${input.accessToken}` },
  })
  if (!response.ok) {
    throw new GeometryExportError(
      `strava_stream_http_${response.status}`,
      `Strava activity stream request failed with HTTP ${response.status}`,
    )
  }

  const streams = streamMap(await response.json())
  const latlng = streams.latlng
  const distance = streams.distance
  const time = streams.time
  if (!latlng) throw new GeometryExportError("missing_latlng_stream", "Activity has no GPS stream")
  if (!distance) throw new GeometryExportError("missing_distance_stream", "Activity has no distance stream")
  if (!time) throw new GeometryExportError("missing_time_stream", "Activity has no time stream")

  const coordinates = parseCoordinates(latlng.data)
  const distances = parseNumberStream(distance.data, "invalid_distance_stream")
  const times = parseNumberStream(time.data, "invalid_time_stream")
  if (coordinates.length < 2) {
    throw new GeometryExportError("insufficient_geometry", "Activity GPS stream has fewer than two points")
  }
  if (coordinates.length !== distances.length || coordinates.length !== times.length) {
    throw new GeometryExportError(
      "unaligned_streams",
      "Activity GPS, distance, and time streams do not have equal lengths",
    )
  }

  const activityRef = sourceActivityRef(input.activity.activityId)
  return {
    type: "Feature",
    id: `strava-activity-${activityRef}`,
    properties: {
      authority: "exploratory_evidence",
      provider: "strava",
      source_activity_ref: activityRef,
      discovery_source: input.activity.source,
      sport_type: input.activity.sportType,
      track_ids: [...input.activity.trackIds].sort(),
      submission_count: input.activity.submissionCount,
      point_count: coordinates.length,
      activity_distance_meters: input.activity.activityDistanceMeters,
      stream_distance_meters: distances[distances.length - 1] ?? 0,
      elapsed_seconds: times[times.length - 1] ?? 0,
      stream_resolution: typeof latlng.resolution === "string" ? latlng.resolution : null,
      coordinate_distances_meters: distances,
      coordinate_times_seconds: times,
    },
    geometry: {
      type: "LineString",
      coordinates,
    },
  }
}

function streamMap(value: unknown): Record<string, Stream> {
  const result: Record<string, Stream> = {}
  if (Array.isArray(value)) {
    for (const candidate of value) {
      if (!isObject(candidate) || typeof candidate.type !== "string") continue
      const stream = parseStream(candidate)
      if (stream) result[candidate.type] = stream
    }
    return result
  }
  if (!isObject(value)) {
    throw new GeometryExportError("invalid_stream_response", "Strava stream response has an unsupported shape")
  }
  for (const [key, candidate] of Object.entries(value)) {
    const stream = parseStream(candidate)
    if (stream) result[key] = stream
  }
  return result
}

function parseStream(value: unknown): Stream | null {
  if (!isObject(value) || !Array.isArray(value.data)) return null
  return {
    data: value.data,
    ...(typeof value.resolution === "string" ? { resolution: value.resolution } : {}),
  }
}

function parseCoordinates(values: unknown[]): Array<[number, number]> {
  return values.map((value) => {
    if (!Array.isArray(value) || value.length !== 2) {
      throw new GeometryExportError("invalid_latlng_stream", "GPS stream contains an invalid coordinate")
    }
    const latitude = value[0]
    const longitude = value[1]
    if (
      typeof latitude !== "number" ||
      typeof longitude !== "number" ||
      !Number.isFinite(latitude) ||
      !Number.isFinite(longitude) ||
      latitude < -90 || latitude > 90 ||
      longitude < -180 || longitude > 180
    ) {
      throw new GeometryExportError("invalid_latlng_stream", "GPS stream contains an invalid coordinate")
    }
    return [longitude, latitude]
  })
}

function parseNumberStream(values: unknown[], code: string): number[] {
  return values.map((value) => {
    if (typeof value !== "number" || !Number.isFinite(value) || value < 0) {
      throw new GeometryExportError(code, "Numeric activity stream contains an invalid value")
    }
    return value
  })
}

async function secureExistingFile(path: string): Promise<void> {
  try {
    await chmod(path, 0o600)
  } catch {
    throw new GeometryExportError("token_file_unavailable", `Could not secure token file: ${path}`)
  }
}

async function readJson(path: string): Promise<unknown> {
  let raw: string
  try {
    raw = await readFile(path, "utf8")
  } catch {
    throw new GeometryExportError("input_file_unreadable", `Could not read required input file: ${path}`)
  }
  try {
    return JSON.parse(raw) as unknown
  } catch {
    throw new GeometryExportError("input_file_invalid_json", `Required input file is not valid JSON: ${path}`)
  }
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

function sourceActivityRef(activityId: string): string {
  return createHash("sha256")
    .update(`strava-activity:${activityId}`)
    .digest("hex")
    .slice(0, 24)
}

function requireNumericActivityId(value: string, source: string): string {
  const trimmed = value.trim()
  if (!/^\d+$/.test(trimmed)) {
    throw new GeometryExportError("invalid_activity_id", `${source} must contain a numeric Strava activity ID`)
  }
  return trimmed
}

function requiredStringField(value: JsonObject, key: string): string {
  const candidate = value[key]
  if (typeof candidate !== "string" || candidate.trim().length === 0) {
    throw new GeometryExportError("invalid_required_field", `Record is missing string field ${key}`)
  }
  return candidate.trim()
}

function requiredFiniteNumberField(value: JsonObject, key: string): number {
  const candidate = value[key]
  if (typeof candidate !== "number" || !Number.isFinite(candidate)) {
    throw new GeometryExportError("invalid_required_field", `Record is missing numeric field ${key}`)
  }
  return candidate
}

function requiredNonEmpty(value: string, name: string): string {
  const trimmed = value.trim()
  if (!trimmed) throw new GeometryExportError("missing_configuration", `${name} is required`)
  return trimmed
}

function boundedInteger(value: number, name: string, minimum: number, maximum: number): number {
  if (!Number.isInteger(value) || value < minimum || value > maximum) {
    throw new GeometryExportError(
      `invalid_${name.replaceAll("-", "_")}`,
      `--${name} must be an integer from ${minimum} through ${maximum}`,
    )
  }
  return value
}

function isObject(value: unknown): value is JsonObject {
  return typeof value === "object" && value !== null && !Array.isArray(value)
}

function safeErrorCode(error: unknown): string {
  if (error instanceof GeometryExportError) return error.code
  return "unexpected_activity_export_error"
}

type CliOptions = {
  tokensPath: string
  submissionsPath: string
  outputPath: string
  reportPath: string
  source: GeometrySource
  athleteKey?: string | undefined
  pages: number
  perPage: number
  limit?: number | undefined
  activityIds: string[]
}

function parseCliArgs(args: string[]): CliOptions {
  const options: CliOptions = {
    tokensPath: resolve("data/strava-tokens.json"),
    submissionsPath: resolve("data/track-submissions.json"),
    outputPath: resolve(".runtime/geometry/strava-activities.geojson"),
    reportPath: resolve(".runtime/geometry/export-report.json"),
    source: "athlete-activities",
    pages: 1,
    perPage: 30,
    activityIds: [],
  }

  for (let index = 0; index < args.length; index += 1) {
    const argument = args[index]
    if (argument === "--help") {
      printHelp()
      process.exit(0)
    }
    if (argument === "--submitted") {
      options.source = "submitted"
      continue
    }
    const value = args[index + 1]
    if (!value || value.startsWith("--")) {
      throw new GeometryExportError("missing_cli_value", `${argument ?? "argument"} requires a value`)
    }
    switch (argument) {
      case "--source":
        if (value !== "athlete-activities" && value !== "submitted") {
          throw new GeometryExportError(
            "invalid_source",
            "--source must be athlete-activities or submitted",
          )
        }
        options.source = value
        break
      case "--submissions":
        options.submissionsPath = resolve(value)
        break
      case "--tokens":
        options.tokensPath = resolve(value)
        break
      case "--out":
      case "--output":
        options.outputPath = resolve(value)
        break
      case "--report":
        options.reportPath = resolve(value)
        break
      case "--athlete-key":
        options.athleteKey = value
        break
      case "--activity-id":
        options.activityIds.push(requireNumericActivityId(value, "--activity-id"))
        break
      case "--pages":
        options.pages = boundedInteger(Number(value), "pages", 1, 10)
        break
      case "--per-page":
        options.perPage = boundedInteger(Number(value), "per-page", 1, 100)
        break
      case "--limit":
        options.limit = boundedInteger(Number(value), "limit", 1, 1000)
        break
      default:
        throw new GeometryExportError("unknown_cli_argument", `Unknown argument: ${argument}`)
    }
    index += 1
  }
  return options
}

function printHelp(): void {
  process.stdout.write(`Usage: npm run geometry:export -- [options]\n\n`)
  process.stdout.write(`Defaults to 30 recent activities from the authenticated athlete.\n\n`)
  process.stdout.write(`Options:\n`)
  process.stdout.write(`  --limit <count>          Attempt only the first N discovered activities\n`)
  process.stdout.write(`  --pages <count>          Activity-list pages to inspect (default: 1, max: 10)\n`)
  process.stdout.write(`  --per-page <count>       Activities per page (default: 30, max: 100)\n`)
  process.stdout.write(`  --activity-id <id>       Export one explicit activity; may be repeated\n`)
  process.stdout.write(`  --source <source>        athlete-activities or submitted\n`)
  process.stdout.write(`  --submitted              Alias for --source submitted\n`)
  process.stdout.write(`  --athlete-key <key>      Select a token record when the store has multiple athletes\n`)
  process.stdout.write(`  --submissions <path>     Submission store path\n`)
  process.stdout.write(`  --tokens <path>          Legacy token store path\n`)
  process.stdout.write(`  --out <path>             GeoJSON output path\n`)
  process.stdout.write(`  --report <path>          Sanitized report output path\n`)
}

async function main(): Promise<void> {
  const cli = parseCliArgs(process.argv.slice(2))
  const result = await exportStravaGeometry({
    ...cli,
    clientId: process.env.STRAVA_CLIENT_ID ?? "",
    clientSecret: process.env.STRAVA_CLIENT_SECRET ?? "",
  })
  process.stdout.write(
    `Geometry export complete: ${result.exported}/${result.requested} exported, ${result.failed} unavailable.\n`,
  )
  process.stdout.write(`GeoJSON: ${result.outputPath}\n`)
  process.stdout.write(`Report: ${result.reportPath}\n`)
  if (result.exported === 0) process.exitCode = 2
}

if (process.argv[1]?.endsWith("export-strava-geometry.js")) {
  main().catch((error: unknown) => {
    const code = safeErrorCode(error)
    const message = error instanceof Error ? error.message : "Geometry export failed"
    process.stderr.write(`Geometry export failed (${code}): ${message}\n`)
    process.exitCode = 1
  })
}
