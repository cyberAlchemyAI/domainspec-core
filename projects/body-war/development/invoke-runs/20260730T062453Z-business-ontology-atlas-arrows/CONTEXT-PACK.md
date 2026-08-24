# Context Pack — Body War Ontology Atlas Arrows

Mode: `standard`  
Strict obligation coverage: `pass`  
Target: `body-war.business-ontology-atlas-arrows`

## Obligations

| ID | Obligation | Status |
| --- | --- | --- |
| `O-01` | Restore visible source → phrase → target arrows without changing ontology meaning. | covered |
| `O-02` | Show whole-ontology cross-lens direction without a 231-edge hairball. | covered |
| `O-03` | Preserve all 237 nodes, 231 relations, 122 internal relations, 109 portals, and 44 zero-degree nodes. | covered |
| `O-04` | Preserve relation identity, source, target, direction, predicate, authority effect, and owner. | covered |
| `O-05` | Keep the atlas static-first, keyboard-readable, responsive, reduced-motion safe, and printable. | covered |
| `O-06` | Produce an execution-ready, non-mutating Invoke plan with bounded validation. | covered |

## Selected evidence

| Source | Selectors | Covers | Why selected |
| --- | --- | --- | --- |
| `projects/body-war/development/invoke-runs/20260730T051037Z-business-ontology-view-atlas/SPEC.md` | capabilities, projection rules, acceptance criteria | O-01, O-03, O-04, O-05 | Governing contract for the completed atlas. |
| `projects/body-war/development/invoke-runs/20260730T051037Z-business-ontology-view-atlas/ARCHITECTURE.md` | projection model, portal model, validation witnesses | O-02, O-03, O-04, O-06 | Defines the conserved source-bound projection. |
| `projects/body-war/development/invoke-runs/20260730T051037Z-business-ontology-view-atlas/UX-PLAN.md` | journeys, portal navigation, responsive semantics | O-01, O-05 | Establishes human and assistive navigation constraints. |
| `projects/body-war/development/invoke-runs/20260730T051037Z-business-ontology-view-atlas/INVOKE-REPORT.md` | outcome, final evidence, boundary | O-03, O-06 | Proves the prior three-SWU frontier completed. |
| `projects/body-war/ontology/business/scripts/generate-views.mjs` | `renderRelationRow`, `renderRelationSvg`, `renderHtmlRelationRow` | O-01, O-04 | Existing Body War source already renders typed arrow sentences. |
| `projects/body-war/ontology/business/scripts/render-view-atlas.mjs` | `renderRelation`, `lensCards`, lens sections, CSS | O-01, O-02, O-05 | Exact implementation seam where visual arrows are absent. |
| `projects/body-war/ontology/business/scripts/view-atlas-projection.mjs` | portal and lens projection | O-02, O-03, O-04 | Current pure projection retains the source data needed by arrows. |
| `projects/body-war/ontology/business/authoring/view-atlas-catalog.mjs` | six editorial lenses and boundary | O-02, O-03 | Keeps lens grouping removable and non-semantic. |
| `projects/body-war/ontology/business/tests/business-view-atlas-render.test.mjs` | static structure and non-regression | O-03, O-04, O-05, O-06 | Existing deterministic acceptance surface. |
| `projects/body-war/ontology/business/scripts/validate-view-atlas-browser.mjs` | pinned browser modes and assertions | O-05, O-06 | Existing runtime evidence seam for the exact atlas. |
| `projects/body-war/ontology/business/receipts/view-atlas-coverage-receipt.json` | source digests and 237/231/122/109/44 counts | O-03, O-04 | Exact current denominator and semantic-source lock. |
| `.arcanum/inventory/entries/body-war-business-view-novice-comprehension-review-result-synthesis.md` | authority boundary and browser-admission boundary | O-05, O-06 | Verified human-view boundary; no comprehension claim. |

## Evidence-derived facts

- The atlas currently renders relationships as linked prose and relation cards,
  not graphical arrows.
- The existing gallery renderer already encodes a proven visual grammar:
  source card → plain-language phrase → target card, with typed predicate and
  explicit authority effect.
- The 109 cross-lens portals collapse into 13 directed lens-pair groups. An
  overview with 13 aggregated arrows is bounded; an overview with all 231
  relations is not.
- The prior browser receipt passed structural behavior, but the user correctly
  identified that structural direction did not preserve the former visual
  arrow representation.

## Excluded candidates

- `nodes/`, `relations/`, `lifecycle-policies/`, `profile.json`, and
  `views/business.json`: exact digests are inputs, but their bodies do not need
  to be re-read or changed for this projection repair.
- `BUSINESS-VIEW-ATLAS.html`: generated output; its renderer and receipts are
  the authoring sources.
- remote graph-layout libraries: unnecessary for six fixed lenses and would
  violate the local static-first boundary.

## Inventory result

`.arcanum/inventory/index.json` validated as lookup-ready with zero failures
and 115 historical tag warnings. The relevant novice-comprehension synthesis
was selected. The user-owned dirty inventory index remains read-only.

## Remaining ambiguity

No blocker ambiguity remains. The user's report identifies the defect, and the
previously proposed progressive shape—overview arrows, relation arrows, exact
details—was followed by an explicit Invoke Define/Design/Plan request.

