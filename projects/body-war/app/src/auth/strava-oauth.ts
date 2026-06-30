import { createCipheriv, createHash, randomBytes, randomUUID } from "node:crypto";
import type { MutableAuthRepositorySet } from "@domainspec/auth-user-management";
import type { BodyWarAuthRepository } from "./body-war-repository.js";
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
      await deps.bodyWarRepo.createOAuthState({
        state,
        nonce: pendingPrincipalId,
        redirectTarget,
        createdAt: new Date().toISOString(),
        expiresAt: new Date(Date.now() + 10 * 60 * 1000).toISOString(),
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

    async callback(code: string, state: string): Promise<AppResult<{
      principalId: string;
      account: ProviderAccount;
    }>> {
      const consumedState = await deps.bodyWarRepo.consumeOAuthState(
        state,
        new Date(),
      );
      if (!consumedState) {
        return {
          ok: false,
          error: appError("invalid_state", 400, "OAuth state is invalid or expired"),
        };
      }

      const tokenResponse = await exchangeCode(config, code);
      const providerUserId = String(tokenResponse.athlete.id);
      const identifier = `strava:${providerUserId}`;
      let principal = await deps.authRepos.principalRepo.findByIdentifier(identifier);
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
      _page: string,
      _perPage: string,
    ): Promise<AppResult<ActivitySummary[]>> {
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
  };
}

async function seedRunnerPermissions(
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
): Promise<StravaTokenResponse> {
  if (config.fakeGateway) {
    return {
      access_token: `fake-access-token-${code}`,
      refresh_token: `fake-refresh-token-${code}`,
      expires_at: Math.floor(Date.now() / 1000) + 3600,
      scope: DEFAULT_STRAVA_SCOPE,
      athlete: {
        id: 123,
        firstname: "Ada",
        lastname: "Runner",
        profile: "https://dgalywyr863hv.cloudfront.net/pictures/athletes/123/large.jpg",
      },
    };
  }

  const response = await fetch("https://www.strava.com/oauth/token", {
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

function protectSecret(value: string, secret: string): string {
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

export function stravaPrincipalPlaceholder(): string {
  return `pending:${randomUUID()}`;
}
