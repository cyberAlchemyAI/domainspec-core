import { randomBytes } from "node:crypto";
import {
  authenticateRequestUseCase,
  authorizeRequestUseCase,
  createTrustedSessionUseCase,
  logoutUseCase,
  AuthValidationError,
  type AuthContext,
  type AuthRepositorySet,
  type MutableAuthRepositorySet,
  type TokenCodec,
} from "@domainspec/auth-user-management";
import { clearCookieHeader, cookieHeader } from "./cookies.js";
import { appError, type AppError, type AppResult, type CookieMap } from "./types.js";

export type BrowserSessionBinding = {
  sessionCookie: string;
  csrfToken: string;
  expiresAt: string;
};

export type BrowserSessionAdapterConfig = {
  sessionCookieName: string;
  csrfCookieName: string;
  csrfHeaderName: string;
  allowedOrigins: Set<string>;
  secureCookies: boolean;
  sessionTtlSeconds: number;
};

export type BrowserSessionAdapterDeps = {
  repos: MutableAuthRepositorySet;
  tokenCodec: TokenCodec;
  config: BrowserSessionAdapterConfig;
};

export type AuthenticateBrowserRequestInput = {
  cookies: CookieMap;
  headers?: Record<string, string | undefined> | undefined;
  method: string;
  requiredPermission?: string | undefined;
  route?: string | undefined;
};

export function createBrowserSessionAdapter(
  deps: BrowserSessionAdapterDeps,
) {
  const config = deps.config;

  return {
    async createSession(input: {
      principalId: string;
      ttlSeconds?: number | undefined;
      metadata?: Record<string, unknown> | undefined;
    }): Promise<AppResult<{
      auth: AuthContext;
      binding: BrowserSessionBinding;
    }>> {
      try {
        const result = await createTrustedSessionUseCase({
          ...deps.repos,
          tokenCodec: deps.tokenCodec,
        })({
          principalId: input.principalId,
          ttlSeconds: input.ttlSeconds,
          metadata: input.metadata,
        });
        return {
          ok: true,
          value: {
            auth: {
              principalId: result.principalId,
              sessionId: result.sessionId,
              tokenId: result.tokenId,
              permissions: result.permissions,
              issuedAt: result.issuedAt,
              expiresAt: result.expiresAt,
            },
            binding: {
              sessionCookie: result.accessToken,
              csrfToken: createCsrfToken(),
              expiresAt: result.expiresAt.toISOString(),
            },
          },
        };
      } catch (error) {
        return { ok: false, error: mapAuthError(error) };
      }
    },

    async authenticate(
      input: AuthenticateBrowserRequestInput,
    ): Promise<AppResult<AuthContext>> {
      try {
        const sessionCookie = input.cookies[config.sessionCookieName];
        const authenticated = await authenticateRequestUseCase({
          sessionRepo: deps.repos.sessionRepo,
          tokenRepo: deps.repos.tokenRepo,
          tokenCodec: deps.tokenCodec,
        })({
          authorizationHeader: sessionCookie ? `Bearer ${sessionCookie}` : undefined,
        });
        const authContext = authenticated.authContext;

        validateBrowserGuards(config, input, authContext);

        if (input.requiredPermission) {
          await authorizeRequestUseCase({
            grantRepo: deps.repos.grantRepo,
          })({
            authContext,
            requiredPermission: input.requiredPermission,
          });
        }

        return { ok: true, value: authContext };
      } catch (error) {
        return { ok: false, error: mapAuthError(error, input.route) };
      }
    },

    async logout(cookies: CookieMap): Promise<void> {
      const sessionCookie = cookies[config.sessionCookieName];
      if (!sessionCookie) return;
      try {
        const authenticated = await authenticateRequestUseCase({
          sessionRepo: deps.repos.sessionRepo,
          tokenRepo: deps.repos.tokenRepo,
          tokenCodec: deps.tokenCodec,
        })({ authorizationHeader: `Bearer ${sessionCookie}` });
        await logoutUseCase({
          sessionRepo: deps.repos.sessionRepo,
          tokenRepo: deps.repos.tokenRepo,
        })({
          sessionId: authenticated.authContext.sessionId,
          callerId: authenticated.authContext.principalId,
          callerPermissions: authenticated.authContext.permissions,
          tokenId: authenticated.authContext.tokenId,
        });
      } catch {
        return;
      }
    },

    sessionCookieHeader(
      binding: BrowserSessionBinding,
      maxAgeSeconds = config.sessionTtlSeconds,
    ): string {
      return cookieHeader(config.sessionCookieName, binding.sessionCookie, {
        httpOnly: true,
        secure: config.secureCookies,
        sameSite: "Lax",
        path: "/",
        maxAgeSeconds,
      });
    },

    csrfCookieHeader(
      binding: BrowserSessionBinding,
      maxAgeSeconds = config.sessionTtlSeconds,
    ): string {
      return cookieHeader(config.csrfCookieName, binding.csrfToken, {
        httpOnly: false,
        secure: config.secureCookies,
        sameSite: "Lax",
        path: "/",
        maxAgeSeconds,
      });
    },

    clearCookieHeaders(): string[] {
      return [
        clearCookieHeader(config.sessionCookieName),
        clearCookieHeader(config.csrfCookieName),
      ];
    },
  };
}

function validateBrowserGuards(
  config: BrowserSessionAdapterConfig,
  input: AuthenticateBrowserRequestInput,
  authContext: AuthContext,
): void {
  if (!isUnsafeMethod(input.method)) return;

  const origin = input.headers?.origin ?? input.headers?.Origin;
  if (!origin || !config.allowedOrigins.has(origin)) {
    throw appError("origin_not_allowed", 403, "Origin is not allowed", {
      route: input.route ?? "",
      principalId: authContext.principalId,
    });
  }

  const cookieToken = input.cookies[config.csrfCookieName];
  const headerToken =
    input.headers?.[config.csrfHeaderName] ??
    input.headers?.[config.csrfHeaderName.toLowerCase()];
  if (!cookieToken || !headerToken || cookieToken !== headerToken) {
    throw appError("csrf_required", 403, "CSRF token required", {
      route: input.route ?? "",
      principalId: authContext.principalId,
    });
  }
}

function isUnsafeMethod(method: string): boolean {
  return !["GET", "HEAD", "OPTIONS"].includes(method.toUpperCase());
}

function createCsrfToken(): string {
  return randomBytes(32).toString("base64url");
}

function mapAuthError(error: unknown, route?: string): AppError {
  if (isAppError(error)) return error;
  if (error instanceof AuthValidationError) {
    const code = error.code.toLowerCase();
    const status = statusForAuthCode(error.code);
    return appError(code, status, error.message, {
      ...(error.details ?? {}),
      route: route ?? "",
    });
  }
  return appError(
    "internal_error",
    500,
    error instanceof Error ? error.message : "Unknown auth error",
  );
}

function statusForAuthCode(code: string): number {
  if (
    code === "AUTH_REQUIRED" ||
    code === "INVALID_TOKEN" ||
    code === "TOKEN_EXPIRED" ||
    code === "TOKEN_REVOKED"
  ) {
    return 401;
  }
  return 403;
}

function isAppError(error: unknown): error is AppError {
  return (
    typeof error === "object" &&
    error !== null &&
    "code" in error &&
    "status" in error &&
    "message" in error
  );
}

export type PackageAuthRepositories = AuthRepositorySet;
