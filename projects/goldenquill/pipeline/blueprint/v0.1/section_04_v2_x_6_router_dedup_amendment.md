---
title: Blueprint §4 Logician — Amendment v2.x.6 (OD-5 full router dedup — `_enforce_cloud_boundary_pre/post` retirement)
filed: 2026-05-16
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-16T16:30:00Z at lock_history row 234 (sibling 1/2; §0.5 v28 sibling 2/2 at row 235). Operator-Ed25519 signature verified against pinned cards-publisher pubkey `0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd` at `vault_shared/cards/publisher_pubkey.signed.yaml`. Canonical SHA3-512 of amendment file = `12cabb58d64b3079…a17e29836f368f2d`. Ed25519 signature prefix = `3efbac425e70a195…845cf16d132a4b0f`. L-005 strict two-cycle CLOSED with FULL live cross-family rigor. Eighteenth substantive v0.1+v0.2 round to LOCK. Companion runtime code landing dispatches separately per LOCK_signoff.md.
parent_lock: pipeline/blueprint/v0.1/section_04_v2_x_5_provider_boundary_amendment.md  (§4 v2.x.5 LOCKED 2026-05-16 row 232)
parent_lock_row: 232
predecessor_disposition: §4 v2.x.5 runtime companion landed 2026-05-16 (daily_log entry) executed OD-5 PARTIALLY — `_http_post` rewired to delegate to `_CANONICAL_STDLIB_URLOPEN_CALLER` via `_INSIDE_WRAPPER` thread-local, but `_enforce_cloud_boundary_pre/post` left in place "compose into the wrapper at the next router refactor; documentary deletion path lands at v0.2 horizon."
amendment_class: narrow-corrective — closes the OD-5 PARTIAL gap by retiring the router-side parallel gate implementation in favor of single-source-of-truth via the existing `pipeline.orchestrator.provider_boundary.enforce_outbound_boundary` wrapper.
precedent_pattern: §4 v2.x.1 narrow-corrective (lock_history row 198) — both extend an already-LOCKed amendment with corrective work without modifying the parent text in-place.
threat_severity_at_v0_1_v0_2: LOW — bounded by v7 LOCKED A1+A4 (single-client + operator-trusted preflight). The parallel-implementation drift risk is contributor-discipline-shaped, not adversarial under the single-operator Beta deployment threat model. Promotion to MED would require multi-contributor or v2 multi-tenant context. The current dual gate-firing paths produce architecturally-equivalent behavior; this amendment eliminates the dual-implementation drift surface.
purpose: Replace router-side `_enforce_cloud_boundary_pre` + `_enforce_cloud_boundary_post` with a router-layer adapter that constructs `enforce_outbound_boundary(stdlib_urlopen_caller, ...)` per dispatch and threads the wrapped callable down to the provider call functions. Eliminates parallel-implementation drift; preserves all existing F-CLASS-* gate firing through the wrapper's PRE/POST chain.
companion_code_to_land_at_lock:
  - "pipeline/orchestrator/router.py (UPDATED — _enforce_cloud_boundary_pre + _enforce_cloud_boundary_post DELETED; _dispatch_with_classification_boundary refactored to construct an OutboundCallable via enforce_outbound_boundary wrapping _CANONICAL_STDLIB_URLOPEN_CALLER, pass it as http_post= down to _call_anthropic / _call_openai_style; _call_anthropic and _call_openai_style updated to accept http_post: OutboundCallable parameter; OutboundBoundaryRefusedError → ClassificationBoundaryError translation in fallback branch; new module-level _load_router_posture_and_register helper for posture + signed-register injection)"
  - "tests/orchestrator/test_router_classification_boundary.py (UPDATED — exception-class assertions migrated to catch OutboundBoundaryRefusedError where the wrapper raises; ClassificationBoundaryError preserved for translation-layer cases; new test cases for posture mid-cycle change + signed-register absence; existing single-gate test surface preserved byte-for-byte by translation layer)"
done_definition:
  - "`grep -rn '_enforce_cloud_boundary_pre\\|_enforce_cloud_boundary_post' pipeline/orchestrator/router.py` returns zero matches (post-deletion grep-verify at LOCK ceremony)."
  - "`_dispatch_with_classification_boundary` body invokes `enforce_outbound_boundary` exactly once per dispatch entry; no router-side F-CLASS gate calls outside the wrapper construction."
  - "`tests/orchestrator/test_router_classification_boundary.py` 100% PASS at Cycle 2 close (count preserved at current state); exception-class assertions updated to accept either OutboundBoundaryRefusedError or its ClassificationBoundaryError translation layer."
  - "Full `scripts/run_tests.sh tests/orchestrator/` PASS at Cycle 2 close."
  - "`scripts/run_lint.sh pipeline` exit 0."
  - "RT-17 (Cycle-1 prior Red Team probe) single-source-of-truth discipline: the wrapper is the SOLE site where F-CLASS PRE/POST gates fire on the router-level cloud dispatch path; no double-gate firing."
  - "Daily-log entry + session-metrics row written at session close."
ws_dispatch: §4 v2.x.6 OD-5-closure dispatch (Cowork session 2026-05-16 post-fixture-migration; Thesis round modeled on §4 v2.x.5 cadence).
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment v2.x.6 — OD-5 full router dedup

## §0. Amendment intent + scope

This narrow-corrective amendment closes the OD-5 PARTIAL gap surfaced by the §4 v2.x.5 runtime companion landing (2026-05-16 daily_log). The §4 v2.x.5 LOCKed amendment §7 specified OD-5: *"Refactor `router._dispatch_with_classification_boundary` to call `enforce_outbound_boundary` directly. Single source of truth; eliminates parallel-implementation drift risk."* The runtime companion executed PARTIALLY:

- **DONE** — `_http_post` rewired to delegate to `_CANONICAL_STDLIB_URLOPEN_CALLER` via the `_INSIDE_WRAPPER` thread-local (commit / runtime companion daily_log entry).
- **NOT DONE** — `_enforce_cloud_boundary_pre` (router.py:507+) and `_enforce_cloud_boundary_post` (router.py:566+) remain. `_dispatch_with_classification_boundary` calls them at the dispatch entry. This is parallel-implementation with the wrapper's `_enforce_pre` / `_enforce_post` (provider_boundary.py:422+ / :510+).

