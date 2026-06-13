---
node: boundary-and-canon
docType: invoke-development
status: flag
updatedAt: 2026-06-13
sourceLedger: docs/strategy/development/boundary-and-canon/.craft/ledger.yml
sourceBuildSpec: docs/strategy/development/boundary-and-canon/BUILD-SPEC.md
dispatch: docs/strategy/development/non-strict-coding-node-invoke/NON-STRICT-CODING-INVOKE.dispatch.json
---

# Invoke Development - Boundary and Canon

## Invoke Result

- Mode: define -> design -> plan
- Phase status: flag
- Target artifact: boundary-and-canon governance authoring package
- Template family: governance decision packet
- Coding boundary: no code, runtime, ledger closure, or canon mutation in this artifact
- Next route: operator decision, then Craft ledger update

## Non-Strict-Coding Classification

This node is selected because its current work is governance and vocabulary
ratification. The blocking item is `DEC-BC-POSTURE-VOCAB`, not a coding task.
`DEC-BC-UI-BOUNDARY` is also a phase decision: read-only projection,
later-phase interactive surface, or out-of-scope for v0.1.

## Define Artifact

Objective: align workbook-derived language with locked Golden Quill canon before
downstream nodes harden artifacts.

Source contracts:

- `docs/golden-quill-task-role-breakdown-handoff.md`
- `AGENTS.md` deployment posture vocabulary
- `CLAUDE.md` v0.1 headless and product-boundary notes
- `docs/strategy/development/boundary-and-canon/BUILD-SPEC.md`

Terms:

- `Frontier-Eligible`
- `Split-Context Hybrid`
- `Local-Only / Sovereign`
- `Sanitized` as deprecated, not a posture
- `read-only projection` as distinct from an interactive UI

Open decisions:

- `DEC-BC-POSTURE-VOCAB`: ratify the 4-to-3 posture translation table.
- `DEC-BC-UI-BOUNDARY`: phase the operator console row without violating the
  v0.1 headless-only lock.

## Design Artifact

Context view: this node protects downstream engineering and customer-facing
surfaces from stale workbook vocabulary.

High-level structure: one blocking posture decision, one UI phase decision, and
three clean-up rules.

Low-level components:

- posture translation table;
- UI phase options;
- `Municipal` -> `Public Agency` clean-up;
- `Sovereign-mode` -> `Local-Only / Sovereign posture` disambiguation;
- external terminology-risk research remains deferred.

Workflow process: Josh ratifies the posture table, chooses the UI phase option,
then a separate Craft update records the decision and downstream nodes consume
the corrected terms.

Decision flow: if posture ratification is absent, keep the node at block. If UI
phase is absent, runtime console rows remain non-executable.

Dependency interface: unblocks `tilth-runtime-build` posture canon and
`node-on-desk-readiness` canon vocabulary gates.

## Plan Artifact

Implementation layering for this authoring pass:

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Do we have the correct canon translation? | Ratify posture table. | `DEC-BC-POSTURE-VOCAB` selected. |
| L1 | Can workbook rows be rewritten without scope drift? | Apply clean-up map to authoring surfaces. | No `Sanitized` posture survives. |
| L2 | Can downstream nodes consume the correction safely? | Record downstream dependency notes. | TRB and NOD gate references updated. |
| L3 | Can public/buyer language be hardened later? | Optional terminology-risk research. | External research approval or deferral. |

Work-pack:

| Task ID | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| BC-AUTH-001 | Ratify posture vocabulary table. | Craft decision record only after Josh approval. | Three posture terms only. |
| BC-AUTH-002 | Decide UI phase boundary. | Craft decision record only after Josh approval. | No interactive v0.1 UI. |
| BC-AUTH-003 | Prepare downstream clean-up checklist. | Planning artifacts. | References TRB and NOD dependencies. |

SWU handoff:

| SWU ID | Parent Task | Done Criteria | Execution Owner |
| --- | --- | --- | --- |
| SWU-BC-001 | BC-AUTH-001 | Josh-approved selected option and rationale captured. | manual |
| SWU-BC-002 | BC-AUTH-002 | UI row phase selected without breaking headless lock. | manual |
| SWU-BC-003 | BC-AUTH-003 | Downstream node references list is complete. | local-fallback |

Residue: operator approval remains required. This artifact does not close the
Craft blocker.

