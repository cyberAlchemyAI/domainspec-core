# Claim ledger

| ID | Claim | Source kind | Evidence | State |
|---|---|---|---|---|
| C1 | RX 12 exposes surgical dialogue-restoration modules suitable for noise, reverb, clicks, plosives, mouth noise, and loudness work. | primary-source | RX-1 | observed |
| C2 | Adobe Enhance Speech v2 accepts uploaded recordings and automatically reduces noise/reverb; enhancement strength can be adjusted on the documented paid route. | primary-source | ADOBE-1, ADOBE-2 | observed |
| C3 | Adobe itself advises reducing enhancement if the result becomes robotic. | primary-source | ADOBE-2 | observed |
| C4 | Auphonic combines restoration, adaptive leveling, loudness normalization, and true-peak limiting, with controls that can retain some ambience, reverb, and breath. | primary-source | AUPH-1 | observed |
| C5 | Auphonic warns that aggressive noise reduction can create artifacts. | primary-source | AUPH-1 | observed |
| C6 | Resemble Enhance can run locally and offers a denoise-only path distinct from its generative enhancer. | related-source | RESEMBLE-1 | observed |
| C7 | ElevenLabs Voice Changer is speech-to-speech conversion and documents control over emotion, timing, and delivery. | primary-source | EL-STS-1 | observed |
| C8 | ElevenLabs Voice Changer re-synthesizes into a target voice; it is not simply restoration of the input waveform. | primary-source + operator-reading | EL-STS-1 endpoint semantics | observed/inferred |
| C9 | Recording the performance first is a better architectural fit for the approved narration contract than stock text-to-speech. | local-inference | LOCAL-1 plus C1–C8 | recommended, not audibly proved |
| C10 | Local restoration should be tried before any cloud or voice-conversion route because it minimizes identity transformation and external disclosure. | local-inference | Route properties in C1–C8 | recommended, account/privacy proof open |
| C11 | Any of these tools will make this narrator sound better. | open-residue | No waveform or listening panel exists | unknown |
| C12 | A particular chain or parameter setting preserves the narrator's voice identity. | open-residue | No A/B evidence exists | unknown |

See [sources.md](sources.md) for exact bindings.
