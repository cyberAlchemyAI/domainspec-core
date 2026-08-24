# Codex App Server to Arcanum integration research

This file is the parent-owned join artifact for the three read-only explorer returns. The explorers did not mutate repository state. The claim ceiling is current official App Server protocol evidence, current local Arcanum contracts/generated packages, and existing local runtime witnesses; no App Server process or model turn was run.

## Agent 1 — explorer-protocol-host

Status: `pass`.

Core verdict: App Server integration is absent. Arcanum has a fixture- and live-run-proven Codex-native collaboration host, a generated Codex skill package, generic runtime handoff, and legacy `codex-exec`/Goal adapters, but none binds App Server JSON-RPC thread/turn/item/request state into Orchestrate action/run/gate receipts.

The official denominator was pinned to `openai/codex` commit `9946da9af1829410271f6b76f9159961f7281e0a`. The installed local binary observed by the lane was `codex-cli 0.147.0-alpha.6.5`, SHA-256 `6e63a38388455ed175ab72d24813d148186e4f6cc55db787fd12b4ebec871012`; installed-binary schema parity was not tested.

Denominator:

- 2 transports: stdio (default, newline-delimited JSON) and experimental unsupported WebSocket.
- 137 client requests.
- 9 server requests: command approval, file-change approval, user input, MCP elicitation, permissions approval, dynamic tool call, auth-token refresh, attestation generation, and current-time read.
- 71 server notifications.
- 7 user-input families: text, image, local image, audio, local audio, skill, mention.
- 18 thread-item families: user message, hook prompt, agent message, plan, reasoning, command execution, file change, MCP tool call, dynamic tool call, collaboration-agent tool call, subagent activity, web search, image view, sleep, image generation, enter review, exit review, context compaction.
- Thread states: `notLoaded`, `idle`, `systemError`, and active waiting on approval or user input. Turn states: `inProgress`, `completed`, `interrupted`, `failed`. Item rule: start, zero or more deltas, complete.

Protocol bindings and boundaries:

- `initialize`/`initialized` establish the adapter connection and capabilities only. They open no Arcanum gate.
- `thread/start|resume|fork` yield a `threadId`; the adapter must map that ID to `dispatch_id`, `run_id`, `action_id`, and `agent_id` without replacing them. Starting a trusted workspace may persist Codex trust state and therefore is not mutation-free preflight.
- `thread/read|list|loaded/list|turns/list|items/list` are recovery/reconciliation reads. They cannot establish a terminal receipt on their own.
- `thread/name/set` and metadata are optional non-authoritative labels.
- `thread/goal/*` is Codex host goal state, not Arcanum Goal or the Craft frontier. Treating it as Arcanum Goal would create a second controller.
- `turn/start` binds a host attempt. `clientUserMessageId` is correlation, not a documented idempotency key. On an ambiguous timeout, reconcile before retry.
- `turn/steer` is a bounded follow-up on a known binding; it is not a new action or gate decision.
- `turn/interrupt` requires terminal `interrupted` evidence and blocks dependents. Resume does not authorize replay of an Arcanum action.
- `turn/started`, `item/*`, `turn/completed`, and `error` form the source event stream. Turn completion is necessary but insufficient: receipt admission also requires identity match, output-schema validation, requested artifacts, and validation evidence.
- `collabAgentToolCall` and `subAgentActivity` are model-driven host activity. They cannot satisfy Orchestrate spawn/join actions unless a future adapter proves exact bindings and causal events.
- Runtime approval or user-input requests are pause/authorization evidence only. They are not Arcanum strategy confirmation, semantic acceptance, owner acceptance, promotion, or publication.
- `skills/list`, skill roots/config, and `UserInput.skill` can point to generated `.agents/skills/<skill>/SKILL.md` bytes, but canonical Arcanum remains the owner. `skills/changed` is cache invalidation, not authority transfer.
- MCP and dynamic-tool results are evidence inputs, not Arcanum receipts without normalization.
- `command/exec` is a possible sandboxed deterministic validation seam, but the current Orchestrate action schema admits only `spawn`.
- `thread/shellCommand` and process APIs are unsandboxed/experimental and conflicting by default.
- Codex review is candidate evidence, not Task Session review, evidence closure, audit, or acceptance.
- Account/config/plugin/marketplace/global administration is excluded from a bounded coding adapter; only safe reads might inform preflight.
- Realtime events are ephemeral and not replayable from thread read/resume/fork.
- Overload or disconnect leaves uncertain host outcome. There is no general documented `turn/start` idempotency; reconcile rather than blindly retry.

Identity collisions:

