# RWO–Codex Runtime Synthesis

Dispatch: `2026-08-14-rwo-codex-runtime-research`  
Review repair: round 1  
Proof status: `specified-unexecuted`

## Decision

Proceed only as a new, private, fixture-first RWO-to-Codex migration epoch. Codex App Server replaces the Eve transport beneath the existing private RWO Go durability owner. `framework/runtime` remains the single outer envelope. Task Session coordinates admission and closeout synchronization; routed owners mutate only their own artifacts under separate authority, and the named capability owner supplies acceptance.

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

The outer runtime may contain only opaque private-record references and digests. It must not create another App Server run folder, raw-message store, recovery cursor, reconciliation loop, retry owner, or terminal truth. A direct public App Server runtime feeding RWO, a second durable App Server runtime behind RWO, RWO replacing Task Session, provider collaboration satisfying Orchestrate, host goals driving Craft/Goal, and a rename-only Eve migration are rejected.

Current evidence does not justify a live leaf, compatibility, implementation readiness, semantic acceptance, lifecycle completion, publication, release, deployment, or production use.

## Evidence-closed Eve denominator

The exact source package is [explorer-denominator-round-001.md](feedback/explorer-denominator-round-001.md), SHA-256 `1c17c5cd91105e79d2988a8a2b23503c9e90350d6a361b205eaa3934b0223588`. It binds every selector and current file/member hash used below.

- Window: `2026-08-14T14:20:00Z..2026-08-14T14:25:29Z`.
- Expression: `Eve(?=$|[^a-z])|EVE(?=$|[^A-Za-z])|eve(?=$|[^a-z])`.
- Method: `rg -a -n -o --pcre2 --hidden`, excluding `.git`, `target`, `__pycache__`, and `*.pyc`, plus the recorded path-only and Eve-shaped semantic checks.
- Scope: the exact RWO Go, Rust, planning, definitions, docs, handoff-notice, and four unrelated-history roots enumerated in the evidence package.
- Closure: 2,378 literal occurrences; 284 literal-hit files; three path-only fixture files; one semantic-only Eve-shaped file; 288 classified files; zero unclassified; zero duplicates; zero Rust-source and recursive-definition occurrences.

| Class | Count | Disposition |
|---|---:|---|
| active provider | 122 | replace or version-separate through private Codex migration |
| provider-neutral Eve-named | 3 literals plus 1 selector family | generalize in V2; preserve V1 |
| test/fixture | 113 | port generic checks; replace Eve protocol cases |
| current docs | 68 | update/version only after new proof |
| generated/lifecycle | 265 | preserve IDs; supersede only through owner |
| immutable history | 1,630 | preserve unchanged |
| unrelated history | 177 | leave untouched |

The active ledger is exactly the thirteen rows/families in the evidence package: `eve_leaf.go`, the active and provider-neutral selectors in `seat_material.go`, the raw/provider selectors in `terminal.go`, the V1 session/stream selector family in `attempts.go`, five test files, the five-member `testdata/eve-one-seat/` family, and the Go README. Each has one hash-bound disposition. The evidence package also binds current-doc, ontology, lifecycle, immutable-history, handoff-notice, and unrelated-history families by member-manifest hash.

This is readable-filesystem closure only for the named roots/window. It is not tracked/untracked/deleted/ignored or post-window Git closure. A mutation Work Pack must refresh a Git-aware inventory without appropriating concurrent work.

## Authority allocation

