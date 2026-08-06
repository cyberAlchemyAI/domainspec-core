import { canonicalBytes, sha256 } from './canonical-json.mjs';

function recursiveForbidden(value, forbidden, path = '') {
  const findings = [];
  if (!value || typeof value !== 'object') return findings;
  for (const [key, child] of Object.entries(value)) {
    const childPath = path ? `${path}.${key}` : key;
    if (forbidden.has(key)) findings.push({ code: 'FIELD_NOT_ALLOWLISTED', field: childPath });
    findings.push(...recursiveForbidden(child, forbidden, childPath));
  }
  return findings;
}

function safeRecord(record, allowlist) {
  const findings = recursiveForbidden(record, new Set(allowlist.forbidden_fields));
  for (const key of Object.keys(record)) if (!allowlist.record_fields.includes(key)) findings.push({ code: 'FIELD_NOT_ALLOWLISTED', field: key });
  if (!allowlist.record_kinds.includes(record.record_kind)) findings.push({ code: 'RECORD_KIND_NOT_ALLOWLISTED', record_kind: record.record_kind });
  if (record.version_bounds) {
    for (const key of Object.keys(record.version_bounds)) if (!allowlist.version_bound_fields.includes(key)) findings.push({ code: 'FIELD_NOT_ALLOWLISTED', field: `version_bounds.${key}` });
  }
  return findings;
}

function overlayToNeutral(record) {
  return {
    record_id: record.record_id,
    label: record.label,
    summary: record.summary,
    record_kind: record.kind === 'episode' ? 'operational_episode' : record.kind,
    ...(record.relation_name ? { relation_name: record.relation_name } : {}),
    evidence_state: record.evidence_state,
    ...(record.episode_lifecycle_state ? { episode_lifecycle_state: record.episode_lifecycle_state } : {}),
    truth_status: record.truth_status,
    clearing_criteria: record.clearing_criteria ?? [],
  };
}

function recordView(record) {
  if (record.record_kind === 'documentation') return 'documentation';
  if (record.record_kind === 'recipe') return 'recipe';
  return 'operational_episode';
}

export function compileNeutralProjection({ baseRecords = [], overlay, allowlist, requestedViews, grantedViews, compilerVersion = '0.1.0', ownerReviewRef }) {
  const allowedViews = new Set(allowlist.views);
  const grants = new Set(grantedViews);
  const invalidViews = requestedViews.filter(view => !allowedViews.has(view) || !grants.has(view));
  if (invalidViews.length) return { status: 'rejected', leakage_report: invalidViews.map(view => ({ code: 'VIEW_NOT_GRANTED', view })), records: [] };
  if (overlay.status === 'pending') return { status: 'pending', diagnostic: { code: 'PROJECTION_PENDING' }, records: [] };
  if (overlay.status === 'failed') return { status: 'failed', diagnostic: { code: 'PROJECTION_FAILED' }, records: [] };

  const records = [...baseRecords, ...overlay.records.map(overlayToNeutral)]
    .filter(record => requestedViews.includes(recordView(record)))
    .sort((left, right) => left.record_id.localeCompare(right.record_id));
  const leakageReport = records.flatMap(record => safeRecord(record, allowlist).map(finding => ({ record_id: record.record_id, ...finding })));
  if (leakageReport.length) return { status: 'rejected', leakage_report: leakageReport, records: [] };
  const allowlistDigest = sha256(allowlist);
  const episodeOverlayDigest = overlay.records.length ? sha256(overlay.records) : null;
  const projectionDigest = sha256({ records, views: [...requestedViews].sort(), source_graph_digest: overlay.canonical_graph_digest, episode_overlay_digest: episodeOverlayDigest, compiler_version: compilerVersion, allowlist_digest: allowlistDigest });
  return {
    status: overlay.status === 'quarantined' ? 'quarantined' : 'current',
    manifest: {
      contract: 'animejs-neutral-projection-manifest/0.1.0',
      source_graph_digest: overlay.canonical_graph_digest,
      episode_overlay_digest: episodeOverlayDigest,
      compiler_version: compilerVersion,
      allowlist_digest: allowlistDigest,
      projection_digest: projectionDigest,
      owner_review_ref: ownerReviewRef,
      views: [...requestedViews].sort(),
    },
    records,
    projection_bytes: canonicalBytes(records),
    projection_digest: projectionDigest,
    leakage_report: [],
    quarantined: overlay.quarantined,
    semantic_effect: 'none',
  };
}
