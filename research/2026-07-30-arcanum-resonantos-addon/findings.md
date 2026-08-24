# Arcanum as a ResonantOS add-on — findings

## Recommendation and claim ceiling

Retain the proposed integration only as **`BUILD-FROM-OWNED + NOVEL-ATTEMPT`**:

1. **Arcanum Bootstrap** remains the sole installer, selector, refresher, and restorer of generated public Arcanum packages in the consumer workspace.
2. **ResonantOS** remains the sole product owner of add-on discovery and installation, reviewed grants, bridge authentication and routes, provider/delegation execution, run truth, artifacts, secrets, disable/uninstall/product rollback, readiness, promotion, and release.
3. **Augmentor** is only the conversational projection: after explicit-command routing, it may classify eligible ordinary language, display immutable proposal bytes and their digest, capture edit/decline/clarification/approval intent, and project owner-returned state and result references.

This is an implementation-usable research contract, not authorization to implement. The requested `../workspace-resonantos` path is absent; the corrected `../workspace-resonant` target still needs owner confirmation; its nested product checkout is stale; the manifest fixture is unvalidated; and no current Arcanum add-on, Arcanum product routes or adapters, exact-approval implementation, two-child browser witness, readiness decision, promotion, or release exists. [Synthesis: `synthesis-revised.md#Recommendation-and-claim-ceiling`, `#Current-evidence-and-missing-product-ledger`; research: `research.md#Agent-1`, `#Agent-2`, `#Agent-3`; underlying: `../workspace-resonant/AGENTS.md:3-13`, `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Normative-Boundary`, `docs/architecture/MODULE-OWNERSHIP.md#Alpha-Ownership`, repository search over `public/addons/`, `src/sdk/addons/`, `browser-first/host/`, and extension `src/lib/`]

## Expected future end state

After every prerequisite and acceptance gate below passes, one ResonantOS-native add-on exposes a deliberately selected set of Bootstrap-managed public Arcanum capabilities through the existing authenticated loopback host. An unmatched ordinary-language request can yield a side-effect-free, digest-bound proposal. A human can edit, decline, clarify, or approve the exact bytes. The host—not Augmentor—validates and persists approval, enforces bridge authentication and scoped capabilities, registers exactly once, invokes retained execution owners, persists run/action/child/artifact truth, and returns opaque redacted projections. The parent conversation remains usable. Each result remains independently openable, attachable to chat, consumable into a follow-up, or eligible for a separate memory-intake review. No third runtime is embedded. [Synthesis: `synthesis-revised.md#Expected-future-end-state`, `#Resolver-to-owner-proof-chain`, `#State-child-and-result-projections`; research: `research.md#Required-interaction-sequence`; underlying: `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Normative-Boundary`, `#Bridge-Boundary`, `#Route-Owners`; `browser-first/host/addon-delegation-service.mjs#executeDelegationRecord`; `chat-session-store.js`; `archive-review-host-service.mjs`]

## Current-versus-target ownership map

| Concern | Current evidence | Target contract and retained owner |
|---|---|---|
| Target location | `../workspace-resonantos` is absent. `../workspace-resonant` is an observed non-Git workspace root; owner confirmation is outstanding. | Confirm the corrected root before any mutation. Do not infer product deployment from workspace files. |
| Product baseline | Nested `2.0.0-alpha` checkout is `dev@6f92af7b32b17d2eef66230d463eb8b6a21a98f7`, seven cached commits behind `origin/dev@3b07e635d596c18f9a047ef5921892acc7cba4ff`. | Refresh `dev`, record the new commit, then re-resolve all SDK, bridge, approval, delegation, chat, UI, and lifecycle selectors. |
| Public Arcanum packages | Generated packages, `.arcanum`, observability, and `tools/arcanum` exist at the workspace root; selection currency is unproven. Strategy is absent, Whisper drifted, Orchestrate materially drifted. | Bootstrap alone owns selection, generation, refresh, provenance, overwrite approval, and restoration. |
| Manifest/catalog | SDK validation and catalog-only registry owners exist; no Arcanum manifest exists. | ResonantOS validates and catalogs one `addon.arcanum` manifest. Discovery must not install, enable, or grant. |
| Installation/grants | `AddOnInstallation`, `CapabilityGrant`, and review UI exist; no Arcanum binding exists. | Product installation owner records installation, enablement, reviewed grants, denial, revocation, and disablement separately. |
| Bridge/security | The Alpha is MV3 extension plus authenticated loopback Node bridge with scoped route-capability tokens. | Reuse the listener, authentication stack, token owner, and capability gates; add only named Arcanum route behavior. |
| Execution/provider | Current delegation bodies support Hermes/OpenCode, not Strategy/Whisper. Provider host owns profiles and credentials. | Add stable native Strategy and Whisper adapters only if they bind real public owner operations; retain provider/delegation execution and scheduling owners. |
| Conversation | Explicit command router, chat/session hydration, cards, and attachments exist. | Augmentor classifies only unmatched language and projects proposal/run/result state; chat/session owners retain conversation and attachment truth. |
| Proposal/approval | No Arcanum proposal, canonical digest, replay guard, or approval persistence exists. | A host-owned contract creates canonical bytes, validates and persists exact approval, revalidates before launch, and enforces replay safety. |
| Runs/children/artifacts | Delegation records, artifact reads, chat forks, and cards are reusable primitives, not the requested composition. | Host delegation owns opaque run/action/child handles, clarification, joins, reload reconciliation, terminal truth, and artifacts. |
| Memory | Archive intake/review/promotion owners exist. | Results may only request a separate intake review; no automatic attachment, consumption, admission, or promotion. |
| Lifecycle | Product vocabulary exists; no Arcanum operational witness exists. | Product owners handle disable, uninstall, and product rollback; Bootstrap separately handles generated-package restore. |

