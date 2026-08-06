# Verbatim Explorer Returns

Dispatch: `2026-07-30-intent-router-bootstrap-runtime-integration`

## Explorer: Hewitt, Carl — Bootstrap and Runtime Portability

```yaml
dispatch_id: 2026-07-30-intent-router-bootstrap-runtime-integration
step_id: s1
capability_ref: research
capability_target: dispatch-sheet.json
capability_mode: explore
wave_id: explore
write_scope: []
status: complete
artifacts: []
validation:
  method: read-only source inspection
  commands_run:
    - targeted sed/rg/find/nl inspection only
  mutations: none
  runtime_execution: none
observer_status: not_run
blockers:
  - No canonical public Arcanum sigil or spell named intent-route-resolver exists.
  - The current resolver package is private and cannot be copied into public Arcanum without an explicit extraction/publication decision.
  - Bootstrap has no generic add-on/package selector; it selects only canonical sigils and spells.
residue:
  - Public extraction boundary and ownership remain undecided.
  - Behavioral-parity fixtures for generated Codex and Claude projections do not yet exist.
  - Bootstrap provenance lacks source/package version and content digest.
  - Full bootstrap force mode has no transactional rollback.
reroute: >
  Route a bounded public-extraction/design task before implementation. If approved,
  create one canonical public Arcanum sigil containing the generic executable core,
  manifest, fixtures, and a thin native skill wrapper; then validate Bootstrap and
  selective-sync projections.
handoff_note: >
  Do not install or sync the existing private package. Treat the proposed commands
  below as future fixtures only, after a canonical public extraction is admitted.
```

Findings

1. Topology decision

Current direct Bootstrap topology: **killed**.

