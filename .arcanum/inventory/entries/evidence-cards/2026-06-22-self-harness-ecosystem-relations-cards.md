---
tags: [inventory, self-harness, harness-self-improvement, regression-gate, research, evidence-card]
node_type: evidence-card
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-22
dispatch_id: 2026-06-22-self-harness-tower-lanes
dispatch_type: research
working_folder: domainspec-lean-formalization/research/self-harness-tower/
sources: [domainspec-lean-formalization/research/self-harness-tower/findings.md, domainspec-lean-formalization/research/self-harness-tower/tower/TOWER.md]
---

# Evidence Cards — Self-Harness × ecosystem relation lanes

Candidate Inventory read models from dispatch `2026-06-22-self-harness-tower-lanes`
(research, resolved). Non-authority; promotion requires the named downstream owner.
Paper claims source-backed to the local tower (arXiv 2606.09498); external precedents
were web-verified by the lane skeptics; in-repo loci read. claim ≤ proof.

## `self-harness-paradigm`

- ID: `self-harness-paradigm`
- Status: candidate
- Claim or candidate: Self-Harness (arXiv 2606.09498, Shanghai AI Lab) is a method where a
  FROZEN-WEIGHT model improves its own NON-PARAMETRIC harness over T rounds via a three-stage
  loop: (1) Weakness Mining — cluster FAILED traces by a verifier-grounded signature
  φ=(terminal cause, causal status, abstract mechanism) into a diagnostic evidence bundle;
  (2) Harness Proposal — a bounded proposer emits K distinct minimal edits, each tied to one
  failure mechanism + one editable surface, with an audit record; (3) Proposal Validation —
  accept iff Δin≥0 ∧ Δho≥0 ∧ max>0, the held-out split NEVER shown to the proposer, passers
  merged. Held-out Terminal-Bench-2.0 deltas: M2.5 40.5→61.9, Qwen3.5 23.8→38.1, GLM-5 42.9→57.1.
- Source refs:
  `domainspec-lean-formalization/research/self-harness-tower/tower/TOWER.md` (§A–G),
  `domainspec-lean-formalization/research/self-harness-tower/findings.md` §1
- Authority level: source-backed to the local tower; deltas cited-as-claimed (paper not reproduced)
- Promotion owner: domainspec-lean-formalization authors
- Trace: `2026-06-22-self-harness-tower-lanes`
- Residue: K, T, and held-in/held-out split sizes are NOT stated in the readable paper (tower R6) —
  confirm before any reproduction.

## `self-harness-held-out-gate-is-the-portable-mechanism`

- ID: `self-harness-held-out-gate-is-the-portable-mechanism`
- Status: candidate
- Claim or candidate: across the five ecosystem targets, the ONE genuinely portable mechanism is
  the proposer-blind held-out non-regression acceptance gate. Every target already owns the
  upstream mining/proposal stages or has a governance reason to refuse the paper's autonomous
  auto-merge; so the gate is admissible only as advisory evidence feeding a human / owner-route /
  kernel-sound promotion — never as the promotion itself.
- Source refs:
  `domainspec-lean-formalization/research/self-harness-tower/findings.md` §4 (cross-cutting)
- Authority level: synthesis over the 10 lane returns
- Promotion owner: parent (dispatch strategist) / each target's owner
- Trace: `2026-06-22-self-harness-tower-lanes`
- Residue: whether any target wants the gate wired automatically vs kept advisory is undecided.

## `self-harness-relation-verdicts-five-targets`

- ID: `self-harness-relation-verdicts-five-targets`
- Status: candidate
- Claim or candidate: adjudicated relation verdicts — Saturn EXTENDS+PRECEDENTED (gains the
  held-out gate to close its still-open loop; SICA/ADAS external precedent → build-from-owned);
  DomainSpec PRECEDENTED+THREATENS (owns the isomorphic TUNING-LOOP in-repo; a regression pass ≠
  a spec proof, Axioms A1/A3); Arcanum PRECEDENTED (owns the loop twice — external + workflow-reflect/
  sigil-development; the paper's auto-merge is a DOWNGRADE vs human-gated promotion); CyberAlchemy-v2
  PRECEDENTED+THREATENS (owns D30/D17/D23; breaks "regression-pass ≠ authority promotion"); Lean
  formalization EXTENDS+INAPPLICABLE (acceptance rule maps exactly onto persistence_lemma +
  promotion_not_isEquivalence, proof-stronger than the paper, but as a soundness gate the kernel
  admits only proved terms).
- Source refs:
  `domainspec-lean-formalization/research/self-harness-tower/findings.md` §2 (relation matrix), §3
- Authority level: synthesis over tensioned explorer/skeptic lane pairs (10 agents)
- Promotion owner: each target's owner (Saturn/DomainSpec/Arcanum/CAv2/Lean)
- Trace: `2026-06-22-self-harness-tower-lanes`
- Residue: verdicts are relation judgments, not adoption decisions; no target has accepted a change.

## `regression-pass-is-not-authority-promotion`

- ID: `regression-pass-is-not-authority-promotion`
- Status: candidate
- Claim or candidate: a recurring cross-target invariant — a statistical pass-rate / non-regression
  gate is NOT a spec proof, NOT authority promotion, and NOT kernel soundness. DomainSpec Axioms
  A1/A3, CAv2 lifecycle D23 ("regression-pass ≠ authority promotion"), and the Lean kernel each
  strictly DOMINATE a pass-rate gate. The paper concedes this in its own limitation
  ("non-regression alone too weak for high-stakes").
- Source refs:
  `domainspec-lean-formalization/research/self-harness-tower/findings.md` §2–§4,
  `implementation/domainspec/AXIOMS.md`, `cyberAlchemy-v2/ontology/LIFECYCLE-MODEL.md`
- Authority level: source-backed (target authority docs) + paper's stated limitation
- Promotion owner: DomainSpec authors + cyberAlchemy-v2 authority owner
- Trace: `2026-06-22-self-harness-tower-lanes`
- Residue: this invariant is the load-bearing reason every "THREATENS" tag was assigned.

## `self-harness-loop-is-externally-precedented`

- ID: `self-harness-loop-is-externally-precedented`
- Status: candidate
- Claim or candidate: the mine→propose→regression-gated-validate loop is externally owned —
  SICA (arXiv 2504.15228), ADAS/Meta-Agent-Search (2024), Darwin Gödel Machine (arXiv 2505.22954),
  Gödel Agent, DSPy/Promptbreeder/STOP, GEPA, TextGrad — the paper's residual novelty is a tighter,
  falsifiable PACKAGING (named three stages + verifier-signature mining + explicit held-out split on
  Terminal-Bench-2.0), not the idea. Build-from-owned, never a kill.
- Source refs:
  `domainspec-lean-formalization/research/self-harness-tower/findings.md` §2–§3,
  `https://arxiv.org/abs/2504.15228`, `https://arxiv.org/abs/2505.22954`
- Authority level: web-verified by lane skeptics (Popper, Quine, Lakatos, Feyerabend, Gödel)
- Promotion owner: domainspec-lean-formalization authors
- Trace: `2026-06-22-self-harness-tower-lanes`
- Residue: the verifier-grounded failure-signature clustering is the one sub-mechanism not found pre-owned.
