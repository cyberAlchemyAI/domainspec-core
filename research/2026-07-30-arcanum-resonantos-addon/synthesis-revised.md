# Revised exact-binding synthesis

## Recommendation and claim ceiling

Retain the three-layer topology only as `BUILD-FROM-OWNED + NOVEL-ATTEMPT`:

1. Arcanum Bootstrap remains the sole owner of installing, selecting, refreshing, and restoring generated public Arcanum packages at the consumer workspace.
2. ResonantOS remains the sole product owner of add-on discovery, installation, reviewed grants, authenticated bridge routes, provider/delegation execution, run state, artifacts, secrets, disable, uninstall, product rollback, promotion, and release.
3. Augmentor is limited to eligibility classification after explicit-command precedence, proposal presentation, human-intent capture, and projection of host-owned state.

No current integration, execution, browser-witness, readiness, promotion, or release claim follows. The candidate product checkout is stale; the add-on, routes, approval contract, capability adapters, and lifecycle witnesses are absent.

Bindings: `research.md#Agent-1`, `research.md#Agent-2`, `research.md#Agent-3`; `reviews/precedent.md`; `reviews/nonvacuity.md`; `reviews/boundary.md`; `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Normative-Boundary`; `docs/architecture/MODULE-OWNERSHIP.md#Alpha-Ownership`.

## Expected future end state

If every dependency and acceptance gate below is later satisfied, Bootstrap-managed public Arcanum capabilities would be exposed through one ResonantOS-native add-on without embedding a third runtime. Augmentor would classify only unmatched ordinary language, present immutable proposal bytes, capture edit, decline, clarification, or approval intent, and submit that intent to a host owner. The host would validate and persist approval, enforce bridge authentication and scoped capability grants, invoke retained execution owners, persist owner truth, and return opaque projections. Results would remain separately openable, attachable, consumable, or eligible for a distinct memory-intake review.

That paragraph describes a target contract, not current behavior.

## Current evidence and missing-product ledger

| Concern | Evidence state | Binding conclusion |
|---|---|---|
| Requested `../workspace-resonantos` path | Absent | The corrected `../workspace-resonant` target still requires owner confirmation. |
| Consumer root | Non-Git root containing generated Arcanum packages, `.arcanum`, observability state, and `tools/arcanum` | Package presence is repository/runtime evidence, not product installation. |
| Product checkout | `dev@6f92af7b32b17d2eef66230d463eb8b6a21a98f7`, seven cached commits behind `origin/dev@3b07e635d596c18f9a047ef5921892acc7cba4ff` | Refresh and selector re-resolution are prerequisites to implementation. |
| Bootstrap installation | Present; selection currency unproven | Bootstrap retains installation/update authority. |
| Subagent Strategy | Consumer package absent | `subagent-strategy.execute` has no current consumer owner operation. |
| Whisper | Generated package present but drifted | Package presence does not establish a ResonantOS adapter or executable product route. |
| Product add-on manifest | Absent | The JSON below is only an unvalidated design fixture. |
| Arcanum bridge routes | Absent | Existing bridge and delegation services are retained-owner precedents only. |
| Proposal and approval | No Arcanum `StrategyProposal`, canonical digest, replay guard, or host approval persistence | Novel host-owned contract required. |
| Child clarification and run projection | Existing chat forks, cards, and delegation records are primitives | No current Arcanum child-handle, clarification, join, run-tray, or reload composition exists. |
| Disable/uninstall/rollback | Vocabulary and installation state exist | No Arcanum-specific operational witness exists. |
| Browser fixture | Absent | No proposal, approval, two-owner execution, clarification, reload, consumption, disable, or rollback witness exists. |

## Owner and use-mode map

