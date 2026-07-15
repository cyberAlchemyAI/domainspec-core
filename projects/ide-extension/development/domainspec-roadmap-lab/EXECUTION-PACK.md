# Execution Pack: DomainSpec v2 Roadmap Lab

## Control

| Field | Value |
| --- | --- |
| planningGateStatus | pass |
| complexity | medium |
| baselineWave | W0 |
| activePlanRef | [WORK-PACK.md](WORK-PACK.md) |
| layeringArtifact | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| activeLayerWindow | L0 |
| readinessProfile | trusted-local-newcomer-pilot |
| mutation status | not started; no SWU selected |

## Wave Schedule

| Wave | Layer | Outcome | SWUs | Entry gate | Exit gate |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | Copy and semantic-event contracts become executable oracles. | 001–002 | design/plan/dispatch pass; dirty-scope review | valid/invalid schema fixtures and contract tests pass |
| [W1](work-pack/waves/W1.md) | L0 | FPR-01 works end to end through a focused Roadmap Lab route. | 003–006 | W0 pass | deterministic build and real browser event witness pass |
| [W2](work-pack/waves/W2.md) | L1 | Coverage, history, restart, and stale-review behavior repeat. | 007–008 | W1 pass | representative-node, republish, restart, and stale evidence pass |
| [W3](work-pack/waves/W3.md) | L2 | Owner routing and failure behavior preserve authority. | 009–011 | W2 pass | route/receipt/denial/retry evidence and boundary review pass |
| [W4](work-pack/waves/W4.md) | L3 | Victor completes the real trial and one accepted copy change closes with evidence. | 013, 012, 014 | W3 pass; real participant; owner acceptance before 012 | trial, accepted round trip, and closeout audit pass |

## Dependency Spine

```text
001 -> 003 -> 004 -> 005 -> 006 -> 007 -> 008 -> 009 -> 010 -> 011
  \-> 002 ----^                                             |
                                                           v
                                                          013
                                                           |
                                               owner acceptance gate
                                                           |
                                                           v
                                                          012 -> 014
```

`SWU-RDL-001` and `SWU-RDL-002` may be executed in either order only if their
new-file write scopes remain disjoint. All work that touches the existing
builder/template or ide-extension runtime is sequential because the current
worktree already contains overlapping user changes.

## Stage Coverage

| Stage | Primary artifacts | Required receipt |
| --- | --- | --- |
| contract | schemas, fixtures, validation tests | Task Session result with fixture counts and no runtime mutation outside scope |
| build | copy data, builder/template, coverage/fingerprint tests | deterministic build receipt and generated-artifact diff summary |
| browser | focused mode, guided surface, history/stale projection | Node/Playwright results and retained screenshots/payloads |
| governance | review adapter, packet schema, disposition projection | class/denial/stale fixtures and owner-boundary review |
| human | Victor protocol/report and accepted round trip | real participant evidence and owner acceptance/application references |
| closeout | traceability and readiness audit | no-overclaim verdict plus remaining gaps |

## Stop Conditions

- A current dirty change overlaps the selected SWU and its owner cannot be
  established.
- Stable copy IDs cannot be extracted without changing graph/roadmap authority.
- An implementation needs a DomainSpec-specific Canvas mutation API.
- The focused route leaks unrelated ide-extension Craft state into the newcomer
  frame.
- An invalid/stale proposal is silently rebased or applied.
- The Victor trial or owner acceptance is unavailable; return a truthful block.
- Any test or review shows submission being described as acceptance/application.

## Handoff

Execution begins only through Task Session with exactly one selected ready SWU.
The first eligible selection is `SWU-RDL-001` after an execution-time dirty-
scope review. This pack schedules work; task files own implementation detail and
`WORK-PACK.md` owns status.

