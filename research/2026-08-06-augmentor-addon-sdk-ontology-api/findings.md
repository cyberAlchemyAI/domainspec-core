# Augmentor consultation in the Add-on SDK: findings

## Plain-language answer

The smallest sound seam is to add the host's existing `augmentor-consultation-read` capability to the public Add-on SDK and pair it with an optional, request-only `ontologyConsultation` manifest object. The manifest says what an add-on can understand and would like to use; it does not say that anything is installed, approved, granted, available, or authoritative. The host continues to own bundle selection, grants, credentials, route admission, consultation policy, evidence, and live status. This is a **build-from-owned design**, not an implementation result. [E1: `research.md#agent-1-sdk-runtime-explorer`; E2: `research.md#agent-2-ontology-projection-explorer`; E3: `research.md#agent-3-security-lifecycle-explorer`; PASS rechecks: `reviews-final.md`]

Current host pieces exist and focused current tests passed, but the SDK-to-host adapter does not. The generated neutral projection is stale (29/30 in the selected projection suite), and no independent exact-byte approval or installation receipt was observed. Those two residues block an acceptance-ready bundle and an executable end-to-end SDK witness. They do not block this research decision.

## Evidence and status language

- **Observed-current** means source bytes were inspected at the evidence-closure digests.
- **Executed-current** means the explorers ran the named current test or validation.
- **Designed** means a target contract, fixture, command, or integration that is not implemented.
- **Absent** means the selected current corpus had no owner or implementation for it.
- **Blocked** means a downstream claim cannot be made until the named residue closes.

Evidence closure is `ready` under the exact-binding contract. The direct bindings, file digests, repository epochs, and explorer receipt identities are recorded in `receipts/evidence-closure.json`.

## Current state and exact SDK gap

| Concern | Owner and evidence | Status |
|---|---|---|
| SDK capability vocabulary | `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:4-20`; `src/sdk/addons/contracts.ts:24-43` [E1, E3] | **Observed-current:** closed vocabulary omits `augmentor-consultation-read`. |
| Manifest and validation | `src/core/contracts.ts:531-602`; `src/sdk/addons/contracts.ts:62-76`; `validation.ts:323-347` [E1, E3] | **Observed-current:** no consultation declaration or cross-field invariant. |
| SDK registry/review state | `src/sdk/addons/registry.ts:90-123` [E1, E3] | **Observed-current:** request, installation, review, verification state exist; consultation binding/status do not. |
| Host capability and route | `bridge-capability-tokens.mjs:23-53`; `augmentor-consultation-host-service.mjs:8-55` [E1, E3] | **Observed-current:** spelling and guarded `POST /augmentor/consultation` exist; host derives context, views, limits. |
| Authentication/admission | `bridge-server.mjs:1006-1012,1066-1098,1187-1191` [E3] | **Observed-current; executed-current:** credential stripping and route gate exist; host/bridge suites passed 11/11. |
| Grant/policy | `augmentor-consultation-access.mjs:12-159`; `augmentor-consultation-service.mjs:252-357` [E1, E3] | **Observed-current:** external grants, expiry, revocation, limits, freshness and policy exist; installation adapter is **absent**. |
| Bundle/query contracts | `augmentor-consultation-contract.mjs:139-167,285-365,382-415`; private schemas [E2, E3] | **Observed-current:** closed operations/version/digest rules and mixed-version rejection exist. |
| Projection compiler | `build-consumer-projection.mjs:11-29,45-47,53-72,86-167` [E2] | **Observed-current mechanics; executed-current 29/30; blocked freshness.** Deterministic approval-shaped metadata is not approval. |
| Cache and answer policy | `augmentor-consultation-cache.mjs:7-59`; `augmentor-consultation-answer-policy.mjs:1-24` [E1, E3] | **Observed-current:** partitioning and no-instruction-following policy exist; public result says `authorityEffect: "none"`. |
| Generated answer | No owner/type found [non-collapse recheck NC-03] | **Absent:** must be consumer-owned. |
| SDK-to-host adapter | Entire selected corpus [E1, E3] | **Absent:** no review-to-grant, installation identity, host status, credential binding, or lifecycle integration. |

