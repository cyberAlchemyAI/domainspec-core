# Implementation Details — Planned, Not Executed

## 1. Bilateral projector

Inputs: one owner-native artifact/receipt, adapter mapping version, target consumer ID, accepted source schema version.  
Output: OBTC projection plus native handle/digest; never a new native verdict.

```text
load exact native artifact
verify source schema and digest
select mapping by source kind + version + consumer
copy only mapped fields; classify every field
reject absent required fields and unknown private/public fields
set projection authority_effect = none
bind native ref and digest
emit deterministic projection or stable structural block
```

Edge cases: unknown version, repeated field, lossy mapping, missing owner, private value in public projection, stale digest. All block before consumer admission.

## 2. Structural validator

```text
validate schema and protocol version shape
require one effect_owner or explicit none for pure projection
require distinct producer/validator roles where contract demands
validate native ref/digest and attempt correlation
validate gate and expected-receipt descriptors are complete
validate freshness/replay/idempotency fields
validate owner-declared route is marked hint_only
never import or call owner policy/effect modules
return structural_pass or stable structural_block[]
```

Forbidden APIs are tested explicitly. A structural pass is input to, not a substitute for, consumer owner policy.

## 3. Outcome-unknown reconciliation

Inputs: attempt/idempotency key, exact effect scope, pre-effect baseline, observed post-crash state, effect-owner probe receipt.  
Output: `effect_absent`, `effect_committed`, or `manual_resolution_required`.

Rules:

1. no automatic retry from `outcome_unknown`;
2. only the effect owner may issue the probe/reconciliation receipt;
3. mismatched scope, identity, baseline, or non-current probe blocks;
4. `effect_absent` may open one freshly admitted retry;
5. `effect_committed` may proceed to terminal/closeout reconstruction only with validation;
6. ambiguous evidence remains manual and blocks successors.

## 4. Effect-boundary concurrency

Task Session binds attempt, semantic epoch, selected unit, producer, target inventory, baseline digests, and concurrency scope. Immediately before effect, compare-and-swap or a scoped lease must still match. A conflict blocks the losing attempt; preflight success is insufficient.

## 5. Causal event projection

Append or emit only event identity, causal predecessor, run/attempt/transition IDs, producer, native handle/digest, projected status, classification, and residue. Payload defaults to absent. Existing observability/runtime owner selects persistence; projection is never queried as semantic authority.

## 6. Orchestrate exact receipt-set repair

```text
compile wave -> persist exact expected action ids and receipt paths
on reduction -> load manifest, not directory glob
reject missing, duplicate, unexpected, identity-mismatched receipts
normalize exactly one receipt per action
reduce only normalized expected set
```

Regression: place unrelated valid/invalid JSON beside receipts; it must not enter the reducer. A missing expected receipt still blocks.

## 7. Orchestrate run-global action IDs

Allocate from one persisted run-level monotonic counter or compile all wave IDs before host effects. Never derive the next ID from current-wave cardinality. Persist allocation before spawn; duplicate/replay blocks without host call.

## 8. Series compatibility facade

The facade validates legacy input, maps it to the approved Implementation Readiness `until-real-blocker` profile, returns canonical receipt references, and writes no frontier/visited/retry/join/stop state. Unsupported legacy semantics block with an explicit migration diagnostic.

## 9. Parity and public boundary

Parity compares canonical identity, generated provenance, expected bytes, and fixture behavior. Public reconstruction uses public sources only, a field allowlist, private marker scan, example payload scan, and exact package sync. A private Refine artifact is evidence for the parent decision, not source text for publication.

