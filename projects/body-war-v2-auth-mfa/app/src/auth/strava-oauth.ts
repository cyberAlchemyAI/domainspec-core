import {
  createCipheriv,
  createDecipheriv,
  createHash,
  randomBytes,
  randomUUID,
} from "node:crypto";
import type { MutableAuthRepositorySet } from "@domainspec/auth-user-management";
import type { BodyWarAuthRepository } from "./body-war-repository.js";
import {
  fetchStravaActivitySummaries,
  fetchStravaActivitySummaryById,
  refreshStravaTokenPair,
  validStravaActivityPagination,
} from "./strava-activity-provider.js";
import { appError, type ActivitySummary, type AppResult, type ProviderAccount } from "./types.js";

export const DEFAULT_STRAVA_SCOPE = "read,activity:read";

export type StravaOAuthAdapterConfig = {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  publicBaseUrl: string;
  fakeGateway: boolean;
  tokenProtectionSecret: string;
};

export type StravaOAuthAdapterDeps = {
  authRepos: MutableAuthRepositorySet;
  bodyWarRepo: BodyWarAuthRepository;
  config: StravaOAuthAdapterConfig;
  fetchImpl?: typeof fetch | undefined;
  now?: (() => Date) | undefined;
};

export type StravaTokenResponse = {
  access_token: string;
  refresh_token: string;
  expires_at: number;
  scope?: string | undefined;
  athlete: {
    id: number | string;
    firstname?: string | undefined;
    lastname?: string | undefined;
    profile?: string | undefined;
  };
};

