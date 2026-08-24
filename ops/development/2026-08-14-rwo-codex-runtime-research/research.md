# Explorer Returns

Dispatch: `2026-08-14-rwo-codex-runtime-research`

These sections preserve the explorer returns verbatim. The parent added only the section labels and verbatim fences.

## `spawn-0001` — `explorer-rwo-eve-inventory`

````json
{
  "action_id": "spawn-0001",
  "role": "explorer-rwo-eve-inventory",
  "status": "completed",
  "mode": "explore",
  "mutation": {
    "files_written": [],
    "git_used": false,
    "providers_executed": false
  },
  "receipt_output_ref": "ops/development/2026-08-14-rwo-codex-runtime-research/receipts/explorer-rwo-eve-inventory.json",
  "findings": {
    "architecture_boundary": [
      "The Rust RWO kernel is provider-neutral and owns deterministic admission, compilation, reduction, semantic identity, at-most-one CommandIntent, and no-successor behavior. It does not own execution, transport, retry authorization, scheduling, or effects.",
      "Delivery identifiers, attempts, clocks, leases, offsets, traces, sessions, and adapter metadata are physical evidence and must never become semantic RWO identity.",
      "RetrySame preserves the complete semantic command; a new physical attempt is not new semantic work. Unknown delivery must never default to retry."
    ],
    "component_map": {
      "retain": [
        "implementations/rwo-rust/**",
        "rwo-sidecar-go/durable_store.go and tests",
        "rwo-sidecar-go/durable_runtime.go architecture",
        "rwo-sidecar-go/child_kernel.go and tests",
        "rwo-sidecar-go/sidecar.go and provider-neutral boundary tests",
        "rwo-sidecar-go/grpc.go, http.go, local_runtime.go and tests",
        "content-addressed material resolution, path containment, symlink rejection, hash checks, closed capability policy",
        "terminal replay/divergence/no-successor convergence after provider translation"
      ],
      "replace_or_split": [
        "eve_leaf.go: replace Eve HTTP/NDJSON/session adapter with Codex App Server adapter",
        "seat_material.go: retain material and command decoding; replace Eve request classes, fields, errors, and RWO-EVE-REQUEST-V1",
        "terminal.go: preserve RawEveLineV1 meaning; add a new provider evidence record and split provider parsing from provider-neutral terminal admission",
        "attempts.go: preserve V1 persisted meaning; introduce versioned provider-neutral handles/checkpoints instead of renaming session/stream fields in place",
        "cmd/rwo-local-runtime/main.go: add actual attempt/provider/terminal worker wiring"
      ],
      "critical_runtime_gap": "The current CLI only starts the Rust child, compiles, opens the durable store, constructs DurableRuntime, and exposes the gRPC event boundary. It does not instantiate AttemptCoordinator, Eve/App Server transport, terminal coordination, or a delivery worker. Migration is therefore partly missing runtime wiring, not merely swapping a live leaf."
    },
    "eve_denominator": {
      "active_provider_code": [
        "implementations/rwo-sidecar-go/eve_leaf.go",
        "Eve-specific request encoding in seat_material.go",
        "RawEveLineV1 writer/parser and Eve event grammar in terminal.go",
        "session/stream-shaped V1 attempt projection in attempts.go"
      ],
      "active_tests_and_fixtures": [
        "eve_leaf_test.go",
        "Eve request cases in seat_material_test.go",
        "Eve terminal grammar/order cases in terminal_test.go",
        "fake-Eve durable_e2e_test.go",
        "Eve-specific failure rows FM06, FM16, FM17 and PC01",
        "session/reconnect vocabulary in attempts_test.go",
        "all five files under testdata/eve-one-seat/"
      ],
      "current_docs_to_supersede_or_refresh": [
        "implementations/rwo-sidecar-go/README.md",
        "docs/features/recursive-work-orchestrator/README.md current fake-Eve ceiling",
        "canonical proposal ontology 0.3.0 Eve compatibility finding/residue/questions"
      ],
      "preserve_as_history": [
        "RWO-IMPLEMENTATION-EVIDENCE-2026-08-13.md",
        "DURABLE-RUNTIME-VALIDATION-REPORT.md",
        "20260813T141038Z-rwo-eve-durable-runtime-implementation/**",
        "WP-RWO-EVE-DURABLE-LOCAL-001, RWO-EVE-DURABLE-STORE-001, SWU-RWO-DRT-* and related lifecycle identifiers",
        "prior Eve research, audit, refresh, rollback, staging, and task-session artifacts"
      ],
      "unrelated_external_tool_history": [
        "research/external-tools-verification/**",
        "sessions/2026-07-21-2120-external-tools-research.md",
        "docs/discovery/external-tools/README.md",
        "agents-communication-infra Eve adoption material"
      ]
    },
    "invariant_analysis": {
      "survives_provider_substitution": [
        "semantic versus physical separation",
        "append and fsync before acknowledgement",
        "hash chain, sequence, cursor CAS, exclusive lock, and poison-on-uncertain-write",
        "only incomplete final-tail truncation during recovery",
        "stable attempt/send-try identity bound to command, adapter profile, request fingerprint, and ordinal",
        "lease/fence ownership",
        "arm-before-send",
        "retry only after exact known-not-sent proof plus continuation authority",
        "ambiguity freeze and exact late-response lineage",
        "persist raw provider evidence before interpretation",
        "material provenance, bounded output schema, terminal replay/divergence checks, and Rust no-successor admission"
      ],
      "falsely_coupled_to_eve": [
        "one session ID as complete provider identity",
        "session_known, stream_attached, stream_detached, last_event_id, MapSession, and session-bound cancel/ack",
        "POST /eve/v1/session, 202 sessionId, NDJSON LF framing, afterEventId, and Eve cancel endpoint",
        "requestInput and RWO-EVE-REQUEST-V1",
        "session.started, task.output, session.completed, and numeric event-ID grammar",
        "terminal keys containing an Eve session ID",
        "a single create operation and Eve tool-free booleans as evidence of App Server permissions or sandbox behavior"
      ]
    },
    "current_evidence_drift": {
      "historical_report_inventory_matches": 20,
      "historical_report_inventory_drifted": 4,
      "drifted_files": [
        {
          "path": "implementations/rwo-sidecar-go/durable_runtime.go",
          "expected_sha256_prefix": "aeec",
          "current_sha256": "b40a401d...1778"
        },
        {
          "path": "implementations/rwo-sidecar-go/durable_runtime_test.go",
          "expected_sha256_prefix": "f914",
          "current_sha256": "1fc1...5f31"
        },
        {
          "path": "implementations/rwo-sidecar-go/attempts.go",
          "expected_sha256_prefix": "5df1",
          "current_sha256": "73d5...244f"
        },
        {
          "path": "implementations/rwo-sidecar-go/terminal.go",
          "expected_sha256_prefix": "991c",
          "current_sha256": "000056...3107"
        }
      ],
      "consequence": "The 2026-08-13 six-SWU PASS cannot be applied to all current active bytes. A fresh complete inventory and validation are required. Existing drift must be preserved as unattributed concurrent work.",
      "recorded_dirty_snapshot": "The active convergence context records 28 tracked changes, 2,858 untracked paths, and 0 staged paths. This was not refreshed because Git inspection was forbidden."
    },
    "prospective_changed_byte_inventory": [
      "attempts.go and attempts_test.go",
      "seat_material.go and seat_material_test.go",
      "replace eve_leaf.go and eve_leaf_test.go with App Server equivalents",
      "terminal.go and terminal_test.go, likely split into generic admission and provider translation",
      "durable_e2e_test.go",
      "failure_injection_test.go",
      "cmd/rwo-local-runtime/main.go",
      "implementations/rwo-sidecar-go/README.md",
      "active fixture bindings plus new testdata/app-server-one-seat/",
      "new provider adapter/interface and versioned durable record/schema files",
      "new dated validation report and versioned ontology migration"
    ],
    "migration_dependency_dag": [
      "G0: close current inventory and resolve or explicitly bind the four-file evidence drift",
      "G1: select provider-neutral physical identity and durable compatibility posture; add new record versions without reinterpreting V1",
      "G2: extract generic attempt/material contracts and provider adapter interface",
      "G3: implement the exact Codex App Server process/protocol translator using independently sourced protocol bindings",
      "G4: implement new raw-provider evidence and App Server event translation into generic terminal admission",
      "G5: wire the real CLI worker, recovery, reconciliation, and single-scheduler ownership",
      "G6: port fixtures/tests and expand crash cuts",
      "G7: issue new report, current documentation, ontology migration, and new Work-Pack identifiers; preserve Eve lineage",
      "G8: run independent evidence closure and owner acceptance"
    ],
    "test_impact": {
      "retain_and_rerun": [
        "Rust offline suite and Python differential/vector tests",
        "durable store, semantic runtime, child kernel, sidecar, gRPC, and local-runtime tests",
        "material provenance/path/symlink/drift tests",
        "ported attempt fencing, ambiguity, terminal replay/divergence, governance-output, and no-successor tests"
      ],
      "replace": [
        "Eve HTTP request/stream/cancel tests",
        "exact Eve request fixture",
        "Eve terminal event grammar/order tests",
        "fake-Eve E2E and PC01"
      ],
      "add": [
        "App Server startup and handshake",
        "connection loss and process recovery",
        "thread/turn/request identity correlation",
        "crash cuts around start/send/response/persist/admission",
        "permission request pause, deny, and bounded continuation",
        "interrupt and recovery-only resume",
        "ambiguous delivery reconciliation",
        "exact duplicate no-op and identity/hash mismatch",
        "invalid and post-terminal event handling",
        "no-successor enforcement and CLI end-to-end integration"
      ]
    }
  },
  "proof_ceiling": [
    "This receipt establishes a source-grounded architecture and current-code inventory only.",
    "The existing report proves an older candidate-local fake-loopback Eve path on one host/filesystem, but not the four drifted active files.",
    "There is no real Eve proof, App Server proof, installed-binary proof, live provider wiring, permission/interruption/recovery proof, lifecycle synchronization, publication, deployment, or production evidence.",
    "No claim of Codex compatibility or implementation readiness is sustained."
  ]
}
````

