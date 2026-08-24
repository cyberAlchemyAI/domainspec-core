# Repaired synthesis: Codex App Server ↔ Arcanum

## Claim ceiling

This is a repaired architecture and evidence candidate. It proves no App Server integration, implementation readiness, acceptance, promotion, publication, release, deployment, or production use.

- Official protocol evidence is pinned to `openai/codex@9946da9af1829410271f6b76f9159961f7281e0a`.
- No App Server process or model turn was run.
- Installed `codex-cli 0.147.0-alpha.6.5`, SHA-256 `6e63a38388455ed175ab72d24813d148186e4f6cc55db787fd12b4ebec871012`, was observed; its generated schema was not compared with pinned source.
- Direct App Server integration is absent.
- The proposed integration is an `app-server` adapter/profile inside the existing `arcanum/framework/runtime` durable runtime. It is not a standalone execution host, controller, ledger, journal, reducer, receipt authority, eval loop, or observability truth.
- Ordinary Refine and Task Session use of that adapter is separate from any future App Server-backed Orchestrate host-profile decision.
- `DECISION-LOOP-OWNER-001`, the August 5 finite-series ownership overlap, remains unresolved. This synthesis selects neither Implementation Readiness nor Task Session Until Blocker and introduces no third reducer.

Proof labels are `source-observed`, `fixture-observed`, `runtime-observed`, `specified-unexecuted`, and `unverified`.

Official selectors: pinned App Server README lines 20-44 and 57-89; `common.rs` client/server-request/server-notification definition macros; `turn.rs:288-325`; `item.rs:230-401`. Local selectors and current-byte hashes are inventoried in the three explorer returns and reviews; load-bearing owners below cite the exact canonical path.

## Architecture and placement

```text
Refine or Task Session
  -> existing framework/runtime durable handoff
       RUN.json, HANDOFF.md, STATUS.json, events.jsonl, adapter-state/
  -> proposed framework/runtime profile: app-server
       protocol/binary preflight
       adapter-local native-ID map
       ordered event contribution
       runtime-request translation
       terminal-state translation
  -> Codex App Server
       process_instance_id -> listener_id -> connection_id
       -> threadId -> turnId -> itemId/request_id
       (outbound code-mode-host connection remains separate)
  -> existing runtime status/result
  -> Task Session executor receipt, when Task Session admitted execution
  -> capability-owner verdict and owner receipt
  -> Task Session reconciliation and owner closeout join
  -> Task Session governance terminal receipt
```

`tools/arcanum` already owns runtime command resolution, adapter selection, output capture, and the runtime event log. The adapter owns provider translation only. App Server owns transport and raw execution; Arcanum retains authoring meaning, Work-Pack authorship, confirmation, selection, mutation admission, semantic judgment, receipt admission, continuation, Craft state, Goal control, lifecycle, and external-effect authority.

Two use cases remain separate:

1. Refine may hand one nonmutating stage to the durable runtime. Task Session may hand one live-admitted task attempt to it. Neither requires Orchestrate.
2. Mapping Orchestrate spawn/wait/interrupt/inventory/join/gates to App Server is a separate future profile/schema decision. Current Orchestrate admits `spawn` actions and its Codex host uses `collaboration.*`; this research does not broaden it.

Primary local owners: `arcanum/framework/runtime/README.md`; `arcanum/arcana/task-session/runtime-adapters/`; Task Session mutation-admission, execution-ticket, executor, owner-hook, precloseout, and governance-terminal schemas; `arcanum/runtime/orchestrate/`; Work Pack Readiness; Decision Gate; Goal; Craft; Experiment Harness; Observed Invocation Loop; Signal Observer.

## Exact official denominators

### Transport, disabled mode, and outbound connector

| Surface | Exact denominator | Classification |
|---|---:|---|
| Inbound transports | 3: stdio, TCP WebSocket, Unix-socket WebSocket | current; TCP WS experimental/unsupported |
| Disabled listen mode | 1: `--listen off` | mode, not transport |
| Outbound code-mode-host connector | 1 family with `ws/wss` or root `http/https` gRPC forms | independent connector shared by process threads; deferred |
| Unix proxy | 1 bridge command | proxy to Unix transport, not a fourth transport |

