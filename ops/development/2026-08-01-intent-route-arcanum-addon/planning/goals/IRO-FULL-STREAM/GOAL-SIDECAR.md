# IRO-FULL-STREAM native Goal sidecar

## Frozen epoch

- Goal epoch label: `20260802T021738Z`
- WPRA epoch: `epoch-a696eda26311d39018e7ac8f`
- Audit projection: `6610d3e26d10c75e24c7eb35b80d34a6a1d74390510a7ca22256af010ed1fdbb`
- Canonical semantic digest: `d993c0f34ea48f31518b453d46bcb97c844168bc2dec7b8885bbfee7308a3ed0`
- Source snapshot digest: `02394458d68f00f1a0ecbaba478a06021314490bd44d077744e229f5583ade32`
- Strict Context coverage: `pass`, 13/13 obligations
- Native execution state: active; outer-chain preflight pending

## Exact controlling artifacts

| Artifact | SHA-256 | Size |
|---|---|---:|
| `planning/work-pack/shared/EXECUTION-CONTRACT.json` | `a7dfdf655e4898659bf9b3f96b4ee9a71dec84a62b4362e619fabf66c8dc49f2` | 22261 |
| `planning/work-pack/session-evidence/IRO-FULL-STREAM/20260802T021738Z/CONTEXT-PACK.md` | `95e6e23254f845aa22efcbcd4315b1d24e975ceea5afb399651cbf387bf09ccb` | 5865 |
| `planning/work-pack/session-evidence/IRO-FULL-STREAM/20260802T021738Z/CONTEXT-PACK.json` | `8eb6eaeb2656c412bd075c76e5c07722dfd436c244c8a5c4bc08599658f24c21` | 19518 |
| `planning/readiness/20260802T021738Z/outputs/work-pack-readiness-report-v2.json` | `492b8538192fcf8d391c1ca11d6d92eb065d6e1750773f4a9f86f619e22eb675` | 107319 |
| `planning/readiness/20260802T021738Z/outputs/objective-execution-manifest.json` | `a27a5f668f8a5e5db44e86fb2c74f0c827aecee02e6d8f1d1890767723beef93` | 101778 |

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

`IRO-REFRESH-002` repaired the missing runtime-output contract. The replacement
WPRA v2 epoch passes with zero findings. The direct Goal-start instruction may
now be persisted against this exact manifest; it grants only outer-chain start
and IRO-001 execution-output writes.
