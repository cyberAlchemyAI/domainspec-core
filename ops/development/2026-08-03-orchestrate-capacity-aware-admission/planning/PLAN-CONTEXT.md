# Plan Context

- Approved design: `../design/ARCHITECTURE.md`
- Design selection: `../design/DESIGN-SELECTION-RESULT.json`
- Design result digest:
  `f1ac2c8335335691d4d0087696ca593a22cd2ddbb1e40c6edd60d8a53cd2a336`
- Delivery boundary: canonical public Orchestrate plus its manifest-declared
  generated surfaces; no host implementation, consumer UI, ontology,
  definition, publication, commit, push, or deployment
- Complexity: high; split output
- Active layer: L0
- First selected SWU: `SWU-OCA-001`
- Runtime context pack: intentionally not generated at Plan; Task Session must
  bind current source digests and unrelated-dirty-work state at execution time
