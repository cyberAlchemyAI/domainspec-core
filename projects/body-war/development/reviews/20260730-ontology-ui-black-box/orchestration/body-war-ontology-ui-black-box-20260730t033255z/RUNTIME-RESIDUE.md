# Native orchestration runtime residue

## Wave-receipt scoping

The first synthesis reduction was given the dispatch-wide receipt directory. The deterministic reducer admitted `spawn-0004` but blocked on the three prior-wave receipts as unexpected. No host action or target mutation followed that result. The corrected reduction used `wave-receipts/synthesize/`, containing exactly the one expected receipt, and passed.

## Cross-wave action identifiers

After the synthesis gate, the coordinator emitted `spawn-0002` and `spawn-0003` because it numbers the next action set from the size of the just-completed wave. Those identifiers already belonged to the attack wave, so native replay protection forbids executing them in the same run.

The parent retained the original coordinator output and created a deterministic run-local rebase:

- emitted `spawn-0002` → admitted `spawn-0005`
- emitted `spawn-0003` → admitted `spawn-0006`
- emitted post-verification `spawn-0003` → admitted `spawn-0007`

Only `action_id` and matching plan/state/gate references changed. Role, capability, target, inputs, outputs, mutation policy, scopes, wave, step, dispatch, and run identity remain byte-equivalent in meaning. This is runtime residue, not a dispatch-route change and not evidence about the viewer.
