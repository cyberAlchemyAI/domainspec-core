---
title: §0.5 v28 — paired-commit amendment for §4 v2.x.6 OD-5 router dedup
filed: 2026-05-16
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-16T16:30:00Z at lock_history row 235 (sibling 2/2 of compound paired-commit; §4 v2.x.6 sibling 1/2 at row 234). Operator-Ed25519 signature verified against pinned cards-publisher pubkey. Canonical SHA3-512 = `474482990b96dcbc…51383683c1a7eed3`. Ed25519 signature prefix = `6a6adfb2b72ddc30…44a72e1183a7d602`. Runtime-live row count: 548 → 549.
parent_lock: pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_5_amendment.md (§0.5 v27 LOCKED 2026-05-16 row 233)
parent_lock_row: 233
amendment_class: narrow-corrective — single-row routing-module update record reflecting the OD-5 router dedup landed in §4 v2.x.6.
sibling_amendment: pipeline/blueprint/v0.1/section_04_v2_x_6_router_dedup_amendment.md
runtime_live_delta: 548 → 549 (+1 row)
---

# §0.5 v28 paired-commit amendment for §4 v2.x.6

## §0. Amendment intent

This narrow paired-commit amendment registers one row update for the OD-5 router dedup landed in `pipeline/blueprint/v0.1/section_04_v2_x_6_router_dedup_amendment.md`. The row records:

- `pipeline/orchestrator/router.py` adopts the OD-5 dedup shape — `_enforce_cloud_boundary_pre` + `_enforce_cloud_boundary_post` retired; `_dispatch_with_classification_boundary` invokes `enforce_outbound_boundary` per cloud dispatch; `_call_anthropic` + `_call_openai_style` accept `http_post: OutboundCallable` parameter.

No new primitive_kinds. No new failure-code rows. No new AST-lint rules. No new sub-kinds. The F-CLASS-* family roster count stays at 16 primitives (unchanged from §4 v2.x.5 row 232 / §0.5 v27 row 233 LOCK).

## §1. Single row entry (post-LOCK target shape)

| row | primitive_kind | seat_owner | path | description | lock_class | lock_history_row |
|-----|---------------|------------|------|-------------|------------|------------------|
| 549 | routing-module | provider_boundary | pipeline/orchestrator/router.py | OD-5 dedup: `_enforce_cloud_boundary_pre/post` retired in favor of single-source-of-truth wrap via `enforce_outbound_boundary(stdlib_urlopen_caller, ...)`. The wrapper is the SOLE site of F-CLASS PRE/POST gate firing for router-level cloud dispatch (closes RT-17 single-source-of-truth from §4 v2.x.5 Cycle 1 Red Team). Exception-class translation layer at `_dispatch_with_classification_boundary` re-raises `OutboundBoundaryRefusedError` as `ClassificationBoundaryError` preserving existing `call_seat` fallback-branch handler contract. | blueprint | 234 (anticipated — sibling member 2/2 of compound paired-commit with §4 v2.x.6 at row 235) |

## §2. Composition with §4 v2.x.5 + §0.5 v27

This amendment extends §0.5 v27 (LOCKED 2026-05-16 row 233) which landed 10 rows (1 routing-module + 5 failure-code sub-tag-extension records + 1 AST-lint + 3 subprocess-envelope-schema sub-tag-extension records). The current §0.5 v27 row covering router.py records the partial OD-5 landing (`_http_post` rewire only). This v28 amendment supersedes that row by extending the same routing-module entry to record the full OD-5 closure.

**Supersession protocol.** Per the v7.0.4-M1 precedent + §4 v2.x.1 row-198 narrow-corrective precedent, the v27 row is preserved on disk as historical audit trail; v28's row 549 is the authoritative current-state record. No in-place edit to v27's row content.

## §3. Compound paired-commit LOCK shape

Per §6.17 Option-B compound-LOCK discipline (same shape as §4 v2.x.5 + §0.5 v27 compound row 232/233):

- `lock_timestamp_utc` shared with §4 v2.x.6 sibling
- `lock_mode: COMPOUND-LOCK sibling 1/2 — paired with [§4 v2.x.6 | §0.5 v28] at the same lock_timestamp_utc`
- `compound_lock_with: ["section_04_v2_x_6_router_dedup_amendment.md"]` (this row) + `["section_00_5_section_04_v2_x_6_amendment.md"]` (sibling row)

Both rows append at the same lock_history.v1.jsonl entry pass per the existing compound-paired-commit protocol.
