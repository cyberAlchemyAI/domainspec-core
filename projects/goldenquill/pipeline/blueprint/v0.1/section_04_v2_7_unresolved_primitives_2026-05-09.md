---
title: §4 v2.7 ↔ §0.5 v9 Re-convergence — Unresolved Primitives Surface
authored: 2026-05-09
authored_by: Cowork Opus 4.7 (re-convergence patch session)
parent_amendment: pipeline/blueprint/v0.1/section_04_v2_x_uploader_gates_amendment.md (§4 v2.7 SCOPING DRAFT 2026-05-09)
sister_amendment: pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md (§0.5 v9 SCOPING DRAFT 2026-05-09)
sister_json: pipeline/blueprint/v0.1/section_00_5_section_12_uploader.json (21 rows, index_version v9)
status: HAND-BACK to dispatch coordinator. WS-F Audit #1 BLOCKED until structural reconciliation lands.
context: WS-F three-session pre-fix. Cowork (§12 + §0.5) chose path-b — defer attachments to v1.1, consolidate PRE-checks per §4 v2.2 pattern. Code session (§4 v2.7) authored before path-b landed; expects 26-row per-gate explode. Find/replace stitch cannot bridge — coordinator decision required.
done_per_task: Step 5 ("do not invent — flag the missing primitive in the daily_log entry and hand back to coordinator with the unresolved list").
---

# §4 v2.7 ↔ §0.5 v9 Re-convergence — Unresolved Primitives Surface

## Summary

The §12 + §0.5 Cowork pre-fix delivered 21 amendment rows (1 marker + 4 schema/contract + 10 failure-code + 3 pre-gate-check + 3 post-gate-check). The §4 v2.7 amendment was authored expecting **26 per-gate explode rows** (13 failure-code + 13 per-gate pre-/post-check). The 5-row delta arises from two structural decisions the §12/§0.5 pre-fix made that the §4 pre-fix authored before:

1. **Path-b attachment deferral (§12 §OQ-12.6 + path-b recommendation).** Attachments deferred to §12 v1.1; the `attachments` field is NOT present on `uploader.input.v1`. This eliminates 3 failure-code primitives and their 3 pre-/post-check primitives: `F-UPLOADER-ATTACHMENT-TAMPERED`, `F-UPLOADER-ATTACHMENT-MISSING`, `F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED`.
2. **PRE-check consolidation per §4 v2.2 pattern.** Five PRE-checks fold into a single `uploader.pre_gate.input_invariants.v1` callable per the JSON description: "Single bundle-validation check callable consolidating F-UPLOADER-RFA-MISSING, F-UPLOADER-SIGNATURE-MISSING (both sub-tags), F-UPLOADER-SIGNATURE-MISMATCH (subclass), F-UPLOADER-INPUT-INCONSISTENT, F-UPLOADER-ORG-CROSS-REF (both sub-tags)."

The §4 amendment's "Open items for Thesis" item 1 explicitly flagged this granularity choice as "Operator preference needed before LOCK." The Cowork pre-fix resolved it as v2.2-consolidated for PRE, one-per-gate for POST. The Code-session §4 amendment does not yet reflect that resolution.

Find/replace alone cannot reconcile — the structural shape of §4's row-citation tables (lines 389-428) does not match the §0.5 v9 row inventory.

## Inventory: 26 placeholders in §4 amendment vs 21 §0.5 v9 rows

26 placeholders break down as:
- 13 failure-code placeholders (lines 393-405)
- 9 PRE-gate-check placeholders (lines 411-419)
- 4 POST-gate-check placeholders (lines 420-423)

21 §0.5 v9 rows break down as:
- 1 marker (`blueprint.section_anchor.s12_uploader.v1`)
- 4 schema/contract (input.v1, output.v1, readiness_checklist.v1, portal_adapter_protocol.v1)
- 10 failure-code (`uploader.failure_code.F-UPLOADER-*.v1` — 10 of the 13 expected; 3 attachment-related missing)
- 3 pre-gate-check (autosubmit_structural.v1, field_map_routing.v1, input_invariants.v1 — consolidated)
- 3 post-gate-check (content_mutation.v1, format_compliance.v1, package_completeness.v1)

