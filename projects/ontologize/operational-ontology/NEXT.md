# NEXT — operational-ontology research

Route `operational-ontology-research-20260612` executed end-to-end 2026-06-12 (all 9 steps,
fanout approved). This file is the ordered roadmap + the governance handoff (step
`prepare-next-handoff`).

## Ordered next actions

1. **Ontology-harness branch-acceptance review** (R1) — present the candidate `B-op` branch seed and
   node schema; decide accept / revise / reject as an operational branch. Owner: ontology-harness.
2. **Draft first operational axiom + constitution candidates** (R2) — e.g. axiom "docs/contract before
   execution"; constitution "every delegated route must carry a closeout receipt". Route through
   PromotionRecord. Owner: Constitution Governance. Run the circular-authority check (R3).
3. **Envelope-aware telemetry derivation** (R-T1) — build the derivation that reads `envelopes/` to
   populate candidate `invocation` / `workflow_gap` nodes with real outcome fields.
4. **Instrument new mutations** (R-G1) — add `discipline_hardened` / `lesson_promoted` envelope fields
   so those mutation types become observable rather than hypothetical.
5. **Broaden per-project observability** (R-T2) so the operational branch samples domainspec-core
   operation, not just the arcanum subrepo.

## Governance handoff — `operational-ontology-review-handoff`

- **From:** ontologize / operational-ontology research (candidate artifacts only).
- **To:** **ontology-harness** (branch acceptance) + **Constitution Governance** (apex promotion).
- **Asserts:** the operational branch is structurally seedable today; its highest knowledge category
  is an operational constitution/axiom set; `DISCIPLINES.md` feeds that set and is not the apex.
- **Asks:** (a) accept/revise `B-op` as a branch; (b) decide whether to draft the first operational
  axiom/constitution candidates via PromotionRecord.
- **Carries:** [decisions/disciplines-as-axiom.md](decisions/disciplines-as-axiom.md),
  [CARRY-SET.md](CARRY-SET.md), [branch/operational-branch-seed.md](branch/operational-branch-seed.md),
  [branch/operational-node.schema.yml](branch/operational-node.schema.yml),
  [residue/open-residue.md](residue/open-residue.md).
- **Guardrail:** no promotion to ontology/constitution/axiom authority without the owners above.
- **Authorization:** branch acceptance and any promotion **require owner review** — not granted here.