The exact integration gap is therefore not a missing ontology or a missing host API. It is the absent public request contract and absent owner-preserving adapter between the SDK lifecycle and the already-owned host route. Additional gaps are consultation-specific receipts, orthogonal status, lifecycle hooks, consumer answer ownership, and a finite integrated witness. Exact-byte approval and installation evidence remain **blocked**.

## Options and verdict matrix

| Candidate | Owner (precedent) | Witnessed? | Sound? | Verdict |
|---|---|---|---|---|
| No SDK change | Existing host route, but no SDK lifecycle seam [E1] | No | No: requires bypass | Rejected as target. |
| Reuse `augmentorSkills` | SDK guidance owner [E1] | No | No: guidance is not data access | **KILL: definitional collapse.** |
| Reuse `memoryAccess` | Living Archive policy owner [E1] | No | No: archive policy is not consultation | **KILL: definitional collapse.** |
| Generic tool/connector | Existing host tool/connector meanings [E1] | Incomplete | No: loses typed consultation/grant semantics | Rejected as primary seam. |
| Declaration only | SDK manifest owner | No capability admission | Sound but vacuous | Rejected alone. |
| Capability only | Existing host capability owner | Partial | Cannot express compatibility or degradation | Rejected alone. |
| New capability spelling | Existing `augmentor-consultation-read` owner | Unnecessary | Duplicate owner | Rejected. |
| Existing capability + additive request + host status | SDK declaration plus existing host owners | Finite target W01-W12; W05-W06 blocked | Yes; all reviewer rechecks PASS | **Selected: build-from-owned.** |

## Proposed public, request-only contract

```ts
export type Capability = /* current values */ | "augmentor-consultation-read";

export interface CapabilityRequest {
  capability: Capability;
  scope: "self";
  revocationBehavior: "hard-stop";
}

export type AugmentorConsultationOperation = "lookup" | "search" | "context";

export interface AddOnOntologyConsultationRequest {
  provider: "host";
  contractFamily: "augmentor.consultation";
  supportedQueryVersions: readonly string[];
  supportedResultVersions: readonly string[];
  requestedOperations: readonly AugmentorConsultationOperation[];
  requestedViews: readonly string[];
  explanationProfiles?: readonly ("brief" | "guided" | "deep")[];
  maxProjectionAgeSeconds?: number;
  unavailableBehavior: "degrade-ui" | "hide-ui";
}

export interface AddOnManifest {
  requestedCapabilities: readonly CapabilityRequest[];
  ontologyConsultation?: AddOnOntologyConsultationRequest;
}
```

Validation, rather than a duplicated serialized field, requires exactly one top-level `augmentor-consultation-read` request whenever `ontologyConsultation` is present. A current `granted` request property, if retained temporarily, is legacy non-authoritative syntax—not review, grant, or runtime truth. The target removes it.

```json
{
  "sdkVersion": "0.2.0",
  "requestedCapabilities": [{
    "capability": "augmentor-consultation-read",
    "scope": "self",
    "revocationBehavior": "hard-stop"
  }],
  "ontologyConsultation": {
    "provider": "host",
    "contractFamily": "augmentor.consultation",
    "supportedQueryVersions": ["augmentor.consultation.query@1.1.0"],
    "supportedResultVersions": ["augmentor.consultation.result@1.1.0"],
    "requestedOperations": ["lookup", "search", "context"],
    "requestedViews": ["experience", "runtime", "knowledge"],
    "explanationProfiles": ["brief", "guided"],
    "maxProjectionAgeSeconds": 86400,
    "unavailableBehavior": "degrade-ui"
  }
}
```

Forbidden manifest fields include effective grant/approval/install state, actual bundle identity, paths, credentials, tokens, principals, handles, effective limits, cache keys, authority claims, instructions, writes, routing, promotion, and effects.

## Host-derived orthogonal status

