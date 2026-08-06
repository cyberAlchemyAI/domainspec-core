
## Boundary and decision states

Evidence was retrieved on **2026-08-04 UTC** and joined from:

- `TC/spawn-0001`: technical-capability explorer
- `RP/spawn-0002`: rights/privacy explorer
- `PA/spawn-0003`: production-audition explorer

Decision cells use only these states:

- **observed** — the explorer retrieved the cited first-party page and found the bounded claim at the named selector;
- **unknown** — required evidence or a required qualifier is absent, unavailable, incomplete, or not bound to the actual provider route/account;
- **conflicting** — cited first-party or explorer evidence supports materially incompatible propositions that have not been reconciled;
- **not applicable** — the protocol excludes the category, with the exclusion stated explicitly.

The source register retains the explorers’ proof word `unverified`; for decision purposes it normalizes to **unknown**, never permission. Nothing provider-facing was executed: no account, terms acceptance, purchase, credentials, upload, API call, audio generation, cloning, or listening test occurred.

This is a desk-research diligence aid, not provider approval, render admission, or a voice-quality ranking.

## Owned narration contract and precedent boundary

The build-from-owned contract is: the exact approved **English** script; one reflective solo narrator; thoughtful-investigation delivery; 120–130 words per minute; natural breaths; and no keynote or advertising delivery. Provider, stock-voice identity, accent/locale, gender presentation, cloning, and production platform remain owner-unset. No deployed narration or accepted waveform exists.

Before any account action, upload, or render, the owner must either select one common audition accent/locale or explicitly approve provider-native accent variation. If `en-US` is later chosen as an experimental control, it must be labeled test-only and not inherited owner approval.

Prior Runway handoffs and “selected voice model” language belong to other unrendered artifacts. They do not establish a narration provider, platform, accent, locale, or accepted voice for this video.

## Hard requirements

| Gate | Required witness | Current state |
|---|---|---|
| Owned narration contract | Exact English script and owned delivery constraints above; separate pre-render owner decision for accent/locale | **observed** locally; accent/locale decision **unknown** |
| TTS availability | Official documentation for the exact provider/model route | Provider-specific states below; availability alone does not establish suitability |
| Exact fixed-excerpt suitability | Whole 237-word excerpt in one request; route-specific limit; lossless master; complete candidate manifest | **unknown** for every provider until a complete manifest is bound |
| Provider manifest | Provider/entity, endpoint/method, model/version state, stock-voice ID/version, spoken language, owner-selected accent/locale, provider voice accent/locale, region/location, account tier, client/version, native output enum/rate/depth/channels, exact excerpt byte/token count versus limit, and complete redacted request | **unknown** for every provider; therefore every `audition_admission` is `not_ready` |
| Master format | At least 24 kHz, 16-bit mono lossless output on the selected route | Documentation is **observed** for some routes; exact configured-route witness is **unknown** |
| Independent text fidelity | Forced alignment for timing plus independent transcription or token-by-token listening audit; explicit mismatch and low-confidence review rules | **unknown** until tools, versions, commands, tolerances, and audit owner are frozen |
| Generated-output ownership/assignment | Actual agreement establishes title or assignment for generated audio | Independent provider states below; never satisfied by use permission |
| Commercial/public-use permission | Actual entity, agreement, plan, stock-voice license, attribution/disclosure, and public educational-video use | **unknown** for every actual account/voice configuration |
| Privacy/data use | Training, human review, safety logging, benchmarking, support access, and pre-upload controls | Independent provider states below; missing controls are **unknown** |
| Retention/deletion | Ordinary, backup, abuse-log, support, and post-termination retention plus deletion mechanics/proof | Independent provider states below; missing periods are **unknown** |
| Security/enterprise controls | Applicable DPA, security terms, audit evidence, region, subprocessors, and account scope | Independent provider states below; security does not imply privacy or retention |
| Custom/cloned voice availability | The audition prohibits custom and cloned voices | **not applicable — prohibited by protocol** |
| Cloning authorization | Speaker identity, consent, revocation, and model deletion | **not applicable — prohibited by protocol**; cloning sources remain exclusion context only |
| Documented usage-price estimate | Time-scoped list-price arithmetic using the frozen assumptions | **observed as of 2026-08-04** where sourced; not a bill or total cost |
| Total production cost | Plan minimums, eligibility, retakes, alignment, timing calls, storage/egress, labor, taxes, and actual billed units | **unknown** for every provider until execution and operator cost accounting |
| Quality claim | Comparable rendered waveforms, blinded listeners, locked score sheets, and unblinding key | **unknown**; no audio or listening evidence exists |
| Operator decision | Named production operator/owner explicitly records `approve`, `reject`, or `defer` after listening and any required longer prototype | Decision role required; named individual **unknown**; scores cannot auto-select |

