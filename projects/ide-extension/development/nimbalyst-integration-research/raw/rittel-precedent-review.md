# Rittel PRECEDENT Review

Registered research: `2026-07-11-nimbalyst-integration-research`
Identity: Rittel, Horst
Gate applied: **PRECEDENT only**
Pinned upstream: `/tmp/nimbalyst-c8ca207c6004` at
`c8ca207c6004653ba2df3d81e06133ce2e9fad3d`

## Gate Rule

This review asks one question: **who already owns the candidate concept or its
implementation?** It does not apply safety, cost, readiness, promotion, or
admission gates. Ownership is routing evidence, not a rejection condition.

- **already-deployed**: the cited local owner has a running or persisted form of
  the candidate's essential concept.
- **build-from-owned**: a cited local owner already controls the concept or the
  boundary, but the candidate itself is not deployed.
- **precedent-clean**: the cited local record establishes no local owner for the
  candidate. Upstream ownership remains valid precedent and does not become local
  ownership.

The upstream checkout is MIT client code: `LICENSE:1-13` grants reuse subject to
notice. Nimbalyst Inc. owns that implementation (`LICENSE:3`). That fact does not
kill a candidate. Separately, the checkout says the collaboration server is a
different project (`README.md:124-146`; `LICENSING.md:5-8`). No server owner,
source revision, or license was available in the reviewed evidence.

## Exact Dispositions

