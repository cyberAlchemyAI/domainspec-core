# Stage 07 — Interrogation (refine-design-review) · parent-led (light)

- Capability: `interrogation` · Mode: `refine-design-review` · Receipt: parent coordinator (standard preset, light)
- Roles: design-advocate / risk-reviewer (parent-held)
- Status: **flag** (3 risks; all repairable, none block)

## Risks found

- **DR1 — Cross-session matching vs a session-scoped event log (high).** DD-AF1 says the index is "regenerable from events," but `BaselineGenealogyFamily` lineages and recognition-over-recall (A5) span **multiple sessions**. A single session's event log can't match an identity seen in a *prior* session. **Repair:** the index must aggregate over **all session event logs in the repo** (a repo-level regenerable projection), keyed by `UIElementIdentity`, not a per-session rebuild. Still derived, still not canonical — just repo-scoped.
- **DR2 — Per-repo cache becoming de-facto source of truth (med).** A persisted projection file invites being edited/trusted directly. **Repair:** stamp it `derived/regenerable; do not edit` + a `rebuild` command; treat any drift from events as the cache being wrong, never the events.
- **DR3 — Resonant namespace-name attribution (med).** Even names-only, the *selection* of which names map to which enum is derived from resonant's work → needs attribution. **Repair:** record the s1 mapping's provenance (source repo + commit + retrieval) in the DNA-fill note, mirroring `VENDORED-LICENSES.md`, **even though nothing is vendored**. Confirms A3 boundary is auditable.

## Confirmed sound

- DD-AF2 names-only fill holds A2 (no raw values). DD-AF3 projection holds A5. DD-AF4 phase-1 od-id equality is deterministic and ships cheaply. No new entity name (A1) holds.

## design-review-ledger → s08
