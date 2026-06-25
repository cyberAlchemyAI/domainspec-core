---
tags: [inventory, machine-map, viable-system-model, saturn, cav2, meta-authority, attestation, moat, observer-executor-split, governance-attenuation, commercialization, claim-le-proof, build-from-owned]
node_type: evidence-card
is_session: false
layer: market, governance
nature: reference
status: candidate
created: 2026-06-24
sources: [development/machine-map/findings.md, implementation/domainspec/GOVERNANCE-ATTENUATION.md, ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md, implementation/domainspec/plan/SATURN-L-SYSTEM.md, implementation/domainspec/AUTHORITY-MAP.md, development/COMMERCIALIZATION-SYNTHESIS.md, domainspec-lean-formalization/README.md, domainspec-lean-formalization/OPEN-SORRIES.md, cyberAlchemy-v2/authority/AUTHORITY-MODEL.md]
---

# Evidence Cards — Machine Map + Moat

Candidate Inventory read models from dispatch `2026-06-24-machine-map-and-moat`
(research; closed `resolved`; both skeptics accepted). Promotion owners = the
DomainSpec plan owner / cav2 authority owner / the commercialization decision-gate.
These cards promote nothing.

## `machine-map-vsm-foundry`

- ID: `machine-map-vsm-foundry`
- Status: candidate
- Claim or candidate: the product is a **self-governing foundry that manufactures +
  continuously maintains domain authorities**, mappable onto Beer's Viable System
  Model: **DomainSpec** = the baseline/model (what is meaningful); **Arcanum** =
  System-1 operations (how); pipeline = S2 coordination; gates/audits = S3 control
  (manual-trigger); the **metric->improvement agent** = the first System-4
  Intelligence organ (built, under-performing); **cav2 AUTHORITY-MODEL** = the
  missing System-5 Policy; **Saturn** = the S3<->S4 convergence control loop
  (intended, NOT shipped).
- Source refs: `development/machine-map/findings.md` §1; `implementation/domainspec/GOVERNANCE-ATTENUATION.md`
  §VSM (S1 ops / S2 coord / S3 control-manual / S4 intelligence-underperforming /
  S5 policy-MISSING); `ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md`
  (Saturn = convergence loop; intended-not-shipped).
- Authority level: candidate synthesis (build-from-owned of GOVERNANCE-ATTENUATION's VSM mapping).
- Promotion owner: DomainSpec plan owner.
- Trace: E1 integrator brief; verified by S1 precedent.
- Residue: Saturn-scope OQ (control-loop vs whole-stack, SATURN-LAYER-MAP OQ-2); cav2-as-S5 is a structural analogy, not a repo-cited link.

## `two-system-5s-recursion-boundary`

- ID: `two-system-5s-recursion-boundary`
- Status: candidate
- Claim or candidate: there are **TWO System-5s, one VSM-recursion apart** — cav2's
  meta-authority (governs what may COUNT as authority KINDS; the S5 of the
  authority-MANUFACTURING system) vs DomainSpec's AXIOMS/CONSTITUTION (object-level
  policy, "docs before code"; the S5 of a MANUFACTURED authority). Collapsing them
  hides a recursion boundary; the foundry thesis is only coherent if the inner
  system's PRODUCT is the very policy the outer system governs.
- Source refs: `development/machine-map/findings.md` §1 (E1 weak point, kept);
  `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md` (kinds/closure); `implementation/domainspec/AUTHORITY-MAP.md` (AXIOMS/CONSTITUTION).
- Authority level: candidate (definitionally verified by S2).
- Promotion owner: cav2 authority owner / DomainSpec plan owner.
- Trace: E1 weak point; S2 keystone.
- Residue: the cav2->DomainSpec-S5 link is analogy, not cited.

## `read-only-observer-not-daemon`

