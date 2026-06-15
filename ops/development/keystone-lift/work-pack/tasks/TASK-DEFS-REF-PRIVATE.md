---
module: keystone-lift
task: TASK-DEFS-REF-PRIVATE
docType: work-pack-task
updatedAt: 2026-06-14
---

# TASK-DEFS-REF-PRIVATE — Rewrite private DS DEFINITIONS.md to reference arcanum; keep moat private

Layer: L2 · Wave: W2 · Complexity: medium · Gate: ready-after S-001

## Objective
After the wedge subset is canonical in arcanum, update the private `implementation/domainspec` normative `DEFINITIONS.md` so wedge terms **reference** arcanum (no duplicate copy), the moat cluster stays canonical and private, and the ambiguous cluster stays private by default.

## Dependencies
S-001 (arcanum canonical wedge exists). Targets `research/projects/domainspec/definitions/DEFINITIONS.md` (private).

## Implementation Detail Spec
- **Inputs:** the now-canonical arcanum wedge IDs; the existing private DEFINITIONS.md.
- **Outputs:** edited private DEFINITIONS.md.
- **Ordered rules:**
  1. For each wedge ID (DS-D1/D2/D3/D7/D8/D10/P1-3): replace the inline definition body with a reference pointer to the arcanum canonical entry (keep the ID + a one-line stub so internal DS links still resolve).
  2. Keep moat cluster (DS-C3/D9/COR-1/F1/F5/F6/M13) bodies fully intact and private.
  3. Keep DS-D4/D5/D6 private and unchanged (decision C3); add a note: "held private pending decoupling review."
  4. Update DS-side indexes (DEFINITIONS-INDEX, TRACEABILITY-MATRIX) to point wedge IDs at arcanum.
  5. Record that DS now depends on the arcanum submodule for wedge vocabulary.
- **Edge cases:** a private moat definition cites a wedge ID → cite the arcanum reference (one-directional dependency is fine; private→public is allowed).
- **Failure modes:** broken internal DS links after stubbing → run DS link check.
- **Validation:** DS wedge references resolve to arcanum; moat cluster present + private; DS link check green.

## Smallest Working Units
- **SWU-KSL-006** — rewrite wedge entries as references; retain moat/ambiguous (write scope: `research/projects/domainspec/definitions/`). Owner: subagent. Verify: refs resolve + moat-grep present.

## Handoff Note
Private-repo edit. Must run AFTER the moat-leak audit confirms the arcanum side is clean. Submodule-first within domainspec.
