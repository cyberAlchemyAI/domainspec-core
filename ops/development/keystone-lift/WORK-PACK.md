---
module: keystone-lift
version: current
status: draft
updatedAt: 2026-06-14
docType: work-pack
---

# WORK-PACK: Keystone Lift

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | block | Mutation blocked until B-KSL-2 moat-leak audit is wired and the defs-split decisions are applied; planning is complete. |
| complexity | medium | Cross-repo (arcanum + domainspec), changes invoke default; reversible, single-owner → medium not high. |
| outputMode | split | Required above low complexity. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Wave choreography + hard stops. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0–L3 decisions. |
| activeLayerWindow | L0 | Start with the non-cutover lift. |
| lastUpdatedAt | 2026-06-14T00:00:00Z | |
| readinessProfile | pilot | Local pilot of the public wedge before M2 pipeline. |

## Objective Summary
- **Objective:** land the DomainSpec keystone in public arcanum — the SPEC+aspect template as invoke's `define` baseline (replacing Module Formulae) and the wedge taxonomy/definitions (DS-D1/D2 canonical) — so the M2 spec→test→observability→audit pipeline has one shared, public spec contract to build on.
- **Primary inputs:** [build-decisions](../domainspec-arcanum-build-decisions.md) (B1/B2/B3, C1/C2/C3), [wedge-inventory](../domainspec-wedge-inventory.md).
- **Success condition:** invoke `define` emits a DomainSpec-format SPEC referencing canonical arcanum IDs; Module Formulae removed; g05 moat-leak audit green; arcanum link-checker/definitions-index green; DS references resolve.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Wedge definitions canonical in arcanum (no cutover) | L0 | W0 | — | arcanum link-checker + definitions-index green; no moat ID present |
| S-002 | DomainSpec SPEC+aspect templates sanitized + placed in invoke | L0 | W0 | — | templates render; grep clean of private paths/`ZefraHub`/PT terms |
| S-003 | invoke `define` cut over to DomainSpec template + discovery gate | L1 | W1 | S-001, S-002 | `define` dry-run emits DomainSpec SPEC referencing canonical IDs |
| S-004 | Private DS references arcanum; moat cluster retained; prose→example | L2 | W2 | S-001, S-003 | DS refs resolve; prose links to IDs; moat cluster still private |
| S-005 | Moat-leak + sanitization audit passes | L2 | W2 | S-004 | g05 whole-diff: zero moat terms/paths public |
| S-006 | Module Formulae removed; contract frozen for M2 | L3 | W3 | S-003, S-005 | no `module-formulae` references; arcanum gates green |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-DEF-LIFT](work-pack/tasks/TASK-DEF-LIFT.md) | Split DEFINITIONS.md; lift wedge subset to arcanum canonical | L0 | high | W0 | C1/C2 | ready | not-started |
| [TASK-TPL-PORT](work-pack/tasks/TASK-TPL-PORT.md) | Sanitize + place DomainSpec SPEC+aspect templates in invoke templates | L0 | medium | W0 | B1/spec-write | ready | not-started |
| [TASK-INVOKE-CUTOVER](work-pack/tasks/TASK-INVOKE-CUTOVER.md) | Wire `define` to DomainSpec template; update SKILL.md/define.md; add discovery soft gate | L1 | high | W1 | spec-write decision | ready-after S-001,S-002 | not-started |
| [TASK-DEFS-REF-PRIVATE](work-pack/tasks/TASK-DEFS-REF-PRIVATE.md) | DS DEFINITIONS.md references arcanum for wedge; keep moat cluster; D4/D5/D6 private | L2 | medium | W2 | C2/C3 | ready-after S-001 | not-started |
| [TASK-PROSE-RECOMPOSE](work-pack/tasks/TASK-PROSE-RECOMPOSE.md) | Recompose TAXONOMY/RELATIONSHIPS prose as example layer pointing at IDs | L2 | low | W2 | C1 | ready-after S-001 | not-started |
| [TASK-AUDIT](work-pack/tasks/TASK-AUDIT.md) | g05 whole-diff moat-leak + sanitization + arcanum validator audit | L2 | medium | W2 | B-KSL-2 | ready-after-impl | not-started |
| [TASK-MF-REMOVE](work-pack/tasks/TASK-MF-REMOVE.md) | Remove `module-formulae/` family; update dev-doc/craft refs | L3 | medium | W3 | B1 full-replacement | ready-after S-003,S-005 | not-started |
| [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) | Completion verification + M2 contract freeze | L3 | medium | W3 | success condition | ready-after-impl | not-started |

