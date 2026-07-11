---
module: investor-business-plan-package
version: current
status: flag
updatedAt: 2026-07-10
docType: work-pack
---

# WORK-PACK: Investor Business Plan Package

## Purpose

Canonical executable plan and SWU manifest for building the private investor BP
package from accepted research while preserving claim <= proof.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | flag | Usable for next planning/writing SWU; not investor-ready. |
| complexity | medium | Multiple dependent artifacts and evidence gates. |
| outputMode | single-file SWU manifest with execution-pack companion | Task-local split files deferred until the first SWU is selected for execution. |
| executionPackRef | `EXECUTION-PACK.md` | Wave choreography for the BP build. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 boundary decisions. |
| dispatchTechniqueTrace | `INVOKE-PLAN.md#dispatch-spec-technique-trace` | Required Invoke plan trace. |
| distillValidationStatus | flag | Local validation recorded; independent Distill run still needed. |
| activeLayerWindow | L3 | BP body complete; investor compression and final audit remain. |
| lastUpdatedAt | 2026-07-10 | BP evidence, economic, operating, and narrative layers drafted. |
| readinessProfile | pilot | Intended for first-investor preparation, not public release. |

## Objective Summary

- Objective: Create a private, evidence-bounded business plan package that can support first-investor conversations and later diligence.
- Primary inputs: accepted BP build findings, business-plan Whisper preset, Invoke plan contract, user constraints on claim discipline and company reach.
- Success condition: BP package exists with evidence registry, financial assumptions, operating plan, full BP, memo/deck substrate, and claim audit; every claim is mapped to evidence, assumption, or future-only status.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Evidence registry and source trace. | L0 | W0 | Accepted findings. | Every BP section has source evidence, missing witness, and demotion gate. |
| S-002 | Financial assumptions and operating model. | L1 | W1 | S-001. | Projections are driver-based and labeled assumptions. |
| S-003 | Full business plan draft. | L2 | W2 | S-001, S-002. | Whisper BP validation checks pass or gaps are explicit. |
| S-004 | Investor memo and deck substrate. | L3 | W3 | S-003. | No new claims beyond BP/data room. |
| S-005 | Claim audit and next-route handoff. | L3 | W4 | S-001 through S-004. | Forbidden claims absent or explicitly demoted. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-BP-001 | Build registry and source trace. | L0 | medium | W0 | BP findings, accepted portfolio/assurance/moat/model-use findings | pass | complete |
| TASK-BP-002 | Build bottom-up financial assumptions and operating plan. | L1 | medium | W1 | BP findings financial checklist, Whisper preset financial model | pass | complete |
| TASK-BP-003 | Draft full BP with evidence boundary. | L2 | medium | W2 | Registry, source trace, financial assumptions | flag | complete-draft |
| TASK-BP-004 | Draft memo and deck substrate. | L3 | medium | W3 | Full BP, claim audit draft | blocked | not-started |
| TASK-BP-005 | Run claim audit and handoff. | L3 | medium | W4 | All package artifacts | blocked | not-started |

## Implementation Detail Specs

### TASK-BP-001: Registry And Source Trace

Inputs: accepted BP research findings and named source findings. Output two
files: `diligence-evidence-registry.md` and `source-trace.md`.

Rules:

1. Classify each evidence item as proven now, assumption, forecast, future-only, missing witness, or forbidden.
2. Map each BP section to source evidence, missing witness, and demotion gate.
3. Preserve private/public boundary labels.
4. Do not draft investor prose in this task.

Edge cases:

- If a source is only an inventory summary, label it as registry evidence, not proof.
- If evidence is stale or unrunnable, label it historical substrate until refreshed.
- If a claim requires buyer evidence, mark it missing even if artifact breadth is strong.

### TASK-BP-002: Financial Assumptions And Operating Plan

Inputs: registry, source trace, sprint-unit model checklist. Outputs
`financial-assumptions.md` and `operating-plan.md`.

Rules:

1. Model diagnostic, sprint, advanced package, retainer, and future platform/license separately.
2. Include price, hours, direct costs, cash timing, founder capacity, conversion, retainer attach, scenarios, and sensitivity.
3. Label all numbers as assumptions unless backed by paid work.
4. Tie use-of-funds placeholders to 30/60/90 milestones.

Edge cases:

- Do not model broad platform ARR as current revenue.
- If ask/runway is unknown, keep a visible decision gap.

### TASK-BP-003: Full Business Plan Draft

Inputs: registry, source trace, financial assumptions, operating plan, Whisper
business-plan preset. Output `business-plan.md`.

Rules:

1. Start with one buyer problem, one wedge, one receipt bundle, and evidence boundary.
2. Separate current service offer from roadmap/platform thesis.
3. Use bottom-up buyer pocket language before broader market language.
4. Include visible risks, non-claims, demotion gates, and 30/60/90 witness queue.

Edge cases:

- If a section lacks evidence, write it as an assumption or future-only thesis.
- If investor ask/runway remains unknown, use a bracketed placeholder and mark it unresolved.

### TASK-BP-004: Memo And Deck Substrate

Inputs: full BP and current claim audit. Outputs `investor-memo.md` and
`deck-substrate.md`.

Rules:

