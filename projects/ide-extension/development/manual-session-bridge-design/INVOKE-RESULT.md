# Invoke Result

- Mode: `design`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library
- Phase status: `pass`
- Mode contract: `spells/invoke/design.md`
- Outputs: `ARCHITECTURE-BUNDLE.md`, `UX-PLAN.md`,
  `GLOSSARY-CONSISTENCY.md`, `IMPLEMENTATION-LAYERING-SEED.md`,
  `DESIGN-TRANSPORT.md`, `EXPERIMENT-EVIDENCE.md`, `DECISIONS.md`,
  `manual-session-bridge.dispatch.json`
- Design views: context, high-level structure, low-level components, workflow
  process, decision flow, dependency interface - complete
- Glossary consistency: `pass`; separate authorization/execution receipt types
  and terminal-result consumption semantics are accepted design deltas
- Dispatch techniques: `sequence`, `concrete_path_evidence`, `frame_handoff`,
  `owner_boundary_check`, `delegation_boundary`, `authority_split_gate`,
  `approval_semantics_map`, `state_namespace_boundary`,
  `execution_receipt_handoff`, `artifact_contract_bridge`, `validation_loop`,
  `residue_ledger`, `scu_swu_reduction`, `recomposition_proof`,
  `handle_handoff`; full dispatch validation recorded in the dispatch artifact
- Distill validation: `pass`; one read/preview request through desk target
  selection, explicit poll, atomic claim, late disclosure, operator recovery,
  execution, and result receipt recomposes into the existing kernel
- Implementation layering: `IMPLEMENTATION-LAYERING-SEED.md`; L0-L3 coverage
  with L0 active and stronger execution boundaries deferred
- Work-pack: n/a in design mode
- Decisions: `DECISIONS.md` passes with five blockers resolved; L0 is read-only,
  uses two receipts, operator release/requeue, unattested local sessions, and one
  desk-selected poll target
- Unresolved design blockers: none
- Planning obligations: spec/typestate/receipt migration; target/claim/recovery/
  result APIs; UI states; fake claimant and real manual witness validation
- Deferred: persistent worker, authenticated identity, timed recovery,
  mutation-capable execution, and IDE/browser integration
- Next route: `plan`

The design package does not modify runtime code and does not claim the bridge is
implemented. It turns the experiment into a plan-ready architecture with the
missing proof boundaries made explicit.
