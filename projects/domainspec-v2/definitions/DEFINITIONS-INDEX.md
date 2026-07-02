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
| `domainspec-v2-D6` | meta-type | candidate | method-vocabulary | [DEFINITIONS.md#domainspec-v2-d6](./DEFINITIONS.md) |
| `domainspec-v2-D7` | category | candidate | method-vocabulary | [DEFINITIONS.md#domainspec-v2-d7](./DEFINITIONS.md) |
| `domainspec-v2-D8` | formal criterion | candidate | method-vocabulary | [DEFINITIONS.md#domainspec-v2-d8](./DEFINITIONS.md) |
| `domainspec-v2-D9` | edge-participation signature | candidate | method-vocabulary (aliased DS-D8) | [DEFINITIONS.md#domainspec-v2-d9](./DEFINITIONS.md) |
| `domainspec-v2-D10` | content validator | candidate | method-vocabulary | [DEFINITIONS.md#domainspec-v2-d10](./DEFINITIONS.md) |
| `domainspec-v2-D11` | instance | candidate | method-vocabulary | [DEFINITIONS.md#domainspec-v2-d11](./DEFINITIONS.md) |
| `domainspec-v2-D12` | instance validator | candidate | method-vocabulary | [DEFINITIONS.md#domainspec-v2-d12](./DEFINITIONS.md) |
| `domainspec-v2-D13` | aspect file | candidate | method-vocabulary | [DEFINITIONS.md#domainspec-v2-d13](./DEFINITIONS.md) |
| `domainspec-v2-D14` | Concept Registry | candidate | method-vocabulary | [DEFINITIONS.md#domainspec-v2-d14](./DEFINITIONS.md) |
| `domainspec-v2-D15` | declared-attributes convention | candidate | method-vocabulary | [DEFINITIONS.md#domainspec-v2-d15](./DEFINITIONS.md) |
| `DS-D1` | Meta-Type System (25 types) | candidate | domain-vocabulary | [meta-types/meta-types.md](./meta-types/meta-types.md) · [.yml](./meta-types/meta-types.yml) |
| `DS-D1.1` | Entity | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.2` | Value Object | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.3` | Enum | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.4` | Operation | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.5` | Query | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.6` | Calculation | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.7` | Rule | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.8` | Policy | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.9` | Workflow | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.10` | Saga | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.11` | Interface | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.12` | Event | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.13` | Mapping | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |
| `DS-D1.14` | State Machine | candidate | domain-vocabulary; formalized | [meta-types.md](./meta-types/meta-types.md) |

## Status vocabulary
- `candidate` — first-cited, carries an `Open / to-ground:` field; not yet validation.
- `active` — a full three-voice card exists and its load-bearing terms resolve.
- `deprecated` — superseded; keep the row with its supersedes/superseded-by link (never delete).

<!-- The domain owner maintains this index through the definitions lifecycle. Every row must resolve to a
     card; the drift audit flags any load-bearing term missing a row. Owed cards (layering-governance,
     drift-governance) are tracked in the drift audit, not yet indexed here. -->
