# Body-War Registry

## Project Artifacts

| Artifact                           | Path                                                        | Status | Purpose                                                           |
| ---------------------------------- | ----------------------------------------------------------- | ------ | ----------------------------------------------------------------- |
| Project overview                   | `docs/PROJECT-OVERVIEW.md`                                  | active | Project identity, source evidence, audience, and scope.           |
| Initial definitions                | `docs/INITIAL-DEFINITIONS.md`                               | active | Glossary, contexts, concepts, rules, interfaces, and ambiguities. |
| Project decisions                  | `docs/PROJECT-DECISIONS.md`                                 | active | Selected and unresolved project-level decisions.                  |
| Hypotheses                         | `docs/HYPOTHESES.md`                                        | active | Falsifiable product, game-design, and risk hypotheses.            |
| Experiment candidates              | `docs/EXPERIMENT-CANDIDATES.md`                             | active | Candidate validation experiments.                                 |
| Game rules spec                    | `docs/features/game-rules/SPEC.md`                          | active | First DomainSpec feature slice.                                   |
| Park track pilot distill           | `docs/features/park-track-pilot/DISTILL.md`                 | active | Distilled first candidate that avoids city-wide hexes.            |
| Park track implementation layering | `docs/features/park-track-pilot/implementation-layering.md` | active | Layered path from manual one-park proof to multi-park pilot.      |
| RunWar GDD source note             | `docs/research/source-notes/runwar-gdd.md`                  | active | Curated notes from the supplied PDF.                              |
| TROQAR JSX source note             | `docs/research/source-notes/troqar-gamificacao-jsx.md`      | active | Curated notes from the supplied JSX.                              |
| TROQAR visual identity source note | `docs/research/source-notes/troqar-visual-identity.md`      | active | Curated notes from supplied images.                               |
| DomainSpec bundle                  | `domainspec/README.md`                                      | active | Local DomainSpec runtime reference bundle.                        |
| Arcanum observability              | `.arcanum/observability/README.md`                          | active | Local Arcanum telemetry surface.                                  |
| Necronomicon harness               | `.arcanum/necronomicon/README.md`                           | active | Local Arcanum repository memory harness.                          |

## Feature Registry

| Feature                       | Path                                                        | Status | Notes                                                                                                                       |
| ----------------------------- | ----------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------- |
| Game Rules                    | `docs/features/game-rules/SPEC.md`                          | draft  | Captures score, conquest, defense, XP, clans, seasons, and anti-cheat gates.                                                |
| Park Track Pilot              | `docs/features/park-track-pilot/implementation-layering.md` | draft  | First candidate: selected parks with delimited tracks, controller status, challenges, and 48h defense.                      |
| Strava-Linked Pilot           | `docs/features/strava-linked-pilot/SPEC.md`                 | draft  | First app-backed validation channel with Strava OAuth, activity import, and track evidence submission.                      |
| Strava-Linked Pilot Test Plan | `docs/features/strava-linked-pilot/WORK-PACK.md`            | draft  | Invoke-authored test work-pack for local smoke, OAuth, activity import, submission, failure handling, and readiness review. |
