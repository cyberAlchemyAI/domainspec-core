# Explorer returns

The sections below preserve the explorer returns verbatim as joined by the dispatch owner. Receipt envelopes live in `receipts/`.

## Agent 1 — Technical capability

## Scope and proof boundary

Retrieved 2026-08-04. Eight providers were compared using current first-party documentation only. “Observed” means the cited page was retrieved and contained the stated claim; no account, API, audio, latency, quota, or quality test was executed. Naturalness, warmth, pacing, and final voice fit remain unverified pending a fixed-script blind audition.

Cost estimates use a provisional 9,258 billable characters (`1,543 words × 6 characters/word`) and 750 seconds. Exact script characters, markup, retries, taxes, storage, and ancillary services could change the result.

## Capability matrix

| Provider / candidate model | Documented production capability | Timing and editability | Limits / availability | Time-scoped price | Technical disposition |
|---|---|---|---|---|---|
| OpenAI — `gpt-4o-mini-tts`; fallback `tts-1`/`tts-1-hd` | Prompted accent, emotion, intonation, speed, and tone; 13 listed voices; MP3, Opus, AAC, FLAC, WAV, and PCM; multilingual output, with voices optimized for English. | Streaming audio, but no speech-generation timestamp response was documented. Pronunciation lexicon/phoneme control was not found. | Speech endpoint input is 4,096 characters; model page says 2,000 input tokens, so the full script requires chunks. Lifecycle evidence conflicts: the guide calls `gpt-4o-mini-tts` newest/reliable while the model catalog labels it deprecated; the guide also says both 11 and 13 built-in voices. | `gpt-4o-mini-tts`: $0.60/M text-input tokens plus $12/M audio-output tokens; no first-party seconds-to-audio-token conversion found. `tts-1`: $15/M characters, approximately **$0.14** for 9,258 characters. | **Conditional, not advanced** until lifecycle and voice-count contradictions are resolved; direct timing is absent. |
| ElevenLabs — Eleven v3 / Multilingual v2 / Flash v2.5 | v3: 70+ languages, 5,000-character requests; Multilingual v2: 29 languages, 10,000 characters and explicitly positioned for long-form stability; Flash v2.5: 32 languages, 40,000 characters. Voice settings, pronunciation dictionaries, text normalization, continuity fields, and multiple encoded/lossless formats are documented. | Dedicated endpoint returns original and normalized character-level alignment. Seed is best-effort, not guaranteed deterministic. | Approximate script fits one Multilingual-v2 request only if the character estimate holds; v3 needs at least two chunks. High-quality PCM/WAV tiers vary by plan. | Free: 10k credits; Starter: $6/month, 30k credits; Multilingual v2 uses about 9.3k credits for the assumed script, Flash about 4.6k–9.3k depending plan/account rate. | **Advance**. Strong direct alignment and continuity evidence; no voice-quality inference. |
| Microsoft Azure Speech — standard neural via batch synthesis | 100+ languages/locales; 24 kHz and 48 kHz neural voices; SSML controls pitch, rate, pauses, volume, pronunciation, lexicons, and styles. Batch synthesis is explicitly intended for audio longer than ten minutes. | SDK events include `WordBoundary`; SSML bookmarks expose offsets. | Real-time output is capped at 10 minutes, so the 12:30 target requires batch or chunking. Batch accepts up to 10,000 text inputs/job and a 2 MB payload. | Billed per character, including most SSML. The current public pricing view withheld regional numeric rates, so cost is **unverified**: `0.009258 × selected regional $/M-character rate`. | **Advance**, provided the exact regional voice and rate are pinned. |
| Google Cloud TTS — Chirp 3: HD | GA in global, US, EU and listed regional endpoints; many English locales; synchronous, streaming, and batch paths. Current preview controls add SSML, IPA/X-SAMPA pronunciation, pace 0.25–2.0, and pause markup. Batch supports MP3, OGG Opus, PCM, A-law and μ-law. | Generic Cloud TTS supports SSML-mark timepoints, but `<mark>` is absent from Chirp 3’s current supported-SSML list. Therefore direct Chirp word timing is **unverified**. | General synchronous content limit is 5,000 bytes, requiring chunking; Chirp 3 request quota is 200/min/project. SSML and voice-control features are Preview even though core Chirp regional availability is GA. | Chirp 3: HD is $30/M characters after its 1M-character free usage allowance; approximately **$0.28** for 9,258 characters before free allowance. | **Advance**, with external alignment or a verified timing route and explicit Preview-feature handling. |
| Amazon Polly — Long-form; Neural reserve | Long-form is designed for extended narration, supports asynchronous synthesis, many SSML tags, MP3/OGG/raw PCM, 24 kHz output, and four en-US voices. Lexicons support pronunciation overrides. | Long-form supports sentence/word/viseme/SSML speech marks. Generative Polly explicitly does **not** support speech marks. | Long-form is available only in `us-east-1`. Synchronous input allows 3,000 billed characters/10 minutes; asynchronous task input allows 100,000 billed characters. | Long-form $100/M characters: about **$0.93** for audio, or **$1.85** if a separate equally billed speech-marks request is needed. Neural is $16/M: about **$0.15**, or **$0.30** with marks. | **Advance** as a stable, timestamp-capable baseline; do not substitute Generative if direct marks remain required. |
| Cartesia — `sonic-3.5-2026-05-04` | Stable dated snapshot; 42 languages. API exposes speed/volume generation controls, pronunciation dictionaries, WAV/MP3/raw output, and unlimited continuation inputs for seam-aware streaming. Pinning the dated snapshot avoids alias drift. | WebSocket responses include word- and phoneme-level timestamps. | Public docs do not state a simple maximum full-transcript character count; continuations have no stated count limit. Plan concurrency ranges from 2 to 15 before Enterprise. | Sonic 3.5 consumes 15 credits/second: 750 seconds ≈ **11,250 credits**. Free includes 20k credits; Pro is $5/month for 100k credits. Commercial licensing is a separate rights-lane gate. | **Advance**. Excellent reproducibility surface on paper; waveform behavior remains untested. |
| PlayHT / PlayAI — Play3.0-mini / PlayDialog | Play3.0-mini documents 36 languages, 20,000-character streaming requests, seed, speed, emotion/guidance controls, formats through 48 kHz, and bulk-oriented generation. PlayDialog has an asynchronous batch endpoint. | No current first-party TTS word-timestamp or pronunciation-control route was located. Seed is unavailable for Dialog Turbo. | General non-Play3.0 requests are limited to 2,000 characters. The documentation spans PlayHT and PlayAI branding and several legacy/current engines. | Current pricing page could not be retrieved; numeric price is **unverified**. | **Do not advance yet**: obtain current pricing, canonical model/lifecycle confirmation, pronunciation path, and alignment path. |
| Hume — Octave 1 / Octave 2 Preview | Streaming and non-streaming endpoints; voice library/design; long-form continuation; per-utterance speed and trailing silence; MP3/WAV/PCM. Octave 2 adds 11 documented languages; Octave 1 supports English and Spanish. | Octave 2 returns word- and phoneme-level timestamps. | 5,000 characters/utterance and up to five generations/request. Octave 2 is explicitly Preview; acting-description control currently applies to Octave 1, while speed applies to both. | Free: 10k characters; Starter: $3/month and 30k characters. The assumed script is about 9.3k characters. | **Conditional reserve**: technically testable, but timestamp-capable Octave 2’s Preview status and split control surface should be accepted explicitly. |

