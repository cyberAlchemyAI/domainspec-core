# Spec card — pipeline.seats.scribe (Round 3: seat.py subprocess entry + Anthropic binding + §7.11 admin-risk + PRE/POST wiring)

**STATUS:** PRE-STAGED 2026-04-21 — §7 v1.1.1 LOCKED + §6 v1-r1 LOCKED (interlock §7.15 SATISFIED) + Scribe R1 LOCKED (row 120, 2026-04-21). Awaits Scribe R2 LOCK (composer + SectionDraft schema) before Code-window paste. Parent card: `section_7_council_seats_pipeline_modules.md` (Lane A step 5). **R3 is the final Scribe round** — closes Scribe as a full pipeline seat invoked by `pipeline.loop.seat_runner.invoke_seat`.

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, standard interface pattern — not restated).

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_07_scribe.md` **v1.1.1 LOCKED 2026-04-21** — §7.1 seat purpose + §7.11 admin-risk integration + §7.12 Editor/Judge/operator handoff (Scribe persists `SectionDraft` via §2 Vault primitive) + §7.13 full F-SCRIBE-* PRE/POST taxonomy + §7.15 prerequisite interlock (now SATISFIED) + §7.17 interface-index rows (schemas + pre/post-gate-checks).
- `pipeline/blueprint/v0.1/section_06_operating_envelope.md` **v1-r1 LOCKED 2026-04-21** — §6.3 A2 Block 1 router.yaml schema (Anthropic envelope that Scribe binds to), §6.5 A3 SFR format (Scribe is NOT exempt per §F.1 — Scribe-adjacent SFR emission hook stubbed at R3 per §D.1 future-stable), §6.6 A4 context-placement + nine-class middle-contradiction lint (Scribe's `F-SCRIBE-SCOPE-MISSING` is a §6 F-CONTEXT-PLACEMENT subclass), §6.11 prompt-template compilation pipeline (R3's Scribe prompt compiles through this pipeline — NOT reimplemented locally).
- `pipeline/blueprint/v0.1/section_05_pipeline.md` **v6 LOCKED 2026-04-18** — §4.3 Scribe invocation tuple return + A-v1-02 trust model + A-v1-13 minimal-env subprocess (R3's seat.py satisfies this contract as invoked by `pipeline.loop.seat_runner.invoke_seat`).
- `pipeline/blueprint/v0.1/section_04_logician.md` **v2.1 LOCKED** (+ v2.2 wave-3/4 LOCKED 2026-04-21) — PRE-gate slot table (§4.2.1 row #8-ish for F-SCRIBE-*); POST-gate §4.4 skeleton (F-POST-10 hard-block; F-POST-11 unsourced). R3 consumes these as-is; does not author new gate predicates.
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` **v7.1 LOCKED 2026-04-19** — §4.10 dispatcher kinds (`conversation_log`, `drafts_manifest` intent). R3 persists drafts via Vault primitive (never raw `open()`).
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` **v7 LOCKED** — §D.2 Scribe role, §D.7 Opus 4.7 envelope (Anthropic binding Block 1), §D.8 context-rot, §F.1 SFR (Scribe is NOT exempt), §J grant-content-never-flows (audit-stamp is shell-hash only per §6.11 v1-r1 tightening).
- **Blueprint hash-at-card** (BLUEPRINT_DEPS pins, compute at card-open immediately before Code-window paste):
  - `section_07_scribe.md` — v1.1.1 (prefix already pinned at R1 as `85b244a26888b52e`; recompute at R3 card-open — R2 LOCK may have invalidated via prose-only amendments)
  - `section_06_operating_envelope.md` — v1-r1 LOCKED (compute at card-open)
  - `section_05_pipeline.md` — v6 LOCKED 2026-04-18 (`34ef007f3ab6d59d` per seat_runner BLUEPRINT_DEPS)
  - `section_04_logician.md` — v2.1 LOCKED + v2.2 waves 3/4 (`e0507e6daaa18676` per R1 pin; recompute at R3 card-open)
  - `section_02_vault_topology.md` — v7.1 LOCKED (compute at card-open)

**Spec-card version:** v1
**Round:** §7 Scribe Round 3 — seat.py subprocess entry + Anthropic provider binding + §7.11 admin-risk register consumption + Logician PRE/POST gate wiring
**Canonical home:** `pipeline/seats/scribe/` (R1 + R2 modules already landed here)

---

## 1. Purpose

R3 closes Scribe as a full pipeline seat. The orchestrator (`pipeline.loop.seat_runner.invoke_seat(seat_kind="scribe", ...)`) launches Scribe as a subprocess; R3 ships the subprocess entry point, the Anthropic provider binding that executes inside that subprocess, the §7.11 admin-risk register adapter that consumes the canonical register at compile time, and the Logician PRE/POST gate wiring that fails-closed on every F-SCRIBE-* condition declared in §7.13.

**R3 is the Scribe seat's LOCK-closing round.** R1 shipped shapes + KGIE predicate (pure Python, zero I/O). R2 ships the composer / SectionDraft shape / SMART / overlooked-expenses / dialect / program templates (deterministic shapers, no LLM call). R3 wires R1 + R2 into a seat that a subprocess launcher can invoke, whose output is a `SeatInvocationResult` the revision loop can persist.

**What R3 does NOT author:**
- The Anthropic HTTP client itself — R3 composes a thin binding that reads router.yaml and consumes the `pipeline.providers.anthropic` surface. **If `pipeline/providers/anthropic.py` does not exist at R3 open, R3 ships a minimal BYOK client stub under `pipeline/seats/scribe/provider_anthropic.py` scoped to the Scribe seat; a proper `pipeline.providers.*` refactor is v0.1.1.** (OQ-1 below.)
- The prompt-template compilation pipeline — §6.11 owns that. R3 constructs the seat-invocation-request dict and calls into §6.11's compile surface; §6.11 returns the compiled prompt with Five-Laws + scope + gate + schema blocks at start/end (A4 FLOOR) already lint-passed. R3 never writes an `open()` on a prompt file.
- The admin-risk register itself — R3 reads `pipeline/institutional_memory/admin_risk_register.yaml` (v2.2 APPROVED 2026-04-21) via a Vault `admin-risk-register-query` primitive per §7.11. R3 NEVER writes the register.
- The PRE/POST gate predicates themselves — R3 wires Scribe-specific gate hooks into the existing `pipeline.logician.pre_gate` + `pipeline.logician.post_gate` orchestrators. R3 does not author gate algorithms.

## 2. Module layout

```
pipeline/seats/scribe/
  seat.py                     # subprocess entry: stdin→envelope→compose→LLM→SectionDraft→stdout
  provider_anthropic.py       # thin BYOK Anthropic binding; reads router.yaml seats.scribe.*
  admin_risk_adapter.py       # §7.11 register consumption + two-axis dialect discipline + flag-routing
  logician_wiring.py          # PRE/POST gate assembly for Scribe-specific F-SCRIBE-* codes
  BLUEPRINT_DEPS              # engineering-process §4.6 hash pins (extend R1 pin to cover §6 + §2)
