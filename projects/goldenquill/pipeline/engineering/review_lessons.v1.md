---
scope: code-review engineering discipline
format: human-readable canonical engineering-lessons log
paired_with: code_reviews/<round-id>/final_synthesis.md entries
last_updated: 2026-04-21 (E-029 Protocol-first gate-scope + E-030 pre-dispatch companion-code pin verification filed from Logician v2.2 arc)
---

# Engineering Review Lessons

Repeat patterns from Code Thesis Committee rounds. Next-round spec cards pre-check against these lessons. Structure mirrors `lessons.md` (grant-side) but prefixed `E-` for engineering.

Entry format:

```
## E-NNN — Title
- First observed: YYYY-MM-DD (round-id)
- Frequency: N occurrences
- Severity: CRITICAL | HIGH | MEDIUM | LOW
- Pattern: ...
- Pre-check (for next round's spec cards): ...
- Origin: where the finding surfaced
```

---

## E-001 — Primitive-layer enforce-by-default + caller-override beats primitive-permissive + caller-enforce

- First observed: 2026-04-19 (Round A)
- Frequency: 1 occurrence
- Severity: MEDIUM
- Pattern: Low-level crypto primitives (HMAC, hash) are tempting to leave permissive at the primitive layer with a docstring that says "callers enforce the real constraint." This feels composable but opens the accidental-operator-mistake attack surface — every future caller has to remember to enforce, and any skipped enforcement only fails at the protocol layer far from the bug.
- Pre-check: Every primitive that has a blueprint-stated minimum bound (key length, entropy, nonce size, etc.) enforces the bound BY DEFAULT at the primitive layer. Override via explicit kwarg. Callers who legitimately need to bypass the default must do so in code that's visible to review. `hmac_sha3_512(..., min_key_bytes=...)` is the reference pattern.
- Origin: Round A RT-v1-M-01 (GPT-OSS-120B, round 1 + round 2). Author initially went permissive-with-docstring; reviewer correctly insisted on enforce-by-default.

## E-002 — Algorithm identifier strings MUST be case-normalized across every dataclass + dispatcher

- First observed: 2026-04-19 (Round A)
- Frequency: 1 occurrence
- Severity: MEDIUM
- Pattern: When multiple dataclasses carry an `algorithm: str` field for crypto-agility (per A12.3 / engineering_process §4.4), drift in casing between types creates a latent bug where a case-sensitive dispatcher expecting one form encounters the other and fails (or, worse, silently mismatches). Blueprints often specify one casing and code may end up using another without anyone noticing until dispatch time.
- Pre-check: Every module's spec card with algorithm identifiers declares the canonical casing (prefer lowercase slug style). Every constructor populating an `algorithm` field reads from a module-level constant (`_ALGO_*`). Reviewers (especially R5 coherence seat) verify cross-module identifier consistency.
- Origin: Round A RT-v2-M-01 (Gemini 2.5 Pro, Round 2 as R5 substitute).

## E-003 — Strict "reject any non-ASCII in NFC" is simpler AND safer than "reject lossy ASCII encode"

- First observed: 2026-04-19 (Round A)
- Frequency: 1 occurrence
- Severity: HIGH
- Pattern: Canonicalization rules that compare pre-encode vs post-encode lengths (whether the ASCII encode "shortened" the string) miss Unicode compatibility-decomposition codepoints that NFKD-decompose directly to pure ASCII with no combining-mark residue. `U+212B` (ANGSTROM SIGN) → NFKD → `"A"` bypasses the shrink check. Any slug function using this pattern will accept `Å` as a distinct-from-`A` slug, creating homoglyph collision surface.
- Pre-check: Every canonicalization primitive that collapses Unicode to ASCII applies the rule "reject any non-ASCII codepoint in the NFC form of the input" at the TOP of its pipeline, BEFORE any NFKD / ASCII-encode step. Simpler + strictly stronger than the "lossy shrink" formula.
- Origin: Round A RT-v1-H-01 (GPT-OSS-120B, adversarial reviewer Round 1).

## E-004 — Committee reviewer model identifiers drift with provider catalogs; router.yaml slots SHOULD carry primary/fallback

- First observed: 2026-04-19 (Round A)
- Frequency: 1 occurrence
- Severity: MEDIUM (process-level)
- Pattern: The Code Thesis Committee's 5 reviewer slots are LOCKed as a canonical roster in A2 Block 2, but each slot's MODEL IDENTIFIER depends on the provider's current catalog. Providers rename, deprecate, or rate-limit models. When the primary model for a slot becomes inaccessible mid-round, the committee blocks. Without a fallback pattern, operators have to manually substitute or the round halts.
- Pre-check: Every `code_reviewer_*` slot in router.yaml carries a `primary` and `fallback` row (identical pattern to author-side seats like scribe). Cross-family rigor verified after fallback resolution (no two of the 5 reviewer slots resolve to the same provider family). Substitutions log to drift_log + round findings_path.
- Origin: Round A D-08 — Kimi K2 inaccessible on Groq from operator's tier; substituted with Gemini 2.5 Pro via Google API. A2 Block 2 canonical roster preserved as `primary`; operational reality is `fallback`.

## E-005 — Spec-card LOC targets must be built sub-system-wise, not module-wise

