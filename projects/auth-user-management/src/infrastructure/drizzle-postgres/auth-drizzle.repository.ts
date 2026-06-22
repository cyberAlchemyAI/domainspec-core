import { and, eq, isNull } from "drizzle-orm";
import type { AccessToken } from "../../domain/auth-access-control/access-token.entity.js";
import type {
  AuthSessionRepository,
  AuthTokenRepository,
  MutablePermissionGrantRepository,
  MutablePrincipalRepository,
} from "../../domain/auth-access-control/auth.repository.js";
import type {
  PermissionGrant,
  UpsertPermissionGrantInput,
} from "../../domain/auth-access-control/permission-grant.entity.js";
import type {
  CreatePrincipalInput,
  Principal,
  PrincipalCredential,
} from "../../domain/auth-access-control/principal.entity.js";
import type { Session, SessionStatus } from "../../domain/auth-access-control/session.entity.js";
import {
  authAccessTokens,
  authPermissionGrants,
  authPrincipals,
  authSessions,
} from "./schema.js";

export type AuthDrizzleDatabase = {
  insert(table: unknown): unknown;
  select(fields?: unknown): unknown;
  update(table: unknown): unknown;
};

type DbRow = Record<string, any>;
type QueryResult<T> = Promise<T[]>;

export function createDrizzlePrincipalRepository(
  database: AuthDrizzleDatabase,
): MutablePrincipalRepository {
  const db = database as DrizzleLikeDatabase;

  return {
    async create(input: CreatePrincipalInput): Promise<Principal> {
      const values: Record<string, unknown> = {
        identifier: input.identifier,
        subjectType: input.subjectType,
        roleKeys: input.roleKeys,
        directPermissions: input.directPermissions,
        credentialHash: input.credentialHash,
        status: "ACTIVE",
      };
      if (input.id) {
        values.id = input.id;
      }

      const result = firstRow(
        await db.insert(authPrincipals).values(values).returning(),
      );
      return toPrincipal(result);
    },

    async findById(id: string): Promise<Principal | null> {
      const [result] = await db
        .select()
        .from(authPrincipals)
        .where(eq(authPrincipals.id, id));
      return result ? toPrincipal(result) : null;
    },

    async findByIdentifier(identifier: string): Promise<Principal | null> {
      const [result] = await db
        .select()
        .from(authPrincipals)
        .where(eq(authPrincipals.identifier, identifier));
      return result ? toPrincipal(result) : null;
    },

    async findCredentialByIdentifier(
      identifier: string,
    ): Promise<PrincipalCredential | null> {
      const [result] = await db
        .select()
        .from(authPrincipals)
        .where(eq(authPrincipals.identifier, identifier));
      return result
        ? {
            principal: toPrincipal(result),
            credentialHash: String(result.credentialHash),
          }
        : null;
    },

    async updateCredentialHashByIdentifier(
      identifier: string,
      credentialHash: string,
    ): Promise<void> {
      await db
        .update(authPrincipals)
        .set({ credentialHash, updatedAt: new Date() })
        .where(eq(authPrincipals.identifier, identifier));
    },
  };
}

export function createDrizzleSessionRepository(
  database: AuthDrizzleDatabase,
): AuthSessionRepository {
  const db = database as DrizzleLikeDatabase;

  return {
    async create(session: Session): Promise<Session> {
      const result = firstRow(
        await db
        .insert(authSessions)
        .values({
          id: session.id,
          principalId: session.principalId,
          status: session.status,
          effectivePermissions: session.effectivePermissions,
          createdAt: session.createdAt,
          expiresAt: session.expiresAt,
        })
          .returning(),
      );
      return toSession(result);
    },

    async findById(id: string): Promise<Session | null> {
      const [result] = await db
        .select()
        .from(authSessions)
        .where(eq(authSessions.id, id));
      return result ? toSession(result) : null;
    },

    async updateStatus(id: string, status: SessionStatus): Promise<void> {
      await db.update(authSessions).set({ status }).where(eq(authSessions.id, id));
    },

    async findActiveByPrincipalId(principalId: string): Promise<Session[]> {
      const results = await db
        .select()
        .from(authSessions)
        .where(
          and(
            eq(authSessions.principalId, principalId),
            eq(authSessions.status, "ACTIVE"),
          ),
        );
      return results.map(toSession);
    },
  };
}

