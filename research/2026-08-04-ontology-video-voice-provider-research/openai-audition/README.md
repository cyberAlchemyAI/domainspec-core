# OpenAI Stock-Voice Audition

This package defines, designs, and plans a bounded OpenAI speech audition for the ontology educational video. It does not implement the runner, use credentials, call the provider, generate audio, approve a voice, or authorize public use.

## Start here

1. [SPEC.md](SPEC.md) defines the audition contract.
2. [DESIGN.md](DESIGN.md) shows the fail-closed architecture and six required views.
3. [WORK-PACK.md](WORK-PACK.md) is the executable planning control panel.
4. [INVOKE-RESULT.md](INVOKE-RESULT.md) records the lifecycle result and next decision.

## Current boundary

- Provider lane: OpenAI speech API, stock voices only.
- Frozen text: [audition-excerpt.txt](audition-excerpt.txt), 237 words.
- Planned model: `gpt-4o-mini-tts-2025-12-15`, subject to later account availability verification.
- Planned output: non-streaming WAV.
- Current admission: `not_ready`.
- Selected voice: none.
- Selected SWU: none.

The package is candidate-local planning evidence. It is not legal advice, procurement approval, provider entitlement, implementation proof, render proof, or voice-quality evidence.
