# findings.md — Primitive/Schema Model (synthesis, reviewer-integrated)

Dispatch: `2026-06-16-music-studio-primitive-schema-stress`. Synthesis (Shannon) over explorers
A/B/C (`research.md`), **revised after the zig-zag review** (Lakatos precedent / Popper non-vacuity
/ Wittgenstein definitional-soundness). Tower: `definitions.md` (D1–D7), `claim-ledger.md`
(C1–C12, O1, O2). Every claim **claim ≤ proof**; keystone claims carry an inline collapse-test.

> **What the review changed (read this first).** Three corrections survived adversarial review and
> are now baked in: **(P)** the closed floor does *not* realize the operator's own example until a
> seedable `Spectralize: Signal→P` estimator is admitted into the closed core (Popper's localized
> KILL + repair); **(W)** "named effects" are **not** a primitive layer and **not** a first-class
> object — they collapse to *saved L2 expressions + labels + a contrastive-review governance gate*
> (Wittgenstein); **(L)** nothing here is novel — every move is `build-from-owned` with real owners
> (Lakatos), and the prior draft both over-claimed novelty (L2) and under-claimed ownership (L1).

---

## Recommendation (the model in 6 sentences)

The three explorers are strata, not rivals, and the corrected stack has **three closed layers + one
open layer**. **L0** = A's deterministic signal/structure primitives (the lossless thing a realizer
runs). **Lσ (new, forced by review)** = a seedable, parameter-frozen `Spectralize: Signal→P`
estimator that turns realized signal into a partial set `P` — without it the perceptual floor cannot
compute on the operator's own stochastic timbre. **L1** = B's closed set of computable perceptual
features over `P`, each a pure estimator `Signal→ℝ` — the governing floor where *checkable* and
*musically-meaningful* coincide, every feature `build-from-owned` (MPEG-7 / Peeters / Sethares).
**L2** = effects, authored as open weighted objectives/constraints over L1 — which is just the tower's
**D3 Objective** renamed and domain-restricted, i.e. the owned "automatic synthesizer programming"
loop (Risset–Mathews → Horner 1993 → DDSP). So the operator's question resolves cleanly: **do not
enumerate effects as primitives; effects are compositions (objectives) over a small closed feature
floor** — and the "named vocabulary" is kept only as **ergonomic labels + a governance gate** over
those compositions (the AudioCommons-style descriptor-to-feature binding), *not* minted as a
primitive or a first-class object, because its contrastive boundary is provably just the
set-difference of two bindings.

---

## Verdict matrix (precedent column filled by Lakatos; witness column adjudicated by Popper)

