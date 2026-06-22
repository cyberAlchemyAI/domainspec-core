# Gap And Blocker Review

Status: `flag`
Review style: local refine pass over `troqar-product-architecture`

## Verdict

The app-wide TROQAR architecture packet is useful and internally coherent, but
it is not mutation-ready. It preserves the known Body War blockers and exposes
new follow-up gaps for app-wide build planning.

## Active Craft Blockers Preserved

| ID | Status | Impact On This Packet | Closure Condition |
| --- | --- | --- | --- |
| `BLK-STRAVA-ACTIVITY-001` | active | Blocks proof that the auth-backed pilot can import and submit a real run. | Import and submit one real Strava run without exposing tokens. |
| `GAP-TAQUARAL-GEOMETRY-001` | active | Blocks map/route GPS validation claims. | Add a sourced track-boundary or lap artifact before geometry or GPS validation claims. |

## New Design Gaps

| Gap ID | Severity | Owner Route | Summary | Suggested Closure |
| --- | --- | --- | --- | --- |
| `GAP-TROQAR-PAGE-PRIORITY-001` | flag | invoke plan | App-wide pages are defined, but the first page implementation order is not selected. | Select L0 page order in a work-pack. |
| `GAP-TROQAR-SCORE-AUTHORITY-001` | flag | decision-gate | Zone Score and fastest-time controller both exist in source evidence. | Decide when `zone_score` can replace or augment L0 controller. |
| `GAP-TROQAR-BACKEND-PROVIDER-001` | flag | invoke plan / deployment-security | Hosted storage/provider specifics remain unnamed for full app architecture. | Select managed storage, secret store, and deployment provider. |
| `GAP-TROQAR-GLOSSARY-PROMOTION-001` | note | definitions-governance | App-wide terms are local candidate definitions, not canonical glossary. | Promote or sync through definitions governance when stable. |
| `GAP-TROQAR-DEFERRED-ECONOMY-001` | note | future decision-gate | Sponsor, RunCoins, store, and premium pages are defined as deferred. | Reopen only after L0 control/evidence loop proves repeat use. |

## Non-Blocker Tensions

| Tension | Current Handling |
| --- | --- |
| Full product architecture vs hosted preview scope | App-wide docs are non-mutating; Parque preview remains first executable slice. |
| Brand page concepts vs product app ergonomics | UI spec makes the first screen an app command surface, not a marketing landing page. |
| Visual guide source is a source note, not raw asset files | Visual definitions remain token/behavior guidance until assets are supplied. |
| Operator page is needed for governance but not runner nav | Operator route is role-gated and excluded from bottom nav. |

## Recommended Next Route

1. Confirm the prepared formal Refine strategy if you want the canonical
   ten-stage gap/blocker loop to run.
2. Otherwise run `invoke plan` on this packet to create the page/domain/backend
   work-pack and select the first SWU.
