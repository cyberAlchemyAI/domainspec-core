# Spec card — pipeline.seats.editor (Round 2: polish — retry-with-clarification + enhanced validation + §8 blueprint rows)

**STATUS:** PRE-STAGED 2026-04-29

**Parent spec:** `pipeline/engineering/spec_cards/section_7_council_seats_pipeline_modules.md` (Lane A step 5; Editor = 2-session arc per §5; R2 is the optional polish round).

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, standard interface pattern — not restated).

---

## 1. Blueprint anchors

- **§8 Editor blueprint — status TBD.** Per parent spec §5, §8 blueprint round is a separate track the operator may open in parallel. If §8 is LOCKED before R2 dispatches, R2 implements any §8-specific schema decisions. If §8 is still DRAFT, R2 proceeds under the R1 contract extensions (adapter pattern remains; no full port).
- `pipeline/blueprint/v0.1/section_07_scribe.md` v1.1.1 LOCKED — SectionDraft shape consumed by Editor (input side; R2 LOCK is the hard pin).
- `pipeline/blueprint/v0.1/section_00_5_interface_index.md` — R1 appends `pipeline.contract.editor.*` rows. R2 refreshes them if §8 blueprint introduces new shapes.
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED — §4.4 Editor invoke_seat subprocess contract.
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 LOCKED + v2.2 — F-EDITOR-* slot allocation (R1 consumes; R2 may extend if new failure modes surface).
- `skills/editor/SKILL.md` — the OpenClaw skill Editor adapter wraps. R2 does NOT modify the skill.
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 §D.3 Editor role, §F.1 (SFR-exempt).

**Blueprint hash-at-card** (BLUEPRINT_DEPS):
- All R1 pins inherited; recompute at R2 open if any anchor was amended post-R1-LOCK.

**Spec-card version:** v1
**Round:** §8 Editor Round 2 — polish round: retry-with-clarification on malformed output, enhanced validation, §0.5 row refresh, optional §8 blueprint row population.
**Canonical home:** `pipeline/seats/editor/` (R1 modules already landed)

---

## 2. Depends on

- **Editor R1 LOCKED** — adapter.py + seat.py + types.py. R2 extends, does not redefine.
- **Scribe R2 LOCKED (SectionDraft shape)** ✅.
- **§4 Logician PRE/POST gate substrate LOCKED** ✅.
- **§6 Operating Envelope LOCKED** ✅.

**Not depended on:** §8 Editor blueprint LOCK (R2 proceeds under R1 contracts if §8 is still DRAFT — this is the adapter-pattern advantage).

---

## 3. What R2 adds

### 3.1 Retry-with-clarification bounded loop

When skill subprocess returns malformed output (JSON parse failure, missing required keys, replacement_options count outside [2,3]):
1. Attempt strip_fences + extract_json (R1 baseline).
2. If parse still fails: re-invoke skill subprocess with a **clarification suffix** appended to stdin (describes the parse failure, asks skill to re-emit clean JSON). Bounded to **1 retry** (same as E-028 transport discipline).
3. If second attempt fails: emit F-EDITOR-OUTPUT-SHAPE and advance via cascade (F-PIPE-06).

### 3.2 Enhanced validation

- **Taxonomy sort audit:** verify that skill's `readability.goals/outputs/outcomes/objectives` classification is internally consistent (no item appears in >1 category).
- **Tone consistency check:** verify `tone_feedback.overall_readability` score is ≥0 and ≤100.
- **Quick-wins deduplication:** strip duplicate entries from `quick_wins[]`.
- **Terms-to-verify cross-reference:** verify each term in `terms_to_verify[]` appears in at least one `flagged_terms[].excerpt`.

### 3.3 §0.5 row refresh

If R1 landed stub rows at §0.5, R2 refreshes with concrete schema references. If §8 blueprint is LOCKED, populate §0.5 with §8-derived contract rows.

---

## 4. Module layout delta

```
pipeline/seats/editor/
  adapter.py               # EXTEND: retry-with-clarification bounded loop
  validator.py             # NEW: enhanced validation predicates (taxonomy sort audit,
                           #   tone consistency, quick-wins dedup, terms-to-verify cross-ref)
  BLUEPRINT_DEPS           # refresh pins
```

No new subprocess entry — seat.py from R1 is stable. validator.py predicates are called by adapter.py after skill output parse, before EditorOutput assembly.

---

## 5. Test surface

- Retry-with-clarification: skill returns malformed JSON → retry succeeds → EditorOutput. Skill returns malformed JSON twice → F-EDITOR-OUTPUT-SHAPE.
- Taxonomy sort: item in >1 category → validation catches and flags.
- Tone consistency: out-of-range score → validation catches.
- Quick-wins dedup: duplicate entries stripped.
- Terms-to-verify cross-ref: orphan term → validation warning (NOTE, not blocking).
- Regression: all R1 test corpus cases still pass with R2 enhancements active.

---

## 6. Done definition

- R2 modules landed in `pipeline/seats/editor/`.
- Tests ≥ 40 (R1 + R2 combined). ≥ 95% coverage. AST-lint clean.
- Full suite GREEN.
- Ledger row: `lock_class: "code"`, committee_round id, SHA-3-512[:16].
- Paired `## LOCK:` block in daily log (F-AMDT-12).
- Committee **5/5 PASS** per L-005.
- **R2 LOCK closes Editor as a full pipeline seat.** Post-R2: §8 whole-section capstone eligible.
