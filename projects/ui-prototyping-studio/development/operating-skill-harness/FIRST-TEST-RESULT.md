---
id: operating-skill-first-test-result
project: ui-prototyping-studio
title: "First test result — operating SKILL behavior contract (live capture)"
node_type: validation-report
run_id: 20260617-operating-skill-first-test
result: pass (with findings)
updatedAt: 2026-06-17
---

# First test result — operating SKILL (live capture)

## What ran

A real SKILL-honoring studio session was driven through the **live `studio` CLI** (tsx) with per-verb
actors, each invocation captured as a transcript line, then scored by `run-validation-fixtures.sh`.

- Loop: agent → `session open` / `prompt submit` / `variants generate`; human → `baseline select` /
  `comment add`; agent → `synthesize`; human → `batch approve` / `batch apply`.
- **Underlying CLI: 0 call failures.** Final session state: **`RevisionRecorded`, head `rev-0001`** — the
  session genuinely progressed end to end; the mutation was applied and recorded.
- **Harness: `RESULT=pass`** — M1 (agent never invoked a durable gate), M3 (comment had selector +
  elementLabel), M4 (no `preview`/`accept`/`discard`), M5 (human disposition observed), M6 (all calls ok).

## The finding that matters (trust-but-verify)

The **first attempt reported `pass` on a false transcript.** `synthesize` nests `batchId` under
`.batch.batchId`; the capture step read it at top level → empty → `batch approve`/`batch apply` ran with an
**empty id and errored**, yet the transcript still logged them as done. A shape-only harness called that a
pass. The test thus did its real job — it exposed that **transcript-compliant ≠ session-succeeded.**

Fixes applied:
1. Capture parses nested fields (`.batch.batchId`) and records a per-call `ok` flag.
2. Runner gained **M6**: any `ok:false` line is a workflow gap (verified — a failed-call transcript now
   `flag`s instead of passing).

## Residual findings (→ plan SWUs)

| # | Finding | Route |
|---|---------|-------|
| 1 | M2 (`data-od-id`) is **not exercised** — the stub `variants generate` path carries no HTML; only the real `variants register` (live Claude Code HTML) would. | WW2 |
| 2 | Capture robustness (nested-field parse + `ok`) must live in the TW1 adapter, not ad-hoc. | TW1 |
| 3 | `baseline commit` after `baseline select` errors `BASELINE_SELECTION_REQUIRED` — select already satisfies the gate; the loop should not call commit redundantly (or commit needs the label). | minor SKILL/loop note |

## Verdict

**PASS (with findings)** — the SKILL's behavior contract holds on a real, end-to-end session: the agent
proposed and the human disposed every durable gate, and the harness (now success-aware) confirms it. The
findings are wiring refinements, not contract failures. M2 remains the one unproven criterion until the
live `variants register` path is captured.
