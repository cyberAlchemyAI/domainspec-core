# Review Returns

## Precedent review

# PRECEDENT REVIEW RETURN

## Overall verdict: PASS

The selected hybrid is `build-from-owned`. It does not require a second ontology API, projection store, installation registry, grant registry, cache, query service, memory path, skill owner, or authority owner.

The proposed `ontologyConsultation` field is a legitimately new SDK declaration because no current manifest field owns its behavior: it declares consultation compatibility and requested views/operations. It is not a renamed `augmentorSkills`, `memoryAccess`, tool, or connector. Those existing fields have materially different semantics.

The synthesis needs four minimal ownership repairs before implementation planning. These do not invalidate the hybrid decision.

## Claim verdicts

| Claim ID | Proposed concern | Existing owner and selector | Verdict | Minimal repair |
|---|---|---|---|---|
| PR-001 | Public capability `augmentor-consultation-read` | Runtime spelling and route admission: `../workspace-resonant/2.0.0-alpha/browser-first/host/bridge-capability-tokens.mjs:23-53`; route: `browser-first/host/augmentor-consultation-host-service.mjs:8-55`; SDK vocabulary mirror: `src/core/contracts.ts:4-20`, `src/sdk/addons/contracts.ts:24-43` | `build-from-owned` | Describe this as exposing the already-owned runtime capability in the SDK vocabulary, not inventing a new capability. Keep one canonical spelling and add a parity test between host and SDK lists. |
| PR-002 | `ontologyConsultation` manifest declaration | Manifest type owner: `src/core/contracts.ts:531-602`; SDK declaration/validation owner: `src/sdk/addons/contracts.ts:62-76`, `validation.ts:323-347` | `precedent-clean` for the field; legitimate additive declaration | Keep it request/compatibility-only. Do not route it through `augmentorSkills`, `memoryAccess`, tools, or connectors. |
| PR-003 | `requiredCapability` inside `ontologyConsultation` | Capability request already owned by `AddOnManifest.requestedCapabilities`; validation owner at `validation.ts:323-347` | Duplicate assertion with drift risk | Remove the serialized `requiredCapability` field. Make its dependency a validator invariant: presence of `ontologyConsultation` requires exactly one top-level `augmentor-consultation-read` request. |
| PR-004 | Supported query/result version arrays | Contract-family/version truth: `augmentor-consultation-contract.mjs:5-13,285-365,382-415`; private family source: `contract-families.json:2-35` as bound by Agent 2 | Compatibility intent is valid; an independently maintained SDK “recognized versions” registry would duplicate ownership | SDK validates closed syntax/family and carries accepted versions as intent. Host performs exact installed-family intersection. If the SDK must reject specific versions offline, generate/import that public list from the contract-family owner rather than maintaining a second registry. |
| PR-005 | Projection and bundle descriptors | Compiler/manifest owner: `build-consumer-projection.mjs:11-29,45-47,53-72,86-167`; validation owner: `augmentor-consultation-contract.mjs:285-365,382-415` | `build-from-owned` | Discovery may project redacted validated facts; it must not store, install, approve, or independently calculate them. |
| PR-006 | Projection approval | Private package explicitly leaves meaning/projection ownership unresolved: `research.md#agent-2-ontology-projection-explorer`, current-state row binding `README.md:20-33`; deterministic metadata at compiler `:148-167` is not approval | Honestly unresolved | Preserve as an explicit prerequisite owner decision. Do not assign it to SDK validation, host validation, or the compiler. |
| PR-007 | Projection installation | Existing installation contract: `docs/reference/AUGMENTOR_CONSULTATION_API.md:22-34`; exact acting owner/receipt was not found | Contract exists; acting owner remains honestly unresolved | Name the installation owner before implementation. Add-on install must never install or delete the shared projection. |
| PR-008 | Query interface and operations | Existing `POST /augmentor/consultation`: host service `:8-55`; closed operations/query: `augmentor-consultation-contract.mjs:139-167`, private `query.schema.json:3-44` | `already-deployed` at host | No second consultation endpoint or generic tool/connector transport. The SDK adapter invokes this route. |
| PR-009 | Query/result version negotiation | Existing contract loader and mixed-version rejection: `augmentor-consultation-contract.mjs:285-365,382-415` | `build-from-owned` | Host remains negotiation authority; SDK version and consultation-family version stay independent. |
| PR-010 | Add-on installation/review registry | `src/sdk/addons/registry.ts:90-123` owns manifest request plus installation/review state | `already-deployed`, with adapter absent | Extend its projection only with declaration metadata. Do not create a consultation installation registry. |
| PR-011 | Consultation grant | External grant registry: `augmentor-consultation-access.mjs:12-55,58-74,77-159` | `already-deployed` for grant mechanics; installation binding absent | Add an installation-identity adapter to this owner. Do not create a second grant registry in SDK state. |
| PR-012 | Capability-token issuance | `bridge-capability-tokens.mjs:23-53`; bootstrap/use at `bridge-client.js:443-488`, `bridge-server.mjs:1006-1012,1019-1040,1066-1098,1110-1128` | `already-deployed` | Installation adapter requests route-scoped authority from this owner; add-on code receives no raw token material. |
| PR-013 | Cache | `augmentor-consultation-cache.mjs:7-59`; service use `augmentor-consultation-service.mjs:276-288` | `already-deployed` | Extend the existing key with installation identity only if principal is not already installation-unique. Do not add an SDK consultation cache or treat UI state as evidence cache. |
| PR-014 | Revocation/expiry | `augmentor-consultation-access.mjs:77-159`; authentication-before-cache and policy/revision separation through host service/cache | `already-deployed` externally; add-on lifecycle binding absent | Disable/uninstall must call the existing grant/token owners. They must not invent SDK-only revocation semantics. |
| PR-015 | Host discovery/status projection | No add-on-facing discovery/status owner was found in the selected corpus; registry stores requests, while host owns runtime truth | Honestly unresolved capability seam | Assign it to the existing consultation host boundary as a redacted read model, or project it through an existing host-owned registry API. State explicitly that it is not a new registry/store and persists no independent runtime truth. |
| PR-016 | UI review and unavailable/degraded projection | Side-panel route mapping exists at `src/lib/bridge-client.js:24-50`, but no selected source establishes ownership of add-on review/status UI | Honestly unresolved | Require a product/UI owner decision. UI consumes host-derived status and SDK review state; it must not calculate grants, freshness, installation, or authority. |
| PR-017 | Audit events | Consultation modules own metrics at `docs/architecture/MODULE-OWNERSHIP.md:20-35`; SDK registry retains review/install state at `registry.ts:90-123`; no selected source proves a unified audit-event or retention owner | Honestly unresolved | Split events by existing transactional owner until an audit owner is named: SDK registry owns declaration/review events; grant registry owns grant/revoke; host owns invocation outcome. A future audit projection may aggregate but must not become an authority registry. |
| PR-018 | Answer policy | `augmentor-consultation-answer-policy.mjs:1-24` | `already-deployed` | Availability may expose a redacted policy status, but must not redefine the policy schema or compose the final answer. |
| PR-019 | Memory and skills | Existing manifest has `augmentorSkills` and `memoryAccess`: `src/core/contracts.ts:531-602`; semantic distinctions bound in `research.md#agent-1-sdk-runtime-explorer` | Reuse rejected because meanings materially differ | Preserve consultation as a separate typed declaration. No memory read/write path and no skill semantics are added. |
| PR-020 | Ontology and authority | Ownership boundary: `docs/architecture/MODULE-OWNERSHIP.md:20-35,43-47`; private package claim ceiling bound in Agent 2 | Existing owners preserved | Keep public output neutral and `authorityEffect: none`; neither manifest, projection, evidence, validation, nor installation becomes ontology authority. |