export function createDrizzleTokenRepository(
  database: AuthDrizzleDatabase,
): AuthTokenRepository {
  const db = database as DrizzleLikeDatabase;

  return {
    async create(token: AccessToken): Promise<AccessToken> {
      const result = firstRow(
        await db
        .insert(authAccessTokens)
        .values({
          tokenId: token.tokenId,
          sessionId: token.sessionId,
          issuedAt: token.issuedAt,
          expiresAt: token.expiresAt,
          revokedAt: token.revokedAt,
          scope: token.scope,
        })
          .returning(),
      );
      return toAccessToken(result);
    },

    async findByTokenId(tokenId: string): Promise<AccessToken | null> {
      const [result] = await db
        .select()
        .from(authAccessTokens)
        .where(eq(authAccessTokens.tokenId, tokenId));
      return result ? toAccessToken(result) : null;
    },

    async findActiveBySessionId(sessionId: string): Promise<AccessToken[]> {
      const results = await db
        .select()
        .from(authAccessTokens)
        .where(
          and(
            eq(authAccessTokens.sessionId, sessionId),
            isNull(authAccessTokens.revokedAt),
          ),
        );
      return results.map(toAccessToken);
    },

    async revoke(
      tokenId: string,
      revokedAt: Date,
      reason: string,
    ): Promise<void> {
      await db
        .update(authAccessTokens)
        .set({ revokedAt, revokeReason: reason })
        .where(eq(authAccessTokens.tokenId, tokenId));
    },

    async revokeAllBySessionId(
      sessionId: string,
      revokedAt: Date,
      reason: string,
    ): Promise<string[]> {
      const activeTokens = await db
        .select({ tokenId: authAccessTokens.tokenId })
        .from(authAccessTokens)
        .where(
          and(
            eq(authAccessTokens.sessionId, sessionId),
            isNull(authAccessTokens.revokedAt),
          ),
        );

      const tokenIds = activeTokens.map((token) => String(token.tokenId));
      for (const tokenId of tokenIds) {
        await db
          .update(authAccessTokens)
          .set({ revokedAt, revokeReason: reason })
          .where(eq(authAccessTokens.tokenId, String(tokenId)));
      }

      return tokenIds;
    },
  };
}

export function createDrizzlePermissionGrantRepository(
  database: AuthDrizzleDatabase,
): MutablePermissionGrantRepository {
  const db = database as DrizzleLikeDatabase;

  return {
    async findByGranteeKeys(granteeKeys: string[]): Promise<PermissionGrant[]> {
      if (granteeKeys.length === 0) return [];
      const results = await db.select().from(authPermissionGrants);
      const allowed = new Set(granteeKeys);
      return results
        .filter((row) => allowed.has(String(row.granteeKey)))
        .map(toPermissionGrant);
    },

    async findAll(options = {}): Promise<PermissionGrant[]> {
      const results = await db.select().from(authPermissionGrants);
      return results
        .filter((row) =>
          options.namespace
            ? String(row.permissionKey).startsWith(options.namespace)
            : true,
        )
        .map(toPermissionGrant);
    },

    async upsertGrant(
      grant: UpsertPermissionGrantInput,
    ): Promise<PermissionGrant> {
      const existing = await db
        .select()
        .from(authPermissionGrants)
        .where(
          and(
            eq(authPermissionGrants.granteeType, grant.granteeType),
            eq(authPermissionGrants.granteeKey, grant.granteeKey),
            eq(authPermissionGrants.permissionKey, grant.permissionKey),
          ),
        );

      if (existing.length > 0) {
        return toPermissionGrant(firstRow(existing));
      }

      const result = firstRow(
        await db
        .insert(authPermissionGrants)
        .values({
          granteeType: grant.granteeType,
          granteeKey: grant.granteeKey,
          permissionKey: grant.permissionKey,
          effect: grant.effect,
        })
          .returning(),
      );

      return toPermissionGrant(result);
    },
  };
}

export function createDrizzleAuthRepositories(
  database: AuthDrizzleDatabase,
) {
  return {
    principalRepo: createDrizzlePrincipalRepository(database),
    sessionRepo: createDrizzleSessionRepository(database),
    tokenRepo: createDrizzleTokenRepository(database),
    grantRepo: createDrizzlePermissionGrantRepository(database),
  };
}

type DrizzleLikeDatabase = {
  insert(table: unknown): {
    values(value: unknown): { returning(): QueryResult<DbRow> };
  };
  select(fields?: unknown): {
    from(table: unknown): {
      where(condition: unknown): QueryResult<DbRow>;
    } & QueryResult<DbRow>;
  };
  update(table: unknown): {
    set(value: unknown): {
      where(condition: unknown): Promise<unknown>;
    };
  };
};

function firstRow(rows: DbRow[]): DbRow {
  const row = rows[0];
  if (!row) {
    throw new Error("Expected database row");
  }
  return row;
}

function toPrincipal(row: DbRow): Principal {
  return {
    id: String(row.id),
    subjectType: row.subjectType as Principal["subjectType"],
    status: row.status as Principal["status"],
    roleKeys: [...(row.roleKeys as string[])],
    directPermissions: [...(row.directPermissions as string[])],
  };
}

function toSession(row: DbRow): Session {
  return {
    id: String(row.id),
    principalId: String(row.principalId),
    status: row.status as SessionStatus,
    effectivePermissions: [...(row.effectivePermissions as string[])],
    createdAt: row.createdAt as Date,
    expiresAt: row.expiresAt as Date,
  };
}

function toAccessToken(row: DbRow): AccessToken {
  return {
    tokenId: String(row.tokenId),
    sessionId: String(row.sessionId),
    issuedAt: row.issuedAt as Date,
    expiresAt: row.expiresAt as Date,
    revokedAt: (row.revokedAt as Date | null) ?? null,
    scope: [...(row.scope as string[])],
  };
}

function toPermissionGrant(row: DbRow): PermissionGrant {
  return {
    grantId: String(row.grantId),
    granteeType: row.granteeType as PermissionGrant["granteeType"],
    granteeKey: String(row.granteeKey),
    permissionKey: String(row.permissionKey),
    effect: row.effect as PermissionGrant["effect"],
    createdAt: row.createdAt as Date,
  };
}
