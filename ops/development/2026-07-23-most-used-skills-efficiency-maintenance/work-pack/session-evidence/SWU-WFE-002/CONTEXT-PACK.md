# Context Pack: SWU-WFE-002

Status: strict coverage pass

Mode: standard

Lifecycle route: Sigil Development `--update` for public Arcanum canonical
source, followed by declared runtime regeneration

## Task boundary

Narrow Task Session's automatic-choice admission and completion classification.
An automatic choice is admitted only when it is explicitly both
nonconsequential and reversible. Failed or unavailable acceptance-critical
validation blocks completion unless an accepted equivalent passes. Preserve
`FLAG` only for named noncritical residue that cannot falsify a done criterion.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| TS1-O1 | Remove the subjective “clearly safe” recommendation escape. | task rule 1; accepted TS-1 finding; canonical step 20 | covered |
| TS1-O2 | In auto mode, require explicit nonconsequential and reversible classification; otherwise ask or block. | task rule 2; Design decision/completion guard | covered |
| TS1-O3 | Classify every done criterion or validation obligation as acceptance-critical or noncritical, with a fail-closed default. | task rule 3; Design risk control | covered |
| TS1-O4 | Failed or unavailable acceptance-critical validation without a passing accepted equivalent returns `BLOCK`. | task rule 4; canonical steps 41-47 | covered |
| TS1-O5 | Preserve `FLAG` only for named noncritical residue that cannot falsify a done criterion. | task rule 5; accepted TS-1 finding | covered |
| TS1-O6 | Add causal negative and positive fixtures for automatic-choice and validation outcomes. | task rule 6 and acceptance boundary | covered |
| TS1-O7 | Generate and parity-check only the declared Codex and Claude Task Session runtime packages. | task write scope; runtime provenance; bootstrap generator | covered |
| TS1-O8 | Keep the implementation owner-local; do not create the explicitly deferred shared validation framework. | Design WFE-D01 and GAP-WFE-05 | covered |
| TS1-O9 | Preserve unrelated dirty generator work and make no application-task changes. | task forbidden scope; live worktree preflight | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-002-TS-AUTO-VALIDATION.md` | objective, rules, acceptance, validation | complete SWU contract | `2bda35d4fde79f5be648813ef6df1c8d0ea34db5eae0249d0a02b3a651274ed7` |
| `work-pack/swu-manifest.json` | `selected_swu`; `SWU-WFE-001`; `SWU-WFE-002` | machine dependency and selected-unit state | `53d2973204b3cd11f006a757635aab144efa3afdd77f1101869f9b78f7e308c5` |
| `WORK-PACK.md` | controls, task/SWU rows, gaps, gates | program order and lifecycle boundary | `6582bdd17694cf145ae058bc7c815a17ded9ddb742002a294520324dbd18f6b3` |
| `DESIGN.md` | Task Session guard; WFE-D01; status and risk controls | implementation semantics and non-framework boundary | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | TS-1 verdict; queue; final disposition | accepted defect and preserved behavior | `0515af8d3dd746f8b020cad3515232afe5bb5cd2f6d60a00b567ee5e314018fd` |
| `arcanum/arcana/task-session/SKILL.md` | flags; inputs; steps 18-25 and 41-47; quality; anti-patterns | canonical public contract | `8dac46ba61eaa3e5d5e92c67467cc4df66c1179790ad760cfd2acb47ed5dd038` |
| `.agents/skills/task-session/SKILL.md` | provenance and contract body | declared Codex runtime target | `b357a7cc778bbdb807e3bd2f3aaf30fd799408c284f84283856f14c01b4b4a27` |
| `.claude/skills/task-session/SKILL.md` | provenance and contract body | declared Claude runtime target | `8d57a5cc15ed0df4cc391fd2bdf9b6055570e762bce2566504934aa6b81f6464` |
| `arcanum/tools/bootstrap_arcanum.sh` | generated-skill writer and runtime profiles | only declared regeneration path | `eed93902a1941cb40eb0560de40e2361ad969cdc72388c0c471009a317f9d257` |

## Constraints and decisions

- The canonical public source remains `arcanum/arcana/task-session/`.
- A Task Session-local machine policy makes the contract executable; it is not a
  shared validation framework.
- Unclassified done criteria and validation obligations fail closed as
  acceptance-critical.
- Bounded recovery remains available, but it cannot turn a still-failed
  acceptance-critical check into `FLAG`.
- An accepted equivalent must pass and must be named in the task contract or
  durable approval evidence.
- Noncritical residue must be named and must be unable to falsify any done
  criterion before `FLAG` is available.
- The existing dirty edits in `arcanum/tools/bootstrap_arcanum.sh` concern the
  Orchestrate runtime package and do not overlap ordinary Task Session package
  generation. They remain untouched.
- No subagents or runtime delegation are used.

## Validation surface

```bash
bash arcanum/arcana/task-session/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/task-session .agents/skills/task-session .claude/skills/task-session
```

Baseline: the focused fixture command is absent, which is the task's declared
red baseline. The canonical and generated contracts still contain the
subjective auto-choice clause and the critical-validation-to-`FLAG` escape.

## Context Builder result

- Files selected: 9
- Obligation coverage: 9/9
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; execution is local and bounded
