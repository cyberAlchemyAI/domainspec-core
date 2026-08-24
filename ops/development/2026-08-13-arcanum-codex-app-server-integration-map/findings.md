# Codex App Server to Arcanum: evidence-closed integration map

## Architecture first, with the claim ceiling

The coherent placement is a proposed `app-server` adapter/profile inside the existing provider-neutral durable runtime at `arcanum/framework/runtime/`. It would translate Codex App Server transport, thread, turn, item, request, approval, and terminal state into the runtime's existing handoff/status/event surface. It would not become a planner, Work-Pack reducer, Task Session, capability owner, receipt authority, Craft ledger, Goal controller, eval loop, observability truth, lifecycle owner, or publication path. Ordinary Refine-stage and Task-Session execution through this adapter is one bounded integration problem. An App Server-backed Orchestrate host profile is a separate future decision and must not be implied by ordinary adapter work. [E1: `research.md`, Agent 1; E2: `research.md`, Agent 2; E3: `research.md`, Agent 3; local owners: `arcanum/framework/runtime/README.md`, `arcanum/arcana/task-session/runtime-adapters/`, `arcanum/runtime/orchestrate/`]

```text
Refine stage or live-admitted Task Session attempt
  -> framework/runtime durable handoff
       RUN.json + HANDOFF.md + STATUS.json + events.jsonl + adapter-state/
  -> proposed app-server adapter/profile
       pinned protocol/binary preflight
       provider-local identity map and cursor
       ordered raw-event translation
       narrow runtime-request responses
       terminal normalization
  -> Codex App Server
       process_instance_id -> listener_id -> connection_id
       -> threadId -> turnId -> itemId/request_id
  -> runtime host result/status
  -> Task Session executor receipt, when execution was Task-Session-admitted
  -> named capability-owner verdict and receipt
  -> Task Session reconciliation, precloseout, owner closeout join
  -> Task Session governance terminal receipt
```

This is an evidence-closed architecture and research map, not an implementation or readiness result. Direct App Server integration is **absent**. No App Server process or model turn was run. Official protocol claims are pinned to `openai/codex@9946da9af1829410271f6b76f9159961f7281e0a`. The observed local binary was `codex-cli 0.147.0-alpha.6.5`, SHA-256 `6e63a38388455ed175ab72d24813d148186e4f6cc55db787fd12b4ebec871012`; parity between that binary's generated schema and the pinned source is **unverified**. The proof labels used below are `source-observed`, `fixture-observed`, `runtime-observed`, `specified-unexecuted`, and `unverified`. No finding proves implementation, integration readiness, semantic acceptance, promotion, publication, release, deployment, or production use. [Evidence closure: `receipts/evidence-closure.json`; E1]

Existing local runtime evidence—nine native agents, 81 causal events, nine terminal/close/join records, and five passing gates—proves only a prior Codex-native `collaboration.*` Orchestrate run. It is `runtime-observed` precedent for identity, wait, join, and gate ownership, but it is not an App Server witness and does not raise this claim ceiling. [E1; local: `arcanum/runtime/orchestrate/` and the completed August 12 native-run receipts referenced by `strategy-inventory-packet.json`]

## Closed official denominator

The pinned source denominator is closed at the macro/family level:

| Surface | Count | Disposition | Proof |
|---|---:|---|---|
| Inbound transports | 3 | stdio, TCP WebSocket, Unix-socket WebSocket; TCP WS is experimental/unsupported | source-observed |
| Disabled listen modes | 1 | `--listen off`; a mode, not a fourth transport | source-observed |
| Outbound connector families | 1 | independent code-mode-host connector using `ws/wss` or root `http/https` gRPC forms; deferred | source-observed |
| Client requests | 137 | exact macro inventory below | source-observed |
| Server-request variants | 11 | 9 current plus 2 deprecated | source-observed |
| Server notifications | 72 | 68 current/experimental plus deprecated/internal variants as classified in source | source-observed |
| User-input families | 7 | text, image, local image, audio, local audio, skill, mention | source-observed |
| Thread-item families | 18 | complete item-family list below | source-observed |
| Candidate fixture contracts | 9 | all specified-unexecuted; none is a runtime witness | specified-unexecuted |

