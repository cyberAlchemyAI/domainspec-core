import {
  jsonb,
  pgEnum,
  pgTable,
  timestamp,
  uniqueIndex,
  uuid,
  varchar,
} from "drizzle-orm/pg-core";

export const principalSubjectTypeEnum = pgEnum("principal_subject_type", [
  "user",
  "service",
  "automation",
]);

export const principalStatusEnum = pgEnum("principal_status", [
  "ACTIVE",
  "DISABLED",
]);

export const sessionStatusEnum = pgEnum("session_status", [
  "ACTIVE",
  "TERMINATED",
  "EXPIRED",
]);

export const permissionEffectEnum = pgEnum("permission_effect", [
  "ALLOW",
  "DENY",
]);

export const granteeTypeEnum = pgEnum("grantee_type", ["role", "principal"]);

export const authPrincipals = pgTable("auth_principals", {
  id: uuid("id").defaultRandom().primaryKey(),
  identifier: varchar("identifier", { length: 255 }).notNull().unique(),
  subjectType: principalSubjectTypeEnum("subject_type").notNull(),
  status: principalStatusEnum("status").default("ACTIVE").notNull(),
  roleKeys: jsonb("role_keys").$type<string[]>().notNull().default([]),
  directPermissions: jsonb("direct_permissions")
    .$type<string[]>()
    .notNull()
    .default([]),
  credentialHash: varchar("credential_hash", { length: 255 }).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const authSessions = pgTable("auth_sessions", {
  id: uuid("id").defaultRandom().primaryKey(),
  principalId: uuid("principal_id")
    .references(() => authPrincipals.id)
    .notNull(),
  status: sessionStatusEnum("status").default("ACTIVE").notNull(),
  effectivePermissions: jsonb("effective_permissions")
    .$type<string[]>()
    .notNull()
    .default([]),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  expiresAt: timestamp("expires_at").notNull(),
});

export const authAccessTokens = pgTable("auth_access_tokens", {
  tokenId: uuid("token_id").defaultRandom().primaryKey(),
  sessionId: uuid("session_id")
    .references(() => authSessions.id)
    .notNull(),
  issuedAt: timestamp("issued_at").defaultNow().notNull(),
  expiresAt: timestamp("expires_at").notNull(),
  revokedAt: timestamp("revoked_at"),
  revokeReason: varchar("revoke_reason", { length: 100 }),
  scope: jsonb("scope").$type<string[]>().notNull().default([]),
});

export const authPermissionGrants = pgTable(
  "auth_permission_grants",
  {
    grantId: uuid("grant_id").defaultRandom().primaryKey(),
    granteeType: granteeTypeEnum("grantee_type").notNull(),
    granteeKey: varchar("grantee_key", { length: 255 }).notNull(),
    permissionKey: varchar("permission_key", { length: 255 }).notNull(),
    effect: permissionEffectEnum("effect").default("ALLOW").notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
  },
  (table) => ({
    uniqueGrant: uniqueIndex("auth_permission_grants_unique_grant").on(
      table.granteeType,
      table.granteeKey,
      table.permissionKey,
    ),
  }),
);

export const authAccessControlSchema = {
  authPrincipals,
  authSessions,
  authAccessTokens,
  authPermissionGrants,
  principalSubjectTypeEnum,
  principalStatusEnum,
  sessionStatusEnum,
  permissionEffectEnum,
  granteeTypeEnum,
};
