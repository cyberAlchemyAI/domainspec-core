# Context Pack: Card System Promotion Governance Research

## Identity

- Task: Run the validated card-system-to-promotion-governance research route.
- Mode: standard
- Session date: 2026-06-01
- Target output: `projects/goldenquill/docs/strategy/goldenquill_card_system_promotion_governance_research_2026-06-01.md`
- Dispatch route: `projects/goldenquill/docs/strategy/goldenquill_card_system_promotion_governance_research_2026-06-01.dispatch.json`
- Session report: `TASK-SESSION-REPORT.md`

## Obligations

| ID | Obligation | Status | Evidence |
| --- | --- | --- | --- |
| O1 | Resolve card-system research source folder. | covered | `projects/goldenquill/docs/card_system_deep_research_2026-05-17/` |
| O2 | Use the canonical naming and orthogonality audit. | covered | `CANONICAL_NAMING_AND_ORTHOGONALITY_AUDIT.md` |
| O3 | Use lifecycle and loader governance findings. | covered | `CARD_LIFECYCLE_AND_LOADER_GOVERNANCE_AUDIT.md` |
| O4 | Use CTO blockers and patch queue as risk and sequencing evidence. | covered | `INITIAL_CTO_HANDOFF_BLOCKERS.md`, `FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md` |
| O5 | Map card-system findings to promotion governance without mutating cards or implementation files. | covered | Research synthesis §Direct Mapping, §Immediate Design Recommendations |
| O6 | Preserve promotion guardrail: evidence, KPI, candidate, privacy, owner decision, and active reuse are separate. | covered | Research synthesis §What The Card-System Audit Teaches |
| O7 | Validate dispatch route shape. | covered | `validate-dispatch.py` pass |
| O8 | Record follow-up decisions instead of executing deeper fanout without separate approval. | covered | Research synthesis §Recommended Follow-Up Dispatch and report follow-up |

## Included Context

### Card Lifecycle And Loader Governance

Selected because it provides the strongest authority-state evidence.

Key selectors:

- Findings L1-F0 through L1-F9.
- §3.1 lifecycle enum drift.
- §3.3 split between `draft_status`, `runtime_load_status`, and `runtime_loadable`.
- §6 loader enforcement posture.

Promotion-governance use:

- Separate application stage, outcome event, validation state, graph authority,
  source truth, candidate state, owner decision, and active reuse.

### Canonical Naming And Orthogonality

Selected because it provides the strongest naming, coupling, and Law-5 evidence.

Key selectors:

- L2-F0 through L2-F9.
- §3 amendment-vs-disk drift.
- §4 naming collision and legacy/canonical phrase drift.
- §5 CIC/CLC orthogonality enforcement layers.
- §6 Law-5 `common_funders_observed` discipline.

Promotion-governance use:

- Add guardrails preventing KPI, source evidence, dashboard labels, feedback, and
  candidates from becoming owner-approved reuse directly.

### Initial CTO Handoff Blockers

Selected because it summarizes severity and sequencing.

Key selectors:

- §0 big picture.
- P0-1 locked-but-not-applied amendments.
- CR-1 LOCK-vs-disk amendment hygiene.
- §5 recommended sequencing.

Promotion-governance use:

- Add companion-readiness status to prevent approved text or approved intent from
  being mistaken for active reusable authority.

### File-By-File Patch Queue

Selected because it classifies repair work by authority impact.

Key selectors:

- Batch A documentation-only.
- Batch B cards-ceremony.
- Batch C gate-body graduation.
- Batch D loader graduation.
- Batch E deferred cleanup.

Promotion-governance use:

- Classify follow-up as client language clarification, evidence ceremony,
  promotion gate hardening, source importer/dashboard graduation, or deferred
  cleanup.

### Phased Card System Research Audit

Selected because it introduces Program Rule Pack routing and shows how external
research should route to a rule layer instead of card content.

Key selectors:

- §0 PRP manifest feedstock.
- §3 routing posture.
- §4 unaddressed next steps.

Promotion-governance use:

- Keep funder/compliance rules separate from outcome-learning promotion.

## Excluded Candidates

- Direct card YAML edits: out of scope; this task is research-only.
- Gate module implementation: out of scope; this task is research-only.
- DomainSpec feature docs: already created separately and not needed to run this research task.
- Client package ZIP: unrelated to this task-session evidence.

## Gate Summary

| Gate | Verdict | Notes |
| --- | --- | --- |
| Source boundary | pass | Research cites the May 17 audit folder and existing promotion-governance artifacts. |
| Mutation boundary | pass | No card, schema, gate, or lock-history mutation was performed. |
| Promotion authority | pass | Findings generate design recommendations only. |
| Fanout authorization | deferred | Deeper fanout remains recommended, not executed. |
| Dispatch validation | pass | Local validator returned no blocks or flags. |

## Next Actions

1. Decide whether to adopt the card-system lessons into the promotion-governance design.
2. If deeper work is desired, run the five-lane fanout named in the dispatch route.
3. If adopted, update promotion governance with companion-readiness states and promotion orthogonality gates.
