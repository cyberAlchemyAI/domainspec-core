import {readFileSync} from "node:fs";
import {isAbsolute, resolve} from "node:path";
import {loadVerifiedDecisionProfile} from "../../request-decision-router/index.mjs";
import {loadSemanticInputProfile} from "../../semantic-input-runtime/index.mjs";
import {sha256HexText} from "../../intent-route-resolver/index.mjs";
import {fail, freezeResult, isRecord, nonEmptyString} from "./canonical.mjs";
import {materializeDefinitionCatalog, materializeOntologySnapshot} from "./source-adapters.mjs";

function absolute(repositoryRoot, path) {
  return isAbsolute(path) ? path : resolve(repositoryRoot, path);
}

function readBoundJson(repositoryRoot, binding) {
  if (!isRecord(binding) || !nonEmptyString(binding.path) || !nonEmptyString(binding.sha256)) {
    return fail("config", ["config.source-binding-invalid"]);
  }
  const path = absolute(repositoryRoot, binding.path);
  let text;
  try {
    text = readFileSync(path, "utf8");
  } catch {
    return fail("config", ["config.source-unreadable"], [{path: binding.path}]);
  }
  const actual = sha256HexText(text);
  if (actual !== binding.sha256) return fail("config", ["config.source-digest-drift"], [{path: binding.path, expected: binding.sha256, actual}]);
  try {
    return {ok: true, document: JSON.parse(text), path, sha256: actual};
  } catch {
    return fail("config", ["config.source-json-invalid"], [{path: binding.path}]);
  }
}

function readLiveJson(repositoryRoot, binding) {
  if (!isRecord(binding) || !nonEmptyString(binding.path)) return fail("config", ["config.source-binding-invalid"]);
  const path = absolute(repositoryRoot, binding.path);
  let text;
  try {
    text = readFileSync(path, "utf8");
  } catch {
    return fail("config", ["config.source-unreadable"], [{path: binding.path}]);
  }
  const actual = sha256HexText(text);
  try {
    return {ok: true, document: JSON.parse(text), path, source_identity: binding.path, source_digest: actual};
  } catch {
    return fail("config", ["config.source-json-invalid"], [{path: binding.path}]);
  }
}

function loadLiveContextSources(profile, repositoryRoot) {
  const sources = profile.sources ?? {};
  const decisionSource = readLiveJson(repositoryRoot, sources.decision_profile);
  if (!decisionSource.ok) return decisionSource;
  const decisionProfile = loadVerifiedDecisionProfile(decisionSource.path, repositoryRoot);
  if (!decisionProfile.ok) return fail("config", decisionProfile.reason_codes ?? ["config.decision-profile-unverified"]);
  const definitionSources = [];
  const sourceSnapshot = [{source_identity: sources.decision_profile.path, source_digest: decisionSource.source_digest}];
  for (const binding of Array.isArray(sources.definition_sources) ? sources.definition_sources : []) {
    const loaded = readLiveJson(repositoryRoot, binding);
    if (!loaded.ok) return loaded;
    definitionSources.push({document: loaded.document, source_identity: loaded.source_identity, source_digest: loaded.source_digest});
    sourceSnapshot.push({source_identity: loaded.source_identity, source_digest: loaded.source_digest});
  }
  const catalog = materializeDefinitionCatalog({sources: definitionSources});
  if (!catalog.ok) return catalog;
  const ontologySource = readLiveJson(repositoryRoot, sources.system_ontology);
  if (!ontologySource.ok) return ontologySource;
  sourceSnapshot.push({source_identity: ontologySource.source_identity, source_digest: ontologySource.source_digest});
  const snapshot = materializeOntologySnapshot({
    document: ontologySource.document,
    source_identity: ontologySource.source_identity,
    source_digest: ontologySource.source_digest,
    required_edge_ids_by_node: profile.context?.required_edge_ids_by_node,
  });
  if (!snapshot.ok) return snapshot;
  sourceSnapshot.sort((a, b) => a.source_identity.localeCompare(b.source_identity));
  return {
    ok: true,
    decision_profile: decisionProfile.value,
    definition_catalog: catalog.value,
    ontology_snapshot: snapshot.value,
    source_snapshot: freezeResult(sourceSnapshot),
    authority_effect: "none",
  };
}

function probeLiveContextSignature(profile, repositoryRoot) {
  const sources = profile.sources ?? {};
  const bindings = [sources.decision_profile, ...(sources.definition_sources ?? []), sources.system_ontology];
  const entries = [];
  for (const binding of bindings) {
    if (!isRecord(binding) || !nonEmptyString(binding.path)) return fail("config", ["config.source-binding-invalid"]);
    let text;
    try {
      text = readFileSync(absolute(repositoryRoot, binding.path), "utf8");
    } catch {
      return fail("config", ["config.source-unreadable"], [{path: binding.path}]);
    }
    entries.push({source_identity: binding.path, source_digest: sha256HexText(text)});
  }
  entries.sort((a, b) => a.source_identity.localeCompare(b.source_identity));
  return {ok: true, signature: sha256HexText(JSON.stringify(entries)), entries};
}