The current state IS architecturally sound at v7 A1+A4: both gate-firing paths invoke the same underlying F-CLASS-* gate functions (`check_class_routing_indeterminate` / `check_class_slot_id_non_opaque` / `check_class_cloud_received_confidential` / `check_class_high_stakes_flag_leak` / `check_class_cloud_received_opaque_slot_filled`). The sovereignty claim holds for both paths. This amendment eliminates the **drift risk** — if a future amendment adds a new F-CLASS gate, contributor-discipline could land it in one path but not the other.

**What this amendment lands.** Three concrete changes at the router layer:

1. **DELETE** `_enforce_cloud_boundary_pre` + `_enforce_cloud_boundary_post` from `pipeline/orchestrator/router.py` (L465-583 inclusive of the DEFERRED-OD-5 docstring block landed by the prior session — that block becomes vestigial once the functions are deleted).
2. **REFACTOR** `_dispatch_with_classification_boundary` to construct an `OutboundCallable` wrapped via `enforce_outbound_boundary(stdlib_urlopen_caller, classification_context=..., posture=..., operator_signed_register=...)` once per dispatch entry, and thread that wrapped callable down to `_call_anthropic` / `_call_openai_style` as an `http_post: OutboundCallable` parameter.
3. **ADAPT** `_call_anthropic` and `_call_openai_style` to accept `http_post: OutboundCallable` (replacing their internal direct call to `_http_post`). The dict↔bytes adapter at the router-level encode/decode boundary preserves the existing public surface of `call_seat`.

**What this amendment does NOT change.**

