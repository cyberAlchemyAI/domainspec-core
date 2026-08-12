# Explorer Returns

## Agent 1 — SDK and runtime explorer

# EXPLORER RETURN — SDK and Runtime

## Decision

The smallest owner-preserving seam is a hybrid additive contract:

1. Add `augmentor-consultation-read` to the SDK `Capability` union.
2. Add an optional manifest field describing an add-on’s consultation compatibility and requested views.
3. Keep availability, installed projection identity, allowed views, limits, grant state, tokens, and answer policy host-derived.
4. Reuse the existing `POST /augmentor/consultation` route. Do not create a second SDK service, connector, projection store, or ontology API.
5. Treat the manifest as a request plus compatibility declaration, never as evidence that consultation is installed, enabled, granted, or authoritative.

This closes the current SDK/host mismatch while preserving the existing owners.

## Current-state classification

| Concern | Current owner and selector | State | Proof |
|---|---|---:|---|
| SDK capability vocabulary | `src/core/contracts.ts:4-17`, `Capability` | Does not contain `augmentor-consultation-read` | observed |
| SDK capability validation | `src/sdk/addons/contracts.ts`, `ADDON_CAPABILITIES`; `validation.ts:323-347` | Closed against the SDK union/list; the host-only name is rejected as unsupported | observed |
| Add-on manifest | `src/core/contracts.ts:531-602`, `AddOnManifest` | Has tools, connectors, `augmentorSkills`, and `memoryAccess`; no consultation field | observed |
| Manifest semantics | `ADR-018-addon-sdk-v0.md:36-51,218-250,322-352` | Manifest requests capabilities; tools are host-mediated; skills guide workflow but grant no authority | observed |
| Augmentor Chat manifest | `public/addons/augmentor-chat.json:30-66` | Requests chat, provider, archive, notification, and delegation capabilities; requests no consultation capability | observed |
| Host route | `browser-first/host/augmentor-consultation-host-service.mjs:8-58` | Implements `POST /augmentor/consultation`, requires `augmentor-consultation-read`, derives views/limits from authentication, and returns consultation plus answer policy | observed |
| Bridge capability registry | `browser-first/host/bridge-capability-tokens.mjs:23-53` | Canonically includes and mints `augmentor-consultation-read` | observed |
| Bridge client mapping | `browser-first/resonantos-side-panel-extension/src/lib/bridge-client.js:24-50` | Maps `POST /augmentor/consultation` to the same capability | observed |
| Runtime token delivery | `bridge-client.js:443-488`; `bridge-server.mjs:1019-1040,1110-1128` | Tokens are runtime-bootstrapped, scoped, and not manifest/config facts | observed |
| External-agent access | `augmentor-consultation-access.mjs:77-163` | Separate hashed client-key registry owns allowed views, limits, expiry, and revocation | observed |
| Local access | `augmentor-consultation-host-service.mjs:27-34` | Local Augmentor receives host-derived context and all four current views | observed |
| Projection installation | `AUGMENTOR_CONSULTATION_API.md:22-34` | Explicit owner-approved bundle installation into user state; bridge never reads private ontology checkout | observed |
| Query/result versions | `augmentor-consultation-contract.mjs:5-13,139-163,324-353` | Closed `@1.1.0` contract family; rejects unsupported and mixed bundle versions | observed |
| Answer policy | `augmentor-consultation-answer-policy.mjs:1-24` | Total mapping: answer/qualify/clarify/abstain; citations required when evidence is usable; retrieved instructions false; authority effect none | observed |
| Consultation behavior | `augmentor-consultation-service.mjs:252-357` | Enforces audience, grant views, freshness, budgets, source binding, conflict handling, cache separation, cancellation, and deadlines | observed |
| Registry/install state | `src/sdk/addons/registry.ts:80-123`; `registry.test.ts:112-132` | Enabled state is derived only from host-owned installation records | observed |
| Ownership boundary | `MODULE-OWNERSHIP.md:28-29,46-47,63` | Consultation host owns read behavior; SDK owns declarations/validation; manifest presence is not installation, enablement, or grant authority | observed |
| End-to-end tests | focused test execution | 17/17 Node consultation/bridge tests and 31/31 SDK tests passed | executed |
| Add-on-to-consultation integration | Entire selected source set | No manifest field, validator rule, registry projection, add-on grant flow, or add-on-facing consultation client exists | absent |

## Semantic distinctions

| Concept | Meaning | Must not collapse into |
|---|---|---|
| `augmentorSkills` | Reusable operating guidance for Augmentor | Data access, route access, grant, tool, ontology authority |
| `memoryAccess` | Living Archive read/intake policy | Ontology projection access or consultation |
| `connectors` | Declared paths to external systems requiring host-mediated configuration | An already host-owned internal route unless an actual external transport is being packaged |
| `tools` | Host-mediated callable actions with input/output schemas | Projection installation, capability grant, or answer generation |
| Projection installation | Owner-approved deployment of verified neutral bytes into host state | Add-on installation or manifest validation |
| Consultation access | Capability/grant-mediated permission to query the installed projection | Projection existence, ontology authority, memory access |
| Consultation evidence | Bounded records/statements and opaque source handles | Instructions, permission, approval, routing, or final answer |
| Answer policy | Host-returned rule for composing or abstaining | Generated answer or authority decision |

