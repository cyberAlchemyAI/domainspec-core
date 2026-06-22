# Design — studio-core evidence loop (Invoke `design`)

Target artifact: **studio-core** — the minimal, deterministic, model-free implementation of the
agentic-music-studio primitive/schema model, built so that constructing it answers open residues
**O8, O1, O6**. Owner/cycle: agentic-music-studio research → build.
Authoring capability: `invoke` (mode `design`). Substrate decision: **Python** (recorded below).

Upstream (the approved "define" baseline this design rests on):
- Model: [../schema-stress/findings.md](../schema-stress/findings.md) (L0 · Lσ · L1 · L2 stack)
- Definitions: [../definitions.md](../definitions.md) (D1–D7); Glossary: [../glossary.md](../glossary.md)
- Claims/residue: [../claim-ledger.md](../claim-ledger.md) and findings residue (O1, O5, O6, O8)

> **Scope (explicit).** This is NOT the full studio. It is the *smallest end-to-end loop* that (a)
> realizes "dark violin stochastic synth → dissonance scale → strangeness" deterministically with no
> generative model, and (b) emits the evidence to settle O8, O1, O6. The ten communication processes,
> voice, gesture, and the full effect library are out of scope here (future work).

---

## Recorded decisions

| # | Decision | Choice | Rationale | Alt (if revisited) |
|---|---|---|---|---|
| DD1 | Substrate | **Python** (numpy/scipy/librosa/sounddevice) | All three residues live in the DSP/analysis side (Spectralize stability, dissonance, objective search, listener study); one language, fastest path | SuperCollider+Python for the production-synthesis path later (the L0 engine is swappable behind its interface) |
| DD2 | Synthesis engine | hand-written GENDYN (dynamic stochastic synthesis) | C2/D4; it IS the operator's "stochastic synth", and the worst case for the floor (Popper) — building it is what tests O8 | additive/`PartialSet` voice as a control case (P authored directly, no Spectralize needed) |
| DD3 | `P` source | **`Spectralize: Signal→P` is mandatory in the closed core** | Popper's KILL: GENDYN has no partial set; every L1 feature needs one | none — without it the floor collapses to signal-only |
| DD4 | Optimizer | `scipy.optimize.differential_evolution` (+ random-search baseline) | GENDYN param space is bounded, stochastic, non-smooth → gradient-free global search fits | CMA-ES / interactive human-fitness (Dahlstedt) later |
| DD5 | Effect representation | effect = weighted Objective over L1 (D3); named effects = labels + contrastive gate | Wittgenstein: "effect" is a renamed Objective; names are governance, not a layer | — |
| DD6 | O1 study execution | harness authored here; **actual listener run handed off to `research-evidence-harness`** | felt-match needs human participants + a pre-registered criterion (route via `experiment`) | self-rating pilot only, clearly labelled non-evidential |

---

## Architecture — the four strata as Python modules

All sound-path code is deterministic and seedable. No model anywhere (C7/C8). Every module is a pure
function or a seeded generator; the contract is `same inputs (incl. seed) → bit-identical output`.

```
studio_core/
  l0_signal/
    gendyn.py        GendynWalk, RandomWalkBound, render()         # the substrate (DD2)
    engine.py        EngineSpec protocol (render(spec, dur, sr)->signal)  # swappable (DD1 alt)
  lsigma/
    spectralize.py   SpectralizeParams (FROZEN), spectralize()->PartialSet  # Popper bridge (DD3) — O8
  l1_features/
    partials.py      PartialSet {partials:[(f,a)], f0?}
    features.py      spectral_centroid, dissonance(P,ratio), dissonance_curve,
                     harmonicity_match(P,template)                  # the governing floor
  l2_effects/
    objective.py     Objective, low()/high()/band(), search()       # effect = objective (DD5)
    gate.py          SensationLabel, register() + contrastive check  # labels+gate — O6
  l3_evidence/
    meter.py         report_features(spec|signal) -> readout         # process #10 reverse channel
    listener_harness.py  build_battery(), score_correlation()        # O1 study scaffold (DD6)
  spec.py            Spec {l0, l1_targets, l2_effects, labels, seed}  # the one shared doc (D1)
  experiments/
    o8_spectralize_stability.py
    o6_reskin_adjudication.py
    o1_strangeness_study.py        # pre-registration + harness driver
```

### L0 — signal substrate (`l0_signal/`)

```python
@dataclass(frozen=True)
class RandomWalkBound:
    lo: float; hi: float; step_dist: str  # 'gauss'|'uniform'|'cauchy'
    step_scale: float; mirror: bool = True

@dataclass(frozen=True)
class GendynWalk:
    breakpoints: int; amp_walk: RandomWalkBound; time_walk: RandomWalkBound; seed: int

def render(walk: GendynWalk, dur_s: float, sr: int) -> np.ndarray: ...
```
- **Contract:** `render` is a pure function of `(walk, dur_s, sr)`; uses `np.random.default_rng(walk.seed)`;
  two calls return bit-identical arrays. Spectrum is *emergent* (C2/D4) — no frequency-domain design.
- `EngineSpec` protocol lets an additive/`PartialSet` voice or (later) SuperCollider stand in (DD1/DD2 alt).

### Lσ — Spectralize (`lsigma/`) — the O8 crux

