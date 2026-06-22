# Hidden-Information Leak Canary

Status: frozen for MVP implementation

The canary scans live observations, decision envelopes, action history,
stdout/stderr capture, public replay exports, state hashes, log material, and
retained inputs.

Forbidden field names:

- `raw_seed`
- `deck_order`
- `opponent_card`
- `future_state`
- `referee_trace`
- `hidden_state_hash`

Live agent input and public replay must pass the canary.
