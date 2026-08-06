import { createHash } from "node:crypto";

const sha = (value) => createHash("sha256").update(typeof value === "string" ? value : JSON.stringify(value)).digest("hex");
const tokens = (value) => new Set(value.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean));

export class ProjectionReader {
  constructor({ projection, manifest }) {
    this.projection = projection;
    this.manifest = manifest;
  }

  read(query, limits, allowedViews) {
    const allowed = new Set(allowedViews);
    const candidates = this.projection.records.filter((record) => record.viewIds.some((view) => allowed.has(view)));
    const queryText = query.query.text?.toLowerCase();
    const queryTokens = tokens(queryText ?? "");
    const ranked = candidates.map((record) => {
      const haystack = `${record.label} ${record.summary} ${Object.values(record.fields).join(" ")}`.toLowerCase();
      const overlap = [...queryTokens].filter((token) => haystack.includes(token)).length;
      const relevance = query.query.id === record.id ? 1 : queryTokens.size ? overlap / queryTokens.size : 0;
      return { record, relevance };
    }).filter(({ record, relevance }) => {
      if (query.query.kind && query.query.kind !== record.kind) return false;
      if (query.operation === "lookup") return query.query.id === record.id;
      return relevance > 0;
    }).sort((a, b) => b.relevance - a.relevance || a.record.id.localeCompare(b.record.id));
    const candidateLimitHit = candidates.length > limits.maxCandidates;
    const boundedCandidates = ranked.slice(0, limits.maxCandidates);
    const recordLimitHit = boundedCandidates.length > limits.maxRecords;
    return {
      records: boundedCandidates.slice(0, limits.maxRecords),
      complete: !candidateLimitHit && !recordLimitHit,
      limitsHit: [candidateLimitHit ? "candidates" : null, recordLimitHit ? "records" : null].filter(Boolean),
      normalizedQueryDigest: sha(query.query),
      candidateScopeDigest: sha(candidates.map((record) => record.id).sort())
    };
  }
}

export const digestValue = sha;
