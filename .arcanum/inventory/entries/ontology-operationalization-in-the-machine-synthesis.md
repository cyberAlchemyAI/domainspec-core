---
tags: [inventory, machine-map, viable-system-model, cav2, non-collapse, map-vs-decision, observer-executor-split, write-authority-proviso, leverage-point, two-ontologies, regulator-self-model, b-op-branch, domainspec-language, ontologize, build-from-owned, moat, claim-le-proof, research, findings]
node_type: synthesis
is_session: false
layer: architecture, governance
nature: reference
status: candidate
created: 2026-06-24
dispatch_id: 2026-06-24-ontology-operationalization-in-the-machine
dispatch_type: research
working_folder: development/machine-map/research/2026-06-24-ontology-operationalization/
sources: [development/machine-map/research/2026-06-24-ontology-operationalization/findings.md, development/machine-map/research/2026-06-24-ontology-operationalization/research.md, development/machine-map/findings.md, cyberAlchemy-v2/authority/AUTHORITY-MODEL.md, implementation/domainspec/ADLC-ALIGNMENT.md, implementation/domainspec/RELATIONSHIPS.md, cyberAlchemy-v2/development/research/2026-06-24-ontology-engineering-precedent/findings.md]
---

# Operationalizing Ontology in the Machine — Synthesis

