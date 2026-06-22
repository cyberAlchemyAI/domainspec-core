import type { PermissionGrantRepository } from "../../domain/auth-access-control/auth.repository.js";

export type GetPermissionCatalogInput = {
  namespace?: string;
  includeDeprecated?: boolean;
};

export type PermissionCatalogEntry = {
  key: string;
  description: string;
  status: "active" | "deprecated";
};

export type GetPermissionCatalogResult = {
  permissions: PermissionCatalogEntry[];
};

export const getPermissionCatalogUseCase =
  (grantRepo: PermissionGrantRepository) =>
  async (
    input: GetPermissionCatalogInput,
  ): Promise<GetPermissionCatalogResult> => {
    const options: GetPermissionCatalogInput = {
      includeDeprecated: input.includeDeprecated ?? false,
    };
    if (input.namespace !== undefined) {
      options.namespace = input.namespace;
    }

    const grants = await grantRepo.findAll(options);
    const seen = new Set<string>();
    const permissions: PermissionCatalogEntry[] = [];

    for (const grant of grants) {
      if (seen.has(grant.permissionKey)) {
        continue;
      }
      seen.add(grant.permissionKey);
      permissions.push({
        key: grant.permissionKey,
        description: "",
        status: "active",
      });
    }

    return { permissions };
  };
