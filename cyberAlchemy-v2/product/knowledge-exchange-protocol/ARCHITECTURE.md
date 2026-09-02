# CyberAlchemy Knowledge Exchange Protocol Architecture

Status: private architecture guide

Snapshot date: 2026-09-01

Product: `CA2-PRODUCT-KNOWLEDGE-EXCHANGE-PROTOCOL`

Current target capability: `CA2-CAP-REALIZE-ENCRYPTED-DURABLE-DEVNET-COOWNERSHIP`

Authority effect: none

This document explains what the CyberAlchemy Knowledge Exchange Protocol is,
how it is being constructed, which architectural responsibilities belong to
which subsystem, what has actually been proved, and what remains before a real
Solana Devnet trial.

It is an explanatory view of exact repository artifacts. It does not replace
canonical definitions, adopt an ontology, admit DomainSpec source, prove an
implementation, authorize credentials, submit a transaction, or deploy a
program. Where the target architecture is ahead of the current implementation,
that distinction is explicit.

## 1. Executive Summary

We are building a protocol for sharing an exact version of encrypted knowledge
between stable identities while preserving provenance, confidentiality, and
the originator's continuing co-ownership.

The first complete protocol proof is intentionally smaller than a marketplace:

```text
one exact artifact version
  + one original owner A
  + one intended recipient B
  + encrypted durable bytes
  + an A-authorized Solana state transition
  + finalized chain/storage reconciliation
  + B's successful retrieval and decryption
  + a bounded key-reissue path
  = evidence that {A} became {A, B} without removing A or pricing the knowledge
```

The blockchain does not hold the knowledge. It holds the minimum public state
needed to coordinate identity, co-owner membership, commitments, revisions,
and replay protection. Encrypted artifact bytes and recipient-specific key
envelopes remain off-chain in governed Durable Storage.

The immediate product boundary is **no-price knowledge sharing**. Solana fees,
account rent, RPC costs, SQL storage, and archive costs are infrastructure
costs. They are not payment for knowledge. Licensing, royalties, resale,
economic reputation, and other market mechanisms are later product layers.

The construction method is the CyberAlchemy-v2 `CAV2-D65` invariant:

```text
canonical definitions
  -> adopted Product Capability
  -> admitted capability-local business ontology
  -> admitted DomainSpec v2 source
  -> admitted compiled graph and system ontology
  -> exact implementation binding
  -> accepted conformance evidence
  -> separately authorized runtime trial
```

Each arrow is a gate. A generated file, passing validator, or language-model
draft cannot promote itself across a gate.

## 2. Product Thesis

Knowledge is easy to copy but difficult to share with durable evidence about:

- which exact artifact version was shared;
- who originated it;
- who was authorized to propagate it;
- whether the originator remained an owner;
- which recipient was given access;
- whether the recipient obtained decryptable material;
- which rules and encryption epoch applied;
- whether a command was replayed;
- how key replacement affected access without changing ownership; and
- which later economic rules, if any, are allowed.

The protocol separates these concerns instead of collapsing them into one NFT,
wallet, database row, or ciphertext locator.

The product thesis is maintained in [PRODUCT-THESIS.md](PRODUCT-THESIS.md).
The core idea can be read as a sequence of preserved facts:

```text
A originates version V under policy P
  -> V is encrypted under encryption epoch E
  -> A authorizes B as an additional co-owner
  -> A remains an owner
  -> B receives a recipient-specific envelope
  -> B can retrieve and decrypt V
  -> later key replacement changes B's access material, not V or its owner set
```

### 2.1 What ownership means here

Protocol co-ownership is a governed membership relation for one exact artifact
version. It is not automatically copyright, legal title, an exclusive right,
or proof that the recipient still possesses plaintext.

The first state transition is:

```text
before: owners(V) = {A}
after:  owners(V) = {A, B}
```

It is not:

```text
before: owner(V) = A
after:  owner(V) = B
```

### 2.2 Why the originator remains present

Knowledge cannot be made unlearned after delivery. A transfer model that
pretends the originator no longer has the knowledge would be false. The first
protocol therefore models expansion of recognized co-ownership, not exclusive
physical transfer.

### 2.3 Product evolution

The intended product evolution is:

```text
Phase 1: no-price encrypted co-ownership proof
  -> Phase 2: optional SOL-denominated consideration
  -> Phase 3: licensing and user-right policies
  -> Phase 4: royalties and downstream propagation economics
  -> Phase 5: evidence-bound economic reputation
```

Only Phase 1 is in the current target capability. Later phases must extend the
definitions and product ontology rather than smuggling economics into network
fees or existing fields.

## 3. System Context

The target system has six runtime participants and one construction/governance
substrate:

