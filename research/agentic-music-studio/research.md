# Research — working synthesis trail

This is the reasoning trail. Adjudicated claims live in `claim-ledger.md`; this file shows how the
pieces were connected.

## 1. Decoding the operator's example against real research

The operator's worked example is not vague — each phrase lands on a concrete, source-backed domain:

| Operator phrase | Real domain it names | Source |
|---|---|---|
| "dark … synth" | timbre as **spectral feature** ("dark" ≈ low spectral centroid, more low-partial energy) | S3 (timbre↔spectrum) |
| "violin … synth" | timbre **target** — match a known instrument's spectrum | S3, S4 |
| "stochastic synth" | **dynamic stochastic synthesis** (Xenakis/GENDYN): waveform deformed by random walks; spectrum emergent | S2 |
| "dissonance scale" | **sensory dissonance** is computable from the timbre; pick a scale whose intervals hit target dissonance | S3 |
| "bring a strangeness to the listener" | a **perceptual objective** — name the target effect, optimize toward it | S3 (+ inference) |

This matters: the operator is already describing **objective-driven engineering**, not generation.
"Bring strangeness" is a *goal*; "use some dissonance scale" is a *deterministic means* (compute a
dissonance curve, choose intervals). The agent's job is to *engineer toward the named perceptual
target*, not to invent audio.

## 2. The load-bearing design move: intent → spec → deterministic realization + search

Reframing the example as a pipeline:

```
"dark violin stochastic synth"        "use a dissonance scale to bring strangeness"
        │                                          │
   parse intent into a SPEC                   name a perceptual OBJECTIVE
   (timbre target: violin-like,              (target: high listener "strangeness")
    dark; engine: GENDYN-class)                       │
        │                                    agent computes dissonance curve (Sethares)
   agent constructs/searches a                for THIS timbre, searches scales/tunings
   stochastic synth whose spectrum            whose intervals land on target dissonance
   matches the target (deterministic)                 │
        └──────────────► both edit ONE reproducible spec ◄──────────────┘
```

No generative model produces the sound. If a model appears at all, it sits only as a **front-end
parser** turning "dark violin stochastic" into spec fields drawn from a *governed, artisan-editable
vocabulary* — a compiler front-end, not a composer. This is the line that keeps craft and
reproducibility (claim C7, C8).

## 3. Strasheela and TidalCycles bracket the two proven surfaces

- **Strasheela (S5)** proves the *declarative* end: a human declares a music theory as constraints;
  the computer deterministically produces compliant music. That is "specs" made literal — and it
  predates the current model wave by ~20 years, so it is evidence the spec-first path is real, not
  speculative.
- **TidalCycles (S1)** proves the *live, performative* end: terse pattern code, evaluated live, the
  human steering the *statistics* of rhythm/sound rather than each note. Craft lives in writing and
  mutating patterns. Algorave shows it is expressive enough for real audiences.

Between them sits the whole interface design space the operator is asking about.

## 4. NIME gives the vocabulary for "interface as communication process"

NIME's DMI triad — **controller → mapping → sound engine** (S4) — separates *the surface the human
touches* from *the rule connecting it to sound* from *the thing that makes sound*. The operator's
question ("what interfaces, as communication processes?") is really: **what controllers and what
mappings**, given that the sound engine is a deterministic, spec-driven, objective-searchable core.
"Communication process" = the *kind of message* (command / declaration / goal / example / critique …)
and *who leads when* — a layer above modality. The taxonomy in `findings.md` is built on that
distinction.

## 5. Ergonomics-first lens (operator's stated first principle)

Per the operator's standing principle, every process is rated on **who-leads-when**, **cognitive
load**, and **friction reduction** — not just "is it possible." The reverse channel (agent → human
perceptual feedback, process #10) is the ergonomic keystone: symbiosis needs a *shared model of the
listener*, so the agent must show what it perceives ("this will read as dissonant/strange"), not
just accept commands. Without that channel the human is flying blind and the studio collapses back
into trial-and-error.

## 6. Why the "no models" stance is coherent (not nostalgia)

The contrast case (S6) is prompt→model→finished-audio. The operator rejects it for two reasons that
hold up: (a) **craft** — a model output is not an authored, reproducible artifact you can diff,
fork, and defend; (b) **control** — you cannot steer a black box toward a precise perceptual
objective the way you can search a parametric engine against a computable metric. Agentic
engineering keeps the artifact authored and the search auditable. The cost is that the studio must
*build* the deterministic engines and objective functions instead of renting a model — that cost is
the project.
