# Arcanum as a ResonantOS Add-on — Explorer Returns

## Agent 1

STATUS: pass  
VALIDATION: pass  
BLOCKERS: ["No blocker to this read-only research return; implementation remains blocked by consumer install drift, absent subagent-strategy package, stale orchestrate/Whisper packages, missing Necronomicon harness state, and no accepted ResonantOS add-on contract or browser witness."]  
ARTIFACTS: [research.md#agent-1]

## Scope and selectors

Inventory was used only as discovery:

- `augmentor-subagent-strategy-integration-research-result-synthesis`
  - `#public-neutral-adapter-and-runtime-profile-contract`
  - `#owner-identity-and-event-mappings`
  - `#exact-two-child-browser-witness`
- `entries-resonantos-living-archive-seam-and-owned-base-synthesis`
  - `#the-owned-base-importance-dispatch-2-owned-base-and-importance`
  - `#open-residue`

Independently checked sources:

- `arcanum/spells/arcanum-bootstrap/README.md:10-18,42-88,92-139,151-181`
- `arcanum/tools/bootstrap_arcanum.sh:100-161,237-355,383-464,507-665,695-758,783-900,1750-1935`
- `arcanum/arcana/subagent-strategy/SKILL.md:15-30,82-99,118-182`
- `arcanum/spells/whisper/README.md:10-21,46-78,100-109,234-255`
- `arcanum/runtime/orchestrate/SKILL.md:1-142`
- `arcanum/registry/SIGILS.md:34,85`
- `arcanum/registry/SPELLS.md:11,14,17`
- `../workspace-resonant/AGENTS.md:1-13`
- `../workspace-resonant/.arcanum/runtime/config.json`
- `../workspace-resonant/.arcanum/runtime/adapters/native-skill.json`
- `../workspace-resonant/.arcanum/observability/**`
- `../workspace-resonant/.agents/skills/{arcanum-bootstrap,whisper,necronomicon,orchestrate}/SKILL.md`
- `../workspace-resonant/tools/arcanum`

The requested `../workspace-resonantos` path is absent. The observed consumer root is `../workspace-resonant`.

## Exact current-state matrix

| Row | Status | Exact finding | Proof |
|---|---|---|---|
| Requested path | absent | `../workspace-resonantos` does not exist. | observed |
| Consumer instructions | current bytes | The workspace declares repo-scoped `.agents/skills`, registry lookup when available, deterministic `tools/arcanum`, and native execution preferred over nested model CLI. | observed: `AGENTS.md:3-13` |
| Native packages | installed, broad, unproven-current | 52 repo-scoped skill directories exist. This is not evidence of an intentional current selection because no installed selection manifest or capability registry was found in the admitted surfaces. | observed |
| `tools/arcanum` | byte-current | Consumer and canonical files have identical SHA-256 `84dff7a59b6c251f3ce038c6b4684b1e29b0df7356a4ae12457061af5a41e231`. | observed |
| Bootstrap skill | byte-current body | Generated package body matches canonical `spells/arcanum-bootstrap/README.md`; frontmatter correctly marks it generated and regeneration-owned. | observed |
| Whisper | installed but drifted | Consumer package predates canonical transport audition, intent-state, surface-map, live-presentation, preset, and observability-owner additions. | observed exact diff |
| Subagent Strategy | absent | Canonical public sigil exists and is registered, but `../workspace-resonant/.agents/skills/subagent-strategy/` is absent. | observed |
| Orchestrate | materially drifted | Consumer has the older 84-line route skill; canonical now owns validated persisted-action native spawn/join/gate execution. | observed exact diff |
| Necronomicon skill | installed/current body | Generated skill body matches canonical spell source. | observed |
| Necronomicon state | absent | `.arcanum/necronomicon/` and its `capabilities.json`, sessions, routes, and capability-update state are absent. Installed skill is not initialized harness state. | observed |
| Runtime config | present | `command_surface` is `repo-codex,claude,repo-local`; default adapter is `native-skill`; eight adapters are marked enabled. | observed |
| Native profile | current | It declares parent-orchestrated handoff, current-session/native-runtime state, no nested model CLI, artifact-plus-stage-receipt output, and parent-owned execution/join. | observed |
| Observability | initialized and used | Structural folders plus signals, hook logs, experiment evidence, and several handoff/dry-run records exist. No product add-on event mapping is present. | observed |
| Registries | absent at consumer root | `AGENTS.md` conditionally references `registry/SIGILS.md` and `registry/SPELLS.md`, but no consumer `registry/` files exist. | observed |
| Add-on integration | absent | No accepted Arcanum add-on manifest, grant, bridge binding, runtime-profile projection, lifecycle mapping, or browser fixture appears in the admitted workspace-root surfaces. | observed/absent |

## Bootstrap versus add-on boundary

Bootstrap owns:

- resolving all-versus-selected sigils and spells;
- generating host-native packages with canonical provenance;
- copying deterministic `tools/arcanum`;
- creating runtime config and non-secret adapter profiles;
- initializing observability structure;
- optionally initializing Necronomicon state;
- optional legacy `.codex/commands`, only by explicit request;
- overwrite refusal unless `--force`.

A ResonantOS-native add-on may own only the product-facing projection:

- add-on manifest and requested host grants;
- capability discovery/review UI;
- loopback-host binding to an already-installed runtime;
- enable, disable, degraded, and rollback presentation;
- owner-backed state/event projection;
- proposal, exact approval, run tray, child-addressing, artifact links, and separate result-consumption choices.

The add-on must not install, synchronize, overwrite, regenerate, vendor, or silently select Arcanum packages. Augmentor may classify and display proposals, but must not become installer, registry, router, scheduler, execution owner, approval owner, artifact/session store, or memory owner.

## Smallest defensible initial catalog

Candidate public product catalog:

1. `subagent-strategy` — governed proposal, confirmation, registration, execution lifecycle, and closeout.
2. `whisper` — bounded governed text composition.

Required internal support, not independent product cards:

- `dispatch-spec` for route validation;
- current `orchestrate` for persisted native execution and joins;
- `tools/arcanum` only for deterministic resolution, validation, handoff, and observability envelopes;
- `native-skill` as the sole initial allowed runtime adapter.

Deferred:

- Necronomicon, until harness state, fallback policy, memory ownership, capability manifest, and product consent semantics exist.
- `codex-exec` and `codex-bypass`, despite being config-enabled; both violate this witness’s no-nested-model-CLI boundary.
- broad exposure of all installed skills; current selection intent and catalog currency are unverified.
- legacy command adapters.

This catalog is an implementation candidate, not currently executable product capability.

## Runtime-profile facts Augmentor may project

Observed, safe facts:

- adapter ID: `native-skill`;
- execution mode: `parent-orchestrated-handoff`;
- state model: `current-session-and-native-runtime`;
- isolation: `no-nested-model-cli`;
- input: command prompt plus dispatch step;
- output: artifact plus stage receipt;
- terminal classes: passed, flagged, blocked, interrupted, timeout;
- limitation: the adapter is not an autonomous shell runtime;
- execution and joining remain host-parent responsibilities.

Augmentor must obtain these facts from the owner-backed runtime profile/status response. It must not infer “running,” “installed-current,” “approved,” or “completed” from package presence, config presence, a proposal, or a receipt-shaped placeholder.

## Two-child acceptance witness

Current proof status: **deferred / not witnessed**.

Canonical Subagent Strategy can govern a confirmed two-or-more-agent dispatch, including digest-bound readiness, tension, explicit confirmation, registration-before-spawn, native execution, join, close, and observability. Canonical Whisper permits long work through native skill/subagent execution with a receipt.

The current consumer cannot support the proposed literal witness because:

- `subagent-strategy` is absent;
- `orchestrate` lacks the current persisted native action contract;
- Whisper is drifted;
- no add-on host binding or browser projection exists;
- Whisper does not itself prove a distinct second-child lifecycle.

A defensible future fixture is: one confirmed Subagent Strategy run creates exactly two owner-backed child actions, one executing a bounded Whisper task and one independently validating it or performing another explicitly selected public capability. The parent remains usable; targeted clarification is routed through the execution owner; reload reconciles owner state; each result remains separately openable/attachable/consumable. Exact manifest, grants, child identity mapping, and browser observations remain for the ResonantOS architecture lane to bind.

## Drift and upgrade obligations

Before implementation:

1. Produce a no-write canonical-versus-consumer manifest for every selected package and support file.
2. Explain why a broad install lacks newer `subagent-strategy`, `continuation-router`, and related packages.
3. Obtain explicit approval before any Bootstrap `--force` refresh; it can replace generated destinations.
4. Preserve consumer-owned files and telemetry; do not treat generated-package refresh as product deployment.
5. Pin Arcanum source identity, bootstrap-script hash, selected capability list, runtime profiles, and generated output hashes.
6. Revalidate runtime config after refresh; “enabled” adapters must not become add-on-granted adapters automatically.
7. Define disable and rollback as product projection operations distinct from Bootstrap downgrade or filesystem restoration.
8. Re-run deterministic package, link, dispatch, receipt, and observability validation before a browser witness.

## Forbidden imports and claim ceilings

Forbidden:

- private DomainSpec, Saturn, `cyberAlchemy-v2`, private dispatch hooks, private ledgers, or private prose;
- `.agents/` packages copied into product bundles as an embedded runtime;
- `.arcanum/observability` raw logs exposed directly to browser code;
- Necronomicon session/memory state without an explicit owner and consent contract;
- secrets in manifests, runtime profiles, proposals, events, receipts, or browser state;
- nested model-backed CLI, `codex-exec`, or `codex-bypass`;
- preview-triggered execution, implicit approval, automatic artifact intake, or automatic memory admission;
- a second installer, registry, router, scheduler, provider fabric, execution owner, workspace, artifact store, session store, approval authority, or memory path.

Proof ceiling: the workspace has installed Arcanum developer/runtime surfaces, but it does **not** currently have a verified-current selected installation, an Arcanum ResonantOS add-on, or an executable two-child browser witness.

## Agent 2

STATUS: block
VALIDATION: pass
BLOCKERS: [no accepted Arcanum add-on contract or implementation, no accepted StrategyProposal/digest-approval contract, no Arcanum bridge adapter or routes, no owner-backed two-child witness, target Inventory unavailable, local dev is seven cached commits behind origin/dev]
ARTIFACTS: [research.md#agent-2]

## Verdict

The smallest defensible seam is additive, but it is not currently implemented or accepted:

1. Arcanum Bootstrap remains the installer/updater of the workspace-level public Arcanum runtime.
2. ResonantOS owns one native `agent-addon` manifest, explicit grants, bridge routes, local process/filesystem mediation, installation state, artifacts, lifecycle, disable/rollback, and release behavior.
3. Augmentor remains only the conversational proposal/control projection over those owners.

Current proof supports this as `BUILD-FROM-OWNED + NOVEL-ATTEMPT`, not as a working integration. The claim ceiling is `NO_WITNESS_CURRENT`. Reject any embedded third runtime or second installer, registry, router, scheduler, provider fabric, approval authority, workspace, artifact/session store, memory path, or secret store.

## Exact evidence and selector status

| Claim | Exact source selector | Proof status |
|---|---|---|
| Alpha runtime is exactly MV3 extension plus authenticated local bridge | `AGENTS.md#Alpha Runtime Boundary`; `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Normative Boundary` | current-source proven |
| Privileged add-on execution belongs behind a named capability-gated bridge service | `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Route Owners`; `docs/architecture/MODULE-OWNERSHIP.md` rows for `bridge-client.js`, `bridge-server.mjs`, and `addon-delegation-*.mjs` | current-source proven |
| SDK manifest, validation, registry, and surface routing owners exist | `src/sdk/addons/contracts.ts#ADDON_SDK_VERSION`; `validation.ts#validateAddOnManifest`; `registry.ts#createAddOnRegistrySnapshot`; `surface-routing.ts#createAddOnSurfaceDockRoutes` | current-source proven |
| Registry discovery does not install, enable, or grant | `docs/architecture/ADR-023-addon-repository-registry-model.md#Registry V0 In Core`; `registry.ts#createAddOnRegistryEntry` | current-source proven |
| Add-on grants are explicit and revocable | `src/core/contracts.ts#CapabilityGrant`; `#AddOnInstallation`; `docs/architecture/ADR-006-addon-runtime-sdk.md#Capability Grant Lifecycle`; `src/lib/addon-capability-review.js#capabilityReviewState` | current-source proven |
| Explicit commands precede ordinary-language interpretation | `browser-first/resonantos-side-panel-extension/src/lib/side-panel-command-router.js#createSidePanelCommandRouter.respondToCommand` | current-source proven |
| Current delegation owner can create records and run only Hermes/OpenCode adapters | `browser-first/host/addon-delegation-service.mjs#executeDelegationRecord`; `addon-delegation-host-service.mjs#addonDelegationRoutes`; `delegation-lifecycle.js#startDelegationLifecycle` | current-source proven |
| Current UI can display add-on status, capabilities, delegation state, and returned artifact summary | `main-workspace-addons.js#createAddonCard/createDelegationCard/renderAddOnsWorkspace`; `delegation-status.js`; `delegation-lifecycle.js` | current-source proven |
| Current chat/session and attachment owner exists | `chat-session-store.js`; `browser-first/test/chat-session-store.test.mjs` session/fork/attachment cases | current-source proven, but not child-run ownership |
| StrategyProposal is side-effect-free and approval is digest-bound | Inventory selector `augmentor-subagent-strategy-integration-research-result-synthesis#public-neutral-adapter-and-runtime-profile-contract` | verified precedent only; absent in current ResonantOS source |
| Owner identity/event separation and independent consumption | Inventory selector `#owner-identity-and-event-mappings` | verified precedent only; absent as an Arcanum product contract |
| Two-child Strategy + Whisper browser witness | Inventory selector `#exact-two-child-browser-witness` | precedent only; no current Arcanum adapter/witness |
| Living Archive integration must supply a body behind host-owned write/promotion seams | Candidate Inventory selector `resonantos-living-archive-seam-and-owned-base-synthesis#the-seam-dispatch-1-living-archive-integration`; current `archive-review-host-service.mjs` ownership | candidate discovery plus current owner proof; not an Arcanum execution seam |
| Accepted native Arcanum add-on | repository search across `public/addons/`, `src/sdk/addons/`, `browser-first/host/`, extension `src/lib/` | missing |
| Current branch represents cached `origin/dev` | `git status --branch`; `git log dev..origin/dev`; `git diff dev..origin/dev` | disproven: local `dev` is behind seven commits |

Inventory was used only as discovery. The target product has no root machine Inventory; the separate nested `agentsofthefree` Inventory is not authority.

## Current-versus-missing matrix

| Concern | Current owner/state | Missing for Arcanum | Proof |
|---|---|---|---|
| Manifest | Validated SDK V0 manifests under `public/addons/*.json` | `public/addons/arcanum.json` or sideloaded creator-owned equivalent, accepted catalog policy | current owner proven; target absent |
| Registry | `src/sdk/addons/registry.ts`; catalog-only | Arcanum registry entry/provenance/release reference | current owner proven; target absent |
| Installation | Host-owned `AddOnInstallation`; add-ons not enabled/granted by discovery | Adapter binding to Bootstrap-installed runtime without reinstalling it | model proven; binding absent |
| Grants | `CapabilityGrant`, review UI, scoped bridge tokens | Narrow Arcanum grant preset and bridge route capabilities | mechanism proven; target absent |
| Host execution | `addon-delegation-host-service.mjs` plus Hermes/OpenCode service bodies | Named Arcanum adapter/service and route family | current owner proven; target absent |
| Provider routing | `provider-host-service.mjs`, `provider-bridge-service.mjs`, provider fabric | Adapter must consume host-selected profile; no Arcanum-owned provider/secret routing | current owner proven |
| Conversation | command router then natural-intent parsers then `runChatTurn`; Augmentor host prompt | Arcanum eligibility classifier after explicit-command precedence | precedence proven; classifier absent |
| Proposal/approval | Browser-control approval mechanisms exist for a different domain | Immutable proposal bytes, SHA-256 digest, edit/decline/new-digest semantics, immediate prelaunch revalidation | analogous owner exists; target contract absent |
| State/events | Delegation records and Hermes/OpenCode statuses/artifacts | Arcanum run/action/event reconciliation and join projection | partial precedent; target absent |
| Child threads | Chat session forks and delegation cards exist | Opaque child handles, targeted clarification, sibling isolation, parent continuity contract | primitives proven; composition absent |
| Run tray | Add-ons workspace and delegation status summaries exist | Multi-child run tray keyed to owner-backed action/run handles | projection seam proven; target absent |
| Result handling | Artifact read and chat attachments exist | Separate `open`, `attach`, `consume`, `request-memory-admission` choices | primitives proven; unified contract absent |
| Memory | Living Archive intake/review/promotion host owns writes | Explicit separate intake request; never automatic admission | owner proven; Arcanum mapping absent |
| Disable/rollback | Installation states and grant revocation vocabulary exist | Stop new launches, reconcile active owners, pin/restore adapter/runtime version, preserve artifacts | vocabulary proven; operational contract absent |

## Proposed owner-preserving contract

### Manifest candidate

`id: addon.arcanum`, `sdkVersion: 0.1.0`, `category: orchestration`, `runtimeType: agent-addon`, provenance initially `sideloaded-unverified`, runtime isolation `host-mediated-agent`, `requiresReviewedGrant: true`, degraded mode supported.

Requested SDK capabilities should be the smallest existing vocabulary:

- `agent-delegation`, scope `workspace`, hard-stop.
- `filesystem`, scope `workspace`, hard-stop, restricted by the host adapter to the selected installed Arcanum workspace/runtime paths.
- `shell`, scope `self`, hard-stop, only for fixed reviewed adapter commands.
- `providers`, scope `shared`, degrade, only if a selected capability actually needs model execution.
- `notifications`, scope `self`, degrade.
- `archive-read` only if selected work requires scoped context.
- `archive-intake-write`, scope `intake-only`, degrade; never trusted writes.

No `network`, `browser-control`, `memory-provider`, `device-integration`, or `ui-embedding` in the initial witness unless separately justified. Manifest secrets, raw paths, private identities, capability tokens, and provider credentials are forbidden.

Initial capability catalog should be narrowed to:

- `subagent-strategy.preview`: deterministic, side-effect-free proposal construction.
- `subagent-strategy.execute`: owner-backed execution only after exact approval and adapter preflight.
- `whisper.execute`: second independent public-capability child for the fixture.
- `run.status`, `run.clarify`, `artifact.read`: adapter operations, not new lifecycle owners.

If current Bootstrap-installed capability contracts cannot expose these through stable public entrypoints without nested model-backed CLI, kill the two-child catalog and retain preview/status only until a native adapter exists.

### Runtime profile

Browser-safe projection:

`profileId`, `profileVersion`, `addonVersion`, `sdkVersion`, public capability refs and versions, availability, degraded reasons, required grant names, supported operations, concurrency ceiling, stop/loop ceilings, and opaque installation/provenance reference.

Server-only:

workspace/runtime paths, executable paths, environment, provider credentials, bridge/capability tokens, private schemas/identities, ledger/registrar commands, and raw evidence paths.

### StrategyProposal and approval

Proposal fields:

`proposalId`, `schemaVersion`, `requestRef`, exact normalized intent, public role/capability refs, bounded inputs/outputs, child definitions, dependency waves, gates, stop/loop ceilings, expected opaque handles/artifact types, permission requirements, runtime-profile ref/version, expiration, and `sha256` over canonical exact bytes.

Preview, edit, decline, and targeted clarification cause zero registration, spawn, process launch, owner call, or run mutation. Edit produces new bytes and a new digest. Approval must bind exact digest, proposal version, runtime profile, capability grants, and approving human. Immediately before launch the bridge revalidates digest, expiry, grants, installed-runtime identity/version, operation availability, and capacity. Any change blocks with zero child starts and requires a new preview/approval.

### State/event mapping

Adapter maps persisted owner truth to opaque browser projections:

`proposal.previewed -> approval.required -> approval.accepted -> launch.validated -> action.started|blocked|failed|succeeded -> run.joined|partially_joined`.

Each event carries `runHandle`, `actionHandle`, `childHandle`, owner status, timestamp, optional `artifactHandle`/`blockerRef`, and evidence ref. UI events never create terminal truth. Notification delivery, read/unread, attachment, result consumption, lifecycle join, and memory intake remain separate flags/events.

## Required interaction sequence

1. Match explicit slash/control/browser/delegation commands first using the existing command router.
2. Only unmatched ordinary language may be classified as Arcanum-eligible.
3. Produce a no-side-effect proposal preview with exact bytes and digest.
4. Human may edit, decline, or approve that exact digest.
5. Bridge revalidates runtime profile, grants, capability availability, expiry, and digest.
6. Adapter invokes one retained owner operation per persisted action; Augmentor does not schedule or execute.
7. Parent chat remains usable while run-tray projections poll/reconcile opaque owner handles.
8. A clarification addressed to child A routes only through A’s owner handle; it does not reparent or mutate child B.
9. Each child result is independently available.
10. For each result the human separately chooses `open`, `attach to current chat`, `consume into a follow-up`, or `request Living Archive intake review`. None implies another; no automatic memory admission.

## Stale-branch uncertainty

Local checkout: `dev` behind cached `origin/dev` by seven commits. The delta changes 15 files, chiefly Agent Control public-submit protections and live-browser certification, including `approval-policy.js`, `control-approval-actions.js`, `browser-page-actions.js`, tests, `docs/STATUS.md`, capability matrix, and `package.json`. It does not show add-on SDK/registry/host-delegation changes, so the traced add-on seam is not directly contradicted by the cached delta. However approval and acceptance-test paths are materially stale. No implementation may begin until `dev` is refreshed and all named selectors are rechecked.

## Validation and witness ceiling

Read-only validation passed: mandated reading order, exact current source, named ADRs/owners, SDK/registry/UI/bridge seams, narrow Inventory selectors, and cached seven-commit delta were inspected. No product code or tests were executed, by contract.

A future acceptance witness must use a local fixture and prove: valid manifest; explicit grant review; no mutation before digest approval; two distinct owner calls; parent chat responsiveness; A-only clarification; A blocked with `blockerRef`; B succeeds with artifact; dependency gate remains blocked; reload reconciles owner state; B-only open/attach/consume leaves A, siblings, lifecycle, and memory unchanged; disable blocks new launches; rollback restores pinned adapter/runtime profile. Required deterministic families are `src/sdk/addons/*.test.ts`, focused bridge/add-on-delegation tests, command-router/chat-session/delegation-lifecycle tests, `npm run test:browser-first`, security pipeline for privileged routes, and finally `npm run verify:alpha`. Until those exist and pass on refreshed `dev`, the integration remains blocked and non-ready.

## Agent 3

STATUS: pass  
VALIDATION: pass  
BLOCKERS: [product checkout is 7 commits behind cached origin/dev; no installed Subagent Strategy package in the workspace; no ResonantOS Arcanum host adapter or manifest; no accepted two-child fixture; no end-to-end browser witness; current delegation owners support Hermes/OpenCode/Engineer rather than Subagent Strategy and Whisper]  
ARTIFACTS: [research.md#agent-3]

## Security-witness verdict

The viable shape is a ResonantOS-native, sideloaded-unverified add-on whose browser presentation is an Augmentor projection and whose privileged operations are implemented by one new bridge service behind existing bridge authentication, scoped route-capability tokens, explicit add-on grants, and host-owned delegation/state/artifact services.

Arcanum remains a repository installation and generated native-skill package owner. ResonantOS remains the runtime, routing, scheduling, execution, session, artifact, secret, and memory owner. Augmentor may classify ordinary language, render a side-effect-free proposal, collect an exact decision, and project owner state; it must not become any of those owners.

This is an implementation candidate, not a demonstrated integration. Current checkout `6f92af7b32b17d2eef66230d463eb8b6a21a98f7` is seven commits behind cached `origin/dev` at `3b07e635d596c18f9a047ef5921892acc7cba4ff`; it must be refreshed before implementation conclusions are frozen.

## Viable shape

1. A manifest validated by `src/sdk/addons/validation.ts`, initially:
   - `id: addon.arcanum`
   - `runtimeType: agent-addon`
   - `category: orchestration`
   - host-mediated panel/tool-action/background-monitor surfaces
   - only narrowly required capabilities, provisionally `agent-delegation` and `notifications`; add `filesystem` only if a separately approved, pinned workspace-root adapter truly needs it
   - `host-mediated-agent` isolation, hard-stop revocation, explicit compatibility and deterministic smoke tests
   - no secrets, tokens, private prose, executable paths, grants, installation state, or enabled-by-default state.

2. One named bridge owner for Arcanum status/proposal/approval/run/status/result operations. Every privileged route requires the bridge token plus a dedicated scoped capability token. Registration alone grants nothing.

3. A host runtime profile that reports only redacted facts: canonical capability ID, generated-package provenance, compatibility/version digest, available native owner operation, health, and degraded reason. It must not expose prompts, private state, tokens, provider credentials, raw filesystem paths, or DomainSpec/Saturn material.

4. Augmentor renders projections over proposal, approval, owner run IDs, child state, blockers, and result references. Owner records remain under ResonantOS external user state; generated Arcanum skills remain repository tooling.

5. Bootstrap is a separate administrator/developer lifecycle. `arcanum-bootstrap` dry-run prints planned writes; normal bootstrap refuses overwrite without `--force`; generated skills carry canonical-source/generated-by provenance. Add-on preview must never invoke bootstrap, mutate packages, or convert `tools/arcanum` into a model executor.

## Killed shapes

- Repository-only copied skills presented as a product add-on: no manifest-to-grant-to-bridge-to-browser witness.
- Embedded Arcanum runtime added as a third Alpha component: violates `ALPHA_RUNTIME_BOUNDARY.md`, which admits only MV3 extension plus authenticated Node bridge.
- Nested `codex exec`, `claude`, or another model-backed CLI: killed. `tools/arcanum` is only a deterministic resolver/validator/handoff/legacy-compatibility surface.
- Augmentor-owned router, scheduler, queue, executor, child/session store, artifact store, or memory intake: duplicates retained owners and makes reload truth unverifiable.
- Preview or manifest discovery that installs, enables, grants, schedules, or executes: killed. ADR-023 explicitly separates catalog discovery from installation and grants.
- Capability recommendation treated as entitlement, or approval inferred from chat continuation: killed.
- Secrets/tokens in manifest, proposal, extension storage, logs, artifacts, screenshots, or argv: killed. Bridge-scoped tokens remain runtime-only; provider credentials remain host-memory/environment state.
- Private DomainSpec, Saturn, `cyberAlchemy-v2`, or `authority-triage` prose copied into public Arcanum or ResonantOS: killed. Use only public capability identifiers and public-neutral evidence/provenance vocabulary.
- Automatic artifact attachment, consumption, promotion, or memory admission after completion: killed.
- Non-loopback service, page-to-process/provider/filesystem access, iframe authority, ambient executable lookup, or unrestricted roots: killed.

## Literal two-child fixture

Current proof status: specification only. Whisper is installed as a generated native package in `../workspace-resonant/.agents/skills/whisper/SKILL.md`; no Subagent Strategy package was found there. Current product delegation routes name Hermes, OpenCode, and Engineer, not either requested capability. Therefore the literal witness cannot honestly claim owner-backed execution yet.

Required fixture:

1. In parent chat, enter: “Have Strategy assess whether this release plan needs parallel review, and have Whisper draft the concise operator notice. Keep both separate.”
2. Command precedence first rejects slash-command ambiguity; Augmentor classification then produces `StrategyProposal P1`.
3. P1 contains two child actions, exact capability/version selectors, bounded inputs, expected outputs, required grants, no-side-effect statement, and canonical digest `D1`. No owner call, file write, child record, or task is created.
4. Edit/decline tests remain side-effect-free. Any byte change produces `D2` and invalidates approval for `D1`.
5. User approves exactly `D1`. Host records approval and exactly-once registration before any owner call.
6. Child A binds to a real Subagent Strategy native owner only if installed and discoverable. Child B binds to the installed Whisper owner through a real host adapter. If A is absent, the approved run must show A `Blocked(missing-owner-operation)` with zero A spawn attempts; it must not silently substitute Hermes or an invented queue.
7. Parent chat remains usable; a new ordinary message appears only in the parent.
8. A child-addressed clarification is delivered only to A and carries parent/run/child correlation IDs. B never receives it.
9. Target positive witness, once A exists: A becomes owner-backed `Blocked` with `blockerRef`; B independently becomes owner-backed `Succeeded` with an artifact reference. A dependent gate remains blocked.
10. Reload hydrates projections by reconciling host owner state. Unreachable owner state displays `Unknown`, never fabricated success.
11. Opening B’s result is a separate read. Attaching/consuming it requires another explicit action. B-only consumption does not alter A, sibling state, lifecycle closure, or memory. Memory admission is a later, separately governed choice.
12. Cancellation is a separate test and cannot replace the required blocked-plus-success partial outcome.

## Deterministic checks

Required unit/contract checks:

- Manifest validation rejects undeclared capabilities, invalid isolation, secret-like content, private boundary markers, default-installed/enabled/trusted state, and unsupported runtime categories.
- Extension capability map equals every gated host route; unknown/missing tokens fail closed.
- Preview/edit/decline create no owner calls or durable child/run state.
- Proposal digest binds complete canonical bytes; changed bytes invalidate approval.
- Approval record precedes owner invocation.
- `(proposalDigest, actionId)` is exactly-once; replay blocks; resume uses a new attempt ID.
- Missing owner operation hard-blocks with zero spawn attempts.
- Child-addressed clarification cannot bleed to parent/B.
- Independent outcomes, dependent-gate blocking, reload reconciliation, and `Unknown` on unreachable owner.
- Result open, attach, consume, and memory admission are distinct.
- Revocation hard-stops new calls; disable preserves auditable state without leaving processes running.
- Spawn adapter uses pinned roots, cleared/minimal environment, no secrets in argv, bounded stdout/stderr, and redaction.
- Private-byte and generated-config scans cover extension source, package, artifacts, and diagnostics.
- Bootstrap dry-run is write-free; generated-package provenance matches canonical public owner bytes.

Relevant repository gates, once implementation exists: focused Node tests, `npm run test:browser-first`, `node scripts/security-pipeline/run-check.mjs`, `npm run pre-release:scan`, and for cross-module/release claims `npm run verify:alpha`. None was run in this read-only action.

## Browser checks

With a local fixture and no network/provider dependency:

- capability review shows requested, granted, denied, and revoked states;
- proposal preview shows `D1`, two children, and “no actions started”;
- approving `D1` yields two distinct owner correlation IDs;
- parent accepts and renders another message while children are active;
- A-only clarification remains confined;
- A blocked/B succeeded states appear independently;
- dependent gate is visibly withheld;
- reload reconstructs the same owner-backed states;
- opening B does not consume it;
- explicit B consumption affects only B;
- no automatic memory intake occurs;
- revoke/disable prevents new execution and preserves redacted history;
- screenshots and diagnostics contain no credentials, tokens, private paths, or private-domain prose.

## Degraded modes

- Bridge unavailable: projection read-only/unavailable; no approval or execution.
- Required capability ungranted/revoked: preview may remain visible; execution hard-blocks.
- Capability package absent or provenance mismatch: `Unavailable`/`Incompatible`; never fallback to nested CLI.
- Subagent Strategy absent: A blocks with zero attempts; B may proceed only if the approved proposal declared independent execution.
- Whisper absent: symmetric behavior.
- Owner capacity unavailable: no Augmentor queue; show blocked/unknown owner truth.
- Partial completion: preserve independent child outcomes.
- Reconciliation failure: `Unknown`, not cached success.
- Runtime/version drift: disable execution pending revalidation and fresh digest approval.
- Serial fallback: only through a newly rendered and exactly approved proposal when semantics remain valid.
- Grant revocation during a run: quarantine further calls; report owner state without claiming cancellation succeeded until acknowledged.

## Upgrade and rollback evidence

Before upgrade: capture manifest/version/hash, generated-package canonical provenance, host-adapter version, capability grants, compatibility result, owner health, and a clean deterministic baseline.

Upgrade must revalidate manifest and adapter, compare requested capabilities, force re-review for new or widened grants, invalidate outstanding proposal digests, and rerun deterministic plus browser witnesses. Never preserve trust solely because the prior version was curated.

Rollback must pin the prior manifest/artifact/adapter hashes, stop or quarantine incompatible active runs, restore the prior adapter without rewriting owner records, revalidate compatibility, reconcile runs as historical projections, and rerun the fixture. Disable must be independently possible even when rollback fails. No rollback claim is valid without a tested prior artifact and observed state reconciliation.

## Claim ceilings

- May claim: current ResonantOS owns an authenticated loopback bridge, scoped route capability tokens, add-on SDK validation, capability-review presentation, host-mediated delegation/artifact routes, chat-session hydration, security checks, and release scans.
- May claim: public Arcanum Bootstrap owns generated repository runtime packages, provenance, validation, overwrite gates, and dry-run planning.
- May not claim: an Arcanum ResonantOS add-on exists, is installed, enabled, compatible, secure, release-ready, or browser-tested.
- May not claim: Subagent Strategy is currently installed in the consumer workspace.
- May not claim: Whisper has a ResonantOS owner adapter merely because its generated skill exists.
- May not claim: current Hermes/OpenCode delegation tests prove the requested two-child route.
- Inventory, manifests, ADRs, proposals, receipts, unit tests, and browser launch are individually non-authoritative for production readiness.

## Exact selectors and proof status

- `.arcanum/inventory/entries/augmentor-subagent-strategy-integration-research-result-synthesis.md#honest-degraded-modes`: verified discovery; current sources agree.
- Same entry `#ordered-implementation-slices`: verified discovery; execution slices remain unbuilt.
- Same entry `#exact-deterministic-tests`: verified blueprint; no Arcanum adapter test suite exists in product.
- Same entry `#exact-two-child-browser-witness`: verified acceptance blueprint; explicitly unproven end to end.
- Evidence card `living-archive-write-seam`: candidate discovery only; supports host-owned read/intake/review separation, not this add-on’s execution.
- `promotion-executor-host-resident`: candidate; correctly warns that a named host seam may lack its provider body.
- `owned-arcanum-base-blueprint-with-validators`: candidate, source-confirmed distinction between runnable bootstrap/validators and prose-driven capability packages.
- `authority-triage-private-boundary`: candidate, binding safety boundary; public-neutral analog only.
- Current owner proof: `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md`, ADR-006, ADR-023, `MODULE-OWNERSHIP.md`, `src/sdk/addons/{contracts,validation}.ts`, `browser-first/host/{bridge-capability-tokens,addon-delegation-host-service,addon-delegation-service}.mjs`, extension capability/runtime-status modules, focused browser-first tests, `scripts/pre-release-scan.sh`, and public `arcanum-bootstrap` README/scripts.
