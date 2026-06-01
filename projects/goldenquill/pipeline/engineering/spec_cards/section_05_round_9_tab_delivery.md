# Spec card — pipeline.loop.tab_delivery (Round 9: §4.11 three-tab envelope ordering + signing dispatcher)

**STATUS:** PRE-STAGED 2026-04-21 (parallel-dispatch partner to §5 Round 8 cascade — see `section_05_round_8_cascade.md`)

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal section: §4.11 v3 `assemble_and_deliver` (blueprint lines 691–747) — inline-literal runtime tab-order check + module-load integrity assert + post-write envelope-hash verification
- Supporting sections: §3.2.6 `TabEnvelope` (lines 353–366, v2 `tab_ordering` typed `Final`); §3.5 banned pattern — `No TabEnvelope(` call with inline tuple/list as `tab_ordering` (line 381, A-v1-06 closure); §4.1 step 11 (tab delivery follows `report_signed`, precedes `tabs_delivered`); §6 F-PIPE-16 (`tab_envelope_ordering_violation`) + F-PIPE-01 (`run_state_corrupt` — post-write hash mismatch path, B-v1-09 closure); §8 `TAB_ORDERING: Final[tuple[...]]` constant with module-load assert; §9.6 test anchor `test_tab_envelope_ordering_runtime_assertion`
- v4 eval-mode shield: §4.15 export-bundle exclusion (line 916) — `assemble_and_deliver` MUST assert `run_state.mode == "submission"` at entry; eval-mode reaching R9 raises F-PIPE-21 with trigger `"eval_run_reached_tab_delivery"`
- Closure rows: B-v1-09 (post-write envelope-hash verify), A-v1-06 (Final-typed ordering + AST-grep banned pattern), V1 (inline-literal rebind-resistance — already discharged in Round 1 `TabEnvelope.__post_init__`), B-v1-17 (module-load integrity assert — already discharged in Round 1 `config.py`)
- §2 vault primitives consumed: `vault_write` dispatcher (`pipeline/vault/vault_write.py` line 127 — SIMPLE intent path, no `txn_token`); vault_read (from `pipeline.vault.vault_query_skill`); identity_tuple (§2 Round 1 — passed through vault_write)
- §2 compound_commit integration: OUT OF SCOPE for R9 — see Cedar / compound_commit carve-out below
- §0.5 Interface index: NOT YET ON DISK at `pipeline/blueprint/v0.1/section_00_5_interface_index.md` — Round 1 `pipeline/loop/__init__.py` serves as de-facto re-export index; `TabEnvelope` LOCKED there per §3.2.6 import line

**Blueprint hash-at-card:**
- `section_05_pipeline.md`: `34ef007f3ab6d59d` (mirrors R7 + R8 — blueprint unchanged since §5 v6 LOCK)

**Spec-card version:** v1 (pre-staged 2026-04-21 at §5 Round 7 SELF-LOCK; parallel-dispatch partner to R8 cascade)
**Round:** §5 Round 9 — tab_delivery (three-tab envelope ordering + signing dispatcher via vault primitives)
**Depends on:** Round 1 (`TabEnvelope`, `TAB_ORDERING`, `F_PIPE_16`, `F_PIPE_01`, `F_PIPE_21`, `RunState`, `RunMode`, `SeatKind`); §2 vault `vault_write` + `vault_read` + `identity_tuple` primitives (SIMPLE-intent surface only); Round 2 `ClockProtocol` + `VaultWriteCallable` + `VaultReadCallable` (no new Protocols anticipated). **NO dependency on Round 7 `rate_limiter` or Round 8 `cascade`** — parallel-safe by construction.

## Operator choice — parallel-dispatch context

R7 pre-stage flagged tab_delivery as "Round 8 candidate B"; R8 cascade landed as candidate A. Per operator PARALLEL decision 2026-04-21, both A (cascade) and B (tab_delivery) are now ACTIVE simultaneously in separate Code windows. R9 ships tab_delivery under its natural round number. Nothing Candidate-B-specific from R8's spec card carries forward — that branch is the one now being realized here.

---

## Summary

