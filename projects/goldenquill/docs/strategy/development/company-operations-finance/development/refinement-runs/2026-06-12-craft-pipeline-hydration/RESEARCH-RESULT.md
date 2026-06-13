# Research Result - Company operations and finance

Local-first research execution of `RESEARCH-DISPATCH.json` (dispatch `gq-research-strategy-company-operations-finance-2026-06-12`). Steps r01-r06 covered. External research DEFERRED (not authorized). This file is route/planning evidence only — no canonical or lifecycle artifact was mutated.

## Node

- Craft node: `company-operations-finance` (`CTX-COF-ROOT`)
- Owns: workbook Workstream G (Company Operations)
- Research lane: company operations and finance research
- Source contract: `docs/golden-quill-task-role-breakdown-handoff.md` (`ART-COF-HANDOFF`)

## Core Question

What operating-floor evidence is needed for entity hygiene, bookkeeping, support triage, Node Care, and validation packet maintenance?

## r01 — Scope (local-evidence-reviewer)

Node scope is cleanly separable from sibling Craft nodes. Workstream G rows 77-80 of the handoff map one-to-one onto the four node gaps. Boundary checks:

- Entity hygiene / banking / bookkeeping / contracts filing / insurance (row 77) → `GAP-COF-ENTITY-HYGIENE`.
- Support channel + issue log + triage rules "support absorbs vs engineering sees" (row 78) → `GAP-COF-SUPPORT-TRIAGE`.
- Node Care delivery: updates, source-index maintenance, quarterly check-ins, vault care (row 79) → `GAP-COF-NODE-CARE-OPS`.
- Investor/funder relations + validation packet maintenance (row 80) → `GAP-COF-VALIDATION-PACKET`.

Adjacent-but-out-of-node (do NOT pull into this lane): Selling & Contracting Workstream E (deposit handling / invoicing / customer agreement / LOI — sales-contracting-legal node), White-Glove Delivery Workstream F (per-customer Day 0 / Day 60 — white-glove-delivery-node-care node), and Quality/Security Workstream C claims register (quality-security-proof node). The validation packet (G) consumes QA evidence produced in C but does not own it — cross-node dependency, not scope merge. No cross-node drift; no business-judgment question requires Josh to scope (the rows are explicit).

## r02 — Local Evidence Baseline (local-evidence-reviewer)

| Evidence class | Concrete source (path / handle) | What it grounds |
| --- | --- | --- |
| Workbook operations rows | `docs/golden-quill-task-role-breakdown-handoff.md` §1 Node on the Desk, Workstream G rows 77-80 | All four gap definitions; effort types (ONGOING; BUILD-then-ONGOING for support) |
| Workbook role map | same file §3 Roles & Gaps, rows: Bookkeeper (fractional) "Deposits, invoicing, cost tracking, investor schedules; few hrs/month at first revenue"; Customer Success "support front line, Node Care; part-time contract as deployments stack" | Ownership + onboarding triggers for ENTITY-HYGIENE, SUPPORT-TRIAGE, NODE-CARE-OPS |
| Workbook after-acceleration | same file §2 After Acceleration, "Next financing: data room, measured unit economics, support-load evidence, renewal data, channel plan — Founder + QA/Measurement" | Forward shape of VALIDATION-PACKET evidence ownership |
| Golden Quill business constraints | `CLAUDE.md` (project instructions): FIT Farms LLC = current legal entity; BYOK only; no metered billing; sovereignty promise | Entity-hygiene framing; what bookkeeping/billing must NOT assume |
| Current Craft ledger | `.craft/ledger.yml` gaps[0..3]; owners founder-bookkeeper / customer-success-engineering / customer-success-backend / founder-qa; treatments author/author/coordinate/coordinate | Gap severity, owner, treatment per gap |
| Node research strategy | run-dir `RESEARCH-STRATEGY.md` | Evidence boundary + validation focus (first-revenue setup, support ownership, issue-log routing, Node Care ops, packet cadence) |
| Prep-stage artifacts | run-dir `REFINE-SEED-PROPOSAL.md`, `INVOKE-FIRST-ARTIFACTS.md`, `RUNTIME-HANDOFF.md`, `evidence-index.json` | Desired outcome (separate first-revenue from ongoing floor); downstream Refine/Invoke route; permission state |

Deduplication note: the four gaps share a single root evidence artifact (`ART-COF-HANDOFF` row block G). No conflicting source versions found. Accuracy: each gap summary in the ledger is a faithful restatement of its workbook row.

## r03 — Research Lane Map per Gap (external-boundary-reviewer)

