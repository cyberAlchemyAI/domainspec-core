# SYNTHESIS RETURN

## Decision

Select a **hybrid additive SDK contract**:

1. Add the already-implemented capability spelling **`augmentor-consultation-read`** to the public SDK capability vocabulary.
2. Add an optional, closed `ontologyConsultation` manifest declaration containing only compatibility requirements and requested views/operations.
3. Have the host derive installed bundle identity, availability, exact versions, effective grant, views, limits, freshness, policy state, and revocation state.
4. Reuse the existing neutral-projection compiler/bundle and `POST /augmentor/consultation`.
5. Keep projection approval and installation as independent owner decisions.

This is a future SDK design, not current implementation. The current host and SDK surfaces work separately; the adapter between them is absent.

### Evidence notation

- **E1** — `research.md#agent-1-sdk-runtime-explorer`, receipt `receipts/explorer-sdk-runtime.json`.
- **E2** — `research.md#agent-2-ontology-projection-explorer`, receipt `receipts/explorer-ontology-projection.json`; blocking residue is independently recorded at `orchestration/run-2026-08-06-augmentor-addon-sdk-ontology-api-01/residue/explorer-ontology-projection.json#/items`.
- **E3** — `research.md#agent-3-security-lifecycle-explorer`, receipt `receipts/explorer-security-lifecycle.json`.

All file selectors below are direct selectors recorded by those explorer returns.

## Current-state owner and contract map

| Concern | Current owner and exact selector | Status |
|---|---|---|
| SDK capability vocabulary | `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:4-20`; SDK closed list at `src/sdk/addons/contracts.ts:24-43` | **Observed-current:** lacks `augmentor-consultation-read`. [E1 current-state map; E3 evidence map] |
| Add-on manifest | `src/core/contracts.ts:531-602`; `src/sdk/addons/contracts.ts:62-76` | **Observed-current:** has `augmentorSkills` and `memoryAccess`, but no consultation declaration. [E1; E3] |
| Manifest validation | `src/sdk/addons/validation.ts:323-347` | **Observed-current:** closed capability validation rejects the host-only spelling. [E1; E3] |
| Installation registry | `src/sdk/addons/registry.ts:90-123` | **Observed-current:** retains manifest requests and installation/review state, but has no consultation-grant bridge. [E1; E3] |
| Host route | `browser-first/host/augmentor-consultation-host-service.mjs:8-55` | **Observed-current:** `POST /augmentor/consultation`, guarded by `augmentor-consultation-read`; local context and external grant scope are host-derived. [E1; E3] |
| Bridge capability | `browser-first/host/bridge-capability-tokens.mjs:23-53`; side-panel mapping `src/lib/bridge-client.js:24-50` | **Observed-current:** canonical current spelling is `augmentor-consultation-read`. [E1] |
| Route authentication | `bridge-server.mjs:1006-1012,1066-1098,1187-1191` | **Observed-current:** route-specific local tokens; TLS and IP allowlist for non-loopback external-key access; credentials stripped before handler. [E3] |
| External grant registry | `augmentor-consultation-access.mjs:12-55,58-74,77-159` | **Observed-current:** hashed keys, views, limits, expiry, revocation, opaque principal, policy digest, registry revision. [E1; E3] |
| Neutral projection compiler | `projects/augmentor/ontology/unified-agent/development/consultation-api/build-consumer-projection.mjs:11-29,45-47,53-72,86-167` | **Observed-current:** compiles allowlisted neutral records and opaque handles; its deterministic approval-shaped reference is not independent approval proof. [E2] |
| Bundle validation | `augmentor-consultation-contract.mjs:285-365,382-415`; private schema `consumer-bundle-manifest.schema.json:3-21` | **Observed-current:** closed schema/version/digest validation; mixed versions fail. [E2; E3] |
| Query contract | `augmentor-consultation-contract.mjs:139-167`; private `query.schema.json:3-44` | **Observed-current:** closed `lookup`, `search`, `context`, views, freshness, and bounded limits. [E2; E3] |
| Service behavior | `augmentor-consultation-service.mjs:252-357` | **Observed-current:** audience, grant, freshness, budgets, provenance, conflicts, cache separation, cancellation, deadlines. [E1] |
| Cache | `augmentor-consultation-cache.mjs:7-59`; service `:276-288` | **Observed-current:** keys include principal, policy/revision, views, bundle, result version, operation/query/profile/scope, and effective limits. [E3] |
| Answer policy | `augmentor-consultation-answer-policy.mjs:1-24` | **Observed-current:** total answer/qualify/clarify/abstain mapping; evidence stays data, retrieved instructions are not followed, `authorityEffect` is `none`. [E1; E3] |
| Ownership boundary | `docs/architecture/MODULE-OWNERSHIP.md:20-35,43-47` | **Observed-current:** host modules own consultation mechanics; not raw ontology, generated answers, memory writes, approval, routing, or authority. SDK owns declaration/validation. [E1; E3] |
| Projection installation | `docs/reference/AUGMENTOR_CONSULTATION_API.md:22-34` | **Observed-current contract:** explicit owner-approved installation into user state; bridge does not read private ontology checkout. Independent current approval/install receipts were not found. [E1; E2] |
| SDK-to-host adapter | Selected source set | **Absent:** no manifest field, validation, review-to-grant adapter, discovery/status API, installation-bound token acquisition, or lifecycle integration. [E1 integration gap; E3 proof gaps] |

