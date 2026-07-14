---
tags: [framework-unification, diagram, feasibility, recon]
node_type: research
is_session: false
layer: architecture
nature: evidence
status: complete
version: 0.1.0
last_updated: 2026-07-14
created_by: victorboscaro@gmail.com
---

# Framework-unification diagram feasibility — raw explorer returns

Dispatch: `2026-07-14-framework-unification-diagram-feasibility` (2 explorers, axis:
inside `projects/framework-unification/` vs rest of repo). Verdict delivered inline in
the session; this file preserves the raw returns.

**Verdict (parent synthesis):** one Mermaid diagram is feasible **with caveats** — pick
ONE spine (the owned, locked two-axis CONCEPT-MAP model), render Saturn as
aspirational/dashed, tag nodes built/designed/aspirational, keep the two S5s and the two
ontologies distinct, and annotate the open forks instead of resolving them.

## Open Questions

- OQ-1: Which secondary framings (meta-layers L0–L7, machine-map VSM, 8-layer deck
  stack) deserve their own overlay diagrams vs staying out entirely? Recommendation:
  decide when the diagram is actually commissioned. Status: OPEN.

---

## Return A — inside `projects/framework-unification/`

### 1. Distinct unification attempts / phases visible in the workspace

Ordered by stated `last_updated`; each is a separate "how it fits" pass, and they do **not** all share one framing.

1. **domainspec-language — "one node envelope" validator** (2026-06-15, strategy session; status: draft/partial). Found a single recurring meta-shape (`intent / connections / residue / epistemic_tag / identity / body`) across ~15 pipeline artifacts; concluded the `epistemic_tag` field (3 costumes: Evidence Type / veracidade / claim≤proof) is the unification seam. File: `layers/domainspec-language/SCHEMA-INVENTORY.md`.
2. **cyber-alchemy-lean-fusion — typed-residue epistemic gate** (status: BLOCKED, later reframed). Fuse Arcanum lifecycle + Lean typed residue; only the `subset-rule` gate is "honest to build," the residue-ledger is unbuilt and gated behind an unresolved "what type fires the gate" question. Files: `layers/cyber-alchemy-lean-fusion/README.md`, `DESIGN.md`.
3. **dispatch-composition-attack — paired-views on dispatch observability** (2026-06-13; status: BLOCKED/exploratory). 7 stances named, decided nowhere; engineer-view never authored (BLOCKER OQ-A); plan never exercised ("fits now ≠ works now"); a typed-DAG reshaping fenced as a cross-repo decision. File: `layers/dispatch-composition-attack/system-view.md`.
4. **research → discovery "One Engine, Three Layers"** (2026-06-15; status: DONE as a map, "everything operational is OPEN"). The core three-pillar / three-mechanism framing. File: `discovery/discovery.md`.
5. **Review red-team** (2026-06-15; status: DONE, verdict FIX). Convicted 3 MAJORs. Load-bearing: **CR-D3 — "Saturn" appears nowhere in findings.md**; the triad only lives in RESEARCH.md. File: `review/findings.md`.
6. **SCOPE.md reframing** (2026-06-15; active). Reassigns the fusion's residue-type blocker to the sibling Lean repo, sets the bar to **utility-not-novelty**, and makes an `## Open Questions` section the operational residue ledger. File: `SCOPE.md`.
7. **CONCEPT-MAP two-axis model** (locked 2026-06-16). The OWNED organizing model: Axis-1 pipeline stages × Axis-2 three mechanisms + invariants. Referenced by every later node.
8. **ARTIFACTS.md four-tier catalog** (2026-06-16). Artifacts split into Tier A object / B knowledge / C signal / D engine; the pipeline Tier-A spine. File: `components/ARTIFACTS.md`.
9. **CAPABILITY-CENSUS** (2026-06-18; draft). Maps shipped sigils onto the two axes; concludes the shipped set is a "knowledge-governance + verification machine, not a generation machine," and the user's Knowledge/Craft/Governance seed buckets collapse onto owned models. File: `components/CAPABILITY-CENSUS.md`.
10. **recon INDEX — six-repo system census** (2026-07-03). Resolves "how many DomainSpecs": one built engine mirrored 3× + one genuine rewrite (v2); lists 6 duplicate-owner assembly targets; **Saturn "nowhere built."** File: `components/recon/INDEX.md` (+ `MAP-cyberalchemy-v2.md`, `MAP-domainspec-v2.md`).
11. **meta-layers-map** (2026-07-03). A **second, competing spine**: maps components onto an L0–L7 "meta-layers" theory imported from the business-philosopher repo. Files: `components/meta-layers-map/EXTRACT-META-LAYERS.md`, `COMPONENT-LAYER-MAP.md`.

