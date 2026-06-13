# Research Result - Staffing, budget, and triggers

- Dispatch ID: `gq-research-strategy-staffing-budget-and-triggers-2026-06-12`
- Run dir: `docs/strategy/development/staffing-budget-and-triggers/development/refinement-runs/2026-06-12-craft-pipeline-hydration`
- Mode: LOCAL-FIRST research execution (r01-r06)
- Lenses: local-evidence-reviewer, external-boundary-reviewer, claim-validation-reviewer
- Overall verdict: **PASS (local-first)** — local evidence fully scopes the node; the budget-blocking gaps are operator-input gaps and one bounded external-comparison gap, none resolvable by mutating artifacts here.

## Node

- Craft node: `staffing-budget-and-triggers`
- Title: Staffing, budget, and triggers
- Research lane: staffing and budget trigger research
- Purpose (CTX-SBT-ROOT): convert workbook roles and empty budget columns into budgetable staffing state.

## Core Question

What hours, rates, role triggers, and onboarding order are needed to turn role rows into budgetable execution state?

## r01 - Scope (node-specific question; cross-node drift rejected)

The node owns staffing budget primitives only: per-role hours, per-role rates, onboarding triggers, and onboarding order. Adjacent nodes carry the *content* of those roles' work and must not be pulled in:

- Hardware build/install labor content -> `hardware-golden-image` / `node-on-desk-readiness`.
- Security-review and QA proof content -> `quality-security-proof`.
- Sales/legal/contracting content -> `sales-contracting-legal`.
- White-glove delivery content -> `white-glove-delivery-node-care`.
- After-acceleration team build-out narrative -> `after-acceleration-roadmap`.

This node reads those workstreams only as *role rows that need hours/rates/triggers*, not as work to plan. No cross-node drift detected. No item required Josh's business judgment to scope (judgment is required to *fill*, see r04).

## r02 - Local Evidence Baseline (cited by path)

Primary source-contract: `[repo-root] docs/golden-quill-task-role-breakdown-handoff.md` (ledger id `ART-SBT-HANDOFF`).

| Finding | Evidence (path + locus) | Source class |
| --- | --- | --- |
| F1. Every `Est. Hrs` and `Notes / Rate` cell is blank across Sheet 1 (lines 33-80), Sheet 2 (lines 89-97), and the Sheet 3 role map. Budget cannot be computed from the workbook as extracted. | `docs/golden-quill-task-role-breakdown-handoff.md:33-97` ; extraction note `:122` ("Empty cells from the workbook are left blank") | workbook (extracted) |
| F2. Staffed core = Josh (Founder/Strategy/Deployment), Koichi (AI Engineer), Vlad (Backend Engineer), Victor (QA/Measurement); all marked "Staffed". | `docs/golden-quill-task-role-breakdown-handoff.md:107-110` | workbook role map |
| F3. Onboard-NOW / near-now roles with no fill and qualitative-only triggers: Domain Experts x4 ("Contract, paid structured input"), Legal/fractional ("before first LOI signs"), Security Reviewer ("One-time, recurring at major releases"). | `docs/golden-quill-task-role-breakdown-handoff.md:113-115` ; tasks at `:58,:63,:68` | workbook role map + task rows |
| F4. Onboard-LATER roles with founder-absorption + qualitative trigger: Customer Success ("Part-time contract as deployments stack"), Field/Install Tech ("Part-time at volume; trained from checklist"), Bookkeeper ("Few hrs/month at first revenue"). | `docs/golden-quill-task-role-breakdown-handoff.md:111-112,:116` ; tasks `:69-79` | workbook role map + task rows |
| F5. Triggers are stated qualitatively ("as deployments stack", "at volume", "at first revenue", "before first LOI") with no numeric thresholds (deployment count / revenue $). | `docs/golden-quill-task-role-breakdown-handoff.md:111-116` ; decision `DEC-SBT-TRIGGER-MODEL` (ledger) | workbook + Craft decision |
| F6. Effort-type legend (BUILD one-time / PER-NODE deployment / ONGOING operating floor) classifies each row's cost kind, but carries no hours. This is the cost-structure scaffold the budget will hang on. | `docs/golden-quill-task-role-breakdown-handoff.md:23-29` | workbook legend |
| F7. "Skills to weigh later" (tech writing, instructional design, public-procurement fluency, hardware logistics, privacy/compliance counsel) are unfilled and flagged "fold into above roles" — not yet distinct budget lines. | `docs/golden-quill-task-role-breakdown-handoff.md:117` | workbook role map |

