# Context Pack: SWU-WFE-001

Status: strict coverage pass

Mode: lean

Lifecycle route: Sigil Development `--update` with private DomainSpec tooling

## Task boundary

Reject contract-forbidden new dispatch and close records at the existing
appender boundary. Preserve the append-only ledger format, all historical rows,
and duplicate-close idempotence.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| DSS1-O1 | Reject submitted RESERVED dispatch types before append while historical rows remain structurally readable. | task algorithm 1; findings DSS-1; `LIVE_TYPES`, `validateDispatch`, `checkLedger` | covered |
| DSS1-O2 | Reject a close without a matching dispatch, but keep an already-present close as a successful no-op. | task algorithm 2; findings DSS-1; close branch after `checkLedger` | covered |
| DSS1-O3 | Reject a final approver equal to a submitted working-agent name after whitespace normalization. | task algorithm 3; strategy invariant; group/agent validation | covered |
| DSS1-O4 | Reject absolute paths, explicit parent traversal, and realpath/symlink escape, including a not-yet-created leaf beneath an escaped existing parent. | Design destination-containment algorithm; task algorithm 4 | covered |
| DSS1-O5 | Preserve the normalized case-insensitive `vault` prohibition without rejecting `vaulted/`. | current section 10 controls; task algorithm 4 | covered |
| DSS1-O6 | Every failed admission leaves the temporary ledger byte-identical and emits a stable exit-2 error. | task algorithm 5; test helpers and done criteria | covered |
| DSS1-O7 | Add positive controls for a non-existing in-root folder, old-shape history, and duplicate-close no-op. | task acceptance boundary; existing sections 12 and 13 | covered |
| DSS1-O8 | Change only the appender and its focused test; synchronize evidence only after validation. | task write scope and synchronization section | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-001-DSS-ADMISSION.md` | objective, algorithm, done criteria, validation | complete SWU contract | `2982d59f277b2bcfad1cf502747e5d65f56300161ce48644df64379f3e41ce40` |
| `work-pack/swu-manifest.json` | `SWU-WFE-001` | selected machine contract | `cc06e2a9e7a60ae0003e08c8b68b15c1b37f26ad8f0f0e6547b94e4408969f19` |
| `WORK-PACK.md` | control fields, task row, blockers, gates | program-order and lifecycle boundary | `ab54275249658e59284d16de445887ff68583dfb4b26c953f5311151db8b2a92` |
| `DESIGN.md` | DSS admission component; destination containment | implementation semantics | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | finding 5; DSS verdict; direct verification | accepted defect and preserved behavior | `0515af8d3dd746f8b020cad3515232afe5bb5cd2f6d60a00b567ee5e314018fd` |
| `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs` | `LIVE_TYPES`, `validateDispatch`, `validateClose`, `checkLedger`, append branches | implementation target | `c2f6cd55fe25ae2a50f0e1768fa6d6b3b13ebc977ab5c0ac4a08c3dbb66d1a30` |
| `implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs` | helpers; sections 10-13 | causal validation target | `3554a07436f1871e46d91fa72d3f33b9daf1f8fc29667d6482574388faad3804` |
| `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md` | register/run, close, routing, invariants | lifecycle semantics already claimed by owner | `bd4266169fad55999fe6cfe941a04d18a9a7858a1818eeeea20a25dcb818ed74` |

## Constraints and decisions

- No record field or schema-version change.
- The accepted broad `DISPATCH_TYPES` list remains for strict record vocabulary
  and historical documentation; new-row admission additionally requires
  membership in `LIVE_TYPES`.
- Agent identity is `agent_name` only. Missing names do not acquire inferred
  identity from roles or prompts.
- Name comparison trims and collapses whitespace but remains case-sensitive;
  no fuzzy identity rule is introduced.
- Destination containment treats `/` and `\` as separators, checks lexical
  traversal, then resolves the root and nearest existing candidate ancestor.
- Duplicate close is tested before orphan-close rejection.
- The real dispatch ledger is never written by the test harness.
- Current scoped worktree overlap: none.

## Validation surface

```bash
node implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs
git diff --check -- implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs
```

Baseline: 83 passed, 0 failed, 0 skipped.

## Context Builder result

- Files selected: 8
- Obligation coverage: 8/8
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; execution is local and bounded
