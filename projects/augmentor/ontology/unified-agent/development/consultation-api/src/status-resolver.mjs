const PRECEDENCE = [
  ["denied", "denied"],
  ["invalid", "invalid_request"],
  ["temporaryFailure", "temporary_failure"],
  ["stale", "stale"],
  ["conflict", "conflict"],
  ["budgetExceeded", "budget_exceeded"],
  ["insufficientEvidence", "insufficient_evidence"],
  ["noMatch", "no_match"],
  ["partial", "partial"]
];

export const resolveStatus = (conditions) => {
  for (const [condition, status] of PRECEDENCE) if (conditions[condition] === true) return status;
  return "ok";
};

export const STATUS_PRECEDENCE = Object.freeze(PRECEDENCE.map(([, status]) => status));