| Stance | owner / precedent | witnessed? (operator example e2e) | definitionally-sound? | verdict | use-mode |
|---|---|---|---|---|---|
| **A** — signal/structure are the *only* primitives; effects are non-authoring measurements; never enumerate | Xenakis/GENDYN (C2,D4), Tidal (C1), Strasheela CSP (C5) — owned | YES as substrate; but routes every percept through a measurement the human pre-translates (ergonomics cost) | **L0 = real joint** (producer side; lossless reproducible substrate). Fails *as the governing floor* | **GO as L0 only / KILL as governing floor** | build-from-owned |
| **B** — closed computable features are primitives; effects are open expressions; never enumerate | `d(P,i)`=Sethares/Plomp–Levelt (C3,D5); centroid/flux/density = **folklore, precedent-clean** (MPEG-7 variants); inharmonicity/attack/loudness/f0 = **owned** (Peeters 2004, MPEG-7 LogAttackTime, Zwicker/ITU-BS.1770, YIN/CREPE) | **CONDITIONAL** — only after `Spectralize` (Lσ) is added; without it the floor collapses to byte-reproducibility of a seed-frozen signal (= L0 relabeled) on GENDYN input | **L1 = real joint** (observer side; "primitive iff a pure estimator two runs reproduce identically") — the closed/open seam | **GO as L1 — the governing floor, conditional on Lσ** | **build-from-owned** (all estimators owned/folklore; O5 closes) |
| **C** — enumerate a governed vocabulary of named sensations *as the primitive layer* | named-descriptor-bound-to-features = **AudioCommons timbral models** (Pearce/Surrey); form = *A Pattern Language*; relational defn = SKOS/ISO 25964; bipolar contrast = von Bismarck 1974 | YES at the authoring surface | **As a primitive layer / first-class object: RE-SKIN** (Wittgenstein) — the misuse boundary is the set-difference of bindings, recoverable as an L1-region; name = macro alias. **The review *gate* + labels survive as governance, not as a layer** | **KILL as primitive layer & as first-class object / GO as governance-gate + labels over L2** | build-from-owned (AudioCommons + the review gate) |
| **L2 "effect" object** | objective-function steering = **automatic synthesizer programming**: Risset–Mathews 1969 → Horner/Beauchamp/Haken 1993 (GA spectral match) → DDSP (Engel 2020); interactive = Johnson 1999 / Dahlstedt 2001; lib SpiegeLib | YES (it *is* the search loop) | **RE-SKIN of D3 Objective** (Wittgenstein) restricted to L1 leaves; boolean sub-case re-skins C5 Strasheela constraint — the restriction is the only added work | **GO (build-from-owned); drop any novelty claim** | build-from-owned |
| **3-layer stratification** | **NIME mapping group**: Rovan/Wanderley 1997, Hunt/Kirk 2000, Hunt/Wanderley/Paradis 2003, Wanderley/Depalle 2004 | n/a (architectural) | real joint (producer/observer split; controller→mapping→engine) | **GO (build-from-owned)** | build-from-owned |
| **SYNTHESIS** — L0 · Lσ · L1 (governing floor) · L2 effects=objectives; names = labels+gate | composes the above; the **only** thin novelty seam is the *first-class contrastive/misuse edge*, and Wittgenstein collapses even that absent a non-reducible case (O6) | **GO conditional on Lσ** (Popper's repair) | real joints at L0/Lσ/L1; "effect" and "named-effect-layer" are re-skins, demoted accordingly | **GO with required repairs** | **build-from-owned throughout** |

---

## The layered model (revised)

### 1. The layers — closed/governed vs open

| Layer | Content | Status | Owner |
|---|---|---|---|
| **L0 — Realization substrate** | A's ~12 typed seedable structs (`Oscillator`, `PartialSet`, `GendynWalk`, `RandomWalkBound`, `Event`, `Pattern`, `Envelope`, `Scale`, `Seed`, transport) + A's combinator algebra (codomain always in L0) | **CLOSED / frozen** | build-from-owned (C1 Tidal, C2/D4 GENDYN, C5 Strasheela) |
| **Lσ — Spectralize (NEW, forced by Popper)** | `Spectralize { window, hop, peak_threshold } : Signal → P` — a seedable, parameter-**frozen** partial-extraction admitted into the closed core, so `P` is a function of `(S, seed)` alone | **CLOSED / frozen + version-pinned** | build-from-owned (STFT/peak-pick; HPS Schroeder 1968, partial-tracking McAulay–Quatieri 1986) |
| **L1 — Perceptual-feature floor** | B's closed feature set over `P`: `spectral_centroid`, `roughness=d(P,i)`, `inharmonicity`, `flux`, `density`, `loudness`, `f0`, `rate`, `attack_time`, `harmonicity_profile` | **CLOSED / governed** (checkable ∧ meaningful) | build-from-owned (Sethares/Plomp–Levelt; Peeters 2004; MPEG-7; Zwicker/ITU; YIN/CREPE; centroid/flux/density folklore) |
| **L2 — Effects (= objectives)** | open weighted objectives / boolean constraints over L1: `Σwᵢ·gᵢ(fᵢ)` (D3's `f`), `high/low/≳τ`, `∧∨¬`, `Δf`, `violated_expectation`, timbre-relative baseline (C3/D5) | **OPEN frontier** | build-from-owned (automatic synth programming; Strasheela for the constraint form) |
| **L2 names — labels + governance gate** | recurring L2 expressions given a `name`, `examples`, `misuse`, `status`, `provenance`, admitted via contrastive review. **NOT a layer, NOT a first-class object** — saved expressions + review ceremony | **OPEN, governed by the gate** | build-from-owned (AudioCommons descriptor-binding; SKOS/von Bismarck for the contrast edge) |

**A-vs-B resolved:** the governing floor is **L1 features, not raw signal** — but only because **Lσ
bridges them.** A is right that signal is the lossless primitive (→ L0); B is right that features are
the artisan-thinkable *and* checkable band (→ L1); Popper showed the two do not connect for free on a
stochastic timbre, so **Lσ is mandatory, not optional**. [A; B; Popper; claim ≤ proof: every L1
estimator consumes `P`, and GENDYN (C2/D4) produces no `P` — emergent spectrum — so a `Signal→P` step
must exist and be seed-frozen or L1 is not reproducible.]
**Collapse-test (keystone, revised):** if `Spectralize` cannot be made reproducible-to-`(S,seed)`
(its window/hop/threshold leak into L1 values) then L1 is not a closed floor on stochastic timbres and
the model degrades to **A (signal-only)** for those voices. Freezing Lσ's parameters is exactly what
prevents that collapse.

### 2. Effects/sensations: primitive or composition? (the operator's direct question)

**Verdict: COMPOSITION (an objective over the closed floor), never a primitive — and the "named
vocabulary" is governance + labels, not a first-class object layer.**

- A+B win the first half: enumerating effects as primitives is the trap (unbounded, culturally
  relative, un-governable) [B]. An effect is an open expression whose every leaf is an L1
  `Feature.id`. Wittgenstein sharpens this: an "effect" **is** the tower's D3 Objective, restricted to
  L1 leaves — a renamed, domain-bounded objective, not a new kind of thing. We adopt that and **drop
  any claim that "effect" is novel.** [W; D3]
- C loses the second half decisively. The prior draft argued a named effect is "more than a re-skin"
  because it carries a contrastive/misuse boundary. **Wittgenstein refuted this on the model's own
  floor-clause:** since every leaf bottoms out in L1, the boundary "strangeness ≠ dissonant-tension"
  is *exactly the set-difference of the two bindings* — a region of L1-space, recoverable without the
  name. The name is a macro alias; provenance/status/review are version-control metadata hangable on
  any saved expression. **So a `SensationEntry` is not a first-class object over its binding.** [W;
  C's own 3rd self-objection; collapse-test below — *already decided against L2-lib as a layer*.]
- **What genuinely survives (kept, but renamed honestly):** (a) the **contrastive-review gate** —
  forcing a human to write the boundary at admission and merging synonyms — does real governance work
  *as a process applied to saved L2 expressions* [W concedes this]; (b) **labels** reduce cognitive
  load and survive hand-off (an ergonomic win, not a metaphysical one) [C]. Both are worth keeping;
  neither makes a layer. The owner of the surviving form is **AudioCommons** (named perceptual
  descriptors bound to acoustic features), not the *A Pattern Language* analogy [L].
**Collapse-test (keystone, now decided):** "exhibit one named effect whose misuse-boundary is *not*
the set-difference of its bindings." Wittgenstein showed `dissonant-tension` vs `strangeness` fails it
(the difference is fully carried by the inharmonicity + violated-expectation terms). **Default verdict:
re-skin.** O6 stays open only as a standing challenge — if no case is ever exhibited, delete the
"object" framing and keep labels + gate.

### 3. The admission rule (room without losing governance)

One rule, two tiers. Governance bites at the **floor-clause** (Tier 1.1) and the **contrastive gate**
(Tier 2.7).

**Tier 1 — admit an L2 effect-expression (cheap, author-time, no migration):**
1. **Closure (floor-clause):** every leaf is an L1 `Feature.id` — no free symbols; a new *feature*
   requires the heavy L1 migration (estimator add + Lσ compatibility + review). [B(1)]
2. **Computability ⇒ reproducible** (inherited from clause 1 + Lσ frozen). [B(2); Popper]
3. **Steerable target:** yields a search gradient over L0 params (D3's `f`). [B(3)]
4. **O1 honesty tag (mandatory):** labeled a **proxy** — surfaced "this hits the target you set; judge
   it", never "this IS strange"; routes the gap to evidence (#10 → listener study → re-weight `wᵢ`).
   [B; C9; O1; D3 anti-misuse]

**Tier 2 — give an expression a NAME + register it (governance ceremony, NOT a new object):** [C; W]
5. **Propose:** submit name + binding + examples + misuse; **a name with no binding is rejected on
   sight.**
6. **Prove binding & tag grounded/proxy** — this distinction is a **real joint** [W]: `grounded`
   (source-backed L1 target, e.g. `dissonant-tension` on `d(P,i)`, D5) can reach `status: admitted`;
   `proxy` (felt link unproven, O1) is capped at `seed|contested`, carries the O1 caveat permanently,
   and enters the evidence lane. It gates legal state-transitions + output framing, so it is not a
   mere confidence tag — **conditional on O5 being closed** (an owner must back "source-backed").
7. **Contrastive review (anti-drift gate):** check vs nearest neighbors; write the boundary into both
   `misuse` fields; **indistinguishable by binding ∧ felt-definition → merge, do not register.** This
   gate is the kept governance value (per §2).
8. **Status lifecycle** (`seed→admitted→contested→deprecated`) — every change a reviewable diff on the
   versioned vocabulary V (like a spec diff, D1).

**Where room-without-losing-governance is won:** room is continuous + combinatorial + open at L2;
governance is finite + closed at L0/Lσ/L1. An artisan writes `menace`/`shimmer`/`seasick` instantly at
Tier 1 (zero migration); the floor-clause guarantees measurability. The **only** heavy governed
migration is adding an L1 feature (which now also requires Lσ to produce its `P` input). [A; B; C]

### 4. The operator example, end-to-end (with Popper's repair)

> "create some dark violin stochastic synth, then use some dissonance scale to bring a strangeness to the listener."

| Phrase | Layer + mechanism | Source |
|---|---|---|
| **stochastic synth** | L0: instantiate `GendynWalk` voice (breakpoints + bounded amp/time walks, seed fixed); spectrum **emergent** | C2/D4; A |
| *(bridge)* | **Lσ: `Spectralize` extracts `P` from the realized signal with frozen window/hop/threshold** — without this step every feature below is undefined on this timbre (Popper) | **Popper repair** |
| **violin** | L1: `harmonicity_profile` match-distance to a violin partial template over `P` (named `violin-ness`, grounded) | B; AudioCommons (L) |
| **dark** | L1: `low(spectral_centroid)` over `P`; agent searches L0 walk-bounds/amplitudes (D3) (label `darkness`, grounded) | B; A |
| **dissonance scale** | L1 `roughness=d(P,interval)` against the **fixed dark-violin `P`**; agent picks `Scale` (L0) hitting target `d` — timbre-relative (label `dissonant-tension`, grounded) | C3/D5; A `tune(Pattern,Scale)` |
| **strangeness** | L2 effect = D3 objective `max w₁·rough + w₂·inharm + w₃·flux`; label `strangeness` at `status: seed/proxy`, O1 tag, contrast "*not* dissonant-tension"; agent searches L0 params; **#10 reports numbers + "judge it"** | B; C9; O1; C12; D3 (W: it is an Objective) |

Five spec edits over a closed L0+Lσ+L1 floor, one open L2, **zero generation in the sound path**
(C7/C8). **Honest status (Popper):** the example is **witnessed only with Lσ in the closed core**; as
originally drafted (no `Signal→P` step) it KILLs at the L0→L1 boundary. "Strangeness" is a proxy,
never asserted — that limitation is witnessed, not vacuous (Popper cleared step 4). The remaining
unverified link is strangeness↦felt = O1.

### 5. Minimal closed core vs open frontier

| | Content | Why |
|---|---|---|
| **Minimal closed core (freeze)** | L0 substrate + combinators · **Lσ `Spectralize` (frozen params)** · L1 feature set + estimators | The smallest thing that must be enumerated + frozen to make everything above measurable/reproducible/diffable. Lσ is non-negotiable for stochastic timbres. |
| **Open frontier (never freeze)** | L2 effect-expressions (Tier-1) · named/registered expressions (Tier-2 labels+gate) · per-piece `SensationComposition`s | Unbounded, cheap, artisan-owned; governed only by the floor-clause + contrastive gate. |

**Smallest loop that proves the thesis (build-first):** L0 = one GENDYN engine; **Lσ = one frozen
STFT+peak-pick**; L1 = `{spectral_centroid, d(P,i), harmonicity_profile}` (3 estimators the example
needs); L2 = the strangeness objective; two labels (`darkness` grounded, `strangeness` proxy) to
exercise the contrastive gate; #10 feedback meter. **First test to run:** does `Spectralize` give a
stable `P` (hence stable centroid/roughness) on GENDYN output across runs of `(S,seed)` — the O5/Popper
crux. [LEARNING-PACK build/block/defer]

---

## Open residue

| ID | Open question | Routes to |
|---|---|---|
| **O1** | Does a Sethares dissonance target predict perceived "strangeness"? Handled architecturally (proxy tag + #10 + re-weight), **not solved**. | listener study → `research-evidence-harness` |
| **O2** (stakes demoted) | Can NL adjectives compile via a governed vocabulary? We no longer claim names are primitives — O2 need only show *bindings compile*, not that names are a layer. | build the Tier-2 gate; measure binding-resolution success |
| **O5** (Lakatos: **mostly closed**) | Estimator ownership. **Resolved:** all L1 features are owned or folklore (MPEG-7/Peeters/Sethares/Zwicker/YIN; centroid/flux/density precedent-clean) — none novel. **Remaining:** pick + pin one specific estimator per feature and cite it. | precedent-clean; finalize citations |
| **O6** (Wittgenstein: **decided against the layer**) | Exhibit one named effect whose contrastive boundary is *not* the set-difference of its bindings. Default = re-skin → keep labels+gate, drop "object/layer" framing. Standing challenge only. | review/experiment if ever contested |
| **O7** | Do sessions spawn `seed` labels faster than contrastive review merges them (dialect fork)? Governance-leak risk concentrated in Tier-2. | observe admission-on-demand rate vs review throughput |
| **O8 (new, Popper)** | Is `Spectralize: Signal→P` actually reproducible-to-`(S,seed)` and stable on inharmonic/noisy GENDYN output? The whole closed floor rests on it. | spike: STFT/peak-pick stability test on GENDYN → `research-evidence-harness` |

---

## Closure note

**Verdict: GO with required repairs — build-from-owned throughout, no clean novelty.** The dispatch's
tension did its job: each skeptic moved the model.
- **Popper (non-vacuity):** localized KILL → forced **Lσ `Spectralize`** into the closed core; the
  operator's own GENDYN example does not close without it. O8 banked.
- **Wittgenstein (definitional):** **L2-lib named-effect collapses to a re-skin** — demoted from
  "first-class object/primitive layer" to "labels + contrastive-review gate over L2"; "effect"
  recognized as a renamed D3 Objective. L0/L1 (producer/observer) and grounded/proxy survive as real
  joints.
- **Lakatos (precedent):** no kills — **everything build-from-owned** (MPEG-7/Peeters/Sethares,
  Risset–Mathews→Horner→DDSP, AudioCommons, NIME Hunt/Wanderley). Corrected the draft's asymmetric
  honesty error (over-claimed L2 novelty, under-claimed L1 ownership). Only thin seam — the first-class
  contrastive edge — is itself collapsed by Wittgenstein (O6).

**One-line answer to the dispatch goal:** *Primitives = a small **closed** floor (signal substrate →
a frozen `Spectralize` → ~10 owned perceptual features); **effects/sensations are NOT primitives and
should not be enumerated as such** — they are open objectives composed over that floor, with named
"sensations" kept only as ergonomic labels + a governance gate, never minted as a layer. That is how
you get maximum authoring room (open L2) without losing governance (closed, owned, reproducible
floor) — provided `Spectralize` can be frozen on stochastic timbres (O8).*
