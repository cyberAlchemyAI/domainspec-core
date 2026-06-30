# TASK-PROMOTION-BODY

## Objective

Specify the host-side trusted-write provider body contract behind ResonantOS's existing
`promote_review_artifact` seam.

## Layer And Slice

- Layer: L3.
- Slice: S-004.
- Wave: W3.

## Source Contracts

- `development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md`
- `development/resonantos-integration/findings.md`
- `work-pack/shared/context.md`

## Dependencies

- `SWU-RCI-005`.

## Blocker State

Runtime implementation is intentionally deferred. This task specifies the contract, not the full
provider.

## Completion State

Completed in `task-session-20260629T164831Z-standalone-package`.

## Smallest Working Units

### SWU-RCI-006

- Goal: write the host-side provider body contract and example pseudocode.
- Dependencies: `SWU-RCI-005`.
- Source anchors: integration guide "Honest gap" and findings section 5.
- Related context: ResonantOS 501 boundary and `canWriteKnowledgePages:false`.
- Write scope:
  - `standalone-package/docs/host-promotion-provider-body.md`
  - `standalone-package/examples/provider-body/`
- Done criteria:
  - Contract names inputs, outputs, decision rules, failure modes, and validation.
  - It states the contract/tool/seam are ResonantOS-owned and the provider body is the supplied
    implementation point.
  - It preserves approve/reject/escalate vocabulary.
  - It does not claim a working host provider exists.
- Acceptance evidence:
  - Claim-boundary scan.
  - Interface and failure-mode review.
- Validation surface:
  - Markdown review and scoped scan for turnkey/drop-in overclaims.
- Execution owner: local-fallback.
- Handoff note: later implementation must happen in the host runtime, not in the portable MCP layer.

## Synchronization Rules

Do not mark this task complete unless the contract explicitly rejects direct trusted writes from
portable/intake-only layers.

## Completion Receipt

- Host provider body contract exists at `standalone-package/docs/host-promotion-provider-body.md`.
- Provider body pseudocode exists at `standalone-package/examples/provider-body/pseudocode.md`.
- Claim-boundary scan passed for non-source package content.
