# Z-Rig / Arcanum Integration Findings

Dispatch: `2026-06-17-zrig-arcanum-integration-handoff`

## Core Verdict

GO for private parent-local governance, planning, review, management, and
handoff artifacts.

REVISE/DEFER bounded execution until a ready work-pack and exactly one private
remediation SWU exist.

NO-GO for live authority, product trust, public promotion, runtime adapter
claims, public Z-Rig command surfaces, or treating Arcanum as Z-Rig's internal
execution engine until engine proofs land.

## Verdict Matrix

| Area | Verdict | Calibration | Target |
| --- | --- | --- | --- |
| Private governance/planning/handoff | Narrow GO | Allowed only as parent-local artifact work. Does not prove product mode. | `projects/zrig/development/arcanum-integration-remediation/` |
| Invoke remediation pack | Narrow GO | First real slice. Every SWU must map to F1-F14 and include command/check. | `SPEC.md`, `DESIGN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, `EXECUTION-PACK.md` |
| Craft scoped state | Narrow GO | Ledger/view only. Records decisions, status, links, and evidence. No runtime authority. | `projects/zrig/.craft/ledger.yml`, `projects/zrig/CRAFT.md` |
| Task-session execution | REVISE/DEFER | Allowed only after work-pack exists and only for one bounded private remediation SWU. Not product-mode proof. | Prefer F1 generic-gate fail-closed behavior or F3 residue schema/fatality policy |
| Architecture inventory | Narrow GO | Private observed-architecture/gap inventory, not declared integration architecture. | `projects/zrig/architecture/PRODUCT-MODE-AUTHORITY-INVENTORY.md` |
| Observability | Design-only | Obligations only. No wired metrics, signal bridge, or active telemetry claim. | `projects/zrig/development/arcanum-integration-remediation/OBSERVABILITY-OBLIGATIONS.md` |
| Runtime handoff adapter | PARK/DEFER | Not a near-term plan item. Requires engine proofs and adapter policy first. | No adapter entrypoint now |
| Signal Observer bridge | PARK/DEFER | Not near-term. Do not claim a bridge over arbitrary Z-Rig waves. | No bridge work now |
| Experiment Harness | PARK/DEFER | Wait until wrapper contract, proofs, and validation policy exist. | No experiment package now |
| Public Z-Rig sigil/spell | NO-GO/PARK | Requires public-safe extraction and validation evidence. | No public Arcanum promotion now |
| Arcanum as Z-Rig inner engine | NO-GO | Would misstate authority and collapse wrapper into runtime. | No runtime replacement |
| Product-mode trust claim | NO-GO | Validation can prove artifact discipline or bounded remediation completion only. | No live/product assurance language |

## Required Private Artifacts

- `projects/zrig/development/arcanum-integration-remediation/SPEC.md`
- `projects/zrig/development/arcanum-integration-remediation/DESIGN.md`
- `projects/zrig/development/arcanum-integration-remediation/IMPLEMENTATION-LAYERING.md`
- `projects/zrig/development/arcanum-integration-remediation/WORK-PACK.md`
- `projects/zrig/development/arcanum-integration-remediation/EXECUTION-PACK.md`
- `projects/zrig/architecture/PRODUCT-MODE-AUTHORITY-INVENTORY.md`
- `projects/zrig/development/arcanum-integration-remediation/OBSERVABILITY-OBLIGATIONS.md`
- `projects/zrig/.craft/ledger.yml`
- `projects/zrig/CRAFT.md`

## Authority Inventory Mapping

`PRODUCT-MODE-AUTHORITY-INVENTORY.md` should map:

| Authority Surface | Finding Link | Why It Matters |
| --- | --- | --- |
| Gates / generic pass behavior | F1 | Product-mode success cannot rely on generic gates for spec-governed waves. |
| Live identity authority | F4 | Bridge-reported model/family identity is not trusted authority. |
| Deploy/sentinel reachability | F6 | Side-effectful waves are not operator-reachable through normal context. |
| Residue schema and fatality policy | F3 | Audit residue can fail while a run reports success. |
| Shared failover cap | F9 | Concurrent failover cannot be enforced by per-seat counters. |
| Dependency declaration | F8 | Verification and live imports are blocked by undeclared dependencies. |

## First Executable SWU

The first executable unit should be one of:

- F1 generic-gate fail-closed behavior with focused regression checks.
- F3 residue schema/fatality policy with focused tests.

Do not start with a runtime adapter, Signal Observer bridge, Experiment Harness,
public sigil/spell, or live/deploy/sentinel path.

## Command-Surface Boundary

No new public Arcanum command, sigil, spell, generated runtime package, adapter
entrypoint, or registry item may mention Z-Rig, OpenClaw, Analog,
deploy/sentinel flows, private product assumptions, or Z-Rig-specific
product-mode claims.

Public Arcanum may own only generic lifecycle contracts. Private parent/Z-Rig
owns product evidence, review material, handoffs, remediation packs,
inventories, and future adapter constraints.

## Validation Limits

Validation may prove:

- artifact discipline;
- public/private boundary discipline;
- Craft ledger/view existence and evidence links;
- one bounded private remediation SWU completion;
- command/check execution for that selected SWU.

Validation must not be worded as proof of:

- live bridge readiness;
- deploy/sentinel authority;
- trusted live identity;
- residue fatality correctness;
- product-mode assurance;
- public promotion readiness.

## Acceptance Conditions

The next architecture/plan packet is acceptable only if it:

- is stored under private `projects/zrig/**` paths;
- names public Arcanum only as generic lifecycle framing;
- maps every implementation task or SWU to F1-F14 or an explicit non-code
  artifact obligation;
- gives each SWU an owner, artifact path, write scope, command/check, and
  acceptance evidence;
- parks runtime adapter, Signal Observer bridge, Experiment Harness, and public
  promotion work until proofs and extraction policy exist.