## Reconciled disagreements

- E2 proposed `ontology-consultation-read`; that spelling is rejected. The actual existing capability is **`augmentor-consultation-read`**, proven by the host service and bridge registry. A neutral public manifest object does not justify renaming the owned runtime capability. [E1 `bridge-capability-tokens.mjs:23-53`; E3 host service `:8-55`]
- E2 allowed a manifest to optionally pin a projection/bundle digest. E1 and E3 provide the safer boundary: installed identity is host-derived. The manifest may express compatibility, but it must not assert an installed digest as runtime truth. Exact digest pinning, if later needed, requires a separate owner decision.
- E1 allowed `unavailableBehavior: "degrade" | "hard-stop"`; E3 requires API invocation to hard-stop after loss of grant while UI may degrade or hide. Reconciliation: the declaration describes **UI/product behavior**, while invocation always fails closed.
- E1 reported 17/17 host/bridge and 31/31 SDK-focused tests; E3 independently reported 11/11 host/deployment and 25/25 SDK-focused tests. These are different selected suites, not a conflict. Both prove separate current surfaces, never the designed adapter.
- E2’s 29/30 projection suite with a freshness failure governs any acceptance-ready bundle claim. It does not negate passing host tests against their fixture; it blocks binding a current bundle digest into a new end-to-end acceptance witness.

## Exact gaps

1. `augmentor-consultation-read` is absent from the SDK union and closed capability list. [E1 `contracts.ts:4-17`; E3 `contracts.ts:4-20`]
2. `AddOnManifest` has no typed consultation compatibility/request object. [E1 `contracts.ts:531-602`]
3. No consultation-specific closed validation or cross-field requirement exists. [E1/E3 `validation.ts:323-347`]
4. Registry state does not distinguish declaration from host-derived availability/grant. [E1/E3 `registry.ts:90-123`]
5. No add-on installation/review identity maps to the existing host grant registry.
6. No safe host discovery/status projection exists for add-ons.
7. No installation-bound route-token acquisition connects the grant to the bridge.
8. Disable, re-enable, upgrade, rollback, and uninstall do not drive consultation revocation/status.
9. No SDK/UI degraded-status integration exists.
10. No manifest-to-grant-to-bridge-to-evidence-to-revocation test exists.
11. **Blocking residue:** the generated projection is stale relative to current compiler inputs; the focused projection suite passed 29/30. [E2 executed validation; residue JSON `/items/0`]
12. **Blocking residue:** no independent exact-byte projection-approval or installation-owner receipt was observed; deterministic `ownerApprovalRef` metadata is insufficient. [E2 compiler `:148-167`; residue JSON `/items/1`]

Items 11–12 block an acceptance-ready bundle and executable end-to-end witness. They do not establish a need for a new projection, API, registry, or owner.

## Option matrix

