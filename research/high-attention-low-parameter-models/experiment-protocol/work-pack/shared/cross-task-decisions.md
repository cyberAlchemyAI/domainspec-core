# Cross-Task Decisions

## Approved Architecture Decisions

| ID | Decision | Status | Source |
| --- | --- | --- | --- |
| HALP-ADR-001 | Content-addressed file artifacts are canonical. | approved-for-plan | [Architecture](../../ARCHITECTURE-BUNDLE.md#design-decisions) |
| HALP-ADR-002 | Four ownership modules join through one TrialCell contract. | approved-for-plan | Architecture |
| HALP-ADR-003 | Deterministic procedural T0 fixtures are first. | approved-for-plan | Architecture/research |
| HALP-ADR-004 | Strict output grammar and deterministic scorer are first. | approved-for-plan | Architecture/research |
| HALP-ADR-005 | Experiment Harness owns repeatable model-run orchestration. | approved-for-plan | Architecture/owner boundary |
| HALP-ADR-006 | Failures and infeasible cells are first-class receipts. | approved-for-plan | Architecture/research |
| HALP-ADR-007 | Retrieval, Phi, realistic data, 128K, and portability are deferred. | approved-for-plan | Architecture/layering |
| HALP-ADR-008 | Resource and capability axes remain separate. | approved-for-plan | Architecture/research |

`approved-for-plan` authorizes planning structure only, not implementation or a
model run.

## Required Human Decisions

| Decision ID | Question | Recommended starting point | Status | Owner | Blocks |
| --- | --- | --- | --- | --- | --- |
| HALP-DEC-001 | What exact checkpoint-scoped claim and primary estimands will the pilot test? | Within-family Llama 1B/3B, stack-specific retention + checkpoint contrast; no causal/general claim. | unresolved | experiment owner | all implementation |
| HALP-DEC-002 | What margins, uncertainty, multiplicity, N, and repetition policy govern acceptance? | Paired analysis with predeclared non-inferiority and false-support margins; values require power/precision rationale. | unresolved | experiment + analysis owner | analysis and run allocation |
| HALP-DEC-003 | What primary workload/matrix is frozen? | Three procedural families; compact/full/absent/no-answer; early/middle/late; 4K plus admitted long bin up to 64K; retrieval deferred. | unresolved | experiment owner | generator/matrix |
| HALP-DEC-004 | What exact model/runtime/backend/precision/KV admission policy is authorized? | Immutable 1B/3B family snapshots, greedy decode, BF16/full KV candidate, dedicated single-H100 stack if admitted. | unresolved | platform owner | admission/execution |
| HALP-DEC-005 | What resource, energy/cost, evidence-retention, license, and publication boundary applies? | GPU-only pilot energy, no cost claim until dated accounting, generated T0 only, external large outputs governed explicitly. | unresolved | repository/resource/publication owners | execution/closeout |

Each decision is recorded separately so a rejected choice does not silently
rewrite another ownership surface.
