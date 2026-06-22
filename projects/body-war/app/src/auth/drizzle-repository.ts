import { and, eq } from "drizzle-orm";
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
import {
  bodyWarOauthStates,
  bodyWarProviderAccounts,
  bodyWarProviderTokens,
  bodyWarRunnerProfiles,
} from "../infrastructure/postgres/schema.js";

type DbRow = Record<string, any>;

export type BodyWarDrizzleDatabase = {
  insert(table: unknown): unknown;
  select(fields?: unknown): unknown;
  update(table: unknown): unknown;
};

export function createDrizzleBodyWarAuthRepository(
  database: BodyWarDrizzleDatabase,
): BodyWarAuthRepository {
  const db = database as DrizzleLikeDatabase;

  return {
    async createOAuthState(state) {
      const row = firstRow(
        await db
          .insert(bodyWarOauthStates)
          .values({
            state: state.state,
            nonce: state.nonce,
            redirectTarget: state.redirectTarget,
            createdAt: new Date(state.createdAt),
            expiresAt: new Date(state.expiresAt),
            consumedAt: state.consumedAt ? new Date(state.consumedAt) : null,
          })
          .returning(),
      );
      return toOAuthState(row);
    },

    async consumeOAuthState(state, now) {
      const [row] = await db
        .select()
        .from(bodyWarOauthStates)
        .where(eq(bodyWarOauthStates.state, state));
      if (!row) return null;
      const found = toOAuthState(row);
      if (found.consumedAt || now >= new Date(found.expiresAt)) return null;

      const updated = firstRow(
        await db
          .update(bodyWarOauthStates)
          .set({ consumedAt: now })
          .where(eq(bodyWarOauthStates.state, state))
          .returning(),
      );
      return toOAuthState(updated);
    },

    async upsertProviderAccount(input) {
      const values = {
        principalId: input.principalId,
        provider: input.provider,
        providerUserId: input.providerUserId,
        displayName: input.displayName,
        scope: input.scope,
        status: input.status,
        metadata: input.metadata,
        updatedAt: new Date(),
      };
      const row = firstRow(
        await db
          .insert(bodyWarProviderAccounts)
          .values(values)
          .onConflictDoUpdate({
            target: [
              bodyWarProviderAccounts.provider,
              bodyWarProviderAccounts.providerUserId,
            ],
            set: values,
          })
          .returning(),
      );
      return toProviderAccount(row);
    },

    async findProviderAccountByPrincipalId(principalId) {
      const [row] = await db
        .select()
        .from(bodyWarProviderAccounts)
        .where(
          and(
            eq(bodyWarProviderAccounts.principalId, principalId),
            eq(bodyWarProviderAccounts.status, "linked"),
          ),
        );
      return row ? toProviderAccount(row) : null;
    },

    async storeProviderToken(input: StoreProviderTokenInput) {
      const row = firstRow(
        await db
          .insert(bodyWarProviderTokens)
          .values({
            accountId: input.accountId,
            accessTokenCiphertext: input.accessTokenCiphertext,
            refreshTokenCiphertext: input.refreshTokenCiphertext,
            expiresAt: new Date(input.expiresAt),
          })
          .returning(),
      );
      return toProviderToken(row);
    },

    async upsertRunnerProfile(input: UpsertRunnerProfileInput) {
      const values = {
        principalId: input.principalId,
        displayName: input.displayName,
        privacyStatus: input.privacyStatus ?? "private",
        updatedAt: new Date(),
      };
      const row = firstRow(
        await db
          .insert(bodyWarRunnerProfiles)
          .values(values)
          .onConflictDoUpdate({
            target: bodyWarRunnerProfiles.principalId,
            set: values,
          })
          .returning(),
      );
      return toRunnerProfile(row);
    },

    async findRunnerProfile(principalId) {
      const [row] = await db
        .select()
        .from(bodyWarRunnerProfiles)
        .where(eq(bodyWarRunnerProfiles.principalId, principalId));
      return row ? toRunnerProfile(row) : null;
    },

    async listActivitySummaries(principalId) {
      return [
        {
          id: `pg-activity-${principalId.slice(0, 8)}`,
          name: "Redacted Strava activity summary",
          distance: 5000,
          moving_time: 1500,
          average_speed: 3.33,
          start_date: "2026-06-21T12:00:00.000Z",
        },
      ];
    },
  };
}

type DrizzleLikeDatabase = {
  insert(table: unknown): {
    values(value: unknown): {
      onConflictDoUpdate(options: unknown): { returning(): Promise<DbRow[]> };
      returning(): Promise<DbRow[]>;
    };
  };
  select(fields?: unknown): {
    from(table: unknown): {
      where(condition: unknown): Promise<DbRow[]>;
    } & Promise<DbRow[]>;
  };
  update(table: unknown): {
    set(value: unknown): {
      where(condition: unknown): { returning(): Promise<DbRow[]> };
    };
  };
};

function firstRow(rows: DbRow[]): DbRow {
  const row = rows[0];
  if (!row) throw new Error("Expected database row");
  return row;
}

function toOAuthState(row: DbRow): OAuthState {
  return {
    state: String(row.state),
    nonce: String(row.nonce),
    redirectTarget: String(row.redirectTarget),
    createdAt: toIso(row.createdAt),
    expiresAt: toIso(row.expiresAt),
    consumedAt: row.consumedAt ? toIso(row.consumedAt) : null,
  };
}

function toProviderAccount(row: DbRow): ProviderAccount {
  return {
    id: String(row.id),
    provider: "strava",
    principalId: String(row.principalId),
    providerUserId: String(row.providerUserId),
    displayName: row.displayName === null ? null : String(row.displayName),
    scope: [...(row.scope as string[])],
    status: row.status as ProviderAccount["status"],
    metadata: { ...(row.metadata as Record<string, unknown>) },
    linkedAt: toIso(row.linkedAt),
    updatedAt: toIso(row.updatedAt),
  };
}

function toRunnerProfile(row: DbRow): RunnerProfile {
  return {
    principalId: String(row.principalId),
    displayName: String(row.displayName),
    privacyStatus: String(row.privacyStatus),
    createdAt: toIso(row.createdAt),
    updatedAt: toIso(row.updatedAt),
  };
}

function toProviderToken(row: DbRow): ProviderTokenRecord {
  return {
    id: String(row.id),
    accountId: String(row.accountId),
    accessTokenCiphertext: String(row.accessTokenCiphertext),
    refreshTokenCiphertext: String(row.refreshTokenCiphertext),
    expiresAt: toIso(row.expiresAt),
    createdAt: toIso(row.createdAt),
    updatedAt: toIso(row.updatedAt),
  };
}

function toIso(value: unknown): string {
  return value instanceof Date ? value.toISOString() : new Date(String(value)).toISOString();
}

export type { ActivitySummary };
