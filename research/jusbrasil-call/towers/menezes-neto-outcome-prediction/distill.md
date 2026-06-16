# Distill

## One-sentence model

Feed only the **first-instance decision text** of a Brazilian federal small-claims appeal into a transfer-learned language model, and it predicts whether the appellate panel will affirm or reverse **better than experienced human judges and clerks given the same text** — modestly in absolute terms (MCC ≈ 0.37) but ~3x the best human.

## Compositional spine

```
High-volume, text-rich, imbalanced legal corpus (765k TRF5 appeals, 79% affirm)
        │
        ▼
Derived binary label (affirm/reverse) via ≥2-of-3 weak-signal voting   ← reproducibility weak point
        │
        ▼
Time-sequential split (no future leakage)                              ← realism guard
        │
        ▼
Three text models: ULMFiT (best) / BERT+LSTM / Big Bird                ← long-doc handling matters
        │
        ▼
MCC as honest metric under imbalance                                   ← not accuracy/F1
        │
        ▼
Head-to-head vs 22 experts on SAME inputs                              ← the credibility move
        │
        ▼
Result: model 0.3688 vs expert 0.1253 (~2.9x), all models beat experts under 0.99 CI
```

The spine's load-bearing joints: **(1)** a derived label, **(2)** a leakage-safe split, **(3)** a same-inputs human baseline. Remove any one and the headline claim weakens.

## Borrow / Analogy / Block

**BORROW (transfers cleanly to the Jusbrasil product):**
- The **same-inputs human baseline** as the way to substantiate "better than experts." Reusable methodology for "Probabilidade de Êxito."
- **MCC (and calibration) over raw accuracy** for imbalanced legal outcomes — accuracy would look great by always predicting "affirm" and be useless.
- **Time-sequential evaluation** as the default for any legal-outcome model (random splits flatter the model and mislead the business).
- BrCAD-5 as a **public benchmark / cold-start asset** for a TRF5 prototype.

**ANALOGY (transfers with adaptation):**
- ULMFiT/BERT/BigBird circa 2022 → today's LLMs/long-context encoders. The *architecture* is dated, but the *finding* (decision text carries predictive signal beyond human reading) generalizes; expect to re-instantiate with modern models.
- TRF5 affirm/reverse → Jusbrasil's national, multi-court, lawyer-side "êxito" framing. The target must be redefined (win for *whom*? at *what* stage?) and re-labeled per jurisdiction.

**BLOCK (does NOT transfer / must not be copied):**
- Do **not** copy the label-construction shortcut (filename/regex/metadata voting) into production without an auditable labeling pipeline — it is the paper's biggest reproducibility liability.
- Do **not** generalize TRF5 (one region, federal small-claims) to all Brazilian courts/instances; the paper itself does no cross-region validation.
- Do **not** present the result as a reliable forecast — the absolute MCC (~0.37) and the authors' "promising/assistive" framing block any "guaranteed outcome" product claim.
