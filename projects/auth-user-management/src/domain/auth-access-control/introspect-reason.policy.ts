export type InactiveReason =
  | "NOT_FOUND"
  | "TOKEN_REVOKED"
  | "TOKEN_EXPIRED"
  | "SESSION_TERMINATED"
  | "SESSION_EXPIRED";

type TokenInfo = {
  revokedAt: Date | null;
  expiresAt: Date;
};

type SessionInfo = {
  status: string;
  expiresAt?: Date;
} | null;

export function resolveIntrospectInactiveReason(
  tokenInfo: TokenInfo | null,
  sessionInfo: SessionInfo,
  now = new Date(),
): InactiveReason | null {
  if (!tokenInfo) return "NOT_FOUND";
  if (tokenInfo.revokedAt !== null) return "TOKEN_REVOKED";
  if (now >= tokenInfo.expiresAt) return "TOKEN_EXPIRED";
  if (!sessionInfo) return "NOT_FOUND";
  if (sessionInfo.status === "TERMINATED") return "SESSION_TERMINATED";
  if (sessionInfo.status === "EXPIRED") return "SESSION_EXPIRED";
  if (sessionInfo.expiresAt && now >= sessionInfo.expiresAt) {
    return "SESSION_EXPIRED";
  }
  return null;
}
