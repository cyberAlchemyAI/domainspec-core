import { PERMISSION_KEY_PATTERN } from "./auth-context.vo.js";
import { AuthValidationError } from "./auth.errors.js";

export function validatePermissionKey(key: string): void {
  if (!PERMISSION_KEY_PATTERN.test(key)) {
    throw new AuthValidationError(
      "FORBIDDEN",
      `Permission key is not canonical: ${key}`,
    );
  }
}

export function validateTokenExpiry(issuedAt: Date, expiresAt: Date): void {
  if (expiresAt.getTime() <= issuedAt.getTime()) {
    throw new AuthValidationError(
      "INVALID_TOKEN",
      "Token expiresAt must be after issuedAt",
    );
  }
}

export function validateRevokedNotActive(
  revokedAt: Date | null,
  status: string,
): void {
  if (revokedAt !== null && status === "ACTIVE") {
    throw new AuthValidationError(
      "TOKEN_REVOKED",
      "Revoked token cannot have ACTIVE status",
    );
  }
}

export function deduplicatePermissions(permissions: string[]): string[] {
  return [...new Set(permissions)];
}

export function validateSidClaim(sid: unknown): asserts sid is string {
  if (typeof sid !== "string" || sid.trim().length === 0) {
    throw new AuthValidationError("INVALID_TOKEN", "Missing sid claim in token");
  }
}
