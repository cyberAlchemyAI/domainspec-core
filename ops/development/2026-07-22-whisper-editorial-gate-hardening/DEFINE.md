# Define: Whisper Editorial Gate Hardening

## Purpose

Make Whisper incapable of reporting editorial readiness from structural evidence alone. A run must expose what text was reviewed, who or what checked each evidence axis, what state the author intent is in, and the rule that limits the final status.

## Problem statement

Whisper currently contains useful prose rules for intent convergence, candidate transports, auditions, and human approval. The run surface and validator do not enforce those rules as a coherent state machine. As a result:

- a structurally valid artifact can be labeled plain-language `pass`;
- an approval for a plan or edit can be misread as approval of the language itself;
- a meaning-changing correction can be followed by another full derivative instead of a small re-audition;
- a conditional retell can become duplicate rendered content;
- proposed phrases can pass while the composed first surface remains expert-facing;
- a rejected prior `pass` is not represented as a false-positive correction event;
- a generated native package can carry a local preset that blind regeneration would erase.

## Capability boundary

The adjustment owns four behaviors:

1. **Evidence separation** — record structural validation, editorial audition, comprehension, and render/runtime validation independently.
2. **State and status enforcement** — compute generation permission and final status ceilings from typed run evidence.
3. **Surface-bound human gates** — bind approvals, comprehension, and post-apply review to the exact composed surface.
4. **Safe packaging** — keep generic Whisper changes public, private integration witnesses private, and repository-local presets outside generated canonical bodies.

It does not own:

- automatic semantic scoring or claims that a machine understands prose;
- browser layout, accessibility, or visual-design validation;
- promotion of a candidate transport;
- changes to Distill, Structured Interview Kits, Workflow Reflect, or Signal Observer internals;
- rewriting the BTE X-Ray as part of this Invoke run;
- a general bootstrap overlay-merging system.

## Required outcomes

| ID | Outcome | Acceptance boundary |
| --- | --- | --- |
| WEG-R1 | A typed run receipt separates the four evidence axes. | Structural or render success cannot fill editorial or comprehension fields. |
| WEG-R2 | A deterministic evaluator computes pre-generation permission and final status ceiling. | Red fixtures for volatile intent, candidate `pass`, missing comprehension, and digest mismatch cannot pass. |
| WEG-R3 | Editorial approval is explicit and surface-bound. | An ambient `confirmed` or `apply approved` record without approval kind and matching digests is rejected. |
| WEG-R4 | Newcomer explainers audition the composed first surface. | The manifest contains the whole required opening role set in reading order, not isolated phrases. |
| WEG-R5 | Comprehension is human evidence with a machine-checkable envelope. | Required question IDs, reviewer, outcome, and matching surface digest exist; tooling does not score answer semantics. |
| WEG-R6 | Post-apply editorial verification is a separate stage. | A final artifact cannot inherit the pre-apply audition result without a post-apply review record. |
| WEG-R7 | Corrections invalidate false-positive readiness. | A meaning-core correction appends an event, marks intent volatile, and prevents continued `pass`. |
| WEG-R8 | Retell and added-surface behavior are explicit. | Rendered retell requires a distinct audience job plus replacement mapping; added blocks name what they replace or why they are distinct. |
| WEG-R9 | Reusable validation proves the gates on low, medium, and complex examples. | Experiment Harness has red and green regimes and records causal pass/fail evidence. |
| WEG-R10 | Canonical, generated, and local runtime state do not overwrite one another. | Generated Whisper derives from public canonical source; local preset resolves from `.arcanum/spells/whisper/presets/`. |

## Source contracts

| ID | Source | Selector or role | Authority in this package |
| --- | --- | --- | --- |
| SC-01 | `arcanum/spells/whisper/README.md` | phases, candidate transport ceiling, intent convergence, delivery flow, retell, approval, observability | Canonical public Whisper contract. |
| SC-02 | `arcanum/spells/whisper/tools/validate-whisper-draft.py` | current conservative document checks | Existing executable baseline; not editorial proof. |
| SC-03 | `.arcanum/observability/reflections/20260722T054438Z-whisper-reflection.md` | newcomer gate, first-surface order, evidence-axis split | Accepted evidence and proposed iteration; not canonical spell authority. |
| SC-04 | `.arcanum/observability/reflections/20260717T130820Z-whisper-concision-reading-flow-maintenance-report.md` | intent state and delivery-flow maintenance | Applied historical evidence and explicit deferred gaps. |
| SC-05 | `.arcanum/inventory/entries/whisper-concision-reading-flow-maintenance-review-strategy-result-synthesis.md` | public/private boundary and local preset residue | Verified non-authority read model. |
| SC-06 | `.agents/skills/whisper/SKILL.md` | generated runtime plus repository-local divergence | Generated surface; never canonical authority. |
| SC-07 | `projects/domainspec-v2/development/first-production-release/backend-type-test-engine-completeness/x-ray/2026-07-21-implementation-architecture/` | private complex integration witness | Private validation input only; forbidden from public fixture text. |

## Proof model

The final status is not the sum of successful checks. It is the requested status limited by the strictest applicable gate:

```text
final_status = stricter_of(requested_status, computed_status_ceiling)
```

where `block < flag < pass`. A successful structural or browser check can satisfy only its own axis; it cannot raise the editorial ceiling.

## Discovery and template selection

- Discovery artifacts found: SC-03, SC-04, SC-05, and the private BTE correction trail.
- Define template: candidate `invoke.spell`, selected because the target is an existing spell revision and the artifact must hand off to Spellcraft.
- Design template: candidate `invoke.architecture`, selected because the adjustment needs explicit source contracts and six views.
- Plan templates: standalone implementation layering, standalone split work pack, and DomainSpec execution-pack wave structure.
- Candidate status is retained. This run does not promote Invoke templates.

## Define gate

- Status: `pass`
- Reason: target, outcomes, non-goals, source contracts, ownership, privacy boundary, and proof semantics are explicit. No blocker decision remains for design.
