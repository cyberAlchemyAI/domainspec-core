# W0 — local source-build proof

- Layer question: after W0, do we know whether the reviewed WaveDB source can
  produce one loadable, upstream-tested addon on the exact local toolchain?
- Ordered units: SWU-WCSB-001, then SWU-WCSB-002.
- Entry: Define/Design/Plan/Dispatch/Distill pass; user source-build
  authorization recorded.
- Parallelization: none; SWU-WCSB-002 consumes the exact runner receipt.
- Gate after SWU-WCSB-001: terminal and Invoke Refresh owner receipts pass and
  uniquely select SWU-WCSB-002.
- Current state: SWU-WCSB-001 passed its ten-case fixture matrix and exact
  material validation; SWU-WCSB-002 is the sole selected unit.
- Exit: source-build receipt passes live validator and SWU-WCSB-002 closeout
  joins with no same-pack successor.
- Stop: any acceptance-critical failure or missing owner join.
- Promotion evidence: L0 result may be offered to a separate parent refresh;
  it cannot enter L1 automatically.
