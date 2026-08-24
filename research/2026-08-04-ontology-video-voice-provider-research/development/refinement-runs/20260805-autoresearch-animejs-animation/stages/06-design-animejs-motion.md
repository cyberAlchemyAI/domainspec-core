# Stage 06 Lane — Anime.js Motion Evidence

## Consultation result

Fifteen exact `QRY-006` coverage queries passed against graph digest `c38e1e9e2a6dbb5b3c50f874dd0178aecc419db76634fd3dbe8deeb974c827f6`. They bind planned primitives to these evidence identities:

| Topic | Evidence id |
|---|---|
| DOM element targets | `evidence:documentation:0aacc0b64d7cb3ca7f620e04` |
| SVG attributes | `evidence:documentation:ba5c1ff060a4f8ec4dfe1899` |
| keyframes | `evidence:documentation:77e236cc961a1a7cc67fbfae` |
| duration | `evidence:documentation:a6556ac1243027a5236a7b10` |
| timeline add | `evidence:documentation:500a500ae78ad57b37b38d2f` |
| timeline position | `evidence:documentation:9676c6f552d9c381601e2106` |
| seek | `evidence:documentation:3fe941385127fbad939fd85f` |
| `createDrawable` | `evidence:documentation:e05dc4243933cc3d17a9e583` |
| `createMotionPath` | `evidence:documentation:fe6e40b6878924dfba2efc7f` |
| `morphTo` | `evidence:documentation:edb077aa60ecc279eb9d3f54` |
| built-in easing | `evidence:documentation:dbceb75f82f8faee9bd0f48d` |
| `utils.set` | `evidence:documentation:3719132040e69adcefb09198` |
| stagger | `evidence:documentation:7a5e2edd5155fe40e37fd651` |
| scope media queries | `evidence:documentation:5bdfaa2ef0a55f6c15cdb72e` |
| accessible text | `evidence:documentation:94f1d1f0cc963808f396ba41` |

`QRY-006` proves exact-route coverage only. It does not prove parameters, runtime behavior, performance, accessibility outcome, compatibility, or successful animation.

## Candidate mappings

### S6 — Edge semantics

Beat `04:29–04:39`: reveal a left-to-right Rule-to-Operation edge and place `enforces` on it. Use separate overlay nodes for two typed objects, edge path, arrowhead, verb, and state markers. Planned primitives: DOM/SVG targets, timeline, explicit positions, duration, keyframes, easing, and `createDrawable`. Reduced motion uses a discrete state replacement from unlabelled to static labelled edge.

### S7 — Owner gate stop

Beat `05:38–05:48`: draw a request toward the gate and stop before it. Planned primitives: timeline, seek, `createDrawable`, and `utils.set`. `createMotionPath` is explicitly excluded because moving a candidate along the route may suggest conveyor-belt admission. The later witness must assert `candidate_max_x < gate_min_x`, gate closed, admission state absent, and semantic equivalence under reduced motion.

### S12 — Final authority hold

Beat `12:19–12:30`: reduce the view to map, owner, closed gate, external key, and the exact final sentence. Planned primitives: keyframes, positions, easing, restrained stagger, and line drawing. The final second must contain no material motion.

The motion lane prefers S7 because it tests the highest-risk negative invariant. It accepts S6 as the lower-cost engine witness and S12 as the closing acceptance witness.

