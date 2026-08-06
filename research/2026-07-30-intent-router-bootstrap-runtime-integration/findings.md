# Findings — Intent Router Bootstrap and Runtime Integration

dispatch_id: `2026-07-30-intent-router-bootstrap-runtime-integration`

## Direct answer

The existing intent-route resolver is real and tested, but only as a private
standalone package. Its bounded witness is 34 passing tests with 0 failures.
It is not currently selectable by Arcanum Bootstrap, generated for Claude or
Codex, installed in a consumer, connected to the orchestrator, or integrated
with the wider reasoning stack.

The current direct Bootstrap topology is **killed**. Bootstrap selects
canonical Arcanum sigils or spells, and no canonical public
`intent-route-resolver` exists.

A fresh, generic, zero-authority public extraction is **selected as a future
topology**, but it is unauthorized and unimplemented. The private package must
not simply be copied into public Arcanum. Extraction, canonical acceptance,
generated-package promotion, release, consumer installation, deployment, and
private reasoning-stack admission are separate decisions.

The resolver advances only the reproducible **pre-inference capability-routing
boundary**. It does not provide semantic judgment, object-level inference,
actor protocol, memory, effects, or a whole reasoning engine.

Exact current-evidence selectors:

- **Private standalone witness:** package
  `cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/intent-route-resolver/`;
  command
  `node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/intent-route-resolver/test/*.test.mjs`;
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/research.md:88-90`;
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/research.md:579-598`;
  and
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/receipts/explorer-reasoning-layer.json`.
- **Current Bootstrap selector limitation:**
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/research.md:49-53`
  and
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/receipts/explorer-bootstrap-runtime.json`.
- **Future orchestrator seam:**
  `projects/cyberalchemy-orchestrator/implementations/server/runtime/host_dispatch_hook.py:373-380`
  for the thin pre-`_workflow_envelope()` adapter seam;
  `projects/cyberalchemy-orchestrator/implementations/server/runtime/host_dispatch_hook.py:410-427`
  for the existing binding/launch owner;
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/research.md:233-278`;
  and
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/receipts/explorer-orchestrator-seam.json`.
- **Reasoning-layer boundary:**
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/research.md:612-643`,
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/synthesis-revised.md:253-271`,
  and
  `research/2026-07-30-intent-router-bootstrap-runtime-integration/receipts/explorer-reasoning-layer.json`.

## Closed verdicts and lifecycle labels

| Question | Verdict | Lifecycle label |
|---|---|---|
| Is the private resolver working? | Yes, as a tested private standalone package only. | **CURRENT / BOUNDED** |
| Can Bootstrap select it today? | No. There is no canonical public resolver selector target. | **KILLED / CURRENT TOPOLOGY** |
| Can a resolver become a Bootstrap-installed add-on later? | Yes in principle, but only as a fresh public, generic, zero-authority sigil after extraction and canonical acceptance. Bootstrap remains installer/projector, not resolver. | **SELECTED / FUTURE** |
| Do Claude and Codex have equivalent integrations now? | No. Both packages are absent. Presence parity is feasible; behavior parity is unwitnessed. | **DEFERRED / FUTURE ACCEPTANCE** |
| Is the parity design mechanically closed? | Yes. The commands, cases, schemas, exits, byte limits, timeout, rollback, and counters are frozen as future design. | **GO / DESIGN ONLY** |
| Is there a current orchestrator adapter? | No. A thin pre-launch process adapter is selected for later work. | **SELECTED / FUTURE, CURRENTLY ABSENT** |
| May resolver output authorize work? | No. It is advisory and always has `authority_effect: none`. | **FAIL-CLOSED OWNER BOUNDARY** |
| Are catalog, normalization, and ACI artifact owners bound? | No. Implementation remains blocked until they are bound. | **DEFERRED / OWNER DECISIONS** |
| Is it part of `cyberAlchemy-v2`? | Yes only as code in the private reasoning-engine implementation tree; no runtime consumer invokes it. | **CURRENT COMPONENT / INTEGRATION DEFERRED** |
| Does it advance the reasoning engine? | Only at deterministic pre-inference route reduction and abstention. | **NARROW ADVANCE / CLAIM CEILING** |
| Can Augmentor or another runtime use it? | A runtime-owned adapter may form requests or consume dispositions without transferring authority. | **ADAPTER COMPATIBLE / ZERO AUTHORITY TRANSFER** |

The three final reviews are `GO`: ownership has no duplicate selection,
Dispatch, registry, or ACI lifecycle owner; evidence and authority constructs
remain non-substitutable; and the future acceptance design is mechanically
non-vacuous. These review results do not establish implementation or runtime
evidence.

## Selected and killed topology

Selected future topology:

```text
source-specific intent capture (Augmentor, Claude, Codex, or another host)
    -> typed intent-route.request@1
    -> digest-bound read-only route-catalog projection
    -> generic zero-authority intent-route resolver
    -> candidate | ambiguous | no-match | invalid
    -> human clarification or confirmation
    -> existing canonical Dispatch/group/seat
    -> existing host binding, authorization, execution, persistence, effects