Bindings for every row: `synthesis-revised.md#Current-evidence-and-missing-product-ledger`, `#Owner-and-use-mode-map`; `research.md#Exact-current-state-matrix`, `#Exact-evidence-and-selector-status`, `#Current-versus-missing-matrix`. Underlying selectors: `arcanum/spells/arcanum-bootstrap/README.md:10-18,42-88,92-139,151-181`; `arcanum/tools/bootstrap_arcanum.sh:100-161,237-355,383-464,507-665,695-758,783-900,1750-1935`; `src/core/contracts.ts#CapabilityGrant`, `#AddOnInstallation`; `src/sdk/addons/contracts.ts#ADDON_SDK_VERSION`; `validation.ts#validateAddOnManifest`; `registry.ts#createAddOnRegistrySnapshot`; `docs/architecture/ADR-023-addon-repository-registry-model.md#Registry-V0-In-Core`; `docs/architecture/ADR-006-addon-runtime-sdk.md#Capability-Grant-Lifecycle`; `browser-first/host/addon-delegation-host-service.mjs#addonDelegationRoutes`; `browser-first/host/addon-delegation-service.mjs#executeDelegationRecord`.

## Options and verdicts

| Option | Verdict | Reason |
|---|---|---|
| Three retained-owner layers | **Select conditionally** | Reuses Bootstrap, product, and conversational owners while isolating novel adapter/proposal work. |
| Repository-generated skills represented as an installed product add-on | **Kill** | Package presence is not manifest, grant, bridge, browser, or product-install evidence. |
| Embedded Arcanum runtime / third Alpha component | **Kill** | Contradicts the MV3-extension-plus-loopback-bridge boundary. |
| Nested `codex exec`, Claude, or another model-backed CLI | **Kill** | The initial route requires native owner operations; `tools/arcanum` is deterministic support, not a model executor. |
| Augmentor-owned install, registry, approval database, router, queue, scheduler, execution, run truth, artifacts, sessions, secrets, or memory | **Kill** | Duplicates retained authorities and destroys reload-verifiable owner truth. |
| Broad exposure of all generated skills | **Defer** | Current installed selection and catalog currency are unverified. |
| Necronomicon / automatic memory integration | **Defer** | Harness state and explicit consent/ownership mappings are absent. |
| Strategy + Whisper product execution | **Kill for current state; defer** | Strategy is absent, Whisper is drifted, and neither has the required product adapter. |
| Strategy + Whisper browser route | **Retain as future acceptance fixture only** | It is a non-vacuous target witness, not present evidence. |
| Preview/status-only degraded surface | **Permit conditionally** | It must be marked unavailable and technically incapable of execution. |

[Synthesis: `synthesis-revised.md#Options-and-kill-decisions`; research: `research.md#Killed-shapes`, `#Claim-ceilings`; underlying: `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Normative-Boundary`; `arcanum/runtime/orchestrate/SKILL.md:1-142`; `../workspace-resonant/.arcanum/runtime/adapters/native-skill.json`; `docs/architecture/ADR-023-addon-repository-registry-model.md#Registry-V0-In-Core`]

## Selected three-layer topology

```text
Arcanum Bootstrap
  owns public package selection, generation, provenance, refresh, restore
                |
                | pinned public capability and provenance facts
                v
ResonantOS native add-on and existing loopback host
  own manifest, reviewed grants, routes, approval persistence,
  provider/delegation execution, run truth, artifacts, lifecycle, release
                |
                | opaque redacted proposal/run/result projections
                v
Augmentor
  classifies unmatched language, captures human intent, presents owner truth
```

No upward or sideways arrow transfers ownership: product enablement cannot refresh Bootstrap packages; add-on uninstall cannot remove them; Augmentor approval intent cannot grant authority; a proposal, receipt, HTTP response, UI event, or browser launch cannot establish execution, readiness, promotion, or release. [Synthesis: `synthesis-revised.md#Owner-and-use-mode-map`, `#Distinct-proof-and-authority-terms`, `#Distinct-lifecycle-operations`; underlying: `arcanum/definitions/DEFINITIONS.md#DEF-ARC-CONTRACT`, `#DEF-ARC-SCHEMA`, `#DEF-ARC-DEVELOPMENT-ARTIFACT`, `#DEF-ARC-PROMOTION-PATCH`; `docs/architecture/MODULE-OWNERSHIP.md#Alpha-Ownership`]