## `spawn-0003` — `explorer-authority-integration`

````markdown
## Bounded research receipt — `spawn-0003`

- Role: `explorer-authority-integration`
- Status: `pass`
- Validation: `pass`
- Mutation: none
- Repository writes: none
- Output for parent persistence: `ops/development/2026-08-14-rwo-codex-runtime-research/receipts/explorer-authority-integration.json`
- Claim ceiling: source-grounded architecture decision, `specified-unexecuted`; no App Server run, implementation, readiness, lifecycle completion, promotion, publication, or deployment is proved.

### Discriminating decision

```text
Task Session admission + execution ticket
  -> one Arcanum framework/runtime envelope
       -> private consuming-repository adapter profile
            -> private RWO durable Go host
                 -> Rust semantic compiler/reducer
                 -> RWO journal + attempt/fence/replay owner
                 -> Codex App Server leaf driver
                      -> pinned App Server process/thread/turn/items
            <- private RWO result + provider evidence references
       <- generic runtime STATUS/events projection
  -> Task Session executor receipt
  -> named capability-owner verdict
  -> reconciliation + precloseout
  -> joined closeout-owner receipt
  -> Task Session governance terminal
  -> privacy-safe observation
```

`framework/runtime` envelopes the RWO host; it does not replace it. The private bridge consumes the Arcanum handoff, but RWO’s Go journal remains the sole authoritative store for RWO semantic and physical delivery state. App Server is a leaf beneath RWO, not another scheduler or runtime envelope.