Thus the denominator is 3 inbound transports + one disabled mode + one independent outbound connector family, not two transports. [Pinned App Server README; source-observed]

### Client requests — exact 137-row inventory

The groups are mutually exclusive and sum to 137.

| Group | Count | Exact members/disposition |
|---|---:|---|
| Initialize | 1 | `initialize`; adapter preflight |
| Diagnostics | 1 | `server/diagnostics`; optional read |
| Thread | 38 | start/resume/fork/archive/delete/unsubscribe; elicitation inc/dec; name; goal set/get/clear; metadata; section move; settings; memory mode; unarchive; compact; shell command; guardian approval; background terminals clean/list/terminate; rollback; list/search/search occurrences/loaded/read/turns/items; inject items; realtime start/audio/text/speech/stop/voices |
| Thread sections | 4 | list/create/update/delete |
| Skills | 3 | list/extra roots/config write |
| Hooks | 1 | list |
| Marketplace | 3 | add/remove/upgrade |
| Plugins | 12 | list/search/installed/read/skill read; share save/update/list/checkout/delete; install/uninstall |
| Apps | 3 | read/list/installed |
| Filesystem | 9 | read/write/mkdir/metadata/readdir/remove/copy/watch/unwatch |
| Turns | 3 | start/steer/interrupt |
| Review | 1 | start |
| Model | 1 | list |
| Model provider | 1 | capabilities read |
| Experimental features | 2 | list/enablement set |
| Permission profiles | 1 | list |
| Remote control | 7 | enable/disable/status; pairing start/status; client list/revoke |
| Collaboration mode | 1 | list |
| Experimental mock | 1 | experimental method |
| Environment | 3 | add/info/status |
| MCP server | 3 | OAuth login/resource read/tool call |
| MCP status | 1 | list |
| Config | 4 | MCP reload/read/value write/batch write |
| Windows sandbox | 2 | setup/readiness |
| Account | 9 | login start/cancel/logout; rate limits/reset credit/usage/workspace messages/credits nudge/read |
| Feedback | 1 | upload |
| Sandboxed command | 4 | exec/write/terminate/resize |
| Unsandboxed process | 4 | spawn/stdin/kill/resize |
| External-agent config | 4 | detect/import/history/read histories |
| Config requirements | 1 | read |
| Memory | 1 | reset |
| Deprecated/legacy | 7 | conversation summary; git diff remote; auth status; fuzzy search + start/update/stop |

Arithmetic: `1+1+38+4+3+1+3+12+3+9+3+1+1+1+2+1+7+1+1+3+3+1+4+2+9+1+4+4+4+1+1+7 = 137`. [Pinned `client_request_definitions!`; source-observed]

### Server requests — exact 11 variants

Current 9: command approval, file-change approval, user input, MCP elicitation, permission approval, dynamic tool call, auth-token refresh, attestation generation, current-time read. Deprecated 2: apply-patch approval and exec-command approval. The earlier count 9 is valid only for current explicit variants; macro denominator is 11. [Pinned `server_request_definitions!`; source-observed]

### Server notifications — exact 72 variants

| Family | Count |
|---|---:|
| Thread including realtime | 22 |
| Item | 14 |
| Turn | 5 |
| Hook | 2 |
| Raw upstream | 2 |
| Command | 1 |
| Process | 2 |
| Server request | 1 |
| MCP | 2 |
| Account including login completion | 3 |
| App | 1 |
| Remote control | 1 |
| External-agent config | 2 |
| Filesystem | 1 |
| Model | 3 |
| Warning/error/config | 5 |
| Fuzzy search | 2 |
| Windows | 2 |
| Skills | 1 |

Arithmetic: `22+14+5+2+2+1+2+1+2+3+1+1+2+1+3+5+2+2+1 = 72`. Source marks thread compacted and file-change output delta deprecated, and two raw-response events internal-only; the remaining 68 are current or experimental macro variants. [Pinned `server_notification_definitions!`; source-observed]

