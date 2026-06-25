---
node_type: research
title: "Operationalizing Ontology in the Machine — collected returns"
dispatch_id: 2026-06-24-ontology-operationalization-in-the-machine
status: collected
created: 2026-06-24
nature: research-raw
---

# Operationalizing Ontology in the Machine — Collected Explorer Returns (verbatim)

Dispatch `2026-06-24-ontology-operationalization-in-the-machine` (research). Four explorers
tensioned on a methodology × temporal-prior × source-corpus composite (structural-placement /
economic-moat-accrual / operational-drift / language-type-system+v2). Returns recorded faithfully;
cited synthesis + verdicts in `findings.md`.

---

## Explorer A — Beer (structural placement / runtime-machine)

**VSM placement (per `development/machine-map/findings.md`):** DomainSpec = modelled object;
Arcanum sigils = S1; Pipeline = S2; Gates/audits (manual) = S3; Saturn = S3↔S4 (intended-not-
shipped); cav2 AUTHORITY-MODEL = **S5-outer** (governs which *kinds* of authority may exist);
DomainSpec AXIOMS/CONSTITUTION = S5-inner. The two S5s must stay distinct or the recursion
boundary collapses. **Caveat (machine-map §1): cav2 = DomainSpec's S5 is a structural ANALOGY,
not a repo-cited dependency.**

Ontology lives **inside cav2's S5-outer perimeter but is explicitly NOT the authority-deciding
organ.** `AUTHORITY-MODEL.md` Non-Collapse rule 2: "Ontology can model authority, but it cannot
decide authority." `cyberAlchemy-v2/ontology/README.md`: the ontology package maps candidate
meaning / authority kinds / postures / relations / lifecycle / evidence / owner routes /
promotion requests / projection boundaries / residue — a **read-side projection and
candidate-staging surface**, not an operator of authority channels.

**Pipeline placement:** canonical pipeline (`projects/framework-unification/CONCEPT-MAP.md`):
`define→research→findings→discovery→paired-views(3b)→plan→spec→stories→tests→implement→verify→
emit-signals`. Ontology's injection point = **stage 3b (paired-views: ontology-view ·
system-view · engineer-view)** — post-discovery, pre-spec. But also cross-cutting: the
ontology-view is "the schema floor" making forbidden edges unconstructible by type wherever typed
edges are built/reviewed. Within-cav2 flow (`ontology/views/system-view.md`): raw/runtime
evidence → inventory evidence cards → authority artifact lifecycle envelope → owner route →
PromotionRecord-compatible decision → authority artifact → optional ontology projection. Ontology
projection is the final **read output**, not the promotion trigger.

**Existing ontology skills:** `ontology-vault` (governed knowledge store; map/distill/promote-
confidence/premise-review/validate — most mature, the primary structure-mutation surface);
`ontology-harness` (spell composing inventory + ontology-vault + context-builder, 13 phases —
coordinates, doesn't author); `ontology-view` (vocab/concept-graph projection; single canonical
term home + typed relations; **seed, unpromoted**); `paired-views` (triad spell enforcing the
four invariants: one home per term / name-once-decide-once / no verdict upstream / authority on
every verdict; **seed**). All built+runnable, **none promoted to stable.**

**Integration points that exist:** ontology↔authority-model (read-only posture); the
ontology/views sub-pipeline; paired-views anchored at 3b; a seed vault map
(`.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md`); inventory as the live seam.

**Gaps (cited):** OQ-1 (authority-kind table is review-governed, deterministic scan pending);
**live contradiction `AUTHORITY-MAP.md` (CONSTITUTION/AXIOMS exist) vs `GOVERNANCE-ATTENUATION.md`
("System-5 Missing")** — until reconciled the observer has no valid baseline; deferred items in
`ontology/views/system-view.md` (append-only authority-ledger validator missing; movement bridge
edge not admitted by edge law; live node/relation/lifecycle schema blocked pending schema
governance); OQ-B (two edge catalogs typed independently — shared registry unresolved); OQ-3
(central observability producer missing); seed skills unexercised against a live target.

