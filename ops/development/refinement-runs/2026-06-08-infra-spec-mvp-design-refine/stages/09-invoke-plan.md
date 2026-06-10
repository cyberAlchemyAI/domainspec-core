# Stage 09 — Invoke Plan (non-executed)
Capability: `invoke` · Mode: `plan` · Status: **pass**

## Non-executed build sequence (candidate → package), each gated by owner review
1. **Promote the candidate schema to a package** ONLY after owner review: move `candidate/infra-spec.schema.json` → `formulae/infra-spec/infra-spec.schema.yml` (+ `.json`), switching inlined `gate_action` to a `$ref` against dispatch-spec `$defs`.
2. **Build `validate-infra-spec.py`** implementing the 6 governance rules (fail-closed gate, status-floor, reversal obligation, unowned-state, analogy-labeling, blocker≠failure), mirroring `validate-dispatch.py` exit-code matrix (block→1, pass/flag→0).
3. **Wire the full fixture set** so every `v-*.json` exits 1 and `spine-pass` exits 0 (the falsification proof) — including the 3 governance fixtures that currently only pass shape.
4. **Pilot on one real project** (e.g. body-war or the now-available `validation/poker-team`) — author one real `infra-spec` instance, observe what the contract misses (feeds residue).
5. **Add the evidence layer additively** (receipts/drift/signals) once real instances exist — per the recomposition proof.

## Owner-review gate (hard)
No package creation, no pipeline wiring, no promotion to canonical until: schema validated, governance fixtures pass, and an owner approves. Runtime evidence never self-promotes.

## Owner boundary
All current writes in `ops/development/refinement-runs/.../` (parent-owned). Submodule contents not modified.

## Verdict
`pass` — non-executed plan with explicit gates; nothing promoted.