| Option | Owner fit | Result |
|---|---|---|
| No SDK change; add-ons call host privately | Bypasses SDK declaration, review, registry, and lifecycle owners | Rejected as a target; preserves current separation but cannot provide supported add-on access. |
| Reuse `augmentorSkills` | Skills are operating guidance, not data access or grant | Rejected: definitional collapse into instructions. [E1 semantic distinctions; E3 trust decision] |
| Generic `tools` or `connectors` declaration | Could describe a callable surface, but creates ambiguous transport/credential semantics and loses typed versions, views, answer policy, and grant lifecycle | Rejected as the primary seam. A generic UI renderer may consume the typed declaration later, but cannot own it. |
| Add only `ontologyConsultation` | Represents compatibility but cannot request the closed capability | Rejected alone: manifest prose without route admission is vacuous. |
| Add only new capability | Requests route access but cannot express contract compatibility, views, operations, or degradation | Rejected alone: insufficient negotiation and UI semantics. |
| **Hybrid: existing capability + additive declaration + host discovery** | Reuses SDK validation/registry, host grant/route/cache/policy, and neutral projection owners | **Selected.** Smallest complete non-collapsing seam. |

No candidate is assigned a research-type terminal `KILL` here; the non-selected shapes are rejected as standalone implementations. The hybrid remains `build-from-owned`, not novel ownership.

## Proposed public TypeScript contract

```ts
export type Capability =
  | /* current values */
  | "augmentor-consultation-read";

export type AugmentorConsultationOperation =
  | "lookup"
  | "search"
  | "context";

export interface AddOnOntologyConsultationDeclaration {
  provider: "host";
  contractFamily: "augmentor.consultation";
  supportedQueryVersions: readonly string[];
  supportedResultVersions: readonly string[];
  requestedOperations: readonly AugmentorConsultationOperation[];
  requestedViews: readonly string[];
  explanationProfiles?: readonly ("brief" | "guided" | "deep")[];
  maxProjectionAgeSeconds?: number;
  requiredCapability: "augmentor-consultation-read";
  unavailableBehavior: "degrade-ui" | "hide-ui";
}

export interface AddOnManifest {
  // existing fields
  ontologyConsultation?: AddOnOntologyConsultationDeclaration;
}

export interface AddOnConsultationAvailability {
  available: boolean;
  granted: boolean;
  reason?:
    | "not-installed"
    | "not-granted"
    | "disabled"
    | "revoked"
    | "expired"
    | "incompatible"
    | "projection-invalid"
    | "projection-stale"
    | "policy-unavailable";
  contractFamily?: "augmentor.consultation";
  queryVersion?: string;
  resultVersion?: string;
  operations?: readonly AugmentorConsultationOperation[];
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
  projectionDigest?: string;
  bundleDigest?: string;
  generatedAt?: string;
  freshness?: "current" | "stale" | "unknown";
  sourceHandleSemantics?: "opaque-reference-only";
  answerPolicy?: {
    status: "available" | "degraded" | "unavailable";
    composesFinalAnswer: false;
    followsRetrievedInstructions: false;
  };
  authorityEffect?: "none";
}
```

`AddOnConsultationAvailability` is host-produced. An add-on cannot submit it as grant, approval, or installation evidence.

## Proposed JSON manifest

```json
{
  "sdkVersion": "0.2.0",
  "requestedCapabilities": [
    {
      "capability": "augmentor-consultation-read",
      "granted": false,
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
    "requiredCapability": "augmentor-consultation-read",
    "unavailableBehavior": "degrade-ui"
  }
}
```

Forbidden manifest fields include paths, credentials, tokens, principals, installed/granted assertions, actual bundle identity, approval/install receipts, effective limits, source handles, cache keys, `authorityEffect` overrides, instructions, ontology/memory writes, routing, approval, promotion, or effects.

## Validation and negotiation

### SDK validation