| Gap | Severity | Owner (ledger) | Local evidence sufficiency | Lane | Bounded external need (if any) |
| --- | --- | --- | --- | --- | --- |
| `GAP-COF-ENTITY-HYGIENE` | flag | founder-bookkeeper | Partial — workbook names the activities (banking, bookkeeping, filing, insurance) and the "fractional bookkeeper at first revenue" trigger, but no operating checklist/cadence exists locally | local-first authoring; gap-triggered external optional | Generic bookkeeping-cadence reference (no client data) — DEFER |
| `GAP-COF-SUPPORT-TRIAGE` | block | customer-success-engineering | Partial — workbook states the triage axis ("support absorbs vs engineering sees") but not the routing rules, channel, or issue-log schema | local-first authoring; gap-triggered external optional | Generic support-triage / tiering pattern (no client data) — DEFER |
| `GAP-COF-NODE-CARE-OPS` | flag | customer-success-backend | Sufficient for authoring — workbook enumerates the four Node Care activities (updates, source-index maintenance, quarterly check-ins, vault care); cadence is an authoring decision, not a research gap | local-first authoring only | None |
| `GAP-COF-VALIDATION-PACKET` | flag | founder-qa | Sufficient for authoring — workbook §2 names the packet contents (data room, unit economics, support-load evidence, renewal data, channel plan); QA owns the evidence per row 80 | local-first authoring only; depends on C-node claims register | None (cross-node coordination, not external) |

Route selection (per `route_menu.selected_item_id` = `gap_triggered_external`): proceed local-first on all four; hold two bounded external comparison passes (ENTITY-HYGIENE, SUPPORT-TRIAGE) behind the approval gate. Two gaps need no external pass at all.

## r04 — External Approval Gate: DEFERRED (external-boundary-reviewer)

External research is NOT authorized in this run (dispatch rg03 = human_approval; strategy "only after approval"). Decision recorded: **DEFERRED**. Bounded external requests, named for a later approved pass:

- **EXT-COF-01 — Bookkeeping cadence reference.** Scope: generic small-LLC / fractional-bookkeeper monthly-close cadence and entity-hygiene checklist (banking separation, filing calendar, insurance categories). Protected-context flag: NONE — no Golden Quill confidential data, no client org data leaves the node. Blocks: `GAP-COF-ENTITY-HYGIENE` checklist completeness. Approval owner: Josh.
- **EXT-COF-02 — Support triage pattern reference.** Scope: generic SaaS/hardware support-tiering and issue-log routing patterns (L1-absorb vs escalate-to-engineering boundary). Protected-context flag: NONE — pattern-level only. Blocks: `GAP-COF-SUPPORT-TRIAGE` routing-rule design (block-severity gap). Approval owner: Josh.

Neither request may run until Josh confirms. Both are pattern/reference-level only; neither requires any org-isolated or Golden Quill-confidential input to be sent outward.

## r05 — Claim-Evidence Validation (claim-validation-reviewer)

Every claim below maps to a source class + concrete path/handle + validation question. Full table in `research-validation-ledger.md`. Summary: 7 claims validated; all carry a local source path; 0 claims depend on unapproved external evidence; owner-boundary check passes for all (planning evidence only). Two authoring gaps (ENTITY-HYGIENE, SUPPORT-TRIAGE) carry a named-but-deferred external dependency that is correctly gated, not asserted.

## r06 — Synthesis Handoff (claim-validation-reviewer)

- **Overall verdict: PASS (local-first sufficient to enter authoring; two bounded external passes deferred).** All four gaps have a local evidence baseline. Two gaps (NODE-CARE-OPS, VALIDATION-PACKET) are fully authorable from local evidence now. Two gaps (ENTITY-HYGIENE, SUPPORT-TRIAGE) are authorable from local evidence with an optional, named, approval-gated external comparison pass to harden them.
- **Next route:** `refine` → Invoke Define/Design/Plan per `INVOKE-FIRST-ARTIFACTS.md`, turning Workstream G rows into a first-revenue-vs-ongoing-floor operations plan. The block-severity `GAP-COF-SUPPORT-TRIAGE` should lead (highest severity; defines the triage boundary other ops depend on).
- **Owner boundary:** this run wrote only the two RUN_DIR files. `.craft/ledger.yml`, canonical architecture, and client org context untouched. Stage receipts in the dispatch remain `not_run` (this is the strategy-execution evidence layer, not a runtime-backed stage).

## Residue

- Two deferred external requests (EXT-COF-01, EXT-COF-02) await Josh's approval before any web pass.
- `GAP-COF-VALIDATION-PACKET` has an unresolved cross-node dependency on the quality-security-proof node's claims register (Workstream C) — the packet consumes that evidence; ownership of the hand-off seam is not yet specified locally.
- Bookkeeper and Customer Success are unstaffed/fractional ("onboard at first revenue" / "as deployments stack") — authoring must encode trigger conditions, not assume staffed roles.

## Next Move

Surface EXT-COF-01 and EXT-COF-02 to Josh for approve/decline, and (independently of that decision) begin the local-first Refine authoring pass led by `GAP-COF-SUPPORT-TRIAGE` (block severity). Neither requires the external passes to start.
