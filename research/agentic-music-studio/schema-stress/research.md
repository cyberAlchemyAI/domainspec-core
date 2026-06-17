# research.md — Primitive/Schema Stress (verbatim explorer returns)

Dispatch: `2026-06-16-music-studio-primitive-schema-stress` · research · 3 explorers (tensioned on
primitive-layer × methodology). Returns are verbatim; synthesis lives in `findings.md`.

---

## Explorer A — Nyquist, Harry (signal-structure primitivist, formal/compositional)

**Primitive set (one layer: deterministic signal/structure).** ~12 typed, seedable, diffable
structs, no perceptual adjectives: `Oscillator`, `Partial`/`PartialSet` (the additive spectrum =
the "violin" carrier), `Grain`/`GrainCloud`, `GendynWalk { breakpoints, amp_walk, time_walk, seed }`
(Xenakis polygon, C2), `RandomWalkBound { min,max,step_dist,mirror }` (the *bound*, not the noise;
field decomposition is A's inference), `Event`, `Pattern` (TidalCycles cyclic container, C1),
`Envelope`, `Tuning`/`Scale` (raw ratios), `Seed` (first-class for `R(S,seed)`, D1),
`OscMsg`/`MidiMsg` (transport). "That is the entire authoring vocabulary."

**Effects/sensations — NO, do not enumerate.** Effects enter only as a second, *non-authoring*
class: `Measurement { name, fn: Signal|Spec → ℝ, window }` and `Objective { measure_ref, target,
tolerance }`. An effect word is never stored — it is *resolved at parse-time* to an Objective over a
Measurement ("dark" → Objective{spectral_centroid, low}; "strange" → Objective{sethares_dissonance,
high-roughness}). The agent searches primitive params θ to minimize |measure(θ) − target| (D3), θ
ranging only over §1 primitives. The reverse channel (#10/C12) reports the *measurement* ("dissonance
= 0.71"), never the adjective. "Strangeness" lives in exactly one place: a transient target on a
Measurement during a search, discarded after the search resolves; the persisted spec holds only
primitives.

**Schema = closed primitive set P + small combinator algebra C over P + read-only Measurement/
Objective layer M (not in P).** Combinators (codomain always in P): `stack`, `seq`/`cat`, `every`/
`fast`/`slow`/`rev`/`degradeBy` (Tidal-class, seed-explicit), `route`, `bind`, `tune`. Closed/governed
because: no constructor yields a perceptual adjective (type system forbids it); M is a *separate
read-only* algebra that can score the spec but never be an *input* to a combinator (the firewall:
analysis scores, never authors); everything seedable → reproducible + diffable.

**Room-vs-governance: room is combinatorial and continuous, not enumerative.** Continuous (every
field is a real or a *bound*; `GendynWalk`'s 5 fields span an uncountable timbre space, spectrum
emergent C2); algebraic (small transform library, infinite patterns — the Tidal ceiling, C1).
"Room comes from the cardinality of parameter space, governance from the finiteness of the type set
— these don't trade off." Effects get unbounded room too, but in M (read-only scoring), at zero
governance cost.

**Operator example:** violin→`PartialSet`; stochastic→`GendynWalk` driving synthesis (spectrum
emergent, C2/D4, seed fixed); dark→Objective{spectral_centroid, low}, agent searches walk-bounds +
amplitudes (D3); dissonance scale→`tune(Pattern, Scale)` with Scale chosen by Objective over
`sethares_dissonance(PartialSet, interval)` (D5, timbre-dependent); strangeness→Objective{
sethares_dissonance, high} searched over Scale degrees — "strangeness" exists only as `target`
during the search; verify via #10 reporting numbers, human supplies the judgment (O1 is theirs).

**Self-objection (honest, real hit): the composability/holism gap.** The firewall assumes every
perceptual target decomposes into a measurement over signal. But many load-bearing sensations are
gestalt/context-dependent with no agreed deterministic measurement — "strangeness" is *not*
`sethares_dissonance`, that's a proxy A smuggles in, and O1 flags it unverified. Where a sensation
is irreducible, M can't author toward it (no measurement exists) → the search optimizes the wrong
objective. "My closure is bought by assuming perceptual reducibility." Ergonomics-first cuts against
A: forcing the human to translate every sensation into a measurement raises cognitive load.

---

## Explorer B — Fourier, Joseph (perceptual-feature primitivist, empirical/psychoacoustic)

**Layer claim:** the primitive layer is the closed set of computable psychoacoustic features — "the
layer at which governance (measurable ⇒ checkable) and musical meaning (the artisan thinks in dark/
rough/dense) coincide." Effects are open expressions over it, never primitives.

**Primitive set (CLOSED floor), each a feature `Signal → ℝ` with a deterministic estimator:**
`spectral_centroid` (≈darkness), `sensory_dissonance/roughness` (Plomp–Levelt `d(P,i)`, C3),
`inharmonicity`, `spectral_flux`, `density`, `loudness`, `pitch/f0`, `tempo/rate`, `attack_time`,
`harmonicity_profile` (the (freq,amp) partial vector both centroid and `d(P,i)` consume; "violin" =
match-distance to a violin template). **Boundary rule:** a thing is a primitive *iff* it has a pure
deterministic estimator two runs reproduce identically. "Strangeness" has no such estimator → barred.
This is the closed/open seam.

**Effects/sensations — NO, do not enumerate.** "Enumerating effects as primitives is the trap: the
list is unbounded, culturally relative, un-governable." An effect is an OPEN expression in a small
composition language over the CLOSED feature set: predicates `high(f)`/`low(f)`/`f≳τ`; boolean
`∧∨¬`; weighted aggregate `Σ wᵢ·gᵢ(fᵢ)` (the steerable objective, D3's f); temporal `Δf`,
`violated_expectation(f)`; conditioning relative to the timbre's own baseline (Sethares correction,
C3/D5). `strangeness ≔ high(roughness) ∧ high(inharmonicity) ∧ high(violated_expectation) ↦
maximize w₁·roughness + w₂·inharmonicity + w₃·flux`. A different artisan's "strangeness" is a
different expression over the *same* primitives — the disagreement becomes explicit and inspectable,
not hidden in a label.

**Schema:** `Feature {id, estimator (pure), unit, range}` (closed, the 10 only); `EffectExpr` =
pred | boolean tree | weighted objective | temporal; `Effect {name, expr, target, provenance}`.
**Admission rule (governance bites here):** (1) closure — every leaf is a Feature.id, no free
symbols (a new *feature* requires a governed estimator add; an effect can't smuggle one); (2)
computability ⇒ reproducible; (3) steerable target (search gradient, D3); (4) honesty tag —
labeled a *proxy*, never "this IS strange" (O1 guard). An effect failing (1) is rejected at author
time.

**Room-vs-governance:** effect space is unbounded and unowned (anyone writes `menace`/`shimmer`/
`seasick` instantly, zero schema migration) — strictly more room than named-sensation (no
standardization committee) and more *meaningful* room than raw-signal (musical thought, not DSP).
Governance never leaks because admission rule (1) forces every effect to bottom out in 10 estimators
⇒ automatically measurable, diffable, replayable, comparable (diff two artisans' "strangeness"
expressions). "Closed where it must be checkable, open where it must breathe." **O1 handled
honestly:** does not claim the proxy is the percept; claims the weaker, defensible thing — the proxy
is the only governable searchable handle, and the architecture *routes the gap to evidence* (honesty
tag + #10 feedback + listener study re-weights wᵢ).

**Operator example:** dark→`low(spectral_centroid)`; violin→`band(match_distance(P, violin_template))`;
stochastic→the engine whose θ the features score; dissonance scale→`roughness=d(P,interval)`, scale
chosen against the *fixed* dark-violin spectrum (C3/D5); strangeness→the composed weighted objective,
agent searches θ + intervals, human watches per-feature meters and judges felt-match. Five spec
edits, one closed feature set, zero generation.

**Self-objection (two real hits):** (A) signal-primitivist — "your features are *derived*, not
fundamental: centroid is a lossy projection, roughness needs a partial model that can be wrong on
inharmonic/noisy timbres (the GENDYN case). The lossless reproducible primitive is the signal/
synthesis-graph; your features are second-class observables." B concedes the layer is mid-level and
genuinely derived; defense is pragmatic (raw signal is reproducible but not *governable as musical
meaning*). (B) named-sensation — "composition-over-features is too diffuse; no musician reaches for
`w₁·roughness + w₂·inharmonicity`; you've pushed the contested modeling ('what IS strangeness') onto
every author every time with no shared vocabulary. 'Open composition' is a euphemism for 'unsolved.'"
The sharper hit; B's answer: it makes the contested modeling explicit and diffable rather than baked
in — but hasn't *solved* felt-match (O1 is exactly this gap). **Where B holds:** both objections
concede the core seam — governance requires a measurable floor; (A) wants it lower, (B) higher; the
feature layer is the unique band that is *both* artisan-thinkable *and* deterministically checkable.

---

## Explorer C — Alexander, Christopher (named-sensation primitivist, HCI/ergonomic-vocabulary)

**Stance:** the primitive layer is an enumerated, governed, growing vocabulary of named sensations
(à la *A Pattern Language*); features/signals are implementation detail reached only through a
sensation's binding. **Ledger anchoring (honest):** the mechanism is grounded (D2/D3/D5, process #3
C8 = "compiles to governed, artisan-editable vocabulary"), but the claim that the vocabulary *is the
primitive layer* (not a macro over feature-primitives) is C's design inference sitting on **O2**
(open: can "dark"/"strange" be compiled by a governed vocabulary without a model).

**Primitive = `SensationEntry { name, definition, binding:[Target], examples:[Reference], misuse,
status: seed|admitted|contested|deprecated, provenance }`**, where `Target := FeatureTarget |
ObjectiveTarget | EngineTarget` points at the lower layers (centroid / Sethares dissonance / GENDYN
walk bounds). Seed entries (8): **darkness** (centroid↓; "not quiet, not sad"), **strangeness**
(dissonance high-but-bounded + non-12-TET; "not dissonant-tension"; proxy/O1), **dissonant-tension**
(dissonance high vs the chosen timbre, D5), **warmth** (low-mid↑, rolloff↑; "not darkness"),
**violin-ness** (partial-profile match; "not a sample"), **menace** (darkness + slow amplitude
instability; "not loudness"), **liminal** (mid dissonance + slow drift; "not strangeness"),
**shimmer** (high-partial energy modulated; "not warmth"). The **misuse/contrast rows are
load-bearing** — each entry is defined partly *against its neighbors*; that contrastive boundary is
"exactly what an open feature-algebra cannot give you."

**Effects/sensations — YES, enumerate (the crux), but governed.** Admission procedure: propose →
prove → review → admit. (1) Any artisan proposes `status: seed` with all four fields; a name with no
binding is rejected on sight (the firewall against re-coining "warmth" as vapor). (2) Proof of
binding: must resolve downward to a real target `R(S,seed)` hits — *grounded* (source-backed feature/
objective → admittable) vs *proxy* (felt correspondence unproven, O1 → `seed`/`contested` only,
carries the O1 caveat, surfaced as "proxy you set, judge it", D3). (3) **Contrastive review (drift
prevention):** check against nearest neighbors, write the boundary into both misuse fields; if
indistinguishable by binding *and* felt definition → synonym, merge, not a new primitive. "The single
most important anti-drift gate." (4) Status lifecycle = governance not freezing; every change a
reviewable diff on V (like a spec diff, D1).

**Schema:** a piece is a `SensationComposition { voices: [{sensation, intensity, at?}] }`; resolution
is deterministic compilation `V ⊢ Composition → Spec` (each name's binding emitted as target rows
into the one shared Spec; realizer runs GENDYN + Sethares search; no model in the sound path,
C7/C8). Features appear only inside bindings, edited once by the entry author under review, never by
the composing artisan. V is itself versioned/diffable. **Ergonomics:** load lands on a small working
set of named handles the artisan already holds; "the human works in the units of their own taste"
(who-leads-when: human names #3 + steers #4, agent searches inside the binding + reports #10).

**Room-vs-governance — enumerated vocabulary gives MORE *usable* room:** shared named handles reduce
cognitive load ("darkness" is one chunk vs a vector expression rebuilt every time); reviewable =
room that *survives being handed to someone else* (open feature expressions are idiosyncratic, two
artisans' "dark-ish" vectors diverge and neither can read the other's); "distinctions are the room"
— misuse/contrast fields encode differences the ear cares about; an open algebra offers infinite
*points* but no *places*. **Risk conceded — combinatorial poverty / "can't say what isn't enumerated
yet":** answered by **admission-on-demand mid-session** — compose existing entries (menace = darkness
+ instability) or open a seed entry on the spot (name it, point at the example #5, agent proposes a
binding from current spec state, proceed at `status: seed`, review later). "The vocabulary is never a
closed gate — it's a frontier that advances exactly where artisans push it."

**Operator example (sensation authoring):** dark-violin-stochastic → invoke `violin-ness` + `darkness`
onto a GENDYN voice (bindings emit spectral targets, agent searches walk bounds); dissonance/
strangeness → `dissonant-tension` (grounded, dissonance-vs-this-timbre D5) + `strangeness`
(seed/proxy, surfaced "judge it"); mid-session at bar 12 the artisan hears "teetering" with no entry
→ admission-on-demand opens a seed entry → session yields both the piece and a candidate vocabulary
growth.

**Self-objection (three hits, the third hurts):** (1) enumeration never keeps up — if every session
spawns seeds, the "primitive layer" is mostly un-reviewed seeds and the features are what's actually
stable. (2) every artisan re-coins "warmth" — felt-words are private; contrastive review is expensive
and subjective with no ground truth (O1 all the way down); the vocabulary may fork into dialects
faster than review merges them, collapsing the room-vs-governance argument. (3) **the real hit — the
vocabulary is just presets/macros re-skinned:** if every entry is *defined by* its binding to
FeatureTargets/ObjectiveTargets, the binding is the primitive and the name is a label on a macro; the
feature layer is load-bearing and governable (centroid, Plomp–Levelt computable, source-backed), the
sensation name is derivative and contested (O1-unproven). C's defense (the name carries the felt
distinction + misuse boundary the binding alone doesn't) "is real but rests on O1 — the one thing the
tower flags unproven." Skeptic will demand one sensation whose value as a primitive is *not* reducible
to its binding; C's best candidate is the contrastive/misuse boundary (a *relational* fact about the
vocabulary, not a point in feature space) — but the skeptic can reply relational structure is just a
partition of feature space, recoverable without names. Unresolved — the O1-vs-O2 seam for the
synthesizer.
