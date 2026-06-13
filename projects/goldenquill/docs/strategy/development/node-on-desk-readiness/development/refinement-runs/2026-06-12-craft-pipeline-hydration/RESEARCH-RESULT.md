# Research Result — Golden Quill node-on-desk readiness (parent)

- Dispatch: `gq-research-strategy-node-on-desk-readiness-2026-06-12`
- Run dir: `docs/strategy/development/node-on-desk-readiness/development/refinement-runs/2026-06-12-craft-pipeline-hydration/`
- Mode: LOCAL-FIRST research execution (r01–r06). External research permission-gated and NOT run.
- Scope level: parent / cross-cutting recomposition readiness only. Child-node detail intentionally not duplicated.

## Node

- Craft node: `node-on-desk-readiness` (CTX-NOD-ROOT)
- Research lane: parent readiness recomposition
- Child spaces: 10 (boundary-and-canon, staffing-budget-and-triggers, hardware-golden-image, tilth-runtime-build, quality-security-proof, capital-logic-library, sales-contracting-legal, white-glove-delivery-node-care, company-operations-finance, after-acceleration-roadmap)

## Core Question

What evidence is needed to prove all child nodes add up to a working customer-node readiness path?

## Findings (each with local source path)

1. **The parent node is a recomposition surface, not a worker.** Its job is to prove the ten child spaces together produce a working customer node; child spaces own detailed blockers/decisions/gaps. Source: `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml` (notes; `recomposition[0]`) + `docs/strategy/development/node-on-desk-readiness/CRAFT.md` ("Current State").

2. **Single source contract feeds every child.** All ten child ledgers cite the same workbook extraction (`ART-*-HANDOFF` → `docs/golden-quill-task-role-breakdown-handoff.md`) as source-of-truth for tasks/roles/effort-types. Coverage of workbook workstreams A–G + After-Acceleration + Roles/Gaps maps 1:1 onto child contexts. Source: `docs/golden-quill-task-role-breakdown-handoff.md` (sheets 1–3) + parent ledger `artifacts_by_path`.

3. **Three parent-level gaps are the recomposition blockers.** `GAP-NOD-HOURS-RATES` (block — blank Est. Hrs / Rate columns block any staffing/capital budget), `GAP-NOD-CANON-VOCAB` (block — deprecated "Unrestricted / Hybrid / Sanitized / Sovereign" posture wording in workbook row B must translate to the canon three-posture set before any surface uses it), `GAP-NOD-SEQUENCE` (flag — workbook has no dependency order, done definitions, or recomposition gates). Source: `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml` (`gaps[0..2]`); workbook posture row at `docs/golden-quill-task-role-breakdown-handoff.md` line 50; blank budget columns at lines 34–80.

4. **The vocabulary gap is confirmed against canon, not just the workbook.** Current canon is the three-posture set Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign; "Sanitized" is explicitly deprecated. The boundary child already holds a blocking decision (`DEC-BC-POSTURE-VOCAB`) and blocker (`BLK-BC-POSTURE-VOCAB`). Source: `docs/strategy/development/boundary-and-canon/.craft/ledger.yml` (`decisions[0]`, `typed_items[0]`, `DEF-BC-POSTURES-001`) cross-checked against project `CLAUDE.md` (Beta Model Strategy v7.0.10 three-posture section).

5. **The UI row is a live scope-drift risk against the v0.1 no-UI lock.** Workbook "Operator console UI" row (handoff line 53) collides with the locked headless-only v0.1 boundary; boundary child carries an open phase-boundary decision (`DEC-BC-UI-BOUNDARY`) and the tilth child mirrors it (`GAP-TRB-UI-PHASE`). Recomposition cannot certify "working node" until this phase question resolves. Source: `docs/strategy/development/boundary-and-canon/.craft/ledger.yml` (`gaps[0]`, `decisions[1]`) + `docs/features/tilth-runtime-build/.craft/ledger.yml` (`gaps[2]`).

