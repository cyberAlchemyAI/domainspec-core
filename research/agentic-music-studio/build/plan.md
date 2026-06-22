# Implementation Plan — studio-core (Invoke `plan`)

Complexity: **medium–high** → per-layer L0–L3 slices + implementation-detail specs for algorithmic
tasks (below). Companions: [design.md](./design.md), [implementation-layering.md](./implementation-layering.md),
work-pack: [WORK-PACK.md](./WORK-PACK.md). Substrate: Python (DD1).

Repo target: `research/agentic-music-studio/build/studio_core/` (package) + `experiments/` + `tests/`.
Tooling: numpy, scipy, librosa (analysis convenience), sounddevice/soundfile (audio I/O), pytest.

---

## Validation strategy (per delivery slice)

| Slice | Validation surface | Evidence artifact |
|---|---|---|
| L0 | pytest determinism + the O8 stability experiment | `tests/test_l0_determinism.py`, `experiments/o8_…` report |
| L1 | pytest feature reproducibility + the operator-example witness reproduces | `tests/test_l1_features.py`, witness replay log |
| L2 | pytest gate logic + the O6 adjudication run | `tests/test_l2_gate.py`, `experiments/o6_…` verdict |
| L3 | harness dry-run produces a scored (synthetic) correlation; criterion frozen | `experiments/o1_…/criterion.md`, dry-run report |

---

## L0 slice — substrate + Spectralize (retires O8)

### Task L0.1 — `gendyn.render` (ALGORITHMIC — implementation-detail spec)
- **Inputs:** `walk: GendynWalk(breakpoints N, amp_walk, time_walk, seed)`, `dur_s`, `sr`.
- **Output:** `np.ndarray` float32 length `round(dur_s*sr)`, range [-1,1].
- **Ordered rules (dynamic stochastic synthesis, C2/D4):**
  1. `rng = np.random.default_rng(walk.seed)`.
  2. Init `N` breakpoints: amplitudes `a_i ∈ [amp_walk.lo,hi]`, time-intervals `t_i ∈ [time_walk.lo,hi]`.
  3. Per output cycle, advance each breakpoint by a seeded random step (`step_dist`, scaled by
     `step_scale`); **reflect** at bounds if `mirror` (mirror = fold back inside [lo,hi]).
  4. The N breakpoints define a polygon (amp vs cumulative time); linear-interpolate to sample grid.
  5. Concatenate cycles until `dur_s` filled; normalize peak to ≤ 1.0.
- **Edge cases:** N<2 → error; degenerate zero-width cycle (Σt_i≈0) → clamp min interval; clipping → pre-normalize.
- **Failure modes:** non-reproducible if any nondeterministic call (forbid `np.random.*` global; only the rng);
  NaN from cauchy steps → clip step magnitude.
- **Validation evidence:** `render` twice → `np.array_equal`; golden-hash test for a fixed `(walk,dur,sr)`.

### Task L0.2 — `spectralize` (ALGORITHMIC — implementation-detail spec) — the O8 estimator
- **Inputs:** `signal`, `sr`, `p: SpectralizeParams(n_fft, hop, window, peak_threshold_db, max_partials)`.
- **Output:** `PartialSet(partials=[(freq_hz, amp)], f0=None)` — a representative spectrum of the voice.
- **Ordered rules:**
  1. STFT: `librosa.stft(signal, n_fft, hop, window)` → magnitude `M[freq,frame]`.
  2. Per frame: pick local maxima above `peak_threshold_db` (rel. to frame max); parabolic-interpolate
     peak bins for sub-bin freq/amp.
  3. Aggregate across frames to a stable representative set: keep peaks present in ≥ τ_frac of frames
     (stability filter), take the `max_partials` strongest, amplitude = median over present frames.
  4. Return sorted-by-freq `PartialSet`.
- **Edge cases:** silent signal → empty `PartialSet` (downstream features defined to return NaN→handled);
  fewer than `max_partials` peaks → return what exists; dense noisy spectrum (GENDYN!) → the ≥τ_frac
  stability filter is what prevents picking transient noise as partials.
- **Failure modes (THE O8 RISK):** window/hop/threshold leak into `P` → feature instability; mitigation =
  freeze `p` (version-pinned) and *measure* the leakage in O8.
- **Validation evidence:** pure-function test (same inputs→same P); on a synthetic additive tone, P recovers
  the known partials within tolerance (sanity anchor before trusting it on GENDYN).

### Task L0.3 — L1 features needed for O8 (centroid, dissonance) — see L1.1/L1.2 (built here for the test).