- `threadId` is a conversation identity, not Arcanum `agent_id` or run identity.
- `turnId` is an execution episode, not predeclared `action_id` or attempt identity.
- `itemId` is an output/side-effect item, not a receipt.
- JSON-RPC request ID is a wire correlation ID, not authorization or acceptance.
- App Server thread/turn states and Arcanum run/wave/gate states are different machines.
- Persisted host goal/plan and Codex review cannot become Craft/Goal frontier or audit state.

Existing owners inspected: Orchestrate causal host map and receipt/event schemas; generic framework runtime with native `local-skill` and legacy `codex-exec`; Task Session runtime handoff; Dispatch Spec boundary techniques; generated runtime manifests. Existing local proof shows nine native agents, 81 causal events, nine terminal/close/join records, and five passing gates for a prior collaboration-host dispatch only—not App Server.

Minimum adapter obligations: separately pin protocol and installed-binary identity; keep an explicit ID map; append action-attempt evidence before creating host state; reconcile ambiguous failures; normalize terminal status plus artifacts/schema/validation; separate runtime pauses from Arcanum gates; preserve sandbox/cwd/network policy; digest-pin generated skills; prevent nested model-driven collaboration from satisfying coordinator actions; add deterministic success, pause, interruption, mismatch, replay, missing-artifact, disconnect, and no-progress canaries.

Primary selectors:

- <https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server/README.md#L20-L55>
- <https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/common.rs#L488-L1279>
- <https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/common.rs#L1554-L1603>
- <https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/common.rs#L1707-L1801>
- <https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/v2/turn.rs#L288-L325>
- <https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/app-server-protocol/src/protocol/v2/item.rs#L230-L401>

## Agent 2 — explorer-authoring-execution

Status: `pass`.

Core verdict: Arcanum defines a strict intent-to-synchronized-result chain, but no inspected source binds App Server thread/turn/item state to it. Generated Codex skills are callable policy and deterministic scripts; they are not an App Server adapter, identity normalizer, approval translator, interruption reducer, or result-to-receipt bridge.

Denominators:

- Refine: 10 stages.
- Invoke: 7 modes; active `define`, `design`, `plan`, `handoff`, `refresh`; deferred `full`, `validate`.
- Invoke templates: 13 physical entries versus 12 declared by the inventory. Baseline: DomainSpec spec. Candidates: architecture, generic, refresh, research, session handoff, sigil, spell, UX plan. Deprecated: module formulae. Retired: implementation plan. Draft companions: implementation layering and Work Pack. The templates README omits the retained retired implementation-plan family.
- Dispatch Spec: 65 techniques: 19 composition, 31 standards, 15 boundary/evidence.
- 58 relevant machine-schema files: Invoke 12, Work Pack Readiness 10, Implementation Readiness 7, Task Session 16, Continuation Router 3, Task Session Until Blocker 5, Decision Gate 5.
- 14 generated packages checked.

Refine/Invoke authoring map:

1. Context Builder selects exact target, obligations, selectors/digests, write scope, and validation surface; it blocks incomplete or stale coverage.
2. Invoke Define authors definitions and emits the artifact/dispatch/template/next-route receipt.
3. Interrogation refine review resolves one evidence-backed question at a time.
4. Research decision remains local-first and explicit.
5. Distill selects the smallest coherent unit while preserving alternatives and residue.
6. Invoke Design uses a closed denominator and fixed-point two-pass selection; it authors design, not Work-Pack tasks.
7. Interrogation design review preserves risks and contradictions.
8. Distill Repair requires declared falsification evidence; telemetry cannot decide the verdict.
9. Invoke Plan authors a finite frontier, SWUs, exact write/validation/receipt/closeout contracts, route digest, and stop classes; it does not execute.
10. Final Interrogation/Refine synthesis requires an artifact or typed blocker for each stage and produces an aggregate result, not implementation authority.

Execution chain:

`Invoke Plan -> frozen Work Pack Readiness Audit -> Implementation Readiness binding -> Task Session fast entry or one typed prerequisite -> Context Builder -> one single-use Task Session mutation admission/ticket -> executor receipt and validation reconciliation -> Continuation Router admits exactly Invoke Refresh apply-approved -> separate Refresh receipt -> Task Session governance terminal receipt and cursor`.

The best topology is an independent thread per authoring stage and one thread per Task Session attempt/SWU. A long-lived thread may be a coordinator projection only; every action still needs fresh immutable inputs, digest checks, explicit capability/mode, write ceiling, receipt schema, and one outstanding action.

Failure traces:

