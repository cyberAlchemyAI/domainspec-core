# Governed Definitions

Load-bearing terms the higher layers depend on. Each: formal expression · notation/intuition ·
anti-misuse. Local research definitions — **not** promoted to any canonical surface.

## D1 — Spec (musical spec)

**Formal.** A persistent, deterministic, version-controllable document `S` declaring (a) musical
*intent* (targets: timbre, rhythm, harmony, perceptual effect) and (b) *constraints* (what must
hold), such that a deterministic realizer `R(S, seed) → audio/score` reproduces the same artifact
for the same `(S, seed)`.

**Intuition.** Source code for a piece. You can diff it, fork it, review it, replay it.

**Anti-misuse.** A spec is **not** a prompt. A prompt asks a model to invent; a spec declares what
is true and is realized deterministically. If two runs of `R(S, seed)` differ, it is not a spec.

## D2 — Agentic engineering (vs. generative modeling)

**Formal.** Producing music by an agent that (1) compiles intent into a spec, (2) constructs/searches
parametric, deterministic engines, and (3) optimizes their parameters against computable objective
functions — with the human supplying intent and aesthetic judgment. Distinct from generative
modeling, where a learned model maps prompt → audio.

**Intuition.** The agent is an engineer + search process, not a composer-in-a-box.

**Anti-misuse.** "Agentic" here ≠ "an LLM with tools that generates audio." The defining line:
**the sound producer is deterministic and authored**, not a generative model (C7, C8).

## D3 — Objective-function steering

**Formal.** A control process where the human names a perceptual target `t` (e.g. "strangeness")
mapped to a computable objective `f` (e.g. target dissonance from a Sethares curve), and the agent
searches engine parameters `θ` to minimize `|f(θ) − t|`, surfacing candidates for human judgment.

**Intuition.** "Bring strangeness" = set the dial's *target*, let the agent find the settings, you
approve the result.

**Anti-misuse.** The metric is a *proxy*, not the goal. `f` predicting `t` is an empirical claim
(O1) requiring evidence; never assert "this is strange" because `f` is high — assert "this hits the
dissonance target you set; judge it."

## D4 — Stochastic synthesis (Xenakis/GENDYN class)

**Formal.** Synthesis where the waveform is a polygon of breakpoints deformed over time by bounded
random walks; spectral content is *emergent* from the walk dynamics rather than specified in the
frequency domain (S2).

**Intuition.** You shape the *behavior of the randomness*, and timbre falls out of it.

**Anti-misuse.** "Stochastic" ≠ "random/uncontrolled." The artisan controls the *bounds and
dynamics* of the walks (and the seed) — fully reproducible. Do not equate with model sampling.

## D5 — Dissonance curve (Sethares class)

**Formal.** For a spectrum `P` (partials + amplitudes), a function `d(P, interval)` giving sensory
dissonance via Plomp–Levelt summation; a "dissonance scale" selects intervals/tuning against target
values of `d` for the chosen timbre (S3).

**Intuition.** Pick the timbre, *then* the scale that sits where you want on the consonance↔roughness
axis. Dissonance is a property of timbre+tuning together, not of intervals alone.

**Anti-misuse.** A 12-TET "dissonant" interval can be consonant under another timbre and vice versa;
never treat dissonance as a fixed property of the interval (the core Sethares correction).

## D6 — Communication process

**Formal.** A `(speech-act, initiative-profile)` pair describing an exchange between human and
studio: the *speech-act* is what the message does (command / declare / set-goal / demonstrate /
critique / author-rule / perform / report), and the *initiative-profile* is who-leads-when
(human-led / agent-led / shared) across the exchange. Realizable over one or more modalities.

**Intuition.** Not "voice vs. text" but "*am I ordering, declaring, setting a goal, giving an
example, or critiquing* — and who drives?"

**Anti-misuse.** Do not collapse process into modality. "Voice control" is a modality that can carry
several processes (a command, a goal, a critique); designing the studio means designing the
*processes*, then choosing modalities for each (C11).

## D7 — Mapping (NIME)

**Formal.** The rule set connecting controller state/gesture to sound-engine parameters (S4). May
be one-to-one, one-to-many, many-to-one, or many-to-many; mapping choice largely determines
expressivity and ergonomics.

**Anti-misuse.** Ergonomics is a property of the *mapping*, not the controller alone. A great
controller with a literal one-to-one mapping can feel worse than a simple controller with a rich,
well-designed mapping.