| Candidate | Exact upstream owner | Exact local owner | PRECEDENT disposition | Required synthesis revision |
|---|---|---|---|---|
| `NIM-C01` `WorkbenchEditorHost` vocabulary | **Nimbalyst Inc., MIT client**: `packages/extension-sdk/src/types/editor.ts:283-410` owns the broad `EditorHost`; `useEditorLifecycle.ts` owns its lifecycle helper. | **ide-extension architecture**: `projects/ide-extension/ARCHITECTURE.md:64-69` owns the local host strategy; lines `38-60` assign kernel and edge authority. It does not deploy this interface. | **build-from-owned** | Replace “adapt locally” with “build from the existing ide-extension host/authority owner, using Nimbalyst as cited interface precedent.” Do not imply that independent local naming removes upstream ownership of the precedent. |
| `NIM-C02` electron-free read-only host | **Nimbalyst Inc., MIT client**: `packages/extension-sdk/src/createReadOnlyHost.ts:25-120` owns the factory behavior against its `EditorHost`. | **NIM-C01 / ide-extension host owner**: `ARCHITECTURE.md:64-69`; the current demo is browser-hosted (`public/demo/l0.html`), but no reusable read-only host factory is deployed. | **build-from-owned** | State that C02 is a local fixture to be built under C01's owner. “Inspired by” does not make the upstream factory ownerless; copied behavior or code still needs exact MIT attribution. |
| `NIM-C03` manifest and validator pattern | **Nimbalyst Inc., MIT client**: `packages/extension-sdk/src/types/extension.ts`, `manifestValidation.ts`, `validate.browser.ts`, and `__tests__/manifestValidation.agentProviders.test.ts` own Nimbalyst's manifest model and hostile fixtures. | **ide-extension registry/schema owner, deployed**: `schemas/module-manifest.schema.json:1-80`, `src/kernel/registry.mjs:4-39`, and `scripts/validate-schemas.mjs:1-19`. The accepted local review confirms runtime enforcement is incomplete (`development/architecture-review-2026-07-10/findings.md:99-107`). | **already-deployed** | Replace primary “precedent” with “already deployed locally; Nimbalyst is comparative test precedent.” The synthesis must not describe local fields or validation ownership as an adaptation from Nimbalyst. Required work is repair/evolution of the deployed local owner. |
| `NIM-C04` public package smoke-check shape | **Nimbalyst Inc., MIT client**: `scripts/extension-sdk-public-checks.sh:8-35` builds, dry-runs `npm pack`, type-checks a dev kit, and builds/types examples; `packages/extension-sdk/package.json:25-56` owns package exports and contents. | **ide-extension package owner**: `projects/ide-extension/package.json` owns current `validate:schemas` and `smoke` commands, but no separately published contract or package-consumer check is deployed. | **build-from-owned** | Replace “adapt locally” with “extend the existing package verification owner if and when it owns a public package.” Nimbalyst owns the precedent shape; it does not own the local package contract. |
| `NIM-C05` raw-native evidence and canonical projection | **Nimbalyst Inc., MIT client**: `docs/TRANSCRIPT_ARCHITECTURE.md:9-15` names the raw log as persisted source; `TranscriptRuntime.ts:237-280` and `TranscriptProjector.ts:96-168` own derivation/projection; `transcriptStreamAccumulator.ts:74-172` owns renderer accumulation. | **ide-extension kernel evidence owner**: `ARCHITECTURE.md:77-88,117-132`; deployed artifact/audit primitives are in `src/kernel/artifacts.mjs` and `src/kernel/audit.mjs`. No provider-native log plus replaceable canonical projector is deployed. | **build-from-owned** | Say “build the provider-native evidence/projection contract from the existing artifact/audit owner.” Keep Nimbalyst as protocol precedent. Do not call raw-event vocabulary locally owned without distinguishing the existing generic artifact owner from the not-yet-built transcript schema. |
| `NIM-C06` `ExternalAgent` lifecycle and event vocabulary | **Nimbalyst Inc., MIT client**: `packages/extension-sdk/src/agents/AgentProtocol.ts:64-94,150-225` owns session options, event tags, and protocol lifecycle; `AgentProtocolHost.ts:101-219` owns the host boundary. | **ide-extension envelope/adapter owner**: `ARCHITECTURE.md:77-115` already assigns adapter custody and defines `describe/prepare/run/collect/interrupt/inspect`. It is architectural, not a deployed external-agent protocol. | **build-from-owned** | Replace “adopt local vocabulary” with “build from the already-owned local envelope vocabulary.” Cite Nimbalyst for additional lifecycle/failure precedent only; do not suggest Nimbalyst owns the local six-verb protocol. |
| `NIM-C07` before/after evidence diff viewer | **Nimbalyst Inc., MIT client**: `README.md:16-24,81-88`, `docs/FEATURE_INVENTORY.md`, and `EditorHost` diff methods at `types/editor.ts:419-450` own Nimbalyst's review grammar and implementation contract. | **UI Prototyping Studio owns local interaction grammar**: `projects/ui-prototyping-studio/interfaces.md:20-48`; **ide-extension kernel owns evidence refs**: `ARCHITECTURE.md:117-132`. No qualifying viewer is deployed; the accepted review says after-state evidence is not materialized (`architecture-review-2026-07-10/findings.md:88-107`). | **build-from-owned** | Replace primary “defer/precedent” with “build from UI Studio interaction ownership plus ide-extension evidence ownership when their owners admit it.” Readiness may remain a separate gate, but it is not the PRECEDENT disposition. |
| `NIM-C08` task-session-artifact-receipt relation view | **Nimbalyst Inc., MIT client**: `README.md:28-39`, `docs/PLANNING_SYSTEM.md`, and `docs/TRACKER_WORKFLOWS.md` own Nimbalyst's task/session/file relations. | **split local owners**: Craft/Arcanum own task/route authority as stated by the synthesis; the ide-extension kernel owns artifact and receipt refs (`ARCHITECTURE.md:40-60,117-132`). The synthesis cites no deployed cross-owner join. | **build-from-owned** | Name the adopting read-model owner instead of saying only “adapt locally.” The join must be built from owner-qualified references; Nimbalyst remains navigation precedent. If Craft/Arcanum is claimed as exact owner, add an exact canonical file citation rather than a bare project name. |
| `NIM-C09` `DesignFeedbackContextPacket` | **Nimbalyst Inc., MIT client**, for corroborating editor/browser/context product behavior: `types/editor.ts` and browser/change-review surfaces. Nimbalyst does not own the local packet schema. | **ide-extension MCP research, explicit owner**: `development/mcp-chat-extension-integration-research/findings.md:45-50`; architecture repeats the exact packet boundary at `ARCHITECTURE.md:90-94`. No schema artifact is yet deployed. | **build-from-owned** | Retain “build-from-owned,” but remove Nimbalyst from the packet's authority/provenance chain. Cite it only as corroborating product precedent. |
| `NIM-C10` redacted per-run MCP descriptor parser | **Nimbalyst Inc., MIT client** owns ambient MCP configuration behavior in `packages/electron/src/main/services/MCPConfigService.ts`, `MCPRemoteOAuth.ts`, IPC handlers, and `docs/MCP_CONFIG_MIGRATION.md`; those are not the proposed pure local parser. | **ide-extension MCP research owns the descriptor contract**: `findings.md:45-67` specifies the local stdio descriptor, custody fields, and hash binding. The witness/parser is not deployed (`findings.md:81-95`). | **build-from-owned** | Replace “defer, then adapt” with “build from the owned L0.5 descriptor contract when its owner schedules it.” Nimbalyst is negative/contrast precedent for ambient configuration, not the source owner of the local parser. |
| `NIM-C11` browser tool vocabulary | **Nimbalyst Inc., MIT client**: `packages/extensions/browser/manifest.json:60-71` names browser permissions; `browserClient.ts:105-217` owns typed IPC calls; `BrowserSessionService.ts:204-446` owns Electron browser sessions and acts. | **ide-extension browser adapter lane**: `ARCHITECTURE.md:77-83,134-142` assigns browser integrations to adapter admission and names L0.6. The vocabulary/adapter is not deployed. | **build-from-owned** | Replace bare “precedent” with “build destination-native vocabulary from the owned L0.6 adapter lane.” Keep Nimbalyst as one precedent beside Playwright/MCP; do not transfer its Electron/IPC ownership. |
| `NIM-C12` fail-loud resume and partial-success semantics | **Nimbalyst Inc., MIT client**: provider implementations under `packages/runtime/src/ai/server/providers/` and `GitWorktreeService.ts` own Nimbalyst-specific resume, interruption, cleanup, and Git residue behavior. | **ide-extension envelope/kernel owner**: `ARCHITECTURE.md:102-115` owns local interrupt/inspect and authority separation; `src/kernel/audit.mjs` owns local event append. The specific resume/residue states are not deployed. | **build-from-owned** | Replace bare “precedent” with “build local failure states from the envelope/audit owner, informed by Nimbalyst examples.” Provider tokens and Git residue remain upstream/adapter-specific evidence. |
| `NIM-C13` Nimbalyst permission/provider/session runtime | **Nimbalyst Inc., MIT client**: `AgentProtocolHost.ts:45-60,101-219`, `packages/runtime/src/ai/server/ProviderFactory.ts`, providers, permissions, and session stores own this runtime. | **ide-extension kernel, already deployed for the overlapping authority concepts**: `ARCHITECTURE.md:38-60,71-88`; current approval, artifacts, audit, envelopes, and receipts are implemented, with known defects recorded in `architecture-review-2026-07-10/findings.md:19-124`. | **already-deployed** | Replace PRECEDENT-layer “kill direct reuse” with “overlapping authority is already deployed under the local kernel owner.” Any no-go or replacement decision belongs to another gate. Being Nimbalyst-owned does not itself kill reuse; it proves there are two concrete owners that must not be conflated. |
| `NIM-C14` terminal, Git/worktree, backend, and storage execution | **Nimbalyst Inc., MIT client** owns the cited PTY, Git/worktree, backend, Electron, repository, worker, migration, backup, and storage implementations. | **split local owner**: ide-extension kernel already owns its bounded durable state/artifact/audit (`ARCHITECTURE.md:38-60`; `src/kernel/artifacts.mjs`; `src/kernel/audit.mjs`); future process/Git powers are assigned to separately admitted adapter lanes by `ARCHITECTURE.md:77-88`, not deployed locally. | **build-from-owned** | Split the composite in the synthesis: local kernel storage overlap is already deployed; terminal/Git/process capabilities must be built from the local adapter owner if pursued. “Kill” is not a PRECEDENT result and cannot stand as the candidate's ownership classification. |
| `NIM-C15` sync, mobile, collaboration, credentials | **Two different ownership claims**: Nimbalyst Inc. owns the MIT client protocol/client/mobile code (`packages/collab-protocol/`, `packages/runtime/src/sync/`, mobile packages; `LICENSE:1-13`). The hosted collaboration server is a separate project (`README.md:133,143-146`; `LICENSING.md:5-8`) whose exact owner/source/license was not established. | **No cited local owner**: `ARCHITECTURE.md:51-60` excludes remote integration authorities, and the synthesis identifies no admitted hosted identity, sync, mobile, or remote-approval owner. | **precedent-clean** | Replace the combined owner/source sentence with separate client and hosted-server rows or subclaims. The MIT client is inspectable precedent; hosted/server deployability is unproven and must not inherit MIT status. “Defer/kill shortcut” may appear only under other gates, not PRECEDENT. |
| `NIM-C16` telemetry and updater | **Nimbalyst Inc., MIT client**: `README.md:90-107` documents updater and PostHog behavior; `packages/electron/src/main/services/autoUpdater.ts` and related source own the implementation. | **No exact local owner is cited** for product analytics or executable update supply chain. “Repository-local observability is governed separately” is not an exact owner citation, and ide-extension has no admitted updater/analytics owner. | **precedent-clean** | Replace “kill reuse” in the PRECEDENT result with “no local owner established; Nimbalyst-owned precedent only.” If local observability is claimed as overlap, cite its canonical owner and split governance observability from product analytics and executable updating. |