## Proposed additive contracts

```ts
export type Capability =
  | /* existing values */
  | "augmentor-consultation-read";

export type AugmentorConsultationOperation =
  | "lookup"
  | "search"
  | "context";

export interface AddOnOntologyConsultationContract {
  provider: "host";
  contractFamily: "augmentor.consultation";
  supportedQueryVersions: string[];
  supportedResultVersions: string[];
  requestedViews: string[];
  operations: AugmentorConsultationOperation[];
  explanationProfiles?: Array<"brief" | "guided" | "deep">;
  requiredCapability: "augmentor-consultation-read";
  unavailableBehavior: "degrade" | "hard-stop";
}

export interface AddOnManifest {
  // existing fields
  ontologyConsultation?: AddOnOntologyConsultationContract;
}
```

Candidate manifest:

```json
{
  "sdkVersion": "0.2.0",
  "requestedCapabilities": [
    {
      "capability": "augmentor-consultation-read",
      "granted": false,
      "scope": "self",
      "revocationBehavior": "degrade"
    }
  ],
  "ontologyConsultation": {
    "provider": "host",
    "contractFamily": "augmentor.consultation",
    "supportedQueryVersions": ["augmentor.consultation.query@1.1.0"],
    "supportedResultVersions": ["augmentor.consultation.result@1.1.0"],
    "requestedViews": ["experience", "runtime", "knowledge"],
    "operations": ["lookup", "search", "context"],
    "explanationProfiles": ["brief", "guided"],
    "requiredCapability": "augmentor-consultation-read",
    "unavailableBehavior": "degrade"
  }
}
```

The field deliberately omits:

- projection path or installation instruction;
- projection or bundle digest claimed by the add-on;
- credentials or capability tokens;
- effective allowed views or limits;
- source handles;
- answer-policy claims;
- ontology write, approval, routing, memory-write, or effect authority.

Those are host facts returned by discovery or invocation.

## Validator and registry delta

Validator additions:

- Recognize the new capability.
- Require `ontologyConsultation.requiredCapability` to equal `augmentor-consultation-read`.
- Require that capability in `requestedCapabilities`.
- Require unique, non-empty requested views and operations.
- Accept only the named provider, contract family, operations, profiles, and degradation modes.
- Require parseable contract-family version strings.
- Reject secrets, paths, projection digests, grants, effective limits, `authorityEffect`, or installation commands inside this field.
- Reject consultation fields attached to tools/connectors as alternate owners.
- Preserve the existing rule that a preset may grant only a requested capability.

Registry projection should expose only declaration metadata:

```ts
ontologyConsultation?: {
  requested: true;
  requestedViews: string[];
  compatibleQueryVersions: string[];
  compatibleResultVersions: string[];
};
```

A separate host-derived runtime view should report:

```ts
type ConsultationAvailability = {
  available: boolean;
  granted: boolean;
  effectiveViews: string[];
  queryVersion?: string;
  resultVersion?: string;
  projectionDigest?: string;
  freshness?: "fresh" | "stale";
  reason?: "not-installed" | "disabled" | "not-granted" |
           "version-mismatch" | "projection-invalid" | "revoked";
};
```

`projectionDigest`, freshness, and effective views become reportable only after the host validates installed bytes and the effective grant.

## Lifecycle behavior

| Event | Required behavior |
|---|---|
| Install add-on | Validate declaration; do not install a projection and do not grant consultation |
| Enable | Resolve host availability and effective grant; degrade or stop according to the manifest |
| Grant | Human/host reviews the capability and view subset; effective views may be narrower than requested |
| Invoke | Host attaches route-scoped authentication and sends the closed query; add-on never receives raw bridge tokens |
| Disable | Remove add-on exposure and stop new calls; do not delete the shared projection or other clients’ grants |
| Revoke | New calls fail closed; invalidate/partition cached state through policy/registry revision |
| Upgrade add-on | Revalidate manifest and contract-version intersection; newly requested views/capabilities require fresh review |
| Upgrade projection/API | Host reports supported versions; no intersection means degraded/blocked, never silent downgrade |
| Roll back | Restore a previously supported add-on/host combination only if installed projection validation still passes |
| Uninstall add-on | Remove add-on installation and its grant binding; retain shared host projection unless its independent owner requests removal |
| Remove projection | Host reports unavailable; add-ons degrade or stop without changing their manifest or memory |

## Comparative precedent

