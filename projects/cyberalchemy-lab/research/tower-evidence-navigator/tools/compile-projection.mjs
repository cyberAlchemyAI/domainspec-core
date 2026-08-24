import { createHash } from 'node:crypto';
import { readFile, rename, writeFile } from 'node:fs/promises';
import { dirname, resolve, relative, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { canonicalize, digestCanonical } from './canonical-json.mjs';

const toolDir = dirname(fileURLToPath(import.meta.url));
const packageRoot = resolve(toolDir, '..');
const recordGroups = ['source_snapshots', 'claims', 'definition_references', 'residue_items', 'evidence_anchors', 'ontology_candidates', 'promotion_records'];

export class CompileError extends Error {
  constructor(code, message) {
    super(`${code}: ${message}`);
    this.name = 'CompileError';
    this.code = code;
  }
}

const fail = (code, message) => { throw new CompileError(code, message); };
const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const json = async (path) => JSON.parse(await readFile(path, 'utf8'));
const flatRecords = (fixture) => [fixture.tower_package_snapshot, ...recordGroups.flatMap((group) => fixture[group] ?? [])];
const unique = (values) => new Set(values).size === values.length;

function safeSourcePath(root, locator) {
  if (typeof locator !== 'string' || isAbsolute(locator)) fail('CAL_SOURCE_DIGEST_MISMATCH', 'source locator must be relative');
  const path = resolve(root, locator);
  if (relative(root, path).startsWith('..')) fail('CAL_SOURCE_DIGEST_MISMATCH', `source locator escapes root: ${locator}`);
  return path;
}

function scanPrivacy(value, policy) {
  const deniedKeys = new Set(Object.values(policy.classes).flatMap((entry) => entry.denied_keys));
  const sentinels = policy.denied_value_sentinels;
  const visit = (node, path = '$') => {
    if (Array.isArray(node)) return node.forEach((item, index) => visit(item, `${path}[${index}]`));
    if (node && typeof node === 'object') {
      for (const [key, item] of Object.entries(node)) {
        if (deniedKeys.has(key)) fail('CAL_PRIVACY_EXPOSURE', `${path}.${key} is denied by the L0 privacy policy`);
        visit(item, `${path}.${key}`);
      }
    }
    if (typeof node === 'string' && sentinels.some((sentinel) => node.includes(sentinel))) {
      fail('CAL_PRIVACY_EXPOSURE', `${path} contains a denied sentinel`);
    }
  };
  visit(value);
}

function recordMapFor(fixture) {
  const records = flatRecords(fixture);
  if (!unique(records.map((record) => record?.id))) fail('CAL_IDENTITY_COLLAPSE', 'record ids must be unique');
  const sources = fixture.source_snapshots ?? [];
  if (!unique(sources.map((source) => source.logical_source_id))) fail('CAL_IDENTITY_COLLAPSE', 'logical source identities must remain distinct');
  if (sources.some((source) => Object.hasOwn(source, 'inferred_same_as'))) fail('CAL_IDENTITY_COLLAPSE', 'identity merging is forbidden');
  return new Map(records.map((record) => [record.id, record]));
}

async function verifySourceBindings(fixture, sourceRoot) {
  for (const source of fixture.source_snapshots ?? []) {
    const bytes = await readFile(safeSourcePath(sourceRoot, source.locator));
    if (sha256(bytes) !== source.content_digest || bytes.length !== source.byte_size) {
      fail('CAL_SOURCE_DIGEST_MISMATCH', `source snapshot does not match ${source.id}`);
    }
  }
  const sourceById = new Map((fixture.source_snapshots ?? []).map((source) => [source.id, source]));
  for (const anchor of fixture.evidence_anchors ?? []) {
    const source = sourceById.get(anchor.source_snapshot_id);
    const selector = anchor.selector;
    if (!source || selector?.kind !== 'utf8-byte-range-v1' || !Number.isInteger(selector.start_byte) || !Number.isInteger(selector.end_byte_exclusive) || selector.start_byte < 0 || selector.end_byte_exclusive < selector.start_byte) {
      fail('CAL_SELECTOR_INVALID', `invalid selector for ${anchor.id}`);
    }
    const bytes = await readFile(safeSourcePath(sourceRoot, source.locator));
    if (selector.end_byte_exclusive > bytes.length || sha256(bytes.subarray(selector.start_byte, selector.end_byte_exclusive)) !== anchor.selected_bytes_sha256 || selector.selected_bytes_sha256 !== anchor.selected_bytes_sha256) {
      fail('CAL_SELECTOR_INVALID', `selector binding does not match ${anchor.id}`);
    }
  }
}

function verifyTowerSnapshot(fixture) {
  const snapshot = fixture.tower_package_snapshot;
  const order = fixture.source_snapshots.map((source) => source.locator);
  const sourceIds = fixture.source_snapshots.map((source) => source.id);
  if (!snapshot || JSON.stringify(snapshot.ordered_artifacts) !== JSON.stringify(order) || JSON.stringify(snapshot.source_bindings) !== JSON.stringify(sourceIds)) {
    fail('CAL_TOWER_SNAPSHOT_STALE', 'tower package snapshot is stale relative to its source bindings');
  }
  if (fixture.package_snapshot_check && fixture.package_snapshot_check !== snapshot.manifest_digest) {
    fail('CAL_PACKAGE_MANIFEST_STALE', 'fixture package snapshot check is stale');
  }
  return digestCanonical({ tower_logical_id: snapshot.tower_logical_id, ordered_artifacts: order, source_bindings: sourceIds }, fixture.schema_version).sha256;
}

function verifyRelations(fixture, registry, records) {
  const byKind = new Map(registry.relations.map((entry) => [entry.kind, entry]));
  for (const relation of fixture.relations ?? []) {
    const spec = byKind.get(relation.kind);
    const from = records.get(relation.from_id);
    const to = records.get(relation.to_id);
    if (!from || !to) fail('CAL_RELATION_DANGLING', `relation ${relation.id} has a dangling endpoint`);
    if (!spec || !spec.from.includes(from.kind) || !spec.to.includes(to.kind)) {
      fail('CAL_KIND_UNSUPPORTED', `relation ${relation.id} uses an unsupported kind or endpoint pair`);
    }
  }
}

function verifySemantics(fixture, policy, records) {
  scanPrivacy(fixture, policy);
  if (fixture.tower_logical_id === undefined || !fixture.allowed_tower_logical_ids?.includes(fixture.tower_logical_id)) {
    fail('CAL_TOWER_NOT_ALLOWLISTED', 'fixture tower is not allowlisted');
  }
  for (const record of records.values()) {
    if (record.authority_effect !== 'none') fail('CAL_AUTHORITY_EFFECT_FORBIDDEN', `authority effect is forbidden for ${record.id}`);
  }
  if (fixture.promotion_records.some((record) => record.gate_result !== 'block')) {
    fail('CAL_AUTHORITY_EFFECT_FORBIDDEN', 'synthetic L0 promotion must remain blocked');
  }
  if (fixture.residue_items.some((record) => record.status !== 'open')) {
    fail('CAL_RESIDUE_STATE_MISMATCH', 'synthetic L0 residue must remain open');
  }
  if (fixture.reserved_consumer_contract?.transport && fixture.reserved_consumer_contract.transport !== 'static-direct-get-shape-only') {
    fail('CAL_TRANSPORT_EFFECT_FORBIDDEN', 'only static direct GET-shaped consumption is permitted');
  }
  for (const validation of fixture.validation_records ?? []) {
    if (!validation.exact_inputs || typeof validation.validator_id !== 'string') fail('CAL_VALIDATION_UNBOUND', 'validation record must bind exact inputs and validator identity');
    if (validation.result === 'pass' && validation.validator_id === 'cal-projection-compiler-v1') {
      fail('CAL_VALIDATOR_NOT_INDEPENDENT', 'compiler cannot issue its own passing validation record');
    }
  }
}

function projectRecord(record, privacyDigest) {
  const allowed = ['kind', 'id', 'status', 'privacy_class', 'authority_effect', 'fixture_class', 'proposition', 'scope', 'claim_ceiling', 'review_state', 'gate_result', 'role', 'selector', 'source_snapshot_id', 'source_digest', 'logical_source_id', 'byte_size', 'media_type', 'evidence_ceiling'];
  const projection = Object.fromEntries(allowed.filter((key) => Object.hasOwn(record, key)).map((key) => [key, record[key]]));
  projection.privacy_policy_digest = privacyDigest;
  return projection;
}

export async function compileFixture(fixture, { sourceRoot = packageRoot, registry, policy, contract } = {}) {
  const loadedRegistry = registry ?? await json(resolve(packageRoot, 'ontology/relation-registry.json'));
  const loadedPolicy = policy ?? await json(resolve(packageRoot, 'privacy/privacy-policy.json'));
  const loadedContract = contract ?? await json(resolve(packageRoot, 'projection/projection-contract.json'));
  const records = recordMapFor(fixture);
  await verifySourceBindings(fixture, sourceRoot);
  const towerSnapshotId = verifyTowerSnapshot(fixture);
  verifyRelations(fixture, loadedRegistry, records);
  verifySemantics(fixture, loadedPolicy, records);
  const privacyDigest = sha256(canonicalize(loadedPolicy));
  const relationOrder = new Map(loadedRegistry.output_order.map((kind, index) => [kind, index]));
  const inputRelations = [...fixture.relations].sort((left, right) => relationOrder.get(left.kind) - relationOrder.get(right.kind) || left.from_id.localeCompare(right.from_id) || left.to_id.localeCompare(right.to_id) || left.relation_id.localeCompare(right.relation_id));
  const outputRecords = [...records.values()].map((record) => projectRecord(record, privacyDigest)).sort((left, right) => left.kind.localeCompare(right.kind) || left.id.localeCompare(right.id));
  const derived = outputRecords.map((record) => ({ kind: 'derived_from', relation_id: `derived:${record.id}`, from_id: `projection-record:${record.id}`, to_id: record.id, direction: 'forward' }));
  const base = {
    schema_version: '1.0.0',
    generator_contract_id: loadedContract.generator_contract_id,
    authority_effect: 'none',
    tower_snapshot_id: towerSnapshotId,
    records: outputRecords,
    relations: [...inputRelations.map(({ kind, relation_id, from_id, to_id, direction }) => ({ kind, relation_id, from_id, to_id, direction })), ...derived],
    adjacency: { forward: {}, reverse: {} },
    privacy: { policy_id: loadedPolicy.policy_id, policy_digest: privacyDigest },
    invalid: false,
    stale: false,
    claim_ceiling: loadedContract.claim_ceiling
  };
  for (const relation of base.relations) {
    (base.adjacency.forward[relation.from_id] ??= []).push(relation.to_id);
    (base.adjacency.reverse[relation.to_id] ??= []).push(relation.from_id);
  }
  for (const map of [base.adjacency.forward, base.adjacency.reverse]) {
    for (const values of Object.values(map)) values.sort();
  }
  const revision = digestCanonical({ projection_schema_version: base.schema_version, tower_snapshot_id: base.tower_snapshot_id, input_record_snapshot_ids_sorted: [...records.values()].map((record) => record.record_snapshot_id).sort(), relation_registry_digest: sha256(canonicalize(loadedRegistry)), projection_rules_digest: sha256(canonicalize(loadedContract.projection_rules)), generator_contract_digest: sha256(canonicalize(loadedContract)), privacy_policy_digest: privacyDigest }, base.schema_version).sha256;
  if (fixture.expected_projection_revision && fixture.expected_projection_revision !== revision) {
    fail('CAL_PROJECTION_STALE', 'fixture expected projection revision is stale');
  }
  return { ...base, projection_revision: revision };
}

export async function compileToFile({ input = resolve(packageRoot, 'fixtures/valid/synthetic-one-tower.json'), output, sourceRoot = packageRoot } = {}) {
  if (!output) throw new TypeError('output is required');
  const projection = await compileFixture(await json(input), { sourceRoot });
  const target = resolve(output);
  const temporary = `${target}.tmp`;
  await writeFile(temporary, canonicalize(projection));
  await rename(temporary, target);
  return projection;
}

function readOption(name) {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : undefined;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  compileToFile({ input: readOption('--input') ?? resolve(packageRoot, 'fixtures/valid/synthetic-one-tower.json'), output: readOption('--output') ?? resolve(packageRoot, 'projection/generated-projection.json'), sourceRoot: readOption('--source-root') ?? packageRoot }).catch((error) => {
    console.error(error.stack ?? String(error));
    process.exitCode = 1;
  });
}
