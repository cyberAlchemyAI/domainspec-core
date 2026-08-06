import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { effectiveLimits, estimateTokens, requestLifetime } from "./effective-limits.mjs";
import { ProjectionReader, digestValue } from "./projection-reader.mjs";
import { validate } from "../scripts/validate-contract.mjs";

const ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const querySchema = JSON.parse(await readFile(path.join(ROOT, "schemas/query.schema.json"), "utf8"));
const VERSION = "augmentor.consultation.result@0.1.0";
const base = (query, status) => ({ schemaVersion: VERSION, requestId: query?.requestId ?? "unknown", questionId: query?.questionId ?? "unknown", status });

const statementsFor = (items, metrics, manifest) => items.flatMap(({ record, relevance }) => Object.entries({ label: record.label, summary: record.summary, ...record.fields }).map(([predicate, object]) => ({
  statementId: `stmt-${digestValue(`${record.id}:${predicate}:${object}`).slice(0, 12)}`,
  subjectId: record.id,
  predicate,
  object,
  displayText: String(object),
  transformation: { kind: "copied-field", version: manifest.compilerVersion, inputFieldRefs: [`${record.id}.${predicate}`] },
  sourceHandles: record.sourceHandles,
  freshness: "current",
  claimCeiling: "fixture-bound evidence only",
  forbiddenInferences: ["authority", "approval", "production-readiness"],
  relevance: { algorithmId: "exact-token-overlap", algorithmVersion: "1.0.0", scale: "normalized-0-1", value: relevance, normalizedQueryDigest: metrics.normalizedQueryDigest, projectionDigest: manifest.outputDigest, candidateScopeDigest: metrics.candidateScopeDigest },
  confidence: record.confidence
})));

export class ConsultationBoundary {
  constructor({ projection, manifest, serviceLimits }) {
    this.projection = projection;
    this.manifest = manifest;
    this.serviceLimits = serviceLimits;
  }

  consult(query, context) {
    if (!context?.principal?.opaquePrincipalRef || !context?.policy?.digest || context.principal.audience !== "augmentor-consultation") return { ...base(query, "denied"), reasonCode: "ACCESS_NOT_AVAILABLE", retryable: false };
    const queryErrors = validate(query, querySchema);
    if (queryErrors.length) return { ...base(query, "invalid_request"), issueCodes: ["QUERY_INVALID"] };
    let lifetime;
    try { lifetime = requestLifetime({ deadlineAt: context.deadlineAt, cancelled: context.cancelled, now: context.now }); }
    catch { return { ...base(query, "invalid_request"), issueCodes: ["EXECUTION_CONTEXT_INVALID"] }; }
    if (!lifetime.active) return { ...base(query, "temporary_failure"), reasonCode: lifetime.reasonCode, retryable: lifetime.reasonCode !== "CANCELLED" };
    let limits;
    try { limits = effectiveLimits({ service: this.serviceLimits, policy: context.policy.limits, request: query.limits }); }
    catch { return { ...base(query, "invalid_request"), issueCodes: ["LIMITS_INVALID"] }; }
    if (context.policy.projectionDigest !== this.manifest.outputDigest) return { ...base(query, "stale"), projectionDigest: this.manifest.outputDigest, freshness: "stale" };
    if (query.scope.maxFreshnessAgeSeconds !== undefined && context.projectionAgeSeconds > query.scope.maxFreshnessAgeSeconds) return { ...base(query, "stale"), projectionDigest: this.manifest.outputDigest, freshness: "stale" };
    const reader = new ProjectionReader({ projection: this.projection, manifest: this.manifest });
    const found = reader.read(query, limits, context.policy.allowedViews);
    if (!found.records.length) return { ...base(query, "no_match"), searchedProjectionDigest: this.manifest.outputDigest };
    const statements = statementsFor(found.records, found, this.manifest);
    if (statements.some((statement) => !statement.sourceHandles.length)) return { ...base(query, "insufficient_evidence"), gapCodes: ["SOURCE_BINDING_MISSING"] };
    const conflict = this.projection.structuredConflicts.find((item) => found.records.some(({ record }) => record.id === item.subjectId));
    if (conflict) return { ...base(query, "conflict"), statementIds: conflict.statementIds };
    const records = found.records.map(({ record }) => ({ id: record.id, kind: record.kind, label: record.label, summary: record.summary, viewIds: record.viewIds, sourceHandles: record.sourceHandles }));
    const kind = query.operation === "context" ? "context" : query.operation === "lookup" ? "records" : "statements";
    const result = { kind, records: kind === "statements" ? [] : records, statements: kind === "records" ? [] : statements };
    const bytes = Buffer.byteLength(JSON.stringify(result));
    const extraLimits = [bytes > limits.maxBytes ? "bytes" : null, estimateTokens(result) > limits.maxTokens ? "tokens" : null].filter(Boolean);
    if (extraLimits.length && !records.length) return { ...base(query, "budget_exceeded"), limitCodes: extraLimits };
    const limitsHit = [...new Set([...found.limitsHit, ...extraLimits])];
    if (limitsHit.length) return { ...base(query, "partial"), result, projectionDigest: this.manifest.outputDigest, complete: false, limitsHit };
    return { ...base(query, "ok"), result, projectionDigest: this.manifest.outputDigest, complete: true };
  }
}

export const loadFixtureBoundary = async (serviceLimits) => {
  const [projection, manifest] = await Promise.all([
    readFile(path.join(ROOT, "fixtures/generated/projection.json"), "utf8").then(JSON.parse),
    readFile(path.join(ROOT, "fixtures/generated/projection-manifest.json"), "utf8").then(JSON.parse)
  ]);
  return new ConsultationBoundary({ projection, manifest, serviceLimits });
};