| Mechanism | Retained owner | Use mode |
|---|---|---|
| Generated Arcanum installation, refresh, restore | Arcanum Bootstrap | `BUILD-FROM-OWNED` |
| Manifest validation and catalog projection | Add-on SDK validator and existing registry | `BUILD-FROM-OWNED`; Arcanum entry absent |
| Installation, enablement, reviewed grants, revocation | ResonantOS `AddOnInstallation` and capability-review owners | `BUILD-FROM-OWNED`; binding absent |
| Bridge listener, authentication, capability enforcement | `bridge-server.mjs` and token owner | `BUILD-FROM-OWNED` |
| Arcanum route behavior | Add-on delegation host/service domain | `NOVEL-ATTEMPT` |
| Deterministic resolution | Pure proposal resolver and host-side public Arcanum resolver | `NOVEL-ATTEMPT` composed from deterministic Arcanum precedent |
| Provider selection and credentials | Provider host/bridge fabric | Retained current owner; new consumer binding |
| Proposal hashing and approval persistence | New host-owned add-on contract | `NOVEL-ATTEMPT` |
| Execution, scheduling, run/action truth | Host delegation/provider owners | `NOVEL-ATTEMPT`; never Augmentor |
| Child handles, clarification, join, reload reconciliation | Host delegation domain | `NOVEL-ATTEMPT` |
| Run tray and proposal UI | Augmentor/browser projection | `PROJECTION_ONLY` |
| Artifact creation/read | Delegation artifact owner | `BUILD-FROM-OWNED` |
| Attachment and follow-up consumption | Chat/session owner | `BUILD-FROM-OWNED` |
| Memory intake, review, promotion | Memory/archive owners | `BUILD-FROM-OWNED`; never automatic |
| Product disable, uninstall, rollback | Installation/grant/add-on host owners | `NOVEL-ATTEMPT` operational contract |
| Product promotion | Product acceptance/promotion owner | Future gated transition |
| Product release | Product release owner | Future post-promotion packaging/distribution |

## Options and kill decisions

| Option | Decision |
|---|---|
| Three retained-owner layers | Retain only as `BUILD-FROM-OWNED + NOVEL-ATTEMPT`. |
| Repository-generated skills represented as an installed product add-on | Kill. |
| Embedded Arcanum runtime or third Alpha component | Kill. |
| Nested `codex exec`, Claude, or another model-backed CLI | Kill. |
| Augmentor-owned installer, registry, router, scheduler, executor, approval database, workspace, session store, artifact store, secret store, or memory path | Kill. |
| Preview, discovery, or recommendation that installs, grants, schedules, or executes | Kill. |
| Broad exposure of all generated skills | Defer. |
| Necronomicon or automatic memory integration | Defer. |
| Literal Strategy plus Whisper execution catalog | Defer until both stable native owner operations and product adapters exist. |
| Strategy plus Whisper acceptance fixture | Retain only as a future acceptance test. |
| Preview/status-only degraded surface | Permit only if clearly marked unavailable and incapable of execution. |

## Initial public capability catalog

| Operation | Current status | Future acceptance condition |
|---|---|---|
| `subagent-strategy.preview` | Absent product operation | Pure canonical proposal construction with zero privileged or provider calls |
| `subagent-strategy.execute` | Killed for current product state | Current generated package plus stable native owner adapter |
| `whisper.execute` | Killed for current product state | Current generated package plus stable ResonantOS owner adapter |
| `run.status` | Absent Arcanum mapping | Host-owned record query |
| `run.clarify` | Absent | Child-handle-scoped host route with isolation proof |
| `artifact.read` | Existing artifact precedent; Arcanum mapping absent | Existing artifact owner accessed through an opaque reference |
| `dispatch-spec`, `orchestrate`, `tools/arcanum` | Internal support only | Must not become browser product cards or model executors |
| Necronomicon, legacy adapters, `codex-exec`, `codex-bypass` | Deferred or killed | Outside the initial product surface |

## Complete validator-shaped manifest design fixture

The following is a complete JSON object shaped to the current `AddOnSdkManifest` contract and current enums. It has not been submitted to `validateAddOnManifest(..., {source: "sideload"})`; therefore it is an **unvalidated design fixture**, not a valid, accepted, installed, enabled, or release-ready manifest.

