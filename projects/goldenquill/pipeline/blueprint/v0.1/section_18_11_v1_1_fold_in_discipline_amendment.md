---
title: Blueprint §18.11 — Amendment v1.1 (Phase 4 fold-in discipline checklist — documentation-only, encodes Wave 2 close synthesis §CC-4)
filed: 2026-05-16
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-17T04:34:50Z — self-LOCK per documentation-only carve-out (§11 v1.1 + §18 v1.1 narrow-corrective precedent). Operator authorized; no L-005 Thesis dispatched. lock_history rows 269 (§18 main file post-OD-D supersession), 270 (this amendment), 271 (§0.5 v30 paired-commit) appended atomically at the same `lock_timestamp_utc`. Audit trail at `pipeline/handoffs/od_d_completion_2026-05-16.md` substitutes for the formal Thesis audit row.
parent_lock: pipeline/blueprint/v0.1/section_18_card_system.md  (§18 v1 — paired with architecture v7.0.11 + §4 v2.x card-hardening + §0.5 v25; cards Wave 2 LOCKED 2026-05-16T16:00:00Z at lock_history row 262)
parent_lock_chain:
  - pipeline/blueprint/v0.1/section_18_v1_1_amendment.md   # §18 v1.1 LOCKED 2026-05-16 — narrow-corrective Wave 1 schema refinement
  - pipeline/blueprint/v0.1/section_18_v1_2_amendment.md   # §18 v1.2 LOCKED 2026-05-16T14:00:00Z — funder_political_axis retirement
  - pipeline/blueprint/v0.1/section_00_5_cards_wave_2_amendment.md  # §0.5 v29 LOCKED 2026-05-16T16:00:00Z row 262 — Wave 2 signature_status flip
companion_lock: pipeline/blueprint/v0.1/section_00_5_section_18_11_v1_1_amendment.md  # §0.5 v30 paired-commit — ONE marker row only (section anchor blueprint.section_anchor.s18_11_v1_1.v1)
amendment_class: documentation-only (Wave 2 close-synthesis fold-in to Phase 4 self-validation checklist)
precedent_pattern: §18 v1.1 narrow-corrective LOCKed at row 565 (2026-05-16) — both amendments extend the §18 surface without modifying §18 v1 architectural decisions. v1.1 fold-in-discipline is narrower than §18 v1.1 (no schema delta; no card patches; no prose-vs-schema reconciliation; pure Phase 4 self-validation checklist text addition).
threat_severity_at_v0_1_v0_2: LOW — documentation-only addition. No runtime enforcement at this amendment; the discipline is operator-author-facing during Wave 3+ card research-write cycles. The runtime enforcement layer (F-CARDS-COUPLING-VIOLATION-EXTENSION + F-CARDS-SCHEMA-INVALID + the seven F-CARDS-* gates registered at §0.5 v25 rows 556-562) is unchanged.
purpose: Encode the Wave 2 close-synthesis §CC-4 lesson statement as a §18.11 Phase 4 self-validation checklist so Wave 3+ card-research authors hit the four refusals pre-Cycle-2 — reducing Cycle 2 NEW-defect-from-Cycle-1-fold churn observed across 6-of-8 Wave 2 cards.
companion_code_landed: NONE — documentation-only. No on-disk module changes; no schema delta; no test surface delta.
companion_tests_landed: NONE — documentation-only. Existing tests at `tests/cards/` (per §18.4 directory layout) continue to pass unchanged. The checklist is author-facing prose; no predicate body reads it.
done_definition:
  - "§18.11 Phase 4 of `pipeline/blueprint/v0.1/section_18_card_system.md` carries the four-refusal checklist + discipline rationale + comment-block-only fallback paragraph in canonical text."
  - "This amendment file documents the addition, the parent-lock chain, the source synthesis pointer (Wave 2 §CC-4), and the precedent pattern (§18 v1.1 narrow-corrective)."
  - "Companion §0.5 v30 paired-commit (`section_00_5_section_18_11_v1_1_amendment.md`) registers ONE marker row anchoring this v1.1 amendment file: primitive_id = `blueprint.section_anchor.s18_11_v1_1.v1`, kind = `marker`, seat_owner = `cards`, stability_tier = `STABLE`."
  - "No new schema rows; no new failure-code rows; no new vocabulary kinds; no new AST-lint rules."
