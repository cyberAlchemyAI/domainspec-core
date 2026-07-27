# Invoke Plan Context

## Implementation Objective

Create the first executable trust proof for the future
`projects/co-op-engine/` application: one dependency-light TypeScript
`ProjectRecord` admission contract and a normalized Poker Agent Arena fixture
that prove a record is admitted only when its truth, owner, freshness, claim,
experiment, policy, and field-visibility obligations close.

This Plan does not build the recruitment page or presentation. It creates the
contract those projections must later consume.

## Approved Design References

| Source | SHA-256 | Plan use |
| --- | --- | --- |
| `ARCHITECTURE-BUNDLE.md` | `9a4895d5cd5cacf2f4b6266d29a04805e1acf6241ac87127e49b4ae7a137b375` | component, state, privacy, layering, and witness boundaries |
| `UX-PLAN.md` | `5f03795cc111311133ac4b6428fc66eb1bd97faf0f3f513175731f2e017b09b5` | later browser and reader acceptance; explicitly deferred from L0 |
| `DESIGN-SELECTION-RESULT.json` | `0764f8564d9fb7eccfdaf15260f1dc09392e7a557b4da85001cdfa6795874379` | `design-validator-pass` and selected concern set |
| `DESIGN-ACCEPTANCE-REVIEW.md` | `1c0418d8398e0e59bc8dbcbe3c714659009c92bb3148a473f104cd740013f140` | accepted Plan boundary and prohibited shortcuts |
| `DESIGN-TRANSPORT.md` | `4159507eafa6977162838c711b0dbd435741f4a03b6fb7bcf841b0dd12dc8f05` | evidence ceiling and next-owner route |
| `UX-EVIDENCE-ACCEPTANCE.md` | `4f165da2d355d2290c90171cabf2ab15cff10efafe0160c87b4451ad9fa4d3a8` | later fixture/harness contract; not an L0 execution claim |

## Delivery Boundary

Included:

- create `projects/co-op-engine/` as the selected project home;
- add a private package manifest with a contract-test command;
- define the `ProjectRecord`, `VisibilityClass`, admission result, and typed
  diagnostic shapes;
- implement one deterministic `admitProjectRecord(record, asOf)` decision;
- normalize the accepted Poker research fixture to the approved 72-hour policy;
- test one admitted fixture and independent failure cases for policy mismatch,
  staleness, missing required truth, and unclassified required fields.

Excluded:

- React, Vite, HTML, CSS, routes, browser rendering, presentation mode;
- collaboration transitions, offers, appointments, receipt persistence;
- network, identity, backend, Sites project, hosting metadata, or deployment;
- fourteen-card materialization;
- Whisper copy and all browser/copy/comprehension audits;
- public release.

## Planning Input Decisions

- Active layer: L0.
- Complexity: medium because the new project requires multiple source/test
  artifacts and split planning evidence, despite having one task.
- Output mode: split.
- Selected first unit: `SWU-COOP-001`.
- Execution owner: local fallback through native Codex goal/Task Session
  semantics; no new subagent dispatch.
- Node baseline: repository runtime `v22.12.0`; use built-in test runner and
  type stripping to avoid introducing package dependencies in L0.
- Planning unknowns: none affecting L0 acceptance.

## Context Builder Readiness

Source anchors, related-context hints, write scope, validation command,
expected result shape, and closeout synchronization targets are complete for
`SWU-COOP-001`. Strict runtime packs are deliberately deferred until after
Plan selection.
