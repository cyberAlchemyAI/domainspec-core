# Distill Repair — Protocol Toy Game

## Target

Validate the repaired Design against a controlled positive trace and named failure traces before Invoke Plan.

## Mode and evidence

- Mode: validate
- Evidence artifact: `stages/08-protocol-toy-game.json`
- Deterministic check: `jq -e` over schema ID, authority effect, case cardinality/uniqueness, pass/block counts, first stops, forbidden effects, positive trace length, outcome-unknown presence, and kernel-policy prohibition
- Executed result: pass
- Cases: 13 total; 1 synthetic positive, 12 one-fault negatives
- Authority effect: none

## Positive toy trace

The synthetic trace contains twelve ordered events from `authored-work-pack` through `series-advance`. A fixture-only material producer is named explicitly so the trace does not pretend to bind the real producer. The toy proves that the repaired records can represent the expected order and that every transition has a place for an owner-native receipt.

It does not prove the real producer, real product mutation, real Refresh join, concurrent execution, crash recovery, generated parity, or production.

## Failure results

| Case | Fault | First stop | Forbidden downstream effects |
|---|---|---|---|
| `TOY-FAIL-001` | unsupported version | consumer version acceptance | semantic admission, owner effect |
| `TOY-FAIL-002` | stale approval | authorization freshness | stage start, spawn, owner effect |
| `TOY-FAIL-003` | crash after effect | outcome unknown | retry, closeout, series advance |
| `TOY-FAIL-004` | concurrent baseline conflict | effect-boundary CAS | second effect/terminal pass |
| `TOY-FAIL-005` | private public-payload field | payload classification | public write/publication |
| `TOY-FAIL-006` | dual authoritative writers | one-writer gate | projection authority/cutover |
| `TOY-FAIL-007` | kernel decides semantics | kernel authority boundary | semantic decision/owner receipt |
| `TOY-FAIL-008` | second series reducer writes | owner singularity | second frontier/retry ledger |
| `TOY-FAIL-009` | Refresh/cursor cycle | causal order | cursor/series advance |
| `TOY-FAIL-010` | missing Refresh join | owner join | synchronized result/cursor/advance |
| `TOY-FAIL-011` | receipt-set overreach | exact receipt-set admission | wave pass/dependent wave |
| `TOY-FAIL-012` | run-global action ID collision | pre-spawn allocation | duplicate spawn/dependent wave |

## Repair decisions

1. Kernel output is `structural_pass|structural_block`; never `semantic_pass`.
2. Owner-local compatibility receipt follows structural validation.
3. Authorization is referenced through `receipts/operator-approval.json`, not copied text.
4. `outcome_unknown` is terminal for automatic control; only effect-owner reconciliation can continue.
5. Concurrent attempts require atomic effect-boundary baseline/lease comparison.
6. Causal events are a projection contract; storage is owned locally and remains non-authoritative.
7. Native owner writes remain authoritative throughout migration.
8. Public projection uses a field allowlist and fails closed on unknown/private fields.
9. Task Session cursor follows joined Refresh; series advancement follows cursor.
10. Orchestrate repairs remain two separate work units and regression suites.

## Proposer/Balancer trace

| Proposer | Balancer objection | Reconciliation |
|---|---|---|
| The toy positive trace validates the architecture. | It validates declared ordering only. | Preserve fixture-only ceiling and require real owner-chain witness. |
| Outcome-unknown enables safe recovery. | No reconciliation implementation exists. | Plan reconciliation contract and fixtures; block runtime claims. |
| Adapter-first avoids flag day. | A second boundary is needed before generalization. | L0 proves one boundary; L1 adds a materially different closeout boundary before shared extraction. |
| Causal projection improves diagnostics. | Storage could duplicate observability. | Reuse an existing local event owner or remain ephemeral; no mandatory store in L0. |

## Closure and recomposition

The smallest executable proof remains one bilateral adapter pair, structural validator, and fixtures for WPRA selection to Task Session entry. It closes without owner effects and recomposes into the larger protocol because the same envelope fields can later be tested on the materially different Task Session-to-Refresh closeout boundary. Generalization is explicitly deferred until both boundaries pass.

## Distill Result

- Verdict: pass for non-executed planning
- Implementation readiness: blocked
- Current smallest coherent unit: one adapter pair + validator + fixtures
- Recomposition: pass at design level
- Evidence emission: partial; deterministic toy fixture only
- Residue: owner decisions, crash/concurrency implementation, second-boundary proof, real E2E, parity, canonical Orchestrate repairs
- Next route: Invoke Plan

