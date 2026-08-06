# Validation Contracts

## L0 S6 relation witness

At a fixed local viewport and pinned runtime, pause and seek to declared state boundaries. Assert:

- the source PNG digest remains unchanged;
- source and target node kinds are present and distinct;
- the arrow points left to right;
- `enforces` is attached to the edge;
- the terminal semantic state is stable;
- no success/runtime-conformance state exists;
- full captions remain a separate surface;
- reduced motion reaches the same semantic end state without path travel.

Capture DOM/SVG state JSON and screenshots at initial, mid-draw, terminal, and reduced-motion terminal states. Screenshot similarity alone cannot pass semantic assertions.

## L1 S7 owner-gate witness

At `0`, `5000`, and `9999` ms within the selected beat, assert `candidate_max_x < gate_min_x`, `gate_state == closed`, `admission_state == absent`, and no solid post-gate state exists. Repeat under reduced motion. This is deferred until L0 proves the harness.

## Common negative fixtures

- source hash drift;
- consultation status not `ok`;
- documentation evidence mislabeled `executed_witness`;
- reversed S6 arrow;
- detached verb label;
- standard/reduced semantic-end-state mismatch;
- S7 candidate overlapping the gate;
- full captions collapsed into decorative text;
- succeeded WorkEpisode mislabeled verified Lesson.

Every negative fixture changes one cause and must fail for the named reason.
