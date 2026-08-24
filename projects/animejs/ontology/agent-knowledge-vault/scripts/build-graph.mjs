#!/usr/bin/env node

import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SOURCE_ROOT = process.env.AKV_SOURCE_ROOT ? resolve(process.env.AKV_SOURCE_ROOT) : ROOT;
const ORIGIN = 'https://animejs.com';
const VERSION_ID = 'version:animejs:4.5.0:2c9cf8ea00329f6768c7d7902252ed977d75ce42';
const TRANSFORM = 'animejs-akv-graph/2.0.0';

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
  return JSON.stringify(value);
}

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function loadJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function loadJsonl(path) {
  return readFileSync(path, 'utf8').trimEnd().split('\n').map(line => JSON.parse(line));
}

function docEvidenceId(row) {
  return `evidence:documentation:${sha256(row.canonical_path).slice(0, 24)}`;
}

function docTopicId(row) {
  return `topic:documentation:${row.canonical_path.replace(/^\/documentation\//, '').replace(/\/$/, '')}`;
}

function docFamily(row) {
  return row.canonical_path.replace(/^\/documentation\//, '').split('/')[0];
}

function repoEvidenceId(row) {
  return `evidence:repository:${row.blob_sha1}:${sha256(row.path).slice(0, 12)}`;
}

function buildGraph() {
  const docsPath = resolve(SOURCE_ROOT, 'sources/documentation.jsonl');
  const repoPath = resolve(SOURCE_ROOT, 'sources/repository.jsonl');
  assert.ok(existsSync(docsPath), `documentation source missing: ${docsPath}`);
  assert.ok(existsSync(repoPath), `repository source missing: ${repoPath}`);
  const docs = loadJsonl(docsPath);
  const repo = loadJsonl(repoPath);
  const docsManifest = loadJson(resolve(SOURCE_ROOT, 'sources/documentation-manifest.json'));
  const repoManifest = loadJson(resolve(SOURCE_ROOT, 'sources/repository-manifest.json'));
  const nodes = [];
  const relations = [];

  nodes.push({
    id: VERSION_ID,
    kind: 'VersionContext',
    record_state: 'validated',
    assertion_scope: 'animejs:version:4.5.0',
    version_context_id: VERSION_ID,
    evidence_record_ids: [],
    payload: {
      package_version: '4.5.0',
      commit_sha: repoManifest.commit_sha,
      commit_tree_sha1: repoManifest.commit_tree_sha1,
      documentation_context: 'live-mutable-not-release-locked',
      documentation_manifest_sha256: docsManifest.semantic_jsonl_sha256,
      repository_manifest_sha256: repoManifest.manifest_jsonl_sha256,
    },
  });

  for (const row of docs) {
    const evidenceId = docEvidenceId(row);
    const topicId = docTopicId(row);
    const canonicalUrl = `${ORIGIN}${row.canonical_path}`;
    nodes.push({
      id: topicId,
      kind: 'DocumentationTopic',
      record_state: 'validated',
      assertion_scope: `documentation:${row.canonical_path}`,
      version_context_id: null,
      evidence_record_ids: [evidenceId],
      payload: {
        canonical_path: row.canonical_path,
        canonical_url: canonicalUrl,
        family: docFamily(row),
        topic_kind: row.topic_kind,
        title: row.title,
        h1: row.h1,
        heading_selectors: row.heading_selectors,
        headings: row.headings,
        parameters: row.parameters,
        returns: row.returns,
        related_topics: row.related_topics,
        examples: row.examples,
        version_notes: row.version_notes,
        badges: row.badges,
        raw_sha256: row.raw_sha256,
      },
    });
    nodes.push({
      id: evidenceId,
      kind: 'EvidenceRecord',
      record_state: 'validated',
      assertion_scope: `documentation:${row.canonical_path}`,
      version_context_id: null,
      evidence_record_ids: [],
      payload: {
        evidence_class: 'DocumentationObservation',
        source_kind: 'official-documentation',
        source_url: canonicalUrl,
        mutable: true,
        selector_or_structured_pointer: 'article#docs-info',
        content_sha256: row.raw_sha256,
        proof_status: 'documented',
        materialization_status: 'reproduced-and-validated-candidate-local',
        runtime_observed: false,
      },
    });
    relations.push({
      id: `edge:documents:${sha256(row.canonical_path).slice(0, 24)}`,
      type: 'documents',
      source_id: evidenceId,
      source_kind: 'EvidenceRecord',
      target_id: topicId,
      target_kind: 'DocumentationTopic',
      version_context_id: null,
      assertion_scope: `documentation:${row.canonical_path}`,
      evidence_record_ids: [evidenceId],
      record_state: 'validated',
    });
  }

  for (const row of repo) {
    nodes.push({
      id: repoEvidenceId(row),
      kind: 'EvidenceRecord',
      record_state: 'validated',
      assertion_scope: `repository:${row.path}`,
      version_context_id: VERSION_ID,
      evidence_record_ids: [],
      payload: {
        evidence_class: row.evidence_status,
        source_kind: `official-${row.kind.replace('_', '-')}`,
        structured_pointer: row.structured_pointer,
        path: row.path,
        blob_sha1: row.blob_sha1,
        size: row.size,
        commit_sha: repoManifest.commit_sha,
        immutable: true,
        runtime_observed: false,
      },
    });
  }

  nodes.sort((left, right) => left.id.localeCompare(right.id));
  relations.sort((left, right) => left.id.localeCompare(right.id));
  const graphDigest = sha256(canonical({
    nodes,
    relations,
    documentation_manifest_sha256: docsManifest.semantic_jsonl_sha256,
    repository_manifest_sha256: repoManifest.manifest_jsonl_sha256,
    transform_version: TRANSFORM,
  }));
  const common = {
    graph_digest: graphDigest,
    transform_version: TRANSFORM,
    source_manifests: {
      documentation: docsManifest.semantic_jsonl_sha256,
      repository: repoManifest.manifest_jsonl_sha256,
    },
    authority_effect: 'none',
    release_admission: 'not-granted',
  };
  return {
    nodesDocument: {
      schema_version: 'animejs.agent-knowledge-vault.nodes.v1',
      ...common,
      counts: {
        total: nodes.length,
        DocumentationTopic: nodes.filter(node => node.kind === 'DocumentationTopic').length,
        EvidenceRecord: nodes.filter(node => node.kind === 'EvidenceRecord').length,
        VersionContext: nodes.filter(node => node.kind === 'VersionContext').length,
        Lesson: nodes.filter(node => node.kind === 'Lesson').length,
      },
      nodes,
    },
    relationsDocument: {
      schema_version: 'animejs.agent-knowledge-vault.relations.v1',
      ...common,
      relation_count: relations.length,
      relations,
    },
  };
}

function validateGraph(nodesDocument, relationsDocument) {
  assert.equal(nodesDocument.graph_digest, relationsDocument.graph_digest);
  assert.equal(nodesDocument.counts.DocumentationTopic, 418);
  assert.equal(nodesDocument.counts.EvidenceRecord, 766);
  assert.equal(nodesDocument.counts.VersionContext, 1);
  assert.equal(nodesDocument.counts.Lesson, 0);
  assert.equal(nodesDocument.counts.total, 1185);
  assert.equal(relationsDocument.relation_count, 418);
  const nodes = new Map(nodesDocument.nodes.map(node => [node.id, node]));
  assert.equal(nodes.size, nodesDocument.nodes.length);
  assert.equal(new Set(relationsDocument.relations.map(edge => edge.id)).size, relationsDocument.relations.length);
  for (const edge of relationsDocument.relations) {
    assert.equal(edge.type, 'documents');
    assert.equal(nodes.get(edge.source_id)?.kind, edge.source_kind);
    assert.equal(nodes.get(edge.target_id)?.kind, edge.target_kind);
    assert.ok(edge.evidence_record_ids.includes(edge.source_id));
  }
  for (const node of nodesDocument.nodes.filter(node => node.kind === 'EvidenceRecord')) {
    assert.equal(node.payload.runtime_observed, false);
  }
  assert.equal(nodesDocument.authority_effect, 'none');
  assert.equal(nodesDocument.release_admission, 'not-granted');
}

function build() {
  const { nodesDocument, relationsDocument } = buildGraph();
  validateGraph(nodesDocument, relationsDocument);
  mkdirSync(resolve(ROOT, 'nodes'), { recursive: true });
  mkdirSync(resolve(ROOT, 'relations'), { recursive: true });
  writeFileSync(resolve(ROOT, 'nodes/nodes.json'), `${JSON.stringify(nodesDocument, null, 2)}\n`);
  writeFileSync(resolve(ROOT, 'relations/relations.json'), `${JSON.stringify(relationsDocument, null, 2)}\n`);
  console.log(`BUILT graph: ${nodesDocument.counts.total} nodes, ${relationsDocument.relation_count} relations, digest ${nodesDocument.graph_digest}`);
}

function check() {
  const expected = buildGraph();
  const actualNodes = loadJson(resolve(ROOT, 'nodes/nodes.json'));
  const actualRelations = loadJson(resolve(ROOT, 'relations/relations.json'));
  validateGraph(actualNodes, actualRelations);
  assert.equal(canonical(actualNodes), canonical(expected.nodesDocument), 'nodes are stale or nondeterministic');
  assert.equal(canonical(actualRelations), canonical(expected.relationsDocument), 'relations are stale or nondeterministic');
  console.log(`PASS graph build: 1185 nodes, 418 relations, digest ${actualNodes.graph_digest}`);
}

try {
  if (process.argv.includes('--build')) build();
  else if (process.argv.includes('--check')) check();
  else throw new Error('usage: build-graph.mjs --build | --check');
} catch (error) {
  console.error(error.stack ?? error.message);
  process.exitCode = 2;
}
