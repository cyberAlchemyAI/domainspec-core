---
artifact: ui-prototyping-studio-interface-workbench-plan-redistill-findings
dispatch_id: 2026-07-27-ui-prototyping-studio-plan-redistill-review
verdict: BLOCK
authority_effect: none
---

# Plan Redistill Review — Verified Findings

## Verdict

**BLOCK.** The remediated Plan passes its 19-row mechanical denominator checks,
but it does not satisfy the Invoke Plan atomicity and exact-closeout gates.
Four MAJOR findings and two MINOR findings survive literal verification.

This is a Plan verdict only. No product test ran, no SWU was selected, no
implementation evidence was produced, and no release, human-study, or
production authority changed.

## Closeout And W5 Contracts

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| PRD-01 / PD-10 | `CLOSEOUT-SYNC-INVENTORY.json`; `WORK-PACK.md`; `EXECUTION-PACK.md`; `PLAN-TRANSPORT.md`; `work-pack/tasks/TASK-UPW-VERIFY.md` | `CLOSEOUT-SYNC-INVENTORY.json:18-58` names abstract writable fields such as `control.lastUpdatedAt`, `receiptInventory`, and `nextRoute`, but the Markdown targets provide no canonical selectors/parser contract for those names. It also permits selection-field writes while `:70` says the successor is never auto-selected. `CLOSEOUT-SYNC-INVENTORY.json:187-264` and `TASK-UPW-VERIFY.md:22-70` name the closure report and its fields but provide no material schema, field types/cardinalities, enumerated six-view/seven-extension truth table, command-result shape, or deterministic verdict/owner function. | MAJOR | Materialize parsable receipt/report schemas and canonical Markdown selectors or JSON pointers; make selection fields preservation-only; define deterministic W5 cardinality, truth-table, verdict, and owner routing validation. |

Artifact verdict: **FIX**. Enumerated paths and rows are not yet an executable
field-level synchronization contract. This blocks Plan pass.

## Hardening SWU Atomicity

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| PRD-02 / PD-05 | `work-pack/tasks/TASK-UPW-HARDENING.md`; `SWU-ACCEPTANCE-MATRIX.json` | SWU-016 combines activation/handler parity and focus transition with live-scope destination, atomicity, and urgency (`TASK-UPW-HARDENING.md:22-42`; `SWU-ACCEPTANCE-MATRIX.json:159-167`). Those child behaviors have independently failing mutants and can pass separately. | MAJOR | Split activation/focus from scoped-status/live-urgency, with one primary assertion and receipt per child. |
| PRD-03 / PD-05 | `work-pack/tasks/TASK-UPW-HARDENING.md`; `SWU-ACCEPTANCE-MATRIX.json` | SWU-017 combines contrast/focus/non-color perceivability with target geometry (`TASK-UPW-HARDENING.md:44-66`; `SWU-ACCEPTANCE-MATRIX.json:169-177`). Perceivability and geometry can pass and fail independently. | MAJOR | Split visual perceivability from target geometry, with one primary assertion and receipt per child. |
| PRD-04 / PD-06 | `work-pack/tasks/TASK-UPW-HARDENING.md`; `SWU-ACCEPTANCE-MATRIX.json`; `SWU-MANIFEST.json` | SWU-019 combines iframe sandbox admission with safe outer-data sinks (`TASK-UPW-HARDENING.md:96-116`; `SWU-ACCEPTANCE-MATRIX.json:189-197`). The mutant classes can pass independently. Its all-outer-data claim also omits inspector/history owners 010/013 from the dependencies at `SWU-MANIFEST.json:214-220`. | MAJOR | Split sandbox admission from safe outer rendering; bind the safe-sink child to every covered outer-region receipt, including 010 and 013. |

Artifact verdict: **FIX**. SWU-016, SWU-017, and SWU-019 are task-shaped under
the literal Invoke Plan rule that independently passable children must be
split. This blocks Plan pass and invalidates the current 19-unit recomposition
as an execution handoff.

The 003/018 server boundary and 006/007 plan/commit boundary remain **KEEP**.
SWU-018 remains **KEEP** as the server route-admission unit.

## Admission And Coordinator Precision

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| PRD-05 | `SWU-SCOPE-INVENTORY.json`; `PLAN-VALIDATION-STRATEGY.md`; `CLOSEOUT-SYNC-INVENTORY.json` | SWU-008 creates `workbench-regions.spec.ts`, later treated as existing by 009–013; 016 similarly creates the 017 spec (`SWU-SCOPE-INVENTORY.json:112-188,218-238`). The current per-SWU gate requires serialization predecessors only to be terminal (`PLAN-VALIDATION-STRATEGY.md:13-23`). Safe preflight blocks mutation, but eligible human selection is not explicitly restricted to passing synchronized creator receipts. | MINOR | Add creator-receipt requirements or `path_created_by` bindings and restrict human selection to the current passing-and-synchronized eligible candidate. |
| PRD-06 | `work-pack/tasks/TASK-UPW-COORDINATOR.md`; `WITNESS-CONTRACTS.md` | SWU-005 compares `flightStartedAt` with an undefined action completion boundary (`TASK-UPW-COORDINATOR.md:38-53`), while the witness contract already requires request/response sequence identities. | MINOR | Replace wall-clock-style comparison with monotonic flight/action sequence identities and specify atomic trailing-slot consumption under concurrent completion. |

Artifact verdict: **FIX, non-blocking in isolation**. These repairs are required
when the blocking Plan remediation regenerates the candidate.

## PD-01 Through PD-10

