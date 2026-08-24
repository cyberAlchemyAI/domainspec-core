# W0 — Baseline and admission preflight

Goal: establish current bytes and authorize no mutation.

Required evidence:

- selected unit is exactly `SWU-OCA-001`;
- execution-time Context Builder output resolves every source/write path;
- material package binds producer schema, SWU, unique attempt, and current hashes;
- Arcanum is on `main`; its current HEAD and dirty paths are classified;
- target paths have no unrelated live change;
- mutation admission contract is satisfied.

Stop if any binding is missing, stale, synthetic, or broader than OCA-001. A W0
pass admits Task Session to execute only OCA-001; it does not admit later waves.