- The declaration is optional; existing manifests remain valid.
- When present, `requiredCapability` must equal `augmentor-consultation-read`, and that capability must be requested exactly once.
- Provider, family, operations, profiles, behavior, and object keys are closed.
- Version arrays and requested view/operation arrays must be non-empty and unique.
- Versions are exact recognized family identifiers; no unbounded or implicit compatibility.
- Reject unknown operations including `write`, `approve`, `route`, `execute`, and memory mutation.
- Reject secrets, tokens, paths, actual grant/install state, and authority fields.
- A preset may grant only a requested capability, but a preset value is not runtime proof.

### Runtime negotiation

1. Host validates the independently installed neutral bundle.
2. Host intersects exact supported query/result versions with one internally coherent installed family.
3. Host intersects requested operations/views with installed availability and explicit grant.
4. Effective limits are the minimum of service, policy/grant, and query.
5. Freshness must satisfy both host policy and declared maximum age.
6. No intersection returns `incompatible`; no silent downgrade.
7. A bundle-digest or policy revision invalidates digest/policy-bound grants and caches until owners rebind them.
8. SDK version and consultation-family versions remain independent.

Adding a union member and optional object warrants an SDK minor bump, proposed `0.1.0` → `0.2.0`. Existing `0.1.0` manifests remain compatible; use of the new field requires a host/SDK advertising `0.2.x`. Exhaustive TypeScript switches may require source changes. [E1 compatibility effect]

## Lifecycle and owner flow

| Flow | Required behavior | Status |
|---|---|---|
| Host startup | Validate exact installed bundle and expose a redacted availability projection | **Designed** atop current loader. |
| Registry/install add-on | Validate declaration and store request only; do not install projection or grant access | **Designed; absent adapter.** |
| Review UI | Show capability, requested views/operations, read-only/non-authority boundary, freshness, and UI degradation behavior | **Designed; absent.** |
| Projection approval | Separate owner approves exact compiler/input/schema/output epoch | **Blocked:** independent receipt absent. |
| Projection installation | Separate host owner atomically installs validated projection, glossary, manifest, and schemas | **Blocked:** current install receipt absent and generated projection stale. |
| Grant | Human/host grants an installation identity a subset of views/operations and effective limits | **Designed; current external grant machinery exists, installation adapter absent.** |
| Discovery | Host returns installed identity, exact versions, effective grant, freshness, limits, answer-policy status, and non-authority invariants | **Designed; absent.** |
| Query | Host provides route-scoped authentication; add-on submits a closed query to existing route | **Partly executed-current at host; SDK adapter absent.** |
| Answer policy | Return bounded evidence and total host policy; consumer answers only according to policy | **Executed-current at host; SDK consumption absent.** |
| Cache | Partition by installation/principal, policy revision, views, bundle, version, query/profile/scope, and limits; clone values | **Executed-current host behavior; installation identity integration designed.** |
| Audit | Record declaration review, grant/revoke, discovery reason, invocation outcome, bundle/policy versions, without private text, credentials, or paths | **Designed; no explorer proved an SDK audit adapter.** |
| Revoke | Fail new calls first, rotate/remove tokens, advance policy revision, make old cache unreachable, degrade/hide UI | **Executed-current for external grant; installation-linked flow absent.** |
| Disable | Revoke runtime exposure while retaining installation/review metadata; re-enable requires a fresh grant | **Designed; absent.** |
| Upgrade add-on | Revalidate; widened views, capabilities, limits, or contract major require review | **Designed; absent.** |
| Upgrade projection/API | Validate coherent bundle, report new exact versions/digests, require compatibility and rebind affected grant/cache | **Designed atop current validation.** |
| Rollback | Restore only an owner-approved, validated, compatible bundle/add-on pair; never silently weaken contracts | **Designed; absent integrated test.** |
| Uninstall | Revoke/delete installation-linked grant and UI state; retain shared projection and other clients | **Designed; absent.** |
| Remove projection | Host becomes unavailable; no raw/private fallback and no manifest mutation | **Designed atop host ownership.** |

## Public/private packaging boundary

Public SDK may expose only neutral contract names, supported operations, public view identifiers, exact public contract versions, opaque digests, freshness, limits, opaque source-handle semantics, answer-policy status, and fixed `authorityEffect: "none"`.

