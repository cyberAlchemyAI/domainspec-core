# IRO-FULL-STREAM native Goal sidecar

## Frozen epoch

- Goal epoch label: `20260802T013311Z`
- WPRA epoch: `epoch-bdf20ffa68dc08377ecaf50e`
- Audit projection: `0a89a79834320bf2ff902a6941036bdfd9f2776b488d7b1357702b495f7c71e8`
- Strict Context coverage: `pass`, 12/12 obligations
- Native execution state: not started

## Exact controlling artifacts

| Artifact | SHA-256 | Size |
|---|---|---:|
| `planning/work-pack/shared/EXECUTION-CONTRACT.json` | `fff0cd65f0999af55daf3040c4d9994dc0a5ef0ff25e96e88a7afc89d62d641c` | 11256 |
| `planning/work-pack/session-evidence/IRO-FULL-STREAM/20260802T013311Z/CONTEXT-PACK.md` | `c4dc126624a61a90db0571b2d513f26f190a4715c03b07222f131ea5a18f48c6` | 9389 |
| `planning/work-pack/session-evidence/IRO-FULL-STREAM/20260802T013311Z/CONTEXT-PACK.json` | `f238ef06c83eeb97d48af52214eb71802cf10706537a47fb79b1b8b00e80b42b` | 14876 |
| `planning/readiness/20260802T013311Z/outputs/work-pack-readiness-report-v2.json` | `429b50ef6afb88e06315e9a66f57878534cd5732ac2e1a6b5407fe34e9b6229f` | 80833 |
| `planning/readiness/20260802T013311Z/outputs/objective-execution-manifest.json` | `006662b63082d25eec1806430cd954c38daaa2b6a0ef40d089d6316f62d2f485` | 75616 |

Paths in this table are relative to
`ops/development/2026-08-01-intent-route-arcanum-addon/`.

## Runtime policy

Read the strict Context Markdown and JSON first. Execute one selected unit at a
time through `task-session`; use only the exact capability lanes and budgets in
`IRO-FULL-STREAM.md` and `EXECUTION-CONTRACT.json`. Subagents are off by
default. One bounded helper is allowed only after an exact current owner or
operator instruction authorizes it, and its terminal role receipt must be
joined before synthesis.

The decision profile is runtime-private at
`.arcanum/profiles/decision-profile.yml`. Consume only these operational
effects: strictest-safe/default-deny posture, every mutation gated,
propose-then-promote, smallest reliable slice, reconcile before act, and
owner-scoped decisions. It grants no approval.

## Write boundary

The coordinator may write only the fixed epoch receipt paths declared by the
execution contract. Owner material writes are separate and require the exact
approval, locator, target inventory, and baseline for the current unit.
Unresolved placeholder scopes block dispatch. The Goal may not widen scope to
canonical Arcanum, generated packages, consumers, ResonantOS, the orchestrator,
or CAV2 by itself.

## Iteration and final report

After each unit, validate the terminal receipt, join the closeout-owner receipt,
project the one successor, then enforce its pause gate. One repair cycle is
allowed; a second failure returns a blocked report with owner, stale/missing
receipt, exact failed command, and residue. Regenerate Context/WPRA on semantic
contract change.

The final report must list every unit/receipt, pause/resume approval, validation
result, browser/runtime provenance, changed files by owner, extra source used
for each named gap, unresolved residue, and the highest honestly proven
lifecycle state. Release, deployment, production, and whole reasoning-engine
claims require separate evidence and are not implied.

## Runtime repair state

The frozen `20260802T013311Z` epoch is superseded because it omitted mandatory Task Session support outputs. Native execution remains not admitted until a new strict Context/WPRA epoch passes and the direct Goal-start instruction is persisted against that exact manifest.
