# FID Refinement Methodology — Disciplined Operating Model

**Document ID:** FID_REFINEMENT_METHODOLOGY_2026-05-18
**Lifecycle:** canonical methodology
**Authored:** 2026-05-18
**Companion:** [`FID_CANONICAL_REFERENCE_2026-05-18.md`](./FID_CANONICAL_REFERENCE_2026-05-18.md)

---

## Purpose

This document encodes the disciplined operating model for refining FID (Funder Intelligence Document) charters in `pipeline/funder_intelligence/pillar_1_charters/`. It defines the pass sequence, source-authority hierarchy, gate taxonomy, no-invention boundary, validation checks, lifecycle labels, and improvements-log format that every refinement specialist must obey.

It is meta-only. Existing charters are not modified by the publication of this document; subsequent refinement passes will be reviewable diffs against this grammar.

---

## Discipline 1 — Pass Model

Refinement runs as an ordered pass sequence. Each pass is performed by a specialist whose scope is bounded by the discipline below. Later passes inherit earlier passes' outputs but never silently rewrite them; conflicts surface to operator review.

| Pass | Specialist | Output |
|---|---|---|
| **Pass 0** | foundations / blocking repair | unblock structural defects (parse errors, missing required fields, broken cross-references) so later passes have a stable substrate |
| **Pass 1** | Logician | canonical gate taxonomy (see Discipline 3); each charter's gate set normalized to the taxonomy |
| **Pass 2** | Scout | discovery channels, deadline cadence, fit-signal grammar |
| **Pass 3** | Scribe | scaffold sections, voice/register, mandatory framings, boilerplate registry |
| **Pass 4** | Judge | rubric dimensions, scoring weights, evaluation themes; cross-checked against funder's published rubric |
| **Pass 5** | Red Team | failure modes, common misreadings, adversarial challenges |
| **Pass 6** *(optional)* | inheritance specialist | parent-funder → program-charter inheritance cleanup; only run when Passes 1–5 surface inheritance drift |

**Rule:** Pass N may not begin until Pass N–1 has produced its patch, improvements log, and validation notes, and the operator has approved them. No pass jumps ahead.

---

## Discipline 2 — Source Authority Rule

Every claim added to or modified in a charter must declare its source authority level. The five levels are enforced:

```yaml
source_authority:
  P0_gate:
    allowed_only_if: "explicitly source-backed and machine-checkable"
  HIGH_warning:
    allowed_if: "strongly source-backed but may require operator interpretation"
  MED_warning:
    allowed_if: "operator-derived, heuristic, or relationship-sensitive"
  drafting_guidance:
    allowed_if: "heuristic or corpus-derived pattern"
  conjecture:
    allowed_runtime_status: "do_not_load_as_enforcement"
```

**Promotion rule:** a claim may be promoted to a stronger authority level only when the supporting source artifact (a NOFA, agency program page, statute, regulation, signed rubric, or canonical-reference doc entry) is cited inline. The canonical reference doc (`FID_CANONICAL_REFERENCE_2026-05-18.md`) is itself a source artifact, but its entries trace back to the operator-supplied synthesis whose citation notation must be preserved.

**Demotion rule:** any P0 gate whose source citation cannot be re-verified during a pass is demoted to HIGH_warning and surfaced to operator review with `validation_status: source_lost`.

**Conjecture handling:** conjecture is permitted in the charter as a comment or appendix entry, but `runtime_load_status: do_not_load_as_enforcement` is mandatory and machine-readable.

---

## Discipline 3 — Pass 1 Produces Canonical Gate Taxonomy

Pass 1 (Logician) defines the gate taxonomy that all later specialists obey. Specialists may not invent new gate types; they may only instantiate gates of the defined types.

```yaml
gate_taxonomy:
  hard_eligibility_gate:
    severity_allowed: [P0]
    source_required: true
    fail_action_allowed: [REJECT_NO_DRAFT, HOLD_DRAFT]

  verify_required_gate:
    severity_allowed: [VERIFY_REQUIRED, HIGH]
    source_required: true
    fail_action_allowed: [HOLD_FOR_OPERATOR_REVIEW]

  competitive_scoring_signal:
    severity_allowed: [LOW, MED, HIGH]
    source_required: true_or_false
    fail_action_allowed: [WARN_OPERATOR, SCORE_DOWN]

  drafting_warning:
    severity_allowed: [LOW, MED]
    source_required: false
    fail_action_allowed: [WARN_SCRIBE]

  relationship_signal:
    severity_allowed: [LOW, MED]
    source_required: false_or_tier_2
    fail_action_allowed: [WARN_OPERATOR]
```

**Gate field contract.** Every gate in every charter must carry:

* `gate_id` — unique string within the charter
* `gate_type` — one of the five taxonomy entries above
* `field` — the PROJECT_CONTEXT or RFA field the gate evaluates
* `operator` — comparison operator (`equals`, `in`, `lte`, `gte`, etc.)
* `value` — comparator value or value set
* `severity` — drawn from the gate-type's `severity_allowed` set
* `fail_action` — drawn from the gate-type's `fail_action_allowed` set
* `source_required` — boolean, matching the gate-type's rule
* `corpus_ref` — citation pointer (NOFA URL, statute section, canonical-reference anchor, or operator-attested note)

A gate missing any of these fields fails Discipline 7 validation and blocks the pass.

---

## Discipline 4 — No Auto-Commit

Each pass produces three artifacts and stops:

1. **Patch / diff** — the proposed changes to charter files, presented as a reviewable diff.
2. **Improvements log** — Discipline 9-format entry describing what changed and why.
3. **Validation notes** — Discipline 7 checklist results.

