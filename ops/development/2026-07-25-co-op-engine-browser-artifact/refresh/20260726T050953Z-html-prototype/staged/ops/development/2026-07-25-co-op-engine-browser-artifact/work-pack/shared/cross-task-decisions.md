# Cross-Task Decisions

- `SWU-COOP-001` is the sole selected mutation unit.
- `SWU-COOP-002` is an L0 planned-unselected serial candidate. It cannot begin
  until `SWU-COOP-001` closes, an operator explicitly selects it, and a new
  strict pack passes.
- Use Node 22 built-in test execution with erasable TypeScript; add no runtime
  or development dependencies in L0.
- Inject `asOf`; do not read the wall clock inside admission logic.
- Return stable typed diagnostic codes and paths; do not throw for expected
  invalid records.
- The research-era 48-hour Poker value is a negative fixture because D-003
  approved 72 hours.
- Closeout has no automatic successor.
- The HTML prototype is one self-contained `prototype.html` with semantic
  structure, all fourteen bounded cards, anchor navigation, and inline
  low-fidelity responsive/print styles.
- The prototype contains no JavaScript, forms, external resources, storage,
  network, final Whisper copy, private metadata, or operational exchange
  behavior.