```

If separately authorized, the generic resolver may become public canonical
Arcanum source. Bootstrap could then project the same closure into thin Claude
and Codex packages. Private `cyberAlchemy-v2` and orchestrator adapters could
depend on that public contract while private CAV2, DomainSpec, Saturn, ACI,
Augmentor, ResonantOS, and reasoning-engine prose and authority remain private.

Killed:

- direct installation or copying of the current private package into public
  Arcanum;
- Bootstrap as semantic resolver;
- a generic Bootstrap package selector for this scope;
- resolver or adapter ownership of a catalog registry, approval, selection,
  scheduling, execution, persistence, replay, rollback, or effects;
- a standalone `selection_id`, selection table, or parallel
  `awaiting-selection` lifecycle;
- a Python resolver or smart adapter that repairs intent, enriches policy,
  ranks routes, chooses ambiguity, retries semantically, or falls back to
  keyword routing;
- Augmentor as resolver, approval owner, or executor;
- public copying of private CAV2, DomainSpec, Saturn, ACI, Augmentor, or
  ResonantOS authority;
- claims of current integration, promotion, public release, installation,
  deployment, production readiness, object-level semantic evaluation, or a
  whole reasoning engine.

## Expected end state

The bounded target, if each future gate is separately approved and passed, is:

1. A fresh, reviewed project-agnostic resolver core, JSON port, protocol
   schemas, zero-authority manifest, synthetic fixtures, and thin canonical
   wrapper are accepted under an Arcanum sigil.
2. Bootstrap generates
   `.agents/skills/intent-route-resolver/` and
   `.claude/skills/intent-route-resolver/` from one canonical closure.
3. A frozen route catalog is projected read-only from explicitly bound
   canonical capability owners and confirmed Dispatch owners. It is
   digest-bound and is never a registry, ledger, or independent authority.
4. A thin adapter projects or rejects inputs and validates transport. It does
   not repair, enrich, rank, select, schedule, approve, persist independently,
   or execute.
5. Request and disposition bytes are retained only as content-addressed ACI
   artifacts referenced by ACI-owned command/event records. There is no
   resolver database, adapter ledger, or second replay/rollback path.
6. Human choice is embodied by confirmation or authorship of the existing
   canonical Dispatch/group/seat. Only that confirmed binding can cross the
   host workflow-binding seam.
7. Private `cyberAlchemy-v2` references the generic contract only at entry
   routing. Private ACI, semantic judgment, actor protocol, memory, effects,
   evidence admission, and promotion authority remain private and separately
   owned.

This is an expected end state, not a description of current software.

## Ownership map

| Concern | Retained owner | Resolver or adapter boundary |
|---|---|---|
| Public extraction permission and scope | Private source owner plus proposed public maintainer | Cannot extract without explicit authority. |
| Canonical Arcanum source | Public Arcanum authority | Extraction does not imply canonical acceptance. |
| Bootstrap generation | Bootstrap/runtime package owner | Projects accepted source; gains no semantic authority. |
| Intent capture | Augmentor, Claude, Codex, or another source host | Source adapter may construct `intent-route.request@1`; normalization owner is not yet bound. |
| Capability and Dispatch source data | Named canonical capability and confirmed Dispatch owners | Catalog projector may project or reject only. |
| Route catalog compilation | Future explicitly named projector owner/path | No identity creation, repair, enrichment, ranking, registry, or ledger. |
| Route disposition | Generic resolver | Emits only non-authorizing advice with `authority_effect: none`. |
| Human choice | Human through the existing canonical Dispatch/group/seat owner | No parallel selection object or lifecycle. |
| Request/disposition retention | ACI and its existing journal | Content-addressed references only; no adapter persistence. |
| Workflow binding and launch | Existing orchestrator runtime, including `RuntimeService.bind_host_workflow_turn()` | Adapter cannot bind, authorize, schedule, or launch. |
| Authorization | Existing authorization owner | A valid binding does not authorize execution. |
| Execution and effects | Existing host runtime | An attempt does not prove an effect. |
| Completion evidence | Existing observation and receipt owners | An observed effect without its required receipt does not prove governed completion. |
| Private reasoning-stack admission | Private `cyberAlchemy-v2` authority | Public extraction conveys no private admission or promotion. |

## Standalone resolver and adapter contract

The current private package proves a standalone resolver shape, not an
integration. A future public contract must be freshly extracted and must retain
the following stable boundary.

Request selector:

```text
schema_version = intent-route.request@1
request_id
intent/discriminators with declared|inferred|unresolved posture
support_evidence_refs[]
catalog_id
catalog_digest
supersedes_request_id?
```

Catalog selector:

```text
schema_version
catalog_id
catalog_digest
derived_from[] = canonical owner identifiers, revisions, and content digests
routes[] = read-only projected capability and confirmed Dispatch bindings
```

Disposition selector:

```text
schema_version = intent-route.runtime-port@1
disposition_schema = intent-route.disposition@1
kind = candidate | ambiguous | no-match | invalid
request_id/request_digest
catalog_id/catalog_digest
evaluated_route_traces
reason_codes
clarification?
candidate_route_identity?
receipt_digest
authority_effect = none
```

`receipt_digest` retains its current wire name but means only **disposition
integrity digest**. It is not support evidence, confidence, approval, a
reasoning receipt, a lifecycle receipt, or authority evidence.

The future standalone process adapter is transport and integrity glue only. It
may:

- invoke one pinned local JSON-port process;
- project or reject source input into `intent-route.request@1`;
- validate request size, stdout size, zero-stderr policy, timeout, protocols,
  versions, catalog and closure digests, result shape, and
  `authority_effect: none`;
- return a trusted non-authorizing disposition or a typed rejection.

It may not:

- repair, infer, enrich, rank, select, or semantically retry;
- open or append a Dispatch;
- synthesize an ACI `dispatch-open`;
- invoke compatibility fallback;
- approve, authorize, schedule, persist independently, execute, or claim
  effects.

Support evidence, disposition integrity, reasoning/lifecycle receipts, and
authority evidence are distinct. None upgrades confidence or authority merely
by existing.

## Bootstrap and Claude/Codex parity contract

Bootstrap can provide **presence parity** only after a canonical public sigil
exists. It would select one canonical closure and generate both runtime
packages. No such resolver package exists under either runtime surface today.

Future behavior parity requires:

- byte-identical core, manifest, schemas, fixtures, executable support closure,
  and closure digest;
- the declared JSON entry point under both generated packages;
- identical normalized fixture outcomes, result kinds, reason codes,
  `authority_effect`, target exits, stdout documents and bytes, stderr bytes,
  disable behavior, and durable rollback result;
- identical zero-authority behavior: neither wrapper may confirm a Dispatch,
  authorize, schedule, execute, persist effects, or report effects;
- per-case Claude canonical response bytes equal to the corresponding Codex
  response bytes.

Only generated provenance fields and the declared Claude tool-token
normalization (`Task` to `Agent`, `AskQuestions` to `AskUserQuestion`) may
differ in wrapper source. Those admitted source differences may not change
semantics.

Lifecycle behavior is also future-only:

- **Select/install:** select a canonical sigil; generation grants no semantic
  authority.
- **Update:** stage both profiles, reject symlinks, and compare checksums.
- **Disable:** a consumer-owned gate prevents invocation without erasing ACI
  artifacts, mutating the catalog, or changing Dispatch lifecycle.
- **Rollback:** reinstall a pinned prior public release into a fresh `mkdtemp`
  root and verify its expected closure digest. Temporary selective-sync backups
  are not durable rollback, and full Bootstrap `--force` is not transactional.
- **Provenance:** bind canonical commit/release, core and manifest versions,
  request/port/disposition protocol majors, executable/support digest, fixture
  digest, and generator identity.

This parity contract is **DEFERRED / FUTURE ACCEPTANCE** and **GO / DESIGN
ONLY**. No runner, fixture result, generated package, release archive, or parity
witness currently exists.

## Orchestrator seam

The selected future seam is a thin process-bound JSON adapter in
`projects/cyberalchemy-orchestrator` before `_workflow_envelope()` chooses the
host binding path. Existing `RuntimeService.bind_host_workflow_turn()` remains
the governed binding/launch owner only. Authorization, persistence, lifecycle,
effects, and receipts remain with their separately retained owners.

The required sequence is:

1. A source adapter constructs `intent-route.request@1`; its normalization
   owner must first be bound.
2. The catalog projector reads named canonical capability and confirmed
   Dispatch sources and emits or rejects a frozen digest-bound projection.
3. The thin adapter invokes the pinned local JSON port and validates transport,
   protocols, versions, digests, limits, and `authority_effect: none`.
4. ACI references request and disposition as content-addressed artifacts in
   ACI-owned command/event records.
5. `candidate` is advisory evidence for a human. `ambiguous`, `no-match`, and
   `invalid` do not cross the workflow-binding seam.
6. A human confirms or authors the existing canonical Dispatch/group/seat.
7. Only that confirmed canonical Dispatch/group/seat may enter
   `RuntimeService.bind_host_workflow_turn()`.
8. Existing owners separately validate binding, authorize execution, attempt
   execution, observe effects, and record terminal evidence.

Human confirmation, Dispatch binding, authorization, execution attempt,
observed effect, and required receipt are non-substitutable and independently
fail closed.

Across all 78 future acceptance IDs:

```text
dispatch_open_or_appender_calls = 0
aci_journal_dispatch_open_calls = 0
compatibility_fallback_calls = 0
```

`workflow_bind_calls=1` only for `A02`, `A25`, `A26`, and `A27`.
`host_spawn_calls=1` only for `A02`, `A26`, and `A27`.

No current adapter, request normalizer, bound catalog owner, ACI artifact
binding, or consumer witness exists.

## Relationship to `cyberAlchemy-v2`

The existing package lives under the private
`cyberAlchemy-v2` Agent Reasoning Engine implementation tree. That establishes
a repository/component relationship only. It does not establish that ACI,
Augmentor, ResonantOS, the orchestrator, the semantic judgment evaluator, or
the wider reasoning stack installs or invokes it.

The future relationship is subordinate and narrow:

- public Arcanum may own a fresh generic entry-routing contract after explicit
  extraction and canonical acceptance;
- private `cyberAlchemy-v2` may reference that generic contract at its entry
  boundary after a separate private admission decision;
- ACI remains the private reasoning/lifecycle integration owner;
- semantic judgment remains a distinct later layer;
- actor protocol, memory, effects, evidence admission, and promotion remain
  private and outside the resolver.

No private prose, vocabulary, fixture, catalog, policy, or authority may be
copied into public Arcanum.

## Reasoning-engine layer verdict

| Reasoning layer | Verdict |
|---|---|
| Intention normalization | Partial |
| Eligibility/exclusion | Current |
| Explicit dominance/candidate reduction | Current, narrow |
| Ambiguity/routing abstention | Current |
| Semantic judgment | Absent |
| Object-level inference | Absent |
| Actor protocol | Absent |
| Memory/replay | Absent |
| Effects | Absent by design |
| Observability | Partial standalone trace |
| ACI integration | Deferred/unwitnessed |

The maximum current claim is:

> A tested private standalone L0 pre-inference resolver/component with a
> transport-neutral JSON surface that deterministically produces
> non-authorizing dispositions.

It is not currently public, integrated, promoted, released, installed,
deployed, production-ready, an object-level semantic evaluator, or a whole
reasoning engine.

## Augmentor and other runtimes

Augmentor, Claude, Codex, or another runtime can later own a source-specific
adapter that captures intent, constructs a typed request, or renders a
disposition. Augmentor remains capture, projection, and interaction owner. The
host remains confirmation, canonical Dispatch, binding, authorization,
execution, persistence, observation, effects, and receipt owner.

Using the resolver does not transfer authority to or from Augmentor or another
runtime. A runtime adapter cannot become the resolver, repair its result,
approve a route, open a Dispatch, execute work, or treat candidate evidence as
authoritative selection.

## Ordered project path

1. Obtain the human extraction and public-boundary decision.
2. Bind exact canonical capability sources, confirmed Dispatch sources,
   catalog projector owner/path, request-normalization owner, and ACI artifact
   reference fields.
3. Author the future public contract with candidate terminology, evidence
   distinctions, provenance, disable, and rollback rules.
4. Produce a reviewed generic extraction candidate and private-boundary scan.
5. Separately accept the candidate as canonical Arcanum source.
6. Implement the canonical runner and synthetic fixtures.
7. Generate disposable Claude and Codex packages from the same closure.
8. Prove presence, digest, behavior, negative, disable, and rollback parity.
9. Separately promote the generated packages.
10. Separately publish a pinned release.
11. Install the pinned release into a disposable consumer and prove local
    acceptance.
12. Implement the orchestrator adapter with injected failures and
    content-addressed ACI artifact references only.
13. Run the adapter in advisory shadow mode without changing launch behavior.
14. Admit only a confirmed canonical Dispatch/group/seat across the binding
    seam.
15. Prove that selection, binding, authorization, attempt, effect, and receipt
    cannot substitute for one another.
16. Add an ACI-subordinate private `cyberAlchemy-v2` entry-routing witness and a
    distinct handoff to semantic evaluation.
17. Consider compatibility-fallback retirement only under a separate decision.

Each authority transition remains independent:

```text
extraction candidate
    != canonical source acceptance
    != generated-package promotion
    != published release
    != consumer installation
    != deployment
    != production readiness
