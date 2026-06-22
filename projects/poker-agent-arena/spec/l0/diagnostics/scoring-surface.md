# Scoring Surface

Status: frozen for MVP implementation

Local Arena CLI v0 reports diagnostics, not a final public leaderboard.

Required surfaces:

- clean EV,
- fallback-inclusive EV,
- invalid rate,
- timeout rate,
- fallback count,
- replay determinism,
- hidden-information canary result,
- public replay redaction result.

Fallback-inclusive EV is the displayed operational result. Clean EV is reported
beside it so protocol failures cannot hide inside raw performance.
