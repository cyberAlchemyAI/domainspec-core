# TASK-OVSS-03 — Projection Algebra, Verifier, And Receipt

- Layer/slice: L0; S-003
- Wave: W0
- Objective: deterministically produce one Markdown view whose semantic emissions are independently recomputable.
- Sources: Stage 06 sections 3.7–3.9; Stage 08 R3–R4 and toy game
- Dependencies: TASK-OVSS-02 complete
- Proposed write scope: `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/projection/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/projection/`
- Current gate: blocked by B-004

## SWU-OVSS-006 — Markdown operation graph

- Primary behavior: compile Markdown and ProjectionTrace using only the closed operation algebra and structural-token allowlist.
- Acceptance boundary: same model/definition/compiler/template yields byte-identical view and trace; every semantic span has exact input selectors.
- Split analysis: compiler output and trace are one acceptance boundary; a trace without output or output without trace is incomplete.
- Dependencies: SWU-OVSS-005.
- Source anchors: Stage 08 R3/R4.
- Write scope: Markdown compiler and positive fixtures only.
- Done: deterministic HumanView/Trace plus generated non-authority banner.
- Validation: exact command requires B-004; repeat byte equality mandatory.
- Execution owner: Sigil Development-owned Task Session route.
- Handoff: graph/query and authoring UX remain deferred.

## SWU-OVSS-007 — Independent projection verification

- Primary behavior: independently re-execute the operation graph and issue a ProjectionReceipt only on exact equality.
- Acceptance boundary: stale source, fake trace, invented stronger state, template claim, current time, wrong output digest, and direct writeback posture each fail distinctly.
- Split analysis: verifier, negative fixtures, and receipt are one trust decision; the projector cannot validate itself.
- Dependencies: SWU-OVSS-006.
- Source anchors: Stage 07 trace/template attacks; Stage 08 T1–T5/T11.
- Write scope: verifier, receipt emitter, and negative fixtures only.
- Done: positive receipt and one discriminating receipt/block result per negative.
- Validation: exact command requires B-004.
- Execution owner: Sigil Development-owned Task Session route.
- Handoff: receipt is evidence only and cannot admit/promote.

## Synchronization

W0 closes only after independent verification and negative controls. A generated
view is never copied into public documentation as if it were admitted source.