- Normal: plan, frozen readiness, selection, fast entry, context, single-use admission, execution, validation, precloseout, router, Refresh, terminal receipt, cursor.
- Blocker: unresolved consequential choice stops before mutation; host approval cannot substitute for Decision Gate.
- Stale plan: changed snapshot/semantic/route digest creates a new epoch and binding; the old host turn cannot be resumed as equivalent.
- Permission pause: runtime-effect approval only; revalidate Arcanum baselines on resume.
- Interrupted execution: preserve touched/output/validation residue and reduce to flag/block; retry only under declared unchanged-route policy or a newly admitted attempt.
- Closeout failure: preserve execution-validated-closeout-pending evidence, but do not emit synchronized completion or a successor cursor.
- Replay: dedupe host events by thread/turn/item and Arcanum actions by loop/action/route fingerprint/idempotency key.

The minimal adapter input includes both native and Arcanum IDs, exact immutable selectors/digests, cwd/sandbox/network/model/approval policy, allowed writes, validation/closeout contracts, receipt schema, and idempotency key. Output includes normalized native events, separate host result and owner receipt, touched/output inventory, validation, narrow approval records, interruption residue, terminal correlation, and replay decision.

All 19 composition techniques are partial dispatch metadata rather than direct host hooks. All 31 standards techniques are validation policy, not host hooks. The 15 boundary/evidence techniques are adapter-relevant and partial: delegation boundary, authority split, protected action mapping, route projection, plan-import preview, capability/role projections, execution/evidence receipts and summaries, concrete paths, approval semantics, artifact bridge, state namespaces, and memory promotion split.

Generated text/schema/script payloads for the 14 selected packages matched canonical source after generated-frontmatter normalization except a material stale Dispatch Spec capability-bound delegation statement and one newline-only Weaver difference. Canonical Dispatch Spec records bounded installed-Codex causal proof while the generated Codex package still says native spawning proof is pending. Byte parity does not prove App Server behavior.

The continuous-controller Refine run remains deferred: validated route only, no ten-stage receipts, zero spawns, and no authority effect.

Local source families: `arcanum/arcana/refine/`, `arcanum/spells/invoke/`, `arcanum/formulae/dispatch-spec/`, Context Builder, Structured Interview Kits, Distill, Decision Gate, Work Pack Readiness, Implementation Readiness, Task Session, Task Session Until Blocker, Continuation Router, the continuous-controller refinement run, and the prior building-system research findings.

## Agent 3 — explorer-recursive-control-evals

Status: `pass`.

Core verdict: there is no deterministic App Server to Craft/Goal/eval/observability integration. Existing owners can consume a normalized execution receipt, but the normalizer, durable identity bridge, replay ledger, Craft receipt-ingestion primitive, bounded-round journal, and App Server-specific fixture harness are absent.

App Server may be an execution substrate only. Its thread, persisted goal, turn, item, approval, hook, and token-usage state must remain distinct from Craft state, Arcanum Goal rounds, Task Session receipts, semantic acceptance, lifecycle promotion, and publication.

Hook map:

- Thread start/resume/fork/session ID: execution container and recovery locator; not Craft context, Goal round, Work-Pack node, or Orchestrate run.
- Thread goal APIs: optional UI/runtime mirror only; conflicting name, absent integration.
- Turn start: begins a host attempt only after an admitted Arcanum route/action/attempt.
- Item deltas: provisional trace evidence. Item completion is final for the item but not the session.
- Turn diff: candidate changed-byte evidence to hash and bind; not acceptance or promotion.
- Approval/permission requests and `serverRequest/resolved`: runtime pause/decision evidence. “Resolved” can also mean cleanup.
- Waiting-on-approval status: runtime pause, not Craft blocker closure.
- Completed/interrupted/failed turn: raw terminal outcome requiring normalization; none implies semantic success.
- Hook events: inputs to an Observed Invocation envelope, not owner validation.
- Token usage: thread budget telemetry, not Craft/Goal budget authority.

Owner findings:

- Craft ledger is sole project-state authority. Deterministic receipt ingestion, row planner, renderer/index update, and validated YAML apply are absent.
- Goal contracts frontier, risk, dispatch, terminal receipt, audit, staged delta, explicit approval, Craft apply; the Python runtime is a read-only skeleton and does not yet run this loop.
- Inventory is a non-authoritative discovery/read model.
- Experiment Harness is the fixture/oracle owner but lacks an App Server profile.
- Observed Invocation Loop, Signal Observer, and Workflow Reflect are provider-neutral downstream seams, not a direct App Server bridge.
- Sigil Maintenance, Sigil Development, and Spellcraft are deferred lifecycle consumers after credible telemetry/evidence.
- Constitution, Discipline, and Definitions governance retain their separate artifact authorities.
- Observability Setup currently conflicts over default topology wording (`hybrid` versus central ledger with reference indexes).
- Bootstrap/generated sync are partial host-package distribution seams; no App Server profile exists.
- Decision Gate is mandatory for Arcanum decisions; host approval cannot substitute.
- Necronomicon and Context Builder stay outside terminal-result authority.
- Research Evidence Harness is a later fit for structured App Server fixtures once an adapter schema exists.

