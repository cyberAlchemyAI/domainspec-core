# Invoke Handoff: Z-Rig / Arcanum Integration Remediation

Dispatch: `2026-06-17-zrig-arcanum-integration-handoff`

## Handoff Intent

Prepare private parent-local remediation artifacts for Z-Rig integration
governance. This is architecture, planning, management, and handoff work only.

Do not create public Arcanum Z-Rig commands, sigils, spells, generated runtime
packages, registry entries, or adapter entrypoints.

Do not claim live Z-Rig authority, product-mode trust, runtime adapter
readiness, wired metrics, or public promotion.

## Core Verdict

- GO: private parent-local governance, planning, review, management, and
  handoff artifacts.
- REVISE/DEFER: bounded execution until a ready work-pack and exactly one
  private remediation SWU exist.
- NO-GO: live authority, product trust, public promotion, runtime adapter
  claims, public Z-Rig command surfaces, or Arcanum as Z-Rig's internal
  execution engine.

## Ownership Boundary

Public Arcanum owns only generic lifecycle contracts.

Private parent/Z-Rig owns:

- product evidence;
- review material;
- handoffs;
- remediation packs;
- observed-architecture/gap inventories;
- observability obligation design;
- future adapter constraints, if proofs and extraction policy later exist.

Private product material must remain under `projects/zrig/**` or another
parent-local private path.

## First Real Slice

Create a private remediation pack at:

`projects/zrig/development/arcanum-integration-remediation/`

Required files:

- `SPEC.md`
- `DESIGN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `EXECUTION-PACK.md`

`WORK-PACK.md` requirements:

- every SWU maps to one or more of F1-F14;
- every SWU has a concrete command/check;
- every SWU states what it can and cannot prove;
- no SWU claims product-mode assurance unless the corresponding engine proof
  exists.

`EXECUTION-PACK.md` requirement:

- include only the selected remediation SWU;
- do not frame execution as live Z-Rig authority;
- do not include runtime adapter, Signal Observer bridge, Experiment Harness, or
  public sigil/spell work.

## Craft Management State

Create or prepare scoped Craft management state:

- `projects/zrig/.craft/ledger.yml`
- `projects/zrig/CRAFT.md`

Craft acceptance:

- ledger/view exist;
- links to review evidence are present;
- blockers, decisions, gaps, next moves, and status are represented;
- no language claims Craft confers runtime authority, proof, or product-mode
  trust.

Suggested initial Craft rows:

- `CTX-ZRIG-PRODUCT-MODE`
- `ART-ZRIG-REVIEW-STRATEGY`
- `ART-ZRIG-ATTACKS`
- `ART-ZRIG-FINDINGS`
- `ART-ZRIG-UNDERSTANDING`
- `BLK-ZRIG-GATES-GENERIC`
- `BLK-ZRIG-LIVE-DEPLOY-SENTINEL`
- `BLK-ZRIG-AUDITABILITY`
- `BLK-ZRIG-RUNTIME-AUTHORITY`
- `BLK-ZRIG-SPEC-DRIFT`
- `DEC-ZRIG-GATE-POLICY`
- `DEC-ZRIG-LIVE-IDENTITY-AUTHORITY`
- `DEC-ZRIG-DEPLOY-SURFACE`
- `DEC-ZRIG-RESIDUE-FATALITY`
- `DEC-ZRIG-AUTO-SPEC`
- `DEC-ZRIG-METRICS-STATUS`
- `GAP-ZRIG-COVERAGE-APPROVAL`
- `GAP-ZRIG-OPERATOR-CONTRACT`
- `GAP-ZRIG-DEPENDENCY-MANIFEST`
- `GAP-ZRIG-REPRO-HARNESS`
- `GAP-ZRIG-RECOMPOSITION-PACKET`

## Architecture Inventory

Create:

`projects/zrig/architecture/PRODUCT-MODE-AUTHORITY-INVENTORY.md`

This is a private observed-architecture/gap inventory, not declared integration
architecture.

It should map:

- gates to F1;
- identity to F4;
- deploy/sentinel to F6;
- residue to F3;
- failover to F9;
- dependencies to F8.

It should distinguish observed behavior, missing proof, required remediation,
and validation/check surface.

## Observability Obligations

Create:

`projects/zrig/development/arcanum-integration-remediation/OBSERVABILITY-OBLIGATIONS.md`

This is design-only.

It may define obligations derived from findings, especially F1, F3, F6, and
F14. It must not claim wired metrics, active telemetry, Signal Observer bridge
readiness, or Z-Rig runtime observability.

## Parked Work

Do not include these as near-term plan items:

- runtime handoff adapter;
- Signal Observer bridge;
- Experiment Harness package;
- public Z-Rig sigil/spell;
- public generated runtime package;
- any public command surface mentioning Z-Rig/private product assumptions.

These remain parked until engine proofs and public-safe extraction policy exist.

## Validation Surfaces

- Parent/submodule boundary: `make doctor`, `make bump-check`, and boundary scan
  before parent publication.
- Handoff validity: every claim cites
  `projects/zrig/review/2026-06-17-zrig-engine-product-mode/{findings.md,understanding-map.md}`
  or a Z-Rig source path.
- Craft slice: ledger/view exist, link to evidence, and do not claim runtime
  authority.
- Work-pack slice: each SWU has owner, artifact path, write scope,
  command/check, and acceptance evidence.
- Engine SWU checks: start with focused tests or blocked-run notes for F1/F3;
  no `--live`, deploy, or sentinel assurance claim until prerequisites are
  fixed.
- Boundary validation: no new public Arcanum command, sigil, spell, generated
  runtime package, adapter entrypoint, or registry item may mention Z-Rig/private
  product assumptions.

Validation can prove artifact discipline and bounded remediation completion. It
must not be worded as proof of live bridge, deploy/sentinel, identity, residue
fatality, or product-mode assurance until those engine checks pass.

## Recommended Next Route

1. Create the private remediation pack and Craft management state.
2. Build `PRODUCT-MODE-AUTHORITY-INVENTORY.md`.
3. Build `OBSERVABILITY-OBLIGATIONS.md` as design-only.
4. Select exactly one private remediation SWU from `WORK-PACK.md`.
5. Run `task-session` only for that selected SWU.

Preferred first SWU:

- F1 generic-gate fail-closed behavior; or
- F3 residue schema/fatality policy.

Completion of one SWU proves only bounded remediation completion for that SWU.
It does not prove Z-Rig product mode.
