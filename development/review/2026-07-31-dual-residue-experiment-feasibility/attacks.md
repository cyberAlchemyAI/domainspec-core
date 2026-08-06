# Governed attack record

Dispatch: `2026-07-31-dual-residue-experiment-feasibility-review`  
Run: `run-20260731-dual-residue-feasibility-02`  
Target: `/home/vrondelli/projects/dual-residue-experiment` (read-only)  
Evidence packet: `orchestrate/run-20260731-dual-residue-feasibility-02/attacker-returns.md`

This record preserves the three attack actions and their Robot Talks reconciliations as distinct positions. Agreement is reported, but disagreement is not flattened into a fictitious single attack.

## spawn-0001 — formal and claim-contract attack

### Initial position

The formal attacker found a CRITICAL comparator mismatch: the public hypothesis says two signals beat one aggregated score (`README.md:37-41`), while E1 compares D with the per-axis minimum of A/B/C (`experiments/E1-dual-residue-loss/PROPOSAL.md:40-51`). It also found a CRITICAL promotion contradiction: E1 disclaims adjudicating `grad_indep` (`experiments/E1-dual-residue-loss/PROPOSAL.md:155-160`) yet says PASS raises its veracidade (`experiments/E1-dual-residue-loss/PROPOSAL.md:281-284`). MAJOR attacks covered categorical overreach, the target premise's undocumented bridge from gradient independence to independent error movement and strict specialist dominance (`domain_knowledge/premise/residue-independence-premises.md:26-32`), inconsistent verdict algebra, missing machine-bound effect direction, and top-level proposal drift. The truth table hides significance and mixed-direction cases (MINOR). This review did not independently inspect the theorem source and therefore does not decide what follows from that source.

Four defended zero-findings survived: E1 states its shallow-schema ceiling (`experiments/E1-dual-residue-loss/PROPOSAL.md:288-290`); research separates gradient cosine, rate covariance, and benchmark deltas (`research/grad-indep-reality/research/findings.md:32-44`); the rich-schema addendum is explicitly proposed (`research/grad-indep-reality/PROPOSAL-addendum-rich-schema.md:59-84`); and configs expose four intended objective arms (`configs/condition_A.yaml:1-20`, `configs/condition_B.yaml:1-20`, `configs/condition_C.yaml:1-20`, `configs/condition_D.yaml:1-23`).

### Robot Talks reconciliation

The mechanics return strengthened, rather than refuted, comparator and gate attacks: A declares DPO but the training entry point delegates to an SFT-only loop; D's null weights become zero; reporter point estimates can emit `VALIDATED`; split provenance is bypassed; invalid outputs alter the instruction denominator; and D's dev selector rewards one axis. The probe's gradient imbalance is a treatment-design warning, not `grad_indep` evidence. The ownership return agreed that absent freeze bindings and upstream objects prevent promotion. Stable scope: repaired D-vs-A and repaired D-vs-B/C are different local questions; neither proves categorical irreducibility, general scalar blindness, gradient independence, rich-schema behavior, or promotion.

## spawn-0002 — executable mechanics and measurement attack

### Initial position

The mechanics attacker found three CRITICAL failures. Condition A promises SFT+DPO (`configs/condition_A.yaml:1-18`) but `scripts/train.py:17-32` calls a path that imports SFT components, reads no DPO config, and constructs/runs only SFT plus the auxiliary wrapper (`src/dual_residue/training/loop.py:213-229`, `src/dual_residue/training/loop.py:284-325`). Condition D's weights are null (`configs/condition_D.yaml:14-23`) and are coerced to zero (`src/dual_residue/training/loop.py:225-229`), with no executed grid-search path. Evaluation emits aggregates only (`scripts/eval.py:94-120`), while reporting declares `VALIDATED` from point-estimate booleans and expressly leaves the p-value uncomputed (`scripts/report.py:81-108`).

