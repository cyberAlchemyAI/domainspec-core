Artifact written to: /home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/02-define.md

# Define: Mutation Execution Mechanics

Takes the grounded s1 baseline and produces a precise problem definition plus three crisp, comparable approach definitions (A/B/C). Fixes vocabulary so the decision stage compares like-for-like. Does NOT decide.

## 1. The Problem, Defined Precisely
- **Statement:** Given an approved, non-stale MutationBatch and the current prototype HTML at the head revision's htmlArtifactRef, produce the next revision's HTML that realizes every applied task's intent AND record an honest account of what changed, appended as exactly one manifest entry, without violating any governance invariant.
- **As a function:** `apply(approvedBatch, currentHtml, sessionContext) -> { nextHtml, diffSummary', provenance }`.
- **Why a real gap:** apply today is pure bookkeeping (s1 §1) — no HTML is read/transformed/written; MutationTask fields only feed counts + appliedTaskIds.
- **Scope:** in = mechanics of task→HTML edit, honest change-record shape, per-approach engine contract, schema/seam consequences. Out = gate logic, synthesis, runtime choice (all settled/honored).

## 2. Vocabulary (fixed for all approaches)
- **"apply" must produce:** (1) next-revision HTML at the existing htmlArtifactRef path shape — absent today; (2) honest DiffSummary derived from real before/after; (3) exactly one RevisionManifestEntry which must gain a verifiable HTML pointer+hash.
- **honest DiffSummary':** {added,changed,removed} derived from a real currentHtml→nextHtml diff (today's counts are inferred from changeType strings before any HTML exists — dishonest by construction). Honesty bar: a claim is valid only if derivable from currentHtml and nextHtml.
- **deterministic validator:** pure core function (no LLM/network/clock) judging (currentHtml, candidateHtml, task|batch)->pass|fail with stable verdicts. Check menu: target-changed, anchor-preserved, scope-bounded, acceptance-satisfied, well-formed/escaped, intent-not-reinterpreted. Necessary for C, impossible-to-fully-satisfy for B, redundant for A.
- **engine contract:** per-approach interface+guarantees (receives/emits/may-assume/forbidden); always behind the studio CLI seam.
- **Other:** anchor (selector vs data-od-id), change params (typed machine ops absent today), ExecutionProvenance (how nextHtml was produced — new), realize-vs-reinterpret (intent is sacred).

## 3. Governance Invariants (G1–G9)
G1 auto-apply forbidden, G2 approval-before-apply, G3 baseline gate, G4 staleness guard, G5 append-only exactly-one-entry (G1–G5 code-enforced), G6 determinism/reproducibility, G7 intent sacred, G8 saw-the-diff ergonomics, G9 Claude Code-native runtime / CLI-only seam. Plus GAP-1 (od-id into MutationTask) and GAP-2 (HTML pointer on manifest) as prerequisites paid by every approach.

## 4. Three Approaches as Comparable Contracts
- **A — Deterministic Patch:** edit decided at synthesis; pure transformer applyPatch(currentHtml, tasks)->nextHtml; no LLM; determinism in patch ops; heaviest schema burden (typed param-bearing changeType union + changeParams; synthesis must emit complete patches); validator redundant; does not use Claude Code for generation.
- **B — Agentic Regeneration:** model is the engine; generate(currentHtml, tasks)->nextHtml at apply time; determinism nowhere (audit chain broken at execution); lightest schema; no structural validator; maximal native fit; G7 unenforced.
- **C — Hybrid Propose+Validate:** propose(currentHtml,tasks)->candidateHtml (Claude Code, post-seam) then validate(...)->pass|fail (pure core); determinism carried by the validator suite (reproducible admission, not generation); medium schema (machine-checkable acceptance); validator central+load-bearing; matches existing core-owns-gates / CLI-is-seam topology.
- At-a-glance comparison table included on: LLM-in-path, where determinism lives, schema burden, audit chain, expressiveness, intent realization, validator need, GAP-1/2.

## 5. Decision Criteria (named)
- **DC1** Auditability/determinism · **DC2** Change expressiveness · **DC3** Claude Code-native fit · **DC4** data-od-id stability · **DC5** Saw-the-diff ergonomics.
- **Central tension:** DC1/DC4 pull toward A; DC2/DC3/DC5 pull toward B; C is the explicit Pareto-frontier attempt (native generation + restored deterministic admission via validator) at the cost of building/trusting that suite. Pivotal decision question: is C's validator buildable and trustworthy enough to be worth its cost?

## 6. Residue / handoff
GAP-1 + GAP-2 are non-differentiating prerequisites; C's validator (esp. intent-not-reinterpreted, scope-bounded) is the pivotal unknown to stress-test; ExecutionProvenance shape to confirm per approach; governance IDs still grep-negative; no decision made here.