1. Compress; do not expand claims.
2. The memo argues the decision case under uncertainty.
3. The deck gets meeting-getter language only, tied to evidence registry.
4. Use a visible non-claims box or equivalent section.

Edge cases:

- Reject any line that introduces unique/first/only, certification, compliance, audit-ready, or proven moat claims.

### TASK-BP-005: Claim Audit And Handoff

Inputs: all package artifacts. Output `claim-audit.md` and final handoff notes.

Rules:

1. Check every artifact against claim <= proof.
2. Classify claims as supported, assumption, forecast, future-only, demote, or forbid.
3. Record next witnesses for 30/60/90 days.
4. Recommend the next route: buyer interviews, task-session receipt refresh, financial-model review, or investor packaging.

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-BP-001 | TASK-BP-001 | `.arcanum/inventory/queries/2026-07-09-business-plan-build-research/findings.md`; `INVOKE-PLAN.md` | Accepted portfolio, assurance, moat, model-use, blind-spot findings referenced by BP findings. | none | `diligence-evidence-registry.md`, `source-trace.md` | Registry and source trace created without investor prose. | Section map includes evidence, missing witness, and demotion gate for every BP section. | Review check: no forbidden claims used as supported claims. | local-fallback | complete |
| SWU-BP-002 | TASK-BP-002 | BP findings sections 6 and 10; Whisper preset financial model requirements. | Registry/source trace from SWU-BP-001. | SWU-BP-001 | `financial-assumptions.md` | Bottom-up assumptions model created. | Price, hours, costs, capacity, cash timing, conversion, scenarios, and sensitivity represented. | Review check: no platform ARR modeled as current validated revenue. | local-fallback | complete |
| SWU-BP-003 | TASK-BP-002 | BP findings wedge model and operations mapping. | Financial assumptions from SWU-BP-002. | SWU-BP-002 | `operating-plan.md` | One paid wedge delivery loop documented. | Owner, metric/workflow, source chain, gate verdict, receipt bundle, feedback loop, and stop rules present. | Review check: operating loop does not claim autonomous governance. | local-fallback | complete |
| SWU-BP-004 | TASK-BP-003 | Whisper preset body parts and validation checks; registry/source trace. | Financial assumptions and operating plan. | SWU-BP-001, SWU-BP-002, SWU-BP-003 | `business-plan.md` | Full BP draft created. | Sections match preset; evidence boundary visible; risks/non-claims included. | Review check: every unsupported claim is labeled assumption/forecast/future-only. | local-fallback | complete-draft |
| SWU-BP-005 | TASK-BP-004 | Full BP; Whisper investor memo and deck substrate output modes. | Claim audit draft if available. | SWU-BP-004 | `investor-memo.md`, `deck-substrate.md` | Memo and deck substrate created. | Memo/deck contain no claims absent from BP/data room. | Review check: deck is compression layer, not diligence replacement. | local-fallback | blocked |
| SWU-BP-006 | TASK-BP-005 | All package artifacts; BP findings non-claims. | Optional external/current comparator refresh. | SWU-BP-004, SWU-BP-005 | `claim-audit.md` | Claim audit completed. | Forbidden claims absent or demoted; gap ledger updated. | `rg` review for forbidden terms plus manual classification table. | local-fallback | blocked |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-BP-001 | financials | Ask amount, runway, and use-of-funds target are unknown. | founder | Decide or authorize placeholders. | before SWU-BP-004 |
| B-BP-002 | market | Buyer-call evidence for one blocked decision is missing. | founder/research | Run 5-10 buyer calls. | before investor use |
| B-BP-003 | commercial | Paid pilot/SOW packet missing. | founder | Create SOW specimen and pursue first paid pilot. | before stronger traction claims |
| B-BP-004 | evidence | Fresh runnable receipts not yet collected. | task-session | Select and rerun receipt checks. | before diligence package |
| B-BP-005 | validation | Independent Distill run not executed. | invoke/distill | Run after initial artifacts exist. | before mutation-ready pass |

## Dispatch Technique Trace

See `INVOKE-PLAN.md#dispatch-spec-technique-trace`.

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit or SWU boundary | pass | `SWU-BP-001` is the first selected unit and does not require prior BP prose. |
| Recomposition proof | pass | SWUs build registry, financial assumptions, operating plan, BP, memo/deck, and audit. |
| Hidden acceptance-critical gaps | flag | Ask/runway, buyer calls, paid pilot, fresh receipts, comparator refresh. |
| Deferred complexity | flag | Subagent strategy and independent Distill run deferred. |
| Navigation to first executable unit | pass | Start at `SWU-BP-001`. |

## Gate Checks

1. Work-pack is `flag`, not `pass`, because final investor readiness gaps remain.
2. `SWU-BP-001` is selected and executable as local-fallback work.
3. Mutation-capable drafting of `business-plan.md` is blocked until registry and financial assumptions exist.
4. Investor use is blocked until claim audit completes and founder decides ask/runway.
5. Public promotion is blocked; this package stays private.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-07-10 | Initial invoke plan work-pack created. | Codex |
| 2026-07-10 | Completed SWU-BP-001 through SWU-BP-004 as a flagged BP draft package. | Codex |
