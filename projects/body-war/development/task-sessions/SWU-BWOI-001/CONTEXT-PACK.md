---
module: body-war-suggested-track-ontology-witness
status: strict-coverage-pass
updatedAt: 2026-07-27
docType: task-session-context-pack
---

# Context Pack: SWU-BWOI-001

This is Task Session evidence, not a reusable source of truth.

## Selection

- Task: `TASK-BWOI-ONTOLOGY`
- SWU: `SWU-BWOI-001`
- Mode: lean, strict
- Runtime: local
- Dependency frontier: empty

## Obligations

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| O-001 | Validate `SuggestedTrack`, `CreateSuggestedTrack`, and `needs_evidence` as a closed local entry set. | task `Inputs` and `Algorithm`; SPEC `T-ONTOLOGY-001` | covered |
| O-002 | Require `CreateSuggestedTrack -> produces -> SuggestedTrack` and `CreateSuggestedTrack -> establishes -> needs_evidence`. | task `Algorithm`; SPEC concept registry | covered |
| O-003 | Admit `none -> needs_evidence`. | `states.md`, `Allowed Transitions` | covered |
| O-004 | Reject `needs_evidence -> source_backed` with `ONTOLOGY_TRANSITION_FORBIDDEN`. | task `Primary behavior`; `states.md` | covered |
| O-005 | Require evidence, confidence, status, next gate, and contradiction path. | CyberAlchemy ontology README `Rule` | covered |
| O-006 | Reject invalid entries, missing endpoints, missing governance metadata, duplicate IDs, and executable logic. | task `Outputs` and `Edge cases` | covered |
| O-007 | Emit a byte-deterministic receipt with candidate-local and non-promoting claim fields. | task `Done criteria`; WORK-PACK validation strategy | covered |
| O-008 | Stay inside the proof-only write scope and keep upstream/runtime sources read-only. | task `Write scope` and `Forbidden` | covered |
| O-009 | Run the ontology test and scoped diff check. | task `Validation` | covered |
| O-010 | Preserve exact closeout baselines for the declared owner targets. | WORK-PACK `Task Session Closeout Sync Contract` | covered |

## Selected Evidence

- `WORK-PACK.md` — control fields, selected SWU, validation, closeout contract.
- `work-pack/tasks/TASK-BWOI-ONTOLOGY.md` — executable contract and exact scopes.
- `work-pack/waves/W0.md` — entry and exit gates.
- `SPEC.md#T-ONTOLOGY-001` — approved standalone ontology verdict.
- `operations.md#CreateSuggestedTrack` — CT-2 through CT-4.
- `states.md#Allowed-Transitions` — legal transition source.
- `cyberAlchemy/ontology/README.md#Rule` — candidate metadata and authority ceiling.
- `.craft/ledger.yml` and `CRAFT.md` — closeout owner targets only.

## Hard Constraints

- The entry set contains no `body.logic` or executable DS-SFOL AST.
- DomainSpec and Body War application code are not loaded by the test.
- Candidate entries remain `candidate-local`.
- `authority_effect` is `none`.
- `release_admission` is `not-granted`.
- An upstream source or control digest change expires this pack.

## Decision Pack

No unresolved consequential decision exists. The selected implementation is a
dependency-free TypeScript validator using Node built-ins and the already
checked-in `tsx` loader. This is reversible and adds no package dependency.

## Coverage Result

- Files selected: 9
- Obligations: 10/10 covered
- Strict coverage: pass
- Blockers: none