```text
                         CyberAlchemy-v2 governance
                     definitions -> D65 -> exact decisions
                                      |
                                      v
+-------------+    signed intent    +---------------------+
| A client /  | ------------------> | Solana program      |
| originator  |                     | public commitments  |
+------+------+                     | owners/revision/     |
       |                            | replay state         |
       | encrypted bytes            +----------+----------+
       v                                       |
+-------------+       observe finalized state  |
| Off-chain   | <------------------------------+
| orchestrator|
+------+------+       write/read/verify
       |        +-------------------------------+
       v        v
+-------------+   +------------------+   +------------------+
| Crypto      |   | Operational SQL  |   | Recovery journal |
| profile     |   | registry         |   | append-only      |
+-------------+   +------------------+   +------------------+
       |                    \                 /
       |                     \               /
       |                      v             v
       |                  +--------------------+
       +----------------> | Immutable archive  |
                          | SQL-independent    |
                          +---------+----------+
                                    |
                                    v
                              +-----------+
                              | B client  |
                              | recipient |
                              +-----------+
```

The diagram is conceptual. There is no deployed Solana program or complete
successor orchestrator yet.

## 4. Responsibility Boundaries

### 4.1 CyberAlchemy-v2

CyberAlchemy-v2 owns product meaning, authority, lifecycle decisions, exact
predecessor selection, and the D65 construction invariant. It answers:

- What outcome are we trying to create?
- Which terms and boundaries are canonical?
- Who may adopt or admit each stage?
- Which exact digest was accepted?
- What remains not evaluable?

It does not manufacture runtime truth from documentation or validation.

### 4.2 DomainSpec v2

DomainSpec v2 turns admitted product meaning into authored system intent. It
describes nodes, relations, operations, rules, policies, mappings, state
machines, contracts, events, and proof obligations.

DomainSpec v2 is not the Solana program and is not a storage adapter. Its
compiled graph and system ontology form the exact semantic predecessor that an
implementation must bind to.

### 4.3 Rust

Rust is the implementation language selected for the current local model and
the intended protocol clients/program components. Rust realizes exact system
ontology obligations; it does not define product ownership or silently choose
new business rules.

The current Rust crate implements a pure local state-transition model. Its
binding explicitly says:

```text
cryptography: opaque caller-produced digests and caller-owned verifier
ciphertext custody: none
durable storage: none
Solana binding: not present
economic effect: none
```

### 4.4 Solana

Solana is the first public coordination substrate. Its responsibility is the
atomic public transition and its replay-safe evidence, not knowledge custody.

The intended on-chain state includes semantic equivalents of:

- exact artifact-version identity;
- stable Knowledge Identity references or their governed mappings;
- co-owner membership;
- propagation-policy identity;
- encryption-epoch identity;
- active recipient-envelope commitments;
- state revision;
- consumed replay identities; and
- environment and program identity needed to interpret evidence.

Concrete account layout, PDA seeds, instruction encoding, upgrade authority,
program ID, and deployment values remain later DomainSpec and implementation
bindings. They are not selected by the Product Capability itself.

### 4.5 Durable Storage

Durable Storage owns provider-neutral persistence, retrieval, verification,
typed failure, migration, recovery, and replacement behavior for immutable
encrypted objects.

The Solana capability is a consumer. It fills the generic storage contract with
its artifact and envelope object kinds, but it does not redefine storage or
select a provider.

### 4.6 The language model

The language model is a construction partner. It can:

- draft definitions, ontology records, DomainSpec source, documentation, code,
  tests, validators, and evidence candidates;
- inspect exact source relationships and expose contradictions;
- generate architecture explanations and failure scenarios;
- maintain digest-bound dependency records; and
- propose the next bounded gate.

It cannot:

- make its own draft canonical;
- infer owner acceptance from a passing test;
- refresh a digest to manufacture admission;
- claim cryptographic security without the required evidence;
- create credentials or submit transactions without exact authorization; or
- turn a Devnet observation into Mainnet or product-value proof.

## 5. Core Domain Model

### 5.1 Knowledge Artifact and Knowledge Artifact Version

A Knowledge Artifact is the enduring conceptual work. A Knowledge Artifact
Version is the immutable protocol subject. Policy, plaintext commitment,
originator, and encryption state are interpreted against the exact version.

Changing material meaning or immutable policy creates a successor version.

### 5.2 Knowledge Identity

A Knowledge Identity is a stable participant identity. It is not a Solana
wallet address and is not an encryption key.

```text
Knowledge Identity
  -> may bind one or more Solana signing keys over time
  -> may bind one or more encryption public keys over time
  -> remains the participant identity when keys are replaced
```

