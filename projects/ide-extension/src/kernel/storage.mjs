import { randomUUID } from 'node:crypto';
import { mkdir, open, readFile, readdir, rename, rm } from 'node:fs/promises';
import path from 'node:path';
import { appendEvent, readEvents } from './audit.mjs';
import { projectionChecksum, reduceEvents } from './projector.mjs';

async function readProjection(file) {
  try {
    return JSON.parse(await readFile(file, 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT' || error instanceof SyntaxError) return null;
    throw error;
  }
}

export async function atomicWriteJson(file, value) {
  await mkdir(path.dirname(file), { recursive: true });
  const temporary = path.join(
    path.dirname(file),
    `.${path.basename(file)}.${process.pid}.${randomUUID()}.tmp`
  );
  let handle;

  try {
    handle = await open(temporary, 'wx');
    await handle.writeFile(`${JSON.stringify(value, null, 2)}\n`, 'utf8');
    await handle.sync();
    await handle.close();
    handle = null;
    await rename(temporary, file);
  } catch (error) {
    if (handle) await handle.close().catch(() => undefined);
    await rm(temporary, { force: true }).catch(() => undefined);
    throw error;
  }
}

async function orphanArtifacts(artifactDir, events) {
  let entries;
  try {
    entries = await readdir(artifactDir, { withFileTypes: true });
  } catch (error) {
    if (error.code === 'ENOENT') return [];
    throw error;
  }

  const referenced = new Set(
    events.flatMap((event) => event.artifact_refs || []).map((ref) => path.basename(ref))
  );
  return entries
    .filter((entry) => entry.isFile() && !referenced.has(entry.name))
    .map((entry) => path.join('artifacts', entry.name))
    .sort();
}

function projectionFailure(error) {
  const failure = new Error(`projection replacement failed: ${error.message}`);
  failure.code = 'projection_write_failed';
  failure.cause_code = error.code || null;
  return failure;
}

async function replaceProjection(writeProjection, workbenchFile, projection) {
  try {
    await writeProjection(workbenchFile, projection);
  } catch (error) {
    throw projectionFailure(error);
  }
}

function blobReferenceError(code, message, fields = {}) {
  const error = new Error(message);
  error.code = code;
  Object.assign(error, fields);
  return error;
}

function unprunedOperationsRevisions(projection) {
  const operations = projection.canvas?.operations_v1;
  if (!operations) return [];
  return Object.values(operations.revisions)
    .filter((revision) => !operations.prune_tombstones[revision.revision_id])
    .sort((left, right) => left.revision_id.localeCompare(right.revision_id));
}

async function reconcileCanvasBlobs(projection, canvasBlobStore) {
  const revisions = unprunedOperationsRevisions(projection);
  if (!canvasBlobStore) {
    if (revisions.length === 0) return null;
    throw blobReferenceError(
      'canvas_blob_store_required',
      'unpruned Operations V1 revisions require a Canvas blob store',
      { revision_ids: revisions.map((revision) => revision.revision_id) }
    );
  }
  if (typeof canvasBlobStore.read !== 'function' || typeof canvasBlobStore.diagnostics !== 'function') {
    throw blobReferenceError('canvas_blob_store_invalid', 'Canvas blob store must expose read and diagnostics');
  }

  for (const revision of revisions) {
    try {
      const blob = await canvasBlobStore.read(revision.content_sha256);
      if (blob.blob_ref !== revision.blob_ref || blob.byte_length !== revision.byte_length) {
        throw blobReferenceError(
          'canvas_blob_metadata_mismatch',
          `blob metadata does not match revision ${revision.revision_id}`,
          {
            expected_blob_ref: revision.blob_ref,
            actual_blob_ref: blob.blob_ref,
            expected_byte_length: revision.byte_length,
            actual_byte_length: blob.byte_length
          }
        );
      }
    } catch (error) {
      throw blobReferenceError(
        'canvas_blob_reference_invalid',
        `invalid blob reference for revision ${revision.revision_id}: ${error.message}`,
        {
          revision_id: revision.revision_id,
          digest: revision.content_sha256,
          cause_code: error.code || null
        }
      );
    }
  }

  const referencedDigests = [...new Set(revisions.map((revision) => revision.content_sha256))];
  const diagnostics = await canvasBlobStore.diagnostics(referencedDigests);
  if (diagnostics.missing_references.length > 0) {
    throw blobReferenceError(
      'canvas_blob_reference_invalid',
      'blob diagnostics found missing committed references',
      {
        cause_code: 'canvas_blob_not_found',
        digests: [...diagnostics.missing_references]
      }
    );
  }
  return diagnostics;
}

export function createProjectionStore(options) {
  const {
    eventsFile,
    workbenchFile,
    artifactDir,
    canvasBlobStore = null,
    append = appendEvent,
    writeProjection = atomicWriteJson
  } = options;

  async function reconcile(reduceOptions = {}) {
    const events = await readEvents(eventsFile);
    const projection = reduceEvents(events, reduceOptions);
    const canvasBlobs = await reconcileCanvasBlobs(projection, canvasBlobStore);
    const existing = await readProjection(workbenchFile);
    const checksum = projectionChecksum(projection);
    const repaired = !existing || projectionChecksum(existing) !== checksum;

    if (repaired) await replaceProjection(writeProjection, workbenchFile, projection);

    return {
      projection,
      events,
      event_count: events.length,
      projection_checksum: checksum,
      repaired,
      orphan_artifacts: await orphanArtifacts(artifactDir, events),
      canvas_blobs: canvasBlobs
    };
  }

  async function commitEvent(event, reduceOptions = {}) {
    const events = await readEvents(eventsFile);
    const nextEvents = [...events, event];
    const projection = reduceEvents(nextEvents, reduceOptions);
    const canvasBlobs = await reconcileCanvasBlobs(projection, canvasBlobStore);
    await append(eventsFile, event);

    try {
      await replaceProjection(writeProjection, workbenchFile, projection);
    } catch (error) {
      const failure = new Error('event committed; projection reconciliation required');
      failure.code = 'reconciliation_required';
      failure.cause_code = error.code;
      failure.event_id = event.event_id;
      throw failure;
    }

    return {
      projection,
      events: nextEvents,
      event_count: nextEvents.length,
      projection_checksum: projectionChecksum(projection),
      repaired: false,
      orphan_artifacts: await orphanArtifacts(artifactDir, nextEvents),
      canvas_blobs: canvasBlobs
    };
  }

  return Object.freeze({ reconcile, commitEvent });
}
