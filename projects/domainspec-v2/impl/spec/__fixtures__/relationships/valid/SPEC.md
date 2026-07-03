# Relationship Fixture - valid

## Concept Registry

| Concept | Type |
| --- | --- |
| MaxAmountRule | Rule |
| ProcessPayment | Operation |
| PaymentCompleted | Event |
| PaymentTransaction | Entity |
| WireTransferSaga | Saga |
| ReserveFunds | Operation |
| Library | Entity |
| Copy | Entity |
| Title | Entity |

## Feature Concept Graph

| From | Edge | To |
| --- | --- | --- |
| MaxAmountRule | enforces | ProcessPayment |
| ProcessPayment | produces | PaymentCompleted |
| PaymentTransaction | emits | PaymentCompleted |
| WireTransferSaga | orchestrates | ReserveFunds |
| Library | owns | Copy |
| Copy | belongs-to | Title |