## Source register

Every entry below was observed on 2026-08-04; selectors are source-local.

- OAI-1: [“Text to speech”](https://developers.openai.com/api/docs/guides/text-to-speech), selectors `### Text-to-speech models`, `### Voice options`, `## Supported output formats`, `## Supported languages`; scope: controls, voices, formats, languages, streaming. **Observed**, with internal 11-versus-13 voice contradiction.
- OAI-2: [“GPT-4o mini TTS Model”](https://developers.openai.com/api/docs/models/gpt-4o-mini-tts), selectors `Pricing`, `Snapshots`, `Rate limits`; scope: token pricing, input maximum, access tiers. **Observed**.
- OAI-3: [“Models”](https://developers.openai.com/api/docs/models/gpt-4-and-gpt-4-turbo), selector `## Specialized models > Speech generation`; scope: lifecycle label. **Observed contradiction**: deprecated versus OAI-1’s newest/reliable.
- EL-1: [“Models”](https://elevenlabs.io/docs/overview/models), selectors `## Flagship models > ### Text to Speech`, `## Models overview`; scope: languages, model limits, long-form positioning. **Observed**.
- EL-2: [“Create speech with timing”](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps), selectors `Query parameters`, `Request`, `Response`; scope: formats, dictionaries, seed, continuity, character alignment. **Observed**.
- EL-3: [“ElevenLabs Pricing for Creators & Businesses of All Sizes”](https://elevenlabs.io/pricing), selectors `### Free`, `### Starter`, `## Compare plans`, `How do text characters and credits work?`; scope: plans and credits. **Observed**.
- AZ-1: [“Text to speech overview”](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech), selectors `## Advanced features`, `## Pricing note > ### Billable characters`; scope: batch, SSML, formats, billing basis. **Observed**.
- AZ-2: [“Quotas and Limits for Azure Speech”](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-quotas-and-limits), selectors `### Text-to-speech quotas and limits per resource`, `#### Batch synthesis`; scope: duration, throughput, payload. **Observed**.
- AZ-3: [“Pricing - Azure Speech in Foundry Tools”](https://azure.microsoft.com/en-us/pricing/details/speech/), selectors `Text to Speech`, `How does billing work?`; scope: SKUs and units. **Observed**, numeric regional rates unavailable in retrieved rendering.
- GC-1: [“Chirp 3: HD voices”](https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd), selectors `## Regional availability`, `## Supported output formats`, `## Chirp 3: HD SSML support`, `## Chirp 3: HD voice controls`; scope: GA footprint and Preview controls. **Observed**.
- GC-2: [“Text-to-Speech pricing”](https://cloud.google.com/text-to-speech/pricing), selector `Pricing table > Latest TTS models`; scope: Chirp and legacy rates. **Observed**.
- GC-3: [“Quotas & limits”](https://docs.cloud.google.com/text-to-speech/quotas), selectors `## Content limits`, `## Requests limit`; scope: request bytes and quotas. **Observed**.
- AWS-1: [“Long-form voices”](https://docs.aws.amazon.com/polly/latest/dg/long-form-voices.html), selectors `## Available long-form voices`, `## Feature and region compatibility`; scope: voices, formats, regions, speech marks. **Observed**.
- AWS-2: [“Generative voices”](https://docs.aws.amazon.com/polly/latest/dg/generative-voices.html), selector `## Feature and region compatibility`; scope: regions, formats, explicit absence of speech marks. **Observed**.
- AWS-3: [“Quotas in Amazon Polly”](https://docs.aws.amazon.com/polly/latest/dg/limits.html), selectors `## SynthesizeSpeech API operations`, `## SpeechSynthesisTask API operations`; scope: request and async limits. **Observed**.
- AWS-4: [“Amazon Polly Pricing”](https://aws.amazon.com/polly/pricing/), selectors `## Amazon Polly Pricing Details`, `### Pricing`; scope: per-character rates. **Observed**.
- CA-1: [“Sonic 3.5”](https://docs.cartesia.ai/build-with-cartesia/tts-models/latest), selectors `## Language support`, `## Model snapshots`, `### Continuous updates`; scope: languages and snapshot stability. **Observed**.
- CA-2: [“Text to Speech (Bytes)”](https://docs.cartesia.ai/api-reference/tts/bytes), selectors `Body`, `output_format`, `pronunciation_dict_id`, `generation_config`; scope: API controls and formats. **Observed**.
- CA-3: [“Text to Speech (WebSocket)”](https://docs.cartesia.ai/api-reference/tts/websocket), selectors `Word Timestamps Response`, `Phoneme Timestamps Response`; scope: timing. **Observed**.
- CA-4: [“Cartesia Pricing”](https://www.cartesia.ai/pricing), selectors `### Text to Speech`, `## Compare plans in detail`; scope: credits, minutes, concurrency. **Observed**.
- PH-1: [“Text to speech HTTP streaming”](https://docs.play.ht/reference/api-generate-tts-audio-stream), selector `Body Params`; scope: models, limits, controls, formats. **Observed**.
- PH-2: [“Models”](https://docs.play.ht/reference/models), selectors `PlayDialog`, `Play3.0-mini`; scope: intended uses, languages and streaming. **Observed**.
- HU-1: [“Text-to-Speech (TTS)”](https://dev.hume.ai/docs/text-to-speech-tts/overview), selectors `## Features`, `### Octave versions`, `## API limits`; scope: versions, languages, endpoints and limits. **Observed**.
- HU-2: [“Timestamps Guide”](https://dev.hume.ai/docs/text-to-speech-tts/timestamps), selectors `## Requesting timestamps`, `## Receiving timestamps`; scope: Octave 2 timing. **Observed**.
- HU-3: [“Pricing”](https://www.hume.ai/pricing), selector `Text-to-speech`; scope: plans, included characters and RPM. **Observed**.

## Exclusions and unresolved items

- WellSaid was excluded from the eight-provider matrix by the cap, not ruled technically unfit. Its current API documents 1,000-character chunks and a word-timing endpoint returning JSON, SRT and VTT, but API plans require provider contact. It is a reasonable feedback-edge substitute if direct VTT generation outweighs open pricing.
- No technically documented feature proves audible quality.
- Exact cost requires the frozen script’s actual billable character/token count, chosen model, retries, markup and plan.
- Availability means documented access/region/model status, not a live uptime or account-entitlement test.
- Required synthesis candidates for the next lane: **ElevenLabs, Azure Speech, Google Chirp 3 HD, Amazon Polly Long-form, and Cartesia Sonic 3.5**. This is a technical set, not an endorsement or audition shortlist.
- Before any audition, resolve OpenAI lifecycle contradictions, Azure’s numeric regional rate, PlayHT’s current pricing/timing/pronunciation evidence, Google Chirp timing, Cartesia’s full-transcript handling, and Hume Preview acceptance.

## Agent 2 — Rights and privacy

Research boundary: current first-party desk research retrieved 2026-08-04 UTC. This is a risk-screening aid, not legal advice, procurement approval, provider selection, or evidence of voice quality. No account, terms acceptance, purchase, credential, upload, API call, synthesis, or cloning occurred. The repository Inventory supplied no provider authority.

The safest current requirement is a prebuilt voice. The fixture does not require cloning, so cloning should remain prohibited unless an owner later establishes a speaker identity, written consent, permitted uses, revocation terms, and deletion requirements.

## Hard gates

1. The exact plan and contracting entity must permit commercial/public educational-video use.
2. Output ownership or assignment must be established separately from commercial-use permission.
3. Script and audio must not be used for general model training unless an owner explicitly accepts that use; any opt-out must be effective before upload.
4. Input/output retention, support access, deletion mechanics, backup deletion, processing region, and subprocessors must be documented.
5. Any custom voice requires documented speaker authorization plus a provider-side consent or verification control. User attestation alone is weaker evidence.
6. Applicable DPA, security terms, and order form must be reviewed for the actual account—not inferred from an enterprise marketing page.
7. Unknown evidence is not permission. A provider failing a gate remains ineligible for production.

Risk tiers below measure policy friction only; they do not rank sound, workflow, or total cost.

## Provider findings

### Tier A — clearer published posture, still conditional on owner review

- **OpenAI API — lower-friction API path.** The current business agreement permits API integration, assigns OpenAI’s interest in output to the customer, limits Customer Content use to service delivery, law/policy enforcement, and abuse prevention, and bars development/improvement use absent explicit agreement. `/v1/audio/speech` is documented as not used for training, with up to 30-day abuse-monitoring retention, no application-state retention, and eligibility for approved Zero Data Retention. Custom voices are limited to eligible customers and require a consent recording. Public commercial use remains subject to OpenAI policies, third-party rights, and the actual order form. Custom-voice artifact retention was not established in the reviewed sources. Security assertions include encryption and API certifications, but no audit report was inspected. **Status: observed, with custom-voice retention unverified.** Sources: [OpenAI Services Agreement](https://cdn.openai.com/osa/openai-services-agreement.pdf), selectors §§2.2, 4.1–4.3, 5.1–5.3; [Data controls in the OpenAI platform](https://developers.openai.com/api/docs/guides/your-data#default-usage-policies-by-endpoint), selectors “Data retention controls for abuse monitoring” and `/v1/audio/speech`; [Audio API Reference](https://developers.openai.com/api/reference/resources/audio), selectors “Create voice” and “Create voice consent”; [Security and privacy at OpenAI](https://openai.com/security-and-privacy/), selectors “For businesses” and “Security compliance & accreditation.” Scope: API/business customers; ZDR and custom voices require eligibility.

- **Google Cloud Text-to-Speech — lower-friction prebuilt path.** Google’s cloud terms let customers integrate GCP services into independently valuable applications, define data derived from customer-provided data as Customer Data, and preserve customer IP rights in Customer Data. Cloud TTS states that it is stateless/resourceless and does not log customer TTS text or audio. The Cloud DPA limits processing to instructions, supplies security measures, and provides deletion deadlines for stored Customer Data. Instant Custom Voice requires a prescribed recorded consent statement and stores consent/reference audio in customer-designated Cloud Storage. Product-specific language expressly addressing public distribution of synthesized TTS audio was not found; procurement should confirm that the general Customer Data rights and chosen voice license cover the video. **Status: observed; product-specific public-distribution language unverified.** Sources: [Google Cloud Terms of Service](https://cloud.google.com/terms/), selectors §§1.1, 5.1–5.2 and definition “Customer Data”; [Cloud TTS Data logging](https://docs.cloud.google.com/text-to-speech/docs/data-logging), selector “Data logging”; [Cloud Data Processing Addendum](https://cloud.google.com/terms/data-processing-addendum/), selectors §§5.2, 6.1–6.2, 7.1; [Chirp 3: Instant Custom Voice](https://docs.cloud.google.com/text-to-speech/docs/chirp3-instant-custom-voice), selector “Record consent and reference audio.” Scope: Google Cloud customer agreement; custom voice has separate storage and consent duties.

- **Microsoft Azure Speech — strong prebuilt privacy evidence, ownership gap.** For real-time prebuilt synthesis, Microsoft states that neither input text nor output audio is stored in Microsoft logs. Batch/long-audio scripts and output are stored in Azure Storage and can be deleted through the API. Microsoft incorporates its DPA for Azure processing. Prebuilt voices may be used without registration for otherwise compliant use cases; the transparency note includes educational, media, and business-content contexts. Custom neural voice is Limited Access and requires explicit written permission, recorded acknowledgment, and speaker verification; Microsoft may retain acknowledgment data and model copies for security/integrity. The reviewed sources did not establish explicit ownership or assignment of generated prebuilt audio. **Status: observed; output-title position unverified.** Sources: [Data, privacy, and security for text to speech](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security), selectors “Prebuilt neural voice,” “Data storage and retention,” and “Recorded acknowledgment statement verification”; [Disclosure for voice and avatar talent](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent), selectors “Requirements and tips for meaningful consent” and “Microsoft’s use of custom models”; [Text to speech transparency note](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/transparency-note), selectors “Use cases” and “Considerations when choosing use cases.” Scope: Azure subscription; custom features are Limited Access.

- **WellSaid — strong business-contract posture, retention clarification needed.** Paid plans advertise full commercial rights; the Business & Enterprise agreement defines both input and output as Customer Data, assigns WellSaid’s interest in output to the customer, prohibits training WellSaid or third-party models on Customer Data, and requires express written speaker consent for custom voices. Customer-supplied text is stored in US-hosted Google Cloud infrastructure. The DPA provides return or secure destruction of Personal Data within 90 days after written request, subject to law. Potential abuse may cause inputs/outputs to be logged for review. Default project-retention duration and backup-deletion timing were not published in the reviewed material. **Status: observed; ordinary retention duration unverified.** Sources: [WellSaid Services Agreement — Business & Enterprise](https://www.wellsaid.io/wsa-business-ent), selectors definitions “Customer Data,” “Input,” “Output,” §§4.2–4.3, 5.1, 7.2; [WellSaid security](https://www.wellsaid.io/features/features-security), selectors “U.S. hosted, secure data” and FAQ “How does WellSaid use customer data?”; [WellSaid DPA](https://www.wellsaid.io/dpa), selector §9 “Return or Destruction of Personal Data”; [WellSaid pricing](https://www.wellsaid.io/ai-voice-pricing), selectors “Starter,” “Pro,” and “Commercial usage rights.” Scope: paid/business plans; free trial has no commercial rights.

### Tier B — contractual or configuration repair required

- **Amazon Polly.** AWS says Polly output is “Your Content.” However, current Service Terms authorize AWS to store and use Polly AI Content to improve Polly and AWS/affiliate AI technologies, including possible processing outside the chosen region, unless an AWS Organizations AI-services opt-out policy is configured. The Polly FAQ confirms the opt-out but supplies no concrete retention period. AWS’s DPA applies automatically where relevant. A newer Polly service card appears to say inputs/outputs are never used for training, creating a first-party inconsistency with controlling Service Terms; the terms should govern unless AWS confirms otherwise in writing. No adequate current public consent procedure for Brand Voice was established. **Gate:** pre-upload opt-out plus written retention and Brand Voice confirmation; otherwise use prebuilt voices only. **Status: observed conflict; retention and custom-voice consent unverified.** Sources: [AWS Service Terms](https://aws.amazon.com/service-terms/), selectors §§50.1–50.4; [Amazon Polly FAQs](https://aws.amazon.com/polly/faqs/), selector “Data Privacy”; [AWS Data Processing Addendum overview](https://docs.aws.amazon.com/whitepapers/latest/navigating-gdpr-compliance/aws-data-processing-addendum-dpa.html), selector “AWS Data Processing Addendum”; [Amazon Polly service card](https://docs.aws.amazon.com/ai/responsible-ai/amazon-polly/overview.html), selector “Privacy.” Scope: AWS customer account and organization-level configuration.

- **Cartesia.** Pro and higher plans advertise a commercial-use license, and Cartesia says it does not claim ownership of customer inputs or outputs. Its public terms nevertheless grant broad, effectively persistent rights to use inputs and outputs for model training and product improvement; opt-out is prospective. Enterprise ZDR covers TTS input and output but excludes cloning and retains operational metadata. The terms prohibit using another person’s voice without express permission, but reviewed public documentation did not establish recorded speaker verification. **Gate:** Enterprise ZDR or negotiated no-training terms must be active before script submission; prebuilt voice only unless cloning verification is contractually established. **Status: observed; provider-side clone verification unverified.** Sources: [Cartesia Terms of Service](https://www.cartesia.ai/legal/terms), selectors §§4.1–4.2 and 5.3(a)–(d); [Cartesia Zero Data Retention](https://docs.cartesia.ai/enterprise/zero-data-retention), selectors “What is covered by ZDR?” and FAQ; [Cartesia pricing](https://www.cartesia.ai/pricing), selectors “Pro” and “Enterprise.” Scope: commercial use begins at Pro; ZDR/DPA are Enterprise.

- **Hume AI.** Creator and higher plans permit commercial use and users retain input/output rights, but the Terms grant Hume a perpetual, irrevocable, sublicensable license to input for platform improvement and product development. An API-specific policy says API data is not used for training and only Registry uploads are retained until deletion, but that policy was last updated in 2023 and does not clearly resolve the broader Terms license. Voice cloning requires a consenting speaker and UI confirmation of rights/consents, but no stronger identity-verification witness was found. DPA and strongest compliance commitments appear request/Enterprise-scoped. **Gate:** obtain written confirmation that the API policy controls TTS submissions, define retention/deletion, and avoid cloning absent stronger verification. **Status: observed contractual tension.** Sources: [Hume Terms of Use](https://www.hume.ai/terms-of-use), selectors §§4–5 and 9; [Hume API Data Usage Policy](https://www.hume.ai/api-data-usage-policy), selectors “Overview” and “Data Retention & Access”; [Hume Voice Cloning](https://dev.hume.ai/docs/voice/voice-cloning), selector “Upload an audio file”; [Hume pricing](https://www.hume.ai/pricing), selectors “Creator” and “Enterprise.” Scope: commercial rights begin at Creator; enterprise compliance is separately scoped.

### Tier C — hold unless negotiated terms repair the posture

- **ElevenLabs.** Paid users may use outputs commercially and retain rights to outputs. The current non-EEA Terms also grant ElevenLabs broad perpetual, irrevocable, sublicensable rights over Content—including voice indicia—and User Voice Models for service improvement and new-product development. Training opt-out is prospective and does not reverse prior use. The Privacy Policy says voice-derived data may be kept for up to three years after the last interaction, describes US storage/transfers, and offers deletion rights subject to applicable limitations. Professional Voice Cloning is restricted to the user’s own verified voice, but that does not cure the script/content license. **Gate:** do not advance under click-through terms; require negotiated enterprise no-training, retention/deletion, voice-library licensing, and DPA terms. **Status: observed for non-EEA terms; EEA/UK terms not evaluated.** Sources: [ElevenLabs Terms of Service](https://elevenlabs.io/terms-of-use), selectors §§1(c), 4(c)–(i); [ElevenLabs Privacy Policy](https://elevenlabs.io/privacy-policy), selectors §§5–6, 8, 10; [ElevenLabs Safety](https://elevenlabs.io/safety), selectors “Our Safeguards” and “Prevent”; [Professional Voice Cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning), selector “Creating a Professional Voice Clone.” Scope: non-EEA/Switzerland/UK click-through terms; commercial use requires paid plan.

## Exclusion

- **PlayHT / PlayAI — exclude from the production shortlist pending evidence repair.** Its first-party safety page states consent-first controls, encryption, deletion on account termination, and security audits “in progress,” but the current [Terms](https://play.ht/terms/) and [Privacy](https://play.ht/privacy/) endpoints returned HTTP 502 during this retrieval. Therefore commercial rights, output ownership, training, TTS retention, deletion SLA, DPA scope, and governing entity could not be verified from operative first-party legal text. Marketing or safety prose cannot substitute for those terms. **Status: legal sources unverified.**

## Questions requiring provider confirmation

1. Which exact agreement, entity, jurisdiction, order form, and voice-library terms govern this account and selected voice?
2. Does that contract permit worldwide, perpetual public and commercial distribution of the rendered educational video?
3. Who owns the audio, and what continuing rights belong to the provider and underlying voice talent?
4. Are TTS text/audio used for training, human review, safety logging, or benchmarking; what control disables each before first upload?
5. What are ordinary, backup, abuse-log, and post-termination retention periods, and what deletion proof is available?
6. What region and subprocessors handle content and support access?
7. Does the DPA cover the selected service and plan, and can current SOC/ISO reports be reviewed?
8. For cloning, how are speaker identity, informed consent, permitted contexts, revocation, and model deletion verified?
9. Are synthetic-voice disclosure, watermarking, attribution, or stock-voice restrictions required?

No voice-quality winner or final provider is established. On rights/privacy evidence alone, OpenAI API, Google Cloud TTS, Azure prebuilt voices, and WellSaid paid/business plans have the clearest published paths to an audition, but each retains the named contractual unknowns. That is not an audition shortlist decision; technical and reproducible-audio gates remain separate.

## Agent 3 — Production audition

## Result

A smallest credible test is feasible, but it selects a provider–model–voice configuration, not an abstract provider. Desk research cannot establish a winner.

The five declared fixture files were read. Current SHA-256 values for the frozen voiceover, production script, and captions match the validation record. The package remains a 12:30 text candidate with explicit recording, waveform-alignment, render, and listening residue.

## Fixed audition excerpt

Use the contiguous 237-word passage beginning:

> At first, this feels like success. The agent found the answer.

and ending:

> Keeping them separate prevents evidence from quietly turning into commitment.

At the approved 120–130 words-per-minute pace, it should run approximately 109–119 seconds. Use text boundaries rather than cutting the editorial VTT by timestamp; the fixture explicitly requires cue boundaries to be realigned to the recorded waveform.

Exact text:

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

This exercises:

- Reflective warmth and a transition from reassurance to uncertainty.
- The exact word “approved.”
- A direct question.
- Separate treatment of time, confidence, and authority.
- The product/model name “Body War.”
- The restrained “ask the responsible owner—or stop” cadence.
- Contrastive delivery: genuine versus current, available versus promoted, confidence versus commitment.

## Documented capability screen

These are evidence for constructing a shortlist, not proof of output quality:

| Provider | Relevant documented capability | Protocol consequence |
|---|---|---|
| OpenAI | The speech endpoint accepts model, voice, text, and delivery instructions; `gpt-4o-mini-tts` can be prompted for tone, intonation, emotion, accent, and speed. WAV and 24 kHz 16-bit PCM are documented. AI-voice disclosure is required. [Official TTS guide](https://developers.openai.com/api/docs/guides/text-to-speech) | Eligible for lossless audition output and the fixed delivery instruction. The reviewed guide does not establish pronunciation-dictionary or alignment output, so use the common external alignment check and test “Body War” directly. |
| ElevenLabs | The API exposes model and voice IDs, voice settings, best-effort seed reproducibility, pronunciation dictionaries, PCM/WAV options, and contextual fields for chunk continuity. A separate endpoint returns character-level alignment. Zero-retention mode is documented as enterprise-only. [Synthesis API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert), [timing endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps), [pronunciation dictionaries](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries) | Eligible when the account tier exposes the required lossless format. Preserve native alignment, but still run the common aligner. Record whether privacy requirements demand an enterprise capability. |
| Azure Speech | SSML supports phoneme, lexicon, prosody, emphasis, and alias controls; the SDK exposes word-boundary events with audio offsets and durations. Audio file type, sample rate, and bit depth can be selected. [Pronunciation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation), [synthesis and word boundaries](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis) | Eligible when a fixed voice/model can produce the required PCM/WAV output. Save native word-boundary events as diagnostic metadata. |
| Google Cloud TTS | AudioConfig exposes encoding, speaking rate, pitch, gain, and sample rate. SSML supports phonemes/custom pronunciations and explicit `<mark>` timepoints. [AudioConfig](https://docs.cloud.google.com/text-to-speech/docs/reference/rest/v1/AudioConfig), [SSML](https://docs.cloud.google.com/text-to-speech/docs/ssml) | Eligible when the selected voice supports the required lossless configuration. Marks are not automatic word alignment; use external forced alignment. |
| Amazon Polly | Synthesis accepts plain text or SSML, engine, voice, lexicon, format, and sample rate. It supplies word/sentence speech marks separately and supports pronunciation lexicons. Its documented PCM output is 16 kHz maximum. [SynthesizeSpeech](https://docs.aws.amazon.com/polly/latest/APIReference/API_SynthesizeSpeech.html), [speech marks](https://docs.aws.amazon.com/polly/latest/dg/speechmarks.html), [lexicons](https://docs.aws.amazon.com/polly/latest/dg/managing-lexicons.html) | It fails a strict ≥24 kHz lossless-video-master prerequisite. It can remain a consciously downgraded control, but should not be silently compared as technically equivalent. |

Hard prerequisites are exact-text synthesis; stable model and voice identifiers; a prebuilt voice with documented permitted use; reproducible request settings; and at least 24 kHz, 16-bit mono lossless output for the production shortlist. Pronunciation controls and native timing are useful but not mandatory if pronunciation passes and common external alignment is used.

Rights and privacy are separate eligibility gates. Synthesis documentation does not settle commercial-use rights, retention, model-training use, regional processing, deletion, or contractual commitments for the actual account.

## Executable audition protocol

1. **Pre-register candidates.** Test at least three providers, with exactly one already-selected stock voice/configuration per provider. Record provider, API version, region, model ID/version, voice ID/version, locale, SDK version, account tier, complete request body excluding credentials, and documentation snapshot date. No custom or cloned voices.

2. **Lock common settings.**

   - Locale: `en-US`.
   - Input: the exact excerpt above, including punctuation and em dashes.
   - One synthesis request for the entire excerpt; no chunking or stitching.
   - Two independent scored repetitions with identical settings.
   - Seed: `8042026` when supported; record that a seed may still be only best-effort.
   - Speed/rate: provider-native `1.0`; pitch `0`; gain `0`; quality mode, with streaming/latency optimization disabled.
   - No music, EQ, compression, denoising, reverb, or time-stretching.
   - Fixed non-spoken instruction where supported:  
     `Reflective solo narrator. Read as a thoughtful investigation: intimate and warm, never a keynote or advertisement. Aim for 120–130 words per minute. Let punctuation create short reflective holds. Give “approved” genuine reassurance before the question introduces doubt. Keep time, confidence, and authority distinct. Deliver “ask the responsible owner—or stop” with restraint, not triumph. Do not add, omit, or paraphrase words.`
   - When free-form instructions are unsupported, record `instruction_support: none`; do not insert descriptive words into the spoken text.

3. **Pronunciation.** First render with unchanged text and no dictionary. The expected product-name reading is ordinary English “Body War,” with stress on the first word. If it fails, permit exactly one provider-native lexicon/phoneme correction without changing visible/spoken words. Discard the failed take from listening, retain it as evidence, lock the correction, and generate two new scored repetitions. Failure after that correction disqualifies the configuration.

4. **Capture raw evidence.** Use opaque UUID filenames such as `raw/ovp-aud-<render-uuid>.wav`. Store the provider mapping in a restricted key manifest. Preserve raw response bytes, SHA-256, request payload without secrets, response/request ID, UTC start/end, billed units, native format, duration, and native timing metadata. Mark raw files immutable. Never overwrite a regeneration.

5. **Create listening derivatives.** Decode each raw master once and produce mono 48 kHz, 24-bit WAV derivatives. Apply only two-pass BS.1770 loudness normalization to `-16 LUFS-I`, with true peak no higher than `-1 dBTP`. Do not trim silence or repair artifacts. Record the filter/tool version, input/output hashes, measured loudness, true peak, and applied gain. Raw masters remain decisive for technical inspection.

6. **Verify text and timing.** Forced-align every normalized clip locally against the exact excerpt. Require an exact normalized word sequence: no addition, omission, substitution, or reordered phrase. Confirm monotonic word boundaries within audio duration. Manually inspect “approved,” the question, all three terms in “time, confidence, and authority,” “Body War,” and “ask the responsible owner—or stop.” Preserve native provider timing separately; it is diagnostic, not caption authority. Derive audition VTT cues from the accepted waveform and check cue order, overlap, reading density, and complete coverage.

7. **Blind the clips.** Assign independent opaque names such as `B001.wav`; keep provider, voice, and repetition hidden. Generate a cryptographically random order after all files are frozen. Use a separately balanced order for each of at least three listeners, preventing the two repetitions of one candidate from appearing consecutively. Keep the unblinding key inaccessible until score sheets are locked.

8. **Listen under fixed conditions.** Same headphones, player, output level, and quiet room. Allow one replay per clip. Score each criterion from 1–5:

   - Reflective warmth/intimacy: 20%.
   - Naturalness and freedom from artifacts: 20%.
   - Semantic arc from reassurance through doubt: 20%.
   - Distinction and clarity of time/confidence/authority: 15%.
   - Pacing, breath placement, and ask-or-stop cadence: 15%.
   - Product-name and general pronunciation: 10%.

   Report median listening score by candidate and the spread across listeners and repetitions. A difference under three weighted points is a tie requiring a longer sequence test.

9. **Keep operational axes separate.**

   - **Editability:** pronunciation correction success, exact-text fidelity, repeat stability, timing usefulness, and ease of regenerating a bounded passage.
   - **Latency:** observed end-to-end duration for each scored request, same machine/region and sequential load. With two repetitions, report raw observations or median—not p95.
   - **Cost:** actual billed units for audition renders plus a same-day projection for the complete 1,543-word narration; do not substitute list-price memory.
   - **Rights:** stock-voice commercial permission, attribution/disclosure, redistribution, and termination effects reviewed by the responsible owner/legal reviewer.
   - **Privacy:** retention, training use, deletion, processing region, subprocessors, DPA availability, and account-specific logging controls reviewed by the privacy owner.

10. **Decide fail-closed.** First require rights/privacy approval and technical fidelity. Then rank subjective listening fit. Apply editability as a declared threshold or tie-breaker. Treat latency and cost as explicit constraints, never as hidden weights in a single “best provider” score.

Disqualify a configuration for altered words; an uncorrected key-term error; cloned/custom voice use; unrecoverable clipping, truncation, or non-speech artifacts; duration outside 75–120 seconds at the locked settings; inability to provide the required master format; missing reproducibility metadata; or failed rights/privacy review.

## What remains unknowable before rendering

Desk research cannot establish naturalness, warmth, semantic emphasis, question contour, pronunciation, cadence, artifact rate, between-run stability, actual duration, actual latency, billed cost, or edit quality. It also cannot show how a winner sustains continuity across the complete 12:30 narration, works with music and motion, supports waveform-aligned captions, or affects audience comprehension. Those remain empirical residue, and even a successful audition would prove only suitability for a longer prototype—not final production readiness.
