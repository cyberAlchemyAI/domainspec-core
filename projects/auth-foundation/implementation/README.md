# Auth Foundation D65 Rust Vertical

This package implements one bounded authorization decision:

> Return `ALLOW` exactly when one uniquely resolved session is current, trusted
> scope evidence and the complete active-role relation are present, and an
> active role grants a permission whose resource, action, and scope exactly
> equal the required permission. Return `DENY` otherwise.

The construction chain is:

```text
accepted Auth definitions
  -> Product Capability
  -> proposed business ontology
  -> DomainSpec v2 authored source
  -> deterministic graph and system ontology
  -> DomainSpec meta-type CLI-generated Rust kernel
  -> exact generated-source binding
  -> local static conformance evidence
```

The Rust crate is a pure decision kernel. Session lookup, role storage, trusted
scope construction, HTTP, tokens, persistence, and audit transport remain
outside this slice. Callers must construct the complete evaluation context.

The property-closed source under `operation-source/` is instantiated by the
standard CLI as `standard-runtime/`. Its receipt binds all 22 record
properties, 15 variants, eight Rules, the selected Operation, and the exact
generated Rust and Cargo manifest. The generated `authorize` function evaluates
the closed Rule internally; callers cannot inject the decision as a Boolean.
Each Rule is a generated Rust predicate with an exact ontology Rule, DomainSpec
selector, and Rust symbol binding.

The earlier bounded `tools/auth-kernel.mjs` output under `runtime/` is retained
as a comparison oracle until the later migration layer. The independent
`standard-conformance/behavior.rs` harness compares the standard candidate with
that oracle across 24 permitted, fail-closed, duplicate, ordering, whitespace,
and combined-failure decision-class cases.
`standard-conformance/receipt.json` reports structural coverage, compilation,
behavioral parity, determinism, and Lean characterization separately.

Build and validate from the repository root:

```bash
PATH=/home/vrondelli/.nvm/versions/node/v22.12.0/bin:$PATH \
  npx --yes tsx@4.20.6 projects/auth-foundation/implementation/scripts/build.ts
python3 projects/auth-foundation/implementation/scripts/validate.py --write-receipt
```

Generated files live under `domainspec/generated/`, `runtime/src/lib.rs`,
`standard-runtime/`, or are named bindings and receipts. Edit the
definition-bound sources, instantiate the standard Operation into a clean
target, rebuild the comparison oracle, and rerun validation. Direct edits to
either generated Rust artifact fail exact observation or generator drift
checks.