## Initial public capability catalog

| Public operation | Present state | Contract |
|---|---|---|
| `subagent-strategy.preview` | Absent product operation | Pure canonical proposal construction; zero provider calls, registrations, processes, or writes. |
| `subagent-strategy.execute` | Not available now | May exist only after current generated package plus stable native owner adapter are proven. |
| `whisper.execute` | Not available now | May exist only after current generated package plus stable ResonantOS owner adapter are proven. |
| `run.status` | Arcanum mapping absent | Query persisted host-owner records; unreachable state is `Unknown`. |
| `run.clarify` | Absent | Deliver by opaque child handle with parent/sibling isolation. |
| `artifact.read` | General precedent exists; mapping absent | Read through existing artifact owner using an opaque reference. |

`dispatch-spec`, current `orchestrate`, and `tools/arcanum` are internal support, never browser product cards or model executors. Necronomicon, legacy adapters, `codex-exec`, and `codex-bypass` are outside the initial surface. If stable native Strategy or Whisper operations require nested model CLI, kill execution and retain unavailable preview/status only. [Synthesis: `synthesis-revised.md#Initial-public-capability-catalog`; research: `research.md#Smallest-defensible-initial-catalog`; underlying: `arcanum/arcana/subagent-strategy/SKILL.md:15-30,82-99,118-182`; `arcanum/spells/whisper/README.md:10-21,46-78,100-109,234-255`; `arcanum/runtime/orchestrate/SKILL.md:1-142`; `../workspace-resonant/.arcanum/runtime/adapters/native-skill.json`]

## Exact product contracts

### Add-on and grant contract

The sole initial design fixture is `addon.arcanum`, version `0.1.0`, SDK `0.1.0`, category `orchestration`, runtime type `agent-addon`, provenance `sideloaded-unverified`, isolation `host-mediated-agent`, with degraded mode and reviewed grants required. Its surfaces are `arcanum-panel`, `arcanum-tool-action`, and `arcanum-run-monitor`. Its only initial requested capabilities are:

- `agent-delegation`, `scope: workspace`, `revocationBehavior: hard-stop`, `granted: false`;
- `notifications`, `scope: self`, `revocationBehavior: degrade`, `granted: false`.

The manifest is an **unvalidated design fixture** until `validateAddOnManifest(fixture, {source: "sideload"})` returns no errors. Discovery must produce `installed:false`, `enabled:false`, and `grantedCapabilities:[]`. A separate manual review may later create `installed:true`, `enabled:false`, with reviewed grants. Enablement remains a separate transition. `filesystem`, `shell`, `providers`, `archive-read`, and `archive-intake-write` are excluded; each would require a necessity argument, a new ungranted request, review, route tests, and a new proposal digest. [Synthesis: `synthesis-revised.md#Complete-validator-shaped-manifest-design-fixture`, `#Requested-capabilities-versus-reviewed-installation-grants`; underlying: `src/core/contracts.ts#AddOnManifest`, `#CapabilityGrant`, `#AddOnSurface`, `#AddOnProvenance`, `#AddOnRuntimeIsolation`; `src/sdk/addons/contracts.ts#AddOnSdkManifest`, `#ADDON_CAPABILITIES`; `src/sdk/addons/validation.ts#validateAddOnManifest`]

### Bridge and route contract

Every JSON request uses existing bridge authentication; every privileged route also requires its declared scoped route-capability token. Reuse the existing listener, authentication stack, token minter, provider fabric, scheduler, delegation records, and artifact store. Proposed endpoints are future contracts, not implemented routes:

| Method and route | Scoped capability | Owner | Result ceiling |
|---|---|---|---|
| `GET /addons/arcanum/runtime-status` | `addon-runtime-read` | Add-on delegation host/status owner | Redacted profile only |
| `POST /addons/arcanum/proposals/preview` | `addon-runtime-read` | Host proposal owner + deterministic resolver | Exact proposal bytes; zero execution |
| `POST /addons/arcanum/approvals` | `addon-runtime-control` | Host approval owner | Persisted approval record only |
| `POST /addons/arcanum/runs` | `addon-record-write` | Delegation host/service | Registration reference, not completion |
| `GET /addons/arcanum/runs/:runHandle` | `addon-record-read` | Delegation record owner | Persisted owner state |
| `POST /addons/arcanum/runs/:runHandle/children/:childHandle/clarifications` | `addon-record-write` | Child-interaction owner | Delivery acknowledgement, not progress |
| `GET /addons/arcanum/artifacts/:artifactHandle` | `addon-record-read` | Existing artifact owner | Artifact read only |

The implementation owner must prove whether existing scoped capabilities suffice before adding token vocabulary. Route registration, HTTP success, authentication, token acceptance, or approval persistence is never start or terminal proof. [Synthesis: `synthesis-revised.md#Proposed-route-contract`, `#Resolver-to-owner-proof-chain`; underlying: `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Bridge-Boundary`, `#Route-Owners`; `docs/architecture/MODULE-OWNERSHIP.md#Host-Route-Contract`; `browser-first/host/bridge-capability-tokens.mjs`; `browser-first/host/addon-delegation-host-service.mjs#addonDelegationRoutes`]

