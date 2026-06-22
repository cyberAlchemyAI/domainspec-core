# Invalid Events

Status: frozen for MVP implementation

Invalid output is diagnostic evidence and triggers deterministic legal fallback.
It does not retire the match in Local Arena CLI v0.

## Event Codes

- `malformed_json`
- `prose_before_json`
- `extra_json_object`
- `mismatched_decision_id`
- `missing_action`
- `illegal_action`
- `illegal_amount`
- `oversized_stdout`
- `invalid_utf8`
- `stderr_json_ignored`
- `timeout`
- `crash`
- `eof`

## Golden Matrix

The fixture matrix lives under `fixtures/l0/invalid_output_matrix/cases.json`.
Every case must produce a named diagnostic event and deterministic fallback.
