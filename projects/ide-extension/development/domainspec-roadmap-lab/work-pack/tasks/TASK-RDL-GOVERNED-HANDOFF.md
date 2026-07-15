# Task Contract: Governed Proposal Handoff

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-RDL-GOVERNED-HANDOFF` |
| Objective | Revalidate and route proposals to their real owner without executing protected effects. |
| Layer / slice / wave | L2 / S-004 / W3 |
| Dependencies | SWU-RDL-008 pass |
| Blockers | Owner routes must remain references; unavailable owners do not justify a generic effect path. |
| Execution | Sequential: packet/classifier before disposition projection. |

## Sources

- [RDL-O03 route flow](../../ARCHITECTURE-BUNDLE.md#rdl-o03-route-and-review-a-proposal)
- [Proposal classes](../../UX-PLAN.md#proposal-classes)
- IDE Whisper/Craft manifests and their forbidden effects.
- [Glossary distinctions](../../GLOSSARY-CONSISTENCY.md)

## SWU-RDL-009 — Review packet and owner classification

- **Objective:** Convert one polled proposal event into a bounded, revalidated
  review packet for copy, graph/claim, Craft continuation, research, or
  unsupported protected action.
- **Dependencies:** SWU-RDL-008.
- **Write scope:** new visibility review-packet schema, local deterministic
  adapter/tool, fixtures, and tests. No owner invocation and no IDE effect API.
- **Rules:** revalidate semantic event; verify Canvas/event binding; compare
  current fingerprint/target/original; preserve raw proposal by handle; classify
  from explicit class only; name target owner and expected evidence; stale or
  unsupported results fail closed; output contains no absolute private paths.
- **Edge cases:** tampered class, missing field, copy proposal aimed at graph
  claim, continuation request that implies closure, source evidence absent,
  unknown event/schema version, duplicate proposal, stale target.
- **Done:** all five outcomes are deterministic, schema-valid, and contain no
  claim of execution/acceptance.
- **Acceptance evidence:** fixture matrix with expected route/status, packet
  samples, and no-direct-effect code/review assertion.
- **Validation:** focused Python schema/adapter suite and deterministic output
  comparison.
- **Owner:** `local-fallback`.
- **Handoff:** pass packet/evidence-reference contract to SWU-RDL-010; actual
  owners receive packets only in a separately authorized runtime route.

## SWU-RDL-010 — Receipt-backed disposition projection

- **Objective:** Show review progress without allowing a local event to become
  owner authority.
- **Dependencies:** SWU-RDL-009.
- **Write scope:** visibility disposition contract/fixtures/adapter tests and
  focused IDE history projection/tests only.
- **Rules:** accept statuses only from the designed state machine; require owner
  route and stable evidence reference; distinguish handoff accepted from
  proposal accepted; `applied-with-evidence` requires application proof fields;
  ignore/reject unknown transitions; render explanation and original proposal.
- **Edge cases:** acceptance without evidence, applied before accepted, rejected
  after applied, status from browser proposal event, stale proposal accepted,
  missing owner, duplicate/superseding receipt.
- **Done:** browser projection can display submitted/stale/under-review/accepted/
  rejected/applied while source of truth stays owner-held.
- **Acceptance evidence:** valid/invalid transition table, UI snapshots, and
  concrete evidence-handle preservation.
- **Validation:** focused schema/adapter/Node/Playwright tests plus Canvas event
  regressions if shared UI changes.
- **Owner:** `local-fallback`.
- **Handoff:** W3 governance mechanics proceed to degraded-mode proof in 011.

## Synchronization And Completion

The adapter may prepare a handoff; it may not invoke Whisper, mutate Craft,
rewrite DomainSpec, start research, or promote a claim. Any such execution is a
new owner-governed dispatch outside this task.

