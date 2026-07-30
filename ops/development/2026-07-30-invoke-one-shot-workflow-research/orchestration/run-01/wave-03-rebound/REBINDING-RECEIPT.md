# Native action-ID rebinding receipt

- Source gate: `g-synthesis` — PASS
- Raw action set:
  `orchestration/run-01/wave-03-raw/next-actions.json`
- Defect: the reducer used the current wave length as the next action-number
  offset and emitted `spawn-0002`, `spawn-0003`, and `spawn-0004`, all of which
  already exist in this run.
- Safety consequence: replaying those IDs would violate the host profile's
  exactly-once action contract and make the causal event stream invalid.
- Bounded repair: call the same canonical
  `_compile_named_wave_actions(...)` function for the already-admitted
  `skeptics` wave with cumulative start number `5`.
- Rebound IDs: `spawn-0005`, `spawn-0006`, `spawn-0007`.
- Semantic delta: none. Wave, roles, capability, targets, modes, mutation
  policies, read/write scopes, input references, and output references are
  unchanged.
- Runtime source was not modified.

This is orchestration-runtime residue and a concrete example of a predictable
mid-route blocker caused by an incomplete cross-wave execution binding.
