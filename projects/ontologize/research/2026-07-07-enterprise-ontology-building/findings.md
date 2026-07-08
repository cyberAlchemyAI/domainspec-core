---
dispatch_id: 2026-07-07-enterprise-ontology-building
kind: research-findings
created: 2026-07-07
status: closed
exit_reason: resolved
final_approver: "Vlachopulos, Ioannis"
verdict: ACCEPT
agents_spawned: { total: 8, explorers: 4, synthesizer: 1, skeptics: 2, auditor: 1 }
note: >
  Post-skeptic, auditor-accepted picture. Every load-bearing claim ≤ its proof.
  Raw evidence in research.md. Ownership claims about our own repos were verified
  on disk by the precedent skeptic (Kuhn) and spot-checked by the auditor.
---

# Findings — How ontologies are built inside companies

## Plain answer (the one line)

The credible reference base is a **spectrum, not the vendor "operating-model" trope**:
(1) classical engineering **methodologies** (Uschold–King, Grüninger–Fox/TOVE,
METHONTOLOGY, DILIGENT, NeOn) as *method* prior art; (2) production **knowledge-graph
systems** (Amazon COSMO/AutoKnow, LinkedIn) as the strongest *evidence* anchors;
(3) governed **shared vocabularies** (schema.org, DAMA, dbt/gist) as *promotion/versioning*
prior art; (4) **BFO/CCO** as a real institutional standard (US DoD/IC). **Against that
base, the ontologize design is mostly build-from-owned** — its five commitments inherit
external prior art — and its **only distinctive-and-owned move is the divergence-preserving
(anti-functorial) bridge edge.**

> The blunt correction the skeptics forced: two things first framed as *outward
> discoveries* — the branch/bridge model and the two-DAG split — are **our own
> schema-enforced architecture**, not findings. Crediting owned design as a survey result
> was the synthesizer's main error, and it was caught.

## Verdict matrix (one row per candidate)

| Candidate | Cluster | Verdict | Commitment | Note |
|---|---|---|---|---|
| Uschold–King / Enterprise Ontology | academic | **keep** | C5 | DTI-funded, named industrial partners |
| Grüninger–Fox / TOVE competency questions | academic | **keep** | C2, C5 | completeness = evidence discipline |
| METHONTOLOGY configuration management | academic | **keep** | C4, C5 | version all artifacts |
| DILIGENT argumentation board / OPJK | academic | **keep** | C3, C5 | traceable-consensus owner decision |
| UPON (UML typing) / ATHENA | academic | **keep** | C2 | |
| NeOn scenarios / FAO of UN | academic | **keep (weak-transfer)** | C1 | modularizes *one* open-world ontology, not two epistemic kinds |
| SAMOD, LOT | academic | **demote** | — | not deep-retrieved (certified thin) |
| Amazon COSMO | industrial | **keep — strongest anchor** | C3, C5 | **+28–60% macro-F1 depending on setting**; auto-promote *diverges* from our human gate |
| Amazon AutoKnow | industrial | **keep** | C2 | 87.7% type accuracy |
| LinkedIn Skills Graph | industrial | **keep — richest edge governance** | C3 | polyhierarchy-only-if-mutually-inclusive rule |
| LinkedIn Knowledge Graph | industrial | **keep** | C2 | hierarchical typing |
| dbt Semantic Layer / MetricFlow | industrial | **keep mechanism / demote adoption** | C4, C5 | semver + contracts = verifiable; breadth = vendor self-report |
| CQL / Conexus functors | industrial | **weak cross-check only** | C3 (acyclicity) | **does NOT transfer** — see "most distinctive" |
| eBay / pharma / finance | industrial | **demote** | — | no first-party build narrative |
| BFO (ISO 21838-2) + DoD/IC memo | standards | **keep (memo=fact) / downgrade "650+"** | C2 | memo multi-source; count advocate-self-reported |
| gist (semver discipline) | standards | **keep mechanism / demote adoption** | C2, C5 | |
| SKOS / OWL2 / RDF / SHACL | standards | **keep** | C3 | domain/range/inverse/constraints |
| DAMA-DMBOK role structure | standards | **keep** | C5 | owner/steward/council roles |
| schema.org pending→promote | standards | **keep (source-backed)** | C5 | unanimous + 10-business-day window confirmed |
| Galaxy operating model | standards | **PROPOSAL, not evidence** | C5 | single vendor blog, zero named orgs — **vacuity kill** |
| Thoughtworks / Stibo / EK drift+culture | socio-org | **demote to hypothesis** | C5 shortfall | consultant consensus, no case data |
| Gartner 90/80/87% prevalence | socio-org | **demote** | — | secondhand, self-echoing |
| ISM 2025 20-case study | socio-org | **demote (unread)** | — | paywalled; would be strongest empirical anchor |

