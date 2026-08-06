# OpenAI Speech Contract Snapshot

Retrieved from official OpenAI documentation on 2026-08-04. This is a planning snapshot, not a provider availability or account-entitlement receipt.

## Official sources

- [Text to speech guide](https://developers.openai.com/api/docs/guides/text-to-speech)
- [GPT-4o mini TTS model](https://developers.openai.com/api/docs/models/gpt-4o-mini-tts)
- [Create speech API](https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create)

## Observed interface

| Surface | Observed contract |
|---|---|
| Endpoint | `POST /v1/audio/speech` with JSON input; successful non-SSE response is binary audio. |
| Model family | `gpt-4o-mini-tts`; current documented snapshot `gpt-4o-mini-tts-2025-12-15`. |
| Input limit | Maximum 2,000 input tokens on the model page. The exact frozen-excerpt token count remains unmeasured. |
| Required request concepts | `model`, `voice`, and `input`. |
| Delivery control | `instructions` can prompt accent, emotional range, intonation, impressions, speed, tone, and whispering. |
| Output | MP3 default; supported formats include Opus, AAC, FLAC, WAV, and PCM. WAV or PCM is recommended for fastest response. Raw PCM is documented as 24 kHz, 16-bit signed little-endian without a header. |
| Disclosure | End users must receive a clear disclosure that the voice is AI-generated and not human. |
| Built-in voices | Current voice-options section lists `alloy`, `ash`, `ballad`, `coral`, `echo`, `fable`, `nova`, `onyx`, `sage`, `shimmer`, `verse`, `marin`, and `cedar`; it recommends `marin` or `cedar` for best quality. |

## Conflict and non-observations

- The guide introduction says 11 built-in voices while its voice-options section lists 13. The audition must bind an exact tested voice ID, never a voice count.
- No cited route establishes a native pronunciation dictionary, phoneme override, speech timestamps, deterministic seed, or numeric pitch/gain control for this model.
- The documentation does not establish the selected account's public-use rights, applicable agreement, retention configuration, region, billed cost, or current endpoint entitlement.
- Documentation is not audible evidence. It establishes no naturalness, warmth, pacing, accent fit, pronunciation quality, or winner.

## Planned request posture

- Use one stock voice only; custom and cloned voices are prohibited.
- Prefer the dated snapshot over an alias when later account availability is verified.
- Send the entire frozen excerpt in one request.
- Use `response_format: "wav"`; do not stream for the audition master.
- Use the approved non-spoken delivery instruction verbatim when `instructions` remains supported.
- Omit undocumented controls rather than inventing defaults.
- If the first unchanged-text take mispronounces “Body War,” reject the configuration; do not alter the spoken text or invent a pronunciation parameter.
