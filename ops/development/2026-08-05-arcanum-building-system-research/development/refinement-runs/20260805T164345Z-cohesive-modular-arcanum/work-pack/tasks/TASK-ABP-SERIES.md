# TASK-ABP-SERIES — Consolidate Ordered-Series Ownership

Objective: implement the approved series-owner decision without changing one-SWU Task Session authority.

Dependencies: `DECISION-ABP-SERIES`, lifecycle-owner acceptance, and L1 pass.

## SWU-ABP-012 — Canonical until-real-blocker profile

- Behavior: selected series owner runs exactly one frontier/visited/action/retry/join/stop state machine.
- Write scope: selected owner package after Decision Gate.
- Acceptance: fresh Task Session receipts alone complete units; owner receipts only reclassify entries.
- Validation: finite frontier, replay, retry, timeout, and stop fixtures.

## SWU-ABP-013 — Stateless compatibility facade

- Behavior: `task-session-until-blocker` delegates to the canonical profile and returns its receipt without independent state.
- Write scope: `arcanum/spells/task-session-until-blocker/`
- Acceptance: no chain ledger/reducer/frontier mutation remains in the facade path.
- Validation: forbidden second-writer tests and compatibility examples.

## SWU-ABP-014 — Legacy migration fixtures

- Behavior: replay captured legacy cases through the canonical owner and classify exact compatibility differences.
- Write scope: exact selected owner and facade fixture roots after owner planning.
- Acceptance: parity or named block; never silent semantic translation.
- Validation: fixture matrix and one-authoritative-writer proof.

Closeout targets are `WORK-PACK.md`, this task, and `evidence-index.json`, plus lifecycle-owned artifacts explicitly named later. Refresh and lifecycle receipts remain separate.