function createLiveContextSourceProvider(profile, repositoryRoot, initialLive) {
  let cached = initialLive;
  let probe = probeLiveContextSignature(profile, repositoryRoot);
  let signature = probe.ok ? probe.signature : null;
  return () => {
    probe = probeLiveContextSignature(profile, repositoryRoot);
    if (!probe.ok) return probe;
    if (cached?.ok && probe.signature === signature) return cached;
    const refreshed = loadLiveContextSources(profile, repositoryRoot);
    if (!refreshed.ok) return refreshed;
    cached = refreshed;
    signature = probe.signature;
    return cached;
  };
}

export function loadRepositoryProfile(profilePath, repositoryRoot) {
  let profile;
  try {
    profile = JSON.parse(readFileSync(profilePath, "utf8"));
  } catch {
    return fail("config", ["config.profile-unreadable"]);
  }
  if (!isRecord(profile) || !["are.codex-wrapper-repository-profile/v1", "are.codex-wrapper-repository-profile/v2", "are.codex-wrapper-repository-profile/v3", "are.codex-wrapper-repository-profile/v4"].includes(profile.schema_version)) {
    return fail("config", ["config.profile-version-unsupported"]);
  }
  const sources = profile.sources ?? {};
  let live;
  if (["are.codex-wrapper-repository-profile/v2", "are.codex-wrapper-repository-profile/v3", "are.codex-wrapper-repository-profile/v4"].includes(profile.schema_version)) {
    live = loadLiveContextSources(profile, repositoryRoot);
  } else {
    const decisionProfileBinding = readBoundJson(repositoryRoot, sources.decision_profile);
    if (!decisionProfileBinding.ok) return decisionProfileBinding;
    const decisionProfile = loadVerifiedDecisionProfile(decisionProfileBinding.path, repositoryRoot);
    if (!decisionProfile.ok) return fail("config", decisionProfile.reason_codes ?? ["config.decision-profile-unverified"]);
    const definitionSources = [];
    for (const binding of Array.isArray(sources.definition_sources) ? sources.definition_sources : []) {
      const loaded = readBoundJson(repositoryRoot, binding);
      if (!loaded.ok) return loaded;
      definitionSources.push({document: loaded.document, source_identity: binding.path, source_digest: loaded.sha256});
    }
    const catalog = materializeDefinitionCatalog({sources: definitionSources});
    if (!catalog.ok) return catalog;
    const ontologySource = readBoundJson(repositoryRoot, sources.system_ontology);
    if (!ontologySource.ok) return ontologySource;
    const snapshot = materializeOntologySnapshot({document: ontologySource.document, source_identity: sources.system_ontology.path, source_digest: ontologySource.sha256, required_edge_ids_by_node: profile.context?.required_edge_ids_by_node});
    if (!snapshot.ok) return snapshot;
    live = {ok: true, decision_profile: decisionProfile.value, definition_catalog: catalog.value, ontology_snapshot: snapshot.value, source_snapshot: freezeResult([]), authority_effect: "none"};
  }
  if (!live.ok) return live;

  for (const bindingName of ["interface", "protocol_observation", "continuation_selection", "context_basis_receipt"]) {
    const loaded = readBoundJson(repositoryRoot, sources[bindingName]);
    if (!loaded.ok) return loaded;
  }

  const semanticEvaluation = isRecord(profile.semantic_evaluation)
    ? profile.semantic_evaluation
    : {enabled: false, trigger: "turn/completed"};
  if (semanticEvaluation.enabled !== true && semanticEvaluation.enabled !== false) return fail("config", ["config.semantic-enabled-invalid"]);
  if (semanticEvaluation.trigger !== "turn/completed") return fail("config", ["config.semantic-trigger-unsupported"]);
  const runtimeJournal = isRecord(profile.runtime_journal)
    ? profile.runtime_journal
    : {journal_id: `are-codex-runtime:${profile.profile_id}`, max_events: 4096, max_closed_turns: 256};
  if (!nonEmptyString(runtimeJournal.journal_id)) return fail("config", ["config.runtime-journal-id-invalid"]);
  for (const field of ["max_events", "max_closed_turns"]) {
    if (!Number.isSafeInteger(runtimeJournal[field]) || runtimeJournal[field] < 0) {
      return fail("config", [`config.runtime-journal-${field.replaceAll("_", "-")}-invalid`]);
    }
  }
  const reasoningState = isRecord(profile.reasoning_state)
    ? profile.reasoning_state
    : {ledger_id: `are-reasoning-state:${profile.profile_id}`, storage_mode: "process-memory"};
  if (!nonEmptyString(reasoningState.ledger_id)) return fail("config", ["config.reasoning-state-ledger-id-invalid"]);
  if (!["process-memory", "append-only-file-fsync"].includes(reasoningState.storage_mode)) return fail("config", ["config.reasoning-state-storage-mode-invalid"]);
  if (reasoningState.storage_mode === "append-only-file-fsync" && !nonEmptyString(reasoningState.log_path)) return fail("config", ["config.reasoning-state-log-path-required"]);
  const gateway = isRecord(profile.gateway) ? profile.gateway : {
    backend_mode: "direct-stdio",
    max_clients: 8,
    max_buffered_messages_per_client: 256,
    reconnect: true,
    allowed_clients: [
      {consumer_id: "codex:human-chat", lane: "interaction-bound"},
      {consumer_id: "codex:plan", lane: "plan-bound", window_ref: "plan:persistent-codex", request_id: "request:persistent-codex-plan"},
    ],
  };
  if (!["direct-stdio", "daemon-proxy", "websocket"].includes(gateway.backend_mode)) return fail("config", ["config.gateway-backend-invalid"]);
  for (const field of ["max_clients", "max_buffered_messages_per_client"]) {
    if (!Number.isSafeInteger(gateway[field]) || gateway[field] < 1) return fail("config", [`config.gateway-${field.replaceAll("_", "-")}-invalid`]);
  }
  if (gateway.reconnect !== true && gateway.reconnect !== false) return fail("config", ["config.gateway-reconnect-invalid"]);
  if (!Array.isArray(gateway.allowed_clients) || gateway.allowed_clients.length === 0) return fail("config", ["config.gateway-clients-required"]);
  const gatewayClients = [];
  const gatewayConsumerIds = new Set();
  for (const client of gateway.allowed_clients) {
    if (!isRecord(client) || !nonEmptyString(client.consumer_id) || !["plan-bound", "interaction-bound"].includes(client.lane) || gatewayConsumerIds.has(client.consumer_id) || (client.lane === "plan-bound" && (!nonEmptyString(client.window_ref) || !nonEmptyString(client.request_id)))) {
      return fail("config", ["config.gateway-client-invalid"]);
    }
    gatewayConsumerIds.add(client.consumer_id);
    gatewayClients.push({consumer_id: client.consumer_id, lane: client.lane, window_ref: client.lane === "plan-bound" ? client.window_ref : null, request_id: client.lane === "plan-bound" ? client.request_id : null});
  }
  let semanticProfile = null;
  if (semanticEvaluation.enabled === true) {
    const semanticProfileSource = readBoundJson(repositoryRoot, sources.semantic_input_profile);
    if (!semanticProfileSource.ok) return semanticProfileSource;
    const loadedSemanticProfile = loadSemanticInputProfile(semanticProfileSource.path, repositoryRoot);
    if (!loadedSemanticProfile.ok) return fail("config", loadedSemanticProfile.reason_codes ?? ["config.semantic-profile-unverified"], loadedSemanticProfile.residue ?? []);
    semanticProfile = loadedSemanticProfile.value;
  }

  return {
    ok: true,
    value: freezeResult({
      schema_version: "are.codex-wrapper-loaded-profile/v4",
      profile_id: profile.profile_id,
      protocol_binding: profile.protocol_binding,
      context: profile.context,
      turn_bindings: profile.turn_bindings,
      effect_defaults: profile.effect_defaults,
      context_projection: profile.context_projection ?? {max_inline_bytes: 32768},
      semantic_evaluation: freezeResult({enabled: semanticEvaluation.enabled, trigger: semanticEvaluation.trigger}),
      runtime_journal: freezeResult({
        journal_id: runtimeJournal.journal_id,
        max_events: runtimeJournal.max_events,
        max_closed_turns: runtimeJournal.max_closed_turns,
      }),
      reasoning_state: freezeResult({
        ledger_id: reasoningState.ledger_id.trim(),
        storage_mode: reasoningState.storage_mode,
        log_path: nonEmptyString(reasoningState.log_path) ? absolute(repositoryRoot, reasoningState.log_path) : null,
        checkpoints: freezeResult({before_model_request: true, before_effect: true, before_continuation: true}),
      }),
      gateway: freezeResult({
        backend_mode: gateway.backend_mode,
        max_clients: gateway.max_clients,
        max_buffered_messages_per_client: gateway.max_buffered_messages_per_client,
        reconnect: gateway.reconnect,
        allowed_clients: gatewayClients.sort((a, b) => a.consumer_id.localeCompare(b.consumer_id)),
      }),
      authority_effect: "none",
    }),
    decision_profile: live.decision_profile,
    definition_catalog: live.definition_catalog,
    ontology_snapshot: live.ontology_snapshot,
    source_snapshot: live.source_snapshot,
    context_source_provider: createLiveContextSourceProvider(profile, repositoryRoot, live),
    semantic_profile: semanticProfile,
  };
}
