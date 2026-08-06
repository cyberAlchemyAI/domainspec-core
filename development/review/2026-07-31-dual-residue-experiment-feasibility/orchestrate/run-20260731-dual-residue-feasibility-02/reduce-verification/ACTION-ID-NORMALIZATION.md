# Executor action-ID normalization

The coordinator emitted `spawn-0003` for the audit wave because it derived the next
ordinal from the two-action verification run plan. That identifier already belongs
to the attack wave. Before the auditor host call, the parent normalized the executor
artifact to `spawn-0007`. All other action fields and the frozen dispatch remain
unchanged.
