# Project Overview

## Identity

| Field | Value |
| ----- | ----- |
| Project id | `body-war` |
| Product brand | TROQAR |
| Tagline | Corra. Conecte. Conquiste. |
| Project type | GPS-based territorial running game |
| Baseline status | initial discovery |

## Summary

TROQAR is a real-world running game where runners compete for city territory. A runner records GPS activity, validates presence inside map zones, conquers or defends hexagonal territories, and earns permanent profile XP while rankings, leagues, and seasonal competition create recurring goals.

The initial product language comes from TROQAR brand material. The initial gameplay model comes from the RunWar GDD and the TROQAR gamification JSX. `body-war` is the internal project id for this DomainSpec and Arcanum workspace.

## Source Evidence

| Source | Evidence Type | Status | Notes |
| ------ | ------------- | ------ | ----- |
| `RunWar_GDD_Completo.pdf` | observed source artifact | seed | Defines hex scale, conquest loop, invasion windows, anti-cheat layers, monetization, and MVP roadmap. |
| `troqar-gamificacao-1.jsx.txt` | observed source artifact | seed | Defines score formula, XP sources, clan contribution, recovery windows, seasons, and interface concepts. |
| Supplied TROQAR images | observed visual artifact | seed | Defines product brand, colors, typography direction, and app positioning. |
| User request | stated intent | selected | Create `projects/body-war`, keep TROQAR as brand, initialize DomainSpec and Arcanum, no prototype code in first pass. |

## Audience

| Actor | Need | Evidence Status |
| ----- | ---- | --------------- |
| Runner | Make real runs feel competitive, social, and consequential. | stated |
| Clan member | Coordinate defense, attacks, and shared progression. | observed |
| City/community operator | Run early pilot loops before full app implementation. | hypothesized |
| Sponsor/brand partner | Attach rewards to real locations and running behavior. | observed |
| Product team | Convert game concept into DomainSpec-ready rules and validation experiments. | stated |

## Current Scope

In scope for this first baseline:

- DomainSpec scaffold and project docs.
- Arcanum observability and Necronomicon harness initialization.
- Initial discovery package.
- First `game-rules` feature spec.
- Curated source notes from the supplied PDF, JSX, and brand images.

Out of scope for this first baseline:

- App or prototype implementation.
- Copying original binary/source assets into the repo.
- Payment provider, map provider, wearable, or push-notification integration implementation.
- Final balancing of XP, RC, monetization, or anti-cheat thresholds.

## Discovery Verdict

The project is ready for game-rules specification and validation planning, but not ready for implementation. The next work should refine the game-rules spec, choose the pilot slice, and separate pre-MVP manual validation from app-backed mechanics.