```ts
export type AddOnConsultationStatus = {
  addonState: "not-installed" | "installed-disabled" | "installed-enabled" | "uninstalled";
  projectionState: "not-installed" | "invalid" | "valid-stale" | "valid-current";
  grantState: "not-reviewed" | "review-denied" | "not-granted" | "active" | "revoked" | "expired";
  compatibilityState: "unknown" | "compatible" | "incompatible";
  policyState: "unknown" | "available" | "degraded" | "unavailable";
  invocationState: "ready" | "blocked-addon" | "blocked-projection" | "blocked-grant" | "blocked-compatibility" | "blocked-policy";
  selectedContract?: { family: "augmentor.consultation"; queryVersion: string; resultVersion: string };
  effectiveOperations?: readonly ("lookup" | "search" | "context")[];
  effectiveViews?: readonly string[];
  explanationProfiles?: readonly ("brief" | "guided" | "deep")[];
  effectiveLimits?: { maxCandidates: number; maxRecords: number; maxSources: number; maxBytes: number; maxTokens: number; maxMillis: number };
  projection?: { projectionDigest: string; bundleDigest: string; generatedAt: string };
  sourceHandleSemantics?: "opaque-reference-only";
};
```

This is a **designed, absent**, non-persistent read projection derived from SDK installation/review, host loader, grant registry, and policy state. `invocationState` is derived; it is not another stored truth. Evidence-result statuses (`ok`, `partial`, `no_match`, `insufficient_evidence`, `conflict`, `stale`, `denied`, `invalid_request`, `budget_exceeded`, `temporary_failure`) remain separate.

## Evidence and generated-answer boundary

```ts
declare const sourceHandleBrand: unique symbol;
export type SourceHandle = string & { readonly [sourceHandleBrand]: "opaque-source-handle" };
export type ConsultationEvidence = {
  status: "ok" | "partial" | "no_match" | "insufficient_evidence" | "conflict" | "stale" | "denied" | "invalid_request" | "budget_exceeded" | "temporary_failure";
  records: readonly { statement: string; sourceHandles: readonly SourceHandle[] }[];
  explanationSupport?: unknown;
  answerPolicy: { disposition: "answer" | "qualify" | "clarify" | "abstain"; citationsRequired: boolean; followsRetrievedInstructions: false };
  authorityEffect: "none";
};
export type GeneratedAnswer = {
  owner: "consumer";
  disposition: "answer" | "qualify" | "clarify" | "abstain";
  prose?: string;
  citedSourceHandles: readonly SourceHandle[];
  constrainedByAnswerPolicy: true;
};
```

`GeneratedAnswer` is **designed; owner absent**. It is not evidence, explanation support, host output, permission, routing, approval, or authority. A handle is an opaque reference only; no public resolver or fetch permission is implied.

## Owners and lifecycle sequence

| Stage | Owner and separation | Status |
|---|---|---|
| Manifest validation | SDK validator; schema acceptance only | **Designed; absent.** |
| Installation/declaration | Existing SDK registry persists request and installation identity only | Registry **observed-current**; adapter **absent**. |
| Add-on review | SDK Add-on Review Owner emits distinct `AddOnReviewReceipt` | Review state **observed-current**; consultation receipt **designed**. |
| Exact-byte approval | Neutral Projection Approval Owner emits `NeutralProjectionApprovalReceipt` | **Blocked:** acting owner and independent receipt absent. |
| Bundle installation | Host Projection Installation Owner emits `NeutralProjectionInstallationReceipt` | **Blocked:** owner/receipt absent; projection stale. |
| Consultation grant | Existing host grant owner, through a stateless installation adapter, emits `InstallationConsultationGrantReceipt` | Mechanics **observed-current**; adapter **absent**. |
| Status | Host derives orthogonal status on read | **Designed; absent.** |
| Authentication | Existing token/access owner supplies route-scoped credential | Mechanism **executed-current**; installation binding **designed**. |
| Route admission | Bridge authenticates and gates capability before handler/cache | **Executed-current.** |
| Policy | Existing service enforces grant, bundle, views, freshness, limits, evidence, cache, deadline and answer policy | **Executed-current.** |
| Answer | Named consumer composes or abstains | **Designed; owner absent.** |
| Revoke/disable | Grant revokes, credential rotates/removes, policy revision makes cache unreachable; SDK disable is separate | External revoke **executed-current**; installation lifecycle **absent**. |
| Re-enable/upgrade/rollback/uninstall | Fresh decisions; no manifest resurrection; uninstall removes only installation-local access, not shared projection | **Designed; absent.** |