cowork_thesis_dispatch_status: OPTIONAL at operator discretion — documentation-only minor amendment with zero runtime enforcement teeth. If operator dispatches L-005 Thesis, model on `pipeline/validation/section_18_v1_1_thesis_2026-05-15/` (narrow-corrective precedent). If operator elects self-LOCK per documentation-only carve-out, audit trail at `pipeline/handoffs/od_d_completion_2026-05-16.md` (this OD-D hand-back) substitutes for the formal Thesis audit row.
session_metrics: pipeline/metrics/session_log.jsonl
od_d_handoff: pipeline/handoffs/od_d_fold_in_discipline_checklist_2026-05-16.md
od_d_completion: pipeline/handoffs/od_d_completion_2026-05-16.md
---

# Amendment v1.1 — §18.11 Phase 4 fold-in discipline checklist (documentation-only, Wave 2 §CC-4 fold-in)

## §0. Amendment intent + scope

This documentation-only amendment **adds** (does **not** replace) a fold-in discipline checklist to the §18.11 Phase 4 self-validation section. The checklist encodes the Wave 2 close-synthesis §CC-4 lesson statement so Wave 3+ card-research authors hit the four refusals pre-Cycle-2, reducing Cycle 2 NEW-defect-from-Cycle-1-fold churn.

The amendment does NOT:

- Modify §18 v1 / v1.1 / v1.2 architectural decisions on the Card System.
- Add new failure-code primitives at §0.5 (the runtime enforcement layer is unchanged — the seven F-CARDS-* gates registered at §0.5 v25 rows 556-562 carry the existing predicate signatures).
- Add new AST-lint rules at §0.5.
- Introduce new vocabulary kinds at §0.5.
- Modify the CIC / CLC JSON schemas.
- Patch any existing card on disk.

The amendment composes against §18 v1 LOCK + §18 v1.1 LOCK + §18 v1.2 LOCK + cards Wave 2 LOCK ceremony (lock_history row 262, 2026-05-16T16:00:00Z) + §0.5 v29.

## §1. Source — Wave 2 close synthesis §CC-4

Verbatim source pointer: `pipeline/validation/cards_wave_2_thesis_2026-05-15/WAVE_2_CLOSE_SYNTHESIS.md` §CC-4 ("Cycle 2 NEW-defect-from-Cycle-1-fold pattern"). Lesson statement reproduced verbatim:

> Fold-in discipline = prose-only inside existing canonical §18.5 / §18.6 fields. Refuse: (a) structured-sub-field expansions on canonical entries; (b) dedicated-field-name forks; (c) compound enum values; (d) literal CIC/CLC slug strings.

Wave 2 evidence count: 6-of-8 Wave 2 cards (CIC-05 cooperative + CLC-02 catalytic_change + CLC-04 research_evidence + CLC-05 market_access + CLC-07 sponsorship_corporate + Wave 1 food_systems carried the same defect class in its own Cycle 2) surfaced NEW P0 / HIGH defects in Cycle 2 introduced by Cycle 1 FOLD-IN edits. CLC-06 credit_underwriting + CLC-08 shared_assets broke the streak by using comment-block-only fold-in discipline + refusal of structured-sub-field expansions — they are the on-disk precedents for the comment-block-only fallback paragraph appended at §18.11 Phase 4.

## §2. Schema/prose delta applied at this amendment

One delta — additive only — at `pipeline/blueprint/v0.1/section_18_card_system.md` §18.11 Phase 4. The pre-existing Phase 4 sentence ("Before review, each draft card must pass: schema completeness check, source/provenance completeness check, no hardcoded CIC × CLC eligibility coupling, no private customer data, no unsourced numeric win-rate claims, no unsupported program claims, no excessive copied source text, no production load if unsigned.") is preserved verbatim. The amendment appends:

1. **Fold-in discipline checklist header** — one paragraph naming the four refusals as Cycle-1-to-Cycle-2 author discipline.
2. **Four numbered refusals** — one per defect class (structured-sub-field expansions; dedicated-field-name forks; compound enum values; literal CIC/CLC slug strings). Each refusal: defect statement + on-disk citation precedent + prose-only remediation.
3. **Discipline rationale** — one paragraph summarizing Wave 2 §CC-4 evidence count + the CLC-06 / CLC-08 streak-breaker pattern.
4. **Comment-block-only fallback paragraph** — one paragraph describing the YAML-comment fold-in pattern that CLC-06 + CLC-08 used at Wave 2 to avoid the four defect classes when a Cycle 1 fold-in proposal cannot be expressed within the existing canonical schema. Routes structural gaps to the card's `_review_handback` operator-decision queue + defers in-data application to a future §18 v1.x amendment.

