# Lucifer's Lights — Chapter 01 ElevenLabs Guide

Status: synchronized to the accepted Chapter 1 manuscript; local compile ready; voice casting, synthesis, timing, and final listen pending

Transport: candidate motion-comic voiceover

Script: `elevenlabs-voiceover-studio.csv`

Accepted manuscript SHA-256: `eb89135bb53d2c8106b26e8005a1c45738bd84a3a2b06b9e64518c9c64fbe2a5`

Spoken length: 1,488 words across 112 clips

Estimated duration: about 11.4 minutes at 130 WPM, or 12.4 minutes at 120 WPM, before extended pauses

## Recommended generation path

Use ElevenLabs Studio or Voiceover Studio and import `elevenlabs-voiceover-studio.csv` as a `speaker,line` script. Assign one voice to each named speaker before generation. Generate a short audition from KF01, KF07, and KF16 before spending credits on the full sequence.

The script uses a small number of square-bracket performance tags. Use **Eleven v3** if those tags remain in the input. If using Multilingual v2 or another model, remove the bracketed tags first because non-v3 models may read them aloud. Eleven v3 does not use SSML break tags; punctuation and audio tags control its pauses.

This package does not contain an API key, voice IDs, generated speech, music, or sound effects.

## Speaker casting

| Speaker | Performance target | Starting point |
|---|---|---|
| LUCIFER | Warm low register; intimate, elegant, precise, amused beneath the words. Human and charismatic—not a theatrical demon or growling villain. Use the same voice for narration and dialogue. | Natural stability; speed around 0.94–0.97. |
| MARA | Woman in her mid-twenties; exhausted but alert. Restrained fear develops into deliberate resolve. | Natural stability; speed around 0.97–1.00. |
| RUTH | Older woman; dry, economical, and formidable without caricature. | Natural or Robust stability; speed around 0.95–0.98. |
| ELENA | Distinct from Mara but plausibly related; protective, intimate, and urgent. Add telephone/recording treatment in post rather than forcing it through the voice prompt. | Natural stability; speed around 0.96–0.99. |
| SYSTEM | Neutral, clean, restrained synthetic delivery. It reads only interface evidence. It is not Michael. | Robust stability; speed around 1.00. |

Treat all settings as audition starting points. Voice choice has more influence than tags, and ElevenLabs generation is nondeterministic.

## Pronunciation lock

- Vesper: **VES-per**
- Mara: **MAH-rah**
- Elena: **eh-LAY-nuh**
- Vale: **VAYL**
- Orison: **OR-ih-sun**
- Lucifer: **LOO-si-fer**
- Michael: **MY-kul**

The script already spells timestamps and locker 318 as spoken words. Test the proper nouns in the audition before generating the complete track. Use a pronunciation dictionary or Eleven v3 IPA only if the selected voices mispronounce them.

## Keyframe-to-clip map

The line numbers below refer to the CSV file, including its header on line 1.

| Keyframe | CSV lines | Beat |
|---|---:|---|
| KF01 | 2–4 | Vesper, Halo, rain, and the train-timed privacy rule |
| KF02 | 5–11 | Mara meets Lucifer and the Light arrives |
| KF03 | 12–19 | Elena request, invasive app access, and definition of a Light |
| KF04 | 20–28 | Open-favor price, rules, and consequence |
| KF05 | 29–37 | Lucifer's contested mythology and knowledge as the first Light |
| KF06 | 38–43 | Accept, blackout, and contract conflict |
| KF07 | 44–57 | Elena's prior Light and Lucifer's refusal to undo it |
| KF08 | 58–67 | Voluntary amendment and approaching pursuers |
| KF09 | 68–73 | Ruth, moth key, and locker 318 |
| KF10 | 74–77 | Train cover and Ruth's coffee diversion |
| KF11 | 78–83 | Flooded-alley escape and Vesper's second map |
| KF12 | 84–89 | Bracelet tracker and Elena's scheduled message |
| KF13 | 90–94 | Hair seal and locker dead drop |
| KF14 | 95–101 | Mara rejects the train escape and chooses to listen |
| KF15 | 102–105 | Elena's recording and tracker discovery |
| KF16 | 106–113 | Michael's request, true-name offer, and footsteps |

Hold longer on KF06, KF07, KF14, and KF16. The quicker transition cluster is KF09–KF13. Final timings must come from the rendered audio, not these text estimates.

## Performance guardrails

- Lucifer's jokes should sound effortless and slightly inappropriate, never announced as punchlines.
- His mythology is his interested interpretation, not neutral religious exposition.
- Mara reads the amendment, accepts it, chooses to stay, and opens the bracelet herself. Do not perform her as passive or hysterical.
- The word **Light** should receive mild emphasis when it means the service or contract, not every time it appears.
- Do not give Michael a voice or reveal his identity.
- Keep rain, train, café, phone, and recording effects on separate post-production layers so dialogue remains intelligible.
- If a tag is spoken aloud or produces an exaggerated result, remove that tag and direct the voice through casting, punctuation, or paragraph settings.

## Audition and acceptance

Generate these three samples first:

1. Opening: CSV lines 2–11.
2. Contract tension: CSV lines 47–64.
3. Final reveal: CSV lines 102–113.

The full generation is ready only when:

- the CSV imports as exactly five speakers and 112 clips;
- Lucifer remains one consistent voice across narration and dialogue;
- the named pronunciations are correct;
- no performance tag is spoken;
- contract logic remains clear in audio;
- Mara's agency is audible at the amendment, train, and bracelet moments;
- Elena sounds like a recording without losing intelligibility;
- no line is clipped, reordered, duplicated, or masked by effects.

## Whisper result

- Spell: whisper
- Transport: motion-comic voiceover
- Transport proof status: candidate
- Objective: turn the approved Chapter 01 into an ElevenLabs-ready performance aligned to sixteen keyframes
- Target public: adult dark urban-fantasy and neo-noir graphic-novel audience
- Intent state: frozen for this candidate cut
- SCU cores: intimate dangerous charm; clear transaction and agency; request-to-cliffhanger movement
- Candidate selected: multi-voice compressed cut, preserving Lucifer as narrator
- Composition plan: sixteen image-aligned beats, five speakers, sparse v3 direction tags
- Draft status: pass for accepted-manuscript synchronization and local compilation; synthesis remains pending
- Human gate: pending voice audition
- Delivery flow: active
- Validation: CSV structure and word-count checks passed; audio checks pending
- Learning residue: full prose is too long for sixteen mostly static images; future audiobook and motion-comic cuts should remain separate
- Next route: voice audition, then timed animatic
