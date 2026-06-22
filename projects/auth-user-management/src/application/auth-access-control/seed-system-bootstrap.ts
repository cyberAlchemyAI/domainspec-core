import type {
  MutablePermissionGrantRepository,
  MutablePrincipalRepository,
} from "../../domain/auth-access-control/auth.repository.js";
import type { RoleDefinition } from "../../domain/auth-access-control/role-definition.js";
import type { PasswordService } from "../../ports/password-service.js";

export type SeedSystemBootstrapInput = {
  adminIdentifier?: string;
  adminPassword?: string;
  generatedPassword?: string;
  adminRoleKey?: string;
  roleDefinitions: RoleDefinition[];
};

export type SeedSystemBootstrapResult = {
  adminIdentifier: string;
  adminCreated: boolean;
  credentialRefreshed: boolean;
  passwordGenerated: boolean;
  generatedPassword?: string;
  grantsUpserted: number;
};

export type SeedSystemBootstrapDeps = {
  principalRepo: MutablePrincipalRepository;
  grantRepo: MutablePermissionGrantRepository;
  passwordService: PasswordService;
};

export const seedSystemBootstrap = async (
  deps: SeedSystemBootstrapDeps,
  input: SeedSystemBootstrapInput,
): Promise<SeedSystemBootstrapResult> => {
  const adminIdentifier = input.adminIdentifier ?? "admin";
  const adminRoleKey = input.adminRoleKey ?? "admin";
  const existingAdmin =
    await deps.principalRepo.findByIdentifier(adminIdentifier);
  let adminCreated = false;
  let credentialRefreshed = false;
  let generatedPassword: string | undefined;

  if (!existingAdmin) {
    const password = input.adminPassword ?? input.generatedPassword;
    if (!password) {
      throw new Error(
        "seedSystemBootstrap requires adminPassword or generatedPassword",
      );
    }

    generatedPassword = input.adminPassword ? undefined : password;
    await deps.principalRepo.create({
      identifier: adminIdentifier,
      subjectType: "user",
      roleKeys: [adminRoleKey],
      directPermissions: [],
      credentialHash: await deps.passwordService.hash(password),
    });
    adminCreated = true;
  } else if (input.adminPassword) {
    await deps.principalRepo.updateCredentialHashByIdentifier(
      adminIdentifier,
      await deps.passwordService.hash(input.adminPassword),
    );
    credentialRefreshed = true;
  }

  let grantsUpserted = 0;
  for (const role of input.roleDefinitions) {
    for (const permissionKey of role.permissions) {
      await deps.grantRepo.upsertGrant({
        granteeType: "role",
        granteeKey: role.roleKey,
        permissionKey,
        effect: "ALLOW",
      });
      grantsUpserted += 1;
    }
  }

  const result: SeedSystemBootstrapResult = {
    adminIdentifier,
    adminCreated,
    credentialRefreshed,
    passwordGenerated: generatedPassword !== undefined,
    grantsUpserted,
  };

  if (generatedPassword !== undefined) {
    result.generatedPassword = generatedPassword;
  }

  return result;
};
