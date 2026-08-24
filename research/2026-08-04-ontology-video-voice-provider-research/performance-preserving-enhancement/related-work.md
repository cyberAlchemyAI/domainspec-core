# Route comparison

| Route | What it does | Keeps real timing/emotion | Voice transformation risk | External disclosure | Best use here |
|---|---|---:|---:|---:|---|
| **Local surgical restoration — RX 12** | Repairs selected defects; supports dialogue isolation, de-click, de-plosive, de-reverb, mouth de-click, voice denoise, and loudness tools | Highest | Low when conservative | None for local processing | **Primary quality/control route** |
| **Automatic mastering — Auphonic** | Levels, filters, normalizes loudness, limits peaks, and can reduce noise/reverb | High | Low–medium; aggressive processing can artifact | Web-service route uploads audio | **Fast consistency pass after restoration** |
| **Cloud enhancement — Adobe Enhance Speech v2** | One-click speech cleanup and source separation with adjustable strength on the documented premium route | High | Medium; provider warns to reduce strength if robotic | Upload required | **Fastest proof of concept** |
| **Local neural enhancement — Resemble Enhance** | Denoising or generative bandwidth/speech reconstruction | High | Denoise-only: low–medium; enhancer: medium–high | None when run locally | **Open/local experiment; begin with denoise-only** |
| **Speech-to-speech — ElevenLabs Voice Changer** | Re-synthesizes a source performance into a target voice | High by design | High: the output is a new synthetic signal | Upload/API request required; zero retention documented as Enterprise-only | **Optional second lane, not default cleanup** |

## Interpretation

The user's idea is real, but it describes two routes:

1. **Enhance my recording:** retain the captured voice and repair/master it.
2. **Use my performance to drive a clone:** retain delivery while synthesizing a target voice.

The first route directly solves the “mechanical reading” problem because the person supplies the performance. The second may smooth tone or consistency, but it can reintroduce synthetic character and should be evaluated separately.

## Recommended chain

`human recording -> immutable raw -> conservative restoration -> gentle mastering -> blind comparison -> narrator approval`

Only if this fails:

`approved recording -> speech-to-speech conversion -> identity/artifact comparison -> separately labeled decision`
