# Executor action-ID normalization

The coordinator emitted `spawn-0002` and `spawn-0003` for the verification wave
because it derived the next ordinal from the one-action synthesis run plan. Those
identifiers already belong to the attack wave in this cumulative run.

Before any verifier host call, the parent normalized the two executor artifacts to
`spawn-0005` and `spawn-0006`. This preserves global action-ID uniqueness. Role,
wave, capability, input/output, target, mutation, and scope fields are unchanged.
The frozen dispatch sheet and dispatch route are unchanged.
