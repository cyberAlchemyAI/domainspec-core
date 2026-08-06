# Plan validation

- Define authoring: pass.
- Design denominator/selection: pass and byte-identical replay.
- Implementation layering: pass with L0/L1 one-SWU cut and L2 owner split.
- Work Pack completeness: paths, dependencies, validation, baselines, stop rules, receipt, and successor cursor explicit.
- Invoke artifact validation: all JSON parses; Design artifacts satisfy canonical schemas; deterministic outputs replay byte-identically; scoped whitespace passes.
- Runtime admission: pending material package, context pack, fast-entry, and mutation-admission receipts.
- Authority: none.

Verdict: `pass-plan-validated`; Task Session may start only after the pending admission artifacts validate.
