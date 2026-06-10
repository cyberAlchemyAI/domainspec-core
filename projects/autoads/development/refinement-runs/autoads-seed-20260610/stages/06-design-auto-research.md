# Stage 6 — Design: Auto-Research Component

- **Role:** auto-research (candidate research & feedback loop design)
- **Receipt:** native-stage design · **verdict: pass**

---

## 1. What Auto-Research Researches & Sources

**Sources (governed source classes):**

1. **Internal residue** [SB]: retired/promoted patterns + low-veracidade observations from prior cycles; mined from the Promotion DAG edges `retired_by`, `drifts_from`, `contradicts`. [adapt] **Internal sources are trusted residual evidence.**
2. **Competitor creatives** [H]: external creative samples labeled by observed ad network (platform, format, audience); ingested as `ExternalSignal` nodes with `veracidade: low` until validated. **External sources are protected context, never auto-trusted.**
3. **Trend signals** [H]: seasonal patterns, platform best-practices (e.g., short-form video lift in Q1), audience segment shifts from industry benchmarks. Captured as `ExternalSignal` with author/recency/confidence metadata. **Require owner approval before use.**

**Governance gate:** External signals enter as candidates only after redaction/generalization (rule GQ-PR-L0-006 [SB]); no proprietary competitor data or client-identifying trends bypass review.

---

## 2. Creative Hypothesis Candidate Object

A researched candidate is a `PromotionCandidate` [SB DAG node N4] shaped for creatives:

```
CreativeHypothesisCandidate {
  hypothesis_statement: str          # e.g., "Short-form video drives 15% higher CTR in Gen-Z audience"
  rationale: str                      # Why now: residue signal + market trend
  source_refs: List[{                 # Audit trail
    kind: "internal_residue" | "external_trend" | "competitor_pattern"
    ref_path: str                     # Edge ID, signal record, or trend name
    confidence: "high" | "medium" | "low"
  }]
  predicted_lift: Optional[float]    # Expected KPI movement; null if unquantified
  ontology_card_target: str          # Which ontology card this would parameterize
  target_window: str                 # Response window for validation (e.g., "7d")
  veracidade: str                    # "high" (prior validated), "medium" (theory), "low" (speculative)
  evidence_refs: List[str]           # Non-empty iff veracidade=high; links to prior runs
  proposed_allowed_uses: str         # Scope: this audience only, test budget, etc. [SB GQ-PR-L0-011]
  contradiction_path: str            # How this could be wrong [SB GQ-PR-L0-004]
}
```

**Entry into pipeline:** A candidate flows directly into the Promotion DAG's `PromotionCandidate` queue, subject to the full review→decision→promote sequence. **No candidate skips the review gate.**

---

## 3. Governance Gate: Candidate → Reviewed → Admitted

**Gate sequence** [SB adaptation of DAG-AND-METRICS §4, step 4–6]:

1. **Candidate proposed** → auto-research emits `CreativeHypothesisCandidate` with all fields above.
2. **Privacy redaction** → if any source_ref is external/competitor, apply generalization (rule GQ-PR-L0-006 [SB]). Block if irreducibly client-identifying.
3. **Deterministic pre-gate** → reject if `contradiction_path` is empty or `proposed_allowed_uses` is unspecified (rules GQ-PR-L0-004, -011 [SB]).
4. **Owner review** → human reviews hypothesis, rationale, and source credibility. No auto-promotion pathway exists [SB metric≠authority].
5. **OwnerDecision** [SB node N5] → approved, rejected, or strategic-bet override (if `veracidade: low` with explicit rationale).
6. **Promotion pathway** → approved candidate becomes a `KnowledgeProjection` [SB node N6] parameterizing the Generator's ontology card.

**Blocks:** Candidates with unresolved `contradicts` edges (DAG-AND-METRICS §3 contradiction gate [SB]) are routed to decision with flagged path, not silently rejected.

---

## 4. Closed Loop: Outcomes Feed Auto-Research Memory

**Feedback mechanism** [SB ontologize improvement loop, adapted]:

1. **Measure outcome** → a creative cycle produces `MetricObservation` (CLC) with `veracidade` + `evidence_refs`.
2. **Grade & compare** → Grader assigns confidence; compare actual lift vs predicted_lift from the originating candidate.
3. **Mine residue** → if lift > predicted (outperformance) or if `drifts_from` edges appear:
   - Outperformance → candidate gets promoted + residue feeds auto-research as high-confidence internal source.
   - Drift → candidate gets low-veracidade refinement added to the residue pool for next cycle.
4. **Underperformance / contradiction** → if actual lift < threshold or contradicts prior pattern:
   - Candidate moves to `contradicted` state (no silent stale patterns).
   - Contradiction path is preserved (rule GQ-PR-L0-004 [SB]); auto-research is blocked from re-proposing the same hypothesis without new evidence.

**Memory structure:** The residue pool is the `(drifts_from, contradicts, promoted_from)` edges in the Promotion DAG — these are queryable, evidence-linked, and feed the next auto-research cycle.

---

## 5. Exploration vs. Exploitation Guardrail

**Overfitting risk:** Auto-research could repeatedly propose variations of recent winners, starving exploration.

**Mitigation** [H hypothesis]:
- **Promotion-weighted decay:** A promoted candidate decreases in internal-source weight after N successive uses (e.g., 3 cycles). Re-proposing the same candidate requires new external or drift-based rationale.
- **Residue diversity budget:** Auto-research allocates exploration quota: 60% from validated residue, 40% from untested external signals or low-confidence internal patterns. This forces periodic re-evaluation of assumptions.
- **Contradiction as teacher:** A contradicted pattern is mined for *why* it failed, not erased — the contradiction path becomes a guardrail for future hypothesis generation.

**Owner override:** Any strategic bet (brand consistency, audience expansion) overrides decay; owner decision is the final arbiter.

---

## Residue

1. **Auto-research triggering policy:** On-demand (per creative brief) vs. periodic batch (after N cycles or one quarter)? Decision in assessment (S5).
2. **Trend-signal governance:** Who authorizes external sources (industry benchmarks, platform advisories)? Single owner or category-scoped approvers? Implementation in Pilot.

---

## Citations

- **[SB]** `projects/ontologize/DAG-AND-METRICS.md` (node types N1–N6, edges, rules GQ-PR-L0-001 through -011, improvement loop)
- **[SB]** `projects/ontologize/OPTIMIZATION-CHAIN-METHOD.md` (analysis→BI chain structure, claim-label bounds)
- **[adapt]** `projects/autoads/development/refinement-runs/autoads-seed-20260610/stages/05-distill.md` (Creative Learning Cycle, auto-research pool)
- **[adapt]** `projects/autoads/development/refinement-runs/autoads-seed-20260610/stages/02-define.md` (ontologize binding, evidence-linked KPIs, governance register)