### Runtime-profile contract

The browser-safe host response contains exactly: `profileId`, `profileVersion`, `addonVersion`, `sdkVersion`, `publicCapabilityRefsAndVersions`, `availability`, `degradedReasons`, `requiredGrantNames`, `supportedOperations`, `concurrencyCeiling`, `stopCeiling`, `loopCeiling`, `opaqueInstallationRef`, and `provenanceDigest`.

It excludes workspace/runtime/executable paths, environment variables, provider credentials, bridge and capability tokens, private identities/schemas, registrar or ledger commands, prompts, and raw evidence paths. It is a new host-owned projection, not the generated `native-skill.json`, and package/config presence cannot be projected as installed-current, approved, running, or complete. [Synthesis: `synthesis-revised.md#Runtime-profile`; research: `research.md#Runtime-profile-facts-Augmentor-may-project`; underlying: `../workspace-resonant/.arcanum/runtime/adapters/native-skill.json`; `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Generated-And-Local-State`]

### Proposal, approval, and command-precedence contract

Explicit slash, control, browser, and delegation commands resolve first through `createSidePanelCommandRouter.respondToCommand`. Only unmatched ordinary language reaches Arcanum eligibility classification. [Research: `research.md#Exact-evidence-and-selector-status`, `#Required-interaction-sequence`; underlying: `browser-first/resonantos-side-panel-extension/src/lib/side-panel-command-router.js#createSidePanelCommandRouter.respondToCommand`]

Canonical `StrategyProposal` bytes bind: `proposalId`, `schemaVersion`, `requestRef`, `normalizedIntent`, `publicCapabilityRefsAndVersions`, `boundedInputsAndOutputs`, `children`, `dependencyWaves`, `gates`, `stopAndLoopCeilings`, `expectedHandleAndArtifactTypes`, `requiredPermissions`, `runtimeProfileRefAndVersion`, `expiration`, and `sha256`.

Preview, edit, decline, and pre-approval clarification create zero owner calls, registrations, run/action/child records, processes, provider calls, or file writes. Any byte edit creates a new digest. Augmentor captures human intent only. The host validates and persists `proposalDigest`, `approver`, `proposalVersion`, `runtimeProfileRefAndVersion`, reviewed grants, expiry, and replay key. Immediately before launch it revalidates all bound facts. Drift or mismatch creates zero starts and requires a new proposal. Registration is exactly once by `(proposalDigest, actionId)`; replay creates no additional start. [Synthesis: `synthesis-revised.md#Proposal-approval-and-Augmentor-boundary`, `#Resolver-to-owner-proof-chain`; research: `research.md#StrategyProposal-and-approval`; underlying precedent: Inventory `augmentor-subagent-strategy-integration-research-result-synthesis#public-neutral-adapter-and-runtime-profile-contract`; analogous product approval owner noted in `research.md#Current-versus-missing-matrix`]

### Run, child, state, event, artifact, and result contract

The host owns opaque `runHandle`, `actionHandle`, `childHandle`, and `artifactHandle` identities. The projected event progression is:

```text
proposal.previewed
  -> approval.required
  -> approval.accepted
  -> launch.validated
  -> action.started | action.blocked | action.failed | action.succeeded
  -> run.joined | run.partially_joined
```

Events carry the relevant opaque handles, owner status, timestamp, and optional `artifactHandle`, `blockerRef`, and evidence reference. Only persisted owner state supplies terminal truth; unreachable owner state is `Unknown`. Reload re-queries owner records.

The run tray is a projection keyed to those handles. It may show owner state, blockers, and artifact references but must not create a queue, schedule work, infer completion, or become a session store. A clarification to child A uses A's owner handle and must not reparent A, modify B, enter the parent chat, or imply that A acted. Parent chat remains owned and usable independently.

Result operations are intentionally non-equivalent:

```text
open
!= attach-to-chat
!= consume-into-follow-up
!= request-memory-intake-review
```

No result operation closes a run, changes sibling state or owner history, promotes content, or admits it to memory automatically. [Synthesis: `synthesis-revised.md#State-child-and-result-projections`; research: `research.md#State-event-mapping`, `#Required-interaction-sequence`; underlying: `main-workspace-addons.js#createAddonCard/createDelegationCard/renderAddOnsWorkspace`; `delegation-status.js`; `delegation-lifecycle.js`; `chat-session-store.js`; `browser-first/test/chat-session-store.test.mjs`; `archive-review-host-service.mjs`]

### File and ownership contract

