import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { canonicalize, digestCanonical } from './canonical-json.mjs';

const toolDir = dirname(fileURLToPath(import.meta.url));
export const packageRoot = resolve(toolDir, '..');
export const PACKAGE_FILES = [
  'README.md', 'TOWER.md', 'PACKAGE-SNAPSHOT.json',
  'schemas/canonical-json-profile.json', 'schemas/lab-records.schema.json', 'schemas/projection.schema.json',
  'ontology/relation-registry.json', 'ontology/candidates.json', 'ontology/relations.json',
  'privacy/privacy-policy.json', 'projection/projection-contract.json',
  'levels/L0-corpus.md', 'levels/L1-residue-map.md', 'levels/L2-closure-plan.md', 'gates/closure-gates.md', 'residue/open-residue.md',
  'residue/residue-items.json', 'decisions/representative-tower.md', 'definitions/definition-bindings.json', 'promotions/blocked-promotion.json', 'validation/expected-validation-records.json',
  'fixtures/source/toy-tower/README.md', 'fixtures/source/toy-tower/TOWER.md', 'fixtures/source/toy-tower/levels/L0-corpus.md', 'fixtures/source/toy-tower/levels/L1-residue-map.md', 'fixtures/source/toy-tower/levels/L2-closure-plan.md', 'fixtures/source/toy-tower/gates/closure-gates.md', 'fixtures/source/toy-tower/residue/open-residue.md',
  'fixtures/valid/synthetic-one-tower.json', 'fixtures/invalid/mutant-matrix.json', 'sources/source-snapshots.json', 'claims/claims.json', 'anchors/evidence-anchors.json',
  'tools/canonical-json.mjs', 'tools/compile-projection.mjs', 'tools/build-package-snapshot.mjs',
  'tests/canonical-json.test.mjs', 'tests/record-contract.test.mjs', 'tests/projection-contract.test.mjs', 'tests/package-structure.test.mjs', 'tests/fixture-contract.test.mjs', 'tests/compile-projection.test.mjs', 'tests/negative-mutants.test.mjs', 'tests/package-snapshot.test.mjs'
];

export class PackageSnapshotError extends Error {
  constructor(code, message) {
    super(`${code}: ${message}`);
    this.code = code;
  }
}

const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const zeroDigest = '0'.repeat(64);

function normalized(document) {
  const copy = structuredClone(document);
  copy.manifest_self_digest = zeroDigest;
  copy.tower_snapshot_id = zeroDigest;
  const self = copy.artifacts.find((artifact) => artifact.path === 'PACKAGE-SNAPSHOT.json');
  if (self) {
    self.content_digest = zeroDigest;
    self.byte_size = 0;
  }
  return copy;
}

export function validateSnapshot(document) {
  const manifest = sha256(canonicalize(normalized(document)));
  if (document.manifest_self_digest !== manifest) {
    throw new PackageSnapshotError('CAL_PACKAGE_MANIFEST_STALE', 'manifest self digest does not match normalized package bytes');
  }
  const tower = digestCanonical({ manifest_self_digest: manifest, artifact_paths: document.artifacts.map((artifact) => artifact.path), source_bindings_digest: document.source_bindings_digest }, document.schema_version).sha256;
  if (document.tower_snapshot_id !== tower) {
    throw new PackageSnapshotError('CAL_TOWER_SNAPSHOT_STALE', 'tower snapshot id does not match package manifest');
  }
}

export async function buildSnapshot({ root = packageRoot, check = false } = {}) {
  const artifacts = [];
  for (const path of PACKAGE_FILES) {
    if (path === 'PACKAGE-SNAPSHOT.json') {
      artifacts.push({ path, content_digest: zeroDigest, byte_size: 0 });
      continue;
    }
    const bytes = await readFile(resolve(root, path));
    artifacts.push({ path, content_digest: sha256(bytes), byte_size: bytes.length });
  }
  const sourceBindings = await readFile(resolve(root, 'sources/source-snapshots.json'));
  const base = {
    schema_version: '1.0.0',
    package_snapshot_id: 'package-snapshot:cyberalchemy-l0',
    tower_logical_id: 'tower:toy',
    authority_effect: 'none',
    normalization: 'normalized-self-v1',
    artifacts,
    source_bindings_digest: sha256(sourceBindings),
    manifest_self_digest: zeroDigest,
    tower_snapshot_id: zeroDigest
  };
  base.manifest_self_digest = sha256(canonicalize(normalized(base)));
  base.tower_snapshot_id = digestCanonical({ manifest_self_digest: base.manifest_self_digest, artifact_paths: artifacts.map((artifact) => artifact.path), source_bindings_digest: base.source_bindings_digest }, base.schema_version).sha256;
  validateSnapshot(base);
  const rendered = `${JSON.stringify(base, null, 2)}\n`;
  const target = resolve(root, 'PACKAGE-SNAPSHOT.json');
  if (check) {
    const current = await readFile(target, 'utf8');
    if (current !== rendered) throw new PackageSnapshotError('CAL_PACKAGE_MANIFEST_STALE', 'PACKAGE-SNAPSHOT.json does not match live package bytes');
  } else {
    await writeFile(target, rendered);
  }
  return base;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  buildSnapshot({ check: process.argv.includes('--check') }).catch((error) => {
    console.error(error.stack ?? String(error));
    process.exitCode = 1;
  });
}
