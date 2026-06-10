# Stage 03 — Interrogation (refine-review)
Capability: `interrogation` · Mode: `refine-review` · Overlay: `dialectic_for_tension` · Status: **pass**
Roles: proposer, critic, synthesizer · Inputs: Define (s02), subagent receipts

## Proposer
Define's MVP scope (operational-contract spine, candidate-only) is well-formed and matches the research brief's winning reading.

## Critic
1. **Is "spine first" right vs evidence-first?** The mvp-shape-tournament-reviewer scored A>B>C: B inverts the dependency DAG and risks runtime-evidence self-promotion before a gate exists. Holds.
2. **Could this drift into building the package?** Risk. Hard constraint reaffirmed: candidate-only, artifacts live in the run folder, no `formulae/infra-spec`, no pipeline wiring.
3. **Is reuse of dispatch `$defs` real or cosmetic?** The schema-discipline reviewer mapped each `$def` (reuse-as-is / with-changes / n/a) with the boundary.kind redefinition justified. Real.
4. **Falsifiability now vs later?** Shape layer is falsifiable immediately (jsonschema); governance layer needs a script. Define must not claim governance falsification it can't run yet → split into shape (now) + governance (deferred). Accepted.

## Synthesizer (residue)
- Supported: spine-first, candidate-only, dispatch-`$def` reuse, shape-layer fixtures now.
- Demoted/clarified: governance-layer falsification is specified-but-deferred (needs `validate-infra-spec.py`); do not claim it as run.
- Carried: 7-stage ladder transition semantics + boundary.kind enum remain candidate (need governance fixtures).

## Verdict
`pass` — scope locked; shape-vs-governance falsification split is the key clarification.
