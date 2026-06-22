import { randomUUID } from "node:crypto";
import type {
  BodyWarAuthRepository,
  StoreProviderTokenInput,
  UpsertProviderAccountInput,
  UpsertRunnerProfileInput,
} from "./body-war-repository.js";
import type {
  ActivitySummary,
  OAuthState,
  ProviderAccount,
  ProviderTokenRecord,
  RunnerProfile,
} from "./types.js";

export function createMemoryBodyWarAuthRepository(): BodyWarAuthRepository {
  const states = new Map<string, OAuthState>();
  const accounts = new Map<string, ProviderAccount>();
  const accountIdsByPrincipal = new Map<string, string>();
  const profiles = new Map<string, RunnerProfile>();
  const tokens = new Map<string, ProviderTokenRecord>();

  return {
    async createOAuthState(state) {
      const cloned = cloneState(state);
      states.set(cloned.state, cloned);
      return cloneState(cloned);
    },

    async consumeOAuthState(state, now) {
      const found = states.get(state);
      if (!found || found.consumedAt || now >= new Date(found.expiresAt)) {
        return null;
      }
      const consumed = { ...found, consumedAt: now.toISOString() };
      states.set(state, consumed);
      return cloneState(consumed);
    },

    async upsertProviderAccount(input) {
      const key = `${input.provider}:${input.providerUserId}`;
      const existing = accounts.get(key);
      const now = new Date().toISOString();
      const account: ProviderAccount = {
        id: existing?.id ?? randomUUID(),
        provider: input.provider,
        principalId: input.principalId,
        providerUserId: input.providerUserId,
        displayName: input.displayName,
        scope: [...input.scope],
        status: input.status,
        metadata: { ...input.metadata },
        linkedAt: existing?.linkedAt ?? now,
        updatedAt: now,
      };
      accounts.set(key, account);
      accountIdsByPrincipal.set(input.principalId, key);
      return cloneAccount(account);
    },

    async findProviderAccountByPrincipalId(principalId) {
      const key = accountIdsByPrincipal.get(principalId);
      const account = key ? accounts.get(key) : undefined;
      return account ? cloneAccount(account) : null;
    },

    async storeProviderToken(input: StoreProviderTokenInput) {
      const now = new Date().toISOString();
      const record: ProviderTokenRecord = {
        id: randomUUID(),
        accountId: input.accountId,
        accessTokenCiphertext: input.accessTokenCiphertext,
        refreshTokenCiphertext: input.refreshTokenCiphertext,
        expiresAt: input.expiresAt,
        createdAt: now,
        updatedAt: now,
      };
      tokens.set(record.id, record);
      return { ...record };
    },

    async upsertRunnerProfile(input: UpsertRunnerProfileInput) {
      const existing = profiles.get(input.principalId);
      const now = new Date().toISOString();
      const profile: RunnerProfile = {
        principalId: input.principalId,
        displayName: input.displayName,
        privacyStatus: input.privacyStatus ?? existing?.privacyStatus ?? "private",
        createdAt: existing?.createdAt ?? now,
        updatedAt: now,
      };
      profiles.set(input.principalId, profile);
      return { ...profile };
    },

    async findRunnerProfile(principalId) {
      const profile = profiles.get(principalId);
      return profile ? { ...profile } : null;
    },

    async listActivitySummaries(principalId) {
      return [
        {
          id: `fake-activity-${principalId.slice(0, 8)}`,
          name: "Redacted Strava activity summary",
          sport_type: "Run",
          type: "Run",
          distance: 5000,
          moving_time: 1500,
          average_speed: 3.33,
          start_date: "2026-06-21T12:00:00.000Z",
        },
      ];
    },
  };
}

function cloneState(state: OAuthState): OAuthState {
  return { ...state };
}

function cloneAccount(account: ProviderAccount): ProviderAccount {
  return {
    ...account,
    scope: [...account.scope],
    metadata: { ...account.metadata },
  };
}
