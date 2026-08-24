# Plan Redistill Review — Synthesis Candidate

Status: `superseded-by-verification-and-findings`

Dispatch: `2026-07-27-ui-prototyping-studio-plan-redistill-review`

## Candidate Verdict

**BLOCK.** PD-01–PD-09 are closed as originally framed. PD-10 remains
**MAJOR** because the closeout/W5 contract is enumerated but not literally
executable or schema-validatable. Three additional non-blocking
execution-clarity flags survive.

No implementation evidence was produced, no product tests were run, no SWU was
selected, and no authority changed.

## Surviving Findings

| ID | Finding and exact artifact evidence | Severity | One-line repair | Affected scope | Plan-pass effect |
| --- | --- | --- | --- | --- | --- |
| PRD-01 / PD-10 | `CLOSEOUT-SYNC-INVENTORY.json:18-58` calls abstract names such as `control.lastUpdatedAt`, `control.selectedSWU`, `currentGate`, `receiptInventory`, and `nextRoute` writable, but the Markdown targets expose prose/frontmatter/tables rather than defined addressable fields (`WORK-PACK.md:1-30`; `EXECUTION-PACK.md:1-68`; `PLAN-TRANSPORT.md:1-66`). Selection fields are writable at `CLOSEOUT-SYNC-INVENTORY.json:21,26` despite the no-auto-selection policy at `:70`. W5 names a schema and field inventory (`CLOSEOUT-SYNC-INVENTORY.json:187-264`; `TASK-UPW-VERIFY.md:22-35`) but supplies no schema bytes, types/cardinalities, enumerated six-view/seven-extension truth table, or deterministic verdict/owner function (`TASK-UPW-VERIFY.md:47-70`). | **MAJOR** | Materialize parsable schemas and canonical Markdown selectors/JSON pointers, forbid selection-field mutation except preservation of `null`/`none`, and define a deterministic W5 cardinality/verdict/owner validator. | All 19 closeout rows; Work Pack, manifest, six task/wave surfaces, execution pack, transport, receipts, W5 report | **Blocks** |
| PRD-02 | SWU-008 creates `workbench-regions.spec.ts`, while 009–013 classify it as existing; 016 similarly creates the accessibility spec consumed by 017 (`SWU-SCOPE-INVENTORY.json:112-188,218-238`). Admission requires serialization predecessors only to be terminal (`PLAN-VALIDATION-STRATEGY.md:13-23`; `CLOSEOUT-SYNC-INVENTORY.json:60-70`). Safe preflight prevents mutation, but the Plan does not explicitly restrict human selection to an eligible passing-and-synchronized candidate. | MINOR | Add `path_created_by` or equivalent creator-receipt requirements and state that human selection is limited to the current eligible candidate. | 008–013, 016–017; per-SWU admission/selection | Does not independently block |
| PRD-03 | SWU-005 orders a flight against an action using `flightStartedAt` and an undefined “completion boundary” (`TASK-UPW-COORDINATOR.md:44-53`), while the approved witness accounting already requires request/response sequence IDs and trailing-refresh causes (`WITNESS-CONTRACTS.md:38-54`). | MINOR | Replace wall-clock-style comparison with monotonic flight/action sequence identities and specify atomic trailing-slot consumption under concurrent completion. | 005; W1; continuity receipt | Does not independently block |
| PRD-04 | SWU-019 claims safe sinks for **all outer data** and governs raw current/staged/history frames (`TASK-UPW-HARDENING.md:96-111`), but its semantic dependencies include only 009, 011, and 018 (`SWU-MANIFEST.json:214-220`), while Context Builder is limited to dependency receipts (`EXECUTION-PACK.md:35-40`). Inspector/history owners 010/013 are therefore absent from the declared context boundary. | MINOR | Add 010/013 as semantic/context dependencies or explicitly bind their synchronized receipts in 019’s handoff. | 019; W4; Context Builder handoff | Does not independently block |

## PD-01–PD-10 Disposition

