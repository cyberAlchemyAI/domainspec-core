---
wave: W1
layer: L1
status: ready-selected-census
---

# W1: FPR-01 Authority Baseline

## Decision

After this wave, we know whether one non-contradictory, owner-ratified source/count/status baseline exists.

## Order

1. `SWU-FPR01-001` — selected for a later Task Session: deterministic census without choosing a winner.
2. `SWU-FPR01-002` — owner dispositions through Decision Gate.
3. `SWU-FPR01-003` — baseline, schema, validator, and mutants.
4. `SWU-FPR01-004` — ratification receipt and independent replay.

## Entry

Verified W0 `SWU-SGRM-007-R1` retry receipt (`sha256:1d842c5c87286c49ae0d8f3158bd3a629a9266c280732493454d0249c5e78a6b`). Selection authority is `work-pack/shared/W0-PROOF-SYNC-DECISION.md`; the refresh itself does not execute the census.

## Promotion Gate

The baseline resolves the 13/14, 24/25, 30/31, composability, source-home, projection, status, and direction-disposition conflicts; count/path/status/direction mutations fail; required owners ratify the exact digest.
