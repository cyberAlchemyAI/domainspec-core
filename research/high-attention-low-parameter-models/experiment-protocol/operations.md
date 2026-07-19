# Operations: High-Attention, Low-Parameter Experiment Protocol

## FreezeProtocol

**Actor:** experiment owner

Inputs: draft protocol, approved decision records, source-evidence handles.

Rules:

1. Every required decision has an approved value.
2. Every outcome and gate has a machine-readable rule.
3. Every artifact contract has a version and validation surface.
4. No typed KILL is contradicted.

Postcondition: an immutable protocol version and hash are emitted; otherwise the
protocol remains `decision_gated`.

## MaterializeCorpus

**Actor:** fixture builder

Inputs: frozen protocol, generator version, master seed, family split, provenance
manifest.

Ordered behavior:

1. Generate a semantic plan independently of evidence position and prompt arm.
2. Assign stable evidence and decoy IDs.
3. Render early/middle/late and required arm variants from the same plan.
4. Record bytes, token IDs after the admitted template is known, and hashes.
5. Validate answer/evidence ground truth and family-level split isolation.

Failure leaves no partially admitted corpus.

## AdmitModelStack

**Actor:** platform owner

Inputs: checkpoint snapshot, tokenizer/template, runtime/backend, hardware
manifest, candidate context lengths.

Rules:

1. Verify immutable identities and access/license conditions.
2. Smoke the exact chat template and output grammar.
3. Produce one capacity witness per model/length cell.
4. Reject any prohibited fallback behavior.

Postcondition: only witnessed cells become `admitted`.

## RenderTrialCell

**Actor:** trial planner

Maps one fixture/arm/position/model tuple to exact rendered bytes and token IDs.
It must fail closed on overflow; it cannot truncate or silently select a shorter
length.

## ExecuteTrialCell

**Actor:** experiment harness

Preconditions: frozen protocol, admitted stack/cell, valid render, clean cache
policy, and authorized run phase.

Ordered behavior:

1. Acquire the declared exclusive/shared resource boundary.
2. Apply frozen warmup and cache rules.
3. Execute exactly one attempt with frozen decoding.
4. Preserve raw output and systems telemetry.
5. Emit a `RunReceipt` whether the attempt succeeds or fails.

Retries are new attempts with their own receipts and may not replace the failed
attempt in analysis silently.

## ScoreTrial

**Actor:** deterministic scorer

Inputs: fixture ground truth, raw output, output grammar, scorer version.

Outputs are separate fields for parse success, answer correctness, evidence
correctness, support/abstention correctness, and false-support eligibility. The
scorer must not call an unversioned qualitative judge.

## AnalyzePhase

**Actor:** analysis owner

Inputs: frozen analysis plan, run and score receipts, exclusion ledger,
resource receipts.

Rules:

1. Pair by semantic instance and rotation as declared.
2. Estimate full-context retention, direct checkpoint contrast,
   difference-in-retention when applicable, middle loss, added-evidence
   behavior, and false support.
3. Apply frozen uncertainty and multiplicity rules.
4. Preserve infeasible cells and typed failures.
5. Separate confirmatory outcomes from diagnostic views.

## EvaluatePhaseGate

**Actor:** experiment owner

Consumes the phase result and value-of-information policy. Returns `continue`,
`narrow`, `pivot`, `stop`, or `repeat_after_repair`. It may not promote a later
phase without the earlier layer's named exit evidence.