| File/state family | Owner and permitted use |
|---|---|
| `.agents/skills/<selected>/`, `.arcanum/runtime/`, generated adapter profiles, `tools/arcanum` | Bootstrap-generated consumer runtime. Product may inspect pinned public provenance through the host but may not vendor, overwrite, remove, or treat these bytes as product installation. |
| `.arcanum/observability/**` | Runtime/observability owner. Browser code receives only selected redacted projections, never raw logs. |
| `public/addons/arcanum.json` or creator-owned sideload equivalent | Future product manifest fixture after validation; not a Bootstrap output. |
| Existing `src/sdk/addons/` contracts/validator/registry | Retained product schema and catalog owners; do not fork a second registry. |
| Existing `browser-first/host/` bridge/delegation composition | Retained process and route ownership; new Arcanum behavior must enter through named, capability-gated routes, not a second listener. |
| Extension/Augmentor UI state | Ephemeral/redacted projection only; not approval, run, child, artifact, secret, or memory truth. |
| External user state for installations, approvals, delegations, artifacts, and chat | Persist only through each existing product owner and retention policy. |

[Synthesis: `synthesis-revised.md#Owner-and-use-mode-map`, `#Complete-validator-shaped-manifest-design-fixture`, `#Secret-boundary-including-the-Alpha-exception`; research: `research.md#Bootstrap-versus-add-on-boundary`, `#Forbidden-imports-and-claim-ceilings`; underlying: `arcanum/tools/bootstrap_arcanum.sh:100-161,237-355,383-464,507-665,695-758,783-900,1750-1935`; `src/sdk/addons/registry.ts#createAddOnRegistrySnapshot`; `docs/architecture/MODULE-OWNERSHIP.md`; `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Generated-And-Local-State`]

## Ordinary-language-to-consumption sequence

1. The user says: “Have Strategy assess whether this release plan needs parallel review, and have Whisper draft the concise operator notice. Keep both separate.”
2. The existing command router gets first refusal. Only after no explicit route matches may Augmentor classify the request as Arcanum-eligible.
3. Augmentor asks the host for a deterministic preview. The host returns canonical `P1` bytes and digest `D1`, describing two bounded independent actions, required grants, owner operations, limits, outputs, and expected handles. The UI states “no actions started.”
4. The user may clarify, decline, or edit. Editing any byte yields `D2`; neither `D1` nor `D2` preview creates durable or execution state.
5. The user expresses approval of the exact current digest. Augmentor transmits intent; the host authenticates, checks the scoped capability, validates and persists the exact approval record, then revalidates profile, grants, expiry, provenance, operation availability, and capacity.
6. The host registers the approved actions exactly once, then invokes one retained owner operation per action. Augmentor neither schedules nor executes. If Strategy is missing, A becomes `Blocked(missing-owner-operation)` with zero substitution or spawn attempts; Whisper may proceed only if the approved proposal declared independence.
7. Two distinct correlation IDs appear only after real owner starts. The parent conversation remains responsive while the run tray projects owner state.
8. A clarification addressed to A goes only through A's opaque owner handle; parent and B remain unchanged.
9. Independent states may coexist, including A `Blocked` and B `Succeeded`; any dependent gate remains blocked. Reload reconstructs the same truth from host records.
10. The user separately chooses whether to open B, attach B to the current chat, consume B into a follow-up, or request memory-intake review. Each operation affects only its owner; none implies another.

This is the required future interaction, not current behavior. [Synthesis: `synthesis-revised.md#Future-Strategy-plus-Whisper-acceptance-fixture`; research: `research.md#Literal-two-child-fixture`; underlying: `browser-first/resonantos-side-panel-extension/src/lib/side-panel-command-router.js#createSidePanelCommandRouter.respondToCommand`; `browser-first/host/addon-delegation-service.mjs#executeDelegationRecord`; `chat-session-store.js`; public `arcanum/arcana/subagent-strategy/SKILL.md:118-182`; `arcanum/spells/whisper/README.md:234-255`]

## Lifecycle contract

1. **Install:** Bootstrap installation/refresh happens separately. Product catalog discovery grants nothing. A reviewed product installation may install the validated add-on record, still disabled, with explicit grants; enablement is separate.
2. **Update:** Refresh the product branch and revalidate selectors. Capture manifest/version/hash, Bootstrap provenance, adapter/profile versions, grants, compatibility, owner health, and a clean baseline. Revalidate manifest and adapter; widened grants require new review; invalidate outstanding proposal digests; rerun deterministic and browser witnesses.
3. **Disable:** Set the product add-on disabled, reject new launches, quarantine further calls, preserve redacted owner state, and reconcile active work from retained owners. Do not claim external work cancelled without owner acknowledgement.
4. **Uninstall:** Disable first, revoke grants and scoped-token access, and remove only add-on-owned installed bytes/config under product policy. Preserve or explicitly dispose of redacted history under its owner. Never remove Bootstrap packages or silently erase external records.
5. **Product rollback:** Restore pinned prior product manifest, adapter, and runtime profile; preserve owner records, reconcile history, and rerun compatibility/lifecycle tests. If rollback fails, remain disabled.
6. **Bootstrap restore:** Through Bootstrap only, regenerate from pinned public source, selected packages, bootstrap-script hash, and explicit overwrite/`--force` approval. Product lifecycle must not copy or rewrite generated bytes.
7. **Readiness, promotion, release:** Separate owner decisions over separate evidence gates. A receipt, manifest validation, unit test, browser launch, or successful rollback is insufficient by itself.