Candidate Inventory synthesis (not canonical). Records the durable result of dispatch
`2026-06-24-ontology-operationalization-in-the-machine` (research; 4 explorers + 2 skeptics;
closed `resolved`; both skeptics accepted). How ontology gets operationalized inside the
machine (DomainSpec/Arcanum/Saturn/cav2), across four lenses — placement, moat, dynamics,
language — and what stays sound. Evidence backing:
[`2026-06-24-ontology-operationalization-cards.md`](evidence-cards/2026-06-24-ontology-operationalization-cards.md).
**Converges with** [`deterministic-retrieval-thesis-synthesis`](deterministic-retrieval-thesis-synthesis.md):
that dispatch reached the same spine from the RAG/determinism angle (typed-referent + recorded gate;
cav2 = recorded gate not generator; determinism = cost not requirement; authority conferred-and-recorded
at write = this synthesis's write-authority-proviso). Two lenses, one machine.

> Thesis: operationalizing ontology is **not a build problem — it is a finishing-and-wiring
> problem** (the observer, the Edge Law, and the binding tools already exist in code). The whole
> thing stays sound under exactly one discipline: **no modeling surface may hold a write-edge to
> a node's `promotion-status`/authority** — keep that edge architecturally absent and the map
> stays a *model*; grant it and the map starts to *decide* (Non-Collapse fails). The DomainSpec
> language is already Ontology A; cav2's authority ontology is a separate Ontology B; they ALIGN,
> they do not merge.

## Decision spine

| Question | Answer | Card |
| --- | --- | --- |
| Is operationalizing ontology a build problem? | No — build-from-owned: the read-only observer already exists in code (`tools/run-async-observer.ts` et al., "built, under-performing"), the Edge Law exists in RELATIONSHIPS.md (label-only), the binding tools (`validate-orphans.ts`, `generate-registry.ts`) exist, the build steps are owned (machine-map §3). | `operationalization-is-build-from-owned` |
| What keeps every option sound? | One architectural invariant: **no modeling operation may acquire a write-edge to authority/`promotion-status`**. Every collapse mode reduces to that re-fusion; soundness is the *absence of the edge*, not a relaxable policy. | `write-authority-proviso-architectural-absence` |
| One ontology or two? | **Two, independent.** A = DomainSpec language schema (L1: 25 meta-types + ~29 typed edges + the Edge Law). B = cav2 authority ontology (9 kinds + promotion DAG). They ALIGN at code-concept binding; B must NOT become A's type-checker; "domainspec-v2" = govern A + enforce A, earned on evidence. | `two-ontologies-language-vs-authority-no-merge` |
| The single highest-leverage act? | **Finish + baseline the already-built read-only observer** — the missing information-feedback loop (Meadows' highest structural leverage short of rules/goals/paradigm). It makes the rest falsifiable. (d) reconcile-spine is its *precondition*, not a lever; (g) "v2"-naming is anti-leverage. | `leverage-point-finish-the-built-observer` |
| Can a v2 type-change kill drift? | **Schema-level drift: yes** (endpoint-type the registry validator → forbidden edges unconstructible, "well-typed = can't-drift"). **Instance-level drift: no** — needs behavioral contracts; "the audit is permanently double." | `schema-drift-eliminable-instance-drift-not` |
| Why is the running ontology fragile? | Correctness is keyed to **review-time, not run-time**; drift-flagged is a **manual** sensor; the archive hardens (append-only) while the live regulator-model **drifts** — a fidelity risk for the whole control loop. | `review-time-not-run-time-regulator-decay` |
| Should machine-map / the model relocate INSIDE cav2? | **DEFAULT-DENY** until (1) cav2=S5 is *proven* (today it is analogy, machine-map §1) AND (2) the contained self-model is proven *write-incapable* — else the regulator re-fuses with the regulated (Conant-Ashby). | `cav2-relocation-default-deny` |

## What the skeptics changed (claim ≤ proof)

1. **Meadows demoted the "build" framing to build-from-owned.** The observer/meter is already in
   code (`tools/run-async-observer.ts`, `run-fast-observer.ts`, `governance-attenuation-audit.ts`);
   the Edge Law validator (`validate-relationships.ts`) exists but checks *label* membership, not
   *endpoint-pair* admissibility (the real net-new). The work is finishing, not inventing.
2. **Ashby reduced all collapse modes to one re-fusion** — a modeling op gaining a write-edge to
   `promotion-status`. SOUND: (a no-writeback), (b schema-A-only), (d), (e non-generative),
   (f flag-only). COLLAPSE: (c as canonical binding), (e relocation), (f auto-promote), (g as merge).
3. **The relocation question is answered as far as research can** — default-deny, gated on two
   proofs; co-locating with machine-map (current placement) is the sound default.

## Build sequence (owned; descriptive)

reconcile the authority-spine contradiction (AUTHORITY-MAP vs GOVERNANCE-ATTENUATION) → **finish +
baseline the read-only observer** → endpoint-type the Edge Law validator + `@biz`/`@sys` binding
closure + flag-only drift automation → non-generative collapsed-S5 policy doc. Each later step is
untestable until the observer's feedback loop exists.

## Routing (owner gates — Inventory cannot promote)

- **DomainSpec plan owner**: the observer finish+baseline; the Edge-Law-validator endpoint typing; the build sequence.
- **cav2 authority owner**: the write-authority-proviso enforcement; the two-System-5 boundary; the relocation decision.
- **constitution-governance + decision-gate**: the non-generative collapsed-S5 policy doc.
- **commercialization decision-gate**: whether the governance-data corpus is the moat bet.

## Open residue

- The write-authority proviso is **unverified in code** — find any path where a modeling edit writes `promotion-status`; if it exists, Non-Collapse is already broken.
- cav2=DomainSpec's-S5 is **analogy, not a cited link** (machine-map §1) — the relocation and the collapsed-S5 option both ride it.
- The governance-data corpus is an **intended stock, not a current one** — conditional on the observer being finished.
- "domainspec-v2" has **no committed milestone**; it is the name for governing+enforcing Ontology A, earned on evidence (passing validator, closed orphan loop, ≥1 constitution governing TAXONOMY).

## Downstream use

Use when a task asks where ontology fits in the machine, how to operationalize it, what the
DomainSpec language↔cav2 ontology relationship is, whether to relocate the machine-map into cav2,
or how to sequence the ontology/observer build. Do not cite as canonical — owners are the
DomainSpec plan + cav2 authority + the commercialization gate. Builds on
[`machine-map-and-moat-synthesis`](machine-map-and-moat-synthesis.md) and the field precedent in
`cyberAlchemy-v2/development/research/2026-06-24-ontology-engineering-precedent/findings.md`.

## Deliverable

`development/machine-map/research/2026-06-24-ontology-operationalization/findings.md` — the full
cited synthesis (four-dimension integration map + 7 options with SOUND/COLLAPSE verdicts + the
leverage point + the decision boundary incl. the relocation answer).
