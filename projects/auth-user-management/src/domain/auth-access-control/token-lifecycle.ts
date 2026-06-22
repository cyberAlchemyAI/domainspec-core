import type { TokenStatus } from "./access-token.entity.js";
import { AuthValidationError } from "./auth.errors.js";

type TokenTransitionEvent = "TokenIssued" | "TokenExpired" | "TokenRevoked";

const VALID_TRANSITIONS: Record<
  string,
  { event: TokenTransitionEvent; to: TokenStatus }[]
> = {
  "[new]": [{ event: "TokenIssued", to: "ACTIVE" }],
  ACTIVE: [
    { event: "TokenExpired", to: "EXPIRED" },
    { event: "TokenRevoked", to: "REVOKED" },
  ],
  EXPIRED: [],
  REVOKED: [],
};

export function transitionToken(
  currentStatus: TokenStatus | "[new]",
  event: TokenTransitionEvent,
): TokenStatus {
  const allowed = VALID_TRANSITIONS[currentStatus] ?? [];
  const match = allowed.find((transition) => transition.event === event);

  if (!match) {
    throw new AuthValidationError(
      "AUTH_REQUIRED",
      `Invalid token transition: ${currentStatus} + ${event}`,
    );
  }

  return match.to;
}

export function isTerminalTokenState(status: TokenStatus): boolean {
  return status === "EXPIRED" || status === "REVOKED";
}