Craft ledger cross-checks (source class: Craft): the three active gaps and the open decision in `.craft/ledger.yml` (`GAP-SBT-HOURS-RATES` block, `GAP-SBT-ONBOARD-NOW` flag, `GAP-SBT-ONBOARD-LATER` flag, `DEC-SBT-TRIGGER-MODEL` pending) are each directly corroborated by the findings above. No deduplication conflict; ledger and workbook agree.

Local-first gate (rg02): satisfied — all evidence classes (workbook roles/gaps, Craft gaps, first-node assumptions) reviewed before any external class considered.

## r03 - Research Lane Map (per gap)

| Gap | Severity | Lane selected | Owner / resolution path | External needed? |
| --- | --- | --- | --- | --- |
| `GAP-SBT-HOURS-RATES` | block | **operator-fill (local)** for hours; **gap-triggered external** for market rate bands | Founder fills per-row `Est. Hrs` against the BUILD/PER-NODE/ONGOING legend (F6); fractional-role *rates* may need external comparison (see r04 EXT-1/EXT-2). | Partial |
| `GAP-SBT-ONBOARD-NOW` | flag | **operator-decide (local)** procurement shape; **gap-triggered external** for rate bands | Founder sets engagement form (contract vs fractional retainer) for Domain Experts / Legal / Security Reviewer; cost band may need external comparison. | Partial |
| `GAP-SBT-ONBOARD-LATER` | flag | **decide (local)** trigger thresholds | Operations + Founder set numeric thresholds for `DEC-SBT-TRIGGER-MODEL` (deployment count / revenue $) at which Josh stops absorbing CS, Field Tech, Bookkeeper. Pure business judgment — no external pass resolves it. | No |

Route-menu selection (per dispatch `selected_item_id: gap_triggered_external`): **local-first executed; external lane mapped but NOT run.**

## r04 - External-Research Decision: DEFERRED

Gate rg03 (human_approval) is NOT satisfied — Josh has not approved a bounded external pass. External research is **deferred**. Bounded requests, named and held for approval:

- **EXT-1 — Fractional legal/security/bookkeeping rate ranges.** Bounded comparison of US-market hourly/retainer bands for: fractional legal counsel (contracts/data-policy/FERPA reading), independent security reviewer (one-time audit + recurring), fractional bookkeeper (few hrs/month). Feeds `GAP-SBT-HOURS-RATES` rate side + `GAP-SBT-ONBOARD-NOW` cost. Protected-context flag: none (no client/org data leaves; generic market query). Trigger: only after Josh confirms.
- **EXT-2 — Hardware install/support labor benchmarks.** Bounded comparison of field-tech / install-tech labor rates and per-deployment support-hour benchmarks for desktop-appliance install + burn-in. Feeds `GAP-SBT-HOURS-RATES` (PER-NODE rows) + `GAP-SBT-ONBOARD-LATER` Field Tech costing. Protected-context flag: none. Trigger: only after Josh confirms.
- **EXT-3 — Domain-expert structured-input compensation norms (conditional).** Comparison of paid honoraria/contract rates for subject-matter expert structured input (4 segment cards). Feeds `GAP-SBT-ONBOARD-NOW`. Lower priority; raise only if EXT-1 does not cover. Trigger: Josh confirm.

No external lookup performed. Org-isolation gate rg04: held — no `orgs/` PROJECT_CONTEXT read; all evidence is Golden Quill project scope.

## r05 - Claim-Evidence Validation

See `research-validation-ledger.md` (sibling file). All seven findings + three gap-lane claims carry a source class, concrete path/handle, and validation question. Verdict there: PASS. Gate rg05 satisfied; no claim lacks a local path, source class, or explicit external-approval state.

## Residue

- The hours dimension of `GAP-SBT-HOURS-RATES` and all of `GAP-SBT-ONBOARD-LATER` are **operator-input residue** — no research (local or external) can close them; they require Josh's numbers and Operations' threshold decision. Flagged as the binding constraint on producing a budget.
- `DEC-SBT-TRIGGER-MODEL` remains `PENDING` (selection). It blocks converting the workbook into a staffing budget but is owner-decision, not research.
- "Skills to weigh later" (F7) are not yet budget lines; revisit only if folded-into-role assumption breaks.
- Owner-boundary (rg06): no canonical/lifecycle artifact mutated; `.craft/ledger.yml` untouched; only the two RUN_DIR outputs written.

## Next Move

Single next move: **present EXT-1/EXT-2 (and conditional EXT-3) to Josh for the rg03 approval decision, and in the same turn request the operator-input residue** — per-row hours against the legend and numeric thresholds for `DEC-SBT-TRIGGER-MODEL`. Local research is exhausted; the node now waits on one approval gate plus operator numbers, after which the Refine route can hydrate a budgetable staffing state.
