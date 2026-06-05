# Project Decisions

## Decision Log

| ID | Decision | Options | Selected | Status | Scope | Reasoning | Source | Date |
| -- | -------- | ------- | -------- | ------ | ----- | --------- | ------ | ---- |
| PD-001 | Internal project id | `body-war`; `troqar`; `runwar` | `body-war` | selected | project | User requested the new project name as body-war. | user request | 2026-05-26 |
| PD-002 | Product brand | TROQAR; RunWar; Body-War | TROQAR | selected | product | User selected keeping TROQAR brand language while scaffolding under `body-war`. | user request | 2026-05-26 |
| PD-003 | First delivery slice | discovery only; game rules first; prototype first | discovery plus game rules first | selected | project | User chose discovery-first and game-rules-first, with no prototype code in this pass. | user request | 2026-05-26 |
| PD-004 | Source policy | copy raw assets; curated source notes; ignore sources | curated source notes | selected | governance | The plan says source files should not be copied unless needed later. | proposed plan | 2026-05-26 |
| PD-005 | DomainSpec initialization | project-local bundle; root-only docs; external dependency only | project-local bundle | selected | tooling | Matches `projects/whisky-doses/domainspec` precedent and makes project self-contained. | repo precedent | 2026-05-26 |
| PD-006 | Arcanum initialization | no Arcanum; observability only; full local command surface | full local command surface | selected | tooling | The accepted plan requested `.arcanum`, Necronomicon, and command surface. | proposed plan | 2026-05-26 |
| PD-007 | First candidate shape | city-wide hex zones; selected parks with delimited tracks; generic leaderboard | selected parks with delimited tracks | selected | pilot | User proposed avoiding hex zones first. Park tracks preserve territory control while cutting geospatial complexity. | user request + distill | 2026-05-26 |

## Open Decisions

| ID | Decision | Candidate Options | Status | Why It Matters |
| -- | -------- | ----------------- | ------ | -------------- |
| OD-001 | Primary conquest metric | Composite Zone Score; fastest reference time; hybrid | unresolved | GDD emphasizes faster reference time; JSX emphasizes composite score. The first implementation must pick one authority. |
| OD-002 | Pilot validation city | Campinas; Sao Paulo neighborhood; another local city | unresolved | Hex count, runner density, sponsor relevance, and manual pilot effort depend on city choice. |
| OD-003 | Initial validation channel | WhatsApp + Strava screenshots; no-code app; native app | unresolved | Determines whether the next phase is operations design, no-code workflow, or technical architecture. |
| OD-004 | Monetization in MVP | defer all; premium notifications only; RunCoins/items; sponsors | unresolved | Monetization can distort game balance if introduced before retention is proven. |
| OD-005 | First park and track set | one local park with 2-3 delimited tracks; multiple parks; single route | unresolved | L0 needs a concrete place and track boundaries before recruiting runners. |

## Verification Baseline

- Required files exist under `projects/body-war/docs/`.
- `projects/body-war/domainspec/README.md` exists and explains the local DomainSpec bundle.
- `.arcanum/observability/config.json` and `.arcanum/necronomicon/capabilities.json` exist.
- `docs/features/game-rules/SPEC.md` contains non-placeholder rules for score, conquest, defense, XP, clans, seasons, and anti-cheat.
- Markdown link checks should pass where repository tooling supports the project-local path.

