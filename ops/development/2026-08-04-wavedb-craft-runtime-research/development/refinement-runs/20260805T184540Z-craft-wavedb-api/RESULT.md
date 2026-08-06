# Refine Result — Craft Consultation API

Status: `complete-with-residue`

## What was produced

The refined target is a private, GET/HEAD-only consultation API over one fully
verified derived WaveDB snapshot. L0 contains status, authorization-filtered
space metadata, and exact raw YAML reads. L1 adds only fixture-validated,
family-scoped 0.3.0 rows. Craft owner ledgers remain the sole source authority;
the snapshot, indexes, rows, and responses always declare `authority: derived`.

Controlling artifacts:

- `API-CONTRACT.md`
- `DATA-MODEL.md`
- `SECURITY-BOUNDARY.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `EXECUTION-PACK.md`

## What the critics changed

All three confirmed read-only critics rejected the initial design. The repair:

- added explicit row actions and authorization-before-observation ordering;
- replaced guessable path-derived IDs with secret-keyed, byte-exact HMAC IDs;
- separated base metadata from path/digest/size permissions;
- fully bound and authenticated space and row cursors;
- fixed error precedence, duplicate/schema behavior, snapshot pinning, freshness,
  and resource ceilings;
- narrowed WaveDB evidence to same-process reopen and expected-key closure;
- distinguished logical from OS-enforced immutability and made runtime anomalies
  invalidate the whole handle;
- kept concurrency, replacement, recovery, and deployment outside L0.

## Plan and current gate

The split Work Pack contains nine atomic SWUs. Its first candidate is
SWU-CAPI-001: a separately launched reader that verifies the existing 55-record
snapshot without product-code changes. This is the narrowest trust-building
step, but it is **not authorized to run**.

`workPackGateStatus = block` and `allowedRoutes = []` because these owner
decisions remain open:

1. approve the proposed private root
   `implementation/domainspec/tools/craft-consultation-api/`;
2. select the authentication principal/session and secret-provider port owners;
3. separately authorize one selected execution SWU.

## Evidence ceiling

The API is designed and planned, not implemented. No OpenAPI/schema code, server,
adapter, fresh-process witness, concurrency/locking proof, OS sealing,
replacement/recovery protocol, deployment, publication, or production evidence
exists. No Craft ledger, WaveDB store/package, implementation tree, or public
Arcanum source was changed by this run.

Next route: `decision-gate`, then a separately authorized Task Session for only
SWU-CAPI-001 if the owner decisions pass.
