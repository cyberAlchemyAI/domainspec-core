import type { AuthContext } from "../../domain/auth-access-control/auth-context.vo.js";
import { isCanonicalPermissionKey } from "../../domain/auth-access-control/auth-context.vo.js";
import type { AuthEventHandler } from "../../domain/auth-access-control/auth.events.js";
import type { PermissionGrantRepository } from "../../domain/auth-access-control/auth.repository.js";
import { AuthValidationError } from "../../domain/auth-access-control/auth.errors.js";
import { resolvePermissionDecision } from "../../domain/auth-access-control/permission-resolution.js";
import { systemClock, type Clock } from "../../ports/clock.js";

export type AuthorizeRequestInput = {
  authContext: AuthContext;
  requiredPermission: string;
};

export type AuthorizeRequestResult = {
  allowed: boolean;
};

export type AuthorizeRequestUseCaseDeps = {
  grantRepo: PermissionGrantRepository;
  clock?: Clock;
  onEvent?: AuthEventHandler;
};

export const authorizeRequestUseCase =
  (deps: AuthorizeRequestUseCaseDeps) =>
  async (input: AuthorizeRequestInput): Promise<AuthorizeRequestResult> => {
    if (!isCanonicalPermissionKey(input.requiredPermission)) {
      throw new AuthValidationError(
        "FORBIDDEN",
        `Permission key is not canonical: ${input.requiredPermission}`,
      );
    }

    const sessionGrants = input.authContext.permissions.map((key) => ({
      permissionKey: key,
      effect: "ALLOW" as const,
    }));
    const principalGrants = await deps.grantRepo.findByGranteeKeys([
      input.authContext.principalId,
    ]);
    const denyGrants = principalGrants
      .filter((grant) => grant.effect === "DENY")
      .map((grant) => ({
        permissionKey: grant.permissionKey,
        effect: "DENY" as const,
      }));

    const decision = resolvePermissionDecision(
      [...sessionGrants, ...denyGrants],
      input.requiredPermission,
    );

    if (decision === "DENY") {
      await deps.onEvent?.({
        type: "AccessDenied",
        principalId: input.authContext.principalId,
        requiredPermission: input.requiredPermission,
        reasonCode: "FORBIDDEN",
        occurredAt: (deps.clock ?? systemClock).now(),
      });
      throw new AuthValidationError(
        "FORBIDDEN",
        "Missing required permission",
        { required: input.requiredPermission },
      );
    }

    return { allowed: true };
  };
