# Research Validation Ledger - Sales, Contracting, and Legal

- Dispatch ID: `gq-research-strategy-sales-contracting-legal-2026-06-12`
- Step: r05-claim-evidence-validation (gate rg05 claim-evidence; rg06 owner-boundary)
- Rule: every claim maps to a source class + concrete path/handle + external-approval state. Any claim lacking a local path, source class, or explicit external-approval state BLOCKS.

## Claim → Source → Validation Table

| ID | Claim | Source class | Source path / handle | External-approval state | Validation question | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | This node owns Workstream E (4 tasks). | local workbook | `docs/golden-quill-task-role-breakdown-handoff.md` rows 66-69 | n/a (local) | Are all four E rows present and node-scoped? | PASS |
| C2 | Legal (fractional) onboard trigger is "before first LOI signs" and carries customer agreement/LOI/data-policy/procurement/FERPA-AI-transparency. | local workbook | `docs/golden-quill-task-role-breakdown-handoff.md` row 114 | n/a (local) | Is the trigger text verbatim and LOI-gated? | PASS |
| C3 | Bookkeeper trigger is "at first revenue," carrying deposits/invoicing/cost-tracking. | local workbook | `docs/golden-quill-task-role-breakdown-handoff.md` rows 69, 116 | n/a (local) | Is deposit work revenue-gated, not LOI-gated? | PASS |
| C4 | "Disclosure rules" attach to sales/pipeline-tracker task but are undefined in the workbook. | local workbook | `docs/golden-quill-task-role-breakdown-handoff.md` row 66 | n/a (local) | Does the workbook define disclosure rules anywhere? (No — gap confirmed.) | PASS (gap, not claim of content) |
| C5 | Data-policy terms must align to locked BYOK + posture + sovereignty model. | project canon | CLAUDE.md "Beta Model Strategy" + "Sovereignty Promise" | n/a (local) | Does canon constrain customer data-policy language? | PASS |
| C6 | Three ledger gaps map to the core-question clauses; qualification clause has no gap. | local craft ledger | `.craft/ledger.yml` gaps[0-2], indexes.active_gaps | n/a (local) | Do gap IDs/severities match the table? | PASS |
| C7 | "public-procurement fluency" + "privacy/compliance counsel" are pre-flagged later-skills. | local workbook | `docs/golden-quill-task-role-breakdown-handoff.md` row 117 | n/a (local) | Are both listed under skills-to-weigh-later? | PASS |
| C8 | Legal templates/benchmarks/statutory text are absent locally (external-gap). | absence-of-evidence | `docs/golden-quill-task-role-breakdown-handoff.md` (whole) + run dir scan | DEFERRED — EXT-SCL-LEGAL-CLAUSE-PATTERNS / FERPA / PROCUREMENT-INSURANCE | Confirmed no template present locally? | PASS (deferred, not fetched) |
| C9 | Disclosure-language comparison patterns are external. | absence-of-evidence | n/a local | DEFERRED — EXT-SCL-DISCLOSURE-LANGUAGE-PATTERNS | Recorded, not fetched? | PASS (deferred) |
| C10 | Deposit/invoicing norms are external comparison material. | absence-of-evidence | n/a local | DEFERRED — EXT-SCL-DEPOSIT-INVOICING-NORMS | Recorded, not fetched? | PASS (deferred) |
| C11 | Sales-material claims depend on Claims Register (Workstream C / quality-security-proof node). | local workbook (cross-node) | `docs/golden-quill-task-role-breakdown-handoff.md` row 59 | n/a (flagged, not pulled) | Is dependency noted without pulling sibling-node internals or any org PROJECT_CONTEXT? | PASS (rg04 held) |
| C12 | No external research was executed in this run. | run-control | this run (r04 decision = DEFERRED) | DEFERRED (no Josh approval present) | Did any external/web lookup occur? (No.) | PASS |

## Gate Checks

| Gate | Condition | Result |
| --- | --- | --- |
| rg02-local-first | Local evidence reviewed before external classes activated | PASS — all C1-C7 local; external never run |
| rg03-external-approval | External requires named gap + Josh approval | PASS — deferred; 5 bounded requests named, none executed |
| rg04-org-isolation | Golden Quill project evidence only; no client org PROJECT_CONTEXT | PASS — no orgs/ files read; cross-node deps flagged only |
| rg05-claim-evidence | Each claim → source class + path/handle + validation state | PASS — 12/12 mapped |
| rg06-owner-boundary | Planning evidence only; no canonical/lifecycle mutation | PASS — only the two RUN_DIR output files written; ledger untouched |

## Overall Verdict

**PASS.** Local-first baseline is complete and fully cited; the block-severity legal gap is correctly identified as an external/counsel-dependent gap and DEFERRED with five named, bounded, approval-gated external requests. No claim lacks a source class, path/handle, or explicit external-approval state. No org-isolation or owner-boundary violation. Strategy is route evidence only; execution of external lanes remains gated on Josh's approval.
