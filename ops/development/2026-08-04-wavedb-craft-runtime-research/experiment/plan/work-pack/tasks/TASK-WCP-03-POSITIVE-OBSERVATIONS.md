# TASK-WCP-03: Positive observations

## SWU-WCP-004: exact B0/B1 normal path

- Layer/slice/wave: L0, S-WCP-02, W1.
- Dependency: SWU-WCP-003 pass.
- Primary behavior: import B0, verify/query every row and index, compare derived
  bytes, then build the independently frozen B1 digest generation.
- Inputs: frozen manifests and adapter.
- Outputs: complete normal-path event bundle, exact byte/hash comparisons,
  isolated stores.
- Edge cases: any count-only or semantic-only comparison is insufficient;
  earlier generation must never satisfy changed YAML.
- Write scope: exact normal run/store/session directories.
- Done: every key/value/count/H_L/H_S/H_P/H_I/H_C matches and YAML pre/post
  bytes match.
- Validation: full manifest comparator, query corpus comparator, derived byte
  comparator, YAML guard.
- Execution owner: Task Session local.

## SWU-WCP-005: iterator visibility

- Layer/slice/wave: L0, S-WCP-03, W2.
- Dependency: SWU-WCP-004 pass.
- Primary behavior: observe the old stream across the B1 barrier and a newly
  opened new stream without claiming a general database snapshot.
- Algorithm: open old iterator; record first byte-exact item; build B1 in its
  different generation; drain old iterator; open/drain new iterator; compare
  each stream with its complete frozen manifest.
- Edge cases: nondeterministic barrier, missing event, hybrid stream, prefix
  subset, order drift. All block.
- Write scope: exact iterator run/store/session directories.
- Done: old and new streams each match one full manifest; no hybrid.
- Validation: event ordering/barrier validator plus exact stream comparator.
- Execution owner: Task Session local.

## Split analysis

Normal query correctness and iterator visibility produce independent evidence
and are separate SWUs. Each stream pair remains one iterator SWU because hybrid
detection needs the joint old/new comparison.
