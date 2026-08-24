# Technical Claim Adjudication

Status: `pass-for-source-understanding`

Checked: `2026-08-03`

## Corrected Stack

```text
artifact bytes
  -> real digest / content-address construction
  -> storage policy and availability mechanism
  -> issuer-controlled signing key
  -> conforming provenance assertion
  -> verifier trust and claim-validation policy
  -> legal/governance decision about authorship, rights, use, and value
```

Each arrow is a separate mechanism. The corpus collapses them into an “eternal
signature,” which the checked standards do not support.

## Adjudications

### Hash and CID

A SHA-256 digest can make byte changes detectable. An IPFS CID contains
multiformat and codec information and can depend on chunking and DAG layout.
The corpus code prefixes `Qm` to truncated hexadecimal output; CIDv0 instead uses
a complete multihash encoded as base58btc. The example is not a CID.

IPFS content addressing does not guarantee that anyone continues to store or
serve the content. Persistence needs an explicit storage/pinning arrangement.

Sources: [IPFS CID documentation](https://docs.ipfs.tech/concepts/content-addressing/),
[IPFS persistence](https://docs.ipfs.tech/concepts/persistence/), and the
[CID specification](https://github.com/multiformats/cid).

### DID and VC

DIDs can reference verification methods under a DID method. A valid signature
can show control of corresponding key material for an assertion. It does not by
itself prove that the controller is the claimed real-world person.

VC Data Model 2.0 states that credential verification does not imply truth of
encoded claims; a verifier must apply its own policy. The corpus JSON includes
placeholder DID, context, verification method, and JWS values. Its Python never
generates a key or signature. It is not a credential proof.

Sources: [DID Core](https://www.w3.org/TR/did-core/),
[VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/), and
[VC Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/).

### Arweave

Arweave documents an economically incentivized long-term storage model. The
endowment analysis depends on storage-cost and token-economic assumptions, and
operators can apply content policies. Its own legal page says there is no
guaranteed deletion path and warns against placing clear-text personal or
confidential data on the blockweave. “Mathematically guaranteed for hundreds of
years” is therefore blocked.

Sources: [protocol](https://docs.arweave.org/developers/development/protocol) and
[legal policies](https://www.arweave.org/legal-policies).

### ERC-7007 and ERC-7857

Both are Final Standards Track ERCs as checked.

- ERC-7007 defines an ERC-721 extension for verifying configured AI-generated
  content relations involving a model and prompt through zkML/opML flows.
- ERC-7857 defines privacy-preserving ownership/transfer mechanics for AI-agent
  NFT metadata such as models, memory, and character definitions.

Neither standard establishes that a model trained on a particular human datum,
maps a weight update to that contribution, compels citation, or requires
royalties. Those corpus claims are false.

Sources: [ERC-7007](https://eips.ethereum.org/EIPS/eip-7007) and
[ERC-7857](https://eips.ethereum.org/EIPS/eip-7857).

### Zero-Knowledge Proofs

A ZKP can prove a precisely encoded relation without revealing the full witness.
It cannot prove broad properties such as “the system did not manipulate the
person” unless a complete, defensible operational property and observation model
exist—an unsolved requirement in this corpus. Even then, the proof covers the
encoded computation, not unobserved social or psychological effects.

## Runnable Claim Boundary

No live DID, VC, CID, storage, ZKP, smart-contract, model-lineage, or payment
mechanism was implemented or executed. A future implementation must begin from
a threat model and test protocol, not from the placeholder code.

