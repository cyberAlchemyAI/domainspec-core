# distill.md — The Smallest Coherent Model

**Date checked:** 2026-06-10

## One-sentence model

> Continued-pretraining a 7B base model on ~1.9B tokens of reputable Brazilian legal text
> buys measurable legal-benchmark gains (~+4.7 pts) but pays for them with catastrophic
> forgetting of general knowledge (~2–4 pts down in PT and EN) — specialization is
> redistribution, not free addition.

## Compositional spine

```
reputable in-domain corpus   (academic + LexML statute + STF case law, ~1.9B tokens)
        │   high-quality-data lever
        ▼
continued pretraining        (Mistral-7B, ~4 epochs, ~7.96B tokens processed)
        │   weight-mutating specialization
        ▼
measured outcome
   ├── IN-BAND  : legal benchmarks ↑  (OAB/ENAM mean 44.5 → 49.2)
   └── OUT-BAND : general knowledge ↓ (PT 50.5 → 48.1 ; EN 61.6 → 58.0)
        │
        ▼
trade-off law: the same operation that lifts the domain lowers the rest.
```

Recompose check: corpus -> CPT -> (gain, forgetting) reproduces the paper's whole argument.

## Borrow / Analogy / Block for Jusbrasil

- **BORROW (carry as-is):** The empirical trade-off itself. "In-house continue-pretrain on
  reputable Brazilian legal text gives real, measured legal gains" is a directly usable,
  evidenced data point for the foundation-model layer decision.

- **ANALOGY (use as a frame, not a number):** *Narrow-band amplifier.* A specialized base is
  louder in-band (law) and quieter out-of-band (general). Good when traffic is law-pure; lossy
  when traffic is mixed. This frames the build-vs-buy choice better than raw accuracy deltas.

- **BLOCK (do NOT carry):** "Specialized base model = better model." False. Juru is narrower,
  not uniformly better. Also block treating exam-accuracy as production-quality, and block
  assuming the ~1.9B-token recipe transfers to Jusbrasil's larger/different corpus without
  re-measurement.

## The compression that matters for the call

Specialization is a **choice to forget**. The decision is not "is a legal model good?" but
"can we afford for the base model to be worse at everything that is not law?" — and for mixed
production traffic, the usual answer is RAG-over-frontier or a router, reserving CPT for
law-pure, latency/cost-sensitive, offline-defensible workloads.
