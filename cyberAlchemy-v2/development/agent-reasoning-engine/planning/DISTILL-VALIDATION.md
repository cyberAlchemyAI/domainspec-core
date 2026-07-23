# Distill validation — agent reasoning engine plan

Verdict: **PASS for plan structure; implementation handoff BLOCKED by named owner decisions**

## Candidate unit

Selected unit: `SWU-ARE-001`, deterministic `semantic-judgment evaluator@1`
witness with immutable acceptance harness.

Primary behavior: for one frozen, owner-authorized catalog request, return
exactly one terminal typed outcome and expose a digest-bound receipt while the
test boundary proves zero/one effect behavior.

## Split analysis

Plausible children are input validation, catalog applicability, reduction,
receipt serialization, historical replay, persisted gate-order recording, two
rule families, and effect test-double checks. They remain one L0 SWU because no
child independently establishes the claimed semantic relation:

- a reducer without counterfactuals can be fixture-specific;
- one rule family does not show catalog generality;
- a receipt without deterministic reduction is shaped prose;
- replay without immutable input binding is only re-execution;
- semantic positivity without the zero/one effect boundary risks becoming
  permission;
- gate-order checks are acceptance instrumentation, not a production runtime.

The full actor protocol, mutable providers, current revalidation, durable
storage, real effects, generalized anti-bias machinery, and packaging can pass
independently and are therefore separate SWUs.

## Narrow-first-unit check

PASS. The unit uses static fixtures, in-memory/persisted-order test records, and
an effect test double. It does not build a general actor runtime, real adapter,
distributed journal, public API, or generalized policy language.

## Recomposition proof

`SWU-ARE-001` supplies the semantic center of the approved architecture. L1
adds `SWU-ARE-010/011` intent and authority/catalog inputs,
`SWU-ARE-012/013/015` entry, effort, and technique controls,
`SWU-ARE-002/003` journaled observations, and `SWU-ARE-004` immutable replay
without changing evaluator code. L2 adds `SWU-ARE-014` exact-effect control plus
`SWU-ARE-005/006/007` current
revalidation, durability, and degraded/incident behavior. L3 adds the private
interface and operational envelope. Every component in the design map has one
later unit; gates remain ports around—not branches inside—the reducer.

## Acceptance-critical gaps

| Gap | Treatment | Distill effect |
|---|---|---|
| finite applicability/precedence/conflict/stale policy missing | G-ARE-POLICY owner record | blocks implementation, not plan structure |
| finite challenge timeout/late-defeat closure missing | G-ARE-POLICY owner record | blocks implementation, not plan structure |
| exact-effect test envelope/idempotency owner missing | G-ARE-POLICY owner record | blocks implementation, not plan structure |
| runtime language assumption | Node 22 ESM recorded as reversible local choice | non-blocking plan assumption |
| canonical serialization and persistence | provisional L0 canonical JSON plus injectable atomic local store | acceptance contract, not production durability |
| revision-history intent mechanics | excluded from L0 inputs | non-blocking residue |
| AntiBiasVector | excluded | blocks efficacy claim, not evaluator witness |

## Plan-quality checks

- L0–L3 boundaries and promotion evidence: pass.
- Medium/high split work-pack: pass.
- Task-local SWUs and write scopes: pass.
- Algorithmic detail and failure behavior: pass.
- One parent and acceptance boundary per SWU: pass.
- First SWU navigation: pass.
- Validation surface per delivery slice: pass.
- Protected/public/canonical boundaries: pass.

The pass authorizes only the plan to route into Craft refresh. It grants no
implementation handoff.
