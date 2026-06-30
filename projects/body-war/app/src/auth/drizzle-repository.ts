import { and, eq } from "drizzle-orm";
import type {
  AddActivityEvidenceCandidateInput,
  BodyWarAuthRepository,
  CreateSuggestedTrackInput,
  StoreProviderTokenInput,
  UpsertProviderAccountInput,
  UpsertRunnerProfileInput,
} from "./body-war-repository.js";
import {
  DEFAULT_SUGGESTED_TRACK,
  suggestedTrackSlug,
} from "./body-war-repository.js";
import type {
  ActivitySummary,
  ActivityEvidenceCandidate,
  OAuthState,
  ProviderAccount,
  ProviderTokenRecord,
  RunnerProfile,
  SuggestedTrack,
} from "./types.js";
import {
  bodyWarActivityEvidenceCandidates,
  bodyWarOauthStates,
  bodyWarProviderAccounts,
  bodyWarProviderTokens,
  bodyWarRunnerProfiles,
  bodyWarSuggestedTracks,
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
  const ensureDefaultSuggestedTracks = async (): Promise<SuggestedTrack[]> => {
    const [existing] = await db
      .select()
      .from(bodyWarSuggestedTracks)
      .where(eq(bodyWarSuggestedTracks.slug, DEFAULT_SUGGESTED_TRACK.slug));

    const values = {
      slug: DEFAULT_SUGGESTED_TRACK.slug,
      name: DEFAULT_SUGGESTED_TRACK.name,
      placeLabel: DEFAULT_SUGGESTED_TRACK.placeLabel,
      city: DEFAULT_SUGGESTED_TRACK.city,
      country: DEFAULT_SUGGESTED_TRACK.country,
      distanceHintMeters: DEFAULT_SUGGESTED_TRACK.distanceHintMeters,
      publicNote: DEFAULT_SUGGESTED_TRACK.publicNote,
      updatedAt: new Date(),
    };

    const row = existing
      ? firstRow(
          await db
            .update(bodyWarSuggestedTracks)
            .set(values)
            .where(eq(bodyWarSuggestedTracks.id, existing.id))
            .returning(),
        )
      : firstRow(
          await db
            .insert(bodyWarSuggestedTracks)
            .values({
              ...values,
              status: "needs_evidence",
              geometryAuthority: "needs_evidence",
            })
            .returning(),
        );
    return [toSuggestedTrack(row)];
  };

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
          sport_type: "Run",
          type: "Run",
          distance: 5000,
          moving_time: 1500,
          average_speed: 3.33,
          start_date: "2026-06-21T12:00:00.000Z",
        },
      ];
    },

    async ensureDefaultSuggestedTracks() {
      return ensureDefaultSuggestedTracks();
    },

    async listSuggestedTracks() {
      await ensureDefaultSuggestedTracks();
      const rows = await db.select().from(bodyWarSuggestedTracks);
      return rows.map(toSuggestedTrack).sort(compareSuggestedTracks);
    },

    async findSuggestedTrack(idOrSlug) {
      await ensureDefaultSuggestedTracks();
      const [row] = await db
        .select()
        .from(bodyWarSuggestedTracks)
        .where(
          isUuid(idOrSlug)
            ? eq(bodyWarSuggestedTracks.id, idOrSlug)
            : eq(bodyWarSuggestedTracks.slug, idOrSlug),
        );
      return row ? toSuggestedTrack(row) : null;
    },

    async createSuggestedTrack(input: CreateSuggestedTrackInput) {
      const rows = await db.select().from(bodyWarSuggestedTracks);
      const slug = uniqueSuggestedTrackSlug(
        suggestedTrackSlug(input.name),
        rows.map((row) => String(row.slug)),
      );
      const row = firstRow(
        await db
          .insert(bodyWarSuggestedTracks)
          .values({
            slug,
            name: input.name,
            placeLabel: input.placeLabel,
            city: input.city,
            country: input.country ?? "BR",
            distanceHintMeters: input.distanceHintMeters ?? null,
            status: "needs_evidence",
            geometryAuthority: "needs_evidence",
            suggestedByPrincipalId: input.principalId,
            publicNote: input.publicNote ?? "",
          })
          .returning(),
      );
      return toSuggestedTrack(row);
    },

    async addActivityEvidenceCandidate(input: AddActivityEvidenceCandidateInput) {
      const row = firstRow(
        await db
          .insert(bodyWarActivityEvidenceCandidates)
          .values({
            suggestedTrackId: input.suggestedTrackId,
            principalId: input.principalId,
            provider: "strava",
            providerActivityId: input.providerActivityId,
            redactedSummary: input.redactedSummary,
            consentText: input.consentText,
            consentedAt: new Date(input.consentedAt),
            status: "submitted",
          })
          .returning(),
      );

      const [track] = await db
        .select()
        .from(bodyWarSuggestedTracks)
        .where(eq(bodyWarSuggestedTracks.id, input.suggestedTrackId));
      if (track?.status === "needs_evidence") {
        await db
          .update(bodyWarSuggestedTracks)
          .set({ status: "evidence_submitted", updatedAt: new Date() })
          .where(eq(bodyWarSuggestedTracks.id, input.suggestedTrackId))
          .returning();
      }

      return toActivityEvidenceCandidate(row);
    },

    async listActivityEvidenceCandidates(suggestedTrackId, principalId) {
      const rows = await db
        .select()
        .from(bodyWarActivityEvidenceCandidates)
        .where(eq(bodyWarActivityEvidenceCandidates.suggestedTrackId, suggestedTrackId));
      return rows
        .map(toActivityEvidenceCandidate)
        .filter((candidate) =>
          !principalId || candidate.principalId === principalId,
        )
        .sort((a, b) => b.createdAt.localeCompare(a.createdAt));
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

function toSuggestedTrack(row: DbRow): SuggestedTrack {
  return {
    id: String(row.id),
    slug: String(row.slug),
    name: String(row.name),
    placeLabel: String(row.placeLabel),
    city: String(row.city),
    country: String(row.country),
    distanceHintMeters: row.distanceHintMeters === null ||
      row.distanceHintMeters === undefined
      ? null
      : Number(row.distanceHintMeters),
    status: row.status as SuggestedTrack["status"],
    geometryAuthority: String(row.geometryAuthority),
    suggestedByPrincipalId: row.suggestedByPrincipalId === null ||
      row.suggestedByPrincipalId === undefined
      ? null
      : String(row.suggestedByPrincipalId),
    publicNote: String(row.publicNote ?? ""),
    createdAt: toIso(row.createdAt),
    updatedAt: toIso(row.updatedAt),
  };
}

function toActivityEvidenceCandidate(row: DbRow): ActivityEvidenceCandidate {
  return {
    id: String(row.id),
    suggestedTrackId: String(row.suggestedTrackId),
    principalId: String(row.principalId),
    provider: "strava",
    providerActivityId: String(row.providerActivityId),
    redactedSummary: { ...(row.redactedSummary as Record<string, unknown>) },
    consentText: String(row.consentText),
    consentedAt: toIso(row.consentedAt),
    status: row.status as ActivityEvidenceCandidate["status"],
    createdAt: toIso(row.createdAt),
    updatedAt: toIso(row.updatedAt),
  };
}

function toIso(value: unknown): string {
  return value instanceof Date ? value.toISOString() : new Date(String(value)).toISOString();
}

function isUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}

function uniqueSuggestedTrackSlug(baseSlug: string, existingSlugs: string[]): string {
  const used = new Set(existingSlugs);
  let slug = baseSlug;
  let suffix = 2;
  while (used.has(slug)) {
    slug = `${baseSlug}-${suffix}`;
    suffix += 1;
  }
  return slug;
}

function compareSuggestedTracks(a: SuggestedTrack, b: SuggestedTrack): number {
  if (a.slug === DEFAULT_SUGGESTED_TRACK.slug) return -1;
  if (b.slug === DEFAULT_SUGGESTED_TRACK.slug) return 1;
  return b.createdAt.localeCompare(a.createdAt);
}

export type { ActivitySummary };