| Finding | Final disposition |
| --- | --- |
| PD-01 | **Closed as originally framed.** All 19 candidate rows have exact existing/create/forbidden authority. PRD-05 adds creator-receipt precision. |
| PD-02 | **Closed.** SWU-002 defines the store token, exact equality, retry limit two after the initial attempt, and typed exhaustion. |
| PD-03 | **Closed.** SWU-003 is current-constructor-only; SWU-018 owns reusable route admission. |
| PD-04 | **Closed.** SWU-006 is pure planning; SWU-007 owns journal/commit/rollback. |
| PD-05 | **Open — MAJOR.** SWU-016 and SWU-017 each contain independently passable children. |
| PD-06 | **Open — MAJOR.** SWU-019 contains independently passable sandbox and safe-sink children. |
| PD-07 | **Closed.** Candidate SWUs 008–013 have exact spec/test names, positive assertions, negative mutants, and receipt fields. |
| PD-08 | **Closed.** Candidate primary assertions and receipt fields are unique; shared witnesses are non-primary. |
| PD-09 | **Closed as originally framed.** Semantic and serialization edges are distinct; PRD-05 remains a bounded eligibility precision repair. |
| PD-10 | **Open — MAJOR.** Closeout fields are not literally addressable and W5 lacks an executable schema/decision contract. |

## Denominator Disposition

### SWUs

| Candidate SWU | Disposition |
| --- | --- |
| SWU-UPW-001 | KEEP; narrowest reversible recommendation, unselected |
| SWU-UPW-002 | KEEP |
| SWU-UPW-003 | KEEP |
| SWU-UPW-004 | KEEP |
| SWU-UPW-005 | FIX for PRD-06 |
| SWU-UPW-006 | KEEP |
| SWU-UPW-007 | KEEP |
| SWU-UPW-008 | KEEP |
| SWU-UPW-009 | KEEP |
| SWU-UPW-010 | KEEP |
| SWU-UPW-011 | KEEP |
| SWU-UPW-012 | KEEP |
| SWU-UPW-013 | KEEP |
| SWU-UPW-014 | KEEP |
| SWU-UPW-015 | KEEP |
| SWU-UPW-016 | SPLIT / blocking |
| SWU-UPW-017 | SPLIT / blocking |
| SWU-UPW-018 | KEEP |
| SWU-UPW-019 | SPLIT / blocking |

SWU-UPW-001 remains the narrowest reversible recommendation and remains
unselected. All 19 candidate rows remain `not-started`.

### Tasks And Waves

| Task / wave | Disposition |
| --- | --- |
| `TASK-UPW-PROJECTION` / W0 | KEEP |
| `TASK-UPW-COORDINATOR` / W1 | FIX for PRD-06 |
| `TASK-UPW-REGIONS` / W2 | KEEP |
| `TASK-UPW-RESPONSIVE-COPY` / W3 | KEEP |
| `TASK-UPW-HARDENING` / W4 | FIX / blocking; regenerate for three required splits |
| `TASK-UPW-VERIFY` / W5 | FIX / blocking; materialize deterministic closure contract |

### Layers And Machine Inventories

- L0 remains coherent but carries the SWU-005 precision repair.
- L1 remains coherent.
- L2 is blocked by the hardening splits and W5 contract.
- L3 remains an external human/readiness boundary with no implementation SWU.
- `SWU-MANIFEST.json`: FIX for new child IDs, dependencies, serialization,
  successors, and count.
- `SWU-SCOPE-INVENTORY.json`: FIX for child scopes and creator-receipt
  admission.
- `SWU-ACCEPTANCE-MATRIX.json`: FIX for new primary assertions, mutants, and
  receipt fields.
- `CLOSEOUT-SYNC-INVENTORY.json`: FIX for new rows, literal mutation selectors,
  selection preservation, receipt schemas, and W5 schema/routing.

UPW-FIX-001 through UPW-FIX-024 remain mapped as Plan assertions. They remain
planned and unexecuted; mapping coverage is not runtime proof.

## Recomposition, Navigation, And Residue

- The current mechanical sequence through 19 candidate SWUs is internally
  referentially valid but is not an executable recomposition proof because
  SWU-016, SWU-017, and SWU-019 must split.
- The regenerated sequence must reprove all four machine inventories, six task
  contracts, W0–W5 mapping, closeout rows, and first-unit navigation.
- No further split is required for 003/018 or 006/007.
- Human outcomes, cross-browser generalization, accessibility certification,
  remote origins, release, deployment, and production readiness remain outside
  this Plan verdict.
- The verifier's first call failed before evidence because its transport stream
  disconnected. The user explicitly authorized one retry; only the successful
  verifier return is review evidence.
- The coverage auditor rejected the stale synthesis candidate because it had
  not propagated the verified PD-05/PD-06 findings and their denominator
  effects. This final artifact incorporates each named missing denominator.

## Ordered Change Requests

1. Split SWU-016 into activation/focus and scoped-status/live-urgency children.
2. Split SWU-017 into visual-perceivability and target-geometry children.
3. Split SWU-019 into iframe-sandbox and safe-outer-rendering children, binding
   the latter to every covered outer-region receipt.
4. Replace abstract closeout permissions with parsable selectors/pointers,
   preservation-only selection rules, checked schemas, and deterministic W5
   validation/routing.
5. Regenerate the manifest, scope, acceptance, closeout, task, wave, layering,
   execution, transport, and traceability denominators; reprove recomposition.
6. Add passing creator-receipt eligibility to predecessor-created paths.
7. Replace SWU-005 timestamp ordering with monotonic coordinator identities.
8. Run a new mechanical validation and fresh governed Plan Distill. Until it
   passes, keep `selected_swu: null` and Task Session blocked.
