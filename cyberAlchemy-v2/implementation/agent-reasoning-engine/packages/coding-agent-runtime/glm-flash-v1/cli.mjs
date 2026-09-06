import {readFileSync, writeFileSync, realpathSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createSecretProviderRegistry, createSecretReference} from '../secret-provider.mjs';
import {createSopsAgeProcessSecretProvider} from '../sops-age-secret-provider.mjs';
import {createReadOnlyToolRuntime} from '../read-only-tools.mjs';
import {createGlmClient, MODEL, need} from './transport.mjs';
import {runGlmAgent} from './agent.mjs';

export function parseConfig(value) {
  const keys = ['schema_version','model','credential','run_id','request','fixture_root','state_directory','observation_allowlist','mutation_allowlist','context_limit','recycle_at','safety_margin'];
  need(value && typeof value === 'object' && !Array.isArray(value) && Object.keys(value).every(k => keys.includes(k)), 'config-fields-invalid');
  need(value.schema_version === 'are.glm-flash-config/v1' && value.model === MODEL, 'config-model-invalid');
  const credential = value.credential;
  need(credential && typeof credential === 'object' && Object.keys(credential).every(k => ['provider_kind','provider_id','locator'].includes(k)), 'credential-config-invalid');
  need(credential.provider_kind === 'local-sops-age' && credential.provider_id === 'local-model-secrets' && credential.locator === 'model/zai-key', 'credential-config-invalid');
  for (const key of ['run_id','request','fixture_root','state_directory']) need(typeof value[key] === 'string' && value[key].length > 0 && !value[key].includes('\0'), 'config-string-invalid');
  for (const key of ['observation_allowlist','mutation_allowlist']) need(Array.isArray(value[key]) && value[key].length > 0 && value[key].every(p => typeof p === 'string' && p.length > 0), 'config-allowlist-invalid');
  need(value.mutation_allowlist.every(p => value.observation_allowlist.includes(p)), 'mutation-not-observable');
  for (const key of ['context_limit','recycle_at','safety_margin']) need(Number.isSafeInteger(value[key]) && value[key] > 0, 'config-budget-invalid');
  // Deliberately far below the advertised model window until long-context conformance.
  need(value.context_limit <= 32768 && value.recycle_at <= value.context_limit - value.safety_margin && value.recycle_at > 2048, 'config-budget-invalid');
  return structuredClone(value);
}

export async function runConfiguredGlm(config) {
  const c = parseConfig(config);
  const root = realpathSync(c.fixture_root);
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 600000);
  const provider = createSopsAgeProcessSecretProvider({provider_id: c.credential.provider_id});
  const registry = createSecretProviderRegistry({providers: [provider]});
  const reference = createSecretReference({provider_id: c.credential.provider_id, locator: c.credential.locator});
  const client = createGlmClient({api_key_ref: reference, secret_registry: registry, signal: controller.signal});
  const tools = createReadOnlyToolRuntime({repository_root: root, observation_allowlist: c.observation_allowlist, maximum_result_bytes: 12000});
  try {
    return await runGlmAgent({run_id: c.run_id, request: c.request, fixture_root: root, client,
      observation_allowlist: c.observation_allowlist, mutation_allowlist: c.mutation_allowlist,
      verification_command: [], tool_runtime: tools, tool_policy: {allow: [...tools.tool_names,'read-context-evidence']}, signal: controller.signal,
      context_recycling: {directory: resolve(c.state_directory), context_limit: c.context_limit, recycle_at: c.recycle_at, safety_margin: c.safety_margin,
        state: {objective: c.request, constraints: ['Propose only; preserve test files.'], completed: [], pending: [c.request], facts: [], lessons: [], evidence_refs: [`run:${c.run_id}`]}}});
  } finally { clearTimeout(timer); }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    need(process.argv.length === 4, 'usage-config-output-required');
    // Reserve output before making paid calls; never overwrite an existing result.
    const {openSync, closeSync} = await import('node:fs');
    const fd = openSync(resolve(process.argv[3]), 'wx', 0o600);
    try {
      const result = await runConfiguredGlm(JSON.parse(readFileSync(resolve(process.argv[2]), 'utf8')));
      writeFileSync(fd, JSON.stringify(result, null, 2) + '\n');
      console.log(JSON.stringify({status: result.status, model: MODEL, output: resolve(process.argv[3]), reasons: result.reason_codes ?? []}));
      process.exitCode = result.status === 'AWAITING_APPROVAL' ? 0 : 1;
    } finally { closeSync(fd); }
  } catch { console.error('GLM runner failed; check configuration and private output destination.'); process.exitCode = 1; }
}