No other §18 prose section modified. No §18.5 / §18.6 schema-example block modified. No §18.12 / §18.13 / §18.14 / §18.15 / §18.16 prose modified.

## §3. Composition with §18 v1 / v1.1 / v1.2 + Wave 2 LOCK ceremony

This v1.1 amendment composes against:

- **§18 v1** (architecture v7.0.11 + §4 v2.x card-hardening + §0.5 v25 compound LOCK) — unchanged. Phase 4 sentence preserved verbatim above the appended checklist.
- **§18 v1.1** (Wave 1 schema refinement + prose-vs-schema reconciliation, LOCKED 2026-05-16 row 565) — unchanged. The frequency_observed + provenance_requirements + dialect_routing_table item-shape extensions stay; the Phase 4 checklist is orthogonal to those schema deltas.
- **§18 v1.2** (funder_political_axis retirement, LOCKED 2026-05-16T14:00:00Z) — unchanged. The dialect_routing_table item-property-set change (drop funder_political_axis; add clc + register_description + example_program) stays; the Phase 4 checklist is orthogonal.
- **Cards Wave 2 LOCK ceremony** (12-card signature_status flip + §0.5 v29 paired-commit, LOCKED 2026-05-16T16:00:00Z at lock_history row 262) — unchanged. The 12 Wave 2 card signature_status fields carry through; the Phase 4 checklist is forward-looking discipline for Wave 3+ cards.

Future §18 v1.x amendments that introduce new schema fields or structural primitives MUST route through the standard §18 v1.x + §0.5 paired-commit pattern — they MUST NOT smuggle structural changes through the Phase 4 fold-in discipline checklist (the checklist is enforcement-against, not enforcement-for-new-structure).

## §4. AST-lint + Logician + tests impact

**AST-lint.** Zero new rules at this amendment. `R-CARDS-NO-COUPLING-FIELD` continues to scan unchanged glob (`pipeline/cards/CIC/**.yaml` + `pipeline/cards/CLC/**.yaml`) and returns 0 findings on Wave 2 LOCKED cards. The checklist is author-facing prose; no AST-lint predicate body reads it.

**Logician F-CARDS-* family.** Zero new failure-code primitives at this amendment. The seven F-CARDS-* gates registered at §0.5 v25 rows 556-562 carry unchanged predicate signatures. Specifically:

- `F-CARDS-SCHEMA-INVALID` continues to call jsonschema Draft202012 validation against the schema files — refusal (a) "structured-sub-field expansions" and refusal (b) "dedicated-field-name forks" both surface as schema invalidations at this gate when they smuggle in via Cycle 1 fold-in.
- `F-CARDS-COUPLING-VIOLATION-EXTENSION` predicate body (NotImplementedError at v0.1 Beta; LIVE at v0.2 first wave) reads card fields for literal CIC/CLC slug strings in ANY value position — refusal (d) "literal CIC/CLC slug strings" hardens at this gate per §CC-3 / OD-C (separate operator-dispatch item).
- Refusal (c) "compound enum values" hardens at the future `F-CARDS-ENUM-NON-CANONICAL` gate per §CC-2 / OD-B (separate operator-dispatch item) — pre-OD-B, the §18.5 / §18.6 schema item shapes carry the canonical enum sets (`HIGH | MEDIUM | LOW` severity, `FREQUENT | OCCASIONAL | RARE | UNKNOWN` frequency) and `F-CARDS-SCHEMA-INVALID` catches compound values as schema-invalid at load time.

**Tests.** Zero new test files at this amendment. Existing tests at `tests/cards/` continue to pass unchanged.

## §5. §0.5 paired-commit (one marker row only)

**§0.5 v30 paired-commit amendment** (`pipeline/blueprint/v0.1/section_00_5_section_18_11_v1_1_amendment.md`) registers ONE marker row anchoring this §18.11 v1.1 amendment file at the §0.5 Interface Index:

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | seat_owner | stability_tier |
|---|---|---|---|---|---|---|---|
| `<resolved_at_LOCK>` | `blueprint.section_anchor.s18_11_v1_1.v1` | `pipeline/blueprint/v0.1/section_18_11_v1_1_fold_in_discipline_amendment.md` | §18.11 v1.1 | `<resolved_at_LOCK>` | marker | cards | STABLE |

