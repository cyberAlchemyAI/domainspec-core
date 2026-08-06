---
module: ontology-video-animejs-prototype
version: 1.1.0
status: completed
updatedAt: 2026-08-06T13:57:30Z
docType: work-pack
---

# WORK-PACK: Ontology Video Anime.js Prototype — OAVA-002

## Purpose and claim boundary

This one-unit Work Pack implements the candidate-local consultation gate between the completed source/candidate contract (`SWU-OAVA-001`) and the first runtime-admission unit (`SWU-OAVA-003`). It captures only `SWU-OAVA-002`.

Completion may prove that one deterministic animation candidate can consult the existing local Anime.js knowledge vault and that stale, abstaining, denied, invalid, failed, or evidence-empty consultations remain ineligible. It does not prove an Anime.js animation, browser behavior, visual quality, HTTP behavior, vault mutation, ontology authority, publication, deployment, or production readiness.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | OAVA-002 was selected, admitted once, applied, and validated within the four-file boundary. |
| complexity | medium | Consumer integration, trust boundaries, and causal negative cases require a split task contract. |
| outputMode | split | Detailed behavior is owned by `work-pack/tasks/TASK-OAVA-CONSULTATION.md`. |
| executionPackRef | `EXECUTION-PACK.md` | Portfolio sequencing authority; OAVA-003–008 stay outside this pack. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | OAVA-002 closes L0 trust and consultation. |
| dispatchTechniqueTrace | `REFINE-DISPATCH.json`; bounded read-only plan audit | No governed multi-agent implementation dispatch is declared. |
| distillValidationStatus | pass | Validate mode selected OAVA-002 as the smallest coherent consultation unit. |
| swuAtomicityStatus | pass | Builder, adapter, eligibility gate, and causal tests are one consumer behavior; splitting them would leave a fail-open intermediate state. |
| firstUnitNarrownessStatus | pass | Runtime admission, DOM/SVG, timeline, browser, review, and episode work are excluded. |
| closeoutSyncStatus | pass | One complete receipt-bound closeout row is declared below. |
| admissionTiming | selected-unit-at-task-session | Material and live target baselines bind only after explicit selection. |
| executionEntryState | completed | The one-unit frontier is terminal; OAVA-003 is exposed but not selected or executed. |
| activeLayerWindow | L0 | Candidate consultation only. |
| readinessProfile | pilot | Target profile only; evidence remains candidate-local. |
| lastUpdatedAt | `2026-08-06T13:57:30Z` | Receipt-backed closeout timestamp. |

## Objective and acceptance

- Build the S6 animation candidate deterministically from source-bound inputs and residue.
- Consult the canonical local vault through its existing `animejs-knowledge-consult-read` capability and transport-neutral service.
- Return exact record and evidence identities for the timeline, SVG, and `createDrawable` guidance used by the proposed edge draw.
- Bind the receipt to the candidate without raising any proof state above `planned_motion`.
- Admit tournament eligibility only when candidate validation passes, the receipt is current and `ok`, exact evidence is non-empty and bound, contradiction status is clear, and standard/reduced terminal meaning matches.
- Prove every non-`ok` status and stale digest blocks; prove canonical vault bytes remain unchanged.

## Work-Pack execution policy

The machine contract is `work-pack/execution-contract-oava002.json`. Its captured frontier is exactly `SWU-OAVA-002`; its only implementation route is Task Session over four exact material paths. The route has repository-local reversible effects only and stops on source drift, vault drift, unexpected writes, network effects, or failed acceptance-critical validation.

## Active SWU handoff

| SWU | Parent | Behavior | Dependencies | Exact write scope | Done criteria | Validation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SWU-OAVA-002` | `TASK-OAVA-CONSULTATION` | Build, consult, bind, and fail-close one source-bound S6 candidate. | Completed `SWU-OAVA-001` closeout | `prototype/lib/build-candidate.mjs`; `prototype/lib/consult-animejs.mjs`; `prototype/lib/evaluate-eligibility.mjs`; `prototype/test/consultation.test.mjs` | Exact evidence IDs returned and bound; current `ok` path is eligible; all non-`ok`, stale, empty, or mismatched paths block; source and vault zero delta | `node --test prototype/test/consultation.test.mjs`; `node --test prototype/test/candidate.test.mjs` | completed |

## Dependency evidence

- `WORK-PACK.md` is the immutable completed OAVA-001 plan.
- `work-pack/closeouts/SWU-OAVA-001.json` is the joined terminal closeout.
- `prototype/test/candidate.test.mjs` passes and remains a prerequisite regression check.
- The canonical vault operational validator remains independently owned; OAVA-002 imports its public local-library surfaces but does not mutate them.

## Explicit exclusions

- No changes under `projects/animejs/ontology/agent-knowledge-vault/`.
- No changes to source media, AutoAds, public Arcanum, the vendored Anime.js runtime, Git, network, deployment, or publication state.
- No HTTP route, server, credentials, remote fetch, package root, Anime.js runtime execution, DOM/SVG scene, timeline, browser witness, reviewer disposition, WorkEpisode, Lesson, or ontology promotion.

## Task Session Closeout Sync Contract

| SWU ID | Lifecycle Owner Route | Terminal Source Receipt Contract | Declared Target Inventory | Baseline Binding | Allowed Delta Classes | Owner Validation | Expected Owner Receipt | Successor Policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SWU-OAVA-002` | `invoke:refresh:apply-approved` | `task-session.governance-terminal-receipt.v1`; task `TASK-OAVA-CONSULTATION`; SWU `SWU-OAVA-002`; result `pass` | `WORK-PACK-OAVA-002.md`; `RUNTIME-HANDOFF-OAVA-002.md`; `work-pack/closeouts/SWU-OAVA-002.json` | Exact live SHA-256 and size immediately before owner apply; closeout JSON initially absent | `evidence_added`, `status_changed`, `route_changed`; blocker deltas only when the terminal receipt proves them | Rerun OAVA-001 and OAVA-002 tests; validate receipt shape; staged/applied equality; zero delta in source media, AutoAds, and canonical Anime.js vault | `work-pack/closeouts/SWU-OAVA-002.json` plus a joined Invoke Refresh receipt | Exactly `SWU-OAVA-003` on pass, `successor_executed=false`, and no runtime execution authority |

## Gates and continuation

1. Work Pack Readiness must freeze and pass this semantic frontier.
2. Implementation Readiness may select exactly OAVA-002 from the direct execution intent.
3. Task Session must bind a fresh material package, strict context, target baselines, single-use mutation admission, and closeout preflight before implementation writes.
4. A passing closeout may expose OAVA-003 only. It may not execute or claim the first visible animation.

No product or semantic choice is open inside OAVA-002. Any change to the S6 meaning, evidence topics, capability audience, runtime scope, or claim ceiling requires a new plan epoch.

## Completion evidence

- Task Session run `oava002-ts-20260806-001` consumed one plan-bound mutation admission and committed the four declared outputs.
- OAVA-002 consultation acceptance passed 8/8 and the OAVA-001 regression suite passed 7/7.
- The actual local consultation returned the exact timeline, SVG, and `createDrawable` records and evidence identities; stale and typed non-`ok` paths remained ineligible.
- The consultation test verified the canonical Anime.js vault byte map was unchanged, and the bounded execution ticket admitted no AutoAds, source-media, runtime, browser, network, public-Arcanum, or publication writes.
- Evidence ceiling remains candidate-local consultation readiness. There is still no Anime.js runtime or browser witness.
