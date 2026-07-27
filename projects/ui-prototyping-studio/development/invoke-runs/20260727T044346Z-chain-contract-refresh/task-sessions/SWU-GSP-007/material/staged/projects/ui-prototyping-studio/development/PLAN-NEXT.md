---
id: plan-next
project: ui-prototyping-studio
title: "PLAN-NEXT — Historical June Hardening Plan"
status: superseded
node_type: implementation-plan
source: refinement-runs/20260618-spec-arch-update-gap-audit
updatedAt: 2026-07-27
---

# PLAN-NEXT — historical hardening plan

> This plan was executed against the June 2026 frontier. It is preserved as
> provenance, not as a live queue. The current authority is
> [invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md](invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md)
> plus the receipts under
> `invoke-runs/20260727T044346Z-chain-contract-refresh/`.

## Historical findings and disposition

| Historical item | Current disposition |
| --- | --- |
| N1 export confirmation in the core | Implemented. CLI and HTTP inherit the application-use-case gate. |
| N2 legacy HTTP decision | Surface retained; critical export route is gated and tested. |
| N3 preview Accept/Discard/Revert | Implemented; Accept/Revert now additionally requires live actor-neutral acknowledgment. |
| N4 revert wrong-target guard | Implemented and covered by unit tests. |
| N5 tester-document sync | Reconciled again by GSP-007 against current receipts. |
| N6 finite AUTO scores | Implemented; invalid scores fail closed. |
| N7 cycle ceiling | Implemented in the core. |
| N8 honest diff | Superseded by explicit structural, style/global, unattributed, and visible-change evidence. |
| N9 comment lifecycle | No-double-fold behavior is covered; broader product semantics remain a design concern. |
| N10 file-store safety | Corrupt files fail closed; GSP-002 adds fresh reads, serialization, and independent-process evidence. |
| N11 preview port resilience | Implemented; GSP-001 further establishes deterministic fail-fast startup and diagnostics. |

The dated suite was green at that frontier. The current completion audit is
TypeScript clean, unit/slice **72/72**, and Playwright **21/21**.

## What the 2026-07-27 chain added

- deterministic, diagnostic browser-harness startup;
- fresh reads across independently running processes;
- one application-owned current-head preview/annotation projection;
- non-silent CSS/global/unattributed diff evidence;
- identity-bound browser acknowledgment for Accept/Revert;
- real-target annotation and a 390px layout witness; and
- separate confirmation, completeness, integration, and implementation
  readiness predicates.

## Remaining routes

The implementation queue in this historical plan is closed. Remaining work is
not an implied continuation of N1–N11:

- a bound human-study route may collect trust/control ergonomics evidence;
- a bound accessibility route may broaden keyboard/focus/axe evidence;
- a release owner may decide publication/deployment/release gates; and
- deeper DOM identity, CSS cascade, and crash-compensation work requires a new
  scoped plan if selected.

No such route is authorized merely by this document.

## Provenance

The original findings and task detail remain under
`refinement-runs/20260618-spec-arch-update-gap-audit/` and in Git history.