### 5.3 Signing-key binding

A signing-key binding connects a stable identity to authority for a specific
protocol action. The Solana program must validate the current binding and the
action's exact policy scope.

### 5.4 Encryption-key binding

An encryption-key binding connects a stable recipient identity to a current
recipient encryption public key. It is versioned and has an explicit validity
boundary. It must never be inferred from a wallet key.

### 5.5 Propagation Policy

The Propagation Policy determines who may add a co-owner and who may fulfill a
recipient's reissue request. It is bound to an exact artifact version.

The first Devnet target uses A as the reissue fulfiller only when A is
authorized by the exact policy and current signing-key binding. This does not
make A universally authoritative.

### 5.6 Encryption Epoch

An Encryption Epoch identifies the content-encryption state shared by one
artifact version and all compatible recipient envelopes.

- Lost, non-compromised recipient key: wrap the same content key to a new
  recipient binding within the same epoch.
- Suspected compromise: create a successor epoch, new content key, new
  ciphertext, and replacement envelopes for every current owner.

### 5.7 Recipient Key Envelope

A Recipient Key Envelope is encrypted material that lets one recipient recover
the content key. Every envelope binds at least:

- artifact version;
- encryption epoch;
- recipient Knowledge Identity;
- recipient encryption-key binding;
- cryptographic profile;
- policy context; and
- envelope revision.

The chain stores a commitment to the envelope, not its plaintext or private
key.

### 5.8 Co-owner membership

Membership records that an identity belongs to the owner set for one artifact
version. Membership and decryptable access are related but distinct:

```text
membership without a valid envelope -> recognized owner with unavailable access
valid envelope without membership   -> invalid protocol state
membership + valid envelope         -> recognized owner with prepared access
finalized activation + retrieval    -> active deliverable access
```

### 5.9 Replay identity and state revision

Every grant, acknowledgement, request, and fulfillment is bound to an expected
state revision and a fresh command or replay identity. A successful transition
advances the revision and consumes the replay identity atomically. Stale or
replayed commands fail without partial state mutation.

## 6. Cryptographic Architecture

The first Devnet target binds the candidate test-only profile
[`KEP-SOL-CRYPTO-DEVNET-V1`](capabilities/solana-coownership/successors/encrypted-durable-devnet/v1/cryptographic-profile.json).

### 6.1 Content encryption

```text
construction: XChaCha20-Poly1305-IETF
key:          32 random bytes per Encryption Epoch
nonce:        24 cryptographically random bytes per encryption
tag:          16 bytes
```

Associated data binds the profile, artifact version, encryption epoch,
plaintext commitment, and propagation policy. Authentication must complete
before any plaintext is returned.

### 6.2 Recipient envelope

The recipient envelope uses RFC 9180 HPKE Base mode with:

```text
KEM:  DHKEM(X25519, HKDF-SHA256)  0x0020
KDF:  HKDF-SHA256                 0x0001
AEAD: ChaCha20Poly1305            0x0003
```

HPKE Base mode does not authenticate the sender. Sender authorization is a
separate protocol concern established through the Knowledge Identity,
signing-key binding, Solana signature, program checks, and Propagation Policy.

### 6.3 Commitments and encoding

- Stored-object and plaintext-content commitments use SHA-256 with different
  domain separators.
- Ciphertext and envelope headers use CBOR under RFC 8949 core deterministic
  encoding requirements.
- Indefinite lengths and floating-point values are forbidden in the selected
  profile.
- Unknown fields are rejected unless a successor profile defines compatible
  handling.
- Randomness must come from an operating-system cryptographically secure random
  generator through an exact implementation binding.

### 6.4 Security claim ceiling

Selecting algorithms is not a security proof. The current profile still needs:

- exact Rust library and version binding;
- known-answer vectors;
- negative and malformed-input vectors;
- fuzzing;
- side-channel and zeroization review;
- dependency and supply-chain review;
- key-custody design; and
- independent security review.

The profile is suitable only as a concrete target for the first controlled
Devnet experiment.

## 7. Durable Storage Architecture

The target instantiation is
[`KEP-SOL-DST-INSTANTIATION-DEVNET-V1`](capabilities/solana-coownership/successors/encrypted-durable-devnet/v1/durable-storage-instantiation.json).

It composes two adopted storage capabilities from published Git object
`1b629e601`:

1. provider-neutral persistence and verified retrieval; and
2. SQL-portable three-layer protection and verified restoration.

### 7.1 Stored object kinds

The Solana consumer specializes the storage port for:

- encrypted artifact bytes; and
- recipient-envelope ciphertext bytes.

