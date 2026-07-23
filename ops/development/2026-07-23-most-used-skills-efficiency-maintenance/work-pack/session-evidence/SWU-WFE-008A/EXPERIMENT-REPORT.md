# Experiment Report: SWU-WFE-008A

- Verdict: `PASS`
- Generic composition fixtures: 15/15
- Live manifest schema: pass
- Live manifest admission: pass
- Public/private scan: pass

## Negative controls

- stale canonical digest;
- protected gate removal with a recomputed base digest;
- undeclared preset directory;
- preset payload or fragment digest mismatch;
- replacement rather than additive insertion;
- unsafe copied-file destination;
- fragment reference to an undeclared preset;
- generated protected-control removal;
- undeclared generated semantics or metadata;
- missing generated payload.

## Positive controls

- declared additive preset and metadata;
- exact-anchor fragment composition;
- generated body plus copied payload parity;
- current Whisper manifest with three fragments, three copied files, two
  runtimes, and six protected controls.

## Boundary

This report admits the composition manifest. Generated Whisper runtime parity
remains the separate SWU-WFE-008B transaction.
