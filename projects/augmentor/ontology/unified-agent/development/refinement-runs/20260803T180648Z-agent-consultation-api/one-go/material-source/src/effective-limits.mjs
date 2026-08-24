export const LIMIT_KEYS = ["maxCandidates", "maxRecords", "maxSources", "maxBytes", "maxTokens", "maxMillis"];

export const effectiveLimits = ({ service, policy, request }) => Object.fromEntries(
  LIMIT_KEYS.map((key) => {
    const values = [service?.[key], policy?.[key], request?.[key]];
    if (!values.every((value) => Number.isInteger(value) && value > 0)) throw new TypeError(`invalid limit ${key}`);
    return [key, Math.min(...values)];
  })
);

export const requestLifetime = ({ deadlineAt, cancelled = false, now = Date.now() }) => {
  if (cancelled) return { active: false, reasonCode: "CANCELLED" };
  const deadline = Date.parse(deadlineAt);
  if (!Number.isFinite(deadline)) throw new TypeError("invalid deadlineAt");
  if (now >= deadline) return { active: false, reasonCode: "DEADLINE_REACHED" };
  return { active: true, remainingMillis: deadline - now };
};

export const TOKEN_ESTIMATOR = Object.freeze({ id: "utf8-bytes-div-4", version: "1.0.0" });
export const estimateTokens = (value) => Math.ceil(Buffer.byteLength(typeof value === "string" ? value : JSON.stringify(value), "utf8") / 4);