```

## Executable future validation plan

Everything in this section is exact **future contract design and non-evidence**.
The named paths, runners, fixtures, archives, and outputs do not currently
exist as accepted witnesses.

### Normative exact-contract binding

The normative future acceptance contract is the current byte sequence at:

```text
research/2026-07-30-intent-router-bootstrap-runtime-integration/acceptance-contract-addendum.md
SHA-256 ae914daf71331ddc787d8b562d78ceddabd10ad2526b568de07ecd92f2707e94
```

This findings section normatively incorporates, by that path and digest, the
addendum's following complete sections:

- `## 1. Frozen constants and sentinel rules`;
- `## 2. Required fixture-manifest fields`;
- section 3's machine schema `intent-route.acceptance-case@1`, including
  `### Top-level fields` and the exact `expected` and `observed` object-shape
  subsection;
- section 4's machine schema `intent-route.acceptance-summary@1`;
- `## 5. Exact future commands`;
- `## 6. Complete scalar case mapping`, including the JSON-port, public-core,
  Codex/Claude wrapper, and orchestrator-adapter case tables;
- `## 7. Seam and zero-call invariant`.

Those digest-bound sections control every fixture field, schema constraint,
constant, sentinel, runner exit, stdout/stderr form, byte count, result kind,
reason code, authority effect, rollback digest, adapter exit, launch counter,
and per-case expectation for `J01`–`J13`, `P01`–`P08`, both `W01`–`W15`
surfaces, and `A01`–`A27`. If the summary below omits or conflicts with a scalar
expectation, the digest-bound addendum controls. Any byte change to the
addendum invalidates this normative binding and requires a new digest and
review. Incorporation does not convert future design into current evidence.

