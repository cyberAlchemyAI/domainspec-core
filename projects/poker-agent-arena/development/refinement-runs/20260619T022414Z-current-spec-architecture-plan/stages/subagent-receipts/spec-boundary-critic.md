# Spec Boundary Critic Receipt

Agent ID: `019eddbc-1c03-7950-a72f-8dab9b459683`
Role ID: `spec-boundary-critic`
Status: `flag`

## Artifacts Reviewed

- `projects/poker-agent-arena/SPEC.md`
- `projects/poker-agent-arena/GLOSSARY.md`
- `projects/poker-agent-arena/INVOKE-RESULT.md`
- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/`

## Findings

| Severity | File | Evidence | Proposed Fix |
| --- | --- | --- | --- |
| MAJOR | `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/LANE-MAP.md` | Says "No subagents have been spawned," while `INVOKE-RESULT.md` consumes `subagent-run/findings.md`, `research.md`, and `REVIEW-REPAIR.md` as inputs. | Add or update an execution manifest that distinguishes route-preview validation from approved subagent execution, with spawn/join/close receipts and the approval boundary. |
| MAJOR | `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/findings.md` | Scoring says "Rank MVP agents by adjusted cash EV... `ev_lcb95`" and later adds risk/adaptation diagnostics, despite the current spec limiting M0 to raw toy EV plus diagnostics. | Reclassify adjusted EV, `ev_lcb95`, risk, and adaptation to M2/follow-up gates; keep M0 wording to raw chip EV, timeout rate, invalid-decision rate, and replay determinism only. |
| MAJOR | `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/receipts/toy-game-validator.md` | Transcript schema says freeze fields including `seed`; this is not qualified as referee-only/redacted, even though live seed visibility is forbidden elsewhere. | Split referee transcript from public/agent replay schema; use `seed_handle` or `seed_commitment` for exported replay and mark raw seed material referee-only. |
| MINOR | `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/receipts/agent-protocol.md` | Example IDs `h-000042` and `h-000042:s2:a7` are structured/predictive, while the repaired handoff requires agent-visible IDs to be opaque and non-predictive. | Replace examples with opaque IDs and keep seat/turn information in explicit allowlisted fields, not embedded identifiers. |

## Residue

The top-level spec mostly survives: it names hidden-information gates, owner non-goals, toy-first M0, engine-parity M1, and blocked composite scoring. Remaining risk is drift between repaired top-level artifacts and older lane receipts.

## Next Route Recommendation

Run a boundary cleanup before `SWU-PAA-001`: align dispatch provenance, redact seed terminology, and demote adjusted scoring/adaptation language out of M0.