```

Corpus fixtures at `tests/corpus/scribe/v1/` (extends R1's pass/fail fixtures with subprocess-level happy-path and error-surface fixtures):
```
tests/corpus/scribe/v1/
  subprocess/
    happy_path_vapg/
      stdin_envelope.json     # seat-envelope.v1 shape per §7.17 row (OQ-4 at R1 resolved: row-append at R3 LOCK)
      expected_stdout.json    # SeatInvocationResult-compatible payload (SectionDraft + hash + envelope_version)
      expected_exit_code: 0
    error_byok_missing/
      stdin_envelope.json     # valid envelope, but BYOK key absent from env
      expected_stderr_match: "F-SCRIBE-BYOK-MISSING"
      expected_exit_code: 2
    error_kgie_fail/
      stdin_envelope.json     # envelope carrying KGIE status="fail"
      expected_stderr_match: "F-SCRIBE-KGIE-FAIL"
      expected_exit_code: 2
    error_admin_risk_stale/
      stdin_envelope.json     # snapshot_age_hours > 24
      expected_stderr_match: "F-SCRIBE-ADMIN-RISK-REGISTER-STALE"
      expected_exit_code: 2
```

## 3. Public API (Round 3)

R3 extends `pipeline/seats/scribe/__init__.py` `__all__` with:

```python
# R3 additions — seat entry + provider binding + admin-risk + wiring
"run_seat",                        # seat.py::run_seat(stdin: BinaryIO, stdout: BinaryIO) -> int
"ScribeEnvelope",                  # seat-envelope.v1 frozen dataclass (row-append to §0.5 at LOCK, per OQ-4)
"ScribeResult",                    # stdout payload wrapper (SectionDraft tuple + compiled_prompt_shell_sha)
"AnthropicBinding",                # provider_anthropic::AnthropicBinding (BYOK-envelope + retry-policy carrier)
"call_anthropic_scribe",           # provider_anthropic::call_anthropic_scribe (thin callable)
"AdminRiskAdapter",                # admin_risk_adapter::AdminRiskAdapter (register consumer + flag router)
"AdminRiskFlag",                   # §7.11 AdminRiskFlag shape (schema row scribe.admin_risk_flag.v1)
"scan_draft_for_admin_risk",       # admin_risk_adapter::scan_draft_for_admin_risk
"assemble_scribe_pre_gate",        # logician_wiring::assemble_scribe_pre_gate
"assemble_scribe_post_gate",       # logician_wiring::assemble_scribe_post_gate
# Failure-code constants (extends R1's four; R3 lands the full §7.13 set)
"F_SCRIBE_SCOPE_MISSING",
"F_SCRIBE_ORG_CROSS_REF",
"F_SCRIBE_DIALECT_UNCLASSIFIED",
"F_SCRIBE_TEMPLATE_UNKNOWN",
"F_SCRIBE_TEMPLATE_DRIFT",
"F_SCRIBE_ADMIN_RISK_REGISTER_STALE",
"F_SCRIBE_UNSOURCED_CLAIM",
"F_SCRIBE_PARAPHRASED_NUMERIC",
"F_SCRIBE_DIALECT_INDUCED_IDENTITY",
"F_SCRIBE_CONVERSATION_ANCHOR_INVALID",
"F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED",
"F_SCRIBE_ADMIN_RISK_UNFLAGGED",
"F_SCRIBE_DIALECT_DRIFT",
"F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED",
"F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED",
"F_SCRIBE_SMART_INVENTED_METRIC",
"F_SCRIBE_EVALUATION_CRITERION_MISSING",
"F_SCRIBE_INELIGIBLE_ACTIVITY",
"F_SCRIBE_BYOK_MISSING",            # new at R3 — not a §7.13 entry; operational fail-close when BYOK env unset
```

## 4. Subprocess entry contract

`seat.py::run_seat(stdin, stdout) -> int` is the only externally-visible subprocess surface. `pipeline.loop.seat_runner.invoke_seat` launches `python -m pipeline.seats.scribe.seat` under the A-v1-13 minimal-env whitelist (`PATH`, `HOME`, `TILTH_SESSION_ID`, `TILTH_RUN_ID`, `TILTH_ORG_SLUG`, `TILTH_SEAT_KIND`). BYOK key is loaded via a separate gated read from the operator keyring — NOT passed through the minimal env (violates A-v1-13).

### 4.1 Stdin envelope (`ScribeEnvelope`)

Proposed schema for §0.5 row-append at R3 LOCK (closes Scribe R1 OQ-4: "seat-envelope canonical schema = row-append at Scribe R3 LOCK"). JSON-serializable frozen dataclass, decoded at subprocess entry:

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class ScribeEnvelope:
    envelope_version: Literal["scribe-envelope.v1"]   # strict enum — rebind-resistant
    run_id: str
    org_slug: str
    iteration_number: int
    rfa_extracted_record: RfaExtractedRecord           # R1 shape, JSON-deserialized
    kgie_preflight_result: KgiePreflightResult         # R1 shape, JSON-deserialized
    project_context: Mapping[str, Any]                 # frozen at construct (MappingProxyType)
    section_spec: SectionSpec                          # which section to draft (§7.5 13-section registry)
    funder_dialect: Literal["conservative", "centrist", "progressive", "soul_fire"]
    operator_override_dialect: str | None
    program_template: ProgramTemplate                  # R2 output (§7.9)
    admin_risk_register_snapshot_path: str             # vault-relative path; adapter reads via admin-risk-register-query
    admin_risk_snapshot_age_hours: float               # freshness; F-SCRIBE-ADMIN-RISK-REGISTER-STALE at > 24
    conversation_log_anchor: str | None                # §7.4a USER_DATA:<run_id>:<turn_ordinal>:<sha3_512[:32]>
    compiled_prompt_shell_sha3_512: str                # §6.11 shell-hash captured pre-dispatch (audit-stamp input)
    envelope_emitted_at_utc: datetime                  # tz-aware; echoed back in result for drift detection
```

