# DomainSpec Paper — Candidate-Additions Brief

- **Dispatch:** `domainspec-paper-update-research-20260610`
- **Date:** 2026-06-10
- **Status:** read-only research output; paper write is gated on operator approval
- **Base (recent):** `implementation/domainspec/docs/research/domainspec-paper.md`
- **Target (older copy to update):** `research/projects/domainspec/papers/domainspec-paper.md`
- **Lanes run:** paper-baseline-differ, e11-evidence, research-evidence, vault-ontology, formal-theory (5 read-only subagents, parent synthesis + skeptical audit applied)

---

## 0. Headline

The "recent" base is already an **evolved** version of the older research copy. The dominant delta is an ontology bump driven by experiment **E9**: **24 meta-types / 26 edges → 25 / 29** (adds the `Saga` meta-type + 3 cross-feature edges `produces-for` / `triggers-cross` / `enforces-cross`), a **composed derivation function** `T_composed = f(C,R,Δ) + f_cross(E_AB, Δ_cross)`, new §1.1 hypotheses/RQs, and a rewrite of §9.2 from *"future work"* to *"resolved"*.

So the update is **two moves**:
1. **Port the recent base** onto the research copy (it carries the 25/29 + composition story the older copy lacks).
2. **Layer in the approved dispersed additions + E11**, each at its true evidence grade.

The skeptical audit surfaced **two existing paper claims that are currently unsupported by any artifact** (§6.5 signal numbers, §8 case-study counts) — these are flagged below as integrity items, not additions.

---

## 1. Port-from-recent-base candidates (status: documented; low risk)

These already exist in the recent base and should replace the older copy's stale equivalents. Source = recent base unless noted.

| ID | Material | Recent base lines | Target §  | Action |
|----|----------|-------------------|-----------|--------|
| P1 | §1.1 Core Hypothesis & Research Questions (H1–H3, RQ1–RQ4, E1–E20 map) | 27–47 | after §1 problems | ADD (net-new) |
| P2 | 25 meta-types incl. `Saga` + `StateMachine` regroup (14 backend / 11 UI) | 219–243 | §4.1 | REPLACE Definition 1 |
| P3 | Cross-feature edges `R_CF` + Table 3b + Property 4 (Cross-Feature Boundary Discipline) | 247–310 | §4.2/§4.3 | REPLACE (supersedes older E-A/E-B) |
| P4 | Definition 5 Composed Derivation Function + §5.2 cross-feature rules sentence | 346–356 | §5.1/§5.2 | ADD |
| P5 | §6.4 Ashby bound recomputed `log₂(54) ≈ 5.75` | — | §6.4 | REPLACE (follows from 25/29) |
| P6 | §9.1 Model-Theory expansion (Γ⊢φ / M⊨φ, closed-world, Gödel barrier, E9 runs) | 697–703 | §9.1 | REPLACE short version |
| P7 | §9.2 rewrite — composition **resolved** (E9 74.5%→100%) | 705–717 | §9.2 | REPLACE "future work" version |
| P8 | §9.3 SMT / Model-Checking paragraph | 719–723 | §9.3 | ADD |
| P9 | §9.5 two E9-specific threats paragraphs | 735, 739 | §9.5 | ADD |

**Fixes to carry during the port:**
- Prose/count drift in recent base: §4 intro says "three structural properties" but lists **four** → fix to "four".
- Numbering collision: "Definition 5" is reused (recent §5.1 Composed Derivation vs older §6.1 Governance Attenuation). Any merge must renumber.

---

## 2. Dropped-content decisions (older copy has these; recent base cut them)

