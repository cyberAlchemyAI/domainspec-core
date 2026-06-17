# DomainSpec v2

Status: research program (pre-implementation)
Owner: DomainSpec v2
Started: 2026-06-11

DomainSpec v2 is the next iteration of the DomainSpec discipline. v1 lives in
[`implementation/domainspec`](../../implementation/domainspec) and is the
evidence source for what already exists. v2 is where we re-think the core ideas
**before** mutating any template, validator, registry, ontology, or runtime
contract.

## How v2 works

v2 advances through **research towers** (see the
[`research-tower`](../../.claude/skills/research-tower/SKILL.md) skill). A tower
turns one hypothesis or source corpus into source-backed, auditable
understanding with explicit borrow / analogy / block / promotion-candidate
decisions. Nothing a tower produces is canonical until a later governed
decision promotes it.

Every tower runs under the [Two-Lane Discipline](research/TWO-LANE-DISCIPLINE.md):

- **Lane Z — zig-zag:** build the proposed idea out, alternating generation and
  critique until it either holds or breaks.
- **Lane A — alternatives:** hold the *underlying problem* fixed and propose a
  genuinely different solution, so we never ship the first idea by default.

## Active research towers

| Tower | Hypothesis under test | Underlying problem | Seed |
| --- | --- | --- | --- |
| [target-state](research/target-state/SEED.md) | Make "target state" an explicit, *buildable* artifact, borrowing from Narrative-Driven Development. | DomainSpec implies a target state everywhere but never formalizes it, so agents lack the discipline of "where are we going / what does done look like." | [SEED](research/target-state/SEED.md) |
| [spec-ontology-unification](research/spec-ontology-unification/SEED.md) | Treat spec and ontology as one typed graph (tree inside a feature, graph across features); feed specs to ephemeral implementation agents that only know node→code-pattern and edge→composition. | Spec→code mapping is implicit, so implementation agents are expensive and drift-prone; spec and code are really two forms of the same domain taxonomy. | [SEED](research/spec-ontology-unification/SEED.md) |
| [dcb-correctness](research/dcb-correctness/HANDOFF.md) | Dynamic Consistency Boundaries as a selective spec-to-code correctness discipline. | Existing validators check a snapshot, not whether a later claim was made against still-current facts. | (already underway) |
| [alloy-tla-modeling](research/alloy-tla-modeling/README.md) | Use Alloy for bounded graph-completeness counterexamples and TLA+/PlusCal for temporal saga behavior, fed by the TypeScript bounded witness. | DomainSpec v2 needs formal-modeling lanes without overclaiming that TypeScript, DCB, Alloy, or TLA+ alone proves saga correctness. | [README](research/alloy-tla-modeling/README.md) |

## Route

The initial target-state and spec-ontology towers are sequenced and gated by one
validated dispatch:
[`domainspec-v2-research-towers.dispatch.json`](research/domainspec-v2-research-towers.dispatch.json).
That route is **designed and validated, not yet executed**. Later towers can
carry their own route or proposed subagent sheet inside their tower folder; for
example, `alloy-tla-modeling` records its `/domainspec-subagents-strategy`
proposal in
[`subagents/PROPOSED-DISPATCH.md`](research/alloy-tla-modeling/subagents/PROPOSED-DISPATCH.md).

## Artifact conventions

- Each tower owns a subfolder under `research/<tower>/` and keeps its own
  seed or `README.md`, `LANE-RECEIPTS.md` when lanes run, learning pack, and
  tower-local notes there.
- Cross-tower, program-level artifacts live at `research/` root and are prefixed
  `PROGRAM-` (e.g. `PROGRAM-SYNTHESIS.md`, `PROGRAM-HANDOFF.md`) so they never
  collide with a tower's own files.
- `dcb-correctness` predates the Two-Lane Discipline; it keeps its four concern
  lanes and carries a recorded alternatives-lane gap (see its
  [RESEARCH-STRATEGY.md](research/dcb-correctness/RESEARCH-STRATEGY.md)).

## Boundaries

- Research writes stay under `projects/domainspec-v2/research/`.
- No template, validator, ontology, registry, or runtime change without a later
  approved `task-session`.
- Public/private submodule discipline still applies (see
  [`SUBMODULE-DISCIPLINE.md`](../../SUBMODULE-DISCIPLINE.md)).
