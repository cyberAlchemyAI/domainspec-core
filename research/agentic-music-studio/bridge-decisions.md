# Bridge Decisions

NON-SOURCE layer. What the real build should do with each idea. Statuses: `borrow-carefully`,
`analogy-only`, `block`, `promotion-candidate`, `future-work`.

| # | Idea | Status | Decision & guardrail |
|---|---|---|---|
| B1 | Spec as the single shared lingua franca every interface edits (D1, C10) | **borrow-carefully** | Adopt as the architectural backbone. Guardrail: it must be deterministic — `realize(spec, seed)` reproducible — or it is not a spec. Validate with a tiny round-trip before scaling. |
| B2 | Objective-function steering with psychoacoustic metrics (D3, C9) | **borrow-carefully** | Adopt for "name the effect, search the parameters." Guardrail: always show *which* objective is optimized; treat the metric as a proxy, never assert it equals the felt effect (O1). |
| B3 | Stochastic synthesis (GENDYN-class) as a core engine (C2) | **borrow-carefully** | Strong fit for "stochastic synth" + reproducibility (seeded walks). Guardrail: exact algorithm params unverified here — read S2 sources in full before implementing. |
| B4 | Live-coding surface (TidalCycles-style) as process #8 (C1) | **borrow-carefully** | Adopt as the high-craft authoring surface. Guardrail: keep it an *editor of the spec*, not a parallel source of truth. |
| B5 | NIME controller→mapping→engine + "ergonomics lives in the mapping" (C4) | **borrow-carefully** | Adopt as the gestural-process (#9) design discipline. |
| B6 | Generative model produces audio (S6 pattern) | **block** | Violates the no-models principle, reproducibility, and craft. Not in the sound path. |
| B7 | A model parses intent → governed spec vocabulary (C8, "compiler front-end") | **analogy-only** | Keep as a *frame* for where a model may sit (#3). Do not commit to a learned parser until O2 is tested — a governed, artisan-editable vocabulary may suffice without a model. |
| B8 | The ten-process taxonomy + who-leads-when matrix (`findings.md`) | **promotion-candidate** | Reusable as an interface-design ontology / checklist for the studio (and arguably for other human-agent symbiosis tools). Promote only via a separate governed decision. |
| B9 | Reverse channel: agent→human perceptual feedback as the ergonomic keystone (C12) | **promotion-candidate** | Strong candidate for a first-class design principle (shared model of the listener). Promote via governed decision. |
| B10 | "Strangeness" and other perceptual targets as measurable objectives | **future-work** | Needs listener evidence that the metric predicts the effect → evidence handoff below (O1). |
| B11 | Adjacent systems (Sonic Pi, ChucK, Max/MSP, FoxDot, Overtone) | **future-work** | Pull into the corpus to widen/validate the surface taxonomy (O4). |

## Evidence-execution handoff

Two questions are **empirical, not source-reading** — route to `research-evidence-harness`:

- **O1** — Does a Sethares/Plomp–Levelt dissonance (or roughness/tension) target predict perceived
  *"strangeness"*? Needs: listener-rating fixtures, an objective-vector (computed dissonance per
  candidate), a scoring rubric, dry-run then live-run summaries. Blocks claim C9 from strengthening
  beyond `local-inference`.
- **O2** — Can natural-language timbre adjectives compile to spectral-feature specs via a *governed*
  (non-model) vocabulary at acceptable reliability? Needs: a fixture set of adjective→spectrum
  mappings and an agreement metric.

Tower/source artifacts supporting these experiments: `levels/L0-corpus.md` (S2, S3), `definitions.md`
(D3, D5), `findings.md` (#4). The evidence mechanics (run schemas, scoring) are out of this tower's
scope.

## Promotion boundary

All of the above is **local-only**. B8 and B9 are the named promotion candidates; nothing here
enters Inventory / Ontology / sigils / runtime contracts without a separate governed promotion
decision.
