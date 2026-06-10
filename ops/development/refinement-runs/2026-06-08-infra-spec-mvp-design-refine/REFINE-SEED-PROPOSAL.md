# Refine Seed Proposal: Infra-Spec MVP Design

Date: 2026-06-08
Target: the infra-spec **research synthesis corpus** (`ops/development/infra-spec-*.md`) produced by the strategy execution
Desired outcome: an MVP-ready, **non-executed** infra-spec design + plan — a YAML-first operational-contract-spine schema candidate, a fixture-first validation plan, and the net-new reversal/lifecycle obligations — all candidate-only (no `formulae/infra-spec` promotion)
Preset: full
Research mode: research-if-gap-appears
Status: seed-ready

## Intent

Refine the infra-spec research synthesis into a concrete, MVP-ready design and non-executed plan. The research route already answered *whether* infra-spec is worth building and *what shape* it should take (an evidence substrate, R3, with an operational-contract surface, R2). This refinement turns that synthesis into the smallest coherent **buildable** unit: the operational-contract spine schema + its fixtures + the missing reversal/lifecycle obligations — without authoring the package.

This is the handoff's recommended next route ("fixture-first MVP schema design"), now executable because the previously-deferred submodules (`implementation/domainspec`, `validation/poker-team`) are initialized.

## Source Context

- `ops/development/infra-spec-research-brief.md` — winning reading (evidence substrate) + candidate definition. Primary.
- `ops/development/infra-spec-candidate-dag.md` — concept nodes N1–N12 + critical path (MVP spine = N1→N2→N3→N4 + N11 gate + N5 status floor).
- `ops/development/infra-spec-interpretation-tournament.md` — why R3 won; R2-vs-R3 MVP tension.
- `ops/development/infra-spec-schema-taxonomy-ledger.md` — 14 axes (12 keep), minimal record shape, reuse of `dispatch.schema.yml` `$defs`.
- `ops/development/infra-spec-lean-transfer-ledger.md` — discipline constraints (schema≠instance, status separation, block≠fail, analogy-demotion).
- `ops/development/infra-spec-gap-hunt-ledger.md` — net-new reversal/lifecycle gap (N12).
- `ops/development/infra-spec-cross-project-pattern-catalog.md` + `…-runtime-atlas.md` — goldenquill promotion precedent; generate-from-spec pattern.
- `.claude/skills/dispatch-spec/dispatch.schema.yml` — the `$defs` to reuse (boundary/authority/receipt/state_namespace/promotion_split/gate).
- Now-available submodules: `implementation/domainspec` (`INFRA-SETUP.md`, `domainspec-infra-*` skills), `validation/poker-team` (canonical exemplar).

## Refinement Questions

1. What is the smallest YAML-first infra-spec record (the operational-contract spine) that is genuinely useful and recomposes into the full evidence substrate?
2. Which axes ship in the MVP vs defer to residue, and why (Pareto: value vs cost vs owner-boundary risk)?
3. What pass + violation fixtures falsify the schema cheaply before any package is built?
4. How are the net-new reversal/lifecycle obligations (N12) encoded so a `promoted` status is trustworthy?
5. What must remain analogy (Lean reflection-tower object, etc.) and not leak into the schema?

## Constraints

- Candidate-only: do NOT create `formulae/infra-spec`, a skill, a validator package, or registry entries. Design + plan + fixtures only.
- YAML-first, validator-backed (infra-spec non-negotiable).
- Reuse `dispatch.schema.yml` `$defs`; redefine only `boundary.kind` for infra (network/secret/data/tenant).
- Runtime evidence is not promotion authority; promotion stays gated + owner-reviewed.
- Write scope: `ops/development/infra-spec-*` and this run folder (parent-owned). Do not mutate submodule contents.
- Preserve, do not flatten, the research residue (template-drift question, F4 evidence-layer gap).

## Done Criteria

- A YAML-first `infra-spec` MVP record shape is specified (candidate), with each field traced to evidence.
- A fixture plan (≥1 pass + ≥1 violation per kept axis) is defined — the toy-game falsification surface.
- Reversal/lifecycle obligations are added to the design.
- Deferred axes recorded as residue with rationale.
- A non-executed plan names the build sequence and the owner-review gate before any package creation.

## Planned Stage Configuration (canonical ten-stage loop)

1. Context Builder evidence baseline: `context-builder` standard (`--strict --emit both --handoff runtime --persist <run-folder>/context-builder`).
2. Invoke Define: `invoke` define (define the MVP design problem).
3. Interrogation refine-review: `interrogation` refine-review.
4. Research decision: refine-owned, research-if-gap-appears.
5. Distill: `distill` standard (tournament over candidate MVP shapes).
6. Invoke Redefine / Design: `invoke` design (the YAML-first schema candidate).
7. Interrogation refine-design-review: `interrogation` refine-design-review.
8. Distill Repair: `distill` validate (toy-game: build + check the fixtures).
9. Invoke Plan: `invoke` plan (non-executed build sequence + owner-review gate).
10. Final Interrogation and Synthesis: `interrogation` refine-final + Refine synthesis.
