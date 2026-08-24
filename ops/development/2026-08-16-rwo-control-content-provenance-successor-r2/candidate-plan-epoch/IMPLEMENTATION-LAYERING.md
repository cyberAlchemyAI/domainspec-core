# Implementation Layering — Control And Content Provenance

| Layer | Owner | Unit | Behavior | Promotion gate |
| --- | --- | --- | --- | --- |
| L0 bootstrap | Task Session plus protected helper | CCP-001 | Create a public-safe legacy bridge without canonical mutation. | Public-only input receipt, disclosure pass, exact capsule inventory. |
| L1 provenance contract and native parity | Context Builder, Invoke, Task Session, package generator | CCP-002 | Atomically install source authority, split contracts, and exact generated packages. | Legacy package/admission pass, canonical/generated rollback closure, inherited drift labeled, live caches preserved, full legacy/split/parity regressions pass. |
| L2 clean-room material | protected helper plus disclosure reviewer | CCP-003 | Reconstruct ten adapter candidates from public inputs only. | No-private-input receipt, source coverage, disclosure pass, staged manifest. |
| L3 public application | Task Session/public runtime owner | CX003R2 | Package and apply ten clean-room adapter targets under split provenance. | New 1.1/1.3 admission, exact target baselines, validations, E/O/V/P/C/B/T. |

## Recomposition Proof

The units are sequential because each changes the admissible evidence language for the next. CCP-001 cannot mutate canonical files. CCP-002 must atomically couple canonical contracts and generated runtimes because producer/consumer cross-version mismatch or generated parity drift is acceptance-critical. CCP-003 is separate because protected-context isolation must be reviewable before public application. CX003R2 is separate because clean-room evidence does not itself grant mutation authority.

The four-unit chain recomposes to one outcome: private governance can control public work without becoming public content provenance, and public bytes are applied only from a truthful public source frontier.

## Deferred

Live App Server/model/provider execution, network transport, deployment, publication, promotion, release, production readiness, Context Builder general schema formalization beyond the two indexes, and any non-CX003R consumer migration remain outside this Work Pack.

## Cross-Cutting Task Session Partition

Every layer carries the same five-way boundary: pre-execution controls; mutation writes; separately route-authorized E; validation V; lifecycle O/P/C/B/T. Output-only layers admit payload outputs only. Material-bound layers admit exact material writes plus E as the sole execution output. The candidate-local regression is a readiness dependency for all four layers.
