---
title: §4 v2.7.1 Targeted Amendment — Uploader attachment family (companion-LOCK with §12 v1.1)
parent: pipeline/blueprint/v0.1/section_04_logician.md (v2.1 LOCKED 2026-04-19)
predecessor_amendment: pipeline/blueprint/v0.1/section_04_v2_x_uploader_gates_amendment.md (§4 v2.7 SCOPING DRAFT 2026-05-09 — Path C reconciliation)
companion_blueprint: pipeline/blueprint/v0.1/section_12_uploader.md (§12 v1.1 — UNAUTHORED at filing time)
companion_index: pipeline/blueprint/v0.1/section_00_5_section_12_uploader.json (§0.5 v9; §0.5 v10 will add the 6 attachment rows on §12 v1.1 lock)
amendment_version: v2.7.1
status: SCOPING DRAFT 2026-05-09 — companion-LOCKs with §12 v1.1 per §6.17 Option-B
filed_by: Cowork Opus 4.7 (Path C reconciliation pass — companion-stub author)
ws_slice: WS-F (§12 Uploader paired slice; v1.1 horizon — out of v0.1 first-cut scope)
discipline: L-005 two-audit + cross-family rigor when §12 v1.1 dispatches; F-INDEX-STALE PRE-gate; Five Laws (Laws 1, 2, 3, 4, 5)
draft_date: 2026-05-09
operator: Josh
architecture_ref: v7 A1-A12 LOCKED 2026-04-19; v7.0.6 amendment (Uploader v0.1 support agent); v7.0.7 amendment (classification-driven routing)
companion_code:
  - pipeline/logician/gates/f_uploader_attachment_tampered.py                     (NEW at v1.1 LOCK — PRE)
  - pipeline/logician/gates/f_uploader_attachment_missing.py                      (NEW at v1.1 LOCK — PRE)
  - pipeline/logician/gates/f_uploader_attachment_admin_risk_unflagged.py         (NEW at v1.1 LOCK — POST)
companion_tests:
  - tests/logician/gates/test_f_uploader_attachment_tampered.py
  - tests/logician/gates/test_f_uploader_attachment_missing.py
  - tests/logician/gates/test_f_uploader_attachment_admin_risk_unflagged.py
deferred_from: §4 v2.7 (path-C narrowing 2026-05-09)
deferred_reason: §12 v1 path-b decision per §OQ-12.6 — `attachments` field NOT present on `uploader.input.v1`; AttachmentRef schema, hash-continuity flow, manual_attach_to_do checklist semantics, foundation-portal manual-attach UX all pending §12 v1.1 spec authoring round.
companion_lock_pairing: This amendment is a companion-LOCK transaction with the §12 v1.1 LOCK ceremony. v1.1 attachment-spec authoring + §0.5 v10 row authoring + this §4 amendment LOCK + Logician gate predicates ship as a single atomic LOCK group, gated on cross-family Thesis pass.
---

# §4 v2.7.1 Targeted Amendment — Uploader attachment family (companion-LOCK with §12 v1.1)

## Status

**SCOPING DRAFT 2026-05-09 — companion-LOCKs with §12 v1.1 per §6.17 Option-B.**

This amendment is a placeholder filed at the moment §4 v2.7 narrowed its
scope to v1 (Path C reconciliation 2026-05-09). It registers the six
attachment-family primitives that were excised from §4 v2.7 to match the
§12 v1 path-b deferral of attachments. None of the predicates, tests, or
§0.5 rows are authored at this filing — the amendment activates and
populates only when §12 v1.1 dispatches its attachment-spec authoring
round (`AttachmentRef` schema, hash-continuity flow, manual-attach
semantics, foundation-portal manual-attach UX), at which point the §0.5
v10 authoring round adds the corresponding rows and this amendment's
predicate / test files / Thesis Round-1 are dispatched.

**Do not LOCK this amendment in isolation.** It companion-LOCKs atomically
with `pipeline/blueprint/v0.1/section_12_uploader.md` v1.1 + the §0.5 v10
amendment that adds the attachment rows.

---

## Scope

When §12 v1.1 ships, this amendment will register six Uploader-attachment
gates as Logician PRE/POST checks:

- **Three failure codes** added to §6 (PRE: ATTACHMENT-TAMPERED, ATTACHMENT-MISSING; POST: ATTACHMENT-ADMIN-RISK-UNFLAGGED).
- **§4.5 PRE-gate row additions** (extends the §4 v2.7 PRE-29…PRE-35 sequence with two new rows; numbering pinned at v1.1 LOCK).
- **§4.6 POST-gate row additions** (extends the §4 v2.7 POST-17…POST-19 sequence with one new row; numbering pinned at v1.1 LOCK).
- **§11 Law-map additions** (Law 5 attachment-substance for the two PRE attachment gates; Law 4 admin-risk for the POST attachment-admin-risk gate).
- **§0.5 paired-commit row citations** — six rows total: 3 failure-code rows + 3 per-gate-check rows (or consolidated per the §4 v2.2 pattern that v2.7 used for its `input_invariants` PRE; consolidation choice pinned at v1.1 Thesis).

No existing §4.1–§4.18 (v2.7) content modified. Surgical addition.

---

## Six deferred primitives (canonical IDs reserved at this filing)