export function createStravaOAuthAdapter(deps: StravaOAuthAdapterDeps) {
  const config = deps.config;
  const fetchImpl = deps.fetchImpl ?? fetch;
  const now = deps.now ?? (() => new Date());

  async function activityAccess(principalId:string):Promise<AppResult<{account:ProviderAccount;accessToken:string}>> {
      const account = await deps.bodyWarRepo.findProviderAccountByPrincipalId(
        principalId,
      );
      if (!account || account.status !== "linked") {
        return {
          ok: false,
          error: appError(
            "strava_not_connected",
            409,
            "Strava account is not connected",
          ),
        };
      }
      if (!hasActivityReadScope(account.scope)) {
        return {
          ok: false,
          error: appError(
            "strava_scope_denied",
            403,
            "Strava activity access was not granted",
          ),
        };
      }

      const token = await deps.bodyWarRepo.findLatestProviderToken(account.id);
      if (!token) {
        return {
          ok: false,
          error: appError(
            "strava_token_missing",
            409,
            "No Strava token is available for the linked account",
          ),
        };
      }

      let accessToken: string;
      let refreshToken: string;
      try {
        accessToken = unprotectSecret(
          token.accessTokenCiphertext,
          config.tokenProtectionSecret,
        );
        refreshToken = unprotectSecret(
          token.refreshTokenCiphertext,
          config.tokenProtectionSecret,
        );
      } catch {
        return {
          ok: false,
          error: appError(
            "strava_token_unreadable",
            500,
            "Stored Strava credentials could not be read",
          ),
        };
      }

      const expiresAt = Date.parse(token.expiresAt);
      if (!Number.isFinite(expiresAt)) {
        return {
          ok: false,
          error: appError(
            "strava_token_unreadable",
            500,
            "Stored Strava credentials could not be read",
          ),
        };
      }
      if (expiresAt <= now().getTime()) {
        const refreshed = await refreshStravaTokenPair({
          clientId: config.clientId,
          clientSecret: config.clientSecret,
          refreshToken,
          fetchImpl,
        });
        if (!refreshed.ok) return refreshed;

        accessToken = refreshed.value.accessToken;
        refreshToken = refreshed.value.refreshToken;
        await deps.bodyWarRepo.storeProviderToken({
          accountId: account.id,
          accessTokenCiphertext: protectSecret(
            accessToken,
            config.tokenProtectionSecret,
          ),
          refreshTokenCiphertext: protectSecret(
            refreshToken,
            config.tokenProtectionSecret,
          ),
          expiresAt: new Date(refreshed.value.expiresAt * 1000).toISOString(),
        });
      }

      return {ok:true,value:{account,accessToken}};
  }

  return {
    configured(): boolean {
      return config.fakeGateway ||
        (config.clientId.trim().length > 0 &&
          config.clientSecret.trim().length > 0);
    },

    async start(
      pendingPrincipalId: string,
      scope = DEFAULT_STRAVA_SCOPE,
      redirectTarget = "/",
    ): Promise<AppResult<{ url: string; state: string }>> {
      if (!this.configured()) {
        return {
          ok: false,
          error: appError(
            "strava_not_configured",
            400,
            "Strava OAuth is not configured for this environment",
          ),
        };
      }
      const state = randomBytes(24).toString("base64url");
      const createdAt = now();
      await deps.bodyWarRepo.createOAuthState({
        state,
        nonce: pendingPrincipalId,
        redirectTarget,
        createdAt: createdAt.toISOString(),
        expiresAt: new Date(createdAt.getTime() + 10 * 60 * 1000).toISOString(),
        consumedAt: null,
      });

      if (config.fakeGateway) {
        return {
          ok: true,
          value: {
            state,
            url: `/api/auth/strava/callback?code=fake-local-code&state=${encodeURIComponent(state)}`,
          },
        };
      }

      const url = new URL("https://www.strava.com/oauth/authorize");
      url.searchParams.set("client_id", config.clientId);
      url.searchParams.set("redirect_uri", config.redirectUri);
      url.searchParams.set("response_type", "code");
      url.searchParams.set("approval_prompt", "auto");
      url.searchParams.set("scope", scope);
      url.searchParams.set("state", state);
      return { ok: true, value: { state, url: url.toString() } };
    },

    async callback(code: string, state: string, link?: {principalId:string;nonce:string;commit:<T>(work:()=>Promise<T>)=>Promise<T>}): Promise<AppResult<{
      principalId: string;
      account: ProviderAccount;
    }>> {
      const callbackTime = now();
      const consumedState = await deps.bodyWarRepo.consumeOAuthState(
        state,
        callbackTime,
      );
      if (!consumedState) {
        return {
          ok: false,
          error: appError("invalid_state", 400, "OAuth state is invalid or expired"),
        };
      }

      if(link&&consumedState.nonce!==link.nonce)return {ok:false,error:appError("invalid_state",400,"Provider link belongs to another session")};
      const tokenResponse = await exchangeCode(
        config,
        code,
        fetchImpl,
        callbackTime,
      );
      const commit=async ():Promise<AppResult<{principalId:string;account:ProviderAccount}>>=>{
      const providerUserId = String(tokenResponse.athlete.id);
      const identifier = `strava:${providerUserId}`;
      let principal = link?await deps.authRepos.principalRepo.findById(link.principalId):await deps.authRepos.principalRepo.findByIdentifier(identifier);
      if(link&&!principal)return {ok:false,error:appError("invalid_session",401,"Runner session no longer exists")};
      if (!principal) {
        principal = await deps.authRepos.principalRepo.create({
          identifier,
          subjectType: "user",
          roleKeys: ["runner"],
          directPermissions: ["body-war.profile.read"],
          credentialHash: "external:strava",
        });
      }

      await seedRunnerPermissions(deps.authRepos);
      const displayName = [
        tokenResponse.athlete.firstname,
        tokenResponse.athlete.lastname,
      ].filter(Boolean).join(" ").trim() || "Strava athlete";
      const scope = parseScope(tokenResponse.scope ?? DEFAULT_STRAVA_SCOPE);
      const account = await deps.bodyWarRepo.upsertProviderAccount({
        provider: "strava",
        principalId: principal.id,
        providerUserId,
        displayName,
        scope,
        status: "linked",
        metadata: {
          athlete: {
            id: providerUserId,
            firstname: tokenResponse.athlete.firstname ?? "",
            lastname: tokenResponse.athlete.lastname ?? "",
            profile: tokenResponse.athlete.profile ?? "",
          },
        },
      });
      await deps.bodyWarRepo.upsertRunnerProfile({
        principalId: principal.id,
        displayName,
      });
      await deps.bodyWarRepo.storeProviderToken({
        accountId: account.id,
        accessTokenCiphertext: protectSecret(
          tokenResponse.access_token,
          config.tokenProtectionSecret,
        ),
        refreshTokenCiphertext: protectSecret(
          tokenResponse.refresh_token,
          config.tokenProtectionSecret,
        ),
        expiresAt: new Date(tokenResponse.expires_at * 1000).toISOString(),
      });

      return { ok: true, value: { principalId: principal.id, account } };
      };
      try{return link?await link.commit(commit):await commit();}catch{return {ok:false,error:appError("provider_link_rejected",409,"Provider account cannot be linked to this session")};}
    },

    async connectionStatus(principalId: string): Promise<{
      connected: boolean;
      account: ProviderAccount | null;
    }> {
      const account = await deps.bodyWarRepo.findProviderAccountByPrincipalId(
        principalId,
      );
      return { connected: !!account, account };
    },

    async listActivitySummaries(
      principalId: string,
      page: string,
      perPage: string,
    ): Promise<AppResult<ActivitySummary[]>> {
      const providerPage = Number(page);
      const recordsPerPage = Number(perPage);
      if (!validStravaActivityPagination(1, recordsPerPage, providerPage)) {
        return {
          ok: false,
          error: appError(
            "strava_provider_bounds_invalid",
            400,
            "Strava activity pagination bounds are invalid",
          ),
        };
      }
      if (!config.fakeGateway) {
        return this.listProviderActivitySummaries(
          principalId,
          "1",
          perPage,
          page,
        );
      }

      const account = await deps.bodyWarRepo.findProviderAccountByPrincipalId(
        principalId,
      );
      if (!account) {
        return {
          ok: false,
          error: appError("strava_not_connected", 409, "Strava account is not connected"),
        };
      }
      return {
        ok: true,
        value: await deps.bodyWarRepo.listActivitySummaries(principalId),
      };
    },

    async getActivitySummary(principalId:string,activityId:string):Promise<AppResult<ActivitySummary>> {
      if(config.fakeGateway){
        const account=await deps.bodyWarRepo.findProviderAccountByPrincipalId(principalId);
        if(!account||account.status!=="linked")return {ok:false,error:appError("strava_not_connected",409,"Strava account is not connected")};
        if(!hasActivityReadScope(account.scope))return {ok:false,error:appError("strava_scope_denied",403,"Strava activity access was not granted")};
        const found=(await deps.bodyWarRepo.listActivitySummaries(principalId)).find(a=>a.id===activityId);
        return found?{ok:true,value:found}:{ok:false,error:appError("invalid_activity",400,"Activity is not available for this runner")};
      }
      const access=await activityAccess(principalId);if(!access.ok)return access;
      return fetchStravaActivitySummaryById({activityId,athleteId:access.value.account.providerUserId,accessToken:access.value.accessToken,fetchImpl});
    },

    async listProviderActivitySummaries(
      principalId: string,
      pageCount: string,
      perPage: string,
      startPage = "1",
    ): Promise<AppResult<ActivitySummary[]>> {
      const pages = Number(pageCount);
      const recordsPerPage = Number(perPage);
      const firstPage = Number(startPage);
      if (!validStravaActivityPagination(pages, recordsPerPage, firstPage)) {
        return {
          ok: false,
          error: appError(
            "strava_provider_bounds_invalid",
            400,
            "Strava activity pagination bounds are invalid",
          ),
        };
      }

      const access=await activityAccess(principalId);if(!access.ok)return access;
      const {accessToken}=access.value;

      return fetchStravaActivitySummaries({
        accessToken,
        pages,
        perPage: recordsPerPage,
        startPage: firstPage,
        fetchImpl,
      });
    },
  };
}

