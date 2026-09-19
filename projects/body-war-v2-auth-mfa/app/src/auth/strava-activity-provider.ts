import {configuration} from "../application/domain.js";
import { appError, type ActivitySummary, type AppResult } from "./types.js";

const STRAVA_ACTIVITIES_URL =
  "https://www.strava.com/api/v3/athlete/activities";
const STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token";
const ELIGIBLE_SPORT_TYPES = new Set(["Run", "TrailRun", "VirtualRun"]);

export type StravaActivityProviderInput = {
  accessToken: string;
  pages: number;
  perPage: number;
  startPage?: number | undefined;
  fetchImpl: typeof fetch;
};

export type StravaTokenRefreshInput = {
  clientId: string;
  clientSecret: string;
  refreshToken: string;
  fetchImpl: typeof fetch;
};

export type StravaRefreshedTokenPair = {
  accessToken: string;
  refreshToken: string;
  expiresAt: number;
};

export async function fetchStravaActivitySummaries(
  input: StravaActivityProviderInput,
): Promise<AppResult<ActivitySummary[]>> {
  const startPage = input.startPage ?? 1;
  if (!validStravaActivityPagination(input.pages, input.perPage, startPage)) {
    return {
      ok: false,
      error: appError(
        "strava_provider_bounds_invalid",
        400,
        "Strava activity pagination bounds are invalid",
      ),
    };
  }

  const summaries: ActivitySummary[] = [];
  for (let offset = 0; offset < input.pages; offset += 1) {
    const page = startPage + offset;
    const url = new URL(STRAVA_ACTIVITIES_URL);
    url.searchParams.set("page", String(page));
    url.searchParams.set("per_page", String(input.perPage));

    let response: Response;
    try {
      response = await input.fetchImpl(url, {
        method: "GET",
        headers: { authorization: `Bearer ${input.accessToken}` },
      });
    } catch {
      return providerFailure();
    }
    if (!response.ok) return providerStatusFailure(response.status, false);

    let payload: unknown;
    try {
      payload = await response.json();
    } catch {
      return providerFailure();
    }
    if (!Array.isArray(payload) || payload.length > input.perPage) {
      return providerFailure();
    }

    for (const value of payload) {
      const translated = translateActivity(value);
      if (translated === undefined) return providerFailure();
      if (translated) summaries.push(translated);
    }
    if (payload.length < input.perPage) break;
  }

  return { ok: true, value: summaries };
}

export function validStravaActivityPagination(
  pages: number,
  perPage: number,
  startPage = 1,
): boolean {
  return validIntegerBound(startPage, 1, 10) &&
    validIntegerBound(pages, 1, 10) &&
    validIntegerBound(perPage, 1, 100) &&
    startPage + pages - 1 <= 10;
}

export async function refreshStravaTokenPair(
  input: StravaTokenRefreshInput,
): Promise<AppResult<StravaRefreshedTokenPair>> {
  if (!input.clientId.trim() || !input.clientSecret.trim() ||
    !input.refreshToken.trim()) {
    return providerFailure();
  }

  let response: Response;
  try {
    response = await input.fetchImpl(STRAVA_TOKEN_URL, {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: input.clientId,
        client_secret: input.clientSecret,
        grant_type: "refresh_token",
        refresh_token: input.refreshToken,
      }),
    });
  } catch {
    return providerFailure();
  }
  if (!response.ok) return providerStatusFailure(response.status, true);

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    return providerFailure();
  }
  if (!isRecord(payload) ||
    typeof payload.access_token !== "string" || !payload.access_token.trim() ||
    typeof payload.refresh_token !== "string" || !payload.refresh_token.trim() ||
    typeof payload.expires_at !== "number" ||
    !Number.isFinite(payload.expires_at) || payload.expires_at <= 0) {
    return providerFailure();
  }

  return {
    ok: true,
    value: {
      accessToken: payload.access_token,
      refreshToken: payload.refresh_token,
      expiresAt: payload.expires_at,
    },
  };
}

