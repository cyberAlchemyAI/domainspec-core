# RCE-000 Strict Context Pack

## Objective

Explain the existing two contract families without changing consultation response behavior, and give the live evidence-statement shape an explicit identity.

## Controlling evidence

- Work Pack SHA-256: `fbefd2379a649b76fdc33ae2d1cc67081412e9e194e4fab684bb20ecff182a0e`.
- Task contract SHA-256: `693ac8b0d21fff185a754d2c549e075b6fb9c6b4d1766da25c54afdb5529b66a`.
- Existing ResonantOS contract SHA-256: `476014a7540b62e84a5d6ac8560260bb5f133fbe8b391bf2a8d68ec3135db5c1`.
- Existing neutral compiler SHA-256: `970935086c050c065b0231aa92fa2f47109a73e20635776aa940cddbbf1c3e7d`.
- Existing generated projection content digest: `235af912339c8fae0c21f21e1ace40eab37d5141bd3e9d37365497f016937e49`.

## Exact material writes

- `projects/augmentor/ontology/unified-agent/development/consultation-api/schemas/README.md` (new)
- `projects/augmentor/ontology/unified-agent/development/consultation-api/schemas/contract-families.json` (new)
- `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/contract-version-matrix.test.mjs` (new)
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-contract.mjs` (one exported identity)

## Acceptance-critical validation

- Contract-family matrix test passes under Node `22.13.0`.
- Current DomainSpec consultation suite remains passing.
- Current targeted ResonantOS consultation suite remains passing.
- Generated consumer projection bytes remain unchanged.

## Closeout and successor

- Terminal receipt: `implementation/receipts/RCE-000.json`.
- Closeout is receipt-backed local evidence only; no canonical plan status is mutated.
- Unique successor on pass: `SWU-RCE-001`.