- First observed: 2026-04-19 (Round B)
- Frequency: 2 occurrences (topology.py, audit.py)
- Severity: MEDIUM (process-level)
- Pattern: Spec-card LOC targets sized by rough whole-module guess under-count when a single blueprint-stated module covers multiple sub-systems. `audit.py` spec-card target was ~430 LOC; actual LOCKed implementation is 966 LOC because §5.6 BT8 HMAC trailer + §5.6 v4 watermark integrity + §5.6 rotation + §5.3 BT3 append protocol are FOUR sub-systems, each requiring frozen-dataclass serialization helpers + canonical dict builders + load-shape validation. Reviewer (GPT-OSS-120B) correctly flagged the LOC MED twice; operator E3 synthesis accepted the overage and retroactively amended the spec-card target. The issue wasn't author bloat — it was an under-estimate.
- Pre-check (next-round spec cards): for each module, list the blueprint sub-sections it implements → estimate ~40-80 LOC scaffolding per sub-section + ~80-120 LOC functional logic per sub-section → sum → add 20% overhead for type gates + docstring anchors. State target as ±25% of this sum.
- Origin: Round B RT-B-v2-MED-2 (GPT-OSS-120B, delta-2 review 2026-04-19). Closure: D-14 drift + retroactive spec-card amendment (topology.py ~180→~270, audit.py ~430→~900).

## E-006 — OpenAI Tier-1 rate limits constrain Codex-slot operation; gpt-4o-mini fallback codified

- First observed: 2026-04-19 (Round B)
- Frequency: 1 occurrence
- Severity: MEDIUM (process-level)
- Pattern: OpenAI account tiers gate TPM hard-limits. Tier-1 (≤$5 paid lifetime + ≤7 days account age) caps `gpt-4o` at 30K TPM per minute. Round-B initial dispatch payload was ~48K tokens, exceeding the cap. Trimmed-payload retry was 30.5K tokens, STILL over the cap (off by 0.5K). `gpt-4o-mini` has ~7x higher TPM on the same tier and passes a correctness+idiom review acceptably. Substitution is the E-004 primary/fallback pattern applied to the OpenAI slot — an access-tier workaround, not a design compromise.
- Pre-check: router.yaml `code_reviewer_1` row carries `primary: openai/gpt-4o` + `fallback: openai/gpt-4o-mini`. Dispatcher either inspects OpenAI tier pre-fire OR attempts primary and falls back on 429 TPM. Log substitutions to drift_log. Revert once operator's OpenAI account reaches Tier-2 (bumps gpt-4o to 450K TPM at $50 lifetime + 7 days).
- Origin: Round B D-13 drift (2026-04-19). Operator-side remediation: pre-pay + age account, or accept gpt-4o-mini as the durable Tier-1 choice.

## E-007 — Monkeypatch must target the imported name in the module under test, not the source module

- First observed: 2026-04-19 (Phase 2a)
- Frequency: 1 occurrence
- Severity: MEDIUM (test-correctness)
- Pattern: When a module does `from pipeline.x._y import func` at the top, the module binds `func` in its own namespace. Monkeypatching `_y.func` (the source) has no effect on calls from within the importing module. All 11 contract tests for the Privacy Router failed because they patched `_classifier_mod.classify_payload` instead of `_router_mod.classify_payload`. Fix: `monkeypatch.setattr(_router_mod, "classify_payload", ...)`.
- Pre-check: spec cards for any module that imports from a sibling internal module note the monkeypatch target explicitly: "patch `<module_under_test>.<imported_name>`".
- Origin: Phase 2a test run; 11 failures on first execution (all immediately fixed).

## E-008 — Contract detail strings in stubs must match spec literals exactly; substring tests mask divergence

- First observed: 2026-04-19 (Phase 2b)
- Frequency: 1 occurrence
- Severity: HIGH (spec-fidelity)
- Pattern: Canary stub produced `detail["reason"] = "v0.1_stub_no_corpus_interface_pinned"` while the spec declared `"v0.1_stub_no_corpus_interface"`. The test asserted `assert "v0.1_stub" in result.detail["reason"]` — a substring check that passed for both strings. The committee caught the divergence; the test did not.
- Pre-check: for every stub detail string, assert the full value (`== "exact_spec_string"`) not a substring. Substring checks are only acceptable for dynamic messages like exception text.
- Origin: Phase 2b Code Thesis Committee Finding 4.1 (OpenAI-OSS/GPT-OSS voice).

## E-009 — Undocumented sub-tag values in failure codes violate §6 spec; mixed-case sub-tags need explicit naming

- First observed: 2026-04-19 (Phase 2b)
- Frequency: 1 occurrence
- Severity: MEDIUM (spec-fidelity)
- Pattern: `check_key_presence` produced `sub_tag = "key_absent_and_empty"` for the case where both absent and empty keys exist. §6 only declares `.key_absent` and `.key_empty`. The undocumented value can cause downstream routing to silently skip alert paths that check exact sub-tag strings.
- Pre-check: every `sub_tag` value used in a detail dict must be listed in §6 as a declared sub-tag. When implementing a failure code with sub-tags, enumerate all possible sub-tag values in the spec before writing the conditional logic.
- Origin: Phase 2b Code Thesis Committee Finding 2.1 (Alibaba/Qwen voice). Fixed by mapping mixed case to `key_absent` (absent takes precedence).