### 2. Candidate diagram elements (nodes / edges + source)

**Stable nodes**

- **Three pillars:** DomainSpec (the *what*) · Arcanum (the *how*) · Saturn (the *evidence loop*) — `discovery.md` §"What the system is"; `recon/INDEX.md` §3. (Saturn caveated — see §3.)
- **Three mechanism layers** (= the three layer folders): representation = `domainspec-language`; communication/observability = `dispatch-composition-attack`; epistemology/gate = `cyber-alchemy-lean-fusion` — `discovery.md` layer table + D-1.
- **Two-axis model:** Axis-1 pipeline × Axis-2 three mechanisms — CONCEPT-MAP (cited by `CAPABILITY-CENSUS.md`, `ARTIFACTS.md`).
- **Pipeline stages (Axis-1 / Tier A spine):** problem-statement → define → research → findings → discovery → paired-views → plan → spec → stories → test-spec → code → (emit signals) — `ARTIFACTS.md` Tier A; `SCHEMA-INVENTORY.md` §A; `COMPONENT-LAYER-MAP.md` "Flow" steps 1–12.
- **Artifact tiers:** A object / B knowledge / C signal / D engine — `ARTIFACTS.md`.
- **Communication substrate:** append-only signal ledgers + `pass|flag|block` verdict vocabulary — `discovery.md` D-2; `recon/INDEX.md` §5; `MAP-cyberalchemy-v2.md` (CAV2-D37).
- **Key artifacts:** `pipeline-signals.jsonl`, `subagents-dispatch.yaml` (schema 0.6.0), the node envelope, TAXONOMY (25 meta-types / 29 edges), AXIOMS→CONSTITUTION→gates chain — `ARTIFACTS.md` Tier C/D; `MAP-domainspec-v2.md`; `COMPONENT-LAYER-MAP.md` L1/L3.
- **Alternative spine — meta-layers L0–L7** (+ L0.5, L1.5, L1.7, L2.5, Signal Protocol, Agent Interface) — `EXTRACT-META-LAYERS.md`; `COMPONENT-LAYER-MAP.md`.

**Stable edges / relations**

