# Redaction Policy

Status: frozen for MVP implementation

## Private To Public Rules

- Replace raw seed material with opaque `seed_handle`.
- Remove deck order.
- Remove referee trace.
- Remove hidden-state hashes.
- Keep own-card information only where it is public by game outcome.
- For showdown, public replay may show both private cards.
- For folds, public replay must not reveal the folded player's card.
- Keep action, fallback, payout, and diagnostic events when they do not expose
  hidden state.

The redaction scan treats these field names as forbidden in public replay:

```text
raw_seed
deck_order
opponent_card
future_state
referee_trace
hidden_state_hash
```
