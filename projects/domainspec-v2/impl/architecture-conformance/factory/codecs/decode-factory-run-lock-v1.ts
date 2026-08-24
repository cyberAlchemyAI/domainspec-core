import type { FactoryRunLockV1 } from "../contracts/factory-run-lock-v1.js";
import { canonicalJson, fail, isRecord, sha256 } from "../shared/canonical.js";

export const decodeFactoryRunLockV1 = (value: unknown): FactoryRunLockV1 => {
  const record = isRecord(value) ? value : fail("FACTORY_LOCK_INVALID");
  if (record.schema_version !== "FactoryRunLock/v1" ||
      record.authority_effect !== "none" || typeof record.lock_sha256 !== "string") {
    fail("FACTORY_LOCK_INVALID");
  }
  const body = Object.fromEntries(Object.entries(record).filter(([key]) => key !== "lock_sha256"));
  if (sha256(canonicalJson(body)) !== record.lock_sha256) fail("FACTORY_LOCK_STALE");
  return record as FactoryRunLockV1;
};