## Cleanly-resolvable placeholders (15 of 26)

These map 1:1 to a unique §0.5 v9 row ID:

| §4 placeholder | §0.5 v9 primitive_id |
|---|---|
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-PACKAGE-INCOMPLETE>` | `uploader.failure_code.F-UPLOADER-PACKAGE-INCOMPLETE.v1` |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-FORMAT-MISMATCH>` | `uploader.failure_code.F-UPLOADER-FORMAT-MISMATCH.v1` |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-AUTOSUBMIT-ATTEMPTED>` | `uploader.failure_code.F-UPLOADER-AUTOSUBMIT-ATTEMPTED.v1` |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-SIGNATURE-MISSING>` | `uploader.failure_code.F-UPLOADER-SIGNATURE-MISSING.v1` |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-CONTENT-MUTATION>` | `uploader.failure_code.F-UPLOADER-CONTENT-MUTATION.v1` |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-INPUT-INCONSISTENT>` | `uploader.failure_code.F-UPLOADER-INPUT-INCONSISTENT.v1` |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-RFA-MISSING>` | `uploader.failure_code.F-UPLOADER-RFA-MISSING.v1` |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-SIGNATURE-MISMATCH>` | `uploader.failure_code.F-UPLOADER-SIGNATURE-MISMATCH.v1` |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-ORG-CROSS-REF>` | `uploader.failure_code.F-UPLOADER-ORG-CROSS-REF.v1` |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-FIELD-MAP-CLOUD-ROUTED>` | `uploader.failure_code.F-UPLOADER-FIELD-MAP-CLOUD-ROUTED.v1` |
| `<§0.5_ROW_ID_PENDING:pre-gate-check:F-UPLOADER-AUTOSUBMIT-ATTEMPTED>` | `uploader.pre_gate.autosubmit_structural.v1` |
| `<§0.5_ROW_ID_PENDING:pre-gate-check:F-UPLOADER-FIELD-MAP-CLOUD-ROUTED>` | `uploader.pre_gate.field_map_routing.v1` |
| `<§0.5_ROW_ID_PENDING:post-gate-check:F-UPLOADER-PACKAGE-INCOMPLETE>` | `uploader.post_gate.package_completeness.v1` |
| `<§0.5_ROW_ID_PENDING:post-gate-check:F-UPLOADER-FORMAT-MISMATCH>` | `uploader.post_gate.format_compliance.v1` |
| `<§0.5_ROW_ID_PENDING:post-gate-check:F-UPLOADER-CONTENT-MUTATION>` | `uploader.post_gate.content_mutation.v1` |

These 15 are not at issue. Coordinator can stitch via straight find/replace once the structural decisions on the other 11 are made.

## Many-to-one (consolidation-pattern) placeholders (5 of 26)

Five PRE-check placeholders map to ONE consolidated row per §0.5 v9's design — but the §4 amendment's row-citation table still lists them as 5 distinct rows:

| §4 placeholder | §0.5 v9 primitive_id (shared) | Resolution |
|---|---|---|
| `<§0.5_ROW_ID_PENDING:pre-gate-check:F-UPLOADER-RFA-MISSING>` | `uploader.pre_gate.input_invariants.v1` | many→one |
| `<§0.5_ROW_ID_PENDING:pre-gate-check:F-UPLOADER-SIGNATURE-MISSING>` | `uploader.pre_gate.input_invariants.v1` | many→one |
| `<§0.5_ROW_ID_PENDING:pre-gate-check:F-UPLOADER-SIGNATURE-MISMATCH>` | `uploader.pre_gate.input_invariants.v1` | many→one |
| `<§0.5_ROW_ID_PENDING:pre-gate-check:F-UPLOADER-INPUT-INCONSISTENT>` | `uploader.pre_gate.input_invariants.v1` | many→one |
| `<§0.5_ROW_ID_PENDING:pre-gate-check:F-UPLOADER-ORG-CROSS-REF>` | `uploader.pre_gate.input_invariants.v1` | many→one |

