# Spec card — pipeline.seats.{scribe,editor,judge} (Section 7: Council seats as production pipeline modules)

**STATUS:** READY (Scribe R1 UNBLOCKED) 2026-04-21 — §6 Operating Envelope v1-r1 LOCKED 2026-04-21 + §7 Scribe v1.1.1 LOCKED 2026-04-21 (both compound with §0.5 v6/v7 amendments). §7.15 prerequisite interlock SATISFIED. Scribe R1 can dispatch. §8 Editor + §9 Judge blueprint rounds remain open (parallel-safe preconditions to Editor R2 + Judge R2). See focused R1 card: `section_07_scribe_round_1_types_and_kgie.md`.

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, dev-vs-prod, standard interface pattern — not restated here).

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_07_scribe.md` **v1.1.1 LOCKED 2026-04-21** (this spec builds the Scribe module against it; §7 LOCK prerequisite satisfied)
- `pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md` **§0.5 v7 LOCKED 2026-04-21** (companion amendment; rows 118-158 register Scribe primitives)
- `pipeline/blueprint/v0.1/section_06_operating_envelope.md` **v1-r1 LOCKED 2026-04-21** (§7.15 prerequisite satisfied — router.yaml schema A2, SFR format A3, context-placement lint A4, track-registry A6 all runtime-live)
- `pipeline/blueprint/v0.1/section_00_5_interface_index.md` v4/v5 LOCKED 2026-04-19 (seat-output interface contract rows — Scribe row set enumerated in §7.17; Editor/Judge rows currently `pipeline.contract.editor` / `pipeline.contract.judge` stubs at §0.5 and require §8/§9 blueprint rounds to expand)
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-18 (§4.3 Scribe invocation; §4.4 Editor; §4.5 Judge — the `invoke_seat` subprocess contract the seats must satisfy)
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 LOCKED 2026-04-19 + `section_04_v2_2_consolidated_amendment.md` (PRE/POST gate table — every Scribe F-SCRIBE-* code per §7.13 has to route through Logician PRE-gate slot or POST-gate sweep)
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 A1-A12 LOCKED 2026-04-19 (§D.2 Scribe, §D.3 Editor, §D.4 Judge; §E cross-family rigor; §D.7 Opus 4.7 envelope; §D.8 F-CONTEXT-PLACEMENT)
- `router.yaml` — seat bindings (Scribe = anthropic/claude-sonnet-4-6 primary + opus-4-6 escalation; Editor = meta/llama-3.3-70b + openai/gpt-4o-mini; Judge = google/gemini-2.5-pro + groq/qwen3-32b). Reference, never hardcode inside the modules.

**Spec-card version:** v1
**Round:** §7 — Council seats as pipeline modules (three seats, three independent LOCK cycles)

---

## 1. Purpose

Promote Scribe, Editor, and Judge from **OpenClaw-skill-only** operational artifacts to **production pipeline modules** under `pipeline/seats/`, bound to Thesis Team review and the §4.1 PRE/POST gate discipline, so that `pipeline.loop.seat_runner.invoke_seat` can orchestrate real seat code (not skill shells) end-to-end.

**Current state.** `skills/scribe-ghostwriter/SKILL.md`, `skills/editor/SKILL.md`, `skills/judge-rubric/SKILL.md` are prose-heavy skill definitions Josh has won three grants with in 2026; `pipeline/orchestrator/seats/{editor,judge,red_team,scout}.py` are legacy CLI stubs that shell out to `router.call_seat()` and write single JSON artefacts — none of them satisfy §4.1 gate-runner contracts, none consume `SeatInvocationContext`, none emit the §7 / §0.5-indexed dataclasses (`SectionDraft`, `KgiePreflightResult`, etc.).

**Gap.** `pipeline.loop.seat_runner` launches subprocesses bound to `seat_kind ∈ {scribe, editor, judge}` with a minimal-env whitelist and expects each subprocess to consume a stdin JSON envelope and emit structured stdout per §4.3-§4.5. No subprocess binary exists. The revision loop (Round 5) already LOCKED — it has no seats to call.

**Critical-path position.** Lane A step 5 per `pipeline/business/final_roadmap_to_ship_2026-04-21.md`. Blocks Group 9 E2E integration (Lane A step 6) which blocks ship gate #12. Without this, the Tilth pipeline has *nothing to orchestrate.*

## 2. Proposed module layout

Recommend **`pipeline/seats/{scribe,editor,judge}/`** — NOT nested under `pipeline/loop/`. Rationale:

- `pipeline/loop/` owns *orchestration state* (revision loop, post-gate runner, seat-runner dispatch). Seat *authors* have a different lifecycle (prompt compilation, dialect code-switch, SMART outcome generation, rubric scoring) and a different §0.5 row set (`scribe.*.v1`, `editor.*.v1`, `judge.*.v1` — not `pipeline.loop.*`).
- `pipeline/seats/scout/` does not exist either (Scout is Section 3 with its own 10-round blueprint and committee dispatch); `pipeline/seats/` as a parent namespace is a clean home for the four non-Logician seats without cross-binding to the pipeline orchestrator's internal namespace.
- The AST-lint R2 ban on `pipeline.loop` importing `pipeline.logician` (Round 1 rule) remains clean; seats import from `pipeline.logician` (they enforce PRE/POST gate contracts), from `pipeline.vault` (they persist drafts), and from `pipeline.providers.<provider>` (adapter layer per engineering process §4.5).

Per-seat layout:

```
pipeline/seats/scribe/
  __init__.py              # __all__ public surface
  types.py                 # RfaExtractedRecord, KgiePreflightResult, SectionDraft, SmartObjective, OverlookedExpensesWalk, ProgramTemplate, AdminRiskFlag, ClaimEvidence (frozen, kw_only — §7.3-§7.11)
  kgie.py                  # KGIE preflight predicate (§7.4)
  smart.py                 # SMART outcome generator (§7.6)
  overlooked_expenses.py   # Overlooked-expenses checklist walker (§7.7)
  dialect.py               # Funder-dialect code-switch (§7.8)
  templates.py             # Program-template loader (§7.9)
  admin_risk.py            # Admin-risk register query + flag generator (§7.11, §7.16)
  compress.py              # Word/character/page limit protocol (§7.10)
  seat.py                  # Main entry: reads stdin envelope, dispatches to phases, emits stdout
  prompt_template.py       # Prompt compilation (consumed by §6 Operating Envelope lint when LOCKed)
  BLUEPRINT_DEPS           # per §4.6 engineering process
