# WORK-PACK — studio-core (Invoke `plan` output)

Execution manifest mapped from [plan.md](./plan.md) tasks + [implementation-layering.md](./implementation-layering.md)
layer decisions. Output mode: **split** (per-layer parent tasks). Each SWU = one parent task with write
scope, acceptance evidence, and a verification command. Next owner: `task-session`.

Package root: `research/agentic-music-studio/build/studio_core/`. Tests: `…/tests/`. Experiments: `…/experiments/`.

## Shared SWU manifest

| SWU | Parent task | Layer | Retires | Depends on |
|---|---|---|---|---|
| SWU-0 | Package scaffold + deps + pytest | — | — | — |
| SWU-1 | GENDYN render (deterministic) | L0 | (floor) | SWU-0 |
| SWU-2 | Spectralize → PartialSet | L0 | — | SWU-1 |
| SWU-3 | centroid + dissonance + match | L0/L1 | — | SWU-2 |
| SWU-4 | **O8 stability experiment** | L0 | **O8** | SWU-3 |
| SWU-5 | Objective combinators + search | L1/L2 | — | SWU-3 |
| SWU-6 | Operator-example witness | L1 | (Popper witness) | SWU-5 |
| SWU-7 | SensationLabel + contrastive gate | L2 | — | SWU-5 |
| SWU-8 | **O6 re-skin adjudication** | L2 | **O6** | SWU-7 |
| SWU-9 | meter (#10) + listener harness | L3 | — | SWU-6 |
| SWU-10 | **O1 pre-registration + dry-run** | L3 | **O1** (frozen) | SWU-9 |

**Gate order (hard):** SWU-4 (O8) must PASS before SWU-5+ carry weight — a failed floor invalidates the
witness and effects. If SWU-4 fails, STOP and bank the finding (per implementation-layering).

---

## SWU details

### SWU-0 — scaffold
- **Write scope:** `studio_core/__init__.py`, `pyproject.toml`/`requirements.txt` (numpy, scipy, librosa, soundfile, sounddevice, pytest), `tests/`.
- **Acceptance:** `pytest` runs (0 tests ok); imports resolve.
- **Verify:** `cd …/build && python -m pytest -q`

### SWU-1 — GENDYN render — *plan L0.1*
- **Write scope:** `l0_signal/gendyn.py`, `l0_signal/engine.py` (EngineSpec protocol), `tests/test_l0_determinism.py`.
- **Acceptance:** `render(walk,dur,sr)` twice → `np.array_equal`; golden-hash stable; range ≤1.0; N<2 raises.
- **Verify:** `python -m pytest tests/test_l0_determinism.py -q`

### SWU-2 — Spectralize — *plan L0.2*
- **Write scope:** `lsigma/spectralize.py` (frozen `SpectralizeParams`), `l1_features/partials.py`, `tests/test_lsigma.py`.
- **Acceptance:** pure-function (same inputs→same P); on a synthetic additive tone P recovers known partials within tol; silent→empty.
- **Verify:** `python -m pytest tests/test_lsigma.py -q`

### SWU-3 — features — *plan L0.3/L1.1–1.3*
- **Write scope:** `l1_features/features.py`, `tests/test_l1_features.py`.
- **Acceptance:** each feature pure + reproducible; dissonance curve matches a Sethares harmonic-template anchor in shape; centroid units correct.
- **Verify:** `python -m pytest tests/test_l1_features.py -q`

### SWU-4 — O8 stability experiment — *plan L0.4* — **retires O8**
- **Write scope:** `experiments/o8_spectralize_stability.py`, `experiments/o8_report.md`.
- **Acceptance:** re-render identity exact; param-perturbation `|Δfeature|/feature < ε` (ε recorded); report states PASS or the honest FAIL ("floor → signal-only").
- **Verify:** `python experiments/o8_spectralize_stability.py` → writes `o8_report.md` with verdict.

### SWU-5 — objective + search — *plan L2.1*
- **Write scope:** `l2_effects/objective.py`, `tests/test_l2_objective.py`.
- **Acceptance:** `search` lowers centroid vs random init on `dark`; differential_evolution seeded → reproducible; random-search baseline present.
- **Verify:** `python -m pytest tests/test_l2_objective.py -q`

### SWU-6 — operator-example witness — *plan L1.5*
- **Write scope:** `experiments/witness_operator_example.py`, `spec.py`.
- **Acceptance:** builds the Spec; `realize(spec)` bit-identical on replay; `low(centroid)`+`match` within tol; dissonance-selected Scale recorded. **This is the Popper witness reproducing.**
- **Verify:** `python experiments/witness_operator_example.py` → replay-identical log.

### SWU-7 — SensationLabel + gate — *plan L2.2*
- **Write scope:** `l2_effects/gate.py`, `tests/test_l2_gate.py`.
- **Acceptance:** reject-no-binding; merge-synonym; admit-distinct; grounded/proxy tagging; set-difference boundary computed.
- **Verify:** `python -m pytest tests/test_l2_gate.py -q`

### SWU-8 — O6 adjudication — *plan L2.3* — **retires O6**
- **Write scope:** `experiments/o6_reskin_adjudication.py`, `experiments/o6_verdict.md`.
- **Acceptance:** runs the `dissonant-tension` vs `strangeness` challenge; verdict KEEP-object (with the non-reducible case named) or RE-SKIN (keep labels+gate). Either retires O6.
- **Verify:** `python experiments/o6_reskin_adjudication.py` → writes `o6_verdict.md`.

### SWU-9 — meter + harness — *plan L3.1/L3.2*
- **Write scope:** `l3_evidence/meter.py`, `l3_evidence/listener_harness.py`, `tests/test_l3.py`.
- **Acceptance:** meter snapshot test; harness builds a blinded battery; `score_correlation` validated on synthetic ratings (no real claim).
- **Verify:** `python -m pytest tests/test_l3.py -q`

### SWU-10 — O1 pre-registration + dry-run — *plan L3.3* — **freezes O1**
- **Write scope:** `experiments/o1_strangeness_study/criterion.md`, `experiments/o1_strangeness_study/dryrun_report.md`.
- **Acceptance:** criterion frozen (ρ threshold, n, blinding) BEFORE any live run; dry-run on synthetic ratings exercises the pipeline. **Live run handed to `research-evidence-harness`/`experiment`.**
- **Verify:** review `criterion.md` frozen + `python experiments/o1_strangeness_study/dryrun.py`.

---

## Validation rollup
- **O8** ← SWU-4 (PASS/FAIL banked). **O6** ← SWU-8 (verdict). **O1** ← SWU-10 (criterion frozen) → external run.
- Witness ← SWU-6 (model's central claim reproduces). All sound-path code deterministic, no model (C7/C8).

## Next route
`task-session` → execute SWUs in gate order (SWU-0→4 first; **stop-gate at SWU-4/O8**; then 5→8; then 9→10).
O1 live study → `experiment` + `research-evidence-harness`.
