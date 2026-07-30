# Precedent and owner-duplication review

STATUS: pass  
VALIDATION: block  
BLOCKERS: [the “exact” manifest candidate is not schema-valid, StrategyProposal/exact-digest approval/runtime-profile/run-state contracts are absent rather than deployed owners, rollback ownership conflates product rollback with Bootstrap-managed generated-package refresh, product checkout is seven cached commits behind `origin/dev`]  
ARTIFACTS: [reviews/precedent.md]  
VERDICT: REVISE

## Exact cited corrections

1. **Replace the manifest YAML with either a complete validated manifest or label it explicitly as a non-validating sketch.** The synthesis omits required `AddOnManifest` fields (`name`, `version`, `author`, `description`, `requestedCapabilities`, `providerRequirements`, `archiveIntegration`, `health`, `installHooks`, `compatibility`), uses string surfaces instead of `AddOnSurface` objects, flattens `runtimeIsolation`, and supplies scalar `provenance` instead of an `AddOnProvenance` object. `src/core/contracts.ts#AddOnManifest`; `src/sdk/addons/validation.ts#validateAddOnManifest`. This is unsupported novelty, not deployed manifest evidence.

2. **Keep one existing registry.** `src/sdk/addons/registry.ts#createAddOnRegistryEntry/createAddOnRegistrySnapshot` already owns catalog projection; ADR-023 keeps discovery distinct from installation, enablement, and grants. The Arcanum add-on contributes one entry/manifest only. Use mode: `BUILD_FROM_OWNED`; current Arcanum entry: absent.

3. **Do not call the proposed runtime profile current.** Current `.arcanum/runtime/adapters/native-skill.json` describes a generated host package, not a browser-safe ResonantOS add-on profile. The target profile must be a new redacted response owned by the add-on host/status service and backed by Bootstrap provenance. Use mode: `NOVEL-ATTEMPT built from owners`.

4. **Move exact approval authority out of Augmentor language.** “Augmentor … collects an exact human decision” is safe only if it means UI intent capture. `StrategyProposal`, canonical proposal hashing, digest-bound approval persistence, expiry/replay checks, and prelaunch revalidation have no current ResonantOS Arcanum owner implementation (`rg StrategyProposal/proposalId/runtimeProfile` finds none). Existing browser-control approvals are a different domain and occur on a checkout whose approval paths are seven cached commits stale. Augmentor renders; a host add-on route owner validates and persists. Use mode: `NOVEL-ATTEMPT`, not `ALREADY_DEPLOYED`.

5. **Bind new Arcanum routes into the existing bridge composition, not a second bridge fabric.** `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md#Bridge Boundary/#Route Owners` assigns authentication/capability enforcement to `bridge-server.mjs` and add-on execution/artifacts to `addon-delegation-host-service.mjs` plus `addon-delegation-service.mjs`. `MODULE-OWNERSHIP.md#Host Route Contract` requires one named service owner and focused tests. New proposal/approval/run routes are admissible additions; a separate listener, auth stack, scheduler, or provider path is not.

6. **Use existing scoped capability-token vocabulary.** `bridge-capability-tokens.mjs` already owns token minting; existing `addon-runtime-read`, `addon-runtime-control`, `addon-record-read`, and `addon-record-write` are precedent. Add a new capability only if route semantics cannot be safely expressed by those owners, with consistency tests. Manifest grants (`agent-delegation`, `filesystem`, `shell`, `providers`, etc.) remain distinct from bridge route-capability tokens.

7. **Do not claim child threads, run tray, or terminal state are already owned compositions.** Chat forks, delegation cards, add-on cards, and Hermes/OpenCode records are primitives only: `chat-session-store.js`; `main-workspace-addons.js#createAddonCard/createDelegationCard`; `addon-delegation-host-service.mjs`. The proposed Arcanum `runHandle/actionHandle/childHandle`, targeted clarification, join truth, reload reconciliation, and `Unknown` state are absent compositions. Persist owner truth in the host delegation domain; Augmentor projects it.

8. **Preserve result-owner separation.** Delegation artifact creation/read belongs to `addon-delegation-service.mjs`; attachment/follow-up consumption belongs to the chat/session owner; archive intake/review/promotion belongs to `memory-host-service.mjs`, `archive-review-host-service.mjs`, and archive policy. The synthesis correctly separates open/attach/consume/intake, but the implementation slices must route each call to its existing owner rather than create an Arcanum result or memory store.

9. **Split rollback into two lifecycles.** Product disable/revoke/adapter rollback belongs to `AddOnInstallation`, capability-grant, add-on route, and external owner-record state. Generated Arcanum package refresh/restore remains exclusively Bootstrap-managed: `arcanum/tools/bootstrap_arcanum.sh:47-48,107-108,795-897`. “Restore prior adapter hashes” must not authorize direct copying over generated skills; use a pinned Bootstrap source/selection and explicit `--force` approval. No tested product rollback exists today.

10. **Retain the deployment ceiling.** `../workspace-resonant` is a non-Git consumer root; package presence is not product installation. The nested product is `dev@6f92af7`, seven cached commits behind `origin/dev@3b07e63`. Subagent Strategy is absent, Whisper is installed but drifted, and `.arcanum/necronomicon/` is absent. These support `BUILD_FROM_OWNED + NOVEL-ATTEMPT`, never “already deployed.”

## Owner/use-mode matrix

| Mechanism | Retained owner | Use mode |
|---|---|---|
| Install/update generated Arcanum | Arcanum Bootstrap | BUILD_FROM_OWNED |
| Manifest/registry/install state | SDK validation + registry + `AddOnInstallation` | BUILD_FROM_OWNED; Arcanum entry absent |
| Grants/revocation | `CapabilityGrant` + capability-review/install owner | BUILD_FROM_OWNED |
| Bridge auth/capability tokens | `bridge-server.mjs` + token registry | BUILD_FROM_OWNED |
| Arcanum route handlers | Add-on delegation host/service domain | NOVEL-ATTEMPT |
| Provider selection/secrets | provider host/bridge fabric | ALREADY_DEPLOYED owner; new consumer binding |
| Command precedence | side-panel command router | BUILD_FROM_OWNED |
| StrategyProposal/digest approval | new host-owned add-on contract | NOVEL-ATTEMPT |
| Scheduler/action/run truth | host delegation owner | NOVEL-ATTEMPT; never Augmentor |
| Child/run tray | delegation state plus UI projection seams | NOVEL-ATTEMPT |
| Artifacts | delegation artifact owner | BUILD_FROM_OWNED |
| Attach/consume | chat/session owner | BUILD_FROM_OWNED |
| Memory admission/promotion | memory/archive review owners | BUILD_FROM_OWNED |
| Disable/product rollback | installation/grant/add-on host owners | NOVEL operational contract |
| Generated-package rollback | Bootstrap only | BUILD_FROM_OWNED; untested target flow |
| Augmentor | classifier, proposal UI, human-intent capture, projection | PROJECTION_ONLY |

## Evidence-closure obligations

- Validate a complete manifest with `validateAddOnManifest(..., {source: "sideload"})`.
- Refresh `dev`, then recheck every approval, bridge, SDK, delegation, chat, and UI selector.
- Demonstrate that each new route uses existing bridge authentication plus one scoped capability token.
- Prove proposal preview/edit/decline create zero host run/action state and exact approval creates exactly one owner record.
- Prove reload truth comes from host records, not Augmentor/browser presentation state.
- Prove disable and adapter rollback independently; use Bootstrap for any generated-package restoration.
- Preserve missing product implementation as a finding, not an automatic failure of the research route.
