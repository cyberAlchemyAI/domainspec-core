---
module: body-war-login-suggest-track-score-preview
version: current
status: candidate-local
updatedAt: 2026-07-28
docType: glossary
---

# Glossary

| Term | Meaning in this run | Authority |
| --- | --- | --- |
| Connected Runner | A Body War principal with a valid browser session and linked Strava provider account. | Existing auth contract |
| SuggestedTrack | A runner-visible route proposal that is not source-backed merely because it exists or has candidate evidence. | Existing Body War feature contract |
| Runner confirmation | The runner's affirmative attachment of one selected activity and its permitted geometry use to one exact SuggestedTrack. It means evidence submitted, not operator acceptance. | This candidate journey, constrained by existing lifecycle |
| ActivitySummary | The existing redacted activity list item: provider ID, name, sport type, distance, moving time, average speed, and start date. | Existing app contract |
| ActivityGeometrySample | Ephemeral `latlng` plus aligned distance/time stream data fetched for one selected activity after confirmation. | Proposed provider adapter contract |
| GeometryCandidate | A normalized, privacy-filtered route geometry derived from one or more consented activity samples. It is candidate evidence, not official route geometry. | Proposed Body War contract |
| Geometry authority | The declared trust state of a route geometry. `candidate_from_activity` must remain weaker than `source_backed`. | Proposed separate geometry lifecycle |
| ScorePolicy | A versioned calculation contract that defines component maxima, normalizers, caps, window, rounding, and missing-data behavior. | Product decision owner |
| ScoreInputSnapshot | An immutable canonical policy-window input containing derived activity metrics, eligibility, geometry/policy/evidence digests, aggregation version, provenance, and history completeness; never raw streams. | Proposed Body War calculation contract |
| ScorePreview | A non-authoritative numeric projection produced by one exact ScorePolicy version from named evidence and geometry candidates. | Proposed Body War read model |
| Zone Score | The broader game calculation described as 40% pace, 35% distance, 25% frequency, with a displayed cap of 550. Its exact normalization and conquest authority remain unresolved. | Existing discovery-level game-rules draft |
| Single-activity preview | A first-test projection that can have frequency evidence of only one unique day and must disclose that limitation. | Proposed prototype mode |
| Source-backed | An operator-owned promotion state supported by accepted source or geometry evidence. No runner action or score calculation grants it. | Existing lifecycle |
| Fake-provider witness | A deterministic Strava-shaped fixture used for local code and usability validation. It is not real Strava evidence. | Test evidence |
| Real-provider witness | A supervised run using a non-fake adapter, server-side token refresh, and official Strava endpoints. | Hosted execution evidence |
| Claim ceiling | The strongest statement supported by the named evidence. Prototype, geometry candidate, score preview, source-backed route, and production are distinct ceilings. | Lifecycle owner |

## Consistency Rules

- Use `ActivityEvidenceCandidate`, not the older ledger synonym
  `TrackEvidenceCandidate`, in feature and implementation artifacts.
- “Confirm” always identifies the runner action and exact track/activity
  binding; it never means operator acceptance or route promotion.
- “Geometry” without a qualifier is ambiguous. Use `ActivityGeometrySample`,
  `GeometryCandidate`, or `source-backed geometry`.
- “Score” in the prototype UI must render as `ScorePreview` with policy
  version, evidence basis, and limitations.
- A passing fake-provider journey does not prove the real Strava gateway.