## Required Synthesis Revisions

1. Add a **PRECEDENT disposition** column using only `already-deployed`,
   `build-from-owned`, and `precedent-clean`. Preserve safety, cost, timing, and
   admission outcomes in separate columns; do not encode them as ownership results.
2. Change C03 and C13 to **already-deployed** for their local overlap. C03 extends
   a deployed local schema/registry even though enforcement is defective. C13
   overlaps a deployed local kernel authority even though that kernel has open
   repairs.
3. Change C01, C02, C04-C12, and C14 to **build-from-owned**. Each has an exact
   local owner or owner split, but its proposed local candidate is not deployed.
4. Change C15 and C16 to **precedent-clean** unless exact local owners are added.
   Absence of a local owner does not imply adoption; it only means PRECEDENT found
   no ownership collision.
5. Keep C09 explicitly local-owned. Nimbalyst may corroborate the user job, but it
   contributes no schema authority and avoids no schema-authority work.
6. For C08, replace bare “Craft/Arcanum” ownership with exact canonical file and
   line citations before claiming an exact task/route owner in the final synthesis.
7. Split C14's already-deployed kernel storage from undeployed terminal/Git/process
   powers. The current composite obscures different owners and deployment states.
8. Split C15 into **MIT client** and **separate hosted server** claims. Never infer
   server source availability, license, self-hostability, or operational ownership
   from the client repository's MIT license.
