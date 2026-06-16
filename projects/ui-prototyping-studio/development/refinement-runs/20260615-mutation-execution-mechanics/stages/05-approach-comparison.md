# Approach Comparison: Mutation Execution Mechanics

Artifact written to: /home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/05-approach-comparison.md

## Scoring discipline (s3 calibrations applied so the comparison is not rigged)
- F3: A inherits NO clean audit chain (existing sha256 binds inputs only; createdAt is wall-clock). Auditability scored on end-state output-reproducibility each approach can REACH, not on a chain A "keeps."
- F4/F7: honest DiffSummary is a shared prerequisite (any approach that produces real HTML gets it). Ergonomics scored on diff FIDELITY + saw-the-diff SEQUENCING, not mere existence of a diff.
- F8: cc_fit = TOPOLOGY fit (generation behind CLI seam, core pure), NOT LLM-usage. Stops cc_fit mechanically ranking B>C>A.

## Comparison table (1–5, equal weight)

| Criterion | A — Det. patch | B — Agentic regen | C — Hybrid |
|---|---|---|---|
| auditability | 5 | 2.5 | 4 |
| expressiveness | 2 | 5 | 4 |
| cc_fit | 2.5 | 5 | 5 |
| odid_stability | 5 | 3 | 4 |
| ergonomics | 3 | 4 | 5 |
| **Total (Σ/25)** | **17.5** | **19.5** | **22.0** |

Divergences from advocate self-scores (stated for fairness):
- A cc_fit raised 2→2.5: under F8 topology reading A passes the seam test; the advocate's 2 was the retired circular (LLM-usage) reading. Raise deliberately HELPS A so the verdict can't be accused of suppressing it.
- B ergonomics trimmed 4.5→4: prices the unmitigated approve-then-generate sequencing problem + non-idempotent retry drift (human approves a diff that a retry can change) and the missing preview gate.
- All other cells agree with advocate self-scores.

## Dominance analysis (strict Pareto)
NO approach is strictly dominated — all three are on the frontier:
- A is sole best on auditability (5) and odid (5) — cannot be eliminated.
- B is sole best on expressiveness (5) — cannot be eliminated.
- C is never best-in-class on aud/expr/odid but is NEVER worst on any criterion, tied-best on cc_fit, best on ergonomics.
Therefore elimination is NOT by dominance (none exists). It is by the equal-weight Pareto total the define stage fixed PLUS qualitative resolution of the central tension — recorded explicitly so it is not mistaken for a dominance claim.

## Verdict: Select C (Hybrid), conditionally
Justified by scores, not fiat:
1. Highest total (22.0 vs 19.5 vs 17.5) under the mandated equal-weight posture.
2. Only approach with NO low outlier — A has structural floors (expr 2, cc_fit 2.5) it cannot raise without becoming "B with extra steps" (F5 fork); B has an irreducible auditability floor (2.5, lowest cell, fail-open, non-deterministic by construction). C trades peaks for the absence of a floor — the right shape when the tension is "don't force a false trade between auditability and expressiveness."
3. Resolves the central tension structurally: generation stays in the runtime (expr/cc_fit), determinism recovered at the ADMISSION boundary (auditability), honest preview gate hosted on its native propose→validate→record shape (ergonomics).

NOT a rubber stamp — C auditability is 4 not 5; the gap is real (validator buildability unproven, s4 GAP-R1). Selection is CONDITIONAL with demotion rules:
- C-1: if acceptanceText cannot be made machine-checkable, C degrades toward B on auditability → verdict flips to B (B is C's documented floor/fallback).
- C-2: if the real comment workload turns out small/enumerable (typed ops cover it without an LLM), A's 5/5 audit+odid peaks win → verdict flips to A. No current evidence supports this (comments are free-text).

Synthesis: C IS the synthesis of A's determinism + B's expressiveness; a fourth blend is not Pareto-superior. Import two A mechanics into C's design at low cost: per-task static same-odId conflict detection (lifts odid toward 5) and opportunistic ops-vs-output reconciliation where a structured op exists (stronger honesty guard).

## Rejected alternatives (residue)
- Approach A standalone — Σ17.5; two structural floors (expr 2, cc_fit 2.5) unraisable without the F5 patch-synthesizer fork. Resurfaces if C-2 fires.
- Approach B standalone — Σ19.5; irreducible auditability floor 2.5 (fail-open, G7 unenforced, post-approval drift). Resurfaces if C-1 fires (C degrades to B anyway).
- "A's validator is redundant" — true only inside A; that property is what caps A's expressiveness.
- "B's human gate is sufficient admission control" — collapses under rubber-stamping; no deterministic scope fence.
- A fourth A∪B∪C blend — no point-wise gain over C, adds owner-lane/schema cost for no Pareto improvement.

Carried-forward open residue (non-blocking): GAP-1/GAP-2 paid under C regardless (its odid 4 + auditability 4 assume full coverage); C-1 validator-buildability spike is the gating next action with s4 GAP-R1 as the bounded fallback; preview/dry-run gate (dormant RevisionApplied state) must be designed; atomicity/rollback for the extra HTML write unresolved (adopt A's produce-then-persist shape); ExecutionProvenance for C = model+prompt+IO hashes+validator verdicts.