Both objects have qualified identities. Identity includes the exact bytes,
cryptographic profile, and required context; it does not include a provider
name, mutable locator, SQL dialect, or deployment region.

### 7.2 Three protection layers

```text
Layer 1: operational SQL registry
  -> current object identity and locator metadata

Layer 2: append-only recovery journal
  -> immutable recovery events for the same operation and object identity

Layer 3: SQL-independent immutable archive
  -> exact object bytes retrievable without the operational SQL realization
```

All three layers must close on the same qualified object identity.

The existing bounded reference realization uses PostgreSQL as the first SQL
adapter and a filesystem content-addressed archive. The core is expressed as
behavioral ports—`OperationalSqlLayer`, `RecoveryJournalLayer`, and
`ImmutableArchiveLayer`—so another SQL adapter may conform without changing
product meaning.

### 7.3 Readiness before Solana submission

Before the client constructs, signs, or submits a grant or reissue fulfillment:

```text
write operational record
  -> append recovery-journal event
  -> write immutable archive object
  -> retrieve and verify operational bytes
  -> retrieve and verify archive bytes
  -> verify artifact/epoch/recipient/key/profile/policy context
  -> storage-ready
```

If any obligation fails:

```text
storage-not-ready
  -> do not construct transaction
  -> do not sign transaction
  -> do not submit transaction
```

### 7.4 Recovery

A copy, journal replay, SQL import, database start, or successful query is not
restoration proof. Restoration succeeds only when the object is reconstructed
into a clean conforming SQL realization, retrieved from that destination, and
verified against its qualified identity.

### 7.5 Failure-domain boundary

The local Docker/PostgreSQL evidence proves three-layer mechanism behavior. It
does not prove three independent production infrastructure failure domains.
Production topology, regions, credentials, retention, RPO, RTO, provider, and
availability objectives remain unselected.

## 8. Solana State and Program Architecture

The admitted no-price Solana business ontology and DomainSpec source describe
the semantic substrate for a future program. The generated system ontology
contains 26 system nodes, including:

- Knowledge Exchange Protocol interface;
- Knowledge Identity and Solana signing-key binding;
- Knowledge Artifact Version and Solana artifact-state aggregate;
- Co-owner membership;
- recipient-envelope commitment;
- Propagation Policy and execution-environment policy;
- grant input and evidence contracts;
- replay domain and consumption record;
- no-price boundary and network cost;
- grant operation;
- completed and rejected events; and
- co-ownership state machine.

These nodes are system intent, not deployed accounts.

### 8.1 Conceptual artifact state

The intended aggregate can be represented as:

```text
ArtifactState {
  artifact_version_id
  policy_id
  encryption_epoch_id
  owners[]
  active_envelope_commitment_by_owner{}
  state_revision
  replay_domain
  consumed_grants{}
}
```

The final account structure must be chosen later against Solana constraints,
rent, maximum growth, serialization stability, migration, and upgrade policy.

### 8.2 Grant transition

Conceptually:

```text
Grant(S, command, A, B, envelope_commitment) -> S'
```

The transition is valid only when:

- `S` names the expected artifact version, policy, epoch, and revision;
- A is a current owner;
- A's current signing-key binding authorizes the exact command;
- the Propagation Policy authorizes A to grant;
- B is the intended stable identity;
- B's encryption-key binding is current;
- the envelope commitment matches durably prepared material;
- B is not already an owner;
- the replay identity is fresh; and
- no knowledge consideration is present.

On success:

```text
owners' = owners union {B}
A remains in owners'
B envelope commitment becomes active at the expected activation boundary
state_revision' = state_revision + 1
replay identity becomes consumed
```

On rejection, the prior state remains unchanged.

### 8.3 No-price boundary

The program may require network fees or rent because Solana requires
infrastructure resources. It must not contain knowledge-price, seller-payout,
royalty, escrow, or treasury-consideration semantics in this capability.

## 9. End-to-End Grant Flow

The target grant sequence is deliberately storage-first and activation-last:

```text
1. Select exact artifact version V and immutable policy P.
2. Resolve stable identities A and B.
3. Validate A's signing-key binding and B's encryption-key binding.
4. Generate a content key for encryption epoch E.
5. Encrypt V under the exact cryptographic profile.
6. Create B's HPKE recipient envelope for the content key.
7. Persist ciphertext and envelope through all required storage layers.
8. Retrieve and verify the prepared objects and their context.
9. Construct the Solana grant against the exact pre-state revision.
10. A signs; the client submits to the exact Devnet program and cluster.
11. The program validates authority, policy, state, commitment, and replay.
12. The transaction records {A, B}, B's commitment, revision + 1, and replay consumption.
13. The orchestrator waits for `finalized` commitment.
14. The orchestrator independently fetches program-owned state.
15. The orchestrator reconciles finalized state with verified stored bytes.
16. B retrieves the active envelope and ciphertext.
17. B decrypts the envelope and then the artifact.
18. Evidence compares B's plaintext digest with the exact source fixture digest.
```

