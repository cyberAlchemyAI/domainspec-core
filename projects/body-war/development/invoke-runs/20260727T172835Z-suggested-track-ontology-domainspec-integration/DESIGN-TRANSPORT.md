---
module: body-war-suggested-track-ontology-domainspec-integration
version: current
status: pass
updatedAt: 2026-07-27
docType: invoke-design-transport
---

# Invoke Design Transport

## Inputs

- Approved Define: `SPEC.md`, `GLOSSARY.md`, `DEFINE-TRANSPORT.md`
- Closed scope: `DESIGN-SCOPE-MANIFEST.json`
- Denominator receipt: `DESIGN-DENOMINATOR-RECEIPT.json`
- Selection result: `DESIGN-SELECTION-RESULT.json`

## Validation

- Manifest input digest:
  `ee7a284299683c87453d8215236c1315053d5ba009d78d9a5be4cde34dee40aa`
- Denominator verdict: pass; 10 signals; no diagnostics
- Denominator receipt digest:
  `95e1f4c61e4d608da4182f939a8dd03351ca03f4d2798491dce56e3f5707c643`
- Selection verdict: pass; fixed point true; no diagnostics
- Design selection digest:
  `e88c0c68bb2e5e61945e787ee40d1aec78b4d873c484ac07c97c0c3896d7b64f`
- Evidence state: `design-validator-pass`
- Plan evidence: `plan-evidence-pending`

## Six-View Coverage

- Context: pass
- High-level structure: pass
- Low-level components: pass
- Workflow process: pass
- Decision/state flow: pass
- Dependency/interface: pass

## Preliminary Design Distill

- Coherent unit: one CT-2 three-witness chain
- Split pressure: the ontology and DomainSpec witnesses pass independently,
  while the bridge is meaningful only after both
- Recomposition: standalone receipts are exact inputs to integration
- Verdict: pass for Plan authoring

## Decisions

- Body War local ontology fixtures, not CyberAlchemy ontology mutation.
- Canonical DomainSpec `body.logic`, not duplicated bridge logic.
- Sidecar bridge v1, not a node-logic schema revision.
- Candidate ontology permitted only in an experimental profile with
  `authority_effect: none`.
- Memory repository is the first backend adapter; Postgres parity is deferred.

## Gaps

- GAP-BWOI-001: generalize through existing DomainSpec libraries rather than
  copying Financial Settlement-specific runners.
- GAP-BWOI-002: promoted Body War ontology remains absent and is outside the
  experimental pass claim.
- GAP-BWOI-003: keep the first node graph within currently admitted kinds and
  edges.

## Next Route

Invoke Plan, using the validated architecture as the only normal Plan source.

