# Invoke Refresh Context Pack — SWU-BWAA-001 Material Admission

- Mode: `standard`, strict
- Activation: `direct-user`
- Mutation mode: `apply-approved` by direct-user default
- Target: `SWU-BWAA-001`
- Scope: exactly three staged product outputs
- Authority: private, candidate-local
- Strict coverage: `pass`

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Preserve the frozen five-SWU frontier and select only 001 | `WORK-PACK.md#Ordered-SWU-Manifest`; blocked chain handoff | covered |
| O2 | Materialize the exact directed lens-flow algorithm | `TASK-BWAA-001.md#Implementation-Detail`; projection contract in `ARCHITECTURE.md` | covered |
| O3 | Touch only the declared three paths | task Write Scope; `TARGET-INVENTORY.json` | covered |
| O4 | Prove 13 ordered flows partition all 109 portals | task Acceptance; staged tests and validator | covered |
| O5 | Preserve 237/231/122/109/44 and semantic locks | Work Pack Semantic Locks; staged overlay validation | covered |
| O6 | Bind approval, owner, publication, and dependency evidence | direct request; material package schema; owner contract | covered |
| O7 | Supply the producer receipt/schema inputs Task Session 1.2 requires | material package, material receipt, receipt schema | covered by this Refresh output |
| O8 | Define closeout expectations before live mutation | `CLOSEOUT-OWNER-CONTRACT.json`; shared Execution Control | covered |
| O9 | Preserve authority and release ceilings | Work Pack and current ontology boundary | covered |

## Selected context

- `WORK-PACK.md#Ordered-SWU-Manifest,#Semantic-Locks,#Execution-Handoff`
  — sequence, locks, and Task Session boundary.
- `work-pack/tasks/TASK-BWAA-001.md#Primary-Behavior,#Implementation-Detail,#Acceptance,#Validation`
  — exact implementation and evidence contract.
- `work-pack/shared/EXECUTION-CONTROL.md#Selection-And-Preflight,#Terminal-Receipt-Contract`
  — mutation and closeout rules.
- `SPEC.md#Acceptance-Contracts`
  — product-facing lens-flow acceptance.
- `ARCHITECTURE.md#Projection-Contract`
  — pure projection boundary.
- `work-pack/session-evidence/20260730T085748Z-bwaa-all-until-blocker/CONTINUATION-HANDOFF.json`
  — stable blocker fingerprint and exact continuation.
- `work-pack/session-evidence/20260730T085748Z-bwaa-all-until-blocker/SWU-BWAA-001-MUTATION-ADMISSION-RECEIPT.json`
  — canonical proof that the producer material trio was missing.
- Current projection, coverage validator, and projection test files
  — exact preimages and integration seams.
- `.agents/skills/invoke/schemas/material-package*.json`
  — producer package and receipt contracts.
- `.agents/skills/task-session/schemas/mutation-admission-*.json`
  — downstream admission boundary.

## Execution contract

The Refresh owner may author and validate staged outputs and handoff artifacts.
It must not replace the live three target files. Task Session owns the later
live mutation, validation, terminal receipt, and successor decision.

The three approved target paths are:

1. `projects/body-war/ontology/business/scripts/view-atlas-projection.mjs`
2. `projects/body-war/ontology/business/scripts/validate-view-atlas.mjs`
3. `projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs`

No ontology nodes, relations, lifecycle policies, renderer, generated HTML,
browser artifacts, app files, or successor-SWU targets are admitted.

## Validation surface

```text
node --test projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs
node projects/body-war/ontology/business/scripts/validate-view-atlas.mjs
git diff --check -- projects/body-war/ontology/business/scripts/view-atlas-projection.mjs projects/body-war/ontology/business/scripts/validate-view-atlas.mjs projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs
```

## Residue

- This pack proves staged SWU-001 material only.
- It does not execute Task Session, mutate live product bytes, complete
  SWU-001, unlock SWU-002, or grant promotion/release authority.