It must not package private node IDs, raw ontology records, CAV2 references or prose, repository paths, internal owner routes, private notes, credentials, source contents, private source-to-handle mappings, approval authority, or promotion state. The neutral projection is evidence-bearing consumer data, not ontology authority or a public copy of the private ontology. [E2 `README.md:3-33`, compiler `:86-138`; E3 ownership map]

## Threat model and controls

| Threat | Required control |
|---|---|
| Malicious manifest self-grants or asserts installation | Closed validation; host derives all actual state. |
| Add-on chooses a path or bundle | No manifest path/install fields; existing host loader owns bytes. |
| Capability/token/key leakage | Never expose raw credentials; route-scoped token delivery; stored external keys remain hashed. |
| Overbroad views or limits | Grant/installed/request intersection; effective minimum limits. |
| Mixed, stale, malformed, or leakage-bearing bundle | Existing closed version/digest/leakage/freshness checks; unavailable before query. |
| Instruction-shaped evidence | Preserve as data; `followsRetrievedInstructions: false`; no tool dispatch from retrieved text. |
| Evidence treated as authority | Fixed `authorityEffect: none`; answer policy cannot grant, approve, route, write, or act. |
| Cache cross-talk | Include installation/principal, policy/revision, views, bundle, versions, query/profile/scope, limits. |
| Revoked token uses cached answer | Authentication precedes cache; token removed and policy revision changes. |
| Silent downgrade | Exact version intersection or `incompatible`. |
| Shared deployment adapter reused for SDK | Prohibited: its shared principal/all-view policy and trusted-proxy assumptions are unsuitable. [E3 deployment adapter `:13-22,47-97`] |
| Status endpoint leaks internals | Return closed reason vocabulary; redact paths, hashes other than allowed public bundle identity, private vocabulary, and loader errors. |
| Disable/uninstall deletes shared projection | Installation-scoped grant removal only; projection has independent owner. |

## Failure and status vocabulary

Discovery status:

- `available`
- `not-installed`
- `not-granted`
- `disabled`
- `revoked`
- `expired`
- `incompatible`
- `projection-invalid`
- `projection-stale`
- `policy-unavailable`

Consultation result status remains the current closed set:

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

[E2 `result.schema.json` selectors `/$defs/*`, `/oneOf`]

Do not merge discovery unavailability with evidence semantics. In particular, `denied` is not `no_match`, `stale` is not `partial`, and `conflict` must remain structured.

## Dependency-ordered implementation slices

1. **SDK vocabulary:** add `augmentor-consultation-read`; preserve old manifests.
2. **Manifest contract and schema:** add closed optional `ontologyConsultation`; implement cross-field validation and rejects.
3. **Registry projection:** persist declaration metadata only.
4. **Host discovery projection:** expose redacted, host-derived compatibility/availability.
5. **Review and grant adapter:** bind installation identity to existing consultation grant owner; add UI review.
6. **Runtime bridge adapter:** issue only route-scoped runtime authority without revealing raw token material to add-on code.
7. **Lifecycle adapter:** revoke/disable/re-enable/upgrade/rollback/uninstall transitions.
8. **Audit and telemetry:** installation-scoped, redacted lifecycle and invocation events.
9. **Projection prerequisite:** regenerate/validate current neutral bundle and obtain independent approval and installation receipts.
10. **Integrated tests:** run manifest-to-grant-to-bridge witness and all negatives.
11. **Browser acceptance:** prove review, available, degraded, revoked, and uninstall UI states.
12. **Docs/migration:** publish SDK contract, threat boundary, version table, lifecycle, and examples.

Slices 1–8 may be developed with fixtures, but slice 9 must close before an acceptance-ready exact-byte witness.

## Exact test matrix