Ship `pipeline/loop/tab_delivery.py` — §4.11 three-tab envelope ordering + signing dispatcher. Per blueprint §4.11 v3 (lines 691–747): hash the three payload files (live_radar / deep_brief / council_draft) from their vault paths; construct a `TabEnvelope` referencing the `TAB_ORDERING` Final constant; stamp `envelope_sha256` via canonical-bytes hash; **verify tab_ordering against an INLINE LITERAL tuple (not the module attribute)** — V1 rebind-resistance discipline; `vault_write` the envelope under `intent="state-success"` (interim per blueprint OQ-3 until a dedicated `tab-envelope-write` intent lands in a future Section 2 amendment); post-write `vault_read` + `TabEnvelope.parse` + `envelope_sha256` equality check (B-v1-09 closure); return the envelope. Fail-closed on tab-order violation (F-PIPE-16), post-write hash mismatch (F-PIPE-01), or eval-mode entry (F-PIPE-21).

Public API (proposed — pulled from blueprint §4.11 lines 710–746; confirm at ORIENT):

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class TabSigningResult:
    envelope: TabEnvelope
    stored_envelope_hash: str          # post-write re-read hash (equals envelope.envelope_sha256)
    vault_path: str                    # f"pipeline/{run_id}/tab_envelope.json"
    written_at_iso: str                # clock-stamp at successful vault_write

class TabOrderViolation(Exception): ...  # wraps F_PIPE_16 with call-site context [NEEDED from §0.5]
class TabDeliveryError(Exception):  ...  # wraps F_PIPE_01 post-write-mismatch path [NEEDED from §0.5]

def deliver_tab(
    *,
    run_state: RunState,
    vault_read: VaultReadCallable,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    hash_file: HashFileCallable,            # injected — reads payload path, returns SHA-256 hex
) -> TabSigningResult: ...
```

**Protocols (candidate — confirm at ORIENT):**
- `HashFileCallable(Protocol, runtime_checkable)` — `__call__(path: str) -> str`. Injection seam for the three payload-hash reads; lets tests pin hashes deterministically. Reuses E-017 injected-Protocol pattern (eighth-plus firing).
- Reuses Round 2's `ClockProtocol` + `VaultReadCallable` + `VaultWriteCallable` — no new clock/vault Protocols.

**Tab-order invariant (inline-literal, blueprint §4.11 line 730):**

```python
# V1 closure — inline literal, monkeypatch-resistant
if envelope.tab_ordering != ("live_radar", "deep_brief", "council_draft"):
    raise F_PIPE_16(trigger="tab_envelope_ordering_violation", details={"observed": envelope.tab_ordering})
