# Explorer Status Normalization

`spawn-0002` reported `STATUS: block` for the target product state while also
reporting `VALIDATION: pass` and returning the complete exact-source research
artifact. The listed blockers are findings—no accepted add-on, adapter,
proposal contract, witness, target Inventory, or branch freshness—not failures
to execute the read-only explorer action.

Orchestrate therefore normalizes the action receipt to `status: pass`,
`validation: pass`, and `blockers: []`. The product blockers remain preserved
verbatim in `research.md#agent-2` and must constrain synthesis, evidence
closure, and final claims. This normalization does not convert any absent
implementation or witness into a positive claim.