The mandatory order is declaration → validation → add-on review → exact-byte approval → bundle installation → grant creation → host-derived status → credential acquisition → route admission → consultation policy → bounded evidence → consumer composition. Authentication proves identity at the route; it is not review, grant, policy, routing permission, or effect authority.

## Public/private boundary and threat model

The public SDK may contain neutral contract names, public operations/views, compatibility intent, host-selected public versions, redacted digests/freshness/limits, opaque-handle semantics, answer-policy status, and the already observed public result invariant `authorityEffect: "none"`. It must not copy private nodes, raw records, CAV2 vocabulary or prose, repository paths, source mappings/content, credentials, owner routes, approval authority, or promotion state.

| Threat | Control and status |
|---|---|
| Manifest self-grant or duplicated capability | Request-only type and exactly-one validator invariant — **designed**. |
| Version fork/downgrade | SDK validates syntax or imports generated constants; host selects exact coherent intersection, never silent downgrade — mechanics **observed-current**, adapter **designed**. |
| Add-on selects bundle/path | No such fields; existing loader owns bytes — **observed-current boundary**. |
| Review/credential/evidence mistaken for grant | Separate types, receipts, stages and negative fixtures — **designed**. |
| Overbroad views/limits | Installed/requested/granted intersection and minimum effective limits — host **observed-current**. |
| Malformed, stale, mixed or leaking bytes | Closed schema/version/digest/leakage/freshness gates — mechanics **observed/executed-current**; current freshness **blocked**. |
| Retrieved instructions trigger tools | Preserve as evidence; policy refuses instruction following; zero-call test — host policy **observed-current**, consumer assertion **designed**. |
| Handle becomes resolver | No resolver; zero-fetch negative — **designed**. |
| Cache cross-talk or post-revoke reuse | Installation/principal + policy/revision + grant/bundle/version/query dimensions; auth before cache — base isolation **executed-current**, installation dimension **designed**. |
| Shared deployment principal reused | Prohibited; shared-principal/all-view trusted-proxy adapter is unsuitable [E3] — explicit negative **designed**. |
| Status leaks internals | Closed redacted state, no paths/tokens/private vocabulary/errors — partial current redaction **executed**, SDK projection **designed**. |
| Generated prose treated as truth | Consumer-owned distinct type — **designed; owner absent**. |

## Compatibility, migration, and audit

The additive capability and optional object justify a proposed SDK minor bump `0.1.0` → `0.2.0`; old manifests remain valid, though exhaustive TypeScript switches need source changes. SDK and consultation-family versions remain independent. Host negotiation intersects one coherent installed family with declared versions, requested operations/views and the active grant, computes minimum limits, enforces freshness, and returns incompatible rather than downgrading. Bundle/policy identity changes invalidate bound grants and cache reachability.

Migration must document the request-only shape, remove or quarantine legacy `granted`, preserve old manifests, publish the cross-field invariant and all fixture contracts, explain every lifecycle owner, document handle non-resolution, orthogonal status, disable/revoke/upgrade/rollback/uninstall, and repeat that validation is not review, approval, grant, installation, deployment, promotion, release, or production readiness.

No unified audit owner was evidenced. Until one is chosen, the SDK registry owns declaration/review/lifecycle events; the grant registry owns grant/expiry/revoke events; the host owns status observations, route outcomes, bundle/policy identity and cache/deadline metrics; the consumer owns retained answer provenance. An aggregate audit view must remain a read model.

## Dependency-ordered implementation slices

1. Add SDK vocabulary parity for `augmentor-consultation-read`.
2. Add request-only `CapabilityRequest` and closed optional `ontologyConsultation`.
3. Add cross-field and SDK/host parity validation.
4. Persist only declaration/review metadata in the current registry.
5. Define separate review, exact-byte approval, installation, and grant receipts.
6. Add a stateless installation-identity adapter to the existing grant owner.
7. Add the non-persistent orthogonal status projection.
8. Bind installation grants to route-credential acquisition.
9. Wire disable, re-enable, upgrade, rollback, and uninstall to existing grant/credential owners.
10. Add the consumer-owned `GeneratedAnswer` boundary.
11. Split audit events among transactional owners pending a named owner.
12. Regenerate and validate the neutral bundle.
13. Obtain independent exact-byte approval and installation receipts.
14. Execute SDK, host, integrated, leakage, and browser matrices.
15. Publish migration, lifecycle, security, and composition documentation.

