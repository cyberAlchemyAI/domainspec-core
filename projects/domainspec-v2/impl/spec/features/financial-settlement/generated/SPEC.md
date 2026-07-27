# Financial Settlement Specification

Generated human view. Canonical semantics live in the project-local machine sources.
Graph digest: `07542be03077c60f6d992cd86c62a6f227783dca63b997cfcf2e7a07e051ec31`.

## Nodes

| Node | Kind | Intent |
| --- | --- | --- |
| `financial-settlement.DealSplitCalculation` | Calculation | Calculate the player deal share admitted by experimental clause C3. |
| `financial-settlement.GenerateSettlement` | Operation | Generate settlement and expose the payout write/event effects admitted by experimental clause P4. |
| `financial-settlement.PayoutCreatedEvent` | Event | Record that the observed payout creation effect occurred. |
| `financial-settlement.PayoutEligibilityRule` | Rule | Identify the bounded experimental condition under which payout effects are observed. |

## Edges

| Edge | From | Type | To |
| --- | --- | --- | --- |
| `financial-settlement.edge.deal-split-calculates-generation` | `financial-settlement.DealSplitCalculation` | `calculates` | `financial-settlement.GenerateSettlement` |
| `financial-settlement.edge.generation-produces-payout-event` | `financial-settlement.GenerateSettlement` | `produces` | `financial-settlement.PayoutCreatedEvent` |
| `financial-settlement.edge.payout-rule-enforces-generation` | `financial-settlement.PayoutEligibilityRule` | `enforces` | `financial-settlement.GenerateSettlement` |

This file is generated; edit machine sources and rebuild.
