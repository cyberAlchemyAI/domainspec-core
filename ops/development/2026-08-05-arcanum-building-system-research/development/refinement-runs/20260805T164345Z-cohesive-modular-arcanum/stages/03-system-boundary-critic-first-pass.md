# System-Boundary Critic — First Pass

Verdict: `block` acceptance of the original shared-kernel hypothesis; continue Refine repair.

## Counterexamples admitted

| ID | Finding | Required repair |
|---|---|---|
| `CRITIC-AUTH-001` | Kernel legality validation can become policy ownership. | Restrict it to structural validation; owner emits semantic decision receipt. |
| `CRITIC-AUTH-002` | Kernel schema evolution has no steward or consumer acceptance rule. | Non-authoritative steward plus independent owner version acceptance. |
| `CRITIC-OWNER-001` | `WorkPackSnapshot` collapses Invoke authoring and WPRA freeze. | Split authored and frozen records. |
| `CRITIC-OWNER-002` | Material producer remains unbound. | Preserve blocking residue and route an owner decision. |
| `CRITIC-OWNER-003` | Closeout transport, mutation, derived result, cursor, and series advance are blurred. | Split all five transitions and owners. |
| `CRITIC-OWNER-004` | Lifecycle class and registry release owner cannot be inferred. | Type lifecycle route and keep release blocked. |
| `CRITIC-FRESH-001` | Copied authorization statuses conflict. | Add one immutable approval receipt; derived artifacts reference it. |
| `CRITIC-REPLAY-001` | Crash after effect but before receipt can duplicate or strand effects. | Idempotency, `outcome_unknown`, reconciliation route, no exactly-once claim. |
| `CRITIC-REPLAY-002` | Preflight digests do not close concurrent TOCTOU. | Atomic baseline/lease check at effect boundary. |
| `CRITIC-CYCLE-001` | Refresh and cursor derivation can depend circularly. | Immutable pre-state, separate post-Refresh snapshot, then series advance. |
| `CRITIC-PROOF-001` | Design/toy evidence cannot prove product E2E or concurrency. | Preserve real witness and crash/concurrency tests. |
| `CRITIC-MIG-001` | Universal records create flag-day/dual-authority risk. | Versioned bilateral adapters, shadow comparison, one authoritative writer. |
| `CRITIC-PRIV-001` | Payloads can leak private paths or assumptions. | Classification, redaction, public-source reconstruction, fixture scan. |

## Tournament additions

- Hybrid A+C: owner receipts plus non-authoritative append-only causal journal.
- Bilateral-adapter-first: prove a real boundary before extracting a universal envelope.

## Added residue

`RESIDUE-KERNEL-GOV-001`, `RESIDUE-SNAPSHOT-OWNER-001`, `RESIDUE-CURSOR-OWNER-001`, `RESIDUE-CRASH-REPLAY-001`, `RESIDUE-COMPAT-001`, `RESIDUE-PRIV-PAYLOAD-001`, and `RESIDUE-AUTHORIZATION-FRESHNESS-001`.

The parent must re-engage the same critic after Design, repair, and Plan artifacts exist.

