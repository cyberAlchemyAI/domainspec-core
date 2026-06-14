---
module: keystone-lift
task: TASK-MF-REMOVE
docType: work-pack-task
updatedAt: 2026-06-14
---

# TASK-MF-REMOVE — Remove the Module Formulae template family + update references

Layer: L3 · Wave: W3 · Complexity: medium · Gate: ready-after S-003,S-005

## Objective
Complete the full replacement (decision B1): delete `module-formulae/` and update every live reference so the DomainSpec template is invoke's sole `define` baseline.

## Dependencies
S-003 (cutover done), S-005 (moat-leak audit green). Targets `arcanum/spells/invoke/templates/module-formulae/` + reference sites.

## Implementation Detail Spec
- **Inputs:** confirmed-working DomainSpec baseline; the grep list of "Module Formulae" references (dev/craft docs, invoke contract text, any compose profiles).
- **Outputs:** removed template dir; updated references.
- **Ordered rules:**
  1. Re-grep `module-formulae|Module Formulae` across arcanum (exclude runtime logs / observability).
  2. For each live doc reference (craft architecture, invoke dev docs, design/plan/full compose profiles): repoint to `domainspec-spec/` or remove if obsolete.
  3. Delete `templates/module-formulae/`.
  4. Confirm no mode contract still composes Module Formulae.
- **Edge cases:** a non-`define` mode (design/plan/full) composed Module Formulae → repoint to the DomainSpec family or record a follow-up if that mode needs its own template work (flag, don't silently break).
- **Failure modes:** dangling reference → final grep must return only historical/log hits.
- **Validation:** `grep -rE 'module-formulae|Module Formulae' arcanum --exclude-dir=.arcanum` → 0 live doc hits; invoke `define` still works.

## Smallest Working Units
- **SWU-KSL-008** — delete family + repoint refs (write scope: `arcanum/spells/invoke/templates/module-formulae/` + ref docs). Owner: local-fallback. Verify: grep clean + define dry-run.

## Handoff Note
Last mutating wave. Submodule-first push only after TASK-VERIFY. Run the whole-diff moat-leak audit one final time before push.