## Eight-provider technical and financial matrix

Every usage figure below is a **documented usage-price estimate as observed 2026-08-04** under the explorers’ stated assumptions. Effective/revision date, provider entity, jurisdiction, actual plan/account, region, currency, taxes, eligibility, and agreement remain **unknown** wherever the source binding does not state them. Total production cost is **unknown for every provider**.

| Provider | Documented TTS availability | Exact fixed-excerpt suitability | Documented usage-price estimate as observed 2026-08-04 | `audition_admission` |
|---|---|---|---|---|
| **OpenAI** — `gpt-4o-mini-tts`; fallback family reported as `tts-1`/`tts-1-hd` | **observed** — prompted delivery and WAV/PCM are documented. Model lifecycle and 11-versus-13 voice evidence are **conflicting**. | **unknown** — exact excerpt count, model/version, stock voice, request body, and complete manifest are not frozen; native pronunciation/timing support was not found. | **observed** — `gpt-4o-mini-tts` $0.60/M text-input tokens + $12/M audio-output tokens. Conversion is **unknown**. The reported `tts-1` $15/M-character rate lacks a specific source-page binding and is **unknown** for decision use. | `not_ready` — technical manifest and account-specific legal/data gates remain unknown. `[FEEDBACK-TC/RP]` |
| **ElevenLabs** — Multilingual v2 / Eleven v3 / Flash v2.5 | **observed** — alignment, pronunciation, continuity, and lossless-format surfaces are documented; seed is best-effort. | **unknown** — exact manifest and actual-plan lossless route are not frozen; current data gates also fail. | **observed** — about 9,258 Multilingual-v2 credits; Flash about 4,629–9,258 credits; Free 10k credits; Starter $6/month/30k credits. | `not_ready` — reviewed click-through data posture fails current gates. `[FEEDBACK-RP]` |
| **Microsoft Azure Speech** — standard neural/batch | **observed** — 24/48 kHz voices, SSML controls, word boundaries, and batch synthesis are documented. | **unknown** — exact endpoint/method, model/version, stock voice, region, output enum, excerpt count/limit, request, and account manifest are absent. | **unknown** — formula `0.009258 × R`, but numeric regional rate `R` was unavailable. | `not_ready` — incomplete manifest plus output-rights, public-use, agreement, rate, retention, and privacy-configuration unknowns. `[FEEDBACK-TC/RP]` |
| **Google Cloud TTS** — Chirp 3: HD | **observed** — regional availability and lossless output are documented; voice controls/SSML additions are Preview. | **unknown** — selected-route sample rate, one-request excerpt capacity, voice/location/client/request manifest, and Preview acceptance are not bound; generic `<mark>` support does not establish Chirp word timing. | **observed** — `$30/M × 9,258 = $0.27774` before the documented 1M-character free allowance. Actual eligibility is **unknown**. | `not_ready` — incomplete manifest plus public-use, selected-voice, agreement, and account privacy-configuration unknowns. `[FEEDBACK-TC/RP]` |
| **Amazon Polly** — Long-form / Neural | **observed** — long-form limits, lexicons, and speech marks are documented. | **conflicting** — technical explorer reported 24 kHz Long-form output while the production explorer found the reviewed `SynthesizeSpeech` PCM route capped at 16 kHz. | **observed** — Long-form `$0.9258`, or `$1.8516` with a separately billed marks request; Neural `$0.148128`, or `$0.296256` with marks. | `not_ready` — master-format and data-use conflicts plus rights/retention unknowns. `[FEEDBACK-TC/PA/RP]` |
| **Cartesia** — `sonic-3.5-2026-05-04` | **observed** — snapshot, WAV/raw output, pronunciation dictionaries, continuations, and word/phoneme timestamps are documented. | **unknown** — whole-excerpt request capacity and complete candidate manifest are absent. | **observed** — `750 seconds × 15 credits/second = 11,250 credits`; Free 20k credits; Pro $5/month/100k credits. Actual eligibility is **unknown**. | `not_ready` — capacity, pre-upload data terms, retention, and actual commercial/public-use configuration remain unknown. `[FEEDBACK-TC/RP]` |
| **PlayHT / PlayAI** — Play3.0-mini / PlayDialog | **observed** — large streaming request, seed, speed, emotion/guidance, and formats through 48 kHz were documented. | **unknown** — pronunciation, timing/alignment, lifecycle, exact manifest, and operative legal evidence are absent. | **unknown** — current pricing was not retrieved. | `not_ready` — no complete technical or legal/data witness route. `[FEEDBACK-TC/RP]` |
| **Hume** — Octave 1 / Octave 2 Preview | **observed** — continuation, lossless formats, and Octave 2 timing are documented. Version/control scope is **conflicting** across Octave versions and Preview status. | **unknown** — exact versioned configuration, Preview acceptance, excerpt route, and complete manifest are absent. | **observed** — about 9,258 characters; Free 10k characters; Starter $3/month/30k characters. Actual eligibility is **unknown**. | `not_ready` — technical manifest plus policy, retention, and enterprise-control conflicts/unknowns. `[FEEDBACK-TC/RP]` |

