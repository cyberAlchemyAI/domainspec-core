# Signal Observer Result

- Observed sigil: `invoke:refresh`.
- Result: `recorded`.
- Central ledger:
  `.arcanum/observability/signals/sigil-invocations.jsonl:435`.
- Per-sigil projection:
  `.arcanum/observability/by-sigil/invoke.jsonl:93`.
- Signals: one `quality-pass`, one `useful-pattern`, and one corrected `rework`.
- Quality Bar: `pass`.
- Anti-Pattern hits: zero.
- Reflection trigger: `none`.
- Recommendation: `none`.
- Reflection counters: updated.
- Validation: envelope parses; both JSONL rows parse; the run ID and dedupe key
  occur exactly once in the central ledger.