This deliberately narrows the August 13 direct-App-Server architecture. That map remains coherent for ordinary Refine or directly admitted Task Session execution, but its stateful live adapter cannot be placed alongside the existing RWO Go attempt coordinator without duplicating provider identity, cursor, ambiguity, retry, raw-event persistence, and terminal-normalization authority. For RWO, reuse the public protocol/profile and `app-server.host-result.v0` evidence shape, not a second independently durable App Server run.

Proof: `arcanum/framework/runtime/README.md:3-15,17-33,64-87,116-118`; `projects/cyberalchemy-orchestrator/implementations/rwo/DURABLE-RUNTIME-VALIDATION-REPORT.md:28-62`; `ops/development/2026-08-13-arcanum-codex-app-server-integration-map/findings.md:182-207`.

### Alternatives rejected

| Alternative | Verdict | Reason |
|---|---|---|
| Public `app-server` runtime adapter directly owns the Codex run and later feeds RWO | reject | It bypasses or duplicates RWO’s proven arm-before-send, lease/fence, delivery-unknown, raw persistence, reconciliation, terminal admission, and retry owner. |
| RWO calls a second complete `framework/runtime app-server` run behind its Go host | reject | Two durable envelopes would retain overlapping provider cursors and terminal truth. Crash recovery could diverge. |
| RWO replaces `framework/runtime` or Task Session | reject | RWO owns recursive domain semantics and physical delivery, not work-pack selection, mutation admission, executor receipts, owner verdicts, or closeout. |
| App Server-backed Orchestrate host | defer separately | App Server collaboration/subagent items cannot satisfy native `collaboration.spawn_agent`, wait, inventory, interrupt, causal join, or gate contracts. |
| App Server host goals drive Craft or Goal | reject | Host goal/thread state is not Craft authority, Goal frontier state, or an apply token. |
| Rename Eve types while retaining session/NDJSON assumptions | reject | App Server introduces process, connection, thread, turn, item, request, pause, interrupt, and recovery identities; the physical state machine needs substantive replacement. |

### Authority allocation

| Concern | Sole owner | Legal downstream evidence |
|---|---|---|
| Work-Pack authoring | Invoke Plan | candidate plan only |
| Frozen-frontier audit | Work Pack Readiness | readiness evidence, not selection/admission |
| Unit selection and mutation admission | Task Session / Implementation Readiness as currently routed | single-use ticket and admission |
| Outer execution envelope | `framework/runtime` / `tools/arcanum` | `RUN.json`, `STATUS.json`, high-level `events.jsonl` |
| RWO semantic scheduling | Rust kernel | accepted-event and command identities; zero-or-one command |
| RWO causal durability | Go `DurableStore` | authoritative journal record references/digests |
| Physical attempt, fencing, ambiguity, retry | Go `AttemptCoordinator` | attempt/send/fence state |
| Provider protocol transport | private Codex leaf driver | raw App Server request/event evidence |
| Provider raw-event persistence and recovery cursor | RWO Go journal | authoritative raw records; outer event log receives references only |
| RWO terminal admission/no-successor | Go terminal coordinator plus Rust reducer | private RWO result |
| Runtime outcome classification | private bridge, projected through framework runtime | raw host result/status, never semantic acceptance |
| Executor receipt | Task Session executor owner | `task-session.executor-receipt.v1` |
| Domain acceptance | named capability owner | owner-native verdict or `task-session.owner-hook-receipt.v1` |
| Governance closeout | Task Session plus joined closeout owner | precloseout and governance-terminal receipts |
| Governed multi-agent dispatch | Orchestrate only | native action/join/gate receipts |
| Project ledger | Craft only | approved ledger mutation |
| Bounded project-control loop | Goal only | frontier/route/audit/staged-delta evidence |
| Fixture/canary behavior evidence | Experiment Harness | eval result only |
| Observation | OIL + Signal Observer | privacy-safe telemetry, not verdict |
| Promotion/publication | target lifecycle/publication owners | separately accepted exact revision |

