# Invoke Define Transport

Status: pass-with-decision-gates

Date: 2026-07-18

Observed capability: `invoke`

Mode: `define`

## Intent And Context

The user requested `invoke define design plan` after an auditor-approved
research dispatch concluded that the methodology is sufficient for
specification authoring but not experiment execution.

Context Builder ran in strict/standard form over seven selected sources. Every
define obligation is covered by the accepted findings, explorer evidence,
DomainSpec templates, Invoke contracts, or the prior framing. Whole-repository
context was excluded.

## Discovery Gate

Pass. Discovery evidence exists at:

- `../experiment-protocol-research/findings.md`
- `../experiment-protocol-research/research.md`
- `../high-attention-low-parameter-models-research.md`

No discovery waiver was used.

## Template Selection

| Candidate | Eligibility | Decision |
| --- | --- | --- |
| DomainSpec spec family | Owns capability-driven spec, concept registry, aspect contracts, architecture bundle, and execution pack. | selected |
| Research candidate family | Useful when evidence is missing or contradictory. | rejected: research is already complete and approved |
| Generic candidate family | Would lose the typed capability/aspect contract needed by downstream design and plan. | rejected |

There was no eligible-template tie. Selection is local usage evidence, not
canonical template promotion.

## Structured Interview Gap Check

Questions asked: 0. The user's explicit three-mode request and the accepted
research fix the target and artifact family. Unanswered project choices are not
invented; they are encoded as approval-bearing decision gates. Verdict: pass
for authoring, block for experiment execution.

## Dispatch Technique Trace

| Technique | Applied to | Validation expectation | Result |
| --- | --- | --- | --- |
| `sequence` | research -> define -> design | downstream artifact consumes explicit handles | pass |
| `concrete_path_evidence` | source references | every load-bearing choice links to research or a decision gate | pass |
| `artifact_contract_bridge` | DomainSpec aspect docs | concepts map to material artifact contracts | pass |
| `owner_boundary_check` | Invoke vs experiment execution | Invoke authors; Task Session/Experiment Harness execute | pass |
| `residue_ledger` | unresolved human choices | no choice is silently frozen | pass |
| `handle_handoff` | design input | design consumes paths, not copied authority | pass |

Full dispatch validation is recorded in `DISPATCH.json` because the composite
route crosses Invoke, Distill, Task Session, Experiment Harness, and
observability boundaries.

## Distill Sanity Check

Result: pass. The smallest coherent definition unit is one versioned experiment
protocol with separately owned workload, platform, inference, and budget
surfaces. Splitting them into independent specs would create hidden glue at the
trial-cell, readiness, and phase-gate boundaries. Execution decomposition is
deferred to plan mode.

## Outputs And Evidence Capability Contract

- `execution_path`: Invoke define, local native authoring.
- `dispatch_trace`: this file plus `DISPATCH.json`.
- `template_selection`: DomainSpec spec family, no tie.
- `layering_or_gap`: layering seed carried in the protocol lifecycle and design
  handoff; full artifact is required in plan.
- `result`: `SPEC.md`, `GLOSSARY.md`, and aspect docs.
- `next_route`: Invoke design.

## Unresolved Gaps

The decision ledger is acceptance-critical for a real run: thresholds, sample
allocation, exact checkpoint/runtime identities, retrieval role, resource
boundary, licenses, and publication scope. Define is complete; experiment
execution remains blocked.
