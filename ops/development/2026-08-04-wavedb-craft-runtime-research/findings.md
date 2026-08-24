# WaveDB for Craft: bounded runtime finding

## Decision

Build only a **candidate-local, digest-bound, disposable WaveDB projection experiment**. The projection may accelerate bounded reads and exercise recovery controls, but `.craft/ledger.yml` remains the sole project-local source of truth. A transactional sidecar that writes while retaining YAML authority remains **HOLD**. Replacing Craft's canonical store with WaveDB is **KILL for this route** and would require a separate authority-changing owner route.

This decision admits a finite experiment, not a ready runtime. No WaveDB code was installed, built, or executed in this research. No crash run, benchmark, package compatibility run, security run, publication, promotion, or production proof exists.

## Claim ceiling

The evidence supports static first-party source review plus an unexecuted synthetic fixture and acceptance design. It supports a bounded architectural recommendation and explicit failure oracles. It does not establish WaveDB durability, failure atomicity, multi-writer safety, migration safety, package compatibility, performance, security closure, license closure, Craft acceptance, or release fitness.

Every future WaveDB open, read, scan, batch, checkpoint, reopen, or projection comparison is **adapter observation only**. It is not Craft validation, acceptance, promotion, authority, or readiness evidence.

## Immutable source identities

### WaveDB corpus