Frozen constants:

```text
request_byte_ceiling       = 262144
target_stdout_byte_ceiling = 1048576
target_stderr_byte_ceiling = 0
adapter_timeout_ms         = 5000
timeout_injected_delay_ms  = 5001
not_started_or_no_exit     = -1
```

Every runner emits canonical JSONL using
`intent-route.acceptance-case@1`, one line per declared case, followed by one
`intent-route.acceptance-summary@1` line. Object keys are lexicographically
ordered, each line ends with one LF, and runner stderr is empty.

Runner exits are exact:

```text
0 = every declared case emitted exactly once and passed
1 = at least one declared case completed but failed expectation
2 = fixture, CLI, schema, or harness configuration failure
3 = runner could not complete or emit a valid summary
```

For exits `2` or `3`, stdout is empty and no acceptance claim may be made.
Fixture manifests use `intent-route.acceptance-fixture@1`, closed surface and
case selectors, exact semantic versions, lowercase 64-hex fixture/catalog/
closure/archive digests, immutable repository-relative prior-release archives,
and `isolated_install_root_mode=mkdtemp`.

### 1. JSON port — `J01` through `J13`

```bash
node arcanum/arcana/intent-route-resolver/package/test/run-json-port-acceptance.mjs \
  --cases arcanum/arcana/intent-route-resolver/fixtures/json-port-acceptance-v1.json \
  --case-ids J01,J02,J03,J04,J05,J06,J07,J08,J09,J10,J11,J12,J13 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0
```

