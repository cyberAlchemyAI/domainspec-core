# Shared Execution Context

## Required sources

- `../../SPEC.md` and aspect docs: semantic and behavioral contract.
- `../../DESIGN.md`: selected architecture and enforcement placement.
- `../../IMPLEMENTATION-DETAILS.md`: algorithms, runtime posture, edge cases.
- `../../VALIDATION-CONTRACTS.md`: planned positive and negative witnesses.
- `../../OPENAI-SPEECH-CONTRACT.md`: current provider documentation snapshot.
- `../../audition-excerpt.txt`: exact 237-word input.

## Fixed boundaries

- Node `v22.12.0`; built-ins first; no new package root.
- No credential in code, config, fixture, artifact, log, digest, or receipt.
- Only SWU-OAIA-003 may later perform a provider call, after separate authorization.
- Custom/cloned voices, chunking, automatic retry, overwrite, text repair, automatic voice selection, full narration, publication, and deployment are excluded.
- Every success receipt is bound to one manifest digest and one declared transition.

## Worker return shape

```yaml
swu_id: SWU-OAIA-NNN
result: pass | flag | block | interrupted
files_touched: []
validation: []
blockers: []
handoff_note: summary for coordinator
```
