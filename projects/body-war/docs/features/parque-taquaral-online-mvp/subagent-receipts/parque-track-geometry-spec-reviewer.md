---
dispatch_id: body-war-pilot-domainspec-subagent-strategy-20260614
role_id: parque-track-geometry-spec-reviewer
agent_id: 019ec50d-8605-7ca0-a5f9-5517782e5799
spawn_status: spawned
join_status: completed
close_status: closed
validation_result: pass
status: complete
last_updated: 2026-06-14
---

# Receipt: Parque Track Geometry Spec Reviewer

## Scope

Audit missing Parque Taquaral track geometry coverage for the hosted friend
preview MVP.

## Key Findings

- Full Parque Taquaral geometry is selected as the pilot target, but the
  geometry gap does not close until a full artifact exists and submission
  evidence is separated from GPS proof.
- Existing docs still classify Parque Taquaral as a place context without a
  sourced lap/track boundary.
- The prototype only seeds `park-track-alpha` with placeholder metadata, not
  Parque identity, distance, lap route, or geometry.
- Preview acceptance is weaker than GPS proof and must not be described as
  final validation.

## Missing Geometry Specs

| Artifact Or Field | Why Needed | Priority |
| --- | --- | --- |
| `TRACK-GEOMETRY.md` | Source-backed full Parque Taquaral pilot track contract. | P0 |
| Static geometry artifact | GeoJSON/GPX/KML or equivalent file consumed by the app. | P0 |
| Track identity fields | Stable `track.id`, name, park, city, country, version, status. | P0 |
| Source fields | Source, source date, license, operator review status. | P0 |
| Route metadata | Distance, lap basis, start/finish note, direction, route description. | P0 |
| Geometry metadata | Format, coordinate system, kind, bbox, simplification policy. | P0 |
| Validation status fields | Distinguish draft/sourced/preview-visible from GPS validated. | P0 |
| Later GPS proof spec | Activity stream matching, tolerance, anti-cheat, privacy. | P1 |

## Tensions

- The forecast says to use placeholders until a sourced artifact exists; the
  later decision selects the existing Parque track as pilot geometry.
- The dispatch says there is an existing geometry target, while discovery/Craft
  still say no sourced geometry/lap boundary exists.
- Older park-track framing expects two or three delimited tracks; this one-shot
  now asks for the full Parque Taquaral track.

## Backlog Contribution

1. Create `TRACK-GEOMETRY.md`.
2. Define static geometry data contract and source authority.
3. Replace `park-track-alpha` placeholder semantics with Parque track identity.
4. Add preview guardrail fields: `geometryStatus`,
   `previewAcceptanceStatus`, and `gpsValidationStatus`.
5. Defer GPS proof/anti-cheat until after hosted friend preview works.

