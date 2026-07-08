---
dispatch_id: 2026-07-07-enterprise-ontology-building
kind: research-transcript
created: 2026-07-07
status: closed
exit_reason: resolved
note: >
  Verbatim explorer returns. This is the raw evidence layer; the reconciled,
  skeptic-corrected, auditor-accepted picture is in findings.md. Transcription
  only — do not edit claims here; corrections live downstream.
---

# Research transcript — How ontologies are built inside companies

Four explorers, pairwise tensioned on composite(methodology × source-corpus ×
temporal-prior). Returns pasted verbatim.

---

## Explorer 1 — Simon, Herbert · academic ontology-engineering methodologies

**Angle:** formal/historical; academic surveys; historical-lineage.

Seven named methods, all retrieved + read:

1. **Uschold–King (1995)** — IJCAI-95 Workshop; Enterprise Ontology built at Edinburgh
   AIAI with **IBM, Lloyd's Register, Logica UK, Unilever**, UK DTI-funded.
   https://www.aiai.ed.ac.uk/project/enterprise/enterprise/ontology.html
   4 skeletal activities: purpose/scope → build (capture/code/integrate) → evaluate →
   document. First "middle-out". Real consortium deliverable.
2. **Grüninger–Fox / TOVE (1994–95)** — IJCAI-95 Workshop; eil.utoronto.ca. Motivating
   scenario → informal **competency questions** → FOL terminology → formal
   defs/constraints → **completeness theorems**. TOVE = Toronto Virtual Enterprise
   testbed. Competency-question technique absorbed into NeOn + successors.