**The DESIGNED-BUT-UNBUILT gap = the deferred system work:** ontology operates as a review-mode
candidate surface; it does not yet plug into any runtime validator. Path to enforcement:
ontology projection → schema-governance decision → validator contract → gate enforcement; steps
2–4 unbuilt.

**Machine-map's owned build steps (descriptive, `machine-map/findings.md §3`):** Step 1 —
reconcile the thin authority spine (the AUTHORITY-MAP vs GOVERNANCE-ATTENUATION contradiction is
the prerequisite blocker). Step 2 (highest-leverage first build) — the **read-only
observer/meter** (closes the meta-metric gap; splits observer from executor — Conant-Ashby
re-fusion is the failure mode). Step 3 — collapsed-S5-constitution (non-generative policy doc) +
continuous-S3 (CI gates data-driven).

---

## Explorer B — Porter (economic moat-accrual)

**Moat stack (`moat-stack-and-authority-triage-synthesis.md`):** four wall layers —
governance-data asset (time-gated) · embedded-workflow switching cost · counter-positioning
(vendor-neutral attestation incumbents won't ship) · proof-it-works (the meta-metric).
**Operationalized ontology is NOT the wall — it is a pre-condition for the wall's first layer.**

- **Governance-data asset:** ontology is the schema that makes governance data structured and
  comparable across runs (typed nodes, promotion-states, per-node challenge contracts). The
  ontology is the **vessel**; the data poured in over runs is the asset. Conditional: the vessel
  alone does not accrue.
- **Switching cost:** Non-Collapse-as-invariant baked into the workflow → a corpus of decisions
  from a system that provably cannot self-authorize; migration requires re-adjudication.
  Accrues **only if the write-authority proviso holds in code (currently unverified).**
- **Counter-positioning:** vendor-neutral, citable operationalization vs TopBraid EDG /
  Metaphacts (coupled to proprietary platforms). The field owns the mechanisms; only this stack
  makes them accessible without vendor capture. A positioning claim, not a novelty claim.
- **Proof-it-works (unbuilt):** the read-only observer makes the corpus auditable; you cannot
  instrument what is not typed. Doesn't yet accrue.

**Stock vs flow — honest verdict: operationalized ontology is a FLOW mechanism that ENABLES a
stock, but is not itself a stock.** Mechanisms (DL typing, OntoClean, SHACL, GRADE, EDG gates)
are field-owned; a competitor reconstructs them in 6–18 months. What *can* be a stock: the
**governance-data corpus** from running over real authorities — time-gated (month-18 competitor
still has zero months of decisions) + cross-run pattern density (if the observer is built).
**Bias confirmed: governance-data is NOT monotonically defensible** — accrues only if (a) the
observer is built, (b) Non-Collapse holds in code, (c) the corpus is retained/queryable. None
currently verified as shipped. **Intended stock, not current stock.**

**Defensible vs commodity partition.** Commodity (field-owned, build-from-owned): typed
node/edge schema (DL TBox), promotion-state lifecycle (OntoUML Phases + EDG), per-term gate
(Wikidata/OBO/GRADE), four-tuple (SHACL), "governed map with receipts" (RDF+PROV-O), challenge
protocol (OntoClean). Defensible (narrow, conditional): (1) Non-Collapse as enforced invariant —
the operational discipline, auditor-legible, hard to fake retrospectively (cond: write-authority
proviso in code); (2) traceable authority as emergent integration property (back-chains to
evidence + forward-chains to meaning in one structure — a competitor with SHACL+PROV-O+EDG in
three systems can't traverse it); (3) the governance-data corpus (cond on 1+2 + observer built).

**Highest-leverage investment for moat accrual = the READ-ONLY OBSERVER/METER**, not the
ontology apparatus (mostly there, field-owned). Without it, runs produce unstructured logs and
the asset never compounds.

---

## Explorer C — Forrester (operational dynamics under load)

Grounded in `NODE-MODEL.md`, `RELATION-MODEL.md`, `LIFECYCLE-MODEL.md`, `PACKAGE-MODEL.md`,
`AUTHORITY-MODEL.md`, `DEFINITIONS.md` (D19/D23/D33/D48/D49), `DEFINITION-DRIFT-AUDIT.md`,
`ARCHITECTURE-KNOWLEDGE-GOVERNANCE.md`, `machine-map-and-moat-synthesis.md`.

**Decay/staleness dynamics.** The ontology is a layered candidate surface with four temporal
object classes. Nodes: `candidate_status` (candidate→reviewed-candidate→deferred→blocked→
projected) then post-promotion lifecycle (active→**drift-flagged**→superseded→deprecated).
`drift-flagged` is the staleness sensor — but the trigger is **not automated** (no background
process advances active→drift-flagged; review-mode, OQ-1). Candidate records carry a
`drift_owner` field with **no enforced update cycle**. Relations: `routes_drift_to` is a
candidate (design-intent) relation, **cannot fire as a run side-effect**. Definitions: CAV2-D33
requires a `drift_route`; `DEFINITION-DRIFT-AUDIT.md` tracks drift **manually**, one-time per
session (its own `Last updated: 2026-06-23` proves correct-at-audit-time, not continuous).

**Key decay mechanism: correctness is parameterized by REVIEW time, not RUN time.** Each run
generates new candidates/projections/ledger events/residue, but **none auto-triggers
re-validation** of existing nodes. The gap widens monotonically until a human audits/contradicts.

**Maintenance burden + ownership.** `drift_route` (definitions) + `drift_owner` (candidate
records) are the assignment instruments; `ARCHITECTURE-KNOWLEDGE-GOVERNANCE.md` formalizes "who
handles stale evidence." **No cross-cutting maintenance owner** — each authority kind's own route
handles its drift-flagged reviews (definitions→definitions-governance, etc.). **Burden scales
linearly with promoted artifacts; review bandwidth does not** (human-gated per-route). Unresolved
debts: deterministic kind-enumeration scan pending (OQ-1); authority-ledger validator missing;
the S5-outer AUTHORITY-MAP vs GOVERNANCE-ATTENUATION contradiction (no stable regulator baseline
until closed).

**Accumulates vs decays — simultaneous, opposite directions.** ACCUMULATES (durable stocks):
promoted definitions (permanent until superseded), ledger events (CAV2-D26 append-only, no
expiry), residue (CAV2-D18, no auto-resolve), challenge contracts (CAV2-D40, per node), evidence
cards/inventory (no pruning). DECAYS: active nodes post-promotion (source/behavior changes, node
stays `active` but diverges — detected only by human audit), projection rows (no auto-
invalidation), candidate records with stale `source_refs` (no path-freshness check), `drift_route`
assignments (static string, no re-validation), **ontology-as-regulator-model** (coverage of the
current system shrinks unless continuously updated — review-mode only).

**Critical dynamic:** the regulator-model's staleness is a **fidelity problem for the entire
control loop** — a stale ontology tells cav2 it regulates a system that no longer matches reality.
**The archive grows authoritative while the live model drifts — two opposite vectors on the same
ontology.** Only reconciler today is episodic human audit. *(Conant-Ashby re-fusion verdict
reserved for skeptic Ashby.)*

---

## Explorer D — Lambek (language / type-system / v2)

**Two ontologies, named precisely.**
- **Ontology A — DomainSpec Language Schema** (TAXONOMY + RELATIONSHIPS): a finitely-presented
  category (= L1 in `domainspec-two-layer-framework.md §3.1`). Objects = 25 meta-types; morphisms
  = ~29 typed edges; the **Edge Law** is already in RELATIONSHIPS.md as typed-endpoint constraints
  (`enforces`: Rule→Operation; `reflects`: State Indicator→State Machine; …). **Already
  schema-level**, not a flat glossary.
- **Ontology B — cav2 Authority Ontology** (AUTHORITY-KINDS + promotion DAG): objects = authority
  kinds (definition/constitution/decision/spec/runtime_contract/projection/evidence/residue);
  morphisms = promotion paths. Non-Collapse → its edges route candidates to gates, do not produce
  verdicts. **NOT L1** — no Entity/Operation/Rule; operates at the meta-level of how artifacts
  move through governance.

**These two are structurally independent** (no shared edges/objects/logical dependency). They may
*refer* to each other (a SPEC artifact can be a `kind.spec` candidate) but kinds don't decompose
into meta-types and meta-types don't imply promotion rights.

**Q1 — converge or stay separate? They stay SEPARATE but must formally ALIGN at the code-concept
binding layer.** ADLC v1.9 (G11+G12, T8-T10) = the `@biz`/`@sys` annotation task = a compilation
contract Δ: L1→L2 (concept graph → TS code schema); registry.json (T10) materializes the functor.
Annotations are **realization witnesses** ("I am an instance of `payment.ProcessPayment :
Operation`"). Orphan detection = Δ not total; unanchored-concept detection = surjection failure.
**The operationalized cav2 ontology (B) does NOT become the type-checker.** The type-checker is the
**Edge Law (E) embedded in RELATIONSHIPS.md** — entirely within Ontology A. Ontology B is upstream
(governs whether TAXONOMY/RELATIONSHIPS reached `kind.constitution` status), not whether a registry
edge is typed correctly. **Reconciliation needed:** a registry concept node declares its
`meta-type`; the registry validator checks edges against the Edge Law for that meta-type →
operationalizing **Ontology A**, not B.

**Q2 — is "domainspec-v2" the cav2 consolidation + ADLC v1.9 binding? YES, with a scope boundary.**
"domainspec-v2" appears nowhere as a named effort (honest: no committed milestone). What exists:
cav2 consolidation (produces Ontology B artifacts — kind.constitution for TAXONOMY.md, decision
records for edge-law changes) + ADLC v1.9 (produces the operational instance of Ontology A —
registry.json, @biz, validator CLI). **Complementary, not the same.** You need both for a "typed,
governed DomainSpec language." **Verdict: v2 = cav2 authority-governance over the language schema +
ADLC v1.9 machine-checkable enforcement of it; should NOT be declared until evidence** (passing
registry validator, closed orphan loop, ≥1 constitution-level artifact governing TAXONOMY.md).
Neither shipped.

**Q3 — can a v2 type change make drift classes unconstructible? YES for schema-level, NO
(automatically) for instance-level** — the two-layer framework names exactly this boundary.
Schema-level: if the registry validator enforces the Edge Law, `Entity —enforces→ Operation` from
an Entity-typed node is **structurally rejected** → the drift class "Entity used as a Rule"
collapses into a type error at registration, not audit. Cross-layer too (a Hook claiming to
`enforces` a Rule). Instance-level: the §3.6 counterexample shows a faithful schema functor Δ can
still have the instance round-trip fail — even with correct `@biz` annotations, runtime behavior
can drift from the Operation spec; requires behavioral contracts (test derivation, separate
layer). **"The audit is permanently double" (§5).** Specific eliminable-by-construction classes:
(1) wrong meta-type wired via illegal edge; (2) cross-layer wrong-endpoint edge; (3) orphaned
concept (T9 CI); (4) unanchored concept; (5) behavioral drift — **NOT** type-eliminable.

**What "operationalizing ontology" means here:** take L1 from Markdown to a machine-checkable
schema with (1) typed nodes (every concept carries a meta-type), (2) edge-law enforcement, (3)
code-binding closure (no unanchored/orphaned). Properties 1+2 = "well-typed concept graph"; 3
closes the L1↔L2 bridge. The three make **schema-level drift unconstructible**. cav2's authority
ontology governs the schema's authority lifecycle — **two different categorical objects that must
coordinate, not collapse.**