**Coordinator question:** does §4 keep the 5-row table with all rows pointing to the same primitive (audit-trail-clarity rationale per §12.9.5 explode-pattern precedent), or collapse to a single row with a multi-failure-code annotation? The §4 v2.7 "Open items for Thesis" item 1 was the placeholder for this decision; Cowork resolved it for §0.5 but §4's table shape was not back-propagated.

## Unresolvable placeholders (6 of 26 — attachment-related, path-b-deferred)

These have NO corresponding §0.5 v9 row because attachments are deferred to v1.1:

| §4 placeholder | Reason no JSON row |
|---|---|
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-ATTACHMENT-TAMPERED>` | Attachments deferred per `uploader.input.v1` ("attachments field NOT present at v1 per §12.6 deferral") |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-ATTACHMENT-MISSING>` | Attachments deferred (same) |
| `<§0.5_ROW_ID_PENDING:F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED>` | Attachments deferred (same; v1.1 horizon row not authored at v1 LOCK) |
| `<§0.5_ROW_ID_PENDING:pre-gate-check:F-UPLOADER-ATTACHMENT-MISSING>` | Attachments deferred |
| `<§0.5_ROW_ID_PENDING:pre-gate-check:F-UPLOADER-ATTACHMENT-TAMPERED>` | Attachments deferred |
| `<§0.5_ROW_ID_PENDING:post-gate-check:F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED>` | Attachments deferred |

The §4 v2.7 amendment authored these gates with the assumption attachments would land at v1. The path-b deferral (recommended in the §12 dispatch brief itself, ratified by Cowork pre-fix per `daily_logs/2026-05-09.md` line 48) eliminates them from v1 scope. The §4 amendment's references to `F-UPLOADER-ATTACHMENT-*` are now ahead of §12.

## Structural decisions surfaced for coordinator

The dispatch coordinator must pick one of these reconciliation paths before WS-F Audit #1 fires:

### Path A — Reauthor §4 v2.7 to match §12 v1 / §0.5 v9 reality (SMALL)

- Drop §4.18 secondary-family rows for ATTACHMENT-TAMPERED, ATTACHMENT-MISSING, ATTACHMENT-ADMIN-RISK-UNFLAGGED.
- Drop PRE-34, PRE-35, POST-20 from row tables (reduce to 7 PRE + 3 POST = 10 base + 1 Cowork-slice each = 11 total).
- Drop §6 entries for the three attachment failure codes.
- Drop §11 Law-map rows for ATTACHMENT-MISSING/TAMPERED/ADMIN-RISK-UNFLAGGED.
- Drop attachment companion gate files / tests from front-matter.
- Collapse 5 PRE-check citations to single `input_invariants` consolidated row in §0.5 row-citation table; OR keep 5 rows pointing to same primitive ID (operator preference per §4 "Open items" 1).
- Add re-convergence note: "v2.7 narrowed to §12 v1 path-b scope; attachment family registers at v1.1 LOCK."

**Implication:** §4 v2.7 ships at 10 gates (or 11 if INPUT-INVARIANTS counts as 5 separate gates folded under one check). uploader.py companion code retains attachment-related predicates IF they were already authored — they become aspirational v1.1 hooks, not load-bearing v1 gates. Audit #1 reviews narrowed scope.

### Path B — Reverse Cowork's path-b decision; expand §12 / §0.5 to path-a 26-row scope (LARGE)