Key sources: `arcanum/arcana/task-session/SKILL.md:239-335,337-417`; `arcanum/runtime/orchestrate/SKILL.md:72-81,124-164,211-223`; `arcanum/spells/goal/README.md:8-17,58-68,82-108`; `arcanum/arcana/craft/SKILL.md:67-71,312-317`; `arcanum/arcana/experiment-harness/SKILL.md:97-102`; `arcanum/spells/observed-invocation-loop/README.md:12-18,51-70`; `arcanum/arcana/signal-observer/SKILL.md:89-104`.

### Identity non-substitution matrix

| Namespace | Identities | Must remain distinct from |
|---|---|---|
| Task Session | `run_id`, `task_id`, `swu_id`, `ticket_id`, `attemptId`, `admissionToken`, `idempotency_key` | every RWO and provider identity |
| Framework runtime | runtime run ID, adapter ID, event sequence, status | RWO stream/cursor and App Server thread |
| RWO semantic | graph, stream, cursor, accepted-event identity, command identity | Task Session admission and provider terminal |
| RWO physical | physical attempt ID, attempt ordinal, send-try ID/ordinal, lease owner, fence epoch | App Server thread/turn/request IDs |
| Provider process | process instance, listener, connection | runtime run or RWO attempt |
| App Server | `threadId`, `turnId`, `itemId`, JSON-RPC/server-request ID, command process ID | RWO command, attempt, send try, receipt, or approval |
| Craft | scope/context and ledger digest/rows | host thread/goal |
| Goal | frontier snapshot, round, route, batch, approval token | host goal and token usage |
| Orchestrate | dispatch/run/wave/step/action/agent IDs | App Server subagent or collaboration item |

The current Go state has one Eve-shaped `SessionID`; replacing it requires a provider binding containing process/connection/thread/turn plus request and item identities. A rename to `ThreadID` is insufficient. An RWO attempt may span multiple provider calls such as initialize, thread start/read/resume, turn start, permission response, interrupt, and reconciliation. Each effectful call needs a durable operation/send identity under the existing RWO attempt, while raw App Server IDs remain correlation values.

Sources: `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/attempts.go:57-113,140-177,371-417,420-487`; `ops/development/2026-08-13-arcanum-codex-app-server-integration-map/findings.md:140-154`.

### State and durability partition

1. Task Session must issue and persist admission/ticket evidence before the private adapter can launch RWO for mutating execution.
2. The RWO journal persists semantic commits, physical attempt state, provider operation state, raw App Server messages, and terminal admission.
3. Before each effectful App Server call, RWO must append the operation’s armed state with the frozen request hash, provider profile, attempt, send identity, and fence.
4. App Server messages must be durably recorded in the RWO journal before translation or semantic interpretation.
5. `framework/runtime/events.jsonl` records high-level transitions and references/digests to the RWO journal. It must not become a competing replay cursor or raw provider store.
6. A crash after an RWO append but before the outer projection is repaired by rebuilding that projection from the authoritative RWO record; no semantic or provider call is repeated.
7. Ambiguous thread/turn delivery freezes the attempt and requires provider reconciliation. Resume is recovery, not replay authority. Blind retry is forbidden.
8. Exact duplicate identity and payload is an inert replay; same identity with changed hash blocks.
9. `turn/completed` is only provider evidence. RWO validates output, effects, policy, and provider-event closure, derives its private terminal accepted event, reduces through Rust, and requires no successor before returning a successful private RWO result.
10. The outer runtime then classifies the host outcome; Task Session still emits the executor receipt and joins owner/closeout evidence.

The current candidate proves this discipline only for Rust plus fake Eve: `DURABLE-RUNTIME-VALIDATION-REPORT.md:14-24,32-62,74-124`. App Server compatibility remains unverified.

### Approval and gate separation

- App Server approval: one response for one provider request ID under the frozen runtime policy.
- RWO authorization event: domain-semantic input to Rust, not an Arcanum mutation admission.
- Task Session admission: one single-use task/SWU execution authorization.
- Decision Gate: one named consequential decision.
- Dispatch confirmation: one exact registered multi-agent dispatch.
- Capability-owner acceptance: one candidate and validation binding.
- Goal token: one bounded proposed Craft-apply attempt.
- Craft apply: active project-ledger mutation by Craft.
- Lifecycle promotion, publication, release, and deployment: separate owner gates.

A provider permission already covered by the frozen admission may receive an `approved-once` response. A permission that expands filesystem, network, process, model, tool, or write scope blocks the current attempt; runtime approval cannot repair stale or expanded Task Session admission.

### Result and receipt chain

```text
RWO private execution result
  + embedded/referenced app-server.host-result.v0
  + authoritative RWO journal selectors/digests
  -> framework/runtime STATUS.json
  -> task-session.executor-receipt.v1
  -> named capability-owner verdict or task-session.owner-hook-receipt.v1
  -> validation reconciliation
  -> task-session.precloseout-execution-receipt.v1
  -> joined closeout owner receipt
  -> observation receipt/reference
  -> task-session.governance-terminal-receipt.v1
```

The Task Session schemas require separate ticket, executor, owner, precloseout, joined closeout, and terminal artifacts. The terminal receipt explicitly forbids executing a successor and carries a null or explicit cursor. RWO journal records and App Server host results are inputs to this chain, not replacements for it.

### Orchestrate, Goal, Craft, eval, and observation hooks

