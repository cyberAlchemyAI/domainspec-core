# RWO–Codex Runtime Research Findings

Dispatch: `2026-08-14-rwo-codex-runtime-research`

Evidence closure: `READY`

Artifact status: `reviewed planning artifact`

Proof status: `specified-unexecuted`

Revision: `AUDIT-EXACTNESS-01`

First audited findings SHA-256: `cce7ceb8baffa395f45b5136d15fbed5d51e3f2b363af684d90e6c9088bfbd7d`

## Decision and claim ceiling

The selected topology is a new private, fixture-first RWO-to-Codex migration epoch. Codex App Server replaces the Eve-shaped physical leaf below the existing private RWO Go durability owner. The Rust kernel remains the only semantic scheduler and reducer. `framework/runtime` remains the one outer execution envelope and projects only generic status plus opaque private-record references and digests. Task Session remains the admission, receipt-topology, owner-verdict, and governance-closeout coordinator.

```text
Task Session admission and single-use ticket
  -> generic framework/runtime envelope
       -> private RWO adapter profile
            -> private RWO Go coordinator and authoritative journal
                 -> Rust semantic compiler/reducer
                 -> private Codex stdio translator
                 -> provider-evidence validation
                 -> Go physical convergence and durable admission recording
                 -> Rust semantic acceptance and no-successor decision
       <- projection-only generic status/events
  -> executor receipt -> capability-owner verdict
  -> routed-owner synchronization -> Task Session governance terminal
  -> privacy-safe observation
```

This rejects five competing placements: a public App Server runtime feeding RWO, a second durable App Server runtime behind RWO, RWO replacing Task Session, provider collaboration satisfying Orchestrate, and provider host goals driving Craft or Goal. It also rejects a rename-only migration that leaves Eve HTTP, NDJSON, session, endpoint, cancel, or replay assumptions in the active path.