9. Split C16 into repository governance observability, product analytics, and
   executable updating. “Governed separately” is not an owner until backed by an
   exact authority citation.
10. Remove `kill`, `defer`, `adapt`, and `adopt` from the PRECEDENT count. They may
    survive as outputs of other gates, but PRECEDENT itself never kills merely
    because Nimbalyst or a local subsystem owns something.

## PRECEDENT Count

| Disposition | Count | Candidates |
|---|---:|---|
| **already-deployed** | 2 | NIM-C03, NIM-C13 |
| **build-from-owned** | 12 | NIM-C01, NIM-C02, NIM-C04, NIM-C05, NIM-C06, NIM-C07, NIM-C08, NIM-C09, NIM-C10, NIM-C11, NIM-C12, NIM-C14 |
| **precedent-clean** | 2 | NIM-C15, NIM-C16 |
| **Total** | **16** | |

## Gate Conclusion

The present synthesis overuses adoption language to answer an ownership question.
Under PRECEDENT, Nimbalyst is neither a blank source of ideas nor a reason to kill
a candidate: it is the exact owner of a substantial MIT client implementation.
Locally, most surviving concepts already have an authority owner and should be
built from that owner rather than described as generic adaptation. The two clean
precedents are clean only because no exact local owner was cited; that is not an
admission decision. The hosted collaboration server remains outside the inspected
MIT ownership proof.
