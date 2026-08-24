import { createHash } from 'node:crypto';

export const PROFILE_ID = 'cal-canonical-json-v1';
export const PROFILE_SCHEMA_VERSION = '1.0.0';

export class CanonicalJsonError extends TypeError {
  constructor(code, message) {
    super(`${code}: ${message}`);
    this.name = 'CanonicalJsonError';
    this.code = code;
  }
}

function fail(code, message) {
  throw new CanonicalJsonError(code, message);
}

function isPrintableAsciiKey(key) {
  return [...key].every((character) => {
    const code = character.codePointAt(0);
    return code >= 0x20 && code <= 0x7e;
  });
}

function assertKey(key) {
  if (!isPrintableAsciiKey(key)) {
    fail('CAL_JSON_KEY_NOT_PRINTABLE_ASCII', `object key ${JSON.stringify(key)} is outside printable ASCII`);
  }
}

class RawJsonScanner {
  constructor(text) {
    if (typeof text !== 'string') {
      fail('CAL_JSON_INPUT_NOT_TEXT', 'raw JSON input must be a string');
    }
    this.text = text;
    this.index = 0;
  }

  scan() {
    this.skipWhitespace();
    this.scanValue();
    this.skipWhitespace();
    if (this.index !== this.text.length) {
      this.syntax('unexpected trailing input');
    }
  }

  syntax(message) {
    fail('CAL_JSON_SYNTAX_INVALID', `${message} at byte-like character offset ${this.index}`);
  }

  skipWhitespace() {
    while (/\s/u.test(this.text[this.index] ?? '') && /[\t\n\r ]/u.test(this.text[this.index])) {
      this.index += 1;
    }
  }

  scanValue() {
    this.skipWhitespace();
    const token = this.text[this.index];
    if (token === '{') return this.scanObject();
    if (token === '[') return this.scanArray();
    if (token === '"') return this.scanString();
    if (token === '-' || /[0-9]/u.test(token ?? '')) return this.scanNumber();
    if (this.text.startsWith('true', this.index)) return void (this.index += 4);
    if (this.text.startsWith('false', this.index)) return void (this.index += 5);
    if (this.text.startsWith('null', this.index)) return void (this.index += 4);
    this.syntax('expected a JSON value');
  }

  scanObject() {
    this.index += 1;
    this.skipWhitespace();
    const keys = new Set();
    if (this.text[this.index] === '}') {
      this.index += 1;
      return;
    }
    while (true) {
      if (this.text[this.index] !== '"') this.syntax('expected an object key');
      const key = this.scanString();
      assertKey(key);
      if (keys.has(key)) {
        fail('CAL_JSON_DUPLICATE_KEY', `duplicate object key ${JSON.stringify(key)}`);
      }
      keys.add(key);
      this.skipWhitespace();
      if (this.text[this.index] !== ':') this.syntax('expected a colon after an object key');
      this.index += 1;
      this.scanValue();
      this.skipWhitespace();
      if (this.text[this.index] === '}') {
        this.index += 1;
        return;
      }
      if (this.text[this.index] !== ',') this.syntax('expected a comma between object members');
      this.index += 1;
      this.skipWhitespace();
    }
  }

  scanArray() {
    this.index += 1;
    this.skipWhitespace();
    if (this.text[this.index] === ']') {
      this.index += 1;
      return;
    }
    while (true) {
      this.scanValue();
      this.skipWhitespace();
      if (this.text[this.index] === ']') {
        this.index += 1;
        return;
      }
      if (this.text[this.index] !== ',') this.syntax('expected a comma between array values');
      this.index += 1;
      this.skipWhitespace();
    }
  }

  scanString() {
    const start = this.index;
    this.index += 1;
    while (this.index < this.text.length) {
      const character = this.text[this.index];
      if (character === '"') {
        this.index += 1;
        const token = this.text.slice(start, this.index);
        try {
          return JSON.parse(token);
        } catch {
          this.syntax('invalid JSON string');
        }
      }
      if (character === '\\') {
        this.index += 2;
      } else {
        this.index += 1;
      }
    }
    this.syntax('unterminated JSON string');
  }