Evidence: [authority explorer `spawn-0003`](research.md#spawn-0003--explorer-authority-integration) → `arcanum/framework/runtime/README.md:3-15,17-33,64-87,116-118`, `projects/cyberalchemy-orchestrator/implementations/rwo/DURABLE-RUNTIME-VALIDATION-REPORT.md:28-62`, and `ops/development/2026-08-13-arcanum-codex-app-server-integration-map/findings.md:182-207`; **source-observed**. The topology and migration behavior are **specified-unexecuted**. The three round-002 reviewers passed owner placement, non-vacuity, and migration integrity; those verdicts prove review closure only.

The ceiling is strict: this artifact proves no Git closure, App Server or model run, live RWO–Codex compatibility, implementation readiness, semantic acceptance, Task Session completion, lifecycle synchronization, publication, release, deployment, or production property.

## Evidence model

Load-bearing statements use these labels:

| Label | Meaning here |
|---|---|
| `source-observed` | Read from the bound current local source, or from the mutable official App Server page at its recorded observation date. It does not imply an immutable upstream revision. |
| `fixture-observed` | Demonstrated only by the existing deterministic F-01 normalized fixture. |
| `historical` | Demonstrated by older fake-Eve evidence or preserved lifecycle records; not current Codex evidence. |
| `specified-unexecuted` | Required contract, trace, validator, or Work-Pack step that has not run. |
| `unverified` | A required parity, host-enforcement, reconciliation, or current-byte fact is still open. |

The evidence-closed synthesis is SHA-256 `2043747ec3fe37f47b938fa1ccde0e68c2a9aa0ba5a8ab343901379648a9d4fd`. The Eve denominator is SHA-256 `1c17c5cd91105e79d2988a8a2b23503c9e90350d6a361b205eaa3934b0223588`. Evidence: [evidence closure](receipts/evidence-closure.json) and [denominator package](feedback/explorer-denominator-round-001.md); **source-observed**.

## Eve active-byte and historical-preservation ledger

### Closed denominator

The bounded search ran over the exact enumerated RWO Go, RWO Rust, planning, definitions, docs, handoff-notice, and four unrelated-history roots during `2026-08-14T14:20:00Z..2026-08-14T14:25:29Z`. It used `Eve(?=$|[^a-z])|EVE(?=$|[^A-Za-z])|eve(?=$|[^a-z])`, plus path-only and Eve-shaped semantic checks. It classified 2,378 literal occurrences in 284 literal-hit files, three path-only fixture files, and one semantic-only file: 288 unique classified files, zero unclassified, zero duplicates, zero Rust-source occurrences, and zero recursive-definition occurrences.

| Class | Literal count | Required disposition | Proof |
|---|---:|---|---|
| active provider | 122 | Replace or version-separate through the private Codex migration. | [RWO explorer `spawn-0001`](research.md#spawn-0001--explorer-rwo-eve-inventory) + [denominator search closure](feedback/explorer-denominator-round-001.md#search-closure); `source-observed` |
| provider-neutral but Eve-named | 3 plus one semantic-only selector family | Generalize only in V2; preserve V1 meaning. | same; `source-observed` |
| test/fixture | 113 | Port provider-neutral invariants and replace Eve protocol cases. | same; `source-observed` |
| current docs | 68 | Update or version only after new proof exists. | same; `source-observed` |
| generated/lifecycle | 265 | Preserve identifiers; supersede only through the owning lifecycle. | same; `source-observed` |
| immutable history | 1,630 | Preserve byte-for-byte. | same; `source-observed` |
| unrelated history | 177 | Leave untouched. | same; `source-observed` |

This is readable-filesystem closure for named roots and the sample window, not tracked/untracked/deleted/ignored or post-window Git closure. A mutation Work Pack must refresh the inventory using Git-aware methods while preserving concurrent work. Evidence: [denominator limitation](feedback/explorer-denominator-round-001.md#limitation-and-ceiling); `source-observed`.

### Complete active ledger

`GO` means `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go`.

| Active selector or family | Bound SHA-256 | Classification | Migration disposition | Proof |
|---|---|---|---|---|
| `GO/eve_leaf.go:17-215` | `a5bbe6699bac0d3a8e26e74f6a092cead0c061f0feac82d6803c531212471845` | active provider | Replace with a private Codex stdio leaf. | [active ledger](feedback/explorer-denominator-round-001.md#active-eve-ledger); `source-observed` |
| `GO/seat_material.go:29,344-465` | `4024b9146a28bfa74ea6614cb3c87c1a0a78b7bdcde10870e9b0e85995893688` | active provider | Replace the Eve request layer; retain material provenance and command decoding. | [RWO explorer component map](research.md#spawn-0001--explorer-rwo-eve-inventory) + active ledger; `source-observed` |
| `GO/terminal.go:19,30-47,96-146,203-322` | `4ad73df8c5064f056105646914d3e3d84187b16c6039c2d93f2a1c5701e80a27` | active provider | Split provider parsing from provider-neutral terminal admission; preserve the V1 decoder. | same; `source-observed` |
| `GO/seat_material.go:28,308-341` | same file hash | provider-neutral Eve-named | Generalize the V2 name; retain the old decoder. | active ledger; `source-observed` |
| `GO/attempts.go:15-41,97-132,396-610,830-859,867-899` | `d77bfb4779f7126e790236d1c43896bf5d19e0496d9e89ff022a2b7be51f0144` | provider-neutral Eve-named | Introduce versioned provider-neutral handles/checkpoints; preserve V1 session/stream semantics. | [RWO explorer invariant analysis](research.md#spawn-0001--explorer-rwo-eve-inventory) + active ledger; `source-observed` |
| `GO/attempts_test.go` | `0a4798500b56475e264d0932ec7038d679ba4581c6aec40406520bd19b786100` | test/fixture | Port fencing, ambiguity, and provider-handle tests. | active ledger; `source-observed` |
| `GO/durable_e2e_test.go` | `48edff41ecb8c41d86b7b52c1eef364a6323185c60a921033bb9448bf417272b` | test/fixture | Replace the fake-Eve E2E with deterministic Codex fixture E2E. | active ledger; `source-observed` |
| `GO/eve_leaf_test.go` | `f9f5ac26c709d28c3520d6db97cf3bfbeea309531609ba1e7245ea658c2d81a2` | test/fixture | Replace with App Server protocol tests. | active ledger; `source-observed` |
| `GO/failure_injection_test.go:25-30,41-42,52` | `5a370b5adf3c816408b6fae891ee6cf4342f2560687b3d740cf4fd668bc1f51c` | test/fixture | Replace Eve rows; retain and extend the generic failure matrix. | active ledger; `source-observed` |
| `GO/seat_material_test.go:138-176` | `762dee78a5b7a868772ff5d7262ee5a1cf58a9601cf4d808ea61138774a38560` | test/fixture | Replace the exact Eve request case. | active ledger; `source-observed` |
| `GO/terminal_test.go` | `a591e8616e40334fbf660938f055f75a43249305d21ff770b72fb04d5e3587aa` | test/fixture | Port provider grammar tests; retain convergence/replay/divergence invariants. | active ledger; `source-observed` |
| `GO/testdata/eve-one-seat/*` | member hashes in denominator | test/fixture | Stop active import, preserve fixture history, and add a new App Server fixture family. | [fixture member manifest](feedback/explorer-denominator-round-001.md#active-eve-ledger); `source-observed` |
| `GO/README.md:6,41,50-51,89-99` | `2774e205cffa0d4e9a18e09e956690f086e203c83f9159a0144d6936e28132af` | current docs | Update only after new proof. | active ledger; `source-observed` |

### History and lifecycle disposition

| Selector family | Classification | Required treatment | Proof |
|---|---|---|---|
| `docs/features/recursive-work-orchestrator/README.md:92-93` | current docs | Refresh only after new proof. | [docs/history families](feedback/explorer-denominator-round-001.md#docs-lifecycle-and-history-families); `source-observed` |
| `docs/features/recursive-work-orchestrator/ontology/**` excluding migrations | current docs | Supersede by version after new proof; do not rewrite as if Codex were already active. | same; `source-observed` |
| `RWO-IMPLEMENTATION-EVIDENCE-2026-08-13.md` | immutable history | Preserve unchanged. | same; `historical` |
| `implementations/rwo/DURABLE-RUNTIME-VALIDATION-REPORT.md` | immutable history | Preserve unchanged; its fake-Eve witness is not Codex evidence. | same; `historical` |
| ontology migration `0.2.0-to-0.3.0/**` | generated/lifecycle | Preserve the applied migration; create a new version. | same; `historical` |
| dated runs `20260813T141038Z`, `20260813T172339Z`, `20260813T190813Z`, `20260813T215634Z` | immutable history | Preserve unchanged. | same; `historical` |
| dated runs `20260814T073949Z`, `20260814T133756Z` | generated/lifecycle | Preserve IDs and route any supersession through the owner. | same; `historical` |
| handoff-notice index and notice members | generated/lifecycle | Preserve lifecycle ID. | same; `historical` |
| four enumerated external-tool/agent-infrastructure roots | unrelated history | Leave untouched. | same; `historical` |

## Current component and authority map

### Reusable versus provider-specific components

| Surface | Decision | Boundary | Evidence and proof |
|---|---|---|---|
| `implementations/rwo-rust/**` | Retain. | Sole semantic compiler/reducer; owns accepted-event and command identity, zero-or-one successor, and no-successor. | [RWO explorer architecture boundary](research.md#spawn-0001--explorer-rwo-eve-inventory); `source-observed` |
| Go `durable_store.go` | Retain and rerun. | Append/sync, hash chain, sequence, cursor CAS, locking, poison-on-uncertain-write, and recovery. | `durable_store.go:257-337,461-465` via [durability manifest](feedback/explorer-denominator-round-001.md#inherited-go-durability-cut-manifest); current structure `source-observed`, Codex cuts `specified-unexecuted` |
| Go `durable_runtime.go` | Retain architecture, revalidate current bytes. | Persists/projects Rust-authored semantic records; does not author or reinterpret them. | `durable_runtime.go:144-180,201-247`; same evidence; `source-observed` with historical witnesses only |
| Go attempt/terminal coordinators | Generalize in V2. | Sole physical owner for attempts, operations, send tries, lease/fence, ambiguity, reconciliation, retry eligibility, terminal convergence, and durable admission recording. | `attempts.go:223-283,396-429,614-622,659-697,803-813`; `terminal.go:203-322,347-398`; `source-observed` |
| Material resolver and boundary services | Retain. | Content addressing, path containment, symlink rejection, hash checks, closed capability policy, child kernel, sidecar, gRPC/HTTP/local runtime boundaries. | [RWO explorer component map](research.md#spawn-0001--explorer-rwo-eve-inventory); `source-observed` |
| Eve leaf, request grammar, raw/event grammar | Replace/version-separate. | No Eve transport assumption may survive under a Codex name. | active ledger above; `source-observed` |
| `cmd/rwo-local-runtime/main.go` | Extend in the new epoch. | Current CLI stops after Rust child, compile, store/runtime construction, and gRPC boundary; it lacks attempt/provider/terminal/delivery workers. | `cmd/rwo-local-runtime/main.go:118-134` via [RWO explorer critical gap](research.md#spawn-0001--explorer-rwo-eve-inventory); `source-observed` |

### Single-owner allocation

| Concern | Sole owner | What its evidence may establish | Direct source selector / proof |
|---|---|---|---|
| Work-Pack authoring | Invoke Plan | Candidate plan, never execution authority. | [authority explorer](research.md#spawn-0003--explorer-authority-integration), `arcanum/arcana/task-session/SKILL.md:239-335`; `source-observed` |
| Selection and mutation admission | Task Session / currently routed readiness owner | Single-use ticket and admission. | `arcanum/arcana/task-session/SKILL.md:239-335,337-417`; `source-observed` |
| Outer execution | `framework/runtime` / `tools/arcanum` | Generic run/status/event envelope only. | `arcanum/framework/runtime/README.md:3-33,64-87`; `source-observed` |
| Semantic decision | Rust RWO kernel | Accepted event, command, cursor transition, and no-successor. | [RWO explorer architecture boundary](research.md#spawn-0001--explorer-rwo-eve-inventory); `source-observed` |
| Semantic-record persistence | Go durable runtime/store | Synced projection of Rust-authored records. | `durable_runtime.go:144-180,201-247`; `source-observed` |
| Provider translation | Private Codex translator | Raw schema/order/identity/approval/item/output/provider-terminal closure. | [Codex explorer protocol matrix](research.md#spawn-0002--explorer-codex-protocol); protocol contract `specified-unexecuted` |
| Physical convergence | Go attempt/terminal coordinators | Attempts, operations, sends, leases, fences, ambiguity, reconciliation, physical retry eligibility, terminal candidate, admission recording. | `attempts.go:57-177,223-283,371-487,614-813`; `terminal.go:203-398`; current code `source-observed`, Codex extension `specified-unexecuted` |
| Semantic terminal acceptance | Rust RWO kernel | Accept/reject provider-neutral terminal and decide successor. | RWO explorer architecture boundary; `source-observed` |
| Executor/owner/closeout chain | Task Session plus named capability and closeout owners | Executor receipt, owner verdict, joined closeout, governance terminal. | `arcanum/arcana/task-session/SKILL.md:239-417`; `source-observed` |
| Governed multi-agent dispatch | Orchestrate | Native action, join, gate, and close evidence only. | `arcanum/runtime/orchestrate/SKILL.md:72-81,124-164,211-223`; `source-observed` |
| Project ledger/frontier | Craft / Goal | Craft-owned apply; Goal-owned bounded frontier/round routing. | `arcanum/arcana/craft/SKILL.md:67-71,312-317`; `arcanum/spells/goal/README.md:8-17,58-68,82-108`; `source-observed` |
| Eval / observation | Experiment Harness / OIL + Signal Observer | Behavior evidence / privacy-safe non-verdict telemetry. | `arcanum/arcana/experiment-harness/SKILL.md:97-102`; `arcanum/spells/observed-invocation-loop/README.md:12-18,51-70`; `arcanum/arcana/signal-observer/SKILL.md:89-104`; `source-observed` |
| Promotion/publication | Target lifecycle/publication owner | Separately accepted exact revision only. | authority explorer; `source-observed` |

## Provider profile and contracts

### Smallest first Codex profile

The candidate profile is `rwo-codex-app-server-fixture-v0`: stdio JSONL, stable API only, `experimentalApi=false`, one initialization handshake, one independently bound thread and one admitted turn per RWO physical attempt, text-only input, exact input/policy/profile/binary digests, restricted read-only roots, and no undeclared writable root or network expansion. The terminal set is `completed | failed | interrupted | delivery_unknown`.

The profile forbids WebSocket/remote code-mode host, fork/steer/review/realtime/thread-goal, shell/command execution, process spawn, direct filesystem APIs, MCP, apps, plugins, marketplace, dynamic tools, session-wide permission grants, broad network, collaboration-agent evidence as Orchestrate evidence, and host goals as Craft/Goal state.

Evidence: [Codex explorer `smallest_candidate_profile`](research.md#spawn-0002--explorer-codex-protocol) and the [official Codex App Server page](https://learn.chatgpt.com/docs/app-server), observed `2026-08-14`; protocol surface is as-of-date `source-observed`, while the RWO binding and denial posture are `specified-unexecuted`. The page identity preserved in the evidence is the URL plus observation date only: no immutable documentation revision, content digest, commit, tag, or generated-schema identity was captured. These claims are therefore never revision-pinned. The page also does not prove a closed tool allowlist or read-only network-denial field; host-enforced denial and a negative witness remain `unverified`.

Observed source identities are the installed binary `/home/vrondelli/.vscode-server/extensions/openai.chatgpt-26.810.41047-linux-x64/bin/linux-x86_64/codex`, version `codex-cli 0.148.0-alpha.9`, SHA-256 `86a4286b2451c69d4c00ad1772fcee5170013f2924e7d257ad2d4f19290c2a20`, and fixture source pin `openai/codex@9946da9af1829410271f6b76f9159961f7281e0a`. Their parity is `unverified`. Evidence: [Codex explorer `source_identity`](research.md#spawn-0002--explorer-codex-protocol); binary metadata `source-observed`, parity `unverified`.

The named method/event selectors used from that as-of-date page are `initialize`, the `initialized` notification, `thread/start`, `thread/started`, `thread/read`, `thread/resume`, `thread/list` as reconciliation evidence, `turn/start`, `turn/started`, `item/started`, item-specific delta notifications, `item/completed`, server-initiated approval/permission requests, `serverRequest/resolved`, `turn/interrupt`, `error`, and `turn/completed` with `completed`, `failed`, or `interrupted` status. The explorer did not preserve the individual method strings for every item-delta or approval-request variant, so those two sub-denominators remain `unverified` until a generated-schema parity step captures exact names and hashes. Evidence: [Codex explorer protocol matrix, gaps, and C01-C17](research.md#spawn-0002--explorer-codex-protocol); official selectors as-of `2026-08-14` are `source-observed`, installed-binary/source/fixture parity is `unverified`.

### Protocol-to-RWO binding

| App Server operation/event | RWO physical meaning | Durable precondition and raw evidence | Never substitutes for | Proof |
|---|---|---|---|---|
| `initialize` → `initialized` | Bind process/connection/profile. | Arm with binary path/version/hash, transport, client/capability hash; persist request, response, and notification before interpretation. | RWO admission or semantic execution. | [Codex explorer protocol matrix](research.md#spawn-0002--explorer-codex-protocol); `specified-unexecuted` |
| `thread/start` | Provider create under one attempt. | Arm command/attempt/operation/send/fence/request/input/policy hashes; persist response and `thread/started`, then bind thread identity. | RWO command, attempt, Task Session, or Craft identity. | same; `specified-unexecuted` |
| `thread/read` / `thread/resume` | Recovery inspection/reconnection. | Arm a new recovery operation; persist full response and new epoch binding before comparison. | Retry, replay authority, or fresh admission. | same; `specified-unexecuted` |
| `turn/start` | Execute the immutable RWO command physically. | Arm exact input/cwd/sandbox/approval/model/profile hashes under the existing attempt and thread. | RWO attempt or semantic command. | same; `specified-unexecuted` |
| `item/started`, deltas, `item/completed` | Ordered provider evidence. | Persist every raw message with arrival sequence and canonical payload hash; deltas stay provisional. | Receipt, accepted event, or authoritative host output inventory. | same; `specified-unexecuted` |
| server approval/permission request | Pause one physical attempt. | Bind connection-scoped request ID plus thread/turn/item and policy digest; persist request, decision intent, armed response, response, and resolution. | Decision Gate, Task Session admission, owner acceptance, Craft apply, or promotion. | same; `specified-unexecuted` |
| `turn/interrupt` | Physical cancellation request. | Persist interrupt intent, arm/send request, persist response and eventual interrupted terminal. | Terminal evidence before `turn/completed`, or retry authority. | same; `specified-unexecuted` |
| error + failed terminal | Typed provider failure. | Persist error details and failed terminal under the bound turn. | Proof that a disconnect was not delivered. | same; `specified-unexecuted` |
| completed terminal | Provider-evidence closure candidate. | Require resolved/cleared requests, raw item closure, actual output inventory, diff hash, and terminal record. | Semantic success, owner acceptance, Task Session closeout, or no-successor. | same; `specified-unexecuted` |

### Public and private contract split

Public Arcanum may own only provider-generic envelopes and explicit authority nulls:

| Proposed public schema | Required fields and ceiling | Proof |
|---|---|---|
| `durable-child.adapter-manifest.v0` | Adapter ID; executable path/version/hash; argv; cwd; environment-name allowlist; timeout; input/output schema refs/hashes; authority ceiling; manifest hash. | [authority explorer public/private boundary](research.md#spawn-0003--explorer-authority-integration); `specified-unexecuted` |
| `framework-runtime.child-handoff.v0` | Runtime ID; adapter/manifest hash; input/policy refs/hashes; readable/writable roots; network policy; deadline; expected result ref. | same; `specified-unexecuted` |
| `framework-runtime.projected-event.v0` | Runtime ID; sequence; phase; opaque child record ref/hash; observed time. No raw messages or recovery cursor. | same; `specified-unexecuted` |
| `framework-runtime.child-result.v0` | Host status; provider-evidence ref/hash; output inventory; typed error; proof status; next owner; authority nulls. | same; `specified-unexecuted` |
| `app-server.protocol-profile.v0` | Source locator and observation date; future owner-captured immutable snapshot/revision identity when available; binary/schema hashes; transport; allowed operations; denied capabilities; sandbox/network/approval policies; profile hash. Current evidence has no immutable official-page revision. | [Codex explorer host-result/profile](research.md#spawn-0002--explorer-codex-protocol); `specified-unexecuted` |
| `app-server.host-result.v0` | Provider identities; raw/approval evidence refs/hashes; terminal/error; actual outputs; diff hash; recovery disposition; proof status; next owner; authority nulls. | same; `specified-unexecuted` |

Every public result explicitly nulls semantic verdict, Task Session admission/terminal, capability acceptance, Craft/Goal state, dispatch acceptance, and lifecycle promotion. Before public extension, the current runtime owner must prove that the existing adapter surface lacks a required field or rule, then extend the existing registry/controller. A second registry, controller, durable run, or public RWO special case is forbidden. Evidence: [authority explorer, current fixed-adapter gap](research.md#spawn-0003--explorer-authority-integration) → `arcanum/framework/runtime/README.md:3-33,64-87`; current limitation `source-observed`, proposed extension `specified-unexecuted`.

Private `rwo.codex-*.v2` records own provider binding, operation/send/fence state, raw message blobs and scoped IDs, reconciliation candidates and decision, terminal/effect/output validation, Rust decision reference, semantic commit sequence, and private runtime result. Only opaque references and digests project publicly. RWO vocabulary, mapping, journal types, retry/ambiguity rules, translator logic, and migration history remain private. Evidence: [authority explorer public/private boundary](research.md#spawn-0003--explorer-authority-integration) → root `AGENTS.md:7-12`; `source-observed` boundary, V2 schemas `specified-unexecuted`.

## Identity, persistence, and receipt rules

Every V2 private record must bind `schema_version`, a `namespace_digest` over canonical schema IDs/names/cardinalities, `provider_profile_digest`, `binary_digest`, `attempt_id`, record-specific identity, canonical payload hash, and journal sequence. A missing or changed digest blocks before interpretation. Persisted Eve V1 records retain their original decoder and meaning.

| Relation | Cardinality and rule | Proof |
|---|---|---|
| semantic command → attempt | `1 → 0..n`; a new attempt is not new semantic work. | [RWO explorer architecture boundary](research.md#spawn-0001--explorer-rwo-eve-inventory); current invariant `source-observed`, V2 encoding `specified-unexecuted` |
| attempt → active provider binding | `1 → 0..1` in profile 1. | [reviewed synthesis identity model](synthesis.md#versioned-identity-and-relation-model); `specified-unexecuted` |
| attempt → provider operation | `1 → 0..n`, strictly ordered. | same; `specified-unexecuted` |
| operation → send try | `1 → 1..n`; every try has unique ID/ordinal; try >1 requires durable exact-known-not-sent proof. | [migration-integrity review](reviews/round-002-migration-integrity.md); `specified-unexecuted` |
| send try → armed-send | Exactly one immutable append-and-synced record before that try's effectful provider write. | `attempts.go:252-283,396-429` precedent via [denominator](feedback/explorer-denominator-round-001.md#inherited-go-durability-cut-manifest); precedent `source-observed`, Codex form `specified-unexecuted` |
| process epoch → connection epoch | `1 → 1..n`; restart mints process epoch, reconnect mints connection epoch. | [Codex explorer identity namespace](research.md#spawn-0002--explorer-codex-protocol); `specified-unexecuted` |
| connection epoch → JSON-RPC request ID | `1 → 0..n`; uniqueness is connection-scoped. | same; protocol `source-observed`, durable encoding `specified-unexecuted` |
| attempt → thread / thread → admitted turn | `0..1` / exactly one in profile 1; reads/resumes create neither. | Codex explorer profile and protocol matrix; `specified-unexecuted` |
| turn → item → server request | `0..n` / `0..n`; each request gets at most one response. | official App Server surface via Codex explorer; `source-observed`, enforcement `specified-unexecuted` |
| normalized event → raw messages | `1..n`; every contributing raw hash is explicit. | Codex explorer host-result contract; `specified-unexecuted` |
| Rust admission → terminal candidate | `0..1`; rejection/block creates no accepted event. | RWO explorer invariant analysis; current invariant `source-observed`, Codex path `specified-unexecuted` |

Provider process, connection, JSON-RPC request, thread, turn, item, and server-request IDs never equal or replace RWO semantic or physical IDs, runtime IDs, Task Session identities, receipt IDs, Orchestrate IDs, Craft state, Goal state, owner verdicts, or lifecycle gates. Evidence: [authority explorer identity matrix](research.md#spawn-0003--explorer-authority-integration) and [Codex explorer forbidden equalities](research.md#spawn-0002--explorer-codex-protocol); `source-observed` protocol namespaces, non-substitution enforcement `specified-unexecuted`.

Before each effectful provider write, Go must append and sync one immutable armed-send record binding the operation and send-try identities/ordinals, attempt, lease/fence, process/connection epochs, canonical request hash, input/policy/profile/binary digests, known provider targets, permitted response/notification kinds, state, and journal sequence. Crash, timeout, or disconnect without exact-known-not-sent proof becomes `delivery_unknown` and freezes; it never authorizes resend. Evidence: `attempts.go:252-283,396-429` and [RWO explorer invariant analysis](research.md#spawn-0001--explorer-rwo-eve-inventory); current arm-before-send precedent `source-observed`, Codex operations `specified-unexecuted`.

The receipt chain is:

```text
private RWO result + app-server.host-result.v0 + RWO journal refs/digests
  -> framework/runtime STATUS.json
  -> task-session.executor-receipt.v1
  -> named capability-owner verdict or task-session.owner-hook-receipt.v1
  -> validation reconciliation
  -> task-session.precloseout-execution-receipt.v1
  -> joined closeout-owner receipt
  -> observation receipt/reference
  -> task-session.governance-terminal-receipt.v1
```

Provider evidence and RWO journal records contribute to but never replace this chain. The terminal receipt forbids successor execution and carries a null or explicit cursor. Evidence: [authority explorer result/receipt chain](research.md#spawn-0003--explorer-authority-integration) → `arcanum/arcana/task-session/SKILL.md:239-417`; `source-observed`.

## Approval, sandbox, recovery, replay, and retry rules

1. **Approval scope.** App Server permission is one response to one provider request under a frozen policy. `approved-once` is legal only when the request is equal to already admitted scope. Any filesystem, network, process, model, tool, or write expansion blocks the attempt. `acceptForSession` is forbidden in profile 1. Provider permission is never human confirmation, RWO semantic authorization, Task Session admission, Decision Gate resolution, capability acceptance, Craft apply, Goal authority, lifecycle promotion, publication, or deployment. Evidence: [Codex explorer permission mapping](research.md#spawn-0002--explorer-codex-protocol) + [authority explorer gate separation](research.md#spawn-0003--explorer-authority-integration); protocol `source-observed`, enforcement `specified-unexecuted`.
2. **Sandbox and network.** The host must independently enforce the declared read-only roots, no undeclared writable root, denied capability set, and network posture. Documentation/configuration claims alone do not prove denial. Evidence: Codex explorer `GAP-AUTH-02`; `unverified`.
3. **Ambiguity.** Persist `delivery_unknown`, freeze, and forbid resend. Reconciliation uses newly armed read/list/resume operations and epochs. All responses persist before comparison. Unfreeze requires one and only one candidate matching every available predecessor, input, policy, profile, request, and identity discriminator, with candidate set and decision synced first. Zero, multiple, insufficient, or mismatched candidates remain frozen. Documentation does not yet prove sufficient discriminators. Evidence: Codex explorer `GAP-IDEMPOTENCY-03` and required fixtures C05/C06; rule `specified-unexecuted`, discriminator sufficiency `unverified`.
4. **Replay.** Same scoped identity, causal position, kind, and payload hash records one duplicate observation and emits no second normalized event. Same identity/position with a changed hash persists the mismatch and blocks as `REPLAY_MISMATCH` before translation, output, terminal admission, retry, or acceptance. The current F-01 validator rejects exact duplicates, so it is contrary evidence, not target proof. Evidence: `arcanum/framework/runtime/development/fixtures/app-server/validate_fixture.py:281-295` and [Codex explorer `GAP-REPLAY-06`](research.md#spawn-0002--explorer-codex-protocol); current behavior `fixture-observed`, target behavior `specified-unexecuted`.
5. **Interruption.** Persist intent, arm and send interrupt, persist response and eventual interrupted terminal. A response alone is not terminal. Recovery may read/resume bound work but may not replay `turn/start`; further work needs new attempt authority. Evidence: Codex explorer protocol matrix and C04; `specified-unexecuted`.
6. **Retry scopes.** Same-operation resend requires durable exact-known-not-sent proof and unchanged operation/request hashes while minting a new send-try and armed-send identity. Provider reconciliation never admits new work. RWO `RetrySame` requires an explicit Rust continuation and creates a new physical attempt for the same semantic command. Task Session recovery, Orchestrate fresh-run retry, Goal round, and Craft apply retry each remain under their own authority and never authorize a provider resend. Evidence: [RWO explorer invariant analysis](research.md#spawn-0001--explorer-rwo-eve-inventory), [authority explorer hooks](research.md#spawn-0003--explorer-authority-integration), and [migration-integrity review](reviews/round-002-migration-integrity.md); current distinctions `source-observed`, Codex enforcement `specified-unexecuted`.

## Finite executable trace plan

Every future trace fixture must contain `trace_id`, complete identity set, preconditions, ordered persisted records, ordered provider messages, expected result, governing gate, first stop, forbidden effects, proof status, and exact validator. Every inbound provider message is appended and synced before interpretation.

### `NV-01` — success and no-successor

- **Identity set:** Task Session `run_id/task_id/swu_id/ticket_id/admissionToken`; framework runtime run, adapter, and manifest IDs; RWO `command_id/accepted_event_id/cursor_before/cursor_after`; Go store instance, journal sequence, `attempt_id`, initialize/thread/turn operation IDs and ordinals, `send_try_id/ordinal`, `armed_send_id`, lease, and fence; provider profile/binary digests, process/connection epochs, connection-scoped JSON-RPC request IDs, `threadId`, `turnId`, item IDs; raw arrival sequence and payload hashes; terminal-candidate ID, Rust decision reference, and output inventory/digests.
- **Preconditions:** valid single-use admission; stable input/policy/profile/binary/namespace/manifest hashes; live lease/fence; no active provider binding or prior admitted turn; host denial policy installed; expected output contract frozen.
- **Ordered persistence/provider messages:** persist admission → attempt/lease/fence/process preparation → armed initialize; send `initialize`, persist response, send `initialized` notification, persist/bind connection → arm `thread/start`; send it, persist response and `thread/started`, bind thread → arm `turn/start`; send it, persist response and `turn/started`, bind turn → persist each `item/started`, item delta, and `item/completed` before translation → persist `turn/completed(completed)` → persist translator closure and output/effect inventory → persist Go terminal candidate → run Rust reduction → append/sync accepted event, cursor/no-successor, and admission marker → project only opaque refs/digests to outer runtime.
- **Result and gate:** host result is successful only after provider closure, output/effect validation, Go convergence, Rust acceptance, synced admission, and no-successor; Task Session owner/closeout gates remain later and separate.
- **First stop:** first digest, identity, order, schema, output, fence, durability, terminal-closure, or Rust-reduction failure.
- **Forbidden effects:** second thread or turn, blind resend, provider completion as semantic success, raw provider data in the public projection, automatic closeout/promotion/next work.
- **Proof / validator:** `specified-unexecuted`; exact validator `TestCodexTraceSuccessNoSuccessor`. Evidence: [Codex explorer C01](research.md#spawn-0002--explorer-codex-protocol), `durable_runtime.go:144-247`.

### `NV-02` — permission pause and scope expansion

- **Identity set:** Task Session ticket/admission and frozen policy digest; runtime and RWO command/attempt IDs; process/connection epochs; bound `threadId/turnId/itemId`; connection-scoped server-request JSON-RPC ID; raw request/resolution hashes; permission-decision ID; response operation, send-try, armed-send, lease, and fence IDs.
- **Preconditions:** a bound in-progress turn, unresolved server permission request, unchanged admission and policy, live fence, and no prior response for that request ID.
- **Ordered persistence/provider messages:** persist the server-initiated request before interpretation → persist physical pause → compare requested effect to frozen policy. Equal scope: persist `approved-once` intent → arm response → send exactly one response → persist response evidence and `serverRequest/resolved` → clear the request. Expanded/unknown scope: persist deny/block before any effect or response that grants it; terminal/interrupt may clear the request only through a persisted closure record.
- **Result and gate:** equal scope may resume once; expansion or uncertainty yields blocked host result and requires separate admission outside this attempt.
- **First stop:** first policy inequality, unknown effect, stale request, missing fence, duplicate response, or unresolved request at terminal.
- **Forbidden effects:** `acceptForSession`, second response, expanded effect, session grant, or treating provider permission as semantic authorization, Task Session admission, owner acceptance, Craft apply, or promotion.
- **Proof / validator:** `specified-unexecuted`; exact validator `TestCodexTracePermissionPauseAndScopeExpansion`. Evidence: [Codex explorer C02](research.md#spawn-0002--explorer-codex-protocol).

### `NV-03` — stale input before launch

- **Identity set:** Task Session run/task/SWU/ticket/admission IDs; framework runtime run/adapter/manifest IDs; RWO command and cursor IDs; frozen/current input, policy, profile, and namespace digests; mismatch/block record and outer projected-event sequence. No provider process, connection, request, thread, turn, item, attempt-send, or raw-message identity may exist.
- **Preconditions:** valid ticket exists, but recomputed launch input digest differs from the admitted frozen digest.
- **Ordered persistence/provider messages:** persist admission/frozen hash → recompute current hash → persist mismatch and blocked disposition → project opaque block reference. Provider sequence is empty: no process launch, `initialize`, thread, or turn message.
- **Result and gate:** block before provider launch; only a fresh admission may bind changed input.
- **First stop:** first admitted/current digest inequality.
- **Forbidden effects:** process/connection/thread/turn creation, output, retry, execution receipt claiming work ran, or admission repair in place.
- **Proof / validator:** `specified-unexecuted`; exact validator `TestCodexTraceStaleInputStopsBeforeLaunch`. Evidence: [Codex explorer C03](research.md#spawn-0002--explorer-codex-protocol).

### `NV-04` — interrupt and recovery-only resume

- **Identity set:** Task Session/runtime/RWO command and attempt IDs; lease/fence; process/connection epochs; bound `threadId/turnId`; interrupt operation, JSON-RPC request, send-try, and armed-send IDs; interrupted terminal/raw hashes; residue reference; new recovery process/connection epoch and read/resume operation IDs.
- **Preconditions:** one bound in-progress turn, persisted prior raw evidence, live interrupt authority/fence, and no terminal record yet.
- **Ordered persistence/provider messages:** persist interrupt intent → arm `turn/interrupt` → send request → persist response, which is not terminal → persist `turn/completed(interrupted)` and residue → mint new process/connection epoch if recovery is needed → arm `thread/read` or `thread/resume` → persist recovery response and rebinding decision without sending `turn/start`.
- **Result and gate:** interrupted host result with residue preserved; unresolved identity remains blocked; further execution requires new RWO attempt authority.
- **First stop:** missing/mismatched thread or turn, stale fence, interrupt response without terminal, or non-unique recovery binding.
- **Forbidden effects:** connection-scoped RPC-ID reuse, `turn/start` replay, resume-as-retry, residue deletion, or automatic new attempt.
- **Proof / validator:** `specified-unexecuted`; exact validator `TestCodexTraceInterruptRecoveryOnlyResume`. Evidence: [Codex explorer C04](research.md#spawn-0002--explorer-codex-protocol).

### `NV-05A` — ambiguous thread creation with unique reconciliation

- **Identity set:** RWO command/attempt, lease/fence, `thread/start` operation/request hash, original send-try/armed-send, original process/connection epoch and request ID; `delivery_unknown`/freeze record; recovery process/connection epoch; read/list operation, send, armed, and request IDs; candidate-set digest; candidate `threadId/sessionId` values; reconciliation-decision ID.
- **Preconditions:** `thread/start` armed and written, response absent after crash/timeout/disconnect, no exact-known-not-sent proof, no bound thread, and frozen immutable input/policy/profile/request discriminators.
- **Ordered persistence/provider messages:** persist unknown/freeze → mint and persist recovery epochs, without another `thread/start` → arm/send `thread/list` and/or `thread/read` → persist every response/candidate before comparison → compare all frozen discriminators → persist candidate-set digest and exactly one matching selection → persist thread rebinding and unfreeze.
- **Result and gate:** continue only when exactly one candidate fully matches and the decision is synced before later operations.
- **First stop:** zero, multiple, missing, insufficient, or mismatched candidates/discriminators.
- **Forbidden effects:** second create, nearest-time selection, arbitrary binding, reconnection as delivery proof, semantic admission, or blind retry.
- **Proof / validator:** `specified-unexecuted`; discriminator sufficiency `unverified`; exact validator `TestCodexTraceAmbiguousCreateUniqueReconciliation`. Evidence: [Codex explorer C05 and `GAP-IDEMPOTENCY-03`](research.md#spawn-0002--explorer-codex-protocol).

### `NV-05B` — ambiguous thread creation fails closed

- **Identity set:** RWO command/attempt, lease/fence, `thread/start` operation/request hash, original send-try/armed-send, original process/connection epoch and request ID; `delivery_unknown`/freeze record; recovery process/connection epoch; read/list operation, send, armed, and request IDs; candidate-set digest and candidate `threadId/sessionId` values; reconciliation-decision ID, null selection, and `AMBIGUOUS_THREAD_CREATE` disposition ID.
- **Preconditions:** the `NV-05A` uncertain-create state, but the persisted candidate set is zero, multiple, insufficient, or mismatched.
- **Ordered persistence/provider messages:** persist unknown/freeze → arm and send recovery reads/lists without create resend → persist all provider candidates → persist failed comparison, null selection, and `AMBIGUOUS_THREAD_CREATE` → retain freeze.
- **Result and gate:** terminally blocked physical attempt; only a separately authorized higher-level continuation may decide what follows.
- **First stop:** failed exactly-one-full-match predicate.
- **Forbidden effects:** resend, arbitrary thread binding, `turn/start`, output, accepted event, automatic RWO retry, or Task Session completion.
- **Proof / validator:** `specified-unexecuted`; exact validator `TestCodexTraceAmbiguousCreateFreezes`. Evidence: [Codex explorer C05](research.md#spawn-0002--explorer-codex-protocol).

### `NV-05C` — ambiguous turn start

- **Identity set:** RWO command/attempt, lease/fence, bound `threadId`, immutable predecessor/input/policy/profile/model/request hashes, `turn/start` operation, original send-try/armed-send/process/connection/request IDs; unknown/freeze record; recovery epoch and `thread/read` operation IDs; candidate `turnId` values and hashes; reconciliation-decision or `AMBIGUOUS_TURN_START` ID.
- **Preconditions:** `turn/start` armed and written, response absent after crash/timeout/disconnect, no exact-known-not-sent proof, thread uniquely bound, and no admitted turn.
- **Ordered persistence/provider messages:** persist unknown/freeze → mint recovery epoch, without a second `turn/start` → arm/send `thread/read` → persist response and every turn candidate → compare exact thread, predecessor, input, policy, profile, model, and request discriminators → persist one exact selection and bind/unfreeze, or persist null selection plus `AMBIGUOUS_TURN_START` and retain freeze.
- **Result and gate:** one exact match may continue; zero/multiple/insufficient/mismatched candidates block the attempt.
- **First stop:** failed exactly-one-full-match predicate or any immutable discriminator mismatch.
- **Forbidden effects:** second `turn/start`, nearest-time choice, arbitrary turn binding, output, terminal admission, accepted event, or retry.
- **Proof / validator:** `specified-unexecuted`; discriminator sufficiency `unverified`; exact validator `TestCodexTraceAmbiguousTurnStartReconcileOrFreeze`. Evidence: [Codex explorer C06](research.md#spawn-0002--explorer-codex-protocol).

### `NV-06` — exact duplicate is inert

- **Identity set:** process/connection epoch; scoped provider request/event identity; `threadId/turnId/itemId` when present; local arrival sequence; event kind and causal position; original and duplicate canonical payload hashes; original normalized-event ID; duplicate-observation ID.
- **Preconditions:** original raw message is synced and translated exactly once; duplicate has identical scope, identity, kind, causal position, and payload hash.
- **Ordered persistence/provider messages:** provider repeats the exact raw message → append/sync duplicate raw observation referencing original → compare identity/position/hash → persist inert duplicate disposition → emit no normalized event and do not advance semantic/provider cursor.
- **Result and gate:** audit no-op; original interpretation remains authoritative.
- **First stop:** exact equality predicate; changed hash routes to `NV-07` instead.
- **Forbidden effects:** protocol-failure rejection, second normalized event/output/cursor advance, retry, or repeated terminal admission.
- **Proof / validator:** target `specified-unexecuted`; F-01's contrary duplicate rejection is `fixture-observed`; exact validator `TestCodexTraceExactDuplicateIsInert`. Evidence: [Codex explorer C07 and `GAP-REPLAY-06`](research.md#spawn-0002--explorer-codex-protocol).

### `NV-07` — identity/hash replay mismatch

- **Identity set:** the same scoped provider/connection/thread/turn/item identity and causal position as an accepted original; original raw/normalized IDs and hash; new arrival sequence and changed hash; `REPLAY_MISMATCH` record ID; attempt/freeze ID.
- **Preconditions:** original raw message is synced and interpreted; a later message reuses its scoped identity/position but changes canonical payload hash.
- **Ordered persistence/provider messages:** provider emits conflicting message → append/sync raw conflict → compare against original → append/sync `REPLAY_MISMATCH` and freeze → stop before translation.
- **Result and gate:** blocked physical attempt; no terminal candidate or Rust admission.
- **First stop:** first payload-hash inequality under equal scoped identity and position.
- **Forbidden effects:** overwrite, reinterpretation, output, cursor advance, retry, accepted event, or success.
- **Proof / validator:** `specified-unexecuted`; exact validator `TestCodexTraceIdentityHashMismatchBlocks`. Evidence: [Codex explorer C08](research.md#spawn-0002--explorer-codex-protocol).

### `NV-08` — invalid, incomplete, or post-terminal provider events

- **Identity set:** attempt/operation, process/connection epoch, request/thread/turn/item/server-request IDs as present; raw arrival sequence/hash; provider grammar/order state; terminal-state ID; typed invalid/order/unknown/divergence disposition; no Rust accepted-event identity.
- **Preconditions:** a bound attempt and the applicable partial provider state for four discriminating subcases: invalid schema; `item/completed` before `turn/started`; item completion then disconnect without `turn/completed`; valid `turn/completed` then another event.
- **Ordered persistence/provider messages:** in every subcase append/sync raw first. Then: invalid schema → persist schema rejection; reordered item → persist order block; item completion plus disconnect → persist `delivery_unknown`; valid terminal → persist terminal closure, then persist late event and divergence. Unresolved permission requests are cleared only by a persisted terminal/interrupt closure; a stale response is prohibited.
- **Result and gate:** typed block or unknown at the first grammar/order/disconnect/post-terminal boundary; no provider-neutral terminal reaches Rust.
- **First stop:** respectively schema failure, missing `turn/started`, missing terminal at disconnect, or first post-terminal message.
- **Forbidden effects:** inferred/fabricated success, ignored late event, output admission, retry, cursor advance, or Rust accepted event.
- **Proof / validator:** `specified-unexecuted`; exact validator `TestCodexTraceInvalidAndPostTerminalEvents`. Evidence: [Codex explorer C09-C11 and C16](research.md#spawn-0002--explorer-codex-protocol).

### `NV-09` — Task Session closeout failure after valid execution

- **Identity set:** Task Session run/task/SWU/ticket/admission IDs; framework runtime run/adapter/manifest/result/status IDs; RWO command, accepted-event, cursor, and no-successor IDs; Go store/journal/attempt/operation/send/armed/fence/terminal identities; provider profile/binary/process/connection/request/thread/turn/item/raw identities; private RWO result and `app-server.host-result.v0` refs/hashes; executor-receipt, owner-verdict, reconciliation, precloseout, closeout-owner, observation, and governance-terminal identity slots; candidate artifact/digest binding.
- **Preconditions:** `NV-01` execution evidence is valid and immutable; executor receipt and capability-owner verdict exist; any artifact synchronization is separately authorized; closeout-owner evidence is required.
- **Ordered persistence/provider messages:** retain the completed `NV-01` provider sequence; no new provider message occurs during closeout → persist private/public result → executor receipt → owner verdict → separately authorized owner synchronization and reconciliation → precloseout → missing/failed joined closeout-owner evidence → persist Task Session non-terminal stop and residue; do not mint governance terminal.
- **Result and gate:** execution result remains valid, but governance terminality fails at the closeout join.
- **First stop:** missing, invalid, or non-pass closeout-owner evidence.
- **Forbidden effects:** completion claim, successor execution, promotion, Goal/Craft advance, mutation of the RWO result, or use of provider completion as closeout proof.
- **Proof / validator:** `specified-unexecuted`; exact validator `TestCodexTraceTaskSessionCloseoutFailure`. Evidence: [authority explorer receipt chain](research.md#spawn-0003--explorer-authority-integration), `arcanum/arcana/task-session/SKILL.md:239-417`.

### `NV-10` — exact durability cut matrix

- **Identity set:** manifest ID/digest; exact nine cut IDs and 42 case IDs; selector and source-file hashes; fixture/profile/binary/namespace hashes; per-case attempt/operation/send/armed/fence/raw/terminal/Rust/projection identities; crash-point ID; pre/post journal sequences; reopen/result ID.
- **Preconditions:** exact-set manifest is validated with no missing/extra/duplicate IDs, selectors or hashes; isolated deterministic fixture state exists for each case; historical fake-Eve results are excluded from Codex pass counts.
- **Ordered persistence/provider messages:** for each case validate manifest binding → establish pre-cut state → execute the declared deterministic fixture boundary. The provider-message denominator is initialize request/response/`initialized`; `thread/start` response/`thread/started`; `turn/start` response/`turn/started`; permission request/response/`serverRequest/resolved`; interrupt request/response/`turn/completed(interrupted)`; armed reconciliation `thread/list`/`thread/read`/`thread/resume` request/responses; and the eight NV-01 inbound raw messages bound by the 16 raw-evidence pre/post cases → crash immediately before or after the named boundary → reopen → replay only synced raw evidence → assert journal/cursor/fence/operation/raw/terminal/Rust/projection cardinalities → persist one case result. No live model/provider run is part of this validator.
- **Result and gate:** aggregate passes only when all nine IDs and all 42 exact cases have one passing result under bound hashes.
- **First stop:** first stale/missing/extra/duplicate selector/hash/case, cardinality mismatch, masked failure, or post-reopen assertion failure.
- **Forbidden effects:** skipped cuts, cleanup masking a failure, historical-result substitution, live provider inference, or readiness/acceptance claim.
- **Proof / validator:** all cases `specified-unexecuted`; exact validator `TestCodexDurabilityCutMatrixComplete`. Evidence: [denominator durability manifest](feedback/explorer-denominator-round-001.md#inherited-go-durability-cut-manifest).

## Exact durability and eval denominator

The validator must compare the exact cut-ID set, exact case set, selector strings, bound current hashes, and exactly one result per case. Counts are exact, not minima.

| Cut ID | Bound current selector | Required Codex cases | Status |
|---|---|---:|---|
| `DUR-STORE-APPEND-SYNC` | `durable_store.go:257-307 / 313-337,461-465` | 2 | `specified-unexecuted` |
| `DUR-CURSOR-CAS` | `durable_store.go:281-289,317-335; durable_runtime.go:217-247` | 2 | `specified-unexecuted` |
| `DUR-LEASE-FENCE` | `attempts.go:223-249,614-622,659-697,803-813` | 2 | `specified-unexecuted` |
| `DUR-ARM-BEFORE-SEND` | `attempts.go:252-283,396-429` | 2 | `specified-unexecuted` |
| `DUR-PROVIDER-WRITE` | Eve precedent `eve_leaf.go:84-126`; Codex pre/post initialize, thread/start, turn/start, permission response, interrupt, reconciliation | 12 | `specified-unexecuted` |
| `DUR-RAW-EVIDENCE` | `eve_leaf.go:160-177; terminal.go:128-146`; pre/post each of eight NV-01 inbound messages | 16 | `specified-unexecuted` |
| `DUR-TERMINAL-CONVERGENCE` | `terminal.go:203-322,347-398` | 2 | `specified-unexecuted` |
| `DUR-RUST-REDUCTION-ADMISSION` | `durable_runtime.go:144-180,201-247` | 2 | `specified-unexecuted` |
| `DUR-OUTER-PROJECTION` | no implementation; `cmd/rwo-local-runtime/main.go:118-134` | 2 | `specified-unexecuted` |
| **Exact total** | **9 IDs** | **42** | **none executed** |

Evidence: [RWO explorer durability feedback](feedback/explorer-denominator-round-001.md#inherited-go-durability-cut-manifest) and [non-vacuity review](reviews/round-002-non-vacuity.md); current selectors `source-observed`, older fake-Eve tests `historical`, every Codex case `specified-unexecuted`.

The broader eval run also includes exact raw-wire schema/profile fixtures; binary/source/schema/fixture denominator parity; host tool/network denial negatives; output/diff versus actual filesystem inventory; permission resolution/clearing; privacy filtering; Task Session receipt topology; lifecycle non-promotion; retained Rust offline and differential/vector suites; and ported material, fence, ambiguity, convergence, divergence, and no-successor tests. Experiment Harness owns the mechanics; no eval result is owner acceptance. Evidence: [authority explorer required eval matrix](research.md#spawn-0003--explorer-authority-integration) and [Codex explorer C01-C17](research.md#spawn-0002--explorer-codex-protocol); `specified-unexecuted`.

## Schema and naming migration map

| Eve/V1 surface | V2 target | Preservation rule | Proof |
|---|---|---|---|
| Eve HTTP/NDJSON/session leaf | Private stdio JSON-RPC Codex translator | Replace active leaf; retain historical source/evidence. | active ledger + Codex protocol matrix; target `specified-unexecuted` |
| `RWO-EVE-REQUEST-V1`, `requestInput`, Eve request errors | Versioned provider-neutral request/material contract plus Codex operation requests | Preserve V1 decoder; do not alias old bytes into V2. | [RWO explorer component map](research.md#spawn-0001--explorer-rwo-eve-inventory); `source-observed` / `specified-unexecuted` |
| `SessionID`, `session_known`, stream attach/detach, `LastEventID` | Provider binding with process/connection epochs, thread/turn/item/server-request IDs, ordered operations, and local raw-message arrival cursor | New V2 namespace; App Server pagination cursor is not the replay cursor. | `attempts.go:57-177,371-487` + Codex explorer identity namespace; current shape `source-observed`, V2 `specified-unexecuted` |
| `RawEveLineV1` and Eve event grammar | Versioned raw App Server JSON-RPC record plus normalized provider-event record with all source hashes | Preserve and keep decoding V1; never reinterpret it as Codex. | `terminal.go:19-146` + active ledger; `source-observed` / `specified-unexecuted` |
| Eve session terminal key | Provider-neutral terminal candidate bound to attempt, operation closure, outputs, effects, approvals, profile/binary/namespace digests, and raw evidence | Rust admission remains separate and `0..1`. | `terminal.go:203-398` + synthesis identity model; target `specified-unexecuted` |
| One create/send identity | Attempt → ordered operation → one-or-more send tries → exactly one armed-send per try | Same operation/request on proven resend; new send-try and armed-send IDs. | migration-integrity review; `specified-unexecuted` |
| Synthetic agent-message path/digest | Authoritative file-change items, turn diff, and host-observed filesystem/output inventory | Host inventory wins; mismatch blocks. | `arcanum/framework/runtime/development/fixtures/app-server/f01-refine-success/expected-host-result.json:1` + Codex explorer `GAP-OUTPUT-05`; current fixture `fixture-observed`, target `specified-unexecuted` |
| Existing RWO Work-Pack/lifecycle IDs | New private Refine/Invoke migration epoch and new owner-issued identifiers | Preserve old IDs/receipts; do not reuse DRT-001 or rewrite history. | [authority explorer lifecycle impact](research.md#spawn-0003--explorer-authority-integration) → current `WORK-PACK.md:1-13,23-39,65-70,85-102`; `source-observed` |

## Prospective, non-exact changed-byte inventory

This section is a planning surface, not an exact add/modify/delete manifest. The current known existing paths implicated by the evidence are:

- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/attempts.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/attempts_test.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/seat_material.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/seat_material_test.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/terminal.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/terminal_test.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/durable_e2e_test.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/failure_injection_test.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/eve_leaf.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/eve_leaf_test.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/cmd/rwo-local-runtime/main.go`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/README.md`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/testdata/eve-one-seat/authorization-event.json`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/testdata/eve-one-seat/composition-tuple.json`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/testdata/eve-one-seat/composition.json`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/testdata/eve-one-seat/output-schema.json`
- `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/testdata/eve-one-seat/seat-manifest.json`
- `docs/features/recursive-work-orchestrator/README.md`

Potential additions are intentionally stated as owner-selected path families, not invented filenames:

- a private RWO Go provider adapter/stdio translator implementation-and-test family;
- a private V2 provider-binding, operation/send, raw-evidence, reconciliation, terminal, namespace, and schema family;
- a private raw-wire App Server fixture, C01-C17/NV trace, and exact durability-manifest/result family;
- a private current validation report, versioned ontology migration, Refine/Invoke migration epoch, and owner-issued Work-Pack family;
- conditionally, an existing-owner-selected provider-generic `framework/runtime` registry/schema/test family, only after a bounded insufficiency finding and separate public-owner authority.

Whether any existing file is modified, retained only as history, renamed, or deleted; the exact paths chosen for every addition; the exact current ontology/doc member set; and every conditional public Arcanum path remain `P0` Git-aware residue. P0 must produce the exact add/modify/delete inventory, ownership, hashes, and concurrent-work exclusions before mutation. Evidence: [RWO explorer prospective inventory and dependency DAG](research.md#spawn-0001--explorer-rwo-eve-inventory), [denominator active ledger](feedback/explorer-denominator-round-001.md#active-eve-ledger), and [authority explorer public/private boundary](research.md#spawn-0003--explorer-authority-integration); known existing paths `source-observed`, candidate membership and additions `specified-unexecuted`.

## Dependency-ordered non-executed implementation Work Pack

This Work Pack is a planning proposal only. Its step labels are local to this artifact; they are not admitted SWU or lifecycle identifiers.

| Step | Owner / bounded output | Required validation and gate | Stop condition |
|---|---|---|---|
| `P0` current-byte closure | Inventory owner: fresh Git-aware tracked/untracked/deleted/ignored inventory, exact hashes, ownership split, concurrent-work exclusions. | Exact denominator and changed-byte manifest; human resolves any ownership ambiguity. | Any unclassified or appropriated byte. |
| `P1` freeze inputs | Relevant source owners: pin Rust/Go and runtime/Task Session bytes; record the official App Server URL and observation date plus any future owner-captured immutable snapshot identity; pin installed binary path/version/hash, schema/fixture sources, namespace digest, and parity posture. The current official-page evidence is not revision-pinned. | Hash and schema denominator validator. | Drift, missing immutable source identity, or parity unknown remains explicit; no live leaf. |
| `P2` new migration epoch | Refine/Invoke owners: author a new private migration design/plan/Work Pack with new IDs. | Owner review of boundaries, dependencies, acceptance criteria, and no reuse of DRT-001. | Any attempt to stretch prior admission or acceptance. |
| `P3` public-surface sufficiency | Current `framework/runtime` owner: prove existing surface sufficient or issue a bounded insufficiency finding. | Duplicate-owner/registry/controller check; private-vocabulary leak check. | No public mutation without insufficiency proof and separate authority. |
| `P4` contracts | Owning public/private schema owners: validate generic public envelopes and private V2 identity/cardinality/persistence/result schemas. | Schema, namespace digest, authority-null, non-substitution, V1 decoder, privacy checks. | Missing digest/cardinality, V1 reinterpretation, or private/public leak. |
| `P5` provider-neutral Go extraction | Private RWO owner: generalize attempts/material/operation/terminal surfaces while retaining Rust and Go owner boundaries. | Existing provider-neutral suites plus V1 compatibility and exact replay/divergence tests. | Semantic scheduling, retry, or terminal authority moves owner. |
| `P6` Codex leaf and runtime wiring | Private RWO owner: stdio translator, raw persistence, epochs, reconciliation, outputs/effects validation, and real CLI workers. | Raw-wire fixtures, arm-before-write proofs, typed terminal rules, no second scheduler/store. | Live provider use, ambiguous resend, or missing host-denial enforcement. |
| `P7` finite evidence closure | Experiment Harness owner: materialize C01-C17, NV-01..10/NV-05C, exact nine-ID/42-case crash matrix, Task Session and privacy fixtures. | Exact-set validators; unit/integration/generation/whitespace checks; independent non-vacuity and migration review. | Any missing, extra, masked, stale, or non-discriminating case. |
| `P8` parity and bounded canary gate | Protocol/runtime owners: prove installed binary/source/schema/fixture parity and host-enforced tool/network denial. | Negative denial witnesses and exact parity report. Then separately request a read-only canary admission. | No canary while parity/denial/reconciliation is open; mutation canary needs separate admission. |
| `P9` acceptance and closeout | Capability, Task Session, observation, and lifecycle owners: fresh validation, exact candidate inventory/digests, independent review, capability-owner verdict, closeout integration, privacy-safe observation, lifecycle non-promotion proof. | Exact candidate acceptance request and owner-specific gates. | No acceptance, completion, publication, release, deployment, or promotion by inference. |

Dependency order is strict: `P0 → P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8 → P9`. Public Arcanum changes, if any, follow the public owner's promotion gate and selectively regenerate only affected packages; bulk generated-surface replacement is forbidden. Evidence: [authority explorer implementation outline](research.md#spawn-0003--explorer-authority-integration), [RWO explorer migration DAG](research.md#spawn-0001--explorer-rwo-eve-inventory), and [reviewed synthesis dependency order](synthesis.md#blockers-and-dependency-order); `specified-unexecuted`.

## Open gates and final residue

The planning decision is closed; implementation admission is not. The required open gates are:

- fresh Git-aware inventory and concurrent-byte ownership;
- current CLI attempt/provider/terminal/delivery worker design and wiring;
- installed binary/source/schema/fixture parity;
- host-enforced tool and network denial with negative witnesses;
- exact unique reconciliation for ambiguous `thread/start` and `turn/start`, or fail-closed freeze;
- raw-wire fixtures and every durability crash cut;
- new private Refine/Invoke migration epoch and owner-issued Work Pack;
- fresh validation, independent review, exact capability-owner acceptance, Task Session closeout, privacy-safe observation, and lifecycle non-promotion evidence.

F-01 remains a deterministic normalized translation fixture only. It omits raw JSON-RPC envelopes and several identities/requests, infers output in a way the target must replace, rejects duplicates contrary to the RWO target, and does not prove append-and-sync or crash behavior. Evidence: `arcanum/framework/runtime/development/fixtures/app-server/f01-refine-success/events.jsonl:1-7`, `arcanum/framework/runtime/development/fixtures/app-server/validate_fixture.py:22-38,220-295`, and [Codex explorer gaps 04-07](research.md#spawn-0002--explorer-codex-protocol); `fixture-observed` with target gaps `unverified`/`specified-unexecuted`.

The three round-002 PASS verdicts establish that this planning artifact's source-bound topology, finite witness plan, identity/cardinality separation, and historical-preservation posture survived the scoped reviews. They do not raise the claim ceiling. Evidence: [precedent review](reviews/round-002-precedent.md), [non-vacuity review](reviews/round-002-non-vacuity.md), [migration-integrity review](reviews/round-002-migration-integrity.md); `source-observed` review closure.
