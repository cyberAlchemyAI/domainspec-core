---
task: SWU-RDL-002
mode: lean-strict
status: pass
createdAt: 2026-07-14T21:59:23Z
session_evidence: true
source_count: 8
obligation_coverage: 100%
---

# Context Pack: SWU-RDL-002 Semantic-event Oracle

This is Task Session evidence, not a reusable source-of-truth document.

## Objective

Define one strict, event-specific message schema plus positive/negative fixtures
and tests for the five Roadmap Lab event names. Prove that every valid message
composes into the existing generic Canvas request without modifying or
registering DomainSpec semantics in the IDE kernel.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| E1 | Cover orientation, restatement, source request, improvement proposal, and proposal disposition. | Implementation plan semantic-event table | covered |
| E2 | Cover all five proposal classes with class-specific target requirements. | UX proposal-class table | covered |
| E3 | Require participant/node/target and input-fingerprint fields where the designed event requires them. | Implementation plan and architecture RDL-O02/O03 | covered |
| E4 | Keep Canvas surface/revision bindings immutable and parent-owned. | Existing exact postMessage adapter and generic Canvas schema | covered |
| E5 | Reject extra fields, wrong types, arrays, absent bindings, path traversal, class mismatch, disposition without evidence, and oversized messages. | Task contract, generic 16 KiB boundary, test strategy | covered |
| E6 | Keep the contract private and validate again in the future review adapter; no runtime registration. | Architecture interface view and work-pack scope | covered |

## Selected Sources

| Source selector | Why included | Obligations |
| --- | --- | --- |
| `WORK-PACK.md` SWU-RDL-002 row and Gate Checks | exact scope/status/authority | E1–E6 |
| `TASK-RDL-CONTRACTS.md#SWU-RDL-002` | done criteria, invalid cases, validation | E1–E6 |
| `IMPLEMENTATION-PLAN.md#Semantic events`, `#Proposal admission` | five event payloads and double-validation rule | E1–E5 |
| `UX-PLAN.md#Proposal Classes` | class-specific target semantics | E2, E3 |
| `ARCHITECTURE-BUNDLE.md#RDL-O02`, `#View 6` | exact browser-to-Canvas composition and owner split | E3, E4, E6 |
| `projects/ide-extension/schemas/canvas-interaction-request.schema.json` | outer request oracle and 16 KiB-adjacent bounds | E4, E5 |
| `projects/ide-extension/public/demo/l0.html:1390-1432` | exact three-key message admission and parent binding injection | E4, E5 |
| `visibility/schemas/roadmap-copy.schema.json` | stable `field_id` shape for presentation-copy proposals | E2, E3 |

Selected excerpt budget: 136 lines across 8 files.

## Contract Decisions

### D-SWU002-01 — Match the real postMessage boundary

- Selected: schema the exact inner message shape
  `{type, eventName, payload}`. The semantic payload contains its own contract
  version and roadmap input fingerprint. Canvas `surface_id`/`revision_id` are
  injected only by the existing parent adapter and validated by the generic
  request schema.
- Reason: duplicating Canvas bindings inside user-originated payload would make
  them editable and create two competing values. The stored Canvas interaction
  already provides the required outer binding.
- Validation: every valid semantic fixture is composed with fixed outer
  bindings and must pass the current generic schema; payload attempts to provide
  `surface_id`/`revision_id` must fail.

### D-SWU002-02 — One discriminated union

- Selected: one private `roadmap-event.schema.json` with five exact event
  branches and reusable payload definitions.
- Rejected: five independent schemas, which would duplicate the exact message,
  fingerprint, participant, and target rules and make cross-event coverage
  harder to audit.

Both decisions are local contract-shape choices determined by live interfaces;
neither changes product authority. Decision Gate is not required.

## Semantic Size Limit

Use 12 KiB for the complete three-key Roadmap message. This stays below the
existing 16 KiB complete Canvas request limit and leaves space for outer schema,
surface, and revision fields. String/array bounds remain explicit in schema;
the focused contract test enforces total serialized UTF-8 size.

## Write Scope And Dirty Gate

Allowed:

- new `visibility/schemas/roadmap-event.schema.json`;
- new `visibility/tests/fixtures/roadmap-events/*.json`;
- new `visibility/tests/test_roadmap_event_contracts.py`;
- this session's context/result and planning synchronization.

Read-only: existing IDE Canvas schema/UI, roadmap copy schema, builder/template,
manifest, generated outputs, Craft state, and public Arcanum.

The product paths do not exist, so no current file overlap is present. Recorded
read-only hashes:

- Canvas schema: `249f508d57e115a11f2872f415bcee7a0ce8ce8e5cb52be7bfbbeac8c0e044de`;
- `l0.html`: `b6a4d62eeaf2c23732c97d8b5cb986688f541f2c4987dc2964812275ffecae0b`;
- copy schema: `67a08dfa6c7d368b5ddb6c55ee63d0d3a86e451e5baeb1f9614e43639a3edf94`.

## Validation

```bash
python3 -m unittest discover \
  -s projects/domainspec-v2/development/first-production-release/visibility/tests \
  -p 'test_roadmap_event_contracts.py'
```

Also run JSON parsing, schema meta-validation, valid event/class coverage,
invalid-reason matrix, generic Canvas composition, size checks, and read-only
hash verification.

## Context Builder Result

- Mode: lean, strict.
- Files selected: 8.
- Obligations: 6/6 covered.
- Noise ratio: low.
- Handoff pack: none; local execution.
- Strict coverage: pass.
- Blockers: 0.

