# Spec card — Demo Driver: MVP end-to-end pipeline (one grant through the full council)

**STATUS:** PRE-STAGED 2026-04-29

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, standard interface pattern — not restated).

---

## 1. Purpose

The demo driver is the **"one grant through the pipeline" integration test**: ingest a real RFA → Scout discovery + verify → Scribe draft → Editor pass → Judge score → Logician gate → output. This is the proof that Tilth v0.1 works end-to-end on the operator's 8 GB M1 Mac Mini.

This is NOT a new module. It is a **test harness + orchestration script** that exercises the existing `pipeline.loop.run_pipeline` capstone (§5 R11, LOCKED) with a real RFA, real PROJECT_CONTEXT, real rubric, and real API keys — the first time all five council seats fire in sequence outside of unit/integration tests.

**The demo driver answers one question:** Does the pipeline produce a scored, gated, audited grant proposal from a standing start?

---

## 2. Blueprint anchors

- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED — §4.1 `run_pipeline` 11-step submission-mode lifecycle. The demo driver invokes `run_pipeline` and verifies all 11 steps execute.
- `pipeline/blueprint/v0.1/section_03_scout.md` — Scout DISCOVER → VERIFY → REVIEW lifecycle.
- `pipeline/blueprint/v0.1/section_07_scribe.md` v1.1.1 LOCKED — Scribe seat invocation.
- `pipeline/blueprint/v0.1/section_06_operating_envelope.md` v1-r1 LOCKED — prompt compilation, SFR format.
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 LOCKED — PRE/POST gates on every seat.
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 — Five Laws, council composition, sovereignty promise.
- `pipeline/rubrics/vapg_fy26.json` — VAPG FY26 rubric (demo rubric).
- `router.yaml` — seat bindings for all six seats (per v7.0.6 SELF-LOCKED 2026-05-09).

---

## 3. Prerequisites (ALL must be LOCKED-as-a-whole-section)

| Section | Seat/Component | Status |
|---|---|---|
| §1 | Sovereignty Envelope | LOCKED ✅ (Round J) |
| §2 | Vault Topology | LOCKED ✅ (Round K) |
| §3 | Scout | Required — whole-section capstone |
| §4 | Logician | Required — Round L capstone (Batches A/B/C + v2.2/v2.3/v2.4/v2.5) |
| §5 | Pipeline Loop | LOCKED ✅ (R13 capstone) |
| §6 | Operating Envelope | LOCKED ✅ (v1-r1) |
| §7 | Scribe | Required — whole-section capstone |
| §8 | Editor | Required — whole-section capstone |
| §9 | Judge | Required — whole-section capstone |

**The demo driver is the LAST spec card to execute.** It is the capstone-of-capstones — every section must be whole-section-LOCKED before this runs.

---

## 4. Demo scenario