Continuous bounded round:

```text
BIND
  -> SNAPSHOT_CRAFT(ledger_sha256, frontier_hash)
  -> SELECT_NODE(owner route already validated)
  -> OPEN_OR_RESUME_HOST(thread/session identity)
  -> START_ATTEMPT(turnId bound to route/action/attempt)
  -> STREAM_EVIDENCE
       -> RUNTIME_PAUSE(permission/approval/question)
       -> RECOVER_STREAM(thread/read or resume)
       -> INTERRUPTED | FAILED | COMPLETED_RAW
  -> NORMALIZE_TERMINAL_RECEIPT
  -> OWNER_VALIDATE
  -> AUDIT
  -> STAGE_CRAFT_DELTA(expected ledger_sha256)
  -> WAIT_ARCANUM_APPROVAL
  -> CRAFT_APPLY_AND_VALIDATE
  -> RECOMPUTE_FRONTIER
       -> NEXT_ROUND | COMPLETE | NO_PROGRESS_STOP | BUDGET_STOP
```

Stop on missing/ambiguous ledger, missing terminal state after recovery, duplicate/replayed terminal mismatch, stale ledger digest, audit veto, missing done evidence, missing exact Arcanum approval, repeated unchanged frontier/receipt/delta hash, or any round/turn/spawn/token/time ceiling.

Preserve two identity namespaces. Arcanum: Craft scope/context, Work Pack/SWU, dispatch/action/attempt, owner receipt, Goal round. App Server: server instance, session, thread, turn, item, request, process. Minimum dedupe keys bind all relevant IDs plus event kind and payload/output/diff hashes. `thread/resume` is recovery, not replay authority. Fork requires a new Arcanum attempt. Deprecated rollback must never roll back Craft.

Existing eval evidence includes nine Goal fixtures, six Sigil Maintenance states plus generated mirrors, Observed Invocation append/dedupe/threshold/reflection/strict-failure cases, and three live Invoke CLI regimes. Missing App Server cases: completed normalization, failed turn, interrupt/resume, duplicate/full-history replay, runtime permission variants, stale Craft digest, item without turn completion, disconnect reconciliation, host-goal non-collapse, audit veto/closeout failure, no-progress stop, generated skill plus observability, privacy filtering, and a live canary.

Required oracle layers: protocol ordering, identity non-substitution, receipt fields/hashes, authority separation, replay no-op, digest-bound approved Craft mutation, lifecycle non-promotion, and exactly-once privacy-safe observability.

Missing deterministic primitives: `AppServerExecutionEnvelope`, bidirectional identity record, ordered event journal/cursor, terminal normalizer, approval/acceptance separation validator, replay store, Craft dry-run/apply receipt ingestion, persistent Goal round journal/no-progress detector, App Server fixture player/failure injection, Experiment Harness App Server profile/canary, observation-envelope derivation, generated-package attachment, and a lifecycle regression proving host success cannot promote a capability.

Official external evidence was constrained to <https://learn.chatgpt.com/docs/app-server>. Local selectors cover Craft skill/architecture/schemas, Goal README/runtime/fixtures, Experiment Harness, Observed Invocation Loop, Signal Observer, Workflow Reflect, observability architecture, Sigil Maintenance/Development, Spellcraft, promotion gates, Observability Setup, Bootstrap, generated sync, and the continuous-controller refinement run.

## Joined tensions for synthesis

1. “Callable from Codex” currently means generated skill policy plus native collaboration tools, not App Server integration.
2. App Server owns transport and execution episodes; Arcanum retains intent, admission, validation, receipt, gate, ledger, lifecycle, and publication authority.
3. One bounded adapter can serve authoring stages and Task Session attempts only if it preserves distinct IDs and owner receipts.
4. Continuous Craft control requires a separately approved, digest-bound staged ledger delta after audit; it cannot be driven from streamed events.
5. The first implementation target should be an execution envelope, identity/replay journal, terminal normalizer, and deterministic fixture profile—not a second goal/controller abstraction.
6. Current claims must remain architecture/research readiness. No App Server runtime or end-to-end integration is proven.