## E-010 — Snapshot mutable env-var-derived state at construction; never re-read post-bind for fail-closed invariants

- First observed: 2026-04-19 (Round D v2 cycle)
- Frequency: 1 occurrence
- Severity: HIGH (same-uid widening of security invariants)
- Pattern: `_check_fs_allowed` originally union-ed `FILESYSTEM_ALLOWLIST | env_var_extension | caller_kwarg` on EVERY call. `verify_bindings_still_hold` invoked it at every gate. An actor who set `TILTH_ISOLATION_FS_ALLOWLIST_EXTEND=ntfs` post-bind could widen the allowlist mid-session. Any env-var-derived security invariant that is meant to hold for the lifetime of a construction MUST be snapshotted at construction and never re-read.
- Pre-check: any ENV-var-derived set/value that participates in a fail-closed check gets captured into an immutable field on the frozen construction (dataclass / closure state / etc.). Post-construction re-checks pass the snapshot explicitly; the re-check path does not call the env-var-reading helper. Pattern: `_check_fs_allowed(path, ext, *, include_env=False)` at check time; `include_env=True` only at bind. Reference: `isolation.OrgRootNamespace.bind` snapshots `frozenset(kwarg) | _read_env_allowlist_extension()` into `fs_allowlist_extend`; `verify_bindings_still_hold` passes `include_env=False`.
- Origin: Round D v2 Code Thesis Committee GPT-OSS-120B HIGH finding (dynamic env-var widening post-bind). Closed in v2 final fix + new adversarial probe `test_adv_post_bind_env_var_mutation_cannot_widen_allowlist`.

## E-011 — LOCKed crypto wrappers: use stdlib primitives inline rather than `bytes(buffer)` at call sites

- First observed: 2026-04-19 (Round E v1)
- Frequency: 1 occurrence
- Severity: HIGH (in-memory key material leak)
- Pattern: Round-A `hmac_sha3_512` wrapper enforces `isinstance(key, bytes)`. A SecretBytes-managed HMAC key is a bytearray; to satisfy the wrapper we originally wrote `hmac_sha3_512(bytes(key.view()), msg)`. `bytes(...)` creates an immutable copy that the GC retains indeterminately; SecretBytes.__exit__ cannot zero it. Round-A wrapper type-gate cannot be relaxed without a LOCK amendment.
- Pre-check: when a LOCKed wrapper forces a copy of secret material at the boundary, bypass the wrapper inline (`hmac.new(key_view.obj, msg, hashlib.sha3_512).digest()`) using the underlying bytearray that the SecretBytes manages. Enforce the wrapper's invariants (length floor, digest module) inline — do not relax them. `memoryview.obj` is documented Python API and returns the bytearray without copy.
- Origin: Round E Code Thesis Committee v1 GPT-OSS-120B HIGH-A (`sign_health_tuple` key-material leak via `bytes(key.view())`). Closed by `_stdlib_hmac.new(key_view.obj, ...)` with inline 32-byte length floor. New adversarial probe `test_adv_sign_health_tuple_does_not_materialize_bytes_key_copy`.

## E-012 — Boot-phase registration hooks must lock against post-boot replacement

- First observed: 2026-04-19 (Round E v1)
- Frequency: 1 occurrence
- Severity: HIGH (post-boot hostile-code hook swap)
- Pattern: `register_vault_commit_hook(hook)` started as a plain setter. Between the boot-time §2 Vault registration and the first `checkpoint()` call, any same-uid code could silently overwrite the hook and redirect interrupted-state writes. Trusted-operator boundary (§3.11 v5) says hostile same-uid Python is out of scope, but the window is cheap to close.
- Pre-check: any registration hook that §2/§4/§5 is expected to install ONCE at boot gets a companion `lock_<hook>()` function that sets a module-level `_<hook>_locked = True` flag; subsequent register calls raise a dedicated `<Hook>Locked` exception. Test-only unlock helper `_unlock_<hook>_for_tests()` uses underscore prefix and is NOT in `__all__`; fixtures call it both before and after yield.
- Origin: Round E Code Thesis Committee v1 GPT-OSS-120B HIGH-C. Closed by `VaultCommitHookLocked` + `lock_vault_commit_hook`. New adversarial probe `test_adv_vault_hook_registration_after_lock_raises`.

## E-013 — Per-rotation grace timers: list, not single-slot

- First observed: 2026-04-19 (Round E v1)
- Frequency: 1 occurrence
- Severity: MEDIUM (secret-lifetime bound violation)
- Pattern: `_rotation_timer: Timer | None` plus a `rotate_hmac_key` that cancels the prior timer when scheduling a new one left earlier old keys un-zeroed past their own grace window on rapid back-to-back rotations. Each rotation's captured old_key_id must be zeroed after ITS OWN grace window, independent of later rotations.
- Pre-check: grace-timer fields for rotated secrets are `list[threading.Timer]` and `list[str]`, not single-slot. Each rotation appends without cancelling priors; each timer closure captures its own id and calls the zero helper. Shutdown path cancels all pending timers and defensively zeroes all queued ids.
- Origin: Round E Code Thesis Committee v1 GPT-OSS-120B MED-B. Closed by `_rotation_timers: list`. New adversarial probe `test_adv_rapid_rotations_every_old_key_zeroed_after_own_grace`.

