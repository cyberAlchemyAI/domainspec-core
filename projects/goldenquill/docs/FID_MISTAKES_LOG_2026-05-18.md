# FID Mistakes Log — 2026-05-18

**Purpose:** Running institutional record of every error class caught during FID refinement, how it was fixed, what validator was added, and what pattern propagation it required. Each pass (0 through 5+) appends its findings.

**Discipline:** Per the FID Refinement Methodology, every pass must:

1. Answer the 4 pattern-propagation questions (recurrence / global-fix / validator / log).
2. Append findings to this log.
3. Surface systemic fixes vs. per-charter fixes.
4. Record what was deferred to operator review.

**Branch under refinement:** `fid-week-1-pillar-1-charters-2026-05-18` (PR #33).
**Charter roster:** 14 Pillar-1 funder depth-charters under `pipeline/funder_intelligence/pillar_1_charters/`.

---

## Pass 0 — Foundations Repair (2026-05-18)

**Scope.** YAML parse, lifecycle normalization, harm-prevention fixes. No interpretive expansion, no new gates beyond the operator-named harm-prevention list, no §1 / §B rewrites beyond the named fixes.

**Charters touched.** 14 of 14.
**Validation pass rate.** 14/14 across all six Pass-0 criteria.
**Diff shape.** +222 / −144 lines across 14 files; patch applied cleanly against PR #33 HEAD `032b4d0`.
**Dry-run artifact (audit trail, gitignored):** `pipeline/validation/pass-0-foundations-dry-run-2026-05-18/`.

### Patterns caught

#### G1 — Unquoted-colon YAML placeholders

- **Frequency:** 8 of 14 charters.
- **Failure mode:** YAML parser breaks on `corpus_ref: <NEEDED — Pillar 2: ...>` — the embedded `: ` after `Pillar 2` is read as a new key marker, so `yaml.safe_load` raises `mapping values are not allowed here`. All eight §B yaml blocks were unparseable as committed.
- **Pattern regex:** `^\s*[a-z_][a-z0-9_]*:\s+<[^>"]*:[^>"]*>\s*$`.
- **Fix applied:** Wrap each offending placeholder value in double quotes (`key: "<NEEDED … : …>"`). Eight instances patched, one per file: NCBA-CLUSA, PA-DCED, PA-DEPT-AG, RICHARD-KING-MELLON-FOUNDATION, USDA-AMS, USDA-NIFA, USDA-RD, USDA-RD-RBDG-FY26.
- **Pattern-propagation answers:**
  1. Recurred in 8+ charters — yes.
  2. Global fix applied — yes (regex-driven; all 8 patched; all §B blocks now parse).
  3. **Validator recommended for Pass 1:** pre-commit hook running `yaml.safe_load` on every fenced ` ```yaml ` block in `pillar_1_charters/*.md`. Tag: `no_unquoted_colon_placeholders` — should be permanent CI check.
  4. Recorded here — yes.
- **Lesson.** Placeholder syntax must be YAML-safe by default. Future authoring tasks (Pillar 2 charter drafting, charter templates) should use `"<NEEDED …>"` from the start. The depth-charter template itself should ship with quoted placeholder examples.

#### G2 — Quoted-scalar + parenthetical list items (SARE-canonical syntax bug; Codex audit 1.1)

- **Frequency:** 10 of 14 charters (SARE was the canonical exemplar that propagated).
- **Failure mode:** `- "Quoted text." (parenthetical comment)` — after the closing `"`, YAML expects only flow-end or end-of-line; the trailing `(...)` confuses block-collection parsing.
- **Pattern regex:** `^\s*-\s+"[^"]*"\s+\(...\)$`.
- **Fix applied:** Wrap the entire list item in single quotes, escaping any interior `'`: `- '"<example>" (<commentary>)'`. 27 list items patched across HEINZ, NCBA-CLUSA, PA-DCED, PA-DEPT-AG, RICHARD-KING-MELLON-FOUNDATION, USDA-AMS, USDA-NIFA, USDA-NIFA-SARE-NE-FY26, USDA-RD, plus the original SARE block. AGINNOV / VAPG / CFP / RBDG / RCDG did not carry the pattern.
- **Pattern-propagation answers:**
  1. Recurred in 10+ charters — yes (SARE-template propagated).
  2. Global fix applied — yes (single regex catches SARE-canonical and propagated forms).
  3. **Validator recommended for Pass 1:** same YAML-parse hook from G1 catches G2 (parse-failure is the signal). Tag: `no_quoted_scalar_paren_list_items`.
  4. Recorded here — yes.
- **Lesson.** SARE was treated as the methodology anchor and its syntax was copied into other charters; any future "anchor charter" should be parse-validated before propagation. Template-by-imitation amplifies syntax errors.

#### G3 — "Gold-standard" rhetoric overstating maturity

- **Frequency:** 14 of 14 charters.
- **Failure mode:** Every charter carried `GOLD-STANDARD DRAFT v0` in the status banner, `gold_standard_v0` in version fields (header table + §B yaml), `"Codex-shape gold-standard YAML"` as §B section heading, and cross-references like `"per same discipline as USDA-RD funder gold-standard"`. The MANIFEST also notes "Zero charters are operator-attested" — i.e., these are pre-corpus hypotheses, not signed runtime logic. The rhetoric created a maturity claim the underlying state does not support.
- **Fix applied:** Two-part normalization.
  - **Rhetoric demotion.** Status banner → `**Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)**`; `gold_standard_v0` → `depth_charter_v0`; §B heading `"gold-standard YAML"` → `"depth-charter YAML"`; cross-references `"X funder gold-standard"` → `"X funder depth charter"`; defensive sweep on remaining `gold-standard(s?)` prose (including plural).
  - **Structural status block.** Inserted after `lifecycle: draft` in §B yaml of all 14 charters:

    ```yaml
    lifecycle: draft
    validation_status: pre_corpus_hypothesis
    runtime_load_status: do_not_load_as_signed_logic
    operator_label: depth_charter_v0
    ```

- **Pattern-propagation answers:**
  1. Recurred in 14 of 14 charters — yes (universal).
  2. Global fix applied — yes (6–10 rhetoric substitutions per file plus one structured-block insert).
  3. **Validator recommended for Pass 1:** mechanical grep `gold[- ]standards?|gold_standard|GOLD[- ]STANDARDS?` against `pillar_1_charters/*_charter_v0_DRAFT.md` — fail CI on any hit. Tag: `no_gold_standard_label_remaining` — already in Pass 0 checklist; promote to CI.
  4. Recorded here — yes.
- **Lesson.** Authoring labels propagate. A rhetoric-vs-state mismatch in one anchor charter cascaded across the roster. The runtime-load-status distinction needs to be machine-readable (the four-field status block) so downstream agents can refuse to load `pre_corpus_hypothesis` artifacts as signed logic.

### Per-charter harm-prevention fixes (operator-named)

These are the four explicit Fix-D items in the operator's canonical reference. Each was applied to exactly one charter; pattern-propagation analysis is below the table.

| Fix tag | Charter | Class | What changed | Operator-flagged review |
|---|---|---|---|---|
| **Fix D-RBDG** | `USDA-RD-RBDG-FY26` | match-logic demotion | Inserted `match_logic` block (`required_match: false`, `competitive_factor: true`, `source_required: true`) before `scoring_rubric:` in §B yaml. Logician must not reject on missing match; vague committed resources warn. | Rubric `reviewer_expectation` ("≥50% cash match, all commitments unconditional") and §A `judge.decision_changed` ("Tie-breakers favor cash-match-≥50%") still imply a hard ≥50% threshold. Pass-1 reconciliation. |
| **Fix D-CFP** | `USDA-RD-CFP-FY26` | boundary-inclusive | `operator: lt` → `operator: lte`; `<20,000` → `≤20,000`; `≥20,000` → `>20,000` in evidence-ladder / §A prose. `(20,000 IS eligible)` annotation inserted. Added `source_required: true`. 8 substitution sites. | Confirm CFP policy: service areas of *exactly* 20,000 ARE eligible (gate fires only on *greater than* 20,000). |
| **Fix D-RCDG** | `USDA-RD-RCDG-FY26` | applicant-gate widening | Token rename `F-RCDG-NOT-NONPROFIT-COOPERATIVE-DEVELOPMENT-CENTER` → `F-RCDG-INELIGIBLE-APPLICANT-TYPE`. New predicate widens to `[nonprofit_institution, nonprofit_corporation, eligible_higher_ed_institution]`. Added companion HIGH gate `F-RCDG-CENTER-CAPACITY-UNDOCUMENTED` with `WARN_OPERATOR` (capacity goes from hard-reject → operator-warning). | §A `red_team.decision_changed` and §A `logician.decision_changed` parentheticals ("501(c) nonprofit CDC") still describe the pre-fix posture. Pass-1 reconciliation. |
| **Fix D-AGINNOV** | `PA-DEPT-AG-AGINNOV-FY26` | polarity flip + grant-type model | Gate renamed `F-AGINNOV-STATE-MATCH-NOT-PA-SOURCE` → `F-AGINNOV-MATCH-USES-STATE-SOURCE`. Predicate flipped: now fires when match *contains* State-sourced funds. Severity HIGH → P0; on_fail WARN_OPERATOR → REJECT_NO_DRAFT. `active_tracks` block replaced by `claimed_grant_type` enum (Planning $7.5K–$50K @ 30%, On-site $5K–$200K @ 50%, Regional $100K–$2M @ 50%) + `source_required: true`. Old `historical_tracks` preserved under `retired_commodity_track_model.historical_tracks_pre_pass_0` for traceability. | (a) Confirm non-State-match posture. (b) Severity promotion HIGH → P0 — acceptable but flag. (c) §A `scribe.decision_changed`, §1 prose, §B `scribe_section_requirements` for §III, evidence-ladder strongest entries, red_team `AGINNOV-PROBE-TRACK-CASCADE-INTEGRITY` probe, and gate `F-AGINNOV-TRACK-ELIGIBILITY-CASCADE-MISMATCH` semantics all still reference commodity tracks. Pass-1 systemic strip. |

#### Pattern propagation across the four harm-prevention fixes

- **D-RBDG (competitive-factor presented as hard requirement).** Same pattern needs auditing in PA-AGINNOV, VAPG, CFP at Pass 1. Not swept in Pass 0 per operator scope. **Validator for Pass 1:** `match_logic_present_when_match_mentioned` schema check.
- **D-CFP (boundary-inclusive vs strict).** RBDG's `≤50,000` rural-pop threshold already correct (`lte`). Pass 1 should sweep all P0 boundary operators across all 14 charters. **Validator for Pass 1:** `p0_gate_boundary_operator_documented` schema check.
- **D-RCDG (over-narrowed predicate beyond source authority).** Same over-narrowing pattern present in AGINNOV (commodity-track model) and possibly VAPG. **Validator for Pass 1:** `p0_gate_predicate_traces_to_source_authority` schema check.
- **D-AGINNOV (polarity bug).** This is the kind of bug a unit test would catch. **Validator for Pass 1:** `gate_predicate_polarity_test` schema check — each gate carries an explicit `fires_when` example pair (positive case + negative case) so the polarity is provable from the artifact alone.

### Per-charter diff sizes

| # | Charter | +lines | −lines | Pass-0 fixes |
|---|---|---:|---:|---|
| 1 | `HEINZ-FOUNDATION` | 11 | 9 | B, C |
| 2 | `NCBA-CLUSA` | 11 | 10 | A, B, C |
| 3 | `PA-DCED` | 11 | 10 | A, B, C |
| 4 | `PA-DEPT-AG-AGINNOV-FY26` | 46 | 17 | C, D-AGINNOV |
| 5 | `PA-DEPT-AG` | 11 | 10 | A, B, C |
| 6 | `RICHARD-KING-MELLON-FOUNDATION` | 11 | 10 | A, B, C |
| 7 | `USDA-AMS-VAPG-FY26` | 8 | 5 | C only |
| 8 | `USDA-AMS` | 11 | 10 | A, B, C |
| 9 | `USDA-NIFA-SARE-NE-FY26` | 12 | 10 | B, C |
| 10 | `USDA-NIFA` | 12 | 11 | A, B, C |
| 11 | `USDA-RD-CFP-FY26` | 17 | 13 | C, D-CFP |
| 12 | `USDA-RD-RBDG-FY26` | 26 | 7 | A, C, D-RBDG |
| 13 | `USDA-RD-RCDG-FY26` | 23 | 11 | C, D-RCDG |
| 14 | `USDA-RD` | 12 | 11 | A, B, C |
| **Totals** | | **222** | **144** | |

### Manifest reconciliation (operator surface point)

Operator surfaced a worry about 12-vs-14 charter count. **Finding: no gap.** MANIFEST.md lists 14 charters; `pillar_1_charters/` contains 14 charter files. PA-DCED present (341 lines). USDA-AMS-VAPG-FY26 present (295 lines). The 12-vs-14 worry predates the [FIDELITY-FIX-HEINZ] commit. No reconciliation action required.

### Deferred to Pass 1 reconciliation

These items were surfaced but not touched in Pass 0 per the no-invention rule. Pass 1 picks them up:

- **AGINNOV commodity-track prose** remains in §A `scribe.decision_changed`, §1 prose, §B `scribe_section_requirements` for §III, evidence_ladder strongest entries, and red_team probe `AGINNOV-PROBE-TRACK-CASCADE-INTEGRITY`. Pass 1 systemic strip → align with grant-type model. Gate `F-AGINNOV-TRACK-ELIGIBILITY-CASCADE-MISMATCH` semantics need re-derivation around grant types.
- **AGINNOV severity promotion HIGH → P0** — operator confirm posture acceptable; flagged for review.
- **RBDG rubric tier descriptors** for the Leveraging criterion ("≥50% cash match, all commitments unconditional, in-kind third-party-documented") still imply a hard threshold. §A `judge.decision_changed` tie-breaker contradicts the new `match_logic.required_match: false`. Pass 1 reconciles tier descriptors with the `match_logic` block.
- **RCDG §A prose** parenthetical still says "501(c) nonprofit CDC" though the gate widened. §A `red_team.decision_changed` describes the pre-fix hard-eligibility posture; new gate has `WARN_OPERATOR` semantics. Pass 1 aligns §A prose with new gate semantics.
- **MANIFEST.md table** still says "GOLD-STANDARD DRAFT v0" for every row — linguistically inconsistent with the new charter-level "DEPTH CHARTER v0" labels. One-line regex fix; deferred to Pass 1 for paired-commit coherence.
- **Remaining P0 gates across all 14 charters** are NOT swept for `source_required: true` (operator scoped Pass 0 to "the gates I touched"). Pass 1: P0-gate source-authority audit across all 14 charters.
- **§A `decision_changed` prose drift** in CFP / RCDG / AGINNOV — gate IDs renamed but surrounding prose unchanged. Pass 1 reconciles §A prose with updated §B yaml.

### Validators recommended for Pass 1+ to add

Add to the CI pipeline (in dependency order):

1. **`yaml_safe_load_all_fenced_blocks`** — pre-commit hook running `yaml.safe_load` on every fenced ` ```yaml ` block in `pillar_1_charters/*.md`. Catches G1 + G2 at author time. Highest priority.
2. **`no_gold_standard_label_remaining`** — mechanical grep against `pillar_1_charters/*_charter_v0_DRAFT.md`. Promotes G3-prevention from Pass-0 checklist to CI.
3. **`match_logic_present_when_match_mentioned`** — schema check: if a charter mentions cash-match in §A / §B, it must carry a `match_logic` block with explicit `required_match`, `competitive_factor`, and `source_required` fields.
4. **`p0_gate_boundary_operator_documented`** — schema check on every P0 gate with a numeric threshold: `operator ∈ {lt, lte, gt, gte}` must be explicit, plus an inline annotation `(threshold IS / IS NOT eligible)`.
5. **`p0_gate_predicate_traces_to_source_authority`** — schema check: every P0 gate must have `source_required: true` AND `corpus_ref:` pointing to a citable source (or quoted `<NEEDED …>` placeholder).
6. **`gate_predicate_polarity_test`** — schema check: every gate carries `fires_when` and `does_not_fire_when` example pairs (positive + negative cases). Would have caught D-AGINNOV polarity inversion at author time.
7. **`section_a_section_b_coherence`** — when a gate is renamed or a predicate's semantics flip, scan §A `decision_changed` strings for the old gate id / old semantics and require a coordinated update. Catches "§A prose drift" deferred items.

---

## Pass 1 — Logician (2026-05-18)

**Scope.** Discipline-3a gate-taxonomy LOCK + per-charter classification of all 67 gates + Discipline-3 source-authority audit across 14 charters + four Pass-0 deferred-reconciliation items (D-RBDG / D-RCDG / D-AGINNOV / MANIFEST normalization) + four cheap validators landed inline.

**Charters touched.** 14 of 14 (charter normalization). MANIFEST.md + README.md (label normalization). `docs/FID_REFINEMENT_METHODOLOGY_2026-05-18.md` (Discipline 3a added; PR #43 dependency).
**Validation pass rate.** 4 of 4 cheap validators GREEN against post-Pass-1 charter corpus; 3 expensive validators scoped with explicit acceptance criteria.
**Diff shape.** ~549 inserts / ~36 deletes across 14 charter files + 2 markdown files + 6 new validator files (`_validators/`) + 2 new docs (`docs/FID_REFINEMENT_METHODOLOGY_*` amended; `docs/FID_CANONICAL_REFERENCE_*` from PR #43).
**Dry-run artifact:** `pipeline/validation/pass-1-logician-dry-run-2026-05-18/`.

### Patterns caught

#### P1-1 — Gate-taxonomy classification missing

- **Frequency:** 14 of 14 charters; 67 of 67 gates lacked `gate_type`.
- **Failure mode:** Discipline 3 / 3a defines a 5-type taxonomy (hard_eligibility_gate / verify_required_gate / competitive_scoring_signal / drafting_warning / relationship_signal); without `gate_type`, downstream consumers (Logician runtime, Cedar policies, future passes) cannot dispatch by class. Pass 0 left the gate roster structured but unclassified.
- **Fix applied:** Pass 1 added `gate_type` to every gate based on the existing `(severity, fail_action)` tuple per the Discipline-3a.4 consistency matrix. Tally: 24 hard_eligibility_gate / 41 competitive_scoring_signal / 2 relationship_signal / 0 verify_required_gate / 0 drafting_warning. The empty verify_required_gate and drafting_warning rosters are flagged for purpose-vs-classification migration (Pattern P1-7).
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes (67 gates classified).
  3. **Validator added:** `gate_dsl_schema_check.py` (presence of `gate_type`) + `gate_taxonomy_consistency.py` (severity ↔ fail_action match).
  4. Recorded here — yes.
- **Lesson.** The taxonomy was defined in methodology Discipline 3 from day one but not propagated into charter shapes. Authoring tools (charter template + sign-helper) should require `gate_type` from the start so Pass 0 doesn't have to retro-classify.

#### P1-2 — `source_required: true` missing on P0 gates

- **Frequency:** 12 of 14 charters; 24 P0 gates needed the field, 21 lacked it pre-Pass-1.
- **Failure mode:** Discipline 2 source-authority rule requires `source_required: true` for any P0 gate (hard_eligibility_gate must be source-backed AND machine-checkable). Pass 0 swept gates it explicitly fixed (D-AGINNOV polarity flip carried `source_required: true`; D-CFP boundary fix carried it) but the rest of the P0 roster inherited from earlier authoring without the field.
- **Pattern regex:** AST-level: gate where `severity == "P0"` AND `source_required` not in fields.
- **Fix applied:** All 24 P0 gates now carry `source_required: true`. Each gets a corpus_ref pointer (regulatory citation if known; `pending_pillar_2` placeholder otherwise) + a `confidence.promotion_requirement` naming what Pillar-2 source would lift confidence.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes.
  2. Global fix applied — yes (24 P0 gates patched).
  3. **Validator added:** `gate_dsl_schema_check.py` (presence of `source_required`); semantic check (P0 + source_required: false is structurally inadmissible) is enforced by `gate_taxonomy_consistency.py` via the Discipline-3a.4 matrix.
  4. Recorded here — yes.
- **Lesson.** Discipline 2 should have been enforced at charter-template authoring time. Pass 0 mistakes log Item 6 had recommended the `p0_gate_predicate_traces_to_source_authority` validator — landed at Pass 1 as the schema check.

#### P1-3 — `confidence` block absent on every gate

- **Frequency:** 14 of 14 charters; 67 of 67 gates.
- **Failure mode:** Discipline 3a.5 (added at Pass 1 LOCK) establishes a pre-corpus confidence default: `{level: low, reason: "pre_corpus_hypothesis ...", promotion_requirement: "..."}`. No charter encoded it because the field did not exist pre-Pass-1.
- **Fix applied:** Every gate gets a `confidence` block. 65 of 67 default to `level: low`; 2 carry `level: medium` (D-RBDG and D-CFP gates with regulatory citations already present); 1 carries `level: high` (`F-HEINZ-INDIVIDUAL-OR-FORPROFIT` — verbatim Heinz grants page citation in [FIDELITY-FIX-HEINZ] commit).
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes (67 blocks added).
  3. **Validator added:** `gate_dsl_schema_check.py` enforces presence.
  4. Recorded here — yes.
- **Lesson.** Discipline 3a's pre-corpus default makes confidence machine-readable. Future authoring should ship confidence-block from charter-template day one.

#### P1-4 — Deprecated operator abbreviations (`lt`, `lte`, `gt`, `eq`, `matches`)

- **Frequency:** 8 of 14 charters (all program-level charters using §B `eligibility_gates` shape).
- **Failure mode:** Discipline 3a.3 establishes the canonical operator vocabulary (`equals`, `less_or_equal`, `greater_than`, `in`, `matches_regex`, etc.). Pre-Pass-1 charters used `lt / lte / gt / gte / eq / matches`. The aliases are deprecated; in-place renames are predicate-decomposition work outside Pass 1 no-invention boundary.
- **Fix applied:** Discipline 3a.3 documents the canonical-vs-deprecated table. Pass 1 adds inline comments at use sites (RBDG, RCDG, CFP, AGINNOV eligibility_gates) flagging the deprecated alias. NO in-place renames at Pass 1.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes.
  2. Global fix applied — no (Discipline 3a.6 no-invention boundary). Discipline 3a.3 documents the canonical names + alias table; renames deferred.
  3. **Validator NOT added at Pass 1:** future predicate-decomposition pass adds `operator_canonicalization_check.py` that fails on any non-canonical operator name. Scoping note in `_validators/README.md`.
  4. Recorded here — yes.
- **Lesson.** Operator-name canonicalization is structural-but-noisy work better done at a single dedicated pass (paired with composite-`matches` decomposition per P1-5) than spread across the charters.

#### P1-5 — Composite `operator: matches` with object-shape threshold

- **Frequency:** 5 charters (RBDG, RCDG, CFP, VAPG, AGINNOV); ~8 gate sites.
- **Failure mode:** Several gates use `operator: matches` with `threshold: { … }` as a composite predicate — e.g., `threshold: { max_new_employees: 50, max_projected_annual_gross_revenue_dollars: 1000000 }`. This shape is not in the canonical DSL grammar (Discipline 3a.3 operator vocabulary). The composite represents un-decomposed multi-field validation. Cedar policies and Logician runtime can't reason about composite shapes as cleanly as atomic predicates.
- **Fix applied:** Each gate flagged via `pass_1_reconciliation_note` with explicit decomposition guidance (e.g., RBDG-SMALL-AND-EMERGING-BENEFICIARY: "Decompose into max_new_employees less_or_equal 50 AND max_projected_annual_gross_revenue_dollars less_than 1000000").
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes.
  2. Global fix applied — no (predicate-decomposition deferred).
  3. **Validator NOT added at Pass 1:** future predicate-decomposition pass.
  4. Recorded here — yes.
- **Lesson.** Composite predicates were a Pass-0-era convenience that obscures source-trace-back. Decomposition pass + canonical-operator pass land together.

#### P1-6 — §A `decision_changed` prose drift from §B yaml

- **Frequency:** 3 of 14 charters (CFP, RCDG, AGINNOV — flagged in Pass-0 mistakes log).
- **Failure mode:** Pass-0 gate-id renames + predicate widening + severity promotions did not flow into §A `decision_changed` prose. CFP and RCDG flagged for Pass 1 in Pass-0 deferred-reconciliation list.
- **Fix applied:** RCDG §A `logician.decision_changed` + `red_team.decision_changed` + §1 strength-test answer reconciled with widened applicant-type predicate. AGINNOV §A `logician.decision_changed` reconciled with Pass-0 polarity flip + severity promotion.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (Pass 0 flagged 2; Pass 1 fixed 3 including AGINNOV).
  2. Global fix applied — yes for the 3 surfaced charters.
  3. **Validator scoped for separate dispatch:** Pass 0's `section_a_section_b_coherence` recommendation — when a gate is renamed or a predicate's semantics flip, scan §A `decision_changed` strings for the old gate id / old semantics.
  4. Recorded here — yes.
- **Lesson.** §A is documentation about §B; they have to update together. Charter authoring tooling should treat §A `decision_changed` strings as derived-from-§B and warn on drift.

#### P1-7 — Purpose-vs-classification mismatch

- **Frequency:** 6 of 14 charters; 10 gates.
- **Failure mode:** Some gates have a `(severity, fail_action)` tuple that classifies them as `competitive_scoring_signal` per Discipline 3a.4 but whose *purpose* would better fit `verify_required_gate` (eligibility-verification) or `drafting_warning` (Scribe register heuristic). Examples: IRB/IACUC gates are eligibility-verification (HOLD_FOR_OPERATOR_REVIEW would be more appropriate than WARN_OPERATOR); outcomes-conflated / unsupported-innovation / legacy-taxonomy / collaborator-language gates are Scribe heuristics (WARN_SCRIBE would be more appropriate).
- **Pattern regex:** Conceptual — no clean syntactic detector; surfaces from gate-purpose narrative review.
- **Fix applied:** Each gate flagged via `pass_1_reconciliation_note` routing to Pass 3 (Scribe) for drafting_warning candidates, Pass 4 (Judge) or operator review for verify_required_gate candidates. fail_action change is a predicate-semantic edit Pass 1 is not authorized to make.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes.
  2. Global fix applied — no (purpose change requires operator decision per gate).
  3. **Validator NOT added at Pass 1:** a "purpose_vs_classification_audit" validator could use keyword heuristics on gate-purpose narrative, but reliably auto-detecting purpose-vs-classification drift is hard. Better routed via explicit reconciliation notes.
  4. Recorded here — yes.
- **Lesson.** The taxonomy classifies by mechanism, not by intent; expect this drift across all future authoring. Pass 3 / Pass 4 / Pass 6 + operator reviews need a standing review item for these.

#### P1-8 — AGINNOV commodity-track prose persistence

- **Frequency:** AGINNOV only (1 of 14 charters).
- **Failure mode:** Pass-0 D-AGINNOV retired the commodity-track model (dairy / specialty-crop / hemp) in favor of the three-grant-type enum (innovation_planning / onsite_project / regional_impact) per canonical reference. The §B `claimed_grant_type` enum + `retired_commodity_track_model` audit-trail comment landed at Pass 0. But the supporting prose throughout §A scribe/red_team `decision_changed`, §1 strength-test answer, §B `evidence_ladder`, and red_team probe `AGINNOV-PROBE-TRACK-CASCADE-INTEGRITY` continued referencing commodity tracks.
- **Fix applied:** §1 prose tagged `[CONJECTURE — Pillar-2 corpus pending]` with explicit reconciliation-routing-to-Pass-3 note. Gate `F-AGINNOV-TRACK-ELIGIBILITY-CASCADE-MISMATCH` flagged via `pass_1_reconciliation_note`. Prose rewrite is Pass 3 (Scribe) scope.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — no (AGINNOV only).
  2. Global fix applied — no (per-charter, prose work deferred to Pass 3).
  3. **Validator NOT added at Pass 1.**
  4. Recorded here — yes.
- **Lesson.** Schema-and-prose-out-of-sync is the standard Pass-N → Pass-N+1 failure shape. Pass 0 fixed schema; Pass 1 flags; Pass 3 (Scribe) rewrites prose.

#### P1-9 — RK Mellon predicate roster mismatch with canonical reference

- **Frequency:** RK Mellon only (1 of 14 charters).
- **Failure mode:** `F-RK-MELLON-OUT-OF-PROGRAM-AREA` predicate enumerates 5 program areas (conservation / economic_development / education / family_wellness / community_vitality); canonical reference §RK Mellon Six Program Areas enumerates 6 (Conservation / Economic Development / Economic Mobility / Health & Well-Being / Organizational Effectiveness / Social-Impact Investments). Names also differ. `F-RK-MELLON-501C3-MISSING` predicate restricts to 501(c)(3); canonical reference also names public-agency + mission-driven-for-profit (social-impact-investment-only).
- **Fix applied:** `pass_1_reconciliation_note` flags both. Predicate widening is Pass 6 (inheritance) or operator review.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — no.
  2. Global fix applied — no (operator/Pass-6 review).
  3. **Validator NOT added at Pass 1.**
  4. Recorded here — yes.
- **Lesson.** Canonical reference + charter must reconcile. A charter-vs-canonical-reference cross-check validator would surface roster drift; scope at a future pass.

#### P1-10 — RCDG placeholder threshold value

- **Frequency:** RCDG only (1 of 14 charters).
- **Failure mode:** `F-RCDG-RURAL-AREA-INELIGIBLE` predicate `kfr.applicant.service_area_rural_population gt 0` is a near-degenerate proxy for the actual 7 CFR 4284-F rural-area threshold. Predicate fires only on zero-rural-population service areas; intended semantics are presumably the RD rural-area population ceiling.
- **Fix applied:** `pass_1_reconciliation_note` flags; threshold-pinning is Pillar-2 source-acquisition work.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — no.
  2. Global fix applied — no (Pillar-2 source-pin).
  3. **Validator NOT added at Pass 1.**
  4. Recorded here — yes.
- **Lesson.** Placeholder thresholds that pass schema validation but are semantically degenerate are a hidden failure mode. A "predicate-threshold-plausibility" validator scoped at a future pass could flag suspiciously placeholder values.

### Per-charter Pass-0 follow-up reconciliations applied

| Follow-up | Charter | Pass-1 action |
|---|---|---|
| D-RBDG: rubric tier descriptors + judge tie-breaker reconciliation | USDA-RD-RBDG-FY26 | `judge_scoring_map.tie_breaker` re-aligned with `match_logic.required_match: false`; tier descriptors flagged for Pass 4 (Judge) but not rewritten at Pass 1 (scoring-weight changes are Pass 4 scope). |
| D-CFP: boundary inclusivity | USDA-RD-CFP-FY26 | Pass 0 completed boundary fix; Pass 1 added gate_type + confidence to all 5 gates. |
| D-RCDG: §A prose reconciliation with widened gate | USDA-RD-RCDG-FY26 | §A `logician.decision_changed` + `red_team.decision_changed` + §1 strength-test answer all reconciled with widened applicant-type predicate. F-RCDG-CENTER-CAPACITY-UNDOCUMENTED gate present (Pass 0 added) and now classified. |
| D-AGINNOV: severity confirmation + commodity-track prose flag | PA-DEPT-AG-AGINNOV-FY26 | P0/REJECT_NO_DRAFT severity CONFIRMED per Discipline 2 (source-backed via canonical reference + machine-checkable). Commodity-track prose flagged via [CONJECTURE — Pillar-2 corpus pending] tag in §1 + `pass_1_reconciliation_note` on F-AGINNOV-TRACK-ELIGIBILITY-CASCADE-MISMATCH. Prose rewrite Pass 3 scope. |
| MANIFEST normalization | MANIFEST.md, README.md | "GOLD-STANDARD DRAFT v0" → "depth_charter_v0 (pre_corpus_hypothesis)" across all 14 MANIFEST rows + §All charters now Codex-framing depth_charter_v0 + §Sign-off path step 1. README §P2 retired "gold-standard" rhetoric + added Discipline-8 lifecycle-flip narrative. |

### Validators added or scoped

**Landed inline at Pass 1 LOCK** (under `pipeline/funder_intelligence/_validators/`):
- `no_unquoted_colon_placeholders.py` — Pass-0 G1 pattern; promoted to permanent CI check.
- `no_gold_standard_label_remaining.py` — Pass-0 G3 pattern; promoted with retirement-narrative exclusion markers.
- `gate_dsl_schema_check.py` — Discipline 3a required-fields contract enforcement.
- `gate_taxonomy_consistency.py` — Discipline 3a.4 severity-fail_action matrix enforcement.

**Scoped for separate dispatch** (acceptance criteria in `pipeline/funder_intelligence/_validators/README.md`):
- `no_quoted_scalar_paren_list_items.py` — Pass-0 G2 pattern; needs YAML-parser hook.
- `artifact_id_matches_filename.py` — header `artifact_id` vs filename stem.
- `lifecycle_status_valid.py` — Discipline-8 enum on four-field status block.

**Future-pass candidates (not yet scoped):**
- `operator_canonicalization_check.py` — fails on deprecated operator aliases (`lt`/`lte`/`gt`/`gte`/`eq`/`matches`). Pair with composite-predicate decomposition pass.
- `section_a_section_b_coherence.py` — Pass-0 recommendation; detects §A `decision_changed` drift from §B gate definitions.
- `predicate_threshold_plausibility.py` — flags placeholder threshold values (e.g., the RCDG `gt 0` pattern).
- `purpose_vs_classification_audit.py` — keyword heuristic over gate-purpose narrative; routes drafting_warning / verify_required_gate migration candidates.
- `charter_vs_canonical_reference_roster_check.py` — cross-checks predicate enums (program areas, applicant types, eligibility-roster) against canonical reference doc rosters.
- `match_logic_present_when_match_mentioned.py` — Pass-0 mistakes-log recommendation; schema check.
- `p0_gate_boundary_operator_documented.py` — Pass-0 mistakes-log recommendation; schema check for numeric P0 thresholds with explicit `lt/lte/gt/gte` + inline annotation.
- `gate_predicate_polarity_test.py` — Pass-0 mistakes-log recommendation; require positive + negative example pair per gate.

### Deferred to Pass 2 (Scout)

- The `pillar_2_dispatch_position` field is already on §B header tables for RBDG / RCDG / CFP / SARE-NE / VAPG / AGINNOV. Pass 2 (Scout) revisits discovery channels, deadline cadence, fit-signal grammar — Pass 1 did not touch any Scout-shaped field.
- The 6 inheritance candidates surfaced in Pass-1's gate inventory + reconciliation notes are routed to Pass 6 (inheritance), not Pass 2.

### Deferred to Pass 3 (Scribe)

- AGINNOV commodity-track prose strip (§A scribe/red_team `decision_changed`, §1 strength-test answer, §B `evidence_ladder`, red_team probe).
- 6 drafting_warning migration candidates (HEINZ outcomes/taxonomy/innovation, SARE-NE producer-as-collaborator, PA-DEPT-AG named-district, RK Mellon permanence).

### Deferred to Pass 4 (Judge)

- RBDG rubric tier descriptors (band 5 ≥50% cash, band 4 ≥30% cash) — Pass 1 reconciled the tie-breaker but not the descriptor language.
- 4 verify_required_gate migration candidates (USDA-NIFA IRB/IACUC, CFP ECF, VAPG value-added) — fail_action change requires Judge or operator decision.

### Deferred to Pass 6 (inheritance) or operator review

- RK Mellon predicate widening (501c3-only → +public-agency +social-impact-investment-for-profit; 5-program-area roster → 6-program-area roster per canonical reference).
- 6 program-level gates that duplicate funder-level gates (inheritance redundancy).

### Deferred to Pillar-2 source-acquisition

- Every `confidence.promotion_requirement` lists the Pillar-2 source artifact that would lift confidence for the gate. Aggregate list in `improvements_log_pass_1.md` §5.
- `F-RCDG-RURAL-AREA-INELIGIBLE` placeholder threshold (`gt 0`) needs actual 7 CFR 4284-F rural-area population threshold.

---

## Pass 2 — Scout (2026-05-19)

**Scope.** Normalize `runtime_consumers.scout` shape from prose to a 7-field structured mapping across all 14 Pillar-1 charters; populate `hard_gate_refs` from Pass-1's `hard_eligibility_gate` classification; surface cross-funder routing signal + operator-escalation triggers; annotate every Scout claim with `source_authority:` per Discipline-2 source-authority rule; author Scout cross-charter heuristic library.

**Charters touched.** 14 of 14.
**Validation pass rate.** 4 of 4 Pass-1 inline validators GREEN against post-Pass-2 corpus; 4 Pass-2 validators scoped with explicit acceptance criteria (not landed inline per Discipline 4).
**Diff shape.** ~498 inserts / ~49 deletes across 14 charter files.
**Dry-run artifact:** `pipeline/validation/pass-2-scout-dry-run-2026-05-18/`.

### Patterns caught

#### P2-1 — Scout block was free-form prose, not structured

- **Frequency:** 14 of 14 charters.
- **Failure mode:** `runtime_consumers.scout: |` was a single multi-line prose string. Substance was there but un-machine-readable — Tilth Scout runtime, Cedar policies, and Pass-3+ specialists could not extract structured Scout behavior. Pre-filter dimensions, hard-gate refs, cross-funder routing, and operator-escalation triggers were all collapsed into one paragraph.
- **Fix applied:** All 14 charters reshaped to a 7-field structured mapping (`pre_filter_question` / `eligibility_dimensions` / `hard_gate_refs` / `cross_funder_signal` / `operator_assist_required` / `source_authority` / `prose_summary`). Pre-Pass-2 prose preserved verbatim under `prose_summary:` for backward compat + audit trail.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes (14 of 14 reshape).
  3. **Validator scoped for separate dispatch:** `scout_block_shape_check.py` — validates 7-field mapping. Acceptance criteria in `improvements_log_pass_2.md` §3.
  4. Recorded here — yes.
- **Lesson.** Free-form prose at scaffold time becomes un-machine-readable structure debt. Future seat-binding reviews should require structured shapes from day one when downstream consumers (runtime + Cedar + later passes) depend on the fields.

#### P2-2 — Hard-gate references not surfaced in Scout block

- **Frequency:** 14 of 14 charters; 24 hard_eligibility_gate IDs absent from Scout pre-Pass-2.
- **Failure mode:** Pass 1 classified 24 of 67 gates as `hard_eligibility_gate`. None of the 14 Scout blocks pre-Pass-2 named these gates explicitly. Scout is the pre-filter that fires hard_eligibility_gate predicates BEFORE Scribe is invoked; the gate IDs must be addressable from Scout's structured shape for Logician + Cedar to wire the contract cleanly.
- **Fix applied:** Each Scout block now populates `hard_gate_refs:` with the exact set of `gate_type: hard_eligibility_gate` gate IDs from its own §B yaml. 24 total surfaced — matches Pass-1's tally exactly.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes (24 references surfaced).
  3. **Validator scoped:** `scout_hard_gate_refs_consistent_with_pass_1.py` — checks Scout's `hard_gate_refs` equals the §B hard_eligibility set. **High priority** — load-bearing Scout↔Logician contract.
  4. Recorded here — yes.
- **Lesson.** Cross-seat contracts (Scout↔Logician here; Scribe↔Judge in Pass-3+ pairs; Judge↔Red-Team) need the shared IDs surfaced on both sides at LOCK time so the contract is self-documenting. Pass 1 left the gates classified but not surfaced; Pass 2 surfaces.

#### P2-3 — Cross-funder routing signal was implicit or absent

- **Frequency:** 14 of 14 charters.
- **Failure mode:** Scout's role isn't just per-funder pre-filter — it's also a portfolio-router (which sister-funders to lateral to when fit is borderline). Pre-Pass-2 charters did not name the sister-funder cohort or the wrong-funder-match flags. Without explicit cross-funder signal, Scout cannot reason about portfolio assembly.
- **Fix applied:** Each Scout block carries `cross_funder_signal:` naming the funder cohort + the routing rules. Cross-charter regularities (Pittsburgh-foundation cohort; USDA portfolio routing; state↔federal routing; coop↔non-coop routing) documented in `_seats/scout/heuristics.md` §2.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes.
  3. **Validator NOT added at Pass 2.** A "cross_funder_routing_documented" validator would be cheap but the inter-charter consistency check (Funder A routes to Funder B; does Funder B's Scout know about the lateral?) is hard to encode mechanically. Scope at a future pass.
  4. Recorded here — yes.
- **Lesson.** Scout-as-portfolio-router is a distinct role from Scout-as-pre-filter. Both need explicit encoding. The CIC/CLC orthogonality rule from CLAUDE.md applies here — Scout's routing is opportunity-driven (CLC-engaged), not archetype-driven.

#### P2-4 — Operator-assist triggers buried in logician block

- **Frequency:** 14 of 14 charters.
- **Failure mode:** Where operator escalation is necessary BEFORE Scribe is invoked, the triggers were named in the logician PRE-gate roster (severity + fail_action tuple) but Scout's own operator-escalation logic was implicit. Without explicit Scout-layer escalation, the orchestrator couldn't route to operator-attention queue before Scribe spins up — wasted Scribe cycles on cases operator should triage.
- **Fix applied:** Each Scout block carries `operator_assist_required:` naming the specific gate-fire conditions that escalate. The 5 universal escalation patterns are documented in `heuristics.md` §4.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes.
  2. Global fix applied — yes.
  3. **Validator NOT added at Pass 2.** The escalation-trigger field is now mandatory in the Scout shape (covered by `scout_block_shape_check.py` if it lands). Semantic-correctness check (does the operator_assist_required prose match the actual escalation-shaped gates?) is harder; scope at a future pass.
  4. Recorded here — yes.
- **Lesson.** Pre-Scribe operator escalation needs Scout-layer surface, not just gate-layer surface. The orchestrator's routing logic depends on it.

#### P2-5 — Foundation funders carry no SAM/UEI baseline; absence wasn't documented

- **Frequency:** 5 of 14 charters (Heinz, RK Mellon, NCBA-CLUSA, PA-DCED, PA-DEPT-AG, PA-DEPT-AG-AGINNOV).
- **Failure mode:** USDA-RD funder-level encodes a 4-gate federal-baseline (SAM, UEI, federal-debt, suspension/debarment). Federal program-instances inherit. But foundations + state-program funders do NOT carry this baseline because they don't require federal registration. The ABSENCE was nowhere documented, leading to implicit confusion: should Scout pre-check SAM for foundation paths? Answer: NO. But the negative-space was invisible.
- **Fix applied:** Negative-space documented explicitly in `heuristics.md` §1.4 (foundations) + §1.3 (state-programs). Per-charter Scout blocks for foundations + state programs omit the `sam_uei_baseline` dimension by design; federal program-instances include it.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes.
  2. Global fix applied — yes (heuristic library + per-charter consistency).
  3. **Validator NOT added at Pass 2.** Negative-space-documentation is hard to mechanize; the heuristic-library reference is the recurrence guard for now.
  4. Recorded here — yes.
- **Lesson.** Absence as load-bearing information is a recurring failure shape. The same pattern shows up in Pass-3 / Pass-4 / Pass-6 when seat behavior is documented for funder class A but the absence of that behavior for funder class B is implicit. Heuristic library + cross-pass review captures this.

#### P2-6 — State-program "state-budget-cycle" Scout pre-filter not in federal funders

- **Frequency:** 3 of 14 charters (PA-DCED, PA-DEPT-AG, PA-DEPT-AG-AGINNOV).
- **Failure mode:** State programs are gated by state-budget reconciliation. Appropriations must be enacted before the program can open. State-budget timing risk is a Scout-layer escalation trigger to operator — federal funders have analogous CR-uncertainty risk but the cadence + cause differ.
- **Fix applied:** State-program Scout blocks carry the state-budget-cycle escalation explicitly. Federal counterpart (continuing-resolution risk, federal-shutdown risk) documented as a separate concern in `heuristics.md` §3.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (all 3 state-program charters).
  2. Global fix applied — yes for state-program family.
  3. **Validator NOT added at Pass 2.**
  4. Recorded here — yes.
- **Lesson.** Funder-class-specific Scout heuristics need explicit encoding when they differ from defaults. The class-axis heuristic library makes this addressable.

#### P2-7 — Source-authority labeling missing on Scout claims

- **Frequency:** 14 of 14 charters.
- **Failure mode:** Pre-Pass-2 Scout prose made claims (e.g., "DISCOVER restricts to rural <20K") without citation. Discipline-2 source-authority rule applies to Scout the same as to Logician — every Scout claim must declare source or be marked conjecture.
- **Fix applied:** Every Scout block carries `source_authority:` field. 9 of 14 source-backed; 3 partial; 2 marked `[CONJECTURE — Pillar-2 corpus pending]` (NCBA-CLUSA, USDA-NIFA funder-level). Aggregate Pillar-2 ingest priority queue documented in `improvements_log_pass_2.md` §5.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes.
  3. **Validator scoped:** `scout_source_authority_documented.py` — validates field present + non-empty; emits Pillar-2 ingest priority queue.
  4. Recorded here — yes.
- **Lesson.** Discipline-2 source-authority is universal across all seats, not just Logician. Every seat's runtime instructions need source-backing or explicit conjecture marker.

#### P2-8 — Pre-filter question was implicit, not addressable

- **Frequency:** 14 of 14 charters.
- **Failure mode:** Scout's job at DISCOVER is to answer one yes/no-shaped question per opportunity. The question varies by funder. Pre-Pass-2 charters never made this question explicit — Scout's "central test" was implicit in the prose.
- **Fix applied:** Each Scout block carries `pre_filter_question:` as a single question-shaped sentence. All 14 questions inspected for question-shape conformance (see `validation_results.md` Inspection 4).
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes.
  3. **Validator scoped:** `scout_pre_filter_question_present.py` — trivial cheap check.
  4. Recorded here — yes.
- **Lesson.** Each seat needs a canonical one-sentence framing of its core test/decision. Pass 3 (Scribe), Pass 4 (Judge), Pass 5 (Red Team) should follow the same pattern.

### Per-charter notable observations

| Charter | Notable Pass-2 observation |
|---|---|
| HEINZ-FOUNDATION | Geographic dimension is weighted-fit (SWPA HIGH / PA-Commonwealth-serving-SWPA MEDIUM / out-of-PA NOT universal-fail) per Heinz GPR 2024. Distinct from RK Mellon's hard-PA-out-of-program-area gate. |
| NCBA-CLUSA | Full conjecture; Pillar-2 priority ingest target. Cooperative-form-authenticity is the central pre-filter dimension. |
| PA-DCED | Multi-program funder; program-instance Scout pre-filters will source-pin at child charters. |
| PA-DEPT-AG-AGINNOV-FY26 | Pass-0 D-AGINNOV grant-type model + match-source polarity flip embedded in dimensions. Commodity-track legacy marked conjecture per P1-8. |
| PA-DEPT-AG | Funder-level; routes DOWN to PA-DEPT-AG-AGINNOV + sister state-AG programs. |
| RICHARD-KING-MELLON-FOUNDATION | P1-9 widened-entity reconciliation flagged in source_authority — 5-program-area charter vs canonical 6-area roster. |
| USDA-AMS-VAPG-FY26 | FY26 cycle CLOSED → FY27 NOFO drop monitored. META gate F-VAPG-CYCLE-CLOSED routes operator to defer. |
| USDA-AMS | Aggregator/distributor misclassification flagged as recurring failure mode in operator_assist_required. |
| USDA-NIFA-SARE-NE-FY26 | Northeast-SARE region applicability; out-of-region routes to sister-SARE programs (Southern, North-Central, Western). |
| USDA-NIFA | `hard_gate_refs: []` (P1-7 purpose-vs-classification migration candidates pending operator decision). |
| USDA-RD-CFP-FY26 | Pass-0 D-CFP boundary-inclusive `lte` rural-pop preserved. Davis-Bacon + NEPA cascade surfaced. |
| USDA-RD-RBDG-FY26 | Pass-0 D-RBDG match-as-competitive-factor (not hard requirement) reflected. |
| USDA-RD-RCDG-FY26 | P1-10 rural-area threshold placeholder flagged in source_authority pending Pillar-2 source-pin. |
| USDA-RD | Funder-level federal-baseline (4 PRE-gates) is the inheritance source for all USDA-RD program-instances. |

### Validators added or scoped

**None landed inline at Pass 2** (per Discipline 4 — operator approval gates inline-validator landing).

**Scoped for separate dispatch** (acceptance criteria in `improvements_log_pass_2.md` §3):
- `scout_block_shape_check.py` — 7-field mapping validator.
- `scout_hard_gate_refs_consistent_with_pass_1.py` — load-bearing Scout↔Logician contract. **High priority.**
- `scout_source_authority_documented.py` — Discipline-2 propagation to Scout layer.
- `scout_pre_filter_question_present.py` — trivial cheap recurrence guard.

**Future-pass candidates (not yet scoped):**
- `cross_funder_routing_documented.py` — inter-charter consistency (Funder A routes to Funder B; does Funder B's Scout know about the lateral?).
- `negative_space_documentation_check.py` — when funder class A carries dimension X and class B doesn't, the absence is documented (state-program absence-of-SAM-baseline pattern; foundation absence-of-SAM-baseline pattern).

### Deferred to Pass 3 (Scribe)

- AGINNOV commodity-track prose strip (continued from Pass-1 P1-8 — Pass-3 scope).
- 6 drafting_warning migration candidates from Pass-1 P1-7 (HEINZ outcomes/taxonomy/innovation, SARE-NE producer-as-collaborator, PA-DEPT-AG named-district, RK Mellon permanence).
- Scribe-shape `pre_filter_question:`-analog (the central test Scribe runs per section).

### Deferred to Pass 4 (Judge)

- RBDG rubric tier descriptors (continued from Pass-1).
- 4 verify_required_gate migration candidates (continued from Pass-1).
- Judge-shape `pre_filter_question:`-analog (the central test Judge applies per rubric dimension).

### Deferred to Pass 6 (inheritance) or operator review

- RK Mellon widened-entity predicate (5 → 6 program-area roster) per Pass-1 P1-9.
- 6 program-level gates duplicating funder-level gates (Pass-1 inheritance redundancy).
- CIC routing field (open question §6.1 in heuristics.md).
- CLC affinity field (open question §6.2).
- Funder-class enum field (open question §6.4).

### Deferred to Pillar-2 source-acquisition

- NCBA-CLUSA full corpus ingest (NCBA program materials + Rochdale Pioneers principles).
- USDA-NIFA funder-level register source-pin (NIFA Grants Application Guide).
- PA-DEPT-AG funder-level portfolio-page ingest.
- PA-DCED Act 90 funding-categories ingest.
- RCDG rural-area population threshold pinning per Pass-1 P1-10.
- RK Mellon canonical 6-program-area roster reconciliation per Pass-1 P1-9.

---

## Pass 3 — Scribe (2026-05-19)

**Scope.** Normalize `runtime_consumers.scribe` shape from prose to a 7-field structured mapping across all 14 Pillar-1 charters; populate inheritance pointers for the 6 program-instance charters; apply Pass-1-deferred AGINNOV commodity-track prose strip across 9 prose locations; verify Heinz M1/M2/M3 mechanism wiring is explicit in the structured shape; surface cross-funder Scribe register family signature at `pipeline/funder_intelligence/_seats/scribe/registers.md`; annotate every Scribe claim with `source_authority:` per Discipline-2 source-authority rule; land 2 Pass-3-inline validators (scribe_block_shape_check + scribe_register_cited_to_canonical).

**Charters touched.** 14 / 14.
**Validation pass rate.** 4 of 4 Pass-1 inline validators + 2 of 2 Pass-3 inline validators GREEN against post-Pass-3 corpus (6 / 6 cheap validators all exit 0).
**Diff shape.** ~1036 inserts/deletes across 14 charter files (patch.diff aggregate).
**Dry-run artifact:** `pipeline/validation/pass-3-scribe-dry-run-2026-05-18/`.

### Patterns caught

#### P3-1 — Scribe block was free-form prose, not structured

- **Frequency:** 14 of 14 charters.
- **Failure mode:** `runtime_consumers.scribe: |` was a single multi-line prose string. Substance was there but un-machine-readable — Tilth Scribe runtime, Cedar policies, and Pass-4+ specialists could not extract structured Scribe behavior. Voice/register/section-ordering/must-do/must-not-do all collapsed into one paragraph. Identical pattern shape to Pass-2 P2-1 (Scout block).
- **Fix applied:** All 14 charters reshaped to a 7-field structured mapping (`voice_change` / `section_ordering` / `must_do` / `must_not_do` / `cross_funder_signal` / `source_authority` / `prose_summary`). Pre-Pass-3 prose preserved verbatim under `prose_summary:` for backward compat + audit trail.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes (14 of 14 reshape).
  3. **Validator added:** `scribe_block_shape_check.py` — landed inline at Pass 3, exit 0.
  4. Recorded here — yes.
- **Lesson.** Same lesson as Pass-2 P2-1: free-form prose at scaffold time becomes un-machine-readable structure debt. Two consecutive passes (Scout + Scribe) hit the same shape; the next two passes (Judge + Red Team) should ship structured shapes from day one. The depth-charter template should be updated to require structured 7-field shapes for all four seat runtime_consumers blocks.

#### P3-2 — Program-instance charters did not declare language_register inheritance explicitly

- **Frequency:** 5 of 6 program-instance charters (CFP, VAPG, RBDG, RCDG, AGINNOV).
- **Failure mode:** Inheritance was implicit ("inherits PA-DEPT-AG funder depth-charter" prose in §A). No standalone `language_register` block + no machine-readable `language_register_inheritance:` pointer. Downstream consumers couldn't address inheritance structure.
- **Fix applied:** Every program-instance charter now carries `language_register_inheritance:` with `parent_charter:` + `inherits:` list + program-specific `overlays:` block. RCDG additionally declares `composed_overlay: NCBA-CLUSA` for sub-cooperative beneficiaries. No re-declaration of funder-level register entries.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (5 of 6 program-instances).
  2. Global fix applied — yes.
  3. **Validator added:** `scribe_register_cited_to_canonical.py` — landed inline at Pass 3, exit 0; emits per-charter inheritance + register inventory.
  4. Recorded here — yes.
- **Lesson.** Inheritance has to be both narratively documented (so operators understand it) AND machine-readable (so downstream consumers can flatten / lookup register entries through the inheritance chain). Pre-Pass-3 charters had only narrative; Pass 3 added structured.

#### P3-3 — Cross-funder routing signal at the SCRIBE layer was implicit or absent

- **Frequency:** 14 of 14 charters.
- **Failure mode:** Pre-Pass-3 Scribe prose did not name the funder cohort or the cross-funder register-axis explicitly. Same applicant pitching multiple funders code-switches per funder; without explicit cross-funder Scribe-layer surface, drafts can drift toward template-by-imitation.
- **Fix applied:** Every Scribe block carries `cross_funder_signal:` naming the funder cohort and the register-axis difference. Cross-charter register families documented in `registers.md` §9 (4 patterns: code-switching per agency / composable overlays / program-instance inheritance / funder-class register families).
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes.
  3. **Validator NOT added at Pass 3:** scoped for future-pass — `scribe_cross_funder_signal_bidirectional.py` (inter-charter consistency: Funder A mentions Funder B; does Funder B mention Funder A?). Cost > value at Pass 3.
  4. Recorded here — yes.
- **Lesson.** Cross-seat surface uniformity. Scout (Pass 2) made cross_funder_signal a structured field. Scribe (Pass 3) mirrored. Judge + Red Team (later passes) should follow the same pattern.

#### P3-4 — Source-authority labeling missing on Scribe claims

- **Frequency:** 14 of 14 charters.
- **Failure mode:** Pre-Pass-3 Scribe prose made register claims without source-authority declaration. Discipline-2 source-authority rule applies to Scribe the same as to Logician + Scout. Identical pattern to Pass-2 P2-7.
- **Fix applied:** Every Scribe block carries `source_authority:` field. Source-backed claims labeled with canonical-reference anchors; operator-derived heuristics labeled explicitly; conjecture marked `[CONJECTURE — Pillar-2 corpus pending]`.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes.
  3. **Validator added:** `scribe_block_shape_check.py` enforces field presence + non-empty.
  4. Recorded here — yes.
- **Lesson.** Same as Pass-2 P2-7: Discipline-2 source-authority is universal across all seats, not just Logician. Every seat's runtime instructions need source-backing or explicit conjecture marker. Pass-3 closes the Scribe gap; Judge + Red Team still pending.

#### P3-5 — AGINNOV commodity-track prose persistence (Pass-1 P1-8 follow-through)

- **Frequency:** 1 of 14 charters (PA-DEPT-AG-AGINNOV-FY26).
- **Failure mode:** Pass-0 D-AGINNOV retired the commodity-track model in favor of the three-grant-type enum at the schema layer (`claimed_grant_type.enum:` + `retired_commodity_track_model.historical_tracks_pre_pass_0:` for audit trail). Pass-0 left supporting prose throughout §A scribe/red_team `decision_changed`, §A strength_test answers, §B evidence_ladder, §B scribe_section_requirements §III, §B red_team_probes AGINNOV-PROBE-TRACK-CASCADE-INTEGRITY, and §1 prose unchanged. Pass-1 P1-8 routed the prose strip to Pass 3 per the no-invention boundary.
- **Fix applied:** Pass-3 strip across 9 prose locations:
  1. §A `runtime_consumer.scribe.decision_changed`.
  2. §A strength_test answer 1 (drafting decision).
  3. §A strength_test answer 2 (proposal rejected).
  4. §A strength_test answer 3 (Red Team probe).
  5. §B `evidence_ladder.strongest`.
  6. §B `evidence_ladder.weak`.
  7. §B `evidence_ladder.unacceptable`.
  8. §B `scribe_section_requirements §III`.
  9. §B `red_team_probes AGINNOV-PROBE-TRACK-CASCADE-INTEGRITY` (probe_question + appended `pass_3_relabel_note`).
  Plus §1 prose paragraph + §1 same-prompt-with/without test + §B `source_backing.corpus_refs` track-cascade-documentation reference. Gate predicate names retained per Pass-1 no-invention rule with explicit relabel notes.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — no (AGINNOV only).
  2. Global fix applied — no (per-charter, prose work).
  3. **Validator NOT added at Pass 3.**
  4. Recorded here — yes.
- **Lesson.** Schema-and-prose-out-of-sync is the standard Pass-N → Pass-N+1 → Pass-N+2 failure shape (Pass-0 fixes schema; Pass-1 flags; Pass-3 rewrites prose). The next time a Pass-0 schema fix retires a primitive (like the commodity-track model), the Pass-1 + Pass-3 strip should be planned together rather than discovered.

#### P3-6 — Heinz M1/M2/M3 mechanism wiring not surfaced in structured Scribe shape

- **Frequency:** 1 of 14 charters (HEINZ-FOUNDATION).
- **Failure mode:** Heinz's three GPR-derived behavior_mechanisms (M1 regional_legitimacy_capital + M2 transition_sensitive_relationship_clarity + M3 capacity_partnership_beyond_grant) were source-backed and load-bearing in §A scribe.decision_changed prose + §B `behavior_mechanisms:` schema + §B drafting_implications. But the Pass-2 (Scout) reshape carried mechanism signals only at the cross_funder_signal level; the Scribe layer had implicit-only wiring in `runtime_consumers.scribe: |` prose.
- **Fix applied:** Heinz's Pass-3 7-field scribe block wires M1/M2/M3 explicitly across 4 fields:
  - `voice_change:` names all three mechanisms with mechanism IDs.
  - `section_ordering:` explicitly threads [M1] / [M2] / [M3] across §I / §III / §V.
  - `must_do:` 4 of 10 entries carry [M1] / [M2] / [M3] prefix anchors.
  - `must_not_do:` 3 entries reference M1/M2/M3 by name.
  - `cross_funder_signal:` contrasts Heinz M1/M2/M3 stack with RK Mellon scale-and-permanence emphasis.
  - `source_authority:` anchors mechanism wiring to Heinz GPR 2024 + [FIDELITY-FIX-HEINZ] commit.
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — no (Heinz-specific mechanism stack).
  2. Global fix applied — no (per-charter).
  3. **Validator NOT added at Pass 3.**
  4. Recorded here — yes.
- **Lesson.** Funder-specific mechanism stacks (like Heinz's M1/M2/M3) must be addressable at every seat's structured shape — not just at the seat-prose layer. The §B `behavior_mechanisms:` schema is canonical; downstream seat structured shapes should reference mechanism IDs explicitly.

#### P3-7 — One-sentence voice-signature framing per seat (cross-pass structural pattern)

- **Frequency:** structural pattern observed across passes (Scout + Scribe; Judge + Red Team pending).
- **Failure mode:** Each seat needs a single one-sentence framing of its core test / decision shape. Pass-2 P2-8 introduced `pre_filter_question:` for Scout. Pass-3 introduced `voice_change:` for Scribe.
- **Fix applied:** `voice_change:` populated on every Scribe block (14 / 14).
- **Pattern-propagation answers:**
  1. Recurred in > 1 charter — yes (universal).
  2. Global fix applied — yes.
  3. **Validator NOT added at Pass 3:** structural pattern already enforced via `scribe_block_shape_check.py` field-presence.
  4. Recorded here — yes.
- **Lesson.** Each seat's structured shape carries one canonical one-sentence-shaped framing field. Pass 4 (Judge) should add `central_rubric_question:` or equivalent; Pass 5 (Red Team) should add `central_adversarial_probe:` or equivalent.

### Per-charter notable observations

| Charter | Notable Pass-3 observation |
|---|---|
| HEINZ-FOUNDATION | M1/M2/M3 mechanism wiring made explicit in structured shape (P3-6). 12 preferred / 4 suspicious terms in standalone language_register. |
| NCBA-CLUSA | Cross-family overlay status documented in `cross_funder_signal:` — NCBA-CLUSA composes onto USDA-RCDG + USDA-VAPG + coop-favoring foundations; not standalone-funder register. [CONJECTURE — Pillar-2 corpus pending] for full corpus. |
| PA-DCED | Standalone register with economic-development-metrics overlay. Distinct from PA sister-agency PA-DEPT-AG (state-program-officer + PA-Preferred). |
| PA-DEPT-AG-AGINNOV-FY26 | Inherits PA-DEPT-AG + AGINNOV-specific overlay. Commodity-track strip applied across 9 prose locations (P3-5). |
| PA-DEPT-AG | Standalone register; parent of AGINNOV. PA-Preferred conditional in overlays. |
| RICHARD-KING-MELLON-FOUNDATION | 5-vs-6 program-area roster reconciliation (P1-9) flagged in source_authority field. |
| USDA-AMS-VAPG-FY26 | Inherits USDA-AMS + VAPG-specific track-selection + value-added definition overlay. Conditional NCBA-CLUSA composition when applicant is cooperative. |
| USDA-AMS | Standalone register; parent of VAPG. VAPG rubric source-backed at pipeline/rubrics/vapg_fy26.json. |
| USDA-NIFA-SARE-NE-FY26 | Standalone language_register (own SARE-specific overlay — three-pillar verbatim + producer-as-co-investigator). Composes USDA-NIFA peer-review-academic base register but adds enough SARE-specific moves that standalone register block is load-bearing. |
| USDA-NIFA | Standalone register; parent of SARE-NE. Peer-review-academic register. |
| USDA-RD-CFP-FY26 | Inherits USDA-RD + CFP-specific overlays (essential-community-facility + MHI + Davis-Bacon + NEPA). |
| USDA-RD-RBDG-FY26 | Inherits USDA-RD + RBDG-specific small-and-emerging + cash-first match (per Pass-0 D-RBDG). |
| USDA-RD-RCDG-FY26 | Inherits USDA-RD + composes NCBA-CLUSA cooperative-authenticity overlay for sub-cooperatives. First charter to explicitly declare `composed_overlay: NCBA-CLUSA`. |
| USDA-RD | Standalone register; parent of CFP / RBDG / RCDG. Cross-program register pattern. |

### Validators added or scoped

**Landed inline at Pass 3 LOCK** (under `pipeline/funder_intelligence/_validators/`):

- `scribe_block_shape_check.py` — 7-field mapping enforcement.
- `scribe_register_cited_to_canonical.py` — language_register OR inheritance pointer enforcement; per-charter inventory emission.

**Scoped for future-pass dispatch** (acceptance criteria in `improvements_log_pass_3.md` §3):

- `scribe_inheritance_no_inline_duplication.py` — defense against future regressions where program-instance charters re-declare funder-level register entries inline.
- `scribe_voice_change_uniqueness.py` — paranoia-defense against template-by-imitation (Pass-0 G2 echo).
- `scribe_cross_funder_signal_bidirectional.py` — inter-charter consistency check.

### Deferred to Pass 4 (Judge)

- 4 verify_required_gate migration candidates (continued from Pass-1).
- RBDG rubric tier descriptors (continued from Pass-1).
- Judge-shape `central_rubric_question:`-analog (one-sentence framing per Pass-3 P3-7).
- Drafting-warning gate-class migration decisions for the 6 P1-7 candidates (HEINZ outcomes/taxonomy/innovation, SARE-NE producer-as-collaborator, PA-DEPT-AG named-district, RK Mellon permanence). Pass 3 kept them as `competitive_scoring_signal` with explicit drafting-warning narrative; Pass 4 / operator decides whether fail_action migration is warranted.

### Deferred to Pass 5 (Red Team)

- AGINNOV-PROBE-TRACK-CASCADE-INTEGRITY semantic relabel (probe_id retained at Pass 3 with `pass_3_relabel_note`; full relabel + any new probes is Pass-5 scope).
- Red-Team-shape `central_adversarial_probe:`-analog (one-sentence framing per Pass-3 P3-7).

### Deferred to Pass 6 (inheritance) or operator review

- RK Mellon predicate widening (5 → 6 program-area roster) per Pass-1 P1-9.
- Funder-class enum field (open question §6.4 in scout heuristics.md + §11.2 in scribe registers.md).
- NCBA-CLUSA overlay composition contract — canonical inheritance shape (open question §11.1).

### Deferred to Pillar-2 source-acquisition

- NCBA-CLUSA full corpus ingest (continued from Pass-2 P2-7).
- USDA-NIFA cross-program weighting heuristics ("methodology rigor ≥30%") pinpoint citations.
- PA-DCED weighting heuristics ("Economic Impact ≥30%") pinpoint citations.
- USDA-RD "leveraging > innovation" cross-program weighting pattern pinpoint citations.
- RK Mellon program-area roster reconciliation (P1-9 carryover).
- F-RCDG-RURAL-AREA-INELIGIBLE placeholder threshold (P1-10 carryover).
- Heinz foundation-program-officer general register Pillar-2 corroboration (M1/M2/M3 mechanism wiring already source-backed; the foundation-register-class heuristic is operator-derived).

---

## Pass 4 — Judge (TBD)

(Appended when Pass 4 dry-run completes. Scope: rubric alignment, tier-descriptor coherence with eligibility gates, cross-rubric cross-checks, scoring-criterion source-authority.)

### Patterns caught

_TBD._

### Per-charter fixes

_TBD._

### Deferred to Pass 5

_TBD._

### Validators added

_TBD._

---

## Pass 5 — Red Team (TBD)

(Appended when Pass 5 dry-run completes. Scope: adversarial probe coverage, cross-family rigor with Scribe / Judge, attack-surface enumeration, failure-mode propagation tests.)

### Patterns caught

_TBD._

### Per-charter fixes

_TBD._

### Deferred to operator review

_TBD._

### Validators added

_TBD._

---

## Cross-pass insights

(Populated after Pass 5 completes — synthesizes systemic patterns across all passes. Expected sections: recurring error families that surfaced across multiple seats; validators that retired others; charter-level coherence patterns; the "anchor charter propagates" pattern; the rhetoric-vs-state-mismatch family; what the next FID cycle should bake into the depth-charter template from day one.)

_TBD._
