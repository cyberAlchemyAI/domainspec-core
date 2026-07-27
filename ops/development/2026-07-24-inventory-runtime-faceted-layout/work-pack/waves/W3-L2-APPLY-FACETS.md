# W3: L2 Apply And Faceted Admission

- Decision: are sequential writes attributable and new facets conformant?
- Ordered SWUs:
  1. `SWU-IFR-003`;
  2. `SWU-IFR-004`;
  3. `SWU-IFR-005`.
- Parallelism: forbidden because these units share append/projection code.
- Entry: W2 receipt.
- Exit: partial-mutation fixtures, new-entry path admission, legacy
  compatibility, and exact facet projections pass.
- Promotion: unlock W4.

