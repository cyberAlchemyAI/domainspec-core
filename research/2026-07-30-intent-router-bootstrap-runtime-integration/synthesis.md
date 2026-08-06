# Intent Router Bootstrap and Runtime Integration Synthesis

dispatch_id: `2026-07-30-intent-router-bootstrap-runtime-integration`  
step_id: `s2`  
capability_ref: `research`  
capability_target: `dispatch-sheet.json`  
capability_mode: `synthesize`  
wave_id: `synthesize`  
write_scope: `[]`  
status: `complete`  
artifacts: `[]`  
validation: `Reconciled the three explorer receipts against their selector-bearing returns in research.md; no new source corpus inspected; no runtime execution or mutation performed.`  
observer_status: `not-invoked-read-only-synthesis`  
blockers:

- `No canonical public Arcanum intent-route-resolver sigil exists.`
- `Public extraction/promotion has not been approved.`
- `No human-owned authoritative selection artifact, live catalog owner, or orchestrator normalization owner exists.`
- `Claude/Codex behavior parity and concrete orchestrator consumption are future witnesses, not current facts.`

residue:

- `public-extraction-decision`
- `catalog-authority`
- `normalization-owner`
- `authoritative-selection-artifact`
- `cross-runtime-behavior-witness`
- `transport-pinning`
- `runtime-persistence-schema`
- `ACI-consumer-integration`

reroute: `After human approval, route a bounded public-extraction/design task, followed by generated-runtime conformance and a separate orchestrator consumer work-pack.`  
handoff_note: `The resolver emits candidate, never authoritative selected. Use selected only for a later human-owned selection artifact. Current direct Bootstrap installation is killed; the narrowed future topology is admissible but unimplemented.`

## Exact-binding decision

Select, with two hard qualifications, this owner-preserving target:

```text
public, project-agnostic, transport-neutral resolver core
  owned canonically as an Arcanum sigil
        |
        +-- Bootstrap selects that canonical sigil
        +-- Bootstrap generates thin Claude and Codex wrappers
        |
        +-- optional host-owned adapters consume its JSON port
                |
                +-- cyberalchemy-orchestrator pre-launch adapter
                |     resolver candidate -> human selection -> existing binding
                |
                +-- cyberAlchemy-v2 entry-routing integration
                      before semantic judgment; private authority retained
```

Qualifications:

1. The current private package cannot be installed or copied directly into public Arcanum. A fresh, reviewed generic extraction must be approved first. [Hewitt receipt; `bootstrap_arcanum.sh:371-383`, `sync-generated-skill-package.sh:80-106`; Ashby receipt; `define/SPEC.md:64-85`]
2. The resolver returns `candidate`, `ambiguous`, `no-match`, or `invalid`. It never returns authoritative `selected`. `selected` is reserved for a later human-owned, separately persisted selection artifact. [Simon receipt; `src/resolve.mjs:137-185`; Ashby receipt; `define/SPEC.md:155-165`, `src/resolve.mjs:103-192`]

Kill any topology in which Bootstrap owns semantic routing, a generated wrapper owns approval/execution, the orchestrator duplicates resolver predicates, or cyberAlchemy-v2 private authority is copied into public Arcanum.

## Direct answers

1. **Can this become an Arcanum add-on installed through Bootstrap?**  
   Not directly today. Bootstrap only selects canonical sigils/spells, and no public canonical resolver exists. Yes as a future topology only after an explicit public extraction creates one canonical zero-authority sigil; Bootstrap may then select it and generate its runtime projections. [Hewitt receipt; `bootstrap_arcanum.sh:371-411`, `bootstrap_arcanum.sh:821`, `bootstrap_arcanum.sh:1215`]

2. **Can Claude and Codex receive equivalent integrations?**  
   Presence parity is structurally supported by generation from one canonical source, but resolver presence is currently absent and behavior parity is unproved. Acceptance requires identical executable/support bytes and canonical outcomes across both generated packages, allowing only generated metadata and the declared Claude tool-token normalization to differ. [Hewitt receipt; `bootstrap_arcanum.sh:1028`, `bootstrap_arcanum.sh:1215`, `VALIDATION-CONTRACTS.md:13`]

