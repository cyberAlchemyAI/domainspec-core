# W0 — local source-build proof

- Layer question: under which exact local Node toolchain, if any, can reviewed
  WaveDB source produce one loadable, upstream-tested addon?
- Ordered units: SWU-WCSB-001 passed; SWU-WCSB-002 produced a preserved Node 22
  block; SWU-WCSB-003 is the selected Node 26 controlled diagnostic.
- Entry: original Define/Design/Plan/Dispatch/Distill and runner receipts pass;
  direct user selected exact Node `v26.6.0`/npm `11.18.0`; retry dispatch passes.
- Parallelization: none.
- Gate before SWU-WCSB-003: Invoke Refresh owner receipt selects only the fresh
  attempt `wcsb-20260805-node26-01`, and Task Session admission rehashes every
  controlling target.
- Current state: Node 22 compiled and loaded the addon but blocked in the first
  upstream concurrent-write test. The Node 26 diagnostic is selected; it has
  no execution evidence yet.
- Historical blocker: `WCSB-UPSTREAM-CONCURRENT-WRITE-STALL` remains open for
  the Node 22 observation. Node 26 is a diagnostic variable, not a resolution.
- Exit: every Node 26 source-build gate and live validator passes, followed by
  a joined SWU-WCSB-003 closeout with no same-pack successor.
- Stop: any acceptance-critical failure, attempt collision, previous-attempt
  mutation, NVM default change, or missing owner join.
- Promotion evidence: a passing L0 result may be offered to a separate parent
  refresh; it cannot enter L1 or Craft automatically.
