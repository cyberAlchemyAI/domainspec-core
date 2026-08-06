# Bella detailed-card deployment receipt

- Date: `2026-08-02T15:28:58Z`
- Domain: `https://cyberalchemize.com/bella`
- Source/live/remote SHA-256: `e0dc32910abe18c63194dbdbce672d34c0ff95de7d7543dd5b5268141f2dfb48`
- Previous live SHA-256: `e84c444e470b3ffd5fa11c5f109b3a4d9246a420ff0cd33814d6c3af2472716b`
- Retained rollback backup: `/srv/co-op-engine/backups/20260802T152628Z`
- Container: `coop-engine-site`
- Layout: `direito-romano:tower-canvas-layout:v3`
- Result: `pass`

## Delivered card anatomy

- Card dimensions increased from 190 by 72 to 224 by 116 graph units.
- Every card has a stable-ID header, textual type and tower abbreviation, and a two-line title.
- At 125% or greater, active-route cards reveal a two-line study summary.
- At 180% or greater, cards reveal both summary and localized evidence class.
- Full source locator, page range, boundary, and route relations remain in the exact inspector.
- Accessible names now include stable ID, type, title, tower, and evidence without repeating the full summary.
- Hover title remains supplementary and includes summary, evidence, and source.

## Acceptance

| Check | Result | Evidence |
| --- | --- | --- |
| Overview | pass | 100% shows compact cards; summary and evidence opacity are zero |
| Text containment | pass | Zero header/title/summary/evidence bounding boxes exceed 224 by 116 |
| Route LOD | pass | Q-08 at 128% reveals TM-C12 summary, keeps unrelated summary hidden, and keeps evidence hidden |
| Detail LOD | pass | TM-C12 at 483% shows summary and evidence |
| Inspector parity | pass | TM-C12 resolves `claims/claim-ledger.md · TM-C12 · PDF pp. 196–199` |
| Accessibility identity | pass | TM-C12 accessible name includes claim type, title, Marky, and primary-source evidence; one roving tab stop remains |
| Graph invariants | pass | 75 nodes, 164 edges, 10 questions, valid endpoints, zero overlap, equivalent navigator, complete provenance |
| Wheel regression | pass | Inactive wheel preserved view and scrolled 400 to 516; active pointer drift was 0.09 px |
| Search regression | pass | `família` returned six navigator objects |
| Mobile | pass | 390 by 844 has no horizontal overflow; 75 visual and 75 navigator nodes remain available |
| Browser isolation | pass | Clean desktop/mobile Firefox contexts reported zero console errors/warnings and zero external requests |
| Byte identity | pass | Selected source, live response, and remote Bella file share the recorded hash |
| Neighbor continuity | pass | Portfolio and Craft hashes remained unchanged; Time Capsule and TROQAR remained HTTP 200 |

## Boundaries

- No new tower or PDF content was required. The richer cards project fields already present in the immutable graph.
- Full provenance and epistemic boundaries remain in the inspector; the visual footer is not a substitute for the exact record.
- Deployment proves the recorded structure and browser behavior, not doctrinal correctness, mastery, grading, pedagogy, or exam readiness.