## Layer-Mapped Waves

- **W0 (L0 — "can the wedge live in arcanum?"):** TASK-DEF-LIFT, TASK-TPL-PORT. Promotion evidence: arcanum link-checker/definitions-index green; templates render; sanitization clean.
- **W1 (L1 — "can define produce DomainSpec specs?"):** TASK-INVOKE-CUTOVER. Promotion evidence: `define` dry-run output.
- **W2 (L2 — "does the split hold with no moat leak?"):** TASK-DEFS-REF-PRIVATE, TASK-PROSE-RECOMPOSE, TASK-AUDIT. Promotion evidence: g05 audit green; DS refs resolve.
- **W3 (L3 — "is it packaged for M2?"):** TASK-MF-REMOVE, TASK-VERIFY. Promotion evidence: no MF refs; contract frozen.

## SWU Manifest (shared)

| SWU | Parent | Goal | Write scope | Acceptance evidence | Verify | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-KSL-001 | TASK-DEF-LIFT | Extract wedge subset (DS-D1/D2/D3/D7/D8/D10/P1-3) into `arcanum/definitions/DEFINITIONS.md` canonical, collision-safe IDs | `arcanum/definitions/` | canonical IDs present; `schema`/`contract` collisions resolved w/ boundary note | arcanum link-checker + definitions-index | subagent |
| SWU-KSL-002 | TASK-DEF-LIFT | Exclude moat cluster (DS-C3/D9/COR-1/F1/F5/F6/M13) + proposed 38-edge ext; hold D4/D5/D6 | (read-only verify) | grep: none of the moat IDs present in arcanum | grep + review | subagent |
| SWU-KSL-003 | TASK-TPL-PORT | Copy + sanitize SPEC.md + aspect templates (operations/queries/interfaces/states/events/mappings) into invoke templates as `domainspec-spec/` | `arcanum/spells/invoke/templates/domainspec-spec/` | templates present; grep clean of private paths/`ZefraHub`/`veracidade`/`convicção` | grep + render check | subagent |
| SWU-KSL-004 | TASK-INVOKE-CUTOVER | Point `define` baseline at `domainspec-spec/`; edit SKILL.md + `define.md` "Module Formulae baseline" → "DomainSpec template" | `arcanum/spells/invoke/{SKILL.md,define.md}` + `.claude/skills/invoke/` mirror | text updated; no dangling MF baseline claim | grep "Module Formulae"; define dry-run | local-fallback |
| SWU-KSL-005 | TASK-INVOKE-CUTOVER | Add discovery-existence soft gate + `--skip-discovery` waiver writeback to define | `arcanum/spells/invoke/define.md` | gate documented; waiver reason field defined | review | local-fallback |
| SWU-KSL-006 | TASK-DEFS-REF-PRIVATE | Replace wedge defs in `implementation/domainspec/.../DEFINITIONS.md` with references to arcanum; keep moat cluster canonical | `research/projects/domainspec/definitions/DEFINITIONS.md` | wedge terms reference arcanum; moat cluster intact; D4/D5/D6 private | DS refs resolve; grep | subagent |
| SWU-KSL-007 | TASK-PROSE-RECOMPOSE | Rewrite TAXONOMY.md/RELATIONSHIPS.md prose to link canonical IDs (example layer) | `arcanum/definitions/TAXONOMY.md`, `RELATIONSHIPS.md` (lifted copies) | prose links resolve to canonical IDs | link-checker | subagent |
| SWU-KSL-008 | TASK-MF-REMOVE | Delete `module-formulae/`; update dev-doc/craft references | `arcanum/spells/invoke/templates/module-formulae/` + ref sites | dir gone; refs updated | grep "module-formulae" → 0 in live docs | local-fallback |

> Closure tasks TASK-AUDIT and TASK-VERIFY carry SWU exemptions (AUDIT / VERIFY).

## Validation Strategy (per slice)
- **S-001/S-007:** `arcanum` markdown-linking constitution + definitions-index + link checker (commit `7de3fd3`) green.
- **S-002/S-003:** invoke `define` dry-run produces a DomainSpec SPEC + aspect docs referencing canonical IDs; template render check.
- **S-004:** DS-side references resolve to arcanum; moat cluster still present + private.
- **S-005 (gating):** g05 whole-diff audit — grep the staged arcanum diff for moat IDs (DS-C3/D9/COR-1/F-series/M13), private paths, `ZefraHub`, PT confidence terms, hardcoded DS validator names → must be zero.
- **S-006:** `grep -r module-formulae arcanum` returns only historical/log hits; arcanum gates green.