Transport and process details come from the pinned App Server README: [lines 20-55](https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server/README.md#L20-L55) and [lines 57-89](https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server/README.md#L57-L89). Request and notification definitions come from pinned `common.rs`: [definitions and protocol surface](https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/common.rs#L488-L1279), [thread state](https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/common.rs#L1554-L1603), and [turn state](https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/common.rs#L1707-L1801). [E1; corrected and rechecked by skeptic non-vacuity]

The 137 client requests partition without overlap as follows. The entries retain the pinned macro's exact family denominator even where operational names below are compacted with slash-separated verbs.

| Family | Count | Members / disposition |
|---|---:|---|
| Initialize | 1 | `initialize` |
| Diagnostics | 1 | `server/diagnostics` |
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
| Model / provider | 2 | model list; provider capabilities read |
| Experimental features | 2 | list/enablement set |
| Permission profiles | 1 | list |
| Remote control | 7 | enable/disable/status; pairing start/status; client list/revoke |
| Collaboration mode | 1 | list |
| Experimental mock | 1 | experimental method |
| Environment | 3 | add/info/status |
| MCP server/status | 4 | OAuth login/resource read/tool call; status list |
| Config | 4 | MCP reload/read/value write/batch write |
| Windows sandbox | 2 | setup/readiness |
| Account | 9 | login start/cancel/logout; rate limits/reset credit/usage/workspace messages/credits nudge/read |
| Feedback | 1 | upload |
| Sandboxed command | 4 | exec/write/terminate/resize |
| Unsandboxed process | 4 | spawn/stdin/kill/resize |
| External-agent config | 4 | detect/import/history/read histories |
| Config requirements | 1 | read |
| Memory | 1 | reset |
| Deprecated/legacy | 7 | conversation summary; git diff remote; auth status; fuzzy search start/update/stop plus fuzzy search request |

The uncombined source-family arithmetic is `1+1+38+4+3+1+3+12+3+9+3+1+1+1+2+1+7+1+1+3+3+1+4+2+9+1+4+4+4+1+1+7 = 137`. [E1; pinned `client_request_definitions!` in `common.rs`]

The 11 server requests are command approval, file-change approval, user input, MCP elicitation, permission approval, dynamic tool call, auth-token refresh, attestation generation, current-time read, plus deprecated apply-patch approval and exec-command approval. [E1; pinned `server_request_definitions!` in `common.rs`]

The 72 notifications partition as: thread including realtime 22; item 14; turn 5; hook 2; raw upstream 2; command 1; process 2; server request 1; MCP 2; account 3; app 1; remote control 1; external-agent config 2; filesystem 1; model 3; warning/error/config 5; fuzzy search 2; Windows 2; skills 1. Arithmetic: `22+14+5+2+2+1+2+1+2+3+1+1+2+1+3+5+2+2+1 = 72`. [E1; pinned `server_notification_definitions!` in `common.rs`]

The 18 thread-item families are user message, hook prompt, agent message, plan, reasoning, command execution, file change, MCP tool call, dynamic tool call, collaboration-agent tool call, subagent activity, web search, image view, sleep, image generation, enter review, exit review, and context compaction. Turn states are `inProgress`, `completed`, `interrupted`, and `failed`; item lifecycle is start, zero or more deltas, complete. [E1; pinned [`turn.rs:288-325`](https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/v2/turn.rs#L288-L325) and [`item.rs:230-401`](https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/v2/item.rs#L230-L401)]

## Local denominator and unavoidable open ledgers

| Surface | Observed aggregate | Closure | Verdict |
|---|---:|---|---|
| Refine stages | 10 | ten stage names recovered; no direct per-stage digest ledger | partial / unverified |
| Invoke modes | 7 | active `define`, `design`, `plan`, `handoff`, `refresh`; deferred `full`, `validate` | partial |
| Invoke templates | 13 physical vs 12 in Inventory | named families recovered; retained retired family omitted by README/Inventory | conflicting |
| Dispatch Spec techniques | 65 = 19 composition + 31 standards + 15 boundary/evidence | 0/65 individual classified rows | open aggregate |
| Relevant machine schemas | 58 = Invoke 12 + Work Pack Readiness 10 + Implementation Readiness 7 + Task Session 16 + Continuation Router 3 + Task Session Until Blocker 5 + Decision Gate 5 | 0/58 individual classified rows | open aggregate |
| Generated packages checked | 14 | 0/14 exact member ledger | open aggregate |
| Eval evidence | 9 Goal fixtures, 6 Sigil Maintenance states, OIL cases, 3 Invoke CLI regimes | no unified exact member ledger | open aggregate |
| Installed-binary schema parity | one binary identity/digest observed | no schema comparison to pinned source | unverified |

The 65-technique, 58-schema, 14-package, and eval-member ledgers remain open. They cannot support an exhaustive local completeness or readiness claim until each member has identity, digest, exact selector, classification, and proof status. [E2; E3; `receipts/evidence-closure.json`]

## App Server hook registry and current status

| App Server surface | Existing Arcanum owner and legal binding | Typed effect | Verdict |
|---|---|---|---|
| `initialize` / capabilities | framework runtime adapter profile | runtime profile/status only; opens no Arcanum gate | partial seam; adapter absent |
| thread start/resume/read/list | adapter-local state plus runtime recovery | host-result contribution only | absent integration |
| thread fork | host operation after a separately admitted Task Session attempt | new ticket/admission and fresh thread binding | absent; conflicting if fork is treated as admission |
| turn start | framework runtime executes immutable handoff only after live Task Session admission | raw terminal then executor receipt | absent integration |
| turn steer | input to a known turn under unchanged policy | runtime event only | partial protocol; no Arcanum transition |
| turn interrupt | adapter requests and reconciles terminal interrupted state | interrupted host result/executor residue | absent reducer |
| item start/delta/complete | adapter contributes ordered events; runtime owns event log | provisional trace evidence | absent extension |
| turn terminal/error | adapter translates raw state | host result, never owner verdict | absent normalizer |
| turn diff/file change | Task Session touched/baseline/output validation | executor evidence input | partial seam |
| command/file/permission/question request | adapter maps one request to one narrow runtime response | runtime-effect response only | absent mapping |
| `serverRequest/resolved` | adapter recovery/cleanup evidence | no acceptance or blocker closure | partial protocol |
| skills list/change and `UserInput.skill` | generated-package resolution/sync owners | digest-pinned attachment/cache invalidation | partial |
| hooks | Observed Invocation Loop and Signal Observer | privacy-safe observation envelope | partial |
| MCP/dynamic tool | adapter records tool identity and hashes | evidence input | partial |
| sandboxed command exec | possible later runtime validation profile | not a current Orchestrate action | deferred / conflicting |
| collaboration-agent/subagent items | diagnostic model-driven host activity | cannot satisfy Orchestrate spawn/join | conflicting if substituted |
| Codex review | named capability-owner evidence input | never audit or acceptance alone | partial |
| host goal APIs | optional UI/runtime mirror only | no Craft/Goal effect | conflicting name; integration absent |
| token usage | Goal/OIL telemetry input | no Craft/Goal budget authority | partial |
| realtime, shell, process, direct filesystem | excluded from first profile | none | deferred / conflicting |
| outbound code-mode-host connector | independent process connector | no inbound identity-chain effect | deferred |
| account/config/plugin/marketplace/global administration | outside bounded coding adapter | none | not applicable |

These classifications derive from E1's protocol-to-owner matrix, E2's execution chain, and E3's recursive-control map. Existing local owners are `arcanum/framework/runtime/`, `arcanum/arcana/task-session/`, `arcanum/runtime/orchestrate/`, `arcanum/arcana/experiment-harness/`, `arcanum/spells/observed-invocation-loop/`, and `arcanum/arcana/signal-observer/`.

## Authority, identity, receipt, and approval boundaries

Invoke Plan authors a Work Pack. Work Pack Readiness audits a frozen frontier but does not select or admit it. Human or Decision Gate confirmation is a prerequisite, not live mutation admission. Task Session selects one bounded unit and issues single-use mutation admission. Framework runtime plus the proposed adapter executes the bounded handoff. The named capability owner judges domain semantics. Task Session reconciles executor and owner evidence, joins required closeout, and emits its governance terminal. Orchestrate owns governed multi-agent dispatch only. Craft alone owns project-ledger state. Goal owns bounded frontier selection, routing, audit, staging, and token consumption, but not Craft apply. Experiment Harness owns fixtures and canaries. OIL and Signal Observer own observation. Lifecycle owners retain promotion. [E2; E3; local: `arcanum/arcana/work-pack-readiness-audit/`, `arcanum/arcana/task-session/`, `arcanum/arcana/craft/`, `arcanum/arcana/goal/`]

| Namespace | Identities | Non-substitution rule |
|---|---|---|
| Orchestrate | `dispatch_id`, `run_id`, `wave_id`, `step_id`, `action_id`, `agent_id` | valid only for a separately designed host profile |
| Task Session | `run_id`, `task_id`, `swu_id`, `ticket_id`, `attemptId`, `admissionToken`, `idempotency_key` | one executable thread per admitted attempt; SWU stays separate |
| Durable runtime | runtime run ID, adapter ID, status, event sequence | parent envelope/store |
| Adapter-local | `process_instance_id`, inbound `listener_id`, inbound `connection_id`, protocol commit, binary digest, cursor | provider-local map |
| App Server | `threadId`, `turnId`, `itemId`, request ID, command process ID, process handle | raw host identities only |
| Craft | scope/context, ledger digest/rows | never a host thread or host goal |
| Goal | context, frontier snapshot, round, route, batch, token | never host goal/token usage |

The inbound chain is `process_instance_id -> listener_id -> connection_id -> threadId`; the optional outbound connector is independent. Forbidden substitutions include `threadId = agent_id/run_id/Craft context`, `turnId = action_id/ticket/attempt`, `itemId = receipt`, JSON-RPC request ID = approval/gate/acceptance, fork = new Arcanum attempt, and steer = an Arcanum transition. Resume is recovery, not replay authority. [E1; definitional review SD-001–SD-007; local: `arcanum/runtime/orchestrate/schemas/` and Task Session schemas]

The typed result chain is: proposed adapter-local `app-server.host-result.v0` → existing runtime `STATUS.json` → `task-session.executor-receipt.v1` → capability-owner-native verdict or `task-session.owner-hook-receipt.v1` → Task Session reconciliation → `task-session.precloseout-execution-receipt.v1` → owner closeout join → `task-session.governance-terminal-receipt.v1`. An Orchestrate action receipt, `arcanum.native-dispatch-runner.receipt.v0.1`, is separate and applies only to exact dispatch actions/joins. Experiment Harness results and OIL observations are evidence, not substitutions. A future Craft apply artifact remains only a proposed `craft.proposed-ledger-apply-receipt.v0` until Craft defines a canonical schema. [E2; E3; definitional review SD-003–SD-004]

Approvals are also disjoint: an App Server response authorizes one runtime effect for one request ID; dispatch confirmation authorizes one exact registered dispatch; Work-Pack confirmation permits selection flow; a Decision Gate record resolves one named decision; a Goal batch token permits one scoped Craft-owned apply attempt; capability-owner acceptance accepts one candidate/validation digest; lifecycle promotion authorizes one lifecycle transition; publication, release, and deployment each require their own target owner and exact revision. No earlier row authorizes a later one. [E1–E3; definitional review SD-005]

## Refine, Invoke, Work Pack, and Task Session

The recovered ten-stage Refine chain is: Context Builder; Invoke Define; Interrogation refine review; explicit research decision; Distill; Invoke Design; Interrogation design review; Distill Repair; Invoke Plan; final Refine synthesis. This remains **partial/unverified** without the missing direct per-stage ledger. Each stage supplies immutable inputs, explicit mode, allowed writes, validation surface, and owner result; host turn completion cannot advance the chain. [E2; local: `arcanum/arcana/refine/`, `arcanum/arcana/context-builder/`, `arcanum/arcana/interrogation/`, `arcanum/arcana/distill/`, `arcanum/spells/invoke/`]

Invoke has seven modes: active `define`, `design`, `plan`, `handoff`, `refresh`; deferred `full`, `validate`. The thirteen physical template families comprise the DomainSpec baseline, candidates for architecture/generic/refresh/research/session-handoff/sigil/spell/UX-plan, deprecated module-formulae, retired implementation-plan, and draft implementation-layering and Work-Pack companions. Inventory declares twelve, so template completeness is **conflicting**. The 65 Dispatch Spec techniques remain aggregate-classified only: 19 composition techniques are partial dispatch metadata, 31 standards techniques are validation policy rather than direct host hooks, and 15 boundary/evidence techniques are adapter-relevant but partial. [E2; local: `arcanum/spells/invoke/`, `arcanum/formulae/dispatch-spec/`]

The execution chain is:

```text
Invoke Plan
 -> frozen Work Pack Readiness audit
 -> Implementation Readiness binding
 -> Task Session fast entry or one typed prerequisite
 -> Context Builder
 -> one single-use Task Session mutation admission and ticket
 -> framework runtime + proposed adapter executes one attempt
 -> executor receipt and validation reconciliation
 -> named capability-owner verdict/receipt
 -> precloseout
 -> Continuation Router admits only apply-approved Invoke Refresh
 -> Refresh receipt and owner closeout join
 -> Task Session governance terminal and cursor
```

The preferred topology is one independent thread per Refine stage and one executable thread per admitted Task Session attempt. A long-lived project thread may only be a read-only coordinator projection. Resume revalidates admission and digests; fork requires fresh admission. App Server-backed Orchestrate remains a separate deferred decision. [E2; local: `arcanum/arcana/implementation-readiness/`, `arcanum/arcana/task-session/`, `arcanum/arcana/continuation-router/`]

## Minimal provider-neutral adapter contract

The adapter extends the existing runtime; it is not a new global envelope or controller.

Required input:

- durable-runtime run/profile identity and exact adapter version;
- pinned App Server protocol commit, installed binary path/version/digest, and parity status;
- Task Session task/SWU/ticket/attempt/admission identities when mutation is possible;
- immutable artifact selectors, input/baseline/route/semantic/profile digests, and one idempotency key;
- cwd, sandbox, permission/approval mode, network policy, model/config, allowed reads/writes, time/token/turn ceilings, and forbidden effects;
- validation, touched/output inventory, closeout contracts, exact owner and receipt schemas;
- generated-skill identity, canonical/generated digest binding, and privacy/observation policy.

Required output/state:

- provider-local process/listener/connection/thread/turn/item/request map without native-ID substitution;
- append-ordered event contribution, cursor, event identity and payload/output/diff hashes;
- explicit runtime-pause records and one-request responses;
- terminal host result distinguished as completed/interrupted/failed/uncertain;
- touched/output inventory, diff/hash evidence, validation results, and interruption residue;
- duplicate no-op versus replay mismatch decision and ambiguous-outcome reconciliation;
- separate Task Session executor receipt and owner receipt references; never a synthesized owner verdict;
- privacy-filtered observation attachment and exact installed/generated identities.

Pre-call attempt evidence must exist before host state is created. Ambiguous timeouts/disconnects require read/resume reconciliation, not blind retry. The first profile should use stdio, deny outbound connector/realtime/shell/unsandboxed process/direct filesystem/global administration, deny undeclared network, and bind each permission response to one exact request. Trust-setting and permission expansion are mutations. [E1; E2; precedent review; local: `arcanum/framework/runtime/`, `arcanum/arcana/task-session/runtime-adapters/`]

## Bounded Goal/Craft control, not a second continuous controller

```text
Goal bind
 -> snapshot Craft ledger digest and frontier hash
 -> select one node whose owner route is already valid
 -> owner executes, optionally via Task Session and adapter
 -> typed owner-route receipt
 -> audit
 -> stage proposed Craft delta
 -> exact Goal/Decision Gate batch token
 -> Craft-owned validate/CAS apply/render/index update
 -> recompute frontier
 -> next bounded round | complete | no-progress stop | budget stop
```

Craft remains sole project-state authority. The missing receipt ingestion, row planning, rendering/index update, validated YAML/CAS apply, and apply receipt are implementations under Craft—not a new integration owner. Goal owns the missing persistent round journal, route accounting, no-progress detector, and loop result—not Craft apply. App Server owns none of these transitions. `DECISION-LOOP-OWNER-001` remains unresolved between Implementation Readiness finite-frontier/until-blocker control and Task Session Until Blocker bounded-series control. This map selects neither and introduces no third reducer. [E3; precedent review; local: `arcanum/arcana/craft/SKILL.md`, `arcanum/arcana/craft/ARCHITECTURE.md`, `arcanum/arcana/goal/README.md`]

Stop conditions include missing/ambiguous ledger, stale ledger digest, missing terminal state after recovery, duplicate identity with mismatched hash, audit veto, absent done evidence, absent exact Arcanum approval, repeated unchanged frontier/receipt/delta hashes, or any declared round/turn/spawn/token/time ceiling.

## Eval, observability, lifecycle, and generated-package hooks

Experiment Harness owns pinned protocol manifests, installed-binary parity, deterministic fixture playback, failure injection, denominator arithmetic, identity/authority/replay/terminal oracles, privacy checks, and an eventual bounded live canary. An eval verdict is behavior evidence only; it cannot emit or replace Task Session or capability-owner receipts, semantic acceptance, Craft apply, lifecycle promotion, publication, release, or deployment. [E3; local: `arcanum/arcana/experiment-harness/`]

Observed Invocation Loop and Signal Observer own privacy-safe envelope derivation, append/deduplication, exactly-once observation, and reflection routing. Workflow Reflect can propose changes from accumulated evidence. Inventory remains a non-authoritative projection. Telemetry cannot decide semantic verdicts, mutate Craft, or promote lifecycle state. [E3; local: `arcanum/spells/observed-invocation-loop/`, `arcanum/arcana/signal-observer/`, `arcanum/arcana/workflow-reflect/`, `arcanum/arcana/inventory/`]

Bootstrap, generation, and generated-skill sync own App Server profile attachment and digest pinning. Generated-package parity is partial: selected payloads matched after frontmatter normalization except a materially stale generated Dispatch Spec native-spawn statement and newline-only Weaver residue. Observability Setup also has conflicting topology wording (`hybrid` versus central ledger with reference indexes). These are explicit conflicts, not permission to repair them in this research artifact. Sigil Maintenance, Sigil Development, Spellcraft, Constitution Governance, Discipline Governance, and Definitions Governance remain later owner-controlled consumers; no host success can promote them. [E2; E3; local: `arcanum/tools/sync-generated-skill-package.sh` and the named canonical capability folders]

## Missing or easily forgotten primitives, routed to existing owners

| Missing primitive or hook | Existing owner | Current verdict |
|---|---|---|
| App Server runtime profile and host-result translation | framework runtime adapter | absent |
| bidirectional native identity map and ordered cursor/event contribution | framework runtime adapter state/log | absent |
| terminal normalizer and disconnect reconciliation | framework runtime adapter | absent |
| approval/acceptance separation mapping and oracle | adapter + Decision Gate/Dispatch Spec owner tests | absent |
| replay/no-op/mismatch state for ordinary execution | adapter state + Task Session idempotence | absent |
| Task Session ticket/admission/executor/reconciliation bindings | Task Session | absent |
| touched/baseline/output validation from host diffs | Task Session existing owner | partial seam |
| deterministic receipt ingestion, row plan, renderer/index update, YAML/CAS apply receipt | Craft | absent |
| persistent bounded-round journal and no-progress detector | Goal | absent implementation; contract/fixtures partial |
| App Server fixture player, failure injection, denominator oracle, installed parity, canary | Experiment Harness | absent |
| observation-envelope derivation from adapter events | OIL + Signal Observer | partial provider-neutral seam |
| generated-package attachment/profile and digest pin | bootstrap/generation/sync | partial |
| lifecycle regression proving host success cannot promote | Experiment Harness + existing lifecycle owners | absent |
| Research Evidence Harness profile for structured App Server runs | Research Evidence Harness, after adapter schema | deferred |
| Necronomicon and Context Builder discovery/context projections | their existing owners; never terminal authority | present/partial seam |
| Decision Gate runtime-pause non-substitution | Decision Gate + adapter oracle | present owner; App Server oracle absent |
| Inventory indexing of resulting evidence | Inventory, as discovery projection only | present owner; integration deferred |
| Observability topology/profile installation | Observability Setup | partial/conflicting wording; no App Server profile |
| Sigil Maintenance, Sigil Development, and Spellcraft consumption | their lifecycle owners, after credible eval/telemetry | deferred |
| Constitution, Discipline, Definitions governance | their existing owners | present owners; integration deferred/not required initially |
| future Orchestrate action/event/receipt mapping | Orchestrate, by separate host-profile decision | deferred |

This list deliberately reuses owners. It does not propose a standalone `CodingExecutionHost`, global identity ledger, second causal store, duplicate scheduler, second receipt authority, or second promotion path. [E3; precedent terminal recheck]

## Nine finite traces: all specified, none executed

Every trace below is a fixture contract with synthetic digests and `specified-unexecuted` proof status.

1. **F-01 Refine stage.** Runtime `rt-refine-001`, Refine run `refine-candidate-001`, stage `invoke-design`, process/connection `asp-fixture-01`/`conn-stdio-01`, thread/turn `thr-refine-001`/`turn-refine-001`; input digest `sha256:1111...1111`. Read-only except `/fixture/out/design.md`, network denied, digest-pinned skill. Ordered path: runtime created → initialize → thread/turn start → agent-message item start/complete → turn completed → adapter host result → owner-local stage verdict. First stop: stage verdict. Forbidden: automatic next stage, Task Session, Craft, promotion.

2. **F-02 Invoke Plan to one SWU.** `WP-AS-001`/`TASK-AS-001`/`SWU-AS-001`; Task Session `ts-as-001`; attempt/admission/ticket `tsa-001`/`adm-as-001`/`ticket-as-001`; runtime/thread/turn `rt-as-001`/`thr-as-001`/`turn-as-001`; plan/validation/baseline digests `2222...`/`3333...`/`4444...`. One SWU, only `src/as_fixture.txt`, no network, stdio, one turn, 300 seconds, exact validator. WP audit → confirmation → selection → admission/ticket → host result → executor → capability-owner receipt → reconciliation/precloseout → Refresh owner receipt → governance terminal. First stop: terminal, no successor. Forbidden: second SWU/turn, admission reuse, implicit Orchestrate, Craft mutation.

3. **F-03 one Goal/Craft round.** Goal `goal-as-001`, round 1, Craft `CTX-AS-001`, frontier/node/route `frontier-as-001`/`NODE-AS-001`/`route-as-001`, batch/token `batch-as-001`/`goal-token-as-001`; ledger/frontier/owner/delta hashes `5555...`/`6666...`/`7777...`/`8888...`. One round/node. Bind/snapshot/classify/route → owner receipt → audit → staged delta → token validation. First stop before active-ledger apply because Craft apply contract is absent; terminal `STOP craft-apply-contract-missing`. Forbidden: host/Goal ledger mutation, token reuse, series-owner selection.

4. **F-04 runtime permission pause.** Task Session `ts-perm-001`; attempt/admission `tsa-perm-001`/`adm-perm-001`; thread/turn/request/item `thr-perm-001`/`turn-perm-001`/`req-perm-001`/`item-cmd-001`; frozen admission digest `9999...`. Workspace-write, network denied, exact validation command. Turn start → command approval request → runtime wait → one `approved-once` response → request resolved → unchanged digest revalidation → item/turn complete → executor receipt `exec-perm-001`. First stop: capability-owner validation. Forbidden: treating runtime approval as Decision Gate, acceptance, Craft, or promotion.

5. **F-05 stale digest.** Task Session/attempt/ticket `ts-stale-001`/`tsa-stale-001`/`ticket-stale-001`; thread/turn `thr-stale-001`/`turn-stale-001`; ticket baseline `aaaa...`, live baseline `bbbb...`. Reconcile/read/baseline reread → `adapter_input_stale` → blocked executor receipt `STALE_TARGET_BASELINE`. First stop before steer/new turn/filesystem; next route is fresh epoch/readiness/admission. Forbidden: old ticket/admission or output reuse.

6. **F-06 interrupt and recovery-only resume.** Task Session/attempt/admission `ts-int-001`/`tsa-int-001`/`adm-int-001`; thread/turn/request/item `thr-int-001`/`turn-int-001`/`rpc-int-001`/`item-file-001`; input `cccc...`. Turn/item start → interrupt → terminal interrupted → `thread/resume(thr-int-001)` only to recover original thread → thread-read reconciliation → touched/output inventory → interrupted executor receipt with residue. First stop before a fresh attempt. Any retry requires new `tsa-int-002`, token, and ticket. Forbidden: resumed execution, admission reuse, replay, residue erasure.

7. **F-07 replay mismatch.** Runtime `rt-replay-001`; thread/turn/item `thr-replay-001`/`turn-replay-001`/`item-replay-001`; cursor 17; accepted hash `dddd...`, replay hash `eeee...`. Recovery with same identity/cursor but different hash → `replay_identity_hash_mismatch` → runtime/executor block `REPLAY_MISMATCH`. First stop before output/owner/side effects. Exact replay of `dddd...` is a no-op. Forbidden: overwrite, second completion, owner receipt, apply.

8. **F-08 failed closeout after valid execution.** Task Session/SWU/ticket `ts-close-001`/`SWU-CLOSE-001`/`ticket-close-001`; executor/owner/Refresh records `exec-close-001`/`owner-close-001`/`refresh-close-001`/`owner-refresh-close-001`; digests `ffff...`/`012345...`/`abcdef...`. Host/executor/capability-owner pass → reconciliation → precloseout `execution-validated-closeout-pending` → Refresh owner blocks on target-inventory mismatch → joined owner receipt → governance terminal block. First stop at closeout invariant, with null cursor/no successor. Forbidden: synchronized completion, next SWU, Craft update, hidden residue.

9. **F-09 no-progress stop.** Goal `goal-np-001`; rounds 17/18; frontiers `frontier-np-017/018`; node/route `NODE-NP-001`/`route-np-001`; repeated frontier/owner/delta hashes `1357...`/`2468...`/all-zero; threshold 2. Round 17 unchanged counter 1 → round 18 unchanged counter 2 → proportionality stop. Terminal Goal result `STOP`, reason no-progress, next route Decision Gate. First stop before round 19. Forbidden: infinite continuation, reducer change, Craft mutation, telemetry-as-progress.

[Trace source: repaired `synthesis.md`, F-01–F-09; non-vacuity terminal recheck `PASS`.]

## Canary and eval plan

Before any live mutation canary, Experiment Harness should close exact pinned-source manifests and installed-binary parity, then run deterministic variants for: successful terminal normalization; failed turn; F-06 interrupt/recovery; exact duplicate no-op and F-07 mismatch; every runtime-permission variant; F-05 stale digest; item completion without turn terminal; disconnect/ambiguous-outcome reconciliation; host-goal non-collapse; audit veto/F-08 closeout failure; F-09 no-progress; generated-skill attachment plus observation; privacy filtering; and lifecycle non-promotion. Required oracle layers are protocol ordering, identity non-substitution, typed receipt fields/hashes, authority separation, replay behavior, digest-bound Craft-owned apply, lifecycle non-promotion, and exactly-once privacy-safe observation. Only after fixture closure should a read-only bounded live canary be considered; a mutation canary remains separately gated. [E3; `arcanum/arcana/experiment-harness/`]

## Migration-compatible, non-executed Work Pack outline

1. **Experiment Harness:** close exact protocol manifests, denominator oracles, and installed-binary schema parity.
2. **Framework runtime:** add a fixture-only `app-server` profile, provider-local identity/cursor state, ordered translation, pause mapping, and terminal normalizer.
3. **Task Session:** extend ticket/admission/executor/reconciliation references without changing its admission or owner boundaries.
4. **Refine + Experiment Harness:** execute F-01 in fixtures; only later gate one read-only live stage.
5. **Task Session + Experiment Harness:** execute F-02 and F-04–F-08 in fixtures; keep Craft and bounded-series control out.
6. **Craft:** define and implement its own dry-run, row plan, renderer/index update, digest-bound CAS apply, validation, and typed apply receipt.
7. **Goal:** execute F-03/F-09 only after Craft's contract exists; do not cross `DECISION-LOOP-OWNER-001`.
8. **OIL/Signal Observer/Experiment Harness/lifecycle owners:** prove privacy, exactly-once observation, and non-promotion.
9. **Optional Orchestrate decision:** only after ordinary runtime integration evidence; independently design actions, events, receipts, replay, host inventory, interruption, and closeout. Do not broaden spawn-only Orchestrate implicitly.

This outline is planning material only. It is not an admitted Work Pack and authorizes no implementation. [E1–E3; precedent and definitional terminal rechecks]

## Consolidated verdicts

- **Present:** the official pinned protocol surface; existing framework runtime, Task Session, Work Pack audit, Craft, Goal, Experiment Harness, observation, Orchestrate, generation, and lifecycle owners; prior native collaboration-host evidence only.
- **Partial:** provider-neutral runtime seam, Task Session runtime handoff, Goal contract/fixtures, generated distribution, observation, host-diff validation input, and aggregate local maps.
- **Absent:** direct App Server profile, identity/cursor map, ordered translation, terminal normalizer, Task Session binding, App Server fixture profile, installed-binary parity, deterministic Craft receipt ingestion/apply, Goal loop implementation, and live canary.
- **Conflicting:** host goal versus Arcanum Goal, runtime approval versus acceptance, native versus Arcanum identities, direct shell/process/filesystem operations versus policy, 13 physical templates versus Inventory 12, stale generated Dispatch Spec wording, and Observability Setup topology wording.
- **Deferred:** outbound connector, realtime/shell/process surfaces, Research Evidence Harness profile, lifecycle maintenance, live mutation canary, and App Server-backed Orchestrate host.
- **Not applicable:** global administration and every claim that host completion itself provides Arcanum semantic acceptance, Craft state, promotion, publication, release, or deployment.
- **Unresolved:** `DECISION-LOOP-OWNER-001`.

The final evidence supports a coherent adapter architecture, exact official macro denominators, explicit open local aggregates, and a finite research/eval frontier. It does **not** support implementation, direct integration, integration readiness, acceptance, promotion, publication, release, deployment, or production claims.

## Evidence key

- **E1:** `research.md`, “Agent 1 — explorer-protocol-host”; official source at pinned `openai/codex@9946da9af1829410271f6b76f9159961f7281e0a`; local runtime/Orchestrate/generated-package inspection; prior collaboration-host runtime evidence explicitly not App Server evidence.
- **E2:** `research.md`, “Agent 2 — explorer-authoring-execution”; local canonical Refine/Invoke/Work-Pack/Task-Session/Continuation/Dispatch Spec sources and generated-package comparison.
- **E3:** `research.md`, “Agent 3 — explorer-recursive-control-evals”; local Craft/Goal/Experiment Harness/observability/lifecycle/generation sources.
- **Review closure:** `reviews/skeptic-precedent.md`, `reviews/skeptic-non-vacuity.md`, `reviews/skeptic-definitional.md`, with matching passing receipts and `receipts/evidence-closure.json`.
