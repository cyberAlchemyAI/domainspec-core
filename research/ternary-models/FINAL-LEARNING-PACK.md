# Final Learning Pack

Profile: ternary-models

Status: partial

Promotion scope: local-research-only

## One Sentence

Ternary-model development should begin from owned prior art: represent weights
as `{-1,0,+1}`, keep training recipe and inference kernels inside the claim
boundary, and treat source-reported efficiency as a hypothesis until measured.

## Source-First Spine

| Layer | Source meaning | Closure artifact |
| --- | --- | --- |
| representation | weights constrained or trained into three values | `NOTATION.md`, `DEFINITIONS.md` |
| training | native low-bit training or ternarization/distillation recipe | `tracks/paper-claim-ledger.md` |
| systems | storage/kernel/runtime path for practical speed or energy gains | `levels/L1-residue-map.md` |
| evidence | source-reported claims awaiting local reproduction | `residue/open-residue.md` |

## Notation Reading

Read `NOTATION.md` before the claim ledger. In particular, distinguish `b1.58`
from binary `1-bit`, and distinguish weights from activations.

## Operator Model

```text
Do not ask "can we quantize a model?"
Ask "which representation, training path, scale/activation handling, runtime,
and evidence route make a ternary model useful for our target?"
```

## What To Borrow Carefully

- `{-1,0,+1}` as the local anchor for ternary weights.
- Native low-bit training as a different claim from post-training
  ternarization.
- bitnet.cpp as the first implementation surface to inspect.

## What To Keep Analogy-Only

- "1-bit" when it means ternary weight representation.
- General "full precision parity" language without benchmark conditions.

## What To Block

- Novelty claims for ternary models.
- Local performance claims without measured evidence.
- Canonical vocabulary promotion before a separate governed decision.

## Remaining Honest Cutoff

The tower is started for source-backed orientation. It is not closed for:

- final related-work sweep;
- implementation recommendation;
- benchmark/evidence production;
- canonical promotion.

## Sources

See `sources/source-record.md`.
