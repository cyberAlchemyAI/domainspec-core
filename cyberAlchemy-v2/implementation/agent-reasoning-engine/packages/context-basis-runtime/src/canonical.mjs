import {
  canonicalJson,
  canonicalizeJson,
  deepFreeze,
  sha256HexText,
} from "../../intent-route-resolver/index.mjs";

export {canonicalJson, canonicalizeJson, deepFreeze, sha256HexText};

export function digestValue(value) {
  return sha256HexText(canonicalJson(canonicalizeJson(value)));
}

export function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

export function nonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

export function uniqueStrings(value) {
  if (!Array.isArray(value)) return [];
  return [...new Set(value.filter(nonEmptyString).map((item) => item.trim()))].sort();
}

export function fail(stage, reasonCodes, residue = []) {
  return deepFreeze(canonicalizeJson({
    schema_version: "are.context-basis-failure/v1",
    ok: false,
    stage,
    reason_codes: [...new Set(reasonCodes)].sort(),
    residue,
    authority_effect: "none",
    effect_calls: 0,
  }));
}

export function succeed(schemaVersion, value, extras = {}) {
  const canonicalValue = canonicalizeJson(value);
  return deepFreeze(canonicalizeJson({
    schema_version: schemaVersion,
    ok: true,
    value: canonicalValue,
    digest: digestValue(canonicalValue),
    authority_effect: "none",
    ...extras,
  }));
}
