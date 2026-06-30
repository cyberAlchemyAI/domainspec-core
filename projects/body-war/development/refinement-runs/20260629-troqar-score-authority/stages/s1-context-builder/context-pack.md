# s1 — Context Builder (evidence baseline)

Owner: context-builder · mode: standard · verdict: pass

## In-scope evidence (relevance-gated)
- **The gap:** `GAP-TROQAR-SCORE-AUTHORITY-001` — Zone Score + fastest-time controller authority
  need an explicit rule; treatment `decision-gate`; severity flag (Craft ledger).
- **Domain vocabulary:** body-war `domainspec/TAXONOMY.md`, `RELATIONSHIPS.md`, `docs/INITIAL-DEFINITIONS.md`
  — Zone/Hex, Clan, XP, League, Season, Activity (Strava), Controller.
- **Product surface:** `docs/features/troqar-product-architecture/{SPEC,states,operations,domain}.md`,
  `docs/features/game-rules/SPEC.md` — zone conquest/defense, territory scoring (deferred).
- **Constraints:** Strava activity is the only validated evidence source (`BLK-STRAVA-ACTIVITY-001`);
  geometry/lap boundary unsourced (`GAP-TAQUARAL-GEOMETRY-001`, deferred).
- **Build-from-owned precedent:** dcb-saga-correctness (cross-record/contention witness, Σ/TOCTOU),
  alloy-tla-modeling (Alloy=adjacency graph, TLA+=temporal contention), claims-ladder (honest labels),
  auto-verdict gate scope (#2).

## Coverage note
Geometry is deferred → the rule must be **geometry-agnostic** (defined over Activities-in-Zone, not
GPS polygons). Contention semantics are the load-bearing unknown → carried to s6/s7/s8.
