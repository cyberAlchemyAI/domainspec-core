# REVISED SYNTHESIS RETURN

## Decision

Select a **hybrid additive SDK contract** that:

1. Exposes the already-owned runtime capability spelling `augmentor-consultation-read` in the public SDK capability vocabulary.
2. Adds an optional, request-only `ontologyConsultation` manifest declaration for compatibility, requested operations/views, freshness requirements, explanation profiles, and UI degradation behavior.
3. Makes the presence of `ontologyConsultation` require exactly one top-level `augmentor-consultation-read` capability request through SDK validation; the dependency is not serialized a second time.
4. Keeps installed-family negotiation, bundle identity, projection state, grant state, effective limits, and answer-policy state host-owned.
5. Reuses the existing neutral projection and `POST /augmentor/consultation` route.
6. Keeps add-on review, exact-byte bundle approval, bundle installation, grant creation, authentication-credential acquisition, route admission, and policy enforcement separate.
7. Treats discovery/status as a non-persistent host-owned read projection, not a second registry.
8. Makes generated prose a consumer-owned `GeneratedAnswer`, distinct from consultation evidence, explanation support, and host authority.

This is a future SDK design. The current SDK and consultation host are implemented and tested separately; their installation-linked adapter is absent.

## Evidence notation

- **E1** — `research.md#agent-1-sdk-runtime-explorer`; `receipts/explorer-sdk-runtime.json`.
- **E2** — `research.md#agent-2-ontology-projection-explorer`; `receipts/explorer-ontology-projection.json`; blocking residue at `orchestration/run-2026-08-06-augmentor-addon-sdk-ontology-api-01/residue/explorer-ontology-projection.json#/items`.
- **E3** — `research.md#agent-3-security-lifecycle-explorer`; `receipts/explorer-security-lifecycle.json`.
- **R-P** — `reviews.md#precedent-review`.
- **R-NV** — `reviews.md#non-vacuity-review`.
- **R-NC** — `reviews.md#non-collapse-review`.

## Current-state owner and contract map

| Concern | Current owner and exact selector | Proof status |
|---|---|---|
| SDK capability vocabulary | `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:4-20`; closed list at `src/sdk/addons/contracts.ts:24-43` | **Observed-current:** lacks `augmentor-consultation-read`. [E1; E3] |
| Add-on manifest | `src/core/contracts.ts:531-602`; `src/sdk/addons/contracts.ts:62-76` | **Observed-current:** has `augmentorSkills` and `memoryAccess`, but no consultation declaration. [E1; E3] |
| SDK validation | `src/sdk/addons/validation.ts:323-347` | **Observed-current:** closes capability requests against the SDK list; no consultation cross-field invariant. [E1; E3] |
| SDK registry | `src/sdk/addons/registry.ts:90-123` | **Observed-current:** owns manifest-request, installation, review, and verification state; no consultation-grant adapter. [E1; E3; R-P PR-010] |
| Host capability spelling | `browser-first/host/bridge-capability-tokens.mjs:23-53` | **Observed-current:** canonical spelling is `augmentor-consultation-read`. [E1; R-P PR-001] |
| Host route | `browser-first/host/augmentor-consultation-host-service.mjs:8-55` | **Observed-current:** `POST /augmentor/consultation`, guarded by that capability; context, views, and limits are host-derived. [E1; E3] |
| Route authentication | `bridge-server.mjs:1006-1012,1066-1098,1187-1191` | **Observed-current:** local route capability token; TLS/IP restrictions for non-loopback key access; credentials removed before handler invocation. [E3] |
| Credential/token owner | `bridge-capability-tokens.mjs:23-53`; `bridge-client.js:443-488`; `bridge-server.mjs:1019-1040,1110-1128` | **Observed-current:** owns route-scoped authentication credentials. It does not own add-on review, grants, routing decisions, or effects. [E1; R-P PR-012] |
| External grant registry | `augmentor-consultation-access.mjs:12-55,58-74,77-159` | **Observed-current:** hashed keys, views, limits, expiry, revocation, opaque principal, policy digest, registry revision. [E1; E3; R-P PR-011] |
| Neutral projection compiler | `projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/build-consumer-projection.mjs:11-29,45-47,53-72,86-167` | **Observed-current:** compiles allowlisted neutral records and opaque handles. Its deterministic approval-shaped reference is not independent approval proof. [E2] |
| Bundle validation | `augmentor-consultation-contract.mjs:285-365,382-415`; private schema `consumer-bundle-manifest.schema.json:3-21` | **Observed-current:** closed schema/version/digest validation and mixed-version rejection. [E2; E3] |
| Query contract | `augmentor-consultation-contract.mjs:139-167`; private `query.schema.json:3-44` | **Observed-current:** closed `lookup`, `search`, `context`, view, freshness, and bounded-limit request. [E2; E3] |
| Consultation service | `augmentor-consultation-service.mjs:252-357` | **Observed-current:** audience, grants, freshness, budgets, provenance, conflicts, cache, cancellation, and deadlines. [E1] |
| Cache | `augmentor-consultation-cache.mjs:7-59`; service `:276-288` | **Observed-current:** keys include principal, policy/revision, views, bundle, result version, operation/query/profile/scope, and limits. [E3] |
| Answer policy | `augmentor-consultation-answer-policy.mjs:1-24` | **Observed-current:** total answer/qualify/clarify/abstain mapping; retrieved instructions are not followed. The public consultation invariant reports `authorityEffect: "none"`. [E1; E3] |
| Generated answer | No owner or type was found in the selected current corpus | **Absent:** must be consumer-owned, not host evidence or authority. [R-NC NC-03] |
| Projection installation contract | `docs/reference/AUGMENTOR_CONSULTATION_API.md:22-34` | **Observed-current contract:** installation is independent and owner-approved; exact acting owner/receipt was not evidenced. [E1; E2; R-P PR-007] |
| Ownership boundary | `docs/architecture/MODULE-OWNERSHIP.md:20-35,43-47` | **Observed-current:** consultation modules do not own raw ontology, generated answers, memory writes, approval, routing, or authority. [E1; E3] |
| SDK-to-host adapter | Entire selected corpus | **Absent:** no manifest contract, cross-field validation, review-to-grant binding, host status projection, installation-bound credential acquisition, or lifecycle integration. [E1; E3] |

