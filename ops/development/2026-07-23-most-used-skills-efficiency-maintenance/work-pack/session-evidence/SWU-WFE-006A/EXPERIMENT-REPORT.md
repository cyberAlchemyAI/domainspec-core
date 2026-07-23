# Experiment Report: Decision Option Admissibility

- Run: `decision-gate-admissibility-20260723T035319Z`
- Result: `PASS`
- Lifecycle owner: `sigil-development`

The causal matrix passed 10/10 cases: zero, one, and two-plus admissible
cardinalities; defer/stop compatibility; rejection before human presentation;
protected and irreversible owner-gate enforcement; duplicate identity; and
invalid evidence shape. Canonical, Codex, and Claude contract/support parity
also passed.

The prefilter routes but never selects among multiple options, executes a sole
route, or satisfies a protected owner gate.