- Re-author §0.5 §12 amendment + JSON to add 5 missing rows: 1 schema (`AttachmentRef.v1`), 3 failure-code (ATTACHMENT-TAMPERED/MISSING/ADMIN-RISK-UNFLAGGED), 1 attachment composition pre-gate-check + 1 attachment admin-risk post-gate-check.
- Explode `input_invariants.v1` consolidated row into 5 distinct PRE-check rows (RFA-MISSING, SIGNATURE-MISSING, SIGNATURE-MISMATCH, INPUT-INCONSISTENT, ORG-CROSS-REF).
- Re-author §12 v1 blueprint to specify `AttachmentRef` schema + attachment validation flow.
- Total rows: 211 + 26 = 237 runtime-live (vs current 232).

**Implication:** Reverses an explicit Cowork pre-fix design decision. §12 LOCK delayed by attachment-spec authoring round (per §12.6 §OQ-12.6 deferral, this was non-trivial — `AttachmentRef` schema, hash-continuity flow, manual_attach_to_do checklist semantics, foundation-portal manual-attach UX all need spec). Likely adds another Thesis round on §12. WS-F timeline pushes further.

### Path C — Hybrid (RECOMMENDED for path-of-least-perturbation)

- Keep Cowork's path-b on §12 + §0.5 (no rework).
- Narrow §4 v2.7 to v1-scope gates only (10 base + 1 Cowork-slice = 11), matching Path A surgical edits.
- Register attachment family as a SEPARATE §4 v2.7.1 amendment companion-locked to §12 v1.1 — `stability_tier=v1.1_HORIZON` rows authored now but engagement deferred.
- Collapse the 5 PRE-check citations to single `input_invariants` row with audit-trail-clarity annotation listing the 5 consolidated failure codes (preserves §12.9.5 explode-pattern precedent).

**Implication:** Smallest blast radius. §12 v1 LOCK proceeds unchanged. §4 v2.7 ships narrower. Attachment work re-emerges as a clean v1.1 amendment dispatch when §12 v1.1 attaches the attachment slice.

## Hand-back artifacts

- This file: `pipeline/blueprint/v0.1/section_04_v2_7_unresolved_primitives_2026-05-09.md` (NEW — surfaces unresolved list).
- §4 amendment: `pipeline/blueprint/v0.1/section_04_v2_x_uploader_gates_amendment.md` — UNCHANGED. All 26 placeholders intact pending coordinator path selection.
- Daily log: `daily_logs/2026-05-09.md` — appended hand-back entry.
- Session metrics: `pipeline/metrics/session_log.jsonl` — single line.

## What this session deliberately did NOT do

- Did not invent §0.5 row IDs for the 6 attachment placeholders (Step 5 prohibition).
- Did not silently collapse the 5 consolidated-pattern placeholders to a single row, because the §4 row-table shape change is a path A/B/C decision, not a stitch.
- Did not stitch the 15 cleanly-resolvable placeholders, because half-stitched + half-pending creates an audit-confusing mid-state for WS-F Audit #1 reviewer. Coordinator should stitch in one pass after path selection.

## Recommendation to coordinator

Path C — narrow §4 v2.7 to v1-scope, defer attachment family to v2.7.1 companion-locked with §12 v1.1. Smallest perturbation; preserves Cowork pre-fix's path-b decision; preserves §12.9.5 explode-pattern precedent for the consolidated PRE row; clean v1.1 surface for the attachment slice.

If Josh prefers Path A (drop attachment family entirely from v0.1 horizon): trivial extension of Path C — skip authoring v2.7.1.

Path B is feasible but disproportionate — it reverses a brief-recommended path-b decision over a row-count delta.

## Next dispatch needed

A scoped Code or Cowork session to apply the chosen path's §4 surgical edits, then re-fire this re-convergence patch. WS-F Audit #1 dispatch remains gated until §4 row-citation block resolves to zero `<§0.5_ROW_ID_PENDING:...>` strings.

WS-A-Review (Tier-0.5) still concurrent; not blocked by this surface.
