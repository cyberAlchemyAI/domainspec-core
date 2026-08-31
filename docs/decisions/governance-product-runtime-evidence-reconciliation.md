# Governance product runtime-evidence reconciliation

Status: decided — proceed
Decision effect: none
Authority effect: none
Decided at: 2026-08-29T21:25:21Z

## Decision question

Should the existing Governance product ontology first reconcile its retired
Arcanum Governance Flow evidence and then add the smallest runnable Governance
Program as candidate runtime evidence?

## Context

The runnable no-effect Rust candidate exists at
`cyberAlchemy-v2/development/examples/smallest-governance-program` and passes
seven semantic tests. Before adding it as product-ontology evidence, the
check-only product validator returned `BLOCK` because the ontology still cites
the removed `arcanum/framework/GOVERNANCE-FLOW-CONTRACT.md` and seven selectors
that no longer exist.

The current `arcanum/framework/README.md` says Governance Flow is disabled. A
read-only defect review found no semantically equivalent replacement for the
old positive runtime evidence. Reconciliation therefore requires product-owner
review rather than a mechanical path repair.

## Considered options

### RECONCILE_THEN_ADD — selected

Reconcile the retired Governance Flow evidence, review or withdraw the affected
relations, then add the Rust candidate, DomainSpec mapping, tests, and no-effect
boundary as candidate evidence.

### DEFER_RECONCILIATION

Keep the runnable candidate separate and leave the Governance product ontology
unchanged. This was admissible but not selected.

### STOP

End the ontology-evidence work without retaining it as a deferred decision. This
was admissible but not selected.

### ADD_ON_RED_BASELINE — rejected before presentation

Adding evidence while leaving the durable ontology validator-blocked was
inadmissible because no append-only PASS receipt could cover the resulting
material and the contradictory positive runtime evidence would remain.

## Decision

- Selected option: `RECONCILE_THEN_ADD`
- Decision source: explicit user correction `It was 1`, resolved against the
  numbered option list presented in the current conversation
- Rationale: the user selected the recommended reconciliation-and-add path; no
  additional motivation is inferred
- Consequential continuation: proceed with the bounded candidate ontology
  reconciliation and evidence addition requested in this conversation
- Runtime candidate changes: none expected
- Promotion, authority, adoption, enforcement, publication, and deployment
  effects: none

## Correction history

The assistant initially interpreted the user's reply as option 2 and recorded
`DEFER_RECONCILIATION`. The user immediately corrected that interpretation to
option 1. This record now preserves the correction and the selected option; the
superseded deferral was never applied to Governance ontology bytes.

## Selected reconciliation scope

- retire the missing Governance Flow contract source and its stale selectors;
- record the current disabled Flow state as counterevidence;
- withdraw the three relations whose only evidence was the retired contract;
- add the runnable Rust candidate and DomainSpec mapping as candidate evidence
  for existing product meanings;
- update the runtime evidence residue without claiming runtime acceptance; and
- require complete package validation before appending a new receipt.

This record documents the selection. It is not an authority grant, promotion,
adoption, enforcement binding, or standing authorization for later work.

## Evidence

- Admissibility receipt:
  `docs/decisions/governance-product-runtime-evidence-reconciliation.admissibility.json`
- Request digest:
  `428257f3ca5a4f778211c045a50e068b287b8006c477f344b437a9f2b5e05184`
- Baseline package digest:
  `36f9194b7ae5db12f63a0f85d3c5b395ed3a2933ad1c8ff49756699118a04c01`
- Failing check:
  `python3 cyberAlchemy-v2/ontology/governance/product/scripts/validate.py`
