import { createHash, randomUUID } from 'node:crypto';
import {
  lstat,
  mkdir,
  open,
  readFile,
  readdir,
  rename,
  rm
} from 'node:fs/promises';
import path from 'node:path';
import { OPERATIONS_V1_LIMITS } from './operations-contracts.mjs';

const DIGEST_PATTERN = /^[a-f0-9]{64}$/;
const BLOB_FILE_PATTERN = /^([a-f0-9]{64})\.html$/;
const TEMPORARY_FILE_PATTERN = /^\.[^/]+\.tmp$/;
const DEFAULT_FILE_SYSTEM = Object.freeze({ lstat, mkdir, open, readFile, readdir, rename, rm });

function blobError(code, message, fields = {}) {
  const error = new Error(message);
  error.code = code;
  Object.assign(error, fields);
  return error;
}

function assertDigest(digest) {
  if (typeof digest !== 'string' || !DIGEST_PATTERN.test(digest)) {
    throw blobError('canvas_blob_invalid_digest', 'blob digest must be 64 lowercase hex characters', {
      digest
    });
  }
  return digest;
}

function ownBytes(bytes) {
  if (!Buffer.isBuffer(bytes)) {
    throw blobError('canvas_blob_invalid_bytes', 'blob content must be a Buffer');
  }
  if (bytes.length === 0) {
    throw blobError('canvas_blob_empty', 'blob content must not be empty');
  }
  if (bytes.length > OPERATIONS_V1_LIMITS.result_html_bytes) {
    throw blobError('canvas_blob_limit_exceeded', 'blob content exceeds the result limit', {
      actual_bytes: bytes.length,
      max_bytes: OPERATIONS_V1_LIMITS.result_html_bytes
    });
  }
  return Buffer.from(bytes);
}