## E-014 — Cross-family exception-taxonomy coherence

- First observed: 2026-04-19 (Round E v1)
- Frequency: 1 occurrence
- Severity: MEDIUM (cross-module exception-coherence)
- Pattern: `CrossFilesystemRename(RuntimeError)` originally inherited directly from `RuntimeError`, so `except IsolationError` did not catch it despite the failure code being in the F-ISO-* family. Downstream code that wanted to catch "any isolation failure" had to list this sibling separately.
- Pre-check: when adding a new exception whose failure code is in an existing family, inherit from that family's established parent (`IsolationError`, `SessionError`, `KeyStoreError`, etc.), not `RuntimeError` directly. If the family parent uses kw-only init and the new error needs positional init, inherit from the grandparent family parent, not from a kw-only sibling.
- Origin: Round E Code Thesis Committee v1 Gemini-2.5-Pro MED-1. Closed by `CrossFilesystemRename(IsolationError)`.

## E-015 — Blueprint-mandated forward-compat scaffolding may appear dead in the current round

- First observed: 2026-04-19 (Round E v2)
- Frequency: 1 occurrence
- Severity: LOW (dead-code heuristic false positive)
- Pattern: `_SessionRuntime._hmac_key_buffer: bytearray | None` is defined and the signal handler conditionally zeroes it, but no round currently populates it (start_session zeroes its local buffer right after `keystore.store`). A reviewer's dead-code heuristic flags this as unused. The field is blueprint-LOCKED (§4.5 v2) and will be populated by §4.6.1 M7 wire layer during active LLM signing.
- Pre-check: when a reviewer flags a field as dead code, check whether the blueprint mandates it and whether a later round is expected to populate it. If yes, keep the field and expand its docstring to name (a) the current pre-wire no-op status, (b) the round that will populate it, (c) the test that simulates the future active-use window. Do NOT remove to satisfy the heuristic — blueprint drift is more expensive than a doc comment.
- Origin: Round E Code Thesis Committee v2 GPT-OSS-120B LOW. Acknowledged; docstring expanded in both `_SessionRuntime._hmac_key_buffer` and `_unified_signal_handler` step 1.

## E-016 — Classifier-regex drift when new provider model slugs land

- First observed: 2026-04-20 (Midas classifier-regex drift patch)
- Frequency: 1 occurrence
- Severity: MEDIUM (process-level gate bypass)
- Pattern: `router.yaml` is the sole source of truth for model bindings, but DET-tier gates that classify model slugs into provider families carry their own regex alternation (e.g. `gpp_det.FAMILY_MAP_RULES`). When a new provider-model slug is added to `router.yaml` whose family is already represented but whose name does not match the existing alternation (e.g. `openai/gpt-5.1` vs regex `gpt-4|gpt-3|codex|o\d`), the classifier falls through to `UNCLASSIFIED(...)`. FAMILY-TAXONOMY then reports an inflated family count and the DET gate FAILs on a true-positive-but-wrong-reason — the taxonomy is fine; the classifier drifted. Every future provider-model addition to `router.yaml` is an opportunity for this drift.
- Pre-check: every PR / plan round that adds a new model slug to `router.yaml` MUST also run `classify_family(<new_slug>)` from `gpp_det` and assert the result is the intended family (not `UNCLASSIFIED(...)`). Prefer generalized regex forms (`gpt-\d`, `o\d+`) over enumerated version lists — alternations that enumerate specific versions (`gpt-3|gpt-4`) are drift traps. When adding the first member of a new family, add a new FAMILY_MAP_RULES row AND a new test row in `test_classify_family_*`. A future §4 AST-lint rule will enforce this mechanically by diffing `router.yaml` model slugs against `FAMILY_MAP_RULES` coverage at check time.
- Origin: 2026-04-20 Midas patch — `test_run_gpp_det_on_real_plan_dir_passes` failed after `openai/gpt-5.1` was added to `router.yaml` on 2026-04-19 as Red-Team escalation. Fix generalized `^openai/(codex|gpt-4|gpt-3|o\d)` → `^openai/(codex|gpt-\d|o\d)` covering gpt-3..gpt-9 and any future gpt-N. Red test `test_classify_family_matches_openai_gpt_5_1` + adversarial `test_adv_openai_oss_still_wins_over_openai_rule` bracket the fix.

## E-024 — Spec-card LOC/test-count floors under-estimate by ~1.5× when modules ship Protocols + V1 rebind-resistance + E-023 Threat-model docs

