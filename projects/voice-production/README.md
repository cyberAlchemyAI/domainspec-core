# Voice Production L0 Synthetic Workflow

This project owns the reusable voice-production contracts and their current
deterministic, local demonstration. Its chapter-neutral compiler requires an
explicit closed config for every `speaker,line` source; it has no built-in
Chapter 1 paths, digests, speakers, or counts. The workflow derives a
three-segment toy selection in source order and exercises the provider-neutral
segment and composite adapter seams. The CLI prints a redacted canonical JSON
summary containing only digests, counts, bounded status labels, proof booleans,
and zero-effect counters.

Lucifer's Lights continues to own the Chapter 1 CSV and production guide. This
project consumes the CSV as an integration fixture; it does not make that
creative derivative part of the reusable package authority.

Run from the repository root with CPython 3.12:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3.12 \
  projects/voice-production/voice_workflow.py \
  projects/lucifers-lights/drafts/graphic-novel/chapter-01/audio/elevenlabs-voiceover-studio.csv \
  projects/lucifers-lights/factory/voice/chapter-01.json \
  projects/lucifers-lights/development/chapter-factory-runs/chapter-01-pilot/voice-handoff.json \
  --repo-root .
```

The Chapter Factory emits
`development/chapter-factory-runs/chapter-01-pilot/voice-handoff.json`. That
artifact now binds the accepted Chapter 1 manuscript, its author-decision
receipt, synchronized performance script, compiler config, and exact ChapterRun.
The CLI rejects drift in those bindings before it compiles. Admission is
strictly `local-compile-only`: it is not permission to resolve credentials,
select provider voices, synthesize audio, spend budget, or publish media.

The workflow proves these synthetic contracts:

- exact Chapter fixture bytes, row order, text, speakers, and bracket-tag count;
- byte-for-byte parity for the prior Chapter 1 manifest plus a materially
  different synthetic chapter using explicit row selection;
- content-, selection-, binding-, transport-, adapter-, schema-, policy-, and
  effect-field digest sensitivity;
- one correlated expected output per segment and one honest composite output;
- unknown composite segment state and denial of unsupported segment retry;
- mandatory capability and unapproved text-projection blocking;
- authorization rejection before credential resolution;
- evidence-bound normalized and gate receipts;
- accepted-work exclusion, unknown-effect reconciliation, and a newly
  authorized bounded retry.

The seam accepts injected adapter objects implementing the local preparation
protocols. No provider SDK or provider-specific identifier is part of this L0
surface.

## Boundary

The only supported claim is: “the synthetic seam passed the declared
no-network contract tests.” This candidate performs no provider call, account
check, credential lookup, network or DNS request, audio generation, external
message, publication, deployment, or production operation. A passing result
does not establish provider compatibility, account authorization, cost or
quality acceptance, provider replaceability, release readiness, or production
readiness.

## Explicit live audition runner

`run_elevenlabs_audition.py` is a separate effect-owning boundary. Its default
mode validates exact source, compiler, manifest, segment, provider, budget, and
output bindings without resolving a secret or contacting ElevenLabs. The
`--execute` switch permits exactly the one request declared by the supplied
config. It consumes `elevenlabs/api-key` inside the local Secret Store callback,
writes a no-overwrite MP3 plus a redacted receipt, and never sends a credential
to the browser or stores one in configuration.

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3.12 \
  projects/voice-production/run_elevenlabs_audition.py \
  projects/lucifers-lights/factory/voice/chapter-01-system-connectivity-audition.json \
  --repo-root .
```

Add `--execute` only for an explicitly authorized paid provider generation.
The current Chapter 1 configuration is one SYSTEM-line connectivity evidence
sample. Its River voice binding is non-canonical and does not accept the cast,
the audio, or the manuscript for publication.

Quality auditions may bind the selected line to neighboring manifest segments
through `previous_text` and `next_text` while still generating only that one
line. The Chapter 1 Sarah/Bella comparison uses Multilingual v2, the same
best-effort seed and settings, and distinct no-overwrite raw outputs. Each
configuration remains one paid call and neither voice becomes canonical merely
because generation succeeds.

`master_elevenlabs_audition.py` is the separate, provider-free mastering edge.
It verifies the canonical live-audition receipt and raw MP3 digest, then uses the
shared pinned Playwright/Chromium runtime to derive a 48 kHz, 24-bit stereo WAV.
The current `lucifers-lights-halo-v2` reference profile keeps the dry voice
centered and adds a filtered stereo plate return with 34 ms pre-delay, a
1.2-second RT60, a 1.7-second render tail, gentle compression, -18 dB RMS
level matching, and a -1.5 dBFS ceiling. Raw audio is never changed, and the
master receipt binds the source, profile, processor, metrics, and output digest.

`lucifers-lights-slow-dark-v3` is the conservative performance revision. It
retains the v2 Halo space, renders the provider take at 0.95 playback rate, and
reduces the dry high shelf by 1 dB at 3.2 kHz. Because browser playback-rate
resampling is not pitch-preserving, the same adjustment lowers pitch by about
89 cents; the receipt reports that identity-affecting change explicitly. The
renderer expands its output frame count before processing so the full reverb
tail remains intact.

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3.12 \
  projects/voice-production/master_elevenlabs_audition.py \
  <raw-audition-receipt.json> \
  projects/lucifers-lights/factory/voice/lucifers-lights-halo-v2.json \
  <master.wav> <master-receipt.json> \
  --repo-root .
```

The default command is validation-only. Add `--execute` to perform the local
offline render. This stage makes no network request, resolves no secret, spends
no provider budget, and grants no casting, manuscript, publication, or release
authority.
