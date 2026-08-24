# Refine Seed Proposal

- Target: the two final non-vacuity defects in the closed Anime.js agent knowledge-vault research dispatch
- Seed needed: `yes`
- Desired outcome: a falsifiable definition/design and non-executed repair plan that can support a newly authorized ontology route
- Preset: `standard`
- Research: `no-research`
- Loop count: canonical ten-stage Refine loop, budget tuned by the standard preset
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: `pass`
- Runtime default: parent-owned native skills
- Runtime eligibility: `blocked pending operator confirmation`
- Write scope: `projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/`

## Source Context

The following inputs are immutable evidence for this run:

- `projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/receipts/evidence-closure.json`
- `projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/receipts/reviewer-non-vacuity-final.json`
- `projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/receipts/knowledge-vault-synthesis-reviewer-repair.json`
- `projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/CLOSEOUT.json`

The prior research dispatch is closed with `loop_ceiling_reached`. Refine may
consume its evidence but may not rewrite the verdict, resume the dispatch, or
materialize the candidate ontology.

## Defects To Refine

### D1 — QRY-003 abstention vocabulary mismatch

The QRY-003 tie path emits `ABSTAIN_AMBIGUOUS_CHOICE`; the closed vocabulary
declares `ABSTAIN_AMBIGUOUS_INTENT`. The refined contract must select exactly
one of these approaches:

1. normalize the emitter to the existing code; or
2. add a distinct code with invariant, trigger, clearing criterion, migration,
   and fixtures.

Every terminal QRY-003 path must emit either a declared code or a positive
result. No synonym or undeclared fallback is admissible.

### D2 — Decorative relation consumer not disproved

A non-empty consumer declaration is not behavioral evidence. For every
retained relation, the refined design must name:

- a finite input fixture;
- the baseline graph/query/validator output;
- one removal or property-change mutant;
- the consumer observing the change;
- the expected retrieval, explanation, diagnosis, validation, invalidation,
  abstention, or next-action delta;
- the disposition when no delta exists: `KILL`, `MERGE`, or `DEFER`.

## Done Criteria

The Refine result is eligible for `pass` only when:

1. the canonical ten-stage loop has native receipts or an explicit blocker for
   every stage;
2. one closed QRY-003 code contract covers ties, conflicts, unknowns,
   performance claims, and clearing criteria;
3. every retained relation has a behavior-changing mutation witness or a
   non-retention disposition;
4. the repair design includes finite positive and negative fixtures that would
   have killed both surviving mutants;
5. Invoke Plan produces a non-executed, bounded repair plan with exact targets,
   validation commands, rollback, and owner handoff;
6. final Interrogation returns `pass` without implying research closure,
   ontology admission, publication, promotion, release, deployment, or
   production readiness.

## Validation Surface

- `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py /home/vrondelli/projects/domainspec-core/projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/REFINE-DISPATCH.json`
- JSON parse for `REFINE-DISPATCH.json` and `evidence-index.json`
- exact source-path existence checks
- stage artifact/blocked-reason completeness against `RUN-MANIFEST.md`
- QRY-003 output-code closed-set fixture matrix
- per-relation baseline-versus-mutant delta matrix
- scoped `git diff --check`

## Selected Technique Overlays

- `baseline_sequence`: preserves the canonical stage and receipt chain.
- `dialectic_for_tension`: tests normalize-versus-add-code alternatives and
  declared-consumer-versus-proven-consumer semantics without smoothing over
  disagreement.
- `toy_game_for_low_cost_falsification`: requires the two surviving mutants to
  fail in a finite fixture before planning can pass.

Considered but not selected:

- `route_menu_for_ambiguity`: the route is now exact; the bounded choice is
  inside the repair design, not the runtime route.
- `tournament_for_alternatives`: Distill already compares the two code repair
  alternatives; a separate overlay would add machinery without another route.
- `xray_for_hidden_structure`: the two hidden structures are already named by
  final reviewer evidence.
- `memory_residue_for_context_recovery`: direct closed receipts, rather than
  reconstructed memory, are the authority for the defects.
- `protected_context_for_external_or_sensitive_evidence`: no external research
  or sensitive corpus is authorized.

## Planned Execution Stages

1. Context Builder creates a strict pack from the four closed evidence inputs.
2. Invoke Define specifies D1 and D2 as closed falsification obligations.
3. Interrogation `refine-review` attacks underspecification with the two
   approved reviewer receipts.
4. Refine records `no-research` and blocks external browsing.
5. Distill selects the smallest coherent repair unit and rejected alternatives.
6. Invoke Design defines the query contract and relation-witness schema.
7. Interrogation `refine-design-review` attacks every terminal path and relation
   row.
8. Distill Repair runs the finite toy mutations and writes the relation witness
   matrix.
9. Invoke Plan writes the non-executed repair plan.
10. Final Interrogation and Refine synthesis decide `pass`, `flag`, or `block`.

## Proposed Subagents

- `query-contract-critic`: read-only; owns QRY-003 closed-code falsification.
- `relation-witness-falsifier`: read-only; owns the 25-row mutation matrix and
  inert-relation dispositions.

Both are advisory inputs to native Interrogation/Distill stages. The parent
joins all receipts and retains final synthesis ownership. Before spawning, the
pair must be normalized into the repository's governed subagent sheet and pass
readiness, tension, registration, join, and closeout requirements. This Refine
confirmation may be carried only when deterministic material equivalence is
proved; otherwise execution blocks for a new decision rather than silently
changing the strategy.

## Deferred Work

- edits to the closed research package;
- creation or mutation of `projects/animejs/ontology/agent-knowledge-vault/`;
- a new governed research or ontology-vault dispatch;
- publication, promotion, release, deployment, or production use.
