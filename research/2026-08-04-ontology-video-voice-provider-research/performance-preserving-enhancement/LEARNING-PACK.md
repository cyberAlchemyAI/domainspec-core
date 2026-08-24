# Learning pack: keep the performance, improve the recording

## The answer

Yes—this route exists, and it is probably a better fit than voice cloning for the immediate problem.

The narrator records the story with the real rhythm, accent, breaths, hesitation, and emotional transitions. Post-production then removes distractions and makes the level consistent. The system does not need to invent the performance.

## Recommended route

### Lane A — default

1. Record the real narration in a quiet, soft room with a close microphone.
2. Keep the original WAV untouched.
3. Repair only defects that are actually present: clicks, plosives, steady noise, excessive room reverb, or clipping.
4. Apply gentle EQ, de-essing, compression, loudness normalization, and peak limiting.
5. Compare the result against the raw recording at matched loudness.
6. Accept it only if it is cleaner **and still unmistakably the same person and performance**.

The best controlled implementation is a local restoration editor such as RX 12. Auphonic is a useful automatic finishing lane. Adobe Enhance Speech v2 is the quickest cloud experiment, but its own guidance acknowledges that excessive enhancement can sound robotic. Resemble Enhance offers a local open implementation; start with `--denoise_only`, because its full enhancer includes generative reconstruction.

### Lane B — optional

Feed the real performance into speech-to-speech conversion targeting an authorized clone of the narrator. This preserves timing and delivery more directly than text-to-speech, but it still re-synthesizes the voice. Treat it as a separate `voice-converted` derivative and test identity, pronunciation, artifacts, privacy, and retention independently.

For the current film, Lane B should be a fallback for selected passages—not the baseline.

## First audition

Use a 30–45 second passage containing:

- one warm explanatory statement;
- one turn from reassurance to doubt;
- the words “time, confidence, and authority”;
- one intentional pause;
- one natural breath that should remain.

Create these opaque, loudness-matched candidates:

- raw recording;
- conservative local restoration;
- restoration plus automatic mastering;
- one automatic enhancer, only if its execution boundary is approved.

Score each from 1–5 for intelligibility, naturalness, recognizable identity, preservation of emotional meaning, artifacts, and listening comfort. Reject any candidate that alters words, clips consonants, flattens the emotional turn, removes meaningful pauses/breaths, or sounds less like the narrator.

Do not include speech-to-speech in this first comparison. If Lane A cannot reach the target, run it as a separately governed second audition.

## Decision

**Proceed with record + restore + master. Defer voice cloning and speech-to-speech until the real recording proves it is necessary.**

This is an evidence-backed design recommendation, not an audible winner. The next honest proof is a short recording and a blind comparison, as specified in [L2 — closure plan](levels/L2-closure-plan.md).
