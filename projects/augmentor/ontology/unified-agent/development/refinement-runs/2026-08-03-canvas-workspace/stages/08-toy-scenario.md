# Stage 08 — Canvas state-continuity toy game

- Pattern: `toy_game`
- Cost: model-only; no product execution
- Status: `pass`
- Purpose: falsify the repaired transition contract before planning

## Tokens

Semantic token `S`:

```text
view=intent-route; query=route; posture=all;
selected=route_disposition; selectedKind=node;
sequence=AUG-INTENT-RESOLVE; explanationLens=plain_meaning;
graphTransform={scale:1, x:240, y:0}
```

Presentation token `P0`:

```text
mode=wide; explanationOpen=true; detailsOpen=true; evidenceOpen=false;
activeMobileSheet=null; canvasFocus=false; focusReturnStack=[]
```

Invariant `I`: every presentation-only move keeps `S` byte-equivalent.

## Play

| Turn | User action | Expected presentation state | Semantic check | Focus check |
| --- | --- | --- | --- | --- |
| 1 | Minimize Details | `detailsOpen=false` | `S` unchanged | stays on Details trigger |
| 2 | Select another node while Details is closed | Details remains closed | only `selected` changes by the explicit semantic action | selected SVG node has visible focus |
| 3 | Reopen Details | `detailsOpen=true` | current selection is read, not recreated | trigger or panel heading according to input mode |
| 4 | Enter Focus canvas | snapshot open regions; all supports closed; `canvasFocus=true` | `S` unchanged | graph heading/viewport receives visible focus |
| 5 | Press Escape | restore snapshot; `canvasFocus=false` | `S` unchanged | Focus canvas trigger restored |
| 6 | Resize until a dock would squeeze graph below 480px | mode normalizes to triggers/sheet; graph ≥480px | `S` unchanged | no focused element is hidden |
| 7 | Open tray with insufficient graph height | tray uses sheet host; graph not overlaid | `S` unchanged | labelled dialog contains focus |
| 8 | Resize to 320×800 and request Details | one Details dialog; background inert | `S` unchanged | focus inside dialog |
| 9 | Switch to Explanations | one Explanation dialog replaces Details atomically | `S` unchanged | focus enters new labelled dialog |
| 10 | Press Escape | no dialog; canvas active | `S` unchanged | Explanations trigger restored |

## Failure cards

- `F1`: selection disappears after Details minimizes → presentation reducer has
  mutated semantic state; block.
- `F2`: dock remains open below the measured 480px graph floor → feasibility
  normalization failed; block.
- `F3`: both mobile sheets exist visually or in the accessibility tree →
  single-host invariant failed; block.
- `F4`: Escape clears selection → legacy handler still owns the key; block.
- `F5`: focus lands behind the sheet or on a hidden trigger → focus stack/inert
  contract failed; block.
- `F6`: tray covers toolbar/selection or leaves graph under 320px → tray geometry
  failed; block.
- `F7`: Fit renders canonical labels below 15px → readability floor failed;
  retain contained navigation instead.

## Result

The modeled sequence reaches the final state with `S` preserved on every
presentation-only turn, one mobile dialog, deterministic Escape priority, and
recoverable focus. This proves internal contract consistency only. Browser and
human evidence remain required after implementation.

