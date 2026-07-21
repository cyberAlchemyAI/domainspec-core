---
module: backend-type-test-engine-completeness
version: current
status: decision-synchronized-awaiting-task-session
updatedAt: 2026-07-17
docType: implementation-layering
---

# Implementation Layering: Backend Type Test Engine Completeness

## Purpose

Sequence the smallest evidence-bearing path from the existing four-kind node package to exact structural verification for all 13 backend kinds. Layer promotion is evidence-based and does not admit a release.

## Global Boundary

The composability path is `work-pack → wave → task → SWU → receipt`. The active backend release dependency is `FPR-02B → FPR-03 → FPR-04 → FPR-07`; `FPR-02U` is an independent development lane and this package cannot skip either lane's owners. The accepted FPR-02B gate removes the decision dependency but does not grant implementation or production authority.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included scope | Deferred scope | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 — Shared criterion proof | After this layer, we know whether one YAML criterion contract can validate Markdown, generated instances, and minted nodes without type-specific rule duplication. | Shared kernel plus adapters covering all eight current rule forms on representative kinds. | Strict YAML subset parsing, preflight, canonical subject, stable violations, parity tests. | All-13 corpus, obligation catalogue, generated tests. | Existing validator suites remain green; representative positive and negative node cases pass/fail identically. | Continue only if no adapter invents semantics and old behavior is preserved. |
| L1 — Exact backend breadth | After this layer, we know whether the successor node/edge style can represent and discriminate every ratified backend kind and signature. | Candidate backend profile plus 13 positive nodes, 16 positive edges, and typed mutants. | Exact kind/signature/schema binding, independent edge roots, resolver scope, deterministic graph/source manifest. | Independent obligations and executable tests. | `13/13` kinds, `16/16` signatures, causal node/edge witnesses, no UI, stable graph and source anchors. | Continue only after every kind and signature is positively exercised. |
| L2 — Independent verification generation | After this layer, we know whether the engine derives exactly the authority-owned structural obligation set and executes every check. | Digest-bound `O_spec`, graph adapter, `O_gen`, executable tests, exact-set comparator, per-key mutation evidence. | Structural formation obligations only; zero skip/todo/orphan/unrunnable. | Relationship breadth, semantic satisfiability, code conformance. | `O_spec = O_gen = T_gen = E_run`; every key has execution and killed mutation evidence. | Continue only if the denominator is not owned solely by the generator. |
| L3 — Release-gate integration | After this layer, we know whether the backend structural claim and both downstream consumer proofs fail closed and are reproducible as one governed validation surface. | Integrated BTE/IOLM/Body War manifest, missing/empty witness negatives, aggregate command, deterministic receipt, independent replay. | Consumer handoffs and non-admission closeout. | UI, semantic satisfiability, business correctness, production authorization. | Clean replay, seeded red failures, exact digests/counts, no false-green missing input, consumer parity. | Route evidence to FPR-04/FPR-07 owners; do not self-admit release. |

## Layer Boundary Heuristic

- L0 stops when the rule evaluator and adapter boundary are proven; adding types before this proof would multiply duplicated logic.
- L1 stops at exact node-formation breadth; relationship and semantic breadth answer different decisions.
- L2 stops at executable structural verification; code conformance and business satisfaction are separate contract planes.
- L3 stops at a reproducible non-admission receipt; release authorization remains external.

## Non-Regression Guardrails

- Existing engine, content/instance, minted compiler, and deterministic-output tests must remain green.
- The four-kind experimental profile remains valid until a separately versioned successor is admitted.
- Missing or empty release witnesses must never pass as complete, even if an empty minted project remains valid at the base compiler layer.
- Generated artifacts never become semantic authority.
- Backend-only coverage cannot be described as full-language coverage.

## Recommended Next Layer

- Next layer: L0 continuation, after a separate authorized Task Session selects `SWU-BTE-003`.
- Next executable SWU: `SWU-BTE-003` minted-node body adapter.
- Decision unlocked: whether minted node bodies can reuse the proven YAML criterion kernel across all eight rule forms without semantic invention or a competing evaluator.
- Major deferred scope: UI/full-language completeness, semantic/application correctness, and production authorization. Backend relationship breadth is now in scope for this package.