6. **Cross-child dependency edges already exist and must be tracked at the parent.** tilth-runtime-build links boundary-and-canon (`GAP-TRB-POSTURE-CANON` → owner boundary-and-canon) and hardware/Golden-Image packaging (`GAP-TRB-GOLDEN-IMAGE-HANDOFF`). capital-logic-library links the existing promotion-governance ledger (`REL-NOD-LINK-PROMO-GOV` → `[repo-root] .craft/ledger.yml`) rather than recreating it. These are the seams where "child nodes add up" is proven or fails. Source: `docs/features/tilth-runtime-build/.craft/ledger.yml` (`gaps[1,3]`) + parent ledger `relations[0]`.

7. **No child receipts have been recomposed upward yet; pipeline is strategy-ready and permission-gated.** Every child carries Refine + Research routes at status `pass` but `RUNTIME-HANDOFF` at `not_run`; parent `recomposition[0].status: flag` with residue "Hours/rates, canon corrections, sequencing, and child-ledger task decomposition remain open." The readiness path therefore cannot yet be asserted as proven. Source: parent ledger `recomposition[0]`; child ledgers' `ART-*-RUNTIME-HANDOFF` status across all sampled spaces.

## Lane Map Per Gap

| Gap | Severity | Local resolvable? | Lane | Owner child | External needed? |
| --- | --- | --- | --- | --- | --- |
| GAP-NOD-HOURS-RATES | block | Partial — structure local; actual hours/rates are operator business judgment | Defer to operator input (Josh) | staffing-budget-and-triggers | No (rates are Josh's call, not external lookup) |
| GAP-NOD-CANON-VOCAB | block | Yes — canon is in-repo | Local-only correction | boundary-and-canon | No |
| GAP-NOD-SEQUENCE | flag | Yes — derivable from child dependency edges | Local-only planning (parent recomposition) | node-on-desk-readiness (parent) | No |
| UI phase question (DEC-BC-UI-BOUNDARY / GAP-TRB-UI-PHASE) | flag | Yes — v0.1 lock is in-repo | Local-only governance decision | boundary-and-canon | No |
| Cross-child seams (posture, Golden-Image, promo-gov link) | flag | Yes — all referents in-repo | Local-only recomposition tracking | parent | No |

Every parent-level gap is resolvable from local evidence or from operator business judgment. None requires external lookup to close at this readiness level.

## External-Research Decision

**DEFERRED.** No named local-evidence gap survives parent-level synthesis that requires outside comparison. Per RESEARCH-DISPATCH rg03 (`human_approval`, on_fail `ask`) and the route-menu default (`none by default`), no external pass is requested.

Bounded external requests parked for a future approved pass (each would need a surviving named gap + Josh's explicit approval before running):

- **EXT-REQ-01 (deployment-readiness patterns):** compare appliance "node-on-desk" readiness checklists / acceptance-gate patterns from comparable sovereign/on-prem AI-appliance vendors — ONLY if `GAP-NOD-SEQUENCE` cannot be fully sequenced from in-repo child dependency edges. Bounded to readiness-gate structure, not product features. Protected-context flag: no Golden Quill confidential detail leaves the node.
- **EXT-REQ-02 (fractional-role market rates):** external market-rate benchmarks for Legal (fractional), Security Reviewer, Bookkeeper, Domain Experts — ONLY if Josh wants market anchors for `GAP-NOD-HOURS-RATES` rather than setting rates himself. Bounded to public rate ranges; no client data.

Both remain DEFERRED until a surviving gap + operator approval exist.

## Residue

- Parent recomposition status stays `flag`: child receipts have not been recomposed upward (no runtime stage run).
- `GAP-NOD-HOURS-RATES` is the single hard block on producing a staffing/capital budget; it needs operator-voice input (Josh's rates/hours), not more research.
- Canon-vocab correction and UI phase decision are owned by boundary-and-canon and gate downstream task derivation across tilth-runtime-build.
- Sequencing (`GAP-NOD-SEQUENCE`) is the parent's own to author from the cross-child dependency edges surfaced in Finding 6.

## Next Move

Author the parent-level recomposition sequence: assemble the cross-child dependency edges (posture-canon → tilth rows; hardware Golden-Image → tilth packaging; promo-gov link → capital) into a dependency-ordered readiness path with done-definitions and recomposition gates — closing `GAP-NOD-SEQUENCE` locally. Surface `GAP-NOD-HOURS-RATES` and the UI phase decision to Josh as the two operator-input items. Do NOT run external research; both bounded requests stay deferred.