## Where the design stands, per commitment

- **C1 Branched → build-from-owned.** The two-epistemic-kind split (meaning vs
  system/behavior) joined by divergence-preserving bridge edges is **owned and
  schema-enforced** (`ONTOLOGY-BRANCHES.md`, `BRANCH-AS-VIEW.md`,
  `schemas/ontology-node.schema.json`). NeOn/DILIGENT are *weak* analogs — they partition
  one open-world ontology, not two kinds. External credit: low.
- **C2 Typed nodes → genuinely external prior art.** BFO/gist/UPON + Amazon + LinkedIn
  confirm typed-node systems ship in production. But our six types are a
  **promotion-pipeline vocabulary, not an upper-ontology substance taxonomy** — so BFO is
  *not* our source and re-invention risk is low. Prior art validates the *pattern*, not our
  instantiation.
- **C3 Edge-governed → external concept + owned constraint.** OWL2 (domain/range/inverse)
  + SHACL (constraints) are real prior art; LinkedIn's rule-guarded catalog is the industrial
  analog. But **per-edge acyclicity + the 4-category edge catalog** are owned and the
  *least externally covered* item — open-world OWL "property soup" does **not** transfer
  (it permits the cycles/collapse the gate forbids).
- **C4 Two orthogonal DAGs → build-from-owned.** Lifted from our own GoldenQuill
  promotion-record DAG (`DAG-AND-METRICS.md §1`). OTKM meta/process split and dbt are
  decoration, not source.
- **C5 Promotion-governed → strongest external prior art.** schema.org + DAMA lifecycles are
  the real precedent; dbt/gist mechanisms are verifiable. Our `veracidade` + `evidence_refs`
  binding is a **tighter variant** of the same pattern — a tightening, not novelty.

## The single biggest gap (corrected)

**Not** the broad "sustainment" story (a consultant trope resting on one unread paywalled
study). Owner routes, `OwnerDecision` (N5), the promotion lifecycle
(captured→…→promoted/rejected/retired/contradicted), and `drifts_from` vs `contradicts`
are **already built and schema-enforced** (`RELATION-MODEL.md`, `LIFECYCLE-MODEL.md`,
`DAG-AND-METRICS.md §3/§6`). The **true residual gap is narrow**: *re-review cadence and
thresholds* — who re-examines promoted `KnowledgeProjection`s on a schedule, and what
triggers a drift-flagged → active re-review. Already logged as `[H]` residue
(`DAG-AND-METRICS.md`). **Actionable next step:** tune cadence/thresholds in the pilot; do
not build a new ownership layer — it exists.

## The single most distinctive thing (corrected)

The **divergence-preserving bridge edge** (`drifts_from` / `observed_by`): intent and
behavior held apart with *no silent smoothing*. Precisely because it preserves divergence
it is **anti-functorial** — a CQL functor preserves constraints *by construction*, so a
"functor that drifts" is not a valid functor, and CQL's headline property **cannot carry
over**. The sharper external contact is a **negative, already-owned** result:
DomainSpec's two-layer no-go (`M6Counter.lean`, cited at `DAG-AND-METRICS.md §5`) —
schema-correctness does *not* force instance-fidelity — which is the real reason a
noncollapse gate must exist. Distinctive, yes; but it is architecture we **own**, not prior
art we found.

> ⚠️ **Cross-repo caveat (auditor):** `M6Counter.lean` is **not** in `domainspec-core` — it
> lives in the sibling `domainspec-lean-formalization` repo
> (`.../lean-formalization/M6Counter.lean`, `m6_strong_refuted_poly`, sorry=0) and is cited
> consistently across this repo. The "distinctive-and-owned" verdict depends on that
> cross-repo artifact; a reader of `domainspec-core` alone cannot open it.

## Audit trail

- **check-tension gate:** REJECT→revise→PASS (both agents). Two explorer pair-evidence
  sentences relabeled off the illegal skeptics-only `attack` axis onto in-group axes.
- **Skeptic round (zig-zag, 1 loop):** Taleb (vacuity) killed the Galaxy operating model as
  evidence, restated COSMO to proof-width, demoted self-counted adoption figures and the
  sustainment gap. Kuhn (precedent) proved both headline claims were owned-design
  self-citation, that CQL is anti-functorial to the bridge, and that the sustainment gap is
  overstated (role/routes/lifecycle already schema-enforced).
- **Auditor (final approver):** ACCEPT. Spot-checked BFO/DoD memo (confirmed, Jan 2024, no
  count on the page), COSMO SIGMOD 2024 (+60% fixed / +28% fine-tuned — range is
  proof-width), schema.org governance (source-backed; picture if anything *under*-claims).
  No citation fails. Cross-repo `M6Counter.lean` caveat noted above.
