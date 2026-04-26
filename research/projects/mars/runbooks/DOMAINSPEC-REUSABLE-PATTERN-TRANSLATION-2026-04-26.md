# DomainSpec Reusable Pattern Translation (MARS)

Date: 2026-04-26
Scope: full pass over `research/projects/domainspec/**`
Objective: extract reusable research-governance patterns and translate them into MARS skills/agent behaviors.

## Pass Coverage

Reviewed artifact families:

- project contracts (`PROJECT.yaml`, `README.md`, `deps/`, `registry/`)
- canonical semantics (`definitions/DEFINITIONS.md`, `definitions/DEFINITIONS-INDEX.md`)
- execution contracts (`protocols/DOMAINSPEC-PROTOCOL-CHECKLIST.md`, `experiments/EXPERIMENTS.md`)
- experiment bundles (`experiments/E1...E11/{context.md,protocol.md,sources.md,data/,results/,README.md}`)
- reference authority stack (`sources/REFERENCE-LEDGER.md`, `sources/AUTHORITY-SOURCES-2026-04-26.md`, `sources/REFERENCE-WAIVERS.md`)
- inventory stack (`inventory/INVENTORY-INDEX.md`, authority/domain entries)
- evidence/adjudication stack (`results/DOMAINSPEC-EVIDENCE-STATUS.md`, `experiments/OPEN-DECISIONS.md`)
- normalization execution artifacts (`results/KNOWLEDGE-STACK-REORGANIZATION-EXECUTION-2026-04-26.md`)

## Reusable Pattern Catalog

| Pattern ID | DomainSpec Evidence | Reusable Abstraction | Current MARS Coverage | Translation Target | Priority |
|---|---|---|---|---|---|
| RP-01 | `definitions/DEFINITIONS.md` + inline intuition | canonical-definition authority with colocated formal+intuition semantics | partial (`mars-research-definitions-governance`) | skill hardening and policy reminders | P0 |
| RP-02 | `definitions/DEFINITIONS-INDEX.md` | definition ID registry with drift notes and optional-candidate promotion | partial (`DEFINITIONS-INDEX.md` exists) | add index-governance checks in planner/protocol flow | P1 |
| RP-03 | `protocols/DOMAINSPEC-PROTOCOL-CHECKLIST.md` | protocol gate checklist with measurable criteria, metadata, anchors, context obligations | strong (`MARS-PROTOCOL-CHECKLIST.md`, protocol-designer agent) | keep parity by periodic checklist sync | P1 |
| RP-04 | `sources/REFERENCE-LEDGER.md` + `sources/REFERENCE-WAIVERS.md` + authority sources extension | authority-source governance (pins, status, waivers, promotion rules) | weak (ledger exists, governance skill missing) | new skill `mars-research-authority-governance` | P0 |
| RP-05 | `inventory/INVENTORY-INDEX.md` multi-view + gaps | inventory readiness dashboard with gap queue and source-entry linkage quality | moderate (`inventory` skill exists) | fold gap taxonomy and readiness metrics into generic inventory workflow | P1 |
| RP-06 | 11/11 `experiments/*/context.md` six-section structure | context bundle minimum contract and conflict visibility | moderate (`MULTI-SOURCE-CONTEXT-PATTERN.md`) | add explicit context governance loop in planning/execution | P1 |
| RP-07 | 11/11 bundle README pattern + root dashboard markers | experiment navigation contract with per-bundle onboarding | strong (`mars-research-experiments-index`, project index scripts) | keep as default for all projects | P0 |
| RP-08 | `experiments/OPEN-DECISIONS.md` generated rollup | unresolved-decision aggregation and remediation workflow | strong (implemented via index script) | extend to all MARS projects with status language conventions | P1 |
| RP-09 | E11 `protocol.md` gate command blocks (G2/G3/G4 scripts) | executable gate preflight checks colocated with protocol | weak (policy exists, codified skill missing) | future skill `mars-research-gate-preflight` | P2 |
| RP-10 | knowledge-stack reorganization report/backlog wave model | wave-based brownfield normalization with residual-risk publication | weak (no dedicated MARS workflow) | new skill `mars-research-knowledge-stack-normalization` | P0 |
| RP-11 | `results/DOMAINSPEC-EVIDENCE-STATUS.md` update policy | claim-evidence vocabulary and transition contract | moderate (`MARS-EVIDENCE-STATUS.md`, evidence-auditor agent) | add explicit downgrade/remediation policy checks | P1 |
| RP-12 | `registry/TRACEABILITY-MATRIX.md` claim-to-artifact matrix | traceability contract across claims, experiments, data, results, paper | strong (MARS matrix exists) | strengthen planner enforcement for missing links | P1 |

## Translation Decisions

### Implement immediately (this wave)

1. Add `mars-research-authority-governance` skill for RP-04.
2. Add `mars-research-knowledge-stack-normalization` skill for RP-10.
3. Update MARS rollout/planner/orchestrator instructions to reference these workflows.

### Queue next

1. Add `mars-research-context-bundle-governance` skill for RP-06.
2. Add `mars-research-gate-preflight` skill for RP-09.
3. Add periodic parity audit between DomainSpec protocol checklist and MARS protocol checklist (RP-03).

## Agent Update Targets

| Agent | Update |
|---|---|
| `mars-research-planner` | invoke normalization skill for brownfield projects with fragmented definitions/references/context artifacts |
| `mars-research-orchestrator` | require authority-governance remediation before passing G2/G3 when pin/waiver drift is detected |
| `mars-research-sourcer` | align source-selection outputs with authority-governance status vocabulary |
| `mars-research-evidence-auditor` | enforce evidence downgrade/upgrade policy language symmetry with claim matrix |

## Success Criteria For Translation

1. New MARS skills encode RP-04 and RP-10 workflows with deterministic outputs.
2. Planner/orchestrator guidance references those skills for dependency-safe execution.
3. Brownfield projects can normalize to MARS contracts without ad hoc runbook invention.
4. Source authority, waivers, and inventory linkage are auditable before execution starts.
