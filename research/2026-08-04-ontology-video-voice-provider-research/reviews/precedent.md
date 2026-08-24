**Verdict: REPAIR**

## Searched selectors

- Current Inventory: `.arcanum/inventory/index.json` for `voice provider`, `text-to-speech`, `TTS`, narration, cloning, provider names, Runway, and Whisper.
- Current strategy packet: `unresolved_gaps`, `excluded`, and `non_authority_notice`.
- Repository-wide provider-decision searches: provider names near `selected`, `approved`, `chosen`, `contract`, `vendor`, `using`, and `deployed`; narration/voice terms near privacy, retention, agreement, and production constraints.
- Target source package:
  - `educational-video-voiceover.md:1-12,118-136`
  - `educational-video-construction-plan.md:15-65,101-103`
  - `educational-video-validation.md:20-74`
- Prior production precedents:
  - `arcanum/development/craft/teaching/craft-cyberalchemy-video-2026-07-15/README.md:1-21,62-81`
  - `.../RUNWAY-AGENT-PRODUCTION-BRIEF.md:1-61`
  - `.../VALIDATION-REPORT.md:1-53`
  - `arcanum/docs/RUNWAY-AGENT-PRODUCTION-BRIEF.md:1-48,760-788`

## Findings

1. **No owned or deployed narration-provider decision found.** The search found no source-selectable vendor contract, provider SKU, account, accepted waveform, or deployed narration system for the target ontology video. This is a bounded precedent-clean result over the searched repository and Inventory surfaces, not proof that no external ownership exists.

2. **One real owner exists: build-from-owned text-package constraints.** The target source binds the exact English text, one reflective solo narrator, thoughtful-investigation delivery, 120–130 WPM, natural breaths, and avoidance of keynote/advertising delivery (`educational-video-voiceover.md:1-12`). It does **not** bind provider, stock voice identity, accent, locale, gender presentation, cloning, or production platform. It is not already deployed: no recording, animation, mix, or render exists (`educational-video-validation.md:65-74`).

3. **The synthesis correctly treats approval as editorial approval, not provider approval.** Its non-spoken instruction at `synthesis.md:156-160` preserves the owned style. The conditional shortlist and `synthesis.md:10-12,30` correctly deny provider approval and render authorization.

4. **The synthesis silently strengthens locale precedent.** `synthesis.md:150` locks locale to `en-US`, while the Inventory packet explicitly states that accent and concrete speaker identity are unspecified (`strategy-inventory-packet.json:120-125`). English script language does not establish an American accent or locale.

5. **Runway precedents are non-binding, build-from-owned handoffs for other artifacts.**
   - The Craft/CyberAlchemy package defines a voice profile and instructs Runway to create narration, but its validation says voice generation remains unreviewed and pending (`VALIDATION-REPORT.md:7-11,39-53`; `README.md:76-81`). “Selected voice model” at `README.md:13-14` is an unresolved generic slot, not a named provider decision.
   - The Refine X-ray Runway brief is explicitly “unexecuted at authoring time” and “unvalidated as an executed Runway Workflow or finished animation” (`arcanum/docs/RUNWAY-AGENT-PRODUCTION-BRIEF.md:1-8,783-788`).
   - Neither precedent binds the ontology-video provider or platform.

6. **“Provider review” is not a narration-provider mention.** At `educational-video-voiceover.md:126` and the corresponding production-script row, it names review of a proposed memory in the Augmentor lane. The synthesis does not misread it as TTS ownership.

7. **Privacy precedent remains clean.** No target-owned provider privacy agreement was found. The synthesis appropriately leaves account-specific data use, retention, agreement, and public-use gates open.

## Affected synthesis rows

- `Hard requirements → Reproducibility` (`synthesis.md:19`), specifically locale ownership.
- `Fixed blind-audition protocol → Generation lock` (`synthesis.md:146-150`).
- No provider-comparison or shortlist row requires removal or recommendation changes.

## Exact repairs

1. Add an owner/precedent row to hard requirements:

   `Owned narration contract — build-from-owned: exact English script; reflective solo narrator; thoughtful investigation; 120–130 WPM; not keynote/advertisement. Provider, voice identity, accent/locale, gender presentation, cloning, and production platform remain owner-unset. No deployed narration or accepted waveform exists.`

2. Replace `locale en-US` at `synthesis.md:150` with:

   `spoken_language: English; locale/accent: owner-unset; record the actual provider locale and voice accent.`

3. Add this execution guard:

   `Before any account action or upload, the operator must select a common audition accent/locale or explicitly approve provider-native accent variation. If en-US is selected only as an experimental control, label it test-only and not inherited owner approval.`

4. Add a bounded precedent note stating that prior Runway handoffs and “selected voice model” language belong to other, unrendered artifacts and do not establish a narration provider for this video.