User inputs are 7/7: text, image, local image, audio, local audio, skill, mention. Thread items are 18/18: user message, hook prompt, agent message, plan, reasoning, command execution, file change, MCP tool call, dynamic tool call, collaboration-agent call, subagent activity, web search, image view, sleep, image generation, enter/exit review, context compaction. Turn states are in-progress/completed/interrupted/failed; item lifecycle is start, deltas, complete. Thread waiting state is not a Craft blocker or Arcanum gate.

## Local completeness ledger

| Surface | Aggregate | Exact row closure here | Verdict |
|---|---:|---:|---|
| Refine stages | 10 | ten names, no direct per-stage digest ledger | partial/unverified |
| Invoke modes | 7 | seven named: five active, two deferred | partial |
| Invoke templates | 13 physical vs inventory 12 | thirteen named families | conflicting inventory |
| Dispatch techniques | 65 | 0/65 individual rows; 19/31/15 aggregate groups only | open |
| Relevant schemas | 58 | 0/58 rows | open aggregate |
| Generated packages | 14 | 0/14 rows | open aggregate |
| Eval evidence | 9 Goal fixtures, 6 maintenance states, OIL cases, 3 Invoke CLI regimes | no unified member ledger | open aggregate |

No completeness/readiness claim may use the 58, 14, or eval aggregates until an exact ledger records identity, digest, selector, classification, and proof status.

## Hook registry under existing owners

| App Server surface | Existing owner and legal mapping | Typed output/gate | Verdict |
|---|---|---|---|
| Initialize/capabilities | framework runtime profile | runtime run/profile/status; no gate | partial seam; adapter absent |
| Thread start/resume/read | adapter-local state and runtime recovery | host-result contribution only | absent implementation |
| Fork | host operation; executable use needs a separately admitted Task Session attempt | new ticket/admission then thread binding | absent |
| Turn start | execute immutable runtime handoff after live Task Session admission | Task Session executor receipt after normalization | absent |
| Steer | host input to known turn under unchanged policy | runtime event; no Arcanum transition | partial protocol |
| Interrupt | request and reconcile terminal interrupted state | executor result interrupted | reducer absent |
| Item/deltas | adapter contributes ordered events; runtime owns log | provisional evidence | absent extension |
| Terminal/error | adapter translates raw state | host result → executor receipt; never owner verdict | absent |
| Diff | Task Session touched/baseline/output input | executor touched files and validation | partial seam |
| Approval/permission/question | one server request to one runtime-effect response | App Server response only | absent mapping |
| Skills | resolve digest-pinned generated package | profile attachment/cache invalidation | partial |
| Hooks | OIL/Signal Observer derive privacy-safe envelope | observation only | partial |
| MCP/dynamic tools | record tool identity and hashes | evidence input | partial |
| Command exec | possible later runtime validation profile | not current Orchestrate action | deferred/conflicting |
| Collaboration items | diagnostic host items | cannot satisfy Orchestrate join | conflicting if substituted |
| Review | capability-owner evidence | never audit/acceptance alone | partial |
| Token usage | Goal/OIL telemetry | no budget authority | partial |
| Shell/process/realtime | excluded from first adapter | none | conflicting/deferred |
| Global administration | out of scope | none | not applicable |

## Authority matrix

Invoke Plan authors Work Packs. Work Pack Readiness audits without selecting or admitting. Exact human/Decision Gate confirmation is a prerequisite, not admission. Task Session selects one unit and issues live mutation admission. The framework runtime plus App Server profile executes the bounded handoff. The named capability owner judges domain semantics. Task Session reconciles executor and owner evidence and joins closeout. Orchestrate remains the multi-agent dispatch owner but has no role in ordinary adapter use. Craft alone owns project ledger state. Goal owns bounded frontier selection/audit/staging/token consumption, not Craft apply. Experiment Harness owns fixtures/canaries. OIL and Signal Observer own observation. Lifecycle owners retain promotion authority.

## Typed identity namespaces

