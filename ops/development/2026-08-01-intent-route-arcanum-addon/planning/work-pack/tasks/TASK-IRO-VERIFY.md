# TASK-IRO-VERIFY — Closure audit

This task is closure-exempt and selects no implementation. Exact inputs,
outputs, validation commands, and the `__complete__` successor sentinel are
owned by [`EXECUTION-CONTRACT.json`](../shared/EXECUTION-CONTRACT.json).

Verify every SWU terminal/owner receipt, exact source and closure digest,
accepted case count, runner stderr/exit, browser/runtime provenance, rollback
preimage, scoped write inventory, private/public boundary, generated/canonical
distinction, consumer authority counters, and lifecycle label.

The final claim must distinguish candidate, canonical, generated, installed,
consumer-admitted, private-admitted, released, deployed, and production states.
Missing evidence downgrades or blocks the claim; it is never inferred. A pass
projects only the terminal `__complete__` sentinel.
