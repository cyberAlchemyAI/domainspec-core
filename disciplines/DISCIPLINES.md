# Private Discipline Catalog (umbrella root)

Status: candidate
Owner: umbrella maintainer

This catalog formalizes recurring practices specific to the **private** `domainspec-core` umbrella. It is the private counterpart to [`arcanum/disciplines/DISCIPLINES.md`](../arcanum/disciplines/DISCIPLINES.md). Private-parent practices live here; general practices go in the public arcanum catalog. See [README.md](README.md) for the boundary.

## Catalog

| ID | Discipline | Status | Steward | Evidence | Next hardening move |
| --- | --- | --- | --- | --- | --- |
| `submodule-orchestration` | Submodule orchestration discipline | candidate | umbrella maintainer | [Submodule discipline](cards/submodule-orchestration.md) | Consolidate the duplicated prose (CLAUDE.md, AGENTS.md, SUBMODULE-DISCIPLINE.md) behind the Makefile `bump-check`/`doctor` validator and route to a constitution. |
| `asset-ownership-propagation` | Asset ownership propagation discipline | active-pattern | ops | [Asset ownership card](cards/asset-ownership-propagation.md) | Promote `tools/check_github_drift.sh` to the named validator and tie each asset class to a single source of truth. |
| `session-closure` | Session closure discipline | candidate | vault / close-session | [Session closure card](cards/session-closure.md) | Decide whether closure routes catalog-only or gains an edge-legality validator over session nodes. |

## Status Meanings

| Status | Meaning |
| --- | --- |
| `candidate` | Useful practice exists, but authority and validation are still being proven. |
| `active-pattern` | Already used by active capabilities, but the discipline-level contract is not canonical. |
| `implemented` | Working repository support exists, may still need discipline-level rules. |
| `canonical` | Accepted authority with validator or constitution support. |
| `deprecated` | Superseded or withdrawn. |

## Growth Rule

Promote a discipline only when the next route names its owner, evidence, validation surface, and mutation boundary. A discipline recommends a route; it cannot directly promote registry, ontology, glossary, sigil, or spell knowledge — and a private discipline never migrates into the public arcanum catalog.
