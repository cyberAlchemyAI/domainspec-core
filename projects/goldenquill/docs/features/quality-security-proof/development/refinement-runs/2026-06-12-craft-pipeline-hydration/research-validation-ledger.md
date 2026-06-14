# Research Validation Ledger - Quality, security, and proof

Run: `2026-06-12-craft-pipeline-hydration`.
Dispatch: `gq-research-strategy-quality-security-proof-2026-06-12`.
Gate: rg05 claim-evidence (each claim → source class + path/handle + validation
question + owner-boundary check). All sources are local Golden Quill project
evidence (rg02 local-first, rg04 org-isolation honored).

## Source-Class Legend

- **WORKBOOK** = source contract `docs/golden-quill-task-role-breakdown-handoff.md`
- **LEDGER** = `docs/features/quality-security-proof/.craft/ledger.yml`
- **STRATEGY** = run-dir `RESEARCH-STRATEGY.md`
- **CANON** = `CLAUDE.md` governance (Five Laws + F-CLASS-* / F-WPFA-* rosters, WPFA §17)
- **RUNDIR** = node-local run artifacts (`REFINE-SEED-PROPOSAL.md`, `INVOKE-FIRST-ARTIFACTS.md`, `evidence-index.json`)

## Claim → Source → Validation

| # | Claim | Source class | Concrete path / handle | Validation question | External? | Owner boundary | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | This node owns exactly six proof surfaces (Workstream C). | WORKBOOK | `docs/golden-quill-task-role-breakdown-handoff.md` rows 56-61 | Do all six rows fall under "C. Quality, Security & Proof"? | No | In-scope; planning only | PASS |
| C2 | QA/Measurement owner is Victor; staffed. | WORKBOOK + LEDGER | WORKBOOK rows 56-61, 110; LEDGER `DESC-QSP-001` | Is the role marked Staffed and bound to Victor? | No | In-scope | PASS |
| C3 | Independent security reviewer is onboard-now, unassigned, one-time + recurring at major releases. | WORKBOOK + LEDGER | WORKBOOK rows 58, 115; LEDGER `gaps[1]` GAP-QSP-SECURITY-REVIEWER | Is the reviewer unassigned and is assignment a staffing (not research) act? | No | **Operator decision (Josh)** — not closable by research | PASS (correctly deferred) |
| C4 | Four active gaps with stated severity/owner/treatment. | LEDGER | `.craft/ledger.yml` gaps[0-3] | Do the four gap ids + severities match the ledger? | No | In-scope | PASS |
| C5 | Guardrails-to-be-tested already exist as local primitives (Five Laws + F-CLASS-* sixteen + F-WPFA-* twelve fail-closed gates). | CANON | `CLAUDE.md` Five Operating Laws; F-CLASS-* roster (v7.0.10); F-WPFA-* roster (§17) | Do named fail-closed gate families exist in canon to source the test plan? | No | In-scope; cross-walk is Invoke-Define authoring, not research | PASS |
| C6 | Claims-register "claim → evidence-category" pattern is already modeled locally (WPFA buyer-facing claims link to coefficient + cycle_id + trace_id). | CANON + WORKBOOK | `CLAUDE.md` WPFA §17; WORKBOOK row 59 | Does an existing local pattern map claims to evidence categories? | No | In-scope; sales-touching claims escalate to Josh | PASS |
| C7 | Instrumentation metric vocabulary (support hrs/node, usage baselines, renewal-intent) is sourced locally. | CANON + WORKBOOK | `CLAUDE.md` WPFA CycleReceipt §17; WORKBOOK rows 61, 96 | Are the instrument terms present in local evidence? | No | In-scope | PASS |
| C8 | All four gaps can be authored local-only; external input is value-add, not blocking. | LEDGER + CANON + STRATEGY | LEDGER gaps[0-3]; CANON gate rosters; `RESEARCH-STRATEGY.md` lines 31-39 | For each gap, is there a local source sufficient to start authoring? | No | In-scope | PASS |
| C9 | No external research was executed; B1-B4 are deferred bounded requests pending Josh approval. | STRATEGY + dispatch | `RESEARCH-STRATEGY.md` lines 47-55; RESEARCH-DISPATCH.json rg03, route `gap_triggered_external` selected but not authorized | Is any external lookup run? Is each external lane bounded + approval-gated? | Deferred | rg03 honored; no external call made | PASS |
| C10 | No client `orgs/` PROJECT_CONTEXT was read; only Golden Quill project evidence used. | (process) | rg04; no orgs/ path opened this pass | Did any read touch a client org folder? | No | rg04 org-isolation honored | PASS |
| C11 | Only the two RUN_DIR output files were written; ledger + canonical artifacts untouched. | (process) | rg06; `RESEARCH-RESULT.md` + `research-validation-ledger.md` only | Were any canonical/lifecycle artifacts mutated? | No | rg06 owner-boundary honored | PASS |
| C12 | Runtime stages and subagents did not execute (planning evidence only). | RUNDIR | `evidence-index.json` stage_receipts all `not_run`; `stages/` holds only `.gitkeep` | Did any runtime stage or subagent run? | No | Planning only | PASS |

## Owner-Boundary Checks (rg06)

- Research did not author the test plan, reviewer scope, claims register, or instrument definitions — those are owned by the Refine/Invoke authoring route after operator confirmation. Honored.
- The security-reviewer assignment (C3) is a staffing decision routed to Josh, not a research output. Honored.

## Overall Verdict

**PASS — local-first research baseline complete.** All twelve claims map to a
concrete local source class and path; zero claims depend on unapproved external
sources; org isolation (rg04), claim-evidence (rg05), and owner-boundary (rg06)
gates all hold; external research (rg03) is correctly DEFERRED with four bounded,
approval-gated requests (B1-B4). Local evidence is sufficient to author all four
gap treatments without external input. One gap (security-reviewer assignment)
is correctly classified as an operator decision outside research scope.
