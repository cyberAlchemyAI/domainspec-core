# Roadmap: DomainSpec Documentation and Packaging Sync

## Overview

This roadmap resolves documentation and packaging drift between the DomainSpec implementation and its published maintainer guidance. The milestone delivers a single focused phase with requirement-complete execution plans and explicit governance safeguards.

## Phases

- [ ] **Phase 1: README and Pack Sync** - Align core docs, copilot docs, installer behavior, and bridge skill packaging with shipped assets.
- [ ] **Phase 2: Harness minimal profile planning** - Plan minimal-first harness execution, Temporal-ready adapter boundaries, and durable promotion gates.

## Phase Details

### Phase 1: README and Pack Sync

**Goal**: Produce accurate, maintainers-first documentation and package integrity for all capabilities currently shipped.
**Depends on**: Nothing (first phase)
**Requirements**: [DOC-01, DOC-02, DOC-03, DOC-04, PKG-01, GOV-01]
**Success Criteria** (what must be TRUE):

1. Main and mirror READMEs document shipped capabilities, versions, and template inventories without drift.
2. Copilot README and INSTALL guide match actual installed agents, skills, and bridge/internal behavior.
3. Required bridge skills referenced by shipped agents exist in distributable copilot skills and install output.
4. A deterministic drift guard can detect command/template/version mismatches.
   **Plans**: 4 plans

Plans:

- [ ] 01-01: Build canonical implementation inventory and drift matrix
- [ ] 01-02: Update canonical and mirror framework READMEs
- [ ] 01-03: Update copilot README and INSTALL documentation
- [ ] 01-04: Fix bridge skill packaging and add drift guardrail

## Progress

**Execution Order:**
Phase 1 executes as wave-ordered plans: Wave 1 -> Wave 2 (parallel) -> Wave 3.

| Phase                               | Plans Complete | Status      | Completed |
| ----------------------------------- | -------------- | ----------- | --------- |
| 1. README and Pack Sync             | 0/4            | Not started | -         |
| 2. Harness minimal profile planning | 0/3            | Not started | -         |

### Phase 2: Harness minimal profile planning

**Goal:** Build an execution-ready phase plan that delivers a deterministic minimal harness profile first, while preserving a clean adapter boundary for future Temporal adoption.
**Depends on:** Phase 1
**Requirements**: [HARN-01, HARN-02, HARN-03, HARN-04]
**Success Criteria** (what must be TRUE):

1. Minimal harness profile is planned as the default build path using deterministic local-first runtime validation.
2. Adapter seams isolate runtime dispatch from durability orchestration so Temporal can be added without harness foundation rewrites.
3. Durable promotion is explicitly gated by trigger conditions: resumable long-running flows, human-in-loop pause-resume, or strict crash-recovery guarantees.
4. Phase plans define synchronization updates for traceability and completion tracking artifacts.
   **Plans:** 3 plans

Plans:

- [ ] 02-01: Define minimal harness profile and Temporal-ready adapter boundary contracts
- [ ] 02-02: Define deterministic harness validation matrix and local-first execution assets
- [ ] 02-03: Define durable promotion gates, migration path, and rollout criteria
