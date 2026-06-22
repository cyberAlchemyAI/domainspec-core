# Proposed Research Dispatch Sheet

Dispatch ID: `2026-06-17-ternary-models-research`

Status: proposed, not registered, not run

Working folder: `research/ternary-models/_dispatch`

## Goal

Study, research, and develop a source-backed local research tower for ternary
models, separating owned prior art, current BitNet-era LLM claims, systems
feasibility, and next buildable work.

## Confirm-Gate Boundary

This sheet is subject to the DomainSpec subagents strategy lifecycle. It may be
registered and run only after:

1. the two-agent check-tension gate passes;
2. the human explicitly confirms the frozen sheet.

## Groups

### explorers

- `n`: 4
- `anti_bias`: source-corpus
- agents:
  - Shannon, Claude: modern BitNet and native low-bit LLM source corpus.
  - Turing, Alan: classic ternary quantization and model-compression source corpus.
  - Wiener, Norbert: systems and inference-runtime source corpus.
  - Friston, Karl: development path and experiment-design source corpus.

Pairwise predicted disagreement evidence:

- Shannon runs modern BitNet/native-LLM sources while Turing runs classic ternary
  quantization sources on the source-corpus axis; a bias in Shannon toward
  recent BitNet claims would be exposed by Turing's older TTQ/TWN/TernaryBERT
  lineage.
- Shannon runs modern BitNet/native-LLM sources while Wiener runs systems and
  inference-runtime sources on the source-corpus axis; a bias in Shannon toward
  architecture claims would be exposed by Wiener's kernel/runtime constraints.
- Shannon runs modern BitNet/native-LLM sources while Friston runs development
  path and experiment-design sources on the source-corpus axis; a bias in
  Shannon toward paper claims would be exposed by Friston's demand for a
  buildable evidence route.
- Turing runs classic quantization sources while Wiener runs systems and
  inference-runtime sources on the source-corpus axis; a bias in Turing toward
  algorithmic compression would be exposed by Wiener's hardware/runtime checks.
- Turing runs classic quantization sources while Friston runs development path
  sources on the source-corpus axis; a bias in Turing toward historical method
  taxonomy would be exposed by Friston's first-build feasibility lens.
- Wiener runs systems/runtime sources while Friston runs development path and
  experiment-design sources on the source-corpus axis; a bias in Wiener toward
  kernel feasibility would be exposed by Friston's measurable project-route
  constraints.

### synthesizer

- `n`: 1
- writer: Noether, Emmy
- role: produce cited findings from explorer returns.

### reviewers

- `n`: 3
- `robot_talks`: true
- `anti_bias`: attack-vector
- agents:
  - Russell, Bertrand: precedent gate.
  - Quine, Willard Van Orman: definitional-soundness gate.
  - Tetlock, Philip: non-vacuity gate.

Pairwise predicted disagreement evidence:

- Russell runs the precedent gate while Quine runs definitional soundness on the
  attack-vector axis; a bias in Russell toward "already owned" would be exposed
  by Quine catching claims that are not merely owned but conceptually collapsed
  or mislabeled.
- Russell runs the precedent gate while Tetlock runs non-vacuity on the
  attack-vector axis; a bias in Russell toward literature ownership would be
  exposed by Tetlock requiring measurable witnesses for any development claim.
- Quine runs definitional soundness while Tetlock runs non-vacuity on the
  attack-vector axis; a bias in Quine toward vocabulary correction would be
  exposed by Tetlock asking whether the corrected concept has a concrete test or
  witness.

## Connections

- explorers -> synthesizer: sequential
- synthesizer -> reviewers: zig-zag, loop_cap 2

## Registration Row

The appender-ready JSON row is `proposed-research-dispatch.json`. It intentionally
does not include non-schema tension-evidence fields.