| Namespace | Fields | Owner/rule |
|---|---|---|
| Orchestrate | `dispatch_id`, `run_id`, `wave_id`, `step_id`, `action_id`, `agent_id` | only a separately designed Orchestrate host profile |
| Task Session | `run_id`, `task_id`, `swu_id`, `ticket_id`, `attemptId`, `admissionToken`, `idempotency_key` | one executable thread per admitted attempt; SWU remains separate |
| Durable runtime | runtime run ID, adapter ID, run/status/event sequence | parent envelope/store |
| Adapter-local | `process_instance_id`, inbound `listener_id`, inbound `connection_id`, protocol commit, binary digest, cursor; separately, optional outbound code-mode-host connection ID | provider-local map; inbound relation is `process_instance_id -> listener_id -> connection_id -> threadId`; the outbound connector is independent and not a listener/connection in this chain |
| App Server | `threadId`, `turnId`, `itemId`, request ID, command process ID, unsandboxed process handle | raw host IDs only |
| Craft | scope/context, ledger digest/rows | never thread/host-goal IDs |
| Goal | context, frontier snapshot, round, route, batch, token | never host goal/token usage |

Forbidden: `threadId=agent_id/run_id/Craft context`; `turnId=action_id/ticket/attempt`; `itemId=receipt`; request ID=approval/gate/acceptance; fork=attempt; steer=Arcanum transition. One thread may contain many turns. Initial profile binds at most one executable turn to one admitted Task Session attempt; `swu_id` identifies neither.

## Typed result/receipt chain

| Type | Exact type/owner | Substitution rule |
|---|---|---|
| Raw host result | proposed adapter-local `app-server.host-result.v0` under framework runtime | not an Arcanum receipt |
| Runtime status | existing `STATUS.json` | not downstream receipt |
| Orchestrate action receipt | `arcanum.native-dispatch-runner.receipt.v0.1` | exact action/join only |
| Task Session executor | `task-session.executor-receipt.v1` | not owner verdict |
| Capability-owner receipt | owner-native verdict or `task-session.owner-hook-receipt.v1` | not executor/terminal |
| Precloseout | `task-session.precloseout-execution-receipt.v1` | no synchronized completion |
| Task Session terminal | `task-session.governance-terminal-receipt.v1` | no lifecycle promotion |
| Goal owner-route result | Goal execution-receipt schema | not Task Session/owner receipt |
| Proposed Craft apply artifact | candidate `craft.proposed-ledger-apply-receipt.v0`; canonical schema absent | nothing until Craft owns/validates |
| Eval result | Experiment Harness report/profile | evidence only |
| OIL observation | OIL result + Signal Observer row | observation only |
| Lifecycle promotion | type-specific lifecycle receipt | lifecycle transition only |

Execution order: raw host terminal → Task Session executor receipt → capability-owner verdict/receipt → Task Session reconciliation → precloseout → required owner closeout join → Task Session governance terminal. Task Session does not own domain judgment.

## Typed approvals and acceptance

| Edge | Owner/scope/digest/use | Consumed effect |
|---|---|---|
| App Server response | one live request ID bound to method/thread/turn/item/payload hash; one response | runtime effect only |
| Dispatch confirmation | human, exact sheet/route digest, one dispatch | registration/spawn only |
| Work-Pack confirmation | human/Decision Gate/exact binding owner, Work-Pack/epoch/semantic/profile digest | permits selection flow, not mutation |
| Decision Gate record | exact target/scope/hazard/request digest; single-use/expiry and consumed-by | named non-protected decision only |
| Goal batch token | Goal/Decision Gate, batch/scope/decision digest, single-use or declared batch scope | one Craft-owned apply attempt |
| Capability-owner acceptance | named owner, candidate/validation digest, one attempt | owner receipt for closeout |
| Lifecycle promotion | type-specific lifecycle owner, candidate/eval/review digest, one transition | lifecycle state only |
| Publication/release/deployment | separate target owner, exact revision/target, one operation | named external effect only |

No row authorizes a later row.

## Refine, Invoke, and thread topology

The ten explorer-reported Refine stages are Context Builder; Invoke Define; Interrogation review; research decision; Distill; Invoke Design; design review; Distill Repair; Invoke Plan; final Refine synthesis. This is partial/unverified without the missing per-stage ledger. Each stage owner supplies immutable input, mode, write/validation scope, and validates its owner result; turn completion cannot advance the stage.

Invoke modes: active define/design/plan/handoff/refresh; deferred full/validate. Thirteen physical templates are named in research, while inventory declares twelve; conflict remains. Dispatch techniques remain aggregate-only at 19 composition/31 standards/15 boundary-evidence.

