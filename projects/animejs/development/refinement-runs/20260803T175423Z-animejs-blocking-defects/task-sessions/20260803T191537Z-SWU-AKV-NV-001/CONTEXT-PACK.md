# Task Session Context Pack — SWU-AKV-NV-001

## Identity

- Resolution mode: `resume-nearest`
- Resolution source: visible current-session context
- Task: `SWU-AKV-NV-001` — Query contract
- Source plan: `../../stages/09-invoke-plan.md`
- Runtime: local Codex Task Session
- Context mode: lean, strict
- Handoff: none; local execution was evaluated

## Resolution

`SWU-AKV-NV-001` is the sole visible current-session candidate and the first unit in the five-unit Refine plan. No `WORK-PACK.md` exists under `projects/animejs`, and no repository-local Task Session continuity cursor refers to Anime.js or this SWU. Unrelated continuity cursors were rejected as cross-scope.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| `O1` | Resolve exactly one live task/SWU. | `09-invoke-plan.md#first-implementation-slice`; `RESULT.md#recommended-next-route` | covered |
| `O2` | Prove dependency readiness and current selection. | `09-invoke-plan.md#work-sequence`; SWU-001 is first and has no declared predecessor. | covered |
| `O3` | Bind the behavioral contract and eight fixtures. | `08-query-contract-matrix.json`; digest `537e0584...342` | covered |
| `O4` | Declare exact material writes and execution outputs. | The plan names artifact kinds only; no repository-relative paths or write partitions exist. | **block** |
| `O5` | Declare concrete validation commands or accepted equivalents. | The plan says “static closed-code check plus eight terminal cases” but names no command, runner, schema, or expected output paths. | **block** |
| `O6` | Bind routed mutation admission to a live material package/producer receipt or a proven output-only profile. | No material package, producer receipt, allowed-write union, or execution-output contract exists. | **block** |
| `O7` | Preflight closeout synchronization before implementation. | No target inventory, target baselines, source-receipt contract, owner validation commands, expected owner receipt, or unique-successor policy exists. | **block** |
| `O8` | Preserve authority and scope ceilings. | `RESULT.md#validation-ceiling`; `VALIDATION.json#evidence_ceiling` | covered |

Strict coverage: 4/8 obligations covered, 4/8 blocked. This pack is not runnable.

## Selected Sources

| Source | Selector | Obligations | Role |
| --- | --- | --- | --- |
| `../../stages/09-invoke-plan.md` | `#work-sequence`, `#first-implementation-slice`, `#required-next-authorization` | O1, O2, O4, O5, O7 | Task identity and incomplete execution contract. |
| `../../stages/08-query-contract-matrix.json` | `closed_abstention_vocabulary`, `primary_precedence`, `receipt_invariants`, `planned_fixtures` | O3, O8 | Exact design-level behavior and fixtures. |
| `../../RESULT.md` | `#validation-ceiling`, `#recommended-next-route` | O1, O8 | Current authority and evidence ceiling. |
| `../../VALIDATION.json` | `checks.query_matrix`, `evidence_ceiling` | O3, O8 | Current validated design evidence. |
| `../../stages/10.receipt.json` | `handoff_note`, `evidence_ceiling` | O1, O8 | Confirms the next route requires new authorization and does not infer ontology authority. |
| `.agents/skills/task-session/SKILL.md` | Steps 1, 4, 4A, 5A, 8 | O4, O5, O6, O7 | Execution and closeout admission contract. |

## Constraints

- Closed research artifacts remain read-only.
- No ontology bytes may be created in this SWU.
- Historical QueryReceipts may not be rewritten.
- Planned fixtures are not execution evidence.
- Publication, promotion, deployment, and production readiness remain out of scope.

## Blockers

1. Exact writable paths and the material-write/execution-output partition are absent.
2. Concrete validation commands and output reconciliation are absent.
3. Mutation-admission producer evidence is absent.
4. Required closeout synchronization cannot be preflighted.

## Required Owner Repair

Invoke Plan/Refresh must emit one executable work-pack row for `SWU-AKV-NV-001` with exact paths, validation commands, mutation-admission profile, target baselines, closeout delta classes, expected owner receipt, and unique successor policy. Task Session must then revalidate those live bytes before execution.
