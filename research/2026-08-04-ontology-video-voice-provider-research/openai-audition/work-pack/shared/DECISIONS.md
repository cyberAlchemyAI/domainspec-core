# Cross-task Decisions

## Fixed by this Plan

| Decision | Value | Basis |
|---|---|---|
| Runtime | Node.js 22.12.0, ESM, built-ins | Current repository runtime; no dependency root needed for L0/L1. |
| Provider route | `POST /v1/audio/speech` | Current official docs. |
| Planned model | `gpt-4o-mini-tts-2025-12-15` | Current documented snapshot; later availability must be verified. |
| Format | non-streaming WAV | Lossless audition master and documented route. |
| Candidate count | one exact stock voice/configuration | Prior fixed protocol. |
| Repetitions | two identical settings | Prior fixed protocol. |
| Initial state | `not_ready` | Open hard gates. |
| First executable unit | SWU-OAIA-001 | Narrowest reversible offline trust step. |
| Selected unit | none | Invoke authoring does not implement. |

## Owner decisions still required

Accent/locale, exact voice, production operator, actual-account rights/data gates, verification tools, listener operations, and any later production route remain unset. `marin` and `cedar` are candidates to hear because the provider currently recommends them; neither is selected.