Preferred topology: independent thread per Refine stage; one executable thread per admitted Task Session attempt. Resume is recovery and revalidates admission/digests. Fork requires new admission. A long-lived project thread may be a read-only projection only. App Server-backed Orchestrate remains deferred and separate.

## Sandbox policy

Pin protocol/binary, runtime/adapter ID, cwd, sandbox/permission/approval mode, network, allowed reads/writes, Task Session baselines/validation, model/config, budgets/stops, forbidden effects, privacy/observation. Initial profile: stdio; no outbound host/realtime/shell/process/direct filesystem mutation/global administration; no dynamic permission expansion beyond one request; trust changes are mutations; command exec is a separate decision. Permission pause freezes the admission digest and requires revalidation.

## Primitive placement

App Server profile/terminal translation and native ID map belong inside framework runtime adapter state. Ordered events extend existing runtime log. Task Session owns ticket/admission/executor/reconciliation extensions. Replay uses adapter state plus current Task Session idempotence; future Orchestrate replay stays in Orchestrate. Runtime approval mapping stays in adapter while existing owners retain decisions. Task Session retains touched/baseline validation. Craft owns missing receipt ingestion/row plan/render/index/CAS apply. Goal owns missing round journal/no-progress execution. Experiment Harness owns App Server fixture player, failure injection, denominator oracle, parity and live canary. OIL/Signal Observer own privacy-safe observation. Generation/sync owns attachment/digest pin. Existing lifecycle owners plus Experiment Harness own non-promotion regression.

## Bounded iterative Goal control loop

```text
Goal bind -> Craft frontier snapshot -> select one node/owner route
 -> owner executes (possibly Task Session + adapter)
 -> typed owner-route receipt -> audit -> staged proposed delta
 -> exact Goal/Decision Gate batch token
 -> Craft-owned validation/apply -> recompute frontier
 -> next bounded round | Goal complete | no-progress stop | budget stop
```

Craft is sole ledger authority. Goal owns frontier/route/audit/staging/token consumption/loop result. App Server owns none. `DECISION-LOOP-OWNER-001` remains open between Implementation Readiness finite-frontier/until-blocker and Task Session Until Blocker bounded series. Goal project rounds do not resolve it; no adapter/Orchestrate profile may become a third reducer.

## Nine exact candidate fixture contracts

Every value below is illustrative; repeated hex strings are synthetic. All cases are `specified-unexecuted`, not witnesses.

### F-01 — one Refine stage

IDs: runtime `rt-refine-001`, Refine run `refine-candidate-001`, stage `invoke-design`, process `asp-fixture-01`, connection `conn-stdio-01`, thread `thr-refine-001`, turn `turn-refine-001`. Input `context-pack.json` digest `sha256:1111...1111`. Policy: fixture cwd; read-only except `/fixture/out/design.md`; network denied; digest-pinned skill; no Task Session. Events: runtime created → initialize/initialized → thread start/started → turn start/started → agent-message item start/complete → turn completed → adapter host result. Results: candidate host result, runtime status passed, owner-local Refine stage result. Owner gate validates digest/output; first stop after stage verdict. Forbidden: automatic next stage, Task Session/Craft/promotion.

### F-02 — Invoke Plan to one Task Session SWU

IDs: `WP-AS-001`, `TASK-AS-001`, `SWU-AS-001`, Task Session `ts-as-001`, attempt `tsa-001`, admission `adm-as-001`, ticket `ticket-as-001`, runtime `rt-as-001`, thread/turn `thr-as-001`/`turn-as-001`. Plan/validation/baseline digests `2222...`, `3333...`, `4444...`. Policy: one SWU; write only `src/as_fixture.txt`; network denied; stdio; one turn; 300 seconds; exact fixture validator. Events/gates: WPRA audit (no selection) → exact confirmation → Task Session selection → single-use mutation admission → execution ticket → runtime/App Server → host result → executor receipt → capability-owner verdict/owner-hook → reconciliation → precloseout → Refresh owner receipt → governance terminal. First stop at terminal with no successor. Forbidden: second SWU/turn, admission reuse, implicit Orchestrate, Craft mutation.