| PD | Candidate disposition |
| --- | --- |
| PD-01 | **Closed.** Exact existing/create/forbidden scopes exist for all 19 SWUs; omitted paths are unauthorized and preflight-bound. PRD-02 is a later eligibility clarification, not a return to vague mutation scope. |
| PD-02 | **Closed.** SWU-002 names token owner, exact equality, retry limit 2, three-attempt exhaustion, and typed error (`TASK-UPW-PROJECTION.md:48-86`). |
| PD-03 | **Closed.** 003 is current-constructor-only; 018 alone owns reusable route admission (`TASK-UPW-PROJECTION.md:88-117`; `TASK-UPW-HARDENING.md:68-94`). |
| PD-04 | **Closed.** 006 is pure planning; 007 alone owns journal/commit/rollback (`TASK-UPW-COORDINATOR.md:60-103`). |
| PD-05 | **Closed with recorded disagreement.** The Plan gives coherent event-outcome and calibrated-visual boundaries for 016/017 (`TASK-UPW-HARDENING.md:22-66`). Abramsky favored further splitting; Rittel withdrew the blocking split demand. No mandatory further split survives as a verified finding. |
| PD-06 | **Closed.** 018 server admission and 019 browser rendering are distinct. Further subdivision of 019 is not established; only PRD-04’s context-binding flag survives. |
| PD-07 | **Closed.** 008–013 each have exact spec/name, positive, mutant, and receipt (`SWU-ACCEPTANCE-MATRIX.json:78-137`). |
| PD-08 | **Closed.** Nineteen unique primary assertions/receipt fields exist; shared witnesses are explicitly non-primary (`SWU-ACCEPTANCE-MATRIX.json:5-6,199-239`). |
| PD-09 | **Closed as originally framed.** Semantic and serialization edges are distinct and ordered; PRD-02/04 are bounded admission/context clarifications. |
| PD-10 | **Open — MAJOR.** Enumerated targets and receipts do not cure non-addressable mutation permissions or the absent executable W5 schema/decision contract. |

## Denominator, Recomposition, and Authority Audit

- The four inventories parse and contain the same 19 unique SWU IDs; their
  sorted-ID digest is
  `d37364601cd058997d23062482279644a6306c75822a21a80e60d77472f271d9`.
- There are 19 unique primary assertions and receipt fields, 19 execution
  receipts, 19 refresh receipts, and six Plan targets per closeout row.
- Six tasks and six waves are present. The manifest correctly contains five
  mutation-task/wave identities; `TASK-UPW-VERIFY`/W5 is the explicit
  closure-only exemption.
- L0–L2 contain the 19 implementation SWUs; L3 deliberately contains no
  implementation SWU and preserves external human/readiness ownership
  (`IMPLEMENTATION-LAYERING.md:13-27`).
- UPW-FIX-001–024 all appear in the acceptance matrix.
- SWU disposition: **KEEP 001–004; KEEP 005 with PRD-03; KEEP 006–018; KEEP
  019 with PRD-04.**
- SWU-001 remains the narrowest reversible recommendation: no dependency,
  create-only versioner/test pair, one digest assertion, and
  `selected_swu: null` (`SWU-MANIFEST.json:5-24`). It is not selected.
- Recomposition remains coherent:
  `001→002→003→004→005→006→007→008–013→014→015→016→017→018→019→W5`.
- Navigation/update accounting remains explicit in
  `WITNESS-CONTRACTS.md:38-58`; it is planned and unexecuted.
- Residue remains explicit: human outcomes, cross-browser generalization,
  certification, remote origins, release, deployment, and production readiness
  remain externally owned (`work-pack/shared/cross-task-gaps.md:15-25`).
- Refuted or withdrawn: “W5 lacks commands/report path” is false; blocking
  predecessor-failure sequencing was reduced to PRD-02 because preflight fails
  safely; 008–013 and FIX-022 ownership objections were withdrawn; mandatory
  further splitting of 016/017/019 did not survive consensus.
- Authority remains `none`: fresh Plan Distill is the current owner, Task
  Session remains blocked, and only the human/lifecycle owner may later select
  one SWU.

SYNTHESIS_COMPLETE
