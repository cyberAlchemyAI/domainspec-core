# Refine Result — intent-engine plan validation

**Verdict: the plan needs MORE DEPTH (yes-substantial) before execution.** The *thesis* is sound and the
*direction* is right — but the work-pack mislabels three net-new sub-projects as "thin reuse," bills a
trivial template as the thesis-proving headline, and lets the flagship demo run on the one timbre the
floor can't measure. Three independent critics (execution-readiness, thesis-integrity, dependency-risk)
converged on the same core. Below: what's solid, the depth-gaps ranked, and the recommended revision.

## What's solid (keep)
- **Thesis is structurally honored** (thesis critic): no model in the sound path; findings.md conclusions
  preserved (effects = objectives not a layer; named effects = labels+gate, O6); the real intelligence
  genuinely lives in the deterministic L1 search — it is "agentic engineering," not "a DSL + an LLM prompt."
- The L0→L3 *spine* (language → engineer targets → author from intent → steer) is the right shape.

## Depth-gaps, ranked (the plan's own three critics, deduped)

### CRITICAL
- **G1 — `pattern` and `scale` are net-new sub-engines, not reuse.** studio-core has **no pitch/scale/note
  concept and no sequencer/event/pattern**; `spec.realize` renders ONE mono voice. The DSL's `pattern "x ~
  x x"` and `scale strange from dissonance(high)` have nothing to compile to. The layering bills L0 as
  "thin DSL over studio-core, cost Low" — false. *(execution critic C1)*
- **G2 — the flagship demo runs on the one timbre the floor can't measure.** The worked example is a
  *stochastic* violin; O8 says features drift 8.8% there. "Demo on additive voices + treat stochastic as
  proxy" relabels the failure: on additive voices the engine works but doesn't need an intent-engine; on
  the stochastic voice the steering readout is ±9% noise. The "proxy" tag silently turns the flagship
  claim into "move a number we admit we can't measure." This is the **single riskiest assumption** — it
  degrades *dishonestly* (green tests, thesis-empty demo). *(dependency critic C1)*
- **G3 — `search` can't tune what the plan assumes.** studio-core `search` optimizes a fixed 3-D GENDYN
  theta only — it can't tune additive params or non-existent "scale params," and there is no `dark` or
  `strangeness` objective (only `low/high/weighted` over the three real feature keys `spectral_centroid` /
  `harmonicity_match` / `dissonance_minor2`; "strangeness" is a value-reducer in the listener harness, not
  a cost). The L1 demo as written cannot call `search`. *(execution critic C2/C3)*

### MAJOR
- **G4 — billing inversion (thesis honesty).** The task branded the thesis headline ("the agent writes the
  code", L2.3/SWU-5) is, in v1, a deterministic template with **zero intelligence**; the task that earns
  the thesis (L1 search) is undersold as plumbing. Rename, or scope a real "agent makes authoring choices"
  task. *(thesis critic C1)*
- **G5 — the author seam is where an LLM silently re-enters.** `author.py` must invent `pattern`+`seed`
  (not in the Spec); "deterministic given spec" is unpinned. Pin every Program field the Spec doesn't carry,
  with a test. *(thesis M1)*
- **G6 — sequencing coupling.** L1/L2.1/L3.2 are coupled to feature *semantics*, not just accuracy;
  Spectralize-v2 *re-anchors* the dissonance/roughness meaning. Building them first risks reworking all
  three modules. Freeze stochastic objective/vocabulary values until v2; make `fit.py` a thin adapter over
  studio-core features. *(dependency M2)*
- **G7 — "human directs" is steering-on-rails.** No SWU lets the human hand-edit the shown DSL and
  re-render — directing is read-mostly + pick-from-lexicon. Add a first-class "human edits code → re-render"
  SWU. *(thesis M2)*
- **G8 — rule-based parser re-raises O2 and is a menu, not a parser.** Off-vocabulary intent ("like rain on
  a tin roof") falls to "no recognized intent." Demote to "governed vocabulary resolver", v1 explicitly
  closed-vocabulary; open intent is the deferred LLM front-end's job, not a v1 gap. Same hardness on the
  output side (G-critique lexicon: magnitude + context + multi-target coupling). *(execution M2, dependency M3/M4)*

### MINOR
- **G9** — vocabulary entries carry directions but not target *values*; the real `FeatureTarget` requires a
  `value`. Add concrete values (or a baseline-relative rule). *(execution M2)*
- **G10** — "reproducible" everywhere = Reading-A (seed-determinism) only; add one Reading-B
  (analyzer-independence on the additive control) so green ≠ false confidence. *(dependency M6)*
- **G11** — the F3-vs-F4 "is a fixed perceptual model model-free?" gate leaks into the engine's "no model"
  prose; resolve it before committing the claim. *(dependency M5)*
- **G12** — paths/import mechanism, determinism scoped to render-not-search (DE isn't bit-identical across
  BLAS), "eyeball" acceptance unautomatable. *(execution m1-m3, M3)*

## Recommended revision (the depth to add)

**Re-scope v1 to a single-voice timbre engine on GENDYN — and say so honestly.**
1. **Cut `pattern` + `scale` from v1** (defer to a named, separately-costed "sequencer + scale module"
   sub-project). v1 DSL = `voice <engine> <effect>*` + `seed` + `targets`. Resolves G1, G3-partly, G5.
2. **Make GENDYN the demo voice** (it's what `search` tunes AND the flagship timbre), and **sequence the
   cheap F3 moment-centroid (from the Spectralize refine) BEFORE L1** so "darkness" aims honestly on the
   stochastic voice. Resolves G2 for centroid; roughness stays an honest proxy with a stated v1 limit.
3. **Rename L2:** "intent → transliterated code (closed vocabulary); the engineering is the L1 search."
   Add a real "human edits the code → re-render" SWU. Resolves G4, G7, G8.
4. **Freeze stochastic objective/vocabulary/lexicon values until Spectralize-v2; `fit.py` = thin adapter.**
   Resolves G6.
5. **Concrete fills:** target values (G9), the strangeness cost form `high(weighted([(1,high("dissonance_minor2")),(0.5,high("harmonicity_match"))]))`, a tiny closed critique table, a Reading-B test (G10), import via PYTHONPATH/editable install, determinism scoped to render (G12).
6. **Resolve G11** (F3 vs F4) as a one-line owner decision before the "no model" prose ships.

**Net:** the plan is the right idea, mis-scoped. After this revision it is a tight, honest, execution-ready
v1 that demonstrates the thesis (agent-engineered timbre from intent, on the flagship GENDYN voice, human
steers + can hand-edit the code) without over-claiming pattern/scale or hiding the floor caveat.

## Next route
Apply the revision (parent edits the four plan artifacts) → then `task-session` on the re-scoped work-pack.
The Spectralize-v2 F3-centroid task should be pulled earlier and sequenced before intent-engine L1.