| Concern | Sole owner and boundary |
|---|---|
| Semantic decision | Rust authors accepted-event and command identity, zero-or-one successor, and no-successor. |
| Semantic-record persistence | Go append-and-syncs and projects Rust-authored semantic records; it never authors/reinterprets them. |
| Provider translation | Private translator validates raw JSON-RPC schema, identity, order, approval closure, items/outputs, and provider-terminal closure. |
| Physical convergence | Go attempt/terminal coordinators own attempts, sends, leases, fences, ambiguity, reconciliation, physical retry eligibility, and durable admission recording. |
| Semantic terminal acceptance | Rust accepts/rejects the provider-neutral terminal and decides the successor. |
| Outer execution | `framework/runtime` launches the registered child and projects generic status plus opaque references/digests only. |
| Admission/governance terminal | Task Session coordinates admission, validates receipt topology, joins owner evidence, and determines governance terminality. |
| Artifact mutation / acceptance | Routed artifact owner mutates separately authorized owned bytes; named capability owner supplies acceptance. |
| Project control | Craft alone applies ledger changes; Goal alone owns frontier/round routing and staged proposals. |
| Agents / eval / observation | Orchestrate owns governed native dispatch; Experiment Harness owns test mechanics; OIL routes post-primary observation; Signal Observer stores privacy-safe non-verdict telemetry. |
| Promotion/publication | Target lifecycle owner accepts one exact revision through its own gate. |

## Versioned identity and relation model

Every private V2 record binds `schema_version`, a `namespace_digest` over canonical schema IDs/names/cardinalities, `provider_profile_digest`, `binary_digest`, `attempt_id`, record-specific identity, canonical payload hash, and journal sequence. Missing or changed digests block before interpretation. Persisted Eve V1 records retain their original meaning and are never decoded as V2.

| Relation | Cardinality and rule |
|---|---|
| semantic command → attempt | `1 → 0..n`; a new attempt is not new semantic work |
| attempt → active provider binding | `1 → 0..1` in profile 1 |
| attempt → provider operation | `1 → 0..n`, strictly ordered |
| operation → send try | `1 → 1..n`; every try has a unique `send_try_id` and strictly increasing per-operation `send_try_ordinal`; try >1 only after durable exact-known-not-sent proof |
| send try → armed-send record | exactly one immutable record with a unique `armed_send_id`, append-and-synced before that try’s effectful provider write |
| process epoch → connection epoch | `1 → 1..n`; restart mints process epoch, reconnect mints connection epoch |
| connection epoch → JSON-RPC request ID | `1 → 0..n`; uniqueness is connection-scoped |
| attempt → thread / thread → admitted turn | `0..1` / exactly one; recovery reads create neither |
| turn → item / turn-item → server request | `0..n` / `0..n`; each request receives at most one response |
| raw message → connection / operation | exactly one / `0..1`; unsolicited messages correlate by thread/turn/arrival |
| normalized event → raw messages | `1..n`, with every source hash explicit |
| terminal candidate → attempt | exactly one after evidence closure |
| Rust admission → terminal candidate | `0..1`; block/rejection creates no accepted event |

A process epoch binds executable path/version/hash, profile, argv, cwd, and environment-name allowlist before launch. A connection epoch binds one initialized JSON-RPC connection. Thread rebinding across epochs requires a synced reconciliation record. Provider process/connection/request/thread/turn/item/server-request IDs never substitute for RWO, Task Session, runtime, receipt, Craft, Goal, or Orchestrate identities.

Before each send try’s effectful provider write, Go append-and-syncs exactly one immutable armed-send record binding armed-send ID, operation ID/ordinal/kind, attempt, unique send-try ID/ordinal, lease/fence, process/connection epochs, canonical request hash, input/policy/profile/binary digests, known provider targets, allowed response/notification kinds, state, and journal sequence. The write may occur only after that try’s armed-send record is synced. A crash, timeout, or disconnect without exact-known-not-sent proof yields `delivery_unknown` and freezes; it never authorizes resend.

Exact same scoped identity, kind, causal position, and payload hash records a duplicate observation but emits no second normalized event. Same identity/position with a changed hash records `REPLAY_MISMATCH` and blocks before translation, output, terminal admission, or retry. F-01’s current rejection of exact duplicates is a gap, not target evidence.

Ambiguity recovery first persists `delivery_unknown`, freezes, and forbids resend. Read/list/resume calls use new armed operations and epochs; all raw responses persist before comparison. Unfreeze requires exactly one candidate matching every available frozen predecessor/input/policy/profile/request discriminator, with the candidate set and decision synced first. Zero/multiple/insufficient/mismatched candidates remain frozen. Documentation does not yet prove sufficient discriminators.

