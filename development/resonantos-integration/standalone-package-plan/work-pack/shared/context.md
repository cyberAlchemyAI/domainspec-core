# Shared Context

## Source Evidence

- `development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md`
- `development/resonantos-integration/findings.md`
- `development/resonantos-integration/owned-base/BASE-FOR-VICTOR.md`
- `development/resonantos-integration/HANDOFF-CARD.md`

## Integration Boundary

ResonantOS owns:

- Living Archive read path.
- Fact-over-time substrate.
- Review Queue surface and approve/reject/escalate decision enum.
- Named `promote_review_artifact` seam.

CyberAlchemy package work owns:

- Public-safe governance contract packaging.
- Evidence-card and EvidenceSet validator carry-forward.
- No-promotion guardrail.
- Scope-tag mapping.
- Host-side provider body contract behind the existing seam.

## Claim Boundaries

- The promotion provider body is unbuilt.
- The package is not a runtime memory service.
- Recall importance is host-owned; govern/rely-on importance is the additive layer.
- Private-only names and internals must not appear in package output.

## Future Package Root

Planned staging root:

`development/resonantos-integration/standalone-package/`

This root does not exist yet and should be created only by `SWU-RCI-001`.
