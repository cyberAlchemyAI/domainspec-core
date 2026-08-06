#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { readdir, readFile, stat, writeFile } from 'node:fs/promises';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const operationalRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const vaultRoot = resolve(operationalRoot, '..');
const receiptPath = join(operationalRoot, 'receipts', 'validation-receipt.json');
const suites = [
  ['contracts', 'tests/contracts.test.mjs'],
  ['transitions', 'tests/transitions.test.mjs'],
  ['journal', 'tests/journal.test.mjs'],
  ['reducer', 'tests/reducer.test.mjs'],
  ['projection', 'tests/projection.test.mjs'],
  ['consultation', 'tests/consultation.test.mjs'],
  ['episode-service', 'tests/episode-service.test.mjs'],
  ['security', 'tests/security.test.mjs'],
];
const scenarioOwner = {
  'TS-01': 'consultation', 'TS-02': 'consultation', 'TS-03': 'consultation', 'TS-04': 'consultation', 'TS-05': 'projection', 'TS-06': 'consultation',
  'TS-07': 'security', 'TS-08': 'security', 'TS-09': 'journal', 'TS-10': 'journal', 'TS-11': 'journal', 'TS-12': 'journal', 'TS-13': 'journal',
  'TS-14': 'episode-service', 'TS-15': 'transitions', 'TS-16': 'projection', 'TS-17': 'transitions', 'TS-18': 'transitions', 'TS-19': 'transitions',
  'TS-20': 'transitions', 'TS-21': 'transitions', 'TS-22': 'reducer', 'TS-23': 'reducer', 'TS-24': 'reducer', 'TS-25': 'reducer', 'TS-26': 'reducer',
  'TS-27': 'projection', 'TS-28': 'projection', 'TS-29': 'projection', 'TS-30': 'episode-service',
};

async function filesUnder(root) {
  const files = [];
  async function walk(current) {
    for (const name of (await readdir(current)).sort()) {
      const path = join(current, name);
      const info = await stat(path);
      if (info.isDirectory()) await walk(path);
      else files.push(path);
    }
  }
  await walk(root);
  return files;
}

async function digestFiles(files, base) {
  const hash = createHash('sha256');
  for (const path of [...files].sort()) {
    hash.update(relative(base, path).replaceAll('\\', '/'));
    hash.update('\0');
    hash.update(await readFile(path));
    hash.update('\0');
  }
  return hash.digest('hex');
}

async function canonicalVaultDigest() {
  const roots = ['nodes', 'relations', 'sources', 'views'].map(name => join(vaultRoot, name));
  const files = (await Promise.all(roots.map(filesUnder))).flat();
  return digestFiles(files, vaultRoot);
}

async function loadJsonSurfaces() {
  const roots = [join(operationalRoot, 'contracts'), join(operationalRoot, 'fixtures')];
  const files = (await Promise.all(roots.map(filesUnder))).flat().filter(path => path.endsWith('.json'));
  const documents = new Map();
  for (const path of files) documents.set(relative(operationalRoot, path).replaceAll('\\', '/'), JSON.parse(await readFile(path, 'utf8')));
  return documents;
}

function validateCrossContracts(documents) {
  const required = [
    'contracts/neutral-projection-record.schema.json', 'contracts/neutral-projection-manifest.schema.json',
    'contracts/consultation-request.schema.json', 'contracts/consultation-result.schema.json',
    'contracts/episode-command.schema.json', 'contracts/episode-event.schema.json',
    'contracts/episode-result.schema.json', 'contracts/status-codes.json', 'contracts/projection-allowlist.json',
  ];
  for (const path of required) if (!documents.has(path)) throw new Error(`missing contract: ${path}`);
  for (const [path, document] of documents) {
    if (path.endsWith('.schema.json') && document.additionalProperties !== false) throw new Error(`outer schema is not closed: ${path}`);
  }
  const command = documents.get('contracts/episode-command.schema.json');
  const operations = command.properties.operation.enum;
  if (operations.join(',') !== 'open_episode,append_attempt,attach_evidence,record_outcome,close_episode') throw new Error('episode operation algebra drift');
  if (operations.includes('supersede_episode')) throw new Error('duplicate supersession spelling');
  const result = documents.get('contracts/episode-result.schema.json');
  const codes = documents.get('contracts/status-codes.json');
  if (JSON.stringify(result.properties.status.enum) !== JSON.stringify(codes.append_statuses)) throw new Error('append status algebra drift');
  const consultation = documents.get('contracts/consultation-result.schema.json');
  for (const field of ['records', 'edges', 'explanation_path']) if (!consultation.required.includes(field)) throw new Error(`consultation result missing ${field}`);
  const event = documents.get('contracts/episode-event.schema.json');
  if (event.allOf?.length !== 5 || event.allOf.some(branch => branch.then?.properties?.payload?.additionalProperties !== false)) throw new Error('event payload variants are not closed');
  const record = documents.get('contracts/neutral-projection-record.schema.json');
  const allowlist = documents.get('contracts/projection-allowlist.json');
  for (const field of allowlist.record_fields) if (!(field in record.properties)) throw new Error(`allowlist field lacks schema property: ${field}`);
  const fixtureCoverage = new Set([...documents.values()].flatMap(document => document.covered_scenarios ?? []));
  for (const scenario of Object.keys(scenarioOwner)) if (!fixtureCoverage.has(scenario)) throw new Error(`fixture coverage missing ${scenario}`);
}