```json
{
  "sdkVersion": "0.1.0",
  "id": "addon.arcanum",
  "name": "Arcanum",
  "version": "0.1.0",
  "author": "ResonantOS",
  "category": "orchestration",
  "description": "Host-mediated projection of selected Bootstrap-managed public Arcanum capabilities.",
  "runtimeType": "agent-addon",
  "surfaces": [
    {
      "id": "arcanum-panel",
      "type": "panel",
      "label": "Arcanum",
      "description": "Proposal, approval-intent, run-status, and result projection.",
      "shellNavigation": {
        "sectionId": "addons",
        "dockIcon": "browser",
        "eyebrow": "Add-on",
        "order": 70,
        "requiredCapabilities": [
          "agent-delegation"
        ]
      }
    },
    {
      "id": "arcanum-tool-action",
      "type": "tool-action",
      "label": "Propose Arcanum route",
      "description": "Creates a side-effect-free proposal for an eligible request."
    },
    {
      "id": "arcanum-run-monitor",
      "type": "background-task-monitor",
      "label": "Arcanum runs",
      "description": "Projects host-owned run and child state."
    }
  ],
  "requestedCapabilities": [
    {
      "capability": "agent-delegation",
      "granted": false,
      "scope": "workspace",
      "revocationBehavior": "hard-stop"
    },
    {
      "capability": "notifications",
      "granted": false,
      "scope": "self",
      "revocationBehavior": "degrade"
    }
  ],
  "provenance": {
    "tier": "sideloaded-unverified",
    "verificationState": "unverified",
    "signed": false
  },
  "runtimeIsolation": {
    "boundary": "host-mediated-agent",
    "supportsDegradedMode": true,
    "requiresReviewedGrant": true
  },
  "providerRequirements": {
    "sharedProfiles": [],
    "supportsPrivateCredentials": false
  },
  "archiveIntegration": {
    "readScopes": [],
    "intakeWriteScopes": [],
    "canRequestIngest": false,
    "canWriteKnowledgePages": false
  },
  "health": {
    "strategy": "bridge-runtime-status"
  },
  "installHooks": {},
  "compatibility": {
    "shellVersion": "2.0.0-alpha",
    "platforms": [
      "linux"
    ]
  }
}
```

Bindings: `src/core/contracts.ts#AddOnManifest`, `#CapabilityGrant`, `#AddOnSurface`, `#AddOnProvenance`, `#AddOnRuntimeIsolation`; `src/sdk/addons/contracts.ts#AddOnSdkManifest`, `#ADDON_CAPABILITIES`; `src/sdk/addons/validation.ts#validateAddOnManifest`.

### Requested capabilities versus reviewed installation grants

Manifest requests are recommendations, not grants. Every manifest request above starts with `granted: false`.

Catalog discovery must produce no installation or entitlement. This separate future test fixture represents that state:

```json
{
  "addonId": "addon.arcanum",
  "source": "sideload",
  "provenanceTier": "sideloaded-unverified",
  "verificationState": "unverified",
  "installed": false,
  "enabled": false,
  "status": "available",
  "grantedCapabilities": [],
  "recommendedGrantPresetIds": [],
  "privateProviderProfileIds": [],
  "notes": [
    "Unvalidated design fixture; discovery grants no authority."
  ]
}
```

Only a separate installation review may populate `AddOnInstallation.grantedCapabilities`. The following is a future transition test vector, not current state or approval:

```json
{
  "addonId": "addon.arcanum",
  "source": "sideload",
  "provenanceTier": "sideloaded-unverified",
  "verificationState": "unverified",
  "installed": true,
  "enabled": false,
  "status": "installed",
  "grantedCapabilities": [
    {
      "capability": "agent-delegation",
      "granted": true,
      "scope": "workspace",
      "revocationBehavior": "hard-stop"
    },
    {
      "capability": "notifications",
      "granted": true,
      "scope": "self",
      "revocationBehavior": "degrade"
    }
  ],
  "recommendedGrantPresetIds": [],
  "grantRecommendationSource": "manual",
  "privateProviderProfileIds": [],
  "notes": [
    "Future reviewed-installation test vector; enablement remains separate."
  ]
}
```

`filesystem`, `shell`, `providers`, `archive-read`, and `archive-intake-write` are omitted. Adding any one requires a separate necessity argument, an updated manifest with `granted: false`, capability review, route tests, and a new proposal digest. A host-selected provider used by a retained delegation owner must not automatically become an add-on grant or provider credential.

## Runtime profile

The target browser projection is a new host-owned, redacted add-on response, not the existing generated `native-skill.json` and not a current capability:

```text
profileId
profileVersion
addonVersion
sdkVersion
publicCapabilityRefsAndVersions
availability
degradedReasons
requiredGrantNames
supportedOperations
concurrencyCeiling
stopCeiling
loopCeiling
opaqueInstallationRef
provenanceDigest
```

Workspace paths, runtime paths, executable paths, environment variables, provider credentials, bridge tokens, capability tokens, private identities, private schemas, registrar or ledger commands, prompts, and raw evidence paths remain outside this response.

