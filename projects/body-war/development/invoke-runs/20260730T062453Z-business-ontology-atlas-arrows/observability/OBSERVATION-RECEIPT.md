# Observation Receipt

## Distill Child

- run:
  `distill-body-war-business-ontology-atlas-arrows-20260730T062453Z`
- result: recorded
- central ledger: `.arcanum/observability/signals/sigil-invocations.jsonl`
- ledger line: 430
- by-sigil index: `.arcanum/observability/by-sigil/distill.jsonl`, line 22
- parent linkage:
  `invoke-body-war-business-ontology-atlas-arrows-20260730T062453Z`
- quality bar: pass
- observer trigger: `gap-threshold`
- recommendation: `reflect-now`

## Invoke Parent

- run:
  `invoke-body-war-business-ontology-atlas-arrows-20260730T062453Z`
- result: recorded
- central ledger: `.arcanum/observability/signals/sigil-invocations.jsonl`
- ledger line: 431
- by-sigil index: `.arcanum/observability/by-sigil/invoke.jsonl`, line 91
- quality bar: pass
- observer trigger: `gap-threshold`
- recommendation: `reflect-now`

The observer derives trigger state from repository counters. It is
non-blocking and changes neither the Distill verdict nor mutation authority.