Construction-time invariants: `envelope_version` is a `Literal` (rebind-resistant); `project_context` frozen to MappingProxyType; `admin_risk_snapshot_age_hours >= 0.0`; `envelope_emitted_at_utc.tzinfo is not None`.

### 4.2 Stdout payload (`ScribeResult`)

Wraps the SectionDraft emission and the data `pipeline.loop.seat_runner` needs to hash + persist:

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class ScribeResult:
    result_version: Literal["scribe-result.v1"]
    run_id: str
    org_slug: str
    iteration_number: int
    section_drafts: tuple[SectionDraft, ...]           # R2 shape — one entry per drafted section
    compiled_prompt_shell_sha3_512: str                # echoed from envelope for audit-stamp verification
    provider_landed_family: str                        # always "anthropic" for Scribe; A-v1-02 trust model
    provider_landed_model_id: str                      # exact model id the provider returned
    admin_risk_flags: tuple[AdminRiskFlag, ...]        # pre-POST-gate; Logician walks these at POST
    seat_emitted_at_utc: datetime
```

Stdout MUST be valid UTF-8 JSON decoding to a non-empty dict with `result_version == "scribe-result.v1"`. `seat_runner.invoke_seat` computes `output_hash = sha256_hex(raw_stdout)`; that hash rides into the revision-loop checkpoint.

### 4.3 Exit codes

| Code | Meaning |
|---|---|
| 0 | Success — stdout is a well-formed `ScribeResult` |
| 1 | Internal error — unhandled exception; stderr carries traceback; `seat_runner` treats as failure but does NOT retry on this code (code-level bug, not transport) |
| 2 | Fail-closed gate trip — stderr carries structured `F-SCRIBE-*` payload (code + evidence); stdout empty; caller surfaces to operator |
| 124 | Timeout — NOT emitted by `seat.py` itself (kernel / launcher issue); `seat_runner` branches on `SubprocessResult.timed_out` at the launcher level |

### 4.4 Error-surface contract

On any fail-closed gate trip, `seat.py` writes to stderr a single JSON line:

```json
{"failure_code": "F-SCRIBE-KGIE-FAIL", "trigger": "kgie_status_fail", "evidence": {...}, "envelope_version": "scribe-envelope.v1", "emitted_at_utc": "..."}
```

and exits 2. `seat_runner.invoke_seat` does NOT parse stderr (that is revision-loop concern at §5 R5+); stderr is captured verbatim in `SubprocessResult.stderr` for checkpoint persistence.

## 5. §7.11 admin-risk integration

R3 consumes canonical `pipeline/institutional_memory/admin_risk_register.yaml` **v2.2 APPROVED 2026-04-21** via `admin_risk_adapter.AdminRiskAdapter`.

### 5.1 Load discipline
- Read through Vault primitive `vault-read(intent="admin-risk-register-read")` — never raw `open()` (§2 invariant).
- Parse YAML; construct a frozen per-entry record carrying `term`, federal `severity` (RED / YELLOW / GREEN → HIGH / MEDIUM / LOW display), `suggested_substitution`, `applicable_dialects`, `progressive_register` (AVOID / OK / EXPECTED / PREFERRED), `rationale`, `entry_added_at_utc`.
- Freshness: `envelope.admin_risk_snapshot_age_hours > 24` → PRE-gate `F-SCRIBE-ADMIN-RISK-REGISTER-STALE`. (Snapshot-age ceiling per §7.16 + OQ-7.5.)

### 5.2 Two-axis dialect discipline (CLAUDE.md Law 4 + register v2.2 top-matter)
Every match carries two independent signals:
- **Federal axis** — `severity` ∈ {HIGH / MEDIUM / LOW}. Governs federal / federal-contract / conservative-state funders.
- **Progressive axis** — `progressive_register` ∈ {AVOID / OK / EXPECTED / PREFERRED}. Governs progressive-state / progressive-foundation / racial-justice / soul-fire funders.

Flag severity on a given draft is the intersection: `envelope.funder_dialect` + `operator_override_dialect` + `program_template.dialect_default` (operator > template > funder; OQ-4 at R3 per OQ-7.4 recommendation). Applicant-identity overlay applies when `KgiePreflightResult.identity_claims` contains an entry matching the funder register — identity-affirming language flips from flagged to EXPECTED/PREFERRED.

### 5.3 Flag-routing (Law 4 invariant — Logician flags, NEVER rewrites)
- **LOW (federal) + auto-substitute-low pre-approval** → silent substitution at COMPILE time (scope-bounded to the register entry's `suggested_substitution`; logged to draft trailer for transparency).
- **MEDIUM (federal) or any AVOID progressive** → always flag. `AdminRiskFlag(term, severity, suggested_substitution, status="pending_operator_approval")`. Scribe emits inline `[ADMIN-RISK:<term>:<proposed-substitution>]` comment. POST-gate `F-SCRIBE-ADMIN-RISK-UNFLAGGED` hard-blocks if a MEDIUM+ term appears without the comment.
- **HIGH (federal)** → always flag AND hard-block finalize until operator explicitly approves. POST-gate `F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED` surfaces on attempted finalize.

Applicant approves EVERY substitution. Scribe NEVER silently rewrites MEDIUM or HIGH terms (Law 4 invariant, correctness-by-construction via prompt template per §6.11).

## 6. PRE/POST gate wiring

R3 authors `logician_wiring.assemble_scribe_pre_gate(envelope) -> PreGateAssembly` and `assemble_scribe_post_gate(envelope, result) -> PostGateAssembly`. These are **pure assemblers**; the predicates themselves live in `pipeline.logician.pre_gate`, `pipeline.logician.post_gate`, `pipeline.logician.cedar_eval`, and `pipeline.logician.source_tag_verify`.

### 6.1 PRE-gate (runs before Scribe's LLM call)
- `F_PRE_CROSS_ORG_READ` — **Cedar `org_isolation` policy** (`pipeline.logician.cedar_eval.evaluate_cross_org_dossier` — already LOCKED). Envelope's `project_context` slug MUST equal `envelope.org_slug`; any other org slug present in the compiled prompt trips `F-SCRIBE-ORG-CROSS-REF`. Cedar enforcement, fail-closed (Law 3).
- **KGIE preflight gate** — reads `envelope.kgie_preflight_result.status`. `status == "fail"` → `F-SCRIBE-KGIE-FAIL`; `status == "needs_operator_input"` → route to operator-open-question surface (NOT a failure); `status == "pass"` → proceed. (R1's predicate is the predicate; R3 consumes its pre-computed result.)
- `F-SCRIBE-RFA-MISSING` — RFA file exists at declared path; session manifest pins content hash.
- `F-SCRIBE-RFA-DRIFT` — RFA file current SHA-3-512 == session-manifest-pinned hash.
- `F-SCRIBE-PHASE-0-MISSING` — `envelope.rfa_extracted_record` is not None.
- `F-SCRIBE-SCOPE-MISSING` — forwarded from §6.11 `F-CONTEXT-PLACEMENT` subclass; §6's prompt-template compiler enforces; R3 reads the §6 verdict and fails-closed if §6 says so.
- `F-SCRIBE-DIALECT-UNCLASSIFIED` — `envelope.funder_dialect` must be one of four; operator override present if unclassified at Phase 0.
- `F-SCRIBE-TEMPLATE-UNKNOWN` — `envelope.program_template.program_code` ∈ `KNOWN_PROGRAMS` (R2 registry).
- `F-SCRIBE-TEMPLATE-DRIFT` — recomputed `template_content_sha3_512` == pinned at Phase 0 (§7.9 v1.1 invariant).
- `F-SCRIBE-ADMIN-RISK-REGISTER-STALE` — `envelope.admin_risk_snapshot_age_hours <= 24`.
- `F-SCRIBE-BYOK-MISSING` — Anthropic BYOK key readable from operator keyring; missing → fail-closed with structured evidence (NOT env-dependent — keys live outside A-v1-13 minimal env).

### 6.2 POST-gate (runs after Scribe's LLM call, before stdout emit)
- `F-SCRIBE-UNSOURCED-CLAIM` — grep-verification via `pipeline.logician.source_tag_verify` against every `SectionDraft.claim_evidence_map` entry. (Known grep limitation on qualitative paraphrase; numeric paraphrase caught separately.)
- `F-SCRIBE-PARAPHRASED-NUMERIC` — numeric-verbatim walk (§7.6 numeric-verbatim invariant); byte-identity after unit-normalization.
- `F-SCRIBE-DIALECT-INDUCED-IDENTITY` — closed-set table `scribe.dialect_identity_proxy_table.v1` (R2 dialect module owns the table); any proxy phrase without matching `KgiePreflightResult.identity_claims` → hard-block.
- `F-SCRIBE-CONVERSATION-ANCHOR-INVALID` — §7.4a canonical shape; `pipeline.logician.conversation_log.verify_anchor` already LOCKED.
- `F-SCRIBE-ADMIN-RISK-UNFLAGGED` / `F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED` — `admin_risk_adapter.scan_draft_for_admin_risk(section_draft, envelope.funder_dialect)` walks; Logician fails-closed per §5.3 above.
- `F-SCRIBE-DIALECT-DRIFT` — dialect-vocabulary mix within one draft; middle-block mix forwarded to §6 `F-CONTEXT-MIDDLE-CONTRADICTION`.
- `F-SCRIBE-SECTION-OVER-LIMIT-UNFLAGGED` — `SectionDraft.over_limit_flag` consistent with `body_text` length vs `rfa_section_limit`.
- `F-SCRIBE-OVERLOOKED-EXPENSE-UNRESOLVED` — budget-section check: `OverlookedExpensesWalk.needed_count == 0` at finalize.
- `F-SCRIBE-SMART-INVENTED-METRIC` — SMART-objective numeric tokens trace to `PROJECT_CONTEXT` / `USER_DATA`.
- `F-SCRIBE-EVALUATION-CRITERION-MISSING` — Executive Summary touches every `evaluation_criteria` entry (exhaustiveness).
- `F-SCRIBE-INELIGIBLE-ACTIVITY` — Scribe-owned Law 2 POST-gate (§7.2 + §7.13); walks `SectionDraft.eligible_activity_map`; exhaustiveness + match invariant.

POST-gate assembly also consumes `pipeline.logician.post_gate.run_post_gate_skeleton` for the F-POST-10 / F-POST-11 floor predicates (admin-risk hard-block count + unsourced-claim count); Scribe-specific F-SCRIBE-* codes ride alongside.

## 7. Discipline requirements

Applies cumulatively on top of R1's disciplines (inline-literal frozen sets, kw-only slotted frozen dataclasses, `__post_init__` invariants, `__all__` tuple literal).

### 7.1 V1 inline-literal rebind-resistance
Every new threshold constant (admin-risk snapshot-age ceiling 24h; stderr JSON-line schema version; exit-code mapping {0, 1, 2}) is inline-literal at the dispatch site. Module-level constants exist for human reading but are never consulted at runtime — rebind-resistance test asserts that mutating `admin_risk_adapter.SNAPSHOT_AGE_HOURS_CEILING` does NOT change the gate behaviour.

### 7.2 E-017 provider-seam pattern (subprocess I/O = new E-017 firing slot)
`seat.py` accepts `stdin: BinaryIO` + `stdout: BinaryIO` + `stderr: BinaryIO` + `clock: ClockFn` + `anthropic_call: AnthropicCallCallable` + `vault_read: VaultReadCallable` + `admin_risk_load: AdminRiskLoadCallable` + `logician_pre: LogicianPreCallable` + `logician_post: LogicianPostCallable` as injected callables. Production wires stdlib `sys.stdin.buffer` / `sys.stdout.buffer` / `sys.stderr.buffer` + real clock + real Anthropic HTTP client; tests inject deterministic stubs. No `sys.exit()` inside `run_seat` — return an `int` and let the CLI wrapper `__main__` block call `sys.exit(run_seat(...))`. (Per E-017 pattern; per Scout / §5 seat_runner precedent.)

### 7.3 E-027 payload-size pre-check (Scribe prompt can exceed 80k prompt-tokens on rich PROJECT_CONTEXT + program template)
Before every Anthropic call, `provider_anthropic.py` computes `prompt_token_estimate = len(compiled_prompt_chars) / 3.7` and logs to SFR-telemetry. E-027 applies to Qwen on Groq, not Anthropic, but the discipline of estimating before dispatch transfers: Anthropic Opus 4.7 has a published token-envelope (§6.3) and running up against `max_tokens=64000` produces truncated drafts. Over-threshold → seat emits `F-SCRIBE-PAYLOAD-CEILING` (operational; documented as R3 residual, not a §7.13 failure code — v0.1.1 candidate if firings accumulate).

### 7.4 E-028 transport-retry discipline
Anthropic call wraps in transport-retry: 120 s wall-clock cap, single-shot retry on connection-level failures only (DNS / TCP reset / 5xx), 30 s health-check between retries. Semantic errors (4xx with structured body) never retry — escalate to fail-closed. L-011 transport-class retry carve-out applies (same pattern as Logician v2.2 qwen retries).

### 7.5 BYOK key loading, fail-closed if missing
Key read path: `pipeline.sovereignty.byok.load_key(provider="anthropic", org_slug=envelope.org_slug)` (already LOCKED). Missing key → `F-SCRIBE-BYOK-MISSING` with structured evidence; NEVER falls back to a global key (Cedar `byok_key_scope` policy enforces, §4.11 compound-commit predicate).

### 7.6 §6.11 audit-stamp shell-hash tightening
Scribe consumes the **`compiled_prompt_shell` SHA-3-512**, not the full-prompt hash. Envelope carries the shell-hash; result echoes it; revision-loop persists only the shell-hash. Grant content (RFA excerpt, PROJECT_CONTEXT substitutions) NEVER crosses the persistence boundary even as a hash (§J + §6.11 v1-r1 closure of Thesis-R1 Red Team R-3).

## 8. Test surface

Floor ≥ 30 source-path tests + 10 adversarial. **E-024 1.5-2× multiplier applies — trident trips (E-017 subprocess I/O + V1 rebind-resistance + E-023 deferred-scope test_adv_* docs).** Expect ~45-60 total source + adversarial. LOC at 1.5-2× the floor is expected; LOC under-run is the investigation signal.

**Subprocess entry tests (12+):**
- `test_run_seat_happy_path_emits_scribe_result` — golden VAPG fixture → stdout parses as `ScribeResult` with `result_version="scribe-result.v1"`; exit 0.
- `test_run_seat_malformed_envelope_exits_2` — envelope missing `envelope_version` → stderr carries `F-SCRIBE-*`; exit 2.
- `test_run_seat_envelope_version_wrong_literal_exits_2` — `envelope_version="scribe-envelope.v2"` → fail-closed; exit 2.
- `test_run_seat_injects_clock_for_determinism` — fixed clock → `seat_emitted_at_utc` byte-identical across two runs.
- `test_run_seat_stdin_eof_mid_json_exits_2` — truncated stdin → structured error; exit 2.
- `test_run_seat_stdout_is_valid_utf8_json` — adversarial body with non-ASCII → stdout decodes cleanly.
- `test_run_seat_stderr_schema_version_literal_pinned` — every fail-closed error carries `envelope_version` echo.
- `test_run_seat_exit_codes_0_1_2_124_are_the_only_codes_emitted` — exhaustiveness over fuzzed envelopes.
- `test_run_seat_no_sys_exit_inside_run_seat` — AST check: `run_seat` body has no `sys.exit(...)` call; `__main__` is the exit caller.
- `test_run_seat_does_not_call_vault_read_for_register_when_path_malformed` — E-017 seam honors injected callables.
- `test_run_seat_conversation_anchor_none_is_permitted` — anchor optional (non-USER_DATA sources OK).
- `test_run_seat_iteration_number_echoed_in_result` — tracks revision-loop iteration.

**Anthropic binding tests (6+):**
- `test_anthropic_binding_reads_router_yaml_scribe_primary` — reads `seats.scribe.primary` (NOT hardcoded model name).
- `test_anthropic_binding_escalation_fires_on_sonnet_fail` — falls over to `seats.scribe.escalation` (Opus 4.6) on specified transport error only.
- `test_anthropic_binding_transport_retry_120s_cap_single_shot` — retry policy per E-028.
- `test_anthropic_binding_byok_missing_fails_closed` — `F-SCRIBE-BYOK-MISSING` + exit 2.
- `test_anthropic_binding_semantic_4xx_never_retries` — 4xx with structured body does NOT trigger retry.
- `test_anthropic_binding_rebind_router_yaml_does_not_change_runtime` — V1 inline-literal discipline on timeout ceiling.

**Admin-risk adapter tests (8+):**
- `test_admin_risk_adapter_loads_v2_2_register` — register v2.2 YAML parses; 40+ entries present.
- `test_admin_risk_two_axis_dialect_federal_high_progressive_expected` — identity-rooted applicant + progressive funder → EXPECTED, not flagged.
- `test_admin_risk_flag_routing_low_auto_substitute_with_preapproval` — pre-approval → silent substitution.
- `test_admin_risk_flag_routing_medium_always_flags` — MEDIUM never silent.
- `test_admin_risk_flag_routing_high_hard_blocks_finalize` — HIGH raises F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED at finalize.
- `test_admin_risk_snapshot_stale_fails_pre_gate` — `snapshot_age_hours=25.0` → `F-SCRIBE-ADMIN-RISK-REGISTER-STALE`.
- `test_admin_risk_applicant_identity_overlay_flips_flag_to_preferred` — Black-led applicant + racial-justice funder → PREFERRED.
- `test_admin_risk_register_malformed_severity_fails_pre_gate_03` — YAML malformed → F-PRE-03 / F-PRE-20 per §4.

**Logician wiring tests (8+):**
- `test_pre_gate_assembly_fires_cedar_cross_org_on_slug_mismatch` — project_context slug != envelope.org_slug → F-CEDAR-03 + F-SCRIBE-ORG-CROSS-REF.
- `test_pre_gate_assembly_forwards_f_context_placement_from_section_6` — §6 compile verdict carried through.
- `test_pre_gate_assembly_kgie_needs_operator_input_does_not_fail_closed` — routes to OQ surface, NOT F-SCRIBE-KGIE-FAIL.
- `test_post_gate_assembly_invokes_source_tag_verify` — claim_evidence_map walked; unsourced claim → F-SCRIBE-UNSOURCED-CLAIM.
- `test_post_gate_assembly_ineligible_activity_scribe_owned` — §7.2 Law 2 POST-gate fires locally, NOT delegated.
- `test_post_gate_assembly_dialect_induced_identity_closed_set` — closed-set table (R2) consulted.
- `test_post_gate_assembly_numeric_verbatim_unit_normalization_allowed` — "12 months" vs "1 year" passes.
- `test_post_gate_assembly_conversation_anchor_sha_mismatch_fails` — USER_DATA anchor tampered → F-SCRIBE-CONVERSATION-ANCHOR-INVALID.

**Property tests (6+ via hypothesis):**
- Idempotent subprocess under fixed clock (two identical envelopes → identical ScribeResult bytes).
- Envelope JSON-roundtrip preserves every field invariant.
- Admin-risk adapter is monotonic under register-growth (adding an entry cannot decrease flag count on an unchanged draft).
- Flag-routing is a pure function of (term, severity, funder_dialect, applicant_identity_overlay).
- No PRE-gate ever writes to disk (property: vault_write mock never invoked in PRE-path).
- `ScribeEnvelope` → `ScribeResult` pipeline preserves `run_id` / `org_slug` / `iteration_number` / `compiled_prompt_shell_sha3_512` exactly.

**Adversarial tests (10+):**
- `test_adv_envelope_with_two_org_slugs_fails_cedar` — PROJECT_CONTEXT carrying smuggled second-org reference → F-CEDAR-03.
- `test_adv_anthropic_response_is_not_json_exits_1_not_2` — provider returns plaintext; fall into exit 1 (code bug class), not exit 2 (gate-class).
- `test_adv_admin_risk_register_contains_yaml_bomb` — billion-laughs / alias-cycle → safe load fails closed; F-PRE-20 candidate.
- `test_adv_section_draft_body_contains_base64_injection_payload` — §6.6 Class-9 encoded-payload; forwarded to F-CONTEXT-MIDDLE-CONTRADICTION (§6-owned).
- `test_adv_byok_key_from_env_var_is_refused` — A-v1-13 minimal-env whitelist does NOT include API keys; reading `os.environ["ANTHROPIC_API_KEY"]` is refused in favor of sovereignty keyring path.
- `test_adv_stdout_oversized_truncates_raises_exit_1` — response exceeds stdout pipe buffer → exit 1, not silent truncation.
- `test_adv_compiled_prompt_shell_hash_tampered_fails_post` — shell-hash mismatch between envelope and result → POST-gate fails closed.
- `test_adv_rfa_drift_between_phase_0_pin_and_seat_run_fails_pre` — operator edits RFA mid-session → F-SCRIBE-RFA-DRIFT.
- `test_adv_template_drift_mid_session_fails_pre` — program template modified after Phase 0 → F-SCRIBE-TEMPLATE-DRIFT.
- `test_adv_conversation_anchor_turn_ordinal_future_fails_post` — anchor references a turn that doesn't exist yet → F-SCRIBE-CONVERSATION-ANCHOR-INVALID.

**Integration tests (4+):**
- `test_int_scribe_invoked_via_seat_runner_contract` — `invoke_seat(seat_kind="scribe", ...)` → well-formed `SeatInvocationResult` with non-None `raw_stdout` + `output_hash`.
- `test_int_scribe_writes_draft_manifest_via_vault_primitive` — §2 dispatcher SIMPLE path; never raw `open()`.
- `test_int_scribe_cross_family_rigor_vs_judge` — router.yaml carries Scribe=Anthropic + Judge=Google → PASS; flip Judge to Anthropic → F-ROUTER-FAMILY-COLLISION at start.
- `test_int_scribe_emits_sfr_telemetry_stub` — R3 ships the §F.1 SFR emission hook as a stub (full SFR is A3 + §6.5); Scribe is NOT exempt but R3 lands the hook surface, not the verdict format.

## 9. Done definition (R3)

- Modules exist at listed paths with `__init__.py` export.
- Public API surface exactly matches §3 above — `__all__` leakage = LOCK fail.
- Every §7.13 failure-code constant exported + wired in `logician_wiring.assemble_scribe_{pre,post}_gate`.
- Subprocess entry satisfies `pipeline.loop.seat_runner.invoke_seat` contract — integration test green.
- §7.11 admin-risk register consumed via Vault primitive; register v2.2 parses; two-axis dialect discipline exercised by ≥ 4 fixtures.
- PRE/POST gate wiring covers every §7.13 code; `F-SCRIBE-INELIGIBLE-ACTIVITY` remains Scribe-owned (not delegated).
- BYOK key loading via `pipeline.sovereignty.byok.load_key`; fail-closed on missing.
- **Test count:** floor ≥ 30 source + 10 adversarial; expect ~45-60 given E-024 trident.
- **Coverage ≥ 95%** on `pipeline/seats/scribe/{seat,provider_anthropic,admin_risk_adapter,logician_wiring}.py`.
- **AST-lint R1-R7 clean** — R2 `loop-logician-ban` does NOT apply to `pipeline/seats/` (parent spec §8); Scribe may import `pipeline.logician`, `pipeline.vault`, `pipeline.providers.*`, `pipeline.sovereignty.byok`. MUST NOT import `pipeline.loop`.
- **BLUEPRINT_DEPS sha-pinned** against §7 v1.1.1 + §6 v1-r1 + §5 v6 + §4 v2.1 + §2 v7.1; L-015 regression test extended.
- **E-030 companion-code pin verification** — every pin resolves to a `lock_history.v1.jsonl` row OR is annotated "live re-export surface / no standalone LOCK" with the per-child-module LOCK rows named.
- **Full suite green** (R1 baseline + R2 delta + R3 expected delta ≈ +45-60 tests).
- **LOCK row** appended to `pipeline/engineering/lock_history.v1.jsonl` with reviewer tokens, test count, F-code surface (18+ F-SCRIBE-* codes).
- **Committee 5/5 PASS cycle-1.** **R3 is NOT self-LOCK eligible.** R3 closes the Scribe seat as a pipeline module with subprocess boundary + provider binding + cross-cutting Logician wiring + register consumption — a materially higher composition risk surface than R1's shape layer. Dispatch to full Code Thesis Committee per engineering process §3. (Precedent: §5 R4 seat_runner itself was committee-reviewed; Scribe R3 sits at an analogous risk tier.)

## 10. Committee composition

Scribe production binding = Anthropic; none of the five standard code-reviewers are Anthropic (codex / qwen3-32b / llama-3.3-70b / gpt-oss-120b / kimi-k2 per `router.yaml`). Cross-family clean.

**Payload-size pre-check (E-027 discipline).** Consolidated R3 dispatch will likely exceed 80k prompt-tokens given 4 modules + test surface + §6 + §7 blueprint anchors. Per engineering process §3.1, **dispatch per-module** (Option 1: `seat.py` + `provider_anthropic.py` + `admin_risk_adapter.py` + `logician_wiring.py` as four independent single-module dispatches). E-029 pattern: narrow reviewer scope + shared infrastructure already validated = cleanest cycle-1 outcomes. R1 + R2 modules are already LOCKED = shared infrastructure validated. R3's per-module dispatch sits in the sweet spot.

## 11. Failure modes (delta — template §3 taxonomy)

- **Subprocess-boundary leakage (new at R3).** Writing structured error to stderr as multiline instead of single-line JSON → `seat_runner` captures but revision-loop parse downstream (R5+) breaks. Mitigation: adversarial test `test_run_seat_stderr_is_single_line_json` pins one-line invariant.
- **Audit-stamp confusion (§6.11 v1-r1 tightening).** R3 uses shell-hash, not full-prompt hash. If a test uses the full-prompt hash as the audit input, `grant-content-never-flows` invariant leaks silently. Mitigation: explicit `test_adv_full_prompt_hash_is_never_persisted_in_r3_path`.
- **Register v2.2 format drift.** v2.2 adds `progressive_register` field; adapter MUST tolerate missing field on legacy entries. Mitigation: per-entry default `progressive_register="OK"` when absent; documented in adapter docstring; `test_admin_risk_legacy_entry_without_progressive_register_defaults_to_ok`.
- **Two-axis dialect discipline miscoding as three-axis.** Applicant-identity overlay + federal + progressive could be read as three axes; register v2.2 treats it as an overlay on the progressive axis, not a third axis. Mitigation: docstring + `test_admin_risk_applicant_identity_is_overlay_not_third_axis`.
- **Cedar `org_isolation` policy compile-time drift.** Cedar policy lives in vault; if unsigned or mismatched → F-PRE-04 at PRE-gate check #4 fires BEFORE Scribe even enters. R3 does NOT re-implement Cedar compile; consumes `pipeline.logician.cedar_eval.compile_cedar_policy` output as-is. Mitigation: `test_pre_gate_compile_delegates_to_cedar_eval` pins non-reimplementation.

## 12. Hardenings (delta — template §4 checklist)

- [ ] `seat.py::run_seat` signature: all I/O and collaborators are injected callables (E-017).
- [ ] `__main__` block is the sole `sys.exit` caller.
- [ ] Every failure code exported as inline-literal string constant AND referenced by-name in wiring.
- [ ] Admin-risk register load is Vault-primitive-only (no raw `open()`).
- [ ] BYOK key load is `pipeline.sovereignty.byok.load_key` only (Cedar `byok_key_scope` enforced upstream).
- [ ] Compiled prompt is `compiled_prompt_shell` hash, never full-prompt hash.
- [ ] `ScribeEnvelope` + `ScribeResult` are frozen, kw-only, slots=True (A-13).
- [ ] Transport-retry: 120s cap, single-shot retry on connection-level errors only, 30s health-check.
- [ ] No `pipeline.loop` import (AST-lint R2 check — but R2 rule currently does NOT sweep `pipeline/seats/`; confirm at R3 AST-lint spin).
- [ ] E-017 / E-024 / E-027 / E-028 disciplines all cited in module docstrings.
- [ ] BLUEPRINT_DEPS pins §7 v1.1.1 + §6 v1-r1 + §5 v6 + §4 v2.1 + §2 v7.1.
- [ ] L-015 citation regression extended to cover R3 module tree.

## 13. Open questions for operator (non-blocking; surface before dispatch)

- **OQ-1 — `pipeline.providers.anthropic` module existence.** R3 currently assumes a minimal BYOK Anthropic binding lives in `pipeline/seats/scribe/provider_anthropic.py` (seat-local). A proper `pipeline/providers/anthropic.py` refactor (reusable across seats) is v0.1.1 scope per `pipeline/providers/` currently being empty. Confirm seat-local binding for v0.1.0 OR request providers-refactor handoff before R3 dispatch. **Recommendation: seat-local at v0.1.0; refactor at v0.1.1** (R3 ships fastest; Editor R3 + Judge R3 can reuse the pattern).

- **OQ-2 — Scribe SFR emission at R3 vs v0.2.** §F.1 says Scribe is NOT exempt from SFR (unlike Editor). §6.5 ships the SFR format. R3 can land either (a) full SFR emission (Premises / Trace / Conclusion) from every Scribe draft, or (b) a stub hook that logs SFR-shaped events for R4-and-forward flesh-out. **Recommendation: stub hook at R3, full SFR at v0.1.1** (full SFR emission doubles the LLM call surface; not needed for first-run acceptance gate #12).

- **OQ-3 — Seat-envelope.v1 schema row-append venue.** R1 OQ-4 at that round was resolved "row-append at Scribe R3 LOCK to §0.5". Confirm §0.5 amendment venue: (a) standalone §0.5 v6.1 narrow-append atomic with R3 LOCK, OR (b) carry through to a §0.5 v7 bundle with Editor-R3 + Judge-R3 seat envelopes. **Recommendation: (a) narrow-append at R3 LOCK**; Editor + Judge are R1-R3 parallel sessions so an (b) bundle would create ordering constraints.

- **OQ-4 — Per-section-iteration vs full-draft-per-invocation dispatch.** Revision loop (§5 R5+) calls Scribe per iteration. R3's envelope carries ONE `section_spec`; does each `invoke_seat` call draft ONE section (N=13 calls for a full first draft) OR the full draft tuple? Spec card assumes ONE section per call (simpler; matches R2 per-section composer shape). Confirm or request batched-sections envelope.

- **OQ-5 — Draft-vault-persistence timing.** §5 R4 `seat_runner` treats `vault_write` as Round 5 concern (`_ = vault_write` in R4). R3 does NOT persist drafts to vault directly (per §4.3 blueprint + §4.10 dispatcher — R5 revision_loop persists). Confirm: R3 emits `ScribeResult` only; revision_loop at §5 R5+ writes to `orgs/<slug>/drafts/<run_id>/sections/*.json`. **Recommendation: confirm — matches §5 design; R3 remains pure stdout emitter.**

- **OQ-6 — `F-SCRIBE-BYOK-MISSING` §7.13 registration.** This code is new at R3 (not a §7.13 entry). Options: (a) §7.13 narrow-append during R3 LOCK (requires §7 v1.2 cut), OR (b) treat as R3-local operational failure code, documented in spec card but not in §7.13 registry. **Recommendation: (b)** — BYOK discipline is architectural (§E M13 signed bypass pathway owns it); Scribe's job is to fail-closed when key absent; not every per-seat operational failure is a §7 blueprint amendment.

## 14. Non-goals at R3

- No proper `pipeline/providers/anthropic.py` refactor — v0.1.1.
- No full SFR emission — hook stub only (v0.1.1 flesh).
- No vault-write of drafts — §5 R5+ revision loop.
- No Phase 0 RFA extractor module — v0.2 roadmap (§7.3).
- No qualitative-paraphrase semantic match — v0.2 (numeric-verbatim only at R3).
- No multi-tenant operator authority (Class 11-12 of §6.6 deferred) — v2.
- No additional dialects beyond the four — §D.2 invariant.
- No Editor / Judge integration beyond handoff-contract pointer — §8 / §9 own those seats.

## 15. Unblocks

- **Scribe whole-seat LOCK** at R3 LOCK (§7 v1.1.1 promoted to pipeline-live).
- Editor R1 + Judge R1 already unblock at **R2 LOCK** (both consume `SectionDraft` schema from R2) — NOT R3-gated. (Correction to prior handoff language: R3 unblocks whole-seat LOCK, not Editor/Judge R1 sessions.)
- §5 R5+ revision loop — consumes `ScribeResult` stdout from R3 as the draft-persistence input.
- First-run acceptance gate #12 (roadmap) — requires whole-seat Scribe LOCK + Editor + Judge LOCKs; R3 is the Scribe critical path.
- §0.5 v6.1 narrow row-append (seat-envelope.v1 + scribe-result.v1 rows) at R3 LOCK per OQ-3.

## 16. Artifacts (populated at R3 LOCK)

- `pipeline/seats/scribe/seat.py` (R3 primary)
- `pipeline/seats/scribe/provider_anthropic.py` (R3)
- `pipeline/seats/scribe/admin_risk_adapter.py` (R3)
- `pipeline/seats/scribe/logician_wiring.py` (R3)
- `tests/scribe/test_seat.py` + `test_provider_anthropic.py` + `test_admin_risk_adapter.py` + `test_logician_wiring.py`
- `tests/scribe/test_adv_seat_subprocess.py`
- `tests/corpus/scribe/v1/subprocess/` (happy-path + error-surface fixtures)
- Committee dispatch artifact tree: `pipeline/validation/code_reviews/scribe_round_3_<module>/` (per-module, 4 dispatches)
- LOCK row in `pipeline/engineering/lock_history.v1.jsonl`
- `pipeline/engineering/review_lessons.v1.md` entries if E-017 / E-024 / E-027 firings accumulate

## 17. Changelog

- **v1 PRE-STAGED 2026-04-21.** Authored post-R1 LOCK (row 120) + post-§6 v1-r1 LOCK (same day, interlock §7.15 SATISFIED) + post-§7 v1.1.1 LOCK. Awaits R2 LOCK before Code-window paste — R3 imports R2's `SectionDraft` schema + composition modules. Parent spec-card (`section_7_council_seats_pipeline_modules.md`) Lane A step 5 closure.

*End spec card — PRE-STAGED. Code-window paste gated on (a) Scribe R2 LOCK, (b) operator triage of OQ-1..OQ-6 above.*
