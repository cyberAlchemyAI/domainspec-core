# Optional Context for MTNG Review Packet v2

MTNG began as a branching/delegation model for reducing agent confusion in mixed workflows.

The early metaphor was resonance-like branching: a messy signal may excite several modes, and it should split at boundaries where validation, context, tool needs, memory treatment, contribution record type, or authority level changes.

After review, the proposal has been narrowed heavily.

The current V1 is not a live orchestration layer. It is an on-demand analysis and artifact extraction pipeline.

The intended first pilot is a Post-Hoc Issue Packager:

```text
selected terminal transcript + chat transcript + git diff + bug notes
→ signal manifest
→ branch nodes only where required
→ validators
→ developer issue packet
→ memory candidates marked review-only
→ contribution records
→ OKF-compatible export
```

The goal is to improve developer handoffs and auditability without giving agents more live authority.

Important interpretation:

- MTNG is not a replacement for Guardian Core.
- MTNG is not a replacement for provider routing.
- MTNG is not a direct memory writer.
- MTNG is not a contribution valuation system.
- MTNG is not always-on monitoring.
- MTNG should be OKF-first for exported knowledge, but MTNG-native for operational state.
