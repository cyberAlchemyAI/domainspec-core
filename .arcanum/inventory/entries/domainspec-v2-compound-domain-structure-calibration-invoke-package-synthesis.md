---
tags: [inventory, invoke, define, design, plan, domainspec-v2, experiment, residual-analysis, ui-meta-type, ds-d1, ds-d8, work-pack, task-session, promotion-guardrail]
node_type: synthesis
is_session: false
layer: verified-result
nature: synthesis
status: verified
created: 2026-07-11
target_owner: DomainSpec v2 compound-domain-structure calibration development cycle
next_route: new bounded F3 evidence-repair generation
sources:
  - projects/domainspec-v2/development/ui-meta-type-repair/research/2026-07-11-compound-domain-structures/findings.md
  - projects/domainspec-v2/development/compound-domain-structure-calibration/SPEC.md
  - projects/domainspec-v2/development/compound-domain-structure-calibration/ARCHITECTURE.md
  - projects/domainspec-v2/development/compound-domain-structure-calibration/WORK-PACK.md
---

# DomainSpec v2 Compound Domain Structure Calibration Invoke Package

This non-authority Inventory read model records the Invoke Define, Design, and
Plan package for calibrating the residual-analysis hypothesis. It does not
claim that a compound kind exists or authorize DS-D1, DS-D8, pattern,
candidate, validator, source-repository, or promotion mutation.

## Define

The specification freezes `H(X) = (G,A,Q,R,S,D,U)`, three generation-1
fixtures, four mutually exclusive fixture outcomes, three mutually exclusive
suite verdicts, acceptance criteria, invariants, scope, local glossary,
decisions, and evidence gaps.

## Design

The six-view architecture separates reviewed human predicate inputs from
deterministic residue and outcome computation. Fixture repositories are
read-only; receipts, results, generations, replay, and audits remain inside the
development package.

## Plan

- Complexity: medium, split work-pack.
- Layers: L0 contracts/evaluator, L1 three fixture receipts, L2 generation
  evaluation, L3 independent replay/audit.
- SWUs: seven, each with one parent, dependencies, write scope, done criteria,
  verification, execution owner, and handoff context.
- Parallelism: only the three disjoint L1 fixture SWUs, after explicit runtime
  permission.
- Distill: pass; `SWU-CDSC-001` was the smallest coherent start and all SWUs
  recompose into one audited generation.
- Full dispatch: schema-valid with zero blocks and zero flags.

## Result Boundary

`CALIBRATION-PASS` means the frozen rubric handled the negative control and
replayed deterministically. It does not mean identity, irreducibility,
portability, pattern admission, replication, authority, or promotion.

## Execution State

All seven SWUs are complete. Generation 1 evaluated F1 and F2 as `EXPLAINED`
and F3 as `INSUFFICIENT-EVIDENCE`, producing `CALIBRATION-DEFER` with an
`evidence-repair` route. A fresh-process replay reproduced all semantic bytes,
record handles, and the generation handle. The full package passes 30/30 tests;
GoldenQuill and Savvy remain read-only.

The result does not establish a compound kind. It shows that existing
explanations account for F1 and the F2 collapse control, while F3 cannot be
adjudicated until its permitted screen replacement and breaking
guard/orchestration mutation are observed.

## Next Route

Do not rewrite generation 1. A future, separately authorized package may
preregister and execute the two missing F3 mutations, then append a new bounded
generation. Portability and Page/Layout pattern replication remain later
research gaps and authorize no promotion.
