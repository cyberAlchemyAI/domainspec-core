# ARE reasoning-state runtime

This candidate package implements the first reusable-reasoning-state vertical:

1. a canonical append-only ledger of explicit reasoning products;
2. immutable, content-addressed Reasoning State epochs and risk-aligned
   checkpoint barriers; and
3. exact reconstruction and verification of an outbound model request.

The ledger records inspectable system state, not hidden model chain-of-thought.
Its events retain their original evidence and authority posture. Sealing or
reusing an epoch does not admit evidence, authorize an effect, or promote a
claim.

A Reasoning State Frontier is an explicit, content-addressed state record for a
completed reasoning boundary. `sealReasoningStateFrontier` appends that record,
seals its single-event epoch, and flushes an `after-turn-completion` checkpoint
as one fail-closed operation. Recovery admits a frontier into its disposable
index only when the event, epoch, subject digest, and matching completion
checkpoint all verify. The frontier contains inspectable semantic and
continuation products; it is not hidden model chain-of-thought.

Two sinks are included. The memory sink is deterministic and useful for tests
or explicitly process-local operation. The append-only file sink writes one
canonical JSON record per line and calls `fsync` at a checkpoint. Existing
bytes are never rewritten. A required checkpoint failure is fail-closed.

File recovery is checkpoint-bounded and performs no external calls. It verifies
UTF-8 and canonical JSONL bytes, record wrappers, ledger identity, event
sequence and predecessor chains, idempotency identities, epoch selections, and
checkpoint bindings before rebuilding disposable indexes. A non-empty log is
recoverable only when its final record is a valid checkpoint. Torn, malformed,
tampered, mixed-ledger, unknown, or uncheckpointed tails block without changing
the source file.

Public operations include:

- `createReasoningStateLedger`
- `appendReasoningStateEvent`
- `sealReasoningStateEpoch`
- `verifyReasoningStateEpoch`
- `replayReasoningStateEpoch`
- `checkpointReasoningState`
- `createMemoryReasoningStateSink`
- `createAppendOnlyFileReasoningStateSink`
- `verifyReasoningStateLog`
- `rebuildReasoningStateIndexes`
- `selectRecoverableCheckpoint`
- `recoverReasoningStateLedger`
- `sealReasoningStateFrontier`
- `verifyReasoningStateFrontier`
- `getReasoningStateFrontier`
- `listReasoningStateFrontiers`
- `createRequestSeriesHeader`
- `materializeReasoningDispatch`
- `verifyReasoningDispatch`
- `reconstructReasoningDispatch`

The package is a bounded implementation candidate. Recovery assumes one
process owns a selected log; cross-process locking, log repair, compaction, and
distributed replication remain absent. It does not establish a durable
CyberAlchemy Session, admission, conformance, publication, deployment, or
authority.
