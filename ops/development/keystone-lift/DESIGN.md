---
module: keystone-lift
version: current
status: draft
updatedAt: 2026-06-14
docType: design
---

# DESIGN: Keystone Lift

Design basis: [SPEC.md](SPEC.md), [build-decisions](../domainspec-arcanum-build-decisions.md), [wedge-inventory](../domainspec-wedge-inventory.md). Six-view coverage is compressed to the four views that matter for a cross-repo doc/template migration (structure, dependency/interface, change-set, governance/validation).

## View 1 — Structure (what exists where, after)

```
public arcanum/
  definitions/
    DEFINITIONS.md        <- + wedge subset canonical (DS-D1/D2/D3/D7/D8/D10/P1-3)
    DEFINITIONS-INDEX.md  <- + new IDs
    DEFINITION-DRIFT-AUDIT.md <- + new IDs
    TAXONOMY.md           <- NEW (prose example layer -> IDs)
    RELATIONSHIPS.md      <- NEW (prose example layer -> IDs)
  spells/invoke/
    templates/domainspec-spec/  <- NEW (SPEC + aspect docs), module-formulae/ REMOVED at L3
    SKILL.md, define.md         <- "Module Formulae baseline" -> "DomainSpec template"; + discovery soft gate
private implementation/domainspec/
  research/projects/domainspec/definitions/DEFINITIONS.md
    wedge defs -> references to arcanum; moat cluster retained; D4/D5/D6 retained private
```

## View 2 — Dependency / Interface rules
- **arcanum must not reference private DS** (public can't depend on private). Canonical wedge text lives in arcanum.
- **DS may reference arcanum** (DS now depends on the arcanum submodule for wedge vocab) — accepted cost (C2).
- **invoke `define` → DomainSpec template → aspect docs**: the aspect-doc contract is the stable interface the M2 pipeline consumes. Freeze it at L3.
- **No new arcanum-native term is overwritten**: `DEF-ARC-CONTRACT`/`DEF-ARC-SCHEMA` stay; colliding DS terms get namespaced IDs + boundary notes.

## View 3 — Change-set (the diff, by wave)
| Wave | Repo | Files | Kind |
| --- | --- | --- | --- |
| W0 | arcanum | `definitions/*`, `spells/invoke/templates/domainspec-spec/*` | add |
| W1 | arcanum | `spells/invoke/{SKILL.md,define.md}` + `.claude/skills/invoke/` mirror | edit |
| W2 | domainspec | `research/projects/domainspec/definitions/DEFINITIONS.md` | edit (refs) |
| W2 | arcanum | `definitions/TAXONOMY.md`, `RELATIONSHIPS.md` | edit (prose→IDs) |
| W3 | arcanum | `spells/invoke/templates/module-formulae/` + ref sites | delete/edit |

## View 4 — Governance / Validation design (the moat-leak gate)
The safety design is **TASK-AUDIT (B-KSL-2)** — a deterministic gate run against the *staged arcanum diff* before any commit/push:

```
moat-leak audit (must all be 0 hits in the public diff):
  grep -E 'DS-C3|DS-D9|DS-COR-1|DS-F1|DS-F5|DS-F6|DS-M13'   # moat IDs
  grep -E 'DS-D4|DS-D5|DS-D6'                                # ambiguous (private by default)
  grep -iE 'ZefraHub|veracidade|convic'                      # stale/PT strings
  grep -E 'validate-governance-chain|validate-signals|domainspec-tuning' # hardcoded DS CI names
  grep -E '/home/.*implementation/domainspec|\.arcanum/'     # private paths
plus: arcanum markdown-linking constitution + definitions-index + link checker green.
```
Any non-zero hit ⇒ BLOCK; remediate before push. The gate runs at W2 (before DS-side + prose land publicly) and again whole-diff before the W3 push.

## Design decisions carried
- C1 formal-IDs canonical; C2 arcanum canonical + DS references; C3 D4/D5/D6 private; B1 full replacement; B2 DomainSpec public brand; B3 (engine) out of keystone scope.

## Risks / mitigations
- **Transitive moat reference inside a wedge def** → strip/abstract; if unseverable, demote that ID to private (TASK-DEF-LIFT rule 7 / edge cases).
- **DS now depends on arcanum submodule** → acceptable; documented; resolves at DS-side wave.
- **Reversibility** → everything reversible until the submodule-first push; the audit is the point of no return.
