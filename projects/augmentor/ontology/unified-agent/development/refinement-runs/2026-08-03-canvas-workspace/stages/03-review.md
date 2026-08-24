# Stage 03 — Define review

- Capability: `interrogation`
- Mode: `refine-review`
- Status: `pass-with-flags`
- Human questions asked: 0

The confirmed route already resolves the only choice that would materially
change the architecture: docked support panels were selected over floating
cards or modal-only drawers. Asking another question would not reveal a current
blocker, so no user answer is invented.

## Pressure test

| Concern | Result | Required response |
| --- | --- | --- |
| Does “everything is the canvas” accidentally create an unbounded/infinite canvas? | Pass | Define the canvas as the bounded workspace viewport and keep graph overflow internal. |
| Can minimizing Details destroy selection? | Pass | Selection remains semantic state; panel visibility is separate. |
| Can two desktop docks make the graph unreadably narrow? | Flag | Cap dock widths and provide Focus canvas; validate at 1440 and an intermediate desktop width. |
| Can mobile panels cover one another? | Pass if enforced | Use a mutually exclusive `activeMobileSheet` state. |
| Can Escape conflict with the current “clear selection” behavior? | Flag | Revise the contract: close the topmost temporary surface first; only an explicit Clear selection clears selection. |
| Does the tray hide important evidence? | Flag | Keep persistent labelled tray toggle and status/count cues; do not imply minimized means resolved. |
| Does larger node geometry solve text collisions by itself? | No | Wrap labels, recalculate edges/anchors from shared geometry, and test actual bounds. |
| Does the design imply runtime support? | Pass | Preserve `candidate-local`, `interpretive-read-model`, and `authority_effect:none` in the shell. |

## Review decisions

1. The graph is persistent, but not literally always unobscured; open docks may
   reduce its usable viewport. This is acceptable only with bounded dock widths,
   contained graph navigation, and a one-action focus mode.
2. Desktop uses non-modal docks. Mobile uses modal-like bottom sheets with a
   backdrop and focus containment, but only one sheet exists at a time.
3. The header's trust boundary remains visible even when support panels are
   minimized; it is not buried in the evidence tray.
4. Zoom acts on the graph viewport, not browser text. Browser zoom and text
   scaling must continue to work independently.

## Named residue

- Real users have not confirmed that the workspace model is easier to learn.
- The minimum comfortable intermediate desktop width is not yet measured.
- A 15px label is a design target, not evidence of subjective readability.
- The text alternative's adequacy for low-vision users remains a human-study
  question.

No blocking definition gap remains. Handoff to the no-research decision.

