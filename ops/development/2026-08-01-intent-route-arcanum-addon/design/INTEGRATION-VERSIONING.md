# Integration and versioning

## Protocol binding

- request: `intent-route.request@1`
- disposition: `intent-route.disposition@1`
- runtime port: `intent-route.runtime-port@1`
- error/public-check/acceptance case/summary schemas: closed by the accepted
  acceptance addendum
- catalog and closure: lowercase SHA-256 content digests

Unsupported versions and digest mismatches fail closed. A new protocol major
requires a new Define/Design decision, parallel fixtures, and explicit
consumer migration; wrappers cannot negotiate semantics independently.

## Generated parity

Codex and Claude packages must contain byte-identical core, manifest, schemas,
fixtures, executable support closure, and closure digest. Only generated
provenance and the declared Claude tool-token normalization may differ, and
those differences must not change behavior.

## Consumer seams

- Claude/Codex: generated wrapper invokes the same local JSON entrypoint.
- Augmentor/other runtime: source adapter projects local capture or rejects.
- orchestrator: thin process adapter occurs before `_workflow_envelope()`;
  `RuntimeService.bind_host_workflow_turn()` remains the binding/launch owner.
- private CAV2: optional compatibility mapper is private and admitted later.

## Rollback

Install tests use isolated temporary roots, pre-install closure hashes, disable
cases, induced failure, and exact durable restoration. A rollback digest
mismatch blocks consumer admission.