## Preserved semantic distinctions

| Concept | Owner and meaning | Must not become |
|---|---|---|
| `augmentorSkills` | SDK-declared operating guidance | Data access, route credential, grant, instruction authority, or ontology authority |
| `memoryAccess` | Living Archive policy | Consultation, projection access, ontology read/write, or evidence cache |
| Tool | Host-mediated callable action | Projection installer, consultation owner, or authority inference |
| Connector | External-system configuration/transport | Alias for the already-owned internal consultation route |
| Raw private ontology | Private candidate source | Public SDK content, runtime store, or authority |
| Neutral projection | Allowlisted evidence-bearing consumer bytes | Raw ontology, approval, installation receipt, grant, truth store, or authority |
| Exact bundle approval | Independent decision over exact source/compiler/schema/output epoch | Compiler output, validation pass, deterministic metadata, or add-on review |
| Bundle installation | Independent admission of exact approved bytes into host state | Add-on installation, projection approval, or capability request |
| Capability request | Unprivileged manifest intent | Add-on review, grant record, authentication credential, route admission, or policy result |
| Add-on review | SDK/host decision on the declared request | Grant record creation, bundle approval, or route authentication |
| Grant record | Host policy record binding installation identity to views/operations/limits | Review receipt, token, route admission, or evidence |
| Authentication credential | Route-scoped proof presented to the bridge | Routing decision, permission to perform effects, or answer authority |
| Route admission | Bridge authentication and capability gate | Grant creation or consultation-policy decision |
| Consultation policy | View, limit, freshness, bundle, evidence, and answer-policy enforcement | Authentication, review, routing, or effect execution |
| Source handle | Opaque evidence reference | Content, URL/path, credential, fetch permission, grant, approval, or authority |
| Consultation evidence | Bounded records/statements and handles | Instructions, generated answer, permission, memory write, approval, routing, or effect |
| Explanation support | Bounded support at `brief`, `guided`, or `deep` detail | Evidence truth, final prose, or authority |
| Answer policy | Host constraint on composition or abstention | Generated answer or authority decision |
| `GeneratedAnswer` | Consumer-owned prose constrained by answer policy | Evidence, explanation support, host output, permission, or authority |
| Public `authorityEffect: "none"` | Observed consultation-result invariant | Imported private definition, private prose, or a configurable manifest claim |

## Exact gaps

1. `augmentor-consultation-read` is absent from the SDK union and closed list. [E1 `contracts.ts:4-17`; E3 `contracts.ts:4-20`]
2. `AddOnManifest` has no consultation declaration. [E1 `contracts.ts:531-602`]
3. No cross-field invariant requires consultation declarations to request the capability. [E1/E3 `validation.ts:323-347`]
4. The current request representation appears to carry grant-shaped state; a request-only target type is needed so manifests never serialize effective grant state. [R-NC NC-04]
5. Registry state does not distinguish persisted declaration/review state from non-persistent host-derived consultation status. [E1/E3 `registry.ts:90-123`; R-P PR-015]
6. No add-on review receipt maps to a distinct consultation grant record.
7. No installation identity maps to the existing host grant registry.
8. No non-persistent host discovery/status projection exists for add-ons.
9. No installation-linked acquisition of route-scoped authentication credentials exists.
10. Disable, re-enable, upgrade, rollback, and uninstall do not drive existing grant and credential owners.
11. No named consumer owner/type exists for `GeneratedAnswer`.
12. Audit events lack a unified named owner; until one is selected, events must remain with their transactional owners.
13. No finite manifest-to-review-to-grant-to-credential-to-route-to-policy-to-evidence-to-answer/revocation witness exists.
14. **Blocking residue:** generated projection is stale; its focused suite passed 29/30 and failed freshness. [E2 executed validation; residue JSON `/items/0`]
15. **Blocking residue:** no independent exact-byte projection-approval or installation-owner receipt was observed; deterministic `ownerApprovalRef` is insufficient. [E2 compiler `:148-167`; residue JSON `/items/1`]

Items 14–15 block only acceptance-ready exact-byte bundle and executable end-to-end witness claims. They do not block the research design and do not justify a new owner.

## Option matrix

| Option | Owner fit | Verdict |
|---|---|---|
| No SDK change | Forces unsupported private invocation and bypasses SDK declaration/review/lifecycle | Rejected as target. |
| Reuse `augmentorSkills` | Operating guidance is not consultation access | Rejected: definitional collapse. |
| Reuse `memoryAccess` | Archive policy is not ontology consultation | Rejected: definitional collapse. |
| Generic tool or connector | Loses typed versions, host grant semantics, evidence policy, and route ownership | Rejected as primary seam. |
| Add only `ontologyConsultation` | Expresses compatibility but cannot enter capability review/admission | Rejected alone as vacuous. |
| Add only capability | Cannot express versions, operations, views, freshness, profiles, or UI degradation | Rejected alone as incomplete. |
| New consultation capability spelling | Duplicates current `augmentor-consultation-read` owner | Rejected. |
| **Hybrid existing capability + additive request + host status projection** | Reuses SDK and host owners without a new store, registry, service, or authority owner | **Selected; `build-from-owned`.** |