Slices 1–11 may be developed against designed fixtures. Slices 12–13 must close before an acceptance-ready exact-byte or executable end-to-end claim.

## Positive witness: 12 exact target fixtures

Every path and command below is a **designed target locator**, not a current-file claim.

| ID | Owner | Exact fixture path | Exact command | Observable assertion | Proof status |
|---|---|---|---|---|---|
| W01 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/valid-request.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "W01 validates request-only consultation manifest"` | Pass; one top-level capability; no grant field. | **Designed; absent.** |
| W02 | SDK registry | Same manifest + `src/sdk/addons/test-fixtures/ontology-consultation/install-enabled.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "W02 persists declaration without runtime truth"` | Stores request/review only, not runtime truth. | **Designed; absent.** |
| W03 | SDK Add-on Review Owner | `browser-first/test/fixtures/addon-consultation/review-approved-experience.json` | `node --test --test-name-pattern="W03 records review separately from grant" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Review approves `experience`; no grant/credential. | **Designed; absent.** |
| W04 | Existing host grant owner via adapter | `browser-first/test/fixtures/addon-consultation/grant-experience-only.json` | `node --test --test-name-pattern="W04 creates installation-bound grant" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Separate installation-bound `experience` grant. | **Designed; adapter absent.** |
| W05 | Neutral Projection Approval Owner | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/receipts/exact-bundle-approval.json` | `node --test --test-name-pattern="W05 verifies independent exact bundle approval" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-bundle.test.mjs` | Exact input/compiler/schema/output digests match independent approval. | **Blocked: receipt absent.** |
| W06 | Host Projection Installation Owner | `browser-first/test/fixtures/addon-consultation/exact-bundle-installation.json` | `node --test --test-name-pattern="W06 verifies exact bundle installation" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Receipt binds approved bytes to one host generation. | **Blocked: stale projection and receipt absent.** |
| W07 | Host status projection | `browser-first/test/fixtures/addon-consultation/status-ready.json` | `node --test --test-name-pattern="W07 derives orthogonal ready status" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | All dimensions permit derived `ready`; no registry persistence. | **Designed; blocked by W05-W06.** |
| W08 | Credential/token owner | `browser-first/test/fixtures/addon-consultation/credential-acquisition.json` | `node --test --test-name-pattern="W08 acquires route authentication credential" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Credential attached without exposing raw token. | Mechanism **executed-current**; binding **designed**. |
| W09 | Bridge admission owner | `browser-first/test/fixtures/addon-consultation/query-experience.json` | `node --test --test-name-pattern="W09 admits experience query through real loopback bridge" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Real loopback POST admits authenticated request. | Route **executed-current**; chain **blocked**. |
| W10 | Consultation policy owner | `browser-first/test/fixtures/addon-consultation/result-experience-ok.json` | `node --test --test-name-pattern="W10 returns bounded evidence and answer policy" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Bounded evidence, opaque handles, no-instruction policy, `authorityEffect: "none"`. | Host **executed-current**; chain **blocked**. |
| W11 | Consumer owner | `browser-first/test/fixtures/addon-consultation/generated-answer-cited.json` | `node --test --test-name-pattern="W11 composes consumer-owned GeneratedAnswer" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Consumer answer is distinct; evidence/policy unchanged. | **Designed; owner absent.** |
| W12 | Grant/credential owners, then UI | `browser-first/test/fixtures/addon-consultation/revoke-and-degrade.json` | `NODE_PATH="$(npm root -g)" node browser-first/test/addon-augmentor-consultation-ui.witness.mjs --case W12` | Revoke denies repeat call; UI degrades/hides without private detail. | Revocation **executed-current**; integrated/browser **absent**. |

The exact-byte end-to-end witness is **blocked at W05-W06**.

## Negative design: 24 independently runnable fixtures

