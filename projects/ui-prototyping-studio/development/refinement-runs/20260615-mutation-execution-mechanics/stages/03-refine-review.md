Artifact written to: /home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/03-refine-review.md

# Refine-Review: Mutation Execution Mechanics (verdict: FLAG)

Adversarial critique of the s2 Define, with every load-bearing claim re-grounded against the real code (apply-approved-batch.ts, domain/models.ts, module tree).

## Problem framing — mostly correct
- The apply(approvedBatch, currentHtml, sessionContext) -> {nextHtml, diffSummary', provenance} framing and "real gap" claim are accurate to the code (apply is pure bookkeeping; htmlArtifactRef never touched; MutationTask feeds only buildDiffSummary + appliedTaskIds).
- F1: framing is single-batch/happy-path; partial realization, retry, task interaction are in-scope mechanics that are unnamed.
- F2: sessionContext (third arg) is never defined; engine visibility is approach-differentiating.

## Three approaches — fair and distinct, with uneven spots
- A/B/C are genuinely comparable and distinct (where-the-edit-is-decided is a clean non-overlapping axis).
- F3: the "checksum-grade audit chain" is overstated for all three and flatters A. The actual sha256 checksum binds only {sourceRevisionId, generatedFromCommentIds, tasks} = INPUTS; it cannot cover produced HTML. And RevisionManifestEntry.createdAt = new Date().toISOString() (line 130) is already wall-clock non-deterministic per run under all approaches. A must EXTEND the chain to cover output, not "preserve" it.
- F4: B's "DiffSummary' computed afterward by diffing" gives B the honest-diff property too; honest-diff is a prerequisite of "real HTML exists," not a B/C differentiator.
- F5: A is under-stressed. Synthesis today is LLM-free substring inference; for A to emit a complete typed patch from free-text intent, synthesis must either gain an LLM (reintroducing non-determinism a stage earlier) or restrict comments to a typed vocabulary (a product change). Add A's pivotal question symmetric to C's validator question.

## Criteria — right axes, gaps
- F6: missing DC6 — failure containment (fail-closed vs fail-open); dominant risk for B (hallucinated layout silently becomes head), absent from DC1-DC5.
- F7: DC5 conflates "real HTML exists" (prereq) with "diff fidelity" (od-id vs file-level, which does differ).
- F8: DC3 "native fit" risks circular LLM-usage bias; re-scope to topology fit (generation behind CLI seam, core pure).

## Missing concerns (all grep-negative in module)
- Partial-apply/rollback: apply persists via 3 non-transactional store writes (saveBatch, appendRevision, saveSession, lines 140-142); adding HTML write makes 4 non-atomic steps; VARIANT_GENERATION_COUNT_MISMATCH post-check detects one torn case but throws AFTER writes already happened — detects, does not roll back. Atomicity/ordering contract needed.
- Multi-task batches: tasks: MutationTask[] but no treatment of conflict (two tasks same od-id), ordering determinism, or per-task-vs-whole-batch failure. Approach-split: A=ordered ops, B=whole-file (no per-task granularity), C=validator could be per-task.
- Idempotency/retry: A pure-function-idempotent; B/C non-idempotent by construction — a retry after the human approved produces different HTML than the human saw.
- How DiffSummary becomes honest: honesty bar defined but diff UNIT (lines/nodes/od-id'd elements) and derivation path unnamed; A=ops-derived, B/C=output-diff-derived.
- How the human "saw the diff": only the data is addressed, not the moment. Lifecycle is MutationApproved -> RevisionApplied -> RevisionRecorded, and in B/C the human approves BEFORE any HTML exists — so the diff is only viewable post-apply, already head. May require a new generate-then-preview gate (RevisionApplied enum, currently unreached, could finally have a use). Most consequential DC5 omission.
- F9: ExecutionProvenance shape deferred but it IS how DC1 is satisfied for B/C; state minimum fields per approach (A: ops; B: model+prompt; C: +validator verdicts).

## Pivotal questions, now symmetric
(a) Is C's validator buildable/trustworthy? (b) Is A's patch synthesizer buildable without an LLM, else A becomes B? (c) Do B/C need a generate-then-preview gate to honor saw-the-diff honestly?

Full fix table (F1-F9 + three contract additions) and handoff in the artifact. No decision made.