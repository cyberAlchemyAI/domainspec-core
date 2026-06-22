export type AuthConfig = {
  sessionTtlMs: number;
  defaultTokenTtlSeconds: number;
  minTokenTtlSeconds: number;
  maxTokenTtlSeconds: number;
  adminLogoutPermissions: string[];
  permissionCatalogNamespace?: string;
};

export const DEFAULT_AUTH_CONFIG: AuthConfig = {
  sessionTtlMs: 8 * 60 * 60 * 1000,
  defaultTokenTtlSeconds: 60 * 60,
  minTokenTtlSeconds: 60,
  maxTokenTtlSeconds: 24 * 60 * 60,
  adminLogoutPermissions: [
    "auth-access-control.admin.logoutAnySession",
    "auth-access-control.admin.*",
  ],
};

export function mergeAuthConfig(config: Partial<AuthConfig> = {}): AuthConfig {
  return {
    ...DEFAULT_AUTH_CONFIG,
    ...config,
    adminLogoutPermissions:
      config.adminLogoutPermissions ?? DEFAULT_AUTH_CONFIG.adminLogoutPermissions,
  };
}