| ID | Owner | Exact fixture path | Exact command | Observable assertion | Proof status |
|---|---|---|---|---|---|
| N01 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/missing-capability.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N01 rejects consultation without capability request"` | Reject `ONTOLOGY_CONSULTATION_CAPABILITY_REQUIRED`. | **Designed; absent.** |
| N02 | Grant owner/status | `browser-first/test/fixtures/addon-consultation/capability-requested-ungranted.json` | `node --test --test-name-pattern="N02 blocks requested but ungranted capability" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | `not-granted`, `blocked-grant`, no credential. | **Designed; absent.** |
| N03 | Consultation service | `browser-first/test/fixtures/addon-consultation/query-disallowed-runtime-view.json` | `node --test --test-name-pattern="N03 denies disallowed runtime view" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Denied; no protected metadata. | Host **executed-current**; fixture **designed**. |
| N04 | Bundle validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/bundles/malformed/` | `node --test --test-name-pattern="N04 rejects malformed bundle" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-bundle.test.mjs` | Reject before projection read; state `invalid`. | Behavior **executed-current**; fixture **designed**. |
| N05 | Bundle validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/bundles/stale/` | `node --test --test-name-pattern="N05 rejects stale bundle" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-projection.test.mjs` | Freshness failure; `valid-stale`; blocked. | **Executed-current failure/residue.** |
| N06 | Bundle validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/bundles/mixed-versions/` | `node --test --test-name-pattern="N06 rejects mixed contract versions" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-bundle.test.mjs` | Mixed family rejects; no downgrade. | Behavior **executed-current**; fixture **designed**. |
| N07 | Leakage validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/bundles/private-path-leak/` | `node --test --test-name-pattern="N07 rejects leakage-bearing bundle" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-leakage.test.mjs` | Leakage hits reject install; no private value in status/result. | Current bundle zero hits **executed-current**; fixture **designed**. |
| N08 | Consumer/policy | `browser-first/test/fixtures/addon-consultation/instruction-shaped-evidence.json` | `node --test --test-name-pattern="N08 returns instruction text with zero tool execution" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Evidence retained; tool-call spy exactly 0. | Host **executed-current**; consumer assertion **designed**. |
| N09 | Cache owner | `browser-first/test/fixtures/addon-consultation/cache-two-installations.json` | `node --test --test-name-pattern="N09 isolates two installation caches" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | `addon-a#1`/`addon-b#1` never cross-hit. | Base isolation **executed-current**; installation dimension **designed**. |
| N10 | SDK/consumer | `browser-first/test/fixtures/addon-consultation/source-handle-non-resolution.json` | `node --test --test-name-pattern="N10 source handle confers no resolution permission" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | No resolver; fetch spy 0; no path/URL/token interpretation. | **Designed; absent.** |
| N11 | Grant validator | `browser-first/test/fixtures/addon-consultation/evidence-as-grant.json` | `node --test --test-name-pattern="N11 evidence cannot satisfy grant record" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Evidence fails grant receipt; state unchanged. | **Designed; absent.** |
| N12 | Approval validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/receipts/evidence-as-approval.json` | `node --test --test-name-pattern="N12 evidence cannot satisfy bundle approval" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-bundle.test.mjs` | Evidence/metadata fails approval receipt. | Insufficiency **observed-current**; fixture **designed**. |
| N13 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/memory-write.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N13 rejects memory write operation"` | Reject memory-write field/operation. | **Designed; absent.** |
| N14 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/ontology-write.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N14 rejects ontology write operation"` | Reject write/mutation; no host call. | **Designed; absent.** |
| N15 | SDK/consumer | `src/sdk/addons/test-fixtures/ontology-consultation/routing-inference.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N15 rejects routing inference"` | Reject routing; no route decision. | **Designed; absent.** |
| N16 | SDK/consumer | `src/sdk/addons/test-fixtures/ontology-consultation/approval-inference.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N16 rejects approval inference"` | Reject approval; no receipt. | **Designed; absent.** |
| N17 | SDK/consumer | `src/sdk/addons/test-fixtures/ontology-consultation/effect-inference.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N17 rejects effect inference"` | Reject action; effect spy 0. | **Designed; absent.** |
| N18 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/manifest-grant-state.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N18 rejects manifest grant state"` | Reject `granted`; legacy parser never projects active grant. | **Designed; absent.** |
| N19 | Host negotiation | `browser-first/test/fixtures/addon-consultation/unsupported-major.json` | `node --test --test-name-pattern="N19 rejects unsupported major without downgrade" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Incompatible, blocked, no selected contract. | Unknown-version rejection **observed-current**; fixture **designed**. |
| N20 | Grant/credential lifecycle | `browser-first/test/fixtures/addon-consultation/revoked-disabled-expired.json` | `node --test --test-name-pattern="N20 blocks revoked disabled and expired installations" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Each state separately blocks credential/invocation/cache. | Revoke/expiry **executed-current**; disable **designed**. |
| N21 | Uninstall adapter | `browser-first/test/fixtures/addon-consultation/uninstall-preserves-shared-projection.json` | `node --test --test-name-pattern="N21 uninstall preserves shared projection" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Remove local grant; other client active; digest unchanged. | **Designed; absent.** |
| N22 | Status projection | `browser-first/test/fixtures/addon-consultation/status-redaction.json` | `node --test --test-name-pattern="N22 redacts status failures" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | No path, token, source, private term, stack, loader error. | Dependency redaction **executed-current**; SDK projection **designed**. |
| N23 | Deployment boundary | `browser-first/test/fixtures/addon-consultation/untrusted-proxy-header.json` | `node --test --test-name-pattern="N23 rejects untrusted deployment principal header" browser-first/test/augmentor-consultation-deployment.test.mjs` | Client header untrusted without proxy boundary; adapter undiscoverable. | **Designed; absent.** |
| N24 | Consumer owner | `browser-first/test/fixtures/addon-consultation/generated-answer-not-evidence.json` | `node --test --test-name-pattern="N24 keeps GeneratedAnswer distinct from evidence" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Answer fails evidence/grant/approval/route/effect validation. | **Designed; absent.** |

N20 is three separate cases under one fixture file, not one aggregate assertion. The reviewer rechecks confirm all 36 fixtures retain owner, exact locator, command, observation, and honest proof status.

## Local executable witness and current commands

The designed witness is W01→W12: manifest → validation → review → grant → exact-byte approval/install → derived status → credential → real loopback bridge → policy/evidence → consumer answer → revoke/degrade. It is finite but **not currently executable end to end**, because W05-W06 are blocked and the SDK integration fixtures are absent.

Current evidence includes `npx vitest run src/sdk/addons/validation.test.ts src/sdk/addons/registry.test.ts` (**executed-current 25/25**), host/bridge focused tests (**executed-current 11/11**), projection/bundle selected suite (**executed-current 29/30; freshness failure**), and independent leakage validation (**executed-current; zero hits**). The integrated Node test, SDK consultation test, and shared-runtime browser witness are **designed; absent**. No new test was run by the writer.

## Product residue and unresolved owner decisions

Blocking product residue:

1. Regenerate the current neutral projection and close its freshness failure.
2. Produce independently owned exact-byte approval and host installation receipts; deterministic `ownerApprovalRef` metadata is insufficient.

Unresolved decisions remain: name the projection approval owner, installation owner, product/UI owner, consumer answer owner, adapter owner, and any unified audit owner; decide installation identity in cache keys; grant binding to bundle/contract/policy/installation; whether requestable limits or expected digest pins are public; rollback retention/re-approval; degraded UI semantics; trusted-proxy/header-test ownership; and generation of public version constants.

## Claim ceiling

This research establishes an evidence-closed, reviewer-PASS design for a future Work Pack. It proves the current host route, capability spelling, authentication, external grant/revocation mechanics, closed contracts, cache partitioning, answer policy, and focused current tests, and it proves the SDK gap. It does **not** prove that the hybrid contract, adapter, status projection, lifecycle integration, `GeneratedAnswer`, fixture files, browser behavior, or full witness are implemented.

It also does not establish an acceptance-ready bundle, ontology authority or canonical truth, memory writes, permission to act, routing, approval, effects, deployment, promotion, release, or production readiness.
