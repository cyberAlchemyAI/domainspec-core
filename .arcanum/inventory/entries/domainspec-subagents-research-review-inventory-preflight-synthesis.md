---
tags: [inventory, strategy-result, dispatch, subagents, research, review-change-request, arcanum-runtime, observability, capability, audit, claim-le-proof]
node_type: findings
is_session: false
layer: workflow
nature: reference
status: verified
created: 2026-07-22
sources: [implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md, implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md, implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/review/SKILL.md, .arcanum/observability/reflections/20260722T062328Z-domainspec-subagents-strategy-reflection.md, .arcanum/observability/tmp/domainspec-subagents-strategy-20260722T062301Z-research-review-inventory-preflight.json]
---

# DomainSpec Subagents Research And Review Inventory Preflight

- ID: `domainspec-subagents-research-review-inventory-preflight`
- Type: synthesis
- Status: verified
- Confidence: high

## Correction And Gap

The prior strategy integration exposed two Inventory routes, neither of which
covered ordinary strategy design:

- the maintenance route retrieved prior evidence only when reflecting on a
  correction; and
- the post-result hook ingested durable strategy and dispatch results only
  after they existed.

The router moved from owner-file reading directly to sheet drafting. Its
`research` and `review` type owners did not consume Inventory matches,
exclusions, source references, or gaps while selecting corpora, lenses, lanes,
or agent inputs.

## Design-Time Preflight Contract

Every request classified as a research or review strategy now performs an
automatic read-only Inventory lookup after its preliminary P1 decision and
type resolution, but before a dispatch sheet or inline strategy is finalized.
The lookup:

1. reads `index.json` first when present and parseable;
2. derives terms from the goal, targets, type, contract area, and likely source
   or lens vocabulary;
3. produces a named `strategy-inventory-packet` with selected and excluded
   evidence, selectors, source references, obligation fit, gaps, residue, and
   a non-authority notice;
4. must change a lane, angle, corpus, selector, or agent input, or explain why
   all candidate matches were excluded; and
5. requires no additional permission because it is read-only.

The lookup is inline strategist work. It is not a subagent group, does not
create a dispatch ledger event, and cannot determine P1, authorize dispatch,
satisfy check-tension, or replace human confirmation.

## Research Consumption

Research uses Inventory to seed prior findings, candidate owners, typed
negatives, source leads, and unresolved questions. Relevant packet fields are
routed narrowly to explorers, the precedent skeptic, the synthesizer, writer,
and auditor.

Inventory remains discovery evidence only. Agents must follow source references
and verify load-bearing claims. In particular, `no_inventory_match` cannot
establish `precedent-clean`; the precedent lane must still perform and cite its
actual search.

## Review Consumption

Review uses Inventory to seed earlier audits, governing contracts, regressions,
target selectors, runnable checks, and unresolved risks. Relevant packet fields
are routed narrowly to attackers, verifiers, the synthesizer, and coverage
auditor.

Every surviving finding must still quote and verify the current target.
Inventory alone cannot establish severity, KEEP/FIX, or a change request.

## Failure And Authority Boundaries

- `inventory_unavailable`, `machine_index_gap`, and `no_inventory_match` are
  visible, non-blocking residue.
- An `index.md` fallback is flagged rather than treated as machine-index parity.
- Automatic preflight never expands into Inventory `install`, `query`,
  `ingest`, `backfill`, or `sync`.
- The separate post-result hook still owns durable strategy/result ingestion.
- Experiment and reserved dispatch types are unchanged.
- No public Arcanum artifact or dispatch ledger schema changed.

## Validation

- Repository `index.json` parsed and was searched before source expansion.
- Research match consumption and independent-source proof boundary: pass.
- Review match consumption and literal-artifact proof boundary: pass.
- No-match, machine-index fallback, and unavailable-state clauses: pass.
- Preflight lookup versus post-result ingestion separation: pass.
- Active Codex runtime contract contains the new preflight: pass.
- Changed private owner files pass `git diff --check`.
- Signal Observer appended one deduplicated manual-correction signal; Workflow
  Reflect wrote a one-signal manual-trigger report recommending the targeted
  update.

## Dispatch Boundary

P1 dispatch triggers were not met for this bounded maintenance task. One
read-only observer helper inspected the gap and returned acceptance checks; the
router classifies that as a helper, not a dispatch. No check-tension sheet,
human dispatch confirmation, registration row, or close row was created.

## Residue

The checks prove the instruction contract and active runtime synchronization.
The first live research and first live review strategy invocation remain the
behavioral proof that runtimes consume the packet as specified.

## Next Action

On the next research or review strategy request, run Inventory lookup without
asking, show the packet's effect on the strategy, and preserve the normal
check-tension and human confirmation gates.

Inventory remains a non-authority read model. This entry records a verified
private capability update; it does not promote Inventory evidence or authorize
a future dispatch.
