# Execution Pack: Invoke Lifecycle Progress Protocol

Status: planned; mutation execution gated

## Choreography

| Wave | Layer | Goal | Included work | Entry gate | Exit gate |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | ratify authority | SWU-ILP-001 | plan and dispatch validation pass | transition owner/source decision receipt |
| [W1](work-pack/waves/W1.md) | L1 | prove contracts in isolation | SWU-ILP-002, 003, 004 | W0 receipt | all false-ready, invalid-edge, and role-collapse fixtures reject |
| [W2](work-pack/waves/W2.md) | L2 | integrate capability boundaries | SWU-ILP-005, 006A, 006B, 007 | W1 receipts | Plan/Refresh/Task Session focused suites and parity pass |
| [W3](work-pack/waves/W3.md) | L3 | migrate and prove live | SWU-ILP-008A, 008B, 009, VERIFY | W2 receipts | live proof and final recomposition pass |

## Program order

The default route is serial:

```text
001 -> 002 -> 003 -> 004 -> 005 -> 006A -> 006B -> 007
    -> 008A -> 008B -> 009 -> VERIFY
```

Technical independence does not authorize parallel lifecycle mutation. A later
owner may propose parallel execution only after proving disjoint exact write
sets and an explicit join contract.

## Stage coverage

- Spellcraft: authority/source decision, protocol schemas, validators, Invoke
  Plan/Refresh integration, legacy adapter, public/generated synchronization.
- Sigil Development: Task Session contract and admission integration.
- transition-admission owner: edge admission contract and receipt semantics.
- Task Session: one bounded live proof after the handoff becomes ready.
- Workflow Reflect: observational progress/churn fields and final reflection.

## Closure obligations

Every mutation-capable SWU must return:

```yaml
swu_id: string
result: pass | flag | block | interrupted
files_touched: [path]
validation: [command-or-check-and-result]
source_receipt: path
closeout_sync:
  status: joined | no-op | blocked
  target_inventory: [path]
  baseline_bindings: [{path, sha256-or-absent}]
  delta_classes: [string]
  owner_receipt: path | null
blockers: [string]
residue: [string]
handoff_note: string
```

The implementation result and closeout owner result remain separate receipts.

## Stop conditions

- `ILP-G01` unresolved;
- missing predecessor receipt;
- public/private leakage;
- dirty overlap inside the exact write scope;
- producer/validator/consumer role collapse;
- incomplete control graph;
- same-epoch control change;
- exact digest mismatch;
- failed causal fixture;
- generated parity failure;
- live proof requires repair Refresh before admission.