### F-03 — one bounded Goal/Craft round

IDs: Goal `goal-as-001`, round 1, Craft `CTX-AS-001`, frontier `frontier-as-001`, node/route `NODE-AS-001`/`route-as-001`, batch/token `batch-as-001`/`goal-token-as-001`. Ledger/frontier/owner/delta hashes `5555...`, `6666...`, `7777...`, `8888...`. Policy: one round/node, no active-ledger direct write, no series reducer. Events: bind/snapshot/classify/route → owner receipt closed → audit pass → stage delta → validate single-use token. Current first stop is before active ledger apply because Craft canonical apply schema/implementation is absent. Terminal Goal result `STOP craft-apply-contract-missing`, next route Craft. Forbidden: host/Goal mutating ledger, token reuse, until-blocker choice.

### F-04 — runtime permission pause

IDs: Task Session `ts-perm-001`, attempt/admission `tsa-perm-001`/`adm-perm-001`, thread/turn `thr-perm-001`/`turn-perm-001`, request/item `req-perm-001`/`item-cmd-001`, executor receipt `exec-perm-001`. Frozen admission digest `9999...`. Policy: workspace-write, network denied, exact validation command only. Events: turn started → command approval request → runtime flagged waiting → narrow runtime response `approved-once` → request resolved → admission digest recomputed as unchanged `9999...` → item completed → turn completed → `task-session.executor-receipt.v1` `exec-perm-001` with `result=pass`. The single first stop is capability-owner validation; no digest-mismatch branch exists in this fixture. Forbidden: Decision Gate/acceptance/Craft/promotion or broader permission inference.

### F-05 — stale digest rejection

IDs: Task Session `ts-stale-001`, attempt/ticket `tsa-stale-001`/`ticket-stale-001`, thread/turn `thr-stale-001`/`turn-stale-001`. Ticket baseline `aaaa...`; live baseline `bbbb...`. Events: reconcile → thread read → baseline reread → `adapter_input_stale` → runtime blocked. Result: executor receipt block with `STALE_TARGET_BASELINE`; no owner pass. First stop before steer/new turn/filesystem. Next route fresh epoch/readiness/admission. Forbidden: ticket/admission reuse, old-turn replay/output apply.

### F-06 — interrupt, resume recovery, and stop before retry

IDs: Task Session `ts-int-001`, attempt/admission `tsa-int-001`/`adm-int-001`, thread/turn `thr-int-001`/`turn-int-001`, request/item `rpc-int-001`/`item-file-001`; input `cccc...`. Events: turn/item start → interrupt request/response → terminal interrupted → `thread/resume(threadId=thr-int-001)` loads the original interrupted thread for recovery → thread-read reconciliation → touched/output inventory. Resume grants no replay authority, mutation authority, new turn, or admission reuse. Result: host interrupted and executor receipt interrupted with residue. The single first stop occurs after reconciliation and before any fresh attempt. A later retry, outside this fixture, requires separately admitted `tsa-int-002` with a new admission token and ticket. Forbidden: dependent progression, admission reuse, resumed execution, replay, mutation after resume, or residue erasure.

### F-07 — replay mismatch

IDs: runtime `rt-replay-001`, thread/turn/item `thr-replay-001`/`turn-replay-001`/`item-replay-001`, event `item/completed`. First hash `dddd...`; replay hash `eeee...`. Events: accept at cursor 17 → recovery yields same identity/cursor with differing hash → `replay_identity_hash_mismatch`. Results: runtime blocked and executor receipt block `REPLAY_MISMATCH`. First stop before output/owner/side-effect admission. Forbidden: overwrite, second completion, owner receipt, touched-file apply. Exact duplicate `dddd...` is no-op.

### F-08 — failed closeout after valid execution

IDs: Task Session `ts-close-001`, SWU `SWU-CLOSE-001`, ticket `ticket-close-001`, executor/owner/Refresh records `exec-close-001`, `owner-close-001`, `refresh-close-001`, `owner-refresh-close-001`. Digests `ffff...`, `012345...`, `abcdef...`. Events: host complete → executor pass → capability owner pass → reconciliation → precloseout `execution-validated-closeout-pending` → Refresh owner blocks on target inventory mismatch → owner receipt joined → governance terminal block. First stop at Refresh/closeout invariant; cursor null and successor false. Forbidden: synchronized-complete, cursor, next SWU, Craft update, hiding residue.

