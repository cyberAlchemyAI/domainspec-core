import { createHash, randomUUID } from 'node:crypto';
import { constants } from 'node:fs';
import { open, realpath } from 'node:fs/promises';
import path from 'node:path';

function canvasError(code, message) {
  const error = new Error(message);
  error.code = code;
  return error;
}

export function normalizeCanvasPath(requestedPath) {
  if (typeof requestedPath !== 'string'
    || path.posix.isAbsolute(requestedPath)
    || requestedPath.includes('\\')
    || requestedPath.includes('%')
    || path.posix.extname(requestedPath) !== '.html') {
    throw canvasError('invalid_canvas_path', 'canvas path must be a normalized relative HTML path');
  }
  const normalized = path.posix.normalize(requestedPath);
  if (normalized !== requestedPath
    || normalized === '..'
    || normalized.startsWith('../')
    || normalized.split('/').some((part) => part === '.' || part === '..')) {
    throw canvasError('invalid_canvas_path', 'canvas path must stay inside the workspace');
  }
  return normalized;
}

function isContainedPath(root, target) {
  const relative = path.relative(root, target);
  return relative === ''
    || (relative !== '..'
      && !relative.startsWith(`..${path.sep}`)
      && !path.isAbsolute(relative));
}

function rethrowCanvasReadError(error) {
  if (['ENOENT', 'ENOTDIR'].includes(error.code)) {
    throw canvasError('canvas_file_not_found', 'canvas file not found');
  }
  if (error.code === 'ELOOP') {
    throw canvasError('canvas_path_escape', 'canvas path escapes the workspace');
  }
  throw error;
}

export async function readWorkspaceHtml(workspaceRoot, requestedPath) {
  const relativePath = normalizeCanvasPath(requestedPath);
  const root = path.resolve(workspaceRoot);
  const lexicalTarget = path.resolve(root, ...relativePath.split('/'));
  if (!isContainedPath(root, lexicalTarget)) {
    throw canvasError('canvas_path_escape', 'canvas path escapes the workspace');
  }

  const canonicalRoot = await realpath(root);
  let canonicalTarget;
  try {
    canonicalTarget = await realpath(lexicalTarget);
  } catch (error) {
    rethrowCanvasReadError(error);
  }
  if (!isContainedPath(canonicalRoot, canonicalTarget)) {
    throw canvasError('canvas_path_escape', 'canvas path escapes the workspace');
  }

  const flags = constants.O_RDONLY | (constants.O_NOFOLLOW || 0);
  let handle;
  try {
    handle = await open(canonicalTarget, flags);
  } catch (error) {
    rethrowCanvasReadError(error);
  }

  let bytes;
  try {
    const fileStat = await handle.stat();
    if (!fileStat.isFile()) {
      throw canvasError('canvas_not_file', 'canvas path must reference a file');
    }
    bytes = await handle.readFile();
  } finally {
    await handle.close();
  }

  return {
    path: relativePath,
    absolute_path: canonicalTarget,
    bytes,
    byte_length: bytes.length,
    content_sha256: createHash('sha256').update(bytes).digest('hex')
  };
}

export function prepareCanvasPublication(projection, input, file, options = {}) {
  const publishedAt = options.published_at || new Date().toISOString();
  const surfaces = projection.canvas?.surfaces || {};
  const revisions = projection.canvas?.revisions || {};
  const existing = Object.values(surfaces).find((surface) => surface.path === file.path) || null;

  if (existing) {
    const current = revisions[existing.current_revision_id];
    if (current?.content_sha256 === file.content_sha256) {
      return { idempotent: true, surface: existing, revision: current, published_at: publishedAt };
    }
  }

  const surfaceId = existing?.surface_id || `surface-${randomUUID()}`;
  const revisionId = `revision-${randomUUID()}`;
  const revision = {
    revision_id: revisionId,
    surface_id: surfaceId,
    content_sha256: file.content_sha256,
    byte_length: file.byte_length,
    published_at: publishedAt
  };
  const surface = {
    surface_id: surfaceId,
    path: file.path,
    title: input.title,
    kind: input.kind,
    current_revision_id: revisionId,
    revision_ids: [...(existing?.revision_ids || []), revisionId],
    created_at: existing?.created_at || publishedAt,
    updated_at: publishedAt
  };
  return { idempotent: false, surface, revision, published_at: publishedAt };
}

export function projectCurrentCanvas(projection) {
  const canvas = projection.canvas;
  const surface = canvas?.current_surface_id
    ? canvas.surfaces[canvas.current_surface_id]
    : null;
  const revision = surface ? canvas.revisions[surface.current_revision_id] : null;
  if (!surface || !revision) return { current: null };
  return {
    current: {
      ...surface,
      revision,
      content_url: `/api/canvas/surfaces/${encodeURIComponent(surface.surface_id)}`
        + `/revisions/${encodeURIComponent(revision.revision_id)}/content`
    }
  };
}
