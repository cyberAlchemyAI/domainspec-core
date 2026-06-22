import type { AccessToken } from "../../domain/auth-access-control/access-token.entity.js";
import type {
  AuthSessionRepository,
  AuthTokenRepository,
  MutableAuthRepositorySet,
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
import { randomUuidGenerator, type IdGenerator } from "../../ports/id-generator.js";

export type PrincipalRecord = Principal & {
  identifier: string;
  credentialHash: string;
};

export type MemoryAuthRepositorySeed = {
  principals?: PrincipalRecord[];
  sessions?: Session[];
  tokens?: AccessToken[];
  grants?: PermissionGrant[];
  idGenerator?: IdGenerator;
};

export type MemoryAuthRepositories = MutableAuthRepositorySet & {
  clear(): void;
  snapshot(): {
    principals: PrincipalRecord[];
    sessions: Session[];
    tokens: AccessToken[];
    grants: PermissionGrant[];
  };
};

export function createMemoryAuthRepositories(
  seed: MemoryAuthRepositorySeed = {},
): MemoryAuthRepositories {
  const idGenerator = seed.idGenerator ?? randomUuidGenerator;
  const principals = new Map<string, PrincipalRecord>();
  const principalIdsByIdentifier = new Map<string, string>();
  const sessions = new Map<string, Session>();
  const tokens = new Map<string, AccessToken>();
  const grants = new Map<string, PermissionGrant>();

  for (const principal of seed.principals ?? []) {
    const cloned = clonePrincipalRecord(principal);
    principals.set(cloned.id, cloned);
    principalIdsByIdentifier.set(cloned.identifier, cloned.id);
  }

  for (const session of seed.sessions ?? []) {
    sessions.set(session.id, cloneSession(session));
  }

  for (const token of seed.tokens ?? []) {
    tokens.set(token.tokenId, cloneAccessToken(token));
  }

  for (const grant of seed.grants ?? []) {
    grants.set(grantKey(grant), clonePermissionGrant(grant));
  }

  const principalRepo: MutablePrincipalRepository = {
    async create(input: CreatePrincipalInput): Promise<Principal> {
      const id = input.id ?? idGenerator.id();
      const record: PrincipalRecord = {
        id,
        identifier: input.identifier,
        subjectType: input.subjectType,
        status: "ACTIVE",
        roleKeys: [...input.roleKeys],
        directPermissions: [...input.directPermissions],
        credentialHash: input.credentialHash,
      };
      principals.set(id, record);
      principalIdsByIdentifier.set(input.identifier, id);
      return toPrincipal(record);
    },

    async findById(id: string): Promise<Principal | null> {
      const principal = principals.get(id);
      return principal ? toPrincipal(principal) : null;
    },

    async findByIdentifier(identifier: string): Promise<Principal | null> {
      const id = principalIdsByIdentifier.get(identifier);
      const principal = id ? principals.get(id) : undefined;
      return principal ? toPrincipal(principal) : null;
    },

    async findCredentialByIdentifier(
      identifier: string,
    ): Promise<PrincipalCredential | null> {
      const id = principalIdsByIdentifier.get(identifier);
      const principal = id ? principals.get(id) : undefined;
      return principal
        ? {
            principal: toPrincipal(principal),
            credentialHash: principal.credentialHash,
          }
        : null;
    },

    async updateCredentialHashByIdentifier(
      identifier: string,
      credentialHash: string,
    ): Promise<void> {
      const id = principalIdsByIdentifier.get(identifier);
      const principal = id ? principals.get(id) : undefined;
      if (principal) {
        principal.credentialHash = credentialHash;
      }
    },
  };

  const sessionRepo: AuthSessionRepository = {
    async create(session: Session): Promise<Session> {
      sessions.set(session.id, cloneSession(session));
      return cloneSession(session);
    },

    async findById(id: string): Promise<Session | null> {
      const session = sessions.get(id);
      return session ? cloneSession(session) : null;
    },

    async updateStatus(id: string, status: SessionStatus): Promise<void> {
      const session = sessions.get(id);
      if (session) {
        sessions.set(id, { ...session, status });
      }
    },

    async findActiveByPrincipalId(principalId: string): Promise<Session[]> {
      return [...sessions.values()]
        .filter(
          (session) =>
            session.principalId === principalId && session.status === "ACTIVE",
        )
        .map(cloneSession);
    },
  };

  const tokenRepo: AuthTokenRepository = {
    async create(token: AccessToken): Promise<AccessToken> {
      tokens.set(token.tokenId, cloneAccessToken(token));
      return cloneAccessToken(token);
    },

    async findByTokenId(tokenId: string): Promise<AccessToken | null> {
      const token = tokens.get(tokenId);
      return token ? cloneAccessToken(token) : null;
    },

    async findActiveBySessionId(sessionId: string): Promise<AccessToken[]> {
      return [...tokens.values()]
        .filter(
          (token) => token.sessionId === sessionId && token.revokedAt === null,
        )
        .map(cloneAccessToken);
    },

    async revoke(
      tokenId: string,
      revokedAt: Date,
      _reason: string,
    ): Promise<void> {
      const token = tokens.get(tokenId);
      if (token) {
        tokens.set(tokenId, { ...token, revokedAt: new Date(revokedAt) });
      }
    },

    async revokeAllBySessionId(
      sessionId: string,
      revokedAt: Date,
      reason: string,
    ): Promise<string[]> {
      const tokenIds = [...tokens.values()]
        .filter(
          (token) => token.sessionId === sessionId && token.revokedAt === null,
        )
        .map((token) => token.tokenId);

      for (const tokenId of tokenIds) {
        await this.revoke(tokenId, revokedAt, reason);
      }

      return tokenIds;
    },
  };

  const grantRepo: MutablePermissionGrantRepository = {
    async findByGranteeKeys(granteeKeys: string[]): Promise<PermissionGrant[]> {
      if (granteeKeys.length === 0) return [];
      const allowed = new Set(granteeKeys);
      return [...grants.values()]
        .filter((grant) => allowed.has(grant.granteeKey))
        .map(clonePermissionGrant);
    },

    async findAll(options = {}): Promise<PermissionGrant[]> {
      return [...grants.values()]
        .filter((grant) =>
          options.namespace
            ? grant.permissionKey.startsWith(options.namespace)
            : true,
        )
        .map(clonePermissionGrant);
    },

    async upsertGrant(
      input: UpsertPermissionGrantInput,
    ): Promise<PermissionGrant> {
      const key = grantKey(input);
      const existing = grants.get(key);
      if (existing) {
        return clonePermissionGrant(existing);
      }

      const grant: PermissionGrant = {
        grantId: idGenerator.id(),
        granteeType: input.granteeType,
        granteeKey: input.granteeKey,
        permissionKey: input.permissionKey,
        effect: input.effect,
        createdAt: new Date(),
      };
      grants.set(key, grant);
      return clonePermissionGrant(grant);
    },
  };

  return {
    principalRepo,
    sessionRepo,
    tokenRepo,
    grantRepo,
    clear() {
      principals.clear();
      principalIdsByIdentifier.clear();
      sessions.clear();
      tokens.clear();
      grants.clear();
    },
    snapshot() {
      return {
        principals: [...principals.values()].map(clonePrincipalRecord),
        sessions: [...sessions.values()].map(cloneSession),
        tokens: [...tokens.values()].map(cloneAccessToken),
        grants: [...grants.values()].map(clonePermissionGrant),
      };
    },
  };
}

function toPrincipal(record: PrincipalRecord): Principal {
  return {
    id: record.id,
    subjectType: record.subjectType,
    status: record.status,
    roleKeys: [...record.roleKeys],
    directPermissions: [...record.directPermissions],
  };
}

function clonePrincipalRecord(record: PrincipalRecord): PrincipalRecord {
  return {
    ...record,
    roleKeys: [...record.roleKeys],
    directPermissions: [...record.directPermissions],
  };
}

function cloneSession(session: Session): Session {
  return {
    ...session,
    effectivePermissions: [...session.effectivePermissions],
    createdAt: new Date(session.createdAt),
    expiresAt: new Date(session.expiresAt),
  };
}

function cloneAccessToken(token: AccessToken): AccessToken {
  return {
    ...token,
    issuedAt: new Date(token.issuedAt),
    expiresAt: new Date(token.expiresAt),
    revokedAt: token.revokedAt ? new Date(token.revokedAt) : null,
    scope: [...token.scope],
  };
}

function clonePermissionGrant(grant: PermissionGrant): PermissionGrant {
  return {
    ...grant,
    createdAt: new Date(grant.createdAt),
  };
}

function grantKey(
  grant:
    | PermissionGrant
    | Pick<PermissionGrant, "granteeType" | "granteeKey" | "permissionKey">,
): string {
  return `${grant.granteeType}:${grant.granteeKey}:${grant.permissionKey}`;
}
