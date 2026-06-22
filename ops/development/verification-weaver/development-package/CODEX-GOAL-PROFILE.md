# Codex Goal Profile: Verification Weaver

## Codex Goal Profile Result

- Source work-pack: `ops/development/verification-weaver/development-package/WORK-PACK.md`
- Selected unit: `SWU-VW-001`
- Readiness: pass
- Goal budget: 4000 chars, pass
- Decision profile: none; consumed fields n/a
- One-shot mode: yes, one SWU covers the full work-pack
- Capability policy: no subagents; no registry/generated runtime exposure; no broad `refine`, `invoke`, `craft`, or `decision-gate` authority unless a named blocker requires a stop report and the user explicitly resumes with that route
- Sidecar profile: `ops/development/verification-weaver/development-package/CODEX-GOAL-PROFILE.md`

## Native Goal

```text
/goal Execute SWU-VW-001 from ops/development/verification-weaver/development-package/WORK-PACK.md to create the candidate public Arcana package arcanum/arcana/verification-weaver/. Pack-first: use CODEX-GOAL-PROFILE.md, WORK-PACK.md, tasks/SWU-VW-001.md, DISPATCH.json, DEFINE.md, DESIGN.md, OUTPUT-CONTRACT.md, QUALITY-BAR.md, ANTI-PATTERNS.md, negative-controls/NEGATIVE-CONTROLS.md, IMPLEMENTATION-LAYERING.md, DISTILL-VALIDATION.md, and RUNTIME-HANDOFF.md as the execution contract. Write primarily inside arcanum/arcana/verification-weaver/ only. Create README.md, SKILL.md, development/OUTPUT-CONTRACT.md, QUALITY-BAR.md, ANTI-PATTERNS.md, VALIDATION-EXPERIMENT.md, synthetic fixtures, runnable negative controls, and a shell-first development/run-validation-fixtures.sh, using TypeScript only if shell cannot safely validate structured receipts. Preserve owner lanes: test-derivation, ux-evidence-validator, experiment-harness, architecture-pattern-inventory, research-evidence-harness. Build fresh public code and synthetic examples only; do not port private implementation code, private fixtures/examples, private pass/fail claims, generated runtime evidence, or local observability logs. Do not edit arcanum/registry/, generated runtime packages, private submodules, validation/poker-team/, or existing owner capabilities except for non-invasive links from the new package. Verify with bash arcanum/arcana/verification-weaver/development/run-validation-fixtures.sh; git diff --check -- arcanum/arcana/verification-weaver; and a private/generated evidence denylist scan scoped to arcanum/arcana/verification-weaver. Stop and report blocked if validation needs private examples, no classifier exists, no runnable negative controls exist, VERIFICATION-WEAVE can promote owner outputs, or registry/generated runtime exposure becomes necessary. Final report must list artifacts, validation results, residue, any extra sources used and the named gap that justified each, and the next sigil-development/experiment-harness route.
```

## Verification Surface

```bash
bash arcanum/arcana/verification-weaver/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/verification-weaver
rg -n "implementation/domainspec|validation/poker-team|/home/vrondelli|\\.arcanum/observability|example-outputs|example-runs|development/runs" arcanum/arcana/verification-weaver
```

The `rg` scan may find documentation that names blocked patterns only when the
context explicitly marks them as blocked and not as copied evidence.

## Boundaries

Write scope:

- Primary: `arcanum/arcana/verification-weaver/`
- Generated validation reports may live under the new package's `development/`
  layout and must be ignored or treated as generated evidence according to the
  package contract.

Read scope:

- `ops/development/verification-weaver/development-package/`
- Public owner skill files referenced by the work-pack.

Do not modify:

- `arcanum/registry/`
- generated runtime skill packages;
- private implementation submodules;
- `validation/poker-team/`;
- existing owner capabilities, except for non-invasive links from the new
  package if needed.

## Handoff Pack

- Markdown: `ops/development/verification-weaver/development-package/WORK-PACK.md`
- Structured index/dispatch: `ops/development/verification-weaver/development-package/DISPATCH.json`

## Strict Coverage

Pass. The selected work-pack has one SWU, concrete write scope, explicit
acceptance criteria, validation commands, owner-boundary constraints, Distill
validation, and a dispatch handoff that validates under Dispatch Spec.

## Fallback Exploration

Named gaps only. Extra exploration is allowed only for a specific blocker from
the pack, such as missing shell validation mechanics, receipt schema parsing,
fixture shape, or public-boundary scan behavior.

## Extra-Source Reporting

Required. The final runtime report must name every source used outside the
handoff pack, the named gap that justified it, and whether it changed the
implementation result.

## Stop Condition

Stop and report blocked if:

- validation needs private examples to pass;
- no target classifier exists;
- no runnable negative controls exist;
- `VERIFICATION-WEAVE` can promote owner outputs;
- generated runtime or registry exposure is needed to satisfy the work-pack;
- public/private evidence rules cannot be enforced.

## Validation

- Readiness checked against `WORK-PACK.md`, `tasks/SWU-VW-001.md`,
  `DISPATCH.json`, `DEFINE.md`, `DESIGN.md`, `OUTPUT-CONTRACT.md`,
  `QUALITY-BAR.md`, `NEGATIVE-CONTROLS.md`, `IMPLEMENTATION-LAYERING.md`,
  `DISTILL-VALIDATION.md`, and `RUNTIME-HANDOFF.md`.
- Sidecar written: yes.