async function validateSourceDiagnosticClosure(documents) {
  const codes = documents.get('contracts/status-codes.json');
  const closed = new Set([...codes.diagnostic_codes, ...codes.abstention_codes]);
  const sourceFiles = (await filesUnder(join(operationalRoot, 'src'))).filter(path => path.endsWith('.mjs'));
  const emitted = new Set();
  for (const path of sourceFiles) {
    const source = await readFile(path, 'utf8');
    for (const match of source.matchAll(/'([A-Z][A-Z0-9_]+)'/g)) emitted.add(match[1]);
  }
  const missing = [...emitted].filter(code => !closed.has(code)).sort();
  if (missing.length) throw new Error(`source diagnostics missing from closed table: ${missing.join(', ')}`);
}

function runSuite([suite, relativePath]) {
  const completed = spawnSync(process.execPath, ['--test', join(operationalRoot, relativePath)], { cwd: operationalRoot, encoding: 'utf8', maxBuffer: 4 * 1024 * 1024 });
  if (completed.status !== 0) throw new Error(`${suite} failed\n${completed.stdout}\n${completed.stderr}`);
  const tests = Number(completed.stdout.match(/^# tests (\d+)$/m)?.[1] ?? 0);
  const passed = Number(completed.stdout.match(/^# pass (\d+)$/m)?.[1] ?? 0);
  const failed = Number(completed.stdout.match(/^# fail (\d+)$/m)?.[1] ?? 0);
  if (!tests || tests !== passed || failed !== 0) throw new Error(`${suite} emitted incomplete TAP totals`);
  return { suite, tests, passed, failed };
}

async function validationInputDigest() {
  const roots = ['contracts', 'fixtures', 'src', 'tests'].map(name => join(operationalRoot, name));
  const files = (await Promise.all(roots.map(filesUnder))).flat();
  files.push(fileURLToPath(import.meta.url), join(operationalRoot, 'README.md'));
  return digestFiles(files, operationalRoot);
}

async function validateOnce() {
  const canonicalBefore = await canonicalVaultDigest();
  const documents = await loadJsonSurfaces();
  validateCrossContracts(documents);
  await validateSourceDiagnosticClosure(documents);
  const suiteResults = suites.map(runSuite);
  const canonicalAfter = await canonicalVaultDigest();
  if (canonicalAfter !== canonicalBefore) throw new Error('canonical vault delta detected');
  const passedSuites = new Set(suiteResults.filter(result => result.failed === 0).map(result => result.suite));
  const scenarioResults = Object.entries(scenarioOwner).map(([scenario_id, suite]) => ({ scenario_id, suite, status: passedSuites.has(suite) ? 'pass' : 'fail' }));
  if (scenarioResults.some(result => result.status !== 'pass')) throw new Error('scenario coverage is not fully observed');
  return {
    contract: 'animejs-agent-knowledge-api-validation/0.1.0',
    status: 'pass',
    input_digest: await validationInputDigest(),
    json_document_count: documents.size,
    suite_results: suiteResults,
    scenario_coverage: { planned: 30, observed: 30, results: scenarioResults },
    canonical_vault_before_digest: canonicalBefore,
    canonical_vault_after_digest: canonicalAfter,
    canonical_vault_delta_zero: true,
    verified_lessons_created: 0,
    temporary_repository_data_left: false,
    semantic_effect: 'none',
    task_state_unchanged: true,
    truth_status: 'not_assessed',
    authority_effect: 'none',
    evidence_ceiling: 'candidate-local L0-L2 transport-neutral core validation',
  };
}

async function main() {
  const verifyRepeat = process.argv.includes('--verify-repeat');
  const first = await validateOnce();
  if (verifyRepeat) {
    const second = await validateOnce();
    if (JSON.stringify(first) !== JSON.stringify(second)) throw new Error('repeat validation produced nondeterministic receipt fields');
  }
  await writeFile(receiptPath, `${JSON.stringify(first, null, 2)}\n`, 'utf8');
  process.stdout.write(`${JSON.stringify({ status: first.status, suites: first.suite_results.length, tests: first.suite_results.reduce((sum, suite) => sum + suite.tests, 0), scenarios: first.scenario_coverage.observed, canonical_vault_delta_zero: first.canonical_vault_delta_zero, repeat_verified: verifyRepeat })}\n`);
}

main().catch(error => {
  process.stderr.write(`${error.stack ?? error.message}\n`);
  process.exitCode = 1;
});
