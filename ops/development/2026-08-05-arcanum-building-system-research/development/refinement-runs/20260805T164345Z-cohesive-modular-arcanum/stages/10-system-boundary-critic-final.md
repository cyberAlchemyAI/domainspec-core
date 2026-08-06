# System-Boundary Critic — Final Pass

Verdict: `flag` — the repaired Design and non-executed Plan are adequate to proceed to Decision Gate.

The design no longer structurally collapses authority. It separates structural validation from owner semantics, splits authored/frozen Work Packs, makes native receipts authoritative, orders Refresh before cursor creation, prohibits automatic retry after indeterminate effects, and keeps the duplicate series reducer behind an explicit decision.

This is design/plan adequacy only. No implementation, real owner-chain execution, canonical Orchestrate repair, generated parity, lifecycle decision, registry release, publication, or production behavior is proven.

## Counterexample retest

| Counterexample | Verdict | Final assessment |
|---|---|---|
| Structural versus semantic kernel | repaired | OBTC returns only structural pass/block; consumer owners issue semantic receipts. |
| Schema/version owner | preserved | A non-authoritative steward and owner-local version acceptance are designed; steward identity remains gated by `DECISION-ABP-PROTOCOL`. |
| Authored versus frozen Work Pack | repaired | `AuthoredWorkPack` and `FrozenWorkPackSnapshot` are distinct. |
| Material producer | preserved | Admission remains blocked until `DECISION-ABP-PRODUCER` binds a real producer. |
| Lifecycle split | repaired | Type-specific lifecycle judgment remains owner-local; protocol classification is separately gated. |
| Registry owner | preserved | Registry release remains unavailable until `DECISION-ABP-REGISTRY`. |
| Authorization drift | renamed | Reference discipline is repaired; the current binding is separately evidenced by `receipts/operator-approval.json`. |
| Crash `outcome_unknown` | repaired | Unknown outcome blocks retry, closeout, and advancement; only effect-owner reconciliation may continue. |
| Effect-boundary concurrency | repaired | CAS/lease plus concurrency scope is required at the effect boundary; implementation evidence remains absent. |
| Refresh/cursor causal ordering | repaired | Immutable pre-state → Refresh post-state → join → synchronized result → cursor → series advance is acyclic. |
| Fixture proof ceiling | repaired | The toy proves synthetic ordering only; real witness remains `SWU-ABP-015`. |
| Bilateral/versioned migration | repaired | Adapter-first, second-boundary-before-generalization, shadow reads, version rules, and rollback avoid a flag day. |
| Single authoritative writer | repaired | Native owner writes remain authoritative; dual writer is a negative trace. |
| Public/private leakage | repaired | Private proofs are separate from later public reconstruction, allowlists, scans, and lifecycle authorization. |
| Orchestrate receipt-set defect | preserved | `SWU-ABP-009` owns a separate canonical repair and regression. |
| Orchestrate cross-wave ID defect | preserved | `SWU-ABP-010` separately owns run-global allocation and regression. |
| Duplicate series reducer | preserved | Implementation Readiness is recommended; the compatibility spell becomes stateless only after Decision Gate and lifecycle acceptance. |

## Plan flags and parent repair

The critic identified three plan flags. The parent incorporated them into the candidate plan without claiming proof:

1. `CRITIC-L0-SEM-001`: L0 now requires a Task Session owner-native shadow acceptance/compatibility receipt before claiming semantic preservation; otherwise it proves only fields and diagnostics.
2. `CRITIC-EVENTS-DEP-001`: causal projection must select fixture-only ephemeral mode or an admitted local persistence owner; deferred ownership cannot create a durable journal.
3. `CRITIC-AUTHZ-EVID-001`: authorization repair is now stated as a design rule with current receipt binding separately cited.

These repairs tighten admission. They do not provide the missing owner decisions or implementation evidence.

## Owner-boundary verdict

`flag`: safe to proceed only to Decision Gate. No SWU is selected or admitted.

## Remaining migration risks

- protocol and series migrations remain pending owner and lifecycle decisions;
- material producer and registry-release owner remain unbound;
- crash, concurrency, rollback, version-skew, and privacy behavior remain fixture plans;
- canonical Orchestrate repairs and generated parity are unexecuted;
- public reconstruction and marker scans are planned only;
- dual-version compatibility may require preserved legacy routes.