## Hybrid-contract finding

The hybrid does not invent a duplicate owner if its three pieces are stated precisely:

1. The SDK owns declaration and closed manifest validation.
2. Existing host consultation modules own runtime query, bundle validation, grants, cache, answer policy, and route admission.
3. A new adapter composes SDK installation identity with those owners but owns no registry, projection, capability semantics, or authority state of its own.

Calling that adapter a “consultation registry,” “ontology service,” or independent “version registry” would be a duplicate-owner defect. The synthesis does not currently do that, but its implementation slices should state the negative ownership explicitly.

## Required synthesis repairs

- Remove serialized `requiredCapability`; enforce the dependency in validation.
- Prevent a hand-maintained second consultation-version registry in the SDK.
- Define discovery/status as a non-persistent host-owned projection of existing loader and grant facts.
- Split audit provenance among existing transactional owners until a unified audit/retention owner is explicitly selected.

The stale projection and absent approval/install receipts remain product proof residue. They block acceptance-ready bundle and executable end-to-end claims, but do not block this precedent verdict or invalidate the hybrid design.

## RECEIPT PAYLOAD

```json
{
  "status": "pass",
  "validation": "pass",
  "artifacts": ["reviews.md#precedent-review"],
  "blockers": [],
  "started_at": "2026-08-06T14:45:00-03:00",
  "finished_at": "2026-08-06T14:52:00-03:00"
}
```

## Non-vacuity review

# NON-VACUITY REVIEW RETURN

**Overall: BLOCK**

The hybrid design is conceptually non-vacuous and should **not be killed**: it preserves SDK validation/review owners and reuses the existing host consultation route. However, the proposed witness is not yet finite enough to become an implementation Work Pack.

The central defect is structural: W1–W10 and N01–N12 describe actions and expected behavior, but do not provide the required combination of:

