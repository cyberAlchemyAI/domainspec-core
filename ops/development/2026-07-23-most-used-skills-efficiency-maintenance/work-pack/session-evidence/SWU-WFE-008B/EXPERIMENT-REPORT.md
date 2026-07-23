# Experiment Report: SWU-WFE-008B

- Verdict: `PASS`
- Isolated bootstrap generation: pass
- Live generated parity: pass
- Per-runtime semantic body digest:
  `124c4f7cb424df867736c7900619e06746baeaf0155a1d29dae89b7f94053cb6`
- Runtime-overlay causal fixtures: 15/15

## Generated composition

| Runtime | Canonical controls | Local fragments | Local copied files | Result |
| --- | ---: | ---: | ---: | --- |
| Codex | 6/6 | 3/3 | 3/3 | pass |
| Claude | 6/6 | 3/3 | 3/3 | pass |

Both runtimes retain canonical `business_plan` and `live_presentation` support.
Both receive `product_research_blueprint` only from the private manifest
payload.

## Isolation proof

The forceful bootstrap ran in `/tmp`, where all non-Whisper generated packages
were disposable. Only the two validated Whisper directories were copied to the
live repository. Their live file trees matched the isolated generated trees
exactly after synchronization.

## Boundary

No private preset content was added to public Arcanum. This proof does not
promote Whisper or publish either repository.
