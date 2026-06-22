# Timeout Fallback Fixture

Status: frozen for MVP implementation

The timeout fixture runs at least one agent with a short local
`decision_timeout_ms` and verifies:

- timeout event is recorded,
- late output is ignored,
- deterministic fallback is used,
- fallback-inclusive EV reflects the fallback,
- timeout rate is greater than zero for the offending agent.