## Secret boundary, including the Alpha exception

Manifests, profiles, proposals, events, receipts, artifacts, screenshots, diagnostics, and argv must contain no provider credentials, scoped route-capability tokens, wallet secrets, private keys, raw private paths, or private DomainSpec/Saturn material.

The current Alpha exception remains intact: an operator-configured bridge target may persist its bridge token and capability-bootstrap token in the local Chrome extension profile so that the selected target survives restart. Clearing the bridge override removes that local record.

That exception does not extend to:

- raw scoped route-capability tokens, which remain runtime-only;
- provider credentials, which remain in bridge process memory or its exported environment;
- add-on manifests, profiles, proposals, events, artifacts, logs, screenshots, or repository files.

Binding: `ALPHA_RUNTIME_BOUNDARY.md#Extension-Boundary`, `#Generated-And-Local-State`.

## Proposal, approval, and Augmentor boundary

Augmentor may:

- classify unmatched ordinary language after explicit command routing;
- render proposal bytes and their digest;
- collect edit, decline, clarification, or approval intent;
- project owner-returned state and result references.

Augmentor may not validate or persist approval, grant authority, create run truth, schedule work, infer completion, or own artifacts or memory.

A future `StrategyProposal` must bind canonical exact bytes for:

```text
proposalId
schemaVersion
requestRef
normalizedIntent
publicCapabilityRefsAndVersions
boundedInputsAndOutputs
children
dependencyWaves
gates
stopAndLoopCeilings
expectedHandleAndArtifactTypes
requiredPermissions
runtimeProfileRefAndVersion
expiration
sha256
```

Preview, edit, decline, and pre-approval clarification must create zero owner calls, registrations, run/action/child records, processes, or file writes. Editing any byte creates a new digest. The host route owner—not Augmentor—must validate and persist approval of the current digest, approver, proposal version, runtime profile, reviewed grants, expiry, and replay key.

Immediately before launch, the host revalidates all bound facts. Any mismatch creates zero starts and requires a new proposal.

## Resolver-to-owner proof chain

The enforceable separation is:

```text
side-effect-free deterministic proposal/capability resolution
  -> authenticated bridge request
  -> scoped route-capability gate
  -> host validation and persisted exact approval
  -> retained provider/delegation execution owner
  -> persisted owner run/action/artifact state
  -> redacted owner-state projection
```

Additional rules:

1. Deterministic resolution and validation make no provider call and establish no execution.
2. Every JSON bridge request requires bridge authentication.
3. Every privileged Arcanum route also requires its declared scoped capability token.
4. Route registration, HTTP success, authentication success, token success, or approval persistence is not execution proof.
5. Only the retained execution owner may report that an operation started.
6. Terminal state comes from persisted owner state, never from HTTP status, UI events, notification delivery, or cached Augmentor state.
7. Unreachable owner state projects as `Unknown`, never inferred success.
8. `tools/arcanum` remains a deterministic resolver, validator, handoff, and legacy-compatibility surface; it is not a model executor.

## Proposed route contract

These are exact future route candidates, not implemented endpoints:

| Method and path | Scoped capability | Primary behavior owner | Result ceiling |
|---|---|---|---|
| `GET /addons/arcanum/runtime-status` | `addon-runtime-read` | Add-on delegation host/status service | Redacted profile only |
| `POST /addons/arcanum/proposals/preview` | `addon-runtime-read` | Host proposal service using deterministic resolution | Proposal bytes; zero execution |
| `POST /addons/arcanum/approvals` | `addon-runtime-control` | Host approval owner | Persisted approval record only |
| `POST /addons/arcanum/runs` | `addon-record-write` | Add-on delegation host/service | Owner registration reference, not completion |
| `GET /addons/arcanum/runs/:runHandle` | `addon-record-read` | Delegation record owner | Persisted owner state |
| `POST /addons/arcanum/runs/:runHandle/children/:childHandle/clarifications` | `addon-record-write` | Delegation child-interaction owner | Delivery acknowledgement, not child progress |
| `GET /addons/arcanum/artifacts/:artifactHandle` | `addon-record-read` | Existing delegation artifact owner | Artifact read only |

The implementation owner must determine whether existing scoped capabilities are sufficient. A new capability is permitted only if route semantics cannot safely use the existing token vocabulary and consistency tests prove the addition. No second listener, authentication stack, token minter, provider fabric, scheduler, or artifact store is permitted.

