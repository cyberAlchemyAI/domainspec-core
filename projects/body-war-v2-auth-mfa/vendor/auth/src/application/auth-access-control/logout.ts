import type { AuthEventHandler } from "../../domain/auth-access-control/auth.events.js";
import type {
  AuthSessionRepository,
  AuthTokenRepository,
} from "../../domain/auth-access-control/auth.repository.js";
import { AuthValidationError } from "../../domain/auth-access-control/auth.errors.js";
import {
  mergeAuthConfig,
  type AuthConfig,
} from "../../ports/auth-config.js";
import { systemClock, type Clock } from "../../ports/clock.js";

export type LogoutInput = {
  sessionId: string;
  callerId: string;
  callerPermissions: string[];
  tokenId?: string;
  revokeAllSessionTokens?: boolean;
};

export type LogoutResult = {
  sessionId: string;
  revokedTokenIds: string[];
};

export type LogoutUseCaseDeps = {
  sessionRepo: AuthSessionRepository;
  tokenRepo: AuthTokenRepository;
  clock?: Clock;
  config?: Partial<AuthConfig>;
  onEvent?: AuthEventHandler;
};

export const logoutUseCase =
  (deps: LogoutUseCaseDeps) =>
  async (input: LogoutInput): Promise<LogoutResult> => {
    const config = mergeAuthConfig(deps.config);
    const clock = deps.clock ?? systemClock;
    const session = await deps.sessionRepo.findById(input.sessionId);
    if (!session || session.status !== "ACTIVE") {
      throw new AuthValidationError(
        "AUTH_REQUIRED",
        "Session not found or not active",
      );
    }

    const isOwner = input.callerId === session.principalId;
    const isAdmin = input.callerPermissions.some((permission) =>
      config.adminLogoutPermissions.includes(permission),
    );

    if (!isOwner && !isAdmin) {
      throw new AuthValidationError(
        "FORBIDDEN",
        "Caller does not own session and lacks admin permission",
      );
    }

    const now = clock.now();
    let revokedTokenIds: string[];

    if (input.tokenId && !input.revokeAllSessionTokens) {
      await deps.tokenRepo.revoke(input.tokenId, now, "LOGOUT_TARGETED");
      revokedTokenIds = [input.tokenId];
      await deps.onEvent?.({
        type: "TokenRevoked",
        tokenId: input.tokenId,
        sessionId: input.sessionId,
        revokedAt: now,
        reason: "LOGOUT_TARGETED",
      });
    } else {
      revokedTokenIds = await deps.tokenRepo.revokeAllBySessionId(
        input.sessionId,
        now,
        "LOGOUT_ALL_SESSION_TOKENS",
      );
      for (const tokenId of revokedTokenIds) {
        await deps.onEvent?.({
          type: "TokenRevoked",
          tokenId,
          sessionId: input.sessionId,
          revokedAt: now,
          reason: "LOGOUT_ALL_SESSION_TOKENS",
        });
      }
    }

    await deps.sessionRepo.updateStatus(input.sessionId, "TERMINATED");
    await deps.onEvent?.({
      type: "LogoutCompleted",
      principalId: session.principalId,
      sessionId: input.sessionId,
      revokedTokenIds,
      occurredAt: now,
    });

    return {
      sessionId: input.sessionId,
      revokedTokenIds,
    };
  };