## Eight-provider legal and data matrix

No positive statement below extends beyond its exact source scope. If effective/revision date, provider entity, jurisdiction, selected plan/account, region, currency, or applicable agreement is missing from the cited binding, that qualifier is **unknown**.

| Provider | Generated-output ownership/assignment | Commercial/public-use permission | Privacy/data use | Retention/deletion | Security/enterprise controls |
|---|---|---|---|---|---|
| **OpenAI** | **observed** for the API/business agreement’s assignment of OpenAI’s output interest; actual order-form scope **unknown**. | **unknown** for the selected stock voice, public video, disclosure, and actual order form. | **observed** for the cited API endpoint’s no-training posture; actual account controls **unknown**. | **observed** up to 30-day abuse monitoring and ZDR eligibility; actual eligibility and complete deletion posture **unknown**. | **unknown** for the actual account, agreement, audit evidence, region, and subprocessors. |
| **ElevenLabs** | **observed** under reviewed non-EEA paid terms; actual entity/jurisdiction/account **unknown**. | **observed** for paid commercial use under the reviewed scope; selected voice and actual agreement **unknown**. | **observed** broad persistent content/model-use rights; acceptable enterprise repair **unknown**. | **observed** voice-derived retention may reach three years; actual account deletion and backup posture **unknown**. | **unknown** for applicable DPA, audit evidence, region, and account controls. |
| **Microsoft Azure Speech** | **unknown** — reviewed sources did not establish generated-audio ownership/assignment. | **unknown** — use-case documentation does not establish actual public-video permission. | **observed** for real-time prebuilt no-log and batch-storage distinctions; actual account configuration **unknown**. | **observed** that batch artifacts are stored in Azure Storage and deletable; complete retention/backups **unknown**. | **unknown** for the actual agreement, DPA applicability, audit evidence, region, and subprocessors. |
| **Google Cloud TTS** | **unknown** — general Customer Data rights do not establish product-specific generated-audio title. | **unknown** — product-specific public-distribution permission and selected-voice license were not found. | **observed** that Cloud TTS is described as stateless/resourceless and not logging text/audio; actual account configuration **unknown**. | **observed** DPA deletion terms at their stated scope; actual stored-data/backups/account applicability **unknown**. | **observed** DPA security measures at their stated scope; actual account applicability, audit evidence, region, and subprocessors **unknown**. |
| **Amazon Polly** | **observed** that AWS describes Polly output as “Your Content”; actual selected-route agreement scope **unknown**. | **unknown** for the selected voice and public-video use. | **conflicting** — Service Terms permit improvement use unless opt-out is configured, while a newer service card appears to deny training use. | **unknown** — no concrete retention period was established. | **unknown** for actual DPA/security/audit/account configuration. |
| **Cartesia** | **observed** that Cartesia does not claim ownership of inputs/outputs; actual agreement scope **unknown**. | **observed** that commercial licensing begins at Pro; selected voice, public-video scope, and actual plan **unknown**. | **observed** broad training/product-improvement rights; acceptable pre-upload ZDR/no-training configuration **unknown**. | **unknown** — Enterprise ZDR scope is documented, but actual enrollment, metadata retention, backups, and deletion proof are not. | **unknown** for actual Enterprise/DPA/audit/region/subprocessor controls. |
| **PlayHT / PlayAI** | **unknown**. | **unknown**. | **unknown**. | **unknown**. | **unknown** — operative Terms and Privacy endpoints returned HTTP 502. |
| **Hume** | **observed** that users retain input/output rights under reviewed terms; actual account scope **unknown**. | **observed** from Creator-and-higher plan language; selected voice and actual agreement **unknown**. | **conflicting** — broad Terms license versus older API no-training policy. | **unknown** — the policy tension does not establish complete ordinary, backup, or deletion behavior. | **unknown** for applicable DPA, enterprise commitments, audit evidence, region, and subprocessors. |