```

Editor + Judge mirror the shape. Editor's `seat.py` consumes `SectionDraft[]`, emits `EditorFindings` (one issue set per section, 2-3 replacement options per issue — §8 blueprint round will pin the schema). Judge's `seat.py` consumes finalized drafts + `claim_evidence_map`, emits `JudgeVerdict` (per-criterion score + evidence + missing, §9 round pins the schema — the rubric library already exists at `pipeline/rubrics/`).

## 3. Interface contract (from §0.5 + seat_runner)

Seats are subprocess binaries invoked by `seat_runner.invoke_seat`. Contract:

- **Input envelope** (stdin, JSON bytes): constructed by Round 5 `revision_loop` caller — shape is under-specified in §0.5 today. Fields inferred from `SeatInvocationContext` + §7/§8/§9 handoff contracts: `session_id`, `run_id`, `org_slug`, `iteration_number`, `seat_kind`, `rfa_extracted_record` (Scribe), `kgie_result` (Scribe), `program_template` (Scribe), `dialect` (Scribe/Editor), `section_drafts[]` (Editor/Judge), `rubric_path` (Judge), `claim_evidence_map` (Judge). **[NEEDED from operator / §0.5 gap]:** canonical envelope schema row (`pipeline.contract.seat_envelope.v1`). Currently silent — propose row-append at Scribe LOCK.
- **Output envelope** (stdout, JSON bytes, no fences per Rule 4): seat-specific. Scribe → `tuple[SectionDraft, ...]` + `claim_evidence_map` + `admin_risk_flags[]` + `scope_check_comments[]` + `draft_dialect`. Editor → `EditorFindings` (per §8). Judge → `JudgeVerdict` (per §9 — must match `default_judge_parse` shape: non-empty JSON object; semantic validation downstream at Logician POST).
- **Env whitelist:** exactly the six keys in `seat_runner.MINIMAL_ENV_ALLOWED_KEYS` — `PATH`, `HOME`, `TILTH_SESSION_ID`, `TILTH_RUN_ID`, `TILTH_ORG_SLUG`, `TILTH_SEAT_KIND`. Seats MUST NOT read any other env var; API keys loaded via `pipeline.providers.<provider>` adapter from operator keyring (not env).
- **Timeouts:** Scribe 300_000 ms, Editor 180_000 ms, Judge 180_000 ms (inline-literal at dispatch per §4.3-§4.5 V1 rebind-resistance).
- **Cross-family invariant:** `seat_runner._level_collides_with_prior` advances cascade when family collides. Seat code MUST report `landed_family` + `landed_model_id` on stdout header so the subprocess launcher can populate `SubprocessResult.landed_family` truthfully (A-v1-02 trust model).
- **PRE/POST gate binding:** every §7.13 Scribe failure code, and equivalent §8/§9 Editor/Judge codes, maps to a §4.2.1 Logician gate slot. Seat code calls `pipeline.logician.gate_runner.evaluate_pre(...)` before substantive work and surfaces `F-*` verdicts with SFR format (architecture §F.1). Editor is SFR-exempt per §F.1 (feedback, not verdict); Scribe + Judge are NOT exempt.
- **Claim-evidence map (Scribe + Judge):** canonical-byte signed via §4 Logician Round 2 assembler; Judge consumes via `PostGateInput` assembled by Round 6 `post_gate_runner`.

## 4. OpenClaw-skill binding pattern — ADAPTER vs. PORT

**Option A — Thin adapter.** Seat module's `seat.py` is a ~200 LOC adapter: validate stdin envelope against §0.5 schema, run Logician PRE-gates, **invoke the OpenClaw skill via `clawdis` subprocess** passing compiled prompt + structured inputs, capture skill stdout, parse + validate against §7 dataclasses, run Logician POST-gates, emit stdout. Skill text (`SKILL.md` system prompts, template library under `skills/scribe-ghostwriter/templates/`) is the load-bearing prose; pipeline code is the envelope + gate enforcement.

- *Pros:* Preserves Josh's three-grant-proven skill prompts verbatim. Minimal surface area to LOCK — skills are already operational. Change-one-place discipline when prompt tuning is needed (edit `SKILL.md`, no code rebuild). Honors the "grant writing skill works TODAY" directive in CLAUDE.md.
- *Cons:* Two-process invocation (seat subprocess → clawdis subprocess → LLM provider) increases wall-clock + failure surface. Couples production pipeline to clawdis's install-tier stability — clawdis catalog/SDK drift becomes a Logician failure code. Skill output shape is plain-text narrative with embedded JSON; parse fragility is a persistent test burden.

**Option B — Full port.** Seat module re-implements the Scribe phase pipeline (Phase 0 extract → Phase 1 KGIE → Phase 2 drafting → Phase 3 assembly) in Python, with prompts compiled via `prompt_template.py` from source-of-truth template files under `pipeline/seats/scribe/templates/` (migrated from `skills/scribe-ghostwriter/templates/`). Provider calls go through `pipeline.providers.<provider>.complete()` adapter layer (engineering process §4.5).

- *Pros:* One-process invocation; direct control over retry + token accounting + telemetry; native dataclass round-trip (no JSON-out-of-prose parse); clean §4.5 provider-adapter path; clawdis removed from the production dependency graph (still available for operator workflows). Testability goes from "golden-corpus fuzz" to "unit test every phase predicate." Prompt-template lint (§6 Operating Envelope) can validate every prompt at CI time, not at runtime.
- *Cons:* Largest LOC scope of any §5-family round (~1500-2000 LOC for Scribe alone given §7's 17-subsection blueprint). Risk of drift from Josh's battle-tested skill prose. Longer critical path — 3-4 Code sessions per seat instead of 2.

**Recommendation: Option B (full port) for Scribe and Judge; Option A (adapter) for Editor as a v0.1.0 shortcut.**

Rationale: Scribe carries the highest RFA-traceability + Law 5 enforcement burden — adapter pattern makes PRE/POST-gate coverage on `F-SCRIBE-UNSOURCED-CLAIM`, `F-SCRIBE-SMART-INVENTED-METRIC`, `F-SCRIBE-DIALECT-DRIFT` brittle (grep-over-narrative). Judge is the scoring backbone; its output must satisfy A3 SFR format and Logician POST-gate rubric-conformance — skill-parse fragility is unacceptable here. Editor is SFR-exempt, its output is structured feedback with a well-defined JSON schema already validated by `pipeline/orchestrator/seats/editor.py` — the existing adapter pattern works; promote + harden rather than port. Editor port can happen in v0.1.1 if drift issues surface.

This recommendation assumes §7 Scribe blueprint LOCKs close to its current shape (v1 SCOPING DRAFT → LOCK v1 via Thesis round). If §7 LOCK compresses scope substantially, revisit.

## 5. Per-seat dispatch plan (round-by-round)

Total estimate: **8 Code sessions** (matches roadmap's 6-9 envelope).

**Scribe (first; 3 sessions).** Anthropic primary binding; longest blueprint; most §0.5 row appends.
- *Scribe R1 — types + Phase 0 + KGIE* (`types.py`, `kgie.py`, corpus fixtures). LOCK on `RfaExtractedRecord`, `KgiePreflightResult`, `GeographyRecord`, `IdentityClaim`, `ExperienceSummary`. Tests: frozen-dataclass pins, KGIE PASS/FAIL/NEEDS_INPUT cases. Depends on §7 LOCK; does NOT depend on §6 LOCK yet (prompt-template lint applies only at Phase 2 drafting).
- *Scribe R2 — Phase 2 drafting + SMART + Overlooked + Dialect + Templates* (`smart.py`, `overlooked_expenses.py`, `dialect.py`, `templates.py`, `compress.py`). LOCK on `SectionDraft`, `SmartObjective`, `OverlookedExpensesWalk`, `ProgramTemplate`, dialect register enum. Corpus: VAPG + REAP + SCBGP + SARE golden drafts per §7.14.
- *Scribe R3 — seat.py + admin_risk.py + stdin/stdout envelope + PRE/POST gate wiring* (`seat.py`, `admin_risk.py`, `prompt_template.py`). LOCK on subprocess entry point. Depends on §6 Operating Envelope v1 LOCK (§7.15 prerequisite-interlock) or an explicit waiver row. §0.5 row-append ≈ 30 rows per §7.17.

**Editor (second; 2 sessions).** Cross-family against Scribe (Meta/OpenAI); adapter-pattern port of `pipeline/orchestrator/seats/editor.py`.
- *Editor R1 — §8 blueprint round* (not a code session — this is a blueprint authoring round parallel to §7 Scribe to produce `pipeline/blueprint/v0.1/section_08_editor.md` v1 SCOPING DRAFT, Thesis-audited, LOCK). Surfaces `EditorFindings` schema, failure codes (`F-EDITOR-*`), revision-loop contract with Scribe. Must LOCK before Editor code session.
- *Editor R2 — module harden + adapter* (`pipeline/seats/editor/{types.py, seat.py}`). LOCK on `EditorFindings`, `ClarityIssue`, `TaxonomyCheck`. Carries the existing Editor system prompt + 2-3-replacement invariant from the skill. PRE/POST gate: `F-EDITOR-SINGLE-REPLACEMENT` (Logician counts `replacements[]` length, enforces 2-3), `F-EDITOR-REWRITE-SILENT` (Law 4 — draft body MUST NOT be rewritten).

**Judge (third; 3 sessions).** Google primary + Reasoner Review escalation; full-port (Option B); SFR format mandatory.
- *Judge R1 — §9 blueprint round* (blueprint authoring parallel to §7/§8; produces `pipeline/blueprint/v0.1/section_09_judge.md` v1 SCOPING DRAFT → LOCK). Surfaces `JudgeVerdict`, `CriterionScore`, rubric-library dispatch contract, three-way cross-family rigor, A3 SFR format binding.
- *Judge R2 — types + rubric loader + scoring predicates* (`types.py`, `rubric_loader.py`, `score_dispatch.py`). Consume `pipeline/rubrics/vapg_fy26.json` + 12-dimension 90+ rubric. PRE-gate: `F-JUDGE-CROSS-FAMILY-COLLISION` (live family consult per `run_iteration_families_so_far`), `F-JUDGE-RUBRIC-MISSING`.
- *Judge R3 — seat.py + SFR emission + POST-gate wiring* (`seat.py`, `sfr_format.py`). LOCK on subprocess entry + A3 `F-VERDICT-CERT-MALFORMED` POST-gate. §0.5 row-append.

Parallelism: §8 + §9 blueprint rounds can dispatch in parallel with Scribe R1 (no shared Code dependency). Editor R2 + Judge R2 cannot start until Scribe R3 has locked the `SectionDraft` schema (Editor consumes it; Judge consumes it + claim-evidence).

## 6. Dependencies (ordering)

1. **§2 Vault LOCK** — required before Scribe R3 (seat persists drafts via §2 dispatcher SIMPLE path; test `test_int_scribe_emits_draft_atomically` per §7.14 depends on §2 `vault_write` being real code, not a stub).
2. **§4 Logician 9-module full committee review** — required before any seat R3 (PRE/POST gate calls must route through real `gate_runner`; `F-SCRIBE-*` slots must be wired in §4.2.1 table v2.1-or-later).
3. **§5 capstone LOCK** — required before Editor R2 + Judge R3 (Scribe R3 only needs §5 v6 seat-runner interface, which is LOCKED; downstream seats need `revision_loop` + `post_gate_runner` stable to assemble `PostGateInput`).
4. **§6 Operating Envelope v1 LOCK** — required before Scribe R3 + Judge R3 (prompt-template lint enforces `F-CONTEXT-PLACEMENT`; router.yaml schema validates provider bindings; A3 SFR format pinned here). ✅ **SATISFIED — §6 v1-r1 LOCKED 2026-04-21** (compound with §0.5 v6 amendment per §6.17). Runtime-live.
5. **§7 Scribe v1 LOCK** — required before Scribe R1. ✅ **SATISFIED — §7 v1.1.1 LOCKED 2026-04-21** (compound with §0.5 v7 amendment). Thesis Rounds 1+2 complete under L-005 two-audit cycle + narrow-fix carve-out (see `pipeline/validation/section_07_thesis_round_2/CLOSEOUT.md`).
6. **§8 Editor v1 LOCK + §9 Judge v1 LOCK** — required before Editor R2 and Judge R2 respectively.

Order for critical path: (§7 LOCK ‖ §2/§4/§5 completion) → Scribe R1 → Scribe R2 → (§6 LOCK ‖ §8 LOCK ‖ §9 LOCK) → Scribe R3 → Editor R2 ‖ Judge R2 → Judge R3.

## 7. Committee composition per seat

Reference `router.yaml` `code_reviewer_*` rows — same five-reviewer committee as every §5 / Scout round (engineering process §3).

**Cross-family guard specific to seat reviews:** per architecture A3 and the §D.4 Section E invariant, **Judge-seat review MUST NOT share family with Judge's own production binding**. `router.yaml` binds Judge to `google/gemini-2.5-pro` primary. Therefore Judge R1-R3 committee's `code_reviewer_3` (algorithm + blueprint adherence) family assignment cannot be Google; Llama 3.3 70B stays as the default. Operator should confirm before Judge R2 dispatch that no reviewer in the five-seat committee is running on Google — substitute to `gpt-oss-120b` or `kimi-k2` if drift occurs.

Scribe and Editor committees: standard five-reviewer ensemble (codex / qwen3-32b / llama-3.3-70b / gpt-oss-120b / kimi-k2). Scribe's production binding is Anthropic; none of the five code-reviewers are Anthropic — clean.

Thesis Team (non-code) reviews each seat's blueprint round (§7, §8, §9): Editor (Llama 3.3 70B Meta) + Judge (Qwen 3 32B Alibaba) + Red Team (gpt-oss-120b OpenAI-OSS). Scribe is authored by Anthropic (Opus 4.7 under §D.7 envelope) — cross-family satisfied.

## 8. Done definition per seat

- Module exists at `pipeline/seats/<seat>/` with `__init__.py` declaring `__all__` (public-API boundary per engineering process §4.1).
- Every public function signature satisfies §0.5 interface index row; new rows appended per §7.17 (Scribe ~30 rows) / §8 (TBD) / §9 (TBD).
- Every §7.13 / §8 / §9 failure code has a Logician PRE- or POST-gate slot; gate-runner fires on fixture-induced violation (not just unit-test assertion).
- Test surface per §7.14: **30+ tests + 5+ adversarial** per seat, covering frozen-dataclass pins, corpus fixtures (≥4 pass + ≥6 fail), property tests (section ordering, claim-evidence exhaustiveness, dialect invariance over N runs), and integration tests (seat-under-seat-runner, atomic vault write, cross-family collision).
- **Coverage ≥ 95%** on the seat's module tree.
- **AST-lint clean** — R1-R7 violations = 0 (R2 `loop-logician-ban` does NOT apply to `pipeline/seats/` since seats DO import Logician for gate calls; confirm lint config exempts `pipeline/seats/` or adds a `seats-logician-allowed` rule).
- **Thesis 5/5 PASS** on the Code Thesis Committee (Scribe R3 / Editor R2 / Judge R3 — the subprocess-entry rounds carry the highest stakes; R1/R2 may self-LOCK per §5 precedent if single-cycle clean).
- **LOCK row** appended to `pipeline/engineering/lock_history.v1.jsonl` with reviewer tokens, test count, F-code coverage.
- **E2 LOCK summary** delivered to operator per engineering process §5.
- BLUEPRINT_DEPS declaration per §4.6 (hash-pinned to §7/§8/§9 LOCK versions).

## 9. Failure modes (delta — framework taxonomy per template §3)

- **Aspiration-as-enforcement on §6 prerequisite-interlock (L-006):** LOCKing Scribe R3 ahead of §6 Operating Envelope v1 LOCK ships a seat whose F-CONTEXT-PLACEMENT PRE-gate has nothing to lint against. Dev-mode symptom: gate always passes. Prod-mode failure: prompt register-drift goes undetected, Judge scores degrade, Law 4 silently violated.
- **Cross-family drift at Judge committee dispatch:** router.yaml Judge primary binding can silently drift (EN-003 family-substitution pattern). Mitigation: Scribe R3 test `test_int_scribe_cross_family_rigor_enforced` already exists in §7.14; extend to Judge R3 + Editor R2. Add Logician PRE-gate `F-ROUTER-FAMILY-COLLISION` to seat cold-start.
- **Skill-adapter output parse fragility (Option A on Editor):** LLM wraps JSON in prose fences or adds self-commentary despite system prompt. Mitigation: `strip_fences` + `extract_json` per existing `pipeline/orchestrator/seats/editor.py:149`; harden with schema validation + retry-with-clarification bounded at N=2.
- **Silent fallback on provider cascade exhaustion:** seat_runner raises F_PIPE_06 on timeout exhaustion. Seat code MUST propagate, not swallow — adversarial test per seat.

## 10. Hardenings (delta — template §4 checklist)

Per-seat verification at LOCK:
- [ ] Cedar gate bound for `seat-draft-write` intent (§2 vault dispatcher allowlist)
- [ ] Logician PRE-gate slot assigned and wired in §4.2.1 table (Scribe 8 codes; Editor TBD; Judge TBD)
- [ ] Logician POST-gate slot assigned (Scribe 10 codes; Editor TBD; Judge 1 SFR-format + N rubric codes)
- [ ] Fallback cascade per §D.7 envelope (Scribe escalation Opus → Judge escalation Reasoner Review; Editor no escalation — v0.1 accepts degraded-mode on Editor outage)
- [ ] State persistence on failure (seat writes partial telemetry to vault even on F_PIPE_*)
- [ ] Self-validation step (Rule 2 Magic: Scribe validates KGIE PASS before emitting draft; Judge validates all 12 dimensions scored before emitting verdict — currently present in `orchestrator/seats/judge.py:77` docstring; promote to hard predicate)
- [ ] Admin-risk register scan integration (Scribe Phase 2 + Editor `terms_to_verify` output — already present in skill; must route through Logician scanner, not in-seat)

## 11. Open questions for operator

- **OQ-1 — Adapter vs. port on Editor.** Recommendation above is adapter (Option A) for v0.1.0, promote to port in v0.1.1. Accept or flip to port-now?
- **OQ-2 — Module location.** Recommendation is `pipeline/seats/{scribe,editor,judge}/`. Alternative is `pipeline/council/{scribe,editor,judge}/` or nested under `pipeline/loop/seats/`. `pipeline/seats/` argued for on grounds above. Confirm or override.
- **OQ-3 — §6 Operating Envelope round scheduling.** §7.15 hard-links Scribe R3 LOCK to §6 v1 LOCK. Does §6 blueprint round open before, parallel to, or after §8/§9 blueprint rounds? Recommendation: §6 opens first (Scribe R3 is the longest critical path). Operator call on whether this displaces Lane B items.
- **OQ-4 — Seat-envelope canonical schema.** No §0.5 row exists for the stdin-envelope shape `seat_runner` passes to subprocesses. Propose `pipeline.contract.seat_envelope.v1` row-append at Scribe R3 LOCK. Confirm or redirect to §6.
- **OQ-5 — v0.1.0 fallback split.** Roadmap risk-register line 169: if 6-9 session estimate exceeds, split v0.1.0 = Scribe + Logician only, v0.1.1 = Editor + Judge. Is that split still live? If yes, which seat does v0.1.0 ship with for the fifth-seat test (v0.1.0 without Editor + Judge means Scribe's draft goes straight to Logician POST-gate → operator — no clarity review, no rubric scoring). Recommendation: keep the split as emergency reserve but aim for full 8-session delivery.
- **OQ-6 — `skills/` retirement path.** When Option B ports land, does `skills/scribe-ghostwriter/` stay as operator-workflow artefact (Josh runs it outside pipeline for ad-hoc grant work) or get sunset? Recommendation: keep both. Skills stay operator-workflow; production pipeline uses the ported module. Documented in seat module docstrings.

## 12. Non-goals

- **Scout seat** — out of scope. Scout has dedicated Section 3 blueprint (LOCKED v5 2026-04-17), dedicated 10-round spec-card sequence (`scout_round_{1..10}`), and is already in active production code under `pipeline/seats/scout/` (via Scout Round 1-10 dispatch track). This spec does not touch Scout.
- **Logician seat** — out of scope. Logician is deterministic Python + Cedar (architecture §D.5 + §D.7); it has no LLM subprocess, no `seat_runner` invocation path, no cross-family concern. Its 9-module review is a separate Lane A step 3 and a prerequisite (§6 of this spec) not an in-scope deliverable.
- **Red Team seat** — out of scope at v0.1 council-seats scope; Red Team fires at Thesis-Team audit time (architecture §F), not in the runtime council loop. A v0.2 backlog candidate if operator elevates.
- **UI / operator-review surface** — out of scope. Seats emit JSON to vault; operator reads via existing headless artefacts. No UI per CLAUDE.md.
- **Three-tab delivery** — §4.11 / §5.9. Round 8+ in the §5 pipeline track; not part of this spec.
- **Blueprint authoring for §8 and §9** — noted as dispatch-plan prerequisites but the authoring itself is separate blueprint rounds with their own Thesis audits. This spec authors neither §8 nor §9.

## 13. Critical-path position + why this is the biggest unsurfaced gap

Lane A step 5 per `pipeline/business/final_roadmap_to_ship_2026-04-21.md`. Gate:

> Without this step, `pipeline.loop.seat_runner.invoke_seat` launches subprocesses that do not exist. The revision loop that LOCKED at §5 R5 has nothing to drive. Integration tests at Lane A step 6 cannot be written because the seats they would integrate do not exist as production modules. Ship gate #12 (first-run grant completes E2E with operator sign-off) is mechanically unreachable.

Currently the work is shadowed inside `skills/` as Cowork-operator artefacts that work TODAY for Josh's manual grant work — which obscured the fact that the *pipeline* carries no seats. The OpenClaw skills are prose, not modules; they have no §0.5 rows, no PRE/POST gate wiring, no subprocess entry point, no `router.yaml` binding the pipeline code actually consults, no telemetry emission per §5 §5.6 schema.

This spec is the bridge. Without it, every Lane A item downstream is blocked.

---

## Changelog

- **v1 PRE-STAGED 2026-04-21.** Authored as Lane A step 5 scoping card. Pre-staged before §7 Scribe blueprint LOCK; Scribe R1 blocked until §7 LOCK (expected 1-2 Thesis rounds out). §8 Editor + §9 Judge blueprint rounds not yet opened — prerequisite for Editor R2 + Judge R2 respectively. Operator decision queue: OQ-1..OQ-6 above.

*End spec card — PRE-STAGED; awaits operator review before Code session opens Scribe R1.*
