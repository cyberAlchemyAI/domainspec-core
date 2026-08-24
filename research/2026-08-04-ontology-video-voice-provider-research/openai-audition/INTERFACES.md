# Interfaces: OpenAI Stock-Voice Audition

## External: OpenAI Speech API

### POST `/v1/audio/speech`

**Exposes:** `RenderCandidate`  
**Auth:** Bearer credential supplied only through the process environment at execution time

### Planned request projection

| Field | Type | Maps to |
|---|---|---|
| model | string | AuditionManifest.model_snapshot |
| voice | string | AuditionManifest.voice_id |
| input | string | FrozenExcerpt.exact_text |
| instructions | string | AuditionManifest.instructions |
| response_format | enum | AuditionManifest.response_format (`wav`) |

### Responses

| Condition | Handling |
|---|---|
| Binary success | Stream to a new temporary file, fsync/close, hash, then atomically bind it to a unique run path. |
| SSE response | Reject; not selected by this audition contract. |
| Non-success or timeout | Preserve redacted status/IDs where available; do not claim a RenderAttempt. |
| Ambiguous or undocumented response | Fail closed. |

No authorization header, API key, or raw error body containing secret material may be persisted.

## Internal: local audition runner

| Command surface | Maps to | Side effect class |
|---|---|---|
| `prepare` | FreezeManifest + InspectManifest | Repository-local planning/runtime artifacts only; no network. |
| `render` | RenderCandidate | External metered provider effect; separately admitted. |
| `verify` | VerifyCandidate | Local evidence production. |
| `blind` | BlindCandidate | Local evidence production. |
| `decide` | RecordOperatorDecision | Human-owned decision record; no publication. |

Command names are planned interfaces, not implemented commands.