- **No new F-CLASS-* failure codes.** The wrapper already raises the same F-CLASS-* codes (and their sub-tag extensions per §4 v2.x.5) as the router's gates would. Family roster stays at 16 primitives.
- **No new AST-lint rules.** R-NO-DIRECT-PROVIDER-HTTP already covers the router file via the allowlist (provider_boundary.py is the sole permitted urllib site; router's `_http_post` delegates to that site).
- **No public-surface change to `call_seat`.** Operator-facing API stays at `call_seat(seat_name, messages, system, tier, classification_context)`. Posture + signed_register are loaded internally by the router from existing modules (`pipeline.orchestrator.deployment_posture.get_current_posture` + `pipeline.vault.classification.signed_register_loader.load_signed_register`).
- **No substrate addition.** All required modules already exist on disk from §4 v2.x.5 runtime companion.

## §1. Target glob + scope discipline

Target glob: `pipeline/orchestrator/router.py` — specifically the L465-583 region containing `_enforce_cloud_boundary_pre` + `_enforce_cloud_boundary_post` + the current body of `_dispatch_with_classification_boundary` + the DEFERRED-OD-5 block comment that the prior session landed.

The rewrite scope also touches `_call_anthropic` + `_call_openai_style` (at the same router file) to accept the `http_post` parameter. No other modules are modified.

Test surface scope: `tests/orchestrator/test_router_classification_boundary.py` — exception-class assertions migrate to catch either `OutboundBoundaryRefusedError` (raised directly by the wrapper) or `ClassificationBoundaryError` (raised by the translation layer in the fallback branch). The existing test cases for PRE-gate routing-indeterminate, confidential-input-blocking, high-stakes-flag-leak, opaque-slot-id, and post-gate drift detection are preserved byte-for-byte at the assertion-shape level — only the exception class checks change.

## §2. Refactor — `_dispatch_with_classification_boundary` (canonical post-LOCK shape)

```python
def _dispatch_with_classification_boundary(
    *,
    provider_name: str,
    provider_cfg: dict,
    seat_cfg: dict,
    messages: list[dict],
    system: str | None,
    classification_context: ClassificationContext | None,
) -> dict:
    if not _is_cloud_provider(provider_name, provider_cfg):
        # Local providers do not need the wrapper; direct dispatch preserves
        # bytes-overhead avoidance for the local-fast-path. The wrapper's
        # gates fail-close on missing classification_context for cloud, so
        # this branch is the only path that bypasses gate firing — and only
        # for local providers, which are explicitly out-of-scope for cloud-
        # egress F-CLASS gates by v7.0.10 §1.
        return _dispatch(provider_cfg, seat_cfg, messages, system)

    if classification_context is None:
        # Cloud provider + no classification_context → fail-closed per v7.0.7
        # Section 4 (same predicate as F-CLASS-ROUTING-INDETERMINATE). The
        # wrapper would also raise here; raising at the router layer keeps
        # the existing public-surface exception contract identical to
        # pre-amendment behavior.
        raise ClassificationBoundaryError(
            F_CLASS_ROUTING_INDETERMINATE,
            "cloud provider requested without classification_context; fail-closed "
            "LOCAL per v7.0.7",
        )

    # Construct the OutboundCallable wrapper once per dispatch. The wrapper
    # encapsulates the F-CLASS PRE-gate chain (routing-indeterminate, slot-id,
    # confidential-input, high-stakes-flag-leak, raw-bytes register scan) and
    # POST-gate chain (confidential drift, opaque-slot drift, high-stakes
    # flag leak in response) per provider_boundary.py:_enforce_pre/_enforce_post.
    posture = get_current_posture()  # pipeline.orchestrator.deployment_posture
    signed_register = load_signed_register()  # may return None at test/dev posture
    pb_classification_context = _coerce_to_provider_boundary_context(
        classification_context
    )
    wrapped_caller = enforce_outbound_boundary(
        _CANONICAL_STDLIB_URLOPEN_CALLER,
        classification_context=pb_classification_context,
        posture=posture,
        operator_signed_register=signed_register,
    )

    # Dispatch with the wrapped caller. _call_anthropic + _call_openai_style
    # accept http_post: OutboundCallable per OD-5 refactor; they encode their
    # provider-specific dict body to bytes once before invocation, decode the
    # response bytes once after, and return the same dict shape as before.
    try:
        return _dispatch(
            provider_cfg, seat_cfg, messages, system, http_post=wrapped_caller
        )
    except OutboundBoundaryRefusedError as e:
        # Translation layer — preserves the existing public exception
        # contract. call_seat's fallback branch catches
        # ClassificationBoundaryError; this re-raise keeps that handler
        # contract intact.
        raise ClassificationBoundaryError(e.failure_code, e.detail) from e
    # Cycle-1 Red Team RT-02 fold-in — explicit narrow translation. Other
    # wrapper-origin exceptions (transport / timeout / runtime integrity) are
    # NOT translated to ClassificationBoundaryError. They propagate as-is and
    # are caught by call_seat's generic `except Exception as primary_err`
    # handler at router.py:747 (existing behavior). This preserves the
    # semantic distinction: ClassificationBoundaryError = fail-closed-by-policy
    # (audited, fallback eligible); transport/timeout = transient failure
    # (also fallback eligible). The wrapper does not currently raise any
    # exception class outside this two-bucket dichotomy; if it grows to do so,
    # the v2.x.7 follow-on amendment extends the translation layer to handle
    # the new shape.
```

## §3. Refactor — `_call_anthropic` + `_call_openai_style` required `http_post` parameter

Per ratified OD-3 (no legacy direct-call branch; required `http_post` parameter), both functions accept `http_post: OutboundCallable` as a REQUIRED keyword-only argument. No `Optional[None]` default. No legacy branch. Runtime assertion at body entry hardens against dynamic-call bypass per Cycle-1 Red Team RT-06 fold-in:

```python
def _call_anthropic(
    provider_cfg: dict,
    seat_cfg: dict,
    messages: list[dict],
    system: str | None,
    *,
    http_post: OutboundCallable,  # REQUIRED — OD-3 ratified
) -> dict:
    # RT-06 fold-in — runtime defense against dynamic-call bypass.
    # Static AST-lint catches `_call_anthropic(...)` shape; this guard catches
    # `getattr(router, '_call_anthropic')(...)` / `from router import _call_anthropic
    # as x; x(...)` / `importlib.import_module(...).module._call_anthropic(...)`
    # call shapes that the lint rule cannot detect statically.
    if http_post is None:  # defense-in-depth — signature already requires
        raise ClassificationBoundaryError(
            F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
            "_call_anthropic invoked without http_post wrapper (direct-call "
            "bypass detected at runtime); fail-closed per OD-3 + RT-06.",
        )
    # ... existing header + body construction ...
    # RT-07 fold-in — pin canonical JSON encoder settings so wrapper PRE-scan
    # operates on byte-equivalent input to what gets POST'd. Standardize
    # ensure_ascii=False + separators=(',', ':') across the stack.
    body_bytes = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    status, response_bytes = http_post(
        url=full_url,
        headers=headers,
        body=body_bytes,
        timeout_seconds=timeout,
    )
    response_text = response_bytes.decode("utf-8", errors="replace")
    return _parse_anthropic_response(status, response_text)
```

(Same shape for `_call_openai_style`.)

**Legacy direct-HTTP branch DELETED.** No `if http_post is None: return _legacy_http_post_dispatch(...)` fallback. The wrapper is the SOLE HTTP egress path for cloud providers via these functions. Production code OR test code that calls `_call_anthropic` / `_call_openai_style` directly MUST provide an `http_post=` argument; AST-lint sub-tag `R-NO-DIRECT-PROVIDER-HTTP.direct_provider_call_without_wrapper` catches static call shapes; the runtime assertion above catches dynamic-call shapes per RT-06.

## §4. Exception-class translation

The wrapper raises `OutboundBoundaryRefusedError` (defined at `provider_boundary.py:283`). The router's existing public exception contract is `ClassificationBoundaryError`. To preserve the `call_seat` fallback-branch behavior (router.py:722-746) without forcing every caller to learn a new exception class, the refactor catches `OutboundBoundaryRefusedError` at `_dispatch_with_classification_boundary` and re-raises as `ClassificationBoundaryError` with the same `failure_code` + `detail`.

This translation is one-way (wrapper → router). `OutboundBoundaryRefusedError` is NOT made a subclass of `ClassificationBoundaryError` (which would require modifying provider_boundary.py — LOCKed canonical state per §4 v2.x.5).

## §5. RT-17 single-source-of-truth discipline

The §4 v2.x.5 Cycle-1 Red Team probe RT-17 named *"Double-gate firing — wrapper performs PRE-gate, then the router (post-wrap) also runs its own POST-gate"* as a LOW reliability risk. This amendment closes that risk: after the rewrite, the wrapper is the SOLE site where F-CLASS PRE/POST gates fire on the router-level cloud dispatch path. The router-side `_enforce_cloud_boundary_pre/post` are GONE.

Grep-verify at LOCK ceremony:

```bash
grep -rn '_enforce_cloud_boundary_pre\|_enforce_cloud_boundary_post' pipeline/orchestrator/router.py
# expected: zero matches
```

## §6. Posture + signed-register injection

The wrapper requires `posture: str` and `operator_signed_register: Mapping[str, Any] | None`. The router obtains these from existing v7.0.7 / v7.0.10 infrastructure:

- **Posture:** `pipeline.orchestrator.deployment_posture.get_current_posture()` — landed at §4 v2.x.5 runtime companion as a process-shared atomic container (RT-C2-07 fold-in). Returns the operator-signed deployment manifest's posture value, validated at process startup. Mid-cycle posture mutation is fail-closed by the wrapper per `F-CLASS-POSTURE-MID-CYCLE-CHANGE`.
- **Signed register:** `pipeline.vault.classification.signed_register_loader.load_signed_register()` — landed at §4 v2.x.5 runtime companion as RT-C2-01 fold-in. Returns the Ed25519-verified classification register payload, or raises on signature failure (which the wrapper translates to `F-CLASS-REGISTER-SIGNATURE-INVALID.signed_file_invalid` sub-tag).

  **Cycle-1 Red Team RT-04 fold-in — fail-closed in non-test postures.** A `None` return from `load_signed_register()` represents two distinct deployment states: (a) test/dev posture where no register has been seeded yet (acceptable; wrapper's RT-04 raw-bytes scan is skipped under None); (b) production posture where misconfiguration / missing key material / corrupted vault has prevented register load (NOT acceptable — Confidential data would egress unscanned by RT-04).

  The router-side load helper `_load_router_posture_and_register` MUST distinguish these:

  ```python
  def _load_router_posture_and_register() -> tuple[Posture, Mapping[str, Any] | None]:
      posture = get_current_posture()
      register = load_signed_register()
      # RT-04 fold-in — fail-closed if production posture lacks the signed register.
      if register is None and posture != "test":
          raise ClassificationBoundaryError(
              F_CLASS_REGISTER_SIGNATURE_INVALID,
              f"signed classification register absent under posture={posture}; "
              f"non-test deployments require an operator-signed register loaded "
              f"at process startup. Fail-closed per RT-04.",
          )
      return posture, register
  ```

  In test deployments (posture == "test" — a non-canonical posture used only for unit tests / dev fixtures), `register is None` is accepted and the wrapper skips its RT-04 raw-bytes scan per provider_boundary.py:497. In any of the three canonical customer-facing postures (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign per v7.0.10 §1), `register is None` is a fail-closed condition.

No new module imports — both exist on disk from §4 v2.x.5 runtime companion. Router gains two new import lines + two new function calls per dispatch.

## §7. ClassificationContext coercion

The router's `ClassificationContext` (defined at `pipeline.orchestrator.classification_context`) and the wrapper's `ClassificationContext` (defined at `pipeline.orchestrator.provider_boundary`) are structurally similar but not identical types. A small coercion helper `_coerce_to_provider_boundary_context` at the router layer maps fields one-to-one:

```python
def _coerce_to_provider_boundary_context(
    rc: ClassificationContext,
) -> provider_boundary.ClassificationContext:
    return provider_boundary.ClassificationContext(
        inputs=tuple(
            provider_boundary.ClassifiedInput(
                field_path=i.field_path,
                class_name=i.class_name,
            )
            for i in rc.inputs
        ),
        classified_values=tuple(
            provider_boundary.ClassifiedValue(
                field_path=cv.field_path,
                value=cv.value,
                class_name=cv.class_name,
            )
            for cv in rc.classified_values
        ),
        high_stakes_flag_values=tuple(rc.high_stakes_flag_values),
        slot_positions=tuple(rc.slot_positions),
        post_fill_draft=rc.post_fill_draft,
    )
```

(Or — if the two `ClassificationContext` types are already structurally identical — replace the wrapper's `ClassificationContext` definition with an import alias from the router's module. Operator-decision item OD-1 in §11.)

## §8. Test surface migration

`tests/orchestrator/test_router_classification_boundary.py` — the existing test cases assert `ClassificationBoundaryError` is raised on F-CLASS-* refusals. Post-amendment, the wrapper raises `OutboundBoundaryRefusedError` which the router translates to `ClassificationBoundaryError` in the fallback branch. **Net effect: zero test assertion changes are required** — the public exception contract is preserved by the translation layer.

New test cases added for the OD-5 refactor:

1. **`test_dispatch_via_wrapper_invokes_enforce_outbound_boundary`** — assert that the dispatch path constructs a wrapper exactly once per call (mock `enforce_outbound_boundary` to count invocations).
2. **`test_outbound_boundary_refused_translates_to_classification_boundary_error`** — assert that the translation layer at `_dispatch_with_classification_boundary` re-raises as `ClassificationBoundaryError` with the original `failure_code` + `detail` preserved.
3. **`test_posture_mid_cycle_change_fails_closed`** — assert that if posture mutates between dispatch entry and wrapper invocation, the wrapper raises `F-CLASS-POSTURE-MID-CYCLE-CHANGE` and the translation layer surfaces it.
4. **`test_signed_register_absent_in_test_posture`** — assert that `load_signed_register()` returning None is acceptable under test/dev posture (wrapper skips RT-04 raw-bytes scan).
5. **`test_local_provider_bypasses_wrapper`** — assert that local providers (Ollama / vLLM) do not invoke the wrapper, preserving the local-fast-path semantics.

## §9. §0.5 paired-commit (companion amendment)

See `pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_6_amendment.md`:

- **1 row** — routing-module update record: `pipeline/orchestrator/router.py` adopts the OD-5 dedup shape; runtime-live row count: 548 → 549.

No new F-CLASS-* failure code rows (the wrapper's existing 16-primitive family covers everything). No new AST-lint rule rows. No new sub-kind rows.

## §10. Failure modes + hardenings (audit-template summary)

| Failure mode | Severity | Defense |
|---|---|---|
| Router dispatch fires wrapper PRE/POST AND its own gates (double-firing) | LOW (RT-17 closed) | `_enforce_cloud_boundary_pre/post` DELETED; only wrapper fires. |
| Posture loaded once at router-module init, becomes stale mid-process | MED | `get_current_posture()` reads from atomic process-shared container; written only on operator-signed posture change. |
| Signed register absent → router crashes | MED | `load_signed_register()` returns `None` at test/dev posture; wrapper skips RT-04 scan; no crash. |
| Exception-class change breaks `call_seat` fallback handler | HIGH (if missed) | Translation layer at `_dispatch_with_classification_boundary` catches `OutboundBoundaryRefusedError` and re-raises as `ClassificationBoundaryError` with same `failure_code` + `detail`. Existing fallback branch handler unchanged. |
| ClassificationContext shape drift between router type and wrapper type | MED | `_coerce_to_provider_boundary_context` helper; OD-1 evaluates whether to unify the two types. |
| `_call_anthropic` / `_call_openai_style` direct-call test surface breaks | LOW | `http_post` parameter is keyword-only with default `None`; existing direct-call tests preserved (the legacy local-only dispatch branch fires when `http_post=None`). |

## §11. Operator decision queue (OD-1 .. OD-3) — RATIFIED 2026-05-16

Operator ratified all three picks via the "choose the best most effective stable intelligent efficient option" directive:

| OD | Decision | Reasoning |
|----|----------|-----------|
| **OD-1** | **RATIFIED: keep two ClassificationContext types + coercion helper + add field-parity drift test** | Preserves architectural decoupling between router's public API and the wrapper's internal contract. Avoids editing LOCKed `provider_boundary.py`. Drift risk closed via a `dataclasses.fields()`-based parity test that converts silent field-set divergence into a noisy test failure. |
| **OD-2** | **RATIFIED: load posture per-dispatch via `get_current_posture()`** | Process-shared atomic accessor — cheap read, always-current. Mid-cycle posture mutation is naturally fail-closed via existing `F-CLASS-POSTURE-MID-CYCLE-CHANGE` gate. Watcher pattern adds complexity for no observable benefit at A1+A4. |
| **OD-3** | **RATIFIED: delete legacy direct-call branch + migrate direct-call tests + R-NO-DIRECT-PROVIDER-CALL-WITHOUT-WRAPPER AST-lint sub-tag** | The keyword-only `http_post: OutboundCallable | None = None` shape would re-open a sovereignty bypass surface in production code — the whole point of OD-5 is to close those. Required `http_post: OutboundCallable` parameter keeps the wrapper as the SOLE path. Test migration cost accepted (proven cheap by the Groq fixture-migration sweep that landed earlier this session). AST-lint sub-tag pins the discipline post-LOCK. |

## §11.1 OD-3 follow-on — AST-lint sub-tag

`R-NO-DIRECT-PROVIDER-HTTP` gains a new sub-tag `.direct_provider_call_without_wrapper` that fires on any call to `_call_anthropic` or `_call_openai_style` at module scope where the call-site does not provide an `http_post` keyword argument. Scope: production code in `pipeline/orchestrator/router.py` only (test code grandfathered via existing `ALLOWLISTED_FILES` / `_GRANDFATHER_PATH_MARKERS` discipline).

The sub-tag rides under existing `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL` top-level row ownership per §4 v2.x.5 sub-tag-extension precedent. Family roster stays at 16 primitives.

## §11.2 OD-1 follow-on — drift test

New test at `tests/orchestrator/test_classification_context_field_parity.py`:

```python
def test_classification_context_field_parity():
    """Drift gate — router + provider_boundary ClassificationContext field sets must match.

    The two types are intentionally separate (OD-1 ratified architectural
    decoupling), but the coercion helper at router._coerce_to_provider_boundary_context
    silently drops any field that exists in one type and not the other.
    This test fires on field-set divergence to convert silent-drop into
    a noisy failure.

    Cycle-1 Judge DC-02 + Red Team RT-05 fold-in: name-set parity catches
    additions/deletions but NOT semantic drift (e.g., `slot_positions: List[int]`
    → `slot_positions: Tuple[str, ...]`). This test also compares field type
    annotations to surface semantic drift.
    """
    from dataclasses import fields
    from pipeline.orchestrator.classification_context import ClassificationContext as RC
    from pipeline.orchestrator.provider_boundary import ClassificationContext as PBC

    rc_field_types = {f.name: f.type for f in fields(RC)}
    pbc_field_types = {f.name: f.type for f in fields(PBC)}

    rc_names = set(rc_field_types)
    pbc_names = set(pbc_field_types)
    assert rc_names == pbc_names, (
        f"ClassificationContext field-name drift detected: "
        f"router-only={rc_names - pbc_names}, "
        f"provider_boundary-only={pbc_names - rc_names}. "
        f"Update _coerce_to_provider_boundary_context or unify the types."
    )

    # Type-annotation parity — catches semantic drift even when names match.
    # Forward-references (`f.type` as str) are compared byte-for-byte; future
    # hardening could resolve via typing.get_type_hints, but the str form is
    # sufficient for OD-1 decoupling discipline.
    type_mismatches = {
        name: (rc_field_types[name], pbc_field_types[name])
        for name in rc_names
        if rc_field_types[name] != pbc_field_types[name]
    }
    assert not type_mismatches, (
        f"ClassificationContext field-type drift detected: {type_mismatches}. "
        f"Same field names but different type annotations. "
        f"Update _coerce_to_provider_boundary_context to handle the new shapes "
        f"or align the type annotations."
    )
```

## §11.3 OD-3 follow-on — test migration scope

Tests calling `_call_anthropic` or `_call_openai_style` directly (without going through `_dispatch_with_classification_boundary`) require an `http_post=` argument. Migration shape mirrors the Groq fixture-migration sweep landed earlier this session — mechanical rename + stub Protocol-shape match. Expected magnitude: <20 call sites (router-test surface is narrower than the Groq seat test surface).

Pre-Cycle-1 grep verifies the scope:

```bash
grep -rn "_call_anthropic\|_call_openai_style" tests/ pipeline/ | grep -v "def _call_\|router.py"
```

## §12. Cycle 1 fold-ins (APPLIED 2026-05-16T15:37Z)

Cross-family Cycle 1 Thesis dispatch closed at 2026-05-16T15:36Z. Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via osascript→openclaw gateway bridge. Full audit text at `pipeline/validation/v4_v2_x_6_thesis_2026-05-16/audit_v1_{editor,judge,red_team}.md`. Synthesis at `pipeline/validation/v4_v2_x_6_thesis_2026-05-16/foldins_v1.md`.

**Cycle 1 verdict summary:**

- **Editor (Meta):** READY_TO_LOCK with 7 LOW/MED findings — all editorial clarity issues. All fold-in-at-LOCK per row-170 (no blocking).
- **Judge (Google):** REQUIRES_FIX 77/100. DC-01 HIGH = §3 code contradicted ratified OD-3 (kept legacy branch + Optional[None] default). DC-02 LOW = drift test name-only.
- **Red Team (OpenAI-OSS):** REQUIRES_FIXES blocking:true with 3 HIGH blocking (RT-01 local-provider bypass, RT-04 signed-register absence, RT-06 dynamic-call bypass) + 6 non-blocking findings (RT-02/03/05/07/08/09) + RT-10 NO-ACTION (no LOCKed-file breach).

**Cycle 1 fold-in disposition matrix (10 audit findings; 1 NO-ACTION):**

| Finding | Severity | Disposition | Applied at |
|---------|----------|-------------|------------|
| Judge DC-01 | HIGH | **FIX-IN-PLACE** — §3 rewritten: required `http_post: OutboundCallable` (no Optional[None]); legacy branch DELETED; runtime assertion added per RT-06. | §3 (this amendment) |
| Judge DC-02 | LOW | **FIX-IN-PLACE** — §11.2 drift test extended to compare `f.type` annotations. Catches semantic drift (same name, different type). | §11.2 (this amendment) |
| Red Team RT-01 | HIGH | **FOLD-IN** — Local-provider bypass exploit. The wrapper-skip branch at §2 reads `_is_cloud_provider(provider_name, provider_cfg)`. Hardening: §2 cross-references the canonical `_CLOUD_PROVIDERS` set + endpoint-pattern check at router.py:451-457. The mitigating invariant is that `_CLOUD_PROVIDERS` is a closed-set constant + `_is_cloud_provider` falls back to endpoint-URL inspection (https + not localhost). A future v2.x.7 follow-on can register a `R-NO-LOCAL-PROVIDER-ON-CLOUD-ENDPOINT` AST-lint rule for tighter static enforcement. RT-01 disposition: **PARTIAL-CLOSE; v2.x.7 follow-on for AST-lint hardening**. | §12.1 (this section) |
| Red Team RT-02 | MED | **FIX-IN-PLACE** — §2 translation block now narrowly handles `OutboundBoundaryRefusedError` only; other wrapper-origin exceptions propagate to `call_seat`'s existing generic `except Exception as primary_err` handler at router.py:747. Semantic two-bucket dichotomy preserved. | §2 (this amendment) |
| Red Team RT-03 | LOW-MED | **FIX-IN-PLACE / DOCUMENTARY** — §6 confirms the architectural invariant: the wrapper uses the SUPPLIED posture value, not re-querying internally. Mid-cycle posture mutation between `get_current_posture()` and wrapper invocation is fail-closed by `F-CLASS-POSTURE-MID-CYCLE-CHANGE` (already extant in provider_boundary.py). RT-03 disposition: **DOCUMENTARY** — invariant surfaced in §12.2 below. | §12.2 (this section) |
| Red Team RT-04 | HIGH | **FIX-IN-PLACE** — §6 amended with explicit `_load_router_posture_and_register` helper that fail-closes if `register is None` under any non-test posture (the three canonical customer-facing postures). | §6 (this amendment) |
| Red Team RT-05 | MED | **FIX-IN-PLACE** (combined with Judge DC-02) — §11.2 drift test extended for `f.type` comparison. Additional runtime validation in `_coerce_to_provider_boundary_context` for field-level type sanity is **DEFERRED to v2.x.7** as that touches the production hot-path; v1 ships the static-detection layer first. | §11.2 (this amendment) + §12.3 (deferral marker) |
| Red Team RT-06 | HIGH | **FIX-IN-PLACE** — §3 runtime assertion at body entry: `if http_post is None: raise ClassificationBoundaryError(...)`. Defense-in-depth against dynamic-call bypass (`getattr` / `importlib` / re-export-as-alias) that the AST-lint sub-tag cannot statically detect. | §3 (this amendment) |
| Red Team RT-07 | MED | **FIX-IN-PLACE** — §3 standardizes `json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")` across `_call_anthropic` and `_call_openai_style`. Provider-side encoder settings match what the wrapper's PRE-scan sees byte-for-byte. | §3 (this amendment) |
| Red Team RT-08 | LOW | **FIX-IN-PLACE** — §14 grep-verify scope expanded from `router.py` only to `pipeline/` + `tests/` with grandfather-list for documentary-only directories (`pipeline/validation/`, `pipeline/handoffs/`, `daily_logs/`, `pipeline/engineering/lock_history`). | §14 (this amendment) |
| Red Team RT-09 | MED | **DOCUMENTARY** — Multi-tenant scope creep is Stage-5 horizon work. v0.1 + v0.2 ship single-operator (A1+A4 invariant). v2.x.7 follow-on at Stage-5 will pass tenant-local context into the wrapper. RT-09 disposition: **v2.x.7 / Stage-5 deferred**. | §12.4 (this section) |
| Red Team RT-10 | NONE | **NO-ACTION** — Red Team confirmed zero LOCKed-file breach. Amendment honors §4 v2.x.5 row 232 canonical state. | n/a |
| Editor E-01 through E-07 | LOW/MED | **DOCUMENTARY** — Editorial clarity improvements. All addressed by the Cycle-1 fold-in edits applied to §2/§3/§4/§6/§11.2/§14. Editor's READY_TO_LOCK verdict holds; no blocking. | §2/§3/§4/§6/§11.2/§14 (this amendment) |

### §12.1 — RT-01 local-provider bypass partial-closure

The Cycle-1 Red Team finding RT-01 surfaces an architectural concern: if `_is_cloud_provider(provider_name, provider_cfg)` returns `False` for a provider that is actually cloud (mis-configured `provider_cfg`, stale `_CLOUD_PROVIDERS` constant, or operator-supplied custom config that tricks the endpoint heuristic), the router takes the local-fast-path and bypasses the wrapper.

**Current state mitigations** (router.py:451-457):

```python
def _is_cloud_provider(provider_name: str, provider_cfg: dict) -> bool:
    if provider_name in _CLOUD_PROVIDERS:
        return True
    if provider_name in _LOCAL_PROVIDERS:
        return False
    endpoint = str(provider_cfg.get("endpoint", ""))
    return endpoint.startswith("https://") and "localhost" not in endpoint
```

The closed-set `_CLOUD_PROVIDERS` + `_LOCAL_PROVIDERS` constants are operator-controlled at router-module load. The endpoint heuristic (https + not-localhost) is a defense-in-depth fallback for providers not in either set.

**Residual risk:** an operator-supplied `provider_cfg` for a "new" provider with `endpoint: "http://corporate-proxy.internal/cloud-egress"` would route through the local-fast-path (no https) while actually egressing to a cloud. The mitigating fact is that this requires operator opt-in via explicit `provider_cfg` registration — adversarial under multi-contributor (Stage-2+) but bounded under A1+A4.

**v2.x.7 follow-on (NEXT amendment):** Add `R-NO-CLOUD-LIKE-LOCAL-PROVIDER` AST-lint rule that scans `router.yaml` for endpoint patterns that look like cloud egress (non-localhost host, non-RFC1918 IP, known cloud-provider TLDs) and fail-closes deployment manifest signing if any local-classified provider has a cloud-shaped endpoint. Out-of-scope for this amendment per L-005 + L-006 (separate enforcement-layer addition; needs its own audit cycle).

### §12.2 — RT-03 posture supplied-not-re-queried invariant

Architectural invariant restated for the audit trail (per Cycle-1 Red Team RT-03 fold-in):

**The wrapper `enforce_outbound_boundary` MUST use the `posture` argument value exclusively. It MUST NOT re-query `get_current_posture()` internally.** The router loads posture once at dispatch entry via `_load_router_posture_and_register`, passes it into `enforce_outbound_boundary`, and the wrapper's internal `F-CLASS-POSTURE-MID-CYCLE-CHANGE` gate compares the SUPPLIED posture against the deployment-manifest-pinned posture — not against a fresh `get_current_posture()` call.

Mid-cycle posture mutation that occurs between the router's `get_current_posture()` call (line N) and the wrapper's invocation (line N+1) is fail-closed by the manifest-pin comparison inside `F-CLASS-POSTURE-MID-CYCLE-CHANGE`: the wrapper compares supplied-posture vs manifest-posture, not vs current-posture. A race-condition mutation would be detected at the next dispatch when `get_current_posture()` reads the new value but the manifest pin is unchanged (manifest mutation requires operator Ed25519 re-signing per v7.0.10 §1.4).

This invariant is documentary at v2.x.6 LOCK — `enforce_outbound_boundary`'s current body already operates this way (per `pipeline/orchestrator/provider_boundary.py:_enforce_pre` argument plumbing). No code change required. The §12.2 documentation locks the invariant against future drift.

### §12.3 — RT-05 ClassificationContext runtime-validation deferral

Cycle-1 Red Team RT-05 surfaced a secondary concern: even with type-annotation parity, the coercion helper `_coerce_to_provider_boundary_context` could silently produce malformed objects if field-level validation rules diverge (e.g., same `class_name` field name but stricter regex on one side).

**v2.x.6 disposition:** Static field-name + field-type parity test (§11.2) lands. Runtime per-field validation in the coercion helper is **DEFERRED to v2.x.7** — that change touches the production hot-path and benefits from its own audit cycle. The static drift test is sufficient to convert silent-drop into a noisy test failure at CI; runtime validation upgrades the protection from CI-only to dispatch-time.

### §12.4 — RT-09 Stage-5 multi-tenant deferral marker

Cycle-1 Red Team RT-09 surfaced a Stage-5 concern: the current design assumes process-wide singleton posture + signed-register. Multi-tenant Sovereign Node commons (Stage-5) requires per-tenant context plumbing.

**v2.x.6 disposition:** Out-of-scope. v0.1 + v0.2 ship single-operator (A1+A4 invariant). v7 LOCKED architecture explicitly bounds multi-tenant at Stage 2+. The current process-wide accessors (`get_current_posture` + `load_signed_register`) are correct for v0.1/v0.2 deployment topology.

**Stage-5 forward-binding:** When Stage 5 lands the cooperative-owned Sovereign Node commons, `enforce_outbound_boundary` gets a per-tenant context parameter and the router resolves tenant-local posture + signed-register via a new `get_current_tenant_context()` accessor. Tracked in `pipeline/planning/stage_5_sovereign_node_commons.md` (forward-binding doc).

## §13. Cycle 2 fold-ins (APPLIED 2026-05-16T15:46Z)

Cross-family Cycle 2 verification Thesis dispatch closed 2026-05-16T15:44..15:46Z. Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via osascript→openclaw gateway bridge. Full audit text at `pipeline/validation/v4_v2_x_6_thesis_2026-05-16/audit_v2_{editor,judge,red_team}.md`.

**Cycle 2 verdict summary:**

- **Editor (Meta):** PASS unanimous. All 7 Cycle 1 findings VERIFIED_CLOSED. 0 new findings. Verdict: READY_TO_LOCK.
- **Judge (Google):** READY_TO_LOCK at **99/100** (up from 77/100 Cycle 1). All Cycle 1 findings (DC-01 HIGH + DC-02 LOW + Red Team blockers via §12 disposition) VERIFIED_CLOSED. 0 new findings. D1=20/D2=20/D3=20/D4=19/D5=20.
- **Red Team (OpenAI-OSS):** READY_TO_LOCK blocking:**false**. All 10 Cycle 1 findings VERIFIED_CLOSED (RT-01 PARTIAL_CLOSURE accepted per deferral marker). 4 NEW exploratory probes RT-C2-01..RT-C2-04 — all non-blocking; fold-in-at-LOCK per row-170 transparent disposition.

**Convergent verdict: READY_TO_LOCK across all three reviewers. L-005 strict two-cycle CLOSED.**

### §13.1 — Cycle 2 NEW probes fold-in disposition (per row-170)

| Probe | Title | Severity | Disposition |
|-------|-------|----------|-------------|
| RT-C2-01 | Residual references to retired functions | LOW | **FOLD-IN as §14 enhancement (LANDED)** — §14 grep-verify already expanded scope to `pipeline/` + `tests/` with grandfather-list. RT-C2-01 is the same probe Red Team articulated more concretely; §14's expanded scope addresses it byte-for-byte. RT-C2-01 also explicitly names `eval` / `exec` strings and reflective calls — these would surface as test failures if exercised; AST-lint at LOCK validation catches the static call-shape surface. Documentary close. |
| RT-C2-02 | `_dispatch` signature alignment | MED | **FOLD-IN as runtime-companion code contract (§13.2 NEW)** — post-LOCK Claude Code dispatch MUST extend `_dispatch` signature to accept `http_post: OutboundCallable` and update ALL call sites (`router.py:_call_anthropic`, `router.py:_call_openai_style`, any other callers). LOCK-grep ensures no stale `_dispatch(...)` call site lacks the kwarg. |
| RT-C2-03 | Signed-register exception handling | MED | **FOLD-IN as §6 strengthening (LANDED inline)** — `_load_router_posture_and_register` MUST also catch exceptions from `load_signed_register()` (e.g., `VaultAccessError`, file I/O errors) and treat them identically to a `None` return for fail-closed semantics. §6 helper signature updated per §13.3 below. |
| RT-C2-04 | Coercion helper field-loss property test | LOW | **FOLD-IN as v2.x.7 drift-test enhancement contract (§13.4 NEW)** — current static drift test (§11.2) catches the common case (field-set divergence + type-set divergence at module-load). Property-based test feeding extra/nested structures is a v2.x.7 hardening item. Static drift test sufficient for v2.x.6 LOCK. |

### §13.2 — RT-C2-02 runtime-companion contract

Post-LOCK Claude Code dispatch (Land OD-5 runtime code) MUST ensure:

1. `_dispatch(provider_cfg, seat_cfg, messages, system, *, http_post: OutboundCallable)` — keyword-only `http_post` parameter added; required.
2. All existing call sites of `_dispatch` updated to pass `http_post=wrapped_caller`.
3. AST-lint test added at `tests/orchestrator/test_dispatch_signature_alignment.py` that imports `_dispatch` and asserts its signature has `http_post` as a keyword-only required parameter (via `inspect.signature(_dispatch).parameters`).

Grep verification at LOCK ceremony:

```bash
# Find any _dispatch( call site that does not pass http_post
grep -rn '_dispatch(' pipeline/orchestrator/router.py | grep -v 'http_post=' | grep -v 'def _dispatch'
# expected: 0 (all call sites pass http_post=)
```

### §13.3 — RT-C2-03 `_load_router_posture_and_register` exception handling

Updated helper shape (supersedes §6 inline code per row-170 fold-in):

```python
def _load_router_posture_and_register() -> tuple[Posture, Mapping[str, Any] | None]:
    posture = get_current_posture()
    register: Mapping[str, Any] | None
    try:
        register = load_signed_register()
    except Exception as e:
        # RT-C2-03 fold-in — any exception from the loader is treated as
        # equivalent to `None` for fail-closed semantics. The loader's own
        # exception classes (VaultAccessError, FileNotFoundError, JSON
        # parse errors, Ed25519 signature failures) all collapse to the
        # same response: fail-closed under non-test posture.
        if posture != "test":
            raise ClassificationBoundaryError(
                F_CLASS_REGISTER_SIGNATURE_INVALID,
                f"signed classification register load failed under posture={posture}: "
                f"{type(e).__name__}: {str(e)[:200]}. Fail-closed per RT-04 + RT-C2-03.",
            ) from e
        register = None  # test posture — accept absence

    # Original RT-04 fold-in path: clean `None` return from loader.
    if register is None and posture != "test":
        raise ClassificationBoundaryError(
            F_CLASS_REGISTER_SIGNATURE_INVALID,
            f"signed classification register absent under posture={posture}; "
            f"non-test deployments require an operator-signed register loaded "
            f"at process startup. Fail-closed per RT-04.",
        )
    return posture, register
```

### §13.4 — RT-C2-04 v2.x.7 drift-test hardening contract

The §11.2 drift test catches the common-case static drift (field-set + type-set divergence). Property-based testing of the coercion helper (feeding `ClassificationContext` instances with edge-case shapes — nested structures, extra default-handling cases) is a v2.x.7 hardening item.

**v2.x.7 contract:** Add `tests/orchestrator/test_classification_context_coercion_property.py` using `hypothesis` (already in dev deps per pyproject) with a strategy that generates `ClassificationContext` instances of varying shapes and asserts:

```python
@given(ctx=classification_context_strategy())
def test_coerce_preserves_all_fields(ctx):
    coerced = _coerce_to_provider_boundary_context(ctx)
    for field in dataclasses.fields(type(ctx)):
        assert getattr(coerced, field.name) == getattr(ctx, field.name), (
            f"Field {field.name} lost during coercion"
        )
```

v2.x.6 LOCK does not block on this — the static drift test is sufficient. v2.x.7 lands the hardening alongside any other OD-5 follow-ons.

## §14. LOCK ceremony grep verifications

Pre-LOCK grep checks per Cycle-1 Red Team RT-08 fold-in — expanded scope to `pipeline/` + `tests/` so vestigial references in audit trails, handoffs, or test files don't smuggle the deleted functions back in (must all return zero NON-DOCUMENTARY matches; matches inside comments/docstrings/audit-trail files are documented + grandfathered):

```bash
# Live-code grep — production source must be clean.
grep -rn '_enforce_cloud_boundary_pre\|_enforce_cloud_boundary_post' pipeline/orchestrator/router.py
# expected: 0

# Wider sweep — references outside router.py must only exist in audit trails
# (pipeline/validation/) and handoff docs (pipeline/handoffs/) as documentary
# historical artifacts. Production code + tests must be clean.
grep -rn '_enforce_cloud_boundary_pre\|_enforce_cloud_boundary_post' pipeline/ tests/ \
    | grep -v 'pipeline/validation/\|pipeline/handoffs/\|daily_logs/\|pipeline/engineering/lock_history' \
    | grep -v ':[[:space:]]*#\|:[[:space:]]*"""\|"""'
# expected: 0

# Vestigial deferral block — the prior session's DEFERRED-OD-5 marker becomes
# vestigial post-deletion.
grep -rn 'DEFERRED-OD-5' pipeline/orchestrator/router.py
# expected: 0
```

Post-refactor file path scan:

```bash
python -c "
import ast
src = open('pipeline/orchestrator/router.py').read()
tree = ast.parse(src)
funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
assert '_enforce_cloud_boundary_pre' not in funcs, 'OD-5 violation: _enforce_cloud_boundary_pre survives'
assert '_enforce_cloud_boundary_post' not in funcs, 'OD-5 violation: _enforce_cloud_boundary_post survives'
print('OD-5 grep-verify: PASS')
"
```

## §15. Predecessor amendments chain

- §4 v2.x.5 LOCKED 2026-05-16 row 232 (parent — CC-007 closure; specified OD-5 in §7; runtime companion executed PARTIALLY)
- §4 v2.x.1 LOCKED 2026-05-10 row 198 (precedent — narrow-corrective + sub-tag-extension shape)
- v7.0.10 LOCKED 2026-05-11 row 215 (predecessor — 16-primitive F-CLASS-* family + three-posture routing)
- v7.0.7 LOCKED 2026-05-10 row 180 (predecessor — F-CLASS-* family origin)

This amendment does NOT modify any LOCKed parent text in-place. The OD-5 closure lives entirely in this new amendment file + the §0.5 v28 paired-commit.
