# Definitional and security-boundary review

STATUS: block  
VALIDATION: block  
BLOCKERS: [B1-browser-secret-policy-contradicts-current-alpha-boundary, B2-manifest-candidate-is-not-a-valid-exact-manifest, B3-receipt-observability-evidence-promotion-release-collapse, B4-disable-uninstall-rollback-collapse, B5-resolver-bridge-provider-execution-boundary-underspecified]  
ARTIFACTS: [reviews/boundary.md]  
VERDICT: REVISE

The three-layer ownership conclusion is sound, and the synthesis correctly rejects private DomainSpec/Saturn leakage, nested model CLI, preview execution, Augmentor ownership, automatic artifact/memory intake, Inventory authority, receipt-as-readiness, and workspace installation as product deployment. It is nevertheless not boundary-closed.

## Exact collapse tests

1. Bootstrap ≠ generated package ≠ product add-on: PASS. Bootstrap owns installation/update; generated skills remain repository/runtime packages; the proposed ResonantOS add-on is explicitly absent and separately installed. Selectors: `synthesis.md:5-18,21-31,146-156`; `research.md:40-82,152-165`.

2. Manifest ≠ requested capability ≠ reviewed grant ≠ installation/enabled state: PARTIAL/BLOCK. The prose separates discovery, enablement, and grants, but the “Manifest candidate” is not an exact valid `AddOnSdkManifest`. `provenance` must be an object, `runtimeIsolation` must contain the isolation fields, and required manifest fields are omitted. Requested grants are full `CapabilityGrant` objects, not three-column prose: they require `capability`, `granted`, `scope`, and `revocationBehavior`. Selectors: `synthesis.md:47-77`; `../workspace-resonant/2.0.0-alpha/src/core/contracts.ts:241-246,269-281,531-602,2180-2191`; `src/sdk/addons/contracts.ts:26-43`; `src/sdk/addons/validation.ts:249-261,566-571,1149-1156`.

3. Browser secret boundary: BLOCK. `synthesis.md:148` categorically forbids bridge tokens from browser storage. Current normative Alpha architecture has a narrow, explicit exception: an operator-configured bridge target stores its bridge token and capability-bootstrap token in the local Chrome profile; only scoped route-capability tokens remain runtime-only. The synthesis cannot silently replace that current owner contract. Selector: `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md:40-45,85-99`.

4. Runtime profile ≠ secret-bearing runtime configuration: PASS, subject to B1. The proposed profile is redacted and opaque. Keep bridge/bootstrap-token storage as an explicit exception owned by the existing bridge-target contract; do not expose it through the profile. Selectors: `synthesis.md:79-91`; `ALPHA_RUNTIME_BOUNDARY.md:85-104`.

5. Augmentor classification ≠ proposal preview ≠ edit ≠ decline ≠ exact approval: PASS. Explicit command precedence is retained; preview/edit/decline create no run/action/owner call; editing invalidates the old digest; approval binds exact bytes and runtime/grant facts. Selectors: `synthesis.md:93-117,131-144,175-195`.

6. Exact approval ≠ entitlement ≠ launch validation: PASS. Approval precedes a fresh bridge recheck; mismatch starts zero children. Registration is expressly not entitlement. Selectors: `synthesis.md:73-77,93-109`.

7. Deterministic resolver ≠ model-backed execution ≠ bridge invocation: PARTIAL/BLOCK. `tools/arcanum` is correctly marked deterministic/internal and nested model CLI is killed, but “one retained-owner operation” does not specify the enforceable split:
   - deterministic resolution/validation produces no provider call;
   - authenticated bridge invocation is transport/authorization, not execution proof;
   - provider/delegation owner performs any model execution;
   - returned owner state is not inferred from HTTP success.
   Selectors: `synthesis.md:34-45,69-77,158-173`; `research.md:60-82,335-346`; `ALPHA_RUNTIME_BOUNDARY.md:15-23,51-80`.

8. Child interaction ≠ run state ≠ artifact projection ≠ result consumption ≠ memory admission: PASS. Child-addressed clarification is handle-scoped; reload reconciles owner truth; open, attach, consume, and intake-review are independent; no automatic memory admission occurs. Selectors: `synthesis.md:111-129,131-144,175-195,197-213`.

9. Receipt ≠ observability ≠ evidence ≠ readiness ≠ promotion ≠ release: BLOCK. The synthesis only provides generic “evidence reference,” repository gates, and the sentence that receipts/browser launch are not readiness. It never defines:
   - receipt as an operation/result record;
   - observability as telemetry about behavior;
   - evidence as claim-supporting material;
   - readiness as a gate decision over required evidence;
   - promotion as an owner-approved authority/lifecycle transition;
   - release as product packaging/distribution after promotion.
   “Only afterward consider promotion/release” collapses two different authorities. Selectors: `synthesis.md:119,197-213`; `arcanum/definitions/DEFINITIONS.md:99-113,234-265,291-322,399-435`.

10. Disable ≠ uninstall ≠ rollback ≠ release: BLOCK. Disable/revoke and rollback are described, but uninstall has no contract. Define uninstall separately: disable first, revoke grants/tokens, remove add-on-owned installed bytes/config according to product ownership, preserve or explicitly retain redacted owner history, never invoke Bootstrap removal implicitly, and never claim active external work was cancelled. Release must remain downstream of independent acceptance/promotion gates. Selectors: `synthesis.md:146-156,215-230`; `src/core/contracts.ts:79,2180-2191`.

11. Inventory ≠ authority: PASS. Inventory is used as discovery only, and every load-bearing claim is expected to bind current source. Selector: `research.md:438-448`.

12. Private/public boundary: PASS. Public product bytes prohibit DomainSpec, Saturn, `cyberAlchemy-v2`, private ledgers/prose/identities; public-neutral Arcanum identifiers and provenance are allowed. Selectors: `synthesis.md:146-149,219-230`; `research.md:152-165,335-346`.

## Required corrections

- Replace the YAML fragment with either a complete validator-shaped manifest fixture or label it explicitly “partial non-valid sketch.” Use `provenance: {tier, verificationState, signed}` and `runtimeIsolation: {boundary, supportsDegradedMode, requiresReviewedGrant}`; include all required manifest fields.
- Render every requested capability as an exact `CapabilityGrant`, initially `granted: false`; keep the installation’s reviewed `grantedCapabilities` separate.
- Amend the secret rule to preserve the normative bridge-target exception while forbidding scoped route tokens, provider credentials, and other secrets from browser persistence.
- Add an explicit resolver → authenticated bridge → capability gate → retained execution owner → owner-state projection contract.
- Add distinct definitions and owner/gate rows for receipt, observability, evidence, readiness, promotion, and release.
- Add uninstall semantics and tests independently from disable, rollback, Bootstrap update/removal, and release.

## Evidence-closure obligations

- Validate the completed sideload manifest through `src/sdk/addons/validation.ts` with source `sideload`.
- Test catalog discovery with `installed=false`, `enabled=false`, no granted capabilities; then separately test install, reviewed grant, enable, revoke, disable, uninstall, rollback, promotion, and release transitions.
- Test the bridge-target storage exception and prove scoped route-capability tokens are never persisted.
- Prove deterministic resolution causes zero provider/model calls; bridge authentication alone yields no execution or success claim.
- Emit separate fixtures for receipt, observability record, evidence bundle, readiness decision, promotion decision, and release artifact.
- Preserve the current claim ceiling: specification-only, stale branch, absent Subagent Strategy owner, absent ResonantOS adapters, and no browser witness.
