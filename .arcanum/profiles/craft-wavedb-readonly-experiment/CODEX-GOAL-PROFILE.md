# Codex Goal Profile Result

- Source work-pack: `ops/development/2026-08-04-wavedb-craft-runtime-research/development/refinement-runs/20260805T184540Z-craft-wavedb-api/WORK-PACK.md`
- Selected unit: proposed one-shot `CRAFT-WAVEDB-READONLY-EXPERIMENT-001`; not yet admitted
- Readiness: `block` — proposal coverage passes, runtime admission is absent
- Goal budget: 4,000 characters; compact goal validation required below
- Decision profile: none; consumed fields: n/a
- One-shot mode: yes
- Capability policy: after admission, native Goal plus one `task-session` per serial node; `decision-gate` is stop/report only; no ambient `invoke`, `refine`, `craft`, or subagent authority
- Sidecar profile: `.arcanum/profiles/craft-wavedb-readonly-experiment/CONTEXT-PACK.md`
- Native Goal:

```text
/goal Complete the admitted one-shot `CRAFT-WAVEDB-READONLY-EXPERIMENT-001` exactly as defined by `.arcanum/profiles/craft-wavedb-readonly-experiment/CONTEXT-PACK.md` and `context-index.json`. Read and hash-check that pack first. Execute `CWE-001 -> CWE-002 -> CWE-003` serially through one bounded Task Session per node only after an applied Work Pack refresh admits the stream, exact route, write root, validation commands, and receipts, and after the operator separately authorizes execution. Bind to Node v26.6.0, the existing local `@vijayee/wavedb@0.15.9` module, accepted tarball/addon hashes, manifest `craft/manifest/v2`, 28-ledger inventory, 57 records, and original-store digest. Confine all writes, disposable store copies, code, fixtures, logs, and receipts to `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-wavedb-readonly-experiment/`. Do not fetch, install, rebuild, vendor, or substitute dependencies. Prove two independent fresh-process readers against isolated copies; implement only `status`, `verify`, `list-ledgers`, and manifest-bounded `get-raw`; make no WaveDB writer or Subtree surface reachable; run disposable-copy missing/damage/open/read failure controls; validate all receipts; and prove canonical ledgers plus the accepted original store are byte-unchanged. Iterate only within the admitted node and write root. If admission or execution authorization is absent, any bound path/hash drifts, a critical check fails, original bytes change, or work would require network, API/HTTP/auth, product paths, Git mutation, npm publication, Docker, deployment, Craft mutation, extra capabilities, or broader scope, stop blocked without widening and report exact evidence. Complete only with one terminal receipt carrying the context pack's maximum claim, and leave every API/product successor unselected.
```

- Verification surface: currently unavailable as executable commands; the
  applied Work Pack refresh must materialize exact commands for node tests,
  receipt validation, input/output hashing, and terminal closure before readiness
  can change to `pass`
- Boundaries: future writes only below
  `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-wavedb-readonly-experiment/`;
  accepted store, canonical ledgers, and resolved dependency are read-only inputs
- Handoff pack: `.arcanum/profiles/craft-wavedb-readonly-experiment/CONTEXT-PACK.md`
  and `.arcanum/profiles/craft-wavedb-readonly-experiment/context-index.json`
- Strict coverage: `pass` for proposal sources and obligations; runtime readiness
  remains `block`
- Fallback exploration: none; any newly needed source is a named gap requiring a
  reviewed refresh
- Extra-source reporting: required if a later refresh authorizes named-gap
  exploration; otherwise n/a
- Stop condition: stop without experiment mutation while `allowedRoutes` is empty,
  the stream/write root/commands are unadmitted, or execution authorization is
  absent; during an admitted run, stop on any identity drift, failed critical
  check, original-byte drift, or boundary expansion
- Validation: proposal structure, source hashes, JSON syntax, cross-file IDs, and
  native Goal length only; no experiment command or Goal was run

## Admission gate

This command is intentionally not runnable from the current Work Pack. Before it
may be used, an applied Invoke Refresh must:

1. select the one-shot stream and its strict node order;
2. add the exact allowed capability route;
3. own the experiment-local write subpaths and exact validation commands;
4. bind each node to a Task Session and receipt contract; and
5. preserve the terminal claim ceiling and no-successor rule.

The operator must then authorize execution separately. Proposal creation is not
that authorization.