| ID | Fixture / expected observation | Proof status |
|---|---|---|
| P01 | Existing manifest without consultation validates unchanged | **Designed**; general current validation passed, exact fixture absent. |
| P02 | Manifest above validates and registry stores request only | **Designed; absent.** |
| P03 | Reviewed `experience`-only grant yields discovery `available` with host-derived exact versions/digests | **Designed; blocked** by bundle/receipt residue. |
| P04 | Closed `experience` query reaches real loopback route and returns bounded evidence plus `authorityEffect: none` | Host segment **executed-current**; full SDK chain **absent/blocked**. |
| P05 | `partial` requires qualification; `ok` permits cited composition; instruction text remains data | **Executed-current** at host policy/tests; SDK consumer integration **designed**. |
| P06 | Disable/revoke makes repeat request denied/unavailable and UI degraded/hidden | Revocation **executed-current** externally; SDK/UI flow **absent**. |
| P07 | Uninstall removes only installation grant; shared projection and other client remain | **Designed; absent.** |
| N01 | Consultation field without requested capability rejects | **Designed; absent.** |
| N02 | Unknown capability/version/family/operation or mixed versions rejects | Mixed/unknown contract behavior **executed-current** host; manifest case **designed**. |
| N03 | Manifest `granted: true`, path, token, key, principal, installed digest, or approval claim rejects | **Designed; absent.** |
| N04 | Requested view outside grant returns denied without protected metadata | **Executed-current** host. |
| N05 | Requested limits above policy are constrained to effective minimum | **Observed-current**; exact SDK fixture **designed**. |
| N06 | Stale, malformed, digest-mismatched, incomplete, or leakage-bearing bundle becomes unavailable | Malformed/mixed/leakage checks **executed-current**; current freshness case **executed-current failure/blocker**. |
| N07 | Instruction-shaped evidence does not trigger tools or change policy | Host data/policy behavior **executed-current**; downstream no-tool test **designed**. |
| N08 | Cache isolates two installations, principals, policies, grants, views, bundles, and versions | Principal/policy isolation **executed-current**; installation dimension **designed**. |
| N09 | Revoked, expired, disabled, upgraded-incompatible, rolled-back-invalid, or uninstalled access cannot invoke | Revoked/expired host cases **executed-current**; SDK lifecycle variants **designed**. |
| N10 | Memory write, ontology write, routing, approval, promotion, permission, or effect inference rejects/remains impossible | **Designed** contract negatives; existing ownership boundary **observed-current**. |
| N11 | Deployment-adapter spoof attempt without trusted proxy is denied and adapter is not discoverable by add-ons | **Designed/absent** explicit header-stripping test. |
| N12 | Failure/status payload exposes no private path, token, key, raw source, private vocabulary, or loader details | Current dependency-error redaction **executed-current**; SDK discovery projection **designed**. |

## Local manifest-to-grant-to-bridge-to-evidence witness

| Step | Action and expected observation | Status |
|---|---|---|
| W1 | Load the proposed concrete manifest; SDK validator accepts its closed declaration. | **Designed; absent.** |
| W2 | Registry records requested capability/views but reports no grant or installed bundle fact. | **Designed; absent.** |
| W3 | Review grants only `experience` to the installation identity. | **Designed; adapter absent.** |
| W4 | Independently approved and installed exact neutral bundle validates; host discovery reports compatible `@1.1.0`, current digest/freshness, and effective `experience`. | **Blocked:** stale generated projection and missing approval/install receipts. |
| W5 | Existing bridge owner issues/attaches route-scoped authority without exposing raw token to add-on code. | Host mechanism **executed-current**; installation binding **designed**. |
| W6 | Add-on sends closed `experience` query through real loopback `POST /augmentor/consultation`. | Route **executed-current**; full add-on chain **absent**. |
| W7 | Observe bounded records/source handles and host answer policy with `authorityEffect: none`, `followsRetrievedInstructions: false`. | **Executed-current** at host. |
| W8 | Send `runtime` query; observe `denied` because effective grant is `experience` only. | **Executed-current** host behavior; installation fixture **designed**. |
| W9 | Revoke/disable; repeat W6; observe denial/unavailable and degraded/hidden UI without private detail. | Revocation **executed-current** externally; SDK/UI behavior **designed**. |
| W10 | Verify no raw token/path/private ontology record, memory write, ontology write, instruction execution, approval, routing, or effect occurred. | Partial host boundary **executed-current**; full witness **blocked**. |

The witness is not executable end to end today. Calling it executed would overstate both the SDK integration and the bundle’s proof state.

## Migration and documentation obligations

