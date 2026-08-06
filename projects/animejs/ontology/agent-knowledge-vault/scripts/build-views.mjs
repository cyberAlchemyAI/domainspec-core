#!/usr/bin/env node

import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SOURCE_ROOT = process.env.AKV_SOURCE_ROOT ? resolve(process.env.AKV_SOURCE_ROOT) : ROOT;
const ORIGIN = 'https://animejs.com';
const TRANSFORM = 'animejs-akv-views/2.0.0';

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
  return JSON.stringify(value);
}

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function topicId(row) {
  return `topic:documentation:${row.canonical_path.replace(/^\/documentation\//, '').replace(/\/$/, '')}`;
}

function family(row) {
  return row.canonical_path.replace(/^\/documentation\//, '').split('/')[0];
}

function repositoryEvidenceId(row) {
  return `evidence:repository:${row.blob_sha1}:${sha256(row.path).slice(0, 12)}`;
}

function loadJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function loadJsonl(path) {
  return readFileSync(path, 'utf8').trimEnd().split('\n').map(line => JSON.parse(line));
}

function tokens(...values) {
  return [...new Set(values.join(' ').normalize('NFKC').toLowerCase().replace(/[^a-z0-9._/-]+/g, ' ').split(/\s+/).filter(Boolean))].sort();
}

function common(graphDigest) {
  return {
    graph_digest: graphDigest,
    transform_version: TRANSFORM,
    authority_effect: 'none',
    release_admission: 'not-granted',
  };
}

function buildViews() {
  const nodesDocument = loadJson(resolve(SOURCE_ROOT, 'nodes/nodes.json'));
  const relationsDocument = loadJson(resolve(SOURCE_ROOT, 'relations/relations.json'));
  const docs = loadJsonl(resolve(SOURCE_ROOT, 'sources/documentation.jsonl'));
  const repo = loadJsonl(resolve(SOURCE_ROOT, 'sources/repository.jsonl'));
  assert.equal(nodesDocument.graph_digest, relationsDocument.graph_digest);
  const graphDigest = nodesDocument.graph_digest;
  const evidenceByTopic = new Map(relationsDocument.relations.filter(edge => edge.type === 'documents').map(edge => [edge.target_id, edge.source_id]));

  const coverage = {
    schema_version: 'animejs.agent-knowledge-vault.documentation-coverage-view.v1',
    ...common(graphDigest),
    route_count: docs.length,
    family_count: new Set(docs.map(family)).size,
    routes: docs.map(row => ({
      id: topicId(row),
      canonical_path: row.canonical_path,
      family: family(row),
      topic_kind: row.topic_kind,
      title: row.title,
      navigation_status: 'observed',
      semantic_status: row.status,
      materialization_status: 'reproduced',
      validation_status: 'validated',
      evidence_record_ids: [evidenceByTopic.get(topicId(row))],
      raw_sha256: row.raw_sha256,
    })),
  };

  const sourceRows = repo.filter(row => ['source', 'type', 'package-documentation'].includes(row.kind));
  const api = {
    schema_version: 'animejs.agent-knowledge-vault.api-view.v1',
    ...common(graphDigest),
    symbol_semantics_status: 'not-extracted',
    abstention_code: 'ABSTAIN_MISSING_SOURCE',
    clearing_criterion: 'Extract exact exports and declarations into APISymbol and SourceFact nodes with intersecting pinned evidence.',
    documentation_topics: docs.map(row => ({
      id: topicId(row),
      canonical_path: row.canonical_path,
      family: family(row),
      title: row.title,
      h1: row.h1,
      evidence_record_ids: [evidenceByTopic.get(topicId(row))],
    })),
    pinned_source_artifacts: sourceRows.map(row => ({
      id: repositoryEvidenceId(row),
      path: row.path,
      kind: row.kind,
      structured_pointer: row.structured_pointer,
      evidence_status: row.evidence_status,
    })),
  };

  const familyRows = docs.filter(row => row.topic_kind === 'family').sort((a, b) => a.canonical_path.localeCompare(b.canonical_path));
  const recipes = {
    schema_version: 'animejs.agent-knowledge-vault.task-recipes-view.v1',
    ...common(graphDigest),
    recipe_count: familyRows.length,
    execution_status: 'guidance-not-executed',
    recipes: familyRows.map(row => ({
      id: `recipe:consult:${family(row)}`,
      intent_tokens: tokens(family(row), row.title, row.h1),
      target_kind: 'DocumentationTopic',
      ordered_steps: [
        `Consult ${row.canonical_path}`,
        'Follow related official topic links matching the exact task constraint.',
        'Bind any project claim to an exact VersionContext and execute the declared local acceptance check.',
      ],
      documentation_topic_ids: [topicId(row)],
      evidence_record_ids: [evidenceByTopic.get(topicId(row))],
      validation_requirement: 'Project-specific execution evidence is required before claiming success.',
      verified_operational_lesson: false,
    })),
  };

  const workLessons = {
    schema_version: 'animejs.agent-knowledge-vault.work-lessons-view.v1',
    ...common(graphDigest),
    verified_lesson_count: 0,
    candidate_lesson_count: 0,
    lessons: [],
    abstention_code: 'ABSTAIN_NO_VERIFIED_LESSON',
    clearing_criterion: 'Close a compatible WorkEpisode with a succeeded Outcome and linked TestObserved or ExecutedWitness, then admit the generalized Lesson through review.',
  };

  const gaps = {
    schema_version: 'animejs.agent-knowledge-vault.unresolved-gaps-view.v1',
    ...common(graphDigest),
    gap_count: 6,
    gaps: [
      ['gap:api-symbol-extraction', 'APISymbol and SourceFact extraction from the pinned source/type rows is not yet materialized.', 'ABSTAIN_MISSING_SOURCE'],
      ['gap:executed-behavior', 'No Anime.js runtime behavior was executed by this ontology build.', 'ABSTAIN_NO_EXECUTED_WITNESS'],
      ['gap:verified-lessons', 'No closed work episode currently supports a verified operational lesson.', 'ABSTAIN_NO_VERIFIED_LESSON'],
      ['gap:performance', 'No controlled performance witness exists for JS versus WAAPI choices.', 'ABSTAIN_PERFORMANCE_EVIDENCE'],
      ['gap:accessibility', 'No named accessibility criterion has a matching executed witness.', 'ABSTAIN_ACCESSIBILITY_EVIDENCE'],
      ['gap:copyright-threshold', 'No reviewed numeric similarity threshold is selected; only metadata and original concise paraphrases are admitted.', 'ABSTAIN_COPYRIGHT_REJECTED'],
    ].map(([id, summary, abstention_code]) => ({ id, summary, abstention_code, state: 'open' })),
  };

  const searchEntries = [
    ...docs.map(row => ({
      id: topicId(row),
      kind: 'DocumentationTopic',
      label: row.title || row.h1 || row.canonical_path,
      tokens: tokens(row.canonical_path, family(row), row.title, row.h1, ...row.headings),
      source_ref: `${ORIGIN}${row.canonical_path}`,
      evidence_status: 'semantic-observed',
    })),
    ...repo.map(row => ({
      id: repositoryEvidenceId(row),
      kind: 'RepositoryArtifact',
      label: row.path,
      tokens: tokens(row.path, row.kind),
      source_ref: row.structured_pointer,
      evidence_status: row.evidence_status,
    })),
  ].sort((left, right) => left.id.localeCompare(right.id));
  const search = {
    schema_version: 'animejs.agent-knowledge-vault.search-index.v1',
    ...common(graphDigest),
    entry_count: searchEntries.length,
    entries: searchEntries,
  };

  return { coverage, api, recipes, workLessons, gaps, search };
}

const OUTPUTS = Object.freeze({
  coverage: 'views/documentation-coverage.json',
  api: 'views/api.json',
  recipes: 'views/task-recipes.json',
  workLessons: 'views/work-lessons.json',
  gaps: 'views/unresolved-gaps.json',
  search: 'indexes/search.json',
});

function validate(views) {
  const graphDigests = new Set(Object.values(views).map(view => view.graph_digest));
  assert.equal(graphDigests.size, 1);
  assert.equal(views.coverage.route_count, 418);
  assert.equal(views.coverage.family_count, 16);
  assert.equal(views.api.documentation_topics.length, 418);
  assert.equal(views.api.pinned_source_artifacts.length, 142);
  assert.equal(views.recipes.recipe_count, 16);
  assert.equal(views.workLessons.verified_lesson_count, 0);
  assert.equal(views.workLessons.abstention_code, 'ABSTAIN_NO_VERIFIED_LESSON');
  assert.equal(views.gaps.gap_count, 6);
  assert.equal(views.search.entry_count, 766);
  assert.equal(new Set(views.search.entries.map(entry => entry.id)).size, 766);
}

function build() {
  const views = buildViews();
  validate(views);
  for (const [key, relative] of Object.entries(OUTPUTS)) {
    const target = resolve(ROOT, relative);
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, `${JSON.stringify(views[key], null, 2)}\n`);
  }
  console.log(`BUILT consultation views: 418 routes, 16 recipes, 766 search entries, digest ${views.coverage.graph_digest}`);
}

function check() {
  const expected = buildViews();
  const actual = Object.fromEntries(Object.entries(OUTPUTS).map(([key, relative]) => [key, loadJson(resolve(ROOT, relative))]));
  validate(actual);
  for (const key of Object.keys(OUTPUTS)) assert.equal(canonical(actual[key]), canonical(expected[key]), `${key} view is stale`);
  console.log(`PASS consultation views: 6/6 fresh, 766 search entries, digest ${actual.coverage.graph_digest}`);
}

try {
  if (process.argv.includes('--build')) build();
  else if (process.argv.includes('--check')) check();
  else throw new Error('usage: build-views.mjs --build | --check');
} catch (error) {
  console.error(error.stack ?? error.message);
  process.exitCode = 2;
}