### F-09 — Goal no-progress stop

IDs: Goal `goal-np-001`, rounds 17/18, frontiers `frontier-np-017/018`, node/route `NODE-NP-001`/`route-np-001`. Repeated frontier/owner/delta hashes `1357...`, `2468...`, all-zero. Policy threshold 2, one node per round, no Work-Pack series. Events: round 17 unchanged triple counter 1 → round 18 same counter 2 → proportionality stop. Goal result `STOP`, rounds 18, reason no-progress, next route Decision Gate. First stop before round 19/new dispatch. Forbidden: infinite continuation, reducer change, Craft mutation, telemetry-as-progress.

## Eval, observability, lifecycle

Experiment Harness owns exact protocol manifests, installed parity, fixture playback/failure injection, F-01–F-09, protocol/identity/authority/replay/terminal oracles, privacy, and eventual bounded live canary. Its `eval_verdict` is behavior evidence only; it cannot emit/substitute for Task Session/capability-owner receipt, semantic acceptance, Craft apply, lifecycle promotion, publication, release, or deployment.

OIL/Signal Observer own privacy-safe envelope derivation and exactly-once telemetry/dedupe/reflection routing. Inventory and observations remain projections/evidence.

Generated attachment belongs to bootstrap/generation/sync. The stale generated Dispatch Spec statement, Weaver newline residue, and Observability Setup topology wording remain explicit conflicts. Lifecycle work starts only after fixtures and bounded canary; host success must have an Experiment Harness non-promotion regression.

## Defects and repaired placements

Transport/client/request/notification arithmetic is repaired at 3 ingress, 137, 11, 72. Installed parity remains absent. Standalone execution-host/global identity ledger/second replay store are killed in favor of current runtime/adapter/Task Session owners. Domain judgment is returned to the capability owner. Every receipt and approval edge is typed. Fork/steer are host operations; thread/SWU cardinality is separated. The loop is bounded Goal control. The finite-series owner decision remains unresolved. Aggregate 58/14/eval closure claims are removed. Craft, Goal, Experiment Harness, observation, generation, and lifecycle work is placed under current owners.

## Migration-compatible Work-Pack outline

1. Experiment Harness closes pinned manifests and installed parity.
2. Framework runtime adds fixture-only App Server profile and adapter-local identities.
3. Task Session extends ticket/admission/executor/reconciliation references.
4. Refine + Experiment Harness exercise F-01; only later consider one live read-only turn.
5. Task Session + Experiment Harness exercise F-02/F-04–F-08; no Craft/series.
6. Craft defines/implements its own dry-run/render/index/CAS apply and receipt.
7. Goal exercises F-03/F-09 after Craft contract; never crosses the series-owner decision.
8. OIL/Signal Observer/Experiment Harness/lifecycle owners prove privacy, exactly-once observation, and non-promotion.
9. Optional Orchestrate host decision occurs only after ordinary runtime integration proof and independently decides actions/events/receipts/replay/closeout.

## Consolidated verdict

- Present: official protocol surface and existing runtime, Task Session, Work-Pack audit, Craft, Goal, Experiment Harness, observation, Orchestrate, lifecycle owners.
- Partial: provider-neutral runtime seam, Task Session handoff, Goal contract/fixtures, generated distribution, observation.
- Absent: App Server profile/ID map/terminal translation/Task Session binding/fixture profile/installed parity/Craft deterministic ingestion/live canary.
- Conflicting: host goal vs Goal; runtime approval vs acceptance; native vs Arcanum IDs; direct commands/process vs policy; template inventory; stale generated statement; observability wording.
- Deferred: outbound connector, realtime/process/shell, lifecycle maintenance, live mutation canary, App Server Orchestrate host.
- Not applicable: global administration and host claims to acceptance/promotion/publication/release/deployment.
- Unresolved: `DECISION-LOOP-OWNER-001`.

Current evidence supports a coherent adapter architecture and a finite research/eval frontier. It does not support an implemented integration or integration-readiness claim.
