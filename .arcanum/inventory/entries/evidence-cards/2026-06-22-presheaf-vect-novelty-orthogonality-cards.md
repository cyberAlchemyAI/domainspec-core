---
tags: [inventory, formalization, category-theory, yoneda, residue, latent-space, cyberalchemy-v2, evidence-card, open-question]
node_type: evidence-card
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-22
dispatch_id: 2026-06-22-presheaf-vect-novelty-lean-repo
dispatch_type: research
working_folder: domainspec-lean-formalization/research/presheaf-vect-novelty/
sources: [domainspec-lean-formalization/research/presheaf-vect-novelty/findings.md, domainspec-lean-formalization/lean-formalization/AsymmetricTowerVEnriched.lean, domainspec-lean-formalization/lean-formalization/TannakianDiagnosis.lean, cyberAlchemy-v2/TO-VLAD/TO-VLAD.md, cyberAlchemy-v2/TO-VLAD/RESOLUTION.md, house_project/docs/business-philosopher/assuntos/theorem/theorem-presentations/v5-bridge-refuted.md]
---

# Evidence Cards — presheaf-in-Vect novelty + orthogonality resolution

Candidate Inventory read models from dispatch `2026-06-22-presheaf-vect-novelty-lean-repo`
(research, resolved). Non-authority; promotion requires the named downstream owner.
Math claims source-backed and reviewer-line-verified; interpretive bridges marked.

## `presheaf-in-vect-not-novel-build-from-owned`

- ID: `presheaf-in-vect-not-novel-build-from-owned`
- Status: candidate
- Claim or candidate: presheaf-in-Vect (Set codomain replaced by Vect / a metric base)
  is NOT a present novelty: the machinery is build-from-owned (Kelly 1982, Basic Concepts
  of Enriched Category Theory §4-5 + Day convolution + enriched Yoneda), and the
  Vect-codomain residue statement is precedent-clean but UN-FORMALIZED (open sequel).
  Popper non-vacuity returned no-witness: every candidate reduces to Kelly, to Set-level
  M2/M6, or to the open sequel. The owned novelty is the Set-level discipline
  (M2Counter:54, M6Counter:125, S2VsS3Counter:158, F11:317 + two-layer audit).
- Source refs:
  `domainspec-lean-formalization/research/presheaf-vect-novelty/findings.md`,
  `domainspec-lean-formalization/lean-formalization/M2Counter.lean:54`,
  `domainspec-lean-formalization/lean-formalization/M6Counter.lean:125`
- Authority level: source-backed (math) + reviewer-verified; "not novel" is a typed negative
- Promotion owner: domainspec-lean-formalization authors (any Vect formalization)
- Trace: `2026-06-22-presheaf-vect-novelty-lean-repo`
- Residue: Blocked witness — a Vect-codomain residue theorem; first obligation = re-target
  `xTower` from `⥤ Type` to `⥤ ModuleCat` and exhibit a residue non-trivial at V=Vect yet
  trivial in Set; likely EMPTY because M2/M6 non-representability is base-independent. Flip
  to already-deployed iff a no-sorry Lean `[C^op, Vect]` adjoint-triple + residue theorem is written.

## `asymmetric-tower-venriched-is-schema-side-set-valued`

- ID: `asymmetric-tower-venriched-is-schema-side-set-valued`
- Status: candidate
- Claim or candidate: `AsymmetricTowerVEnriched.lean` (the long-open trust-but-verify flag
  from the D1/bet tower) is sorry-free but a SCHEMA-SIDE bicyclic NEGATIVE result
  (`v_no_global_transport_lan_enriched`); its presheaf tower is STILL Set-valued
  (`xTower : ∀ n, T n ⥤ Type`). It does NOT own Vect-codomain presheaves. Resolved: the
  repo owns a V-enriched negative tower, not a positive Vect-codomain presheaf/residue theorem.
