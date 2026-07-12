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

export function createProjectionStore(options) {
  const {
    eventsFile,
    workbenchFile,
    artifactDir,
    append = appendEvent,
    writeProjection = atomicWriteJson
  } = options;

  async function reconcile(reduceOptions = {}) {
    const events = await readEvents(eventsFile);
    const projection = reduceEvents(events, reduceOptions);
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
      orphan_artifacts: await orphanArtifacts(artifactDir, events)
    };
  }

  async function commitEvent(event, reduceOptions = {}) {
    const events = await readEvents(eventsFile);
    const nextEvents = [...events, event];
    const projection = reduceEvents(nextEvents, reduceOptions);
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
      orphan_artifacts: await orphanArtifacts(artifactDir, nextEvents)
    };
  }

  return Object.freeze({ reconcile, commitEvent });
}