## Proposed public contract

```ts
export type Capability =
  | /* current values */
  | "augmentor-consultation-read";

export interface CapabilityRequest {
  capability: Capability;
  scope: "self";
  revocationBehavior: "hard-stop";
}

export type AugmentorConsultationOperation =
  | "lookup"
  | "search"
  | "context";

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
  // existing fields
  requestedCapabilities: readonly CapabilityRequest[];
  ontologyConsultation?: AddOnOntologyConsultationRequest;
}
```

There is no serialized `requiredCapability`. Validation owns the invariant:

```ts
if (
  manifest.ontologyConsultation &&
  countRequested(
    manifest.requestedCapabilities,
    "augmentor-consultation-read"
  ) !== 1
) {
  reject("ONTOLOGY_CONSULTATION_CAPABILITY_REQUIRED");
}
```

If the current SDK request schema requires a `granted` property, that is **legacy non-authoritative request-shape residue**. It is neither review approval nor an effective grant. The target type above removes it rather than perpetuating grant-shaped manifest state.

### Host-owned non-persistent status projection

```ts
export type AddOnConsultationStatus = {
  addonState:
    | "not-installed"
    | "installed-disabled"
    | "installed-enabled"
    | "uninstalled";

  projectionState:
    | "not-installed"
    | "invalid"
    | "valid-stale"
    | "valid-current";

  grantState:
    | "not-reviewed"
    | "review-denied"
    | "not-granted"
    | "active"
    | "revoked"
    | "expired";

  compatibilityState:
    | "unknown"
    | "compatible"
    | "incompatible";

  policyState:
    | "unknown"
    | "available"
    | "degraded"
    | "unavailable";

  invocationState:
    | "ready"
    | "blocked-addon"
    | "blocked-projection"
    | "blocked-grant"
    | "blocked-compatibility"
    | "blocked-policy";

  selectedContract?: {
    family: "augmentor.consultation";
    queryVersion: string;
    resultVersion: string;
  };

  effectiveOperations?: readonly AugmentorConsultationOperation[];
  effectiveViews?: readonly string[];
  explanationProfiles?: readonly ("brief" | "guided" | "deep")[];

  effectiveLimits?: {
    maxCandidates: number;
    maxRecords: number;
    maxSources: number;
    maxBytes: number;
    maxTokens: number;
    maxMillis: number;
  };

  projection?: {
    projectionDigest: string;
    bundleDigest: string;
    generatedAt: string;
  };

  sourceHandleSemantics?: "opaque-reference-only";
};
```

This object is derived on read from SDK installation/review state, the existing host loader, the existing grant registry, and the current policy. It persists no independent runtime truth and is not a second registry.

The orthogonal state fields prevent contradictions such as `available: true`, `granted: false`, and one ambiguous reason. `invocationState` is derived from the other dimensions.

### Evidence and generated-answer boundary