- Orchestrate stays outside ordinary RWO-to-Codex execution. Use it only when the Arcanum route itself is a separately validated governed multi-agent dispatch.
- App Server collaboration-agent and subagent activity is diagnostic provider activity. It cannot satisfy Orchestrate spawn/join.
- Goal may select and audit a Craft frontier node whose owner route eventually invokes Task Session/RWO, but it cannot interpret an App Server host goal, turn completion, or token count as project progress.
- Craft receives only a separately audited staged delta and applies it through its own approval/validation path.
- Experiment Harness owns protocol manifests, installed-binary parity, deterministic fixture playback, failure injection, denominator checks, privacy checks, and bounded canaries.
- OIL should observe the outer managed invocation after primary completion. Signal Observer stores summaries, identities, paths, validation state, and hashes—not private prompts, raw model content, credentials, or unrestricted provider messages.
- Observation failure is non-blocking unless strict telemetry was explicitly part of the task contract.

### Public/private boundary

Public Arcanum may contain only generic contracts:

- bounded runtime handoff and status/event envelope;
- generic locally registered durable-child adapter validation, if added;
- pinned App Server protocol/profile and raw host-result schemas;
- authority-null fields and non-substitution rules;
- fixture/eval machinery;
- Task Session bindings and generic generated-package propagation.

Private parent/nested RWO owns:

- RWO vocabulary, semantic tuple, graph/cursor/accepted-event/command model;
- RWO journal record types and attempt/fence/replay rules;
- the `rwo-codex` consuming-repository profile and bridge;
- mapping from RWO command/material to Codex thread/turn inputs;
- mapping from validated Codex terminal evidence to `SeatTerminalObservedV1`;
- private migration and historical-preservation ledgers.

Do not add `RWO`, `SeatTerminalObservedV1`, private Work-Pack IDs, or private authority prose to public `arcanum/`. Root authority explicitly states Arcanum is public and the surrounding system is private: `AGENTS.md:7-12`.

A current implementation gap remains: `tools/arcanum` recognizes a fixed adapter set, and live `app-server` is reserved but absent. The safe repair is a generic, manifest-validated local adapter registration mechanism with exact executable digest, argv array, cwd, environment-name allowlist, timeout, output paths, and authority ceiling. Do not special-case private RWO identifiers in public `tools/arcanum`, and do not grant generic shell authority.

### Lifecycle impact

The current RWO planning surface has advanced beyond the older validation report wording:

- candidate-local implementation evidence is recorded;
- a reconciliation audit passed;
- only `SWU-RWO-DRT-001` validation-only evidence adoption is selection-ready;
- selection is null;
- Task Session admissions and terminal receipts remain zero;
- continuation is not authorized.

Sources: current `WORK-PACK.md:1-13,23-39,65-70,85-102`; current `EXECUTION-ENTRY.json#/execution_entry` and `#/pre_execution_owner_prerequisite/governed_lifecycle_state`; `20260813T190813Z.../APPLY-REPORT.md:14-22`.

The Codex migration must not reuse that DRT-001 route. It permits only two validation evidence outputs and forbids product mutation. The old Work Pack also states that semantic/profile/schema/identity change routes back through Refine/Invoke Refresh. Therefore the migration needs a new planning epoch and non-executed Work Pack. Existing Eve planning, receipts, tests, and audit evidence remain immutable historical proof or are explicitly superseded; they must not be rewritten into Codex evidence.

### Dependency-ordered implementation outline

1. Close the active Eve denominator and historical-preservation ledger from the implementation explorer.
2. Freeze current Rust/Go source, current Arcanum runtime/Task Session contracts, pinned App Server protocol, installed binary identity, and binary/source parity status.
3. Author a new private Refine/Invoke migration epoch. Do not mutate or appropriate the existing DRT-001 evidence-adoption route.
4. Define the generic public durable-child adapter/profile contract, or prove an existing contract sufficient. Require exact executable/argv/cwd/environment/output/timeout bindings and projection-only outer events.
5. Define the private RWO provider-neutral leaf port. Preserve semantic and physical owners while removing Eve HTTP/session/NDJSON assumptions.
6. Extend the RWO physical state machine for process/thread/turn/request/item bindings and per-operation pre-call evidence. Keep attempt, send, lease, fence, ambiguity, and retry authority in Go.
7. Implement the private Codex stdio leaf with the minimal profile. It may launch only the pinned App Server child; it must not expose App Server’s unsandboxed-process API to the model.
8. Replace the Eve terminal validator with App Server event/result normalization. Provider completion must pass schema, effect, ordering, identity, and no-post-terminal checks before Rust admission.
9. Implement the private outer bridge: Task Session/runtime handoff to RWO input; private RWO result and provider evidence to generic runtime status and Task Session executor evidence.
10. Build deterministic fixtures and crash injection before any live process run.
11. Prove installed-binary/source-schema parity.
12. Run one read-only bounded live canary only after fixture closure. A mutation canary requires separate admission.
13. Run named capability-owner review, Task Session closeout integration, privacy-safe observation, and lifecycle non-promotion tests.
14. If public Arcanum canonical sources change, run their owner promotion gates and selectively regenerate only affected packages with `sync-generated-skill-package.sh`; never bulk-replace the generated surface.
15. Return a fresh candidate inventory, digests, independent review, and exact owner acceptance request before any apply.

### Required eval matrix