Bindings: `ALPHA_RUNTIME_BOUNDARY.md#Bridge-Boundary`, `#Route-Owners`; `MODULE-OWNERSHIP.md#Host-Route-Contract`.

## State, child, and result projections

Proposed event progression:

```text
proposal.previewed
  -> approval.required
  -> approval.accepted
  -> launch.validated
  -> action.started | action.blocked | action.failed | action.succeeded
  -> run.joined | run.partially_joined
```

Events carry opaque `runHandle`, `actionHandle`, `childHandle`, owner status, timestamp, and optional `artifactHandle`, `blockerRef`, and evidence reference. They are projections; they do not create terminal truth.

A clarification addressed to child A must use A’s opaque owner handle. It must not reparent A, modify B, deliver into the parent conversation, or infer that A acted. Reload must query host owner records. Existing chat forks, cards, and delegation records are reusable primitives, not proof that this composition exists.

Result actions remain independent:

```text
open
!= attach-to-chat
!= consume-into-follow-up
!= request-memory-intake-review
```

None closes the run, alters a sibling, changes owner history, or admits content to memory automatically.

## Distinct proof and authority terms

These are integration-local applications of the Arcanum contract/schema/artifact boundaries, not new Arcanum-wide definitions.

| Term | Meaning | Owner | Gate and non-equivalence |
|---|---|---|---|
| Receipt | Operation/result record containing inputs, owner, outcome, timestamps, and references | The operation owner | Records what an operation reported; not observability, evidence sufficiency, readiness, promotion, or release |
| Observability | Structured telemetry about runtime behavior and transitions | Runtime/observability owner | Supports inspection; raw telemetry is not automatically selected claim evidence |
| Evidence | Integrity-bound material selected to support a named claim | Evidence/validation owner | Must bind claim, source, and method; schema shape or existence alone is insufficient |
| Readiness | Explicit acceptance decision over a required evidence set and unresolved blockers | Product acceptance owner | Cannot be inferred from a receipt, manifest validation, unit test, or browser launch |
| Promotion | Owner-approved authority or lifecycle transition that admits a candidate into an accepted product/canonical stage | Owning promotion route | Requires target, selected evidence, approval, and validation; is not release |
| Release | Packaging and distribution of an already promoted product artifact under release policy | Product release owner | Happens only after independent promotion and release gates |

Bindings: `arcanum/definitions/DEFINITIONS.md#DEF-ARC-CONTRACT`, `#DEF-ARC-SCHEMA`, `#DEF-ARC-DEVELOPMENT-ARTIFACT`, `#DEF-ARC-PROMOTION-PATCH`.

## Distinct lifecycle operations

| Operation | Exact effect | Forbidden collapse |
|---|---|---|
| Disable | Set product add-on disabled, reject new launches, quarantine further calls, preserve redacted owner state | Does not delete bytes, cancel external work by assertion, uninstall, roll back, refresh Bootstrap packages, promote, or release |
| Uninstall | Disable first; revoke product grants and scoped-token access; remove only add-on-owned installed bytes/config according to product policy; retain or explicitly dispose of redacted owner history under its owner | Must not invoke Bootstrap removal, rewrite generated Arcanum packages, erase external owner records silently, or claim active work cancelled |
| Product rollback | Restore a pinned prior product manifest, adapter, and runtime-profile artifact; preserve owner records; reconcile historical state; rerun compatibility and lifecycle tests | Does not restore generated Arcanum packages or imply release rollback succeeded |
| Bootstrap refresh/restore | Bootstrap-managed regeneration from pinned public source, selection, script hash, and explicit overwrite approval | Must not be performed by add-on uninstall or direct product file copying |
| Promotion | Admit an accepted candidate through the product promotion owner after readiness evidence passes | Does not package or distribute |
| Release | Package and distribute the promoted product artifact after release-specific verification | Does not substitute for promotion or readiness |

Disable must remain possible if uninstall or rollback fails. A Bootstrap `--force` refresh or restoration requires separate explicit approval and must never be implied by product enablement, update, uninstall, or rollback.

## Exact implementation dependency sequence and acceptance gates

