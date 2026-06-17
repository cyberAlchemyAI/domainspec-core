# Learning Pack — Agentic Music Studio: Interfaces as Communication Processes

For the operator. Plain language, one worked example threaded throughout, source-backed claims
labeled, honest about its cutoff.

## The core idea (one sentence)

Build a studio where **you supply the intent and the taste, and the agent does deterministic
engineering and goal-driven search over one shared, reproducible spec** — so every interface is just
a different way of editing that spec, and no generative model is ever in the sound path.

## Why your example already proves the thesis

> "create some dark violin stochastic synth, then use some dissonance scale to bring a strangeness
> to the listener."

Each phrase is a real, buildable engineering target — not a vibe:

- **"dark violin"** = a *timbre target* — a spectrum (dark ≈ more low-partial energy; violin ≈ match
  violin partials). [Sethares, timbre↔spectrum — primary-source]
- **"stochastic synth"** = *dynamic stochastic synthesis* (Xenakis/GENDYN): the waveform is a shape
  deformed by controlled random walks; the timbre *emerges* from how the randomness moves — and it's
  fully reproducible because you control the bounds and the seed. [primary-source]
- **"use some dissonance scale to bring strangeness"** = you name a *perceptual goal* ("strangeness")
  and the agent reaches it by a *deterministic means*: compute the dissonance curve for that timbre,
  pick a scale whose intervals land where you want on the consonance↔roughness axis. Dissonance is
  computable, and it depends on the timbre, not just the interval. [Sethares — primary-source]

So you're not describing prompt-to-audio. You're describing **name the effect → agent engineers
toward it → you judge**. That is the whole studio.

## The architecture in one diagram

```
    INTENT ──parse (governed vocabulary)──► SPEC ──deterministic realize + search──► SOUND
       ▲                                      │  (one reproducible document)           │
       │                                      │                                        │
   your judgment ◄──── perceptual feedback: meters · spectrum · predicted effect ◄─────┘
```

- The **spec** is the lingua franca — like source code for a piece. Diff it, fork it, replay it.
  Craft is preserved because the artifact is *authored*, not a black-box output. [Strasheela proves
  declarative composition works — primary-source]
- The agent's intelligence is **engineering + search**, not generation.
- A model, *if* you use one at all, sits only at the front: turning "dark violin stochastic" into
  spec fields from a vocabulary *you* can inspect and edit — a compiler front-end, never the
  composer. [design stance — labeled inference, not source fact]

## The answer to your question: ten communication processes

You asked what *interfaces, as communication processes,* the studio could have. A communication
process = **what kind of message it is + who leads when** — a layer above "voice vs. text". Here are
ten; most can ride voice, text, gesture, or annotation.

| # | Process | What you say/do | Who leads | In your example |
|---|---|---|---|---|
| 1 | **Imperative** — do this now | "mute the bass", live eval | you → agent executes | "create … synth" |
| 2 | **Declarative** — this must stay true | "bass never clashes with the kick" | you declare, agent maintains | "dark", "violin", "stochastic" as persistent targets |
| 3 | **Intent naming** — name the aesthetic | "a dark violin stochastic synth" | you name, agent compiles to spec | the whole opening phrase |
| 4 | **Objective steering** — name the effect | "bring strangeness" | you set goal + judge, agent searches | dissonance-curve search |
| 5 | **By-example** — like this | point at a clip / hum a phrase | you point, agent analyzes & fits | "strange like that Penderecki bit" |
| 6 | **Conversational** — propose/critique | "too muddy" → "more bite" | shared turn-taking | shaping the synth by ear |
| 7 | **Annotation** — mark the timeline | "more tension *here*" | you mark, agent satisfies | "strangeness peaks at bar 12" |
| 8 | **Rule authoring** — write the process | edit patterns / random-walk bounds | you (this is where craft lives) | hand-tune the stochastic walks |
| 9 | **Gestural** — play it | ride a fader, breath, sensors | you perform, agent maps | sweep "darkness" live |
| 10 | **Perceptual feedback** — agent reports | meters, spectrum, "reads as strange" | agent → you | watch the dissonance you're actually hitting |

**The keystone is #10.** For human-agent symbiosis you need a *shared model of the listener* — the
agent must show you what it perceives, not just take orders. Pair every other process with #10 and
the studio stops being trial-and-error.

**They cohere because** #1–9 are *write* paths into the one spec and #10 is the *read* path back.
Modalities are interchangeable editors; the deterministic engine + objective search is the shared
core. Your example is really five of them in sequence: **#3 name → #1 create → #4 objective → #8
tune the process → #10 verify by ear and meter** — zero generation anywhere.

## What to build first (borrow/block)

- **Build:** the spec backbone (#2), one stochastic engine (GENDYN-class), one objective (Sethares
  dissonance), and the feedback meter (#10). That's the smallest loop that proves the thesis.
- **Block:** any generative model in the sound path. A model may *parse intent* (#3); it must never
  *produce sound* — that's the line that keeps craft and reproducibility.
- **Defer (needs evidence, not reading):** whether a dissonance metric actually predicts felt
  "strangeness" — that's a listener study, routed to an evidence harness.

## Honest cutoff

- No source here was read in full — summaries only. Before implementing the GENDYN engine or the
  dissonance metric, read the Xenakis and Sethares sources end-to-end (`levels/L0-corpus.md`).
- The ten-process taxonomy is **design synthesis** (labeled `operator-reading`/`local-inference` in
  `claim-ledger.md`), grounded in the sources but not stated by them.
- Two big questions are unproven and need experiments, not more reading: does the dissonance metric
  predict "strangeness" (O1), and can "dark"/"strange" be compiled by a *governed* vocabulary
  without a model (O2). See `bridge-decisions.md` → evidence handoff.
- Adjacent systems (Sonic Pi, ChucK, Max/MSP, FoxDot) were not surveyed and could change the
  taxonomy.

## Sources

- [TidalCycles](https://tidalcycles.org/) · [TidalCycles (Wikipedia)](https://en.wikipedia.org/wiki/TidalCycles)
- [Xenakis — Stochastic Synthesis](https://www.iannis-xenakis.org/en/stochastic-synthesis/) · [Implementing Dynamic Stochastic Synthesis (HAL)](https://hal.science/hal-02986346v1/document)
- [Sethares — Tuning, Timbre, Spectrum, Scale](https://sethares.engr.wisc.edu/ttss.html) · [William Sethares (Wikipedia)](https://en.wikipedia.org/wiki/William_Sethares)
- [NIME — New Interfaces for Musical Expression](https://en.wikipedia.org/wiki/New_Interfaces_for_Musical_Expression)
- [Strasheela](https://github.com/tanders/strasheela) · [Strasheela (algorithmic.net)](http://www.algorithmic.net/system/strasheela)
- [AI Music Agents (contrast case)](https://www.soundverse.ai/blog/article/ai-music-agents-explained)
