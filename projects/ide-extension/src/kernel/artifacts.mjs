import { lstat, mkdir, open, readFile, realpath, stat } from 'node:fs/promises';
import path from 'node:path';

const ARTIFACT_ID_PATTERN = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;

function artifactError(code, message, fields = {}) {
  const error = new Error(message);
  error.code = code;
  Object.assign(error, fields);
  return error;
}

function assertArtifactId(artifactId) {
  if (typeof artifactId !== 'string' || !ARTIFACT_ID_PATTERN.test(artifactId)) {
    throw artifactError('invalid_artifact_id', `invalid artifact id: ${artifactId}`);
  }
  return artifactId;
}

export function evidenceArtifactIds({ run_id: runId, approval_id: approvalId }) {
  assertArtifactId(runId);
  assertArtifactId(approvalId);
  const prefix = `artifact-${runId}-${approvalId}`;
  return Object.freeze({
    before: `${prefix}-before`,
    after: `${prefix}-after`,
    receipt: `${prefix}-receipt`
  });
}

export function claimArtifactIds({ run_id: runId, claim_id: claimId }) {
  assertArtifactId(runId);
  assertArtifactId(claimId);
  const prefix = `artifact-${runId}-${claimId}`;
  return Object.freeze({
    claim: `${prefix}-claim`,
    interrupt: `${prefix}-interrupt`,
    release: `${prefix}-release`
  });
}

export function executionArtifactIds({ run_id: runId, receipt_id: receiptId }) {
  assertArtifactId(runId);
  assertArtifactId(receiptId);
  const prefix = `artifact-${runId}-${receiptId}`;
  return Object.freeze({
    after: `${prefix}-after`,
    result: `${prefix}-result`,
    receipt: `${prefix}-execution-receipt`
  });
}

export async function ensureArtifactDir(artifactDir) {
  await mkdir(artifactDir, { recursive: true });
}

export function artifactRefFor(artifactDir, artifactId) {
  assertArtifactId(artifactId);
  return path.relative(process.cwd(), path.join(path.resolve(artifactDir), `${artifactId}.json`));
}

export function resolveArtifactRef(artifactDir, artifactRef) {
  if (typeof artifactRef !== 'string' || artifactRef.length === 0) {
    throw artifactError('invalid_artifact_ref', 'artifact ref must be a non-empty string');
  }

  const root = path.resolve(artifactDir);
  const resolved = path.resolve(process.cwd(), artifactRef);
  if (path.dirname(resolved) !== root || path.extname(resolved) !== '.json') {
    throw artifactError('artifact_path_escape', `artifact ref escapes its root: ${artifactRef}`, {
      artifact_ref: artifactRef
    });
  }
  return resolved;
}

export async function writeArtifactRef(artifactDir, artifactId, value) {
  await ensureArtifactDir(artifactDir);
  const artifactRef = artifactRefFor(artifactDir, artifactId);
  const file = resolveArtifactRef(artifactDir, artifactRef);
  let handle;

  try {
    handle = await open(file, 'wx');
    await handle.writeFile(`${JSON.stringify(value, null, 2)}\n`, 'utf8');
    await handle.sync();
  } catch (error) {
    if (error.code === 'EEXIST') {
      throw artifactError('artifact_exists', `artifact already exists: ${artifactId}`, {
        artifact_id: artifactId,
        artifact_ref: artifactRef
      });
    }
    throw error;
  } finally {
    if (handle) await handle.close();
  }

  return artifactRef;
}

export async function readArtifactRef(artifactDir, artifactRef) {
  const file = resolveArtifactRef(artifactDir, artifactRef);
  let raw;
  try {
    const details = await lstat(file);
    if (!details.isFile() || details.isSymbolicLink()) {
      throw artifactError('artifact_path_escape', `artifact ref is not a contained regular file: ${artifactRef}`, {
        artifact_ref: artifactRef
      });
    }
    raw = await readFile(file, 'utf8');
  } catch (error) {
    if (error.code === 'ENOENT') {
      throw artifactError('artifact_not_found', `artifact does not exist: ${artifactRef}`, {
        artifact_ref: artifactRef
      });
    }
    throw error;
  }

  try {
    return JSON.parse(raw);
  } catch {
    throw artifactError('malformed_artifact', `artifact is not valid JSON: ${artifactRef}`, {
      artifact_ref: artifactRef
    });
  }
}

export async function validateArtifactRef(artifactDir, artifactRef, expectedBindings) {
  const artifact = await readArtifactRef(artifactDir, artifactRef);

  for (const [field, expected] of Object.entries(expectedBindings)) {
    if (JSON.stringify(artifact[field]) !== JSON.stringify(expected)) {
      throw artifactError(
        'artifact_binding_mismatch',
        `${artifactRef}: ${field} does not match its bound value`,
        { artifact_ref: artifactRef, field }
      );
    }
  }

  return artifact;
}

export async function validateEvidenceRefs(evidenceRoot, evidenceRefs) {
  if (!Array.isArray(evidenceRefs)) {
    throw artifactError('invalid_evidence_refs', 'evidence refs must be an array');
  }

  const root = path.resolve(evidenceRoot);
  let realRoot;
  try {
    realRoot = await realpath(root);
  } catch {
    throw artifactError('evidence_root_not_found', `evidence root does not resolve: ${root}`);
  }

  for (const evidenceRef of evidenceRefs) {
    if (typeof evidenceRef !== 'string' || evidenceRef.length === 0 || path.isAbsolute(evidenceRef)) {
      throw artifactError('invalid_evidence_ref', `invalid evidence ref: ${evidenceRef}`);
    }
    const resolved = path.resolve(root, evidenceRef);
    const relative = path.relative(root, resolved);
    if (relative.startsWith('..') || path.isAbsolute(relative)) {
      throw artifactError('evidence_path_escape', `evidence ref escapes its root: ${evidenceRef}`);
    }

    try {
      const realResolved = await realpath(resolved);
      const realRelative = path.relative(realRoot, realResolved);
      if (realRelative.startsWith('..') || path.isAbsolute(realRelative)) {
        throw artifactError('evidence_path_escape', `evidence ref escapes its root: ${evidenceRef}`);
      }
      const details = await stat(realResolved);
      if (!details.isFile()) throw new Error('not a file');
    } catch (error) {
      if (error.code === 'evidence_path_escape') throw error;
      throw artifactError('evidence_not_found', `evidence ref does not resolve: ${evidenceRef}`, {
        evidence_ref: evidenceRef
      });
    }
  }

  return evidenceRefs;
}
