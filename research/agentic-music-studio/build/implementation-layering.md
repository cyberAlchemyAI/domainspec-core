# Implementation Layering — studio-core (Invoke companion, required for `plan`)

Transmutation: `implementation-layering`. Bounds the plan by explicit layer decisions + promotion
evidence. Companion to [design.md](./design.md) and [plan.md](./plan.md).

**Layer principle here:** layers are ordered by *value/cost* AND each layer's promotion gate is the
**retirement of one open residue** — so progress is measured in resolved questions, not lines of code.
Build stops (honestly) at any layer whose gate fails, because a failed floor invalidates everything
above it.

---

## Layer decision snapshot

| Layer | Minimum working unit | Value | Cost | Promotion gate (evidence to advance) | Residue retired |
|---|---|---|---|---|---|
| **L0** | A GENDYN voice renders deterministically **and** `Spectralize` yields a stable `P`; 3 L1 features compute on it | **Highest** — the floor everything rests on; building it is the only way to test the gating risk | Low–med (hand-written DSP, no UI) | **O8 stability test passes**: P identical across re-renders; \|Δcentroid\|,\|Δdissonance\| < ε under the param-perturbation grid. *Fail ⇒ STOP*: floor degrades to signal-only, reconsider the model | **O8** |
| **L1** | Objective search realizes the operator example end-to-end and reproduces from `(Spec, seed)` | High — proves the model's central claim (intent→spec→deterministic realize + search) | Med (optimizer + dissonance-driven scale select) | **Witness reproduces**: "dark violin stochastic synth → dissonance scale" yields a `Spec` whose `realize` is bit-identical on replay; targets hit within tol | — (the Popper witness) |
| **L2** | Strangeness objective authored; contrastive gate admits/merges labels; O6 adjudication run | Med — answers the "do we enumerate effects" question empirically | Low–med (logic over L1, little new DSP) | **O6 verdict produced**: either a witnessed non-reducible label (KEEP object framing) or a documented re-skin (keep labels+gate, drop layer claim) | **O6** |
| **L3** | Feature meter (#10) + listener-study harness + pre-registered O1 criterion | Med — closes the felt-match loop, but the *answer* needs humans | **High** (needs participants; partly handed off) | **O1 criterion frozen + harness validated on a dry-run**; live run handed to `research-evidence-harness`/`experiment` | **O1** (frozen here; rendered there) |

---

## Boundary rationale (why these cuts)

- **L0 first, not the engine-by-itself.** The tempting cut is "L0 = synth, separate task = analysis."
  Rejected: the synth alone retires nothing and Popper showed the synth is exactly where the floor is
  at risk. The MWU is *synth + Spectralize + features together*, because only the composite can answer
  O8 — the gating residue. Highest value, build first.
- **L1 is the witness, not "more features."** We add only the 3 estimators the operator example needs
  (centroid, dissonance, harmonicity-match). Adding the full ~10-feature set is deferred — it is cost
  without new evidence until the witness reproduces.
- **L2 is logic, not DSP.** Effects are objectives over L1 (already built); the gate is bookkeeping +
  a set-difference check. Cheap, and it retires O6. Comes before L3 because it needs no humans.
- **L3 last and partly external.** The listener study is the highest-cost, lowest-controllable layer
  (human participants, blinding). We build the harness and *freeze* the O1 criterion, but the live run
  is owned by `research-evidence-harness` — promotion here means "evidence machinery ready", not
  "O1 answered". This honors the tower's evidence-execution handoff.

## Promotion discipline

- No layer advances on preference — each gate is an artifact (a passing test, a reproduced witness, a
  written verdict, a frozen criterion). Evidence from the previous layer, not optimism (Invoke global gate).
- **L0 is a hard gate.** If O8 fails, the build does not "route around" it — it stops and the finding
  (floor degrades to signal-only for stochastic timbres) is itself a banked result. This is the single
  most important honesty rule of the plan.
- Each layer keeps the closed core closed: adding an L1 feature (and its Lσ compatibility) is the only
  event that touches the frozen substrate; everything else is open-frontier work.

## Per-layer planning slices → see [plan.md](./plan.md)

L0/L1/L2/L3 each get a planning slice with implementation-detail specs for the algorithmic tasks
(GENDYN render, Spectralize, dissonance, objective search, O8 stability test, O6 gate, O1 harness) and
SWUs in [WORK-PACK.md](./WORK-PACK.md).