### Task L0.4 — O8 stability experiment (`experiments/o8_spectralize_stability.py`)
- **Inputs:** a fixed `GendynWalk` family, a perturbation grid over `p` (n_fft ±, hop ±, threshold ±).
- **Procedure:**
  1. **Re-render identity:** render same `(walk,seed)` twice → assert identical signal → identical P → identical features. (Must pass; it's the determinism floor.)
  2. **Seed sweep:** render K seeds; record distribution of centroid/dissonance — characterize spread (expected; GENDYN is stochastic by design).
  3. **Param-perturbation sensitivity:** hold `(walk,seed)` fixed, vary `p` over the grid; measure `|Δcentroid|`, `|Δdissonance|`. **This is O8.**
- **Pass criterion:** step-1 exact; step-3 `|Δfeature|/feature < ε` (ε default 0.05, a plan decision — tune on the additive sanity case first).
- **Outcome:** PASS → L0 promotes. FAIL → STOP, bank "floor degrades to signal-only on stochastic timbres" (the model's own collapse-test), reconsider Lσ design.

---

## L1 slice — feature floor + the witness

### Task L1.1 — `spectral_centroid(P)` — amplitude-weighted mean partial freq. Pure; range [0,sr/2]. Unit Hz.
### Task L1.2 — `dissonance(P, ratio)` + `dissonance_curve(P, ratios)` (ALGORITHMIC)
- **Inputs:** `PartialSet P`, interval ratio(s).
- **Output:** sensory dissonance scalar / curve (Plomp–Levelt/Sethares, C3/D5).
- **Ordered rules:** for each pair of partials `(f_i,a_i),(f_j,a_j)` at interval r (one set shifted by r),
  add Plomp–Levelt dissonance `d(f_i, f_j, a_i, a_j)` using the standard model constants; sum; normalize.
- **Edge cases:** empty/one-partial P → 0; overlapping partials → contributes max consonance.
- **Validation:** reproduce the canonical Sethares 2.3:1-style curve shape on a harmonic template (owned anchor).

### Task L1.3 — `harmonicity_match(P, violin_template)` — distance to a violin partial profile. Template source = a measured/synthetic violin spectrum (plan decision; cite source).
### Task L1.4 — objective search wiring (`search`) — see L2.1.
### Task L1.5 — operator-example witness (`experiments/witness_operator_example.py`)
- Build the `Spec` for "dark violin stochastic synth → dissonance scale": GENDYN voice; targets
  `low(centroid)`, `harmonicity_match≤τ`; pick `Scale` by `dissonance_curve` against the fixed P.
- **Validation:** `realize(spec)` bit-identical on replay; targets within tol → witness reproduces (L1 gate).

---

## L2 slice — effects = objectives + gate (retires O6)

### Task L2.1 — `Objective` combinators + `search` (ALGORITHMIC)
- **Inputs:** param space (bounds over GendynWalk fields + Scale degrees), an Objective (weighted sum of L1 features), constraints.
- **Output:** best `Params`.
- **Rules:** `scipy.optimize.differential_evolution(objective, bounds, seed=…)` (DD4); random-search baseline for comparison; termination on tol/budget.
- **Edge cases:** non-improving → return best-so-far + flag; constraint infeasible → report.
- **Failure modes:** optimizing a proxy (strangeness) — never assert felt result (O1 tag).
- **Validation:** on `dark` (low centroid) the search demonstrably lowers centroid vs random init.

### Task L2.2 — `SensationLabel` + `register` contrastive gate (ALGORITHMIC — the O6 mechanism)
- **Inputs:** a candidate `SensationLabel(name, expr, examples, misuse)`, the registry.
- **Output:** admit | merge | reject + status (grounded/proxy).
- **Rules:** reject if no binding; compute nearest neighbor by binding-overlap; **set-difference of bindings** = the operationalized contrastive boundary; require a felt-distinction note; tag grounded (source-backed L1) vs proxy (O1).
- **Validation:** unit tests for reject-no-binding, merge-synonym, admit-distinct.

### Task L2.3 — O6 adjudication (`experiments/o6_reskin_adjudication.py`)
- **Procedure:** attempt to construct a named effect whose contrastive boundary is NOT the set-difference of its bindings (the Wittgenstein challenge). Try the `dissonant-tension` vs `strangeness` candidate.
- **Outcome:** witnessed non-reducible case → KEEP "object" framing; else → documented re-skin → keep labels+gate, drop layer claim. **Either is a banked result that retires O6.**

---

## L3 slice — evidence channel (freezes O1)

### Task L3.1 — `meter.report_features` — the #10 reverse channel: given a spec/signal, print/plot centroid + dissonance hit ("judge it"), never the adjective. Validation: snapshot test.
### Task L3.2 — `listener_harness` (ALGORITHMIC scaffolding)
- **Inputs:** a strangeness-objective, a target grid; **Output:** a blinded stimulus battery + a scoring fn.
- **Rules:** render stimuli at varying objective targets; randomize order; collect per-stimulus rating; `score_correlation(objective_values, ratings)` → r + effect size.
- **Edge cases:** too-few raters → underpowered flag; objective saturates → cap grid.
- **Validation:** dry-run with *synthetic* ratings yields a sane correlation pipeline (no real claim).
### Task L3.3 — O1 pre-registration (`experiments/o1_strangeness_study/criterion.md`)
- Freeze the success/failure criterion BEFORE any listener run (e.g. "objective↔rating Spearman ρ ≥ 0.4, n≥20, pre-registered"). **Hand off the live run** to `research-evidence-harness` / `experiment` (DD6). This task produces the frozen criterion only.

---

## Handoffs (next owners)
- **Execution of this plan** → `task-session` per [WORK-PACK.md](./WORK-PACK.md) SWUs.
- **O1 live study** → `experiment` (pre-register) then `research-evidence-harness` (run schema, scoring, adjudication).
- **Production synthesis path** (SuperCollider behind `EngineSpec`) → future `invoke design` (out of scope).

## Unresolved gaps
- Invoke gaps: none blocking — plan is execution-ready at L0–L2; L3 live-run is intentionally external.
- Target-artifact gaps: ε threshold + perturbation grid (L0.4), violin template source (L1.3), O1 rater pool (L3.3 → handoff).