There is no distributed transaction spanning SQL, archive, and Solana. The
ordering and reconciliation rules contain the inconsistency window.

## 10. Finalized Activation and Reconciliation

Prepared material is not active merely because storage succeeded. A submitted
transaction is not active merely because an RPC node returned a signature.

Activation requires all of:

```text
storage_ready(material)
  AND transaction commitment >= finalized
  AND independently fetched program state == expected post-state
  AND on-chain material commitment == digest(verified stored bytes)
```

Otherwise the material remains one of:

- prepared;
- rejected;
- expired; or
- reconciliation-required.

### 10.1 Failure cases

```text
storage fails before submission
  -> block construction/signing/submission

transaction fails
  -> preserve prepared material as inactive evidence

transaction outcome is ambiguous
  -> query chain state; do not resubmit blindly

transaction finalizes but stored bytes cannot be verified
  -> membership remains chain truth; delivery is a typed failure

stored bytes exist but chain commitment differs
  -> withhold delivery; record reconciliation failure

RPC observes a weaker commitment only
  -> wait or expire under explicit policy; do not activate
```

## 11. Key-Reissue Flow

Reissue exists because stable identity must survive encryption-key replacement.

### 11.1 Request

```text
B is still a co-owner
  -> B binds a new encryption-key binding
  -> B signs a replay-safe reissue request
  -> request names exact artifact version, epoch, current envelope, and revision
  -> request becomes pending
```

The request records intent. It does not activate a new envelope.

### 11.2 Fulfillment

```text
create replacement envelope
  -> write it to all required storage layers
  -> retrieve and verify it
  -> exact Propagation Policy authorizes A to fulfill
  -> A signs the fulfillment
  -> Solana atomically consumes the request and changes B's active commitment
  -> wait for finalized
  -> reconcile stored bytes with finalized state
  -> activate replacement
```

The transition may change only:

- B's active envelope commitment;
- B's envelope revision;
- request status;
- state revision; and
- replay record.

It must preserve:

- all owner memberships;
- Knowledge Artifact Version;
- Encryption Epoch;
- Propagation Policy;
- economic state; and
- every other recipient's envelope.

The prior envelope is retained until a separately governed cleanup decision is
eligible and evidenced.

## 12. Lost Key versus Compromised Key

The architecture draws a hard boundary:

```text
lost, not suspected compromised
  -> same artifact version
  -> same Encryption Epoch
  -> same content key
  -> new recipient encryption-key binding
  -> new recipient envelope only

suspected compromised
  -> successor Encryption Epoch
  -> new content key
  -> new ciphertext
  -> replacement envelopes for every current owner
  -> no ordinary reissue shortcut
```

The existing pure Rust core already models and tests this distinction. The new
Solana and Durable Storage vertical has not yet implemented it end to end.

## 13. D65: How We Are Building It

The project follows meaning before machinery.

### Stage 1 — Canonical definitions

Definitions establish the stable terms, formal models, operational meaning,
plain-language intuition, boundaries, and consumers.

For the current vertical:

- `KEP-SOL-D1` through `KEP-SOL-D10` define the no-price Solana substrate;
- `KEP-SOL-D11` through `KEP-SOL-D17` define cryptographic profile, storage
  instantiation, reissue, finalized activation, Devnet trial, and evidence;
- `KEP-DST-D1` through `KEP-DST-D15` define reusable Durable Storage meaning.

### Stage 2 — Product Capability

The Product Capability states the exact user-visible outcome, scope,
exclusions, owners, contracts, policies, evidence, and claim ceiling.

The current capability was adopted at SHA-256:

```text
1b841eff87f1e4cd87de71b7b339ecd6c67185337fd17c80c0df88977491470f
```

Its decision is
[product-capability-adoption-001.json](capabilities/solana-coownership/successors/encrypted-durable-devnet/v1/decisions/product-capability-adoption-001.json).

### Stage 3 — Capability-local business ontology

The ontology makes product meaning explicit as typed nodes, relations, rules,
premises, proof requirements, and residue. It composes the admitted no-price
Solana ontology with the admitted SQL three-layer storage ontology.

At this snapshot, the successor ontology is **authorship in progress**. Its
directory changed during preparation of this guide as definition bindings,
nodes, and relations were materialized after the initial profile and source
registry. No stable complete-package validation or owner admission was selected
as evidence for this guide. Its authoritative status therefore remains
in-progress and not admitted regardless of how many candidate files are
present at a particular instant.