- Repository: [`vijayee/WaveDB`](https://github.com/vijayee/WaveDB/tree/01c77e8b70f71de9b72480e73a3a179f6e93a009)
- Commit: `01c77e8b70f71de9b72480e73a3a179f6e93a009`
- README blob: `cc11106438a926849ed91cac18a773ccae2fba19`
- README SHA-256: `140880186286dc723118526d110075fe2520655cc112e4e9f694e15915c35095`
- Node manifest SHA-256: `82e87aaaac10113cb1294732bf149356f6f7df76ecde0259181999c6a3fe9dc3`
- Reviewed Node package identity: `@vijayee/wavedb@0.15.8`; the README's unscoped install text is not an admitted install instruction.

### Arcanum/Craft corpus

The public Arcanum checkout was pinned at commit `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295` with these blobs:

| Source | Blob |
|---|---|
| [`arcana/craft/SKILL.md`](../../../arcanum/arcana/craft/SKILL.md) | `d7df17c75d5c644799dd5cb8cd2299df393222bd` |
| [`arcana/craft/ARCHITECTURE.md`](../../../arcanum/arcana/craft/ARCHITECTURE.md) | `e5a37d792200adefbea838fa53efaa3b2bb285e2` |
| [`arcana/craft/README.md`](../../../arcanum/arcana/craft/README.md) | `ff4a8eaacda0677a6e9a93bf18fcbe7bd12ad2bb` |
| [`arcana/craft/templates/ledger.schema.yml`](../../../arcanum/arcana/craft/templates/ledger.schema.yml) | `3dd789e27cc711299104d8532c0f6b94c6619ae3` |
| [`arcana/craft/templates/schemas/ledger-core.schema.yml`](../../../arcanum/arcana/craft/templates/schemas/ledger-core.schema.yml) | `0fad7f0c356fa4d276ab9106c57a94b810690141` |
| [`arcana/craft/templates/schemas/index.schema.yml`](../../../arcanum/arcana/craft/templates/schemas/index.schema.yml) | `cbd7b6c67591abda5aa8d97f490c6d12c6480dd5` |
| [`arcana/craft/examples/product-launch-CRAFT.md`](../../../arcanum/arcana/craft/examples/product-launch-CRAFT.md) | `87866a77d26286b164fbf4e5f4bc5fde3a17b7bf` |
| [`arcana/craft/examples/product-launch-ledger.yml`](../../../arcanum/arcana/craft/examples/product-launch-ledger.yml) | `97d5e014562a73d953f9e77a5fb29c1f8f7f97c2` |
| [`development/craft/CRAFT-REFINE-RUNTIME-STRATEGY.md`](../../../arcanum/development/craft/CRAFT-REFINE-RUNTIME-STRATEGY.md) | `d6c777edfd0881a88941f3a5b0371a48b1a85e03` |
| [`development/craft/CRAFT-RUNTIME-DESIGN.md`](../../../arcanum/development/craft/CRAFT-RUNTIME-DESIGN.md) | `26e355aab6dc3bb73d35d233e094d66e5cb31543` |

The files under `arcanum/arcana/craft/` are the canonical Craft contract reviewed here. The files under `arcanum/development/craft/` are historical design and failure evidence only; they do not authorize a storage change.

### Frozen research and fixture constants

- Frozen explorer corpus: `research.md`, SHA-256 `1a5999ab113e7d22a52022e18a817912f1575ffe2db2b0422e76bb0762af55bd`.
- Independently recomputed from the frozen `L0` YAML block using LF and one terminal newline: `H_L = 39ab11452f8983999a8f2154bd9255e2e0ed8363243b804c3d67dc48f1a51af7`.
- Independently recomputed from the frozen `C0` Craft view block using LF and one terminal newline: `sha256(C0) = 2ccd199aaa6d75e64e26f5cd9a12a9d90c0c4585a167d3bce171350de3c4f85a`.
- `H_S`, both required `H_P` values, and `sha256(J(I0))` remain unresolved. They cannot become acceptance constants until the parser identity/options, complete normalized model, complete index `I0`, and complete sorted key/value manifest are materialized independently of the adapter.

## Three-posture verdict matrix

| Posture | Verdict | What may advance | Decisive boundary |
|---|---|---|---|
| Digest-bound WaveDB projection/cache | **BOUND — advance only as candidate-local experiment** | One isolated adapter, synthetic fixture, deterministic codec, exact manifest, read observations, quarantine/rebuild controls | YAML remains authoritative; the database is disposable; no database-to-YAML path; no active-generation pointer |
| Transactional sidecar retaining YAML authority | **HOLD** | Research only | No owned filesystem CAS, cross-process lease, crash contract, true mid-apply fault seam, or recovery proof; peer YAML/DB dual-write is forbidden |
| WaveDB as canonical Craft store | **KILL for this route** | Nothing | It changes authority, validation, portability, recovery, schema, and promotion ownership; reconsideration requires a separate Craft-owner governance route |

## Corrected v0 architecture

```text
filesystem-resolved workspace root
           |
           v
fresh read of canonical .craft/ledger.yml bytes (L0)
           |
           +--> validate with the Craft-owned schema and model
           |
           +--> H_L = sha256(L0)
                         |
                         v
isolated WaveDB test store: /craft/v1/workspaces/<W>/generations/<H_L>/
                         |
                         +--> raw verification copy of L0
                         +--> deterministic rows and indexes
                         +--> derived verification copies
                         +--> closed manifest after complete readback
                         |
                         v
serve a query only when the exact digest-named generation fully re-verifies
```

There is no `active_generation`, activation manifest, alias, symlink, or mutable current-generation pointer in v0. Before each query, the adapter freshly reads canonical YAML, validates it, recomputes `H_L`, and direct-selects only `/generations/<H_L>/`. A missing, incomplete, malformed, stale, or hash-mismatched generation produces zero rows and is quarantined or rebuilt as a new isolated sibling. It never causes fallback to database content as authority.

`source/ledger.yml` and every `rows/...` value are immutable, digest-bound verification copies of one canonical YAML epoch. They may be read only to compare with a fresh canonical YAML read. They may never reconstruct, restore, mutate, or replace `.craft/ledger.yml`. A digest mismatch invalidates the complete generation.

The adapter exposes no YAML write, derived-view import, canonical mutation, schema migration, multi-writer, graph, GraphQL, SQL, replication, or peer-to-peer interface. Workspace access is resolved and authorized in the filesystem before a WaveDB key is constructed; a hierarchical prefix is not an authorization boundary.

## Exact v0 key, value, and codec proposal

This is a candidate codec to freeze in the Work Pack, not an existing Craft contract.

### Key encoding

1. Every logical key is UTF-8 without BOM and begins with `/craft/v1/`.
2. `W` is a stable workspace identifier supplied only after filesystem resolution. Each variable path segment is UTF-8 NFC followed by RFC 3986 percent-encoding of every byte except `A-Z a-z 0-9 - . _ ~`; hex digits are uppercase. `/`, NUL, `.` and `..` cannot escape a segment.
3. `H_L` is exactly 64 lowercase hexadecimal characters.
4. Keys are compared and sorted by unsigned UTF-8 byte order.
5. The generation prefix is exactly:

   ```text
   /craft/v1/workspaces/<seg(W)>/generations/<H_L>/
   ```

6. The admitted suffix families are:

   ```text
   meta/manifest.json
   source/ledger.yml
   rows/context/<seg(id)>.json
   rows/child/<seg(id)>.json
   rows/artifact/<seg(id)>.json
   rows/description/<seg(id)>.json
   rows/blocker/raw/<seg(id)>.json
   rows/blocker/refined/<seg(id)>.json
   rows/decision/<seg(id)>.json
   rows/gap/<seg(id)>.json
   rows/receipt/<seg(id)>.json
   rows/recomposition/<seg(id)>.json
   indexes/by-kind/<kind>.json
   indexes/by-parent/<seg(id)>.json
   derived/CRAFT.md
   derived/index.json
   ```

The fixture manifest must enumerate the complete actual key set. An unlisted key, duplicate decoded ID, invalid reference, or unexpected kind is a hard failure.

### Value encoding

- `source/ledger.yml` is the exact `L0` byte sequence, including its single terminal newline.
- `derived/CRAFT.md` is the exact generated UTF-8 view bytes, including its declared terminal-newline rule.
- `rows/**/*.json`, `indexes/**/*.json`, `derived/index.json`, and `meta/manifest.json` use `J(x)`.
- `J(x)` is UTF-8 JSON without BOM, insignificant whitespace, or terminal newline. Object keys are recursively sorted by Unicode scalar value; arrays retain model-defined order; JSON strings use the deterministic serializer's escaping; only schema-admitted JSON scalar types are allowed. The Work Pack must pin the YAML parser, its version/options, the normalized model rules, and the JSON serializer before `H_S` is frozen.
- Row values contain one complete normalized entity plus its canonical ID and source selector. They do not create new relation or artifact authority.
- Index values contain only ordered IDs and source selectors. They do not duplicate entity bodies and cannot become source truth.
- Every receipt and receipt reference remains solely at its externally owned filesystem path. No receipt path/digest record, receipt body, verdict, execution proof, or Craft receipt is stored in WaveDB.

### Hash and manifest encoding

Let `L0` be the exact YAML bytes, `S0 = parseYaml(L0)` under the frozen parser contract, `I0` the complete derived index value, and `P` the complete generation key/value set excluding only `meta/manifest.json`, which must be excluded to prevent self-reference. Because the manifest is the only admitted `meta/**` key, `P` contains every other admitted stored key and value without exception.

```text
H_L = sha256(L0)
H_S = sha256(J(S0))
H_P = sha256(concat(for k in bytewise_sort(keys(P)):
                    utf8(k) || 0x00 || value_bytes(P[k]) || 0x0a))
H_I = sha256(J(I0))
H_C = sha256(C0)
```

`meta/manifest.json` is `J(...)` over:

```json
{
  "adapter_schema": "craft-wavedb-projection/v0",
  "craft_schema": "<pinned Craft schema identity>",
  "workspace": "<W>",
  "ledger_sha256": "<H_L>",
  "semantic_sha256": "<H_S>",
  "projection_sha256": "<H_P>",
  "index_sha256": "<H_I>",
  "craft_view_sha256": "<H_C>",
  "payload_key_count": 0,
  "payload_key_value_digests": [
    {"key": "<exact key>", "value_sha256": "<sha256(value bytes)>"}
  ],
  "verification": "complete"
}
```

The array is in bytewise key order and `payload_key_count` equals its length. It enumerates and digests every non-manifest key in the closed generation. The manifest is written only after a full independent readback matches every non-manifest key/value, value digest, aggregate hash, derived hash, and canonical YAML digest. Query admission independently enumerates the complete stored key set, rejects any unadmitted or missing key, and re-verifies every admitted key/value including the manifest. Missing or non-`complete` verification is zero-output failure, not a partially useful cache.

## Finite v0 Work Pack

No product mutation begins until the owner gates below admit the exact package and write boundaries. All outputs belong to an isolated candidate fixture directory; the experiment does not edit canonical Craft sources or a user's `.craft/ledger.yml`.

### WP-0 — freeze inputs and environment

1. Pin the WaveDB source commit, exact registry package identity, tarball integrity, native toolchain, operating systems, architectures, and dependency graph. Stop on any source/package mismatch or unscoped package resolution.
2. Pin Craft commit/blob identities, schema files, YAML parser/version/options, normalization rules, JSON serializer, adapter schema, and test-store location.
3. Materialize `L0` and `C0`; independently require the two hashes recorded above.
4. Materialize full `S0`, `I0`, and the exact sorted key/value fixture manifest. Freeze `H_S`, pre-update `H_P`, post-update `H_P`, `H_I`, every value digest, and exact key/row counts independently of the adapter.

Acceptance is non-vacuous: a single wrong byte, missing key, extra key, changed ordering, parser drift, wrong count, or wrong literal hash fails WP-0.

### WP-1 — construct the projection adapter

1. Expose only: `buildGeneration(workspaceRoot, expectedH_L)`, `verifyGeneration(workspaceRoot, expectedH_L)`, `queryGeneration(workspaceRoot, expectedH_L, query)`, `renderFromYaml(workspaceRoot)`, `quarantineGeneration(expectedH_L, reason)`, and `rebuildGeneration(workspaceRoot, expectedH_L)`.
2. Resolve and authorize `workspaceRoot` in the filesystem before database access.
3. Fresh-read and validate YAML, require `sha256(L0) == expectedH_L`, encode the complete payload into a previously unserved digest-named generation, read it back, and write the closed manifest only after full verification.
4. Provide no active-generation pointer and no write path from database bytes to YAML or from an edited derived view to the database.

Acceptance requires unchanged YAML bytes before and after every operation, the exact codec manifest, and zero query output until complete verification.

### WP-2 — exact normal-path observations

1. Import the frozen fixture into a fresh isolated store as batch `B0`.
2. Verify every exact key/value digest, count, `H_L`, `H_S`, first `H_P`, `H_I`, and `H_C`.
3. Query each entity kind and each declared index; compare canonical JSON bytes, not only semantic equality or row counts.
4. Regenerate `CRAFT.md` and index from fresh YAML through the Craft-owner-approved renderer/indexer boundary and compare exact bytes/hashes.
5. Run one declared `B1` fixture update in a new digest-named generation and require the independently frozen second `H_P`. The earlier digest generation remains disposable historical cache data and is never selected for the new YAML digest.

### WP-3 — iterator visibility observation

1. Open an iterator over the pre-`B1` generation at a deterministic barrier.
2. Record the iterator-open event and the first exact key/value bytes.
3. Complete `B1` in its different digest-named generation.
4. Record every remaining old-stream byte and the complete new-stream bytes from a newly opened iterator.
5. Compare both streams with frozen manifests.

This can observe iterator MVCC behavior. It does not turn `database_snapshot()` into a general read snapshot or prove broader isolation.

### WP-4 — non-vacuous negative controls

| Control | Required trigger | Exact failure oracle |
|---|---|---|
| Invalid relation | Fixture contains a frozen invalid reference | Preflight fails before any generation is query-eligible; zero rows |
| Wrong workspace | Seed `ws-beta` with a unique sentinel and first prove a direct beta query can see it | An alpha-bound query returns `WORKSPACE_MISMATCH` before row emission and never exposes the beta sentinel |
| Stale digest | Mutate fixture YAML after deriving `expectedH_L` | `LEDGER_DIGEST_MISMATCH`; zero rows; no stale generation fallback |
| Batch preflight rejection | Include one invalid operation or limit-exceeding batch before submission | Entire batch rejected pre-apply; no key from the rejected generation is query-eligible |
| Derived-view edit | Modify only candidate `CRAFT.md`, leaving YAML unchanged | Regeneration overwrites the edit from unchanged YAML; edit is never ingested; YAML hash stays exact |
| Iterator timing | Use the WP-3 barriers | Old stream and new stream each match their complete frozen manifest; no hybrid |
| Crash phase | Terminate the child at barriers before batch, after submission/before resolution when safely observable, after resolution/before verification, and after verification/before query admission | On reopen, an unverified generation yields zero rows and is quarantined; only a fully reverified digest-named generation is served; no power-loss claim |
| Logical corruption | Replace one named key/value in an isolated copy | Recomputed value, aggregate, derived, or canonical hash fails; zero output; externally owned quarantine artifact; fresh sibling rebuild matches exact hashes |
| Physical corruption | Damage one named isolated store file | Any open success with incomplete or wrong state is a hard failure; never inspect or repair a user's live store |
| Concurrent A/B observation | Synchronize two writer IDs against an isolated store | Record whether complete A/A or B/B wins; any hybrid is fatal. This does not admit multi-writer adapter support or prove a lease/CAS contract |
| YAML mutation guard | Hash canonical YAML before and after every control | Any byte change is fatal and ends the experiment |

The batch control is named `batch-preflight-rejection`; it is not evidence of true mid-apply failure atomicity. True mid-apply injection remains HOLD until a safe first-party or fork-owned fault seam exists.

### WP-5 — recovery, quarantine, and observation receipts

1. On any mismatch or malformed/missing manifest, emit the quarantine or observation artifact solely to its externally owned filesystem path, return zero rows, and construct a fresh isolated sibling. Never write that artifact, its reference, or its digest into the invalid generation or any closed generation.
2. Prove the rebuilt generation matches the independently frozen manifest before reading any row from it.
3. Record package identity, commit, toolchain, OS/architecture, WaveDB configuration, WAL mode, exact barriers, inputs, store-copy hashes, outputs, and all failure codes.
4. Record optional latency/size observations with environment details. They are descriptive observations and cannot gate correctness or create performance or durability claims.

### WP-6 — bounded closeout

1. Require all positive and negative oracles above to pass with exact bytes and stable failure codes.
2. Preserve all HOLD/KILL residue below; do not silently convert excluded behavior into acceptance.
3. Delete only the explicitly resolved isolated temporary fixture store. Cleanup is not evidence for workspace deletion, prefix deletion atomicity, schema migration, or rollback.
4. Route the observation package to the Craft owner. Separate decisions are required for any next product slice, publication, promotion, or distribution.

## HOLD and KILL residue

| Residue | Status | What would be needed to reconsider it |
|---|---|---|
| True WaveDB mid-apply atomicity | **HOLD** | Safe owned fault seam and a deterministic mid-apply failure witness with exact rollback oracle |
| Transactional YAML-authority sidecar | **HOLD** | Owned YAML CAS, cross-process lease, crash contract, recovery protocol, and no peer dual-write ambiguity |
| Multi-writer adapter operation | **HOLD** | Specified owner, admission/lease mechanism, stable loser code, exact winner manifest, crash evidence |
| Crash/power durability | **HOLD** | Platform-specific destructive harness and acknowledged-write oracles; process termination alone is insufficient |
| Schema migration and downgrade | **HOLD** | Explicit source/target schema pair, transformed fixture bytes, unsupported-pair refusal, cache disable, and downgrade oracle |
| Encryption reopen/rotation/key-loss behavior | **HOLD** | Owned security protocol and executable key lifecycle evidence |
| Native package/platform compatibility | **HOLD** | Exact tarball/source mapping and declared build/platform observations |
| Core/dependency license closure and publication | **HOLD** | Root/dependency authority, SBOM, and publication-owner approval |
| Prefix/workspace deletion semantics | **HOLD** | Destructive-operation owner route and atomicity/recovery evidence |
| In-place recovery from a corrupted store | **KILL for v0** | v0 always quarantines and rebuilds; it never trusts a valid prefix or repairs in place |
| Unscoped `npm install wavedb` | **KILL** | Exact admitted package identity is required |
| Graph/GraphQL relations as canonical Craft relations | **KILL for v0** | Craft retains relation ownership; these APIs are excluded |
| WaveDB as canonical Craft store | **KILL for this route** | Separate authority-changing Craft-owner governance route |

## Owner gates

1. **Craft owner:** approve the bounded projection contract, schema/model interpretation, renderer/indexer boundary, test-store location, and proof that native artifact bytes and called-capability verdicts remain with their existing owners.
2. **Adapter owner:** own the deterministic codec, parser/serializer pins, exact fixture manifest, quarantine behavior, stable errors, and removal of every database-to-YAML or derived-ingestion path.
3. **Package and security owner:** approve exact registry identity/tarball integrity, source correspondence, native toolchain, dependency inventory, platform matrix, WAL configuration, and security scope before installation begins.
4. **Publication owner:** close core/dependency license and SBOM residue before distribution or publication. Projection correctness does not close this gate.
5. **Destructive-operation owner:** separately authorize any real deletion, corruption, key-loss, or crash/power harness. V0 uses only explicit isolated copies.
6. **Authority-change owner route:** required before revisiting a transactional writer or canonical replacement. This finding grants no such authority.

## Exact-binding evidence table

| ID | Claim and verdict | Immutable source and exact selector | Proof status |
|---|---|---|---|
| `AUTH-001` | Canonical Craft owns the ledger; YAML is source truth and views/index are derived — **BOUND** | Arcanum `07b01c9...`; [`SKILL.md`](../../../arcanum/arcana/craft/SKILL.md) blob `d7df17...`, lines 33-71 and 312-316; [`ARCHITECTURE.md`](../../../arcanum/arcana/craft/ARCHITECTURE.md) blob `e5a37d...`, lines 39-79 and 241-261 | Observed static contract |
| `AUTH-002` | Development documents are historical evidence only — **BOUND** | Arcanum `07b01c9...`; [`CRAFT-REFINE-RUNTIME-STRATEGY.md`](../../../arcanum/development/craft/CRAFT-REFINE-RUNTIME-STRATEGY.md) blob `d6c777...`, lines 3-90 and 146-149; [`CRAFT-RUNTIME-DESIGN.md`](../../../arcanum/development/craft/CRAFT-RUNTIME-DESIGN.md) blob `26e355...`, lines 16-20 | Observed historical evidence |
| `WDB-001` | Hierarchical paths and bounded iterators are plausible projection primitives — **BOUND** | [WaveDB commit `01c77e8...`](https://github.com/vijayee/WaveDB/tree/01c77e8b70f71de9b72480e73a3a179f6e93a009); `src/HBTrie/path.h:19-57`; `src/Database/database_iterator.h:31-55` | Observed static source |
| `WDB-002` | Normal batch shares one WAL record/transaction, but failure atomicity is unresolved — **HOLD** | [WaveDB commit `01c77e8...`](https://github.com/vijayee/WaveDB/tree/01c77e8b70f71de9b72480e73a3a179f6e93a009); `src/Database/batch.h:30-35`; `database.c:2931-3064`; `wal_manager.c:1646-1737,1865-1873` | Observed static source; not executed |
| `WDB-003` | Iterator MVCC differs from persistence checkpoint — iterator observation **BOUND**, broader snapshot claims **HOLD** | [WaveDB commit `01c77e8...`](https://github.com/vijayee/WaveDB/tree/01c77e8b70f71de9b72480e73a3a179f6e93a009); `database.c:1890-1931,2587-2604`; `database_iterator.c:792-873` | Observed static source; not executed |
| `WDB-004` | WAL modes exist; crash/power durability is unresolved — **HOLD** | [README lines 129-146 at `01c77e8...`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/README.md#L129-L146); `wal.h:58-60`; `wal_manager.c:263-299,1475-1627` | Observed static source; not executed |
| `WDB-005` | Corruption may return a valid prefix; in-place recovery — **KILL**; quarantine/rebuild plan — **BOUND** | [WaveDB commit `01c77e8...`](https://github.com/vijayee/WaveDB/tree/01c77e8b70f71de9b72480e73a3a179f6e93a009); `wal_manager.c:320-432,1646-1737` | Observed failure path; plan unexecuted |
| `WDB-006` | Reviewed package is scoped; installation remains unresolved — **HOLD**, unscoped install — **KILL** | [`bindings/nodejs/package.json:1-29`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/bindings/nodejs/package.json#L1-L29); [`README.md:351-356`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/README.md#L351-L356) | Observed metadata; not installed |
| `WDB-007` | Encryption exists; reopen/rotation/key-loss behavior unresolved — **HOLD** | [WaveDB commit `01c77e8...`](https://github.com/vijayee/WaveDB/tree/01c77e8b70f71de9b72480e73a3a179f6e93a009); `encryption.c:32-112,265-281`; `database_config.h:36-49,200-214` | Observed static source; not executed |
| `LIC-001` | Node binding carries MIT text; core/dependency closure remains open — publication **HOLD** | [`README.md:561-563`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/README.md#L561-L563); [`bindings/nodejs/LICENSE:1-20`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/bindings/nodejs/LICENSE#L1-L20); [`.gitmodules:1-12`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/.gitmodules#L1-L12) | Observed repository state; closure absent |
| `FIX-001` | Synthetic fixture is a finite input witness — **BOUND as input only** | Frozen `research.md` SHA-256 `1a5999...`; lines 270-490; `H_L=39ab1145...`; `sha256(C0)=2ccd199a...` | Unverified fixture design except independently recomputed L0/C0 hashes |
| `POST-001` | Projection/cache may advance only as a candidate-local experiment — **BOUND** | Frozen research lines 160, 201-224, 493-524 plus the three reviewer receipts and `evidence-closure.json` | Cross-source research recommendation |
| `POST-002` | Transactional sidecar is not admitted — **HOLD** | Frozen research lines 161, 206-233 plus reviewer receipts | Unverified design residue |
| `POST-003` | Canonical replacement is outside this route — **KILL** | Frozen research lines 162, 199, 201-224 plus Craft authority and WaveDB failure evidence | Route decision |

## Next decision

The next owner decision is binary and intentionally narrow: either admit WP-0 through WP-6 as an isolated, candidate-local projection experiment under the gates above, or stop. Do not broaden that admission into a transactional writer, a persistent Craft runtime, package publication, or canonical storage migration.

If admitted, the first evidence-producing step is WP-0: freeze the exact package/source correspondence, parser/serializer contract, `H_S`, both `H_P` values, `H_I`, and every key/value digest. Failure to close any one of those constants stops construction before WaveDB is installed or any Craft source is changed.