export async function seedRunnerPermissions(
  repos: MutableAuthRepositorySet,
): Promise<void> {
  for (const permissionKey of [
    "body-war.profile.read",
    "body-war.activity.read",
    "body-war.submission.create",
    "body-war.suggested-track.read",
    "body-war.suggested-track.create",
    "body-war.suggested-track-evidence.create",
    "body-war.auth.disconnect",
  ]) {
    await repos.grantRepo.upsertGrant({
      granteeType: "role",
      granteeKey: "runner",
      permissionKey,
      effect: "ALLOW",
    });
  }
}

async function exchangeCode(
  config: StravaOAuthAdapterConfig,
  code: string,
  fetchImpl: typeof fetch,
  now: Date,
): Promise<StravaTokenResponse> {
  if (config.fakeGateway) {
    return {
      access_token: `fake-access-token-${code}`,
      refresh_token: `fake-refresh-token-${code}`,
      expires_at: Math.floor(now.getTime() / 1000) + 3600,
      scope: DEFAULT_STRAVA_SCOPE,
      athlete: {
        id: 123,
        firstname: "Ada",
        lastname: "Runner",
        profile: "https://dgalywyr863hv.cloudfront.net/pictures/athletes/123/large.jpg",
      },
    };
  }

  const response = await fetchImpl("https://www.strava.com/oauth/token", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      client_id: config.clientId,
      client_secret: config.clientSecret,
      code,
      grant_type: "authorization_code",
    }),
  });
  if (!response.ok) {
    throw appError("strava_exchange_failed", 502, "Strava token exchange failed");
  }
  return (await response.json()) as StravaTokenResponse;
}

function parseScope(scope: string): string[] {
  return scope
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean);
}

export function protectSecret(value: string, secret: string): string {
  const key = createHash("sha256").update(secret).digest();
  const iv = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", key, iv);
  const ciphertext = Buffer.concat([
    cipher.update(value, "utf8"),
    cipher.final(),
  ]);
  const tag = cipher.getAuthTag();
  return `aes256gcm:${iv.toString("base64url")}:${tag.toString("base64url")}:${ciphertext.toString("base64url")}`;
}

export function unprotectSecret(value: string, secret: string): string {
  const parts = value.split(":");
  if (parts.length !== 4 || parts[0] !== "aes256gcm") {
    throw new Error("Unsupported protected secret");
  }
  const iv = Buffer.from(parts[1] ?? "", "base64url");
  const tag = Buffer.from(parts[2] ?? "", "base64url");
  const ciphertext = Buffer.from(parts[3] ?? "", "base64url");
  if (iv.length !== 12 || tag.length !== 16 || ciphertext.length === 0) {
    throw new Error("Invalid protected secret");
  }
  const key = createHash("sha256").update(secret).digest();
  const decipher = createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(tag);
  return Buffer.concat([
    decipher.update(ciphertext),
    decipher.final(),
  ]).toString("utf8");
}

function hasActivityReadScope(scope: string[]): boolean {
  const granted = new Set(
    scope.flatMap((value) => value.split(/[\s,]+/)).filter(Boolean),
  );
  return granted.has("activity:read") || granted.has("activity:read_all");
}

export function stravaPrincipalPlaceholder(): string {
  return `pending:${randomUUID()}`;
}
