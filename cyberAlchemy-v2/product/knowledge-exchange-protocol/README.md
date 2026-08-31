# CyberAlchemy Knowledge Exchange Protocol

Status: private candidate product model

This package defines the first bounded product slice for a Solana-oriented
knowledge-sharing protocol. The first proof is deliberately smaller than a
marketplace: one originator adds one recipient as an additional co-owner of one
encrypted knowledge-artifact version, gives that recipient a decryptable key
envelope, and receives a signed acknowledgement bound to the exact artifact
version.

The protocol does not custody plaintext, content-encryption keys, or the
encrypted artifact. The artifact is kept at an external content-addressed
location. A stable Knowledge Identity (`KEP-D3`) authorizes actions with a
signing key and binds a separate encryption public key through an Identity
Encryption-Key Binding (`KEP-D4`).

## Definition Authority

The product-local canonical vocabulary is
[authority/definitions/DEFINITIONS.md](authority/definitions/DEFINITIONS.md),
with lookup entries in
[authority/definitions/DEFINITIONS-INDEX.md](authority/definitions/DEFINITIONS-INDEX.md).
`KEP-D1` through `KEP-D12` own the Knowledge Exchange Protocol's business
meaning. CyberAlchemy-v2 contributes shared construction primitives but does
not own these product-local terms.

## First Product Capability

`CA2-CAP-GRANT-ENCRYPTED-KNOWLEDGE-COOWNERSHIP` makes this outcome possible:

```text
owner set {A}
  + A-authorized co-ownership grant for B
  + immutable artifact-version and policy identities
  + encrypted artifact reference
  + recipient-specific key envelope for B
  + B-signed decryption acknowledgement
  = owner set {A, B} with bounded delivery evidence
```

B may later sign a key-reissue request. Reissuing a key envelope does not add
an owner, remove an owner, change the artifact, or create payment. A lost key
may receive the same content key wrapped to a new encryption key. A compromised
key requires a new encryption epoch and new content key; merely rewrapping the
old content key is insufficient.

## D65 Construction State

The product-local definitions are active definition authority. Every successor
remains separately bounded:

1. `KEP-D1` through `KEP-D12` are canonical product-local definitions;
2. the Product Capability remains a candidate that must bind those definitions;
3. the capability-local business ontology remains an unadmitted candidate; and
4. existing DomainSpec-generated and Rust artifacts are premature candidate
   evidence descended from the earlier unbound model.

The next eligible step is a digest-bound business-ontology admission review.
DomainSpec admission, implementation conformance, Solana realization,
publication, and deployment remain blocked or `not_evaluable`.

## Validate

```bash
python3 cyberAlchemy-v2/product/knowledge-exchange-protocol/validate.py
python3 cyberAlchemy-v2/product/knowledge-exchange-protocol/tests/test_validate.py
```

## Claim Ceiling

A PASS proves only the internal shape, exact external-source currency, graph
closure, shared-schema conformance, and honest D65 stage posture of these
candidate bytes. It does not adopt the capability, prove cryptographic
security, prove recipient decryption, implement a Solana program, authorize a
share, transfer SOL, establish licensing or royalties, publish, release, or
deploy anything.