- Source refs:
  `domainspec-lean-formalization/lean-formalization/AsymmetricTowerVEnriched.lean:132`,
  `domainspec-lean-formalization/lean-formalization/AsymmetricTowerVEnriched.lean:351`,
  `domainspec-lean-formalization/lean-formalization/AsymmetricTowerVEnriched.lean:462`,
  `domainspec-lean-formalization/lean-formalization/TannakianDiagnosis.lean:58-65`
- Authority level: source-backed, reviewer-line-verified (Lakatos precedent gate)
- Promotion owner: domainspec-lean-formalization authors
- Trace: `2026-06-22-presheaf-vect-novelty-lean-repo`
- Residue: TannakianDiagnosis:58-65 — enrichment cannot live at the (Discrete) schema level;
  it would be a presheaf-VALUE-level orthogonal axis, not a refinement of M5/M6.

## `orthogonality-two-distinct-notions`

- ID: `orthogonality-two-distinct-notions`
- Status: candidate
- Claim or candidate: the two senses of "orthogonality" in this program are TWO DISTINCT
  NOTIONS, not one. CAV2 `I(Lᵢ;Lⱼ)=0` is Shannon statistical independence (commutative,
  non-contextual by construction); the Lean machinery's `⟪vᵢ,vⱼ⟫=0` is Hilbert
  inner-product zero (non-commutative, generates contextuality). They "point in opposite
  directions": a spectral-presheaf checker on any `I=0` schema returns "no obstruction" by
  construction (the presheaf admits a global constant-false section). They share only the
  word and the zero-form and could sit under a common nLab factorization-system/lifting
  roof, but do NOT unify as a single construction. (Refutes the "unified-via-lifting" reframe.)
- Source refs:
  `cyberAlchemy-v2/TO-VLAD/TO-VLAD.md:19-36`,
  `cyberAlchemy-v2/TO-VLAD/TO-VLAD.md` (ontology-axioms.md:84 Shannon; KCBSProjectorsReal.lean:140 Hilbert; KCBSSpectralPresheaf.lean:302,283 global section),
  `https://ncatlab.org/nlab/show/orthogonality`
- Authority level: source-backed via the TO-VLAD owner audit (Victor); nLab external standard
- Promotion owner: cyberAlchemy-v2 authority owner (CAV2-D22 already amended) + domainspec authors
- Trace: `2026-06-22-presheaf-vect-novelty-lean-repo`
- Residue: a common abstract roof (factorization-system orthogonality) is nameable but unwritten;
  not load-bearing for any current claim.

## `to-vlad-handoffs-move-the-target`

- ID: `to-vlad-handoffs-move-the-target`
- Status: candidate
- Claim or candidate: cyberAlchemy-v2/TO-VLAD/ handoffs already reframed the orthogonality /
  residue work: CAV2-D22 amended to "admission/compression discipline, NOT contextuality
  machinery"; CAV2-D28 (value-cycle edge guard) + CAV2-C13 (constitutional guard) promoted —
  CAV2-C13 overlaps the prior dispatch's "Representability-Grounded Promotion Gate" candidate;
  residue-typing redirected from label-layer to EDGE-layer; per-rule `residue_profile`
  auto-populating the D18/D26 ledger routes as CAV2-D25 Schema Amendment Witness.
- Source refs:
  `cyberAlchemy-v2/TO-VLAD/RESOLUTION.md:26-29`,
  `cyberAlchemy-v2/TO-VLAD/SESSION-HANDOFF-cav2-primordial-basis.md:43,71`,
  `cyberAlchemy-v2/TO-VLAD/TO-VLAD-residue-typing-in-generation.md`
- Authority level: source-backed (the handoffs themselves)
- Promotion owner: cyberAlchemy-v2 authority owner (definitions-governance / constitution-governance)
- Trace: `2026-06-22-presheaf-vect-novelty-lean-repo`
- Residue: cross-check whether the existing CAV2-C13 already satisfies the prior dispatch's
  Representability-Grounded Promotion Gate candidate, or whether they are distinct gates.
