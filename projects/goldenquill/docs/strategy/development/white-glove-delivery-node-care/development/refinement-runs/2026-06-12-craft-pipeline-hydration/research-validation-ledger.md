# Research Validation Ledger — White-Glove Delivery and Node Care

- **Dispatch ID:** `gq-research-strategy-white-glove-delivery-node-care-2026-06-12`
- **Gate owner:** interrogation (rg05 claim-evidence) + dispatch-spec (rg06 owner-boundary)
- **Validation rule (rg05):** every claim → source class + concrete path/handle + validation question + external-approval state.
- **Source classes:** `workbook` (task-role handoff) · `playbook` (v0.1 Beta procedure) · `ledger` (Craft) · `doctrine` (CLAUDE.md project canon).

| # | Claim | Source class | Path / handle | Validation question | External-approval state |
|---|---|---|---|---|---|
| C1 | Node owns Workstream F (7 PER-NODE delivery tasks: pre-deployment, Day 0, vault build, source universe, first packet, first-draft+training, Day 60). | workbook | `docs/golden-quill-task-role-breakdown-handoff.md` rows 70–76 | Do all seven stages appear as distinct F rows? | n/a (local) |
| C2 | The technical onboarding spine already exists as a written, locked procedure (BULK_INGEST → Classification Review → posture → first cycle → AWARD_INGEST). | playbook | `docs/white_glove_v0_1_beta.md` §§1–4 | Is each stage a numbered section with a done-condition? | n/a (local) |
| C3 | The playbook gap is the human-facing service *wrapper* (document-request kit, questionnaire, posture script, deployment record, training curriculum, closeout, missing-doc list), not the engine. | workbook + playbook | handoff rows 70, 72–76 (name the wrapper items) vs. `white_glove_v0_1_beta.md` (covers engine, not wrapper) | Are the wrapper items named in F rows but absent as procedure in the v0.1 playbook? | n/a (local) |
| C4 | Delivery is founder-led first and must become a CS + Field-Tech repeatable process. | ledger + workbook | `.craft/ledger.yml` DESC-WGD-001; handoff row 111 ("Josh absorbs first nodes → part-time contract as deployments stack") | Does a local source state the founder→non-founder transition explicitly? | n/a (local) |
| C5 | CS/Field-Tech handoff *trigger* is owned by `staffing-budget-and-triggers`; this node only consumes the trigger + authors the executable checklist. | ledger | `.craft/ledger.yml` gaps[1] (GAP-WGD-CS-HANDOFF, `owner: staffing-budget-and-triggers`) | Does the ledger assign this gap's ownership outside this node? | n/a (local) |
| C6 | Day 60 review needs four named outputs (metrics, support-load, renewal signal, next-cycle plan); metrics are QA-instrumentation-sourced. | ledger + workbook | `.craft/ledger.yml` gaps[2]; handoff rows 61 (instrumentation) + 76 (Day 60 row) | Do the four outputs + their QA metric source both appear locally? | n/a (local) |
| C7 | Node Care (updates, source-index maintenance, quarterly check-ins, vault care) is the ongoing tail; ties to update-and-signing + INCREMENTAL_INGEST confidential default. | workbook + playbook | handoff rows 41, 79; `white_glove_v0_1_beta.md` §5 | Is Node Care a named ongoing Workstream-G row + reflected in INCREMENTAL_INGEST? | n/a (local) |
| C8 | Every delivery artifact must preserve and demonstrate the sovereignty promise (operator owns hardware/keys/data; classification-gated routing) at the test cycle. | doctrine + playbook | `CLAUDE.md` Sovereignty Promise; `white_glove_v0_1_beta.md` §§2.3, 7 | Is sovereignty stated as a non-negotiable acceptance criterion locally? | n/a (local) |
| C9 | GAP-WGD-PLAYBOOK is authorable now from local evidence as a delta over the v0.1 playbook; external passes are enhancement-only. | derived (C1+C2+C3) | RESEARCH-RESULT.md r03–r04 | Can the playbook delta be written without any external source? | external DEFERRED (EXT-WGD-01 optional) |
| C10 | The workbook's "Unrestricted / Hybrid / Sanitized / Sovereign" posture label is stale vs. the three-posture v7.0.10 model. | workbook vs. doctrine | handoff row 50 vs. `CLAUDE.md` Beta Model Strategy (v7.0.10) | Does the doctrine supersede the four-posture wording? (residue; not this node's to fix) | n/a (local; owner-boundary flagged) |

## Owner-Boundary Check (rg06)

- **PASS.** Two output files written into RUN_DIR only (`RESEARCH-RESULT.md`, `research-validation-ledger.md`). No canonical/lifecycle artifact mutated. `.craft/ledger.yml` not edited. C5/C6/C10 residues explicitly routed to owning nodes rather than authored here.

## Org-Isolation Check (rg04 / Law 3)

- **PASS.** Only Golden Quill PROJECT evidence read (handoff, v0.1 playbook, ledger, CLAUDE.md). No `orgs/` client PROJECT_CONTEXT accessed.

## External-Research Check (rg03)

- **PASS / DEFERRED.** No web search or external lookup performed. Three bounded requests (EXT-WGD-01/02/03) recorded as optional, approval-gated enhancement passes; none blocks node progress.

## Overall Verdict

**PASS.** All ten claims map to a concrete local Golden Quill source path + source class + validation question. No claim depends on un-approved external research. Owner-boundary and org-isolation gates clean. The block-severity gap (GAP-WGD-PLAYBOOK) is locally authorable; the two flag-severity gaps are correctly routed as coordinate-with dependencies. Node is research-complete and ready for the permission-gated Refine handoff.
