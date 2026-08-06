# L2 — closure plan

The next step should be a bounded empirical run, not more provider prose.

1. Record one 30–45 second passage in the intended delivery and room.
2. Preserve the 48 kHz, 24-bit WAV as immutable raw and record its SHA-256.
3. Produce, at most, four derivatives:
   - conservative local surgical restoration;
   - local denoise-only;
   - one automatic cloud-enhancement result, only if upload is authorized;
   - restored-plus-mastered output.
4. Do not use automatic filler, silence, or breath cutting in the first comparison.
5. Loudness-match the comparison files so louder is not mistaken for better.
6. Blind the files and score intelligibility, naturalness, identity, emotional arc, artifacts, and listener fatigue separately.
7. Select the lightest chain that clears all gates in [closure-gates.md](../gates/closure-gates.md).
8. Use speech-to-speech only in a second experiment, and label it `voice-converted`.

## Evidence-harness handoff

The empirical run should be represented as a `research-evidence-harness` fixture with immutable inputs, exact tool/version/parameter manifests, hashes, randomized listening order, raw score sheets, and a named owner verdict. This tower does not execute that run.
