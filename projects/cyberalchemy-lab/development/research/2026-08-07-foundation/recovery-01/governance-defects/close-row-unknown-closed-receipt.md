# Close-row `closed` Field Defect Receipt

- Classification: governance-only
- Affected edge: recovery dispatch close-row append
- Failing command: `node implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs .register-dispatch-close.tmp.json`
- Diagnostic: `unknown key "closed" on a close record`
- Ledger mutation from failed attempt: none

## Root cause

The temporary caller record supplied `closed`, but schema v0.8.0 makes that timestamp appender-owned and stamps it only after validation. The incoming close-key set therefore rejects `closed` before ledger access.

## Invariant and repair

The append-only ledger must receive exactly one dispatch row and one close row, and callers may not supply appender-owned timestamps. The minimal repair removes only the top-level `closed` field from the temporary candidate while preserving the exit reason, agent counts, loop count, feedback prompt, identity, and accepted findings.

Changed accepted bytes: none. Renewed owner acceptance is not required because this is mechanical temporary-record conformance and does not change the confirmed strategy or final findings SHA-256 `07a29e2fc62f92b6eb2d28c197b19c2ccc036a9952b75474f52c5ac9a44de11d`.

## Revalidation

JSON-parse the repaired temporary record, run the appender once from the repository root while preserving its exit status, then verify one new unique `close_of` row with an appender-stamped ISO timestamp and the exact preserved payload. Recheck that accepted findings bytes did not change.

## Permanent regression proposal

Add a non-mutating `--validate-close` or `--validate-record` path that reports the schema and `LEDGER_MUTATION=none`; add fixtures accepting a close candidate without `closed`, rejecting caller-supplied `closed`, and proving the close-record builder never serializes stamped fields.

Authority ceiling: mechanical close-row conformance only; no authority over findings, dispatch semantics, direct ledger edits, Git, publication, promotion, or external effects.

## Applied result

The repaired appender call succeeded and stamped `closed: 2026-08-08T04:16:51.573Z`. An initial uniqueness precheck used an empty `rg -c` result and emitted `integer expression expected`; because the compound shell continued, that precheck is explicitly rejected as evidence. A separate `set -euo pipefail` post-append validation proved exactly one matching close row, the expected resolved payload and feedback prompt, scoped whitespace cleanliness, and the unchanged accepted findings digest. Result: `CLOSE_ROW_VALIDATION=pass`, `CLOSE_ROW_COUNT=1`.
