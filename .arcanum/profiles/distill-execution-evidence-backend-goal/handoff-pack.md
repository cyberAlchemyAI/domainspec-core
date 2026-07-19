# Codex Goal Handoff Pack: Distill Execution Evidence Backend

## Identity

- Task/stream: `GOAL-DISTILL-EXECUTION-EVIDENCE-BACKEND`
- Source work-pack: `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- Session/run id: `2026-07-17-distill-backend-goal`
- Session evidence path: `.arcanum/profiles/distill-execution-evidence-backend-goal/`
- Runtime handoff: `codex-goal`
- Evidence date: `2026-07-17`

## Ordered Stream

1. Bind and execute `SWU-DEE-004` role/process semantic validation.
2. Bind and execute `SWU-DEE-005` provenance and cross-artifact agreement.
3. Bind and execute `SWU-DEE-006` deferred-mode capability/fail-close behavior.
4. Bind and execute `SWU-DEE-007` active Invoke-mode evidence projection.
5. Bind and execute `SWU-DEE-008`, `SWU-DEE-009`, and `SWU-DEE-010` focused positive, missing,
   and fabricated-evidence fixtures, one SWU at a time.
6. Bind and execute `SWU-DEE-011` generated mirror parity.
7. Bind and execute `SWU-DEE-012` and `SWU-DEE-013` Workbench replay and superseding status,
   one SWU at a time.
8. Execute `TASK-DEE-VERIFY` only after every dependency and lifecycle receipt passes.

## Obligation Coverage

| Obligation | Status | Evidence | Resolution |
| --- | --- | --- | --- |
| Preserve the backend objective | covered | `WORK-PACK.md#Objective-Summary` | Complete the ordered validator-to-replay stream, not only the current substrate. |
| Completed substrate is the prerequisite | covered | `WORK-PACK.md#SWU-Manifest`, DEE-002 and DEE-003 result artifacts | Treat DEE-002/003 as complete inputs. |
| Future writes stay receipt-bound | covered | `SPELLCRAFT-DEE-003-LIFECYCLE-RECEIPT.md#SWU-DEE-003-Binding` | Before each future SWU, Spellcraft must name owner and exact paths. |
| One SWU per Task Session | covered | `.agents/skills/task-session/SKILL.md#Step-1` | No combined implementation mutation. |
| Validate reusable behavior after each slice | covered | `TASK-DEE-02-EVIDENCE-SUBSTRATE.md`, prior result artifacts | Focused deterministic evidence is required before advancing. |
| Preserve authority boundaries | covered | `SPELLCRAFT-LIFECYCLE-RECEIPT.md#Accepted-Invariant` | Events and authored results never authorize mutation. |
| Stop on unresolved authority or evidence | covered | `WORK-PACK.md#Blockers`, capability policy below | Report exact blocker and do not guess through it. |
| No private data in public Arcanum | covered | repository AGENTS boundary | This sidecar stays under private `.arcanum/`. |

Strict coverage: `pass` for orchestration and control policy. Future implementation paths are
intentionally resolved per lifecycle receipt before each mutation phase.

## Selected Sources

- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
  - Selectors: `Objective Summary`, `SWU Manifest`, `Blockers`, `Next Route`
  - Evidence: current backend graph and remaining ordered units.
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/`
  - Selectors: each task objective, acceptance boundary, dependencies, and validation surface.
  - Evidence: unit-specific contracts.
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/`
  - Selectors: DEE-002 and DEE-003 result obligations.
  - Evidence: completed substrate and focused harness proof.
- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-LIFECYCLE-RECEIPT.md`
  - Selectors: accepted invariant and authority boundary.
  - Evidence: validator-owned handoff rule.
- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-003-LIFECYCLE-RECEIPT.md`
  - Selectors: exact binding and next route.
  - Evidence: receipt-bound execution pattern.

## Capability Policy

- `spellcraft validate`: allowed before each unselected SWU; must emit a lifecycle receipt with
  canonical owner, exact implementation paths, governance/evidence paths, acceptance conditions,
  and next route.
- `task-session`: allowed for exactly one receipt-selected SWU; must produce synchronized result
  evidence and focused validation.
- `experiment-harness`: allowed for deterministic fixture/behavior validation after each slice.
- `decision-gate`: blocker-only for a consequential unresolved choice.
- `context-builder`: pack-first, lean or standard; no runtime delegation without strict coverage.
- `sigil-development`, `invoke`, `refine`, and `craft`: disallowed unless a future receipt or
  explicit operator instruction authorizes their named scope.
- Subagents: disallowed by default; a future receipt must explicitly authorize them and require
  joined/closed role receipts before synthesis.

## Constraints And Non-Goals

- Keep writes inside the exact paths of the current lifecycle receipt.
- Do not edit `arcana/distill/`, generated Distill packages, unrelated Invoke modes, or Workbench
  code before their own SWUs are selected.
- Do not treat schema validity, runtime events, authored verdicts, or resolver output as
  mutation authority.
- Do not run broad repository discovery. Explore only named gaps needed to resolve a current
  contract or validation command.
- Do not promote or publish the backend from this stream.

## Validation Surface

- Each SWU's receipt-named deterministic command or accepted substitute.
- Existing DEE-002 and DEE-003 focused runners.
- `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py` for the package dispatch.
- Final `TASK-DEE-VERIFY` evidence, including mirror and Workbench replay checks.

## Gaps And Blockers

- `DEE-004-selection`: currently open; Spellcraft must bind the semantic validator before its
  implementation can start.
- Later selection gaps are expected and must be resolved one at a time, never pre-authorized by
  this sidecar.

## Authority Precedence

1. Repository `AGENTS.md` and public/private boundary.
2. Accepted Spellcraft lifecycle receipt for the currently selected SWU.
3. Current task/SWU contract and Work Pack.
4. Preserved design and Distill validation evidence.
5. Existing implementation conventions and focused tests.

## Fallback Exploration

Named gaps only. Any extra source must be reported with the gap that justified it and whether it
changed the result.

## Output Paths

- Markdown: `.arcanum/profiles/distill-execution-evidence-backend-goal/handoff-pack.md`
- JSON/index: `.arcanum/profiles/distill-execution-evidence-backend-goal/handoff-index.json`
