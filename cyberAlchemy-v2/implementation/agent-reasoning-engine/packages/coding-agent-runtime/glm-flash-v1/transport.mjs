import {createHash} from 'node:crypto';
import {request as httpRequest} from 'node:http';
import {request as httpsRequest} from 'node:https';
import {createStatelessRecyclingTransport} from '../context-recycling.mjs';
import {projectSecretReference} from '../secret-provider.mjs';

export const MODEL = 'glm-5.3-flash';
export const stable = value => JSON.stringify(value, (_, item) => item && typeof item === 'object' && !Array.isArray(item)
  ? Object.fromEntries(Object.keys(item).sort().map(key => [key, item[key]])) : item);
export const hash = value => createHash('sha256').update(typeof value === 'string' ? value : stable(value)).digest('hex');
const integer = value => Number.isSafeInteger(value) && value >= 0;
export class GlmError extends Error {
  constructor(code, receipt = null) { super(`glm.${code}`); this.code = code; this.receipt = receipt; }
}
export const need = (ok, code) => { if (!ok) throw new GlmError(code); };

function endpoint(value) {
  let url; try { url = new URL(value); } catch { throw new GlmError('endpoint-invalid'); }
  need(!url.username && !url.password && !url.search && !url.hash, 'endpoint-invalid');
  need(url.origin === 'https://api.z.ai' || (url.protocol === 'http:' && ['127.0.0.1', '[::1]'].includes(url.hostname)), 'endpoint-forbidden');
  return url;
}

// No redirects, pooling or implicit retry. Deadline covers the entire response.
export function postOnce(url, body, {apiKey, timeout_ms, maximum_response_bytes, signal}) {
  return new Promise((resolve, reject) => {
    let req, response, settled = false;
    const finish = (error, value) => {
      if (settled) return;
      settled = true; clearTimeout(timer); signal?.removeEventListener('abort', abort);
      if (error) { response?.destroy(); req?.destroy(); reject(error); } else resolve(value);
    };
    const fail = code => finish(new GlmError(code));
    const abort = () => fail('cancelled');
    const timer = setTimeout(() => fail('deadline-exceeded'), timeout_ms);
    signal?.addEventListener('abort', abort, {once: true});
    if (signal?.aborted) return abort();
    const headers = {'content-type': 'application/json', accept: 'application/json', 'content-length': Buffer.byteLength(body)};
    if (apiKey !== null) headers.authorization = `Bearer ${apiKey}`;
    try {
      req = (url.protocol === 'https:' ? httpsRequest : httpRequest)(url, {method: 'POST', agent: false, headers}, incoming => {
        response = incoming;
        incoming.on('error', () => fail('response-interrupted'));
        incoming.on('aborted', () => fail('response-interrupted'));
        if (!/^application\/json(?:;|$)/i.test(incoming.headers['content-type'] ?? '')) return fail('content-type-invalid');
        if (incoming.headers['content-encoding'] && incoming.headers['content-encoding'] !== 'identity') return fail('encoding-unsupported');
        const declared = incoming.headers['content-length'];
        if (declared !== undefined && (!/^\d+$/.test(declared) || Number(declared) > maximum_response_bytes)) return fail('response-too-large');
        const chunks = []; let size = 0;
        incoming.on('data', chunk => {
          size += chunk.length;
          if (size > maximum_response_bytes) return fail('response-too-large');
          if (!settled) chunks.push(chunk);
        });
        incoming.on('end', () => {
          if (settled) return;
          try {
            const payload = JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(Buffer.concat(chunks)));
            finish(null, {status: incoming.statusCode, payload, bytes: size});
          } catch { fail('response-json-invalid'); }
        });
      });
      req.on('error', () => fail('request-failed'));
      req.end(body);
    } catch { fail('request-failed'); }
  });
}

