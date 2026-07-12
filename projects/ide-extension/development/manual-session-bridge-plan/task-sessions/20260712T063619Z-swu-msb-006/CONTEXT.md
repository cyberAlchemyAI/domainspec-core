# Context Pack: SWU-MSB-006

- Task/SWU: `TASK-SESSION-PROTOCOL / SWU-MSB-006`
- Dependency: [SWU-MSB-005](../20260712T063105Z-swu-msb-005/TASK-SESSION-RESULT.md)
- Sources: session task contract, approved UX/architecture, stable W1 HTTP APIs,
  package/script conventions and child-process test conventions
- Runtime: local Codex; no delegation

## Boundaries

- One process performs one command and exits; no timer, loop, daemon, worker,
  skill resolver, browser controller, or automatic retry.
- Commands are only `ready`, `claim`, `result`, and `interrupt`.
- Operator actions approve, ready/unready, reject/revoke, and release are absent.
- HTTP is loopback-only. Success JSON goes to stdout; diagnostics/errors go to
  stderr with stable nonzero exit classes; claim packet is never logged on error.
- Result/interrupt input is bounded JSON from stdin or an explicit file.

## Gate

- Stable kernel interfaces and 83-test W1 baseline: pass.
- Decisions/blockers: none.
- Required evidence: child-process stdout/stderr/exit codes, loopback refusal,
  zero-ready and conflict behavior, successful ready/claim/result/interrupt,
  no lingering process, and no operator command surface.
- Gate verdict: PASS.