Required result: exactly 14 stdout JSONL lines, 13 passed cases, runner exit
`0`, and zero runner stderr bytes.

### 2. Public core/private scan — `P01` through `P08`

```bash
node arcanum/arcana/intent-route-resolver/scripts/run-public-core-acceptance.mjs \
  --root arcanum/arcana/intent-route-resolver \
  --cases arcanum/arcana/intent-route-resolver/fixtures/public-core-acceptance-v1.json \
  --case-ids P01,P02,P03,P04,P05,P06,P07,P08 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0
```

The eight selectors prove core tests, private-content scan, private-import scan,
zero-authority manifest, package-version binding, protocol-version binding,
closure-digest binding, and fixture-digest binding. Required result: exactly 9
stdout JSONL lines, all 8 cases pass, runner exit `0`, and zero runner stderr
bytes.

### 3. Codex wrapper — `W01` through `W15`

```bash
node .agents/skills/intent-route-resolver/scripts/run-wrapper-acceptance.mjs \
  --entry .agents/skills/intent-route-resolver/scripts/invoke-json-port.mjs \
  --cases .agents/skills/intent-route-resolver/fixtures/wrapper-acceptance-v1.json \
  --case-ids W01,W02,W03,W04,W05,W06,W07,W08,W09,W10,W11,W12,W13,W14,W15 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0 \
  --prior-release-id-field prior_release_id \
  --prior-release-archive-field prior_release_archive \
  --prior-release-archive-digest-field expected_prior_release_archive_digest \
  --expected-prior-closure-digest-field expected_prior_closure_digest \
  --expected-restored-closure-digest-field expected_restored_closure_digest \
  --isolated-install-root-mode mkdtemp
```

