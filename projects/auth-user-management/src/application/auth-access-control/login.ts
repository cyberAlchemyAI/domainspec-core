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
import {
  evaluateLoginRiskPolicy,
  type LoginRiskContext,
} from "../../domain/auth-access-control/login-risk-policy.js";
import { resolveEffectivePermissions } from "../../domain/auth-access-control/permission-resolution.js";
import type { Session } from "../../domain/auth-access-control/session.entity.js";
import {
  mergeAuthConfig,
  type AuthConfig,
} from "../../ports/auth-config.js";
import { noopAuthTelemetry, type AuthTelemetry } from "../../ports/auth-telemetry.js";
import { systemClock, type Clock } from "../../ports/clock.js";
import { randomUuidGenerator, type IdGenerator } from "../../ports/id-generator.js";
import type { PasswordService } from "../../ports/password-service.js";
import type { TokenCodec } from "../../ports/token-codec.js";

export type LoginInput = {
  identifier: string;
  secret: string;
  context?: LoginRiskContext;
};

export type LoginResult = {
  accessToken: string;
  expiresAt: Date;
  issuedAt: Date;
  sessionId: string;
  tokenId: string;
  principalId: string;
  permissions: string[];
};

export type IssueAccessTokenInput = {
  sessionId: string;
  ttlSeconds: number;
};

export type IssueAccessTokenResult = {
  accessToken: string;
  expiresAt: Date;
  issuedAt: Date;
  tokenId: string;
};

export type LoginUseCaseDeps = {
  principalRepo: PrincipalRepository;
  sessionRepo: AuthSessionRepository;
  tokenRepo: AuthTokenRepository;
  grantRepo: PermissionGrantRepository;
  tokenCodec: TokenCodec;
  passwordService: PasswordService;
  clock?: Clock;
  idGenerator?: IdGenerator;
  config?: Partial<AuthConfig>;
  telemetry?: AuthTelemetry;
  onEvent?: AuthEventHandler;
};

export type IssueAccessTokenUseCaseDeps = {
  sessionRepo: AuthSessionRepository;
  tokenRepo: AuthTokenRepository;
  tokenCodec: TokenCodec;
  clock?: Clock;
  idGenerator?: IdGenerator;
  config?: Partial<AuthConfig>;
  telemetry?: AuthTelemetry;
  onEvent?: AuthEventHandler;
};

export const loginUseCase =
  (deps: LoginUseCaseDeps) =>
  async (input: LoginInput): Promise<LoginResult> => {
    const config = mergeAuthConfig(deps.config);
    const clock = deps.clock ?? systemClock;
    const idGenerator = deps.idGenerator ?? randomUuidGenerator;
    const telemetry = deps.telemetry ?? noopAuthTelemetry;

    if (!input.identifier || !input.secret) {
      telemetry.record?.("auth.login.denied", { reason: "INVALID_CREDENTIALS" });
      throw new AuthValidationError(
        "INVALID_CREDENTIALS",
        "Missing identifier or secret",
      );
    }

    const credential = await deps.principalRepo.findCredentialByIdentifier(
      input.identifier,
    );
    if (!credential || credential.principal.status !== "ACTIVE") {
      telemetry.record?.("auth.login.denied", {
        reason: "PRINCIPAL_DISABLED",
      });
      throw new AuthValidationError(
        "PRINCIPAL_DISABLED",
        "Principal not found or disabled",
      );
    }

    const principal = credential.principal;
    const validCredential = await deps.passwordService.verify(
      input.secret,
      credential.credentialHash,
    );
    if (!validCredential) {
      telemetry.record?.("auth.login.denied", { reason: "INVALID_CREDENTIALS" });
      throw new AuthValidationError("INVALID_CREDENTIALS", "Invalid credentials");
    }

    evaluateLoginRiskPolicy(input.context);

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

    const tokenResult = await issueAccessTokenInternal({
      session,
      ttlSeconds: config.defaultTokenTtlSeconds,
      tokenRepo: deps.tokenRepo,
      tokenCodec: deps.tokenCodec,
      clock,
      idGenerator,
      telemetry,
      onEvent: deps.onEvent,
    });

    await deps.onEvent?.({
      type: "LoginSucceeded",
      principalId: principal.id,
      sessionId: session.id,
      occurredAt: now,
    });
    telemetry.record?.("auth.login.completed", { result: "success" });

    return {
      accessToken: tokenResult.accessToken,
      expiresAt: tokenResult.expiresAt,
      issuedAt: tokenResult.issuedAt,
      sessionId: session.id,
      tokenId: tokenResult.tokenId,
      principalId: principal.id,
      permissions: effectivePermissions,
    };
  };

export const issueAccessTokenUseCase =
  (deps: IssueAccessTokenUseCaseDeps) =>
  async (input: IssueAccessTokenInput): Promise<IssueAccessTokenResult> => {
    const config = mergeAuthConfig(deps.config);
    const session = await deps.sessionRepo.findById(input.sessionId);
    if (!session || session.status !== "ACTIVE") {
      throw new AuthValidationError("AUTH_REQUIRED", "Session not active");
    }

    if (
      input.ttlSeconds < config.minTokenTtlSeconds ||
      input.ttlSeconds > config.maxTokenTtlSeconds
    ) {
      throw new AuthValidationError(
        "FORBIDDEN",
        `ttlSeconds must be between ${config.minTokenTtlSeconds} and ${config.maxTokenTtlSeconds}`,
      );
    }

    return issueAccessTokenInternal({
      session,
      ttlSeconds: input.ttlSeconds,
      tokenRepo: deps.tokenRepo,
      tokenCodec: deps.tokenCodec,
      clock: deps.clock ?? systemClock,
      idGenerator: deps.idGenerator ?? randomUuidGenerator,
      telemetry: deps.telemetry ?? noopAuthTelemetry,
      onEvent: deps.onEvent,
    });
  };

type IssueAccessTokenInternalInput = {
  session: Session;
  ttlSeconds: number;
  tokenRepo: AuthTokenRepository;
  tokenCodec: TokenCodec;
  clock: Clock;
  idGenerator: IdGenerator;
  telemetry: AuthTelemetry;
  onEvent?: AuthEventHandler | undefined;
};

async function issueAccessTokenInternal(
  input: IssueAccessTokenInternalInput,
): Promise<IssueAccessTokenResult> {
  const issuedAt = input.clock.now();
  const tokenId = input.idGenerator.id();
  const expiresAt = new Date(issuedAt.getTime() + input.ttlSeconds * 1000);
  validateTokenExpiry(issuedAt, expiresAt);

  const accessToken = await input.tokenCodec.sign(
    {
      sid: input.session.id,
      jti: tokenId,
    },
    {
      expiresInSeconds: input.ttlSeconds,
      issuedAt,
    },
  );

  const tokenRecord: AccessToken = {
    tokenId,
    sessionId: input.session.id,
    issuedAt,
    expiresAt,
    revokedAt: null,
    scope: input.session.effectivePermissions,
  };

  await input.tokenRepo.create(tokenRecord);
  await input.onEvent?.({
    type: "TokenIssued",
    tokenId,
    sessionId: input.session.id,
    issuedAt,
    expiresAt,
  });
  input.telemetry.record?.("auth.token.issued", { result: "success" });

  return { accessToken, expiresAt, issuedAt, tokenId };
}
