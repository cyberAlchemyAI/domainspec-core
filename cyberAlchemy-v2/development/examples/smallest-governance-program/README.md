# Smallest Governance Program

This is a runnable, no-effect candidate showing the smallest complete
Governance evaluation:

```text
Governance Program + Governance Request + Governance Fact Set
                              |
                              v
                    pure evaluate calculation
                              |
                              v
                 allow | deny | abstain | error
```

The example asks whether a synthetic agent may publish a synthetic document.
The Program itself is immutable Rust data. It declares the exact request it
matches and requires:

1. an exact rule adopted into an exact Constitution;
2. that rule to apply to this request;
3. an exact active enforcement binding; and
4. both repository and publication authority to permit the consequence.

The evaluator interprets those clauses. It does not contain a special-case
publication decision.

Its result precedence is explicit and independent of clause order:

1. invalid Program or Facts produce `error`;
2. missing or false adoption, applicability, or binding produces `abstain`;
3. otherwise any explicit authority forbid produces `deny`;
4. otherwise missing authority produces `abstain`; and
5. otherwise every clause is satisfied and the result is `allow`.

## Run it

From the repository root:

```bash
cargo run --manifest-path cyberAlchemy-v2/development/examples/smallest-governance-program/Cargo.toml
```

The default case intentionally omits the binding fact, so it prints
`verdict=abstain`. This is the safe documented example: missing governance
authority is neither permission nor a prohibition.

Run every outcome:

```bash
cargo run --manifest-path cyberAlchemy-v2/development/examples/smallest-governance-program/Cargo.toml -- allow
cargo run --manifest-path cyberAlchemy-v2/development/examples/smallest-governance-program/Cargo.toml -- deny
cargo run --manifest-path cyberAlchemy-v2/development/examples/smallest-governance-program/Cargo.toml -- abstain
cargo run --manifest-path cyberAlchemy-v2/development/examples/smallest-governance-program/Cargo.toml -- error
```

Run the tests:

```bash
cargo test --manifest-path cyberAlchemy-v2/development/examples/smallest-governance-program/Cargo.toml
```

## What each result means here

- `allow`: every declared synthetic fact is present and each required authority
  layer permits the request.
- `deny`: a required authority layer explicitly forbids the request.
- `abstain`: the request is outside the Program or adoption, applicability,
  binding, or authority is not established.
- `error`: malformed, undeclared, duplicate, or conflicting facts make the
  evaluation unreliable.

Every fact names a scope, source, and verifier. These strings are visibly
synthetic and prove no real adoption or authority.

## Boundary

This crate hashes nothing, reads no repository state, changes no lifecycle,
enforces no rule, invokes no integration, and performs no requested effect. Its
`EffectCeiling` has only `NoEffect`; there is intentionally no enforce variant.

This proves only that one candidate Rust representation can be interpreted
deterministically. It is not the accepted Governance runtime, a portable policy
language, a canonical DomainSpec binding, a Constitution, an authority grant,
or permission to publish anything.

See [DOMAIN-MODEL.md](DOMAIN-MODEL.md) for the DomainSpec v2 meta-type mapping.
