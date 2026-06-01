# §5 v6.1 Amendment Proposal — Seat Output Schema Pin

**Status:** `PROPOSAL` — not dispatched; queued for Thesis when operator greenlights.
**Date:** 2026-04-20
**Author:** Cowork session per Josh's disposition after Editor v1.1 agent-prompt rename sweep
**Parent amendment:** `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 (LOCKED-internal 2026-04-18) + `section_05_v6_amendment.md` (LOCK-READY)
**Scope:** Editor, Judge, Scribe seat output schemas

---

## Problem surfaced

Editor's v1.1 agent-prompt rename sweep (`F-CROSS-FAMILY-VIOLATION` → `F-ROUTER-FAMILY-COLLISION`) exposed that §5's Editor seat contract is tracked at **contract level** (input, output shape, rubric, cross-family rigor) but not at **field level**. The agent prompt is currently the **sole authority** for the Editor output schema — what fields exist, what types they carry, what invariants they satisfy.

Same gap applies to Judge and Scribe contracts per a first-pass read. Field-level schema is authored once (in the agent prompt) and consumed downstream (by `pipeline/loop/`, by `pipeline/logician/` gates that inspect verdicts, by tests that assert on verdict shapes). There is no canonical schema-of-record against which the consumers and the agent-prompt author can both be audited.

**Failure mode that this gap enables:**
- Author updates agent prompt, adds a new output field, forgets to update `pipeline/loop/` consumer; consumer silently drops the new field; downstream gates (F-VERDICT-BLOCKING-MISSING, F-VERDICT-CITATION-MISSING — v2.2 Wave 1) scan for fields that don't arrive and fail-closed on every verdict.
- Consumer updates what it expects; author's prompt doesn't change; verdicts stop parsing; pipeline grinds to halt with no one obviously at fault.
- §0.5 Blueprint Interface Index can't fire F-INDEX-STALE because the Index tracks §5's parent hash, which doesn't change when agent-prompt-level schema drifts.

**Law 1 erosion:** "RFA Is the Source of Truth" extends by analogy to seat contracts — the canonical contract should be the source of truth, and the agent prompt is a consumer of it. Today the agent prompt IS the contract, which is an asymmetry relative to how RFAs vs applicant drafts are treated.

## Scope

This proposal covers the three LLM-backed seats whose outputs feed the pipeline:

- **Editor** — clarity-pass output (flags + replacement options + rationale)
- **Judge** — rubric-scoring output (per-dimension scores + citations + verdict + blocking field)
- **Scribe** — section-draft output (section content + KGIE-preflight results + overlooked-expenses checklist)

Scout, Red Team, Reasoner Review, and Logician are out of scope: Scout outputs are radar candidates (separately schematized in `pipeline/scout/_types.py`); Red Team outputs feed Judge-or-operator cross-check (schema matches Judge's rubric shape); Reasoner Review outputs are narrative prompts (not pipeline-consumed); Logician outputs are deterministic gate results (schema lives in `pipeline/logician/gates/` error-type declarations).

## Three candidate homes for the field-level schema pin

### Option A — New section in §5 v6.1 amendment

- **Shape:** new §5.N sub-section per seat ("§5.12 Editor Output Schema Pin", "§5.13 Judge Output Schema Pin", "§5.14 Scribe Output Schema Pin"). Each sub-section declares required fields, types, invariants, validation errors, example valid + invalid payloads.
- **Pro:** Co-located with the seat contracts it extends; familiar to the Thesis Team reviewing §5 generally; single amendment round covers all three.
- **Con:** Section 5 is already ~long; adding three dense schema blocks grows it further; schemas that want to evolve independently are coupled to §5's next-round cadence.

### Option B — New `pipeline/blueprint/v0.1/schemas/` registry

- **Shape:** new directory. One schema file per seat (`editor_output.schema.md`, `judge_output.schema.md`, `scribe_output.schema.md`). §5 is amended to reference the registry paths. Each schema file LOCKs independently; `section_00_5_interface_index.v1.json` gains a row per schema file for drift detection.
- **Pro:** Separation of concerns — schemas evolve independently of their consuming section's architecture; per-schema Thesis rounds are lighter-weight than section amendments; §0.5 drift detection naturally applies.
- **Con:** New directory is a new architectural layer that needs its own justification; adds blueprint-reader cognitive load (another place to look for relevant content); does not exist today.

### Option C — Logician POST-gate `F-SEAT-OUTPUT-SCHEMA-DRIFT` + schemas embedded in gate code

- **Shape:** the canonical schema lives as a Python dataclass or TypedDict in `pipeline/logician/gates/f_seat_output_schema_drift.py`; gate fires POST on every seat verdict ingestion, validates against the embedded schema. v2.2 Wave 2 or v2.3 addition.
- **Pro:** Schema is mechanically enforced at runtime (the strongest position); gate can co-evolve with the agent prompts as a paired commit; leverages the existing Logician-gate infrastructure; natural home for blocking-field + citation-field + dimension-list invariants that are already separate gates (F-AMDT-02, F-AMDT-03).
- **Con:** Schema in Python code is harder to read for non-coders reviewing the contract; "where does the Editor output schema live?" is answered by "look at a Logician gate," which is one layer removed; makes §5 look thinner than it is.

### Recommended hybrid: B + C

Option B as the **declarative** home (what the schema IS — readable by anyone auditing Tilth), Option C as the **enforcement** home (mechanical POST-gate validation that the declarative schema is honored at runtime). Option A's co-location value is preserved via §5 v6.1 amendment including references to B's registry paths and a POST-gate wiring note pointing to C's gate. Author updates: (1) schema file in B, (2) gate in C as paired commit, (3) agent prompt as paired commit — three-way paired commit, not two-way.

## Proposed Thesis round scope (if operator greenlights)

- **Author:** single Cowork session drafts the registry + schemas (B), the POST-gate (C), and the §5 v6.1 amendment (A-lite) as a paired commit proposal.
- **Reviewers per L-005:** Editor + Judge + Red Team from router.yaml at the time of dispatch (current: Llama 3.3 / Gemini 2.5 Pro / GPT-OSS 120B). L-003 cross-family rigor preserved.
- **Cycle 1 DRIVER:** per-seat audit of the proposal's three-way paired commit.
- **Cycle 2 VERIFICATION:** re-audit after fixes.
- **LOCK outcome:** §5 v6.1 LOCKED-internal. Downstream: schemas registry LOCKED; gate added to v2.2 queue at gate #13 (or v2.3 if v2.2 is closed).

## Open questions for operator decision

1. **Greenlight Thesis round now, or park until v2.2 implementation closes?** v2.2 queue is already 12 gates; adding gate #13 (F-SEAT-OUTPUT-SCHEMA-DRIFT) right after Wave 4 would push total to 13. If v2.3 is more natural, park the proposal there.
2. **Hybrid B+C, or pick a single home?** Hybrid is the strongest shape but is three paired commits not two. Single home is simpler but each has its con.
3. **Seat scope** — just Editor for MVP (the seat that surfaced the gap via the v1.1 rename), or all three at once? Editor-only is narrow; all-three is the cleaner architectural position.

## Deliverable if approved

- `pipeline/blueprint/v0.1/schemas/editor_output.schema.md` (LOCK candidate)
- `pipeline/blueprint/v0.1/schemas/judge_output.schema.md` (LOCK candidate)
- `pipeline/blueprint/v0.1/schemas/scribe_output.schema.md` (LOCK candidate)
- `pipeline/blueprint/v0.1/section_05_v6_1_amendment.md` (LOCK candidate; registry + gate references)
- `pipeline/engineering/spec_cards/logician_v2_2_f_seat_output_schema_drift.md` (gate #13 spec card)
- `pipeline/engineering/lock_history.v1.jsonl` — row per LOCK
- §0.5 interface index rows for each schema file (drift detection)

## What this proposal does NOT do

- Dispatch a Thesis round (operator decision required).
- Implement the POST-gate (gate-build is downstream of LOCK).
- Modify agent prompts (agent prompts are consumers of the LOCKed schema; re-run of v1.1 etc. happens after schema LOCKs).

---

*Proposal authored 2026-04-20 by Cowork session. Park in place until operator greenlights Thesis round OR defers to v2.3 post-MVP.*
