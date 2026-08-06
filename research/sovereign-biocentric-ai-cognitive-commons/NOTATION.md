# Notation Bridge

Target: `Sovereign Biocentric AI and Cognitive Commons`

Status: `pass`

The corpus uses a small amount of mathematical-looking and standards notation.
This bridge separates real technical structures from rhetorical shorthand.
There is no repository-level `research/shared-notation-glossary.md` to link.

## Corpus Symbols

| Symbol | Corpus meaning | Plain-language reading | Boundary | Used in |
| --- | --- | --- | --- | --- |
| `T` | Time of a “Cognitive Act” | A claimed event timestamp | A timestamp does not prove who acted or what happened | Corpus stage S07-S08 |
| `S` | Space of a “Cognitive Act” | A claimed location or context | Exact location can create privacy and safety risk; context need not be geographic | Corpus stage S07-S08 |
| `T/S` | “Chronotopic coordinates” | Time-plus-place context | Metaphor/local term, not a standard provenance primitive | `DEFINITIONS.md` |
| `DID` | Decentralized Identifier | Identifier resolvable under a DID method | A DID can support key-based verification; it does not itself prove real-world identity or authorship | Technical adjudication |
| `VC` | Verifiable Credential | Issuer-signed, tamper-evident claims | Verification authenticates an issuer statement; W3C explicitly says it does not prove claim truth | Technical adjudication |
| `JSON-LD` | Linked-data JSON syntax | Machine-readable claims with shared vocabularies | A placeholder context URL is not an implemented vocabulary | Worked example |
| `h(x)` | Cryptographic digest of bytes `x` | Tamper-evident fingerprint | Integrity is not storage, identity, authorship, ownership, or truth | Local correction |
| `CID` | IPFS Content Identifier | Multiformat content address | A CID includes codec and multihash structure; `"Qm" + truncated SHA-256 hex` is not a valid CID | Technical adjudication |
| `ZKP` | Zero-knowledge proof | Proof of a specified statement without exposing all witness data | It proves only the circuit/relation encoded, not fairness, consent, originality, or non-manipulation | Technical adjudication |
| `ERC-7007` | Ethereum interface for verifiable AI-generated-content NFTs | Can verify a model/input/output relation in configured zkML/opML flows | Does not force arbitrary models to cite or pay a human contributor | Technical adjudication |
| `ERC-7857` | Ethereum interface for AI-agent NFTs with private metadata transfer | Supports ownership/transfer proof mechanics for agent metadata | Does not establish general human cognitive ownership | Technical adjudication |

## Local Structural Notation

The tower replaces the corpus's “eternal ownership” equation with separable
questions:

```text
Contribution record R = (artifact, contributors, context, consent, evidence)
Integrity             I = verify_digest_and_signature(R)
Claim validity        V = verifier_policy(R.claims, R.evidence)
Rights                L = applicable_law_and_agreements(R)
Allocation            A = governed_contribution_process(R)
```

`I` does not imply `V`, `L`, or `A`.

The corpus's rhetorical equation

```text
Data Sovereignty + Friction-by-Will + Biocentric Metrics
  = Sustainable Human Renaissance
```

is an `operator-reading`, not a causal or mathematical result. Its careful
translation is:

```text
privacy control + meaningful override + wellbeing-aware evaluation
  -> candidate design conditions requiring empirical validation
```

## Reading Order

1. Read integrity-versus-truth-versus-rights above.
2. Read DID, VC, CID, ZKP, and ERC boundaries.
3. Read [`DEFINITIONS.md`](DEFINITIONS.md).
4. Read [`tracks/cognitive-act-worked-example.md`](tracks/cognitive-act-worked-example.md).

## Notation Residue

| Symbol | Question | Status | Next route |
| --- | --- | --- | --- |
| `S` | What minimum context can support provenance without precise location? | `open` | Privacy threat model |
| `V` | Which verifier policy can assess originality and contribution? | `open` | Governance design |
| `A` | How should collective value be allocated? | `open` | Community decision plus evidence harness |

