# Invoke Observability Receipt

## Recorded Signals

| Capability | Run ID | Central ledger line | Result |
| --- | --- | ---: | --- |
| Distill child | `distill-body-war-ontology-focus-scene-pivot-20260730T052754Z` | 425 | recorded |
| Invoke parent | `invoke-body-war-ontology-focus-scene-pivot-20260730T050022Z` | 426 | recorded |

Central ledger:
`.arcanum/observability/signals/sigil-invocations.jsonl`

The Distill signal is linked to the Invoke run with relation `invoked-by`. Both
signals use Signal Observer version `0.1.0` and have stable run-ID dedupe keys.

## Evidence State

Both signals correctly record partial execution evidence: the authoring and
validation work completed, but no Body War runtime source, build, browser
acceptance, or release execution occurred.

Signal Observer normalized both rows to `gap-threshold` / `reflect-now` because
the repository-level reflection threshold was already reached. That
recommendation is observability maintenance residue; it does not change the
Distill pass verdict, select an SWU, grant mutation authority, or block this
Plan handoff.