## Field-level public/private contracts

Public Arcanum may own only provider-generic envelopes and explicit authority nulls:

- `durable-child.adapter-manifest.v0`: adapter ID, executable path/version/hash, argv, cwd, environment-name allowlist, timeout, input/output schema refs/hashes, authority ceiling, manifest hash.
- `framework-runtime.child-handoff.v0`: runtime ID, adapter/manifest hash, input/policy refs/hashes, readable/writable roots, network policy, deadline, expected result ref.
- `framework-runtime.projected-event.v0`: runtime ID, sequence, phase, opaque child-record ref/hash, observed time—never raw messages or recovery cursor.
- `framework-runtime.child-result.v0`: host status, provider-evidence ref/hash, output inventory, typed error, proof status, next owner, authority nulls.
- `app-server.protocol-profile.v0`: source/revision, binary/schema hashes, transport, allowed operations, denied capabilities, sandbox/network/approval policies, profile hash.
- `app-server.host-result.v0`: provider epochs/thread/turn/item/request inventories, raw/approval evidence refs/hashes, provider terminal/error, actual outputs, diff hash, recovery disposition, proof status, next owner, authority nulls.

Public authority nulls must explicitly null semantic verdict, Task Session admission/terminal, capability acceptance, Craft/Goal state, dispatch acceptance, and lifecycle promotion. Before any public extension, the existing runtime owner must prove the current adapter surface lacks an exact field/rule, then extend its existing registry/controller. A second registry, controller, or public RWO special case is forbidden.

Private `rwo.codex-*.v2` records own provider binding, armed operations/sends/fences, raw message blobs and scoped IDs, reconciliation candidates/decision, terminal candidate/effect/output validation, Rust decision reference, semantic commit sequence, and private runtime result. Private values project publicly only as opaque reference plus digest. RWO vocabulary, mappings, journal records, retry/ambiguity/terminal rules, translator logic, and migration history never enter public Arcanum.

## Retry-scope matrix

| Scope | Owner | Required proof | Permitted / forbidden |
|---|---|---|---|
| same-operation resend | Go coordinator | durable exact-known-not-sent proof, live fence, and the same operation/request with unchanged hashes | resend the same operation/request using new send-try and armed-send identities; uncertainty is not proof |
| provider reconciliation | Go plus translator | durable unknown, new epoch, armed read/list/resume | inspect/bind existing work; never resend/new admission |
| RWO `RetrySame` | Rust decision plus Go | explicit continuation after typed disposition | new attempt, same semantic command; provider failure alone is insufficient |
| Task Session recovery | Task Session | valid ticket/admission lineage | recover task coordination; never authorize provider resend/new semantic command |
| Orchestrate retry | Orchestrate | valid route and explicit fresh-run authority | new native run/action; provider/RWO identities cannot satisfy it |
| Goal round | Goal | audited frontier and round token | next bounded project action; never a provider retry |
| Craft apply retry | Craft | re-audited delta and ledger/frontier binding | exact owned ledger apply only |

## Exact durability denominator

The future manifest contains exactly nine IDs and 42 required cases; `TestCodexDurabilityCutMatrixComplete` must compare exact ID/case sets, selector strings, bound hashes, and one fixture result per case. All Codex cases remain `specified-unexecuted`.