The six §0.5 v10 row IDs reserved by this amendment for the attachment
family. These are CANONICAL TARGETS — the §0.5 v10 amendment that adds
them must use exactly these primitive_ids so §4 v2.7.1 row-citations
resolve cleanly at v1.1 LOCK:

### Failure codes (3)

| Primitive ID | Tier | Prerequisite §12 v1.1 schema |
|---|---|---|
| `uploader.failure_code.F-UPLOADER-ATTACHMENT-TAMPERED.v1` | PRE | `AttachmentRef.content_sha3_512` (hash-continuity field) |
| `uploader.failure_code.F-UPLOADER-ATTACHMENT-MISSING.v1` | PRE | `AttachmentRef.file_path` (file-existence field) |
| `uploader.failure_code.F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED.v1` | POST | Admin-risk register surface ready in v1.1 |

### Per-gate checks (3)

| Primitive ID | Kind | Backing failure code |
|---|---|---|
| `uploader.pre_gate.attachment_existence.v1` | pre-gate-check | F-UPLOADER-ATTACHMENT-MISSING |
| `uploader.pre_gate.attachment_integrity.v1` | pre-gate-check | F-UPLOADER-ATTACHMENT-TAMPERED |
| `uploader.post_gate.attachment_admin_risk.v1` | post-gate-check | F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED |

(Consolidation alternative: at v1.1 Thesis, the two PRE attachment-checks
may be consolidated into a single `uploader.pre_gate.attachment_invariants.v1`
callable per the §4 v2.2 pattern — depends on operator preference at
companion-LOCK. The failure-code-row layer remains 3 distinct rows for
audit-trail clarity per §12.9.5 explode-pattern precedent.)

---

## Pre-LOCK gates (must clear before this amendment activates)

1. **§12 v1.1 SCOPING DRAFT filed** — `AttachmentRef` schema, hash-continuity
   flow, `manual_attach_to_do` checklist semantics, foundation-portal
   manual-attach UX all specified.
2. **§0.5 v10 SCOPING DRAFT filed** — adds the 6 reserved primitive_ids as
   v10 amendment rows.
3. **WS-F Audit #1 cross-family Thesis** dispatches against the post-stitch
   v1.1 artifact set (§12 v1.1 + §0.5 v10 + this amendment + Logician
   predicate scaffolding + tests).
4. **WS-F Audit #2 verification** — L-005 two-audit cycle.
5. **§12 v1 + §4 v2.7 already LOCKED** (v1 LOCK is a precondition; v1.1
   builds on v1).

---

## Path-C provenance

Filed 2026-05-09 by the Cowork Opus 4.7 surgical-edit pass that landed
Path C against the §4 v2.7 ↔ §0.5 v9 re-convergence surface
(`pipeline/blueprint/v0.1/section_04_v2_7_unresolved_primitives_2026-05-09.md`).
Path C: narrow §4 v2.7 to v1-scope; defer attachment family to companion
§4 v2.7.1 amendment that LOCKs with §12 v1.1; preserves Cowork pre-fix
path-b decision; preserves §12.9.5 explode-pattern precedent; smallest
blast radius.

The six excised primitives are surfaced in the §4 v2.7 row-citation block
under `### v2.7.1 horizon stub — attachment family deferred to §12 v1.1`
to keep the deferral visible to Audit #1 reviewers without tripping
F-INDEX-STALE against §0.5 v9.

---

## What this amendment does NOT do at filing time

- Does NOT author predicate code (`f_uploader_attachment_*.py`) — pending §12 v1.1 spec round.
- Does NOT author tests — pending predicate code.
- Does NOT author §0.5 v10 rows — pending §12 v1.1 SCOPING DRAFT.
- Does NOT activate any Logician gate — runtime engagement begins only at companion-LOCK with §12 v1.1.
- Does NOT block §4 v2.7 LOCK — they are independent LOCK transactions.
- Does NOT extend the v0.1 first-cut surface — v1.1 is a horizon.

---

## Filing artifacts

- This file: `pipeline/blueprint/v0.1/section_04_v2_7_1_attachment_family_amendment.md` (NEW — companion-lock placeholder).
- §4 v2.7 amendment row-citation block updated with `### v2.7.1 horizon stub` subsection pointing here.
- Daily log: `daily_logs/2026-05-09.md` — Path C closeout entry references this amendment.
- Session metrics: `pipeline/metrics/session_log.jsonl` — single line.

---

## Re-engagement criteria

Activate this amendment (move from SCOPING DRAFT placeholder to authored
SCOPING DRAFT) when:

- §12 v1 has LOCKED (precondition).
- §12 v1.1 spec authoring round is dispatched and `AttachmentRef` schema
  + hash-continuity flow + `manual_attach_to_do` semantics are specified.
- §0.5 v10 amendment is dispatched against the 6 reserved primitive_ids
  in this file.

When those preconditions clear, dispatch a Code or Cowork session against
this file with the prompt: "Author the predicates / tests / §4 row tables
/ §11 Law-map / §0.5 row citations for the six attachment primitives
reserved at SCOPING DRAFT 2026-05-09."

---

## L-005 Audit record (pending companion-LOCK with §12 v1.1)

Not yet dispatched. Audit #1 fires when §12 v1.1 + §0.5 v10 + this
amendment + Logician scaffolding are all post-author. Cross-family roster
per WS-B per dispatch plan.