3. **METHONTOLOGY (1997, UPM)** — AAAI-97 Spring Symposium; KAW98
   (https://ksi.cpsc.ucalgary.ca/KAW/KAW98/blazquez/). Three bands: project management
   (planning/control/QA); development (specification → conceptualization → formalization
   → implementation); support (knowledge acquisition/evaluation/integration/documentation/
   **configuration management**). Evolving-prototypes lifecycle. Built (KA)² ontology;
   basis of WebODE; IEEE 1074 alignment. Config management = version all
   documentation/code/ontology + control changes.
4. **On-To-Knowledge / OTKM (2001)** — Staab/Studer/Sure; Springer
   doi 10.1007/978-3-540-24750-0_6. Knowledge Meta Process 5 steps: feasibility →
   kickoff → refinement → evaluation → **application & evolution**. Separates
   Meta-Process (build) from Process (use). EU project; OntoEdit. Has evolution phase but
   OMITS documentation + configuration management.
5. **DILIGENT (2004–05)** — Pinto/Tempich/Staab/Sure; ECAI-04, ESWC-05
   doi 10.1007/11431053_17. 5-stage decentralized: build → local adaptation → analysis →
   revision → local update, central **board** controls shared core; formal
   **argumentation** framework (RST) for traceable consensus. Applied to **OPJK**
   (legal ontology, Spanish jurists). The only classical method built around distributed
   governance + evolution — argumentation over concept introduction = edge/change
   governance analog.
6. **UPON (2005)** — De Nicola/Missikoff/Navigli; DEXA-05 doi 10.1007/11546924_64;
   Information Systems 34(2) 2009. Port of Unified Software Process — use-case-driven,
   iterative/incremental (inception→elaboration→construction→transition). EU **ATHENA**
   project. UML-style typing/versioning.
7. **NeOn (2008–15, UPM/OEG)** — Applied Ontology 10(2) 2015 doi 10.3233/AO-150145.
   NOT a rigid workflow — **9 scenarios** (from scratch; reuse/re-engineering; alignment;
   **modularization**; **localization**; design patterns) + ~59 processes. Assumes
   **ontology networks**. Case: **FAO of the UN**. Richest mapping surface.

**Mapping notes:** Typed ← TOVE CQ completeness, UPON UML. Versioning ← METHONTOLOGY
(config mgmt), OTKM (evolution), NeOn (re-engineering), DILIGENT. Edge-governed/promotion
← DILIGENT argumentation board (closest classical analog), NeOn scenario gates.
Branched/two-DAG ← NeOn localization+modularization, DILIGENT central-core-vs-local.
Post-NeOn: SAMOD, LOT (agile/LLM variants, not deep-retrieved — **certified thin spot**).

**Surface certified:** web sweep (7 queries) across academia.edu, ResearchGate,
SpringerLink, ACM DL, Semantic Scholar, UPM oa.upm.es, AIAI Edinburgh, Cambridge Core.
Read in full: AIAI Enterprise Ontology, KAW98 METHONTOLOGY, OEG NeOn. Blocked (flagged,
backfilled from abstracts): two oa.upm.es PDFs (garbled), Springer OPJK (auth redirect),
Cambridge evolution review (429).

---

## Explorer 2 — Wisnesky, Ryan · industrial knowledge-graph practice

**Angle:** empirical; engineering blogs/case studies; modern-only.

**Confirmed production deployments (strong):**

- **Amazon COSMO** —
  https://www.amazon.science/blog/building-commonsense-knowledge-graphs-to-aid-product-recommendation
  Amazon's *first production* system using instruction-tuned LLMs to build+serve a KG.
  query-purchase + co-purchase → LLM emits typed relations (usedFor/capableOf/isA/cause)
  → refined into finer typed set → heuristic winnow → **human review on plausibility +
  typicality** → ML classifier threshold → survivors re-encoded as instructions. 30k
  annotations → 29M edges / 18 categories. +60% macro-F1 (fixed encoder), KDD Cup 2022.
  Dual-threshold = edge-admission governance. No versioning.
- **Amazon AutoKnow** —
  https://www.amazon.science/blog/building-product-graphs-automatically
  +200% facts, product-type typing 87.7%. Taxonomy typing + entity canonicalization core.
- **LinkedIn Skills Graph** —
  https://www.linkedin.com/blog/engineering/data/building-maintaining-the-skills-taxonomy-that-powers-linkedins-skills-graph
  entity-discovery → sanitization → **hybrid curation** (human taxonomists assign
  parent-child edges + train KGBert). Richest edge-governance source: **polyhierarchy
  allowed only when parents mutually inclusive**; ambiguous mappings prohibited by rule.
  39k skills / 374k aliases / 200k relationships / 26 locales. No versioning protocol (gap).
- **LinkedIn Knowledge Graph** —
  https://www.linkedin.com/blog/engineering/knowledge/building-the-linkedin-knowledge-graph
  standardized entity taxonomies+relationships so products "speak same language". Title
  standardizer classifier. Hierarchical typing title→super-title→function.

**Method infrastructure:**

- **CQL / Conexus** — https://categoricaldata.net/CQL/ ·
  https://conexus.com/functorial-data-migration/ Spivak functorial data migration;
  schemas = categories, migrations = functors that **provably preserve constraints** —
  integrity by construction vs classifier threshold. Named deployments (Uber, NIST)
  thinly documented — enterprise adoption **plausible-but-under-evidenced**; tool+math real.
- **dbt Semantic Layer / MetricFlow** — https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl
  metrics defined once in code, git-versioned. Best promotion/versioning coverage:
  **metrics carry explicit versions like APIs**, data contracts + access policies,
  ownership defined, definitions auditable to source. In production across dbt customers.

**Thin:** eBay (no build narrative); pharma/finance (vendor-level not first-party).

**Cross-cutting pattern:** discover from behavioral/free-text signal → sanitize → **typed
relation vocab as governance object** → hybrid human+ML admission gate → serve
online+offline. Two governance philosophies: *statistical admission* (Amazon thresholds,
LinkedIn guardrails) vs *constraint-preserving construction* (CQL functors). Versioning
weakest everywhere except dbt.

---

## Explorer 3 — Beer, Stafford · standards & vocabulary authority

**Angle:** formal; standards bodies/data-management canon; mixed.

- **BFO** — ISO/IEC 21838-2:2021 (https://www.iso.org/standard/74572.html);
  github bfo-ontology/BFO-2020. ISO-standardized top-level ontology; conformance
  requirements on domain ontologies. **650+ projects**; Jan 2024 BFO + Common Core made
  **baseline standard for all US DoD + Intelligence Community ontology work** (CDO memo).
  ISO 21838 also admits DOLCE, TUpper — the standard itself is the promotion gate for
  "what counts as foundational".
- **gist (Semantic Arts)** — semanticarts.com/gist; github semanticarts/gist.
  Minimalist enterprise upper ontology (~135 classes) in ordinary business vocab;
  single-maintainer authority; **semver release discipline** ("gist 13.0.0 major release
  breaks backward compat, includes migration scripts"). Finance/healthcare/gov adoption.
- **SKOS / OWL2 / RDF / SHACL** — SKOS governs concept schemes (broader/narrower/
  prefLabel); OWL2 formal semantics; **SHACL machine-checkable constraint enforcement**.
  TopQuadrant EVN = collaborative SKOS vocab management enterprise-wide.
- **DAMA-DMBOK** — dama.org. Defines **role structure** for term ownership — Data
  Owners / Data Stewards / Governance Councils. DAMA Dictionary 2000+ terms.
- **schema.org governance** — https://schema.org/docs/howwework.html Explicit **promotion
  gate**: proposed terms enter **pending** status for testing/feedback before promotion to
  core; small Steering Group final approval (unanimous, ~10-business-day window); larger
  Community Group day-to-day via GitHub. Clean propose→pending→promote pipeline.
- **Enterprise ontology operating model** —
  https://www.getgalaxy.io/articles/ontology-management-semantic-modeling-operating-model-enterprise-context
  three-role ownership (Domain Stewards / Semantic Architecture Board / Platform);
  "ontology changes are contract changes" (versioned v2.3.0); **three-tier change
  classification** Editorial → Additive → Breaking; **semantic registry** tracking each
  term's owner/version/status/downstream consumers.
  ⚠️ *Single vendor article — caveat carried downstream.*

**Assessment:** strongest single import = change-tier → approval-depth matrix + semantic
registry. Caveat: adoption figures + schema.org/Galaxy process details from secondary
summaries + one vendor article; ISO/W3C/GitHub locators primary.

---

## Explorer 4 — Alexander, Christopher · socio-organizational reality & failure modes

**Angle:** historical/adversarial; KM literature/post-mortems; mixed.

**Surface certified: thin on hard evidence, thick on convergent practitioner consensus.**

1. **Maintenance/drift is the dominant killer, not construction** —
   https://www.thoughtworks.com/insights/blog/data-strategy/why-ontologies-matter-fail-build-anyway
   "Construction is a one-time event, reconciliation is continuous"; stale within two
   quarters; *"If you can't answer 'who decides when meaning changes,' you don't have an
   ontology program."* Opinion, high consensus.
2. **Semantic drift invisible to standard monitoring; distributed governance trades
   agility for drift** — arXiv 2606.01722 + Medium. Needs named semantic stewards.
3. **Big-bang / model-everything scope kills projects** — Thoughtworks; timbr.ai;
   stibosystems.com. "Look visionary but ship nothing… die after a year".
4. **Translation gap** — engineers know formalism not business; SMEs vice versa; interview
   transfer lossy (Thoughtworks).
5. **Governance fails from org-culture misfit** —
   https://enterprise-knowledge.com/taxonomy-governance-best-practices/ centralized/
   top-down vs decentralized/bottom-up ownership; start tight, loosen as users mature;
   governance = living document over months/years.
6. **Prevalence (adjacent):** Stibo cites Gartner "90% programs fail"; Gartner "80%
   governance initiatives fail by 2027"; arXiv 2201.06310 "87% data-science projects never
   reach production".
7. **UNREAD empirical anchor (paywalled 403):** "The Data Governance Journey in Practice:
   Insights from Case Study Research", Information Systems Management 2025,
   doi 10.1080/10580530.2025.2477459 — open-coding of 20 empirical case studies.

**Bottom line:** enterprises can **build** but cannot **sustain**. Load-bearing failures:
(a) no standing owner / undefined "who decides when meaning changes"; (b) continuous
reconciliation underfunded → drift invisible; (c) top-down big-bang scope outruns
adoption; (d) governance-culture misfit. **Caveat:** mostly self-echoing practitioner
opinion; the one 20-case empirical study is paywalled/unread.