function digestBytes(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function wrappedFailure(kind, error, digest, cleanupError = null) {
  if (typeof error.code === 'string' && error.code.startsWith('canvas_blob_')) return error;
  return blobError(
    `canvas_blob_${kind}_failed`,
    `blob ${kind} failed: ${error.message}`,
    {
      digest,
      cause_code: error.code || null,
      cleanup_code: cleanupError?.code || null
    }
  );
}

function entryKind(entry) {
  if (entry.isFile()) return 'file';
  if (entry.isDirectory()) return 'directory';
  if (entry.isSymbolicLink()) return 'symlink';
  return 'other';
}

export function createCanvasBlobStore(options = {}) {
  if (typeof options.stateDir !== 'string' || options.stateDir.length === 0) {
    throw blobError('canvas_blob_invalid_state_dir', 'stateDir must be a non-empty string');
  }
  const stateDir = path.resolve(options.stateDir);
  const blobDir = path.join(stateDir, 'canvas', 'blobs');
  const fileSystem = Object.freeze({
    ...DEFAULT_FILE_SYSTEM,
    ...(options.fileSystem || {})
  });
  const randomId = options.randomId || randomUUID;
  if (typeof randomId !== 'function') {
    throw blobError('canvas_blob_invalid_random_id', 'randomId must be a function');
  }
  const inFlight = new Map();

  function blobPath(digest) {
    return path.join(blobDir, `${assertDigest(digest)}.html`);
  }

  function blobRef(digest) {
    return path.posix.join('canvas', 'blobs', `${assertDigest(digest)}.html`);
  }

  async function readBlob(digest) {
    assertDigest(digest);
    const file = blobPath(digest);
    let details;
    try {
      details = await fileSystem.lstat(file);
    } catch (error) {
      if (error.code === 'ENOENT') {
        throw blobError('canvas_blob_not_found', `blob does not exist: ${digest}`, { digest });
      }
      throw wrappedFailure('read', error, digest);
    }

    if (!details.isFile() || details.isSymbolicLink()) {
      throw blobError('canvas_blob_not_regular', `blob is not a regular file: ${digest}`, { digest });
    }
    if (details.size === 0 || details.size > OPERATIONS_V1_LIMITS.result_html_bytes) {
      throw blobError('canvas_blob_corrupt', `blob size is invalid: ${digest}`, {
        digest,
        reason: details.size === 0 ? 'empty' : 'size_limit',
        actual_bytes: details.size
      });
    }

    let bytes;
    try {
      bytes = await fileSystem.readFile(file);
    } catch (error) {
      throw wrappedFailure('read', error, digest);
    }
    if (bytes.length === 0 || bytes.length > OPERATIONS_V1_LIMITS.result_html_bytes) {
      throw blobError('canvas_blob_corrupt', `blob read size is invalid: ${digest}`, {
        digest,
        reason: bytes.length === 0 ? 'empty' : 'size_limit',
        actual_bytes: bytes.length
      });
    }
    const actualDigest = digestBytes(bytes);
    if (actualDigest !== digest) {
      throw blobError('canvas_blob_corrupt', `blob digest mismatch: ${digest}`, {
        digest,
        actual_digest: actualDigest,
        reason: 'digest_mismatch'
      });
    }

    return Object.freeze({
      sha256: digest,
      blob_ref: blobRef(digest),
      byte_length: bytes.length,
      bytes
    });
  }

  async function writeBlob(bytes, digest) {
    try {
      await fileSystem.mkdir(blobDir, { recursive: true });
    } catch (error) {
      throw wrappedFailure('write', error, digest);
    }

    try {
      const existing = await readBlob(digest);
      return Object.freeze({ ...existing, deduplicated: true });
    } catch (error) {
      if (error.code !== 'canvas_blob_not_found') throw error;
    }

    const temporary = path.join(
      blobDir,
      `.${digest}.${process.pid}.${randomId()}.tmp`
    );
    let handle = null;
    let ownsTemporary = false;

    try {
      handle = await fileSystem.open(temporary, 'wx', 0o600);
      ownsTemporary = true;
      await handle.writeFile(bytes);
      await handle.sync();
      await handle.close();
      handle = null;

      try {
        await fileSystem.rename(temporary, blobPath(digest));
        ownsTemporary = false;
      } catch (error) {
        if (error.code !== 'EEXIST') throw error;
        await fileSystem.rm(temporary, { force: true });
        ownsTemporary = false;
        const existing = await readBlob(digest);
        return Object.freeze({ ...existing, deduplicated: true });
      }

      const stored = await readBlob(digest);
      return Object.freeze({ ...stored, deduplicated: false });
    } catch (error) {
      if (handle) await handle.close().catch(() => undefined);
      let cleanupError = null;
      if (ownsTemporary) {
        try {
          await fileSystem.rm(temporary, { force: true });
        } catch (failure) {
          cleanupError = failure;
        }
      }
      throw wrappedFailure('write', error, digest, cleanupError);
    }
  }

  async function put(bytes) {
    const owned = ownBytes(bytes);
    const digest = digestBytes(owned);
    const pending = inFlight.get(digest);
    if (pending) {
      await pending;
      const existing = await readBlob(digest);
      return Object.freeze({ ...existing, deduplicated: true });
    }

    const operation = writeBlob(owned, digest);
    inFlight.set(digest, operation);
    try {
      return await operation;
    } finally {
      if (inFlight.get(digest) === operation) inFlight.delete(digest);
    }
  }

  async function diagnostics(referencedDigests = []) {
    if (!Array.isArray(referencedDigests)) {
      throw blobError('canvas_blob_invalid_references', 'referenced digests must be an array');
    }
    const references = [...new Set(referencedDigests.map(assertDigest))].sort();
    let entries;
    try {
      entries = await fileSystem.readdir(blobDir, { withFileTypes: true });
    } catch (error) {
      if (error.code !== 'ENOENT') throw wrappedFailure('diagnostics', error, null);
      entries = [];
    }

    const blobs = [];
    const temporaryFiles = [];
    const unexpectedEntries = [];
    for (const entry of [...entries].sort((left, right) => left.name.localeCompare(right.name))) {
      const match = entry.name.match(BLOB_FILE_PATTERN);
      if (match && entry.isFile()) {
        const blob = await readBlob(match[1]);
        blobs.push(Object.freeze({
          sha256: blob.sha256,
          blob_ref: blob.blob_ref,
          byte_length: blob.byte_length,
          referenced: references.includes(blob.sha256)
        }));
        continue;
      }
      if (entry.name.startsWith('.') && entry.name.endsWith('.tmp')) {
        const details = await fileSystem.lstat(path.join(blobDir, entry.name));
        temporaryFiles.push(Object.freeze({
          name: entry.name,
          byte_length: details.isFile() ? details.size : null,
          kind: entryKind(entry)
        }));
        continue;
      }
      unexpectedEntries.push(Object.freeze({ name: entry.name, kind: entryKind(entry) }));
    }

    const present = new Set(blobs.map((blob) => blob.sha256));
    const missingReferences = references.filter((digest) => !present.has(digest));
    const unreferencedBlobs = blobs
      .filter((blob) => !blob.referenced)
      .map((blob) => blob.sha256);
    const largestBlob = blobs.reduce((largest, blob) => (
      !largest || blob.byte_length > largest.byte_length ? blob : largest
    ), null);
    const totalBytes = blobs.reduce((total, blob) => total + blob.byte_length, 0);
    const temporaryBytes = temporaryFiles.reduce(
      (total, entry) => total + (entry.byte_length || 0),
      0
    );

    return Object.freeze({
      blob_count: blobs.length,
      total_bytes: totalBytes,
      temporary_bytes: temporaryBytes,
      physical_total_bytes: totalBytes + temporaryBytes,
      largest_blob: largestBlob,
      blobs: Object.freeze(blobs),
      temporary_files: Object.freeze(temporaryFiles),
      missing_references: Object.freeze(missingReferences),
      unreferenced_blobs: Object.freeze(unreferencedBlobs),
      unexpected_entries: Object.freeze(unexpectedEntries)
    });
  }

  async function deleteBlob(digest) {
    const existing = await readBlob(digest);
    try {
      await fileSystem.rm(blobPath(digest));
    } catch (error) {
      if (error.code === 'ENOENT') {
        return Object.freeze({
          sha256: existing.sha256,
          blob_ref: existing.blob_ref,
          byte_length: existing.byte_length,
          deleted: false
        });
      }
      throw wrappedFailure('delete', error, digest);
    }
    return Object.freeze({
      sha256: existing.sha256,
      blob_ref: existing.blob_ref,
      byte_length: existing.byte_length,
      deleted: true
    });
  }

  async function deleteTemporary(name) {
    if (typeof name !== 'string'
      || path.basename(name) !== name
      || !TEMPORARY_FILE_PATTERN.test(name)) {
      throw blobError('canvas_blob_invalid_temporary', 'temporary blob name is invalid', { name });
    }
    const file = path.join(blobDir, name);
    let details;
    try {
      details = await fileSystem.lstat(file);
    } catch (error) {
      if (error.code === 'ENOENT') {
        return Object.freeze({ name, byte_length: 0, deleted: false });
      }
      throw wrappedFailure('delete', error, null);
    }
    if (!details.isFile() || details.isSymbolicLink()) {
      throw blobError(
        'canvas_blob_temporary_not_regular',
        `temporary blob is not a regular file: ${name}`,
        { name }
      );
    }
    try {
      await fileSystem.rm(file);
    } catch (error) {
      if (error.code === 'ENOENT') {
        return Object.freeze({ name, byte_length: details.size, deleted: false });
      }
      throw wrappedFailure('delete', error, null);
    }
    return Object.freeze({ name, byte_length: details.size, deleted: true });
  }

  return Object.freeze({
    blob_dir: blobDir,
    put,
    read: readBlob,
    delete: deleteBlob,
    deleteTemporary,
    diagnostics
  });
}
