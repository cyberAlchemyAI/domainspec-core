# Encrypted Durable Co-Ownership: Devnet Test Tutorial

Status: configuration tutorial; Devnet execution is not yet authorized

This tutorial prepares one disposable, non-production Solana Devnet trial of
`CA2-CAP-REALIZE-ENCRYPTED-DURABLE-DEVNET-COOWNERSHIP`. It does not authorize
wallet creation, an airdrop, program deployment, transaction submission, or a
database connection. Run the effectful sections only after the local gates in
this document pass and the protocol owner authorizes the exact trial envelope.

The trial proves a narrow result:

```text
encrypted artifact bytes
  -> three-layer verified storage
  -> finalized Devnet co-owner grant A -> {A, B}
  -> B retrieves and decrypts the exact artifact version
  -> optional B key-reissue request fulfilled by A under policy
  -> evidence records exact identities, finality, and infrastructure cost
```

It does not prove production readiness, Mainnet safety, availability, legal
ownership, licensing, royalties, resale rights, or a knowledge price.

## 1. Do not configure Devnet until these local gates pass

The final local implementation must provide all of the following:

- an accepted successor Rust binding for the exact provider and local
  program-test surface;
- XChaCha20-Poly1305 and RFC 9180 HPKE known-answer and negative-vector tests;
- deterministic CBOR rejection tests;
- provider-neutral SQL integration and storage failure-injection tests;
- three-layer write, retrieval, identity, and restoration checks;
- a local Solana `program-test` grant, rejection, replay, reissue, and finality
  simulation;
- a structural proof that plaintext, content keys, private keys, credentials,
  and ciphertext bytes are absent from program-owned state; and
- an independent security review of the exact dependency and threat-boundary
  bytes selected for the trial.

Until those gates close, use only offline/local test commands documented by the
accepted implementation candidate. Do not create a Devnet wallet merely to
work around an incomplete local gate.

## 2. Install and verify the tools

You need:

- the Rust toolchain pinned by the repository;
- the Solana CLI with `cargo build-sbf`, `solana`, and `solana-keygen`;
- PostgreSQL 13 or newer for the first provider realization; and
- a writable directory outside the repository for the SQL-independent archive
  and trial evidence.

