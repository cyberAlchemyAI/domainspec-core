import type { PermissionGrant } from "./permission-grant.entity.js";

export type PermissionDecision = "ALLOW" | "DENY";

export const matchPermission = (
  grantedPermission: string,
  requiredPermission: string,
): boolean => {
  const grantedParts = grantedPermission.split(".");
  const requiredParts = requiredPermission.split(".");

  for (let i = 0; i < requiredParts.length; i += 1) {
    const grantedPart = grantedParts[i];
    const requiredPart = requiredParts[i];

    if (!grantedPart) {
      return false;
    }

    if (grantedPart === "*") {
      return true;
    }

    if (grantedPart !== requiredPart) {
      return false;
    }
  }

  return grantedParts.length <= requiredParts.length;
};

export const hasRequiredPermission = (
  grantedPermissions: string[],
  requiredPermission: string,
): boolean => {
  if (grantedPermissions.length === 0) {
    return false;
  }

  return grantedPermissions.some((permission) =>
    matchPermission(permission, requiredPermission),
  );
};

export function resolvePermissionDecision(
  grants: Array<{ permissionKey: string; effect: "ALLOW" | "DENY" }>,
  requiredPermission: string,
): PermissionDecision {
  const requiredParts = requiredPermission.split(".");
  let hasDeny = false;
  let hasExactAllow = false;
  let hasScopedWildcard = false;
  let hasGlobalWildcard = false;

  for (const grant of grants) {
    if (matchPermissionKey(grant.permissionKey, requiredParts)) {
      if (grant.effect === "DENY") {
        hasDeny = true;
      } else {
        const grantParts = grant.permissionKey.split(".");
        if (isExactMatch(grantParts, requiredParts)) {
          hasExactAllow = true;
        } else if (isGlobalWildcard(grantParts)) {
          hasGlobalWildcard = true;
        } else {
          hasScopedWildcard = true;
        }
      }
    }
  }

  if (hasDeny) return "DENY";
  if (hasExactAllow || hasScopedWildcard || hasGlobalWildcard) return "ALLOW";
  return "DENY";
}

function matchPermissionKey(
  grantKey: string,
  requiredParts: string[],
): boolean {
  const grantParts = grantKey.split(".");
  for (let i = 0; i < requiredParts.length; i += 1) {
    const grantPart = grantParts[i];
    if (!grantPart) return false;
    if (grantPart === "*") return true;
    if (grantPart !== requiredParts[i]) return false;
  }

  return grantParts.length <= requiredParts.length;
}

function isExactMatch(grantParts: string[], requiredParts: string[]): boolean {
  if (grantParts.length !== requiredParts.length) return false;
  return grantParts.every((part, index) => part === requiredParts[index]);
}

function isGlobalWildcard(grantParts: string[]): boolean {
  return grantParts.length >= 1 && grantParts[0] === "*";
}

export function resolveEffectivePermissions(
  roleKeys: string[],
  directPermissions: string[],
  grants: PermissionGrant[],
): string[] {
  const granteeKeys = new Set([...roleKeys]);
  const allowSet = new Set(directPermissions);

  for (const grant of grants) {
    if (
      grant.effect === "ALLOW" &&
      (granteeKeys.has(grant.granteeKey) || grant.granteeType === "principal")
    ) {
      allowSet.add(grant.permissionKey);
    }
  }

  return [...allowSet];
}
