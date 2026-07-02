<!-- MINT-BASELINE BACKFILL (2026-07-01) for domainspec-v2 — cast from templates/definitions-index.md
     (Tier-1 addition #8, SWU-5), which post-dates v2's 2026-06-29 first mint. INTERNAL/private.
     INHERITS the definition-index FORMAT; LOCALIZES the rows (one per DEFINITIONS.md card). -->

# DomainSpec v2 Definitions Index

Status: active
Owner: definitions-governance (domain-local)
Reconciled by: [DEFINITION-DRIFT-AUDIT.md](./DEFINITION-DRIFT-AUDIT.md)

The canonical registry of every DomainSpec v2 definition card. A **load-bearing term** (the constitution's
Load-Bearing Term Tracking rule, `C(meta-4)`) is "tracked" iff it has a row here that resolves to a card in
[DEFINITIONS.md](./DEFINITIONS.md). A load-bearing term cited with no row here is a **drift defect** the
[drift audit](./DEFINITION-DRIFT-AUDIT.md) must flag.

| Definition ID | Term | Status | Source kind | Card |
| --- | --- | --- | --- | --- |
| `domainspec-v2-D1` | Drift | active | operator-reading; local-inference | [DEFINITIONS.md#domainspec-v2-d1](./DEFINITIONS.md) |
| `domainspec-v2-D2` | Validation governance | active | local-inference (domain-originated; RATIFIED kind) | [DEFINITIONS.md#domainspec-v2-d2](./DEFINITIONS.md) |
| `domainspec-v2-D3` | Edge-Law Admissibility | active | local-inference (build-from-owned: CAV2-D22/D29/D16) | [DEFINITIONS.md#domainspec-v2-d3](./DEFINITIONS.md) |
| `domainspec-v2-D4` | Executable Typed Graph | active | local-inference; synthesis | [DEFINITIONS.md#domainspec-v2-d4](./DEFINITIONS.md) |
| `domainspec-v2-D5` | Two-Plane Boundary | active | local-inference | [DEFINITIONS.md#domainspec-v2-d5](./DEFINITIONS.md) |

## Status vocabulary
- `candidate` — first-cited, carries an `Open / to-ground:` field; not yet validation.
- `active` — a full three-voice card exists and its load-bearing terms resolve.
- `deprecated` — superseded; keep the row with its supersedes/superseded-by link (never delete).

<!-- The domain owner maintains this index through the definitions lifecycle. Every row must resolve to a
     card; the drift audit flags any load-bearing term missing a row. Owed cards (layering-governance,
     drift-governance) are tracked in the drift audit, not yet indexed here. -->
