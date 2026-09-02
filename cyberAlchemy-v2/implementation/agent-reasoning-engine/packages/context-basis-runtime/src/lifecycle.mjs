import {canonicalizeJson, deepFreeze, digestValue, fail, isRecord} from "./canonical.mjs";
import {composeContextBasis} from "./compose.mjs";
import {bindContextWindowView} from "./context-window-view.mjs";
import {assembleContextEnvelope} from "./context-envelope.mjs";
import {assessContextRefresh} from "./context-refresh.mjs";

const SCHEMA_VERSION = "are.context-lifecycle-composition/v1";

function withView(composition, view) {
  const value = canonicalizeJson({...composition.value, context_window_view: view});
  return deepFreeze({schema_version: composition.schema_version, ok: true, value, digest: digestValue(value), authority_effect: "none"});
}

export function composeContextLifecycle(input) {
  if (!isRecord(input)) return fail("context-lifecycle", ["lifecycle.input-required"]);
  const viewInput = isRecord(input.view) ? input.view : {};
  let composition = composeContextBasis({...input, view: {...viewInput, reuse_predicate: null}});
  if (!composition.ok) return deepFreeze({schema_version: SCHEMA_VERSION, ok: false, stage: "context-basis", composition, authority_effect: "none"});
  const refresh = assessContextRefresh(input.previous_envelope ?? null, composition, input.current_sources ?? []);
  if (!refresh.ok) return deepFreeze({schema_version: SCHEMA_VERSION, ok: false, stage: "context-refresh", composition, refresh_assessment: refresh, authority_effect: "none"});

  if (viewInput.lane === "plan-bound" && refresh.value.reuse_allowed === true && isRecord(viewInput.predecessor_view)) {
    const basis = composition.value.necessary_context_basis;
    const rebound = bindContextWindowView({...viewInput, basis: basis.value, basis_digest: basis.digest, reuse_predicate: {equal: true, current: true, digest: refresh.digest}});
    if (!rebound.ok) return deepFreeze({schema_version: SCHEMA_VERSION, ok: false, stage: "context-window-view", composition, refresh_assessment: refresh, authority_effect: "none"});
    composition = withView(composition, rebound);
  }

  const freshnessState = refresh.value.disposition === "reuse-current" ? "current-reused" : "successor-current";
  const envelope = assembleContextEnvelope(composition, {...(input.projection_policy ?? {}), current_sources: input.current_sources ?? [], freshness_state: freshnessState});
  if (!envelope.ok) return deepFreeze({schema_version: SCHEMA_VERSION, ok: false, stage: "context-envelope", composition, refresh_assessment: refresh, context_envelope: envelope, authority_effect: "none"});
  const value = {schema_version: SCHEMA_VERSION, composition, refresh_assessment: refresh, context_envelope: envelope, authority_effect: "none"};
  const digest = digestValue({composition_digest: composition.digest, refresh_digest: refresh.digest, context_envelope_digest: envelope.digest});
  return deepFreeze({schema_version: SCHEMA_VERSION, ok: true, value, digest, authority_effect: "none"});
}