| Step | Dependency | Acceptance gate |
|---|---|---|
| 1 | Confirm corrected target and refresh product `dev` | Record refreshed commit; re-resolve every SDK, bridge, approval, delegation, chat, UI, and lifecycle selector |
| 2 | Produce a no-write Bootstrap canonical-versus-consumer manifest | Pin source identity, bootstrap hash, selected packages, runtime profiles, and generated hashes; no writes observed |
| 3 | Obtain separate approval for selected generated-package refresh | Subagent Strategy, Whisper, Orchestrate, and support bytes match pinned canonical provenance |
| 4 | Freeze public/private/secret and owner maps | No private DomainSpec/Saturn bytes, second owners, raw secrets, or nested model CLI |
| 5 | Persist the complete manifest fixture and validator test | `validateAddOnManifest(fixture, {source: "sideload"})` returns no errors; discovery leaves installation, enablement, and grants false/empty |
| 6 | Implement reviewed installation/grant transitions | Requested `granted:false` objects remain distinct from host-reviewed `grantedCapabilities`; revoke and enable tests pass |
| 7 | Implement named routes through the existing bridge composition | Every route declares method, path, owner, scoped capability, inputs, redaction, resources, and focused fail-closed tests |
| 8 | Implement redacted runtime status and deterministic resolution | Deterministic resolution makes zero provider/model calls; profile exposes no secret or raw path |
| 9 | Implement canonical proposal bytes and host approval persistence | Preview/edit/decline create zero state; stale digest fails; approval precedes exactly-once registration; replay creates zero additional starts |
| 10 | Implement stable native Strategy and Whisper adapters | Each binds to a real public owner operation; missing operation creates zero spawn attempts; no Hermes/OpenCode substitution |
| 11 | Implement owner-backed run/action/child state | HTTP/auth success is not terminal truth; reload reconstructs owner state; unreachable owner renders `Unknown` |
| 12 | Implement child clarification | A-addressed clarification reaches A only and leaves parent/B unchanged |
| 13 | Implement independent result actions | `open`, `attach`, `consume`, and `request-memory-intake-review` mutate only their owning domains |
| 14 | Implement disable, uninstall, product rollback, and Bootstrap-managed restore tests | Each lifecycle operates independently; disable blocks new launches even when another lifecycle fails |
| 15 | Run deterministic repository and security gates | Focused SDK/bridge/delegation/router/session/lifecycle tests, browser-first suite, security pipeline, pre-release scan, and Alpha verification pass |
| 16 | Run literal browser acceptance fixture | All future-witness observations below are captured from owner-backed state on refreshed source |
| 17 | Decide readiness | Acceptance owner evaluates the complete evidence bundle; receipts or browser launch alone cannot pass |
| 18 | Decide promotion | Promotion owner admits or rejects the exact candidate independently |
| 19 | Decide release | Release owner packages/distributes only the promoted, release-verified artifact |

## Future Strategy plus Whisper acceptance fixture

Retain this literal route solely as a future acceptance fixture:

> Have Strategy assess whether this release plan needs parallel review, and have Whisper draft the concise operator notice. Keep both separate.

It is not runnable now because the Strategy package is absent, Whisper is drifted and lacks a ResonantOS adapter, the product branch is stale, and no Arcanum proposal, approval, route, clarification, reload, disable, uninstall, or rollback witness exists.

Required future observations:

1. Explicit commands resolve before Arcanum eligibility classification.
2. Proposal `P1/D1` shows two bounded children and “no actions started.”
3. Preview creates no run, child, process, file write, registration, or provider call.
4. Editing creates `D2`; approval of `D1` creates zero starts.
5. Host validation persists approval of the current digest before exactly-once registration.
6. Two distinct retained-owner correlation IDs are returned only after actual owner starts.
7. Strategy binds only to a real Subagent Strategy owner operation.
8. Whisper binds only to a real Whisper owner adapter.
9. Missing Strategy produces `Blocked(missing-owner-operation)` and zero substitution/spawn attempts.
10. Parent chat remains responsive while owner work is active.
11. A-only clarification reaches A and not parent/B.
12. Independent A `Blocked` and B `Succeeded` states may coexist; a dependent gate remains blocked.
13. Reload reconstructs identical state from host records.
14. Opening B does not attach, consume, close, promote, or admit it to memory.
15. Explicit B-only attachment or consumption leaves A, siblings, lifecycle, and memory unchanged.
16. Disable rejects a new launch.
17. Uninstall, product rollback, and Bootstrap restore are tested separately.
18. Screenshots, diagnostics, events, argv, receipts, and artifacts reveal no forbidden secrets or private material.