## Blockers
- **B-KSL-1 (resolved):** DS-D4/D5/D6 placement → held PRIVATE by default (decision C3); applied in TASK-DEFS-REF-PRIVATE. Revisit only if definitions-governance proves decoupling.
- **B-KSL-2 (open, gates W2→W3):** the g05 moat-leak + sanitization audit must pass before any arcanum push and before Module Formulae removal. Owner: TASK-AUDIT.
- **B-KSL-3 (constraint):** submodule-first — commit+push in arcanum before any parent gitlink bump (`make bump-check`).

## Recorded Gaps
- **G-KSL-1 (resolved):** define + design now authored — [SPEC.md](SPEC.md), [GLOSSARY.md](GLOSSARY.md), [DESIGN.md](DESIGN.md). The build-decisions record + wedge-inventory remain the decision basis.
- **G-KSL-2 (resolved):** all 8 task contracts + [EXECUTION-PACK.md](EXECUTION-PACK.md) authored. Work-pack is execution-ready.
- **Remaining (execution-time only):** B-KSL-2 moat-leak audit must run+pass at execution; this is a runtime gate, not an authoring gap.

## Current State (2026-06-14, task-session)
**Done — local working tree in `arcanum`, nothing committed/pushed:**
- ✅ TASK-DEF-LIFT — wedge subset (DS-D1/D2/D3/D7/D8/D10/P1-3) canonical in `arcanum/definitions/DEFINITIONS.md`; index updated; link+anchor checker GREEN; exclusions verified (moat/ambiguous/38-edge absent).
- ✅ TASK-TPL-PORT — `arcanum/spells/invoke/templates/domainspec-spec/` (SPEC + 6 aspect docs + README); audit clean.
- ✅ TASK-INVOKE-CUTOVER (define.md) — baseline → `domainspec-spec/`; discovery soft gate added. (SKILL/other-mode "Module Formulae" sweep deferred to W3/TASK-MF-REMOVE.)
- ✅ TASK-AUDIT (B-KSL-2) — whole-diff moat-leak audit GREEN (moat IDs / ambiguous / stale-PT / DS-CI-names / private-paths / 38-edge all = 0).

**W2 done (local):**
- ✅ TASK-PROSE-RECOMPOSE — `arcanum/definitions/TAXONOMY.md` + `RELATIONSHIPS.md` lifted with example-layer banners → canonical DS-D1/D2; broken DS-internal links stripped; link checker GREEN.
- ✅ TASK-DEFS-REF-PRIVATE — parent `research/projects/domainspec/definitions/DEFINITIONS.md` now carries the open-core split banner (arcanum canonical for wedge; moat + D4/D5/D6 private). *Follow-up: full prose de-duplication of the 9 wedge bodies (kept as local mirror for now).*

**W3 status:**
- ⚠️ **TASK-MF-REMOVE — BLOCKED/deferred (evidence-based).** "Module Formulae" has 80+ live references including the invoke spell's **own validation fixtures, experiment-loops, and live-evidence**, plus the separate `mogt-agentic-conversation` research project's `module-formulae/` artifact convention. Physically deleting the family now would break the invoke validation suite. Per the TASK-MF-REMOVE "flag, don't silently break" clause: marked the pack **deprecated** in-place (`module-formulae/README.md`) pointing at `domainspec-spec/`; physical removal + fixture/contract migration is a separate follow-up task (TASK-MF-REMOVE-2).
- ✅ TASK-VERIFY (verdict: **FLAG**) — wedge lift + define cutover done + whole-diff audit GREEN + all link checks GREEN; deferred: live `define` dry-run (contract cut over, not executed end-to-end) and module-formulae physical removal.

**Final whole-diff moat-leak audit: GREEN** (moat/ambiguous/PT/private-paths/DS-CI/38-edge all = 0).

**Outstanding (gated):** commit + push — awaiting explicit operator go per "commit/push only when asked." Change set: 7 arcanum items (public) + 1 parent private-defs edit + planning artifacts.

activeLayerWindow: L0+L1 done, L2 done, L3 partial (MF-REMOVE deferred).

## Next Route
`sigil-development` / `spellcraft` own the invoke contract + template changes (target is a spell); `task-session` executes the definition-lift and DS-side SWUs. Plan authors handoff context only — it does not mutate arcanum or domainspec.