[Synthesis: `synthesis-revised.md#Distinct-lifecycle-operations`, `#Distinct-proof-and-authority-terms`; research: `research.md#Upgrade-and-rollback-evidence`; underlying: `arcanum/spells/arcanum-bootstrap/README.md:42-88,92-139,151-181`; `arcanum/tools/bootstrap_arcanum.sh:507-665,695-758,1750-1935`; `src/core/contracts.ts#AddOnInstallation`; `docs/architecture/ADR-006-addon-runtime-sdk.md#Capability-Grant-Lifecycle`]

## Public, private, and secret boundaries

- Product and public Arcanum surfaces may carry only public capability identifiers and public-neutral provenance/evidence vocabulary.
- Never copy DomainSpec, Saturn, `cyberAlchemy-v2`, private ledgers, private dispatch hooks, private prompts/prose, raw observability, private identities/schemas, registrar commands, or raw evidence paths into Arcanum, ResonantOS, manifests, browser state, events, diagnostics, or artifacts.
- Provider credentials, wallet secrets, private keys, scoped route tokens, and raw paths are forbidden in manifests, runtime profiles, proposals, events, receipts, artifacts, logs, screenshots, diagnostics, and argv.
- The one current Alpha exception is narrow: the operator-configured local Chrome extension profile may persist the bridge token and capability-bootstrap token so the selected bridge target survives restart. Clearing the override removes the record.
- That exception does not cover scoped route-capability tokens, which remain runtime-only, or provider credentials, which remain in bridge process memory/exported environment.
- No page-to-process/provider/filesystem authority, non-loopback service, iframe authority, ambient executable lookup, unrestricted workspace root, nested model CLI, automatic artifact intake, or automatic memory admission is allowed.

[Synthesis: `synthesis-revised.md#Secret-boundary-including-the-Alpha-exception`; research: `research.md#Forbidden-imports-and-claim-ceilings`, `#Killed-shapes`; underlying: `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Extension-Boundary`, `#Generated-And-Local-State`; `browser-first/host/bridge-capability-tokens.mjs`; public `arcanum-bootstrap` provenance contracts]

## Ordered implementation slices

1. Confirm `../workspace-resonant`; refresh product `dev`; pin the commit; re-resolve all named selectors.
2. Produce a no-write canonical-versus-consumer Bootstrap manifest with public source identity, bootstrap hash, selected package versions, runtime profiles, and generated hashes.
3. Obtain separate approval for any Bootstrap refresh; prove Strategy, Whisper, Orchestrate, and support bytes match pinned canonical provenance.
4. Freeze owner, public/private, and secret maps; reject second owners, private bytes, raw secrets, and nested model CLI.
5. Persist the complete manifest fixture and pass sideload validation; prove discovery remains uninstalled, disabled, and ungranted.
6. Implement and test separate installation, reviewed-grant, revoke, enable, and disable transitions.
7. Add named Arcanum routes through the existing authenticated bridge with scoped, fail-closed capabilities and redaction/resource contracts.
8. Implement redacted runtime status and pure deterministic proposal resolution with zero provider/model calls.
9. Implement canonical proposal bytes, host approval persistence, prelaunch revalidation, expiry/drift invalidation, exactly-once registration, and replay rejection.
10. Implement stable native Strategy and Whisper adapters; missing operations produce zero spawn attempts and no Hermes/OpenCode substitution.
11. Implement owner-backed run/action/child/artifact state, join semantics, reload reconciliation, and `Unknown`.
12. Implement handle-scoped child clarification and prove parent/sibling isolation.
13. Implement independent open, attach, consume, and memory-intake-review actions.
14. Implement independent disable, uninstall, product rollback, and Bootstrap-restore tests.
15. Run focused deterministic, security, browser-first, pre-release, and Alpha repository gates.
16. Run the literal local two-child browser fixture and capture all required owner-backed observations.
17. Ask the product acceptance owner for readiness; only then separately ask promotion and release owners.

[Synthesis: `synthesis-revised.md#Exact-implementation-dependency-sequence-and-acceptance-gates`; underlying: `src/sdk/addons/validation.ts#validateAddOnManifest`; `browser-first/host/addon-delegation-host-service.mjs#addonDelegationRoutes`; `browser-first/test/chat-session-store.test.mjs`; `scripts/security-pipeline/run-check.mjs`; `scripts/pre-release-scan.sh`; product package scripts for `test:browser-first`, `pre-release:scan`, and `verify:alpha`]

## Future literal two-child local-fixture acceptance witness

The literal input is:

> Have Strategy assess whether this release plan needs parallel review, and have Whisper draft the concise operator notice. Keep both separate.

It is **future acceptance evidence only**. It is not runnable now: Strategy is absent, Whisper is drifted and has no product adapter, the checkout is stale, the manifest is unvalidated, and proposal, approval, routes, clarification, reload, lifecycle, and browser witnesses are absent.