Until every observation is witnessed, the correct claim is: retained owner seams and an implementation candidate have been identified; no working Arcanum add-on or browser-valued two-child route exists.

## Required deterministic validation

- Manifest validation rejects unknown enums, undeclared capabilities, invalid isolation, secret/private markers, default trust, and unsupported runtime claims.
- Catalog discovery proves `installed:false`, `enabled:false`, and empty reviewed grants.
- Grant tests distinguish requested, reviewed, denied, revoked, enabled, and disabled states.
- Bridge tests prove authentication and scoped-token enforcement separately.
- Resolver tests prove zero provider/model calls.
- Proposal tests prove complete-byte digest binding and zero preview mutation.
- Approval tests prove persistence before execution, expiry/profile/grant invalidation, and replay failure.
- Adapter tests prove stable native operations, pinned roots, minimal environment, bounded output, and zero fallback substitution.
- State tests prove HTTP success is not execution proof, owner-backed terminal truth, reload fidelity, and `Unknown` reconciliation.
- Child tests prove handle-scoped clarification and sibling/parent isolation.
- Consumption tests prove open, attach, consume, and intake review are distinct.
- Lifecycle tests independently exercise disable, uninstall, product rollback, and Bootstrap-managed restore.
- Security tests cover stored-token exception, runtime-only scoped tokens, provider credentials, private markers, diagnostics, logs, artifacts, screenshots, and argv.
- Repository gates include focused `src/sdk/addons/*.test.ts`, focused bridge/delegation/router/session/lifecycle tests, `npm run test:browser-first`, `node scripts/security-pipeline/run-check.mjs`, `npm run pre-release:scan`, and `npm run verify:alpha`.

## Degraded modes

- Bridge unavailable: read-only/unavailable projection; no approval or execution.
- Bridge authenticated but scoped capability missing: fail closed; no owner call.
- Required add-on grant denied or revoked: preview may remain visible; execution blocked.
- Generated package absent or provenance mismatched: `Unavailable` or `Incompatible`; no nested CLI fallback.
- Strategy absent: Strategy action blocked with zero attempts; Whisper may proceed only if the approved proposal declared independence.
- Whisper absent: symmetric behavior.
- Owner capacity unavailable: report `Blocked` or `Unknown`; Augmentor must not create a queue.
- Partial completion: preserve independent owner results.
- Reconciliation failure: `Unknown`, never cached success.
- Runtime/profile/grant drift: invalidate the proposal digest and require new approval.
- Mid-run revocation: quarantine further calls; do not claim cancellation until the execution owner acknowledges it.
- Product rollback failure: remain disabled; do not rewrite owner history.
- Bootstrap restore unavailable: product lifecycle remains separate and must not copy generated bytes directly.

## Owner decisions still required

1. Confirm `../workspace-resonant` as the corrected target.
2. Approve the refreshed product commit as the implementation baseline.
3. Approve the exact Bootstrap selection and any `--force` refresh separately.
4. Approve or reject the minimal two-grant manifest fixture after validation.
5. Name the product owners for proposal/approval routes and Arcanum adapter behavior.
6. Decide whether Strategy and Whisper expose stable native operations without nested model CLI.
7. Define retention policy for redacted owner history after uninstall.
8. Define independent readiness, promotion, and release authorities.

## Kill criteria

Kill execution and retain at most unavailable preview/status if any of these persists:

- no stable public native Strategy or Whisper operation;
- nested model CLI is required;
- the manifest cannot validate with the minimal reviewed capability set;
- private bytes or forbidden secrets enter product/browser surfaces;
- Augmentor must own validation, approval persistence, scheduling, execution, or terminal state;
- preview or edit mutates owner state;
- approval cannot bind all launch inputs;
- bridge authentication and scoped capability checks cannot fail closed;
- HTTP success must be treated as execution proof;
- child clarification cannot remain isolated;
- reload cannot reconstruct owner truth;
- disable cannot block new launches independently;
- uninstall implicitly removes Bootstrap-managed packages;
- product rollback or Bootstrap restore lacks pinned, tested artifacts;
- the refreshed-branch browser fixture cannot demonstrate owner-backed value.

STATUS: pass
VALIDATION: pass
BLOCKERS: []
ARTIFACTS: [synthesis-revised.md]
