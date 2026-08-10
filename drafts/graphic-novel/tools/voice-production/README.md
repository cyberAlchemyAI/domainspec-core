# Voice Production L0 Synthetic Workflow

This candidate assembles the existing voice-production contracts into one
deterministic, local demonstration. It compiles the exact Chapter 1
`speaker,line` CSV, derives a three-segment toy selection in source order, and
exercises the provider-neutral segment and composite adapter seams. The CLI
prints a redacted canonical JSON summary containing only digests, counts,
bounded status labels, proof booleans, and zero-effect counters.

Run from the repository root with CPython 3.12:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3.12 \
  drafts/graphic-novel/tools/voice-production/voice_workflow.py \
  drafts/graphic-novel/chapter-01/audio/elevenlabs-voiceover-studio.csv
```

The workflow proves these synthetic contracts:

- exact Chapter fixture bytes, row order, text, speakers, and bracket-tag count;
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
