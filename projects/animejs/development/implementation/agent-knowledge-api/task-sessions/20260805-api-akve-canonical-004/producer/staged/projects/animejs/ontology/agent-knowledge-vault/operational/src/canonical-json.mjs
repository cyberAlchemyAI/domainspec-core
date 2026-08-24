import { createHash } from 'node:crypto';

function normalize(value, seen = new Set()) {
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) throw new TypeError('canonical JSON forbids non-finite numbers');
    return Object.is(value, -0) ? 0 : value;
  }
  if (typeof value !== 'object') throw new TypeError(`canonical JSON forbids ${typeof value}`);
  if (seen.has(value)) throw new TypeError('canonical JSON forbids cycles');
  seen.add(value);
  let result;
  if (Array.isArray(value)) {
    result = value.map(item => normalize(item, seen));
  } else {
    const prototype = Object.getPrototypeOf(value);
    if (prototype !== Object.prototype && prototype !== null) throw new TypeError('canonical JSON requires plain objects');
    result = {};
    for (const key of Object.keys(value).sort()) {
      if (value[key] === undefined) throw new TypeError(`canonical JSON forbids undefined at ${key}`);
      result[key] = normalize(value[key], seen);
    }
  }
  seen.delete(value);
  return result;
}

export function canonicalJson(value) {
  return JSON.stringify(normalize(value));
}

export function canonicalBytes(value) {
  return Buffer.from(canonicalJson(value), 'utf8');
}

export function sha256(value) {
  const bytes = Buffer.isBuffer(value) || value instanceof Uint8Array ? value : canonicalBytes(value);
  return createHash('sha256').update(bytes).digest('hex');
}
