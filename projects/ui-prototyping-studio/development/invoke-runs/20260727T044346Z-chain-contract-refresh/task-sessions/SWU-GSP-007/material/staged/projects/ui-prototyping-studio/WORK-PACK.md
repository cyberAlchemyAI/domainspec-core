---
id: ui-prototyping-studio-historical-work-pack
project: ui-prototyping-studio
title: "UI Prototyping Studio — Historical June Build Plan"
status: superseded
node_type: work-pack
updatedAt: 2026-07-27
---

# Historical Work Pack

> This root work-pack records the June 2026 extraction and deep-spec plan. It
> is retained as design lineage and **must not be used as the current execution
> selector**.

## Current authority

The current execution contract is
[development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md](development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md).
Task Session results and joined Invoke closeout receipts under
`development/invoke-runs/20260727T044346Z-chain-contract-refresh/` own
implementation evidence. [.craft/ledger.yml](.craft/ledger.yml) owns scoped
lifecycle state.

## Historical objective

The June plan proposed extracting the Studio backend, establishing the CLI and
operating skill, adding an artifact/canonicalization substrate, implementing a
deterministic admission fence and two-gate apply flow, adding browser
annotation/action surfaces, and restoring a runnable test harness.

That plan used wave labels such as X1/X2, M0–M3, U1/U2, P, E, and Z. Those
labels are historical decomposition, not selectable work units now. Detailed
contracts remain available through Git history and the dated material under:

- `development/deep-spec-dispatch/`
- `development/refinement-runs/`
- `development/PLAN-NEXT.md`
- `provenance/legacy-domainspec-spec/`

## What replaced it

The 2026-07-27 architecture review reconciled the live implementation and
reduced the remaining defects to the seven-unit Governed State Projection
chain:

```text
GSP-001 evidence harness
GSP-002 store freshness
GSP-003 current-head projection
GSP-004 honest visible-change diff
GSP-005 action acknowledgment, annotation, and mobile evidence
GSP-006 separated handoff readiness predicates
GSP-007 receipt-driven docs and Craft closeout
```

The amended work-pack and immutable receipts—not this historical plan—record
their actual completion status and verification counts.

## Claim boundary

Local implementation completion does not imply:

- complete accessibility or human ergonomics evidence;
- publication, deployment, or release authorization;
- production-complete DOM identity/CSS attribution;
- complete crash-compensation behavior; or
- delivery of the historical L4–L6 research ambitions.

## Next route

There is no executable route from this historical work-pack. The current Craft
ledger and amended work-pack own the frontier. After the seven GSP units close,
human-study evidence and release ownership are separate routes that require
explicit owners; there is no further implied implementation SWU.
