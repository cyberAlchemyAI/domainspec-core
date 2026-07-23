# Agent reasoning engine implementation layering

Status: **plan-ready candidate; implementation not authorized**

## Global boundary

The whole architecture is planned, but evidence promotes one layer at a time.
No layer may claim a general reasoning engine, real-world truth, anti-bias
efficacy, canonical promotion, or effect permission.

| Layer | Question | Included work | Explicitly excluded | Promotion evidence |
|---|---|---|---|---|
| L0 — semantic witness | Can one repository-owned finite reducer map frozen admissible inputs to exactly one typed outcome and enforce zero/one effect-test behavior? | evaluator@1, finite owner-authorized catalog fixture, two rule families, counterfactual suite, immutable replay, persisted-order recorder, entry/effect test doubles | full actor runtime, mutable providers, real effects, AntiBiasVector, public package | all counterfactuals pass; unchanged evaluator handles second family; replay stable; exact effect invariant holds |
| L1 — repeatable governed inputs/protocol | Can intent, authority/catalog inputs, entry/effort control, and bounded actors feed the reducer without owning its conclusion? | intent/frame projection, snapshot/catalog verification, entry gate, effort/technique controller, command/event journal, joins/timeouts, observation transport, deterministic replay | protected external effects, general orchestration platform, confidence aggregation | projection, authority validation, zero-call entry, effort monotonicity, partial-failure, timeout, challenge, and replay fixtures pass through L0 unchanged |
| L2 — governed effect/reliability | Can exact-effect control, current revalidation, durability, and degraded operation fail closed? | exact-effect gate adapter, revalidation, artifact admission, recovery, telemetry, incident/compensation routing | canonical admission without owner decision, automatic compensation | exact-envelope/zero-effect, drift/revocation/expiry/recovery suites; owner decisions; durability and audit receipts |
| L3 — private integration and scale | Can the private capability be packaged, observed, load-tested, and rolled out without widening authority? | private API/CLI boundary, compatibility, performance, operational runbooks, staged rollout | public Arcanum publication, general reasoning-engine promotion, real effects without separate approval | compatibility/performance/security evidence and explicit private rollout gate |

## Selected first unit

`SWU-ARE-001` is selected as the first future executable unit, but no Task
Session handoff is authorized by this plan. It owns one behavior: deterministic
semantic reduction for one frozen request to one terminal outcome, proven by its
acceptance harness. The gate/order recorder and effect adapter are test doubles,
not separate production capabilities.

Its implementation is blocked until:

1. the authority-model owner pins finite applicability, precedence, exception,
   contradiction, stale-rule, cycle, and self-judgment behavior; and
2. the challenge-contract owner pins timeout and late-material-defeat closure.
3. the effect-gate owner pins the exact test-only action envelope, gate fixtures,
   and idempotency semantics without authorizing a real effect.

## Cross-layer invariants

- Entry decision precedes any actor/evaluator event.
- Entry `block/defer/flag` causes zero calls; `flag` needs a new explicit pass.
- Evaluator-owned admission, applicability, reduction, and receipt assembly stay
  deterministic and non-authorizing.
- Exact-effect gate follows the persisted receipt and binds one identical
  envelope.
- Historical replay performs no mutable calls; current revalidation is a new run.
- Layer promotion cites previous-layer evidence; preference is insufficient.
