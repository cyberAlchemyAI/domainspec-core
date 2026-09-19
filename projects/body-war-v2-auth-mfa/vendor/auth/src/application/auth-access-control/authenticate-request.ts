import type { AuthContext } from "../../domain/auth-access-control/auth-context.vo.js";
import type {
  AuthSessionRepository,
  AuthTokenRepository,
} from "../../domain/auth-access-control/auth.repository.js";
import { AuthValidationError } from "../../domain/auth-access-control/auth.errors.js";
import { validateSidClaim } from "../../domain/auth-access-control/auth.validation.js";
import { systemClock, type Clock } from "../../ports/clock.js";
import { TokenCodecError, type TokenCodec } from "../../ports/token-codec.js";

export type AuthenticateRequestInput = {
  authorizationHeader: string | undefined;
};

export type AuthenticateRequestResult = {
  authContext: AuthContext;
};

export type AuthenticateRequestUseCaseDeps = {
  sessionRepo: AuthSessionRepository;
  tokenRepo: AuthTokenRepository;
  tokenCodec: TokenCodec;
  clock?: Clock;
};

export const authenticateRequestUseCase =
  (deps: AuthenticateRequestUseCaseDeps) =>
  async (
    input: AuthenticateRequestInput,
  ): Promise<AuthenticateRequestResult> => {
    const header = input.authorizationHeader;
    if (!header || !header.startsWith("Bearer ")) {
      throw new AuthValidationError("AUTH_REQUIRED", "Missing bearer token");
    }

    const clock = deps.clock ?? systemClock;
    const rawToken = header.slice(7);
    let payload: { sid?: unknown; jti?: unknown; iat?: number; exp?: number };

    try {
      payload = await deps.tokenCodec.verify(rawToken, { now: clock.now() });
    } catch (error) {
      if (error instanceof TokenCodecError && error.code === "TOKEN_EXPIRED") {
        throw new AuthValidationError("TOKEN_EXPIRED", "Token expired");
      }
      throw new AuthValidationError("INVALID_TOKEN", "Invalid bearer token");
    }

    validateSidClaim(payload.sid);
    const sid = payload.sid;
    const tokenId = typeof payload.jti === "string" ? payload.jti : "";
    if (!tokenId) {
      throw new AuthValidationError("INVALID_TOKEN", "Missing token id claim");
    }

    const tokenRecord = await deps.tokenRepo.findByTokenId(tokenId);
    if (!tokenRecord) {
      throw new AuthValidationError("INVALID_TOKEN", "Unknown bearer token");
    }

    if (tokenRecord.revokedAt !== null) {
      throw new AuthValidationError("TOKEN_REVOKED", "Token has been revoked");
    }

    const session = await deps.sessionRepo.findById(sid);
    if (!session) {
      throw new AuthValidationError("AUTH_REQUIRED", "Inactive or missing session");
    }

    if (session.status !== "ACTIVE") {
      throw new AuthValidationError("AUTH_REQUIRED", "Session is not active");
    }

    if (clock.now() >= session.expiresAt) {
      throw new AuthValidationError("AUTH_REQUIRED", "Session has expired");
    }

    return {
      authContext: {
        principalId: session.principalId,
        sessionId: session.id,
        permissions: session.effectivePermissions,
        tokenId,
        issuedAt: payload.iat ? new Date(payload.iat * 1000) : clock.now(),
        expiresAt: payload.exp ? new Date(payload.exp * 1000) : session.expiresAt,
      },
    };
  };
