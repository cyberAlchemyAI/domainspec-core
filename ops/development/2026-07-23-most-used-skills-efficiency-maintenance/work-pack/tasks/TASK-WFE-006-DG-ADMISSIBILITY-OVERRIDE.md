# TASK-WFE-006 — Filter Decision Options And Type Overrides

- Change: DG-1 / WFE-R07
- Layer/slice/wave: L1 / S1 / W1
- Lifecycle owner: `sigil-development` for Decision Gate
- Status: complete; see SWU-WFE-006A and SWU-WFE-006B receipts

## Objective

Keep malformed structure out of human preference questions and replace ambient
override with typed, target-bound, one-use authorization that cannot bypass a
protected owner gate.

## Sources

- `arcanum/arcana/decision-gate/SKILL.md`: applicability, viable options,
  explicit override, observability
- accepted findings DG-1 and verifier correction: two or more admissible
  options, not only repairs
- `../../DESIGN.md#decision-flow-view`

## SWU-WFE-006A — Option admissibility

- Primary behavior: route candidate cardinality after structural admissibility.
- Acceptance boundary: zero admissible → direct structural `BLOCK`; one safe
  admissible route → owning gate/direct route; two or more → Decision Gate;
  options may include defer/stop.
- Split analysis: the three outcomes are rows of one deterministic prefilter.

Inputs: candidate options with structural verdict, owner gate, reversibility,
hazard class, and evidence. Output: `block | direct | gate` plus reasons.

## SWU-WFE-006B — Typed override

- Dependency: 006A pass.
- Primary behavior: validate and consume one override for one target/scope/hazard.
- Acceptance boundary: ambient assent, missing target, stale receipt, scope
  mismatch, second use, and protected hazard without owner receipt fail; exact
  valid override consumes once.
- Split analysis: scope, hazard, target, lifetime, issuer, and consumption are
  conjuncts of one override-admission decision.

Required fields:

```yaml
override_id: string
target: string
scope: [repo-relative path or decision id]
hazard_class: reversible | destructive | authority | promotion | publication | spend | other
issuer: string
rationale: string
issued_at: timestamp
expires_at: timestamp | null
owner_gate_receipt: path | null
consumed_by: run id | null
```

Protected classes require their owning gate regardless of generic override.

## Scope and validation

- Canonical and fixtures: `arcanum/arcana/decision-gate/`.
- Generated runtimes: declared outputs only.

```bash
bash arcanum/arcana/decision-gate/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/decision-gate .agents/skills/decision-gate .claude/skills/decision-gate
```

Create the focused harness if absent and record it as part of the first SWU.

- Execution owner: `sigil-development`.
- Receipt: option cardinality matrix, override replay matrix, protected-gate proof.

## Done

Humans see only real choices, one safe route does not manufacture consent
theater, and override cannot become ambient reusable authority.
