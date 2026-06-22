# Review Repair

Dispatch ID: `2026-06-19-poker-agent-arena-mechanics`

Reviewer receipts:

- `reviews/exploitability-abuse.md`: `ACCEPT_WITH_EDITS`
- `reviews/mvp-minimality.md`: `ACCEPT_WITH_EDITS`

Applied repair:

- Narrowed MVP to a toy-game-first CLI arena using Kuhn/Leduc before Hold'em integration.
- Split toy MVP legal actions from Hold'em-specific min-raise, short all-in, and reopen behavior.
- Moved side pots, odd chips, uncalled refunds, tied showdown, composite scoring, exploitability, adaptation, time-bank, and multiway all-in fixtures behind follow-up gates.
- Added invalid-action abuse, replay/seed redaction, penalty calibration, adaptation leakage, time-credit signaling, and collusion-adjacent side-channel guardrails.
- Reordered implementation into M0 toy CLI contract, M1 Hold'em engine parity, then M2 leaderboard/novelty.

Close judgment:

The review loop did not reject the handoff. The revised `findings.md` is acceptable as
design evidence and should not be treated as implementation-ready code or validated runtime
behavior.