3. **Can cyberalchemy-orchestrator consume it?**  
   Yes, later, through a thin process-bound JSON adapter immediately before `_workflow_envelope()` chooses the binding path. The resolver proposes a `candidate`; a human-owned artifact selects; existing `RuntimeService.bind_host_workflow_turn()` retains validation, authorization, dispatch, persistence, and lifecycle. This seam is not implemented. [Simon receipt; `implementations/server/runtime/host_dispatch_hook.py:373-427`, `service.py:5192-5566`]

4. **Does it advance the cyberAlchemy-v2 reasoning engine, and how does it relate to Augmentor/other runtimes?**  
   It advances only the reproducible front-door, pre-inference capability-routing boundary. It is a working private L0 reasoning-support adapter, not yet runtime-integrated, not an object-level semantic evaluator, and not a whole reasoning engine. Augmentor and other runtimes may project intent or consume advisory dispositions through owner-specific adapters; they do not become resolver, approval, dispatch, or execution owners. [Ashby receipt; `define/SPEC.md:10-42`, `agent-reasoning-engine/spec/SPEC.md:127-178`, `semantic-judgment-evaluator/src/reducer.mjs:113-157`; Ashby receipt; `define/SPEC.md:75-85`]

## Expected end state

- One canonical public Arcanum sigil contains a freshly extracted generic core, JSON port, public protocol schemas, zero-authority manifest, synthetic fixtures, and a thin native wrapper. [Hewitt receipt; `bootstrap_arcanum.sh:821`, private precedent `package.json:7`, `addon-manifest.json:20-22`]
- Bootstrap selects the sigil and generates `.agents/skills/intent-route-resolver/` and `.claude/skills/intent-route-resolver/` from the same closure. [Hewitt receipt; `bootstrap_arcanum.sh:1215`]
- Each host supplies its own adapter and catalog snapshot; neither core nor wrapper owns live catalog authority, human selection, persistence, approval, dispatch, or effects. [Simon receipt; `src/json-port.mjs:12-55`; Ashby receipt; `define/SPEC.md:64-85`]
- cyberalchemy-orchestrator records immutable request, disposition, and human selection evidence, then enters its existing workflow-binding path. [Simon receipt; `host_dispatch_hook.py:373-427`, `service.py:5516-5761`]
- cyberAlchemy-v2 references the public generic contract at its entry-routing layer while retaining private ACI, semantic judgment, actor protocol, memory, effect, and promotion authority. [Ashby receipt; `agent-reasoning-engine/spec/SPEC.md:15-31`, `:127-178`, `:287-302`]

## Current-versus-target matrix

| Concern | Current | Target |
|---|---|---|
| Core | Working private ESM package; 34 tests pass | Freshly reviewed public generic core [Ashby receipt; `src/resolve.mjs:19-192`; Hewitt receipt; `package.json:7`] |
| Bootstrap | Unknown selector; direct topology killed | Select canonical public sigil [Hewitt receipt; `bootstrap_arcanum.sh:371-411`] |
| Claude/Codex | Resolver absent | Both packages generated from one source [Hewitt receipt; `bootstrap_arcanum.sh:1215`] |
| Behavior parity | Unproved | Same fixtures, bytes, outcomes, and failure classes [Hewitt receipt; `VALIDATION-CONTRACTS.md:13`] |
| Orchestrator | No normalizer, catalog owner, adapter, or selection artifact | Thin pre-launch JSON adapter plus human selection [Simon receipt; `host_dispatch_hook.py:373-427`] |
| cyberAlchemy-v2 | Standalone private L0 package | Entry-routing consumer, ACI-subordinate, private authority retained [Ashby receipt; `decisions/aci-reasoning-binding/DECISION.md:33-38`, `:57-67`] |
| Reasoning claim | Meta-level deterministic routing | Integrated reasoning-support component only after a consumer witness; never whole-engine by this evidence [Ashby receipt; `agent-reasoning-engine/spec/SPEC.md:287-302`] |

## Options and kill matrix