Every trace must bind Task Session, runtime, RWO semantic/physical, and provider identities; persisted records; first stop; forbidden effects; proof status; and validator.

- successful command → Codex turn → validated RWO terminal → Rust no-successor;
- permission pause under unchanged policy;
- permission expansion block;
- stale baseline before provider launch;
- interrupt followed by recovery-only resume;
- ambiguous process/thread creation;
- ambiguous turn start;
- exact duplicate no-op;
- identity/hash replay mismatch;
- invalid, reordered, or post-terminal provider event;
- item completion without turn terminal;
- provider terminal without valid RWO output;
- Task Session closeout-owner failure after valid RWO execution;
- crash before each effectful provider call;
- crash after RWO arm and before provider response;
- crash after each raw provider event append;
- crash after provider terminal persistence but before RWO terminal validation;
- crash after Rust semantic terminal commit but before admission marker;
- crash after private RWO terminal but before outer runtime projection;
- privacy-filtered exactly-once observation;
- lifecycle non-promotion after successful host execution.

### Explicitly excluded first-profile integrations

- App Server-backed Orchestrate host;
- provider collaboration/subagent items as Arcanum agents;
- outbound code-mode-host connector;
- realtime/audio;
- shell and sandboxed-command APIs;
- unsandboxed process APIs;
- direct filesystem APIs;
- MCP, plugins, apps, marketplace, account, config, remote-control, or global administration;
- broad or undeclared network;
- provider host goals as Goal/Craft state;
- automatic Craft apply;
- automatic next SWU, DRT-002, or Goal round;
- multi-host durability or distributed consensus;
- publication, release, deployment, production, Git commit, push, or parent gitlink movement.

### Residue and open proof gaps

- No live App Server adapter exists.
- Installed-binary parity is unverified.
- No RWO-to-App-Server success witness exists.
- The current RWO attempt model is Eve-session-shaped and lacks exact thread/turn operation state.
- A generic safe local adapter registration contract is absent from `tools/arcanum`.
- The public fixture covers only F-01 translation.
- No Task Session ticket/admission/executor/closeout fixture currently binds RWO to App Server.
- No privacy-safe observation fixture covers private RWO provider evidence.
- Current planning reconciliation does not authorize this migration.

These are implementation-planning gaps, not blockers to the research decision.
````

## `spawn-0002` — `explorer-codex-protocol`