- First observed: 2026-04-20 (§5 Round 2 state_checkpoint LOCK, filed as candidate)
- Frequency: 6 occurrences (§5 R2 state_checkpoint +58%, §5 R3 run_lifecycle +68%, §5 R4 seat_runner, §5 R5 revision_loop, §3 Scout R5 channel_c+d, §3 Scout R6 channel_e_rss +49%/+51%, §3 Scout R7 channel_f_websearch — pattern held through R7)
- Severity: MEDIUM (process-level; spec-card calibration)
- Pattern: Spec-card LOC targets sized by whole-module estimate systematically under-count when the module (a) declares its own Protocol surface for Vault/Clock/reader/writer injection (E-017 pattern), (b) implements inline-literal V1 rebind-resistance for threshold constants, AND (c) ships a `test_adv_*` file that documents deferred-scope threat models (E-023 pattern). Each discipline adds scaffolding: Protocols → fake implementations per test + Protocol-contract tests; V1 rebind-resistance → rebind-attempt adversarial tests; E-023 Threat-model docs → honest `test_adv_*` entries citing each deferral. Combined overhead lands at ~1.5× the naive spec-card floor across 6 consecutive rounds. Formal elevation at 6th firing per E-005's "process-level lesson" precedent. Extends E-005 (LOC targets must be built sub-system-wise) with a concrete multiplier for the Protocol+V1+E-023 trident.
- Pre-check (spec-card template §11 clause): spec cards for modules that apply ANY TWO of {E-017 injected Protocols, V1 rebind-resistance, E-023 deferred-scope `test_adv_*` docs} declare LOC/test-count floors THEN multiply by 1.5× for the "expected" ceiling. Format: `floor ≥ N tests, expect ~1.5N given E-024 multiplier`. Spec-card target LOC: `target ±25%` applied to the 1.5× figure, not the naive figure. Avoids committee HIGH/MED findings flagged as LOC-overrun that are actually E-024 calibration gaps. LOC under-run (landing below the floor) is a genuine signal to investigate; LOC at 1.5× the floor is expected.
- Origin: Filed as E-024 candidate at §5 Round 2 state_checkpoint LOCK (2026-04-20, Gemini R5 LOC-estimation finding, 553 LOC actual vs 210-350 spec). Second data point §5 Round 3 run_lifecycle (+67.9% source, +106.5% adversarial). Third through sixth firings: §5 R4 seat_runner, §5 R5 revision_loop, Scout R5, Scout R6 channel_e_rss (+49%/+51%, 103 tests vs 69 floor), Scout R7 channel_f_websearch (131 tests, 1095 LOC — Midas self-lock memo logs "sixth firing (1.5× multiplier holds)"). Spec-card scout_round_8_capstone_dispatcher.md already bakes in the multiplier: "floor ≥ 70 tests, expect ~105 given E-024 1.5× multiplier — sixth firing holds" — formal elevation ratifies the discipline.

## E-025 — Smoke-test the live `pipeline/` tree BEFORE writing tests when shipping a new AST-lint rule

- First observed: 2026-04-20 (ARCH-05 AST-lint walker-intensive R6/R7)
- Frequency: 2+ occurrences (ARCH-05 R6 builtins-attribute-form miss + R7 channel_a false positive; reapplied preemptively at Scout R6 / R7 / R8)
- Severity: MEDIUM (test-fixture blind-spot)
- Pattern: AST-lint rule test suites built fixture-first (hand-crafted `tmp_path` modules exercising the rule) pass green while the live `pipeline/` tree carries patterns the fixtures never anticipated. Two firings at ARCH-05: R6 missed builtins-attribute-form usage; R7 flagged Channel A's legitimate pattern as a false positive. Both were discovered only when `scripts/run_lint.sh` ran against the live tree AFTER the fixture suite was green. Adding a live-tree smoke pass to the BUILD step costs one extra `scripts/run_lint.sh` invocation and catches both fixture-blindness classes.
- Pre-check: spec cards for AST-lint rules include a `Live-tree smoke` item in the Done definition: "scripts/run_lint.sh against the live pipeline/ tree exits 0 AND every intended-true-positive is caught AND every legitimate-pattern is permitted." Fixtures are the RED→GREEN loop; live-tree smoke is the adversarial pass. For version-pin tests specifically, use range-checks (`rN >= 6` via tuple comparison) not equality-checks so new-round additions don't cascade into version-pin failures across downstream tests.
- Origin: ARCH-05 R6/R7 Midas implementation round, 2026-04-20. Filed as candidate; applied from start at Scout R6 via `test_version_pin_rN_ge_6` and at Scout R7 via `test_version_pin_rN_ge_7`. Reaffirmed at Scout R8 spec card (`test_version_pin_rN_ge_8`). Not yet formally elevated (two rounds; pattern holds).

## E-026 — Use `__module__` lineage inspection for shared-Protocol provenance, not `is` identity under `sys.modules` reload