Required result: exactly 16 stdout JSONL lines, all 15 cases pass, runner exit
`0`, zero runner stderr bytes, and
`W15.observed.post_rollback_closure_digest` equals both expected prior and
restored closure digests.

### 4. Claude wrapper — `W01` through `W15`

```bash
node .claude/skills/intent-route-resolver/scripts/run-wrapper-acceptance.mjs \
  --entry .claude/skills/intent-route-resolver/scripts/invoke-json-port.mjs \
  --cases .claude/skills/intent-route-resolver/fixtures/wrapper-acceptance-v1.json \
  --case-ids W01,W02,W03,W04,W05,W06,W07,W08,W09,W10,W11,W12,W13,W14,W15 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0 \
  --prior-release-id-field prior_release_id \
  --prior-release-archive-field prior_release_archive \
  --prior-release-archive-digest-field expected_prior_release_archive_digest \
  --expected-prior-closure-digest-field expected_prior_closure_digest \
  --expected-restored-closure-digest-field expected_restored_closure_digest \
  --isolated-install-root-mode mkdtemp
```

Required result: exactly 16 stdout JSONL lines, all 15 cases pass, runner exit
`0`, zero runner stderr bytes, the same rollback equality, and case response
bytes equal to the corresponding Codex case bytes.

### 5. Orchestrator adapter — `A01` through `A27`

```bash
python projects/cyberalchemy-orchestrator/implementations/tests/runtime/run_intent_route_adapter_acceptance.py \
  --cases projects/cyberalchemy-orchestrator/implementations/tests/runtime/fixtures/intent-route-adapter-acceptance-v1.json \
  --case-ids A01,A02,A03,A04,A05,A06,A07,A08,A09,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,A23,A24,A25,A26,A27 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0 \
  --timeout-ms 5000 \
  --prior-release-id-field prior_release_id \
  --prior-release-archive-field prior_release_archive \
  --prior-release-archive-digest-field expected_prior_release_archive_digest \
  --expected-prior-closure-digest-field expected_prior_closure_digest \
  --expected-restored-closure-digest-field expected_restored_closure_digest \
  --isolated-install-root-mode mkdtemp
```

