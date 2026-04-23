# E7 Instrumentation Kickoff (2026-04-23)

Status: started
Experiment: E7-signal-emission-rate

## Objective

Start longitudinal emission tracking immediately while E11 D4 manual evidence work runs in parallel.

## First Data Artifact

- `data/run-2026-04-23-longitudinal-start.jsonl`
- rows captured: 1
- kickoff feature: `domainspec-e11-d4-manual-clearance`

## Initial Snapshot

- expected_signal_count: 6
- actual_signal_count: 5
- emission_rate: 0.8333
- missed signal types: `spec-drift`

## Next Accumulation Steps

1. Append one row per pipeline session.
2. Compute rolling statistics every 5 sessions.
3. Preserve append-only JSONL history for E8 dependency usage.
