# Context Pack: SWU-SCW-004

## Selection

- Task/SWU: `TASK-PUBLISH-DISPLAY / SWU-SCW-004`
- Mode: standard, local Task Session
- Dependency: SWU-SCW-003 PASS

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Add full-width unframed canvas with compact controls. | UX plan and task rules. | covered |
| O2 | Fetch current metadata and display complete revision after Refresh. | SWU-003 API contract. | covered |
| O3 | Preserve current iframe until replacement loads. | Implementation plan failure rules. | covered |
| O4 | Preserve Approval Desk flows and selectors. | Existing workbench/Playwright tests. | covered |
| O5 | Support trusted-local interactive HTML. | DG-SCC-002 and actual Craft presentation. | covered |
| O6 | Prove desktop/mobile layout and real presentation controls. | W1 exit gate and Playwright. | covered |

## Execution Decisions

- Place Canvas as a full-width band below the compact three-column desk.
- Preflight the content URL, load a hidden replacement iframe, then atomically
  swap it into view on `load`; failures preserve the current iframe.
- Existing general Refresh updates both proposal state and Canvas; Canvas also
  has its own focused Refresh control.
- Use the existing Craft causal class presentation as the realistic browser
  fixture without modifying it.

## Gates

- Dependency/context/write scope/validation: pass.
- Blocker decisions: none.
- Strict coverage: pass, six of six obligations.

## Required Evidence

- Static workbench selectors and script syntax pass.
- Actual presentation title and controls work in iframe.
- Desktop and 390px have no page overflow or overlapping Canvas controls.
- Existing Approval Desk Node and Playwright suites remain green.