| Option | Decision | Boundary |
|---|---|---|
| Transport-neutral standalone core | **Select after extraction** | Pure JSON relation, zero effects [Ashby receipt; `addon-manifest.json:1-22`] |
| Copy private package into Arcanum | **Kill** | Violates public/private authority boundary [Ashby receipt; `define/SPEC.md:64-85`] |
| Bootstrap generic add-on selector | **Kill for this scope** | Bootstrap currently owns canonical sigil/spell selection only [Hewitt receipt; `bootstrap_arcanum.sh:371-411`] |
| Bootstrap-selected canonical sigil | **Select, future** | Requires public extraction approval [Hewitt receipt; `bootstrap_arcanum.sh:821`, `:1215`] |
| Thin generated Claude/Codex wrappers | **Select, future** | Invocation only; no semantic divergence [Hewitt receipt; `bootstrap_arcanum.sh:1028`] |
| Python reimplementation | **Kill** | Creates a second drifting resolver [Simon receipt; `src/json-port.mjs:12-55`] |
| Thin process-bound orchestrator adapter | **Select, future** | Transport/integrity only [Simon receipt; `host_dispatch_hook.py:373-427`] |
| Smart adapter that chooses or retries | **Kill** | Would duplicate semantics or convert advisory output into authority [Simon receipt; `src/resolve.mjs:74-100`, `:137-185`] |
| Augmentor as resolver/executor | **Kill** | Augmentor remains an intent/proposal projection, not authority [Ashby receipt; `define/SPEC.md:75-85`] |
| Whole reasoning-engine claim | **Kill** | Object-level inference, actor protocol, memory, effects, and ACI witness absent [Ashby receipt; `agent-reasoning-engine/spec/SPEC.md:287-302`] |

## Public-private extraction boundary

Public candidate surface:

- generic canonical JSON utilities;
- request/catalog validation;
- typed epistemic posture without private vocabulary;
- eligibility, exclusions, explicit dominance, ambiguity, and abstention;
- `candidate | ambiguous | no-match | invalid` disposition;
- JSON port, generic schemas, zero-authority manifest, synthetic fixtures.

[Hewitt receipt; `package.json:7`, `addon-manifest.json:20-22`; Ashby receipt; `src/eligibility.mjs:11-114`, `src/resolve.mjs:19-192`]

Private or separately redesign-required:

- current package bytes and private provenance;
- `selected-local` compatibility mapper and private IntentRecord assumptions;
- CAV2, DomainSpec, Saturn, ACI, reasoning-engine, Augmentor, or ResonantOS prose and fixtures;
- private route catalogs and authority vocabulary;
- adapters that persist, approve, dispatch, or execute.

[Hewitt receipt; `INTEGRATION-VERSIONING.md:21`; Ashby receipt; `define/SPEC.md:64-85`]

## Bootstrap lifecycle contract

- **Selection:** only a canonical public sigil selector; no private path selector. [Hewitt receipt; `bootstrap_arcanum.sh:371-411`]
- **Install:** staged generation of both profiles from the same source closure; installation grants no route authority. [Hewitt receipt; `bootstrap_arcanum.sh:821`, `:1215`]
- **Update:** prefer selective sync, staged for both profiles with checksum comparison and symlink rejection. [Hewitt receipt; `sync-generated-skill-package.sh:136-196`]
- **Disable:** host-owned configuration stops wrapper invocation; disabling must not mutate catalogs, prior evidence, or existing orchestrator lifecycle records. This remains contract work, not current implementation.
- **Rollback:** restore a pinned prior committed/released package. Selective-sync temporary backups are not durable rollback; full `--force` is non-transactional. [Hewitt receipt; `sync-generated-skill-package.sh:196`]
- **Provenance:** bind canonical Arcanum revision/release, core and manifest versions, supported protocol majors, executable/support digest, and fixture-set digest. Current wrapper provenance is insufficient. [Hewitt receipt; `bootstrap_arcanum.sh:795`]

## Claude/Codex parity

