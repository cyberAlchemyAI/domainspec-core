# Spec card — pipeline.seats.judge (Round 2: cross-rubric dispatcher + responsiveness mapper + JudgeVerdict)

**STATUS:** PRE-STAGED 2026-04-29

**Parent spec:** `pipeline/engineering/spec_cards/section_7_council_seats_pipeline_modules.md` (Lane A step 5; Judge = **FULL PORT** per OQ-1).

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, standard interface pattern — not restated).

---

## 1. Blueprint anchors

- **§9 Judge blueprint — REQUIRED BEFORE R2 CODE WINDOW.** Per parent spec §5, §9 blueprint round is a prereq for Judge R2. R2 MUST NOT dispatch until §9 blueprint is LOCKED-internal. The blueprint will define: JudgeVerdict full shape, cross-rubric dispatch strategy, responsiveness-map semantics, and multi-rubric scoring precedence.
- `pipeline/rubrics/vapg_fy26.json` — canonical first-run demo rubric. R1 pinned the schema; R2 consumes the pinned schema for multi-rubric dispatch testing.
- `pipeline/blueprint/v0.1/section_07_scribe.md` v1.1.1 LOCKED — §7.5 `SectionDraft` handoff contract (Judge consumes at R2 via concrete import, not Protocol).
- `pipeline/blueprint/v0.1/section_00_5_interface_index.md` — `pipeline.contract.judge` row is STUB pending §9. R2 populates the row with JudgeVerdict + JudgeInput + cross-rubric-dispatch contract.
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 §D.4 (Judge role), §E (cross-family), §F.1 (SFR — Judge NOT exempt; SFR emission deferred to R3).
- `router.yaml` — `tilth.judge` primary = `google/gemini-2.5-pro`; escalation tiers. Reference only.

**Blueprint hash-at-card** (BLUEPRINT_DEPS, computed at Round-open):
- `pipeline/blueprint/v0.1/section_09_judge.md` — compute at R2 open (MUST be LOCKED first)
- `pipeline/rubrics/vapg_fy26.json` — inherit R1 pin or recompute
- `pipeline/blueprint/v0.1/section_07_scribe.md` — inherit R1 pin or recompute
- `pipeline/blueprint/v0.1/section_00_5_interface_index.md` — compute at R2 open

**Spec-card version:** v1
**Round:** §9 Judge Round 2 — cross-rubric dispatcher + responsiveness mapper + JudgeVerdict full shape + §0.5 row population
**Canonical home:** `pipeline/seats/judge/` (R1 modules already landed here)

---

## 2. Depends on

- **Judge R1 LOCKED** — shapes + rubric_loader + dimension_scorer. R2 extends, does not redefine.
- **§9 Judge blueprint LOCKED** — required. R2 implements §9-owned schema decisions. Cannot proceed without §9 LOCK.
- **Scribe R2 LOCKED** — SectionDraft concrete shape. R2 binds `SectionDraftLike` Protocol (from R1) to the concrete `SectionDraft` import. E-026 `__module__` lineage test added.
- **Architecture v7 §D.4 + §F.1 LOCKED** ✅.
- **VAPG rubric extracted** ✅.

---

## 3. Proposed modules

```
pipeline/seats/judge/
├── __init__.py               # extend R1 __all__ with R2 exports + BLUEPRINT_DEPS refresh
├── types.py                  # EXTEND: JudgeVerdict full shape, ResponsivenessEntry, 
│                             #   Protocol-to-concrete bind (SectionDraftLike → SectionDraft)
├── cross_rubric_dispatch.py  # NEW: routes criteria to correct scorer-role handlers;
│                             #   multi-rubric precedence (when >1 rubric applies to a section)
├── responsiveness_mapper.py  # NEW: maps funder's "responsiveness factors" to scored dimensions;
│                             #   produces ResponsivenessMap consumed by JudgeVerdict assembly
├── verdict_assembler.py      # NEW: collects per-criterion CriterionScore[] → JudgeVerdict;
│                             #   validates total score, evidence coverage, rubric hash continuity
└── BLUEPRINT_DEPS            # refresh with §9 blueprint pin
```

Coverage target ≥ 95% per module (R1 precedent: 100%).

---

## 4. Public API (Round 2 additions)

```python
# R2 additions to __all__
__all__ += (
    # Verdict shape
    "JudgeVerdict",
    "ResponsivenessEntry",
    "ResponsivenessMap",
    # Dispatch
    "dispatch_criteria_to_scorers",   # routes criteria by scorer_role
    # Assembly
    "assemble_verdict",               # CriterionScore[] + Rubric → JudgeVerdict
    # Responsiveness
    "build_responsiveness_map",       # RFA responsiveness factors → scored mapping
)
```

---

## 5. Key design decisions (scoped by §9 blueprint — validate at R2 open)

- **Multi-rubric precedence:** When a single section is scored by multiple rubrics (e.g., VAPG primary + cross-check rubric from Judge library), dispatch resolves by funder-primary-first, then cross-check-additive. Per-rubric JudgeVerdict instances are separate; verdict_assembler merges into a `JudgeVerdictBundle` only if §9 blueprint mandates it — otherwise, single-rubric-per-invocation.
- **Responsiveness mapping:** VAPG's "responsiveness" criteria (criteria f/g in vapg_fy26.json) require a different evaluation posture (programmatic/organizational capacity vs. technical proposal quality). responsiveness_mapper isolates this.
- **Evidence verbatim enforcement:** R2 maintains R1's `evidence_quote: str` constraint (Law 5). verdict_assembler validates every evidence_quote is a verbatim substring of the source SectionDraft.body_text. Pre-gate for R3's F-JUDGE-EVIDENCE-NOT-IN-DRAFT.

---

## 6. Test surface

- Per-module unit tests (≥20 per module).
- Protocol-to-concrete bind test: `SectionDraftLike` satisfied by real `SectionDraft` import (E-026 `__module__` lineage assertion).
- Cross-rubric dispatch: VAPG 7-criteria routing + synthetic 3-criteria rubric routing + edge: rubric with zero subcriteria.
- Verdict assembly: valid assembly, partial scores (missing criterion → F-JUDGE-CRITERION-MISSING), out-of-bound score, rubric hash drift between load and assembly.
- Responsiveness: VAPG f/g mapping, empty responsiveness factors, duplicate factor entries.

---

## 7. Done definition

- All R2 modules landed in `pipeline/seats/judge/`.
- §0.5 interface-index rows populated for `pipeline.contract.judge.input.v1`, `pipeline.contract.judge.output.v1`, `pipeline.contract.judge.verdict.v1`.
- Tests ≥ 60 (R1 + R2 combined). ≥ 95% coverage per module. AST-lint clean.
- Full suite GREEN.
- Ledger row with `lock_class: "code"`, committee_round id, SHA-3-512[:16].
- Paired `## LOCK:` block in daily log (F-AMDT-12).
- Committee **5/5 PASS** per L-005.
