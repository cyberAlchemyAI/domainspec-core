# Goal Loop — Component Registry (A1) + Studio Readiness (B)

- Spell: `goal` · Bound ledger: `projects/ui-prototyping-studio/.craft/ledger.yml` (`ui-prototyping-studio.craft`)
- Decision profile: `neutral-default` (fail-closed)
- Mode: read + author + **stage** (no ledger mutation, no commit — approval-gated)

## Frontier snapshot (round 1)

Routed nodes (from the bound ledger):
- **A1 →** `GAP-COMPONENT-REGISTRY-002` (R-1, persistence/index entity unspecified) + `BLK-IDENTITY-TYPES-002` (identity/DNA types absent from `models.ts`).
- **Goal B →** `GAP-CONTRACT-DRIFT-004`, `BLK-FIXTURE-CORPUS-001`, `GAP-DOCS-CODE-SPLIT-005`, `DEC-CLI-NOT-MCP-012`.

## Risk classification

| Node | Action | Risk tier | Route |
| --- | --- | --- | --- |
| A1 author `UIIdentityIndex` design | author new doc | **T1 reversible** | `invoke design` → done (artifact written) |
| A1 close `GAP-COMPONENT-REGISTRY-002` in ledger | ledger mutation | **T2 durable** | staged delta — approval-gated |
| Goal B author readiness plan | author new doc | **T1 reversible** | `invoke plan` → done (artifact written) |
| Goal B stage readiness nodes in ledger | ledger mutation | **T2 durable** | staged delta — approval-gated |
| B4 docs/code-split decision | operator decision | **T2 durable** | `decision-gate` — operator-owned |

## Dispatched (T1, complete)

- `invoke design` → `development/component-registry-spec/UIIdentityIndex-DESIGN.md` (A1 deliverable). Receipt: **pass** (parent-coordinator).
- `invoke plan` → `development/component-registry-spec/STUDIO-READINESS-PLAN.md` (Goal B route). Receipt: **pass** (parent-coordinator).

## Staged ledger deltas (PROPOSED — not applied)

1. **+ artifact** `ART-UIIDENTITYINDEX-DESIGN` → `development/component-registry-spec/UIIdentityIndex-DESIGN.md`; relates-to `GAP-COMPONENT-REGISTRY-002`, `BLK-IDENTITY-TYPES-002`.
2. **+ artifact** `ART-STUDIO-READINESS-PLAN` → `development/component-registry-spec/STUDIO-READINESS-PLAN.md`; relates-to `GAP-CONTRACT-DRIFT-004`, `BLK-FIXTURE-CORPUS-001`, `GAP-DOCS-CODE-SPLIT-005`.
3. **~ gap** `GAP-COMPONENT-REGISTRY-002`: treatment `defer` → `fix-in-design-merge`; note "R-1 specified in `ART-UIIDENTITYINDEX-DESIGN`; pending merge into `SYNTHESIZED-DEEP-DESIGN.md §2.4`."
4. **~ blocker** `BLK-IDENTITY-TYPES-002`: add design ref `ART-UIIDENTITYINDEX-DESIGN §3`; status stays `active` (implementation = A2, gated).
5. **+ next-moves** B1–B4 from the readiness plan as proposed slices (not active rows).

## Gates

| Gate | State |
| --- | --- |
| Source authority | **pass** (ledger bound) |
| Risk classification | **pass** (all tiered; no unknown/protected) |
| Read-only boundary | **pass** (T1 authored; T2 staged, not written) |
| Receipt closeout | **pass** (both T1 lanes terminal) |
| Approval token | **PENDING** — staged deltas await operator approval before ledger apply/commit |

## Stop

`stop_reason: batch-ready`. Two T1 artifacts authored; five staged ledger deltas framed. **Awaiting approval token** to promote (apply to `ledger.yml`) and/or commit. Nothing mutated yet.