  scanNumber() {
    const source = this.text.slice(this.index);
    const match = /^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/u.exec(source);
    if (match === null) this.syntax('invalid JSON number');
    const token = match[0];
    this.index += token.length;
    if (/^-0(?:\.0+)?(?:[eE][+-]?0+)?$/u.test(token)) {
      fail('CAL_JSON_NEGATIVE_ZERO', 'negative zero is forbidden');
    }
    if (/[.eE]/u.test(token)) {
      fail('CAL_JSON_NUMBER_FORM_FORBIDDEN', `fraction or exponent form is forbidden: ${token}`);
    }
    if (!Number.isSafeInteger(Number(token))) {
      fail('CAL_JSON_UNSAFE_INTEGER', `integer is outside the JavaScript safe range: ${token}`);
    }
  }
}

function assertDataObject(value) {
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== Object.prototype && prototype !== null) {
    fail('CAL_JSON_UNSUPPORTED_VALUE', 'only plain objects are accepted');
  }
  for (const key of Reflect.ownKeys(value)) {
    if (typeof key !== 'string') {
      fail('CAL_JSON_UNSUPPORTED_VALUE', 'symbol object keys are forbidden');
    }
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (!descriptor?.enumerable || !Object.hasOwn(descriptor, 'value')) {
      fail('CAL_JSON_UNSUPPORTED_VALUE', `object key ${JSON.stringify(key)} must be an enumerable data property`);
    }
  }
}

function serialize(value, ancestors) {
  if (value === null) return 'null';
  if (typeof value === 'boolean') return value ? 'true' : 'false';
  if (typeof value === 'string') return JSON.stringify(value);
  if (typeof value === 'number') {
    if (Object.is(value, -0)) fail('CAL_JSON_NEGATIVE_ZERO', 'negative zero is forbidden');
    if (!Number.isInteger(value)) fail('CAL_JSON_NUMBER_FORM_FORBIDDEN', 'only integers are accepted');
    if (!Number.isSafeInteger(value)) fail('CAL_JSON_UNSAFE_INTEGER', 'integer is outside the JavaScript safe range');
    return String(value);
  }
  if (typeof value !== 'object') {
    fail('CAL_JSON_UNSUPPORTED_VALUE', `unsupported JavaScript value type: ${typeof value}`);
  }
  if (ancestors.has(value)) fail('CAL_JSON_CYCLE', 'cyclic values are forbidden');
  ancestors.add(value);
  try {
    if (Array.isArray(value)) {
      for (let index = 0; index < value.length; index += 1) {
        if (!Object.hasOwn(value, index)) fail('CAL_JSON_UNSUPPORTED_VALUE', 'sparse arrays are forbidden');
      }
      return `[${value.map((item) => serialize(item, ancestors)).join(',')}]`;
    }
    assertDataObject(value);
    const keys = Object.keys(value);
    for (const key of keys) assertKey(key);
    keys.sort((left, right) => Buffer.compare(Buffer.from(left, 'ascii'), Buffer.from(right, 'ascii')));
    return `{${keys.map((key) => `${JSON.stringify(key)}:${serialize(value[key], ancestors)}`).join(',')}}`;
  } finally {
    ancestors.delete(value);
  }
}

export function parseCanonicalJson(text) {
  new RawJsonScanner(text).scan();
  let value;
  try {
    value = JSON.parse(text);
  } catch (error) {
    fail('CAL_JSON_SYNTAX_INVALID', error.message);
  }
  serialize(value, new Set());
  return value;
}

export function canonicalize(value) {
  return Buffer.from(serialize(value, new Set()), 'utf8');
}

export function canonicalizeJsonText(text) {
  return canonicalize(parseCanonicalJson(text));
}

function assertSchemaVersion(schemaVersion) {
  if (typeof schemaVersion !== 'string' || schemaVersion.length === 0) {
    fail('CAL_JSON_SCHEMA_VERSION_REQUIRED', 'a non-empty value schema version is required');
  }
}

export function digestCanonical(value, schemaVersion) {
  assertSchemaVersion(schemaVersion);
  const bytes = canonicalize(value);
  const hash = createHash('sha256');
  hash.update(PROFILE_ID, 'utf8');
  hash.update('\0', 'utf8');
  hash.update(PROFILE_SCHEMA_VERSION, 'utf8');
  hash.update('\0', 'utf8');
  hash.update(schemaVersion, 'utf8');
  hash.update('\0', 'utf8');
  hash.update(bytes);
  return {
    profileId: PROFILE_ID,
    profileSchemaVersion: PROFILE_SCHEMA_VERSION,
    valueSchemaVersion: schemaVersion,
    bytes,
    sha256: hash.digest('hex')
  };
}

export function digestCanonicalJsonText(text, schemaVersion) {
  return digestCanonical(parseCanonicalJson(text), schemaVersion);
}