| ID | Material | Older lines | Verdict |
|----|----------|-------------|---------|
| D1 | §3.1.1 Hard Layer-System Definitions (L-A Layer Set, L-B Track Projection, L-C L7 Orchestration Contract) | 138–182 | **RE-INCORPORATE.** Rigorous, no conflict with recent changes; strengthens §3. (Fix latent typo `au(u)`→`\tau(u)` if kept.) |
| D2 | §4.2 Definition E-A (Edge Family Partition) + E-B (Edge Signature Operator σ) | 282–302 | **PARTIALLY SUPERSEDED.** E-A's 3-way partition is stale (missing `R_CF`); do not re-add verbatim. E-B (σ operator) is optional — re-add only if updated to the 4-family taxonomy. `DEFINITIONS.md` DS-D8 formalizes σ if wanted. |
| D3 | §6.1 Definition 5 Governance Attenuation `A(k)=1−φ(k)` | 478–490 | **OPTIONAL re-add as renumbered Definition.** Still valid; complements §6.3 Corollary 1. Cut likely due to numbering collision. |
| D4 | §1 pointer to `definitions/DEFINITIONS.md` as authoritative contract | 29 | **AUTHOR DECISION.** Re-add only if DEFINITIONS.md remains source of truth (it does — see lane evidence). Recommend keep. |
| D5 | §7.1 "instantiates Definition L-C" sentence | 577 | Keep only if D1 re-incorporated. |

---

## 3. E11 integration plan

**What E11 is:** the MARS/DomainSpec "Technique/Specialization Applicability" experiment. A decision protocol `d(x)` (model **DS-M13**) selecting a technique family + specialization from a symptom taxonomy, over a provisional 24-technique catalog **T01–T24** (Saga T01–T03, Outbox T04, CQRS T05–06, Read Model T07, …, Hexagonal Ports/Adapters T24). DDD-pattern→technique mapping: Outbox=T04, Read Model=T07, Port+Adapter=T24, Saga=T01–T03.

**TRUE evidence grade (do not upgrade):**
- D4 = **go**, but via a **single-human policy override**, not the protocol's dual+third-rater cycle (`E11-D4-decision-packet-2026-04-25.md:24-31`).
- Claim matrix **unchanged by explicit operator decision** (`E11-claim-delta.md` `status_change: none`).
- Canonical C2 status stays **moderate / partially supported (E6, E9 only)**; E11 is listed as *next recommended experiment*, **not** yet a supporting one.
- MARS auditor file is **stale** (still says D4 "no-go / provisional AI") — do not cite MARS-C2 as current.
- The catalog T01–T24 is **provisional**; the 7-step ontology-promotion path is **not executed**.
- Only hard number: execution **reproducibility = 1.000** (process metric, not a domain measurement).

**Where E11 goes (and does NOT go):**

| ID | Material | Target § | Evidence status | Draft |
|----|----------|----------|-----------------|-------|
| E11-1 | DS-M13 validity property (PrecisionF1 ≥ .75 ∧ ApplicabilityRate ≥ .80 ∧ AmbiguityRate ≤ .15 ∧ TradeoffCompleteness ≥ .85) | §4.3 (as a *decision-protocol* property, distinct from §4.1 code-artifact types) | documented (thresholds met once, under override) | see lane draft |
| E11-2 | Technique/Specialization as a **separate axis**, deliberately *not* a meta-type | §4.1 clarifying note | conjectural/documented | "Technique specializations … have no structural code-artifact shape, only decision-protocol shape, governed by DS-M13 rather than the §4.1 ontology." |
| E11-3 | E11 as controlled-experiment exemplar for derivation reproducibility (1.000) | **§9.4 Controlled Experiments** | documented / on-hold | "…demonstrates bundle-scope reproducibility … closure relied on a single-reviewer override, so it is not yet promoted to claim-level support." |
| E11-4 | Adjudication-trace data point (35-row subset, 19 disagreements, all third-rater resolved) | §9.4 (or §6.5 governance-trace) | measured (within bundle) | optional |

**Hard guardrail:** E11 must **NOT** feed §8.2/§8.3/§8.4. Those report the poker-team production case study (different system + methodology). Putting E11 in §8 conflates two evidence bases. E11's honest home is **§9.4 + §4.1–4.3 notes**.