- First observed: 2026-04-20 (Scout R5 candidate; R6 second firing; R7 third firing)
- Frequency: 3 occurrences (Scout R5 channel_c+d candidate filing; Scout R6 channel_e_rss promoted to formal on second firing; Scout R7 channel_f_websearch third firing — matches E-023's 2-firing-to-formal precedent)
- Severity: MEDIUM (test-fragility under full-suite reload)
- Pattern: Scout rounds 3+ share Protocols (e.g., `FDBroker`, `ClockFn`, `SessionLike`) across channel modules. Tests verifying "channel_e imports FDBroker from channel_a, not re-declares it" naively use `is` identity: `assert channel_e.FDBroker is channel_a.FDBroker`. Under full-suite execution, `importlib.reload(module_under_test)` elsewhere in the suite OR `sys.modules.pop(...)` in adversarial tests creates a new class object that passes `isinstance(obj, FDBroker)` but fails `is` identity. The import-hygiene intent — verifying lineage, not object identity — is better expressed via `__module__` lineage: `assert channel_e.FDBroker.__module__ == "pipeline.scout.channel_a_federal_apis"`. This is the documented-Python contract and is stable across reloads. Formal elevation at 3rd firing matches E-023's promote-at-second-firing precedent (E-023 was promoted formal on second firing per ARCH-04 → §5 R2 chain).
- Pre-check (spec-card template §11 clause): spec cards for any module that imports Protocols/types from sibling modules include a `TestSharedProtocolReuse::test_<symbol>_origin_is_<source_module>` entry that asserts `<symbol>.__module__ == "<fully.qualified.source.module>"`. NEVER use `is` identity for cross-module Protocol-lineage checks. NEVER use `importlib.reload(module_under_test)` in adversarial tests that the shared-Protocol test suite will later depend on. The Round 7 aftermath specifically showed the `sys.modules` eviction cascade propagating into downstream tests — any round shipping shared Protocols MUST apply E-026 from the start.
- Origin: Scout R5 channel_c+d filed E-026 as candidate (first observation). Scout R6 channel_e_rss LOCK memo promoted to formal on second firing (daily_logs/2026-04-20.md line 689: "E-026 promoted from Round-5 candidate to formal on second firing"). Scout R7 channel_f_websearch applied it from start; Scout R8 capstone_dispatcher spec card §126 cites it as "fourth firing candidate" and pre-flights the `sys.modules` eviction cascade as an engineering risk. Formal entry here ratifies the R6 promotion.

## E-027 — Qwen3-32B on Groq returns non-rubric verdict tokens on consolidated payloads >~80k prompt tokens (+ degenerate `<think>`-block repetition when reasoning_effort unset)

- First observed: 2026-04-20 (vault_batch_1 parent — partial truncation, findings arrived but rubric drift noted)
- Frequency: 3 formal observations + 2 retry-confirmed. (1) vault_batch_1 parent ~120k → partial. (2) vault_batch_1_redispatch ~124k → `{"verdict": "LOCKED"}` 20 completion tokens; L-011 transport-retry with `reasoning_effort="none"` + verdict-token reinforcement addendum returned identical malformed `LOCKED` at 16 completion tokens. (3) vault_batch_3_remediation_phase2 mirror_verify ~96k → **new sub-pattern**: when `reasoning_effort` is *not* set, qwen's `<think>` block entered a degenerate text-repetition loop (same ~80-char sentence cycled ~200× with minor mutation, exhausting the full 8000-token completion budget before emitting any JSON). First retry at `temperature=0.05 + max_tokens=3000` reproduced the loop (shorter before exhaustion, still no verdict). Second retry at `reasoning_effort="none" + max_tokens=1500 + system-prompt <think>-ban` returned `{"verdict":"LOCKED"}` at 12 completion tokens — same semantic-PASS shape as E-027 firing #2. Other 4 seats (llama-3.3-70b / gemini-2.5-pro / gemini-2.5-flash / gpt-oss-120b) returned rubric-compliant verdicts on each identical payload — qwen-specific ceiling, not a payload-size issue writ large.
- Severity: MEDIUM (cosmetic rubric violation; semantic intent remains interpretable — "LOCKED" from a promote-framed ask reads as PASS — but the verdict field contract is broken; the `<think>`-block degenerate-repetition sub-pattern is more severe in isolation because the raw response carries NO JSON, requiring retry-mitigation before a verdict exists at all)
- Pattern: Qwen3-32B reasoning-mode tokens silently consume the completion-token budget on large consolidated payloads. Two failure shapes surface depending on how `reasoning_effort` is set: (a) `reasoning_effort="none"` — model emits a minimal non-rubric verdict token (semantic-PASS, typically `"LOCKED"`), rubric field contract broken but promotion-aligned; (b) `reasoning_effort` unset (default medium/high) — model may enter a degenerate text-repetition loop inside `<think>`, burning the full completion budget without emitting any closing JSON. Shape (b) shows up when the payload also hits a multi-invariant module review (e.g. mirror_verify's §2.4 seed manifest + §2.5 trust-root mirror + §9 step 6 triple); shape (a) shows up on single-invariant / consolidated-amendment reviews. Reinforcing the rubric in a system-prompt addendum does not fix shape (a); forcing `reasoning_effort="none"` bypasses shape (b) but collapses into shape (a). Three mitigations (per `engineering_process_v0.1.md` §3.1): (1) split the dispatch per-module so each packet stays under the threshold; (2) accept semantic-PASS convention for qwen only, documenting the soft spot in the promotion row's `committee_tally` citation; (3) substitute qwen for a different cross-family reviewer for that round only (round-local deviation, not a roster amendment). Default Option 1 when per-module split is clean; Option 2 when split would fragment cross-module findings; Option 3 only when 1 and 2 are both unavailable. **New Option 2a (for shape (b) degenerate-repetition)**: when the initial qwen response burns the full completion budget on `<think>`-block repetition without emitting JSON, retry with `reasoning_effort="none"` + `max_tokens<=2000` + a system-prompt `<think>`-ban addendum; accept the resulting minimal semantic-PASS verdict under the same convention as Option 2.
- Pre-check (spec-card template §11 clause): any consolidated committee dispatch targeting `code_reviewer_2 = qwen3-32b` MUST include a `prompt_token_estimate` field computed as `len(user_content_chars) / 3.7`. If the estimate exceeds 80,000, the dispatch README MUST declare which of the three mitigations applies (`dispatch_shape: per_module_split` / `qwen_semantic_pass_accepted` / `qwen_substituted_for_this_round`). Dispatching a consolidated payload over the threshold without declaring a mitigation is a scope-honest discipline violation and must be logged in the round's `pre_dispatch_disclosure.md`. Note: `router.yaml` line 77 self-falls-back on Groq Dev tier (no same-family alternative in catalog as of 2026-04-22) — substitution under Option 3 must be sourced cross-family with round-local deviation logging, not via the routine fallback path.
- Sibling to: L-011 (transport-class retry carve-out — the retry that confirmed this is qwen-intrinsic, not a one-shot transport glitch); E-016 (classifier-regex drift when new provider model slugs land — both are provider-catalog-reality lessons); E-004 (router primary/fallback discipline — this lesson extends the discipline with payload-size context).
- Origin: vault_batch_1 parent round 2026-04-20 (first observation, partial truncation); vault_batch_1_redispatch 2026-04-22 R1 qwen malformed at 124k prompt tokens (second observation) + L-011 transport-retry with reasoning suppression + addendum reinforcement returning identical result (confirmation that no in-prompt mitigation fixes the ceiling). vault_batch_3_remediation_phase2 2026-04-22 R1 qwen mirror_verify at ~96k prompt tokens (third observation) — new sub-pattern: degenerate `<think>`-block text-repetition when `reasoning_effort` unset; mitigation via `reasoning_effort="none"` + `max_tokens<=2000` + `<think>`-ban addendum produces the same semantic-PASS `{"verdict":"LOCKED"}` shape as firing #2. Synthesis + adjudication documented in `pipeline/validation/code_reviews/vault_batch_1_redispatch_2026-04-22/synthesis.md` §3 + `pipeline/validation/code_reviews/vault_batch_3_remediation_phase2_2026-04-22/synthesis.md` §D-08. Engineering-process-doc §3.1 added in the same filing pass as firing #2; Option 2a added at firing #3.

## E-029 — Protocol-first + single-gate-scope dispatches produce the cleanest cycle-1 outcomes

- First observed: 2026-04-21 (Logician v2.2 Wave 3 F-AMDT-05 first zero-retry cycle-1)
- Frequency: 6 occurrences (F-AMDT-05 / F-AMDT-10 / F-AMDT-11 / F-AMDT-08 / F-AMDT-09 / F-AMDT-04 — six consecutive Wave-3/Wave-4 gates, each via independent single-gate 5-family dispatch, each cycle-1 all-PASS)
- Severity: MEDIUM (process-level dispatch discipline; governs bundle-vs-split decisions)
- Pattern: Multi-gate bundle dispatches (Wave-1 F-AMDT-02/03 joint; Wave-2 F-AMDT-01/06/07/12 joint) took 1-2 transport retries each to reach cycle-1 all-PASS. When Wave-3 shifted to single-gate-per-dispatch AFTER Protocol surface (`pipeline/logician/gates/_protocols.py`) was pre-landed in the prior session, cycle-1 outcomes went cleaner by every measure: zero transport retries on 5 of 6 gates (F-AMDT-04 had 1 gemini-flash 503, still cycle-1 PASS), zero semantic findings at any severity on 5 of 6 gates, zero cycle escalations. The pattern reads as: **narrow reviewer scope + shared infrastructure already validated = fewer hallucination vectors**. Bundled dispatches force each reviewer to hold N gate modules + N test files + shared helpers in context simultaneously; single-gate dispatches keep the review packet at O(one gate + `_protocols.py`), reducing the "which module did the reviewer mean?" ambiguity that showed up in Wave-2 F-AMDT-12's qwen hallucination-retry (referenced a module not in the packet). Combine this with L-012's scope-honest pushback (session-split decisions) and the dispatch pattern is: share infrastructure across sessions (pre-build Protocols, fake helpers, test fixtures in session A); dispatch one gate per committee round in session B. The 6-gate run from Wave-3 Session A-tail + Session B vindicates both disciplines jointly.
- Pre-check (spec-card template §11 clause): spec cards for committee-dispatched gate modules declare `dispatch_shape: single_gate` explicitly, with a reference to the shared Protocol module the gate imports from (e.g. `shared_protocols: pipeline/logician/gates/_protocols.py @ sha3_512[:16]=<hash>`). If the spec card proposes bundling N gates in one dispatch, the justification must name the shared surface being amortized AND assert the surface has been cross-family-validated in a prior round (otherwise L-012 session-split applies). For Thesis rounds that author a new shared Protocol surface, the first gate that imports it MUST be dispatched alone to validate the Protocol contract cross-family before downstream gates ride on it. Amendment-enforcement gates (F-AMDT-* family) specifically inherit this discipline: single-gate dispatch is the default; bundling requires a `bundle_justification:` field in the spec card.
- Sibling to: L-012 (scope-honest pushback — session-split vs single session); E-017 (injected-Protocol pattern — Protocols ARE the shared surface that make single-gate dispatches viable).
- Origin: Logician v2.2 Wave 3 + Wave 4 arc, 2026-04-21. Six-firing confirmation: F-AMDT-05 (`b1e0c448251c0c73`, 0 retries, 0 findings — first observation), F-AMDT-10 (`e2d88d06a624f4b1`), F-AMDT-11 (`dadbacf61b347d76`), F-AMDT-08 (`e1398bee597153a2`), F-AMDT-09 (`12dd8ed02e20e136`), F-AMDT-04 (`d66f21d9e1d7c83e`, 1 gemini-flash transport retry, 0 findings). Per-gate LOCK roster documented in `pipeline/handoffs/logician_v2_2_queue_closed_2026-04-21.md` table "Per-gate LOCK roster with cycle-1 discipline". Six consecutive cleanest-cycle outcomes is a durable pattern; formal elevation at 6th firing matches E-024's promote-at-6th-firing precedent.

## E-030 — Pre-dispatch companion-code SHA/LOC pins MUST resolve to lock_history.v1.jsonl rows

- First observed: 2026-04-21 (§4 Logician v2.2 Consolidated Blueprint Amendment pre-dispatch self-check)
- Frequency: 1 occurrence (pre-dispatch self-check prevented the miss from reaching committee dispatch)
- Severity: HIGH (spec-fidelity; would have tripped cross-artifact SHA check under any reviewer's criterion-6 no-hidden-scope pass)
- Pattern: Consolidation amendments and multi-module LOCK handoffs often declare `companion_code:` or `companion_code_complete:` front-matter tables pinning files by SHA + LOC (e.g., `pipeline/logician/gates/__init__.py (Wave 2 pin: 104 LOC, sha3_512[:16]=11ad867f5ac0da5d)`). The pin is only meaningful if it resolves to an actual `pipeline/engineering/lock_history.v1.jsonl` row under the same hash prefix — otherwise the pin is unverifiable, which violates the no-hidden-scope criterion every Gemini-Pro-class reviewer's cross-artifact check fires on. Live re-export surfaces (package `__init__.py` files that re-export from child modules) commonly have NO standalone lock_history row — they are implicitly pinned by the per-child-module LOCK rows that populate them. Declaring an invented SHA pin for such a surface is worse than honest annotation: it looks authoritative and fails the first reviewer cross-check. Caught once at the v2.2 consolidation pre-dispatch 6-criteria self-check and fixed via honest annotation: "no standalone lock_history row — live re-export surface; pinned implicitly by the 12 per-gate LOCK rows that populate it." Would have tripped Gemini-2.5-Pro's R4 criterion-6 check on first dispatch.
- Pre-check (spec-card template §11 clause + pre-dispatch self-check): before dispatching any consolidation / bundle / multi-module LOCK handoff, the author runs a companion-code pin verification loop: for every entry in the `companion_code*` front-matter table, grep `pipeline/engineering/lock_history.v1.jsonl` for the claimed `code_sha3_512_prefix`; if a row exists, the pin is verified; if no row exists, EITHER (a) the pin is invented and must be removed / annotated honestly, OR (b) the file is a live re-export surface with no standalone LOCK, in which case the entry must be annotated "no standalone lock_history row — live re-export surface; pinned implicitly by <list of per-child-module LOCK rows>". Applies to: §N v2.X consolidated amendments, paired-commit compound-transaction handoffs, any LOCK handoff whose `companion_code*` front-matter declares SHA/LOC pins. Complements L-006 (preflight enforcement-layer existence audit) — that audit checks whether cited mechanisms EXIST as infrastructure; E-030 checks whether cited file pins RESOLVE in the ledger. Both are pre-dispatch artifact-truth checks.
- Sibling to: L-006 (preflight enforcement-layer existence audit — both are pre-LOCK truth checks against the on-disk state); L-005 (two-audit cycle — E-030 prevents the miss from consuming a cycle).
- Origin: §4 Logician v2.2 Consolidated Blueprint Amendment pre-dispatch 6-criteria self-check, 2026-04-21. DRAFT's `companion_code_complete:` front-matter + §10 paired-commit table claimed `pipeline/logician/gates/__init__.py (Wave 2 pin: 104 LOC, sha3_512[:16]=11ad867f5ac0da5d)` — the 11ad867f5ac0da5d prefix did not appear in any of the 90 pre-existing lock_history rows. Fix: replaced the invented pin with honest annotation pointing at the 12 per-gate LOCK rows (F-AMDT-01..12) that populate the re-export surface. Self-check caught the defect before dispatch; committee dispatch subsequently returned 5/5 PASS cycle-1 with zero findings (see E-029 sixth firing — the consolidated round was the cleanest in the v2.2 arc). Spec-card template §11 amended with companion-code pin verification clause same commit as this lesson filing.

---

(End of current entries — next-round committee dispatches check these before starting. Candidates pending formal elevation: E-017 injected-Protocol pattern — referenced ≥7 times but not yet filed here; E-023 isomorphic-to-deferred-scope → honest docs — referenced ≥6 times but not yet filed here. Backfill recommended at next review-lessons consolidation pass.)