| Check | Presence | Behavior |
|---|---|---|
| Generated package path | Both must exist | Insufficient alone |
| Core/manifest/schemas/fixtures | Byte-identical digest | Required |
| `SKILL.md` | Same canonical semantics | Differences limited to generated provenance and declared `Task → Agent`, `AskQuestions → AskUserQuestion` mapping [Hewitt receipt; `bootstrap_arcanum.sh:1028`] |
| Outcomes | Same fixture set present | Byte-identical canonical JSON |
| Failures | Same fixture set present | Same typed classification and exit policy |
| Authority | Both say zero authority | Neither may select, approve, dispatch, or execute |

## Stable request/result contract

Request must bind:

```text
schema_version = intent-route.request@1
request_id
intent/discriminators with declared|inferred|unresolved posture
evidence references
catalog_id
catalog_digest
supersedes_request_id?
```

The catalog is a frozen owner-supplied snapshot; the adapter may not compile or repair it. [Simon receipt; `src/selected-local.mjs:106-175`, `:267-309`; Ashby receipt; `define/SPEC.md:87-113`]

Result must bind:

```text
schema_version = intent-route.runtime-port@1
disposition_schema = intent-route.disposition@1
kind = candidate | ambiguous | no-match | invalid
request_id/digest
catalog_id/digest
evaluated-route traces
reason codes
clarification?
candidate route identity?
receipt_digest
authority_effect = none
```

[Simon receipt; `src/json-port.mjs:12-55`, `src/resolve.mjs:74-100`, `:137-185`]

A later authoritative artifact, never emitted by the resolver:

```text
selection_id
request_digest
disposition_digest
catalog_id/digest
route_id
selected_by
selection_basis/evidence
selected_at
```

It must be human-owned, catalog-bound, immutable, and separately authorized. A resolver `candidate` is not `selected`.

## Orchestrator seam, lifecycle, and owners

Sequence:

1. Source adapter normalizes intent or applies an admitted selected-local mapping.
2. Catalog owner supplies a frozen catalog snapshot.
3. Thin adapter invokes one pinned local JSON-port process with timeout and byte ceilings.
4. Adapter verifies protocol, canonical bytes, digests, and `authority_effect: none`.
5. `candidate` enters `awaiting-selection`; `ambiguous` enters `awaiting-clarification`; `no-match` and `invalid` launch nothing.
6. Human supplies a catalog-bound selection artifact.
7. Existing hook maps that artifact to a confirmed Dispatch/group/seat.
8. Existing `RuntimeService.bind_host_workflow_turn()` retains manifest/prompt integrity, authorization, idempotency, scheduling, persistence, completion, and close gates.

[Simon receipt; `host_dispatch_hook.py:373-427`, `service.py:5192-5761`, `migrations/009_host_workflow_binding.sql:1-30`]

Explicit human route precedence is a target integration rule, not currently typed. A valid explicit selection may bypass advisory resolution only after catalog identity/digest validation.

## Reasoning-engine layer map and proof ceiling

| Layer | Verdict |
|---|---|
| Intention normalization | Partial |
| Eligibility/exclusions | Current |
| Explicit dominance/candidate reduction | Current, narrow |
| Ambiguity/routing abstention | Current |
| Semantic judgment | Absent |
| Object-level inference | Absent |
| Actor protocol | Absent |
| Memory/replay | Absent |
| Effects | Absent by design |
| Observability | Partial standalone trace only |
| ACI integration | Deferred/unwitnessed |

[Ashby receipt; `src/eligibility.mjs:11-114`, `src/resolve.mjs:61-192`, `agent-reasoning-engine/spec/SPEC.md:127-178`, `:287-302`]

Claim ceiling: **A tested private, transport-neutral L0 pre-inference control/reasoning-support adapter that deterministically produces non-authorizing route dispositions.** It is not currently consumer-integrated, public, promoted, deployed, production-ready, an object-level semantic evaluator, or a whole reasoning engine.

## Exact future validation fixtures