**Contradiction to record:** E11 *sharpens* the §9.5 author-bias threat — the "external" literature survey converged on concepts a third internal source (E11) had already validated, so the independence grade was downgraded **0.90 → ~0.75**. Any claim that E11 provides *independent* corroboration is an overstatement (same repo/author frame).

**Disambiguation:** there are two "E11"s — DomainSpec `E11-technique-specialization` (complete) vs meta-meta `E11 Governance Signal Extraction` (not started). The paper must disambiguate if it cites "E11".

---

## 4. Dispersed empirical additions (research-evidence + vault-ontology lanes)

High-value, **measured** material the paper does not yet fully exploit. All carry a construct-validity caveat — keep the hedges.

| ID | Material | Source | Status | Target § | Note |
|----|----------|--------|--------|----------|------|
| R1 | **E6 vocabulary sufficiency:** 99.87% concept (95% CI [99.25, 99.98]) / 98.96% relationship coverage; 18 domains, 36 features, 747 concepts, 670 rels; 1 strained concept (ReadModel), 1 missing edge (`subscribes`) | `E6-results.md:248-254,293` | **measured** | §9.1, §9.4(c) | Strongest completeness evidence in the repo; currently under-cited |
| R2 | **E9 composition:** 74.5% original-ontology gap (CI [64.8, 82.2]) → 100% extended resolution; 94 edges / 6 domains (117/7 combined) | `E9-run2-rerun-results.md:50-75` | **measured + caveat** | §9.2 | The 74.5% is **rubric-definitional** (edge_type→status); independent run-1 = 47.8%. Cite rerun, footnote circularity |
| R3 | **Saga universality:** 6/6 domains, mean 4.3 contexts → justifies the 25th meta-type | `E9-run2-rerun-results.md:110-120` | **measured** | §4.1 footnote / §9.2 | |
| R4 | **Cross-feature test cardinality:** triggers-cross→3, produces-for→3, enforces-cross→2 obligations/edge | `E9-results.md:148-150` | measured | §5.2 | Concrete derivation-rule detail |
| R5 | **Domain inventories:** 6 multi-BC domains (86 concepts, 94 edges) all classify within the 25 meta-types; no inventory surfaced an uncovered type | `inventory/INVENTORY-INDEX.md:50-59` | documented | §9.1 | Independent corroboration of completeness |
| R6 | **Claim-grade honesty:** only C2 has partial support (E6, E9); C1/C3/C4 insufficient pending E4/E5/E7/E8 | `DOMAINSPEC-EVIDENCE-STATUS.md:9-12` | documented | §9.4/§9.5 | Strengthens the paper's credibility |
| R7 | **Derivation-function gap:** E6/E9 validate the *input space*; whether `f` produces correct tests is untested pending E1/E3 | `E9-results.md:661-663` | documented (gap) | §9.5 | Important honesty bound |

**Ontology reconciliation to preserve (vault lane):**
- Shipped catalogs `TAXONOMY.md` / `RELATIONSHIPS.md` are at **25/29** (matches recent base). ✔
- A design study proposes growing to **~38 edges / 7+4 categories** (Aggregate Root, Repository, Read Model, Outbox, Saga-completing edges) — **PROPOSED, not adopted**; "Adopted" in that doc means *decision recorded*, not catalog-changed. **Do not let §4/§9.1 imply the 38-edge extension is in the vocabulary.**
- E6 (intra-feature) and E9 (inter-feature) coverage are **non-overlapping** — §9.1 must not blend them. Together they bound the proposed extension to 2 meta-types (ReadModel + Saga) + 4 edges (`subscribes` + 3 cross-context).

---

## 5. Formal / Lean additions (formal-theory lane) — high overclaim risk

Only a few results are genuinely `sorry`-free and citable, each with a mandatory hedge. **Recommend: cite sparingly or defer** — the paper currently makes no mechanized-proof claim, and the safest additions are 1–2 narrow, well-hedged sentences.

