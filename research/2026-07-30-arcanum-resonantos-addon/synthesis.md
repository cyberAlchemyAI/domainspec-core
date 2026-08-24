# Exact-binding synthesis

## Expected end state

Select the three-layer topology, narrowed to an implementation candidate: Arcanum Bootstrap installs and updates selected public Arcanum capabilities at the resolved workspace root; the nested ResonantOS product owns one native, initially `sideloaded-unverified` add-on and all grants, authenticated loopback routes, provider/delegation execution, state, artifacts, secrets, disable, rollback, and release behavior; Augmentor classifies eligible ordinary language only after explicit-command precedence, previews immutable proposal bytes, collects an exact human decision, and projects owner-backed progress and separately consumable results. Augmentor is never an installer, registry, authoritative router, scheduler, executor, approval authority, workspace, session/artifact store, or memory path. This is `BUILD-FROM-OWNED + NOVEL-ATTEMPT`, not a current product or readiness claim. [research.md#agent-1 → `arcanum/spells/arcanum-bootstrap/README.md:10-181`, `arcanum/tools/bootstrap_arcanum.sh:100-900,1750-1935`; research.md#agent-2 → `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Normative Boundary`, `src/sdk/addons/{contracts,validation,registry,surface-routing}.ts`; research.md#agent-3 → `#Security-witness verdict`]

## Current-versus-target ownership map

| Concern | Current exact state | Target retained owner | Binding |
|---|---|---|---|
| Requested target | `../workspace-resonantos` absent | Human must confirm corrected `../workspace-resonant` target | research.md#agent-1 → observed requested/resolved paths |
| Workspace root | Non-Git consumer root with 52 generated skills, `.arcanum`, observability, and byte-current `tools/arcanum`; selection is not proven current | Arcanum Bootstrap owns generated installation; workspace remains consumer | research.md#agent-1 → `../workspace-resonant/AGENTS.md:3-13`, `.arcanum/runtime/config.json`, `.agents/skills/**`, `tools/arcanum` |
| Product owner | Clean nested Git checkout at `2.0.0-alpha`, `dev@6f92af7`, seven cached commits behind `origin/dev@3b07e63` | ResonantOS product `dev`, refreshed before mutation | research.md#agent-2 → `git status --branch`, `git log dev..origin/dev`, `git diff dev..origin/dev` |
| Install/update | Bootstrap exists; Whisper and Orchestrate drift; Subagent Strategy and Necronomicon state absent | Bootstrap only; no add-on-initiated refresh | research.md#agent-1 → bootstrap README/script; `.agents/skills/{whisper,orchestrate,necronomicon}` |
| Alpha runtime | MV3 extension plus authenticated loopback Node bridge | Same two-component boundary; no embedded third runtime | research.md#agent-2 → `ALPHA_RUNTIME_BOUNDARY.md#Normative Boundary` |
| Add-on model | SDK validation, registry, grants, surface routing, status UI exist; Arcanum add-on absent | ResonantOS add-on SDK and `AddOnInstallation` | research.md#agent-2 → `src/sdk/addons/*`, ADR-006, ADR-023 |
| Execution | Delegation/provider owners currently support Hermes/OpenCode/Engineer, not requested Arcanum operations | One Arcanum bridge/adapter behind existing provider, delegation, state, and artifact owners | research.md#agent-2 → `addon-delegation-{service,host-service}.mjs`; research.md#agent-3 → `#Viable shape` |
| Conversation | Explicit command router, chat/session and attachment owners exist; classifier/proposal absent | Augmentor is projection only | research.md#agent-2 → `side-panel-command-router.js#createSidePanelCommandRouter.respondToCommand`, `chat-session-store.js` |
| Artifacts/memory | Host artifact read, attachment, and Living Archive intake/review owners exist | Preserve them; every consumption/admission action remains separate | research.md#agent-2 → `delegation-lifecycle.js`, chat attachment tests, Living Archive host owner |

## Options and kill matrix

| Option | Decision | Reason and kill condition |
|---|---|---|
| Three retained-owner layers | **SELECT, narrowed** | Only shape compatible with Bootstrap ownership and the Alpha boundary. It remains blocked from product execution until adapter and witness exist. [research.md#agent-1 → `#Bootstrap versus add-on boundary`; research.md#agent-3 → `#Viable shape`] |
| Repository-only generated skills shown as product | **KILL** | No manifest → grant → bridge → browser witness. [research.md#agent-3 → `#Killed shapes`; `src/sdk/addons/validation.ts`] |
| Embedded Arcanum runtime/third Alpha component | **KILL** | Violates extension-plus-loopback-host boundary. [research.md#agent-2 → `ALPHA_RUNTIME_BOUNDARY.md#Normative Boundary`] |
| Nested `codex exec`, Claude, or model CLI | **KILL** | Native profile forbids nested model CLI; `tools/arcanum` is deterministic only. [research.md#agent-1 → `.arcanum/runtime/adapters/native-skill.json`; research.md#agent-3 → `#Killed shapes`] |
| Augmentor-owned routing/execution/state | **KILL** | Duplicates retained product owners and makes reload truth unverifiable. [research.md#agent-2 → `MODULE-OWNERSHIP.md`, delegation services; research.md#agent-3 → `#Killed shapes`] |
| Broad exposure of 52 installed skills | **DEFER/KILL initially** | Selection and currency are unproven. [research.md#agent-1 → `#Exact current-state matrix`] |
| Two-child Strategy + Whisper catalog | **CONDITIONAL SELECT** | Keep only if refreshed generated packages and a native adapter expose stable owner operations; otherwise reduce to preview/status. [research.md#agent-1 → `arcanum/arcana/subagent-strategy/SKILL.md:15-182`, `arcanum/spells/whisper/README.md:10-255`; research.md#agent-2 → `#Manifest candidate`] |
| Necronomicon/memory exposure | **DEFER** | Harness state and consent/ownership contract are absent. [research.md#agent-1 → absent `.arcanum/necronomicon/`] |

## Initial public capability catalog

| Public operation | Status | Binding |
|---|---|---|
| `subagent-strategy.preview` | Initial; deterministic and side-effect-free | research.md#agent-2 → `#Manifest candidate`; canonical behavior research.md#agent-1 → `arcanum/arcana/subagent-strategy/SKILL.md:82-182` |
| `subagent-strategy.execute` | Conditional on current installation and native adapter | Same selectors; currently absent at consumer root |
| `whisper.execute` | Conditional second independent child | research.md#agent-1 → `arcanum/spells/whisper/README.md:46-109,234-255`; installed package exists but is drifted |
| `run.status`, `run.clarify`, `artifact.read` | Adapter projections, not lifecycle owners | research.md#agent-2 → delegation status/lifecycle and chat attachment owners |
| `dispatch-spec`, `orchestrate`, `tools/arcanum` | Internal support only | research.md#agent-1 → current Orchestrate source and native runtime profile |
| Necronomicon, legacy commands, `codex-exec`, `codex-bypass` | Deferred or killed | research.md#agent-1 → runtime config and `#Forbidden imports and claim ceilings` |

If native stable entrypoints cannot be proven without nested model CLI, ship no execution catalog: retain preview/status as explicitly unavailable/degraded product state.

## Exact add-on and bridge contract

Manifest candidate:

```yaml
id: addon.arcanum
sdkVersion: 0.1.0
category: orchestration
runtimeType: agent-addon
provenance: sideloaded-unverified
isolation: host-mediated-agent
requiresReviewedGrant: true
supportsDegradedMode: true
surfaces: [panel, tool-action, background-monitor]
```

Requested grants, minimized per selected capability:

| Grant | Scope / failure | Constraint |
|---|---|---|
| `agent-delegation` | `workspace` / hard-stop | Owner-backed actions only |
| `filesystem` | `workspace` / hard-stop | Add only if pinned installed-runtime paths are essential |
| `shell` | `self` / hard-stop | Fixed reviewed adapter commands only |
| `providers` | `shared` / degrade | Only where a selected capability needs model execution |
| `notifications` | `self` / degrade | Projection only |
| `archive-read` | scoped / degrade | Omit unless required |
| `archive-intake-write` | `intake-only` / degrade | Separate review request; never trusted write |

Initial witness forbids `network`, `browser-control`, `memory-provider`, `device-integration`, and `ui-embedding`. Discovery installs, enables, and grants nothing. [research.md#agent-2 → `src/core/contracts.ts#CapabilityGrant`, `#AddOnInstallation`, ADR-006, ADR-023; research.md#agent-3 → `#Viable shape`]

Create one named Arcanum host bridge service behind existing bridge authentication. Each privileged route requires both the bridge token and a dedicated scoped route-capability token. Routes cover `runtime-status`, `proposal-preview`, `approval-submit`, `run-start`, `run-status`, `child-clarify`, and `artifact-read`. Registration is not entitlement. The adapter invokes exactly one retained-owner operation for each persisted action. [research.md#agent-2 → `ALPHA_RUNTIME_BOUNDARY.md#Route Owners`, `MODULE-OWNERSHIP.md`, `bridge-capability-tokens`, `addon-delegation-host-service.mjs`; research.md#agent-3 → `#Viable shape`]

## Runtime profile, proposal, approval, and projections

Browser-safe runtime profile:

```text
profileId, profileVersion, addonVersion, sdkVersion,
public capability refs/versions, availability, degradedReasons,
requiredGrants, supportedOperations, concurrencyCeiling,
stopCeiling, loopCeiling, opaqueInstallationRef, provenanceDigest
```

Server-only: workspace/runtime/executable paths, environment, credentials, tokens, private identities/schemas, registrar or ledger commands, prompts, and raw evidence paths. [research.md#agent-1 → `.arcanum/runtime/adapters/native-skill.json`; research.md#agent-2 → `#Runtime profile`]

`StrategyProposal` exact bytes bind:

```text
proposalId, schemaVersion, requestRef, normalizedIntent,
role/capability refs and versions, bounded inputs/outputs,
children, dependencyWaves, gates, stop/loop ceilings,
expected handle/artifact types, permissions,
runtimeProfile ref/version, expiration, sha256
```

Preview, edit, decline, and pre-approval clarification create no run/action record, registration, owner call, process, or file mutation. Editing creates new canonical bytes and digest. Approval binds digest, proposal version, runtime profile, grants, and approving human. Immediately before launch, the bridge rechecks digest, expiry, grants, installed-runtime identity, operation availability, and capacity; mismatch starts zero children and requires a new preview. [research.md#agent-2 → `#StrategyProposal and approval`; research.md#agent-3 → `#Deterministic checks`]

Command precedence and event mapping:

```text
explicit slash/control/browser/delegation command
  > existing intent/parser route
  > unmatched ordinary-language Arcanum eligibility classification

proposal.previewed
  -> approval.required
  -> approval.accepted
  -> launch.validated
  -> action.started | blocked | failed | succeeded
  -> run.joined | partially_joined
```

Events carry opaque `runHandle`, `actionHandle`, `childHandle`, owner status, timestamp, optional `artifactHandle`, `blockerRef`, and evidence reference. UI events never establish terminal truth. [research.md#agent-2 → `side-panel-command-router.js#createSidePanelCommandRouter.respondToCommand`, `#State/event mapping`]

Child threads and run tray are projections keyed to owner handles. A clarification addressed to child A travels only through A’s owner handle; it neither reparents nor mutates B. Reload reconciles host owner records; unreachable truth renders `Unknown`. Existing add-on/delegation cards are the UI seam, not a new state store. [research.md#agent-2 → `main-workspace-addons.js#createAddonCard/createDelegationCard/renderAddOnsWorkspace`, `delegation-status.js`, `delegation-lifecycle.js`; research.md#agent-3 → `#Literal two-child fixture`]

Artifact/result operations remain independent:

```text
open != attach-to-chat != consume-into-follow-up != request-memory-intake-review
```

None closes a lifecycle, changes siblings, or admits memory automatically. [research.md#agent-2 → chat attachment and Living Archive owners; research.md#agent-3 → fixture steps 9–11]

## Interaction sequence

1. Resolve explicit commands first.
2. Classify only unmatched ordinary language.
3. Render canonical proposal bytes and digest with “no actions started.”
4. Allow edit, decline, or approval of the exact digest.
5. Revalidate digest, expiry, grants, runtime identity, availability, and capacity.
6. Register exactly once, then invoke one retained owner operation per action.
7. Keep parent chat responsive while the run tray reconciles opaque owner handles.
8. Route A-only clarification through A’s handle.
9. Preserve independent child outcomes and dependent-gate blocking.
10. Let the human separately open, attach, consume, or request intake review for each result.

[research.md#agent-2 → `#Required interaction sequence`; research.md#agent-3 → `#Literal two-child fixture`]

## Boundaries and lifecycle

Public product bytes may contain only public Arcanum capability identifiers and public-neutral provenance. Private DomainSpec, Saturn, `cyberAlchemy-v2`, private ledgers, registrars, prose, and identities are prohibited. Secrets, bridge tokens, credentials, raw paths, prompts, and private evidence cannot enter manifests, profiles, proposals, events, browser storage, artifacts, screenshots, logs, or argv. [research.md#agent-1 → `#Forbidden imports and claim ceilings`; research.md#agent-3 → `#Killed shapes`]

- Install/update: Bootstrap administrator lifecycle only. First produce a no-write canonical-versus-consumer manifest; pin Arcanum source identity, bootstrap hash, selection, profile, and generated hashes. `--force` requires explicit approval.
- Enable: product installation plus reviewed grants; never inferred from catalog discovery.
- Disable/revoke: stop new launches immediately, quarantine further calls, preserve redacted auditable owner state, and do not fabricate cancellation.
- Upgrade: refresh product branch first; revalidate manifest/adapter, review widened grants, invalidate outstanding digests, rerun deterministic and browser witnesses.
- Rollback: restore pinned prior manifest/artifact/adapter hashes without rewriting owner records; quarantine incompatible active runs, reconcile historical projections, and rerun fixture. Disable must work even if rollback fails.

[research.md#agent-1 → `#Drift and upgrade obligations`; research.md#agent-3 → `#Upgrade and rollback evidence`]

## Implementation dependency sequence and slices

1. Confirm corrected target path; refresh product `dev`; recheck all selectors.
2. Produce Bootstrap dry-run and exact drift/provenance manifest; select and refresh only required generated packages with separate approval.
3. Freeze catalog and public/private/secret schema.
4. Add valid sideloaded manifest and capability-review fixture.
5. Implement one capability-token-gated Arcanum bridge service and redacted runtime-status profile.
6. Implement side-effect-free proposal canonicalization, SHA-256 digest, edit/decline, exact approval, revalidation, and replay protection.
7. Bind adapter operations to existing provider/delegation/state/artifact owners.
8. Add child/run projection, targeted clarification, reload reconciliation, and run tray.
9. Add distinct result open/attach/consume/intake-review actions.
10. Add disable, revocation, upgrade, rollback, and degraded-mode handling.
11. Run deterministic gates, literal local fixture, browser witness, security scan, and Alpha verification.
12. Only afterward consider promotion/release; receipts and browser launch alone are not readiness.

[research.md#agent-3 → `#Exact selectors and proof status` selectors `#ordered-implementation-slices`, `#exact-deterministic-tests`; research.md#agent-2 → `#Validation and witness ceiling`]

## Literal two-child fixture

Parent input:

> Have Strategy assess whether this release plan needs parallel review, and have Whisper draft the concise operator notice. Keep both separate.

Expected fixture:

- Preview `P1/D1` shows two bounded children and creates no owner state.
- Editing yields `D2`; approval of `D1` then fails.
- Exact approval of current digest records approval before exactly-once registration.
- A binds only to a real installed Subagent Strategy owner; B binds only through a real Whisper adapter.
- If A is absent, A becomes `Blocked(missing-owner-operation)` with zero spawn attempts; Hermes/OpenCode substitution is forbidden.
- Parent chat accepts another message while work is active.
- Clarification addressed to A is observed only by A.
- Target positive result: A owner-backed `Blocked` with `blockerRef`; independent B `Succeeded` with `artifactHandle`; dependent gate remains blocked.
- Reload reconstructs those states from host truth.
- Opening B does not consume it; explicit B-only attachment/consumption leaves A, siblings, lifecycle, and memory unchanged.
- Disable blocks a new launch; rollback restores the pinned adapter/profile.

Current status is specification-only because Subagent Strategy is absent and neither capability has a ResonantOS owner adapter. [research.md#agent-1 → `#Two-child acceptance witness`; research.md#agent-3 → `#Literal two-child fixture`]

## Deterministic and browser validation

| Gate | Required observation |
|---|---|
| Manifest/SDK tests | Reject undeclared grants, invalid isolation, secrets/private markers, default trust, unsupported runtime |
| Route-capability map | Every privileged route has matching scoped token; unknown/missing token fails closed |
| Proposal tests | Preview/edit/decline cause zero owner calls/state; complete bytes bind digest |
| Approval tests | Approval precedes invocation; changed bytes/profile/grants invalidate; `(digest, actionId)` exactly once |
| Adapter tests | Missing operation produces zero attempts; pinned roots/minimal environment; bounded/redacted output |
| Child/state tests | A-only clarification; independent outcomes; dependent gate blocked; reload and `Unknown` reconciliation |
| Consumption tests | Open, attach, consume, intake are distinct; no automatic memory write |
| Lifecycle tests | Revocation/disable block new calls; rollback preserves owner records |
| Bootstrap tests | Dry-run is write-free; generated provenance matches canonical public bytes |
| Repository gates | Focused `src/sdk/addons/*.test.ts`, bridge/delegation, router/session/lifecycle tests; `npm run test:browser-first`; `node scripts/security-pipeline/run-check.mjs`; `npm run pre-release:scan`; finally `npm run verify:alpha` |
| Browser witness | Reviewed grants, `D1`, “no actions started,” two owner IDs, responsive parent, A-only clarification, A blocked/B succeeded, gated dependency, reload fidelity, separate B consumption, no memory intake, disable/rollback, secret-free diagnostics |

[research.md#agent-2 → `#Validation and witness ceiling`; research.md#agent-3 → `#Deterministic checks`, `#Browser checks`]

## Degraded modes

Bridge unavailable → read-only/unavailable; grant missing/revoked → execution hard-blocked; capability absent or provenance mismatch → `Unavailable`/`Incompatible`; owner capacity unavailable → report blocked/unknown without an Augmentor queue; partial completion → preserve independent results; reconciliation failure → `Unknown`; runtime drift → disable execution and require a fresh digest; serial fallback → new proposal and approval only; mid-run revocation → quarantine further calls while reporting acknowledged owner truth. [research.md#agent-3 → `#Degraded modes`]

## Owner decisions and kill criteria

Required owner decisions:

1. Confirm `../workspace-resonant` as the intended corrected target.
2. Approve refreshed product `dev` as the implementation baseline.
3. Approve exact Bootstrap selection/refresh separately from add-on implementation.
4. Decide whether `filesystem`, `shell`, `providers`, archive read, or intake grants are truly necessary.
5. Accept Strategy + Whisper only after stable public native operations exist.
6. Define the product owner for the new bridge service and release artifact.

Kill execution, leaving preview/status only, if any of these persists: no stable public native operation; nested model CLI required; private bytes or secrets enter product/browser surfaces; Augmentor must own scheduling/state; proposal preview mutates; exact approval cannot bind all launch inputs; route tokens cannot fail closed; child clarification cannot remain isolated; reload cannot reconstruct owner truth; disable cannot block new launches; rollback lacks a pinned tested artifact; or refreshed-branch browser witness cannot demonstrate owner-backed value. [research.md#agent-1 → `#Forbidden imports and claim ceilings`; research.md#agent-3 → `#Killed shapes`, `#Claim ceilings`]