### Stage 4 — DomainSpec v2 authored source

After ontology admission, DomainSpec v2 must map every selected semantic node,
rule, relation, and proof requirement into system intent. Missing mapping
closure blocks compilation.

No DomainSpec source exists yet for the new encrypted/durable/Devnet successor.

### Stage 5 — Compiled graph and system ontology

The compiler must deterministically produce the same graph and system ontology
from the admitted DomainSpec source. Compilation PASS does not admit either
artifact; admission is a separate exact-digest decision.

### Stage 6 — Exact implementation binding

The implementation binding must name exact source, manifest, lockfile, schema,
program, client, storage adapter, cryptographic library, and test bytes and map
them to system-ontology obligations.

### Stage 7 — Conformance evidence

Evidence must cover positive behavior, negative authorization, replay,
corruption, restoration, cryptographic mismatch, reconciliation, and effect
ceilings. Dependent checks that cannot run are `not_evaluable`, not omitted.

### Stage 8 — Devnet trial

Devnet is a separately authorized external experiment. It requires disposable
test identities, non-repository key material, test SOL, exact program build,
cluster identity, genesis hash, endpoint class, storage realization, fixture,
commitment policy, and evidence bundle.

## 14. Current Construction and Evidence Status

| Layer | Current evidence | Lifecycle interpretation |
| --- | --- | --- |
| Base encrypted co-ownership definitions and ontology | Exact private definitions, admitted business and system ontology | Admitted semantic predecessor |
| Base Rust state-transition model | Exact binding accepted; 13 tests passed twice | Accepted local D65 realization; no runtime/crypto/Solana claim |
| No-price Solana Product Capability | Digest `42ac5b…` adopted | Adopted product meaning |
| No-price Solana business ontology | Exact candidate admitted | Admitted business meaning |
| No-price Solana DomainSpec source | Successor source digest `ccb300…` admitted | Admitted source |
| No-price Solana generated system ontology | Deterministic generated candidate exists | Not located as a separate owner admission in the selected package |
| Lean core-grant theorem | Candidate theorem evidence for pure transition model | Does not prove a Solana program |
| Solana program | No exact program implementation binding | Not implemented/admitted |
| Generic Durable Storage | Published complete D65 local-reference chain | Reusable admitted predecessor; no production provider |
| SQL three-layer storage | Published Rust/PostgreSQL/Docker conformance evidence; 8/8 behavior tests and integration PASS | Bounded local realization, not production topology |
| Encrypted Durable Devnet Product Capability | Digest `1b841e…` adopted | Current target product meaning |
| Test cryptographic profile | Exact candidate values selected | Test-only; no production security approval |
| Solana storage instantiation | Exact candidate consumer binding | Provider unbound; no storage operation authorized |
| Successor business ontology | Candidate files were being materialized during this snapshot | Authorship in progress; no stable complete-package PASS or owner admission selected |
| Successor DomainSpec/system ontology | Absent | `not_evaluable` |
| Successor implementation binding | Absent | `not_evaluable` |
| End-to-end local conformance | Absent | `not_evaluable` |
| Real Devnet trial | No wallet, program, transaction, or evidence bundle | Not authorized or executed |

### 14.1 Existing Rust core evidence

The current core crate implements:

- co-ownership grant;
- decryption acknowledgement;
- lost-key envelope reissue;
- compromised-key epoch rotation;
- state-revision checks;
- command and challenge replay protection; and
- policy-scoped authorization through an injected verifier.

Its receipt records 13/13 tests PASS on two runs. `clippy` was
`not_evaluable` because the installed toolchain did not contain the component.
The receipt does not claim live runtime behavior.

### 14.2 Existing storage evidence

The published SQL three-layer realization records:

- 8/8 Rust behavior tests PASS;
- portable-core adapter isolation PASS;
- PostgreSQL integration PASS;
- journal and archive recovery with destination verification PASS;
- append-only journal mutation rejected; and
- local Docker resources removed after governed runs.

This does not establish production availability or independent infrastructure
failure domains.

## 15. Formal Reasoning Lane

The Lean FormalClaim for the no-price grant proves a deliberately small pure
model proposition:

```text
valid modeled success
  -> A preserved
  -> B added
  -> B commitment recorded
  -> revision incremented
  -> replay consumed
  -> zero knowledge consideration preserved

modeled rejection
  -> exact pre-state preserved
```

This is valuable because it gives implementation and test authors a precise
invariant. It does not prove signer validation, Solana account safety,
cryptography, storage availability, transaction behavior, deployment, or the
new finalized activation workflow.

Formal evidence and runtime evidence are complementary:

