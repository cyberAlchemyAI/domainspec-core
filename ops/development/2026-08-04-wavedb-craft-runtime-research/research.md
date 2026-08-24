# WaveDB/Craft runtime research

> Frozen explorer evidence. Each agent payload below is copied verbatim from the completed native subagent return. Synthesis, review, writing, and audit outputs are intentionally excluded.

## Agent 1

## Verbatim Research Return

### Immutable source identity

- Repository: `vijayee/WaveDB`
- Mutable ref inspected: `master`
- Resolved commit: [`01c77e8b70f71de9b72480e73a3a179f6e93a009`](https://github.com/vijayee/WaveDB/commit/01c77e8b70f71de9b72480e73a3a179f6e93a009), authored `2026-07-28T12:49:48Z`
- Access date: `2026-08-04`
- README Git blob: `cc11106438a926849ed91cac18a773ccae2fba19`, 19,725 bytes
- README SHA-256: `140880186286dc723118526d110075fe2520655cc112e4e9f694e15915c35095`
- Evidence ceiling: first-party static source inspection only. Nothing was installed, built, tested, benchmarked, or executed.

### Current-versus-roadmap matrix

| Capability | Static status at pinned commit | Candidate Craft use | Unverified boundary or gap |
|---|---|---|---|
| Hierarchical paths and scans | **Current/source-observed.** `path_t` is an ordered sequence of identifiers and raw delimited keys are parsed into components ([`path.h` L19-L57](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/HBTrie/path.h#L19-L57)). Iterators expose bounded forward/reverse scans and retain one `read_txn_id` ([`database_iterator.h` L31-L55](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database_iterator.h#L31-L55)). | Could encode workspace/row/index namespaces and rebuild derived views through bounded scans. | Encoding, escaping, ordering, maximum depth/size, and round-trip behavior for actual Craft identifiers need fixture tests. |
| Batch writes and atomicity | **Current mechanism; strong atomicity not established.** A batch is documented as one WAL entry and one transaction ID ([`batch.h` L30-L35](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/batch.h#L30-L35)). Submission serializes one `WAL_BATCH`, applies operations sequentially, then commits ([`database.c` L2931-L3064](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database.c#L2931-L3064)). | Could atomically refresh a rebuildable projection or related derived indexes on the normal success path. | No executed failure witness. Mid-apply errors have no explicit rollback in this function. Recovery skips malformed batch sub-entries, applies the valid remainder, and later advances visibility ([`wal_manager.c` L1646-L1737](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/wal_manager.c#L1646-L1737), [`L1865-L1873`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/wal_manager.c#L1865-L1873)). Craft must not assume corruption-safe all-or-nothing recovery. No compare-and-swap or stale-ledger-digest guard was found. |
| MVCC and snapshots | **Current, with two distinct meanings.** Point reads select the latest committed transaction at call time ([`database.c` L2587-L2604](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database.c#L2587-L2604)); a scan fixes its visibility ID when opened. `database_snapshot()` is instead a WAL flush, MVCC GC, and persistence checkpoint ([`database.c` L1890-L1931](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database.c#L1890-L1931)). | A single scan could support a consistent derived export. | There is no public general transaction/read-snapshot handle spanning arbitrary gets plus scans. README wording about “snapshot isolation” must not be equated with `database_snapshot()`. Core tests declare snapshot-isolation cases, but were not run. |
| WAL and crash durability | **Current/source-observed, not execution-proven.** Modes are IMMEDIATE, DEBOUNCED, and ASYNC ([`wal.h` L58-L60](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/wal.h#L58-L60)). Code fsyncs every immediate flush, delays debounced fsync, and performs no fsync for ASYNC ([`wal_manager.c` L263-L299](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/wal_manager.c#L263-L299)). Recovery scans files, CRC-checks entries, sorts transaction IDs, and replays them ([`L1475-L1627`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/wal_manager.c#L1475-L1627)). | Could make a sidecar projection recoverable after process restart. | README process-crash/power-loss statements remain unexecuted claims. Partial/torn/corrupt input handling, directory fsync, acknowledgement timing, recovery idempotence, and recovery atomicity require destructive harnesses. ASYNC expressly has no power-loss guarantee. |
| Subtrees | **Current/source-observed.** Subtrees prepend prefixes and keep the database referenced ([`database_subtree.h` L24-L48](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database_subtree.h#L24-L48)); CRUD, batches, snapshot delegation, counts, and scans are exposed. CMake registers subtree and close-crash tests ([`CMakeLists.txt` L349-L373](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/CMakeLists.txt#L349-L373)). | Could provide logical per-workspace or per-view namespaces. | Prefix isolation is not authorization or a security boundary; root database access can cross namespaces. Tests were not run. |
| Graph and GraphQL layers | **Current/source-observed.** Graph creation, triple insertion, DSL execution, and schema parsing are public APIs ([`graph.h` L57-L66](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Layers/graph/graph.h#L57-L66), [`L134-L156`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Layers/graph/graph.h#L134-L156)). GraphQL exposes layer creation, SDL parsing, and synchronous queries ([`graphql.h` L46-L73](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Layers/graphql/graphql.h#L46-L73), [`L128`](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Layers/graphql/graphql.h#L128)). Tests are registered in CMake. **SQL is roadmap**, as is P2P replication ([`README.md` L556-L559](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/README.md#L556-L559)). | Graph could index derived Craft links; GraphQL could provide a read façade. | Neither layer supplies Craft schema authority, receipt semantics, or canonical relation ownership. Their query correctness and coexistence were not executed. |
| Node.js binding | **Current source package, maturity HOLD.** Package metadata names `@vijayee/wavedb` version `0.15.8`, builds during install, and runs Mocha after rebuilding ([`package.json` L1-L29](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/bindings/nodejs/package.json#L1-L29)). | This is the most plausible adapter surface for a JavaScript Craft runtime. | Root and binding READMEs say `npm install wavedb`, contradicting the scoped package name ([`README.md` L351-L356](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/README.md#L351-L356)). Core CMake version is `0.1.15` while Node is `0.15.8`. `IMPLEMENTATION_STATUS.md` claims production readiness while `KNOWN_ISSUES.md` records snapshot/version-chain limitations ([`KNOWN_ISSUES.md` L10-L48](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/bindings/nodejs/KNOWN_ISSUES.md#L10-L48)). No build, package publication, platform compatibility, or test result was verified. |
| Encryption and keys | **Partly current/source-observed.** AES-GCM code exists, persisted pages call encryption, WAL manager receives the encryption context, and key bytes are cleansed at destruction ([`encryption.c` L32-L112](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Storage/encryption.c#L32-L112), [`page_file.c` L336-L349](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Storage/page_file.c#L336-L349)). Config states that key material is not persisted, only salt/check ([`database_config.h` L36-L49](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database_config.h#L36-L49)). | Symmetric encryption could protect a rebuildable local projection if external key custody is supplied. | Encryption is immutable after creation; no rotation API was found. Asymmetric reopen is source-inconsistent: `encryption_create_from_config` requires a 32-byte raw key before its asymmetric branch ([`encryption.c` L265-L281](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Storage/encryption.c#L265-L281)), while public asymmetric config exposes DER keys, not that DEK ([`database_config.h` L200-L214](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database_config.h#L200-L214)). Reopen, write-only nodes, key loss, and rotation remain HOLD pending execution and owner clarification. |
| Build, tests, dependencies | **Declaratively current.** README commands are recursive clone, CMake, `make`, and `ctest` ([`README.md` L509-L524](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/README.md#L509-L524)). CMake defaults tests on and registers MVCC, WAL, batch, encryption, subtree, GraphQL, and Graph targets. Pinned gitlinks are googletest `94be250…`, hashmap `f64faee…`, libcbor `d638af0…`, and xxhash `82cead7…` ([`.gitmodules` L1-L12](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/.gitmodules#L1-L12)). OpenSSL is optional at build time, with encryption stubs otherwise ([`CMakeLists.txt` L184-L208](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/CMakeLists.txt#L184-L208)). | Supplies a candidate native dependency path. | No command was run. Toolchain/platform requirements, ABI stability, installation reproducibility, and transitive-license review remain open. “No external dependencies” in README is imprecise given submodules, Threads, Node build dependencies, and optional OpenSSL. |
| Performance | **README-only author-reported measurement.** The README pins hardware, OS, cache, compiler, ASYNC WAL, and reported throughput ([`README.md` L485-L506](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/README.md#L485-L506)); benchmark source files exist. | Numbers may inform later hypotheses only. | Not reproduced, not a Craft workload, and measured in the least durable WAL mode. No performance claim should enter the Craft architecture as evidence. |
| MIT licensing | **Mixed/HOLD.** README states MIT ([`README.md` L561-L563](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/README.md#L561-L563)); the Node binding contains a full MIT license ([`bindings/nodejs/LICENSE` L1-L20](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/bindings/nodejs/LICENSE#L1-L20)). | Potentially permits a packaged adapter. | The pinned repository tree has no root `LICENSE` file, so the core-library license is README-only. Publication requires owner/legal confirmation plus dependency-license closure. |

### Source-bound verdict

WaveDB is credible enough for a finite **projection/cache or non-authoritative sidecar prototype**, especially through hierarchical keys, stable scans, batches, subtrees, and the Node native binding. Static evidence does not support making it Craft’s canonical store or relying on it for authoritative transactional mutation. The minimum gating witnesses are batch crash/corruption atomicity, concurrent stale-source rejection, scan consistency, reopen/recovery, symmetric key failure, asymmetric reopen, package installation identity, round-trip projection rebuild, and root-license closure.

## Receipt Fields

- `status`: `pass`
- `validation`: `pass`
- `artifacts`: `["receipts/explorer-wavedb-source.json"]`
- `blockers`: `[]` — research action completed; the HOLD items above block stronger architecture claims, not this return.
- `started_at`: `parent-bound persisted spawn timestamp; not exposed to native helper`
- `finished_at`: `2026-08-04T17:03:05Z`
- `handoff_note`: Pinned WaveDB at commit `01c77e8…`; static source supports a bounded projection/sidecar investigation, while canonical-store use, strong recovery atomicity, asymmetric key behavior, install identity, runtime performance, and core licensing remain unproven. No execution evidence or file mutation occurred.

## Agent 2

## Verbatim Research Return

### Authority and claim ceiling

Canonical authority is `arcanum/arcana/craft/`; both named `arcanum/development/craft/` documents are historical evidence only, not `$craft` runtime authority (`arcanum/arcana/craft/SKILL.md:33-53`, `ARCHITECTURE.md:39-53`).

The current contract is unequivocal:

- `.craft/ledger.yml` is the sole project-local source of truth.
- `CRAFT.md` and `.craft/index.json` are rebuildable derived views.
- Called capabilities retain ownership of their native artifacts, validation, and verdicts.
- Craft currently ships no command runner, renderer, index builder, row updater, public CLI, library, or generated adapter.

Selectors: `SKILL.md:56-71,312-316`; `README.md:27-39`; `ARCHITECTURE.md:55-79,241-261`.

All WaveDB operations below are candidate adapter mappings. They depend on the external explorer verifying exact WaveDB `put/get/batch/scan/snapshot` behavior; they are not claims that those guarantees have been proven.

### Invariants

1. **Authority:** Database rows cannot supersede YAML unless a separate Craft-owner route changes every affected canonical contract. A digest mismatch makes all database state stale.
2. **Stable identity:** Every ordinary row retains its canonical ID; recomposition uses `(child_id,parent_id)`. References must resolve, and links retain `{label,target,kind}` rather than being collapsed into database graph edges. Selectors: `ledger-core.schema.yml:18-34,313-358,735-771,773-845`.
3. **Workspace binding:** Filesystem discovery and user-scope disambiguation precede every database lookup or mutation. Database namespace discovery cannot silently select a workspace. Selector: `SKILL.md:129-149`.
4. **Lifecycle:** Raw/typed blockers cannot become resolved directly; human-required closure needs owner/decision/human evidence; blocking decisions stop dependent work; child closure requires recomposition evidence. Selectors: `SKILL.md:181-227,257-261`; `ledger-core.schema.yml:194-257,670-771`.
5. **Indexes:** Required indexes are `by_id`, `open_decisions`, `blocking_decisions`, `active_blockers`, `active_gaps`, `next_moves`, and `artifacts_by_path`. Generated indexes point to source IDs/selectors and carry `ledger_sha256`; they do not copy authoritative row content. Selector: `index.schema.yml:18-42,44-169`.
6. **Derived views:** `CRAFT.md` must retain anchors/links and quick links. It never writes back. Selectors: `SKILL.md:91-100`; `product-launch-CRAFT.md:3-12,68-83`.
7. **Route evidence:** Craft records paths, status, evidence references, and receipts without rewriting the called capability’s payload or verdict. Route-shape evidence is not execution proof. Selectors: `SKILL.md:188-203,312-316,363-375`.
8. **Schema ceiling:** Route exchange, projections, row updates, validation reports, and artifact manifests are deferred schemas. Full database row copies are therefore a new projection surface, not an existing generated-index behavior. Selectors: `ledger.schema.yml:24-47,934-955`; `ARCHITECTURE.md:168-180`.
9. **Validation:** Canonical validation remains against YAML and its schemas. A successful database read, batch, snapshot, WAL recovery, or graph traversal is neither Craft validation nor evidence of promotion.

### Candidate hierarchical namespace

Use a distinct derived generation for each authoritative ledger digest:

```text
/craft/v1/workspaces/<W>/
  meta/scope-path
  meta/source-ledger
  meta/schema-version
  meta/active-generation
  generations/<ledger-sha256>/
    rows/contexts/<context-id>
    rows/artifacts/<artifact-id>
    rows/descriptions/<description-id>
    rows/definitions/<definition-id>
    rows/gaps/<gap-id>
    rows/relations/<relation-id>
    rows/typed-items/<item-id>
    rows/decisions/<decision-id>
    rows/recomposition/<E(child-id)>~<E(parent-id)>
    indexes/by-id/<E(row-id)>
    indexes/open-decisions/<E(decision-id)>
    indexes/blocking-decisions/<E(decision-id)>
    indexes/active-blockers/<E(item-id)>
    indexes/active-gaps/<E(gap-id)>
    indexes/next-moves/<E(context-id)>
    indexes/artifacts-by-path/<sha256(path)>
    indexes/reverse-links/<E(target)>/<E(source-id)>
    indexes/evidence-refs/<sha256(evidence-ref)>/<E(source-id)>
```

`W` should be a digest of the normalized repository-relative Craft scope, with the unhashed path retained as metadata. `E` is deterministic UTF-8 base64url encoding. Each row value preserves the complete schema row plus family and stable ID; index values contain selectors/IDs only. `meta/active-generation` is a cache pointer, never authority, and is usable only when it matches the current YAML digest.

### Row-family mapping

| Canonical family | Candidate key/value rule | Selector |
|---|---|---|
| `contexts` | ID-keyed row; preserve parent, stage, gate, next move, artifacts, links | `ledger-core.schema.yml:314-358` |
| `artifacts` | ID-keyed metadata; preserve owner, path, type, status; native bytes remain filesystem-owned | `ledger-core.schema.yml:360-390` |
| `descriptions` | ID-keyed versioned descriptions; never overwrite history | `ledger-core.schema.yml:392-419` |
| `definitions` | ID-keyed; preserve local/candidate status and owner-promotion boundary | `ledger-core.schema.yml:421-453,819-821` |
| `gaps` | ID-keyed with scope, severity, treatment, owner, status, evidence | `ledger-core.schema.yml:455-497` |
| `relations` | Preserve explicit relation row; reverse-link indexes are derived and do not replace it | `ledger-core.schema.yml:499-555` |
| `typed_items` | ID-keyed blockers/gates/enablers with lifecycle, lanes, roles, closure, evidence | `ledger-core.schema.yml:556-668` |
| `decisions` | ID-keyed; batch changes with affected blocker/index rows | `ledger-core.schema.yml:670-733` |
| `recomposition` | Composite encoded key; preserve residue, evidence, status, next parent move | `ledger-core.schema.yml:735-771` |

`route_handoffs` and `receipts` appear in an example (`product-launch-ledger.yml:241-258`), but their schema layer is explicitly deferred (`ledger-core.schema.yml:526-541`; `ledger.schema.yml:947-949`). Until that layer exists, WaveDB may carry those YAML sections opaquely for round-trip preservation, while queryable route evidence remains artifact rows referencing native handoff/receipt files (`product-launch-ledger.yml:99-110`). It must not reinterpret native receipt contents.

### Operation mapping

| Craft operation | Candidate database operations | Mandatory authority guard |
|---|---|---|
| `start_project` | After filesystem scope resolution and YAML creation, one `batch` creates the digest generation and indexes | Database cannot establish the workspace or root ledger |
| `state` | Hash YAML; `get` matching generation metadata; `get` selected rows/indexes or `scan` the workspace prefix under a consistent `snapshot` | On missing/mismatched digest, ignore database and rebuild |
| `describe`, `add_blocker`, `add_enabler`, `add_gap`, `add_definition`, `open_child_context`, `link` | Projection posture: YAML commit first, then `batch` the new generation. Sidecar posture: `snapshot` expected digest, stage affected rows/indexes with `batch` | No canonical success before YAML is atomically committed and validated |
| `refine_blocker`, `open_decision`, `decide` | `get` affected rows at a snapshot; `batch` row plus blocker/decision/index deltas | Enforce lifecycle and human/owner evidence from canonical rules |
| `next` | `batch` the context row and `next_moves` entry | YAML value remains decisive |
| `recompose` | One staged `batch` for recomposition, parent next move, links, and indexes | Child closure remains blocked until committed YAML contains valid evidence |
| `validate` | Validate YAML first; use `snapshot`/`scan` only to compare projected rows, references, and indexes against that digest | Database validation alone cannot return Craft pass |
| Index rebuild | `snapshot` one immutable generation; derive index records; `batch` them and stamp the same digest | Never mix generations |
| `export_ledger` | Read YAML directly or a digest-matched immutable generation; regenerate anchors/quick links | Never accept `CRAFT.md` writeback |

Canonical method selectors: `SKILL.md:152-265,319-340`.

### Derived index and `CRAFT.md` flow

1. Resolve the owning filesystem workspace.
2. Read exact YAML bytes; compute SHA-256.
3. Parse and validate source rows, references, lifecycles, and required indexes.
4. Build a new immutable WaveDB generation from that parsed model.
5. Derive `.craft/index.json` with schema version, YAML digest, generation time, generator version, source path, selectors, and freshness status.
6. Render `CRAFT.md` from the same model with stable anchors and quick links.
7. Re-read YAML digest before publishing outputs; on mismatch, discard and retry.
8. Record an adapter receipt containing source path/digest, adapter version, generation key, generated artifact hashes, validation result, and residue. The receipt is evidence, not authority.

### Exact posture deltas

| Posture | Required delta | Verdict |
|---|---|---|
| **Projection/cache only** | Add a projection schema, WaveDB adapter/builder, deterministic fixture, stale-digest behavior, generated-index/Markdown generation if in scope, and documentation identifying the optional cache path. Canonical YAML policies remain unchanged. | **Acceptable candidate.** Smallest authority-preserving posture. |
| **Transactional sidecar; YAML authority** | Everything above plus row-update/validation/receipt schemas, expected-digest compare-and-swap, filesystem lock/atomic replace, crash recovery, idempotent transaction states, concurrency tests, and a runtime adapter/CLI owner. Stage in WaveDB, render and validate complete YAML, atomically replace only if the original digest still matches, then rebuild the database from committed YAML. A crash before YAML replacement has no canonical effect; a crash afterward leaves only a stale/rebuildable sidecar. | **HOLD pending design and owner approval.** Viable only with this commit protocol; naïve dual-write is rejected. |
| **WaveDB canonical-store replacement** | Change `SKILL.md`, README, architecture, source/index schemas, examples, storage contract, validation, export semantics, workspace portability, migration/downgrade, backup/recovery, concurrency, corruption handling, encryption/key ownership, packaging, licensing, and promotion evidence. YAML becomes an explicit derived export. | **Reject by assumption / HOLD for a separate Craft-owner governance route.** Current research cannot authorize it. |

Rejected collapses: database equals ledger; WAL equals Craft event history; snapshot equals receipt; graph edge equals canonical relation; namespace equals authority scope; generated index equals source truth; successful runtime behavior equals promotion; derived-view writeback; stale database mutation; or rewriting a called capability’s artifacts.

Historical evidence only: recursive command-backed Refine attempts timed out without artifacts (`CRAFT-REFINE-RUNTIME-STRATEGY.md:3-26`), motivating bounded orchestrator-owned stages (`:28-90`) while remaining a flagged candidate (`:146-149`). The runtime design itself states it defines boundaries but implements nothing (`CRAFT-RUNTIME-DESIGN.md:16-20`). These support bounded adapter stages and explicit receipts; they do not support WaveDB authority.

## Receipt Fields

- status: `pass`
- validation: `pass`
- artifacts:
  - `receipts/explorer-craft-contract.json`
- blockers: `[]`
- started_at: `2026-08-04T16:52:00Z`
- finished_at: `2026-08-04T16:59:29Z`
- handoff_note: Canonical Craft permits a digest-bound rebuildable WaveDB projection without authority change. A transactional sidecar requires an explicit YAML compare-and-swap and recovery contract; canonical-store replacement requires a separate Craft-owner route. External WaveDB API guarantees remain to be bound from the empirical explorer. No files were edited or written.

## Agent 3

## Verbatim Research Return

### Evidence boundary

WaveDB was pinned to commit [`01c77e8b70f71de9b72480e73a3a179f6e93a009`](https://github.com/vijayee/WaveDB/commit/01c77e8b70f71de9b72480e73a3a179f6e93a009), dated 2026-07-28. Raw SHA-256: README `140880186286dc723118526d110075fe2520655cc112e4e9f694e15915c35095`; Node package manifest `82e87aaaac10113cb1294732bf149356f6f7df76ecde0259181999c6a3fe9dc3`.

Canonical Craft fixes these invariants:

- `.craft/ledger.yml` is the sole project-local source of truth; `CRAFT.md` and `.craft/index.json` are rebuildable views ([SKILL.md](/home/vrondelli/projects/domainspec-core/arcanum/arcana/craft/SKILL.md:33), [ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/arcanum/arcana/craft/ARCHITECTURE.md:55)).
- Workspace selection precedes mutation; stable IDs, references, required indexes, residue, and recomposition evidence must survive.
- Called capabilities retain ownership of native artifacts and verdicts; database state or a WAL entry cannot substitute for a Craft receipt.
- Craft currently ships no database adapter, public CLI, row updater, renderer, or generated index builder ([ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/arcanum/arcana/craft/ARCHITECTURE.md:245)).
- Historical orchestrator-first guidance is failure evidence, not runtime authority; it requires bounded stages and an artifact or blocked reason per stage ([CRAFT-REFINE-RUNTIME-STRATEGY.md](/home/vrondelli/projects/domainspec-core/arcanum/development/craft/CRAFT-REFINE-RUNTIME-STRATEGY.md:7)).

Therefore:

- **Projection/cache:** viable for a bounded prototype if it is disposable, digest-bound, and rebuilt only from validated YAML.
- **“Transactional sidecar” with YAML authority:** **HOLD** if it implies peer dual-write. It is acceptable only when every database state remains a post-YAML derived generation.
- **WaveDB canonical replacement:** **KILL for this route.** It changes Craft authority and needs a separate Craft-owner contract/schema/runtime/publication route.

### Failure-mode table

| Event | Pressure-test finding | Required response | Verdict |
|---|---|---|---|
| Bootstrap/import | There is no current Craft adapter or round-trip proof. | Validate YAML first; import into a fresh generation; store source digest, Craft schema, adapter version, WaveDB revision, row counts, and deterministic export hash. Never overwrite the only ledger. | HOLD until fixture passes |
| Steady-state mutation | YAML and WaveDB cannot share one atomic commit. Peer dual-write creates split-brain. | Commit and validate YAML first; refresh WaveDB afterward. If refresh fails, mark cache stale and continue from YAML. | KILL peer dual-write |
| Individual WAL failure | Current put/delete paths log WAL failures but continue applying and return success ([database.c lines 2410–2530](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database.c#L2410-L2530)). | Do not use WaveDB acknowledgements as canonical Craft durability evidence. | KILL canonical replacement |
| Concurrent writes | MVCC and sharded locks exist in-process, but no verified cross-process writer lease was found. | Adapter must enforce one workspace writer and compare the expected ledger digest immediately before YAML commit. | HOLD multi-writer use |
| Concurrent reads / snapshot | Each get reads the latest committed transaction ID, but no Node read-transaction/snapshot handle proves a stable multi-key Craft read. `database_snapshot()` is a persistence/GC checkpoint, not a retained read snapshot. | Bind reads to a stored ledger epoch/digest; retry or block if it changes. | HOLD snapshot-dependent claims |
| Batch failure | A normal batch is one WAL record and becomes visible after commit, but its apply loop has no compensating rollback if an operation fails after earlier operations were inserted ([database.c lines 2931–3064](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database.c#L2931-L3064)). | Require failure injection and reopen tests; never infer cross-YAML atomicity from WaveDB batch atomicity. | HOLD |
| Process crash | WAL replay exists, but repository status documents conflict about close-time snapshots. Current persistence tests weaken overwrite/delete assertions, accepting old or null values in cases that require exactness ([persistence test](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/bindings/nodejs/test/persistence.test.js#L50-L75)). | Require exact crash/reopen assertions against a pinned package before relying on recovery. Projection may instead rebuild from YAML. | HOLD |
| Power loss | README explicitly limits ASYNC mode and exposes a debounce loss window ([README](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/README.md#L129-L146)). | No power-durability claim without IMMEDIATE mode plus destructive power-loss evidence. | KILL ASYNC/DEBOUNCED durability claim |
| Stale cache | A valid database may reflect an older YAML digest. | Every read checks `source_ledger_sha256`; mismatch blocks database use and triggers rebuild. | Mandatory |
| WAL corruption | Partial headers, payloads, CRC failures, and decryption failures stop file reading but return the valid prefix as success ([wal_manager.c lines 320–432](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/wal_manager.c#L320-L432)). Recovery then continues and can skip malformed entries. | Treat any corruption as fail-closed; quarantine the generation and rebuild from YAML. | KILL in-place “successful recovery” |
| Schema upgrade | Craft schema is `0.3.0`; no Craft↔WaveDB migration matrix exists. WaveDB config writes version 1 but load does not enforce that version. | Versioned adapter plus forward/backward fixture for every supported pair. | HOLD |
| WaveDB legacy upgrade | Its legacy-WAL migration renames a backup but explicitly does not replay old entries before marking migration complete ([wal_manager.c lines 785–940](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/wal_manager.c#L785-L940)). | Reject legacy stores or require an upstream-fixed, tested migration. | KILL affected upgrade |
| Rollback/downgrade | No compatible downgrade contract is established. | Close writer, retain YAML, disable/quarantine cache generation, rebuild views. Never reverse-apply database state into YAML. | Projection rollback only |
| Database corruption | Page/WAL checksums exist, but recovery is not consistently fail-closed. | Preserve corrupted bytes and diagnostics; rebuild a new generation from authoritative YAML. | No in-place repair claim |
| Rebuild | Rebuild is safe only if YAML validates and artifacts remain owned externally. | Deterministic import/export hashes, reference checks, indexes, and `CRAFT.md` regeneration receipt. | Required acceptance |
| Key loss | Key material is not persisted; a lost symmetric/private key makes encrypted state unavailable. | Recovery must be “rebuild from YAML with a replacement key,” subject to source-data availability. | KILL “recover encrypted DB” claim |
| Key rotation | README calls asymmetric mode suitable for rotation, but encryption is immutable after creation and no verified rotate operation exists. | New encrypted generation plus verified export/import; security approval required. | HOLD |
| Workspace deletion | Prefix deletion scans and deletes keys one by one, so failure can leave partial deletion ([database_subtree.c lines 73–105](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database_subtree.c#L73-L105)). A subtree is namespace convenience, not an authority boundary. | Tombstone generation manifest first; retain rollback evidence; perform physical deletion only through an explicit destructive owner route. | KILL direct deletion |
| Public installation | README says `npm install wavedb`, but that registry name is an unrelated package. The repository package is `@vijayee/wavedb@0.15.8`. It runs a native `node-gyp` install build and ships vendored C sources. | Use exact scoped name and tarball integrity; test supported OS/Node/toolchain/OpenSSL; produce SBOM and license inventory. | KILL unscoped install; HOLD publication |

### Migration, recovery, and rollback contract

1. **Preflight:** resolve one Craft workspace; acquire a single-writer lease; validate ledger schema, IDs, links, indexes, and artifacts; capture ledger SHA-256 and immutable backup; pin WaveDB source/package integrity and platform.
2. **Build generation:** create a sibling temporary database, never inside or over the only canonical ledger. Import one normalized YAML epoch and store metadata `{ledger_sha256, craft_schema_version, adapter_version, wavedb_commit, package_integrity, import_id}`.
3. **Verify:** export every canonical row family, compare normalized hashes, rebuild required indexes and `CRAFT.md`, test wrong workspace and stale digest, then close/reopen and compare exact values.
4. **Activate:** atomically switch only a small cache-generation manifest after verification. YAML authority does not move.
5. **Mutate:** lock → read/validate YAML at digest E0 → prepare change → durable YAML temp/rename → validate E1 → refresh database generation from E1 → emit mutation receipt. Database failure after E1 means “Craft committed, cache stale,” not rollback.
6. **Recover:** on startup, any digest/version mismatch or WaveDB error disables the cache. Corruption, missing keys, or incomplete recovery causes quarantine and clean rebuild.
7. **Rollback:** stop writers, verify YAML, disable the active cache generation, rebuild derived views, and record a rollback receipt. Restoring older YAML requires a separate owner-approved compensation/restore decision.

Required receipts are `migration`, `mutation`, `recovery`, and `rollback`, each carrying before/after ledger digests, schema and adapter versions, WaveDB identity, package integrity, operation counts, exact validation results, durability mode, platform, timestamps, and residue. WaveDB WAL/MVCC state is never itself a Craft receipt.

### Security, licensing, packaging, and owner gates

- **Craft owner:** posture selection; adapter/runtime/schema changes; deletion semantics; any change to canonical authority.
- **Security owner:** data classification, file permissions, encryption mode, key custody/backup/rotation, corruption fail-closed behavior, native-addon supply chain, and crash/power-loss test authorization.
- **Licensing owner:** MIT notice inclusion plus license/SBOM review for bundled OpenSSL, libcbor, xxHash, hashmap, and generated package contents. The Node binding carries an MIT license, but repository README wording alone is insufficient for dependency clearance.
- **Publication owner:** scoped package name, reproducible tarball/integrity, supported platform matrix, install-time native build policy, public/private scan, and explicit claim ceiling.
- **WaveDB maintainer or bounded fork owner:** WAL error propagation, corruption signaling, legacy migration, snapshot semantics, exact persistence tests, and key-rotation behavior.

Explicit **KILL** conditions: WaveDB or a derived graph/index becomes authoritative without Craft-owner approval; peer YAML/database dual-write; cache read on digest mismatch; multi-process writers without a lease; unscoped `wavedb` installation; power-durability claims under ASYNC/DEBOUNCED; corrupted-WAL recovery accepted without exact completeness proof; database-to-YAML rollback; destructive prefix deletion without owner approval.

Explicit **HOLD** conditions: unresolved exact crash/reopen fixture, unsupported schema pair, missing round-trip hash, absent key-recovery plan, unverified platform/native build, incomplete dependency licensing, or a missing migration/recovery receipt.

Claim ceiling: source-reviewed candidate architecture only. No package was installed, no build or destructive test was run, and no runtime, durability, security, publication, promotion, or production claim is established.

## Receipt Fields

- status: `pass`
- validation: `pass`
- artifacts:
  - `receipts/explorer-lifecycle-failure.json`
- blockers: `none for the research return; implementation remains gated by the KILL/HOLD conditions above`
- started_at: `2026-08-04T16:43:00Z`
- finished_at: `2026-08-04T17:01:54Z`
- handoff_note: `Synthesis should retain WaveDB only as a disposable, ledger-digest-bound projection candidate; HOLD any transactional-sidecar wording that implies dual authority, and KILL canonical replacement under the current Craft contract. Prioritize WAL error propagation, corruption fail-closed behavior, exact crash/reopen assertions, scoped package installation, and key lifecycle as prototype gates.`

## Agent 4

## Verbatim Research Return

Verdict: use WaveDB only as a rebuildable, workspace-scoped projection for this prototype. `.craft/ledger.yml` remains authoritative; database rows, indexes, checkpoints, receipts, and `CRAFT.md` remain derived. The plan targets WaveDB commit `01c77e8b70f71de9b72480e73a3a179f6e93a009`.

WaveDB’s pinned Node interface verifies string/array paths, string/Buffer values, `put`, `get`, `batch`, and bounded read streams. Subtrees verify prefix isolation, synchronous batch, prefix scan, and `snapshot()`. However, `snapshot()` flushes WAL, performs MVCC GC, and persists pages; it is not a historical read handle. Scan iterators separately capture a read transaction when created. The batch implementation uses one transaction, but its operation-failure branch shows no explicit rollback of already-applied operations, so failure atomicity remains a hypothesis requiring the partial-batch control below. [Node API](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/bindings/nodejs/lib/wavedb.js#L138-L268), [subtree API](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/bindings/nodejs/lib/subtree.js#L58-L111), [checkpoint implementation](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database.c#L1890-L1931), [batch implementation](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database.c#L2931-L3064), [iterator MVCC capture](https://github.com/vijayee/WaveDB/blob/01c77e8b70f71de9b72480e73a3a179f6e93a009/src/Database/database_iterator.c#L792-L873).

Synthetic authoritative fixture, UTF-8, LF endings, one terminal newline:

```yaml
ledger_id: craft.fixture.wavedb.runtime
schema_ref: "[repo-root]arcanum/arcana/craft/templates/ledger.schema.yml"
schema_version: 0.3.0
status: candidate-local
source_of_truth: .craft/ledger.yml
human_view: CRAFT.md
indexes:
  by_id:
    CTX-WAVEDB-ROOT: contexts[0]
    CTX-WAVEDB-CHILD: contexts[1]
    ART-WAVEDB-LEDGER: artifacts[0]
    ART-WAVEDB-VIEW: artifacts[1]
    ART-WAVEDB-RECEIPT: artifacts[2]
    DESC-WAVEDB-001: descriptions[0]
    BLK-WAVEDB-RAW-001: typed_items[0]
    BLK-WAVEDB-REFINED-001: typed_items[1]
    DEC-WAVEDB-STORE-001: decisions[0]
    GAP-WAVEDB-RECOVERY-001: gaps[0]
  open_decisions: []
  blocking_decisions: []
  active_blockers:
    - BLK-WAVEDB-RAW-001
    - BLK-WAVEDB-REFINED-001
  active_gaps:
    - GAP-WAVEDB-RECOVERY-001
  next_moves:
    - context_id: CTX-WAVEDB-ROOT
      next_move: Refine BLK-WAVEDB-RAW-001, then run the recovery fixture.
    - context_id: CTX-WAVEDB-CHILD
      next_move: Recompose RECEIPT-WAVEDB-001 into CTX-WAVEDB-ROOT.
  artifacts_by_path:
    .craft/ledger.yml: ART-WAVEDB-LEDGER
    CRAFT.md: ART-WAVEDB-VIEW
    receipts/wavedb-fixture.json: ART-WAVEDB-RECEIPT
contexts:
  - context_id: CTX-WAVEDB-ROOT
    parent_id: root
    title: WaveDB projection fixture
    purpose: Test a rebuildable runtime projection without changing Craft authority.
    stage: plan
    gate: block
    next_move: Refine BLK-WAVEDB-RAW-001, then run the recovery fixture.
    owned_artifacts: [ART-WAVEDB-LEDGER, ART-WAVEDB-VIEW]
    links:
      - {label: Raw blocker, target: BLK-WAVEDB-RAW-001, kind: row-id}
      - {label: Refined blocker, target: BLK-WAVEDB-REFINED-001, kind: row-id}
      - {label: Recovery gap, target: GAP-WAVEDB-RECOVERY-001, kind: row-id}
  - context_id: CTX-WAVEDB-CHILD
    parent_id: CTX-WAVEDB-ROOT
    title: Adapter-boundary review
    purpose: Select the authority-preserving adapter posture.
    stage: closed
    gate: pass
    next_move: Recompose RECEIPT-WAVEDB-001 into CTX-WAVEDB-ROOT.
    owned_artifacts: [ART-WAVEDB-RECEIPT]
    links:
      - {label: Fixture receipt, target: ART-WAVEDB-RECEIPT, kind: artifact-id}
artifacts:
  - {artifact_id: ART-WAVEDB-LEDGER, owner_context_id: CTX-WAVEDB-ROOT, path: .craft/ledger.yml, artifact_type: ledger-source, status: active}
  - {artifact_id: ART-WAVEDB-VIEW, owner_context_id: CTX-WAVEDB-ROOT, path: CRAFT.md, artifact_type: human-view, status: active}
  - {artifact_id: ART-WAVEDB-RECEIPT, owner_context_id: CTX-WAVEDB-CHILD, path: receipts/wavedb-fixture.json, artifact_type: execution-receipt, status: pass}
descriptions:
  - description_id: DESC-WAVEDB-001
    context_id: CTX-WAVEDB-ROOT
    description: WaveDB is a digest-guarded projection; YAML remains the sole source of truth.
    status: active
    evidence: ART-WAVEDB-LEDGER
typed_items:
  - item_id: BLK-WAVEDB-RAW-001
    kind: blocker
    base_type: definition_blocker
    primary_lane: blocker_refiner
    source_id: CTX-WAVEDB-ROOT
    target_id: CTX-WAVEDB-ROOT
    status: active
    refinement_status: raw
    closure_condition: Define and approve the deterministic row-value codec.
    evidence: ART-WAVEDB-LEDGER
    reason: Encoding ambiguity prevents reproducible hashes.
  - item_id: BLK-WAVEDB-REFINED-001
    kind: blocker
    base_type: validation_blocker
    primary_lane: validator
    source_id: CTX-WAVEDB-ROOT
    target_id: CTX-WAVEDB-ROOT
    status: active
    refinement_status: refined
    default_role: validator
    allowed_roles: [validator, auditor]
    delegation_route: task-session
    requires_human: false
    role_confidence: candidate
    owner_ref: validator
    closure_condition: Crash/reopen and partial-batch receipts preserve every pre-batch or post-batch hash with no hybrid state.
    evidence: ART-WAVEDB-RECEIPT
    decision_ref: DEC-WAVEDB-STORE-001
    reason: Runtime usefulness depends on falsifiable recovery behavior.
decisions:
  - decision_id: DEC-WAVEDB-STORE-001
    scope_id: CTX-WAVEDB-CHILD
    decision_type: selection
    question: What authority posture may the prototype use?
    description: Select a rebuildable WaveDB projection guarded by the current YAML digest.
    options: [yaml-authority-wavedb-projection, transactional-sidecar, wavedb-authority]
    default_option: yaml-authority-wavedb-projection
    selected: yaml-authority-wavedb-projection
    rationale: It exercises runtime APIs without transferring canonical ownership.
    evidence: ART-WAVEDB-RECEIPT
    status: closed
    blocking: false
    impact: Any stale or damaged projection is discarded and rebuilt from YAML.
    owner: craft
gaps:
  - gap_id: GAP-WAVEDB-RECOVERY-001
    scope_id: CTX-WAVEDB-ROOT
    summary: Crash, corruption, and concurrent-writer behavior have not been executed.
    severity: block
    treatment: plan
    owner: validator
    status: active
    evidence: ART-WAVEDB-RECEIPT
receipts:
  - receipt_id: RECEIPT-WAVEDB-001
    context_id: CTX-WAVEDB-CHILD
    route: task-session
    status: pass
    evidence: [ART-WAVEDB-RECEIPT]
    validation_result: Synthetic fixture confirms the selected adapter boundary; it is not WaveDB runtime proof.
recomposition:
  - child_id: CTX-WAVEDB-CHILD
    parent_id: CTX-WAVEDB-ROOT
    summary: The child selected YAML authority with a rebuildable WaveDB projection.
    evidence: ART-WAVEDB-RECEIPT
    residue: Recovery and deterministic-codec blockers remain active.
    next_parent_move: Refine BLK-WAVEDB-RAW-001, then run the recovery fixture.
    status: pass
```

Encoding contract:

- `L0` is the exact fixture bytes above; `H_L = sha256(L0)`.
- `J(x)` is UTF-8 JSON with recursively Unicode-code-point-sorted object keys, preserved array order, no insignificant whitespace, and no terminal newline.
- `H_S = sha256(J(parseYaml(L0)))`.
- Projection hash `H_P = sha256(concat(sort(key || 0x00 || value || 0x0a)))`.
- Artifact-path components escape `/` as `%2F`.
- No database value may be parsed as instruction or authority.

Open `db.openSubtree("craft/workspaces/ws-alpha")`. Exact relative layout:

```text
meta/workspace_id                         "ws-alpha"
meta/schema_version                       "0.3.0"
meta/source_ledger                        ".craft/ledger.yml"
meta/ledger_sha256                        H_L
meta/semantic_sha256                      H_S
meta/import_id                            "IMP-0001"
meta/adapter_version                      "0.0.0-fixture"
source/ledger.yml                         L0
rows/<family>/<stable-id>                 J(exact row above)
rows/recomposition/CTX-WAVEDB-CHILD~CTX-WAVEDB-ROOT
                                           J(exact recomposition row)
indexes/by_id/<stable-id>                 UTF-8 selector shown above
indexes/open_decisions                    J([])
indexes/blocking_decisions                J([])
indexes/active_blockers                   J(["BLK-WAVEDB-RAW-001","BLK-WAVEDB-REFINED-001"])
indexes/active_gaps                       J(["GAP-WAVEDB-RECOVERY-001"])
indexes/next_moves/<context-id>           J(exact next_move record)
indexes/artifacts_by_path/.craft%2Fledger.yml
                                           "ART-WAVEDB-LEDGER"
indexes/artifacts_by_path/CRAFT.md        "ART-WAVEDB-VIEW"
indexes/artifacts_by_path/receipts%2Fwavedb-fixture.json
                                           "ART-WAVEDB-RECEIPT"
derived/index.json                        J(I0)
derived/CRAFT.md                          C0
derived/index_sha256                      sha256(J(I0))
derived/craft_md_sha256                   sha256(C0)
adapter_receipts/IMP-0001                 J(import receipt)
probe/a                                   "0"
probe/b                                   "0"
```

`I0` must contain every required generated-index field from [the canonical index schema](/home/vrondelli/projects/domainspec-core/arcanum/arcana/craft/templates/schemas/index.schema.yml): metadata `{schema_version:"0.3.0",ledger_sha256:H_L,generated_at:"2026-08-04T17:00:00Z",generator_version:"0.0.0-fixture",source_ledger:".craft/ledger.yml"}`, the exact embedded lists/maps above, `by_family`, `row_selectors`, `pending_by_node`, `reverse_links`, `references`, `evidence_refs`, and `stale_status:"fresh"`. All lookup values point to source IDs/selectors; none copy authoritative row content.

Exact `C0` export:

```markdown
# WaveDB projection fixture

> Derived from `.craft/ledger.yml`; never edit this view as authority.

## Context CTX-WAVEDB-ROOT

Stage: `plan` · Gate: `block`

WaveDB is a digest-guarded projection; YAML remains the sole source of truth.

Next move: Refine BLK-WAVEDB-RAW-001, then run the recovery fixture.

### Blockers

- [BLK-WAVEDB-RAW-001](#blocker-blk-wavedb-raw-001): Encoding ambiguity prevents reproducible hashes.
- [BLK-WAVEDB-REFINED-001](#blocker-blk-wavedb-refined-001): Runtime usefulness depends on falsifiable recovery behavior.

### Decision

- [DEC-WAVEDB-STORE-001](#decision-dec-wavedb-store-001): `yaml-authority-wavedb-projection`

### Gap

- [GAP-WAVEDB-RECOVERY-001](#gap-gap-wavedb-recovery-001): Crash, corruption, and concurrent-writer behavior have not been executed.

### Child context

- CTX-WAVEDB-CHILD (`closed`, `pass`)

### Recomposition

The child selected YAML authority with a rebuildable WaveDB projection.
```

Batches and observations:

1. Validate all Craft references and derive `H_L`, `H_S`, `I0`, and `C0` in memory. Validation failure performs zero WaveDB calls.
2. `B0`: one `subtree.batchSync` containing every key above. Then scan and compute `H_P`; write no post-batch “success marker” outside `B0`.
3. `CP0`: call `subtree.snapshot()` and record it only as a persistence checkpoint.
4. `R0`: `scanSyncRaw("rows/contexts")` returns exactly two rows; `rows/typed_items` returns two; `rows` returns twelve; `probe` returns `a=0,b=0`. `ws-beta` returns zero rows.
5. Create a root `createReadStream` over `[craft/workspaces/ws-alpha/probe, craft/workspaces/ws-alpha/probe~)`, pause after its first entry, then run `B1={probe/a:"1",probe/b:"1"}` and resume. The paused iterator must yield `0/0`; a new scan must yield `1/1`. This tests iterator MVCC, not `snapshot()`.
6. `CP1`: checkpoint, close, reopen with `wal.syncMode:"immediate"`, rescan, and require the post-`B1` `H_P`.
7. Export raw source bytes and require `sha256(export)==H_L`; reconstruct parsed rows and require `sha256(J(reconstructed))==H_S`; regenerate and require index/view hashes unchanged.

Expected receipts: `fixture-validation.json`, `adapter-import.json`, `scan-isolation.json`, `derived-export.json`, `recovery.json`, `concurrency.json`, `negative-controls.json`, and `benchmark.json`. Every receipt carries `workspace_id`, WaveDB commit, adapter version, input digest, pre/post projection hashes, operation/batch ID, checkpoint semantics, observed scan keys, status, errors, timestamps, and claim ceiling.

Negative controls:

- Invalid reference: replace the raw blocker target with `CTX-MISSING`; expect `VAL-012`, zero database mutation.
- Wrong workspace: request `ws-beta` against `meta/workspace_id=ws-alpha`; expect `WORKSPACE_MISMATCH`, no rows or outputs.
- Stale ledger: change one YAML byte after import; expect `STALE_LEDGER_DIGEST`, projection ignored and rebuilt.
- Partial batch: submit a valid first operation plus an invalid second operation, then an oversized batch exceeding configured `wal.maxFileSize`; both must reject with the marker absent. This proves only preflight/pre-apply failure. True mid-apply failure remains HOLD until a safe first-party fault seam exists.
- Concurrent writers: race two batches writing both probe keys to `A/A` and `B/B`; final state must be entirely A or B, never hybrid. No compare-and-set API was verified, so stale-writer rejection belongs in the adapter’s single-writer/digest guard.
- Crash/reopen: child process, immediate WAL, resolved `B0`/`B1`, `SIGKILL` before close; reopen must show one complete batch state.
- Corruption: alter one projection value and separately damage a copied temporary database file; digest mismatch or open error must block rendering. Silent acceptance is KILL.
- Derived writeback: modify `CRAFT.md`, then refresh; ledger hash remains unchanged and `CRAFT.md` is regenerated from YAML. Importing the view must return `DERIVED_WRITEBACK_FORBIDDEN`.

Measurement hypotheses, not claims:

- Unit: 100/100 repeated codecs produce identical `H_S`; 100% reference and index coverage.
- Integration: 100/100 imports satisfy `H_L`, `H_S`, `H_P`, derived hashes, and zero writes on invalid input.
- Recovery: 100/100 immediate-WAL crash trials reopen to a complete pre- or post-batch state; zero hybrids.
- Migration/rollback: 100/100 import-delete-subtree-reimport cycles leave YAML bytes unchanged.
- Concurrency: 1,000 paired-writer trials produce zero hybrids and zero cross-workspace rows.
- Corruption: 100% of injected logical corruption is caught before serving; undetected physical corruption is KILL.
- Benchmark hypotheses on pinned hardware: small-fixture p95 import ≤25 ms and derived render ≤10 ms; 10,000-row p95 import ≤2 s and point lookup ≤5 ms. These are tuning targets only, never acceptance evidence.

## Receipt Fields

```yaml
status: pass
validation: pass
artifacts:
  - receipts/explorer-fixture-design.json
blockers: []
started_at: 2026-08-04T14:05:07-03:00
finished_at: 2026-08-04T14:08:44-03:00
handoff: >-
  The synthesizer can bind this finite witness to the projection/cache posture.
  Preserve YAML authority, distinguish persistence checkpoints from iterator
  snapshots, and retain HOLD on true mid-apply failure until a safe fault seam
  is verified.
```

