# Research Direction — Steering Semantics (scoped: ONLY this)

**Status:** OPEN research direction (a seed, not a run). Opened from the SWU-7 task-session: the
weighted-objective fix (Option 1) works, but it exposed that *how a human steers a parametric synth by
critique* is a genuine research question, not a settled implementation detail. Scope is **only steering** —
not the engine, not the vocabulary, not the floor.

## The question
When the human says **"more bite"** / "darker" / "warmer" to an agent that tunes a deterministic synth by
objective search, **what should happen?** Concretely: how do plain-language critiques map to movement
through the engine's reachable space of timbres?

## Why it's non-trivial (what SWU-7 revealed)
The intent's targets genuinely **conflict** — "dark" (hold centroid low) pulls against "strangeness"
(maximize dissonance, which tends to raise centroid). So the set of achievable `(darkness, bite, …)`
points is a **Pareto front**, and steering = *navigating that front*. The first naive attempt (bump the
strangeness *target value*) was **inert** — the objective already maximized dissonance, so nothing moved.

## Interim solution (implemented, measured)
**Option 1 — weighted-sum steering.** Each target carries a `weight`; 'low' targets *seek* their value
(two-sided) so they compete with 'high' targets; a critique shifts a weight, sliding the trade-off.
Measured: `more bite` → centroid **499→558 Hz**, dissonance **1.37→9.30** (trades ~60 Hz of darkness for
~7× bite). Responsive and reproducible. **But weighted-sum is the crudest Pareto-navigation method** and
carries known limits — hence this direction.

## Open sub-questions to investigate
1. **Weighted-sum vs explicit Pareto navigation.** Weighted-sum can't reach concave parts of a Pareto
   front and the weight→outcome map is opaque ("how much weight = how much bite?"). Alternative: compute a
   small Pareto set and let the human *pick/scrub* between rendered options (show the front, not a dial).
2. **The magnitude problem.** "more bite" has no inherent size. Fixed deltas (current) vs adaptive step vs
   "keep nudging until the human stops" (interactive hill-climb).
3. **Preference / active learning.** Learn the weights from pairwise "this one or that one?" (preference-
   based multi-objective optimization; active preference elicitation) instead of a hand lexicon — *without*
   putting a model in the sound path (the model would only rank human-rendered options).
4. **Interactive evolutionary computation** (Dahlstedt 2001; Johnson 1999): human as the fitness function,
   the agent evolves candidates. Owned precedent — likely `build-from-owned`.
5. **Context-dependence & coupling.** "darker" after already-dark; "warmer" = several features at once
   (centroid down + roughness down + odd-harmonic up). The closed lexicon can't express these.
6. **Open-vocabulary critique.** Off-lexicon critiques ("less polite", "more like rain") — the same O2/LLM-
   front-end question as intent parsing, on the output side.
7. **Link to O1 (felt-match).** A critique is a *felt* judgment; its mapping to features is only as valid as
   the feature↔percept link (O1, open). Steering and O1 are entangled.

## Scope boundary (what this is NOT)
Not the engine, the DSL, the vocabulary, the floor (Spectralize-v2), or the felt-match study (O1) — those
are separate. This direction is *only* the critique→movement mapping.

## Owned anchors to sweep (when run)
Interactive evolutionary computation (Dahlstedt, Johnson); preference-based / interactive multi-objective
optimization (Pareto navigation, reference-point methods, NIMBUS-style); creativity-support-tool steering
patterns; automatic-synthesizer-programming interaction studies (Yee-King). Precedent-first: most of this
is likely `build-from-owned`.

## Next route (when prioritized)
A `research` dispatch (synthesis + precedent sweep) scoped to "critique→Pareto-navigation for parametric
synth steering" → feeds an `invoke design` for steering-v2. **Not blocking v1** — Option 1 is the shipped
interim and the intent-engine works end-to-end without it.
