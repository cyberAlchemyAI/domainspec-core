---
module: keystone-lift
version: current
status: draft
updatedAt: 2026-06-14
docType: spec
---

# SPEC: Keystone Lift

## What This Module Owns
The migration that makes the **DomainSpec wedge** public: invoke's `define` mode emits DomainSpec-format specs (replacing Module Formulae), and the taxonomy/relationships/definitions vocabulary becomes canonical in public `arcanum`. It owns the wedge/moat split boundary for definitions and the moat-leak safety gate. It does **not** own the M2 pipeline sigils that later consume the template.

## Capabilities

| Capability | What | Key Aspects | Detail |
| --- | --- | --- | --- |
| Public canonical definitions | DS-D1/D2 wedge subset canonical in arcanum | lift, collision-guard, exclude moat | TASK-DEF-LIFT |
| DomainSpec spec template | SPEC+aspect templates as invoke `define` baseline | sanitize, place, cut over | TASK-TPL-PORT, TASK-INVOKE-CUTOVER |
| Wedge/moat definition split | DS keeps moat cluster + references arcanum for wedge | reference rewrite, D4/D5/D6 private | TASK-DEFS-REF-PRIVATE |
| Moat-leak safety gate | whole-diff audit blocks any moat term going public | grep gate, sanitization | TASK-AUDIT |
| Module Formulae retirement | remove the replaced template family | delete, ref-update | TASK-MF-REMOVE |

## Domain Concepts

| Concept | Type | Key Constraints |
| --- | --- | --- |
| Wedge subset | Set of definition IDs | DS-D1/D2/D3/D7/D8/D10/P1-3 only; canonical in arcanum |
| Moat cluster | Set of definition IDs | DS-C3/D9/COR-1/F1/F5/F6/M13; never public |
| Ambiguous cluster | Set of definition IDs | DS-D4/D5/D6; private by default until proven decoupled |
| Canonical home | Authority rule | arcanum canonical for wedge; DS references it |
| Moat-leak audit | Gate | zero moat IDs/private-paths/`ZefraHub`/PT-terms in the public diff |

## Behavior Contracts
1. **No moat leak (invariant):** at no point does a moat ID, private path, stale project string, or hardcoded DS validator name appear in a public-arcanum diff. Enforced by TASK-AUDIT before any push.
2. **One source of truth (invariant):** wedge definitions are canonical only in arcanum; DS holds references, not copies. No third source.
3. **Non-cutover-first (ordering):** definitions + templates land in arcanum (L0) before invoke's default changes (L1) before Module Formulae is removed (L3).
4. **Reversible until push:** all authoring + the lift are local until the moat-leak audit passes and submodule-first push happens.
5. **Brand:** public artifacts carry the "DomainSpec" name (decision B2); "CyberAlchemy"/governance engine stays private.

## Success Condition
invoke `define` dry-run emits a DomainSpec SPEC + aspect docs referencing canonical arcanum IDs; `module-formulae/` removed; g05 moat-leak audit green; arcanum link-checker/definitions-index green; DS references resolve.

## Out of Scope (M2+)
test-derivation engine, doc→metrics sigil, sync-registry, sync-user-stories, code-tag toolchain, audit-alignment, and all deferred improvements/new sigils.
