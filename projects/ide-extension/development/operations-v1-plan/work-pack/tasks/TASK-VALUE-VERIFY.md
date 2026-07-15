# Task Contract: Agent Workflow Value Proof And Closeout

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-VALUE-VERIFY` |
| Objective | Prove a normal agent can create, operate, show, and interact with HTML through the local workbench, then close only the supported claim. |
| Layer / slice / wave | L2 / OV1-S7 / W6 |
| Execution owner | Task Session, one SWU at a time |
| Execution status | completed; SWU-OV1-013 passed machine proof plus human Option 1 usefulness review, and SWU-OV1-014 passed integrated closeout. |

## Source Handles

- [Honest claim](../../../operations-v1-design/ARCHITECTURE-BUNDLE.md#honest-claim)
- `projects/ide-extension/scripts/session-bridge.mjs`
- `projects/ide-extension/tests/e2e/session-content-workbench-matrix.spec.mjs`
- [Traceability](../shared/traceability.md)

## SWU-OV1-013: CLI And Interactive Value Witness

**Goal:** expose concise agent commands and retain a real end-to-end HTML
presentation workflow in the workbench.

**Dependencies:** SWU-OV1-012 pass.

**Exact write scope:** `scripts/session-bridge.mjs`, CLI tests, Operations V1
fixtures/Playwright witness, evidence report/screenshots, package test scripts,
and Task Session evidence. Core kernel semantics change only for a proven CLI
binding defect and must remain within prior contracts.

**CLI surface:** add machine-readable commands for `derive`, `operate`,
`navigate`, `storage`, and `prune`; preserve existing commands and JSON stdout/
stderr exit behavior. HTML may be provided inline or from an admitted project
file according to the operation mode; the CLI does not bypass API limits,
hashes, CAS, or path admission.

**Witness:**

1. Create a complete interactive presentation HTML inside a temporary project.
2. Publish it through unchanged V0.
3. Derive an Operations V1 surface from the exact revision.
4. Replace or rebuild, then append one visible interactive section with a fresh
   operation id and expected revision.
5. Redirect the durable workbench target to the result.
6. Confirm automatic complete-revision reload and interact inside the iframe.
7. Poll the resulting generic canvas event through the existing session path.
8. Restart server/browser and confirm the target and immutable content recover.

Automated evidence includes exact CLI JSON, event/revision counts, content
digests, browser assertions, and desktop/mobile screenshots. The Task Session
also pauses for explicit human usefulness review of the retained workbench
result; without that review it returns `block`, not simulated approval.

**Done criteria:** machine proof passes and the operator confirms the workbench
result is useful enough to proceed to integrated closeout.

**Validation:** `npm run test:operations-value` and retained manual review
record.

**Execution owner:** local fallback plus human review. **Expected result:** pass
or honest human-review block with evidence path. **Handoff:** SWU-OV1-014 only
after pass.

## SWU-OV1-014: Integrated Audit And Plan Synchronization

**Goal:** close traceability with full evidence and no broader claim.

**Dependencies:** SWU-OV1-013 pass including human review.

**Exact write scope:** tests only for a discovered acceptance regression;
otherwise work-pack evidence, statuses, traceability, Invoke/Task Session
receipts, and observability. Product/design authority files are read-only.

## Smallest Working Unit Exemption

This is the one closure-only `VERIFY` unit represented by this task section; it
does not decompose further.

**Audit:** run all focused Operations V1 scripts, existing V0 canvas/bridge/
persistence/schema suites, full Playwright desktop/mobile journeys, dispatch
validation, JSON/JSONL checks, and scoped diff review. Map every OV1-D/OVG item
to an evidence path and classify remaining gaps.

**Closure claim:** only report that a trusted local agent can derive an
immutable surface from an exact V0 revision, apply retry-safe whole-document
operations, and display committed complete revisions without changing V0.
Explicitly deny regions, collaboration, automatic merge, hostile HTML safety,
remote control, and protected-effect execution.

**Done criteria:** all accepted obligations have retained evidence; work-pack,
waves, tasks, and traceability agree; no active blocker remains; unrelated
worktree changes are untouched.

**Validation:** reviewable integrated report containing exact commands, counts,
artifacts, remaining residue, and scoped diff result.

**Execution owner:** local fallback. **Expected result:** completed work pack or
block with the exact failed obligation and reroute.

## Synchronization

Only SWU-OV1-014 may mark the package complete. Human usefulness review is
evidence for the local workbench value claim, not authority for deferred L3.