- current or proposed owner;
- exact fixture path/name;
- exact command;
- expected observable assertion;
- proof status.

The concrete manifest is shown, but it is not bound to a fixture locator. No proposed closed-query fixture is provided. The full witness has no executable harness command. Therefore it cannot yet prove that a future implementation goes through SDK validation, review, explicit grant, host-derived discovery, and lifecycle owners rather than bypassing them.

Specific gaps:

- W1–W3 lack fixture paths, commands, and named SDK validation/registry/review owners.
- W4 correctly blocks on stale projection plus missing exact-byte approval and installation receipts.
- W5–W9 distinguish current host behavior from absent installation integration honestly, but lack exact fixtures and commands for the proposed adapter chain.
- W10 is an aggregate claim rather than a finite assertion set.
- N01–N12 name the important negative classes, including all required classes, but combine multiple cases per row and omit owners, fixture locators, commands, and exact observations.
- The instruction-shaped-text case does not identify the consuming harness that proves zero tool execution.
- Cache isolation does not define the two installation identities, policies, grants, bundle digests, or the observations proving no cross-hit.
- Direct write/authority inference is described as impossible but lacks closed payload fixtures and explicit assertions for memory write, ontology write, routing, approval, and effect.
- Honest degraded behavior lacks an exact status/UI fixture and browser or bridge command.

The stale projection and missing approval/install receipts are classified correctly: they block an acceptance-ready exact-byte bundle and executable end-to-end witness, but do not block the research design itself or establish implementation, deployment, promotion, or release. The Inventory result-hook failure is non-authoritative residue and does not change this verdict.

Minimal repair:

1. Revise the witness into one row per step with columns: `ID`, `owner`, `fixture`, `command`, `expected observation`, and `proof status`.
2. Bind the manifest, query, grant, bundle, discovery response, answer-policy response, disable/revoke state, and degraded UI/status to exact proposed fixture paths.
3. Split every negative into an independently runnable fixture, especially malformed versus stale versus mixed-version versus leakage cases.
4. Provide exact target commands for SDK tests, host/bridge tests, integrated witness, and browser/degraded-state validation.
5. Preserve `designed`, `absent`, `executed-current`, and `blocked` labels; do not claim execution before the adapter exists or before projection approval and installation receipts close.

```json
{
  "RECEIPT PAYLOAD": {
    "status": "block",
    "validation": "block",
    "artifacts": ["reviews.md#non-vacuity-review"],
    "blockers": [
      "Witness and negative matrix lack per-step owners, exact fixture locators, commands, and independently assertable expected observations.",
      "Acceptance-ready exact-byte witness remains blocked by the stale generated projection and missing independent projection-approval and installation-owner receipts."
    ],
    "started_at": "2026-08-06T14:43:00-03:00",
    "finished_at": "2026-08-06T14:50:00-03:00"
  }
}
```

## Non-collapse review

# NON-COLLAPSE REVIEW RETURN

**Overall: BLOCK**

The selected hybrid seam is directionally sound and preserves most owner boundaries, but the public examples and lifecycle vocabulary still contain authority and state collapses that must be repaired before evidence closure.

## Claim verdicts

