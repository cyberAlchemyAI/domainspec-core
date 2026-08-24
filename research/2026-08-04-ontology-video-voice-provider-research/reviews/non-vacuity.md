**Verdict: REPAIR**

The 237-word frozen excerpt and 75–120 second acceptance window are concrete. The normalization, blinding, repetition, hard-gate separation, listener scoring, and raw-artifact retention are directionally sound. However, no shortlisted provider yet has a fully specified, authorized, reproducible witness route. Quality remains correctly unclaimed.

| Provider | Witness route supported by cited official documentation | Missing witness evidence | Decision |
|---|---|---|---|
| Microsoft Azure Speech | **Partial.** AZ-1 documents standard voices at 24/48 kHz and SSML pronunciation, rate, pitch, volume, pauses, and lexicons. AZ-2 permits ten minutes and 64 KB SSML per real-time request, sufficient in principle for the excerpt. | No selected stock-voice ID, region, REST/SDK route and version, native output-format enum, complete SSML/request body, or account tier. AZR-3 does not close output ownership or public-video permission. Actual agreement, retention, and privacy configuration remain open. | **REPAIR through TC/RP feedback.** Keep only if every missing field and hard gate is positively bound before rendering; otherwise **KILL**. |
| Google Cloud TTS, Chirp 3: HD | **Partial.** GC-1 documents synchronous LINEAR16, a named stock-voice request shape, and Preview pace/custom-pronunciation controls. Common external alignment is permissible. | GC-1 does not bind a native sample rate meeting the ≥24 kHz master gate or the one-request input limit. No selected voice/location/endpoint/client version/request body exists. Preview acceptance, public-distribution permission, actual agreement, and privacy configuration remain open. | **REPAIR through TC/RP feedback.** Prove sample rate and excerpt capacity, freeze the configuration, and close gates; otherwise **KILL**. |
| OpenAI speech API | **Partial.** OAI-1 documents prompted delivery and WAV/PCM, with PCM specified as 24 kHz/16-bit. OAI-2 documents a 2,000-token limit and version-locking via `gpt-4o-mini-tts-2025-12-15`. | The excerpt’s exact token count, stock voice, full request body, SDK version, and account tier are not frozen. No cited native pronunciation dictionary, timestamps, seed, numeric pitch, or gain controls exist. Selected-voice/public-use terms, disclosure handling, actual agreement, retention, and account data controls remain open. | **REPAIR through TC/RP feedback.** Unsupported controls must be recorded as unsupported and omitted. If “Body War” fails on the first take, this route has no documented correction path and is **KILLED**. Any unclosed hard gate also **KILLS** it before rendering. |
| ElevenLabs | Technically supports the witness, but reviewed click-through rights/training/retention posture fails current data gates. | Enterprise no-training, deletion/retention, DPA, and stock-voice terms. | **KILLED from this audition.** Reopen only through RP feedback with positive enterprise evidence. |
| Amazon Polly | The cited production path has an unresolved 24-versus-16 kHz conflict. | Path-specific master format plus training-use, retention, and rights closure. | **KILLED from this audition/control set** until TC/PA/RP feedback resolves every conflict. |
| Cartesia | Controls and timing are promising, but full-excerpt request capacity and acceptable pre-upload data terms are absent. | Capacity, ZDR/no-training, retention, and commercial/public-use closure. | **KILLED from this audition.** Enterprise repair may reopen through TC/RP feedback. |
| PlayHT / PlayAI | Operative legal evidence, pricing, pronunciation, and alignment remain unavailable. | Multiple capability and every required legal/data gate. | **KILL.** No current witness route. |
| Hume | Lossless/continuation route exists, but versioned control/timestamp features and policy posture conflict. | Terms/API-policy reconciliation, retention/deletion, Preview acceptance, and exact configuration. | **KILLED from this audition.** Reopen only through TC/RP feedback. |

### Affected evidence rows

- Hard requirements: `Reproducibility`, `Master format`, `Exact-text fidelity`, `Commercial/public use`, `Output rights`, `Data use`, `Retention/privacy`, `Selection`, and `Quality claim`.
- Provider rows and bindings: OpenAI `OAI-1/OAI-2/OAIR-1/OAIR-2`; Azure `AZ-1/AZ-2/AZR-1/AZR-3`; Google `GC-1/GCR-1/GCR-2/GCR-3`.
- Sections: `Conditional desk-research shortlist`, `Generation lock`, `Pronunciation and evidence capture`, and `Verification and listening`.

### Exact repairs and kill rules

1. Through the declared explorer-feedback edge, add one immutable candidate manifest per survivor containing the exact provider, endpoint/method, model snapshot or documented version state, stock-voice ID, locale, region/location, account tier, SDK/client and version, native output enum/sample rate/bit depth/channels, exact excerpt byte/token count versus request limit, and complete redacted request body.

2. Replace the generic generation lock with provider-specific fields. Never claim `seed`, numeric rate/pitch/gain, quality mode, latency optimization, pronunciation correction, or native timestamps when the selected route does not expose them. Record `unsupported/not exposed` and omit invented parameters.

3. Positively close actual-plan commercial/public-video permission, output rights, disclosure/attribution, training use, retention/deletion, region, and applicable agreement before any upload. Unknown is a hard failure. A row not closed by explorer feedback is **KILLED**, not carried as a conditional audition candidate.

4. Make verification executable: freeze tool names, versions, exact normalization/decoding and alignment commands, excerpt-to-VTT cue mapping, timing tolerance, UUID manifest, randomized-order manifest, and protected unblinding key. Forced alignment against supplied text cannot alone prove no omission or substitution; require an independent transcription or token-by-token listening audit plus low-confidence/manual-review rules.

5. Freeze the scoring formula and anchors, define “three weighted points” on an explicit scale, and preserve raw responses, failed takes, derivatives, request/response metadata, hashes, score sheets, order manifests, caption/timing results, and hard-gate decisions.

No candidate may be rendered under the present evidence state. Desk research and vendor documentation establish only possible routes; no audible quality, duration, fidelity, pronunciation, caption accuracy, or winner has been established.
