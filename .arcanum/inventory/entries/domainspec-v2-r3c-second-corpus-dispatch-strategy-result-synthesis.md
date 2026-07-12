---
tags: [inventory, strategy-result, dispatch, subagents, domainspec-v2]
node_type: synthesis
is_session: false
layer: strategy
nature: reference
status: proposed
created: 2026-07-12
dispatch_id: 2026-07-12-r3c-second-corpus-selection
dispatch_type: research
working_folder: projects/domainspec-v2/development/r3-closeout-plan/research/2026-07-12-second-corpus-selection/
sources: [projects/domainspec-v2/development/r3-closeout-plan/DECISIONS.md, projects/domainspec-v2/development/r3-closeout-plan/WORK-PACK.md, projects/domainspec-v2/development/r3-closeout-plan/work-pack/tasks/TASK-R3C-CORPUS.md]
---

# DomainSpec v2 R3C Second-Corpus Dispatch Strategy Result

This is a non-authority Inventory read model of the proposed, unregistered
`SWU-R3C-004` corpus-selection strategy. It records a human-gated dispatch
design, not approval, execution, corpus selection, or relationship authority.

## P1 Trigger Decision

Dispatch is justified by synthesis, isolation, and parallelism: candidate
corpora must be searched across several repo-owned source surfaces, while a
separate formal lens must reject duplication and invented business semantics.

The full SWU is not delegated as code. `dispatch_type: code` is reserved. The
live research dispatch ends at a source-backed select/reject/no-suitable
recommendation; the parent Task Session owns any later mutation and validation.

## Lanes And Subagents

- `corpus_explorers`: Shannon, Claude performs empirical reuse-oriented corpus
  inventory; Noether, Emmy derives formal DS-D8/SWU obligations and rejects
  candidates without owned semantics. Their composite methodology plus
  source-corpus axis is explicitly tensioned.
- `corpus_synthesizer`: Turing, Alan reconciles the returns into a cited
  candidate matrix.
- `corpus_reviewers`: Popper, Karl applies a non-vacuity witness gate; Lakatos,
  Imre applies a definitional-soundness/no-invention gate. Their attack-vector
  axis is explicitly tensioned.
- `corpus_writer`: Baez, John persists `findings.md` only.
- `corpus_auditor`: Brandenburg, Martin evaluates `findings.md` only and is the
  independent final approver.

## Dependency Flow

`corpus_explorers -> corpus_synthesizer <-> corpus_reviewers -> corpus_writer
-> corpus_auditor`, with one bounded synthesizer/reviewer exchange and one
bounded auditor-to-writer revision. No explorer feedback edge is predeclared.

## Gate And Ledger State

- Check-tension: double PASS from independent read-only gate agents.
- Human confirmation: pending.
- Registration: not registered.
- Dispatch ledger: unchanged by this proposal.
- Expected closeout after confirmation: exactly one dispatch append, one close
  append, an explicit exit reason and spawn report, result inventory, and
  observability synchronization.

## Next Human Action

Choose one option in
[DEC-R3C-004-DISPATCH](../../../projects/domainspec-v2/development/r3-closeout-plan/DECISIONS.md#dec-r3c-004-dispatch--second-corpus-execution-route):
confirm the checked research dispatch, explicitly reassign the SWU to local
parent execution, defer it, or request more context. Silence does not confirm.
