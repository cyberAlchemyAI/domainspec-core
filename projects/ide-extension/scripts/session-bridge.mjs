import { readFile } from 'node:fs/promises';

const EXIT = Object.freeze({ usage: 2, unavailable: 3, connection: 4, rejected: 5 });
const DEFAULT_BASE_URL = 'http://127.0.0.1:8765';

function fail(code, error, details = {}) {
  process.stderr.write(`${JSON.stringify({ error, ...details })}\n`);
  process.exitCode = code;
}

function parseOptions(values) {
  const options = {};
  for (let index = 0; index < values.length; index += 2) {
    const flag = values[index];
    const value = values[index + 1];
    if (!flag?.startsWith('--') || value === undefined || value.startsWith('--')) {
      throw new Error(`invalid option near ${flag || '<end>'}`);
    }
    const key = flag.slice(2).replaceAll('-', '_');
    if (Object.hasOwn(options, key)) throw new Error(`duplicate option ${flag}`);
    options[key] = value;
  }
  return options;
}

function resolveBaseUrl(raw) {
  const url = new URL(raw || process.env.IDE_EXTENSION_BRIDGE_URL || DEFAULT_BASE_URL);
  if (url.protocol !== 'http:'
    || !['127.0.0.1', 'localhost', '[::1]'].includes(url.hostname)
    || (url.pathname !== '/' && url.pathname !== '')) {
    throw new Error('base URL must be a loopback HTTP origin');
  }
  url.pathname = '';
  url.search = '';
  url.hash = '';
  return url.toString().replace(/\/$/, '');
}

async function inputJson(source) {
  const raw = source === '-'
    ? await new Promise((resolve, reject) => {
        const chunks = [];
        process.stdin.on('data', (chunk) => chunks.push(chunk));
        process.stdin.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
        process.stdin.on('error', reject);
      })
    : await readFile(source, 'utf8');
  const value = JSON.parse(raw);
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('input must be one JSON object');
  }
  return value;
}

async function requestJson(baseUrl, route, options = {}) {
  let response;
  try {
    response = await fetch(`${baseUrl}${route}`, {
      ...options,
      headers: { 'content-type': 'application/json', ...(options.headers || {}) }
    });
  } catch (error) {
    fail(EXIT.connection, 'bridge_unreachable', { message: error.message });
    return null;
  }
  const raw = await response.text();
  let body;
  try {
    body = JSON.parse(raw);
  } catch {
    fail(EXIT.rejected, 'invalid_bridge_response', { status: response.status });
    return null;
  }
  if (!response.ok) {
    const unavailable = response.status === 404 || response.status === 409;
    fail(unavailable ? EXIT.unavailable : EXIT.rejected, body.error || 'bridge_rejected', {
      status: response.status
    });
    return null;
  }
  return body;
}

async function main() {
  const [command, ...values] = process.argv.slice(2);
  if (!['ready', 'claim', 'result', 'interrupt', 'publish', 'events'].includes(command)) {
    fail(EXIT.usage, 'usage', { commands: ['ready', 'claim', 'result', 'interrupt', 'publish', 'events'] });
    return;
  }

  let options;
  let baseUrl;
  try {
    options = parseOptions(values);
    baseUrl = resolveBaseUrl(options.base_url);
  } catch (error) {
    fail(EXIT.usage, 'invalid_arguments', { message: error.message });
    return;
  }

  let body;
  if (command === 'ready') {
    const allowed = new Set(['base_url']);
    if (Object.keys(options).some((key) => !allowed.has(key))) {
      fail(EXIT.usage, 'invalid_arguments');
      return;
    }
    body = await requestJson(
      baseUrl,
      '/api/bridge/requests/ready?agent_ref=codex.current-session'
    );
    if (body && body.request === null) {
      fail(EXIT.unavailable, 'no_ready_request');
      return;
    }
  } else if (command === 'publish') {
    const allowed = new Set(['base_url', 'path', 'title', 'kind']);
    if (Object.keys(options).some((key) => !allowed.has(key))
      || !options.path || !options.title || !options.kind) {
      fail(EXIT.usage, 'invalid_arguments', { required: ['path', 'title', 'kind'] });
      return;
    }
    body = await requestJson(baseUrl, '/api/canvas/publish', {
      method: 'POST',
      body: JSON.stringify({
        schema_version: '1',
        path: options.path,
        title: options.title,
        kind: options.kind
      })
    });
  } else if (command === 'events') {
    const allowed = new Set(['base_url', 'after']);
    if (Object.keys(options).some((key) => !allowed.has(key))
      || !/^(0|[1-9][0-9]*)$/.test(options.after || '')
      || !Number.isSafeInteger(Number(options.after))) {
      fail(EXIT.usage, 'invalid_arguments', { required: ['after'] });
      return;
    }
    body = await requestJson(
      baseUrl,
      `/api/canvas/events?after=${encodeURIComponent(options.after)}`
    );
  } else if (command === 'claim') {
    const allowed = new Set(['base_url', 'request_handle', 'session_ref']);
    if (Object.keys(options).some((key) => !allowed.has(key))
      || !options.request_handle || !options.session_ref) {
      fail(EXIT.usage, 'invalid_arguments', { required: ['request-handle', 'session-ref'] });
      return;
    }
    body = await requestJson(
      baseUrl,
      `/api/bridge/requests/${encodeURIComponent(options.request_handle)}/claim`,
      {
        method: 'POST',
        body: JSON.stringify({
          schema_version: '2',
          envelope_id: options.request_handle,
          agent_ref: 'codex.current-session',
          session_ref: options.session_ref,
          assurance: 'unattested'
        })
      }
    );
  } else {
    const allowed = new Set(['base_url', 'claim_id', 'input']);
    if (Object.keys(options).some((key) => !allowed.has(key))
      || !options.claim_id || !options.input) {
      fail(EXIT.usage, 'invalid_arguments', { required: ['claim-id', 'input'] });
      return;
    }
    let input;
    try {
      input = await inputJson(options.input);
    } catch (error) {
      fail(EXIT.usage, 'invalid_input', { message: error.message });
      return;
    }
    body = await requestJson(
      baseUrl,
      `/api/bridge/claims/${encodeURIComponent(options.claim_id)}/${command}`,
      { method: 'POST', body: JSON.stringify(input) }
    );
  }

  if (body) process.stdout.write(`${JSON.stringify(body)}\n`);
}

await main();
