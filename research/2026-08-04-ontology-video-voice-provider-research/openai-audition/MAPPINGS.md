# Mappings: OpenAI Stock-Voice Audition

## ManifestToSpeechRequest

**From:** AuditionManifest  
**To:** OpenAI Create Speech JSON  
**Direction:** outbound

| Source field | Target field | Transform | Notes |
|---|---|---|---|
| model_snapshot | model | direct | Dated snapshot preferred; verify account availability before admission. |
| voice_id | voice | direct | One exact documented stock voice. |
| excerpt_path + excerpt_sha256 | input | read exact UTF-8 bytes after digest verification | No headings, edits, chunking, or markup. |
| instructions | instructions | direct | Non-spoken delivery instruction. |
| response_format | response_format | direct | Fixed to `wav`. |
| provider endpoint | none | transport configuration | Fixed `/v1/audio/speech`; not serialized in body. |
| credential | Authorization header | runtime-only | Never part of manifest or mapping output. |

### Validation

| Field | Validation | On failure |
|---|---|---|
| input | SHA-256 and exact count match | Block before network. |
| model | Equals admitted dated snapshot | Block before network. |
| voice | Equals admitted stock voice ID | Block before network. |
| instructions | Byte-equal to frozen instruction | Block before network. |
| request keys | No undocumented or secret-shaped fields | Block before network. |

## RawResponseToAttempt

| Source | Target | Transform |
|---|---|---|
| response byte stream | raw audio file | Unique temp file followed by atomic binding; no overwrite. |
| response/request IDs | attempt metadata | Redacted direct mapping where available. |
| UTC start/end | attempt metadata | Monotonic duration plus wall-clock timestamps. |
| raw bytes | sha256 | SHA-256 after closed write. |

## AttemptToBlindAsset

| Source | Target | Transform |
|---|---|---|
| accepted derivative | opaque asset | Copy/reference under random UUID label. |
| candidate + repetition | unblinding key | Deterministic protected mapping. |
| listener assignment | listener-order manifest | Balanced order with candidate repetitions separated. |
