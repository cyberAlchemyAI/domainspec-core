# Signal Observer Result

- Observed capabilities: `distill` child and `invoke:refresh` parent.
- Result: two telemetry rows recorded exactly once.
- Central ledger lines: 432 and 433.
- Quality Bar: pass for the observed Refresh and Distill evidence.
- Anti-Pattern hits: zero.
- Workflow gap: the generated capability mirror disappeared and was restored
  during Refresh; `BWAA-SKILL-MIRROR` remains a conditional preflight guard.
- Reflection trigger: `gap-threshold`.
- Recommendation: `targeted-update`.
- JSON/JSONL validation: both envelopes parse, and both run IDs have exactly
  one central-ledger row.
- Observer runtime residue: reflection-state update reported `failed` because
  the emitted `workflow_gaps` value used a string rather than the runtime's
  structured severity object. The central telemetry rows were still recorded.
  This non-blocking observer-format gap does not change the Refresh result and
  must not be reported as a successful reflection-state update.
