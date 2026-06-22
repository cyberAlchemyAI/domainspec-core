# Agentic Music Studio

Turning human intent into music through deterministic engineering -- not generative models.

A studio where the human **directs** -- says what they want, judges it, edits the code -- and an
agent **writes deterministic, inspectable code** that is then run to make sound. The defining line:
**no AI model ever generates the audio.** A model may only parse intent into an inspectable spec; the
music comes from running seeded, reproducible code. Craft is preserved because the artifact is
authored, diffable, replayable code -- not a black-box output.

> **The one-sentence thesis.** You supply intent and taste; the agent does deterministic engineering --
> objective search against real measurements -- over one shared, reproducible spec. Every interface is
> a way of editing that spec, and no generative model is ever in the sound path.

## The pipeline

```
INTENT            SPEC              PROGRAM            RENDER          STEER
"dark violin   -> targets       -> agent writes    -> deterministic -> human hears +
 stochastic,      (closed          Tidal-style        OBJECTIVE         reads/edits the
 bring            vocabulary,      code               SEARCH tunes      code + critiques
 strangeness"     no model)                           it (no model)     -> loops back
```

Where the intelligence lives: not in "writing the code" (a deterministic template fill) but in the
**search** that engineers the synth parameters to hit measurable perceptual targets. That is *agentic
engineering*.

## What we built

Two Python packages, fully deterministic, with zero models in the sound path.

- **studio-core** -- the engine + measurement floor: GENDYN dynamic stochastic synthesis (Xenakis), Sethares sensory-dissonance, spectral features, a gradient-free objective search, and a feature meter (the reverse channel back to the human).
- **intent-engine** -- intent to agent-written code to sound: a small Tidal-flavoured DSL the agent writes and the human reads/edits, a closed-vocabulary resolver, the search tuner, and a steering loop (critique + hand-edit). 14 automated tests green; renders real, playable WAV audio.

> **It makes sound today.** The studio renders playable audio from the operator's own example --
> "dark violin stochastic synth, bring strangeness" -- as deterministic, seeded code. Xenakis
> stochastic synthesis is harsh and granular by nature; that texture *is* the stochastic synth, not a
> smooth violin.

## Key findings

Each is backed by an artifact -- a test, a measurement, or an adversarial review.

### 1. Effects are not primitives -- they are objectives over a closed floor

A tensioned multi-agent design review settled the core schema question. Primitives are a small,
**closed** set of measurable features. Effects and sensations like darkness or strangeness are **open**
objectives composed over them; named effects are governance labels, not a new primitive layer. The
"named-effect-as-primitive" idea was shown to collapse into a re-skin of a saved objective.

### 2. The floor must be measured, not assumed

Reading a stochastic timbre's spectrum by peak-picking wobbled 6.1% just from changing analyzer
settings -- the perceptual floor was not solid for exactly the sound the project is about. The fix: a
full-spectrum, multitaper "moment centroid". We **measured** the result rather than assuming it.

| Estimator | Centroid drift on GENDYN | Verdict |
| --- | --- | --- |
| Peak-pick (old) | 6.1% median | fails the 5% bar |
| Multitaper moment (new) | 1.3% median | PASS -- analyzer-independent |
| Clean additive tone | 0.05% | reference baseline |

### 3. Honesty discipline, enforced

Every perceptual claim is labelled: analyzer-independent vs felt vs proxy. A verification pass caught
us over-claiming the easy feature (darkness "aims for real") and we corrected it: the number is a
property of the sound, but whether it matches *felt* darkness is a separate, open listening question.

### 4. Steering is Pareto navigation

Targets genuinely conflict -- "dark" (low centroid) pulls against "strangeness" (high dissonance) -- so
steering means moving along a trade-off front. The critique "more bite" slides that trade-off
measurably:

```
baseline        : centroid 499 Hz   dissonance 1.37
after "more bite": centroid 558 Hz   dissonance 9.30   (trades darkness for bite)
```

## What is deliberately open

Named, scoped, and not blocking the v1 proof.

- **Spectralize-v2** -- a peak-free roughness so dissonance/strangeness is as stable as darkness is now.
- **O1 felt-match** -- a listener study: does the dissonance objective actually predict felt strangeness? Handed to an evidence harness with a frozen, pre-registered criterion.
- **Steering-v2** -- how should a human steer by critique? Weighted-sum works as an interim; explicit Pareto navigation / preference learning is the open research direction.
- **Scope** -- open-vocabulary intent, plus rhythm and pitch (a sequencer + scale module). v1 is a single-voice timbre engine on purpose.

## Status

> **v1 is a working proof -- success.** Intent goes in; the agent writes deterministic, inspectable
> code; a search tunes it to hit measurable targets; it renders real audio; the human hears it, reads
> the code, and steers. No generative model touches the sound. The craft stays with the human; the
> engineering grind goes to the agent.

### How we worked (method)

The project was developed through a governed pipeline: research towers to ground the ideas, a tensioned
multi-agent design dispatch to settle the schema, layered build plans, adversarial verification passes,
and refresh cycles -- every finding tied to an artifact, every claim kept no larger than its proof.

---

Built on: Xenakis dynamic stochastic synthesis; Sethares "Tuning, Timbre, Spectrum, Scale"; Thomson
multitaper spectral estimation; TidalCycles live-coding; NIME interface design.