- Bump SDK minor version and document exhaustive-switch impact.
- Publish the new capability and closed manifest schema.
- Document declaration versus grant versus host-derived availability.
- Document independent SDK, consultation-family, projection, and bundle versioning.
- Document review, grant, revoke, disable, re-enable, upgrade, rollback, uninstall, and shared-projection retention.
- Document `augmentorSkills`, `memoryAccess`, tools/connectors, consultation evidence, answer policy, and authority as distinct concepts.
- Document the public/private packaging allowlist and forbidden fields.
- Document status/result vocabulary and UI behavior.
- Add concrete positive and negative manifest examples.
- Add migration guidance: old manifests need no change; consultation users require `0.2.x`, explicit capability request, declaration, review, and host grant.
- Record the acceptance prerequisite: fresh exact bundle plus independent approval and installation receipts.
- Document that passing validation is not installation, approval, deployment, promotion, release, or production readiness.

## Unresolved owner decisions

1. Which existing SDK/host owner owns the installation-review-to-consultation-grant adapter?
2. Which UI owner presents consultation review and degraded/unavailable status?
3. Which owner defines the redacted discovery endpoint or registry projection?
4. Which owner approves the exact neutral bundle epoch?
5. Which owner installs that exact bundle into host state?
6. Whether grants bind to bundle digest, contract major, policy digest, or a defined combination.
7. Whether add-ons may request named limits or only views/operations; effective limits remain host-owned either way.
8. Whether an expected digest pin is ever permitted as compatibility intent; it cannot be installed-state proof.
9. Which audit owner and retention policy cover declaration, grant, invocation, revocation, and uninstall events.
10. Exact rollback retention and re-approval rules.
11. Whether `degrade-ui` and `hide-ui` are sufficient product modes; invocation remains hard-stop regardless.
12. Which consumer owns safe answer composition while preserving `followsRetrievedInstructions: false`.
13. Which trusted-proxy owner supplies and tests header stripping for the deployment adapter; that adapter remains outside the SDK seam.

## Claim ceiling

Current evidence proves that the host consultation route, capability gate, authentication, external grant/revocation, closed contracts, bundle validation mechanics, cache partitioning, answer policy, and focused host tests exist. It also proves that the SDK currently lacks the capability and consultation declaration.

The hybrid contract, discovery projection, grant adapter, UI, installation-linked lifecycle, audit integration, tests, and full witness are **designed**, not implemented. The stale generated projection and absent independent approval/install receipts block any acceptance-ready bundle or executable end-to-end claim. Nothing here proves ontology authority, promotion, deployment, release, production readiness, memory writes, routing, approval, or permission to act.

## RECEIPT PAYLOAD

```json
{
  "status": "pass",
  "validation": "pass_with_blocking_residue",
  "artifacts": ["synthesis.md"],
  "blockers": [
    "Acceptance-ready bundle and executable end-to-end witness are blocked because the current generated consumer projection is stale relative to current compiler inputs; the focused suite passed 29/30 and failed projection freshness.",
    "Acceptance-ready bundle and executable end-to-end witness are blocked because no independently evidenced exact-byte projection-approval receipt or installation-owner receipt was observed; deterministic ownerApprovalRef metadata is insufficient."
  ],
  "started_at": "2026-08-06T14:34:00-03:00",
  "finished_at": "2026-08-06T14:41:19-03:00"
}
```

### Receipt clarification

```json
{
  "status": "pass",
  "validation": "pass",
  "artifacts": ["synthesis.md"],
  "blockers": [],
  "started_at": "2026-08-06T14:34:00-03:00",
  "finished_at": "2026-08-06T14:43:00-03:00"
}
```

Residue:

- Acceptance-ready bundle and executable end-to-end witness claims remain blocked because the current generated consumer projection is stale relative to current compiler inputs; the focused suite passed 29/30 and failed projection freshness.
- Acceptance-ready bundle and executable end-to-end witness claims remain blocked because no independently evidenced exact-byte projection-approval receipt or installation-owner receipt was observed; deterministic `ownerApprovalRef` metadata is insufficient.

The synthesis action passed; this receipt correction does not change or soften its claim ceiling.
