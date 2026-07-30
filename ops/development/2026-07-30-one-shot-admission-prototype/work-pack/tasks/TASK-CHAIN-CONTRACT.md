# TASK-CHAIN-CONTRACT

## SWU-OAP-003 — Freeze additive public chain contracts

- Primary behavior: express one versioned chain configuration, immutable
  transition, and semantic NO_OP proof against the WPRA manifest vocabulary.
- Dependencies: OAP-001.
- Write scope:
  - `arcanum/spells/task-session-until-blocker/README.md`
  - `arcanum/spells/task-session-until-blocker/schemas/chain-config.schema.json`
  - `arcanum/spells/task-session-until-blocker/schemas/chain-transition.schema.json`
  - `arcanum/spells/task-session-until-blocker/schemas/closeout-no-op-proof.schema.json`
- Algorithm:
  1. Bind the exact manifest, approved epoch, frontier, budget, and risk ceiling.
  2. Define hash-linked transition identity and exclusive-create policy.
  3. Define NO_OP proof inputs and Continuation Router verification.
  4. Require compensation policy `none` with rationale or `owner-routed`.
- Done criteria: schemas parse and reject missing approval, cursor, NO_OP, or
  compensation fields.
- Validation: JSON parse and schema meta-validation.
- Execution owner: local fallback under candidate fast lane.
