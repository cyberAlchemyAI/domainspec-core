#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const ALGORITHM_VERSION = 'animejs-akv-query/1.0.0';
export const ABSTENTION_PRECEDENCE = Object.freeze([
  'ABSTAIN_UNKNOWN_VERSION',
  'ABSTAIN_RUNTIME_CONTEXT',
  'ABSTAIN_CONFLICT',
  'ABSTAIN_PERFORMANCE_EVIDENCE',
  'ABSTAIN_MISSING_SOURCE',
  'ABSTAIN_AMBIGUOUS_INTENT',
]);

const QUESTION_CONTRACT = Object.freeze({
  ABSTAIN_UNKNOWN_VERSION: ['Which exact Anime.js version and lock digest should this answer target?', 'Supply a validated exact VersionContext and, for project claims, its lock digest.'],
  ABSTAIN_RUNTIME_CONTEXT: ['Which runtime, browser, and framework context should this answer target?', 'Supply the installed version, runtime/browser, and relevant framework environment.'],
  ABSTAIN_CONFLICT: ['Which scope or admissible witness resolves the conflicting propositions?', 'Partition the assertions into non-overlapping scopes or provide a question-specific witness.'],
  ABSTAIN_PERFORMANCE_EVIDENCE: ['What measured workload and threshold should decide this performance choice?', 'Supply a controlled matching ExecutedWitness with environment, metric, baseline, repetitions, and threshold.'],
  ABSTAIN_MISSING_SOURCE: ['Which official source binding establishes the required feature?', 'Supply validated exact-scope official documentation or pinned source evidence.'],
  ABSTAIN_AMBIGUOUS_INTENT: ['Which discriminating constraint should choose between the tied surfaces?', 'Supply a constraint that leaves exactly one top-ranked compatible candidate.'],
});

function stableUnique(values) {
  return [...new Set(values.filter(Boolean).map(String))].sort((a, b) => a.localeCompare(b));
}

function stableObjects(values) {
  return [...values].sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b)));
}

function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function digest(value) {
  return createHash('sha256').update(canonicalJson(value)).digest('hex');
}

function questionFor(code) {
  const [prompt, clearingCriterion] = QUESTION_CONTRACT[code];
  return {
    id: `next:${code.toLowerCase()}`,
    gap_code: code,
    prompt,
    clearing_criterion: clearingCriterion,
  };
}

export function evaluateDecision(input) {
  const candidates = (input.candidates ?? [])
    .filter(candidate => candidate.compatible === true)
    .map(candidate => ({
      ...candidate,
      id: String(candidate.id),
      score: Number(candidate.score ?? 0),
      evidence_record_ids: stableUnique(candidate.evidence_record_ids ?? []),
    }))
    .sort((left, right) => right.score - left.score || left.id.localeCompare(right.id));

  const detected = [];
  if (!input.version_context?.exact_version || !input.version_context?.lock_digest) detected.push('ABSTAIN_UNKNOWN_VERSION');
  if (input.requires_runtime_context && !input.runtime_context?.complete) detected.push('ABSTAIN_RUNTIME_CONTEXT');
  if ((input.conflicts ?? []).length > 0) detected.push('ABSTAIN_CONFLICT');
  if (input.performance_intent && !input.executed_performance_witness) detected.push('ABSTAIN_PERFORMANCE_EVIDENCE');
  if ((input.missing_sources ?? []).length > 0 || (input.intent_recognized !== false && candidates.length === 0)) detected.push('ABSTAIN_MISSING_SOURCE');
  if (input.intent_recognized === false) detected.push('ABSTAIN_AMBIGUOUS_INTENT');

  const topScore = candidates[0]?.score;
  const topCandidates = candidates.filter(candidate => candidate.score === topScore);
  if (topCandidates.length > 1) detected.push('ABSTAIN_AMBIGUOUS_INTENT');

  const orderedCodes = ABSTENTION_PRECEDENCE.filter(code => detected.includes(code));
  const primary = orderedCodes[0] ?? null;
  const tieOnly = primary === 'ABSTAIN_AMBIGUOUS_INTENT' && topCandidates.length > 1;
  const selectedIds = primary === null || tieOnly ? stableUnique(topCandidates.map(candidate => candidate.id)) : [];
  const evidenceIds = stableUnique(topCandidates.flatMap(candidate => candidate.evidence_record_ids));
  const receiptBasis = {
    query_id: 'QRY-003',
    input_id: input.id,
    algorithm_version: ALGORITHM_VERSION,
    graph_digest: input.graph_digest,
    selected_ids: selectedIds,
    abstention_code: primary,
  };

  return {
    schema_version: 'animejs.agent-knowledge-vault.query-receipt.v1',
    receipt_id: `qry:${digest(receiptBasis).slice(0, 24)}`,
    query_id: 'QRY-003',
    algorithm_version: ALGORITHM_VERSION,
    graph_digest: input.graph_digest,
    selected_ids: selectedIds,
    evidence_record_ids: evidenceIds,
    conflicts: stableObjects(input.conflicts ?? []),
    absences: stableObjects(input.missing_sources ?? []),
    abstention_code: primary,
    subordinate_gaps: stableUnique([
      ...orderedCodes.slice(1),
      ...(input.subordinate_gaps ?? []),
    ]),
    next_questions: primary === null ? [] : [questionFor(primary)],
    generated_at: input.generated_at,
  };
}

export function queryCoverage(canonicalPath, coverageDocument) {
  const normalized = `/${String(canonicalPath).split('?')[0].split('#')[0].split('/').filter(Boolean).join('/')}/`;
  const row = (coverageDocument.routes ?? coverageDocument.rows ?? []).find(candidate => candidate.canonical_path === normalized);
  if (!row) throw new Error(`coverage route not found: ${normalized}`);
  return {
    schema_version: 'animejs.agent-knowledge-vault.coverage-query.v1',
    query_id: 'QRY-006',
    algorithm_version: ALGORITHM_VERSION,
    canonical_path: normalized,
    navigation_status: row.navigation_status,
    semantic_status: row.semantic_status,
    materialization_status: row.materialization_status,
    validation_status: row.validation_status,
    evidence_record_ids: stableUnique(row.evidence_record_ids ?? []),
  };
}

function main(argv) {
  if (argv[0] === 'coverage') {
    const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
    const document = JSON.parse(readFileSync(resolve(root, 'views/documentation-coverage.json'), 'utf8'));
    process.stdout.write(`${JSON.stringify(queryCoverage(argv[1], document), null, 2)}\n`);
    return;
  }
  if (argv[0] === 'decision') {
    const input = JSON.parse(readFileSync(resolve(argv[1]), 'utf8'));
    process.stdout.write(`${JSON.stringify(evaluateDecision(input), null, 2)}\n`);
    return;
  }
  throw new Error('usage: query.mjs decision <input.json> | coverage <canonical-path>');
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 2;
  }
}