MAJOR attacks: training regenerates data rather than consuming the hashed corpus (`src/dual_residue/training/loop.py:257-266`; `data/splits/manifest.json:1-14`); evaluator counts invalid JSON as instruction failure (`scripts/eval.py:100-115`) despite the core metric exposing valid-only semantics (`src/evals/metrics.py:73-92`); D selects `min(eta_sch_rate, eta_ins_rate)` (`configs/condition_D.yaml:20-23`); token/prefix alignment lacks an asserted test contract; and the committed probe has zero instruction gradients on two batches and roughly 400–700x norm imbalance on the others (`results/grad_cosine_postSFT.json:7-43`). README's “nothing run,” 58-test, no-results/no-splits inventory is stale (`README.md:18`, `README.md:97-98`) (MINOR wording, MAJOR evidence-state effect).

Command receipts: the proposal's frontmatter-oriented validator passed; pytest and the smoke path were blocked by absent dependencies; Torch, Transformers, Datasets, TRL, PEFT, NumPy, Pydantic, and Pytest were absent; an ephemeral report invocation exited zero and printed `VALIDATED` without bootstrap fields; declared split JSONL files were absent. No training, installation, download, network access, or target write occurred.

### Robot Talks reconciliation

No mechanics finding was refuted. Formal review raised the missing statistical binding and comparator mismatch to claim-validity failures, while ownership review required a single frozen contract before parity could be judged. The reconciled position is cumulative: `CONCEPTUALLY-MIS-SPECIFIED` and `NOT-YET-MECHANICALLY-FEASIBLE`. Retry requirements are faithful A and D arms, verified splits, per-example paired statistics and direction, fail-closed reporting, aligned losses, runnable tests, separated comparators, and local-only promotion semantics.

## spawn-0003 — ownership, lifecycle, and repository-fit attack

### Initial position

The ownership attacker found MAJOR evidence-state drift (`README.md:18` conflicts with the manifest and probe results), no frozen source of truth (`PROPOSAL.md:1-15`; `experiments/E1-dual-residue-loss/PROPOSAL.md:24-29`), unresolved checkout-relative upstream references (`README.md:103-110`), 8B/0.5B contract drift (`domain_knowledge/constitution/pre-registration-constitution.md:49-62`; `configs/condition_D.yaml:4-7`), and claim-identity drift (README says A/B/C/D test `grad_indep`, while E1 disclaims that). The review did not verify those checkout-relative references as authority objects. MINOR findings cover high-veracity wording on a pending verdict (`experiments/E1-dual-residue-loss/VERDICT.md:8-16`) and a procedurally complete research ledger whose substantive residue remains open. The checkout was clean on `main` at `a07d8bcf10f6292d708e063b2ea992ee744cf807` during that attack.

Its distinct contextual conclusion was positive: an adjacent, standalone experiment harness is a sensible candidate evidence producer for DomainSpec, but it is not a canonical authority source.

### Robot Talks reconciliation

The claim-identity inconsistency is promotion-blocking. There is presently no stable executable contract against which code, data, and verdict can be compared. The reconciled feasibility status is `NOT-YET-FEASIBLE`: the purpose and ownership boundary are repairable, but current bytes cannot issue the contracted verdict. This is distinct from `MISFIT`, which would mean the repository's purpose or ownership boundary is itself inappropriate. The review's architectural assessment remains that placement is sensible. Reconsider only after claim, comparator, verdict, code/report parity, corpus/arm demonstrations, and a fresh freeze. A repaired run can establish a local result for pinned bytes and inputs; it cannot promote an axiom, alter a theorem, establish broad `grad_indep`, or bind DomainSpec without separate canonical-owner acceptance.

## Cross-attack convergence without collapse

- Formal: the experiment currently asks and adjudicates different questions.
- Mechanics: the runnable path does not implement or measure the declared arms and gates.
- Ownership: the repository is a good evidence-harness location, but its lifecycle and upstream bindings do not support authority claims.
- Shared non-finding: none of the attacks argued that two-budget motivation is incoherent, that deterministic shape/content metrics are useless, that the proposed rich-schema successor is already proven, or that the four-arm configuration surface should be deleted.
