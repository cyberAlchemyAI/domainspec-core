# Distill — the one-screen model

> **Reading layer.** This is a distillation of source material, not new source. Labeled
> `local-inference` except where it quotes the spec.

## One sentence

**MTNG is a discipline for splitting one messy report into the fewest contracted, validated
pieces that still recombine into an honest artifact — and V1 ships that discipline as an
offline issue-packager, not a live agent controller.**

## The compositional spine

```
selected Signal(s)
   → propose Mode(s)              (kind-of-work hypotheses; routing-signature hints)
   → branch into Node(s)          ONLY when a contract boundary changes  (else: fast path)
   → each Node runs under a contract  (accepts/rejects/context/output/validator)
   → Validator gates each Node    (also detects misrouting → bounded reroute)
   → Synthesis recombines         (passed + partial + failed-as-status; never hides conflict)
   → emit: issue packet · memory candidates(review-only) · contribution records(no value) · OKF export
```

Two invariants hold the whole thing up:

1. **Branch only on a named boundary.** No fan-out without a structural reason. (DEF-3)
2. **Validate before synthesis; never flatten.** Failures and conflicts survive the merge. (DEF-4, DEF-5)

## What carries the reasoning load

- The **node contract** (DEF-2) — without it MTNG is just a summarizer. It is the primitive that
  makes delegation inspectable.
- The **validator-as-misrouting-detector** (DEF-4) — the cleverest idea in the spec: a quality
  gate doing double duty as a routing corrector.
- The **defer-valuation** move (DEF-6) — capture contribution *structure*, refuse to score it.

## Borrow / analogy-only / block (one-liner each — full table in bridge-decisions.md)

| Idea | Verdict for Arcanum | One-line why |
|---|---|---|
| "Branch only on named boundary" | **borrow-carefully** | Same spirit as the P1 dispatch triggers; reinforces, doesn't replace. |
| "Validator = misrouting detector" | **borrow-carefully** | Maps to check-tension as a structural gate. |
| "Capture contribution, defer valuation" | **borrow-carefully** | Matches register-dispatch's no-scoring stance. |
| `closed_result` / `exit_reason` parallel | **analogy-only** | Nice mirror; don't merge the vocabularies. |
| MTNG as a runtime/orchestrator | **block** | V1 is explicitly not that; Arcanum already routes via dispatch. |
| "OKF as the export standard" | **future-work** | Unverified format; pin before adopting. |
| The numeric Branch Pressure Score | **block (for now)** | Deferred even by the spec; no empirical basis yet. |

## The honest shape of the proposal

v2 is a **disciplined narrowing** of an ambitious v1. The narrowing is the strength: every
reviewer asked for the same boundary and the author drew it. But narrowing scope is not the same
as proving value — the post-hoc packager's usefulness, its classifier accuracy, and its overhead
all remain **unmeasured**, and the host architecture it must plug into remains **unmapped**. The
design is review-ready; it is not build-ready.