No new schema rows. No new failure-code rows. No new AST-lint rows. No new vocabulary kinds. The single `kind` value used — `marker` — appears in the v5 + v6 + v17-v19 closed vocabulary.

Row delta:

- Runtime-live total at §0.5 v29 LOCK (cards Wave 2 paired-commit, lock_history row 262, 2026-05-16T16:00:00Z): unchanged at v29 (signature_status flip only; no new rows).
- This amendment adds 1 marker row.
- New runtime-live total at compound LOCK: **previous + 1**.

The exact row number resolves at LOCK ceremony relative to any intervening §0.5 amendments. Per documentation-only carve-out, this amendment MAY self-LOCK if operator confirms (a) the Wave 2 §CC-4 source text is authoritative and (b) the four refusals reproduce the source faithfully.

## §6. v1.x amendment-realization checklist (forward-binding contracts)

Two contracts forward-bind from this amendment to future amendments:

```
[ ] OD-B realization (separate operator-dispatch item). When the AST-lint
    rule R-CARDS-ENUM-CANONICAL + Logician PRE-gate
    F-CARDS-ENUM-NON-CANONICAL land, refusal (c) "compound enum values"
    promotes from author-facing prose discipline to runtime-enforced
    schema gate. Update §18.11 Phase 4 checklist refusal (c) to cross-
    reference the new gate failure-code. Owner: the operator-dispatched
    OD-B Wave-3-LOCK-or-§18-v1.3 amendment.

[ ] OD-C realization (separate operator-dispatch item). When the
    F-CARDS-COUPLING-VIOLATION-EXTENSION pattern-coverage hardening
    lands (extended regex coverage on any field value, not just
    designated coupling-fields), refusal (d) "literal CIC/CLC slug
    strings" promotes from author-facing prose discipline to runtime-
    enforced regex gate. Update §18.11 Phase 4 checklist refusal (d) to
    cross-reference the hardened gate. Owner: the operator-dispatched
    OD-C amendment.
```

These contracts are documentation-only forward-binders — they do not block this v1.1 amendment LOCK; they direct future amendment authors to update the Phase 4 checklist cross-references when the corresponding runtime enforcement layers land.

## §7. Cross-references

- Source synthesis: `pipeline/validation/cards_wave_2_thesis_2026-05-15/WAVE_2_CLOSE_SYNTHESIS.md` §CC-4.
- OD-D handoff brief: `pipeline/handoffs/od_d_fold_in_discipline_checklist_2026-05-16.md`.
- OD-D completion hand-back: `pipeline/handoffs/od_d_completion_2026-05-16.md`.
- Parent §18 v1 LOCK: `pipeline/blueprint/v0.1/section_18_card_system.md` (paired with architecture v7.0.11 + §4 v2.x card-hardening + §0.5 v25).
- Sibling §18 v1.1 LOCK: `pipeline/blueprint/v0.1/section_18_v1_1_amendment.md` (LOCKED 2026-05-16 row 565).
- Sibling §18 v1.2 LOCK: `pipeline/blueprint/v0.1/section_18_v1_2_amendment.md` (LOCKED 2026-05-16T14:00:00Z).
- Cards Wave 2 LOCK ceremony: `pipeline/blueprint/v0.1/section_00_5_cards_wave_2_amendment.md` (§0.5 v29, LOCKED 2026-05-16T16:00:00Z row 262).
- Companion §0.5 v30 amendment: `pipeline/blueprint/v0.1/section_00_5_section_18_11_v1_1_amendment.md`.
- Comment-block-only on-disk precedents: `pipeline/cards/CLC/credit_underwriting.yaml` + `pipeline/cards/CLC/shared_assets.yaml` (Wave 2 CLC-06 + CLC-08 streak-breakers per §CC-4).
- Narrow-corrective precedent: §18 v1.1 + §0.5 v26 paired-commit (LOCKED 2026-05-16 row 565). §11 v1.1 + §0.5 v19 paired-commit (lock_history rows 209/210, 2026-05-11). §4 v2.x.1 + §0.5 v16 paired-commit (lock_history rows 198/199, 2026-05-10).
- OD-B / OD-C forward-binding operator-dispatch items: see Wave 2 close synthesis §CC-2 + §CC-3 operator-decision queue.