| ID | Material | Source | Status | Target § | Hedge |
|----|----------|--------|--------|----------|-------|
| F1 | MaxEnt bound `H(p) ≤ log card`, equality iff uniform | `DiscreteEntropy.lean:60,192` | **proved (sorry-free)** | §6.3/§6.4 | Generic inequality only — **NOT** `log₂(54)`, NOT Ashby, NOT channel capacity |
| F2 | Compilation determinism (type-safety leg) | `DomainSpec.lean:159` `T0'_C1` | **proved** | §4.3 | unconditional |
| F3 | Image validity / typing preservation | `DomainSpec.lean:175` `T0'_C2` | **proved but conditional** | §4.3 | conditional on **axiomatized** `EdgeLaw` — not unconditional |
| F4 | Signal/noise partition monotonicity | `SignalNoiseDecomposition.lean:79` | **proved (toy)** | §4.3 | predicate-level toy model, not the typed categorical result |
| F5 | Weak inter-axis independence (V/H/D) | `InterAxisIndependence.lean:95` | **proved (weak)** | §4.3 | strong form build-evidenced but unaudited here |

**Do NOT add (confirmed overclaims):** "Ashby/requisite variety/channel capacity formalized in Lean" (zero Lean hits); "`log₂(54)` mechanically verified"; "governance attenuation is a proved theorem" (operational doc, "math silent on cost"); "attenuation depth is a closed tower bound" (hypothesis-gated); "lake-build-green ⇒ proved".

---

## 6. Integrity flags (existing paper claims the audit could NOT verify)

These are **not additions** — they are existing claims in the base that lack a traceable artifact. Recommend the update resolve or hedge them, since publishing them as-is is a risk.

1. **§6.5 empirical figures** — "23 signals from ~10 pipeline sessions, ~30–40% emission rate." The live `signals.jsonl` is **empty (0 rows)** across all three projects; the "≥60% vs 30–40%" exists only as an **E5 protocol target** (aspirational). E7 (signal emission) is not started. → **Unsupported.** Hedge to "projected/illustrative" or remove pending E7.
2. **§8 case-study counts** — 89 concepts / 445 tests / 146 metrics / verdicts 1·4·1·1 appear **only in the paper's own tables**; no independent experiment artifact or JSONL reproduces them. → Author-tabulated; acceptable as a case study but should be labeled as direct tabulation, not analyzed-experiment evidence.
3. **§9.4 (a)(b)(d)** — backing experiments E2/E4/E5/E10 are **not started**; any sentence implying results exist is unsupported. Only (c) vocabulary sufficiency (E6) is evidenced.

---

## 7. Recommended bounded update shape (tournament result)

Winner: **"E11-integrated refresh."** Adopt the recent base as the research copy, re-incorporate D1 (and optionally D3) from the older copy, layer in the **measured** dispersed evidence (R1–R7) where it strengthens §9.1/§9.2/§9.5, integrate **E11 into §9.4 + §4.1–4.3 notes only**, and resolve the §6.5/§8 integrity flags. Cite Lean (F1–F5) only as 1–2 hedged sentences, or defer.

**Rejected shapes:** *minimal diff-merge* (misses the dispersed measured evidence and E11); *full-evidence-consolidation* (would import unsupported §6.5/§9.4 claims and inflate the paper past its evidence).

---

## 8. Open questions for operator before paper write

1. **Scope of write** — port-base + E11 only, or also fold in R1–R7 dispersed evidence and the §6.5/§8 integrity fixes?
2. **Dropped content** — re-incorporate D1 (Hard Layer-System Definitions)? D3 (Governance Attenuation definition, renumbered)?
3. **Lean** — add hedged F1–F5 sentences, or defer all mechanized-proof claims?
4. **Integrity flags** — hedge/remove the unsupported §6.5 numbers now, or leave for a separate pass?
