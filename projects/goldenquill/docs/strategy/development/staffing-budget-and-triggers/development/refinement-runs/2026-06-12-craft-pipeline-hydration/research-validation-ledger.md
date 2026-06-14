# Research Validation Ledger - Staffing, budget, and triggers

- Dispatch ID: `gq-research-strategy-staffing-budget-and-triggers-2026-06-12`
- Step: r05-claim-evidence-validation (gate rg05)
- Source classes: `workbook` (extracted from `docs/golden-quill-task-role-breakdown-handoff.md`), `craft` (`.craft/ledger.yml`), `external-deferred` (named, not run, awaiting rg03 approval).

## Claim -> Source -> Validation table

| # | Claim | Source class | Path / handle | Validation question | External approval state | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | All `Est. Hrs` and `Notes / Rate` cells are blank; budget is not computable from the workbook. | workbook | `docs/golden-quill-task-role-breakdown-handoff.md:33-97`, `:122` | Are both columns blank across all three sheets? | n/a (local-confirmed) | PASS |
| C2 | Staffed core is Josh, Koichi, Vlad, Victor (all "Staffed"). | workbook | `docs/golden-quill-task-role-breakdown-handoff.md:107-110` | Does the role map mark exactly these four "Staffed"? | n/a | PASS |
| C3 | Domain Experts, Legal, Security Reviewer are onboard-NOW roles, unfilled, with qualitative-only triggers. | workbook | `docs/golden-quill-task-role-breakdown-handoff.md:113-115`, `:58,:63,:68` | Do these three rows show "—" / "Onboard NOW" with non-numeric triggers? | n/a | PASS |
| C4 | Customer Success, Field Tech, Bookkeeper are onboard-LATER, founder-absorbed, qualitative trigger. | workbook | `docs/golden-quill-task-role-breakdown-handoff.md:111-112,:116`, `:69-79` | Are these three founder-absorbed with "as deployments stack / at volume / at first revenue"? | n/a | PASS |
| C5 | Onboarding triggers are stated qualitatively with no numeric deployment-count or revenue thresholds. | workbook + craft | `docs/golden-quill-task-role-breakdown-handoff.md:111-116`; `DEC-SBT-TRIGGER-MODEL` in `.craft/ledger.yml` | Does any cell give a numeric threshold? (expected: none) | n/a | PASS |
| C6 | Effort-type legend (BUILD/PER-NODE/ONGOING) is present and is the cost-structure scaffold, but carries no hours. | workbook | `docs/golden-quill-task-role-breakdown-handoff.md:23-29` | Is the legend present and hours-free? | n/a | PASS |
| C7 | "Skills to weigh later" are unfilled and flagged "fold into above roles" — not yet budget lines. | workbook | `docs/golden-quill-task-role-breakdown-handoff.md:117` | Is this row unfilled with a fold-in note? | n/a | PASS |
| C8 | `GAP-SBT-HOURS-RATES` (hours side) is operator-input; no research closes it. | craft | `.craft/ledger.yml` gaps[0]; owner `founder` | Is the owner a founder-fill, not a research lane? | n/a | PASS |
| C9 | `GAP-SBT-ONBOARD-LATER` / `DEC-SBT-TRIGGER-MODEL` thresholds are pure operator business judgment. | craft | `.craft/ledger.yml` gaps[2], decisions[0] (`selected: PENDING`) | Is the decision unresolved and owner-set, not externally derivable? | n/a | PASS |
| C10 | Fractional legal/security/bookkeeping + hardware install rate bands require a bounded external comparison. | external-deferred | RESEARCH-RESULT.md r04 EXT-1, EXT-2, EXT-3 | Has Josh approved (rg03)? | **DEFERRED — not approved, not run** | PASS (correctly gated) |

## Data-quality checks (r05 overlay)

- Accuracy: each local claim cites a concrete line range; no paraphrase substitutes for the source (Law 1 spirit). PASS.
- Completeness: all three active gaps + the open decision are covered; no gap left without a lane. PASS.
- Conformity: every row has source class + path/handle + validation question + approval state. PASS.
- Integrity: ledger and workbook agree (no contradiction between `.craft/ledger.yml` gap statements and workbook cells). PASS.
- Deduplication: Craft gaps and workbook findings mapped 1:1, no double-counting. PASS.

## Gate status

- rg02 local-first: PASS (local exhausted before any external class activated).
- rg03 external-approval: correctly **ASK/DEFERRED** — no external research run; C10 held pending Josh approval.
- rg04 org-isolation: PASS (no `orgs/` PROJECT_CONTEXT read; Golden Quill project evidence only).
- rg05 claim-evidence: PASS (every claim mapped to source class + path/handle + validation question + approval state).
- rg06 owner-boundary: PASS (no canonical/lifecycle artifact mutated; `.craft/ledger.yml` untouched; only two RUN_DIR outputs written).

## Overall verdict

**PASS (local-first complete; external deferred).** Local evidence fully scopes the node and corroborates every Craft gap/decision. The binding residue (per-row hours, fractional-rate bands, numeric onboarding thresholds) is operator-input plus one approval-gated bounded external pass (EXT-1/EXT-2/EXT-3). No fail-closed condition; no boundary violation.
