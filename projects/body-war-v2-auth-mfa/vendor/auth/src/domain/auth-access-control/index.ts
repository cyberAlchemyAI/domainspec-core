export { type AccessToken, type TokenStatus } from "./access-token.entity.js";
export {
  AUTH_ERROR_CODES,
  type AuthErrorCode,
} from "./auth-error-code.enum.js";
export {
  AuthInternalError,
  AuthValidationError,
} from "./auth.errors.js";
export type {
  AccessDeniedEvent,
  AuthEvent,
  AuthEventHandler,
  LoginSucceededEvent,
  LogoutCompletedEvent,
  TokenIssuedEvent,
  TokenRevokedEvent,
} from "./auth.events.js";
export type {
  AuthRepositorySet,
  AuthSessionRepository,
  AuthTokenRepository,
  MutableAuthRepositorySet,
  MutablePermissionGrantRepository,
  MutablePrincipalRepository,
  PermissionGrantRepository,
  PrincipalRepository,
} from "./auth.repository.js";
export {
  isCanonicalPermissionKey,
  parsePermissionKey,
  PERMISSION_KEY_PATTERN,
  type AuthContext,
  type PermissionKey,
} from "./auth-context.vo.js";
export {
  deduplicatePermissions,
  validatePermissionKey,
  validateRevokedNotActive,
  validateSidClaim,
  validateTokenExpiry,
} from "./auth.validation.js";
export {
  resolveIntrospectInactiveReason,
  type InactiveReason,
} from "./introspect-reason.policy.js";
export {
  evaluateLoginRiskPolicy,
  type LoginRiskContext,
} from "./login-risk-policy.js";
export {
  type GrantEffect,
  type PermissionGrant,
  type UpsertPermissionGrantInput,
} from "./permission-grant.entity.js";
export {
  hasRequiredPermission,
  matchPermission,
  resolveEffectivePermissions,
  resolvePermissionDecision,
  type PermissionDecision,
} from "./permission-resolution.js";
export type {
  CreatePrincipalInput,
  Principal,
  PrincipalCredential,
  PrincipalStatus,
  SubjectType,
} from "./principal.entity.js";
export type { RoleDefinition } from "./role-definition.js";
export { isTerminalSessionState, transitionSession } from "./session-lifecycle.js";
export type { Session, SessionStatus } from "./session.entity.js";
export { isTerminalTokenState, transitionToken } from "./token-lifecycle.js";
