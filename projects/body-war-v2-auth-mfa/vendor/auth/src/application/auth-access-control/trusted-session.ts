import type { AccessToken } from "../../domain/auth-access-control/access-token.entity.js";
import type { AuthEventHandler } from "../../domain/auth-access-control/auth.events.js";
import type {
  AuthSessionRepository,
  AuthTokenRepository,
  PermissionGrantRepository,
  PrincipalRepository,
} from "../../domain/auth-access-control/auth.repository.js";
import { AuthValidationError } from "../../domain/auth-access-control/auth.errors.js";
import {
  deduplicatePermissions,
  validateTokenExpiry,
} from "../../domain/auth-access-control/auth.validation.js";
import { resolveEffectivePermissions } from "../../domain/auth-access-control/permission-resolution.js";
import type { Session } from "../../domain/auth-access-control/session.entity.js";
import {
  mergeAuthConfig,
  type AuthConfig,
} from "../../ports/auth-config.js";
import { noopAuthTelemetry, type AuthTelemetry } from "../../ports/auth-telemetry.js";
import { systemClock, type Clock } from "../../ports/clock.js";
import { randomUuidGenerator, type IdGenerator } from "../../ports/id-generator.js";
import type { TokenCodec } from "../../ports/token-codec.js";

export type TrustedSessionInput = {
  principalId: string;
  ttlSeconds?: number | undefined;
  metadata?: Record<string, unknown> | undefined;
};

export type TrustedSessionResult = {
  accessToken: string;
  expiresAt: Date;
  issuedAt: Date;
  sessionId: string;
  tokenId: string;
  principalId: string;
  permissions: string[];
};

export type TrustedSessionUseCaseDeps = {
  principalRepo: PrincipalRepository;
  sessionRepo: AuthSessionRepository;
  tokenRepo: AuthTokenRepository;
  grantRepo: PermissionGrantRepository;
  tokenCodec: TokenCodec;
  clock?: Clock;
  idGenerator?: IdGenerator;
  config?: Partial<AuthConfig>;
  telemetry?: AuthTelemetry;
  onEvent?: AuthEventHandler;
};

export const createTrustedSessionUseCase =
  (deps: TrustedSessionUseCaseDeps) =>
  async (input: TrustedSessionInput): Promise<TrustedSessionResult> => {
    const config = mergeAuthConfig(deps.config);
    const clock = deps.clock ?? systemClock;
    const idGenerator = deps.idGenerator ?? randomUuidGenerator;
    const telemetry = deps.telemetry ?? noopAuthTelemetry;
    const principalId = input.principalId.trim();

    if (!principalId) {
      telemetry.record?.("auth.trusted_session.denied", {
        reason: "AUTH_REQUIRED",
      });
      throw new AuthValidationError("AUTH_REQUIRED", "Missing principal id");
    }

    const principal = await deps.principalRepo.findById(principalId);
    if (!principal || principal.status !== "ACTIVE") {
      telemetry.record?.("auth.trusted_session.denied", {
        reason: "PRINCIPAL_DISABLED",
      });
      throw new AuthValidationError(
        "PRINCIPAL_DISABLED",
        "Principal not found or disabled",
      );
    }

    const grants = await deps.grantRepo.findByGranteeKeys([
      ...principal.roleKeys,
      principal.id,
    ]);
    const effectivePermissions = deduplicatePermissions(
      resolveEffectivePermissions(
        principal.roleKeys,
        principal.directPermissions,
        grants,
      ),
    );
    const tokenTtlSeconds = input.ttlSeconds ?? config.defaultTokenTtlSeconds;
    if (
      tokenTtlSeconds < config.minTokenTtlSeconds ||
      tokenTtlSeconds > config.maxTokenTtlSeconds
    ) {
      throw new AuthValidationError(
        "FORBIDDEN",
        `ttlSeconds must be between ${config.minTokenTtlSeconds} and ${config.maxTokenTtlSeconds}`,
      );
    }

    const now = clock.now();
    const session: Session = {
      id: idGenerator.id(),
      principalId: principal.id,
      status: "ACTIVE",
      effectivePermissions,
      createdAt: now,
      expiresAt: new Date(now.getTime() + config.sessionTtlMs),
    };

    await deps.sessionRepo.create(session);

    const issuedAt = clock.now();
    const tokenId = idGenerator.id();
    const expiresAt = new Date(issuedAt.getTime() + tokenTtlSeconds * 1000);
    validateTokenExpiry(issuedAt, expiresAt);
    const accessToken = await deps.tokenCodec.sign(
      {
        sid: session.id,
        jti: tokenId,
      },
      {
        expiresInSeconds: tokenTtlSeconds,
        issuedAt,
      },
    );
    const tokenRecord: AccessToken = {
      tokenId,
      sessionId: session.id,
      issuedAt,
      expiresAt,
      revokedAt: null,
      scope: session.effectivePermissions,
    };

    await deps.tokenRepo.create(tokenRecord);
    await deps.onEvent?.({
      type: "TokenIssued",
      tokenId,
      sessionId: session.id,
      issuedAt,
      expiresAt,
    });
    telemetry.record?.("auth.trusted_session.completed", {
      result: "success",
      metadata: input.metadata ? JSON.stringify(input.metadata) : "",
    });

    return {
      accessToken,
      expiresAt,
      issuedAt,
      sessionId: session.id,
      tokenId,
      principalId: principal.id,
      permissions: effectivePermissions,
    };
  };
