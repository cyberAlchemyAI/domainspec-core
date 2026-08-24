# Strategy Inventory Packet — Body War Track Challenges

## Lookup Status

- Mode: `lookup`
- Machine index: `.arcanum/inventory/index.json`
- Generated at: `2026-08-12T15:08:10Z`
- Lookup readiness: `ready`
- Validation: pass with `0` failures and `153` uncontrolled-tag warnings
- Validation boundary: `inventory-read-model-only`
- Source coverage: partial by design

Inventory is a discovery read model. It does not adopt game rules, establish
track geometry, resolve score authority, authorize a dispatch, or promote any
Body War artifact.

## Query Terms

`Body War`, `Track Challenge`, `Volta do Taquaral`, `SuggestedTrack`, `track
geometry`, `source-backed geometry`, `reference time`, `Zone Score`, `RunCoin`,
`challenge`, `daily`, `weekly`, `monthly`, `record`, `reward`, `sponsor`, `gym`,
`supplement`, `anti-cheat`, `privacy`, `final approver`, `agent pool`,
`predicted disagreement`, and `confirmation readiness`.

## Selected Entries

### `body-war-suggested-track-testable-prototype-gap-research-result-synthesis`

- Path: `.arcanum/inventory/entries/body-war-suggested-track-testable-prototype-gap-research-result-synthesis.md`
- Status/confidence: `verified` / `high`
- Relevant selectors: `#exact-current-boundary-and-evidence-status`,
  `#claim-ceilings-and-deferred-items`
- Evidence cards / EvidenceSets: none declared
- Obligation fit: identifies the implemented SuggestedTrack boundary and keeps
  source-backed geometry, scoring, promotion, and pilot claims deferred.
- Direct-source follow-up: current Craft ledger, game-rules spec,
  SuggestedTrack feature contracts, and current ontology nodes.

### `body-war-login-score-invoke-plan-review-result-synthesis`

- Path: `.arcanum/inventory/entries/body-war-login-score-invoke-plan-review-result-synthesis.md`
- Status/confidence: `verified` / `high`
- Relevant selectors: `#verified-change-requests`, `#prototype-boundary`,
  `#next-owner-route`
- Evidence cards / EvidenceSets: none declared
- Obligation fit: identifies unresolved score normalizers, geometry/privacy
  decisions, and the distinction between a preview and control authority.
- Direct-source follow-up:
  `projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/SPEC.md`.

### `body-war-business-ontology-relationship-coverage-research-result-synthesis`

- Path: `.arcanum/inventory/entries/body-war-business-ontology-relationship-coverage-research-result-synthesis.md`
- Status/confidence: `verified` / `high`
- Relevant selectors: `#decisions`, `#authority-boundary`
- Evidence cards / EvidenceSets: none declared
- Obligation fit: guards against inventing ontology relations while a new
  rules/economy/geometry model is still candidate-level.
- Direct-source follow-up: current Body War business ontology node and relation
  files, not the Inventory summary.

## Excluded Matches

- Mint / Body War convergence findings: useful for general claim-boundary
  discipline, but not evidence for competition rules, geometry, or rewards.
- Body War OEW UI and novice-comprehension reviews: presentation evidence only;
  they do not decide product semantics.
- DomainSpec v2 consumer-proof entries: useful ownership context, but not
  evidence for Body War game design.
- Earlier SuggestedTrack strategy artifacts: route precedent only; their stale
  schema or prior gate state is not reused.

## Direct Evidence That Supersedes Inventory Summaries

- `projects/body-war/.craft/ledger.yml`
- `projects/body-war/CRAFT.md`
- `projects/body-war/docs/features/game-rules/SPEC.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/SPEC.md`
- `projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/SPEC.md`
- `projects/body-war/ontology/business/nodes/entity.challenge.json`
- `projects/body-war/ontology/business/nodes/value.runcoin.json`
- `projects/body-war/ontology/business/nodes/value.track-geometry.json`
- `projects/body-war/ontology/business/nodes/value.reference-time.json`
- `projects/body-war/ontology/business/nodes/policy.score-policy.json`
- `projects/body-war/ontology/business/nodes/policy.controller-selection.json`
- `cyberAlchemy-v2/implementation/ontology-evidence-workbench/public/datasets/body-war/adapter-receipt.json`

## Unresolved Gaps And Residue

- `GAP-TAQUARAL-GEOMETRY-001` remains active: no source-backed route geometry or
  lap boundary is established.
- `GAP-TROQAR-SCORE-AUTHORITY-001` remains active: fastest time, Zone Score, or
  a hybrid has not been adopted as control authority.
- `RunCoin` is deferred; earning, spending, purchase, transfer, expiration, and
  redemption rules are unresolved.
- Current ontology nodes cover generic challenges and seasons but do not define
  a rolling record bounty, ability divisions, or sponsor redemption.
- The public OEW dataset is a deterministic authority-neutral projection. Its
  receipt explicitly disclaims source-backed geometry and score authority.
- Brazil/Campinas is the proposed jurisdictional baseline because Parque
  Taquaral is the pilot location. Current official legal and municipal sources
  must be checked during research; this packet contains no legal conclusion.

## Design Consequences

1. The dispatch must begin from the current game-rules and ontology owners, not
   from the generated OEW dataset.
2. Geometry research gets an exact-binding lane and must return an unresolved
   gap rather than guess coordinates, length, corridor width, or lap boundary.
3. Competition and economy research must keep `record`, `event winner`,
   `attempt token`, `reward credit`, `RunCoin`, `voucher`, and legal tender
   distinct.
4. The original rolling-pot idea is compared against an earned-only,
   non-transferable, capped alternative and a split-ledger sponsor model.
5. No researcher may edit canonical Body War specs, ontology, app bytes, Craft
   state, Inventory, the public dataset, or dispatch telemetry.

