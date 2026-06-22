# Referee Transcript

Status: frozen for MVP implementation

The private referee transcript is the authority for replay and diagnostics.

## File Format

`private-transcript.jsonl` contains one JSON object per line.

Required event types:

- `match_start`
- `hand_start`
- `decision`
- `action`
- `fallback`
- `hand_result`
- `match_summary`

Private transcript material may include raw seed material and full private card
state. It must never be sent to live agents.