For all eight providers, `custom_cloned_voice_availability: not_applicable` and `cloning_authorization: not_applicable` because the protocol prohibits both. The cloning sources below remain exclusion context and do not support stock-voice admission.

## Exact source bindings

Every binding below has retrieval date **2026-08-04**, exact official URL, source-local selector, explorer reference, evidence scope, and proof status.

- **OAI-1** — [Text to speech](https://developers.openai.com/api/docs/guides/text-to-speech); selectors `### Text-to-speech models`, `### Voice options`, `## Supported output formats`, `## Supported languages`; capability/formats/voices/streaming; `TC/spawn-0001`; **observed with internal voice-count conflict**.
- **OAI-2** — [GPT-4o mini TTS Model](https://developers.openai.com/api/docs/models/gpt-4o-mini-tts); selectors `Pricing`, `Snapshots`, `Rate limits`; token price/input/access; `TC/spawn-0001`; **observed**.
- **OAI-3** — [Models](https://developers.openai.com/api/docs/models/gpt-4-and-gpt-4-turbo); selector `## Specialized models > Speech generation`; lifecycle; `TC/spawn-0001`; **observed conflict with OAI-1**.
- **OAIR-1** — [OpenAI Services Agreement](https://cdn.openai.com/osa/openai-services-agreement.pdf); selectors `§§2.2, 4.1–4.3, 5.1–5.3`; API/business rights and content use; `RP/spawn-0002`; **observed**.
- **OAIR-2** — [Data controls in the OpenAI platform](https://developers.openai.com/api/docs/guides/your-data#default-usage-policies-by-endpoint); selectors `Data retention controls for abuse monitoring`, `/v1/audio/speech`; training/retention/ZDR eligibility; `RP/spawn-0002`; **observed**.
- **OAIR-3** — [Audio API Reference](https://developers.openai.com/api/reference/resources/audio); selectors `Create voice`, `Create voice consent`; custom-voice consent; `RP/spawn-0002`; **observed**, custom-voice retention unverified.

- **EL-1** — [Models](https://elevenlabs.io/docs/overview/models); selectors `## Flagship models > ### Text to Speech`, `## Models overview`; languages/limits/long-form positioning; `TC/spawn-0001`; **observed**.
- **EL-2** — [Create speech with timing](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps); selectors `Query parameters`, `Request`, `Response`; formats/dictionaries/seed/continuity/alignment; `TC/spawn-0001`; **observed**.
- **EL-3** — [ElevenLabs Pricing for Creators & Businesses of All Sizes](https://elevenlabs.io/pricing); selectors `### Free`, `### Starter`, `## Compare plans`, `How do text characters and credits work?`; plans/credits; `TC/spawn-0001`; **observed**.
- **ELR-1** — [ElevenLabs Terms of Service](https://elevenlabs.io/terms-of-use); selectors `§§1(c), 4(c)–(i)`; commercial use/output/content license; `RP/spawn-0002`; **observed for non-EEA terms**.
- **ELR-2** — [ElevenLabs Privacy Policy](https://elevenlabs.io/privacy-policy); selectors `§§5–6, 8, 10`; storage/transfers/retention/deletion; `RP/spawn-0002`; **observed**.
- **ELR-3** — [Professional Voice Cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning); selector `Creating a Professional Voice Clone`; identity/consent control; `RP/spawn-0002`; **observed**.

- **AZ-1** — [Text to speech overview](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech); selectors `## Advanced features`, `## Pricing note > ### Billable characters`; batch/SSML/formats/billing basis; `TC/spawn-0001`; **observed**.
- **AZ-2** — [Quotas and Limits for Azure Speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-quotas-and-limits); selectors `### Text-to-speech quotas and limits per resource`, `#### Batch synthesis`; duration/payload/throughput; `TC/spawn-0001`; **observed**.
- **AZ-3** — [Pricing - Azure Speech in Foundry Tools](https://azure.microsoft.com/en-us/pricing/details/speech/); selectors `Text to Speech`, `How does billing work?`; SKU/billing units; `TC/spawn-0001`; **observed**, numeric regional rate unverified.
- **AZR-1** — [Data, privacy, and security for text to speech](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security); selectors `Prebuilt neural voice`, `Data storage and retention`, `Recorded acknowledgment statement verification`; logging/storage/deletion/consent; `RP/spawn-0002`; **observed**.
- **AZR-2** — [Disclosure for voice and avatar talent](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent); selectors `Requirements and tips for meaningful consent`, `Microsoft’s use of custom models`; custom-voice consent; `RP/spawn-0002`; **observed**.
- **AZR-3** — [Text to speech transparency note](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/transparency-note); selectors `Use cases`, `Considerations when choosing use cases`; use-case scope; `RP/spawn-0002`; **observed**, output ownership unverified.

- **GC-1** — [Chirp 3: HD voices](https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd); selectors `## Regional availability`, `## Supported output formats`, `## Chirp 3: HD SSML support`, `## Chirp 3: HD voice controls`; availability/formats/Preview controls; `TC/spawn-0001`; **observed**.
- **GC-2** — [Text-to-Speech pricing](https://cloud.google.com/text-to-speech/pricing); selector `Pricing table > Latest TTS models`; pricing; `TC/spawn-0001`; **observed**.
- **GCR-1** — [Google Cloud Terms of Service](https://cloud.google.com/terms/); selectors `§§1.1, 5.1–5.2`, definition `Customer Data`; integration/data rights; `RP/spawn-0002`; **observed**, product-specific public distribution unverified.
- **GCR-2** — [Cloud TTS Data logging](https://docs.cloud.google.com/text-to-speech/docs/data-logging); selector `Data logging`; TTS logging; `RP/spawn-0002`; **observed**.
- **GCR-3** — [Cloud Data Processing Addendum](https://cloud.google.com/terms/data-processing-addendum/); selectors `§§5.2, 6.1–6.2, 7.1`; processing/security/deletion; `RP/spawn-0002`; **observed**.
- **GCR-4** — [Chirp 3: Instant Custom Voice](https://docs.cloud.google.com/text-to-speech/docs/chirp3-instant-custom-voice); selector `Record consent and reference audio`; custom-voice consent/storage; `RP/spawn-0002`; **observed**.

- **AWS-1** — [Long-form voices](https://docs.aws.amazon.com/polly/latest/dg/long-form-voices.html); selectors `## Available long-form voices`, `## Feature and region compatibility`; voices/formats/region/marks; `TC/spawn-0001`; **observed**, in conflict with the production lane’s generic PCM finding.
- **AWS-4** — [Amazon Polly Pricing](https://aws.amazon.com/polly/pricing/); selectors `## Amazon Polly Pricing Details`, `### Pricing`; character rates; `TC/spawn-0001`; **observed**.
- **AWSR-1** — [AWS Service Terms](https://aws.amazon.com/service-terms/); selectors `§§50.1–50.4`; content use and organization opt-out; `RP/spawn-0002`; **observed**.
- **AWSR-2** — [Amazon Polly FAQs](https://aws.amazon.com/polly/faqs/); selector `Data Privacy`; opt-out; `RP/spawn-0002`; **observed**, retention unverified.

- **CA-1** — [Sonic 3.5](https://docs.cartesia.ai/build-with-cartesia/tts-models/latest); selectors `## Language support`, `## Model snapshots`, `### Continuous updates`; language/version stability; `TC/spawn-0001`; **observed**.
- **CA-3** — [Text to Speech WebSocket](https://docs.cartesia.ai/api-reference/tts/websocket); selectors `Word Timestamps Response`, `Phoneme Timestamps Response`; timing; `TC/spawn-0001`; **observed**.
- **CA-4** — [Cartesia Pricing](https://www.cartesia.ai/pricing); selectors `### Text to Speech`, `## Compare plans in detail`; credits/plans/concurrency; `TC/spawn-0001`; **observed**.
- **CAR-1** — [Cartesia Terms of Service](https://www.cartesia.ai/legal/terms); selectors `§§4.1–4.2, 5.3(a)–(d)`; ownership/training/commercial-use conditions; `RP/spawn-0002`; **observed**.
- **CAR-2** — [Cartesia Zero Data Retention](https://docs.cartesia.ai/enterprise/zero-data-retention); selectors `What is covered by ZDR?`, `FAQ`; ZDR scope/exclusions; `RP/spawn-0002`; **observed**.

- **PH-1** — [Text to speech HTTP streaming](https://docs.play.ht/reference/api-generate-tts-audio-stream); selector `Body Params`; model/limits/controls/formats; `TC/spawn-0001`; **observed**.
- **PH-2** — [Models](https://docs.play.ht/reference/models); selectors `PlayDialog`, `Play3.0-mini`; uses/languages/streaming; `TC/spawn-0001`; **observed**.
- **PHR-1** — [Terms](https://play.ht/terms/) and [Privacy](https://play.ht/privacy/); selector `HTTP response status; no page selector available`; operative legal posture; `RP/spawn-0002`; **unverified because both returned HTTP 502**.

- **HU-1** — [Text-to-Speech](https://dev.hume.ai/docs/text-to-speech-tts/overview); selectors `## Features`, `### Octave versions`, `## API limits`; versions/languages/endpoints/limits; `TC/spawn-0001`; **observed**.
- **HU-2** — [Timestamps Guide](https://dev.hume.ai/docs/text-to-speech-tts/timestamps); selectors `## Requesting timestamps`, `## Receiving timestamps`; Octave 2 timing; `TC/spawn-0001`; **observed**.
- **HU-3** — [Pricing](https://www.hume.ai/pricing); selector `Text-to-speech`; plans/characters; `TC/spawn-0001`; **observed**.
- **HUR-1** — [Hume Terms of Use](https://www.hume.ai/terms-of-use); selectors `§§4–5, 9`; rights/input license; `RP/spawn-0002`; **observed**.
- **HUR-2** — [Hume API Data Usage Policy](https://www.hume.ai/api-data-usage-policy); selectors `Overview`, `Data Retention & Access`; API training/retention; `RP/spawn-0002`; **observed but not reconciled with HUR-1**.

## Explicit exclusions and residue

- **PlayHT/PlayAI:** excluded until operative legal sources, pricing, lifecycle, pronunciation, and alignment are verified.
- **Amazon Polly:** excluded from the current audition/control set until its path-specific 24-versus-16 kHz conflict and AWS training-use contradiction are resolved.
- **ElevenLabs:** excluded under reviewed click-through terms despite strong technical fit; enterprise contractual repair could reopen it through the declared explorer-feedback edge.
- **Cartesia:** excluded until pre-upload ZDR/no-training terms and full-request capacity are established.
- **Hume:** excluded until its Terms/API-policy conflict and Octave 2 Preview acceptance are resolved.
- **WellSaid:** outside the eight-provider cap, not technically rejected. Its reported 1,000-character chunking conflicts with the protocol’s one-request requirement unless the exact excerpt fits; ordinary retention and API-plan pricing are also unresolved. It may replace a failed row only through explorer feedback.
- No documentation proves naturalness, warmth, pacing, pronunciation, edit quality, actual duration, latency, actual billed cost, total production cost, or full-video continuity.
- All eight current providers have `audition_admission: not_ready`. No provider may be rendered under this evidence state.

## Unordered diligence shortlist — not render candidates

This list only prioritizes unresolved diligence. It is **unordered by voice quality** and does not alter `audition_admission: not_ready`:

1. **Microsoft Azure Speech, prebuilt neural voice** — diligence remains on the exact manifest, generated-output ownership, public-use permission, numeric regional rate, actual agreement, retention, and privacy configuration.
2. **Google Cloud TTS, Chirp 3: HD prebuilt voice** — diligence remains on the exact manifest, selected-route sample rate and one-request capacity, Preview acceptance, generated-output ownership, public-distribution permission, selected-voice terms, and actual agreement/configuration.
3. **OpenAI speech API, prebuilt voice** — diligence remains on lifecycle/voice-count conflicts, exact manifest and excerpt count, price binding, generated-output/order-form scope, selected-voice public-use terms, disclosure, retention, and account data controls.

Any repair that adds or changes a positive capability, rights, privacy, or cost row must return through the declared `synthesizer → explorers` feedback edge; it must not be repaired by prose.

## Candidate manifest requirements

A route remains `not_ready` while any required manifest field is unknown. Unsupported settings are recorded as `unsupported/not exposed` and omitted; they are never replaced by generic defaults.

### Common immutable manifest

- provider and contracting entity;
- endpoint/method and API version;
- model ID plus snapshot or documented version state;
- stock-voice ID/version;
- `spoken_language: English`;
- owner-selected common accent/locale or explicit approval of provider-native variation;
- actual provider voice accent/locale;
- region/location and account tier;
- SDK/client name and version;
- native output enum, sample rate, bit depth, and channels;
- exact excerpt byte/token count and the selected route’s request limit;
- complete redacted request body or SSML;
- exact disclosure/attribution behavior;
- actual agreement, plan, policy qualifiers, and hard-gate decisions;
- tool/version/command manifest for decoding, normalization, independent transcription or token audit, forced alignment, VTT construction, and randomization;
- named production operator/owner.

### Microsoft Azure Speech manifest

Current **unknowns**: endpoint/method, model/version state, stock-voice ID, provider accent/locale, owner accent/locale decision, region, account tier, SDK/client/version, native output enum, exact excerpt count versus request limit, complete SSML/request, actual agreement, and all unresolved legal/data gates. Only controls positively documented for the exact selected route may appear. Free-form delivery instructions, seed, and latency flags are `unsupported/not exposed` unless later bound through explorer feedback.

### Google Cloud TTS Chirp 3: HD manifest

Current **unknowns**: endpoint/location, model/version state, stock-voice ID, provider accent/locale, owner accent/locale decision, account tier, SDK/client/version, native output enum/sample rate/depth/channels, exact excerpt count versus request limit, complete request, Preview acceptance, actual agreement, and all unresolved legal/data gates. Native automatic word timing, seed, and free-form delivery instructions are `unsupported/not exposed` for the cited selected-route evidence; external alignment remains required.

### OpenAI speech API manifest

Current **unknowns/conflicts**: exact model/version state, lifecycle, voice count, stock-voice ID, provider accent/locale, owner accent/locale decision, account tier, SDK/client/version, exact excerpt token count versus limit, complete request, price conversion/binding, actual order form, and all unresolved legal/data gates. Native seed, numeric pitch/gain, pronunciation dictionary, and speech timestamps are `unsupported/not exposed` by the cited route and must be omitted. If “Body War” fails on the first take, this route has no documented correction path and is rejected for this audition unless explorer feedback positively binds one.

The other five providers remain outside the diligence shortlist and have no admissible candidate manifest. Reopening one requires the already-declared explorer-feedback route to repair its named technical and legal/data failures.

## Fixed blind-audition protocol

### Frozen excerpt

Use this exact contiguous 237-word passage:

> At first, this feels like success. The agent found the answer.
>
> But did it find permission today—or evidence from the past?
>
> The approval was genuine. It was not fabricated. But its validity period had ended. A later review might supersede it. And the evidence we selected did not establish a current decision from the person who now owns the program.
>
> Nothing here makes the old record false. It changes what we are justified in doing with it.
>
> This is where time, confidence, and authority have to remain separate.
>
> Time tells us when a statement is meant to hold. Confidence tells us how strongly the evidence supports it. Authority tells us who may establish or change the governed state.
>
> The ontology did not vote yes or no. It made the missing premises visible.
>
> The safer answer is not simply “approved.” It is: “I found a genuine earlier approval. I cannot establish that it is current. I should ask the responsible owner—or stop.”
>
> A small example from another ontology makes this separation easier to see.
>
> In the Body War model, a score preview can become available after a calculation succeeds. But available does not mean promoted. The evidence behind that preview may carry medium confidence while an owner’s commitment remains low.
>
> Those statements do not contradict each other. They answer different questions. Confidence describes support. Promotion describes governed status. Keeping them separate prevents evidence from quietly turning into commitment.

### Generation lock

- No account action, upload, or render is permitted while `audition_admission` is `not_ready`.
- Before admission, the owner must make and record the accent/locale decision. The inherited contract supplies `spoken_language: English`; it does not supply `en-US` or another accent/locale.
- After admission, pre-register exactly one stock voice/configuration per admitted provider using its complete immutable manifest.
- Submit the whole excerpt once per render, with no chunking or stitching, only after whole-excerpt suitability is **observed** for that manifest.
- Produce two scored repetitions with identical supported settings.
- Use seed `8042026` only where the selected route documents a seed; record best-effort semantics where documented. Otherwise record `seed: unsupported/not exposed` and omit it.
- Apply native rate, pitch, gain, quality, streaming, or latency settings only when the exact selected route documents them. Record every absent control as `unsupported/not exposed`; do not synthesize generic defaults into the request.
- Use no music, EQ, compression, denoising, reverb, or time-stretching.
- Apply the following non-spoken instruction only where the exact selected route supports free-form delivery instructions:

> Reflective solo narrator. Read as a thoughtful investigation: intimate and warm, never a keynote or advertisement. Aim for 120–130 words per minute. Let punctuation create short reflective holds. Give “approved” genuine reassurance before the question introduces doubt. Keep time, confidence, and authority distinct. Deliver “ask the responsible owner—or stop” with restraint, not triumph. Do not add, omit, or paraphrase words.

When unsupported, record `instruction_support: unsupported/not exposed`, omit the instruction, and never insert descriptive words into the spoken text.

### Pronunciation and evidence capture

- First render the unchanged text without a dictionary. Expect ordinary English “Body War,” stressed on “Body.”
- If the selected route documents a provider-native lexicon/phoneme correction, permit exactly one correction without changing visible or spoken words. Retain the failed take, lock the correction, and create two replacement repetitions. Failure after that correction disqualifies the configuration.
- If pronunciation correction is `unsupported/not exposed`, an incorrect first take disqualifies that configuration; do not invent a correction parameter.
- Preserve immutable raw response bytes, SHA-256, redacted request, request/response ID, UTC times, billed units, native format, duration, and native timing metadata under unique UUID filenames. Never overwrite a regeneration.
- Before execution, freeze exact decoding and two-pass BS.1770 normalization tools, versions, commands, and tolerances in the manifest. The intended derivative is mono 48 kHz, 24-bit WAV at `-16 LUFS-I`, true peak at or below `-1 dBTP`; this method remains **unknown/not executable** until those command fields are populated. Record hashes, measured loudness, true peak, and gain.

### Verification and listening

- Freeze exact forced-alignment and independent-fidelity tools, versions, commands, timing tolerances, low-confidence thresholds, excerpt-to-VTT mapping rules, and manual-review owner before execution. Those fields are currently **unknown** and keep admission `not_ready`.
- Force-align each derivative locally to the exact text for timing evidence only. Require monotonic boundaries within audio duration; provider timestamps remain diagnostic, not caption authority.
- Independently validate the spoken sequence using either transcription produced without supplying the reference text or a token-by-token listening audit independent of the forced-alignment pass. Compare that result to the frozen excerpt for additions, omissions, substitutions, and reordered phrases.
- Send every mismatch, low-confidence token, unintelligible segment, or disagreement to manual review. Any unresolved difference disqualifies the configuration. Preserve the independent transcript/audit record, confidence output, comparison result, and reviewer decision.
- Manually inspect “approved,” the question, “time, confidence, and authority,” “Body War,” and “ask the responsible owner—or stop.”
- Preserve provider timing only as diagnostic metadata; waveform-derived cues remain caption authority.
- Generate VTT cues from the accepted waveform using the frozen mapping rules; verify ordered non-overlapping cues, complete text coverage, and the declared timing tolerances.
- Blind files with opaque identifiers. Freeze the randomization tool/version/command, UUID manifest, separately balanced listener-order manifests, and protected unblinding-key location before execution. Generate order only after artifacts are frozen, separate each candidate’s repetitions, and hide the key until score sheets are locked.
- Use at least three listeners under the same headphones, player, output level, and quiet-room conditions; permit one replay.

Score 1–5:

- Reflective warmth/intimacy: 20%
- Naturalness/artifact freedom: 20%
- Reassurance-to-doubt semantic arc: 20%
- Time/confidence/authority distinction: 15%
- Pacing, breath placement, ask-or-stop cadence: 15%
- Product-name/general pronunciation: 10%

Use anchors `1 = unacceptable/clear failure`, `3 = adequate`, and `5 = excellent`, with 2 and 4 as intermediate judgments. For each score sheet calculate `weighted_points = Σ(weight_percent × score / 5)` on a 0–100 scale. Report the candidate median plus listener/repetition spread. An absolute difference below 3.0 weighted points is a tie requiring a longer-sequence test. Preserve raw score sheets, formula output, listener-order manifests, and the locked unblinding key.

Disqualify altered words, uncorrected key-term errors, cloned/custom voices, clipping/truncation/non-speech artifacts, duration outside 75–120 seconds, failure to provide the required master, missing reproducibility metadata, or failed rights/privacy review.

### Terminal operator decision

`decision_owner: unknown`. Before rendering, the owner must identify the named production operator/owner responsible for the terminal decision. After all hard gates close, blind listening completes, results are unblinded, and any required longer prototype is reviewed, that operator must listen and record exactly one dated outcome: `approve`, `reject`, or `defer`, with reasons and the governing artifact hashes.

Weighted listening scores are advisory. They never auto-select a provider and cannot absorb or override fixed-excerpt suitability, output ownership, commercial/public-use permission, privacy/data use, retention/deletion, security/enterprise controls, total production cost, or operator judgment.

Only after hard gates and technical fidelity pass may listening fit be ranked. Editability is a declared threshold or tie-breaker; latency and documented usage-price estimates remain separate observed constraints, while total production cost remains unknown until execution and operator accounting. No rendered audio, duration, fidelity, pronunciation, caption accuracy, quality result, winner, final provider approval, completed narration, or production-ready video has been established.