```

## §5 v6 compliance decisions (must confirm at ORIENT)

1. **Result shape — `TabOrder` constant vs `TabSigningResult` dataclass.** Blueprint §4.11 does not name a result dataclass; `assemble_and_deliver` simply returns `TabEnvelope`. R9 adds `TabSigningResult` as a thin wrapper so callers can assert post-write hash + vault path in one object. [NEEDED: confirm wrapper is acceptable, or keep return type as bare `TabEnvelope` and expose `stored_envelope_hash` via a side-channel.]
2. **`write_mode` for envelope write.** Blueprint §4.11 does not specify. Default Section 2 v7 behaviour for state writes is `overwrite`. Propose `write_mode="write-if-absent"` since each `run_id` produces exactly one envelope — CAS-style duplicate-write protection. [NEEDED: blueprint silent; propose write-if-absent.]
3. **Canonical-bytes contract.** `TabEnvelope.canonical_bytes()` and `TabEnvelope.canonical_bytes_without_self_hash()` are referenced in blueprint §4.11 (lines 724, 735) but NOT yet defined on the Round 1 `TabEnvelope` dataclass (see `pipeline/loop/types.py` line 310). R9 must add them OR R9 spec card flags this as a Round 1 backfill. Propose: R9 ships them as module-level helpers (`_canonical_bytes(envelope)` + `_canonical_bytes_without_self_hash(envelope)`) rather than extending Round 1's frozen dataclass post-LOCK. Follow Round 2 + Round 7 canonicalizer template: `json.dumps(asdict(envelope), sort_keys=True, separators=(",",":"))`.
4. **Payload-path templates.** Blueprint §4.11 hardcodes three vault paths: `vault/fund_radar/{run_state.run_id_date}/live_radar.json`, `vault/deep_brief/{run_state.run_id}/brief.md`, `vault/pipeline/{run_state.run_id}/iter_{final_N}/scribe_draft.md`. `run_state.run_id_date` and `final_N` (last iteration number) are not yet present on Round 1 `RunState`. [NEEDED: confirm these derivations — `run_id_date` from ULID prefix? `final_N` from `run_state.iteration_count` at phase=`report_signed`?]
5. **`intent="state-success"` interim pattern.** Blueprint §4.11 line 736 explicitly flags this as interim until a dedicated `tab-envelope-write` intent is added in a future Section 2 amendment (OQ-3). R9 matches; document the interim stance in module docstring. No-op once the intent lands.
6. **eval-mode shield.** §4.15 line 916 mandates `assert run_state.mode == "submission"` at `assemble_and_deliver` entry; eval-mode raises F-PIPE-21 with trigger `"eval_run_reached_tab_delivery"` (already in `F_PIPE_21_TRIGGERS` per Round 1 config.py line 151). R9 inline-literals the comparison (`"submission"`) per V1 discipline.

## Cedar / compound_commit carve-out (EXPLICIT — parallel-safe guarantee)

**R9 unit tests use mocked vault primitives only.** `vault_write` + `vault_read` are injected as `VaultWriteCallable` / `VaultReadCallable` kwargs and stubbed with deterministic fakes in tests. R9 does NOT exercise the §2 `compound_commit` predicate, the Cedar policy evaluator, the `commit_compound_txn` ceremony, or the M15 signed-commit ledger. The blueprint-level "signing path" through `vault_write` is a SIMPLE-intent path (`intent="state-success"`, no `txn_token`) — compound plumbing is NOT engaged at the tab-delivery layer in v0.1.

Full Cedar + compound_commit end-to-end integration for the tab-delivery write path lives in the **Group 9 integration suite** (§5 capstone integration, future round), NOT in R9 scope. This carve-out decouples R9 from the in-flight §2 vault committee dispatch and the stalled M15 signed-commit ceremony — R9 can self-LOCK without blocking on either.

**Guardrail:** IF the §2 Vault committee dispatch surfaces any interface-level finding that changes `vault_write`'s public signature, `TabEnvelope` canonical-bytes contract, or the SIMPLE-intent dispatch path, R9 DISPATCH PAUSES until the §2 finding is resolved. Cross-reference: `pipeline/engineering/spec_cards/vault_dispatcher_commit_compound_txn.md` and the active §2 committee handoff in `pipeline/handoffs/`. R9 parallel dispatch is safe only while §2's public surface is unchanged.

## Public surface + invariants

- `deliver_tab` is **one-shot** per `run_id` (write-if-absent; duplicate-dispatch raises `VaultWriteExists` which R9 propagates unwrapped — trusted-operator contract, E-023 residual).
- Signature takes only injected primitives (vault_read, vault_write, clock, hash_file) — no network, no subprocess, no env reads, no Cedar callback (that plumbing lives in the vault dispatcher, not here).
- Deterministic: same `(run_state, payload bytes)` → same envelope bytes → same `envelope_sha256`.
- **Signature-chain depth:** 1 (single envelope write). v0.1 does NOT chain three per-tab signatures; the envelope itself is the single signed artefact. Future multi-tab detached signatures (Stage-2+) are out of scope.
- **Non-monotonic clock handling:** `assembled_at_iso` is a display field only — not used in equality or hash verification. A decreasing clock produces an unusual timestamp but does not corrupt the envelope integrity check (hash is over canonical bytes with timestamp baked in; downstream readers trust hash, not wallclock).
- **Threat-model docstring (E-023 residual surfacing):** the module docstring MUST enumerate the adversarial residuals NOT defended at this layer — (a) malformed envelope bytes at read-back (JSON decode failure → propagate unwrapped), (b) missing signature file (not applicable v0.1 — no detached sigs), (c) half-signed tab (not applicable v0.1 — single envelope), (d) zero-tab delivery (impossible by TabEnvelope shape — three payload-hash fields required). All four are explicitly NON-defended at R9 because the threat model assumes a trusted operator and Cedar policies enforce intent allowlist at the vault dispatcher layer.

Reference `pipeline/templates/component_analysis_template.md` for the Five Laws / Four Rules posture — Law 1 (RFA Is Truth) satisfied via RunState hash-anchoring; Law 2 (No Boundary Drift) satisfied via the eval-mode shield (F-PIPE-21) preventing tab delivery in eval runs; Law 3 (Org Isolation) satisfied via vault_write dispatcher's cross-org-access guard (delegated); Law 4 (apolitical) N/A at this layer; Law 5 (applicant substance) N/A at this layer. Rule 1 (save state) satisfied via post-write verify; Rule 2 (test own work) is the post-write envelope-hash check; Rule 3 (explicit) satisfied via injected-Protocol kwargs; Rule 4 (clean output) satisfied via canonical-bytes helper.

## Test plan

Target coverage **100%** (per §5 R3/R4/R5/R6/R7 precedent — pure orchestrator module, no network, no subprocess).

**Happy paths** (`tests/loop/test_tab_delivery.py`) — ~10 tests:
- `deliver_tab` succeeds → returns `TabSigningResult` with envelope + stored_envelope_hash matching; vault_write called exactly once with `intent="state-success"` + `write_mode="write-if-absent"`; vault_read called exactly once for post-write verify.
- `envelope.tab_ordering` equals `("live_radar", "deep_brief", "council_draft")` Final constant.
- `envelope.envelope_sha256` is canonical-bytes-without-self-hash SHA-256 hex.
- Post-write `stored.envelope_sha256 == envelope.envelope_sha256` — the B-v1-09 closure.
- `hash_file` called exactly 3× — once per payload path, in declaration order.
- `assembled_at_iso` stamped from injected `clock.now_iso()` (or equivalent).
- `vault_path` returned matches `f"pipeline/{run_id}/tab_envelope.json"`.
- Canonical-bytes helper determinism — same envelope twice → same bytes → same hash.
- `TabEnvelope.__post_init__` inline-literal check passes on happy path.
- Re-export surface: `from pipeline.loop import deliver_tab, TabSigningResult, HashFileCallable` resolves.

**Adversarial** (`tests/loop/test_adv_tab_delivery.py`) — ~18 adv tests × E-024 2× multiplier applied to LOC (not count):
- **V1 rebind-resistance — `TAB_ORDERING`.** Monkeypatch `pipeline.loop.config.TAB_ORDERING = ("council_draft","deep_brief","live_radar")`; R9's inline-literal check still raises `F_PIPE_16` on reordered envelope. Module-load integrity assert catches a pre-import rebind.
- **V1 rebind-resistance — eval-mode sentinel string.** Monkeypatch any module-level `"submission"` literal if present; R9's entry-gate comparison still uses inline-literal `"submission"`.
- **F-PIPE-16 trigger-string taxonomy pin.** Raised exception: `CODE == "F-PIPE-16"`, `trigger == "tab_envelope_ordering_violation"`, `details["observed"]` == the mis-ordered tuple.
- **F-PIPE-21 eval-mode shield.** `run_state.mode == "eval"` → `deliver_tab` raises `F_PIPE_21` with trigger `"eval_run_reached_tab_delivery"` BEFORE any vault read. No vault_read / vault_write / hash_file called.
- **Post-write hash mismatch.** Stubbed `vault_read` returns bytes whose parsed `envelope_sha256` differs from the written value → raise `F_PIPE_01` with trigger referencing tab envelope mismatch (B-v1-09 regression pin).
- **Malformed envelope bytes at read-back (E-023 residual).** `vault_read` returns bytes that `TabEnvelope.parse` cannot decode → `JSONDecodeError` propagates unwrapped (trusted-operator contract; documented in module docstring).
- **Missing payload file (E-023 residual).** `hash_file` raises `FileNotFoundError` for live_radar path → propagates unwrapped; no vault_write happens. Same for deep_brief + council_draft (three independent tests).
- **Zero-tab shape impossibility.** Attempting to construct `TabEnvelope` with any empty payload-hash field → `TabEnvelope` dataclass accepts empty strings (v0.1 does not reject empty hashes at the dataclass layer); R9 defends by asserting all three hashes are non-empty before constructing envelope, raising a module-local `ValueError` (programmer contract). Document as E-023 residual.
- **Half-signed tab shape impossibility.** v0.1 emits one envelope signature, not three per-tab signatures → no half-signed state possible. Documented as NOT-applicable in threat-model docstring; test pins the docstring text.
- **Duplicate dispatch — `write-if-absent` path.** Second `deliver_tab` call for the same `run_id` → `vault_write` raises `VaultWriteExists` → propagates unwrapped (E-023 residual, trusted-operator contract).
- **Non-monotonic clock.** `clock.now_iso()` returns a timestamp before the previous call's → envelope still integrity-checks; `assembled_at_iso` field reflects the (wrong) wallclock but `envelope_sha256` is stable.
- **AST-grep banned-pattern regression (A-v1-06).** Grep `pipeline/loop/tab_delivery.py` for `TabEnvelope(` calls with inline tuple/list `tab_ordering` arg → zero matches (must reference `TAB_ORDERING` constant). Mirrors blueprint §3.5 line 381.
- **Canonical-bytes stability under field-order change.** Reordering fields in the internal dict before `json.dumps` → same canonical bytes (sort_keys=True pin).
- **Empty `run_id` / malformed RunState.** RunState with `run_id=""` → propagates unwrapped path-template-format error (E-023 residual).
- **Cross-family non-dependency.** R9 does NOT consume rate_limiter / cascade / any Round 7 / Round 8 export — `grep -r "rate_limiter\|cascade" pipeline/loop/tab_delivery.py` returns zero. Parallel-safe regression pin.
- **Module-load integrity assert.** Import `pipeline.loop.tab_delivery` with `TAB_ORDERING` pre-rebound via `sys.modules` manipulation → import fails at module load (inherits Round 1 config.py assert).
- **Threat-model docstring presence pin.** `pipeline.loop.tab_delivery.__doc__` contains the four E-023 residual enumerations (malformed bytes, missing signature, half-signed tab, zero-tab delivery).
- **`deliver_tab` signature hygiene.** All kwargs are keyword-only (no positional injection); all callable kwargs match injected-Protocol shape.

## Testing budget (E-024 2× multiplier applied)

| File | Target | Target ±25% | Comment |
|------|--------|-------------|---------|
| `pipeline/loop/tab_delivery.py` | 300 | 225–375 | `deliver_tab` + canonical-bytes helpers + `TabSigningResult` dataclass + `HashFileCallable` Protocol + eval-mode shield + post-write verify. Simpler than R7 (no CAS retry loop, no refill arithmetic); comparable to R8 cascade (pure dispatch). |
| `tests/loop/test_tab_delivery.py` | 420 | 315–525 | ~10 tests × ~42 LOC/test with shared fakes. |
| `tests/loop/test_adv_tab_delivery.py` | 1100 | 820–1380 | ~18 adv tests × 2× multiplier (E-024 seventh-firing precedent reaffirmed at Round 7). |

Test-count total: **~28 tests** (10 happy + 18 adv) — meets the 30+ target within ±2 per E-024 calibration noise.

## Done definition

- [ ] `pipeline/loop/tab_delivery.py` shipped with `deliver_tab` + `TabSigningResult` + `HashFileCallable` + canonical-bytes helpers.
- [ ] `tests/loop/test_tab_delivery.py` + `tests/loop/test_adv_tab_delivery.py` green.
- [ ] Coverage 100% on `pipeline/loop/tab_delivery.py`.
- [ ] AST-lint R1–R7 zero violations (`lint_tree(Path('pipeline/loop/'), DEFAULT_RULES)`).
- [ ] `pipeline/loop/__init__.py` re-exports R9 public surface.
- [ ] Rebind-resistance tests pass (inline-literal `TAB_ORDERING` + `"submission"` + `"live_radar","deep_brief","council_draft"` tuple).
- [ ] Full suite green (baseline post-R7 ~4119 → target ≥ ~4147 after +28 tests; R8 lands independently in parallel).
- [ ] `pipeline/engineering/lock_history.v1.jsonl` appended with verdict=LOCKED, self-LOCK single-cycle v1 per §5 R3/R4/R5/R6/R7 precedent.
- [ ] Round-recap memory file written to `MEMORY/project_memories/`.
- [ ] `MEMORY.md` index prepended.

## Self-LOCK eligibility

**Eligible for single-cycle self-LOCK.** Pure §5 orchestrator primitive — no network, no subprocess, no §4 Logician consumption, no `compound_commit` engagement (see carve-out above). All dependencies (Round 1 dataclasses + constants + failure codes; §2 SIMPLE-intent vault surface) are LOCKED. Follow §5 R3/R4/R5/R6/R7 precedent: single-cycle pass + 100% coverage + AST-lint clean → self-LOCK with committee dispatch deferred to capstone.

## Pre-staged Round 10

**Round 10: §5 capstone LOCK paperwork** — aggregate R1–R9 into whole-section LOCK per §1 Round J pattern. Write `pipeline/validation/section_05_capstone_2026-04-XX/` with: (a) single-file roll-up of LOCKED blueprint delta (if any amendments accumulated during R2–R9), (b) committee-dispatch prompt covering the §5 orchestrator as a unit (Scribe author + Editor + Judge + Red-Team seats), (c) the eval-mode driver (§4.15) + golden-set scoring (§4.14) + calibration-report (§4.16) + `run_pipeline.py` wiring as the three remaining pre-capstone rounds IF operator prefers granular R10/R11/R12/R13 over a single capstone LOCK. Propose granular path — four single-cycle self-LOCKs at R7/R8/R9 velocity is faster than one high-dispatch capstone round.

Parallel-dispatch note: R8 cascade pre-staged Round 9 candidates as "A tab_delivery / B cron_scheduler". R8's Round-9 preview is now realized by THIS card. Whatever R8's final round-number fill becomes (Round 10 or Round 11 depending on parallel landing order), cron_scheduler (§4.10 v2 flock + vault-stamp dedupe) remains a pre-staged successor.

## Open questions (resolve at ORIENT)

1. **`TabEnvelope.canonical_bytes` placement.** Round 1 does not ship this method on the frozen dataclass. R9 adds module-level helpers OR backfills Round 1. Propose helpers (no post-LOCK dataclass mutation).
2. **`run_id_date` + `final_N` derivation on RunState.** Blueprint §4.11 uses both but Round 1 RunState field presence needs verification. If absent, R9 derives locally (ULID-timestamp-prefix → date; `iteration_count` at `report_signed` phase → `final_N`).
3. **`write_mode` for envelope write.** Blueprint silent; propose `write-if-absent`.
4. **`HashFileCallable` naming.** Matches `VaultReadCallable` / `VaultWriteCallable` pattern. Confirm naming or align with an existing §2 hash primitive if one is exposed.
5. **Round 1 backfill for `TabOrderViolation` + `TabDeliveryError`.** Blueprint references F_PIPE_16 + F_PIPE_01 directly; R9's extra wrapper classes may be redundant. Propose: drop the wrappers, raise F_PIPE_16 / F_PIPE_01 directly (matches R7 precedent of raising F_PIPE_06 directly rather than wrapping).

## Artifacts (to be filled in at LOCK)

- `pipeline/engineering/lock_history.v1.jsonl` row — placeholder:
  ```
  {"ts":"2026-04-XX","round":"§5 R9 tab_delivery","verdict":"LOCKED","single_cycle":true,"blueprint_hash":"34ef007f3ab6d59d","test_delta":"+28","coverage":"100%"}
  ```
- `MEMORY/project_memories/section_05_round_9_tab_delivery_recap.md` — round-recap memory, placeholder.
- `MEMORY.md` index prepend — placeholder row for the R9 recap.
