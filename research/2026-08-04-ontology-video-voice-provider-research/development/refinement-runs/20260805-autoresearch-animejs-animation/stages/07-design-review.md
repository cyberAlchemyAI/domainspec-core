# Stage 07 — Design Review

## Verdict

`PASS_WITH_REPAIRS_REQUIRED`

The design is coherent and locally bounded, but it required explicit repairs before planning.

## Review findings

| ID | Severity | Finding | Required repair |
|---|---|---|---|
| DR-01 | critical | Documentation coverage could be mislabeled runtime evidence. | Make proof state per atomic claim and require a later browser receipt for `executed_witness`. |
| DR-02 | critical | Standard and reduced motion could end in visually different semantics. | Require named semantic end states and equality assertions, not screenshot similarity. |
| DR-03 | major | Source and motion lanes disagree on S6 versus S7. | Preserve dissent; select by first-unit reversibility and retain the other as the next high-risk witness. |
| DR-04 | major | Flattened PNGs cannot expose internal animation targets. | Use immutable raster references/backplates plus separately owned SVG/DOM overlays only. |
| DR-05 | major | `createMotionPath` in S7 could imply automatic gate passage. | Exclude it from the owner-gate prototype; animate the request path, not the candidate crossing. |
| DR-06 | major | The Anime.js runtime needed to execute the plan is not installed or vendored in scope. | Add a fail-closed runtime admission gate; no CDN or implicit network resolution. |
| DR-07 | minor | AutoAds diversity and decay numbers have no animation evidence. | Keep them optional, excluded from L0 acceptance. |
| DR-08 | minor | Script beats and caption cues are not one-to-one. | Bind exact script interval plus overlapping caption cue identities; treat both as provisional until recorded voice. |

## Toy-game falsification

| Mutant | Expected result | Design result |
|---|---|---|
| Change source image digest | candidate becomes stale | pass |
| Set consultation to `ok` with no evidence ids | precheck rejects | pass |
| Label QRY-006 as `executed_witness` | proof-state validator rejects | pass |
| Reverse the S6 arrow | semantic witness fails | pass |
| Remove `enforces` from the edge | label-ownership assertion fails | pass |
| Let reduced motion omit arrow direction | semantic-equivalence assertion fails | pass |
| Move S7 candidate to or beyond gate | owner-boundary assertion fails | pass |
| Close a successful WorkEpisode as a Lesson | episode/Lesson non-collapse gate rejects | pass |

## No new user decision

The unresolved Anime.js runtime asset is an execution prerequisite, not a design preference. Planning may specify the fail-closed requirement, but acquisition or external installation requires separate authorization at execution time.

