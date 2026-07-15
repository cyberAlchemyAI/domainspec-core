---
task_id: TASK-FPR-02-SUPPORTED-PROFILE
owner_node: FPR-02
layer: L1
status: blocked
---

# TASK-FPR-02-SUPPORTED-PROFILE

## Objective

Freeze one machine-readable product/profile/pilot boundary whose admitted and exercised sets, claims, failures, roots, obligations, origin, redaction, rollback, and owner roles are exact and digest-bound.

## Dependency

Verified `authority-baseline-ratification.json` from FPR-01.

## SWU-FPR02-001: Profile Decision Envelope

- Source anchors: FPR-01 receipt; accepted product decision; Body War bounded witness; `GAP-SH-UI11-MIGRATE`; `EGI-003/007/008/012`.
- Write scope: FPR-02 decision artifact under `development/first-production-release/decisions/` only.
- Done criteria: decide literal admitted backend node types, relationship signatures, required documents, obligations, exercised subsets, excluded/deferred UI formation, source roots, callback/origin route, allowed redacted fields, claims, rollback, and accountable roles.
- Acceptance evidence: Decision Gate artifact with no placeholder owner and no unresolved origin/redaction field.
- Validation: every FPR-02 required field has one owner and disposition; admitted/exercised/deferred are disjoint and trace to FPR-01 IDs.
- Owner: claim and semantic owners through Decision Gate.
- Handoff: no schema authoring before acceptance.

## SWU-FPR02-002: Machine Contract and Stable Digest

- Dependencies: FPR02-001.
- Write scope:
  - `product-contract.yml` and schema
  - `supported-profile.yml` and schema
  - `pilot/body-war-scenario.yml`
  - `pilot/claim-matrix.yml`, `negative-matrix.yml`, `rollback-matrix.yml`, `allowed-redacted-fields.yml`
  - `tools/validate-supported-profile.cjs`
  - `evidence/profile-digest.json`
- Done criteria: one validator consumes all artifacts, rejects undeclared inputs, and emits one normalized stable digest bound to the FPR-01 baseline.
- Acceptance evidence: schema-valid artifacts and two-run digest equality.
- Validation: planned validator command from `EXECUTION-PACK.md`; JSON/YAML parse; exact input-set check.
- Owner: profile/validation owner.
- Handoff: pass validator and digest to FPR02-003.

## SWU-FPR02-003: Fail-Closed Negative Matrix

- Dependencies: FPR02-002.
- Write scope: `development/first-production-release/fixtures/supported-profile/` and FPR-02 evidence/receipt only.
- Done criteria: empty profile, empty content, unknown type, absent schema/root, formation-deferred type, legacy source path, placeholder owner, missing obligation kind, unresolved origin, and empty redaction allowlist each fail with a distinct stable code; positive profile remains green.
- Acceptance evidence: matrix mapping every negative to command, expected code, actual code, and killed status.
- Validation: run all fixtures twice; no zero-exit false green; digest stays stable after negative runs.
- Owner: independent validation owner.
- Handoff: verified profile digest and matrix open FPR-03.

## Synchronization

FPR-02 freezes a bounded backend profile, not the whole DomainSpec language. Any breadth claim beyond admitted/exercised sets blocks closeout.

