import type { AccessToken } from "./access-token.entity.js";
import type {
  PermissionGrant,
  UpsertPermissionGrantInput,
} from "./permission-grant.entity.js";
import type {
  CreatePrincipalInput,
  Principal,
  PrincipalCredential,
} from "./principal.entity.js";
import type { Session, SessionStatus } from "./session.entity.js";

export type AuthSessionRepository = {
  create(session: Session): Promise<Session>;
  findById(id: string): Promise<Session | null>;
  updateStatus(id: string, status: SessionStatus): Promise<void>;
  findActiveByPrincipalId(principalId: string): Promise<Session[]>;
};

export type AuthTokenRepository = {
  create(token: AccessToken): Promise<AccessToken>;
  findByTokenId(tokenId: string): Promise<AccessToken | null>;
  findActiveBySessionId(sessionId: string): Promise<AccessToken[]>;
  revoke(tokenId: string, revokedAt: Date, reason: string): Promise<void>;
  revokeAllBySessionId(
    sessionId: string,
    revokedAt: Date,
    reason: string,
  ): Promise<string[]>;
};

export type PrincipalRepository = {
  findById(id: string): Promise<Principal | null>;
  findByIdentifier(identifier: string): Promise<Principal | null>;
  findCredentialByIdentifier(
    identifier: string,
  ): Promise<PrincipalCredential | null>;
};

export type MutablePrincipalRepository = PrincipalRepository & {
  create(input: CreatePrincipalInput): Promise<Principal>;
  updateCredentialHashByIdentifier(
    identifier: string,
    credentialHash: string,
  ): Promise<void>;
};

export type PermissionGrantRepository = {
  findByGranteeKeys(granteeKeys: string[]): Promise<PermissionGrant[]>;
  findAll(options?: {
    namespace?: string;
    includeDeprecated?: boolean;
  }): Promise<PermissionGrant[]>;
};

export type MutablePermissionGrantRepository = PermissionGrantRepository & {
  upsertGrant(grant: UpsertPermissionGrantInput): Promise<PermissionGrant>;
};

export type AuthRepositorySet = {
  principalRepo: PrincipalRepository;
  sessionRepo: AuthSessionRepository;
  tokenRepo: AuthTokenRepository;
  grantRepo: PermissionGrantRepository;
};

export type MutableAuthRepositorySet = {
  principalRepo: MutablePrincipalRepository;
  sessionRepo: AuthSessionRepository;
  tokenRepo: AuthTokenRepository;
  grantRepo: MutablePermissionGrantRepository;
};