```python
@dataclass(frozen=True)
class SpectralizeParams:   # version-pinned; changing it is an L1-migration event
    n_fft: int; hop: int; window: str; peak_threshold_db: float; max_partials: int

def spectralize(signal: np.ndarray, sr: int, p: SpectralizeParams) -> PartialSet: ...
```
- **Contract:** pure function of `(signal, sr, p)`. Composed with L0 determinism ⇒ `P` is a function of
  `(Spec, seed)` alone — this is exactly what closes Popper's L0→L1 gap (DD3).
- **The open question O8 is whether `P` is *stable*, not merely deterministic:** robust to small
  perturbations of `p` and reproducible across re-renders. The stability metric is defined in the O8
  experiment; if it fails, the model's own collapse-test fires (floor → signal-only).

### L1 — feature floor (`l1_features/`)

Each feature is a pure function over `PartialSet` (build-from-owned; Lakatos):
- `spectral_centroid(P) -> float` — amplitude-weighted mean partial frequency (MPEG-7 variant).
- `dissonance(P, interval_ratio) -> float` and `dissonance_curve(P, ratios) -> np.ndarray` —
  Plomp–Levelt/Sethares sensory dissonance over partial pairs (C3/D5; owned).
- `harmonicity_match(P, violin_template) -> float` — distance to a violin partial profile (AudioCommons-style).
- **Contract:** each carries a reproducibility self-test (`feature(P)` identical across runs) and a
  unit/range. A feature with no reproducible estimator is demoted to L2 or rejected (keystone collapse-test).

### L2 — effects = objectives + the gate (`l2_effects/`) — the O6 crux

```python
Objective = Callable[[Params], float]           # built from L1 features (this IS D3's f; DD5)
def low(feature, target, tol) -> Objective: ...
def high(feature) -> Objective: ...
def search(space, objective, constraints) -> Params   # differential_evolution (DD4)

@dataclass
class SensationLabel:
    name: str; expr: Objective; examples: list; misuse: str
    status: str   # 'grounded'|'proxy(O1)'|'seed'|'contested'; provenance: ...
def register(label, registry) -> Result   # enforces: binding present; contrastive distinctness
```
- An "effect" is a weighted objective over L1 (`Σ wᵢ·gᵢ(fᵢ)`). `register()` runs the **contrastive gate**:
  rejects a name with no binding; on admit, computes the set-difference of bindings vs nearest neighbor
  and demands a felt-distinction note; tags grounded vs proxy.
- **O6 is operationalized here:** the adjudication experiment tries to exhibit a named effect whose
  contrastive boundary is *not* recoverable as the set-difference of bindings. Default outcome:
  re-skin → keep labels + gate, drop "object/layer" framing.

### L3 — evidence channel (`l3_evidence/`) — the O1 crux

- `meter.report_features(spec|signal)` — the reverse channel (process #10, C12): prints/plots the L1
  numbers ("centroid = X Hz, dissonance hit = 0.71") — never the adjective.
- `listener_harness` — builds a blinded battery of stimuli at varying strangeness-objective targets and
  scores correlation between objective value and rated strangeness. **The actual run is handed off to
  `research-evidence-harness` with a pre-registered criterion** (DD6).

---

## The one shared Spec (`spec.py`, D1)

```python
@dataclass
class Spec:
    l0: dict          # engine specs per voice (GendynWalk, ...)
    l1_targets: list  # FeatureTarget(feature, op, value)
    l2_effects: list  # Objective exprs (+ optional label ref)
    labels: list      # SensationLabel refs invoked
    seed: int
```
Every interface edits this; `realize(spec) -> signal` is deterministic. Diffable, forkable, replayable.

---

## Evidence map — how building this answers the residues

| Residue | Retired at | Mechanism | Pass / outcome criterion |
|---|---|---|---|
| **O8** — is `Spectralize` reproducible/stable on stochastic timbres? | **L0+Lσ** (`experiments/o8_…`) | re-render identity + seed-sweep distribution + param-perturbation sensitivity of P→centroid/dissonance | identical across re-renders; |Δfeature| < ε under small `p` perturbation. Fail ⇒ floor degrades to signal-only (honest stop) |
| **O6** — named effect non-reducible to its bindings? | **L2** (`experiments/o6_…`) | attempt to construct a label whose contrastive boundary ≠ set-difference of bindings | a witnessed case (KEEP "object") OR a documented re-skin (keep labels+gate) — either is a real result |
| **O1** — does the dissonance objective predict felt strangeness? | **L3** (`experiments/o1_…` → harness) | blinded listener battery; correlation of objective value vs rated strangeness | **pre-registered criterion frozen here; run handed off** to `research-evidence-harness`/`experiment` |

Witness for the whole model (Popper's spec) runs end-to-end at L1→L2: `dark violin stochastic synth →
dissonance scale → strangeness`, reproducible from `(Spec, seed)`, zero generation.

---

## Glossary consistency

Reuses tower terms unchanged (D1 Spec, D3 objective-steering, D4 stochastic synthesis, D5 dissonance
curve, Lσ/Spectralize from findings). No new canonical terms coined; `SensationLabel` is the code name
for findings' "named effect = label + gate" (not a primitive). Promotion of any of these to canonical
status remains a separate governed decision (local-only boundary preserved).

## Open gaps carried into `plan`
- O8 stability metric thresholds (ε, perturbation grid) are a plan/implementation-detail decision.
- O1 needs human participants + an IRB-free informal-study protocol; only the harness is built here.
- Violin partial template source (measured vs synthetic) — a plan task with a cited source.