| Cut | Exact current selector surface | Cases |
|---|---|---:|
| `DUR-STORE-APPEND-SYNC` | `durable_store.go:257-307 / 313-337,461-465` | 2 |
| `DUR-CURSOR-CAS` | `durable_store.go:281-289,317-335; durable_runtime.go:217-247` | 2 |
| `DUR-LEASE-FENCE` | `attempts.go:223-249,614-622,659-697,803-813` | 2 |
| `DUR-ARM-BEFORE-SEND` | `attempts.go:252-283,396-429` | 2 |
| `DUR-PROVIDER-WRITE` | Eve precedent `eve_leaf.go:84-126`; Codex pre/post for initialize, thread/start, turn/start, permission response, interrupt, reconciliation | 12 |
| `DUR-RAW-EVIDENCE` | `eve_leaf.go:160-177; terminal.go:128-146`; pre/post for eight NV-01 messages | 16 |
| `DUR-TERMINAL-CONVERGENCE` | `terminal.go:203-322,347-398` | 2 |
| `DUR-RUST-REDUCTION-ADMISSION` | `durable_runtime.go:144-180,201-247` | 2 |
| `DUR-OUTER-PROJECTION` | no implementation; CLI stops at `cmd/rwo-local-runtime/main.go:118-134` | 2 |

Current file hashes and historical fake-Eve witness names are bound in the denominator evidence package. No historical test ran during this research, drift prevents treating it as current acceptance, and no Codex cut has executed.

## Finite trace specifications

Each future fixture contains `trace_id`, `identity_set`, `preconditions`, `persisted_sequence`, `provider_sequence`, `expected_result`, `gate`, `first_stop`, `forbidden_effects`, `proof_status`, and `validator`. Every inbound provider message persists before interpretation.

| Trace | Preconditions and ordered persisted/provider sequence | Result/gate and first stop | Forbidden effects | Status / validator |
|---|---|---|---|---|
| `NV-01` success | Valid ticket/runtime; bound command/cursor, attempt, init/thread/turn operations, epochs, RPC/thread/turn/item IDs, immutable hashes and fence. Persist admission→attempt/fence→arm/send/persist initialize→arm/send/persist thread response/started→arm/send/persist turn response/started→persist item started/completed and turn completed→translator closure→Go terminal candidate→Rust accept/no-successor→synced semantic/admission→opaque outer projection. | Host success only after every gate; first digest/identity/order/output/fence/durability/Rust failure stops. | second thread/turn, blind resend, completion-as-semantic-success, raw outer data, automatic closeout/promotion/next work | specified-unexecuted / `TestCodexTraceSuccessNoSuccessor` |
| `NV-02` permission | Bound turn and frozen policy. Persist scoped server request→physical pause→policy compare. Equal scope: persist approved-once intent→arm/send one response→persist resolved. Expanded scope: persist deny/block before effect; clear once on resolution/terminal. | Equal may continue once; expansion/unknown blocks at comparison. | session grant, second response, expanded effect, provider permission as admission/acceptance/Craft/promotion | specified-unexecuted / `TestCodexTracePermissionPauseAndScopeExpansion` |
| `NV-03` stale input | Ticket input digest differs at launch. Persist admission/frozen hash→recompute→persist mismatch/block→opaque projection. No provider identities exist. | Block before process launch; first inequality stops. | process/connection/thread/turn, output, retry, execution receipt | specified-unexecuted / `TestCodexTraceStaleInputStopsBeforeLaunch` |
| `NV-04` interrupt/recovery | One bound turn/residue. Persist interrupt intent→arm/send interrupt→persist response (not terminal)→persist interrupted completion/residue→new epoch→arm read/resume→persist recovery without turn/start. | Interrupted result; unresolved identity stops; further work needs new attempt authority. | reuse scoped RPC ID, replay turn/start, resume-as-retry, delete residue, automatic attempt | specified-unexecuted / `TestCodexTraceInterruptRecoveryOnlyResume` |
| `NV-05A` unique reconcile | Armed create lost before response. Persist unknown/freeze→new epochs without create resend→arm read/list→persist all candidates→compare frozen discriminators→sync exactly one match/selection→unfreeze. | Continue only on one full match; zero/multiple/missing/mismatch stops. | second create, nearest-time selection, semantic admission, reconnection-as-proof | specified-unexecuted and discriminators unproved / `TestCodexTraceAmbiguousCreateUniqueReconciliation` |
| `NV-05B` ambiguous freeze | Same uncertainty, but zero/multiple/insufficient candidates. Persist candidates/comparison→`AMBIGUOUS_THREAD_CREATE` with null selection→retain freeze. | Terminal block for attempt at failed unique predicate. | resend, arbitrary binding, turn start, output, accepted event, automatic retry | specified-unexecuted / `TestCodexTraceAmbiguousCreateFreezes` |
| `NV-06` duplicate inert | First raw scoped identity/hash already synced and translated. Persist exact duplicate observation referencing original; emit no normalized event. | Inert audit no-op; equality is first stop. | protocol-failure rejection, second output/event/cursor/retry | specified-unexecuted; F-01 is contrary gap / `TestCodexTraceExactDuplicateIsInert` |
| `NV-07` mismatch | Original message interpreted; same scoped identity/position arrives with changed hash. Sync raw mismatch then `REPLAY_MISMATCH`; freeze before translation. | Block at hash inequality. | overwrite, interpretation, output, retry, accepted event, success | specified-unexecuted / `TestCodexTraceIdentityHashMismatchBlocks` |
| `NV-08` bad events | Four subcases persist raw first: invalid schema→reject; completed item before turn start→order block; item completion plus disconnect without turn terminal→unknown; valid terminal then later event→divergence. | Block or unknown at first grammar/order/disconnect/post-terminal stop; never Rust admission. | inferred/fabricated success, ignored late event, output, retry | specified-unexecuted / `TestCodexTraceInvalidAndPostTerminalEvents` |
| `NV-09` closeout fail | NV-01 execution succeeds→persist private/public result→executor receipt→owner verdict→separately authorized owner sync→closeout join missing/fails→Task Session persists non-terminal stop. | Execution evidence remains; governance terminality fails at closeout evidence. | completion claim, successor, promotion, Goal/Craft advance, rewriting RWO result | specified-unexecuted / `TestCodexTraceTaskSessionCloseoutFailure` |
| `NV-10` durability | Exact nine-row/42-case manifest and hashes. For each: assert sets/selectors/hashes/cardinality→establish pre-cut→crash immediately pre/post boundary→reopen→assert journal/cursor/fence/operation/raw/terminal/Rust/projection counts→record result. | Aggregate passes only if all exact cases pass; first stale/missing/extra/duplicate/cardinality/assertion failure stops. | historical tests as Codex proof, skipped/masked cut, provider run, readiness claim | specified-unexecuted / `TestCodexDurabilityCutMatrixComplete` |

