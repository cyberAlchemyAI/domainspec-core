# TASK-WCP-05: Quarantine and rebuild

## SWU-WCP-007

- Layer/slice/wave: L0, S-WCP-03, W2.
- Dependency: SWU-WCP-006 pass.
- Primary behavior: refuse a suspect generation, record quarantine externally,
  and rebuild an exact fresh sibling from canonical YAML.
- Algorithm: select one negative-control suspect; fresh admission must return
  zero; write external quarantine receipt; construct new sibling from fresh
  YAML; fully verify; only then query and compare exact bytes.
- Inputs: suspect isolated generation, canonical fixture, frozen manifest.
- Outputs: quarantine receipt, sibling build/verification receipt, exact
  comparison.
- Edge cases: quarantine marker inside DB, partial prefix reuse, in-place
  repair, read-before-verify, stale YAML, non-exact sibling.
- Write scope: exact recovery/sibling/session directories.
- Done: suspect is never served; no database receipt key exists; sibling matches
  every frozen digest and query byte; YAML unchanged.
- Validation: full key enumeration of suspect/sibling, external receipt path
  check, query admission logs, exact manifest comparator, YAML guard.
- Execution owner: Task Session local.

## Split analysis

Quarantine and rebuild remain together because the recovery claim needs both
zero trust in the suspect and a fresh exact path from canonical YAML. In-place
repair is explicitly excluded.
