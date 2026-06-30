---
tags: [inventory, strategy-result, dispatch, subagents, research, long-context, attention, parameter-efficiency, claim-le-proof]
node_type: synthesis
is_session: false
layer: research
nature: reference
status: candidate
created: 2026-06-29
dispatch_id: 2026-06-29-high-attention-low-parameter-models
dispatch_type: research
working_folder: research/high-attention-low-parameter-models/
sources: [research/high-attention-low-parameter-models/research.md, research/high-attention-low-parameter-models/findings.md, telemetry/agents/subagents-dispatch.yaml]
---

# High-Attention Low-Parameter Models Strategy Result

This is a non-authority Inventory read model for the governed research dispatch
`2026-06-29-high-attention-low-parameter-models`. It records the strategy result
and points to the durable research artifacts. It does not promote a model
architecture, benchmark, definition, or novelty claim.

## Strategy Summary

**P1 trigger decision:** dispatch was justified by synthesis, context protection,
isolation, and parallelism. The question combined at least four lenses:
formal attention/KV scaling, information-channel usability, systems/serving
mechanisms, and empirical long-context behavior. The final finding also required
review gates for precedent, non-vacuity, and definitional soundness.

**Lanes / groups:**

- `explorers` ran in parallel with a composite
  `methodology + source-corpus + temporal-prior` anti-bias axis.
- `synthesizer` reconciled explorer returns into a candidate map.
- `reviewers` ran as a robot-talks-style skeptic group on the `attack-vector`
  axis.
- `writer` produced `findings.md` only.
- `auditor` evaluated `findings.md` and approved without revision.

**Subagents and angles:**

- `Abramsky, Samson` — formal/asymptotic resource lens over dense attention,
  KV cache, positional scaling, and parameter independence.
- `Shannon, Claude` — information-channel lens over visible versus usable
  context, distractors, and evidence survival.
- `Hewitt, Carl` — systems/serving lens over paged KV, cache policies, sparse
  attention, retrieval, and production constraints.
- `Simon, Herbert` — empirical/temporal-prior lens over benchmark behavior,
  bounded-rationality lineage, and parameter-normalized utility.
- `Noether, Emmy` — synthesizer.
- `Russell, Bertrand` — precedent skeptic.
- `Kahneman, Daniel` — non-vacuity skeptic.
- `Quine, Willard Van Orman` — definitional-soundness skeptic.
- `Turing, Alan` — writer.
- `Brandenburg, Martin` — auditor and final approver.

**Dependency flow:** explorers -> synthesizer -> reviewers -> writer -> auditor.
The sheet included synthesizer<->reviewers zig-zag (`loop_cap: 2`),
synthesizer->explorers feedback (`loop_cap: 1`), and auditor->writer feedback
(`loop_cap: 1`). No feedback edge fired after audit; the auditor approved the
writer output.

**Gate / ledger state:** the first check-tension pass found a Test-3 spread flaw
in the explorer group; the sheet was revised to make the explorer axes explicit.
The second check-tension pass returned double PASS. The dispatch row and close
row are both appended to `telemetry/agents/subagents-dispatch.yaml`; close state
is `exit_reason: resolved` with 10 agents spawned and `loops_used: 1`.

## Result

The dispatch answer is conservative: small-parameter models can expose large
visible context windows, but large usable context remains an empirical behavioral
property. Strict big attention means dense retained-token attention and remains
costly; retrieval, KV/cache engineering, recurrence, compression, sparse
attention, and positional extension are neighboring mechanisms, not synonyms for
strict big attention. The clean research lane is a parameter-normalized usable
context harness under position, distractor, reasoning, KV-policy, and
retrieval-vs-raw-context stress.

## Source Refs

- `research/high-attention-low-parameter-models/research.md` — explorer
  transcript.
- `research/high-attention-low-parameter-models/findings.md` — auditor-approved
  synthesis and experiment harness.
- `telemetry/agents/subagents-dispatch.yaml` — dispatch and close rows.

## Downstream Use

Use this entry when planning long-context small-model experiments, evaluating
claims about "big attention," or preparing a research-evidence harness. Do not
use it as a novelty claim for any existing mechanism; the findings explicitly
classify the mechanism families as already-known/already-deployed or
build-from-owned.

## Residue

- The proposed harness is not implemented here.
- No benchmark fixtures or model runs were executed.
- Million-token small-model usable-context claims remain unproven until a
  witness tuple and kill criteria are satisfied.
