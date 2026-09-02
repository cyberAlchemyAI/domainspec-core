# Continuous Construction Governance Program

This package is a candidate-only, no-effect implementation of `CAV2-C19` over
the active `CAV2-D65` construction order. It evaluates one owner-authorized,
bounded construction attempt and emits exactly one decision:

- `CONTINUE` when the next eligible local stage may proceed inside the existing
  authorization envelope;
- `STOP` when a predecessor, owner gate, scope, packet, or authority condition
  fails closed;
- `READY_FOR_HUMAN_TEST` when all applicable D65 stages validate and one exact
  frozen input packet is ready for its human procedure with no observation yet;
  or
- `REQUEST_TERMINAL_CONFIRMATION` only after a separate immutable passing
  observation binds that same packet ref and digest.

Routine confirmation is never required before the terminal request. A stop may
carry a blocker request or authority request, but those are not routine
confirmation. Every result has `authority_effect: none` and
`effect_authorized: false`; the program performs no stage transition or effect.

## Governed admission

- Classification: governed, `candidate-not-admitted`.
- Initiating intent: `CAV2-C19`, continuous eligible D65 construction followed
  by one exact human test and terminal confirmation request.
- Non-collapse boundary: `dependency-kernel/` cannot absorb this package. It
  owns selector-level dependency relevance, while this package owns a distinct
  Product Capability and business meaning for ordered construction continuity,
  exact authorization/stage/gate evidence, and terminal human-test separation.
- Narrowest owning surface: this package, under the Governance parent
  entrypoint [`../README.md`](../README.md).
- Source boundary: exact selected `CAV2-C19`, `CAV2-D65`, and `CAV2-D67`
  sections plus Governance Product record set
  `GCC-SEL-GOVERNANCE-PRODUCT-RECORDS`: `GOV-PRODUCT-MODULE`,
  `GOV-ACTOR-WORK-OWNER`, `GOV-ACTOR-VALIDATOR-ENFORCER`,
  `GOV-CAP-ASSESS-RULE-FITNESS`, `GOV-CAP-ENFORCE-ACTIVE-RULES`,
  `GOV-OUTPUT-GOVERNANCE-ASSESSMENT`, `GOV-OUTPUT-ENFORCEMENT-RESULT`,
  `GOV-RULE-GOVERNANCE-SERVES-WORK`, `GOV-RULE-AUTHORITY-BOUNDED-VISIBLE`,
  `GOV-RULE-NON-COLLAPSE`, and `GOV-RULE-RUNNABLE-GOVERNANCE`.
- Canonical posture: non-canonical candidate implementation package. Its
  Product Capability, business ontology, DomainSpec profile/system ontology,
  Rust baseline, and evidence are not adopted, admitted, or accepted.
- Validation and evidence: `scripts/validate.ts`,
  `domainspec/generated/system-ontology-receipt.json`, and
  `evidence/conformance-candidate.json`.
- Current residue: C19/capability adoption, DomainSpec profile and system
  ontology admission, independent Rust baseline acceptance, conformance, and
  route activation remain unresolved.
- Next owner and challenge route: CyberAlchemy v2 governance-model owner; route
  semantic challenges through the Constitution, definitions, Governance
  Product, DomainSpec, implementation, or exact terminal-decision owner named
  by the challenged binding.

The evaluator verifies exact attributed authorization bytes, their raw-byte
digest, closed record shape, and attempt-envelope cross-bindings. It does not
authenticate the human principal, verify signatures or credentials, or prove
that the attributed principal possessed external authority. Candidate bytes
cannot manufacture owner authority.

## D65 construction order

The package keeps these layers separate:

1. current canonical definitions (`CAV2-D65`, `CAV2-D67`) and the selected
   candidate Constitution rule (`CAV2-C19`);
2. candidate Product Capability and capability-local business ontology;
3. candidate DomainSpec v2 authored source;
4. deterministic compiled graph and system-ontology read models;
5. exact candidate Rust implementation binding; and
6. candidate behavior evidence whose conformance claim remains
   `not_evaluable` until the owner-controlled predecessors are admitted.

## Runtime

From `runtime/`:

```text
cargo test --locked
cargo run --quiet --locked -- validate-program \
  --program ../programs/continuous-construction.program.json \
  --repository-root ../../../../..
cargo run --quiet --locked -- evaluate \
  --program ../programs/continuous-construction.program.json \
  --attempt ../examples/attempts/continue.json \
  --repository-root ../../../../..
```

Every authorization, validated stage, and bound owner gate is resolved through
a repository-contained ref and verified against its raw-byte digest. The CLI
only prints a deterministic evaluation. It does not edit the
repository, accept an owner gate, run the human procedure, request a decision
from a person, or map the decision to an external effect.

## Claim boundary

The Product Capability, business ontology, development profile, generated
system ontology, Rust baseline, fixtures, construction binding, and evidence
are candidates. Nothing here adopts C19, admits DomainSpec or an ontology,
accepts an implementation, proves conformance, activates routing, or authorizes
publication, release, deployment, or another external effect.

Exact authorization-byte verification is integrity and attribution evidence,
not human identity or authenticity proof and not an owner decision.
