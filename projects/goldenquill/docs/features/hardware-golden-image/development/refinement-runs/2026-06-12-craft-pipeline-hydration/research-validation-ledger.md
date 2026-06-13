# Research Validation Ledger - Hardware and Golden Image

- Run ID: `2026-06-12-craft-pipeline-hydration`
- Dispatch: `gq-research-strategy-hardware-golden-image-2026-06-12`
- Gate applied: rg05 (claim-evidence) + rg02 (local-first) + rg04 (org isolation) + rg06 (owner boundary)
- Validation rule: every claim maps to a source class + concrete file path/handle + validation state. Block if any claim lacks a local path, source class, or explicit external-approval state.

## Source Classes

- SC-LEDGER — node Craft ledger (`.craft/ledger.yml`)
- SC-CONTRACT — source workbook handoff (`docs/golden-quill-task-role-breakdown-handoff.md`)
- SC-CONFIG — project router/hardware config (`router.yaml`)
- SC-CANON — project doctrine (`CLAUDE.md`)
- SC-RUN — node-local run artifacts (seed / invoke-first / strategy / evidence-index)
- SC-EXT — external (NOT activated this run; permission-gated)

## Claim → Source → Validation

| # | Claim | Source class | Path / handle | Validation state |
| --- | --- | --- | --- | --- |
| C1 | Four active gaps exist with named severity + owner | SC-LEDGER | `.craft/ledger.yml` gaps[0-3] | VERIFIED-LOCAL |
| C2 | Eight Workstream-A hardware tasks with role/effort bindings | SC-CONTRACT | `docs/golden-quill-task-role-breakdown-handoff.md` §1 Workstream A | VERIFIED-LOCAL |
| C3 | Golden Image = one installable, versioned, signed artifact (cross-node interface) | SC-CONTRACT | same, §1 Workstream B "Golden Image assembly" | VERIFIED-LOCAL |
| C4 | Golden Image manifest verification + router-template Ed25519 signing already governed | SC-CONFIG / SC-CANON | `router.yaml` L17-23, L48; `CLAUDE.md` v7.0.7 §6.1 | VERIFIED-LOCAL |
| C5 | Reference SKUs (M3 Ultra / GX-10 / Spark) + 128 GB floor named in doctrine, not as testable spec | SC-CANON | `CLAUDE.md` Product Naming Chain + Hardware section | VERIFIED-LOCAL |
| C6 | Refine seed pre-selected falsification + x-ray overlays; first deliverable = hardware-to-image x-ray + low-cost acceptance test | SC-RUN | `REFINE-SEED-PROPOSAL.md`; `INVOKE-FIRST-ARTIFACTS.md` | VERIFIED-LOCAL |
| C7 | Local evidence sufficient to author spec SHAPE of all 4 gaps; insufficient for burn-in numeric thresholds + current-SKU specs | SC-RUN / SC-CONFIG | synthesis of C2+C4+C5 vs `RESEARCH-STRATEGY.md` External Evidence Classes; `router.yaml` holds no SKU/burn-in data | VERIFIED-LOCAL (negative confirmed) |
| C8 | EXT-HGI-1 (reference-SKU specs) needed for `GAP-HGI-REFERENCE-SPEC`; bounded; no protected-context risk | SC-EXT | DEFERRED — not run; approval pending Josh (gate rg03) | DEFERRED-PENDING-APPROVAL |
| C9 | EXT-HGI-2 (burn-in threshold references) needed for `GAP-HGI-BURN-IN`; bounded; no protected-context risk | SC-EXT | DEFERRED — not run; approval pending Josh (gate rg03) | DEFERRED-PENDING-APPROVAL |
| C10 | GAP-HGI-IMAGE-VERIFY + GAP-HGI-BACKUP-RECOVERY are locally authorable; block severity = "not yet written," not "evidence missing" | SC-CONFIG / SC-CANON | `router.yaml` L17-48 signing chain; `CLAUDE.md` Sovereignty Promise | VERIFIED-LOCAL (assessment) |

## Gate Checks

| Gate | Condition | Result |
| --- | --- | --- |
| rg02 local-first | Local evidence reviewed before any external class activated | PASS — all VERIFIED claims local; no external run |
| rg03 external-approval | External research only with named gap + Josh approval | HELD — EXT-HGI-1/2 named + deferred; nothing executed |
| rg04 org-isolation (Law 3) | Golden Quill project evidence only; no client org PROJECT_CONTEXT read | PASS — no `orgs/` read |
| rg05 claim-evidence | Each claim → source class + path/handle + validation question | PASS — C1-C10 mapped |
| rg06 owner-boundary | Planning evidence only; no canonical/lifecycle mutation | PASS — only 2 RUN_DIR files written; ledger untouched |

## Overall Verdict

**PASS (local-first).** All ten claims carry a source class and concrete path. Two claims (C8, C9) are correctly held in DEFERRED-PENDING-APPROVAL state rather than executed, satisfying the local-first + permission-gate discipline. No claim is unsupported, no client org context was read, and no canonical store or lifecycle artifact was mutated. The node is ready for an operator decision: approve the two bounded external passes and/or authorize a local-first Refine execution pass for the three locally-authorable gaps.
