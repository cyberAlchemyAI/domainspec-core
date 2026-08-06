const overlayKinds = new Set(['episode', 'attempt', 'outcome', 'evidence_binding', 'supersession_reference']);

function episodeRecords(snapshot, evidenceEligibility) {
  const { state } = snapshot;
  const evidence = state.attempts.flatMap(attempt => attempt.evidence.map(item => ({ ...item, attempt_ordinal: attempt.ordinal })));
  const revoked = evidence.some(item => (evidenceEligibility[item.handle] ?? item.state) === 'revoked');
  const records = [{
    kind: 'episode', record_id: `episode:${state.episode_id}`, label: state.goal,
    summary: `Work episode ${state.lifecycle_state} at revision ${state.revision}.`,
    episode_lifecycle_state: state.lifecycle_state,
    evidence_state: revoked ? 'unconfirmed' : (evidence.length ? 'admissible' : 'not_applicable'),
    truth_status: 'not_assessed', clearing_criteria: revoked ? ['attach current admissible evidence in a superseding episode'] : [],
  }];
  for (const attempt of state.attempts) {
    records.push({
      kind: 'attempt', record_id: `episode:${state.episode_id}:attempt:${attempt.ordinal}`,
      label: `Attempt ${attempt.ordinal}`, summary: attempt.action_summary,
      evidence_state: attempt.evidence.length ? (attempt.evidence.some(item => (evidenceEligibility[item.handle] ?? item.state) === 'revoked') ? 'unconfirmed' : 'admissible') : 'not_applicable',
      truth_status: 'episode_local_observation', clearing_criteria: [],
    });
    if (attempt.outcome) records.push({
      kind: 'outcome', record_id: `episode:${state.episode_id}:outcome:${attempt.ordinal}`,
      label: `${attempt.outcome.classification} outcome`, summary: attempt.outcome.observations.join(' ') || 'No observations recorded.',
      evidence_state: attempt.evidence.some(item => (evidenceEligibility[item.handle] ?? item.state) === 'revoked') ? 'unconfirmed' : (attempt.evidence.length ? 'admissible' : 'not_applicable'),
      truth_status: 'episode_local_observation', clearing_criteria: [],
    });
    for (const item of attempt.evidence) records.push({
      kind: 'evidence_binding', record_id: `episode:${state.episode_id}:evidence:${item.handle}`,
      label: `Evidence for attempt ${attempt.ordinal}`, summary: `${item.evidence_class} evidence binding`,
      evidence_state: evidenceEligibility[item.handle] ?? item.state,
      truth_status: 'not_assessed', clearing_criteria: (evidenceEligibility[item.handle] ?? item.state) === 'revoked' ? ['replace with a current host-resolved evidence handle'] : [],
    });
  }
  if (state.supersedes_episode_id) records.push({
    kind: 'supersession_reference', record_id: `episode:${state.episode_id}:supersedes`,
    label: 'Supersedes prior episode', summary: `Overlay-only reference to ${state.supersedes_episode_id}.`,
    relation_name: 'supersedes_episode', evidence_state: 'not_applicable', truth_status: 'not_assessed', clearing_criteria: [],
  });
  return records;
}

export function compileEpisodeOverlay({ reductionResults, evidenceEligibility = {}, canonicalGraphDigest, canonicalGraphDigestAfter = canonicalGraphDigest }) {
  if (canonicalGraphDigest !== canonicalGraphDigestAfter) throw new Error('CANONICAL_GRAPH_DELTA');
  const records = [];
  const quarantined = [];
  let pending = false;
  let failed = false;
  for (const result of reductionResults) {
    if (result.status === 'pending') { pending = true; continue; }
    if (result.status === 'failed') { failed = true; continue; }
    if (result.status === 'quarantined' || result.status === 'corrupt') {
      quarantined.push({ episode_id: result.episode_id ?? null, code: result.diagnostic?.code ?? 'EPISODE_QUARANTINED' });
      continue;
    }
    if (result.status === 'current') records.push(...episodeRecords(result.snapshot, evidenceEligibility));
  }
  if (records.some(record => !overlayKinds.has(record.kind))) throw new Error('FORBIDDEN_OVERLAY_KIND');
  return {
    contract: 'animejs-work-episode-overlay/0.1.0',
    status: failed ? 'failed' : pending ? 'pending' : quarantined.length ? 'quarantined' : 'current',
    canonical_graph_digest: canonicalGraphDigest,
    records: records.sort((left, right) => left.record_id.localeCompare(right.record_id)),
    quarantined,
    canonical_graph_delta: 0,
    verified_lessons_created: 0,
    authority_effect: 'none',
  };
}