**Target RFA:** USDA VAPG FY26 (or the closest open RFA at demo time; if VAPG FY26 is closed, use the stored RFA envelope from `pipeline/rfa/` — the demo exercises the pipeline, not the RFA's live status).

**Target org:** FIT Farms LLC (under `orgs/fit_farms_llc/PROJECT_CONTEXT.md`). Law 3 enforced — only FIT Farms LLC data flows through the pipeline.

**Target rubric:** `pipeline/rubrics/vapg_fy26.json` (100 pts, 7 criteria).

**API keys:** Operator's BYOK keys per `router.yaml`. Scout uses Groq (Scribe uses Anthropic, Editor uses skill subprocess, Judge uses Google). All keys read from operator keystore (§1 keys.py).

---

## 5. Pipeline stages (mapped to §5 R11's 11-step lifecycle)

### Stage 1 — Boot
§1 Sovereignty Envelope boots. Session created. Vault initialized. Org isolation gate bound.

### Stage 2 — RFA Ingest
RFA envelope sealed under BT1 dual-hash. PROJECT_CONTEXT loaded and sealed.

### Stage 3 — Scout DISCOVER
Six channels (A–F) fan out in parallel. Candidates aggregated with health tuples.

### Stage 4 — Scout VERIFY
Per-candidate live synopsis fetch. VERIFIED_FIT / VERIFIED_NOT_FIT / UNVERIFIED assigned.

### Stage 5 — Scout REVIEW
VERIFIED_FIT candidates get fit rationale. Entity research pass. Human review queue populated.

### Stage 6 — Scribe Draft
For each RFA section: KGIE preflight → compose prompt → Anthropic LLM call → SectionDraft output. Admin-risk register consumed for flag-routing.

### Stage 7 — Editor Pass
SectionDraft[] fed to Editor adapter. Skill subprocess fires. 2-3 replacement options per flagged term. Taxonomy sorted. Tone assessed.

### Stage 8 — Revision Loop
Scribe receives Editor feedback. Bounded revision loop (§5 R5, max iterations per §4 config). Re-draft sections that need revision.

### Stage 9 — Judge Score
Final SectionDraft[] fed to Judge. Per-criterion scoring against VAPG rubric. Evidence quotes verified as verbatim (Law 5). SFR emitted. JudgeVerdict assembled.

### Stage 10 — Logician Gate
POST-gate validates entire pipeline output. Every F-code predicate fires. Verdict: PASS (score ≥ min_score + all gates green) or FAIL (with F-code citations).

### Stage 11 — Output
Scored proposal written to Vault. Audit trail sealed. Tab delivery (§5 R9) produces human-readable output.

---

## 6. Test harness structure

```
tests/demo/
├── test_demo_driver.py           # pytest harness: boots → runs pipeline → asserts output
├── conftest.py                   # fixtures: synthetic RFA envelope, PROJECT_CONTEXT, rubric
├── demo_rfa/                     # stored VAPG FY26 RFA (or synthetic)
│   └── vapg_fy26_synopsis.json
├── demo_project_context/         # FIT Farms LLC PROJECT_CONTEXT snapshot
│   └── PROJECT_CONTEXT.md
└── expected/                     # golden-output expectations (structure, not content)
    └── pipeline_output_schema.json
```

**Test categories:**

### 6.1 Happy path (1 test, long-running)
Full 11-stage pipeline with real API calls. Asserts:
- Pipeline exits with PASS or scored FAIL (not crash).
- All 11 stages executed (checkpoint files present in Vault).
- SectionDraft[] output exists for every RFA section.
- JudgeVerdict exists with all 7 criteria scored.
- Audit trail sealed with valid hash chain.
- Total score is an integer in [0, 100].

### 6.2 Degraded-mode tests (≥5 tests, mock API calls)
- Scout API timeout → pipeline continues with cached/partial results (M10 degraded-run flag set).
- Scribe LLM returns malformed output → revision loop retries within bound → eventually succeeds or cascade-advances.
- Editor skill subprocess crashes → F-PIPE-06 cascade advance → pipeline continues without Editor pass.
- Judge LLM returns unparseable score → F-JUDGE-SCORE-UNPARSEABLE → pipeline output includes the failure flag.
- All API keys missing → boot fails cleanly with explicit error (not crash).

### 6.3 Law enforcement tests (≥5 tests)
- Law 1: fabricated claim in Scribe output → POST-gate catches (F-POST-10).
- Law 3: cross-org data reference → PRE-gate catches (F-PRE-CROSS-ORG-READ).
- Law 4: flagged admin-risk term in Scribe output → Scribe adapter routes for operator approval.
- Law 5: Judge evidence quote not verbatim → F-JUDGE-EVIDENCE-NOT-IN-DRAFT.
- Sovereignty: no network call to any non-API endpoint; no data exfiltration path.

### 6.4 Performance gate (1 test)
Full pipeline on 8 GB M1 Mac Mini completes within wall-clock budget (TBD — operator sets budget at demo time; initial target: ≤30 minutes for a 5-section VAPG proposal).

---

## 7. Done definition

- Demo harness landed at `tests/demo/`.
- Happy-path test passes with real API calls on M1 Mac Mini.
- Degraded-mode + Law enforcement tests pass with mocked API calls.
- Performance gate meets operator's wall-clock budget.
- No new production code — demo driver is test infrastructure only.
- Daily log entry documenting demo results.

---

## 8. What happens after the demo

The demo driver's output is the **Group 10 outside-audit intake artifact**. A successful demo run produces:
- A scored VAPG proposal (the artifact the outside auditor evaluates for quality).
- A full audit trail (the artifact the outside auditor evaluates for process integrity).
- A performance profile (the artifact that proves 8 GB viability).

The demo is not the end — it is the gate to outside audit, which is the gate to real LOCK (internal two-audit + outside-impartial audit + operator signature).

---

## 9. Pointers

- §5 run_pipeline capstone: `pipeline/engineering/spec_cards/section_05_round_11_run_pipeline_capstone.md`
- §5 eval pipeline: `pipeline/engineering/spec_cards/section_05_round_12_B_run_eval_pipeline.md`
- Full build roadmap: `pipeline/business/full_build_roadmap.md`
- VAPG rubric: `pipeline/rubrics/vapg_fy26.json`
- FIT Farms LLC org: `orgs/fit_farms_llc/PROJECT_CONTEXT.md`
- King Midas prompt: `pipeline/engineering/king_midas_implementation_prompt_v2_1.md`
