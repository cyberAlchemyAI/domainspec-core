---
module: keystone-lift
task: TASK-INVOKE-CUTOVER
docType: work-pack-task
updatedAt: 2026-06-14
---

# TASK-INVOKE-CUTOVER — Wire invoke `define` to the DomainSpec template + discovery soft gate

Layer: L1 · Wave: W1 · Complexity: high · Gate: ready-after S-001,S-002 · Route: spellcraft (spell lifecycle)

## Objective
Make the DomainSpec template invoke's `define` baseline and add the harvested discovery-existence soft gate. This is spell-lifecycle work — route through `spellcraft`; this contract is the handoff spec.

## Dependencies
S-001 (canonical defs exist), S-002 (templates placed). Targets `arcanum/spells/invoke/` (+ `.claude/skills/invoke/` mirror).

## Implementation Detail Spec
- **Inputs:** placed `domainspec-spec/` templates; canonical arcanum definitions; current `define.md` + invoke `SKILL.md`.
- **Outputs:** updated `define.md` (baseline = DomainSpec template), updated `SKILL.md` (prereqs text), discovery soft-gate clause.
- **Ordered rules:**
  1. In `define.md` Template Selection, replace the Module Formulae baseline with the `domainspec-spec/` family as the standalone baseline; keep companion/candidate scaffolds.
  2. Replace "Module Formulae baseline coverage" wording in invoke `SKILL.md` + prerequisites with "DomainSpec template baseline."
  3. Add the **discovery-existence soft gate**: `define` searches for a discovery artifact; HALTs with a fixed recommendation if missing; `--skip-discovery` permitted but writes `discovery_waiver_reason` into the SPEC frontmatter.
  4. Update the `.claude/skills/invoke/` mirror to match.
  5. Do not remove `module-formulae/` yet (TASK-MF-REMOVE, L3) — only stop referencing it as baseline.
- **Edge cases:** other modes (design/plan/full) reference Module Formulae composition → leave those refs until L3; only the `define` baseline changes here.
- **Failure modes:** dangling "Module Formulae baseline" claim after edit → caught by `grep "Module Formulae" arcanum/spells/invoke/{SKILL.md,define.md}`.
- **Validation:** `invoke define` dry-run on a sample feature emits a DomainSpec SPEC + aspect docs referencing canonical IDs; grep shows no baseline claim on Module Formulae.

## Smallest Working Units
- **SWU-KSL-004** — repoint baseline + update SKILL/define text (write scope: `arcanum/spells/invoke/{SKILL.md,define.md}` + mirror). Owner: local-fallback (governance text).
- **SWU-KSL-005** — add discovery soft gate + waiver writeback (write scope: `arcanum/spells/invoke/define.md`). Owner: local-fallback.

## Handoff Note
Spell-lifecycle change → `spellcraft` owns validation/observation. Submodule-first.