`bootstrap_arcanum.sh --sigils intent-route-resolver` can resolve only directories under `arcanum/formulae`, `arcanum/transmutations`, or `arcanum/arcana` ([bootstrap_arcanum.sh:371](arcanum/tools/bootstrap_arcanum.sh#L371), [bootstrap_arcanum.sh:383](arcanum/tools/bootstrap_arcanum.sh#L383)). The standalone resolver exists only under private `cyberAlchemy-v2`, so selection terminates with `Unknown sigil`.

`--spells intent-route-resolver` is likewise invalid because spell selection requires `arcanum/spells/<id>/README.md` ([bootstrap_arcanum.sh:411](arcanum/tools/bootstrap_arcanum.sh#L411)).

Selective sync has the same boundary: it accepts exactly one canonical sigil or spell and rejects anything outside those canonical locations ([sync-generated-skill-package.sh:80](arcanum/tools/sync-generated-skill-package.sh#L80), [sync-generated-skill-package.sh:106](arcanum/tools/sync-generated-skill-package.sh#L106)).

Narrowed target topology:

```text
public canonical Arcanum sigil
  arcana/intent-route-resolver/
    SKILL.md                 thin native invocation wrapper
    package/                 pure executable core
    addon-manifest.json      machine-readable protocol/package contract
    fixtures/                cross-host conformance witnesses
    scripts/                 deterministic fixture runner
        |
        +-- Bootstrap repo-codex --> .agents/skills/intent-route-resolver/
        |
        +-- Bootstrap claude -----> .claude/skills/intent-route-resolver/
```

This fits the existing generator: all top-level support files and all support directories except `development/` are copied into each generated package ([bootstrap_arcanum.sh:821](arcanum/tools/bootstrap_arcanum.sh#L821)). Both projections are generated from the same canonical source and support tree ([bootstrap_arcanum.sh:1215](arcanum/tools/bootstrap_arcanum.sh#L1215)).

2. Current-versus-target compatibility

| Concern | Current state | Required target |
|---|---|---|
| Executable core | Private ESM package, version `0.1.0`; pure and side-effect-free | Publicly reviewed generic subset under canonical Arcanum ownership |
| Native skill wrapper | None for resolver | One canonical `SKILL.md`, host-neutral except declared tool vocabulary |
| Add-on manifest | Private `addon-manifest.json`; protocols, entry points, zero permissions | Public manifest copied identically into both projections |
| Optional host adapter | Deliberately outside L0 core | Remain owner-supplied and separately versioned; never bundled implicitly |
| Runtime state | Core requires none | No `.arcanum` route authority or mutable state required by the resolver |
| Bootstrap selection | Impossible | `--sigils intent-route-resolver` after canonical public sigil exists |
| Codex projection | Absent | `.agents/skills/intent-route-resolver/` |
| Claude projection | Absent | `.claude/skills/intent-route-resolver/` |
| Presence parity | Absent | Generated in one staged operation |
| Behavioral parity | Unproven | Same fixture corpus and canonical responses under both installed paths |
| Version provenance | Package/manifest say `0.1.0`; generated wrapper provenance has no version/digest | Pin core version, protocol majors, canonical source revision, and content digest |
| Authority | Installation grants none by design | Wrapper must preserve candidate-only semantics and host-owned approval/execution |

The executable package already exposes distinct core, JSON port, selected-local mapper, and manifest entry points ([package.json:7](cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/intent-route-resolver/package.json#L7)). Its manifest declares zero permissions and no side effects ([addon-manifest.json:20](cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/intent-route-resolver/addon-manifest.json#L20)). The design explicitly keeps runtime projection, decisions, approval, execution, persistence, and host adapters outside the L0 package ([INTEGRATION-VERSIONING.md:3](cyberAlchemy-v2/development/agent-reasoning-engine/intent-route-resolver/design/INTEGRATION-VERSIONING.md#L3), [INTEGRATION-VERSIONING.md:33](cyberAlchemy-v2/development/agent-reasoning-engine/intent-route-resolver/design/INTEGRATION-VERSIONING.md#L33)).

3. Behavior-parity constraint

Bootstrap rewrites generated frontmatter and, for Claude, maps only `Task → Agent` and `AskQuestions → AskUserQuestion` in `allowed-tools` ([bootstrap_arcanum.sh:1028](arcanum/tools/bootstrap_arcanum.sh#L1028)). Executable support bytes should therefore remain identical, but that fact must be verified.

Required parity claim:

- Identical executable files, manifest, schemas, and fixtures by digest.
- Equivalent wrapper semantics after normalizing the six generated provenance fields and the explicitly permitted Claude tool-token mapping.
- Byte-identical canonical resolver responses for every shared fixture.
- Identical failure classification for invalid version, malformed JSON, catalog digest mismatch, ambiguity, and no-match.
- No host SDK imports, external calls, approval, dispatch, or execution.

The existing validation contract already requires identical canonical Node/Chromium JSON responses and a zero-authority add-on boundary ([VALIDATION-CONTRACTS.md:13](cyberAlchemy-v2/development/agent-reasoning-engine/intent-route-resolver/design/VALIDATION-CONTRACTS.md#L13)).

4. Safe future fixture commands

After public extraction, against a disposable Git repository:

```bash
arcanum/tools/bootstrap_arcanum.sh \
  --target "$FIXTURE_REPO" \
  --sigils intent-route-resolver \
  --spells none \
  --profiles repo-codex,claude \
  --no-necronomicon
```

Expected:

- Both host package directories exist.
- Both contain `SKILL.md`, executable core, manifest, and fixtures.
- No Necronomicon state or route authority is created.
- Claude validation passes.
- Existing destinations cause refusal unless overwrite was explicitly admitted.

Selective preview:

```bash
arcanum/tools/sync-generated-skill-package.sh \
  --target "$FIXTURE_REPO" \
  --sigil intent-route-resolver \
  --profiles repo-codex,claude
```

Expected: preview only, no target mutation ([sync-generated-skill-package.sh:240](arcanum/tools/sync-generated-skill-package.sh#L240)).

Conformance:

```bash
node "$FIXTURE_REPO/.agents/skills/intent-route-resolver/package/test/run-conformance.mjs"
node "$FIXTURE_REPO/.claude/skills/intent-route-resolver/package/test/run-conformance.mjs"
```

Expected: equal canonical JSON output and equal exit classification for every positive and negative fixture.

Digest parity:

```bash
diff -ru \
  "$FIXTURE_REPO/.agents/skills/intent-route-resolver/package" \
  "$FIXTURE_REPO/.claude/skills/intent-route-resolver/package"
```

Expected: no differences in executable/support payloads. Compare `SKILL.md` separately with only declared generated metadata and Claude tool-token normalization permitted.

5. Provenance, overwrite, rollback

Current generated wrappers record runtime, canonical source, alias, generator, and regeneration policy ([bootstrap_arcanum.sh:795](arcanum/tools/bootstrap_arcanum.sh#L795)). Target provenance should additionally bind:

- resolver package version;
- add-on manifest version;
- supported protocol majors;
- canonical Arcanum commit or release;
- digest of executable/support closure;
- fixture-set digest.

Overwrite:

- Full Bootstrap refuses any existing generated destination unless `--force`.
- `--force` removes/replaces support directories individually; it is not transactionally atomic.
- Selective sync stages both profiles first, rejects symlink surfaces, snapshots existing destination packages, applies checksum-based sync, and restores prior package bytes if either application fails ([sync-generated-skill-package.sh:136](arcanum/tools/sync-generated-skill-package.sh#L136), [sync-generated-skill-package.sh:196](arcanum/tools/sync-generated-skill-package.sh#L196)).

Therefore the preferred update/rollback route is selective sync, not full forced Bootstrap. Durable rollback still requires a committed previous version or retained release artifact because selective-sync backups are temporary and deleted when the script exits.

6. Public/private extraction boundary

Safe candidate for extraction:

- generic canonical JSON utilities;
- request/catalog validation;
- eligibility and dominance logic;
- disposition resolver;
- JSON runtime port;
- generic protocol schemas;
- synthetic conformance fixtures;
- generic add-on manifest.

Requires explicit review or exclusion:

- `selected-local` compatibility mapper, because it names a private intent-record model;
- private catalog examples, authority vocabulary, design prose, receipts, and work-pack evidence;
- Augmentor and ResonantOS integration details;
- private paths, identifiers, or fixtures derived from DomainSpec/Saturn authority;
- any adapter that persists decisions or calls approval/execution owners.

The selected-local mapper is explicitly compatibility-only, not universal core input ([INTEGRATION-VERSIONING.md:21](cyberAlchemy-v2/development/agent-reasoning-engine/intent-route-resolver/design/INTEGRATION-VERSIONING.md#L21)). It should remain private or be generalized under a separately approved public contract.

7. Failure and residue model

Expected blockers:

- Unknown selector before canonical extraction.
- Existing destination without explicit overwrite approval.
- Invalid profile, non-root Git target, symlinked runtime surface, missing staged `SKILL.md`, or staged symlink.
- Claude skill validation failure.
- Cross-host fixture mismatch.
- Manifest/core version mismatch or unsupported major protocol.
- Any private-source leakage blocks publication.

Residual non-authority outputs after a successful future install:

- generated host skill packages;
- optional Bootstrap runtime/observability configuration if those profiles are separately selected;
- no decision, approval, execution, or mutable resolver state from the core itself.

The two existing generated Bootstrap wrappers demonstrate only generator presence parity: their canonical source and mutation policy match, while runtime differs as intended ([Codex wrapper:4](.agents/skills/arcanum-bootstrap/SKILL.md#L4), [Claude wrapper:4](.claude/skills/arcanum-bootstrap/SKILL.md#L4)). They do not prove resolver behavioral parity.

## Explorer: Simon, Herbert — Orchestrator Consumer Seam

dispatch_id: `2026-07-30-intent-router-bootstrap-runtime-integration`  
step_id: `s1`  
capability_ref: `research`  
capability_target: `dispatch-sheet.json`  
capability_mode: `explore`  
wave_id: `explore`  
write_scope: `[]`  
status: `completed`  
artifacts: `[]`  
validation:

- Read-only source inspection only; no processes, services, tests, writes, fetches, installs, or branch changes.
- Nested repository state bound at `7b98bf8edbfc0647934fabfa5c9158297837ea9c`, branch `master`, with `git status --short` empty at inspection.
- Mandatory nested policy read first: `AGENTS.md:1-9`.
- Compared the live Python host/runtime boundary with the private resolver’s request, disposition, JSON-port, selected-local mapping, manifest, and conformance tests.

observer_status: `not-invoked-read-only-research`  
blockers: `[]`  
residue:

- type: `authority-selection`
  statement: The resolver emits only `candidate`, `ambiguous`, `no-match`, or `invalid`; it never emits an authoritative `selected` result. A consumer contract for explicit operator selection remains to be defined outside the resolver.
- type: `normalization-owner`
  statement: No current orchestrator component owns construction of `intent-route.request@1` or selected-local mapping profiles.
- type: `catalog-authority`
  statement: The orchestrator has no bound owner/path for an effective capability-catalog snapshot.
- type: `transport-pinning`
  statement: A process adapter needs a pinned resolver package/ref, executable, timeout, byte ceiling, exit-code policy, and stderr policy before implementation.
- type: `persistence-schema`
  statement: No table/event currently records route request, disposition, clarification, or operator-selection evidence.
- type: `explicit-route-contract`
  statement: “Explicit route” precedence is an integration rule inferred from the resolver’s zero-authority contract, not a currently implemented typed artifact.

reroute: `none`  
handoff_note: Implement only after the owner accepts a separate authoritative selection artifact and catalog/normalization ownership. Keep the resolver package unchanged and keep dispatch/execution authority in the existing orchestrator runtime.

### Exact finding

The smallest future seam is a new, narrow **intent-route consumer adapter in the host pre-launch path**, invoked after a host request has been normalized into a resolver request but before `HostDispatchHook` chooses either:

1. the governed parent-workflow binding path, or
2. the existing compatibility-dispatch path.

The exact insertion point is `implementations/server/runtime/host_dispatch_hook.py:373-380`, before `_workflow_envelope()` currently determines the path. After authoritative route selection, the existing execution handoff remains `RuntimeService.bind_host_workflow_turn()` at `implementations/server/runtime/host_dispatch_hook.py:410-427`.

The adapter must not be added inside `RuntimeService.bind_host_workflow_turn()`. That service already owns confirmed Dispatch/group/seat validation, prompt and manifest integrity, follow-up targeting, persistence, lifecycle, and launch authorization. Putting routing there would mix advisory selection with execution authority.

### Selected, narrowed, and killed options

#### Selected: JSON-port contract with a process-bound transport adapter

Use the resolver’s existing canonical JSON port as the integration contract:

- request protocol: `intent-route.request@1`
- response protocol: `intent-route.runtime-port@1`
- disposition: `intent-route.disposition@1`

The adapter may launch a pinned local resolver process and exchange exactly one bounded JSON request/response. It owns only transport validation and mapping into a consumer decision. It must not inspect route predicates, rank candidates, repair malformed requests, synthesize missing discriminators, or choose among candidates.

Why this is the smallest honest seam:

- The orchestrator runtime is Python; the resolver is an ECMAScript module.
- The resolver already exposes an environment-neutral JSON port at `src/json-port.mjs:12-55`.
- The resolver manifest declares zero permissions and no side effects at `addon-manifest.json:20-22`.
- A thin process adapter avoids reimplementing resolver semantics in Python.

#### Narrowed: in-process library

Viable only if the consuming host itself becomes Node/ECMAScript or receives an already-loaded injected resolver callable. The library API is clean (`index.mjs:12-41`), but embedding it directly in the current Python runtime would require a JS engine or a new mixed-language composition layer. That is larger than the seam.

Do not port the resolver to Python. That would create a second resolver whose normalization, canonical JSON, eligibility, ambiguity, digest, and diagnostic behavior could drift.

#### Killed: generic process-bound “smart adapter”

Reject any process wrapper that:

- reads catalogs independently;
- retries with modified intent;
- converts ambiguity into a winner;
- falls back to keyword routing;
- schedules work;
- creates Dispatch records;
- issues capabilities; or
- treats a process exit code as route authority.

That becomes a second resolver/control plane.

### Integration sequence and exact fields

#### 1. Preserve explicit route precedence

Before calling the resolver, inspect a separately typed, human-originated route-selection artifact.

Required proposed fields:

```text
schema_version
selection_id
request_id
route_id
capability_ref
mode
owner_ref
selected_by
selection_evidence_ref
selection_evidence_digest
selected_at
catalog_id
catalog_digest
```

If valid and catalog-bound, this artifact bypasses advisory resolution. The adapter must still verify that the selected route identity agrees with the effective catalog snapshot; it must not reinterpret it.

A prompt string, inferred keyword, workflow marker, or resolver candidate is not an explicit route.

#### 2. Normalize intent outside the resolver consumer

Construct:

```text
schema_version = intent-route.request@1
request_id
intent:
  schema_version = routable-intent@1
  source_schema
  source_digest
  raw_intent
  discriminators:
    <key>:
      posture = declared | inferred | unresolved
      value
      evidence_refs
      inference_note
  constraints
catalog_snapshot
supersedes_request_id?
```

The resolver normalizes exact request fields and discriminator posture/evidence at private selectors:

- `src/request.mjs:8-12`
- `src/request.mjs:46-89`
- `src/request.mjs:91-150`
- `src/request.mjs:164-215`

If the source is a selected-local intent record, use the resolver’s mapping profile rather than recreating the mapping:

- source admission: `src/selected-local.mjs:106-175`
- mapping: `src/selected-local.mjs:267-309`

The orchestrator should persist the input bytes/digest as evidence, but normalization ownership must remain with the source-specific adapter/profile owner.

#### 3. Invoke the JSON port

Send canonical JSON and require:

```text
protocol_version = intent-route.runtime-port@1
request_id
disposition | null
transport_diagnostic | null
```

The port separates malformed transport/request failures from valid resolver dispositions at `src/json-port.mjs:18-55` and `src/json-port.mjs:58-88`.

#### 4. Verify, then consume by disposition

Verify:

- exact protocol version;
- response `request_id`;
- mutually exclusive `disposition` / `transport_diagnostic`;
- disposition `request_digest`;
- `catalog_id`;
- `catalog_digest`;
- `receipt_digest`;
- `authority_effect == "none"`.

Disposition fields are defined by `src/resolve.mjs:172-185`; receipt verification exists at `src/resolve.mjs:188-192`.

Consumption:

- `candidate`: retain as advisory evidence. Require an explicit human selection artifact before dispatch binding or compatibility Dispatch creation.
- `ambiguous`: surface exactly `ambiguity.reason_code`, `material_discriminators`, and `question`; do not launch. A human answer creates a new request with `supersedes_request_id` referring to the prior request.
- `no-match`: stop with a typed no-route result. Do not fall back to `_role()` keyword inference or auto-create a compatibility Dispatch.
- `invalid`: stop as an input/catalog validation failure.
- `transport_diagnostic != null`: stop as adapter/transport failure.

The resolver’s kinds and zero-authority effect are explicit at `src/resolve.mjs:137-185`. Clarification generation is at `src/resolve.mjs:74-100`.

#### 5. Continue through existing owners

Only after explicit selection:

- map selected route metadata to an already-confirmed parent Dispatch/group/seat;
- preserve the existing `ACI-WORKFLOW-BINDING-V1` envelope;
- call `RuntimeService.bind_host_workflow_turn()` unchanged;
- allow the hook/runtime to authorize or deny launch.

Existing envelope fields remain:

```text
schema
dispatch_id
group_id
seat_index
turn_ordinal
attempt_id
prompt_template_path
prompt_template_digest
workflow_manifest_path
workflow_manifest_digest
```

Source: `implementations/server/runtime/host_dispatch_hook.py:41-53`, parsed at `:267-295`.

### Owner matrix

| Concern | Retained owner |
|---|---|
| Source-specific intent capture and discriminator posture | Source adapter / selected-local mapping profile |
| Request normalization and canonical digest | Resolver request contract |
| Eligibility, dominance, ambiguity, no-match | Private intent-route resolver |
| Catalog authority and effective snapshot | Catalog owner, not orchestrator adapter |
| Explicit route choice and clarification answer | Human/operator authority |
| JSON transport, timeout, byte limits, protocol checking | New consumer adapter |
| Parent Dispatch, group, seat, prompt, and manifest binding | `RuntimeService.bind_host_workflow_turn()` |
| Launch authorization | Existing host hook plus runtime capability boundary |
| Scheduling/order/follow-up targeting | Existing orchestration runtime |
| Dispatch ledger authority | Existing validated appender/bridge |
| Turn persistence and idempotency | Runtime journal and `host_workflow_turn_bindings` |
| Terminal lifecycle | `complete_host_workflow_turn()` |
| Observability | Existing journal events/projections, extended with route-consumption events only |

### Retained execution and lifecycle invariants

The current runtime must retain:

- Repository-relative, non-symlink source binding and byte hashing: `service.py:5192-5218`.
- Exact workflow manifest identity, target, ordered slots, schemas, cardinality, source hashes, and byte ceilings: `service.py:5220-5359`.
- Open parent Dispatch and current link requirement: `service.py:5403-5416`.
- Declared group/seat requirement: `service.py:5417-5438`.
- Spawn prompt equality and digest binding: `service.py:5439-5449`.
- Follow-up template and prior-terminal-agent targeting: `service.py:5450-5492`.
- Stable binding identity and divergent-retry rejection: `service.py:5516-5566`.
- Terminal states `resolved | error | cancelled`: `service.py:5678-5761`.
- Persisted state constraints and uniqueness: `migrations/009_host_workflow_binding.sql:1-30`.
- Dispatch cannot close while a bound turn is running: `service.py:1389-1406`.

### Lifecycle and error mapping

| Resolver/adapter condition | Consumer lifecycle | Runtime/error mapping |
|---|---|---|
| Valid candidate, no human selection | `awaiting-selection` | Gate-blocked; no runtime binding |
| Ambiguous | `awaiting-clarification` | Gate-blocked; preserve question and candidates |
| Clarification answered | new request superseding old | Re-run resolver; old request remains immutable |
| No-match | `no-route` terminal | Validation/domain outcome, no launch |
| Invalid disposition | `invalid` terminal | `VALIDATION_ERROR` or `READ_INTEGRITY_FAILURE`, based on request versus digest/catalog corruption |
| Transport invalid JSON/version | `adapter-error` terminal | `VALIDATION_ERROR` |
| Process timeout/nonzero/unavailable | `adapter-error` terminal | `LOCAL_PILOT_SERVE_BLOCKED`; no fallback |
| Digest/request/catalog mismatch | `integrity-error` terminal | `READ_INTEGRITY_FAILURE` |
| Explicit selection conflicts with catalog | `selection-conflict` terminal | `CONFLICT` |
| Selection principal/evidence unauthorized | `selection-denied` terminal | `AUTHORIZATION_DENIED` |
| Selected and runtime binding succeeds | `launch-authorized` | Existing runtime receipt |
| Bound host call succeeds/fails/aborts | `resolved/error/cancelled` | Existing terminal event |

Existing closed runtime vocabulary is at `implementations/server/runtime/errors.py:4-37`. The hook already maps host completion/error/abort to `resolved/error/cancelled` at `host_dispatch_hook.py:528-559`.

### Persistence and observability extension

Add future route evidence without changing dispatch ownership:

1. Immutable route request artifact: canonical request bytes and digest.
2. Immutable port response artifact: canonical response bytes and digest.
3. Optional explicit selection artifact.
4. Journal events, suggested names:

```text
intent_route.requested@1
intent_route.disposition_recorded@1
intent_route.clarification_requested@1
intent_route.selection_recorded@1
```

Each event should carry IDs/digests, not duplicate full resolver logic. No event should itself authorize execution. The existing host binding event remains the first launch-authorizing runtime transition (`service.py:89-90`, `:163-168`).

### Migration slices

1. **Contract-only slice:** define consumer input/output, explicit-selection artifact, lifecycle states, error map, and process constraints. No launch integration.
2. **Adapter conformance slice:** implement a deterministic injected fake plus JSON-port subprocess adapter; record request/response evidence only.
3. **Advisory shadow slice:** call resolver for eligible host requests but never affect launch; compare recorded outcomes.
4. **Clarification gate slice:** block ambiguous/no-match/invalid cases; allow explicit route bypass.
5. **Selection-to-binding slice:** require an explicit selection artifact before entering the existing governed workflow binding.
6. **Compatibility-path retirement slice:** only after fixture parity, disable `_role()`/automatic compatibility Dispatch fallback for intent-routed requests. Do not remove the compatibility path globally without a separate decision.

### Required validation fixtures

- Exact selected-local mapping preserves posture, evidence, inference note, source digest, and unmapped fields.
- Explicit human route bypasses resolver but is rejected when catalog digest or route identity differs.
- One candidate remains advisory and cannot launch without selection.
- Ambiguous disposition exposes the resolver’s exact question and launches nothing.
- Clarification response produces a distinct request with `supersedes_request_id`.
- No-match never reaches `_opening_record()`, appender, journal dispatch open, or host spawn.
- Invalid request and malformed JSON preserve typed diagnostics with no stack leakage.
- Resolver timeout, nonzero exit, oversized stdout/stderr, extra output, or unsupported protocol fail closed.
- Request ID, request digest, catalog ID/digest, receipt digest, and authority effect mismatch fail integrity checks.
- Selected route maps only to a declared open parent Dispatch/group/seat.
- Spawn/follow-up prompt and workflow-manifest invariants remain unchanged.
- Divergent retry remains an idempotency conflict.
- Running binding still prevents parent close.
- Terminal host results retain `resolved/error/cancelled`.
- Assert the adapter contains no route predicates, rankings, keyword routing, scheduler calls, appender calls, or capability issuance.

Existing evidence patterns:

- JSON-port typed diagnostics: private `test/json-port.test.mjs:59-113`.
- Selected-local preservation and no guessing: private `test/selected-local.test.mjs:67-107`.
- Zero-permission/environment-neutral package: private `test/selected-local.test.mjs:110-159`.
- Parent workflow binding/idempotency/close gate/follow-up/output integrity: `implementations/tests/runtime/test_host_workflow_binding.py:245-427`.
- Hook-bound launch without another YAML Dispatch and unbound-follow-up denial: `implementations/tests/runtime/test_host_dispatch_hook.py:125-173`.

### Kill criteria

Kill or redesign the integration if any implementation:

- treats `candidate` as authorization;
- chooses among ambiguous candidates;
- guesses unresolved discriminator values;
- lets no-match fall through to keyword role inference;
- duplicates catalog predicates or resolver ranking in Python;
- mutates the resolver request/result;
- accepts noncanonical or unverifiable response evidence;
- changes dispatch, scheduling, capability, or execution ownership;
- creates a second ledger/appender path;
- bypasses the confirmed parent Dispatch/group/seat;
- weakens prompt/manifest hashing or follow-up target checks;
- launches on adapter timeout/error;
- requires network access;
- makes the resolver a daemon or policy authority;
- claims full provider effective-input capture;
- cannot replay the exact request, catalog, response, and human selection from persisted digests.

The essential boundary is: **the resolver proposes; a human selects; the existing orchestrator binds, authorizes, dispatches, persists, and closes.**

## Explorer: Ashby, W. Ross — Reasoning-Engine Layer

```json
{
  "dispatch_id": "2026-07-30-intent-router-bootstrap-runtime-integration",
  "step_id": "s1",
  "capability_ref": "research",
  "capability_target": "dispatch-sheet.json",
  "capability_mode": "explore",
  "wave_id": "explore",
  "write_scope": [],
  "status": "pass",
  "artifacts": [],
  "validation": {
    "command": "node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/intent-route-resolver/test/*.test.mjs",
    "result": "pass",
    "tests": 34,
    "failures": 0,
    "duration_ms": 592,
    "scope": "standalone package only",
    "historical_witness": "aggregate Node/Chromium receipt PASS"
  },
  "observer_status": "not-invoked",
  "blockers": [],
  "residue": [
    "No concrete consumer runtime installs or invokes the resolver.",
    "The live capability-catalog compiler and admitted registry source are deferred.",
    "Natural-language intent projection quality is outside the witness.",
    "Host RouteDecision persistence, approval, execution, actor protocol, memory, and effects are absent.",
    "ACI-subordinate conformance remains separately planned and unwitnessed.",
    "The resolver does not satisfy the minimum reasoning-engine witness because its executable relation selects routes rather than deriving or evaluating an object-level conclusion."
  ],
  "reroute": "Define and plan one concrete ACI-subordinate consumer integration, preserving the resolver as a non-authorizing pre-inference adapter; separately retain semantic-judgment-evaluator@1 as the object-level evaluator slice.",
  "handoff_note": "The package is a working private standalone L0 resolver, not a runtime-integrated cyberAlchemy-v2 reasoning engine. Treat its candidate output as advisory control information only."
}
```

### Direct answer

**Does the standalone resolver work as part of cyberAlchemy-v2?**

- **Yes, narrowly:** it exists inside the private `cyberAlchemy-v2` implementation tree, its complete standalone suite passes live, and its recorded Node/Chromium witness passes.
- **No, if “as part of” means runtime-integrated:** no Agent Reasoning Engine, ACI, Augmentor, ResonantOS, or other concrete consumer currently supplies its production catalog, calls its port, persists its decision, or carries its result into semantic evaluation.
- Therefore the exact classification is: **working standalone private L0 pre-inference control/reasoning-support adapter; not yet an integrated reasoning-engine component and not the whole engine.**

### Strongest proof-backed claim

The resolver deterministically transforms a machine-readable typed intent envelope plus a frozen owner-supplied route catalog into a canonical, digest-bound, non-authorizing `candidate`, `ambiguous`, `no-match`, or `invalid` disposition. It exposes complete per-route predicate traces, fails closed on unresolved or invalid input, uses only explicit catalog dominance, and has passing Node/Chromium conformance.

This advances the reasoning architecture by making the **front-door capability-selection boundary** explicit and reproducible before an engine run. It does not advance object-level semantic derivation itself.

### Minimum reasoning-engine witness

| Requirement | Result | Reason |
|---|---|---|
| Machine-readable epistemic input | Pass, bounded | Typed intent discriminators carry declared/inferred/unresolved posture and evidence references. |
| Executable object-level inference/evaluation | **Fail** | Executed predicates answer “which capability route is eligible?”, not “what conclusion follows from observations and rules?” |
| Traceable derived output | Pass, bounded | Every disposition includes evaluated-route traces, reasons, input/catalog digests, and a receipt digest. |

The route resolver therefore fails the minimum witness as a reasoning engine even though it performs genuine deterministic computation. Its computation is **meta-level routing**, not object-level semantic judgment.

By comparison, `semantic-judgment-evaluator@1` consumes admitted observations and finite rules, evaluates applicability/defeat/challenge state, and derives a typed semantic outcome. That is the bounded object-level evaluator slice, although its own contract explicitly denies that it is a whole engine.

### Layer map

| Concern | State | Exact interpretation |
|---|---|---|
| Intention normalization | Partial/current | Generic validation and canonicalization are implemented; selected-local mapping preserves posture/evidence. Natural-language projection and universal IntentRecord fitness are absent. |
| Eligibility | Current | Required predicates and exclusions are evaluated deterministically; exclusions take precedence. |
| Candidate ranking | Current, narrowly | Explicit acyclic dominance reduction exists. There is no similarity score, confidence rank, learned ranking, or fallback. |
| Ambiguity | Current | Multiple non-dominated routes or material unresolved discriminators produce one stable clarification question. |
| Abstention | Current as routing abstention only | `ambiguous`, `no-match`, and `invalid` prevent guessed routing. They are not semantic `Deferred.Insufficient` judgments. |
| Semantic judgment | Absent | Explicitly out of resolver scope and retained by the semantic evaluator. |
| Object-level inference/evaluation | Absent | Route predicates evaluate catalog eligibility, not domain conclusions from observations. |
| Actor protocol | Absent | No commands, events, joins, retries, timeouts, or actor lifecycle. |
| Memory/replay | Absent | No runtime journal, durable memory, or historical/current-state replay semantics. Deterministic re-execution is not engine replay. |
| Effects | Absent by design | `authority_effect: none`; zero effect, dispatch, persistence, and external calls. |
| Observability | Partial | Full evaluated-route trace, reason codes, digests, witness receipts, and zero-call audit exist; integrated runtime telemetry/journaling does not. |
| Evidence | Current, bounded L0 | Live 34-test pass plus recorded 17-case Node/Chromium parity witness. No product or production evidence. |
| ACI | Deferred/unintegrated | The parent architecture selected ACI-subordinate ownership, but this resolver has no executable ACI binding or conformance witness. |

### Exact selectors

- Standalone objective and non-authorizing relation: `intent-route-resolver/define/SPEC.md:10-22`.
- Runtime-neutral expected boundary and retained neighboring responsibilities: `define/SPEC.md:24-42`.
- Semantic evaluation, execution, persistence, discovery, and public Arcanum explicitly excluded: `define/SPEC.md:64-73`.
- Ownership separation from semantic evaluator, dispatch, orchestration, Augmentor, and host: `define/SPEC.md:75-85`.
- Typed epistemic posture and evidence fields: `define/SPEC.md:87-113`.
- Four-outcome algebra: `define/SPEC.md:155-165`.
- Deterministic eligibility, ambiguity, dominance, and no-score rules: `define/SPEC.md:167-183`.
- Runtime sequence showing later user decision, host persistence, approval, and execution: `define/SPEC.md:214-230`.
- Open integration and product-evidence ceiling: `define/SPEC.md:248-258`.
- Pure component layering and prohibited calls: `design/ARCHITECTURE.md:47-75`.
- Implemented predicate evaluation and unresolved handling: `src/eligibility.mjs:11-33`.
- Eligibility, conditionality, explicit dominance, and complete trace assembly: `src/eligibility.mjs:35-114`.
- Canonical non-authorizing disposition and trace digest: `src/resolve.mjs:19-42`, `src/resolve.mjs:103-192`.
- Ambiguity construction: `src/resolve.mjs:61-101`.
- Selected-local missing mappings remain unresolved: `src/selected-local.mjs:267-309`.
- Zero-permission, no-side-effect add-on surface: `addon-manifest.json:1-22`.
- Completed standalone L0 frontier and deferred integration owners: `planning/WORK-PACK.md:29-41`, `planning/WORK-PACK.md:128-140`, `planning/WORK-PACK.md:169-177`.
- Recorded witness ceiling: `generated/runs/intent-route-resolver-v1-20260730T213000Z/receipt.json:17-30`.
- Node zero-call/import audit: `generated/runs/intent-route-resolver-v1-20260730T213000Z/node-receipt.json:64-90`.
- Chromium byte parity: `generated/runs/intent-route-resolver-v1-20260730T213000Z/browser-receipt.json:1-17`.
- Parent whole-engine boundary and non-promotion: `agent-reasoning-engine/spec/SPEC.md:15-31`.
- Parent engine pipeline placing semantic evaluation after actor observations: `agent-reasoning-engine/spec/SPEC.md:127-178`.
- Parent whole-engine responsibilities absent here: `agent-reasoning-engine/spec/SPEC.md:287-302`.
- Semantic evaluator’s object-level fact/rule comparison: `semantic-judgment-evaluator/src/reducer.mjs:113-157`, `semantic-judgment-evaluator/src/reducer.mjs:202-280`.
- ACI-subordinate decision and non-integration ceiling: `decisions/aci-reasoning-binding/DECISION.md:33-38`, `decisions/aci-reasoning-binding/DECISION.md:57-67`.

### Counterexamples preventing a broader claim

1. A `candidate` result still has `authority_effect: none`; it cannot approve or execute the route.
2. Passing literal route fixtures does not show that natural-language intent was projected correctly.
3. Canonical replay of the pure function is not a RuntimeJournal with commands, attempts, joins, timeouts, and current-state revalidation.
4. Predicate matching over route metadata is not semantic reduction over provenance-bearing observations and governed domain rules.
5. Browser parity proves portable execution of the package, not Augmentor, ResonantOS, ACI, or Agent Reasoning Engine acceptance.
6. Repository location beneath `implementation/agent-reasoning-engine` does not itself prove architectural integration.

### Public/private boundary

The potentially project-agnostic surface is the abstract JSON relation:

`typed routable intent + frozen finite route catalog -> non-authorizing route disposition`

Its portable ideas are typed uncertainty, explicit exclusions, owner-declared dominance, ambiguity instead of guessing, canonical receipts, and zero permissions.

However, the current package, selected-local compatibility mapper, CAV2 authority references, Agent Reasoning Engine contracts, ACI disposition, and consumer assumptions are private. There is presently **no public Arcanum contract or publication claim**. Any future public extraction must define a fresh project-agnostic contract and reference private authority by stable identifiers where permitted; it must not copy private CAV2/DomainSpec prose or treat this private witness as public promotion.

### Validation implications

The standalone implementation is sufficiently evidenced for isolated reuse experiments. Integration acceptance still requires a separate bounded work-pack proving:

- admitted live catalog ownership and compilation;
- concrete consumer invocation through the JSON port;
- immutable decision persistence and correction/supersession;
- explicit handoff from route disposition to the engine’s entry gate and semantic evaluator;
- ACI-owned command/event identity, journal, replay cursor, and effect-intent conformance;
- unchanged `authority_effect: none` across the resolver boundary;
- negative tests showing that candidate selection cannot bypass semantic evaluation, approval, or exact-effect gating.