1. Canonical public extraction contains no private identifiers, prose, imports, paths, or fixtures.
2. Bootstrap dry-run/selective preview identifies both profiles without mutation.
3. Generated Claude and Codex support closures have identical digests.
4. Wrapper diff contains only admitted metadata/tool-token differences.
5. Both projections return identical canonical bytes for `candidate`, `ambiguous`, `no-match`, and `invalid`.
6. Negative parity covers malformed request, malformed catalog, capability denial, unsupported protocol/version, catalog digest mismatch, disabled integration, and pinned-version rollback.
7. One `candidate` cannot launch without a human selection artifact.
8. Ambiguity preserves the exact clarification question and launches nothing.
9. Clarification creates a distinct request with `supersedes_request_id`.
10. Timeout, nonzero exit, oversized/multiple output, stderr-policy violation, and unavailable process fail closed.
11. No-match/invalid never reaches dispatch opening, appender, journal dispatch-open, or host spawn.
12. Selected route must match an open confirmed Dispatch/group/seat and retain current prompt/manifest hashes, retry conflict, follow-up, and close-gate behavior.
13. Adapter source contains no predicates, ranking, keyword fallback, scheduler, appender, capability issuance, or network access.
14. An ACI-bound integration fixture proves disposition-to-entry-gate handoff without bypassing semantic judgment, approval, or effect gating.

Existing fixture patterns are cited by Simon at `test/json-port.test.mjs:59-113`, `test/selected-local.test.mjs:67-159`, `test_host_workflow_binding.py:245-427`, and `test_host_dispatch_hook.py:125-173`; standalone execution evidence is cited by Ashby at the 34-test receipt and `generated/runs/.../receipt.json:17-30`.

## Ordered implementation slices

1. Human decision on public extraction, naming, canonical Arcanum ownership, and license/public boundary.
2. Contract-only public design: generic schemas, candidate terminology, authority ceiling, manifest, provenance, disable/rollback semantics.
3. Fresh generic extraction with synthetic fixtures; exclude private mapper and vocabulary.
4. Canonical sigil wrapper and deterministic conformance runner.
5. Bootstrap generation into disposable Claude/Codex fixture repositories.
6. Cross-runtime presence, digest, behavior, failure, disable, and rollback acceptance.
7. Orchestrator contract slice: normalizer owner, catalog owner, selection artifact, lifecycle/error map, transport pinning.
8. Adapter conformance with injected fake and pinned JSON subprocess; no launch integration.
9. Advisory shadow recording.
10. Clarification/no-route/invalid gating.
11. Human-selection-to-existing-binding integration.
12. ACI-subordinate cyberAlchemy-v2 consumer witness and semantic-evaluator handoff.
13. Compatibility-path retirement only after separate evidence and approval.

## Decisions requiring human approval

- Whether any generic subset may be extracted to public Arcanum.
- Canonical sigil name and public API/version commitment.
- Whether `selected-local` stays private or is redesigned generically.
- Catalog authority and compilation owner.
- Normalization owner for each consumer.
- Shape, principal policy, and retention of the authoritative selection artifact.
- Process pinning, timeout, byte, stderr, disable, update, and rollback policies.
- Whether orchestrator shadow mode may progress to a launch gate.
- Whether and when compatibility fallback is retired.
- Whether the resulting entry-routing integration is admitted into private cyberAlchemy-v2 authority; implementation evidence alone cannot promote it.

## Typed residue

- `extraction_authority`: no public extraction decision.
- `terminology`: downstream materials must replace resolver-level `selected` with `candidate`.
- `catalog_authority`: no live effective catalog owner/path.
- `normalization_owner`: no owner for `intent-route.request@1` construction.
- `selection_authority`: no typed human-owned selection artifact.
- `parity_witness`: no generated Claude/Codex resolver fixtures.
- `provenance_gap`: generated packages do not yet bind core/manifest/fixture digests.
- `disable_contract`: target behavior specified only at principle level.
- `rollback_gap`: full forced Bootstrap is non-transactional; selective backups are temporary.
- `transport_contract`: executable/ref, limits, exit and stderr policies unpinned.
- `persistence_schema`: no route request/disposition/selection event schema.
- `explicit_precedence`: inferred integration rule, not current typed artifact.
- `consumer_witness`: no orchestrator, Augmentor, ACI, or other runtime invocation.
- `reasoning_ceiling`: no object-level inference, actor protocol, memory, effects, or whole-engine witness.
