import type {
  AuthSessionRepository,
  AuthTokenRepository,
} from "../../domain/auth-access-control/auth.repository.js";
import {
  resolveIntrospectInactiveReason,
  type InactiveReason,
} from "../../domain/auth-access-control/introspect-reason.policy.js";
import { systemClock, type Clock } from "../../ports/clock.js";
import type { TokenCodec } from "../../ports/token-codec.js";

export type IntrospectTokenInput = {
  token: string;
  includeScopes?: boolean;
};

export type IntrospectTokenResult = {
  active: boolean;
  principalId?: string;
  exp?: number;
  iat?: number;
  scopes?: string[];
  inactiveReason?: InactiveReason;
};

export type IntrospectTokenUseCaseDeps = {
  sessionRepo: AuthSessionRepository;
  tokenRepo: AuthTokenRepository;
  tokenCodec: TokenCodec;
  clock?: Clock;
};

export const introspectTokenUseCase =
  (deps: IntrospectTokenUseCaseDeps) =>
  async (input: IntrospectTokenInput): Promise<IntrospectTokenResult> => {
    const clock = deps.clock ?? systemClock;
    const includeScopes = input.includeScopes ?? true;

    let claims: { jti?: unknown; sid?: unknown; iat?: number; exp?: number };
    try {
      claims = await deps.tokenCodec.verify(input.token, {
        ignoreExpiration: true,
        now: clock.now(),
      });
    } catch {
      return { active: false, inactiveReason: "NOT_FOUND" };
    }

    const tokenId = typeof claims.jti === "string" ? claims.jti : null;
    const sid = typeof claims.sid === "string" ? claims.sid : null;
    if (!tokenId || !sid) {
      return { active: false, inactiveReason: "NOT_FOUND" };
    }

    const tokenRecord = await deps.tokenRepo.findByTokenId(tokenId);
    if (!tokenRecord) {
      return { active: false, inactiveReason: "NOT_FOUND" };
    }

    const session = await deps.sessionRepo.findById(tokenRecord.sessionId);
    const inactiveReason = resolveIntrospectInactiveReason(
      { revokedAt: tokenRecord.revokedAt, expiresAt: tokenRecord.expiresAt },
      session ? { status: session.status, expiresAt: session.expiresAt } : null,
      clock.now(),
    );

    if (inactiveReason) {
      const result: IntrospectTokenResult = {
        active: false,
        inactiveReason,
      };
      if (session) {
        result.principalId = session.principalId;
      }
      result.exp = Math.floor(tokenRecord.expiresAt.getTime() / 1000);
      result.iat = Math.floor(tokenRecord.issuedAt.getTime() / 1000);
      return result;
    }

    if (!session) {
      return { active: false, inactiveReason: "NOT_FOUND" };
    }

    const result: IntrospectTokenResult = {
      active: true,
      principalId: session.principalId,
      exp: Math.floor(tokenRecord.expiresAt.getTime() / 1000),
      iat: Math.floor(tokenRecord.issuedAt.getTime() / 1000),
    };

    if (includeScopes) {
      result.scopes = tokenRecord.scope;
    }

    return result;
  };
