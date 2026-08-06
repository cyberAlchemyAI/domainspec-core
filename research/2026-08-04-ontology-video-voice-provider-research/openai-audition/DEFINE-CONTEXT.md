# Define Context

Context budget: Standard. Selected files: 7. Selected source regions: under 280 lines. Inventory was lookup-ready but returned no direct OpenAI-audition implementation precedent; direct owner sources were used.

## Intent

Define a local, reproducible, fail-closed audition for one OpenAI stock voice reading the frozen ontology-video excerpt. The audition exists to create comparable evidence about the voice, tone, accent, pronunciation, pacing, and semantic delivery that the user considers most important.

## Evidence obligation matrix

| Obligation | Source | Define consequence |
|---|---|---|
| Preserve the approved script and rhythm | SRC-04 through SRC-06 | Freeze exact excerpt; narration words cannot be edited during audition. |
| Keep provider admission fail-closed | SRC-01 through SRC-03 | `not_ready` remains the initial state; documentation alone cannot open rendering. |
| Bind an exact route | SRC-01, SRC-02, provider docs | Manifest must bind model snapshot, voice ID, instructions, format, counts, account qualifiers, and redacted request. |
| Keep quality empirical | SRC-01, SRC-02 | No voice-quality claim exists until waveforms and locked score sheets exist. |
| Protect authority boundaries | SRC-01, SRC-02, SRC-06 | Scores advise; the named production operator decides `approve`, `reject`, or `defer`. |
| Respect provider disclosure | Official OpenAI guide | AI-generated-voice disclosure is acceptance-critical. |
| Reject unsupported pronunciation repair | SRC-01, SRC-02, provider docs | A failed “Body War” first take rejects the configuration. |
| Avoid credential leakage | Execution safety boundary | Credential comes from process environment only and is never written, logged, hashed, or included in receipts. |

## Explicit exclusions

- No API call, upload, account action, terms acceptance, purchase, render, or listening test.
- No custom or cloned voice.
- No full 12:30 narration.
- No waveform processing, forced alignment, caption generation, or public release.
- No provider winner, voice approval, legal conclusion, or production-readiness claim.
- No mutation outside `openai-audition/` during this Invoke authoring run, except its linked observability envelopes.

## Open decisions carried forward

1. Owner-selected common accent/locale or explicit provider-native variation.
2. One exact stock voice ID; `marin` and `cedar` are documented recommendations, not an automatic selection.
3. Named production operator for the terminal decision.
4. Actual-account public-use, agreement, privacy/data-use, retention/deletion, and security gates.
5. Exact tokenizer/count route and exact frozen-excerpt token count.
6. Pinned decoding, BS.1770 normalization, forced-alignment, independent-fidelity, VTT, and randomization tools.
