---
tags: [dispatch, verification-weaver, public-private-boundary]
node_type: dispatch-sheet
is_session: false
layer: research
nature: reference
status: pass
created: 2026-06-21
dispatch_id: 2026-06-21-verification-weaver-research
dispatch_type: research
working_folder: ops/development/verification-weaver/research/2026-06-21-verification-weaver-research/
sources:
  - implementation/domainspec/.codex/agents/domainspec-test-designer.agent.toml
  - implementation/domainspec/tools/test-derivation-engine/
  - implementation/domainspec/TEST-PIPELINE.md
  - arcanum/arcana/test-derivation/
  - arcanum/arcana/ux-evidence-validator/
  - arcanum/arcana/experiment-harness/
  - arcanum/arcana/architecture-pattern-inventory/
  - arcanum/arcana/research-evidence-harness/
---

# Dispatch Sheet: Verification Weaver Research

Dispatch ID: `2026-06-21-verification-weaver-research`

Goal: produce evidence-bound findings that map existing test-related tools and
testing practices inside `domainspec-core`, then recommend a public-safe Arcanum
testing capability that combines DomainSpec derivation, UI/UX evidence,
execution validation, and inventory usefulness without copying private
implementation code into public `arcanum`.

## Confirmation Gate

User confirmed the strategy after the check-tension gate passed.

Preflight helpers:

- `Fermat`: check-tension PASS.
- `Wegener`: check-tension PASS.

Ledger registration:

- Registered in `telemetry/agents/subagents-dispatch.yaml`.
- Dispatch type: `research`.
- Max loops: `1`.
- Final approver in the registered route: `Meadows, Donella H.`

## Agent Route

| Group | Count | Purpose | Status |
| --- | ---: | --- | --- |
| Explorers | 4 | Map private deterministic derivation, public Arcanum testing owners, UI/UX evidence, and practical validation surfaces. | complete |
| Synthesizer | 1 | Reconcile explorer returns into candidate capability shapes and owner boundaries. | complete |
| Reviewers | 3 | Apply precedent, definition, and counterexample gates. | complete |
| Writer | 1 | Produce findings-ready text from returns and reviewer corrections. | complete |
| Auditor | 1 | Audit final findings and package readiness. | pending at write time |

## Frozen Anti-Bias

Primary tension:

`deterministic derivation optimism` vs `public Arcanum reuse pressure` vs
`UI/UX evidence risk` vs `implementation practicality`.

The package must not let one strong lane become fake authority for all testing.

## Source Anchors

Private implementation sources used as research input:

- `implementation/domainspec/.codex/agents/domainspec-test-designer.agent.toml`
- `implementation/domainspec/tools/test-derivation-engine/`
- `implementation/domainspec/TEST-PIPELINE.md`
- Representative private test and validation surfaces in `implementation/domainspec/`
  and `validation/poker-team/`.

Public Arcanum owners used as placement evidence:

- `arcanum/arcana/test-derivation/SKILL.md`
- `arcanum/arcana/ux-evidence-validator/SKILL.md`
- `arcanum/arcana/experiment-harness/SKILL.md`
- `arcanum/arcana/architecture-pattern-inventory/SKILL.md`
- `arcanum/arcana/research-evidence-harness/SKILL.md`
- `arcanum/framework/EXPERIMENT-HARNESS-STANDARD.md`

## Dispatch Result

The route converged on a candidate public Arcana package named
`verification-weaver`, but only as a testing-specific router and parent receipt
contract. It is not a canonical tester and must not own derivation, UX
validation, execution, architecture mapping, research adjudication, task
execution, definition mutation, or promotion.