function translateActivity(value: unknown): ActivitySummary | null | undefined {
  if (!isRecord(value)) return undefined;
  const sportType = typeof value.sport_type === "string"
    ? value.sport_type
    : typeof value.type === "string"
    ? value.type
    : null;
  if (!sportType || !ELIGIBLE_SPORT_TYPES.has(sportType)) return null;

  if ((typeof value.id !== "string" && typeof value.id !== "number") ||
    typeof value.name !== "string" ||
    !safeNumber(value.distance) ||
    !safeNumber(value.moving_time) ||
    !safeNumber(value.average_speed) ||
    typeof value.start_date !== "string") {
    return undefined;
  }

  return {
    id: String(value.id),
    name: value.name,
    sport_type: typeof value.sport_type === "string"
      ? value.sport_type
      : sportType,
    type: typeof value.type === "string" ? value.type : sportType,
    distance: value.distance,
    moving_time: value.moving_time,
    average_speed: value.average_speed,
    start_date: value.start_date,
  };
}

function providerStatusFailure(
  status: number,
  refreshing: boolean,
): AppResult<never> {
  if (status === 429) {
    return {
      ok: false,
      error: appError(
        "strava_rate_limited",
        429,
        "Strava temporarily rejected the request",
      ),
    };
  }
  if (status === 401 || status === 403 || (refreshing && status === 400)) {
    return {
      ok: false,
      error: appError(
        "strava_credentials_revoked",
        401,
        "Strava credentials are no longer accepted",
      ),
    };
  }
  return providerFailure();
}

function providerFailure(): AppResult<never> {
  return {
    ok: false,
    error: appError(
      "strava_provider_failed",
      502,
      "Strava could not provide activity summaries",
    ),
  };
}

function validIntegerBound(value: number, minimum: number, maximum: number): boolean {
  return Number.isInteger(value) && value >= minimum && value <= maximum;
}

function safeNumber(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value) && value >= 0;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return !!value && typeof value === "object" && !Array.isArray(value);
}

// Activity detail identity is checked before projecting any provider fields.
function stravaId(value:unknown):string|null {
  const text=typeof value==='string'?value:typeof value==='number'&&Number.isSafeInteger(value)?String(value):'';
  return /^[1-9][0-9]{0,18}$/.test(text)&&BigInt(text)<=9223372036854775807n?text:null;
}
export async function fetchStravaActivitySummaryById(input:{activityId:string;athleteId:string;accessToken:string;fetchImpl:typeof fetch}):Promise<AppResult<ActivitySummary>> {
  const unavailable=():AppResult<never>=>({ok:false,error:appError('invalid_activity',400,'Activity is not available for this runner')});
  const activityId=stravaId(input.activityId),athleteId=stravaId(input.athleteId);
  if(!activityId||!athleteId)return unavailable();
  let response:Response;
  try{response=await input.fetchImpl('https://www.strava.com/api/v3/activities/'+activityId+'?include_all_efforts=false',{method:'GET',headers:{authorization:'Bearer '+input.accessToken},redirect:'error',signal:AbortSignal.timeout(configuration.HistoricalActivityPolicy.timeoutMs)});}catch{return providerFailure();}
  if(response.status===404)return unavailable();
  if(response.status===403)return {ok:false,error:appError('strava_scope_denied',403,'Strava activity access was not granted')};
  if(!response.ok)return providerStatusFailure(response.status,false);
  let payload:unknown;
  try{
    if(!response.body)return providerFailure();const reader=response.body.getReader(),chunks:Uint8Array[]=[];let size=0;
    while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>configuration.HistoricalActivityPolicy.maxResponseBytes){await reader.cancel();return providerFailure();}chunks.push(value);}
    payload=JSON.parse(Buffer.concat(chunks).toString('utf8'));
  }catch{return providerFailure();}
  if(!isRecord(payload)||stravaId(payload.id)!==activityId||!isRecord(payload.athlete)||stravaId(payload.athlete.id)!==athleteId)return unavailable();
  const summary=translateActivity(payload);if(summary===undefined)return providerFailure();if(summary===null)return unavailable();
  return {ok:true,value:summary};
}
