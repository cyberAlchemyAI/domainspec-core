# Stage 09 — Invoke Plan (non-executed)

- Capability: `invoke` · Mode: `plan` · Status: **pass**

## Build slices (architecture-first; each independently meaningful)

### A1 — Specify `UIIdentityIndex` (design artifact; closes Q4 on paper)
- Add to the deep-spec as a **derived read-model** (no new entity name): repo-scoped projection over the append-only event logs, keyed by `UIElementIdentity` via `TypedReference`, regenerable, non-canonical.
- **Done:** Q4 residue in `SYNTHESIZED-DEEP-DESIGN.md §2.4` moves from RESIDUE → specified; states store/query/match.
- **Cost:** doc only. **No code.**

### A2 — Implement the index projection (when L4 lands)
- Build `UIIdentityIndex` as a regenerable cache over the repo's event logs; **phase-1 `data-od-id` equality** matching; `rebuild` command; cache stamped `derived; do not edit` (RP-2).
- **Done:** identities resolve across sessions; drift always resolves to events.

### A3 — DNA enum-name fill for R-7 dimensions
- From the **existing s1 mapping**, add resonant token **namespace-names** as enum members for Motion/Interaction/State/Feedback/Numeric — names only, `external_context`, `confidence<1.0`, **provenance recorded** (RP-3). **No vendoring, no values, no promotion.**
- **Done:** the 24-enum genome's underfilled dims carry recognizable names; A2/A3 audited.

### A4 — Components page = projection of the index
- Render `UIIdentityIndex` as the components page (read-model projection); inherits recognition-over-recall.
- **Done:** the "page for components" exists as a projection — *free* once A2 ships.

## Sequencing

A1 (doc, now) → A2 (needs L4) → A3 (parallel to A2, doc+enums) → A4 (free after A2). A1 + A3 are doable today without touching runtime.

## Deferred (named, gated)

- **DNA-similarity matching** (AF4 phase 2) — after phase-1 proves out.
- **resonant vendoring** — gated behind `bounded-research` (license/provenance); not needed for A1–A4.
- Cross-session lineage edge-cases beyond identity keying.

## Validation surface

Deep-spec review for A1/A3; when A2/A4 build, they must keep L0 green and express only in existing vocabulary (A1).

## Non-executed — recommended build order for a future `task-session`.