Acceptance requires all of the following in a local fixture with no network/provider dependency:

1. Explicit commands precede eligibility classification.
2. `P1/D1` shows two children and “no actions started.”
3. Preview creates zero run, child, process, file write, registration, owner, or provider call.
4. An edit creates `D2`; approval of `D1` causes zero starts.
5. Current-digest approval persists before exactly-once registration.
6. Distinct correlation IDs appear only after actual retained-owner starts.
7. A binds only to a real Strategy owner operation; B binds only to a real Whisper adapter.
8. Missing Strategy yields `Blocked(missing-owner-operation)` and zero substitution/spawn attempts.
9. Parent chat remains responsive.
10. A-only clarification reaches neither parent nor B.
11. A `Blocked` and B `Succeeded` may coexist while a dependent gate remains blocked.
12. Reload reconstructs identical owner state.
13. Opening B does not attach, consume, close, promote, or admit it to memory.
14. Explicit B-only attach or consume leaves A, siblings, lifecycle, and memory unchanged.
15. Disable rejects a new launch.
16. Uninstall, product rollback, and Bootstrap restore pass as distinct tests.
17. Screenshots, diagnostics, events, argv, receipts, and artifacts contain no forbidden secrets or private material.

Until every observation is captured, the only supported claim is that retained owner seams and an implementation candidate were identified. [Synthesis: `synthesis-revised.md#Future-Strategy-plus-Whisper-acceptance-fixture`; research: `research.md#Literal-two-child-fixture`, `#Browser-checks`; underlying: public `arcanum/arcana/subagent-strategy/SKILL.md:15-30,82-99,118-182`; `arcanum/spells/whisper/README.md:10-21,46-78,100-109,234-255`; current delegation routes in `browser-first/host/addon-delegation-host-service.mjs`]

## Deterministic test matrix

| Domain | Required deterministic proof |
|---|---|
| Manifest/catalog | Reject unknown enums, undeclared capabilities, invalid isolation, secrets/private markers, default trust, and unsupported runtime claims; discovery remains uninstalled, disabled, and ungranted. |
| Grants | Requested, reviewed, denied, revoked, enabled, and disabled states remain distinct. |
| Bridge | Authentication and scoped capability checks fail independently and closed; extension capability map equals gated host routes. |
| Resolver | Deterministic resolution performs zero provider/model calls. |
| Proposal | Digest binds complete canonical bytes; preview/edit/decline perform zero mutation. |
| Approval/replay | Approval persists before invocation; expiry/profile/grant/provenance drift invalidates; `(digest, actionId)` starts at most once. |
| Adapter | Stable native operations, pinned roots, minimal environment, bounded/redacted output, no secrets in argv, and no fallback substitution. |
| State/reload | HTTP success is not execution; terminal truth is owner-backed; reload is faithful; unreachable owner is `Unknown`. |
| Child | Clarification is handle-scoped; parent and sibling isolation hold. |
| Results/memory | Open, attach, consume, and intake review are independent and never automatic. |
| Lifecycle | Disable, uninstall, product rollback, and Bootstrap restore are independently exercised; disable still works when rollback fails. |
| Security | Cover the stored-token exception, runtime-only scoped tokens, provider credentials, private markers, raw paths, logs, diagnostics, screenshots, artifacts, and argv. |
| Repository gates | Focused `src/sdk/addons/*.test.ts`; focused bridge/delegation/router/session/lifecycle tests; `npm run test:browser-first`; `node scripts/security-pipeline/run-check.mjs`; `npm run pre-release:scan`; `npm run verify:alpha`. |

[Synthesis: `synthesis-revised.md#Required-deterministic-validation`; research: `research.md#Deterministic-checks`, `#Browser-checks`; underlying: `src/sdk/addons/validation.ts#validateAddOnManifest`; `browser-first/host/bridge-capability-tokens.mjs`; `browser-first/test/chat-session-store.test.mjs`; `scripts/security-pipeline/run-check.mjs`; `scripts/pre-release-scan.sh`; product package scripts]

## Degraded modes

| Condition | Required behavior |
|---|---|
| Bridge unavailable | Read-only/unavailable projection; no approval or execution. |
| Bridge authenticated, scoped capability missing | Fail closed; zero owner calls. |
| Required grant denied/revoked | Preview may remain visible; execution blocked. |
| Package absent/provenance mismatch | `Unavailable` or `Incompatible`; no nested CLI fallback. |
| Strategy absent | Strategy blocks with zero attempts; Whisper proceeds only when approved as independent. |
| Whisper absent | Symmetric behavior. |
| Owner capacity unavailable | Show `Blocked` or `Unknown`; Augmentor creates no queue. |
| Partial completion | Preserve each independent owner result. |
| Reconciliation failure | `Unknown`, never cached success. |
| Runtime/profile/grant drift | Invalidate digest and require a fresh proposal and approval. |
| Mid-run revocation | Quarantine further calls; do not claim cancellation until owner acknowledgement. |
| Product rollback failure | Remain disabled and preserve owner history. |
| Bootstrap restore unavailable | Keep product lifecycle separate; never copy generated bytes directly. |

