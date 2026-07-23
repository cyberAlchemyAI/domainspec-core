# S2 Spellcraft Acceptance — Whisper Editorial Gate Hardening

## Spellcraft Result

- Mode: `design`
- Mutation mode: `proposal-only`
- Spell: `whisper`
- Canonical ID: `whisper`
- Alias used: none
- Scope: library
- Spell file: `arcanum/spells/whisper/README.md`
- Invoke handoff: `../../../SPELLCRAFT-HANDOFF.md`
- Design source: `../../../DESIGN.md`
- Work pack: `../../../WORK-PACK.md`
- Sigils referenced: `structured-interview-kits`, `distill`, `experiment-harness`, `signal-observer`, `workflow-reflect`
- Proposed phases: 8
- Current canonical phases: 7
- Lifecycle acceptance: `pass`
- Structural/lifecycle validation: `flag`
- Observability: configured in the design and canonical spell
- Next action: Task Session may execute `SWU-WEG-001` after rebuilding context from current digests

## Owner acceptance decision

Spellcraft accepts:

1. The objective: prevent structural evidence from self-certifying editorial readiness.
2. The owner split: humans judge language/comprehension; deterministic tools enforce evidence shape, digest binding, state transitions, and status ceilings.
3. Separate pre-generation permission and final-status decisions.
4. Candidate transport status capped at `flag` without separate promotion evidence.
5. The eight-phase target composition in the Invoke handoff.
6. The public/private boundary: generic contracts and fixtures may enter public Arcanum; BTE prose remains a private integration witness.
7. `SWU-WEG-001` as the first reversible lifecycle unit.

This receipt satisfies dispatch decision `S2.spellcraft-acceptance` and W0's owner-entry gate. It does not claim that the revision is implemented or validated.

## Phase and gate review

| Proposed phase | Inputs/outputs | Gate | Failure behavior source | Review |
| --- | --- | --- | --- | --- |
| 1. Intake and state | target, audience, transport, corrections → intent state | volatile permits bounded artifacts only | Design correction reducer and compensation rules | accepted |
| 2. Composition plan | state and selected candidate → surface/change plan | every visible block has one job | Design change-manifest rules | accepted |
| 3. Surface assembly | plan/selectors → ordered manifest/digests | required roles complete | invalid/incomplete manifest blocks evidence binding | accepted |
| 4. Editorial audition | exact manifest → approval/comprehension | evidence binds current digests | mismatch rejects evidence | accepted |
| 5. Pre-generation admission | run receipt → allow/block | state, approval, surface ownership | fail-closed generation algorithm | accepted |
| 6. Draft/application | admitted plan → applied artifact/render evidence | evidence axes stay separate | machine results cannot raise editorial status | accepted |
| 7. Post-apply verification | applied digest → human review | review binds applied artifact | missing/prior-digest review caps status | accepted |
| 8. Correction/observation | response/prior receipt → event/state/signal | false-positive readiness invalidates current pass | append-before-project and reflect route | accepted |

## Validation flag

The following reusable-spell evidence is intentionally pending:

- `arcanum/spells/whisper/development/VALIDATION-EXPERIMENT.md` is absent.
- `arcanum/spells/whisper/development/VALIDATION.md` is absent.
- The typed run-receipt schemas and evaluator are unimplemented.

Ownership and repair:

- `SWU-WEG-001` initializes the generic Experiment Harness definition, red/green fixtures, and honest `not-enforced` baseline.
- Later SWUs implement schemas and evaluators.
- `TASK-WEG-VERIFY` creates the final validation report and returns promotion residue.

These gaps block lifecycle validation/promotion, not design acceptance or fixture-baseline work.

## Conditions on SWU-WEG-001

- Write only its three declared public development surfaces.
- Do not edit canonical `README.md`, schemas, tools, or generated runtime.
- Use product-neutral fixtures; a non-empty private-language sweep blocks completion.
- Record missing enforcement as `not-enforced`, never as implementation pass/fail.
- Return one Task Session receipt before work-pack state synchronization.

## Gate result

- S2 owner decision: `pass`
- Reusable-behavior validation: `flag`, expected and owned
- Promotion readiness: `block`, not in scope
- Returned next route: `task-session:execute` target `SWU-WEG-001`