| Precedent | Fit | Non-fit |
|---|---|---|
| MCP initialization/version and capability negotiation | Supports host-derived availability and explicit version intersection before operation | MCP need not become the transport; the existing host route already owns transport |
| WebExtension required/optional permissions | Supports separating declaration from runtime grant and revocation | Browser permission semantics do not define ResonantOS views, projection provenance, or answer policy |
| JSON Schema 2020-12 closed validation | Supports machine-closed additive object validation and versioned schemas | It does not own runtime authorization or ontology semantics |
| JSON-LD/RDF dataset interchange | Could support a future interoperable semantic projection | Current implementation uses a deliberately closed neutral JSON projection; RDF is not required and adopting it now would widen scope and ownership |

Official precedents consulted: [MCP lifecycle and capability negotiation](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle), [WebExtension optional permissions](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/optional_permissions), [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12), and [JSON-LD 1.1 API](https://www.w3.org/TR/json-ld11-api/). Their use above is comparative; the selected shape remains a repository-specific inference.

## Fixtures

Positive:

1. Manifest requests the new capability and a subset of views; validator passes.
2. Host has a valid `@1.1.0` projection and reviewed subset grant; availability is true.
3. Closed query traverses manifest validation → host grant → bridge route → bounded evidence → answer policy.
4. `ok` permits a cited answer; `partial` requires qualification.
5. Disable/revoke makes subsequent invocation unavailable without affecting unrelated clients.
6. Existing manifests without `ontologyConsultation` continue to validate unchanged.

Negative:

1. Consultation field without requested capability.
2. Capability required by field but unsupported by SDK version.
3. Manifest claims `granted: true` as runtime proof.
4. Requested view outside host-approved views.
5. Unsupported/mixed query, result, manifest, projection, or glossary version.
6. Missing, malformed, stale, or leakage-invalid projection.
7. Instruction-shaped retrieved text; policy must keep `followRetrievedInstructions: false`.
8. Cross-principal or cross-policy cache reuse.
9. Add-on supplies projection path, access key, capability token, or effective grant.
10. Tool/connector bypasses the host route.
11. Attempted ontology write, memory write, approval, routing, or authority inference.
12. Uninstall deletes the shared projection or another client’s access.
13. Silent downgrade when no contract-version intersection exists.

## Developer-facing witness

Proposed finite witness:

1. Load a concrete manifest containing the candidate field.
2. `validateAddOnManifest` passes and registry records only the request.
3. Host installation state says enabled, but consultation remains unavailable until separately granted.
4. Host discovery reports installed `@1.1.0` contracts and a compatible projection.
5. Human grants `augmentor-consultation-read` with `experience` only.
6. Add-on invokes an `experience` query through the host mediator.
7. Bridge authenticates the route; consultation returns bounded evidence and host answer policy.
8. A `runtime` query is denied because the effective grant excludes that view.
9. Revocation causes the original query to return unauthorized/denied.
10. No test exposes a raw token, private source path, raw ontology record, or write/authority effect.

Current tests already prove steps 6–9 at the host/bridge layer, but steps 1–5 are proposed and remain unimplemented.

## Compatibility effect

Adding a union member is source-compatible for existing manifests but may break exhaustive TypeScript switches. Adding an optional manifest field is JSON-compatible, yet changing the stable capability vocabulary merits an SDK minor bump from `0.1.0` to `0.2.0`. Existing `0.1.0` manifests remain accepted; manifests using the new field require an SDK/host declaring `0.2.x` support. Consultation’s independent `@1.1.0` versions must not be inferred from the SDK version.

## Claim ceiling

Observed and executed evidence establishes that the consultation service, bridge capability, authentication, revocation, closed contracts, answer policy, and focused tests exist and pass. It also establishes that the Add-on SDK does not model them. The additive SDK contract, registry projection, grant binding, discovery API, lifecycle wiring, fixtures, and complete manifest-to-host witness are designed here, not implemented.

## RECEIPT PAYLOAD

```json
{
  "status": "pass",
  "validation": "pass",
  "artifacts": ["research.md#agent-1-sdk-runtime-explorer"],
  "blockers": [],
  "started_at": "2026-08-06T14:27:00-03:00",
  "finished_at": "2026-08-06T14:31:57-03:00"
}
```

## Agent 2 — Ontology and projection explorer

# EXPLORER RETURN — Agent 2: Ontology and Projection Contract

## Verdict

The smallest owner-preserving seam is a **hybrid, host-mediated consultation contract**:

1. The add-on manifest may request a neutral capability and declare compatibility requirements.
2. The host remains authoritative for actual availability, installed bundle identity, permitted views/operations, effective limits, freshness, answer-policy state, and grants.
3. The add-on invokes only the existing read-only consultation service.
4. Static bundle descriptors may support inspection or offline tooling, but must not become the runtime access or installation authority.
5. Projection approval and installation require separate explicit owners.

A manifest-only/static-bundle design is insufficient because it cannot truthfully establish current installation, grant, freshness, or answer-policy state. A generic tool/connector-only design is too weak unless its discovery result carries the typed consultation contract and non-authority semantics. The hybrid preserves useful discovery without creating another ontology API or copying private vocabulary into a public SDK.

Current validation is **blocked for an acceptance-ready bundle claim**: the focused suite produced 29 passes and one failure because `generated/consumer/projection.json` is stale relative to the current compiler inputs. Leakage validation independently passed with zero hits. This does not invalidate the contract analysis, but any current bundle digest or installation witness must be refreshed by its owner before use.

## Exact current-state map

| Claim | Exact source identity and selector | Scope | Proof |
|---|---|---|---|
| The private ontology is candidate-local, authority-effect none, release not granted. | `README.md`, SHA-256 `de4776…b947`, lines 3–7, 11–18; `profile.json`, SHA-256 `3665e6…3485`, JSON selectors `/status`, `/authority_effect`, `/release_admission`, `/claim_ceiling` | Private package status | observed |
| Product/runtime ownership remains in ResonantOS; meaning, projection, production-route, and canonical-writer owners are unresolved. | `README.md` lines 20–33 | Ownership boundary | observed |
| The current neutral projection compiler reads reviewed nodes, explanations, glossary, and a validation receipt; it allowlists consumer fields and emits opaque record/source/owner identifiers. | `build-consumer-projection.mjs`, SHA-256 `989b66…5adf`, lines 11–29, 45–47, 53–72, 86–133 | Compiler mechanics | observed |
| The consumer projection carries records, structured conflicts, bounded explanation support, source handles, confidence, and no private source paths. | `consumer-projection.schema.json`, SHA-256 `7bc53c…a0eb`, selectors `/required`, `/properties/records/items`; compiler lines 92–138 | Public-neutral data shape | observed |
| The bundle manifest binds compiler, allowlist, input-source handles/digests, schema versions/digests, record counts, generation time, projection/glossary/bundle digests, and an approval-shaped reference. | `consumer-bundle-manifest.schema.json`, SHA-256 `927077…8c6`, lines 3–21 | Static descriptor | observed |
| The stored manifest identifies projection `ff1a…afdc`, bundle `118c…3f1c`, 22 records, 14 terms, generated `2026-08-03T16:44:36Z`. | `generated/consumer/projection-manifest.json`, SHA-256 `8f02a7…138d`, selectors `/outputDigest`, `/bundleDigest`, `/recordCounts`, `/generatedAt` | Stored generated bytes only | observed |
| The stored `ownerApprovalRef` is not proof of a real owner decision: the compiler deterministically hashes the literal `APPROVE_EXACT_EPOCH:augmentor-consultation-l1-l2`. | Compiler lines 148–167, especially line 166 | Approval semantics | observed mechanics; inferred insufficiency |
| Contract families are closed and explicitly incompatible across versions unless a consumer recognizes the exact family. Unknown versions reject. | `contract-families.json`, SHA-256 `945242…8674`, lines 2–35 | Version policy | observed |
| Query operations are only `lookup`, `search`, and `context`; view scope, optional freshness ceiling, and six positive request limits are closed. | `query.schema.json`, SHA-256 `671609…8f48`, lines 3–44 | Fixture-family request shape | observed |
| Results distinguish `ok`, `partial`, `no_match`, `insufficient_evidence`, `conflict`, `stale`, `denied`, `invalid_request`, `budget_exceeded`, and `temporary_failure`. | `result.schema.json`, SHA-256 `dc92cd…d126`, selectors `/$defs/*` and `/oneOf` | Fixture-family result semantics | observed |
| Explanation profiles are `brief`, `guided`, `deep`; they return support, not final prose, and glossary terms fix `authorityEffect` to `none`. | `explanation-support.schema.json`, SHA-256 `be22f6…8904`, lines 6–13, 76–85; `TERMINAL-EVIDENCE.md`, SHA-256 `b532e4…1414`, lines 7–11, 25–26 | Rich candidate semantics | observed |
| Local implementation evidence explicitly does not prove deployment, promotion, release, production, or an integrated reasoning engine. | `TERMINAL-EVIDENCE.md` lines 3–11, 46–52 | Proof ceiling | observed |
| Publication remains plan-only; that Invoke package performed no product or production mutation. | publication `README.md`, SHA-256 `c62baa…39d`, lines 3–16 | Publication status | observed |

## Proposed public-neutral types

```ts
type OntologyConsultationRequirement = {
  contractFamily: "augmentor.consultation";
  supportedQueryVersions: readonly string[];
  supportedResultVersions: readonly string[];
  requiredOperations?: readonly ("lookup" | "search" | "context")[];
  requiredViews?: readonly string[];
  explanationProfiles?: readonly ("brief" | "guided" | "deep")[];
  maxProjectionAgeSeconds?: number;
};

type OntologyConsultationDiscovery = {
  contractFamily: "augmentor.consultation";
  queryVersion: string;
  resultVersion: string;
  operations: readonly ("lookup" | "search" | "context")[];
  views: readonly string[];
  projectionDigest: string;
  bundleDigest: string;
  generatedAt: string;
  freshness: "current" | "stale" | "unknown";
  limits: {
    maxCandidates: number;
    maxRecords: number;
    maxSources: number;
    maxBytes: number;
    maxTokens: number;
    maxMillis: number;
  };
  sourceHandleSemantics: "opaque-reference-only";
  explanationProfiles: readonly ("brief" | "guided" | "deep")[];
  answerPolicy: {
    status: "available" | "degraded" | "unavailable";
    composesFinalAnswer: false;
    followsRetrievedInstructions: false;
  };
  authorityEffect: "none";
};

type OntologyConsultationGrant = {
  capability: "ontology-consultation-read";
  addOnId: string;
  allowedOperations: readonly ("lookup" | "search" | "context")[];
  allowedViews: readonly string[];
  effectiveLimits: OntologyConsultationDiscovery["limits"];
  projectionDigest: string;
  policyDigest: string;
};
```

Public SDK names should remain neutral. It must not expose private node IDs, CAV2 contract references, private owner routes, repository paths, raw source digests mapped to private locations, internal notes, or private authority vocabulary.

## Declaration versus discovery

| Metadata | Add-on may declare | Host must discover/derive |
|---|---:|---:|
| Contract family and acceptable versions | compatibility range/list | selected exact versions |
| Required operations/views | yes, as request | available and granted subset |
| Projection/bundle digest | optional expected pin | actual installed identity |
| Freshness requirement | maximum acceptable age | generation time and current freshness |
| Limits | requested maxima | effective minimum of service, policy, request |
| Source-handle semantics | required semantic expectation | exact opaque-handle implementation |
| Explanation profiles | acceptable profiles | supported profiles and chosen profile |
| Answer-policy requirements | required invariants | current policy availability/status |
| `authorityEffect` | must require `"none"` | host must return/fix `"none"` |
| Approval/install state | no | explicit owner receipts only |

A manifest claim is never a host fact or a grant.

## Option comparison

| Shape | Fit | Rejection boundary |
|---|---|---|
| Static bundle descriptor | Useful for deterministic packaging, hashes, schemas, offline inspection | Cannot establish installed/current/granted/available state |
| Host-mediated read-only service | Strong runtime owner fit; enforces identity, policy, views, limits, freshness | Needs SDK discovery and permission ergonomics |
| Generic tool/connector discovery | Reuses a broad discovery mechanism | Reject if it collapses typed versions, grants, projection identity, or authority semantics |
| Hybrid manifest requirement + host discovery + existing consultation invocation | Best fit | Must not create a second projection store, installer, grant owner, or answer generator |

## Invariants

- Consultation is read-only and has `authorityEffect: "none"`.
- Retrieved records and instruction-shaped strings remain data; they are never executable instructions.
- Evidence is not final truth, approval, routing, a grant, memory access, an ontology write, or permission to act.
- Source handles are opaque references, not source contents, URLs, paths, credentials, or authority.
- Manifest requirements are untrusted requests until validator, review, and grant owners admit them.
- Effective limits are the minimum of service, policy/grant, and request limits.
- View access is the intersection of installed availability and explicit grant.
- Projection and glossary install atomically under one recognized bundle family and digest.
- `brief`, `guided`, and `deep` may change detail, never evidence truth, status, authority, or instruction-following behavior.
- Structured conflicts remain structured; neither SDK nor consultation service silently chooses meaning.
- Denied responses disclose no projection, policy, bundle, or protected principal metadata.
- Approval and installation are different decisions:
  - projection approval owner accepts exact source/compiler/schema/output epoch;
  - installation owner admits exact bundle bytes into a host generation.
- Disable, revoke, upgrade mismatch, or uninstall makes discovery unavailable/degraded and blocks invocation; it does not fall back to raw ontology access.

## Version negotiation

1. The add-on lists exact supported query/result versions, not a permissive unbounded string.
2. The host selects one internally coherent family whose query, result, projection, manifest, glossary, and explanation-support versions match its installed consumer.
3. No implicit `0.1 ↔ 1.0 ↔ 1.1` compatibility.
4. Unknown family/version rejects before reading projection data.
5. If the add-on requires an unavailable operation, view, profile, or freshness bound, activation or invocation fails explicitly.
6. Bundle-digest changes invalidate digest-bound grants/caches until the installation/grant owner rebinds them.
7. Downgrade requires explicit compatibility and owner approval; silent downgrade is rejected.

## Required reject tests

- Unknown contract family or mixed query/result/bundle versions.
- Manifest asserts an installed digest that differs from host state.
- Bundle is missing one of projection, glossary, manifest, or schemas.
- Projection/compiler/allowlist/schema/glossary/bundle digest mismatch.
- Unrecognized or synthetic-only `ownerApprovalRef` presented as approval.
- Install attempted without separate projection-approval and installation receipts.
- Unknown fields or operations such as `write`, `approve`, `route`, `execute`, or memory mutation.
- Requested view outside the installed/granted intersection.
- Stale projection beyond requested maximum age.
- Missing source handle or provenance.
- Private path, `workspace-resonant`, `cyberalchemy`, `authority_effect`, internal-note/private-id, secret, password, or bearer-shaped leakage.
- Private formal vocabulary copied into the public SDK.
- Instruction-shaped text changes control flow or is followed.
- Explanation profile changes truth/status/authority.
- Evidence becomes final answer, grant, approval, routing decision, or effect.
- Conflict is flattened into one asserted meaning.
- Cache key omits add-on/principal, policy digest, bundle digest, view scope, or explanation selector.
- Revoked/disabled/uninstalled capability still resolves or silently falls back to static/raw bytes.

## Executed validation

Command: focused nine-file Node test suite, then leakage validation.

Observed:

- 30 tests: 29 passed, 1 failed.
- Failure: `consumer-projection.test.mjs` reported `projection.json is stale; rebuild the neutral consumer projection.`
- Independent leakage validator: `status: pass`, `hits: []`.

The current validation receipt was regenerated on `2026-08-06T13:24:19-03:00`, while the stored consumer manifest says `generatedAt: 2026-08-03T16:44:36.000Z`. Because compiler output binds the receipt-derived reviewed date, this is consistent with the observed stale-output failure. That causal explanation is inferred from compiler lines 65–68 and 101–107; it was not repaired or regenerated in this read-only run.

## Non-goals

No raw ontology distribution, second ontology store, ontology editing, memory access, reasoning engine, answer generation, routing, approval, protected effects, projection promotion, installation, deployment, release, or production-readiness claim.

## Blocker

Before an executable SDK acceptance witness can bind the current projection/bundle digest, the projection owner must regenerate and validate the neutral consumer bundle from the current reviewed inputs, and the separate approval/install owners must provide real exact-byte receipts. The deterministic `ownerApprovalRef` string is insufficient.

## RECEIPT PAYLOAD

```json
{
  "status": "pass",
  "validation": "block",
  "artifacts": [
    "research.md#agent-2-ontology-projection-explorer"
  ],
  "blockers": [
    "Current generated consumer projection is stale relative to current compiler inputs; focused suite passed 29/30 and failed consumer-projection freshness.",
    "No independently evidenced projection-approval receipt or installation-owner receipt was observed; the generated ownerApprovalRef is deterministic metadata, not sufficient proof of approval or installation."
  ],
  "started_at": "2026-08-06T14:25:00-03:00",
  "finished_at": "2026-08-06T14:32:26-03:00"
}
```

## Agent 3 — Security and lifecycle explorer

# EXPLORER RETURN — Agent 3 Security/Lifecycle Explorer

## Verdict

A public `augmentor-consultation-read` SDK capability is safe only as a narrow request for a host-mediated, read-only service. It must not authorize projection installation, select paths, assert availability, grant itself, or carry credentials.

The current host consultation boundary is strong and executable, but the Add-on SDK is not connected to it. There is no current manifest-to-installation-grant-to-bridge witness, and disable/uninstall integration is absent. The correct target is therefore an additive SDK capability plus host-derived discovery/status—not a manifest-owned ontology contract and not the shared deployment adapter.

## Evidence-bound current state

| Claim | Source identity and exact selector | Scope | Proof |
|---|---|---|---|
| The host route is exactly `POST /augmentor/consultation`, protected by `augmentor-consultation-read`; local bridge calls receive a host-generated context, while external keys receive grant-derived views and limits. | `../workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-host-service.mjs:8-55` | Current host-service behavior | observed |
| Non-loopback consultation-key access requires both TLS and an active IP allowlist. The key is accepted only through this route’s authenticator. | Same source, lines 20-25; `bridge-server.mjs:1066-1098,1187-1191` | Current bridge authentication and dispatch | observed |
| Local bridge authorization requires both the bridge token and the route-specific capability token. External authorization requires the route authenticator to return that capability. Consultation credentials are removed before the handler is invoked. | `bridge-server.mjs:1006-1012,1066-1098` | Current bridge route gate and token hygiene | observed |
| The external access registry has a closed versioned shape, validates client IDs/views/limits, stores only SHA-256 key hashes in a mode-0600 file, supports expiry and revocation, and derives an opaque principal plus policy digest containing registry revision, views, limits, status, and expiry. | `augmentor-consultation-access.mjs:12-55,58-74,77-112,115-159` | Current grant lifecycle | observed |
| Query identity, policy, path, credentials, or operations cannot be injected as undeclared top-level fields because the query is closed; supported operations, views, freshness, and limits are bounded. | `augmentor-consultation-contract.mjs:139-167` | Current request contract | observed |
| Projection/glossary structures are closed and leakage-scanned; the manifest binds the approved allowlist, exact contract versions, schema digests, projection/glossary/bundle digests, opaque sources, timestamps, counts, and an opaque owner-approval reference. Mixed versions or digest disagreement fail loading. | `augmentor-consultation-contract.mjs:285-365,382-415` | Installed neutral bundle validation | observed |
| Cache isolation includes opaque principal, policy digest plus registry revision, allowed views, bundle digest, result-contract version, operation/query/explanation/scope, and effective limits. Values are cloned. | `augmentor-consultation-cache.mjs:7-59`; `augmentor-consultation-service.mjs:276-288` | Current in-memory cache | observed |
| Requested views must be a subset of host-derived allowed views; effective limits take the minimum of service, grant, and query limits. Freshness is checked before cache lookup. | `augmentor-consultation-service.mjs:258-284`; `augmentor-consultation-contract.mjs:368-375` | Overbroad views, limits, stale evidence | observed |
| Results remain evidence: all policy statuses are total, retrieved instructions are never followed, and authority effect is always `none`. | `augmentor-consultation-answer-policy.mjs:1-24` | Answer-policy semantics | observed |
| Instruction-shaped projection text remains returned data, while mixed contract versions fail closed as `temporary_failure`; malformed dependencies do not disclose temporary paths. | `browser-first/test/augmentor-consultation.test.mjs:150-179,210-238` | Adversarial data and malformed bundle behavior | executed |
| Per-principal/per-policy cache isolation, disallowed-view denial, hashed-key storage, revocation, route scoping, insecure-remote denial, local capability denial, and real loopback HTTP success are covered. | `browser-first/test/augmentor-consultation.test.mjs:75-115,241-348` | Focused host/bridge witness | executed |
| The public SDK capability union lacks `augmentor-consultation-read`; its manifest has `augmentorSkills` and `memoryAccess` but no ontology-consultation field. | `src/core/contracts.ts:4-20`; `src/sdk/addons/contracts.ts:24-43,62-76` | Current SDK type surface | observed |
| SDK validation accepts only the closed `ADDON_CAPABILITIES` list and checks request uniqueness and shape. A capability declaration is not a runtime grant. | `src/sdk/addons/validation.ts:323-347`; `docs/architecture/MODULE-OWNERSHIP.md:43-47` | Current SDK validation/authority | observed |
| Registry entries copy manifest-requested capabilities and retain installation/review/verification state, but this does not currently bridge consultation grants. | `src/sdk/addons/registry.ts:90-123` | Current registry projection | observed |
| The consultation modules own projection validation, grants, answer policy, cache, deadlines, and metrics, and explicitly do not own raw ontology, generated answers, memory writes, approval, routing, or authority. | `docs/architecture/MODULE-OWNERSHIP.md:20-35` | Current ownership boundary | observed |
| The deployment adapter trusts a fixed reverse-proxy principal header and uses one shared principal, all views, default limits, and a fixed policy digest. It owns neither public authentication nor TLS. | `run-augmentor-consultation-deployment.mjs:13-22,47-97`; `MODULE-OWNERSHIP.md:28-29` | Private deployment adapter only | observed |

## Executed validation

Executed from `../workspace-resonant/2.0.0-alpha`:

```text
node --test browser-first/test/augmentor-consultation.test.mjs \
  browser-first/test/augmentor-consultation-deployment.test.mjs
```

Result: 11/11 passed, including a real loopback HTTP bridge witness.

```text
npx vitest run src/sdk/addons/validation.test.ts \
  src/sdk/addons/registry.test.ts
```

Result: 25/25 passed.

These executions prove current host and SDK behavior separately. They do not prove the proposed SDK integration.

## Trust decision

Manifest metadata may be trusted only as unprivileged requested intent after SDK validation:

- requested capability: `augmentor-consultation-read`;
- required consultation contract major/version range;
- optional required operation names;
- optional requested view IDs;
- declared degradation behavior;
- non-secret UI/help text.

It must be treated as a request, never a grant or runtime fact.

The host must derive and return:

- whether consultation is installed and available;
- the actually installed contract family/version;
- projection and bundle digest;
- freshness/generated time;
- owner-approval reference validity;
- supported operations and views;
- granted view subset and effective limits;
- grant status, expiry, registry revision, and policy digest;
- answer-policy result;
- degraded/denied reason.

The manifest must never contain or control:

- projection paths or raw/private source locations;
- access keys, bridge tokens, capability tokens, or trusted proxy principals;
- bundle digests asserted as installed truth;
- owner approval or projection-installation authority;
- cache keys or principal identity;
- memory-write, ontology-write, routing, approval, promotion, or effect semantics.

## Safe target contract and lifecycle

Add `augmentor-consultation-read` to the SDK capability union with scope no broader than `self` and `revocationBehavior: "hard-stop"` for API invocation. A UI that depends on it may degrade or hide its consultation affordance, but cached evidence must not remain usable as current consultation after revocation.

Keep fine-grained view/limit policy host-owned. Installation/review should translate the reviewed SDK request into a distinct host consultation grant associated with the installation identity. Do not reuse `augmentorSkills`, `memoryAccess`, generic network permission, or a connector credential.

Lifecycle requirements:

1. Validation rejects unknown contract versions, duplicate declarations, undeclared capability dependencies, credentials, paths, installation claims, and fields outside the closed contract.
2. Review shows capability, requested views, limits ceiling, read-only/non-authority claim, and degradation behavior.
3. Grant creates or updates a host record; no manifest `granted: true` value is authoritative.
4. Runtime discovery returns host-derived status and installed contract metadata.
5. Invocation still passes the existing bridge capability gate and consultation service’s view, limit, freshness, bundle, and answer-policy gates.
6. Revocation first disables invocation, increments host policy state, and removes runtime tokens. Existing cache entries become unreachable because authentication fails and policy/revision changes alter keys.
7. Disable performs the same runtime revocation while retaining reviewed installation metadata.
8. Upgrade revalidates SDK compatibility and requires review for widened views, limits, or contract major.
9. Downgrade or mixed-version projection returns an explicit unavailable/incompatible state; it must not silently negotiate to a weaker contract.
10. Uninstall revokes/deletes the installation-linked consultation grant, removes runtime tokens, clears that installation’s consultation UI state, and must not delete or rewrite the shared approved projection.
11. Re-enable requires a fresh host grant; stale manifest state cannot resurrect access.

## Adversarial findings

- A compromised add-on cannot safely be allowed to choose projection paths, provide a trusted bundle digest, install a projection, or assert owner approval. Those facts must come from the existing host loader.
- Instruction-shaped ontology records are structurally allowed as evidence text. Safety therefore depends on the answer-policy/context boundary, which currently forces `followRetrievedInstructions: false`. Every consuming agent/tool path must preserve that bit; sanitizing text alone is insufficient.
- Cache cross-talk is currently controlled for per-agent key mode. The shared deployment adapter intentionally collapses callers to `shared-basic-auth`; it is unsuitable as the add-on SDK seam because it has shared identity, fixed all-view access, and no per-add-on revocation.
- The deployment principal header is secure only when the container is loopback/private and the trusted reverse proxy strips and replaces client-supplied copies. Direct or accidentally exposed access would permit header spoofing. This adapter must remain outside SDK discovery.
- Current host errors redact dependency details, but the proposed SDK status endpoint must likewise never return paths, tokens, hashes, private vocabulary, or raw loader errors.
- A manifest version range must never trigger automatic downgrade. The host either proves a compatible installed version or returns `incompatible`.
- Evidence may support prose only under `answerPolicy`; it must never be converted into tool instructions, permission, grant, routing, memory writes, ontology writes, approval, promotion, or effects.

## Deterministic target tests required

Positive witness:

1. Validate a concrete add-on manifest requesting `augmentor-consultation-read`.
2. Review and explicitly grant only `experience`.
3. Host discovery reports installed compatible version and host-derived digest/freshness.
4. Obtain a scoped runtime token through the existing bridge owner.
5. Call the real loopback bridge.
6. Observe bounded source-backed evidence plus `authorityEffect: none`.
7. Disable/revoke.
8. Repeat the same request and observe denial plus honest degraded UI/status.

Negative fixtures must cover:

- absent declaration;
- declared but ungranted capability;
- manifest `granted: true` ignored or rejected;
- overbroad/disallowed view;
- widened limits constrained by the host;
- credential, token, or filesystem path in manifest fields;
- stale projection;
- malformed and leakage-bearing bundle;
- mixed contract/schema version;
- unsupported major and downgrade attempt;
- instruction-shaped evidence with no tool execution;
- cache isolation across two installations, two policies, two grants, and two bundle digests;
- revoked, disabled, expired, upgraded, rolled-back, and uninstalled add-ons;
- direct memory write, ontology write, route/approval/effect inference;
- deployment-adapter principal spoofing when bypassing its trusted proxy;
- browser or bridge UI witness showing unavailable/degraded state without exposing private details.

## Proof gaps

The following are absent, not failures of the already-implemented host:

- SDK capability/type for consultation;
- consultation-specific manifest validation;
- installation review-to-host-grant adapter;
- host-derived SDK discovery/status contract;
- installation-linked revocation, disable, upgrade, rollback, and uninstall behavior;
- runtime token acquisition tied to the add-on installation grant;
- deterministic manifest-to-grant-to-bridge-to-revoke witness;
- browser witness for degraded/disabled/uninstalled behavior;
- explicit trusted-proxy header-stripping test for the deployment adapter.

The design can proceed, but implementation or release claims would be inflated until these gaps are built and executed.

## RECEIPT PAYLOAD

```json
{
  "status": "pass",
  "validation": "pass",
  "artifacts": ["research.md#agent-3-security-lifecycle-explorer"],
  "blockers": [],
  "started_at": "2026-08-06T14:27:00-03:00",
  "finished_at": "2026-08-06T14:32:29-03:00"
}
```

### Agent 2 receipt clarification

The explorer action passed; the acceptance-ready bundle claim remains blocked and must enter synthesis as residue.

```json
{
  "status": "pass",
  "validation": "pass",
  "artifacts": [
    "research.md#agent-2-ontology-projection-explorer"
  ],
  "blockers": [],
  "residue": [
    "The current generated consumer projection is stale relative to current compiler inputs; the focused suite passed 29/30 tests and failed projection freshness.",
    "No independently evidenced projection-approval receipt or installation-owner receipt was observed; the deterministic ownerApprovalRef is metadata, not sufficient proof of approval or installation."
  ],
  "started_at": "2026-08-06T14:25:00-03:00",
  "finished_at": "2026-08-06T14:34:00-03:00"
}
```