export function createGlmClient({api_key_ref, secret_registry,
  chat_endpoint = 'https://api.z.ai/api/paas/v4/chat/completions',
  tokenizer_endpoint = 'https://api.z.ai/api/paas/v4/tokenizer',
  maximum_output_tokens = 2048, maximum_requests = 12, timeout_ms = 30000,
  maximum_request_bytes = 131072, maximum_response_bytes = 262144,
  token_margin = 256, reasoning_effort = 'low', signal} = {}) {
  const chat = endpoint(chat_endpoint), tokenizer = endpoint(tokenizer_endpoint);
  need(chat.pathname.endsWith('/chat/completions') && tokenizer.pathname.endsWith('/tokenizer') && chat.origin === tokenizer.origin, 'endpoint-pair-invalid');
  for (const n of [maximum_output_tokens, maximum_requests, timeout_ms, maximum_request_bytes, maximum_response_bytes, token_margin]) need(integer(n) && n > 0, 'limits-invalid');
  need(maximum_output_tokens <= 2048 && maximum_requests <= 12 && timeout_ms <= 30000, 'limits-exceed-candidate');
  need(maximum_request_bytes <= 131072 && maximum_response_bytes <= 262144 && token_margin <= 4096, 'limits-exceed-candidate');
  need(['low', 'high', 'max'].includes(reasoning_effort), 'reasoning-effort-invalid');
  const authenticated = api_key_ref !== undefined || secret_registry !== undefined;
  need(chat.protocol === 'http:' || authenticated, 'credentials-required');
  need(!authenticated || (api_key_ref && typeof secret_registry?.consume === 'function'), 'credentials-incomplete');
  const reference = authenticated ? projectSecretReference(api_key_ref) : null;
  const identity = hash({version: 1, model: MODEL, chat: chat.href, tokenizer: tokenizer.href, maximum_output_tokens,
    maximum_requests, timeout_ms, maximum_request_bytes, maximum_response_bytes, token_margin, reasoning_effort, reference});
  const measurements = new Map();
  const receipts = [];
  let modelCalls = 0, tokenizerCalls = 0;
  async function send(url, object, kind) {
    need(!signal?.aborted, 'cancelled');
    const body = stable(object);
    need(Buffer.byteLength(body) <= maximum_request_bytes, 'request-too-large');
    let response, failure, sent = false, active = true;
    const started = Date.now();
    const controller = new AbortController();
    const abort = () => controller.abort();
    signal?.addEventListener('abort', abort, {once: true});
    const invoke = async material => {
      need(active && !sent, 'duplicate-credential-dispatch'); sent = true;
      try {
        response = await postOnce(url, body, {apiKey: material === null ? null : Buffer.from(material).toString('utf8'), timeout_ms, maximum_response_bytes, signal: controller.signal});
      } catch (error) { failure = error; }
    };
    try {
      if (authenticated) await secret_registry.consume({secret_ref: api_key_ref, consumer_id: 'glm-flash-transport', request_digest: hash(body), consumer: invoke});
      else await invoke(null);
    } catch { failure ??= new GlmError('secret-resolution-failed'); }
    finally { active = false; controller.abort(); signal?.removeEventListener('abort', abort); }
    const code = response?.payload?.error?.code ?? response?.payload?.code;
    const providerCode = /^\d{3,6}$/.test(String(code)) ? String(code) : null;
    const receipt = {kind, model: MODEL, request_sha256: hash(body), status: response?.status ?? null,
      latency_ms: Date.now() - started, response_bytes: response?.bytes ?? 0, provider_code: providerCode,
      dispatched: sent, automatic_retries: 0, redirects_followed: 0, authority_effect: 'none'};
    receipts.push(receipt);
    if (failure) throw new GlmError(failure instanceof GlmError ? failure.code : 'request-failed', receipt);
    need(response, 'response-missing');
    if (response.status !== 200) {
      const category = providerCode === '1113' ? 'billing-unavailable' : [401,403].includes(response.status) ? 'authentication-or-permission' : response.status === 429 ? 'rate-limited' : 'http-error';
      throw new GlmError(category, receipt);
    }
    return {payload: response.payload, receipt};
  }
  function bodyFor(prompt) {
    const value = JSON.parse(prompt);
    need(value && Array.isArray(value.messages) && value.messages.length > 0 && Array.isArray(value.tools), 'wire-input-invalid');
    need(Object.keys(value).every(k => ['messages','tools'].includes(k)), 'wire-input-invalid');
    return {...value, model: MODEL, stream: false, max_tokens: maximum_output_tokens,
      thinking: {type: 'enabled', clear_thinking: false}, reasoning_effort};
  }
  const transport = createStatelessRecyclingTransport({adapter_id: `glm-flash:${identity}`, source_ref: `glm-flash-v1:${identity}`, maximum_output_tokens,
    async measure_request({prompt}) {
      const body = bodyFor(prompt), key = hash(body);
      need(Buffer.byteLength(stable(body)) <= maximum_request_bytes, 'request-too-large');
      if (!measurements.has(key)) {
        need(tokenizerCalls < maximum_requests * 2, 'tokenizer-limit'); tokenizerCalls++;
        const {payload, receipt} = await send(tokenizer, {model: MODEL, messages: body.messages, tools: body.tools}, 'tokenizer');
        const count = payload?.usage?.prompt_tokens;
        need(integer(count), 'tokenizer-count-invalid');
        receipt.input_tokens = count;
        measurements.set(key, count + token_margin);
      }
      return measurements.get(key);
    },
    async request_once({prompt, dispatch}) {
      need(dispatch.sequence <= maximum_requests && modelCalls < maximum_requests, 'model-request-limit');
      const body = bodyFor(prompt), key = hash(body);
      need(measurements.get(key) === dispatch.input_upper_bound, 'measurement-binding-invalid');
      modelCalls++;
      const {payload, receipt} = await send(chat, body, 'model');
      need(payload?.model === MODEL, 'model-mismatch');
      need(Array.isArray(payload.choices) && payload.choices.length === 1, 'choice-invalid');
      const usage = payload.usage;
      need(integer(usage?.prompt_tokens) && integer(usage?.completion_tokens), 'usage-invalid');
      const reasoning = usage.completion_tokens_details?.reasoning_tokens ?? null;
      const cached = usage.prompt_tokens_details?.cached_tokens ?? null;
      need((reasoning === null || (integer(reasoning) && reasoning <= usage.completion_tokens)) && (cached === null || (integer(cached) && cached <= usage.prompt_tokens)), 'usage-details-invalid');
      Object.assign(receipt, {input_tokens: usage.prompt_tokens, output_tokens: usage.completion_tokens, reasoning_tokens: reasoning, cached_tokens: cached,
        reserved_input_tokens: dispatch.input_upper_bound, output_cap: maximum_output_tokens, finish_reason: payload.choices[0].finish_reason});
      need(usage.prompt_tokens <= dispatch.input_upper_bound, 'input-reservation-exceeded');
      need(usage.completion_tokens <= maximum_output_tokens, 'output-cap-exceeded');
      const {message, finish_reason} = payload.choices[0];
      need(message?.role === 'assistant' && !message.function_call, 'message-invalid');
      need(message.reasoning_content === undefined || typeof message.reasoning_content === 'string', 'reasoning-invalid');
      if (finish_reason === 'length') throw new GlmError('incomplete-output', receipt);
      need(['stop','tool_calls'].includes(finish_reason), 'finish-reason-unsupported');
      if (finish_reason === 'tool_calls') need(Array.isArray(message.tool_calls) && message.tool_calls.length > 0 && message.tool_calls.length <= 8, 'tool-calls-invalid');
      else need(!message.tool_calls && typeof message.content === 'string' && message.content.length > 0, 'final-text-invalid');
      return {final_bytes: stable({message, finish_reason}), receipt};
    }});
  return Object.freeze({transport, identity, maximum_requests, receipts, model: MODEL});
}
