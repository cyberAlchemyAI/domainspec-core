---
tags: [inventory, self-harness, golden-chain, dpi, regression-gate, research, evidence-card, open-question]
node_type: evidence-card
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-22
dispatch_id: 2026-06-22-self-harness-golden-chain-mining
dispatch_type: research
working_folder: domainspec-lean-formalization/research/cyberalchemy-functor-stack-bet/bridges/self-harness-mining/
sources: [domainspec-lean-formalization/research/cyberalchemy-functor-stack-bet/bridges/self-harness-mining/findings.md, domainspec-lean-formalization/research/cyberalchemy-functor-stack-bet/findings.md, domainspec-lean-formalization/research/cyberalchemy-functor-stack-bet/experiment-package/GAME-LOOP.md, domainspec-lean-formalization/research/cyberalchemy-functor-stack-bet/experiment-package/SCORING-MODEL.md]
---

# Evidence Cards — Self-Harness as a golden-chain miner

Candidate Inventory read models from dispatch `2026-06-22-self-harness-golden-chain-mining`
(research, resolved). Builds on [[2026-06-22-self-harness-ecosystem-relations-cards]] and the
existing cyberAlchemy functor-stack-bet tower. Non-authority; promotion requires the named owner.
External precedents web-verified; in-repo loci read. claim ≤ proof.

## `self-harness-golden-chain-miner-fork`

- ID: `self-harness-golden-chain-miner-fork`
- Status: candidate
- Claim or candidate: applying the Self-Harness loop as a golden-chain miner splits on ONE fork.
  Fork A — wired to the `stack_s_only` arm (Self-Harness as-written, optimizing pass-rates of
  previous-stage outputs, no source re-access): TRIPS BOTH the standing DPI KILL (it is the strong/
  killed arm — relocates residue, can amplify) and the claim-guard (a Δho pass is exactly the row
  class the guard rejects; a pass ≠ a golden chain). Fork B — wired to `stack_s_plus_source`,
  source-grounding injected, harness-targeted not kernel-targeted, held-out-gated, with a SOUND
  verifier (not a bare pass-rate): survives both, because it improves the measurement/repair
  apparatus, not the fixed Markov kernel. The unguarded default is Fork A; only Fork B is admissible.
- Source refs:
  `.../bridges/self-harness-mining/findings.md` §2 (fork adjudication),
  `.../cyberalchemy-functor-stack-bet/findings.md:151-170,189` (DPI KILL + source-grounding escape),
  `.../experiment-package/GAME-LOOP.md:23,92`, `.../experiment-package/SCORING-MODEL.md:93`
- Authority level: synthesis over a tensioned constructor/skeptic pair, bound to one shared object
- Promotion owner: domainspec-lean-formalization authors (functor-stack-bet owner)
- Trace: `2026-06-22-self-harness-golden-chain-mining`
- Residue: Fork B presupposes a sound verifier for software golden chains — see `sound-verifier-open-question`.

## `golden-chain-mining-precedented-alphaproof-stp`

- ID: `golden-chain-mining-precedented-alphaproof-stp`
- Status: candidate
- Claim or candidate: automated scored-chain mining via self-improving expert-iteration is already
  externally owned — AlphaProof (Nature s41586-025-09833-y) and STP (arXiv 2502.00212) mine verified
  derivation chains and gate on a SOUND formal verifier (the Lean kernel), not a pass-rate delta; STP
  fights overfitting structurally (≤16 proofs/statement subsampling + curriculum). So the generic miner
  is non-novel (build-from-owned, owned-externally-but-portable), and Self-Harness's statistical gate is
  a WEAKER variant of owned art. The portable lesson: gate on a sound verifier, not a bare pass-rate.
- Source refs:
  `.../bridges/self-harness-mining/findings.md` §4 (PRECEDENTED),
  `https://www.nature.com/articles/s41586-025-09833-y`, `https://www.arxiv.org/pdf/2502.00212`
- Authority level: web-verified by the guard/precedent skeptic (Taleb)
- Promotion owner: domainspec-lean-formalization authors
- Trace: `2026-06-22-self-harness-golden-chain-mining`
- Residue: what stays DomainSpec-original is multi-stage residue-composition with source-grounding injection —
  Self-Harness contributes nothing there (no per-stage residue measure, no grounding term).

## `narrow-arm-source-grounding-is-the-dpi-escape`

- ID: `narrow-arm-source-grounding-is-the-dpi-escape`
- Status: candidate
- Claim or candidate: residue reduction is admissible ONLY on the `stack_s_plus_source` arm, where a
  stage re-injects source grounding (I(L_k; source | L_{k-1}) > 0) — the DPI escape the functor-stack
  tower already named. A Self-Harness miner on that arm rediscovers the escape by itself: mining a
  policy-loss residue card yields a repair "carry the source predicate into the downstream stage,"
  which IS source-grounding injection. On the `stack_s_only` arm the same loop only churns pass-rates
  while residue stays silently relocated.
- Source refs:
  `.../bridges/self-harness-mining/findings.md` §5 (mechanism X + guardrails),
  `.../cyberalchemy-functor-stack-bet/distill.md` (compositional spine), `.../levels/L2-closure-plan.md`
- Authority level: source-backed to the tower distill + the constructor lane (Fong)
- Promotion owner: domainspec-lean-formalization authors
- Trace: `2026-06-22-self-harness-golden-chain-mining`
- Residue: "Fork B reduces residue" remains a PREDICTION until the decisive experiment runs.

## `golden-chain-miner-mines-candidates-not-gold`

- ID: `golden-chain-miner-mines-candidates-not-gold`
- Status: candidate
- Claim or candidate: a load-bearing convergence of BOTH lane agents — a Self-Harness miner can at most
  populate `candidate`/`synthetic` rows; it cannot move the collapse meter or mint promoted GOLDEN chains.
  Promotion stays behind real held-out/live rows clearing a pre-registered window for a named environment
  class (claim-guard); the miner's speed does not bypass that rate-limiter, nor the need for a sound verifier.
- Source refs:
  `.../bridges/self-harness-mining/findings.md` §2–§3,
  `.../experiment-package/GAME-LOOP.md:98-107`, `.../experiment-package/SCORING-MODEL.md:86-94`
- Authority level: synthesis; agreed by both constructor and skeptic
- Promotion owner: domainspec-lean-formalization authors (functor-stack-bet owner)
- Trace: `2026-06-22-self-harness-golden-chain-mining`
- Residue: the whole regime is only as honest as the residue judge + verifier; a weak verifier turns a fast miner into a fast cheat.

## `sound-verifier-open-question`

- ID: `sound-verifier-open-question`
- Status: open-question
- Claim or candidate: chief open residue — does a SOUND verifier exist for software golden chains the way
  the Lean kernel is sound for proofs? If yes, Fork B is genuinely strong and worth building; if no, the
  miner degrades toward the precedented-and-weaker generic miner and "Fork B reduces residue" stays a prediction.
- Source refs:
  `.../bridges/self-harness-mining/findings.md` §6 (residue)
- Authority level: open question (inference from the AlphaProof verifier-gate precedent)
- Promotion owner: domainspec-lean-formalization authors
- Trace: `2026-06-22-self-harness-golden-chain-mining`
- Residue: ties to the un-run decisive experiment in the functor-stack-bet L2 closure plan.
