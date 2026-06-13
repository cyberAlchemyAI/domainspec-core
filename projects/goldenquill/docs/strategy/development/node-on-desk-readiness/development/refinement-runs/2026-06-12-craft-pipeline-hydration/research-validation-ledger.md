# Research Validation Ledger — node-on-desk readiness (parent)

Dispatch: `gq-research-strategy-node-on-desk-readiness-2026-06-12` · Gates checked: rg02 local-first, rg04 org-isolation, rg05 claim-evidence, rg06 owner-boundary.

Source classes: `craft-ledger` (parent/child `.craft/ledger.yml`) · `source-contract` (workbook handoff) · `canon` (project AGENTS.md / CLAUDE.md). All paths repo-root relative.

| # | Claim | Source class | Source path / handle | External approval state | Validation question | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | Parent node is a recomposition surface; children own detail | craft-ledger | `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml` (notes, `recomposition[0]`); `CRAFT.md` | n/a (local) | Does the ledger state children own detail and parent recomposes? | PASS |
| C2 | All 10 child spaces exist and cite the same workbook source contract | craft-ledger + source-contract | parent ledger `artifacts_by_path`; 10 child `.craft/ledger.yml` (`ART-*-HANDOFF`); `docs/golden-quill-task-role-breakdown-handoff.md` | n/a (local) | Do all 10 child ledgers resolve and reference the workbook? | PASS (4 read in full, 6 existence+gap-count confirmed) |
| C3 | Three parent-level gaps (hours/rates block, canon-vocab block, sequence flag) | craft-ledger | `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml` (`gaps[0..2]`) | n/a (local) | Are all three gaps present with stated severities? | PASS |
| C4 | Workbook uses deprecated 4-posture wording incl. "Sanitized"; canon is 3-posture | source-contract + canon | handoff line 50; `CLAUDE.md` Beta Model Strategy v7.0.10; `docs/strategy/development/boundary-and-canon/.craft/ledger.yml` (`DEC-BC-POSTURE-VOCAB`, `DEF-BC-POSTURES-001`) | n/a (local) | Does workbook wording differ from canon 3-posture set? | PASS |
| C5 | UI row conflicts with locked v0.1 no-UI boundary; open phase decision exists | source-contract + canon + craft-ledger | handoff line 53; `CLAUDE.md` (no-UI v0.1 lock); boundary ledger `decisions[1]` + tilth ledger `gaps[2]` | n/a (local) | Is there a locked no-UI boundary and an open decision against the UI row? | PASS |
| C6 | Cross-child dependency edges exist (posture, Golden-Image, promo-gov link) | craft-ledger | `docs/features/tilth-runtime-build/.craft/ledger.yml` (`gaps[1,3]`); parent ledger `relations[0]` | n/a (local) | Do child ledgers encode cross-space dependency edges? | PASS |
| C7 | No child receipts recomposed upward; pipeline strategy-ready/permission-gated | craft-ledger | parent `recomposition[0].status: flag`; child `ART-*-RUNTIME-HANDOFF` status `not_run` | n/a (local) | Are all runtime handoffs `not_run` and recomposition `flag`? | PASS |
| C8 | No surviving gap requires external research at parent level | derived (lane map) | RESEARCH-RESULT.md lane-map table; RESEARCH-DISPATCH `route_menu` (`none by default`) | DEFERRED (rg03 not invoked) | Is every parent gap local- or operator-resolvable? | PASS |
| C9 | hours/rates gap needs operator business judgment, not research | craft-ledger | `docs/strategy/development/staffing-budget-and-triggers/.craft/ledger.yml` (`GAP-SBT-HOURS-RATES`, `DEC-SBT-TRIGGER-MODEL` PENDING) | DEFERRED (optional EXT-REQ-02) | Is the gap a rate/threshold decision Josh owns? | PASS |

## Owner-Boundary Check (rg06)

- Wrote only the two RUN_DIR outputs (`RESEARCH-RESULT.md`, `research-validation-ledger.md`). No canonical/lifecycle artifact mutated; `.craft/ledger.yml` not edited. PASS.

## Org-Isolation Check (rg04 / Law 3)

- Evidence drawn only from Golden Quill PROJECT artifacts (node ledgers, workbook handoff, project canon). No `orgs/` client PROJECT_CONTEXT read. PASS.

## Local-First Check (rg02)

- No web search / WebFetch / external lookup performed. External classes recorded as DEFERRED bounded requests only. PASS.

## Overall Verdict

**PASS — readiness path is mappable but NOT yet proven.** Local evidence is sufficient to recompose the node-on-desk readiness structure and to identify every cross-cutting gap with a source path. Two of three parent gaps are local-only resolvable (canon-vocab, sequence); the third (hours/rates) is an operator-input block, not a research block. External research is correctly DEFERRED — no named gap survives that requires it. The "working customer-node readiness path" cannot be asserted as proven until child runtime receipts are recomposed upward and the hours/rates + UI-phase operator decisions land.
