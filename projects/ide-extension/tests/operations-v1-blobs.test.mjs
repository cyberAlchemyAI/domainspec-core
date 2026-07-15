import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import * as fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { createCanvasBlobStore } from '../src/kernel/canvas-blobs.mjs';
import { OPERATIONS_V1_LIMITS } from '../src/kernel/operations-contracts.mjs';

async function fixture(t) {
  const stateDir = await fs.mkdtemp(path.join(os.tmpdir(), 'ide-extension-blobs-'));
  t.after(() => fs.rm(stateDir, { recursive: true, force: true }));
  return { stateDir, store: createCanvasBlobStore({ stateDir }) };
}

function digest(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

test('stores, reads, verifies, and deduplicates exact bytes', async (t) => {
  const { stateDir, store } = await fixture(t);
  const bytes = Buffer.from('<!doctype html><p>Alchemy</p>', 'utf8');
  const expectedDigest = digest(bytes);

  const first = await store.put(bytes);
  assert.equal(first.sha256, expectedDigest);
  assert.equal(first.blob_ref, `canvas/blobs/${expectedDigest}.html`);
  assert.equal(first.byte_length, bytes.length);
  assert.equal(first.deduplicated, false);
  assert.deepEqual(first.bytes, bytes);

  bytes.fill(0);
  const read = await store.read(expectedDigest);
  assert.equal(read.bytes.toString('utf8'), '<!doctype html><p>Alchemy</p>');

  const second = await store.put(Buffer.from('<!doctype html><p>Alchemy</p>'));
  assert.equal(second.deduplicated, true);
  assert.deepEqual(second.bytes, read.bytes);

  const entries = await fs.readdir(path.join(stateDir, 'canvas', 'blobs'));
  assert.deepEqual(entries, [`${expectedDigest}.html`]);
});

test('serializes simultaneous same-digest writes to one final file', async (t) => {
  const { stateDir, store } = await fixture(t);
  const bytes = Buffer.from('<!doctype html><body><p>Concurrent</p></body>');
  const results = await Promise.all(Array.from({ length: 16 }, () => store.put(bytes)));

  assert.equal(results.filter((result) => !result.deduplicated).length, 1);
  assert.equal(results.filter((result) => result.deduplicated).length, 15);
  assert.equal(new Set(results.map((result) => result.sha256)).size, 1);
  const entries = await fs.readdir(path.join(stateDir, 'canvas', 'blobs'));
  assert.deepEqual(entries, [`${results[0].sha256}.html`]);
  assert.equal(entries.some((entry) => entry.endsWith('.tmp')), false);
});

test('rejects non-Buffer, empty, and oversized bodies before filesystem mutation', async (t) => {
  const { stateDir, store } = await fixture(t);
  await assert.rejects(store.put('html'), { code: 'canvas_blob_invalid_bytes' });
  await assert.rejects(store.put(Buffer.alloc(0)), { code: 'canvas_blob_empty' });
  await assert.rejects(
    store.put(Buffer.alloc(OPERATIONS_V1_LIMITS.result_html_bytes + 1)),
    (error) => error.code === 'canvas_blob_limit_exceeded'
      && error.actual_bytes === OPERATIONS_V1_LIMITS.result_html_bytes + 1
      && error.max_bytes === OPERATIONS_V1_LIMITS.result_html_bytes
  );
  await assert.rejects(fs.access(path.join(stateDir, 'canvas', 'blobs')), { code: 'ENOENT' });
});

test('fails closed for invalid, missing, non-regular, empty, and corrupt blobs', async (t) => {
  const { stateDir, store } = await fixture(t);
  await assert.rejects(store.read('../escape'), { code: 'canvas_blob_invalid_digest' });
  await assert.rejects(store.read('a'.repeat(64)), { code: 'canvas_blob_not_found' });

  const blobDir = path.join(stateDir, 'canvas', 'blobs');
  await fs.mkdir(blobDir, { recursive: true });
  const emptyDigest = digest(Buffer.alloc(0));
  await fs.writeFile(path.join(blobDir, `${emptyDigest}.html`), Buffer.alloc(0));
  await assert.rejects(
    store.read(emptyDigest),
    (error) => error.code === 'canvas_blob_corrupt' && error.reason === 'empty'
  );

  const expected = Buffer.from('expected');
  const expectedDigest = digest(expected);
  await fs.writeFile(path.join(blobDir, `${expectedDigest}.html`), 'corrupt');
  await assert.rejects(
    store.read(expectedDigest),
    (error) => error.code === 'canvas_blob_corrupt' && error.reason === 'digest_mismatch'
  );
  await assert.rejects(store.put(expected), { code: 'canvas_blob_corrupt' });

  const directoryDigest = 'b'.repeat(64);
  await fs.mkdir(path.join(blobDir, `${directoryDigest}.html`));
  await assert.rejects(store.read(directoryDigest), { code: 'canvas_blob_not_regular' });
});

test('cleans only its owned temporary file after permission or rename failure', async (t) => {
  const mkdirDir = await fs.mkdtemp(path.join(os.tmpdir(), 'ide-extension-blob-mkdir-'));
  const permissionDir = await fs.mkdtemp(path.join(os.tmpdir(), 'ide-extension-blob-permission-'));
  const renameDir = await fs.mkdtemp(path.join(os.tmpdir(), 'ide-extension-blob-rename-'));
  t.after(() => Promise.all([
    fs.rm(mkdirDir, { recursive: true, force: true }),
    fs.rm(permissionDir, { recursive: true, force: true }),
    fs.rm(renameDir, { recursive: true, force: true })
  ]));

  const mkdirStore = createCanvasBlobStore({
    stateDir: mkdirDir,
    fileSystem: {
      mkdir: async () => {
        const error = new Error('permission denied');
        error.code = 'EACCES';
        throw error;
      }
    }
  });
  await assert.rejects(
    mkdirStore.put(Buffer.from('mkdir permission')),
    (error) => error.code === 'canvas_blob_write_failed' && error.cause_code === 'EACCES'
  );

  const permissionStore = createCanvasBlobStore({
    stateDir: permissionDir,
    fileSystem: {
      open: async () => {
        const error = new Error('permission denied');
        error.code = 'EACCES';
        throw error;
      }
    },
    randomId: () => 'permission'
  });
  await assert.rejects(
    permissionStore.put(Buffer.from('permission')),
    (error) => error.code === 'canvas_blob_write_failed' && error.cause_code === 'EACCES'
  );
  assert.deepEqual(await fs.readdir(path.join(permissionDir, 'canvas', 'blobs')), []);

  const unrelated = '.unrelated.tmp';
  const blobDir = path.join(renameDir, 'canvas', 'blobs');
  await fs.mkdir(blobDir, { recursive: true });
  await fs.writeFile(path.join(blobDir, unrelated), 'keep');
  const renameStore = createCanvasBlobStore({
    stateDir: renameDir,
    fileSystem: {
      rename: async () => {
        const error = new Error('rename failed');
        error.code = 'EXDEV';
        throw error;
      }
    },
    randomId: () => 'rename'
  });
  await assert.rejects(
    renameStore.put(Buffer.from('rename')),
    (error) => error.code === 'canvas_blob_write_failed' && error.cause_code === 'EXDEV'
  );
  assert.deepEqual(await fs.readdir(blobDir), [unrelated]);
});

test('reports deterministic reachability, totals, largest blob, and stale temporaries', async (t) => {
  const { stateDir, store } = await fixture(t);
  const smaller = await store.put(Buffer.from('small'));
  const larger = await store.put(Buffer.from('a larger complete html body'));
  const blobDir = path.join(stateDir, 'canvas', 'blobs');
  await fs.writeFile(path.join(blobDir, '.stale.123.tmp'), 'stale');
  await fs.writeFile(path.join(blobDir, 'README.txt'), 'unexpected');
  const missing = 'f'.repeat(64);

  const first = await store.diagnostics([missing, smaller.sha256, smaller.sha256]);
  const second = await store.diagnostics([smaller.sha256, missing]);
  assert.deepEqual(second, first);
  assert.equal(first.blob_count, 2);
  assert.equal(first.total_bytes, smaller.byte_length + larger.byte_length);
  assert.equal(first.largest_blob.sha256, larger.sha256);
  assert.deepEqual(first.blobs.map((blob) => blob.sha256), [larger.sha256, smaller.sha256].sort());
  assert.deepEqual(first.missing_references, [missing]);
  assert.deepEqual(first.unreferenced_blobs, [larger.sha256]);
  assert.deepEqual(first.temporary_files, [
    { name: '.stale.123.tmp', byte_length: 5, kind: 'file' }
  ]);
  assert.deepEqual(first.unexpected_entries, [{ name: 'README.txt', kind: 'file' }]);

  const entriesAfter = await fs.readdir(blobDir);
  assert.ok(entriesAfter.includes('.stale.123.tmp'));
  assert.ok(entriesAfter.includes('README.txt'));
});

test('reports missing references deterministically when the blob directory is absent', async (t) => {
  const { store } = await fixture(t);
  const references = ['2'.repeat(64), '1'.repeat(64), '2'.repeat(64)];
  const report = await store.diagnostics(references);
  assert.equal(report.blob_count, 0);
  assert.equal(report.total_bytes, 0);
  assert.equal(report.largest_blob, null);
  assert.deepEqual(report.missing_references, ['1'.repeat(64), '2'.repeat(64)]);
  assert.deepEqual(report.temporary_files, []);
});
