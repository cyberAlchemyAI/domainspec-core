# Stage 02 — Invoke Define

Capability: `invoke` · Mode: `define` · Runtime: native · Status: **pass**
Inputs: `context-builder-frame`, `REFINE-SEED-PROPOSAL.md`

## Definition: the MVP design problem

Produce the **smallest YAML-first infra-spec record** that (a) is genuinely useful on its own, (b) recomposes into the full evidence substrate, and (c) can be cheaply falsified with fixtures — without authoring a package.

## Scope of the MVP (the operational-contract spine)

From the candidate DAG critical path, the MVP record carries:

- `runtime_profile` (N1): `dev | single-vps | split-vps | ha` — source-backed by `INFRA-SETUP.md`.
- `environments[]` (N1 detail): named envs with profile.
- `services[]` (N2): `id`, `owner`, `deployment_unit`, `dependencies[]`.
- `boundaries[]` (N3): `kind ∈ {network, secret, data, tenant}`, rule.
- `state_namespaces[]` (N4): `source | runtime | generated | local | private | evidence`.
- `gates[]` (N11): fail-closed promotion gates (ids reused from existing pipeline gates where possible).
- `status` (N5): `specified | implemented | deployed | observed | validated | reflected | promoted`.
- `residue[]` (N10): typed, owned.
- `reversal` (N12, **net-new**): rollback / migration / backup / retention obligations.
- Optional refs (not redefined): `observability_refs[]`, `receipt_refs[]` (point at existing signal/SLO/receipt schemas).

## What stays OUT of the MVP (defer → residue)

- event/queue/backpressure (no broker artifact exists).
- the full evidence layer (receipts/drift instances) — referenced, not required, until real instances exist.
- reflection-tower *object* and any categorical/physics analogy (label-only, never schema).

## Definition of success (testable)

- D1: a `infra-spec.schema.yml` candidate exists with the spine fields, each traced to evidence.
- D2: ≥1 pass + ≥1 violation fixture per kept axis validate against the schema (toy-game).
- D3: reversal/lifecycle obligations present and testable.
- D4: candidate-only — no `formulae/infra-spec`, skill, or registry entry created.
- D5: non-executed plan names the build sequence + the owner-review gate.

## Smallest coherent unit (for Distill)

> *"A YAML-first infra-spec **operational-contract spine** (profile→environments→services→boundaries→state-namespaces + fail-closed gates + 7-state status + typed residue + reversal obligations), reusing dispatch.schema `$defs`, falsified by per-axis pass/violation fixtures, recomposable into the evidence substrate — authored as a run-folder candidate, not a package."*

## Verdict

`pass` — MVP design problem bounded; open choice for Distill: which shape *leads* the MVP (contract-spine vs evidence-first vs schema-only) → tournament.