- `user intent → DomainSpec (structured intent) → Arcanum (routed execution) → signals → feedback correction → code` — `discovery.md` §"What the system is."
- Each pipeline stage: `producer skill → artifact`, with `derives-from` / `cites` edges — `ARTIFACTS.md` Tier A rows.
- Upward build + feedback edges: `L2⇢L1` (wired, via audit-alignment/DRIFT-CONVERGENCE); `L2.5⇢L0` (**unwired — Saturn's intended job**); `L3⇢L1,L2` governs; `L6⇢` blocks (only blocking layer) — `COMPONENT-LAYER-MAP.md` "Feedback edges"; `EXTRACT-META-LAYERS.md` §2.
- Division of labor: **novelty = sibling Lean repo; operationalization = this workspace (judged by utility)** — `SCOPE.md` §1; `discovery.md` D-4.
- `dispatch → existing ledger writer → central ledger`, fed by a `record producer` — `dispatch-composition-attack/system-view.md` §6.

### 3. Contradictions / unresolved forks that would make one diagram misleading

- **Two competing "fit" framings coexist, both dated 2026-07-03, neither retired.** The three-pillar / two-axis model (`CONCEPT-MAP` + `discovery.md`) vs the L0–L7 meta-layers spine (`COMPONENT-LAYER-MAP.md` / `EXTRACT-META-LAYERS.md`, imported from business-philosopher). Different node sets, different edges. Merging them into one diagram would be the biggest misleading move.
- **Saturn is a named pillar but not real.** "Saturn appears nowhere in findings" (`review/findings.md` CR-D3) and is "nowhere built… named as future actuator" (`recon/INDEX.md` §3; `MAP-domainspec-v2.md`; `MAP-cyberalchemy-v2.md`). Drawing it as a peer of DomainSpec/Arcanum overclaims.
- **"DomainSpec" is not one thing.** One built engine mirrored in 3 checkouts at 3 commits **plus** a genuine rewrite (domainspec-v2); v1↔v2 precedence unresolved (freeze gate unmet) — `recon/INDEX.md` §2, §4.2; `MAP-domainspec-v2.md` OQ.
- **Undecided owners (open forks), each an OPEN annotation, not a resolved edge:** dispatch-composition owner + v0.5.2 typed-DAG ratification (`discovery.md` OQ-1); `obligation_id` bridge owner B-1 (OQ-2); observability **producer feeding the central ledger is unbuilt** (OQ-3; `COMPONENT-LAYER-MAP.md` L2.5 "the one missing floorboard"); six duplicate-owner targets incl. authority spine (cav2 vs domainspec-v2), governance sigils in two homes, subagents-strategy home, and a taxonomy count stated three ways (24/26 vs 25/29 vs 25) — `recon/INDEX.md` §4.
- **The middle mechanism layer has no verdicts.** dispatch-composition engineer-view was never authored, so all 7 stances are provisional (BLOCKER OQ-A) — `system-view.md` §9.
- **The "one linear pipeline" (Axis-1) is itself contested.** whisper/x-ray form a *second* end-product producer lifecycle no stage places; the view-triad is an ownership layer, not a pipeline stage — `CAPABILITY-CENSUS.md` OQ-1/OQ-2. Node-granularity "one artifact" rule is proposed, not ratified — `ARTIFACTS.md` OQ-1.
- **Superseded framing still on disk.** The fusion README still frames the residue-ledger as gated on the residue-type blocker, while `SCOPE.md` §1 declares that blocker mis-scoped and reassigned to the Lean repo.
- **Dangling reference:** `SCOPE.md` and `discovery.md` cite `IMPROVEMENTS.md` (A-3 proposed SCOPE; A-1/C reprioritized), but **no IMPROVEMENTS.md exists anywhere in the workspace** (confirmed by search).

### 4. Verdict — feasible? **Yes, with caveats.**

A single coherent Mermaid diagram is buildable from this material **only if you pick ONE spine** — most defensibly the OWNED, locked three-pillar × two-axis pipeline model (CONCEPT-MAP, 2026-06-16), which every later node cites, and treat the L0–L7 meta-layers as a *separate overlay diagram*, not merged in. Required caveats: render **Saturn dashed/aspirational**; mark the **L2.5 observability producer** edge as the unbuilt gap; annotate the **v1-mirror-×3 + v2-rewrite** fork; keep duplicated-owner seams as **OPEN** annotations; use **built / designed / aspirational** status tags; do **not** fuse the three-pillar and L0–L7 framings into one graph.

---

## Return B — outside `projects/framework-unification/`

Note: `projects/framework-unification/CONCEPT-MAP.md` is repeatedly treated by all the docs below as the **owned, locked (2026-06-16) canonical unification model**. Everything outside that folder is either a *feeder into it*, a *different cut over the same machine that defers to it*, or a *pillar-specific rebuild*. No competing canonical unification exists outside it — but there are genuine forks a single diagram must resolve (§4).

### 1. Inventory of unification attempts (outside the folder)

| # | Name / location | Date | Status | One-line outcome |
|---|---|---|---|---|
| 1 | **Machine-Map** — `development/machine-map/findings.md` | 2026-06-24 | active (roadmap, mostly unbuilt) | Maps all four pillars onto Beer's VSM: DomainSpec=the modelled *what*, Arcanum=S1 *how*, Saturn=the S3↔S4 control loop, cav2=S5-outer meta-authority, DomainSpec AXIOMS=S5-inner. Key claim: **two distinct System-5s, one recursion apart, must NOT collapse.** |
| 2 | **Commitment-Levels lens** — `development/machine-map/commitment-levels.md` | 2026-07-03 | active (PROPOSED lens, explicitly *not* a replacement) | A "third cut" over the same machine (understanding→canonical→execution bands). Explicitly does **not** re-derive the two-S5 split and does **not** re-sequence CONCEPT-MAP's locked pipeline. |
| 3 | **Ontology-operationalization** — `development/machine-map/research/2026-06-24-ontology-operationalization/findings.md` | 2026-06-24 | resolved | Rules that DomainSpec-language (Ontology A) and cav2-authority (Ontology B) are **two independent ontologies that must NOT merge** ("B is not the type-checker"). |
| 4 | **Capability-taxonomy** — `research/cyber-alchemy-space/capability-taxonomy/findings.md` | 2026-06-18 | superseded / absorbed | Tried a Knowledge/Craft/Governance 3-bucket taxonomy; a skeptic pass **retracted it** because the two-axis model was already owned+locked by CONCEPT-MAP. Re-presented as a reuse map. |
| 5 | **SATURN-LAYER-MAP** — `ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md` | 2026-06-21 | active (explainer/reconciliation) | Authoritative "DomainSpec is the structured-intent layer of Saturn" statement. Flags **OQ-2: the deck's 8-layer stack vs CONCEPT-MAP's two-axis model may be two competing layer ontologies.** |
| 6 | **DomainSpec v2** — `projects/domainspec-v2/` | 2026-06-11 → 2026-07-11 | active | The DomainSpec pillar's own rebuild. Its `spec-ontology-unification` tower unifies *spec and code into one typed graph* (within-pillar, not cross-pillar). |
| 7 | **RELATED-FRAMEWORK-CROSSWALK** — `projects/domainspec-v2/RELATED-FRAMEWORK-CROSSWALK.md` | active | active | Crosswalks cav2, v1, lean-formalization, Saturn as **precedents with reuse verdicts, explicitly "crosswalk ≠ dependency."** |
| 8 | **cav2 SOURCE-MAP / authority spine** — `cyberAlchemy-v2/SOURCE-MAP.md`, `README.md` | 2026-06 | candidate | Lists framework-unification as a *source cohort* it ingests, not owns. |
| 9 | **System-recon session** — `sessions/2026-07-03-2014-system-recon-builder-reframe.md` (+ `-2010`, `-2104`) | 2026-07-03/06 | active (feeder) | 6-scout recon; pinned the objective: **unify to one coherent engine (one canonical source per capability, one authority spine)**. Wrote outputs *into* framework-unification's `components/recon/`. |

Tangential (NOT pillar-unification): `development/resonantos-integration/`, `development/deterministic-retrieval-thesis/`, `implementation/domainspec/PRODUCT-COMPONENTS-IDEA.md` (matched "unifica" only in the entropy/MI or retrieval sense).

### 2. How each relates to the framework-unification workspace

- **Machine-Map** — *parallel/complementary cut*, not superseded: reads the machine "by VSM system" where CONCEPT-MAP reads it "by two axes"; `commitment-levels.md` §9–10 cites CONCEPT-MAP as the map it is a *third cut* over.
- **Commitment-Levels** — *subordinate lens*; frontmatter and §0 state it "does not replace" CONCEPT-MAP.
- **Ontology-operationalization** — *constraint provider*; supplies the load-bearing **write-authority proviso** any unified diagram must respect.
- **Capability-taxonomy** — *absorbed-into-framework-unification*; cites CONCEPT-MAP as the OWNED model and downgrades itself to a reuse map.
- **SATURN-LAYER-MAP** — *parallel framing*; treats CONCEPT-MAP's two-axis view as one of two rival layer models (its OQ-2); sources from `cyberAlchemy/agentic-system-deep-dive.md`.
- **DomainSpec v2** — *pillar rebuild*; framework-unification recon treats it as "one genuine rewrite with its own local authority spine"; its unification is intra-pillar (spec==ontology, Lane Z vs Lane A).
- **Crosswalk & cav2** — *feeders / precedents*; both deliberately avoid dependency edges.
- **Recon session** — *direct feeder*; produced `components/recon/INDEX.md` and `meta-layers-map/`; introduced the **"builder vs product" reframe** (L0–L7 = product anatomy; the builder is the under-theorized unification target).

### 3. Authoritative "how the pillars fit" statements a diagram must respect

1. **Canonical three-pillar prose** (`cyberAlchemy/agentic-system-deep-dive.md:88-90,100,144`): DomainSpec = *what* (structured intent); Arcanum = *how* (reusable capabilities); Saturn = top-level convergence/control loop closing intent↔reality with evidence; Saturn "does not own ontology storage, memory mechanics, or every execution route."
2. **Layer statement** (`SATURN-LAYER-MAP.md` §4): "DomainSpec is the structured-intent layer of Saturn… Arcanum is the execution layer; inventory/ontology are knowledge layers; telemetry/reflection are perception layers Saturn reads back" — with an ASCII layer diagram (Modeling/Intent → Operation/Execution → Verification/Perception → Regulation/Interface), a ready diagram skeleton.
3. **CONCEPT-MAP compressed form**: "DomainSpec says *what*, Arcanum says *how*, Saturn closes the loop with *evidence*," refined by one horizontal pipeline × three vertical mechanisms.
4. **Two-System-5 rule** (`machine-map/findings.md` §1): cav2 = S5-outer; DomainSpec AXIOMS/CONSTITUTION = S5-inner; keep them one VSM-recursion apart.
5. **Two-ontologies rule** (`ontology-operationalization/findings.md` §1, §3g): Ontology A and Ontology B align at code-concept binding, they do **not merge**.
6. **Write-authority proviso** (same, §2): no modeling/observer surface may hold a write-edge to `promotion-status`/authority — Saturn/the observer is read-only-proposes-to-a-gate.

### 4. Forks a single unified diagram must pick a side on (or annotate as open)

- **FORK A — 8-layer stack vs two-axis model** (`SATURN-LAYER-MAP.md` OQ-2): two competing layer ontologies; one must be declared primary.
- **FORK B — Saturn's scope**: "just the S3↔S4 control loop" vs "the whole stack" — unresolved; determines whether Saturn is a loop *edge* or an enclosing *box*.
- **FORK C — cav2-as-DomainSpec's-S5**: recorded as analogy, not a repo-cited link (default-deny until proven).
- **FORK D — two-S5 vs belief/rule cut** (`commitment-levels.md` §4, §8c): orthogonal partitions of the same authority artifacts; convergence is an open owner question.
- **FORK E — public vs intended** (`SATURN-LAYER-MAP.md` §2, §5): only Arcanum is shipped; Saturn and DomainSpec are intended-not-shipped; the diagram must mark built vs intended.
- **FORK F — spec/ontology fusion undecided** (`spec-ontology-unification/toy/verdict.md`): Lane Z vs Lane A still OPEN.

**Feasibility read:** feasible — the SATURN-LAYER-MAP §4 sketch plus the deep-dive three-pillar prose give an authoritative skeleton — but only if the diagram (a) picks the control-loop reading of Saturn, (b) keeps the two S5s / two ontologies visibly distinct with no write-edge from model to authority, (c) marks Saturn+DomainSpec as intended-not-shipped, and (d) annotates Forks A/C/F as open rather than resolving them.