```ts
declare const sourceHandleBrand: unique symbol;

export type SourceHandle = string & {
  readonly [sourceHandleBrand]: "opaque-source-handle";
};

export type ConsultationEvidence = {
  status:
    | "ok"
    | "partial"
    | "no_match"
    | "insufficient_evidence"
    | "conflict"
    | "stale"
    | "denied"
    | "invalid_request"
    | "budget_exceeded"
    | "temporary_failure";
  records: readonly {
    statement: string;
    sourceHandles: readonly SourceHandle[];
  }[];
  explanationSupport?: unknown;
  answerPolicy: {
    disposition: "answer" | "qualify" | "clarify" | "abstain";
    citationsRequired: boolean;
    followsRetrievedInstructions: false;
  };
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

`GeneratedAnswer` is created by the consuming add-on/agent after applying the host answer policy. It is not returned consultation evidence, explanation support, a host decision, approval, grant, routing instruction, or authority.

No public SDK resolver is implied for `SourceHandle`. Possession of a handle confers no fetch permission and exposes no content, URL/path, credential, grant, approval, or authority.

## Proposed manifest

```json
{
  "sdkVersion": "0.2.0",
  "requestedCapabilities": [
    {
      "capability": "augmentor-consultation-read",
      "scope": "self",
      "revocationBehavior": "hard-stop"
    }
  ],
  "ontologyConsultation": {
    "provider": "host",
    "contractFamily": "augmentor.consultation",
    "supportedQueryVersions": [
      "augmentor.consultation.query@1.1.0"
    ],
    "supportedResultVersions": [
      "augmentor.consultation.result@1.1.0"
    ],
    "requestedOperations": ["lookup", "search", "context"],
    "requestedViews": ["experience", "runtime", "knowledge"],
    "explanationProfiles": ["brief", "guided"],
    "maxProjectionAgeSeconds": 86400,
    "unavailableBehavior": "degrade-ui"
  }
}
```

Forbidden fields include grant state, approval state, install state, actual bundle identity, paths, credentials, tokens, principals, source handles, effective limits, cache keys, `authorityEffect`, instructions, ontology/memory writes, routing, approval, promotion, or effects.

## Validation and version negotiation

### SDK validation owner

The SDK declaration/validation owner:

- Accepts the optional closed request object.
- Requires exactly one top-level `augmentor-consultation-read` request when the object is present.
- Rejects duplicate capability requests.
- Validates closed provider/family syntax and well-formed query/result version identifiers.
- Validates non-empty unique operation, view, version, and profile arrays.
- Rejects operations such as `write`, `approve`, `route`, `execute`, and memory mutation.
- Rejects credentials, paths, installed/granted assertions, and authority fields.
- Does **not** maintain a second hand-authored registry of installed or supported consultation versions.

If offline validation needs a finite public version list, it must import or generate constants from the consultation contract-family owner. It must not fork that truth into an independently edited SDK list. [R-P PR-004]

### Host negotiation owner

The existing consultation host:

1. Validates the independently installed exact bundle.
2. Selects one internally coherent installed query/result/projection/manifest/glossary family.
3. Intersects that family with the add-on’s declared compatibility.
4. Intersects requested operations/views with installed availability and the active grant.
5. Calculates effective limits as the minimum of service, grant/policy, and query.
6. Enforces freshness.
7. Returns `compatibilityState: "incompatible"` when no exact intersection exists.
8. Never silently downgrades.
9. Invalidates digest/policy-bound grants and cache reachability when bundle or policy identity changes.

SDK version and consultation-family versions remain independent. Adding the capability union member and optional manifest object warrants a proposed SDK minor bump from `0.1.0` to `0.2.0`; old manifests remain accepted. Exhaustive TypeScript switches may need source changes. [E1 compatibility effect]

## Separate decision and receipt owners

| Decision/artifact | Owner | Receipt | Boundary |
|---|---|---|---|
| Add-on declaration validation | SDK validator | `AddOnManifestValidationReceipt` | Proves schema acceptance only. |
| Add-on review decision | **SDK Add-on Review Owner**, using existing registry state at `src/sdk/addons/registry.ts:90-123` | `AddOnReviewReceipt` | Approves or denies the request; does not create a consultation grant. |
| Exact bundle approval | **Neutral Projection Approval Owner — acting owner unresolved and must be named before acceptance** | `NeutralProjectionApprovalReceipt` | Approves exact input/compiler/schema/output epoch; compiler metadata is insufficient. |
| Exact bundle installation | **Host Projection Installation Owner — acting owner unresolved and must be named before acceptance** | `NeutralProjectionInstallationReceipt` | Proves exact approved bytes were atomically installed into a host generation. |
| Consultation grant | Existing host grant-registry owner at `augmentor-consultation-access.mjs:12-159` through a designed installation adapter | `InstallationConsultationGrantReceipt` | Creates active installation-bound views/operations/limits. |
| Authentication credential acquisition | Existing bridge capability-token/access owner | Ephemeral credential issuance evidence, never manifest state | Supplies a route-scoped authentication credential only. |
| Route admission | Existing bridge server | Route outcome | Authenticates and admits/denies the request. |
| Policy enforcement | Existing consultation service and answer-policy owner | Consultation result/status | Enforces grant, freshness, limits, evidence, and answer policy. |
| Generated answer | Named consuming add-on/agent owner, still unresolved per product | Consumer-owned answer record | Composes or abstains; does not acquire authority. |

## Lifecycle and data flow

| Stage | Required behavior | Proof status |
|---|---|---|
| Manifest validation | Validate request-only declaration and top-level capability dependency | **Designed; absent.** |
| Add-on installation | Persist declaration and installation identity only | **Designed; adapter absent.** |
| Add-on review | SDK Add-on Review Owner records approve/deny decision | Existing review state **observed-current**; consultation-specific receipt **designed**. |
| Bundle approval | Neutral Projection Approval Owner approves exact epoch | **Blocked:** independent receipt absent. |
| Bundle installation | Host Projection Installation Owner atomically installs exact approved bundle | **Blocked:** receipt absent and generated projection stale. |
| Grant creation | Existing grant owner creates installation-bound subset grant after review | Grant mechanics **observed-current**; installation adapter **absent**. |
| Status projection | Host derives orthogonal status on read; no independent persistence | **Designed; absent.** |
| Credential acquisition | Existing token/access owner supplies a route-scoped authentication credential | Mechanism **executed-current**; installation binding **designed**. |
| Route admission | Bridge authenticates credential and capability before handler/cache | **Executed-current.** |
| Policy enforcement/query | Existing service enforces views, limits, freshness, bundle, provenance, cache, deadlines | **Executed-current.** |
| Evidence return | Host returns bounded evidence, opaque handles, explanation support, and answer policy | **Executed-current.** |
| Answer composition | Consumer constructs `GeneratedAnswer` or abstains under answer policy | **Designed; consumer owner absent.** |
| Revoke | Grant owner revokes first; credential owner removes/rotates credentials; changed policy makes cache unreachable | External behavior **executed-current**; installation lifecycle **absent**. |
| Disable | SDK registry marks disabled, then existing grant and credential owners block invocation; metadata remains | **Designed; absent.** |
| Re-enable | Requires a fresh grant decision; manifest state cannot resurrect access | **Designed; absent.** |
| Add-on upgrade | Revalidate; widened capability/views/operations/limits or contract major requires review and grant update | **Designed; absent.** |
| Bundle/API upgrade | Approval and installation owners admit exact coherent bytes; host renegotiates and rebinds affected grant/cache | Validation mechanics **observed-current**; integrated lifecycle **designed**. |
| Rollback | Restore only an approved, installed, compatible prior combination; never silently weaken versions | **Designed; absent.** |
| Uninstall | Remove installation-linked grant and UI state; retain shared projection and other clients | **Designed; absent.** |
| Projection removal | Host reports projection absent; no raw/private fallback | **Designed atop existing owner boundary.** |

## Audit split

No selected source proves a unified audit/retention owner. Until one is explicitly named:

- SDK registry owns declaration, validation, install, enable/disable, and add-on review events.
- Consultation grant registry owns grant, renewal, expiry, revoke, and installation-binding events.
- Consultation host owns discovery projection observations, route outcomes, query result status, bundle/policy identities, deadlines, and cache metrics.
- The consumer owns `GeneratedAnswer` provenance if such records are retained.
- A future audit projection may aggregate redacted events but must remain a read model, not a grant, review, installation, projection, or authority registry.

## Public/private packaging boundary

The public SDK may expose neutral contract names, public operation/view identifiers, compatibility intent, host-selected public contract versions, redacted opaque digests, freshness, effective limits, opaque-handle semantics, answer-policy status, and the observed consultation-result invariant `authorityEffect: "none"`.

It must not copy private node IDs, raw ontology records, CAV2 definitions or prose, repository paths, internal owner routes, private notes, credentials, source contents, private source-to-handle mappings, approval authority, or promotion state.

The use of `authorityEffect: "none"` here is limited to the observed public consultation invariant at `augmentor-consultation-answer-policy.mjs:1-24`. No private definition or prose is imported.

## Threat model

| Threat | Required control |
|---|---|
| Manifest self-grants | Request-only target type; host derives grant state. |
| Duplicate capability assertion | No serialized `requiredCapability`; one validator invariant. |
| SDK forks version truth | Syntax-only SDK validation or generated/imported public constants; host owns installed-family selection. |
| Add-on selects projection path/bundle | No path/install fields; existing loader owns bytes. |
| Review treated as grant | Separate `AddOnReviewReceipt` and `InstallationConsultationGrantReceipt`. |
| Credential treated as permission to act | Call it a route-scoped authentication credential; route and consultation policy still decide admission/result. |
| Overbroad views/limits | Installed/requested/granted intersection and effective minimum. |
| Mixed/stale/malformed/leaking bundle | Closed schema/version/digest/leakage/freshness validation before query. |
| Instruction-shaped evidence | Preserve as data; `followsRetrievedInstructions: false`; consumer harness asserts zero tool execution. |
| Evidence treated as grant/approval | Separate types and negative fixtures; evidence cannot satisfy either receipt schema. |
| Source handle treated as resolver | No public resolver; negative fixture proves no fetch and no path/URL interpretation. |
| Cache cross-talk | Installation-unique principal or explicit installation identity plus policy/revision, grant scope, bundle, version, query, profile, and limits. |
| Revoked caller reuses cache | Authentication precedes cache; credential removed; policy revision changes key reachability. |
| Silent downgrade | Exact host intersection or incompatible state. |
| Shared deployment adapter reused | Prohibited: shared principal/all-view/trusted-proxy shape is unsuitable. [E3 adapter `:13-22,47-97`] |
| Status leaks internals | Closed orthogonal states; redact paths, credentials, raw source, private vocabulary, and loader details. |
| Disable/uninstall deletes projection | Installation-scoped grant removal only. |
| Generated prose treated as host truth | Consumer-owned `GeneratedAnswer`, explicitly distinct from evidence and host authority. |

## Failure and status vocabulary

### Host-derived orthogonal state

- `addonState`: `not-installed`, `installed-disabled`, `installed-enabled`, `uninstalled`
- `projectionState`: `not-installed`, `invalid`, `valid-stale`, `valid-current`
- `grantState`: `not-reviewed`, `review-denied`, `not-granted`, `active`, `revoked`, `expired`
- `compatibilityState`: `unknown`, `compatible`, `incompatible`
- `policyState`: `unknown`, `available`, `degraded`, `unavailable`
- Derived `invocationState`: `ready`, `blocked-addon`, `blocked-projection`, `blocked-grant`, `blocked-compatibility`, `blocked-policy`

### Existing consultation-result state

- `ok`
- `partial`
- `no_match`
- `insufficient_evidence`
- `conflict`
- `stale`
- `denied`
- `invalid_request`
- `budget_exceeded`
- `temporary_failure`

[E2 `result.schema.json` selectors `/$defs/*` and `/oneOf`]

Discovery state and evidence-result state remain distinct. `denied` is not `no_match`; `stale` is not `partial`; `conflict` stays structured.

## Dependency-ordered implementation slices

1. Add SDK vocabulary parity for existing `augmentor-consultation-read`.
2. Introduce request-only `CapabilityRequest` and optional closed `ontologyConsultation`.
3. Add cross-field validation and SDK/host capability parity tests.
4. Persist declaration/review metadata only in the existing SDK registry.
5. Define `AddOnReviewReceipt`, `NeutralProjectionApprovalReceipt`, `NeutralProjectionInstallationReceipt`, and `InstallationConsultationGrantReceipt` as separate artifacts.
6. Implement the installation-identity adapter to the existing grant owner; own no state independently.
7. Implement the non-persistent host status projection with orthogonal states.
8. Bind installation grants to acquisition of route-scoped authentication credentials.
9. Implement disable/re-enable/upgrade/rollback/uninstall calls into existing grant/credential owners.
10. Add the consumer-owned `GeneratedAnswer` boundary.
11. Split audit events among transactional owners pending a named audit owner.
12. Regenerate and validate the neutral bundle through its owner.
13. Obtain independent exact-byte approval and installation receipts.
14. Execute SDK, host, integrated, leakage, and browser matrices.
15. Publish migration, lifecycle, security, and consumer-composition documentation.

Slices 1–11 may be developed against designed fixtures. Slices 12–13 must close before an acceptance-ready exact-byte or executable end-to-end claim.

## Exact target commands

These commands are **designed** unless explicitly marked executed-current.

```text
# SDK unit fixtures — designed target
npx vitest run src/sdk/addons/ontology-consultation.test.ts

# Existing focused SDK suites — executed-current by E3: 25/25
npx vitest run src/sdk/addons/validation.test.ts src/sdk/addons/registry.test.ts

# Existing host/bridge suites — executed-current by E3: 11/11
node --test browser-first/test/augmentor-consultation.test.mjs browser-first/test/augmentor-consultation-deployment.test.mjs

# Integrated manifest-to-host witness — designed target
node --test browser-first/test/addon-augmentor-consultation-integration.test.mjs

# Projection/bundle suite — designed target command; current selected suite was 29/30
node --test projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-projection.test.mjs projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-bundle.test.mjs

# Leakage suite — designed target command; current independent leakage validation passed with zero hits
node --test projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-leakage.test.mjs

# Shared-runtime browser degraded-state witness — designed target; no repository package root
NODE_PATH="$(npm root -g)" node browser-first/test/addon-augmentor-consultation-ui.witness.mjs
```

The designed paths are exact target locators, not claims that those files currently exist.

## Finite positive witness

| ID | Owner | Exact proposed fixture path | Exact command | Expected observable assertion | Proof status |
|---|---|---|---|---|---|
| W01 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/valid-request.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "W01 validates request-only consultation manifest"` | Manifest passes; exactly one top-level `augmentor-consultation-read`; no grant field exists. | **Designed; absent.** |
| W02 | SDK registry | Same manifest plus `src/sdk/addons/test-fixtures/ontology-consultation/install-enabled.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "W02 persists declaration without runtime truth"` | Registry stores request/review metadata but no projection, grant, compatibility, credential, or invocation state. | **Designed; absent.** |
| W03 | SDK Add-on Review Owner | `browser-first/test/fixtures/addon-consultation/review-approved-experience.json` | `node --test --test-name-pattern="W03 records review separately from grant" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | `AddOnReviewReceipt` approves requested `experience`; no grant record or credential exists yet. | **Designed; absent.** |
| W04 | Existing host grant owner through adapter | `browser-first/test/fixtures/addon-consultation/grant-experience-only.json` | `node --test --test-name-pattern="W04 creates installation-bound grant" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | `InstallationConsultationGrantReceipt` records only `experience`; review receipt remains separate. | **Designed; adapter absent.** |
| W05 | Neutral Projection Approval Owner | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/receipts/exact-bundle-approval.json` | `node --test --test-name-pattern="W05 verifies independent exact bundle approval" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-bundle.test.mjs` | Exact compiler/input/schema/output digests match an independently signed/owned approval receipt. | **Blocked:** current independent approval receipt absent. |
| W06 | Host Projection Installation Owner | `browser-first/test/fixtures/addon-consultation/exact-bundle-installation.json` | `node --test --test-name-pattern="W06 verifies exact bundle installation" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Installation receipt binds the approved exact bundle to one host generation. | **Blocked:** stale projection and installation receipt absent. |
| W07 | Consultation host status projection | `browser-first/test/fixtures/addon-consultation/status-ready.json` | `node --test --test-name-pattern="W07 derives orthogonal ready status" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | States are enabled/current/active/compatible/available and derived `invocationState` is `ready`; facts are not persisted in SDK registry. | **Designed; blocked by W05–W06.** |
| W08 | Credential/token owner | `browser-first/test/fixtures/addon-consultation/credential-acquisition.json` | `node --test --test-name-pattern="W08 acquires route authentication credential" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Route-scoped authentication credential is acquired/attached; raw token material is not exposed to add-on code. | Host mechanism **executed-current**; installation binding **designed.** |
| W09 | Bridge route-admission owner | `browser-first/test/fixtures/addon-consultation/query-experience.json` | `node --test --test-name-pattern="W09 admits experience query through real loopback bridge" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Real loopback `POST /augmentor/consultation` admits the authenticated capability request. | Route segment **executed-current**; full adapter chain **blocked.** |
| W10 | Consultation service/policy owner | `browser-first/test/fixtures/addon-consultation/result-experience-ok.json` | `node --test --test-name-pattern="W10 returns bounded evidence and answer policy" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Bounded evidence, opaque handles, policy with no instruction following, and public `authorityEffect: "none"` are observed. | Host behavior **executed-current**; full chain **blocked.** |
| W11 | Consumer owner | `browser-first/test/fixtures/addon-consultation/generated-answer-cited.json` | `node --test --test-name-pattern="W11 composes consumer-owned GeneratedAnswer" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Consumer creates cited `GeneratedAnswer`; evidence and policy objects remain unchanged and distinct. | **Designed; consumer owner absent.** |
| W12 | Grant and credential owners, then UI | `browser-first/test/fixtures/addon-consultation/revoke-and-degrade.json` | `NODE_PATH="$(npm root -g)" node browser-first/test/addon-augmentor-consultation-ui.witness.mjs --case W12` | Revocation removes invocation readiness; repeated query is denied; UI shows degraded/hidden state without private details. | External revocation **executed-current**; integrated/browser case **absent.** |

The exact-byte end-to-end witness remains blocked at W05–W06.

## Independently runnable negative fixtures

| ID | Owner | Exact proposed fixture path | Exact command | Expected observable assertion | Proof status |
|---|---|---|---|---|---|
| N01 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/missing-capability.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N01 rejects consultation without capability request"` | Reject `ONTOLOGY_CONSULTATION_CAPABILITY_REQUIRED`. | **Designed; absent.** |
| N02 | Host grant owner/status projection | `browser-first/test/fixtures/addon-consultation/capability-requested-ungranted.json` | `node --test --test-name-pattern="N02 blocks requested but ungranted capability" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | `grantState: not-granted`; `invocationState: blocked-grant`; no route credential. | **Designed; absent.** |
| N03 | Consultation service | `browser-first/test/fixtures/addon-consultation/query-disallowed-runtime-view.json` | `node --test --test-name-pattern="N03 denies disallowed runtime view" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | `denied`; no protected projection/grant metadata disclosed. | Host behavior **executed-current**; installation fixture **designed.** |
| N04 | Bundle validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/bundles/malformed/` | `node --test --test-name-pattern="N04 rejects malformed bundle" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-bundle.test.mjs` | Bundle load rejects before projection read; status projects `projectionState: invalid`. | Current malformed behavior **executed-current**; exact target fixture **designed.** |
| N05 | Bundle validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/bundles/stale/` | `node --test --test-name-pattern="N05 rejects stale bundle" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-projection.test.mjs` | Freshness failure; `projectionState: valid-stale`; invocation blocked. | **Executed-current failure/blocking residue.** |
| N06 | Bundle validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/bundles/mixed-versions/` | `node --test --test-name-pattern="N06 rejects mixed contract versions" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-bundle.test.mjs` | Mixed query/result/projection/manifest/glossary family rejects; no downgrade. | Mixed-version behavior **executed-current**; exact fixture **designed.** |
| N07 | Leakage validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/bundles/private-path-leak/` | `node --test --test-name-pattern="N07 rejects leakage-bearing bundle" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-leakage.test.mjs` | Non-empty leakage hits reject installation; no private value reaches status/result. | Leakage validator **executed-current pass on current bundle**; negative fixture **designed.** |
| N08 | Consumer harness and answer policy | `browser-first/test/fixtures/addon-consultation/instruction-shaped-evidence.json` | `node --test --test-name-pattern="N08 returns instruction text with zero tool execution" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Text remains evidence; tool-call spy count is exactly `0`; policy says not to follow retrieved instructions. | Host data behavior **executed-current**; zero-tool consumer assertion **designed.** |
| N09 | Cache owner | `browser-first/test/fixtures/addon-consultation/cache-two-installations.json` | `node --test --test-name-pattern="N09 isolates two installation caches" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Installations `addon-a#1` and `addon-b#1`, distinct policies/grants/bundle digests, produce no cross-hit; cache-hit counters remain installation-local. | Principal/policy isolation **executed-current**; installation dimension **designed.** |
| N10 | SDK/consumer boundary | `browser-first/test/fixtures/addon-consultation/source-handle-non-resolution.json` | `node --test --test-name-pattern="N10 source handle confers no resolution permission" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | No SDK resolver exists; fetch spy count is `0`; handle is not interpreted as path, URL, credential, or content. | **Designed; absent.** |
| N11 | Grant validator | `browser-first/test/fixtures/addon-consultation/evidence-as-grant.json` | `node --test --test-name-pattern="N11 evidence cannot satisfy grant record" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Evidence object fails `InstallationConsultationGrantReceipt`; `grantState` remains unchanged. | **Designed; absent.** |
| N12 | Bundle approval validator | `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/fixtures/receipts/evidence-as-approval.json` | `node --test --test-name-pattern="N12 evidence cannot satisfy bundle approval" projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consumer-bundle.test.mjs` | Evidence/deterministic `ownerApprovalRef` fails `NeutralProjectionApprovalReceipt`. | Metadata insufficiency **observed-current**; fixture **designed.** |
| N13 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/memory-write.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N13 rejects memory write operation"` | Reject unknown/forbidden memory-write field or operation. | **Designed; absent.** |
| N14 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/ontology-write.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N14 rejects ontology write operation"` | Reject `write`/ontology mutation; no call reaches host. | **Designed; absent.** |
| N15 | SDK validator/consumer | `src/sdk/addons/test-fixtures/ontology-consultation/routing-inference.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N15 rejects routing inference"` | Reject routing field/operation; evidence cannot produce a route decision. | **Designed; absent.** |
| N16 | SDK validator/consumer | `src/sdk/addons/test-fixtures/ontology-consultation/approval-inference.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N16 rejects approval inference"` | Reject approval field/operation; no review/approval receipt is created. | **Designed; absent.** |
| N17 | SDK validator/consumer | `src/sdk/addons/test-fixtures/ontology-consultation/effect-inference.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N17 rejects effect inference"` | Reject effect/action field; effect spy count is `0`. | **Designed; absent.** |
| N18 | SDK validator | `src/sdk/addons/test-fixtures/ontology-consultation/manifest-grant-state.json` | `npx vitest run src/sdk/addons/ontology-consultation.test.ts -t "N18 rejects manifest grant state"` | Target schema rejects `granted`; legacy parser, if retained, marks it non-authoritative and never projects active grant. | **Designed; absent.** |
| N19 | Host negotiation owner | `browser-first/test/fixtures/addon-consultation/unsupported-major.json` | `node --test --test-name-pattern="N19 rejects unsupported major without downgrade" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | `compatibilityState: incompatible`; `invocationState: blocked-compatibility`; selected contract absent. | Host unknown-version rejection **observed-current**; adapter fixture **designed.** |
| N20 | Grant/credential lifecycle owners | `browser-first/test/fixtures/addon-consultation/revoked-disabled-expired.json` | `node --test --test-name-pattern="N20 blocks revoked disabled and expired installations" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Each state independently blocks credential acquisition/invocation; no cache result returned. | Revoked/expired host cases **executed-current**; disable binding **designed.** |
| N21 | Uninstall adapter | `browser-first/test/fixtures/addon-consultation/uninstall-preserves-shared-projection.json` | `node --test --test-name-pattern="N21 uninstall preserves shared projection" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Installation grant removed; other client remains active; shared projection digest unchanged. | **Designed; absent.** |
| N22 | Status projection | `browser-first/test/fixtures/addon-consultation/status-redaction.json` | `node --test --test-name-pattern="N22 redacts status failures" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | No path, credential, raw source, private vocabulary, stack, or loader error appears. | Current dependency redaction **executed-current**; SDK projection **designed.** |
| N23 | Deployment boundary | `browser-first/test/fixtures/addon-consultation/untrusted-proxy-header.json` | `node --test --test-name-pattern="N23 rejects untrusted deployment principal header" browser-first/test/augmentor-consultation-deployment.test.mjs` | Direct client-supplied principal header is not trusted without the configured proxy boundary; adapter remains undiscoverable to add-ons. | Explicit header-stripping fixture **absent/designed.** |
| N24 | Consumer owner | `browser-first/test/fixtures/addon-consultation/generated-answer-not-evidence.json` | `node --test --test-name-pattern="N24 keeps GeneratedAnswer distinct from evidence" browser-first/test/addon-augmentor-consultation-integration.test.mjs` | Generated answer cannot validate as consultation result, grant, approval, route, or effect record. | **Designed; absent.** |

Each negative has one independently addressable fixture, command, and assertion. Compound lifecycle values in N20 must be implemented as separate test cases under the same fixture file, not one aggregate assertion.

## Migration and documentation obligations

- Bump the SDK minor version and document exhaustive-switch impact.
- Preserve old manifests unchanged.
- Publish the request-only capability shape and closed `ontologyConsultation` schema.
- Document the cross-field capability invariant; do not serialize `requiredCapability`.
- Document current `granted` request syntax, if required, as legacy non-authoritative residue and migrate to request-only shape.
- Document declaration, add-on review, grant record, authentication credential, route admission, policy enforcement, evidence, and generated answer as separate stages.
- Document SDK version versus host-owned consultation-family negotiation.
- Document the non-persistent orthogonal status projection.
- Document the separate add-on review, exact bundle approval, bundle installation, and consultation-grant receipts.
- Document source-handle non-resolution and lack of fetch permission.
- Document `augmentorSkills`, `memoryAccess`, tools/connectors, projection, evidence, explanation support, answer policy, and `GeneratedAnswer` separately.
- Document audit event ownership until a unified owner is named.
- Document disable, re-enable, revoke, expiry, upgrade, rollback, uninstall, and shared-projection retention.
- Document the public/private allowlist and that public `authorityEffect: "none"` is an observed consultation invariant, not imported private prose.
- Publish all positive and negative fixture contracts and designed commands.
- State that validation is not review, grant, approval, installation, deployment, promotion, release, or production readiness.

## Unresolved owner decisions

1. Name the concrete Neutral Projection Approval Owner.
2. Name the concrete Host Projection Installation Owner.
3. Name the product/UI owner for add-on review and orthogonal degraded status.
4. Name the consumer owner for `GeneratedAnswer`.
5. Decide which existing component owns the installation-identity adapter without becoming a registry.
6. Decide whether installation identity is already encoded by opaque principal or must be added explicitly to cache keys.
7. Decide grant binding across bundle digest, contract major, policy digest, and installation identity.
8. Decide whether requestable limits are public or only host-returned.
9. Decide whether expected digest pins are ever allowed as compatibility intent; they cannot assert installation.
10. Name a unified audit/retention owner, or ratify the transactional split.
11. Define rollback retention and re-approval rules.
12. Confirm `degrade-ui` and `hide-ui`; invocation always fails closed.
13. Name the trusted-proxy owner and header-stripping acceptance test owner.
14. Decide how generated/imported public version constants are produced if SDK offline validation needs them.

## Claim ceiling

Current evidence proves that the host consultation route, existing capability spelling, authentication, external grant/revocation, closed contracts, bundle-validation mechanics, cache partitioning, answer policy, and focused host tests exist. It also proves that the SDK currently lacks the capability and consultation declaration.

The hybrid SDK contract, request-only capability representation, status projection, review/grant adapter, installation-linked credential flow, UI, lifecycle, audit integration, `GeneratedAnswer`, proposed fixtures, and full witness are **designed**, not implemented.

The stale generated projection and absent independent exact-byte approval/install receipts block an acceptance-ready exact-byte bundle and executable end-to-end witness. They do not block this research synthesis and do not establish a need for a new owner.

Nothing here proves ontology authority, canonical truth, memory writes, permission to act, routing, approval, effects, promotion, deployment, release, or production readiness.

## RECEIPT PAYLOAD

```json
{
  "status": "pass",
  "validation": "pass",
  "artifacts": ["synthesis.md"],
  "blockers": [],
  "started_at": "2026-08-06T14:54:00-03:00",
  "finished_at": "2026-08-06T15:04:00-03:00"
}
```

Residue:

- Acceptance-ready exact-byte bundle and executable end-to-end witness claims remain blocked because the current generated consumer projection is stale relative to current compiler inputs; the focused suite passed 29/30 and failed projection freshness.
- Acceptance-ready exact-byte bundle and executable end-to-end witness claims remain blocked because no independently evidenced exact-byte projection-approval receipt or installation-owner receipt was observed; deterministic `ownerApprovalRef` metadata is insufficient.