## Blockers and dependency order

Open blockers are: fresh Git-aware current-byte inventory; missing CLI attempt/provider/terminal/delivery wiring; installed `codex 0.148.0-alpha.9` hash `86a428…c2a20` versus fixture source pin parity; unproved closed tool/network denial; no documented create idempotency; F-01 raw/output/duplicate/durability gaps; and the existing validation-only DRT-001 lifecycle route.

Implementation order:

1. Refresh Git-aware inventory and preserve concurrent/historical bytes.
2. Freeze Rust/Go, Arcanum runtime/Task Session, official App Server protocol, installed binary, namespace digest, and parity posture.
3. Create a new private Refine/Invoke migration epoch and Work Pack.
4. Prove existing runtime adapter insufficiency before its owner extends the current generic surface.
5. Define/validate the public generic and private V2 contracts.
6. Extract provider-neutral attempt/material/operation/terminal contracts without reinterpreting V1.
7. Implement private stdio translator, raw persistence, epochs, reconciliation, and real CLI workers.
8. Materialize and run NV-01..10, including all 42 durability cases.
9. Prove binary/schema/fixture parity and host denial; only then request a separately admitted read-only canary.
10. Issue fresh validation, independent review, exact capability-owner acceptance request, Task Session closeout integration, privacy-safe observation, and lifecycle non-promotion proof.

## Claim ceiling

This closes a source-grounded planning artifact for the scoped filesystem denominator. It specifies but does not execute the Codex identity model, contracts, traces, reconciliation, or durability cuts. It proves no Git closure, App Server/model run, RWO–Codex compatibility, implementation readiness, semantic acceptance, Task Session completion, lifecycle synchronization, publication, release, deployment, or production property.