- ID: `read-only-observer-not-daemon`
- Status: candidate
- Claim or candidate: the metric->improvement agent (the user's "agent that reads
  perf/bugs/latency/malformed-ontology-node metrics and applies improvements") must
  be a **READ-ONLY OBSERVER that PROPOSES to an S3 gate + owner** — NEVER a
  measure-and-mutate daemon. An agent that observes AND acts **re-fuses regulator
  and system** (Conant-Ashby: the executor cannot be its own high-fidelity model).
  The deterministic slices (latency thresholds, orphan/malformed-node detection,
  bug-hotspot from churn) compute at S3; the behavioral judgments (brittle
  abstraction) need the read-only S4 observer pass. Split observer from executor.
- Source refs: `implementation/domainspec/GOVERNANCE-ATTENUATION.md` §"Split Observer
  from Executor" (Conant-Ashby; read-only shadow agent; hybrid detector);
  `development/machine-map/findings.md` §2-3.
- Authority level: candidate (E2 Conant-Ashby + E3 meter).
- Promotion owner: DomainSpec plan owner / sigil-development.
- Trace: E2 + E3; the correction to the user's framing.
- Residue: the read-only observer is the highest-leverage first build (below).

## `build-vs-attenuate-discriminator`

- ID: `build-vs-attenuate-discriminator`
- Status: candidate
- Claim or candidate: "making the machine" is **right as structural consolidation +
  read-only observation, wrong as new acting organs.** GOVERNANCE-ATTENUATION's own
  theorems (Godel, Ashby requisite-variety, Via Negativa) say adding governance
  organs ATTENUATES fidelity. Discriminator: ADD only fidelity-RAISING read-only
  organs (a read-only observer that splits observer from executor; a COLLAPSED
  read-only policy DOCUMENT that fills the empty-but-necessary System-5 slot) AND
  SUBTRACT the scattered instruction-governance (collapse the ~7 authority surfaces
  into one constitution; make S3 continuous via CI). REFUSE a measure-and-mutate
  daemon or a new prose governance layer.
- Source refs: `implementation/domainspec/GOVERNANCE-ATTENUATION.md` ("the fix is not
  more layers"; Via Negativa; Priority #1/#2/#4; "collapse scattered governance");
  `development/machine-map/findings.md` §2 (E1+E2 resolution).
- Authority level: candidate (E2 weak point = decisive: S5 is genuinely MISSING so filling it is required, but as a doc not a daemon).
- Promotion owner: DomainSpec plan owner / constitution-governance.
- Trace: E2 dividing line (read-only-policy-artifact required vs acting-metric-organ attenuating).
- Residue: which authority surfaces collapse first is a sequencing decision.

## `moat-inversion-attestation-not-provability`

- ID: `moat-inversion-attestation-not-provability`
- Status: candidate
- Claim or candidate: the defensible MOAT is **attestation + the governance-data
  asset + the vertical** (immutable, vendor-neutral, cross-tool audit trail that
  SOC2/ITGC/SOX auditors require and single-vendor incumbents can't ship).
  **Provability (category theory + Lean) is a conjectural credibility AMPLIFIER, NOT
  the moat** — the commercialization doc itself calls Lean "the proof HALF". The
  user's "provable cav2 = the moat" is honestly **inverted**. Collapse-test: if
  auditors accept the attestation trail WITHOUT a Lean proof (they do), provability's
  marginal contribution to the defensible moat -> ~0. Lean status is conjectural:
  NO cav2 invariants are yet in Lean; Perrone (2024) owns the entropy/MI unification;
  the H-axis rigidity is REFUTED at n=2; the chain cav2-invariant->Lean-theorem->
  proof-running-engine-obeys-it has ZERO complete links. Attestation is an
  INTEGRATION problem (buy-the-gate, months); provability is a RESEARCH problem.
- Source refs: `development/COMMERCIALIZATION-SYNTHESIS.md` ("give away the wedge, sell
  the trust"; moat = engine+governance+ATTESTATION+vertical; "Lean = the proof half";
  "most of the moat is deferred/unbuilt, enter as services"); `domainspec-lean-formalization/README.md`
  + `OPEN-SORRIES.md` (status:conjectural; none in Lean; Perrone; H-axis refuted);
  `development/machine-map/findings.md` §4.
- Authority level: candidate (E4 + verified by S2 against the Lean repo; under-claims vs the repo).
- Promotion owner: the commercialization decision-gate.
- Trace: E4 inversion; E4 own weak point = the collapse-test confirms it.
- Residue: betting on provability-as-moat anyway is a live owner-decision (build the attestation wall first).

## `one-gap-four-names-saturn-is-the-fix`

- ID: `one-gap-four-names-saturn-is-the-fix`
- Status: candidate
- Claim or candidate: the through-line of the whole session — the SAME single gap
  appears under four names: (1) "the mold is **hand-operated, not a machine**", (2)
  "**System-5 missing + System-3 manual**" (GOVERNANCE-ATTENUATION/VSM), (3) the
  "**meta-metric gap**" (governance governing itself has no measure it works), (4)
  "**most of the moat is deferred/unbuilt**". **Saturn** (read-only observation +
  continuous gates + collapsed policy) is the proposed fix, and it is **mostly
  unbuilt** -> the machine thesis is a **roadmap, not a description**. Highest-leverage
  FIRST build = the **read-only observer/meter** (it is the only build that closes the
  meta-metric gap and makes the rest falsifiable), after a thin authority-spine slice.
- Source refs: `development/machine-map/findings.md` §3+§5; `projects/ontologize/development/reflexive-substrate-harness/findings.md`
  (meta-metric gap); `ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md` (Saturn unshipped).
- Authority level: candidate synthesis.
- Promotion owner: DomainSpec plan owner.
- Trace: E3 sequencing + the cross-dispatch through-line.
- Residue: the live AUTHORITY-MAP-vs-GOVERNANCE-ATTENUATION contradiction (CONSTITUTION exists vs S5 missing) must be resolved before the observer has a baseline.