```text
theorem: the modeled transition has the desired property
tests:   selected code paths exhibit expected behavior
Devnet:  exact deployed bytes behaved in the bounded external environment
```

None substitutes for the others.

## 16. Evidence Architecture for the Devnet Trial

The future end-to-end evidence bundle must connect one exact construction
chain to one exact external observation. It should include:

- definition digests;
- adopted Product Capability digest;
- admitted business ontology digest;
- admitted DomainSpec source digest;
- admitted compiled graph and system ontology digest;
- implementation binding digest;
- Solana program realization and build identity;
- cluster identity and genesis hash;
- cryptographic profile and storage instantiation IDs;
- storage realization identity;
- test fixture digest;
- disposable test identity references without secret key material;
- transaction signatures and slots;
- commitment observations through `finalized`;
- raw pre/post account digests;
- ciphertext and envelope commitments;
- source and decrypted plaintext digests;
- grant, replay, wrong-signer, wrong-state, corruption, and mismatch results;
- reissue request and fulfillment evidence;
- network, rent, RPC, storage, and archive costs classified separately; and
- all missing dependent checks as `not_evaluable` with causal blockers.

The bundle may prove that one bounded trial succeeded. It cannot prove
perpetual availability, production security, legal title, market demand, or
Mainnet readiness.

## 17. Failure and Threat Boundaries

### 17.1 Secrets

Never place in Git, Solana state, logs, evidence bundles, SQL rows, or archive
metadata:

- plaintext knowledge;
- content-encryption keys;
- recipient private keys;
- Solana private keys or seed phrases;
- decrypted envelope plaintext;
- database passwords;
- RPC credentials; or
- production credentials of any kind.

### 17.2 Identity substitution

Reject any design that treats a wallet address or encryption public key as the
stable Knowledge Identity. Key rotation must not create a new participant.

### 17.3 Commitment mismatch

Every retrieved object must be recomputed under the exact profile and context.
A locator, provider ETag, SQL row ID, or transaction field is not sufficient.

### 17.4 Replay and stale state

Every mutation binds an expected revision and fresh replay identity. A client
must re-read state after ambiguous outcomes rather than retrying blindly.

### 17.5 Cross-system partial failure

There is no claim of atomic commit across storage and Solana. The architecture
uses storage-first preparation, finalized activation, explicit inactive states,
and reconciliation evidence.

### 17.6 Availability

One verified retrieval proves one observation, not perpetual custody. Retention
and availability are policy and evidence concerns over time.

### 17.7 Irreversibility of learned knowledge

Removing an envelope or membership cannot revoke plaintext already learned.
Future licensing or access rules must not claim otherwise.

## 18. Cost and Economic Architecture

The current capability separates three categories:

```text
knowledge consideration
  = exactly absent

Solana infrastructure cost
  = fees + account rent + refundable reserves + RPC cost

Durable Storage infrastructure cost
  = SQL + journal + archive + retrieval + operations
```

When a paid capability is introduced, it must define:

- quoted knowledge price;
- asset and denomination;
- payer and recipients;
- settlement conditions;
- originator payout rule;
- downstream royalty rule, if any;
- failure and refund semantics;
- interaction with delivery activation; and
- evidence distinguishing price from infrastructure cost.

Those rules are not present in the no-price vertical.

## 19. Deployment Model: Future Devnet Shape

A likely first Devnet environment will contain:

```text
Rust CLI or test orchestrator
  -> exact crypto library binding
  -> Durable Storage port
       -> PostgreSQL operational adapter
       -> PostgreSQL append-only journal adapter
       -> SQL-independent archive adapter
  -> Solana RPC client
  -> exact deployed Solana program
  -> evidence collector
```

This is a target topology, not a selected deployment. The implementation stage
must still decide:

- client/program crate boundaries;
- Solana framework or native program approach;
- account and instruction encoding;
- program upgrade posture;
- local validator versus Devnet sequencing;
- exact HPKE and XChaCha Rust libraries;
- key-custody and disposable test-key procedure;
- SQL adapter reuse strategy;
- archive realization for Devnet;
- RPC endpoint class and retry policy;
- evidence capture and redaction; and
- cleanup policy for test resources.

## 20. Recommended Construction Sequence

The shortest governed path from the current state to a real test is:

```text
1. Complete successor business-ontology registries and validator.
2. Run deterministic ontology validation and mutation regressions.
3. Freeze one ontology candidate digest.
4. Obtain explicit owner admission for that digest.
5. Author successor DomainSpec v2 source with total mapping closure.
6. Validate and freeze its exact source digest.
7. Obtain explicit DomainSpec source admission.
8. Compile twice; require byte-identical graph and system ontology.
9. Obtain exact system-ontology admission.
10. Implement Rust cryptography, storage orchestration, Solana program, and client.
11. Bind every implementation byte and dependency to system obligations.
12. Run local positive, negative, recovery, corruption, and reconciliation tests.
13. Obtain bounded local-conformance acceptance.
14. Prepare a Devnet trial sheet: identities, program, cluster, storage, fixture, costs, and stop rules.
15. Obtain exact wallet/program/transaction authorization.
16. Execute one no-price Devnet grant and reissue trial.
17. Close the evidence bundle without inflating its claims.
```

The current immediate blocker is closing steps 1 through 4: finish the
successor ontology package, obtain a stable deterministic validation result,
freeze one exact candidate digest, and obtain a separate owner admission.

## 21. Architectural Decisions and Their Reasons

| Decision | Reason | Cost or trade-off |
| --- | --- | --- |
| Co-ownership expands `{A}` to `{A,B}` | Models copyable knowledge honestly | Exclusive-transfer products require a different model |
| Stable identity is separate from keys | Allows safe key replacement | Requires binding registries and more validation |
| Plaintext and content keys stay off-chain | Preserves confidentiality | Requires off-chain storage and reconciliation |
| Chain stores commitments, not artifacts | Keeps public state bounded | Availability is not guaranteed by Solana |
| Artifact policy is version-bound | Prevents silent rule changes | New rules require successor versions |
| Store before submitting | Avoids granting access to missing material | Can leave inactive orphaned prepared objects |
| Activate only at `finalized` | Stronger first-trial delivery boundary | Higher latency and no universal-finality claim |
| No cross-system atomicity claim | Reflects real SQL/archive/chain behavior | Requires reconciliation states and evidence |
| Three-layer storage uses behavioral ports | Preserves SQL portability | Adapter conformance must be proved separately |
| Reissue changes one envelope only | Preserves ownership and artifact identity | Compromise requires expensive epoch rotation |
| Costs are classified separately | Prevents fees from becoming hidden price | Later paid model needs explicit economics |
| Every lifecycle decision binds a digest | Prevents moving-target acceptance | Material changes require a new candidate decision |

## 22. Source Map

Primary product and construction sources:

- [Product thesis](PRODUCT-THESIS.md)
- [Product package guide](README.md)
- [Base encrypted co-ownership Product Capability](grant-encrypted-knowledge-coownership.product-capability.json)
- [No-price Solana Product Capability](realize-no-price-solana-coownership.product-capability.json)
- [No-price Solana capability package](capabilities/solana-coownership/README.md)
- [No-price Solana business ontology](capabilities/solana-coownership/ontology/README.md)
- [No-price Solana DomainSpec source](capabilities/solana-coownership/domainspec/README.md)
- [Lean core-grant FormalClaim](capabilities/solana-coownership/formalization/claims/CA2-FC-KEP-SOLANA-CORE-GRANT-001/README.md)
- [Current encrypted/durable/Devnet Product Capability](capabilities/solana-coownership/successors/encrypted-durable-devnet/v1/product-capability.json)
- [Current Product Capability adoption](capabilities/solana-coownership/successors/encrypted-durable-devnet/v1/decisions/product-capability-adoption-001.json)
- [Test-only cryptographic profile](capabilities/solana-coownership/successors/encrypted-durable-devnet/v1/cryptographic-profile.json)
- [Durable Storage instantiation](capabilities/solana-coownership/successors/encrypted-durable-devnet/v1/durable-storage-instantiation.json)
- [Successor ontology work area](capabilities/solana-coownership/successors/encrypted-durable-devnet/v1/ontology/README.md)
- [Existing Rust implementation binding](runtime/implementation-binding.json)
- [Existing Rust conformance receipt](runtime/conformance-receipt.json)

Published Durable Storage predecessors are resolved at Git object `1b629e601`.
Their paths and exact hashes are bound in the storage instantiation and current
Product Capability candidate envelope.

## 23. Claim Ceiling

This architecture guide describes the product direction, admitted predecessor
substrates, candidate target architecture, and open construction path.

It does not establish:

- completion or admission of the successor business ontology;
- successor DomainSpec or system-ontology admission;
- a conforming cryptographic implementation;
- a Solana program or deployed program identity;
- successful storage integration for the new consumer;
- wallet creation, signing, transaction submission, or SOL transfer;
- successful recipient decryption on Devnet;
- production security, availability, recovery, RPO, or RTO;
- licensing, rights, royalties, resale, legal title, or reputation;
- publication, release, deployment, or external-effect authority; or
- evidence that users want or will pay for the product.

Those claims require their own exact artifacts, evidence, owners, and gates.