````json
{
  "action_id": "spawn-0002",
  "role": "explorer-codex-protocol",
  "status": "completed",
  "mutation_policy_observed": "read-only",
  "research_verdict": "A bounded fixture-first Codex profile can be specified, but current evidence does not support a live RWO leaf replacement. Installed-schema parity, tool and network denial, and exact ambiguous-create reconciliation remain blockers.",
  "claim_ceiling": "Official-protocol and local-fixture analysis only. No App Server process or model turn was started; no integration, semantic acceptance, readiness, lifecycle, publication, or production claim is supported.",

  "source_identity": {
    "official": "Current Codex App Server documentation fetched 2026-08-14: https://learn.chatgpt.com/docs/app-server",
    "installed_binary_path": "/home/vrondelli/.vscode-server/extensions/openai.chatgpt-26.810.41047-linux-x64/bin/linux-x86_64/codex",
    "installed_binary_version": "codex-cli 0.148.0-alpha.9",
    "installed_binary_sha256": "86a4286b2451c69d4c00ad1772fcee5170013f2924e7d257ad2d4f19290c2a20",
    "fixture_source_pin": "openai/codex@9946da9af1829410271f6b76f9159961f7281e0a",
    "installed_binary_to_fixture_pin_parity": "unverified"
  },

  "smallest_candidate_profile": {
    "profile_id": "rwo-codex-app-server-fixture-v0",
    "proof_status": "specified-unexecuted except existing F-01 normalized fixture",
    "transport": "stdio JSONL only",
    "api_surface": "stable API only; experimentalApi false",
    "connection": "initialize once, then initialized notification",
    "conversation": "one independently bound thread and one turn per RWO physical attempt",
    "input": "text-only, exact input digest and policy digest",
    "sandbox": "restricted read-only roots; no undeclared writable root",
    "forbidden": [
      "WebSocket and remote code-mode host",
      "fork, steer, review, realtime, thread goal, shell-command and command/exec APIs",
      "process/spawn, direct filesystem APIs, MCP, apps, plugins, marketplace and dynamic tools",
      "session-wide permission grants",
      "undeclared network or filesystem expansion",
      "collaboration-agent items as Orchestrate evidence"
    ],
    "terminal_set": ["completed", "failed", "interrupted", "delivery_unknown"],
    "authority_stop": "A completed Codex turn contributes only a physical host result. The RWO terminal validator and Rust reducer still own accepted-event identity, cursor advancement, and the zero-or-one successor decision."
  },

  "protocol_to_rwo_matrix": [
    {
      "protocol": "initialize -> initialized",
      "rwo_mapping": "Bind binary/profile/process/connection identity after durable provider-connection preparation.",
      "pre_call_evidence": "Binary path, version, digest, transport, clientInfo and capability hash.",
      "raw_persistence": "Request, response and initialized notification before interpretation.",
      "result": "Connection-ready only.",
      "forbidden_substitution": "Connection readiness is not RWO admission or semantic execution."
    },
    {
      "protocol": "thread/start",
      "rwo_mapping": "First provider create within one armed physical attempt.",
      "pre_call_evidence": "command_id, attempt_id, send_try_id, fence, exact request hash, input and policy digests.",
      "raw_persistence": "Response and thread/started notification; bind returned threadId and sessionId.",
      "result": "Provider thread bound.",
      "forbidden_substitution": "threadId must not equal command, attempt, Task Session or Craft identity."
    },
    {
      "protocol": "thread/read and thread/resume",
      "rwo_mapping": "Recovery inspection and reconnection for an already bound thread.",
      "pre_call_evidence": "Known threadId plus recovery reason and prior durable provider cursor.",
      "raw_persistence": "Full read/resume response and new connection binding.",
      "result": "Reconciled, still unknown, or blocked.",
      "forbidden_substitution": "Resume is not retry, replay authority, or fresh admission."
    },
    {
      "protocol": "turn/start",
      "rwo_mapping": "Physical execution call for the immutable RWO CommandIntent.",
      "pre_call_evidence": "Arm-before-send record binding command, attempt, send try, thread, exact input, cwd, sandbox, approval and model hashes.",
      "raw_persistence": "Response yielding turnId, followed by turn/started.",
      "result": "Turn in progress.",
      "forbidden_substitution": "turnId is not the RWO attempt or command identity."
    },
    {
      "protocol": "item/started, deltas, item/completed",
      "rwo_mapping": "Ordered physical evidence contribution.",
      "pre_call_evidence": "Existing bound turn.",
      "raw_persistence": "Every raw notification with adapter arrival sequence and canonical payload hash.",
      "result": "Deltas remain provisional; item/completed is authoritative.",
      "forbidden_substitution": "An item, agent message, command result or file change is not a receipt or semantic event."
    },
    {
      "protocol": "server-initiated approval or permission request",
      "rwo_mapping": "Pause the physical attempt and bind connection-scoped JSON-RPC request id with threadId, turnId and itemId.",
      "pre_call_evidence": "Exact requested effect and policy/admission digest.",
      "raw_persistence": "Request, intended decision, response-before-send record, response and serverRequest/resolved.",
      "result": "One runtime-effect decision only.",
      "forbidden_substitution": "Never Decision Gate confirmation, owner acceptance, Task Session admission, Craft apply or promotion. acceptForSession is forbidden in the first profile."
    },
    {
      "protocol": "turn/interrupt",
      "rwo_mapping": "Physical cancellation request.",
      "pre_call_evidence": "Durable interrupt intent bound to known threadId and turnId.",
      "raw_persistence": "Request/response plus eventual turn/completed status interrupted.",
      "result": "Interrupted host result with touched/output residue.",
      "forbidden_substitution": "A successful interrupt response is not terminal until turn/completed arrives; retry requires a new attempt."
    },
    {
      "protocol": "error plus turn/completed failed",
      "rwo_mapping": "Typed provider failure.",
      "pre_call_evidence": "Bound turn.",
      "raw_persistence": "Error details, codexErrorInfo, HTTP status when present, and failed terminal notification.",
      "result": "Failed host result.",
      "forbidden_substitution": "A disconnect without terminal is not failure proof; it remains delivery_unknown."
    },
    {
      "protocol": "turn/completed completed",
      "rwo_mapping": "Close physical evidence, verify output inventory and normalize host result.",
      "pre_call_evidence": "All prior raw items and approval requests resolved or explicitly cleared.",
      "raw_persistence": "Completed terminal plus authoritative item records and output/diff hashes.",
      "result": "Provider completed only; then a provider-neutral terminal candidate may be submitted to the Rust reducer.",
      "forbidden_substitution": "Completed is not semantic success, capability-owner acceptance, Task Session closeout or no-successor proof."
    }
  ],

  "identity_and_state_namespace": {
    "rwo_semantic": ["command_id", "accepted_event_id", "cursor_before", "cursor_after"],
    "go_durability": [
      "runtime_run_id",
      "store_instance_id",
      "journal_sequence",
      "attempt_id",
      "send_try_id",
      "lease_id",
      "fence"
    ],
    "codex_provider": [
      "binary_digest",
      "process_instance_id",
      "listener_id",
      "connection_id",
      "jsonrpc_request_id scoped to connection",
      "threadId",
      "sessionId",
      "turnId",
      "itemId",
      "server_request_id",
      "provider processId when present"
    ],
    "adapter_cursor": "Durable local arrival sequence plus raw message hash. App Server pagination cursors are not replay cursors.",
    "forbidden_equalities": [
      "threadId != RWO command_id or attempt_id",
      "turnId != RWO attempt_id or send_try_id",
      "itemId != accepted_event_id or receipt id",
      "JSON-RPC request id != approval, admission or acceptance identity",
      "sessionId != Task Session id",
      "Codex goal != Arcanum Goal or Craft state"
    ]
  },

  "host_result_contract": {
    "required": [
      "provider manifest: source/docs identity, installed binary path/version/digest, schema parity",
      "RWO binding: command, attempt, send try, fence, input and policy digests",
      "provider identity map",
      "pre-call evidence references and canonical request hashes",
      "append-ordered raw message references, hashes and adapter cursor",
      "approval/request ledger",
      "recovery and ambiguity disposition",
      "provider terminal status and typed error",
      "authoritative item inventory",
      "actual touched/output inventory and content hashes",
      "turn diff digest as evidence only",
      "proof status and explicit next owner"
    ],
    "authority_nulls": [
      "semantic verdict",
      "capability-owner verdict",
      "Task Session admission and terminal",
      "Craft state",
      "Goal control",
      "lifecycle promotion"
    ]
  },

  "material_gaps": [
    {
      "id": "GAP-PARITY-01",
      "finding": "The installed binary advanced from the previously audited 0.147.0-alpha.6.5 to 0.148.0-alpha.9, while F-01 remains pinned to an older source commit. No generated-schema comparison was authorized.",
      "effect": "No installed-binary protocol compatibility claim."
    },
    {
      "id": "GAP-AUTH-02",
      "finding": "Official stable documentation exposes sandbox and approval controls but does not establish a closed tool allowlist that disables shell/file tools, nor a documented read-only network-denial field.",
      "effect": "The tool-free, no-network Eve boundary has no proven live Codex equivalent. A host-level denial oracle and live negative witness are required."
    },
    {
      "id": "GAP-IDEMPOTENCY-03",
      "finding": "No client-supplied idempotency key is documented for thread/start or turn/start.",
      "effect": "Crash after send but before durable response creates an ambiguity that must freeze. thread/list/read can contribute reconciliation evidence but do not, from the documentation alone, prove unique exact delivery."
    },
    {
      "id": "GAP-FIXTURE-WIRE-04",
      "finding": "F-01 uses normalized dotted event names and omits raw JSON-RPC envelopes, initialized, request/response IDs, sessionId, userMessage and server requests.",
      "selectors": [
        "arcanum/framework/runtime/development/fixtures/app-server/f01-refine-success/events.jsonl:1-7",
        "arcanum/framework/runtime/development/fixtures/app-server/validate_fixture.py:22-38"
      ],
      "effect": "Fixture-observed normalization only, not wire parity."
    },
    {
      "id": "GAP-OUTPUT-05",
      "finding": "F-01 attaches a path/digest directly to an agentMessage. Official agentMessage is text; file evidence belongs to fileChange items, turn diffs and actual filesystem inventory.",
      "effect": "Replace synthetic output inference with authoritative item and host-observed output validation."
    },
    {
      "id": "GAP-REPLAY-06",
      "finding": "F-01 rejects a same-id/same-payload duplicate, while the current RWO durability contract requires exact replay to be inert.",
      "selectors": [
        "arcanum/framework/runtime/development/fixtures/app-server/validate_fixture.py:281-295",
        "projects/cyberalchemy-orchestrator/implementations/rwo/DURABLE-RUNTIME-VALIDATION-REPORT.md:44-50"
      ],
      "effect": "Adapter replay semantics must become exact-duplicate no-op and same-identity/different-hash block."
    },
    {
      "id": "GAP-DURABILITY-07",
      "finding": "The fixture hashes a complete synthetic JSONL file but does not witness append-and-sync-before-interpretation or crashes at raw-event boundaries.",
      "effect": "Go journal crash-cut fixtures remain mandatory."
    }
  ],

  "required_fixture_variants": [
    "C01 stable stdio success: exact raw initialize/thread/turn/item/terminal trace, host result, RWO accepted event, no successor",
    "C02 permission pause: exact request binding, durable pause, one narrow response or fail-closed decline, resolved cleanup, no authority inflation",
    "C03 stale input before turn/start: no provider call",
    "C04 interrupt and recovery-only resume: interrupted terminal, residue preserved, fresh attempt required",
    "C05 ambiguous thread/start: no second create; reconcile uniquely or block AMBIGUOUS_THREAD_CREATE",
    "C06 ambiguous turn/start: thread/read with exact predecessor/input binding; reconcile uniquely or block AMBIGUOUS_TURN_START",
    "C07 exact duplicate raw event: no-op",
    "C08 same provider identity with different payload hash: REPLAY_MISMATCH",
    "C09 error notification followed by failed terminal",
    "C10 item completion followed by disconnect without turn terminal: delivery_unknown",
    "C11 invalid or post-terminal event: block before RWO accepted-event admission",
    "C12 crash before provider send after pre-call arm: bound known-not-sent proof",
    "C13 crash after raw message sync before reduction: replay raw message and reduce once",
    "C14 crash after terminal normalization before semantic admission marker: reopen and admit once",
    "C15 output/diff mismatch: host inventory wins and blocks",
    "C16 request cleared by completion or interrupt: prohibit stale response",
    "C17 installed schema/source/fixture denominator mismatch: parity gate fails"
  ],

  "local_evidence": [
    "projects/cyberalchemy-orchestrator/implementations/rwo/DURABLE-RUNTIME-VALIDATION-REPORT.md:28-62",
    "projects/cyberalchemy-orchestrator/implementations/rwo/DURABLE-RUNTIME-VALIDATION-REPORT.md:95-124",
    "ops/development/2026-08-13-arcanum-codex-app-server-integration-map/findings.md:182-207",
    "arcanum/framework/runtime/development/fixtures/app-server/f01-refine-success/profile.json:1-69",
    "arcanum/framework/runtime/development/fixtures/app-server/f01-refine-success/expected-host-result.json:1",
    "arcanum/framework/runtime/development/fixtures/app-server/validate_fixture.py:220-295"
  ]
}
````
