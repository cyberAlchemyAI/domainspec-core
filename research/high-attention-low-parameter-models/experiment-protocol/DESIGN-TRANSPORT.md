# Invoke Design Transport

Status: pass-with-execution-blockers

Date: 2026-07-18

Observed capability: `invoke`

Mode: `design`

## Activation Evidence

- Approved/stable define outputs: `SPEC.md`, `GLOSSARY.md`, aspect docs, and
  `DEFINE-TRANSPORT.md`.
- Source contracts: listed in `ARCHITECTURE-BUNDLE.md`.
- Lifecycle approval: the user explicitly requested define, design, and plan.
- Profile selection: DomainSpec architecture bundle; no eligible tie.

## Context Builder Coverage

Design context used the approved define artifacts and the accepted research
findings. Coverage is complete for the six views, glossary consistency, owner
boundaries, risks, and plan handoff. Runtime implementation evidence was
excluded because design mode is non-mutating.

## Structured Interview Gap Check

Questions asked: 0. Core architecture is determined by the accepted evidence
and define contract. Unresolved numeric/platform/resource choices are explicit
gates and do not require architecture invention. They remain blockers for
execution and inputs to the plan's first task.

## Template/Profile Selection

| Profile | Eligibility | Decision |
| --- | --- | --- |
| DomainSpec architecture profile | Approved DomainSpec define outputs exist and all six views are meaningful. | selected |
| Research companion | Evidence gap would block a design decision. | not triggered; approved research exists |
| UX companion | No human-facing workflow or accessibility surface is in scope. | skipped |
| Architecture pattern inventory | Local file-artifact pipeline is sufficient; no alternative system pattern decision blocks. | skipped |

## Six-View Coverage

1. Context: pass.
2. High-level structure: pass.
3. Low-level components: pass.
4. Workflow process: pass.
5. Decision flow: pass.
6. Dependency/interface: pass.

## Dispatch Technique Trace

| Technique | Applied to | Validation expectation | Result |
| --- | --- | --- | --- |
| `sequence` | define handles -> architecture -> plan handles | no hidden source substitution | pass |
| `artifact_contract_bridge` | components and file contracts | every boundary has producer, consumer, and validation | pass |
| `owner_boundary_check` | Invoke/Task Session/Experiment Harness/Inventory | no false lifecycle or promotion authority | pass |
| `concrete_path_evidence` | source contracts and outputs | load-bearing claims point to artifacts | pass |
| `residue_ledger` | design risks | each gap has owner/treatment | pass |
| `handle_handoff` | plan activation | plan consumes source refs by path | pass |

Full route validation: `DISPATCH.json`.

## Distill Design-Unit Check

Verdict: pass. One protocol instance is the smallest unit that closes trial
identity, readiness, scoring, and phase interpretation. The four ownership
surfaces remain separate components but cannot become independent plans without
hidden cross-surface glue. Optional retrieval, external-family, realistic-data,
and 128K extensions are deferred.

## Implementation Layering

Seed emitted in `ARCHITECTURE-BUNDLE.md`: deterministic artifact closure, one
stack smoke, paired decision pilot, then decision-bearing extensions. Invoke
plan owns the full layering artifact.

## Outputs And Evidence Capability Contract

- `execution_path`: Invoke design, local native authoring.
- `dispatch_trace`: this file plus `DISPATCH.json`.
- `source_contracts`: define outputs and accepted findings.
- `template_selection`: DomainSpec architecture profile.
- `result`: `ARCHITECTURE-BUNDLE.md` and `GLOSSARY-CONSISTENCY.md`.
- `next_route`: Invoke plan.

## Unresolved Gaps

All seven architecture gaps are carried to the work-pack. They block experiment
execution but not planning.
