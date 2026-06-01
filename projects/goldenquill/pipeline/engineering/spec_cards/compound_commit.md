# Spec card — pipeline.logician.compound_commit (§4 Logician v2.1 §4.11 compound-commit predicate)

**STATUS:** PRE-STAGED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` §4.11 (compound-commit predicate — four-phase structure; embedded Cedar companion; three context booleans)
- `pipeline/blueprint/v0.1/section_04_logician.md` §4.10.7 (`commit_compound_txn` entry point)
- `pipeline/blueprint/v0.1/section_04_logician.md` §6.13 (F-CEDAR-COMPOUND-DENIED failure-code family)
- `pipeline/blueprint/v0.1/section_04_logician.md` §9.8 (test vectors 9.8.1 happy path / 9.8.2 fail-intents-missing / 9.8.3 fail-hash-mismatch / 9.8.4 fail-session-mismatch)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.5 (signed compound-kind registry; v0.1 enumeration = `{index_amendment}`; references the Cedar companion policy by path)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §2.6 (Cedar entity shapes — `Session`, `VaultPath`, `CompoundTxn`)

**Blueprint hash-at-card:** `<to-fill-at-implementation-time>` — author runs `python scripts/check_blueprint_drift.py` to compute the 16-char SHA3-512 prefix of `section_04_logician.md` v2.1 + `section_02_vault_topology.md` v7.1 and pastes them here before Committee dispatch.

**Spec-card version:** v1
**Round:** Logician-compound-commit-R1 (Option-B compound-transaction enforcement; v0.1 canonical path per project memory `project_option_b_compound_txn_decision.md`)
**Futureproofing scope:** §4.1 public-API boundary; §4.6 BLUEPRINT_DEPS pinning; §4.9 regression discipline; §4.10 type hints; §4.11 docstring blueprint anchors; §4.12 engineering-lessons accumulation. Additional scope: extensibility for new `CompoundTxnKind` values added at a future Section 4 LOCK cycle (v0.1 = `{index_amendment}` only; growth path: row-append to registry + new `permit` rule in `compound_commit.cedar` + row-append test vectors).

**Companion artefacts (must land in the same commit):**
- `pipeline/logician/cedar_policies/compound_commit.cedar` — SKELETON already on disk 2026-04-20. First LOCK of this module activates the file into the Section 4 CedarEvaluator load path.
- `pipeline/blueprint/v0.1/section_00_5_cedar_policy_kinds_amendment.md` — DRAFT §0.5 amendment filing row 103 (`logician.cedar_policy.compound_commit`) with `stability_tier = PENDING_PARENT_BACKFILL`; this spec card's LOCK is the "load-path activation backfill" that flips the row to `STABLE`.

---

## Summary

Ship the deterministic, fail-closed compound-commit predicate that Section 2 vault dispatcher consults before atomically committing a `CompoundTxn` (v0.1: only `index_amendment` per §2 v7.1 §4.10.5). The predicate runs four phases in fixed order and returns a structured verdict consumed by the Vault's Option-B compound-transaction path:

1. **Required-intents multiset equality** — over `txn.staged_writes` (Counter over intent tags against `registry[txn.kind].required_intent_multiset`) → F-VAULT-24 on mismatch.
2. **Stored hash-binding equality** — over each staged write's pre-image hash + post-image hash against `registry[txn.kind].hash_binding_rules` → F-VAULT-25 on mismatch.
3. **Session match** — `txn.session_id` equal to every staged write's `session_id` AND present in the active `Session` entity lookup → F-VAULT-26 on mismatch.
4. **Cedar dispatch** — principal `Seat::"Dispatcher"`, action `VaultAction::"commit_compound_txn"`, resource `CompoundTxn::"<kind>"`, context `{required_intents_present: True, hash_bindings_valid: True, session_matches: True}`. Cedar does NOT re-derive phases 1-3; it affirmatively signs off as the final commit gate. Unknown `kind` outside the v0.1 enumeration → `F-CEDAR-COMPOUND-DENIED.unknown_kind`. Cedar policy denies (context not satisfied OR resource not permitted) → `F-CEDAR-COMPOUND-DENIED.predicate_denied`.

Landing this closes the "blueprint-pinned, target-missing" gap flagged in `gpp_det_report_2026-04-19` §4.11. Activates the Cedar policy skeleton `pipeline/logician/cedar_policies/compound_commit.cedar`. First Option-B enforcement module in the Logician; establishes the pattern for subsequent compound kinds (eventual report-submission at v0.2, content-vertical publish at v0.2+).

## Design decisions

1. **Predicate, not executor.** `compound_commit_predicate` RETURNS a verdict; it does NOT perform the commit. The Vault caller (Section 2 dispatcher at §4.10.7) owns the commit action, and only proceeds when the predicate returns `PredicateResult(admit=True)`. Rationale: Law 4 (fail-closed) — separating decision from execution prevents "predicate almost passed, committed anyway" paths.
2. **Python, not LLM.** Pure deterministic module; zero token cost; no network; no LLM seat involved. Imports: `collections.Counter`, `dataclasses`, `typing`, `pipeline.vault.entities` (the frozen entity dataclasses), `pipeline.logician.cedar_eval` (Cedar policy loader + evaluator). NEVER imports any LLM-client SDK — banned by ARCH-04 R1 `LOGICIAN_IMPORT_BAN`.
3. **Four phases in fixed order, short-circuit on first failure.** §4.11 prose is explicit that phases evaluate in order; a phase 1 failure does NOT evaluate phase 2. Rationale: (a) failure codes must be single-source-of-truth (ambiguous ordering → ambiguous which F-VAULT-* the caller sees); (b) performance irrelevant at v0.1 but the semantic lock is load-bearing for Option-B audit.
4. **Cedar is the fourth gate, not a re-derivation.** §4.11 is clear: phases 1-3 DERIVE the three context booleans (`required_intents_present`, `hash_bindings_valid`, `session_matches`); Cedar SIGNS OFF on them. Cedar does NOT re-evaluate phases 1-3. Rationale: (a) Cedar's role is authorization policy, not state re-computation; (b) the Python phases carry the evidence trail consumed by the Logician verdict object.
5. **v0.1 `CompoundTxnKind` enumeration is a lock, not a default.** The only permitted kind at v0.1 is `index_amendment` (per §2 v7.1 §4.10.5 signed compound-kind registry). Any other `kind` value flows straight to `F-CEDAR-COMPOUND-DENIED.unknown_kind` — does NOT attempt phases 1-3 at all. Rationale: prevents a malformed txn from spending phase-1 cycles before being rejected at phase 4; aligns with Cedar's default-deny stance on resources not in the enumeration.
6. **Cedar file is code-adjacent, not vault_shared seed.** The companion `.cedar` file lives at `pipeline/logician/cedar_policies/compound_commit.cedar` (per §0.5 primitive_kind `cedar-policy-code`), loaded at Section 4 module boot by the CedarEvaluator — NOT at §9 step 9 by `m15_ledger.cedar_policy_loader_load_all` (that loader walks only `vault_shared/cedar/*.cedar`). Changes to the code-side policy require a new Section 4 LOCK cycle, NOT an M15 operator re-type. See `project_option_b_compound_txn_decision.md` memory + `section_00_5_cedar_policy_kinds_amendment.md` for the vocabulary split.
7. **PredicateResult carries structured evidence, not a boolean.** Return type is a frozen dataclass with `admit: bool`, `failure_code: Optional[str]`, `phase_reached: Literal[1,2,3,4]`, `evidence: dict[str, object]`. Rationale: the Vault dispatcher writes the verdict into the admin-risk ledger on failure; a boolean discards too much context to reconstruct why the commit was denied.
8. **No partial commits, no rollback.** If predicate returns `admit=False`, the Vault never began committing — there is nothing to roll back. If predicate returns `admit=True`, the Vault's commit path IS atomic (Section 2 v7.1 §4.10.7 guarantees this); the predicate is NOT in that atomic critical section. Rationale: keeps the predicate stateless and free of crash-safety obligations.

## Public API (goes in `__all__`)

```python
# pipeline/logician/compound_commit.py
__all__ = [
    # Futureproofing pin (§4.6)
    "BLUEPRINT_DEPS",
    # Public dataclasses
    "PredicateResult",
    "CompoundTxn",          # re-export of the shape authored in section_02 §4.10.5
    "CompoundTxnKind",      # Literal type alias — v0.1: Literal["index_amendment"]
    "StagedWrite",          # inner record of CompoundTxn
    "HashBindingRule",      # entry type in registry[kind].hash_binding_rules
    "RegistryEntry",        # one compound-kind's registry entry shape
    # Entry point
    "compound_commit_predicate",
    # v0.1 registry constant (enumeration = index_amendment)
    "V0_1_COMPOUND_TXN_REGISTRY",
]
```

- `PredicateResult` — frozen, kw_only: `admit: bool`, `failure_code: Optional[str]` (one of the failure codes below), `phase_reached: Literal[1, 2, 3, 4]`, `evidence: Mapping[str, object]` (phase-1 includes the observed Counter vs expected Counter; phase-2 includes the first failing (pre, post) pair; phase-3 includes the mismatched session_id pair; phase-4 includes the Cedar context dict).
- `CompoundTxn` — frozen, kw_only: `kind: str` (raw string, validated inside the predicate), `staged_writes: tuple[StagedWrite, ...]`, `session_id: str`.
- `StagedWrite` — frozen, kw_only: `intent_tag: str`, `pre_image_hash: str`, `post_image_hash: str`, `session_id: str`, `vault_path: str`.
- `HashBindingRule` — frozen, kw_only: `intent_tag: str`, `expected_pre_image_hash_source: str`, `expected_post_image_hash_source: str` (source descriptors name where the expected hash comes from — e.g., `"parent_lock_file_sha3"` or `"staged_proposed_bytes_sha3"`).
- `RegistryEntry` — frozen, kw_only: `kind: str`, `required_intent_multiset: Counter[str]`, `hash_binding_rules: tuple[HashBindingRule, ...]`.
- `compound_commit_predicate(txn: CompoundTxn, registry: Mapping[str, RegistryEntry], cedar: CedarEvaluator) -> PredicateResult` — entry point.
- `V0_1_COMPOUND_TXN_REGISTRY: Mapping[str, RegistryEntry]` — frozen v0.1 registry with exactly one entry (`"index_amendment"`). Growth at v0.2+ requires Section 4 LOCK cycle.

## Data structures

All frozen + kw_only per blueprint §0.5 discipline. `CompoundTxn` and its inner `StagedWrite` are value objects; `PredicateResult` is a verdict record. No mutation anywhere.

The `staged_writes` tuple is NOT mutated or sorted by the predicate; the Counter in phase 1 is built from `[w.intent_tag for w in txn.staged_writes]` without reordering the underlying tuple — reordering would lose the hash-binding pairing in phase 2 (each staged write is matched to its hash-binding rule by intent_tag AND position; positional mismatch across reorderings would fail a valid txn).

## Algorithms

**Phase 0 — kind enumeration check.** If `txn.kind not in registry` → return `PredicateResult(admit=False, failure_code="F-CEDAR-COMPOUND-DENIED.unknown_kind", phase_reached=4, evidence={"observed_kind": txn.kind, "enumerated_kinds": sorted(registry.keys())})`. Note `phase_reached=4` even though phases 1-3 never executed: §6.13 classifies unknown_kind as a Cedar-layer rejection (resource not in the permit-rule enumeration), not a phase-1/2/3 failure.

**Phase 1 — required-intents multiset equality.**
Observed = `Counter(w.intent_tag for w in txn.staged_writes)`.
Expected = `registry[txn.kind].required_intent_multiset`.
If `observed != expected` → return `PredicateResult(admit=False, failure_code="F-VAULT-24", phase_reached=1, evidence={"observed": dict(observed), "expected": dict(expected), "missing": dict(expected - observed), "extra": dict(observed - expected)})`.

**Phase 2 — stored hash-binding equality.**
For each `(w, rule)` pair in `zip(txn.staged_writes, registry[txn.kind].hash_binding_rules, strict=True)`:
1. Assert `w.intent_tag == rule.intent_tag` — if not, the registry or caller violated the intent_tag pairing invariant; return `PredicateResult(admit=False, failure_code="F-VAULT-25", phase_reached=2, evidence={"pairing_violation": True, "staged_intent": w.intent_tag, "rule_intent": rule.intent_tag})`.
2. Resolve the expected pre-image hash and expected post-image hash via the source descriptors in `rule`. Source descriptors are resolved through a module-private `_resolve_hash_source(descriptor: str, txn: CompoundTxn, w: StagedWrite) -> str` helper that maps a descriptor like `"parent_lock_file_sha3"` to the concrete hash value via a registered resolver table. Unknown descriptor → raise a `CompoundCommitInvariantError` (programming error, not a txn-level failure — crashes the predicate with a fail-closed signal to the Vault caller, which must treat this as a hard abort).
3. Compare `w.pre_image_hash == expected_pre` and `w.post_image_hash == expected_post`. If either mismatches → return `PredicateResult(admit=False, failure_code="F-VAULT-25", phase_reached=2, evidence={"failing_intent": w.intent_tag, "pre_image_ok": (w.pre_image_hash == expected_pre), "post_image_ok": (w.post_image_hash == expected_post)})`.

Short-circuit on first failure — do NOT continue iterating.

**Phase 3 — session match.**
If any `w.session_id != txn.session_id` for any staged write → return `PredicateResult(admit=False, failure_code="F-VAULT-26", phase_reached=3, evidence={"txn_session_id": txn.session_id, "first_mismatching_write_index": <idx>, "staged_session_id": w.session_id})`.
Additionally: verify `txn.session_id` resolves to an ACTIVE `Session` entity via `cedar.lookup_session(txn.session_id)` (the CedarEvaluator exposes a helper that reads from the live session registry maintained by Section 2). If the lookup returns None (no such session) OR returns a session in a terminal state (closed / revoked) → same failure, with `evidence={"session_lookup": "missing_or_terminal"}`.

**Phase 4 — Cedar dispatch.**
Build context: `{"required_intents_present": True, "hash_bindings_valid": True, "session_matches": True}` (all True by construction — if any were False we short-circuited earlier).
Call `cedar.is_authorized(principal=Seat("Dispatcher"), action=VaultAction("commit_compound_txn"), resource=CompoundTxn(kind=txn.kind), context=context)`.
If the Cedar evaluator returns DENY (context booleans not satisfied under the policy — impossible under this code path given we asserted all three above, unless the on-disk `compound_commit.cedar` drifts from the embedded blueprint §4.11 snippet in a subsequent bad edit, which AST-lint + blueprint-hash would catch pre-flight; nevertheless the runtime denies defensively) → return `PredicateResult(admit=False, failure_code="F-CEDAR-COMPOUND-DENIED.predicate_denied", phase_reached=4, evidence={"cedar_context": context})`.

On PERMIT → return `PredicateResult(admit=True, failure_code=None, phase_reached=4, evidence={"cedar_context": context})`.

## Failure codes

Emitted by this module:

- **`F-VAULT-24`** — required-intents multiset mismatch (phase 1). Family: Section 4 §6.13 + Section 2 §4.10.7. Phase: 1.
- **`F-VAULT-25`** — stored hash-binding mismatch (phase 2). Family: same. Phase: 2. Also fires on an intent_tag pairing violation between staged_writes and hash_binding_rules (programmer error surfacing as an invariant check).
- **`F-VAULT-26`** — session mismatch (phase 3). Family: same. Phase: 3. Covers both (a) per-write session_id diverging from txn.session_id and (b) session lookup returning missing/terminal.
- **`F-CEDAR-COMPOUND-DENIED.unknown_kind`** — `txn.kind` not in the registry (phase 0). Family: Section 4 §6.13. Phase: 4 (Cedar-layer surface).
- **`F-CEDAR-COMPOUND-DENIED.predicate_denied`** — Cedar denied after context was built (phase 4). Family: same. Phase: 4.

Not emitted (fail-out-of-scope): `F-CEDAR-01.*` (those are Section 4 module-boot failures from `cedar_policy_loader_load_all` or AST-lint surface — they fire before this predicate ever runs).

## Test surface

### Property tests
- `test_predicate_is_pure_function` — same inputs → same output across 1000 random perturbations of other module state.
- `test_predicate_does_not_mutate_txn` — `copy.deepcopy` comparison pre/post call.
- `test_predicate_does_not_mutate_registry` — same, on the registry.
- `test_predicate_returns_frozen_result` — `dataclasses.is_dataclass(result) and result.__dataclass_params__.frozen`.
- `test_v0_1_registry_is_singleton_kind` — `set(V0_1_COMPOUND_TXN_REGISTRY.keys()) == {"index_amendment"}`.
- `test_v0_1_registry_is_mapping_proxy` — registry is wrapped in `types.MappingProxyType` (runtime immutability).

### Failure-code tests (§9.8 test vectors 9.8.1-9.8.4 — RED-FIRST discipline)
- **Vector 9.8.1 happy path** — `test_9_8_1_happy_path_admits` — valid `index_amendment` txn with correct intents, correct hashes, matching session → `admit=True, failure_code=None, phase_reached=4`.
- **Vector 9.8.2 fail-intents-missing** — `test_9_8_2_intent_missing_fails_phase_1` — txn missing one required intent → `admit=False, failure_code="F-VAULT-24", phase_reached=1, evidence.missing non-empty`.
- **Vector 9.8.2a extra intent** — `test_9_8_2a_extra_intent_fails_phase_1` — txn with an unexpected intent tag → same family, `evidence.extra non-empty`.
- **Vector 9.8.3 fail-hash-mismatch** — `test_9_8_3_hash_mismatch_fails_phase_2` — one staged write has wrong pre-image hash → `admit=False, failure_code="F-VAULT-25", phase_reached=2, evidence.pre_image_ok=False`.
- **Vector 9.8.3a post-hash mismatch** — `test_9_8_3a_post_image_mismatch_fails_phase_2` — `evidence.post_image_ok=False`.
- **Vector 9.8.4 fail-session-mismatch** — `test_9_8_4_session_mismatch_fails_phase_3` — one staged write has session_id diverging from txn.session_id → `admit=False, failure_code="F-VAULT-26", phase_reached=3`.
- **Vector 9.8.4a session-missing** — `test_9_8_4a_session_lookup_missing_fails_phase_3` — `cedar.lookup_session` returns None → same failure code, `evidence.session_lookup="missing_or_terminal"`.
- `test_unknown_kind_fails_phase_0` — `txn.kind = "not_in_registry"` → `admit=False, failure_code="F-CEDAR-COMPOUND-DENIED.unknown_kind", phase_reached=4, evidence.enumerated_kinds=["index_amendment"]`.
- `test_cedar_deny_under_context_all_true` — inject a CedarEvaluator stub that denies even when context is all-True → `admit=False, failure_code="F-CEDAR-COMPOUND-DENIED.predicate_denied", phase_reached=4`. Documents defensive deny-path.

### Short-circuit discipline tests
- `test_phase_1_failure_does_not_attempt_phase_2` — instrument the hash resolver; assert zero calls after a phase-1 F-VAULT-24.
- `test_phase_2_failure_does_not_attempt_phase_3` — instrument the session lookup; assert zero calls after a phase-2 F-VAULT-25.
- `test_phase_3_failure_does_not_attempt_phase_4` — instrument the Cedar evaluator; assert `is_authorized` never called after a phase-3 F-VAULT-26.

### Adversarial tests (`test_adv_*`)
- `test_adv_reordered_staged_writes_fail_phase_2` — swap two staged writes; intent_tag Counter still equal in phase 1, but the zip in phase 2 now pairs wrong hash rules → F-VAULT-25 (documented behaviour; caller must submit writes in registered intent-pair order).
- `test_adv_duplicate_staged_write_fails_phase_1` — two writes with the same intent_tag but expected multiset had one → F-VAULT-24 with `evidence.extra` non-empty.
- `test_adv_empty_staged_writes_fails_phase_1` — `staged_writes = ()` → F-VAULT-24 with `evidence.missing == expected.total()`.
- `test_adv_none_staged_write_pre_hash_fails_phase_2` — a staged write with `pre_image_hash=""` (empty string, not None since field is `str`) → F-VAULT-25.
- `test_adv_cedar_evaluator_returns_error_raises` — Cedar evaluator raises `CedarPolicyLoadFailed` mid-call → predicate does NOT catch it (propagates to caller); test asserts `pytest.raises`.
- `test_adv_kind_is_not_a_string` — caller passes a non-string `kind` (e.g., int) → predicate raises `TypeError` (no soft-fail into F-CEDAR-COMPOUND-DENIED.unknown_kind; this is a programmer bug, caller's responsibility).
- `test_adv_session_id_empty_string_fails_phase_3` — txn.session_id = "" → Cedar session lookup returns None → F-VAULT-26.

### Corpus tests
- `tests/corpus/compound_commit/v1/pass/` — fixture txns that must pass the predicate.
- `tests/corpus/compound_commit/v1/fail/` — fixture txns paired with expected `(failure_code, phase_reached)` manifests; covers each of the five failure codes at least once.

### Cedar-file integrity test (cross-module guard)
- `test_cedar_file_matches_blueprint_snippet` — reads `pipeline/logician/cedar_policies/compound_commit.cedar`, extracts the embedded policy body from blueprint §4.11 via a `scripts/extract_blueprint_cedar.py` helper, asserts the on-disk file's canonical bytes (whitespace-normalized) match the blueprint's embedded version. Drift → test fails; fix is to re-lock Section 4 (NOT to silently sync the file). Guards against the Design Decision #6 drift vector.

## Futureproofing commitments

- Public-API surface declared in `__all__`; internal helpers (`_resolve_hash_source`, `_build_cedar_context`) stay module-private.
- Schema version: `V0_1_COMPOUND_TXN_REGISTRY` pinned to v0.1 enumeration. Growth to v0.2 enumeration (adding `report_submission`, `content_publish`, etc.) requires Section 4 LOCK cycle + registry row-append + matching `permit` rule in `compound_commit.cedar` + new §9.8 test vectors. Card explicitly delegates that work to a future round; does NOT ship stubs.
- Crypto-agile hash types: `pre_image_hash` and `post_image_hash` are typed `str` at v0.1 with implicit SHA-3-512 hex encoding (matches the canonical-bytes hashing used elsewhere in the codebase). A future crypto agility refactor (if SHA-3 is ever deprecated) would wrap these in a `HashValue(algo, hex)` frozen dataclass — v0.2 backlog.
- `BLUEPRINT_DEPS` populated at LOCK:
  ```python
  BLUEPRINT_DEPS = {
      "section_04_logician.md": {
          "sections_implemented": ["§4.10.7", "§4.11", "§6.13", "§9.8.1-4"],
          "hash_at_lock": "<16-char-prefix>",
          "hash_source_version": "v2.1",
      },
      "section_02_vault_topology.md": {
          "sections_implemented": ["§4.10.5", "§2.6"],
          "hash_at_lock": "<16-char-prefix>",
          "hash_source_version": "v7.1",
      },
  }
  ```
  Drift-guard test `test_blueprint_deps_hashes_match_live_blueprints` fails when either parent blueprint is edited without bumping this pin.
- Regression discipline: corpus fixture files are preserved indefinitely; future registry growth is ADDITIVE (new corpus files row-append; existing pass corpus must keep passing).
- Extensibility: new `CompoundTxnKind` added by (a) row-append to `V0_1_COMPOUND_TXN_REGISTRY` (rename to `V0_2_COMPOUND_TXN_REGISTRY`), (b) new permit rule in `compound_commit.cedar` under a new Section 4 LOCK, (c) row-append §9.8 vectors, (d) row-append §0.5 row if the new kind needs its own Index primitive (e.g., a new hash-binding-rule kind).

## Done definition

1. `pipeline/logician/compound_commit.py` implemented with the public API above. Property tests green (purity, non-mutation, frozen result, registry singleton).
2. All five failure-code tests red-before-fix, green-after. Each of §9.8 vectors 9.8.1-9.8.4 (+ 9.8.2a, 9.8.3a, 9.8.4a variants) covered with a dedicated test.
3. All three short-circuit discipline tests green — phase N failure provably does not trigger phase N+1 work.
4. All adversarial tests exercise the documented threat model; none passes vacuously.
5. Cross-module Cedar-file integrity test (`test_cedar_file_matches_blueprint_snippet`) green; drift between on-disk `compound_commit.cedar` and blueprint §4.11 embedded snippet is caught.
6. Coverage on `pipeline/logician/compound_commit.py` ≥ 95% (branch coverage, not just line — every phase short-circuit path reached).
7. AST-lint surface (ARCH-04) passes on the new module: no LLM-client import, no loop-internal access, no vault-path `open()`.
8. `BLUEPRINT_DEPS` populated with live 16-char SHA3-512 prefixes of §4 v2.1 + §2 v7.1; drift-guard test green.
9. Cedar policy file `pipeline/logician/cedar_policies/compound_commit.cedar` promoted from SKELETON to ACTIVE — header updated to remove "NOT YET DEPLOYED" and replace with "ACTIVATED <date> under Section 4 v2.1 LOCK — loaded by CedarEvaluator at module boot".
10. §0.5 row 103 (`logician.cedar_policy.compound_commit`) flipped from `stability_tier = PENDING_PARENT_BACKFILL` to `STABLE` via an amendment that lands same commit (single-row `§0.5_v{N}_cedar_policy_activation_amendment.md`).
11. Code Thesis Committee dispatch: 5 cross-family reviewers per `router.yaml` `code_*` rows (Codex OpenAI / Qwen 3 32B Alibaba / Llama 3.3 70B Meta / GPT-OSS 120B OpenAI-OSS / Kimi K2 Moonshot); all-pass, retry cap 1. Non-code artefacts (the §0.5 amendment, the Cedar file header update) route through Thesis Team (Editor + Judge + Red Team) per `project_code_thesis_committee.md` memory — cross-family rigor preserved.
12. `pipeline/validation/logician_compound_commit_r1_<date>/` audit-trail folder created with Committee verdicts + Thesis verdicts + closure narrative.
13. `pipeline/engineering/lock_history.v1.jsonl` telemetry line appended: `{"card":"compound_commit","round":"logician_compound_commit_r1","shipped":["phase_0","phase_1","phase_2","phase_3","phase_4"],"failure_codes":["F-VAULT-24","F-VAULT-25","F-VAULT-26","F-CEDAR-COMPOUND-DENIED.unknown_kind","F-CEDAR-COMPOUND-DENIED.predicate_denied"]}`.
14. `daily_logs/2026-04-20.md` (or the LOCK-day log) updated with: card filed, Committee+Thesis dispatch, LOCK commit hash, §0.5 row flip.
15. Engineering lesson `E-NNN` added: "Cedar companion policies for code-side predicates must be activated by the predicate module's LOCK, not authored and left floating as skeletons. Skeleton-to-active is a §0.5 row-tier flip that rides the LOCK commit." Pre-check: any future Cedar-companion skeleton added to `pipeline/logician/cedar_policies/` must have a paired spec card filed same round.
16. Downstream unblocks: Section 2 dispatcher's Option-B commit path at §4.10.7 can now call `compound_commit_predicate` with a live v0.1 registry; the remaining §2 v7.1 integration is tracked in its own card.
17. Next staged (per CLAUDE.md proactive pre-staging): either (a) Section 2 dispatcher §4.10.7 spec card (the caller side of this predicate — clearly unblocked by this LOCK and derivable from blueprint without operator input), OR (b) `vault_shared/cedar/org_isolation.cedar` M15 signed-commit activation card (sibling Cedar policy; activation path distinct — requires M15 operator re-type per M15.3 discipline; may need operator input on signing-ceremony timing so surfaces as an open question rather than a pre-staged card).

---

*Spec card v1 — 2026-04-20 — authored under operator delegation ("do everything you suggest to have the best cleanest most stable tool and lets carry on"); ready for Midas dispatch once blueprint hash prefixes pinned at pre-LOCK Committee preflight.*