[Synthesis: `synthesis-revised.md#Degraded-modes`; research: `research.md#Degraded-modes`; underlying: `docs/architecture/ADR-006-addon-runtime-sdk.md#Capability-Grant-Lifecycle`; `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Route-Owners`; `delegation-lifecycle.js`]

## Branch and version prerequisites

- Owner must confirm `../workspace-resonant` as the corrected target.
- Refresh the nested product checkout from stale `dev@6f92af7b32b17d2eef66230d463eb8b6a21a98f7`; record the accepted new baseline and recheck every selector. The cached seven-commit delta does not directly contradict the add-on seam but materially changes approval and live-browser certification paths.
- Pin Arcanum public source identity, Bootstrap script hash, exact selected capability list, runtime-profile versions, generated hashes, product manifest and adapter hashes, SDK version, browser runtime, and fixture inputs.
- Obtain explicit, separate approval before Bootstrap `--force`; product enablement/update/uninstall/rollback never implies generated-package mutation.
- Validate the manifest fixture before calling it valid. Prove reviewed grants and enablement separately.
- Prove stable native Strategy and Whisper operations and adapters before enabling execution.

[Synthesis: `synthesis-revised.md#Current-evidence-and-missing-product-ledger`, `#Exact-implementation-dependency-sequence-and-acceptance-gates`; research: `research.md#Stale-branch-uncertainty`, `#Drift-and-upgrade-obligations`; underlying: `git status --branch`, `git log dev..origin/dev`, `git diff dev..origin/dev`; `arcanum/tools/bootstrap_arcanum.sh:507-665,695-758`; `src/sdk/addons/validation.ts#validateAddOnManifest`]

## Risks, owner decisions, and kill criteria

### Principal risks

- **Authority duplication:** novel routes or UI may accidentally become a second installer, approval owner, scheduler, execution store, or memory path.
- **Stale-contract implementation:** the seven-commit-old checkout may produce wrong approval and browser acceptance assumptions.
- **Presence inflation:** generated skill/config bytes may be mistaken for current selection, product installation, adapter availability, execution, or readiness.
- **Grant creep:** filesystem, shell, provider, archive, or browser capabilities may be added without a proved necessity.
- **Secret/private leakage:** runtime tokens, provider credentials, paths, observability, or private pillar prose may enter browser-visible material.
- **False execution proof:** HTTP/auth/token/UI/receipt success may be treated as owner start or terminal state.
- **Lifecycle collapse:** product uninstall/rollback may mutate Bootstrap packages or erase external owner truth.

[Synthesis: `synthesis-revised.md#Recommendation-and-claim-ceiling`, `#Resolver-to-owner-proof-chain`, `#Secret-boundary-including-the-Alpha-exception`, `#Distinct-lifecycle-operations`; research: `research.md#Claim-ceilings`; underlying: `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md`; `docs/architecture/MODULE-OWNERSHIP.md`; `arcanum/tools/bootstrap_arcanum.sh`; `src/core/contracts.ts#AddOnInstallation`]

### Owner decisions still required

1. Confirm the corrected target.
2. Approve the refreshed product commit.
3. Approve exact Bootstrap selection and any forced refresh separately.
4. Approve or reject the minimal two-grant manifest after validator evidence.
5. Name product owners for proposal/approval routes and Arcanum adapter behavior.
6. Decide whether Strategy and Whisper expose stable native operations without nested model CLI.
7. Define redacted owner-history retention after uninstall.
8. Name independent readiness, promotion, and release authorities.

[Synthesis: `synthesis-revised.md#Owner-decisions-still-required`]

### Kill criteria

Kill execution and retain at most unavailable preview/status if any of these persists:

- no stable public native Strategy or Whisper operation;
- nested model CLI is required;
- the minimal manifest cannot validate;
- private bytes or forbidden secrets enter product/browser surfaces;
- Augmentor must own validation, approval persistence, scheduling, execution, or terminal state;
- preview/edit mutates owner state;
- approval cannot bind every launch input or prevent replay;
- bridge authentication or scoped capability enforcement cannot fail closed;
- HTTP success must stand in for owner-backed execution;
- child clarification cannot remain isolated;
- reload cannot reconstruct owner truth;
- disable cannot independently block new launches;
- uninstall removes Bootstrap-managed packages;
- product rollback or Bootstrap restore lacks pinned tested artifacts; or
- the refreshed-branch local browser fixture cannot demonstrate owner-backed value.

[Synthesis: `synthesis-revised.md#Kill-criteria`; research: `research.md#Killed-shapes`, `#Validation-and-witness-ceiling`; underlying: `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Bridge-Boundary`; `src/sdk/addons/validation.ts#validateAddOnManifest`; `browser-first/host/addon-delegation-host-service.mjs`; public Bootstrap overwrite/provenance contracts]

STATUS: pass
VALIDATION: pass
BLOCKERS: []
ARTIFACTS: [findings.md]