Required result: exactly 28 stdout JSONL lines, all 27 cases pass, runner exit
`0`, zero runner stderr bytes, and `A18.cases.injected_delay_ms=5001`.

The case families cover:

- `candidate`, `ambiguous`, `no-match`, and `invalid`;
- malformed JSON/catalog, capability denial, and request/port/core/manifest
  version mismatch;
- catalog and content/closure digest mismatch;
- disable and rollback, including rollback digest mismatch;
- timeout, unavailable executable, nonzero target exit, multiple stdout
  documents, `1048577`-byte oversized stdout, and any stderr byte;
- confirmed versus unconfirmed Dispatch binding;
- authorization denial, execution error, and effect without its required
  receipt.

Exact result schemas are `intent-route.runtime-port@1`,
`intent-route.error@1`, and `intent-route.public-check@1`. Exact accepted
resolver result kinds remain `candidate | ambiguous | no-match | invalid`;
every trusted disposition has `authority_effect: none`.

The proposed `IR_*` codes and all runners above are future acceptance names,
not current executable vocabulary.

## Human decisions still required

- Permission and scope for public extraction.
- Canonical sigil name, public API, license, and compatibility commitment.
- Exact canonical capability and confirmed Dispatch sources projected into the
  catalog.
- Catalog projector and request-normalization owners and paths.
- Whether `selected-local` remains private or receives a separately reviewed
  generic replacement.
- ACI command/event fields that reference request and disposition
  content-addressed artifacts.
- Transport executable/ref, versions, limits, timeout, error policy, disable
  control, release pin, and durable rollback artifact.
- Canonical source acceptance.
- Generated-package promotion and public release.
- Consumer installation and any later deployment.
- Advancement from advisory shadow use to gating.
- Any compatibility-fallback retirement.
- Admission into private `cyberAlchemy-v2` authority.

## Claim ceilings

Current evidence permits these claims:

- the private standalone package exists and passed 34 tests with 0 failures;
- it deterministically reduces typed intent and a frozen catalog to traced,
  digest-bound, abstaining, non-authorizing dispositions;
- its current contribution is bounded to pre-inference route reduction;
- the selected future topology and acceptance design passed the three bounded
  reviews.

Current evidence does not permit claims of:

- public extraction or canonical Arcanum acceptance;
- generated Claude or Codex packages;
- behavior parity;
- generated-package promotion or public release;
- consumer installation or deployment;
- orchestrator integration or ACI artifact binding;
- Augmentor, ResonantOS, or other runtime integration;
- semantic judgment, object-level inference, whole reasoning-engine status, or
  production readiness.

## Typed residue

- `extraction_authority`: public extraction not approved.
- `canonical_source_absent`: no accepted public sigil exists.
- `catalog_owner_unbound`: exact canonical capability and Dispatch inputs,
  projector owner, and path are missing.
- `normalization_owner_unbound`: no owner constructs
  `intent-route.request@1`.
- `aci_artifact_contract_unimplemented`: content-addressed references and ACI
  record fields do not exist.
- `generated_packages_absent`: Claude/Codex projections do not exist.
- `parity_no_witness`: presence and behavior parity remain unproved.
- `future_commands_non_evidence`: all five acceptance surfaces are contract
  proposals only.
- `negative_coverage_unwitnessed`: the complete error matrix is not executable
  today.
- `transport_unpinned`: executable, version, timeout, limits, and stderr policy
  are not implemented.
- `disable_unimplemented`: the consumer disable gate is not implemented.
- `rollback_source_absent`: no pinned prior public release/digest exists.
- `consumer_adapter_absent`: no orchestrator adapter or zero-call
  instrumentation exists.
- `consumer_witness_absent`: no runtime installs or invokes the resolver.
- `ACI_integration_unwitnessed`: no ACI-subordinate handoff exists.
- `reasoning_ceiling`: no object-level inference, actor protocol, memory,
  effects, or whole-engine witness.

## Handoff

Proceed only through the separately gated owner-binding and authority
transitions above. The immediate next decision is whether to authorize a fresh
public extraction and bind the canonical catalog-projection, normalization,
and ACI artifact-reference owners. Until then, the repaired topology remains
owner-preserving, implementation-ready design only.