Use the official [Solana installation guide](https://solana.com/docs/intro/installation)
for the CLI. Verify tools without changing external state:

```bash
rustc --version
cargo --version
solana --version
solana-keygen --version
psql --version
```

Record these versions in the trial evidence. Do not silently upgrade between
the local proof run and the Devnet trial.

## 3. Prepare an ignored configuration file

Create this file outside the repository, for example
`/absolute/private/path/kep-devnet.env`. Restrict it to the current user. Never
commit it, paste it into chat, or include its values in evidence.

```bash
# Fixed semantic identities
KEP_ENVIRONMENT_ID=solana-devnet
KEP_CRYPTO_PROFILE_ID=KEP-SOL-CRYPTO-DEVNET-V1
KEP_STORAGE_INSTANTIATION_ID=KEP-SOL-DST-INSTANTIATION-DEVNET-V1
KEP_SOLANA_COMMITMENT=finalized

# Operational SQL layer and append-only recovery journal
# PostgreSQL is the first realization. The runtime contract remains SQLx Any
# so another admitted SQL URL can be used without changing product meaning.
KEP_SQL_URL=postgresql://USER:PASSWORD@127.0.0.1:5432/cyberalchemy_kep_devnet
KEP_SQL_SCHEMA=cyberalchemy_kep_devnet

# SQL-independent immutable archive and evidence output
KEP_ARCHIVE_DIR=/absolute/private/path/kep-devnet/archive
KEP_EVIDENCE_DIR=/absolute/private/path/kep-devnet/evidence

# Devnet boundary
KEP_SOLANA_RPC_URL=https://api.devnet.solana.com
KEP_SOLANA_KEYPAIR_PATH=/absolute/private/path/kep-devnet/devnet-authority.json
KEP_SOLANA_PROGRAM_KEYPAIR_PATH=/absolute/private/path/kep-devnet/program-keypair.json
KEP_SOLANA_PROGRAM_SO=/absolute/path/to/target/deploy/cyberalchemy_kep.so

# Fill after deployment
KEP_SOLANA_PROGRAM_ID=
KEP_TRIAL_ID=
```

The SQL password and keypair bytes are credentials. The evidence bundle may
record their opaque binding identifiers and public keys, never their values.

## 4. Configure the three storage layers

The first trial uses three logical protection layers:

1. `operational`: mutable SQL registry of qualified object identity and current
   opaque locator metadata;
2. `recovery-journal`: append-only SQL events stored separately from the live
   tables; and
3. `immutable-archive`: exact encrypted bytes in a SQL-independent archive.

All layers must close on the same qualified byte identity. A same-host trial
proves the mechanism only; it is not three independent disaster-recovery
failure domains.

Create a dedicated local PostgreSQL database and least-privilege trial role.
Apply only the migration shipped and digest-bound by the accepted provider
implementation. Do not manually create substitute tables when a migration is
missing—the missing migration is a local blocker.

The archive directory must:

- be outside the Git worktree;
- reject overwrite of an existing object identity;
- contain only encrypted artifacts and recipient-envelope ciphertext;
- never contain plaintext, content keys, private keys, database passwords, or
  wallet material; and
- support exact-byte retrieval after the operational SQL layer is unavailable.

Before Devnet, run the provider's local readiness and restoration commands.
The future implementation must print a receipt rather than secrets. Expected
receipt fields are storage-realization ID, provider kind, migration digest,
archive policy, object identities, verified layers, and `ready: true`.

## 5. Create a disposable Devnet identity — effectful

Stop here until the owner authorizes wallet creation and the exact keypair
paths. Use new Devnet-only keys. Never reuse a Mainnet, exchange, personal, or
customer wallet.

```bash
solana-keygen new --outfile "$KEP_SOLANA_KEYPAIR_PATH"
solana-keygen new --outfile "$KEP_SOLANA_PROGRAM_KEYPAIR_PATH"

solana config set \
  --url "$KEP_SOLANA_RPC_URL" \
  --keypair "$KEP_SOLANA_KEYPAIR_PATH" \
  --commitment finalized

solana config get
solana address
```

Confirm that the URL is exactly Devnet before funding. Solana documents the
public Devnet endpoint as `https://api.devnet.solana.com`; it is rate-limited
and Devnet may reset. See [Clusters and public RPC endpoints](https://solana.com/docs/references/clusters).

## 6. Obtain test SOL — effectful

An airdrop changes external state even though Devnet SOL has no real monetary
value. Run it only inside the authorized trial:

```bash
solana airdrop 2
solana balance
```

If the public faucet is rate-limited, stop and record the failure. Do not switch
RPC providers, wallets, or clusters without a successor authorization.

## 7. Build and deploy the exact program — effectful

Build only the accepted source revision and record the source and `.so` SHA-256
digests before deployment:

```bash
cargo build-sbf
sha256sum "$KEP_SOLANA_PROGRAM_SO"

solana program deploy \
  "$KEP_SOLANA_PROGRAM_SO" \
  --program-id "$KEP_SOLANA_PROGRAM_KEYPAIR_PATH"
```

Set `KEP_SOLANA_PROGRAM_ID` to the returned program ID and verify it:

```bash
solana program show "$KEP_SOLANA_PROGRAM_ID"
```

The Solana CLI deployment flow and its required program authority are described
in [Deploying Programs](https://solana.com/docs/programs/deploying). Do not
transfer authority, make the program immutable, upgrade it, or close it during
this trial unless those operations are separately authorized.

## 8. Run the protocol trial — effectful

The accepted implementation will supply the exact command. It must consume the
configuration above and perform this sequence:

1. generate disposable A and B protocol identities, keeping signing and HPKE
   key roles separate;
2. encrypt one test-only artifact version under a new encryption epoch;
3. write and independently retrieve the encrypted artifact and B envelope from
   all required storage layers;
4. refuse transaction construction unless storage readiness is complete;
5. submit the A-authorized no-price grant that preserves A and adds B;
6. wait for `finalized`, then reconcile program state, revision, commitment,
   storage retrieval, and program/trial identity;
7. allow B to retrieve and decrypt the exact bytes;
8. exercise stale revision, replay, wrong binding, and unfinalized-state
   negatives without changing accepted state;
9. optionally request and fulfill one lost-key reissue without changing the
   artifact, epoch, owners, policy, or economic state; and
10. record network fee, rent, and storage cost strictly as infrastructure cost,
    never knowledge consideration.

Do not run an improvised client if the exact trial command or its expected
binary digest is absent. That absence means the repository has not yet reached
the Devnet gate.

## 9. Evidence to retain

The trial evidence bundle must contain only public or non-secret observations:

- source, build, binding, implementation, migration, and program digests;
- Solana CLI version, cluster genesis hash, RPC class, program ID, loader ID,
  upgrade posture, transaction signatures, slots, and finalized observations;
- trial ID, artifact-version ID, encryption-epoch ID, public identity bindings,
  revisions, replay-domain IDs, and qualified byte commitments;
- storage-realization ID, opaque locators, layer receipts, verified retrievals,
  and recovery result;
- proof-by-proof PASS, FAIL, partial, or `not_evaluable` results with causal
  blockers; and
- fees, rent, storage, and retrieval costs classified as infrastructure cost.

Never retain plaintext, content keys, recipient private keys, wallet secret
keys, seed phrases, database passwords, full connection URLs, or undeclared
customer material.

## 10. Exact authorization bundle required from the owner

Before the first Devnet command, present one immutable trial envelope containing:

- accepted local binding and implementation digests;
- accepted crypto, SQL, local program-test, and security-review evidence;
- exact source/build/program/migration digests;
- Devnet RPC URL and observed genesis hash;
- public wallet address and keypair path, but not key bytes;
- requested airdrop ceiling;
- program ID and upgrade posture;
- SQL provider class and opaque credential reference;
- archive and evidence directory identities;
- allowed instructions, maximum transaction count, and maximum test-SOL spend;
- retention and cleanup posture; and
- explicit permission for wallet use, RPC, airdrop, deployment, transaction
  submission, finalized observation, and evidence capture.

Acceptance of a local implementation or this tutorial is not that permission.

