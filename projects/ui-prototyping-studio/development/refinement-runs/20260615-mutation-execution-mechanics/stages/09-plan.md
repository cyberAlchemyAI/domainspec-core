# Plan: Mutation Execution Mechanics (s9, NON-EXECUTED)

Artifact written to: `/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/09-plan.md`

## What it covers (all spec requirements)

- **Schema migrations** (Layer 0.1, domain/models.ts): GAP-1 `MutationTask.odId` + `MutationChangeType` union; `DiffSummaryHonest`/`OdDiffFragment`; GAP-2 manifest `htmlArtifactRef`/`candidateHtmlHash`/`provenance`; `ExecutionProvenance`. All tagged PROPOSAL.
- **Deterministic validator modules, one per check** (Layer 1.2, new `domain/validators/v1..v9b.ts`) plus the whole-tree od-id-attributed diff (Layer 1.1, R1/TG-1 BLOCK fix) and suite runner + composite verdict D14 (Layer 1.3).
- **Engine contract + CLI wiring** (Layer 2.1 port + canonical-serialized envelope F1; Layer 5 `studio apply` CLI: propose via Claude Code -> validate -> show diff -> accept, value-in/value-out, impure lane only in interface/).
- **Apply state-machine changes** (Layer 2.3 activating dormant `RevisionApplied` preview state, single-flight, expiry; Layer 2.4 two-gate accept + accept-time staleness re-check D13/C3; Layer 3 atomic all-or-nothing recorder + compensating rollback + `removeRevision`).
- **Testing** (Section 5): deterministic validator unit tests (one per validator, toy-game falsifiers as regression fixtures), state-machine unit tests with a fake proposer, recorder atomicity tests, calibration boundary tests, and a toy-game-style e2e through the full CLI with a scripted proposer.

## Ordering and layout
- Ordered MWU -> hardening: L0 substrate (closes A1 artifact port) -> L1 pure validator suite (MWU, closes B1) -> L2 two-gate machine (closes C1) -> L3 recorder atomicity (closes C2) -> L4 spike-gated calibration + R2 -> L5 CLI seam -> L6 governance/migration.
- Each element mapped to real files in domain/application/infrastructure/interface, verified against the code (no invented surfaces).

## Proposal discipline
- 10 numbered PROPOSAL items (Section 4); 2 marked spike-gated (S/B/k/c calibration, V2 R2-a/R2-b). No canonical mutation without approval. RESIDUE-B named as the single gating next action; L0-L3 buildable before the spike, L4 numbers/semantics spike-gated.
- Full s7/s8 obligation -> layer traceability table (Section 3); nothing dropped.