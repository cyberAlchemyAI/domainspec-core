import {
  integer,
  jsonb,
  pgEnum,
  pgTable,
  text,
  timestamp,
  uniqueIndex,
  uuid,
  varchar,
} from "drizzle-orm/pg-core";

export const bodyWarProviderStatusEnum = pgEnum("body_war_provider_status", [
  "linked",
  "disconnected",
]);

export const bodyWarSuggestedTrackStatusEnum = pgEnum(
  "body_war_suggested_track_status",
  [
    "needs_evidence",
    "evidence_submitted",
    "operator_review",
    "source_backed",
    "retired",
  ],
);

export const bodyWarActivityEvidenceCandidateStatusEnum = pgEnum(
  "body_war_activity_evidence_candidate_status",
  ["submitted", "operator_review", "accepted", "rejected"],
);

export const bodyWarRunnerProfiles = pgTable("body_war_runner_profiles", {
  principalId: uuid("principal_id").primaryKey(),
  displayName: varchar("display_name", { length: 255 }).notNull(),
  privacyStatus: varchar("privacy_status", { length: 64 })
    .notNull()
    .default("private"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const bodyWarOauthStates = pgTable("body_war_oauth_states", {
  state: varchar("state", { length: 255 }).primaryKey(),
  nonce: varchar("nonce", { length: 255 }).notNull(),
  redirectTarget: varchar("redirect_target", { length: 500 }).notNull().default("/"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  expiresAt: timestamp("expires_at").notNull(),
  consumedAt: timestamp("consumed_at"),
});

export const bodyWarProviderAccounts = pgTable(
  "body_war_provider_accounts",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    principalId: uuid("principal_id").notNull(),
    provider: varchar("provider", { length: 64 }).notNull(),
    providerUserId: varchar("provider_user_id", { length: 255 }).notNull(),
    displayName: varchar("display_name", { length: 255 }),
    scope: jsonb("scope").$type<string[]>().notNull().default([]),
    status: bodyWarProviderStatusEnum("status").notNull().default("linked"),
    metadata: jsonb("metadata")
      .$type<Record<string, unknown>>()
      .notNull()
      .default({}),
    linkedAt: timestamp("linked_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
  },
  (table) => ({
    uniqueProviderUser: uniqueIndex("body_war_provider_unique_user").on(
      table.provider,
      table.providerUserId,
    ),
  }),
);

export const bodyWarProviderTokens = pgTable("body_war_provider_tokens", {
  id: uuid("id").defaultRandom().primaryKey(),
  accountId: uuid("account_id").notNull(),
  accessTokenCiphertext: varchar("access_token_ciphertext", {
    length: 2048,
  }).notNull(),
  refreshTokenCiphertext: varchar("refresh_token_ciphertext", {
    length: 2048,
  }).notNull(),
  expiresAt: timestamp("expires_at").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const bodyWarSuggestedTracks = pgTable(
  "body_war_suggested_tracks",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    slug: varchar("slug", { length: 140 }).notNull(),
    name: varchar("name", { length: 255 }).notNull(),
    placeLabel: varchar("place_label", { length: 255 }).notNull(),
    city: varchar("city", { length: 120 }).notNull(),
    country: varchar("country", { length: 2 }).notNull().default("BR"),
    distanceHintMeters: integer("distance_hint_meters"),
    status: bodyWarSuggestedTrackStatusEnum("status")
      .notNull()
      .default("needs_evidence"),
    geometryAuthority: varchar("geometry_authority", { length: 64 })
      .notNull()
      .default("needs_evidence"),
    suggestedByPrincipalId: uuid("suggested_by_principal_id"),
    publicNote: text("public_note").notNull().default(""),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
  },
  (table) => ({
    uniqueSlug: uniqueIndex("body_war_suggested_tracks_unique_slug").on(
      table.slug,
    ),
  }),
);

export const bodyWarActivityEvidenceCandidates = pgTable(
  "body_war_activity_evidence_candidates",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    suggestedTrackId: uuid("suggested_track_id").notNull(),
    principalId: uuid("principal_id").notNull(),
    provider: varchar("provider", { length: 64 }).notNull().default("strava"),
    providerActivityId: varchar("provider_activity_id", { length: 255 })
      .notNull(),
    redactedSummary: jsonb("redacted_summary")
      .$type<Record<string, unknown>>()
      .notNull(),
    consentText: text("consent_text").notNull(),
    consentedAt: timestamp("consented_at").notNull(),
    status: bodyWarActivityEvidenceCandidateStatusEnum("status")
      .notNull()
      .default("submitted"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
  },
);

export const bodyWarSchema = {
  bodyWarRunnerProfiles,
  bodyWarOauthStates,
  bodyWarProviderAccounts,
  bodyWarProviderTokens,
  bodyWarSuggestedTracks,
  bodyWarActivityEvidenceCandidates,
  bodyWarProviderStatusEnum,
  bodyWarSuggestedTrackStatusEnum,
  bodyWarActivityEvidenceCandidateStatusEnum,
};
