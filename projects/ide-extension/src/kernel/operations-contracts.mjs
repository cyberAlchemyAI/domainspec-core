const KIB = 1024;
const MIB = 1024 * KIB;
const GIB = 1024 * MIB;

export const OPERATIONS_V1_EVENT_VERSION = 4;

export const OPERATIONS_V1_EVENT_TYPES = Object.freeze([
  'canvas.operations_surface_derived',
  'canvas.content_operation_committed',
  'canvas.display_target_selected',
  'canvas.pruning_requested',
  'canvas.revision_pruned',
  'canvas.pruning_completed',
  'canvas.interaction_recorded'
]);

export const OPERATIONS_V1_LIMITS = Object.freeze({
  http_request_bytes: 5 * MIB,
  source_html_bytes: 4 * MIB,
  fragment_html_bytes: 512 * KIB,
  result_html_bytes: 8 * MIB,
  retention_soft_bytes: GIB,
  retention_hard_bytes: 2 * GIB,
  retention_grace_ms: 7 * 24 * 60 * 60 * 1000,
  retention_reclaim_below_bytes: GIB
});

export function utf8ByteLength(value) {
  if (typeof value !== 'string') {
    throw new TypeError('UTF-8 byte measurement requires a string');
  }
  return Buffer.byteLength(value, 'utf8');
}

export function assertUtf8ByteLimit(value, maxBytes, limitName) {
  if (!Number.isSafeInteger(maxBytes) || maxBytes < 0) {
    throw new TypeError('UTF-8 byte limit must be a non-negative safe integer');
  }
  if (typeof limitName !== 'string' || !limitName) {
    throw new TypeError('UTF-8 byte limit requires a name');
  }

  const actualBytes = utf8ByteLength(value);
  if (actualBytes > maxBytes) {
    const error = new Error(`${limitName} exceeds ${maxBytes} UTF-8 bytes`);
    error.code = 'operations_byte_limit_exceeded';
    error.limit_name = limitName;
    error.max_bytes = maxBytes;
    error.actual_bytes = actualBytes;
    throw error;
  }
  return actualBytes;
}
