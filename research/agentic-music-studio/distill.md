# Distill — Compact Operator Knowledge

## One-sentence model

An agentic music studio is one where **the human supplies intent and aesthetic judgment while the
agent does deterministic engineering and objective-driven search over a single shared, reproducible
spec** — so every interface (voice, live-code, gesture, annotation) is just an editor of that spec,
and no generative model is ever in the sound path.

## Compositional spine

```
        INTENT  ──(parse, governed vocabulary)──►  SPEC  ──(deterministic realize + search)──►  SOUND
          ▲                                          │                                            │
          │                                          │ one reproducible document                  │
   human judgment ◄───────── PERCEPTUAL FEEDBACK (meters, spectrum, predicted effect) ◄───────────┘
```

- **SPEC** is the lingua franca (D1). All write-interfaces edit it; it is diffable, forkable,
  replayable — craft preserved as authored artifact.
- **ENGINE + SEARCH** is the agent's intelligence: parametric deterministic synthesis (e.g.
  Xenakis/GENDYN-class) + optimization against computable objectives (e.g. Sethares dissonance).
- **FEEDBACK** closes the loop so human and agent share a model of the listener.

## What to borrow

- **Spec-as-lingua-franca** (Strasheela proves declarative composition works, S5/C5).
- **Objective-function steering** with psychoacoustic metrics — "name the effect, search the
  parameters" (Sethares, S3/C3; the operator's "strangeness via dissonance scale").
- **Live-coding as one high-craft surface** (TidalCycles, S1/C1) — process #8.
- **NIME's controller→mapping→engine separation** and "ergonomics lives in the mapping" (S4/C4).
- **The ten-process taxonomy and who-leads-when matrix** (`findings.md`) as the interface design
  checklist.

## What to keep analogy-only

- "**Compiler front-end**" for intent parsing — a useful frame for where a model *may* sit
  (parsing intent into spec fields), not a literal architecture decision yet.
- Calling the studio "agentic" — means *deterministic-engineering agent*, not LLM-with-tools.

## What to block

- **Generative-model audio synthesis** in the sound path (the S6 pattern). Violates "not relying
  on models", breaks reproducibility and craft. A model may parse intent (#3) but must never
  produce sound.
- Asserting a metric *is* the felt effect ("high dissonance = strange"): proxy, not truth (O1).

## The five-process walk-through (operator's example)

"create some dark violin stochastic synth, then use some dissonance scale to bring strangeness":
**#3 name** → **#1 create** → **#4 objective** → **#8 tune the stochastic process** → **#10 verify
by ear + meter** — all editing one spec, zero generation.