The operator reviews all three before any commit lands. No pass commits its own work. No pass merges another pass's work without operator sign-off.

**Branching convention:** each pass writes to a pass-scoped branch (e.g., `fid-pass-1-logician-2026-MM-DD`). The operator merges to the integration branch after review. The final integration branch is the unit of PR review.

---

## Discipline 5 — Pattern Propagation Check (per pass)

Every pass must answer the following four questions in its improvements log. Failure to answer is itself a validation failure.

* **Did this error appear in more than one charter?** If yes, it is a pattern, not a per-charter defect.
* **Did the fix get applied globally?** If the error is a pattern, the fix must touch all affected charters in the same pass.
* **Did we add a validator so this class of error does not recur?** Pattern fixes that don't add a recurrence guard are incomplete.
* **Did the improvements log record the pattern?** The log is the institutional memory; an unrecorded pattern will be re-discovered by a future pass.

---

## Discipline 6 — No-Invention Rule

The specialist's authority is bounded. The specialist may shape and surface; it may not fabricate.

```yaml
no_invention_rule:
  specialist_may:
    - normalize structure
    - flag missing evidence
    - convert vague logic into typed placeholders
    - propose source-needed fields
    - demote unsupported claims
  specialist_must_not:
    - invent eligibility rules
    - invent scoring weights
    - invent reviewer behavior
    - promote conjecture to source-backed fact
    - create P0 gates without explicit source support
```

When a specialist encounters a missing rule or weight that cannot be inferred from source, it must insert a `[NEEDED: source_required]` placeholder and surface the gap in the improvements log. This is the same `[NEEDED]` convention used in PROJECT_CONTEXT.md files.

---

## Discipline 7 — Validation Checklist After Every Pass

```yaml
validation_after_each_pass:
  - all_yaml_blocks_parse
  - artifact_id_matches_filename
  - lifecycle_status_valid
  - every_gate_has: [gate_id, gate_type, field, operator, value, severity, fail_action, source_required, corpus_ref]
  - no_unquoted_colon_placeholders
  - no_P0_without_source_required_true
  - no_gold_standard_label_without_source_backing
  - gate_taxonomy_consistency        # added at Pass 1 LOCK 2026-05-18
  - gate_dsl_schema_check            # added at Pass 1 LOCK 2026-05-18
  - no_gold_standard_label_remaining # added at Pass 1 LOCK 2026-05-18 (promoted from Pass-0 recommendation)
```

Each item is machine-checkable. Validators live under `pipeline/funder_intelligence/_validators/`. Pass 1 ships the first four cheap validators; the remaining items (artifact-id-vs-filename, lifecycle-status-valid, paren-list-list-items, P0-without-source-required) are scoped for separate dispatch with explicit acceptance criteria recorded in the Pass-1 improvements log.

---

## Discipline 8 — Honest Lifecycle Labels

The phrase "gold-standard draft" is retired from charter status fields. It described aspiration, not validation status, and it inflated the runtime trust that downstream consumers placed in unvalidated charters.

**Pre-corpus / hypothesis state:**

```yaml
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0
```

**Post Pillar-2 source-lock state** (after the source artifact has been ingested, citations verified, and operator has attested):

```yaml
validation_status: source_backed
runtime_load_status: eligible_for_runtime_test
operator_label: gold_standard_candidate
```

The phrase `gold_standard_candidate` denotes readiness for runtime evaluation, not certification. A charter only earns a non-candidate `gold_standard` label after it has survived at least one full grant cycle in submission_mode with operator sign-off.

---

## Discipline 9 — Improvements-Log Format

Each pass writes one improvements-log entry. The log lives at `pipeline/funder_intelligence/_audits/pass_<N>_<specialist>_<YYYY-MM-DD>.md` and answers exactly five questions in this order:

1. **What patterns did the specialist notice?** Cross-charter regularities, including false patterns that turned out to be coincidence.
2. **What systemic fixes were applied (vs per-charter)?** Distinguish pattern fixes (touched ≥ 2 charters) from per-charter fixes (touched 1).
3. **What new validators were added?** Per Discipline 5, pattern fixes require recurrence guards. List each guard added and the test that exercises it.
4. **What was deferred to operator review?** Every `[NEEDED]` placeholder, every demotion, every conflict between source and prior charter content.
5. **What conjecture was flagged for Pillar-2 promotion?** Claims that look promising but lack source backing; queued for verification when the source artifact ingest reaches them.

The log entry ends with the validation-checklist results from Discipline 7 and the operator approval signature line (left blank until operator signs).

---

## Cross-References

* Canonical reference doc: [`FID_CANONICAL_REFERENCE_2026-05-18.md`](./FID_CANONICAL_REFERENCE_2026-05-18.md)
* Pillar-1 charter set: [PR #33 — FID Pillar-1 charters](https://github.com/FIT-Farms/GoldenQuill/pull/33)
* Charter directory: `pipeline/funder_intelligence/pillar_1_charters/`
* Charter template: `pipeline/funder_intelligence/_templates/depth_charter_template.md`
* Validator scripts (per Discipline 7): `pipeline/funder_intelligence/_validators/`
* Audit log directory: `pipeline/funder_intelligence/_audits/`
* Mistakes log (running): `docs/FID_MISTAKES_LOG_2026-05-18.md`

---

## Footer

**Status:** canonical methodology. All FID refinement passes must obey these nine disciplines. Deviations require source-backed justification logged in the affected pass's improvements log and operator approval before merge.

**Authored:** 2026-05-18.
**Pass-1 amendment:** Discipline 3a added 2026-05-18 (Pass 1 / Logician).
