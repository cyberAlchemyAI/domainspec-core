# Execution Pack

Status: `planned; no execution authorized`

The source-of-truth SWU definitions are in [WORK-PACK.md](WORK-PACK.md) and the
linked task files. This file owns only ordering and wave gates.

| Wave | Layer | SWUs | Layer question | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0-CONTRACTS.md) | L0 | 001-002 | are the callable and durable languages closed? | selected 001 admitted | all schemas/codes and negative fixtures pass |
| [W1](work-pack/waves/W1-STATE.md) | L0-L1 | 003-006 | can history be appended and derived deterministically? | W0 receipts | transition, crash, replay, quarantine, zero-write receipts |
| [W2](work-pack/waves/W2-SERVICES.md) | L2 | 007-009 | can a local host use the contract without privilege confusion? | W1 receipts | consultation, episode, evidence, authorization tests |
| [W3](work-pack/waves/W3-INTEGRATION.md) | L2 | 010 | does the complete local candidate pass the attack matrix? | W2 receipts | two aggregate passes and evidence index |

Within each wave the dependency chain is serial. No parallel mutation is
planned because adjacent SWUs share contract semantics and each successor must
bind the prior terminal receipt. Validation-only reads may run concurrently
only after the corresponding writer has closed.

Stop at the first blocker, target-inventory drift, failed acceptance command,
unjoined receipt, or owner-boundary conflict. W3 completion does not enter L3.