| Claim ID | Verdict | Collapse test | Required repair |
|---|---|---|---|
| NC-01 — Synthesis lines 7–13, 74–81 | PASS | `augmentorSkills`, generic tools/connectors, and consultation access are tested as substitutes. The synthesis rejects each because their behavior differs. | Retain the option matrix and explicitly carry the explorer semantic-distinction table into the writer artifact. |
| NC-02 — Lines 35, 42, 65–68, 223–224 | PASS | Neutral projection, deterministic approval-shaped metadata, projection approval, and installation are independently classified. Validation is not treated as approval or installation. | Retain the exact-byte receipt prerequisite and blocked acceptance claim. |
| NC-03 — Lines 40–41, 145–150, 254–255, 319–320, 346 | PASS with repair | Evidence, explanation support, answer policy, and generated answer are mostly separated: the policy does not compose the final answer and retrieved text is not followed. The synthesis does not give the generated answer a named owner or explicit separate type. | Add a distinct `GeneratedAnswer`/consumer-composition row: it is consumer-owned output constrained by answer policy, not consultation evidence, explanation support, or a host authority decision. |
| NC-04 — Lines 154, 188, 194–201 | **BLOCK** | The prose says an add-on cannot submit grant state and forbids installed/granted assertions, but the public JSON manifest includes `"granted": false`. Even a false value makes grant state manifest-shaped and conflicts with the stated boundary. | Remove `granted` from the request example. If the existing SDK schema structurally requires it, name that as legacy request-shape residue and state that it is non-authoritative—not a reviewed or effective grant. Prefer a request-only type without any grant-state field. |
| NC-05 — Lines 225, 301–302, 342–345 | **BLOCK** | “Review grants,” “route-scoped runtime authority,” and “route-scoped authority” collapse three distinct operations: review/approval, grant issuance, and route authentication. Authentication proves a caller/credential at a route; it is neither a routing decision nor effect authority. | Split the flow into `review decision → grant record → authentication credential/token acquisition → route admission → policy enforcement`. Replace “runtime authority” with “route-scoped authentication credential.” Change W3 to “review approves the request; the grant owner creates an experience-only grant.” |
| NC-06 — Lines 113–150 and 263–293 | **BLOCK** | The status shape conflates independent state dimensions. `available: boolean`, `granted: boolean`, and `reason` can contradict one another. `not-installed` ambiguously means add-on installation or neutral projection installation; `disabled`, `revoked`, and `expired` do not name whether they concern the add-on, grant, service, or projection. | Use a discriminated union or separate dimensions, for example `addonState`, `projectionState`, `grantState`, `compatibilityState`, and derived `invocationState`. Rename reasons precisely: `projection-not-installed`, `addon-disabled`, `grant-not-issued`, `grant-revoked`, `grant-expired`, `contract-incompatible`, etc. |
| NC-07 — Lines 241–243 | PASS with caution | Raw ontology and neutral projection remain distinct; private node IDs, CAV2 references/prose, paths, raw records, private mappings, and promotion state are excluded. | Keep public names neutral. Treat `authorityEffect: "none"` only as an existing public consultation-contract invariant; do not import CAV2 definitions, IDs, prose, or promotion vocabulary to explain it. If that public ownership cannot be shown, rename it to a neutral non-action invariant. |
| NC-08 — Lines 188, 199–201, 243, 254–255, 325, 329, 332 | PASS | Retrieved text remains data; evidence cannot grant permission; manifests cannot establish host facts; writes, routing, approval, promotion, or effects are rejected. | Add explicit fixtures proving retrieved instruction text cannot initiate tool/connector calls and evidence cannot satisfy a grant or approval input. |
| NC-09 — Lines 21, 27–43 | PASS | Load-bearing current-state claims bind to direct explorer selectors rather than Inventory. | Preserve direct selector bindings; Inventory must remain discovery-only and absent from proof language. |
| NC-10 — Lines 310, 316–351, 365–366, 384–388 | PASS | Designed, absent, executed-current, and blocked states remain visibly distinct. The synthesis expressly denies executable end-to-end, deployment, release, promotion, and production claims. | Preserve these claim ceilings unchanged. |
| NC-11 — Lines 205–212, 234–235, 375–380 | PASS with repair | Version negotiation, rollback, approval, and installation remain owner-dependent, but “owner-approved bundle/add-on pair” could be read as one approval covering two independently governed objects. | Name separate approval receipts and owners for the bundle epoch and add-on review; installation remains a third decision. |
| NC-12 — Lines 241–243 and public TypeScript example | PASS with repair | Source handles are opaque and distinct from evidence statements, but the availability shape reports only handle semantics and does not state that possession of a handle confers no fetch permission. | Add `sourceHandleSemantics: "opaque-reference-only"` documentation and a negative test: a handle is neither source content, a resolvable URL/path, credential, grant, nor authority. |

## Required collapse tests

1. A manifest containing `granted`, installed digests, approval references, projection paths, or effective host state must reject or be explicitly classified as legacy non-authoritative request syntax.
2. Review approval alone must not create a grant.
3. A grant alone must not authenticate a route request.
4. Successful route authentication without an active reviewed grant must deny.
5. A routing decision must not imply approval, effect authorization, ontology write, or promotion.
6. `not-installed` must identify the missing object; no generic lifecycle reason may span add-on, projection, grant, and service states.
7. An evidence statement containing imperative text must remain data and cause no skill, tool, connector, memory, ontology, routing, approval, or effect invocation.
8. A source handle must not resolve through SDK-visible paths or convey permission.
9. Explanation profile changes may alter detail only; they must not change evidence status, answer policy, grant, or authority.
10. Validation success must not satisfy projection approval, projection installation, deployment, release, or promotion gates.

The product residue does not invalidate the design review, but correctly blocks acceptance-ready bundle and executable end-to-end claims.

```json
{
  "RECEIPT PAYLOAD": {
    "status": "block",
    "validation": "block",
    "artifacts": ["reviews.md#non-collapse-review"],
    "blockers": [
      "Public manifest example includes granted:false despite the stated prohibition on manifest-supplied grant state.",
      "Review, grant issuance, and route authentication are collapsed by review-grants and route-scoped-authority wording.",
      "Discovery lifecycle vocabulary conflates add-on, projection, grant, compatibility, and invocation state."
    ],
    "started_at": "2026-08-06T14:45:00-03:00",
    "finished_at": "2026-08-06T14:51:00-03:00"
  }
}
```
