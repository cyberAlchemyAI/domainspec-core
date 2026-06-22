# Method Export: Signal Observation Baseline

Producer: mars
Version: 0.1.0

Minimum telemetry checks before claim upgrades:

1. Emit gate outcome signals for every G1-G4 decision.
2. Emit an evidence-gap signal when a claim cannot be upgraded due to missing data.
3. Keep signal rows append-only with `timestamp`, `experiment_id`, and `run_id` metadata.
4. Link each emitted signal to at least one adjudication artifact path.

This method gives downstream projects a lightweight, compatible signal policy.
