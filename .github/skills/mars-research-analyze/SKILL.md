---
name: mars-research-analyze
description: "Analyze raw experiment data through a 10-step empirical analysis pipeline grounded in software engineering research methodology. Transforms JSONL data into validated conclusions, threat assessments, and paper-ready artifacts."
argument-hint: "<experiment-id | --all-completed> [--focus <descriptive|inferential|threats|claims>] [--reanalyze]"
agent: mars-research-analyst
allowed-tools: Read, Write, Bash, Glob, Grep, Fetch, AskQuestions
---

<objective>
Transform raw experiment data into rigorous, reproducible, peer-review-ready conclusions through a structured 10-step analysis pipeline.

This skill exists because:
1. **Analysis determines credibility.** Raw data without proper statistical analysis, threat assessment, and triangulation is anecdotal evidence — insufficient for academic claims at ICSE/FSE/ASE venues.
2. **Reproducibility requires protocol.** Ad-hoc analysis produces different conclusions depending on which statistics the operator chooses to compute. A fixed pipeline ensures every experiment receives the same analytical treatment.
3. **Validity threats are systematic, not ad-hoc.** Wohlin et al.'s four-threat framework (internal, external, construct, conclusion) must be applied methodically — not retroactively after a reviewer flags gaps.
4. **Claim adjudication must be traceable.** Every conclusion that strengthens or weakens a paper claim must trace back through: claim → experiment → data → statistic → threshold → judgment.

Grounded in:
- Wohlin et al. (2012) *Experimentation in Software Engineering* — experiment design and analysis framework
- ACM SIGSOFT Empirical Standards — reporting guidelines for SE venues
- Basili (1996) GQM (Goal-Question-Metric) — structuring measurement
- Runeson & Höst (2009) — case study methodology and triangulation
- Kitchenham et al. (2002) — preliminary guidelines for empirical SE research
</objective>

<flags>
- `--all-completed`: Analyze all experiments with status "completed" in EXPERIMENTS.md.
- `--focus <phase>`: Run only a specific analysis phase (e.g., `--focus threats` runs only Step 8).
- `--reanalyze`: Re-run analysis on an experiment that already has results, producing a delta report.
</flags>

<context>
**Input:**
- `research/projects/domainspec/definitions/DEFINITIONS.md` — canonical term semantics.
- `research/projects/domainspec/definitions/DEFINITIONS-INDEX.md` — definition IDs and lookup map.
- `domainspec/docs/research/data/EX-*.jsonl` — raw experiment data (append-only, never modified).
- `domainspec/docs/research/experiments/EX-*.md` — experiment protocol with success criteria, data schema, and traceability.
- `domainspec/docs/research/EXPERIMENTS.md` — experiment index with status and cross-experiment dependencies.
- `domainspec/docs/research/domainspec-paper.md` — paper claims (C1–C4) and section structure (condensed narrative artifact).
- `domainspec/TAXONOMY.md`, `domainspec/RELATIONSHIPS.md` — meta-model vocabulary (for construct validity checks).

**Output:**
- `domainspec/docs/research/results/EX-results.md` — structured results file (from TEMPLATE.md).
- Updated experiment file (`experiments/EX-*.md`) — Results Analysis section appended.
- Updated `EXPERIMENTS.md` — status change to "completed".
- (Optional) Paper section drafts when results are conclusive.

**Cross-references:**
- `domainspec/docs/research/results/TEMPLATE.md` — output format template.
- `domainspec/docs/research/sources/SOURCE-CATALOG.md` — source quality ratings (for session retrospective).
- Other `results/EX-results.md` files — for triangulation (Step 7).
</context>

<principles>
1. **Empirical honesty.** Report what the data shows. If an experiment weakens a claim, document it and propose revision — never suppress unfavorable results.
2. **Fixed pipeline, adaptive depth.** Every experiment passes through all 10 steps. Steps produce "N/A — insufficient data" rather than being skipped. Depth within each step scales with data volume.
3. **Wohlin's four threats are mandatory.** Internal, external, construct, and conclusion validity must each be explicitly assessed. "No threats identified" is almost always wrong — dig deeper.
4. **Effect sizes over p-values.** For small-sample SE experiments, emphasize practical significance (effect size, confidence intervals) over statistical significance. Report both when possible.
5. **Triangulation requires independence.** Cross-experiment validation only counts when the experiments use different data sources, methods, or operators. Two experiments using the same project data are corroborating, not triangulating.
6. **Claim adjudication is conservative.** Default to "partially supported" unless evidence is overwhelming. "Strongly supported" requires: (a) all success criteria passed, (b) no contradicting subgroup, (c) threats are bounded, (d) triangulation exists.
7. **Definition authority discipline.** Canonical semantics come from `definitions/DEFINITIONS.md`; analysis outputs must reference definition IDs via `definitions/DEFINITIONS-INDEX.md` and flag undefined terms.
</principles>

<process>

## Step 1 — Data Integrity Audit

**Methodology:** Wohlin et al. §11.1 "Data Validation" — verify data completeness and conformance before analysis.

**Actions:**
1. Read raw JSONL from `data/EX-*.jsonl`.
2. **Schema conformance:** Verify every row contains all fields defined in the experiment protocol's data schema. Flag missing or malformed fields.
3. **Completeness check:** Compare row count against protocol expectations (e.g., E6 expects 36 rows = 18 domains × 2 features). Report `actual / expected` with percentage.
4. **Value range validation:** Check numeric fields are within plausible ranges (e.g., coverage ∈ [0, 1], counts ≥ 0). Flag outliers (> 3 IQR from median).
5. **Protocol deviation audit:** Compare actual data collection against the experiment protocol. Document every deviation:
   - Was the execution order changed?
   - Were any steps skipped?
   - Were additional data fields collected beyond the schema?
   - Were any data points re-collected or corrected?
6. **Metadata verification:** Confirm every row has required metadata (experiment_id, run_id, timestamp, domainspec_version, operator).

**Output:** Data Integrity Report — row count, schema violations, range violations, protocol deviations.

**Gate:** If >10% of rows have schema violations, STOP and request data remediation before proceeding.

## Step 2 — Descriptive Statistics

**Methodology:** Standard empirical practice — summarize the data before testing hypotheses. Basili GQM — metrics must trace to goals.

**Actions:**
7. **Central tendency:** Compute mean, median, and mode for all numeric metrics.
8. **Dispersion:** Compute standard deviation, IQR (interquartile range), min, max, range.
9. **Distribution shape:** For each key metric, characterize the distribution:
   - Is it normal, skewed, bimodal, or uniform?
   - Compute skewness and kurtosis if sample size permits (N ≥ 20).
   - For small samples, describe the distribution qualitatively.
10. **Frequency tables:** For categorical variables (e.g., coverage status: covered/strained/uncovered), produce frequency counts and percentages.
11. **Cross-tabulations:** For experiments with two categorical dimensions (e.g., domain tier × coverage), produce contingency tables.
12. **Coverage rates:** Compute ratio metrics defined in the experiment (e.g., concept_coverage = covered / total).
13. **Summary tables:** Produce publication-ready markdown tables with clear column headers, units, and row labels.

**Output:** Summary Statistics section with tables for (a) overall metrics, (b) per-subgroup metrics, (c) distribution summaries.

## Step 3 — Hypothesis Testing (Success Criteria Evaluation)

**Methodology:** Wohlin et al. §11.3 "Hypothesis Testing" — formalize success criteria as testable hypotheses.

**Actions:**
14. **Formalize hypotheses:** For each success criterion in the experiment protocol:
    - $H_0$: The metric does NOT meet the threshold (null hypothesis).
    - $H_1$: The metric meets or exceeds the threshold (alternative hypothesis).
    - Test type: one-tailed (directional) since thresholds are lower/upper bounds.
15. **Point estimate:** Compute the observed value of each metric.
16. **Confidence interval:** For proportions (coverage rates), compute 95% Wilson score interval. For means, compute 95% bootstrap CI (1000 resamples) if sample permits, or exact binomial CI for small N.
17. **Threshold comparison:** Does the entire confidence interval exceed the threshold? Or only the point estimate?
    - **PASS (strong):** Entire 95% CI above threshold.
    - **PASS (marginal):** Point estimate above threshold, but CI lower bound is within 5% of threshold.
    - **FAIL:** Point estimate below threshold.
18. **Effect size:** When comparing against a threshold, compute the gap: observed - threshold. Express as both absolute and relative (percentage points above threshold).
19. **Decision:** For each criterion, record PASS/FAIL with evidence strength.

**Output:** Success Criteria Evaluation table with columns: Criterion | Target | Observed | 95% CI | Effect Size | Status.

## Step 4 — Subgroup Analysis (Cross-Cutting Dimensions)

**Methodology:** Stratified analysis — check whether aggregate results mask subgroup heterogeneity. Simpson's paradox detection.

**Actions:**
20. **Identify natural subgroups:** From the experiment protocol and data schema, identify all categorical dimensions that partition the data (e.g., tier, emphasis type, source category, complexity level).
21. **Per-subgroup statistics:** For each subgroup, compute the same metrics as Step 2.
22. **Cross-group comparison:** For each key metric:
    - Compute the range across subgroups (max - min).
    - Identify the best-performing and worst-performing subgroup.
    - Flag if any subgroup fails a success criterion that passes in aggregate (Simpson's paradox signal).
23. **Variance decomposition:** What fraction of total variance is between-group vs within-group? High between-group variance suggests the aggregate metric is misleading.
24. **Interaction effects:** For experiments with 2+ subgroup dimensions, check for interactions (e.g., does coverage differ by tier differently for workflow-heavy vs data-model-heavy features?).

**Output:** Subgroup Analysis section with per-subgroup tables, cross-group variance, and any Simpson's paradox flags.

## Step 5 — Anomaly & Gap Taxonomy

**Methodology:** Grounded theory-inspired analysis (Strauss & Corbin) — open coding of anomalies, then axial coding into categories, then selective coding into a taxonomy.

**Actions:**
25. **Identify anomalies:** Extract all data points where coverage ≠ 100% or status ≠ "works" (or equivalent non-ideal result). These are the "interesting" data points.
26. **Open coding:** For each anomaly, describe what happened in domain terms. What concept/relationship/edge was strained or broken? Why?
27. **Axial coding:** Group anomalies by common cause. Do they share a pattern? (e.g., "all strained relationships involve async event consumption" or "all uncovered concepts are materialized projections").
28. **Selective coding:** Name each category and assess:
    - **Systematic vs incidental:** Does this gap reflect a fundamental vocabulary limitation, or is it an edge case?
    - **Frequency:** How often does this pattern appear (N occurrences, % of total)?
    - **Severity:** Is it strained (workable but imprecise) or broken (no workaround)?
    - **Remediation:** What would fix it? (new meta-type, new edge type, documentation clarification, protocol change)
29. **Saturation check:** For multi-wave experiments, check if new anomaly categories appeared in later waves. If no new categories after wave 2, taxonomy is saturated.
30. **Gap taxonomy table:** Produce a structured table of all identified gaps with category, frequency, severity, and proposed remediation.

**Output:** Gap Taxonomy section with anomaly classification, pattern clustering, and remediation proposals.

## Step 6 — Sensitivity Analysis

**Methodology:** Robustness checking — would conclusions change under different reasonable assumptions?

**Actions:**
31. **Reclassification analysis:** What if borderline "covered" items were reclassified as "strained"? How many items are within the "judgment zone" where a different operator might classify differently?
32. **Threshold sensitivity:** For each success criterion, what threshold would cause a FAIL? (e.g., "SC-1 passes at ≥85%; the data shows 99.86%; threshold would need to be ≥99.87% to fail"). Report the **margin** = observed - threshold.
33. **Domain removal test:** For each domain/source, remove it and recompute coverage. Does any single domain's removal change a pass/fail? If yes, conclusions depend critically on that domain.
34. **Operator variance estimation:** For experiments with subjective classification (covered vs strained), estimate inter-rater reliability potential:
    - How many classifications are "clear" (unambiguous) vs "borderline"?
    - What would coverage be if all borderline cases went the other direction?
35. **Report fragility:** Rate each conclusion as **robust** (survives all perturbations), **moderate** (survives most), or **fragile** (sensitive to specific assumptions).

**Output:** Sensitivity Analysis section with perturbation results and robustness ratings.

## Step 7 — Triangulation & Cross-Experiment Validation

**Methodology:** Runeson & Höst (2009) — multi-source evidence convergence. Triangulation types: data triangulation (different sources), method triangulation (different methods), observer triangulation (different operators).

**Actions:**
36. **Identify triangulation opportunities:** Which other completed experiments touch the same claim?
37. **Data triangulation:** Do experiments using different data sources (e.g., E6 uses 18 domains, E9 uses poker-team project) reach consistent conclusions about the same claim?
38. **Method triangulation:** Do experiments using different methods (e.g., vocabulary coverage vs composition stress vs derivation determinism) reinforce or contradict each other?
39. **Convergence assessment:** For each claim:
    - **Convergent:** All sources/methods agree → evidence is strengthened.
    - **Complementary:** Sources/methods measure different facets → evidence is broadened.
    - **Divergent:** Sources/methods disagree → evidence is weakened, investigate why.
40. **Cross-experiment findings table:** Map which findings from this experiment reinforce, extend, or contradict findings from other experiments.

**Output:** Triangulation section with cross-experiment comparison table and convergence assessment.

## Step 8 — Validity Threat Assessment

**Methodology:** Wohlin et al. §12 — four categories of validity threats, each must be explicitly assessed.

**Actions:**

### Internal Validity (causal inference threats)
41. Did the experimental design eliminate confounds?
42. Could the operator's domain knowledge bias concept classification?
43. Were there order effects (e.g., later domains analyzed faster/differently than early ones)?
44. Were there maturation effects (operator's skill improved during the experiment)?

### External Validity (generalizability threats)
45. Is the domain sample representative? What domains/industries are missing?
46. Would results generalize to domains with different characteristics (e.g., highly regulated, real-time, ML-heavy)?
47. Is there a DDD bias? (Most sources are DDD-informed; would non-DDD domains produce different results?)
48. Would results hold with a different DomainSpec version?

### Construct Validity (measurement threats)
49. Does "concept coverage" actually measure what we claim it measures?
50. Is the covered/strained/uncovered trichotomy well-defined? Could two operators classify the same concept differently?
51. Are there domain concepts that the experiment design systematically misses (e.g., non-functional requirements, UI concepts, operational concerns)?

### Conclusion Validity (statistical threats)
52. Is the sample size sufficient for the claimed precision? (e.g., 99.86% from N=738 has a different CI than from N=10)
53. Are the success criteria thresholds well-calibrated? (e.g., ≥85% might be too easy; ≥99% might be too strict)
54. Could multiple comparisons inflate apparent success? (testing 6 criteria simultaneously)

**Output:** Validity Threat Assessment section organized by the four categories, each with specific threats identified and mitigation strategies.

## Step 9 — Claim Adjudication

**Methodology:** Evidence-to-claim mapping with structured strength assessment.

**Actions:**
55. **Identify affected claims:** Which paper claims (C1–C4) does this experiment provide evidence for?
56. **Resolve definition anchors:** For each claim finding, map terms to canonical definition IDs from `definitions/DEFINITIONS-INDEX.md`; flag any undefined or ambiguous terms as remediation items.
57. **Evidence mapping:** For each claim, list:
    - Supporting evidence from this experiment (specific findings, metrics).
    - Contradicting evidence (if any).
    - Evidence from other experiments (from Step 7 triangulation).
58. **Evidence strength rating:** Apply this rubric:

| Rating | Criteria |
|--------|----------|
| **Strong** | All success criteria passed with margin, no contradicting subgroups, threats are bounded, triangulation exists |
| **Moderate** | Most criteria passed, minor subgroup variance, threats identified but bounded |
| **Weak** | Criteria marginally passed, significant threats, no triangulation |
| **Insufficient** | Experiment not yet complete or key criteria not testable |
| **Contradicted** | Evidence actively contradicts the claim |

59. **Claim status update:** For each affected claim, produce:
    - Current status: supported / partially supported / insufficient evidence / contradicted.
    - What would change the status? (additional experiments, more data, revised claim wording).
60. **Recommended claim revisions:** If evidence contradicts or partially supports a claim, propose revised wording that the evidence does support.

**Output:** Claim Adjudication section with evidence mapping, strength ratings, status, and revision recommendations.

## Step 10 — Synthesis & Paper Integration

**Methodology:** Consolidate all analysis phases into publication-ready artifacts.

**Actions:**
60. **Produce results file:** Create `results/EX-results.md` from TEMPLATE.md, incorporating outputs from Steps 1–9.
61. **Update experiment file:** Append a `## Results Analysis` section to `experiments/EX-*.md` with:
    - Aggregate coverage tables (from Step 2).
    - Success criteria evaluation (from Step 3).
    - Identified gaps and their categories (from Step 5).
    - Claim impact summary (from Step 9).
    - Recommended paper actions (from Step 9).
62. **Draft paper sections:** When results are conclusive, draft or revise the relevant paper section:
    - Use academic tone — precise, concise, evidence-backed.
    - Use KaTeX for equations: inline `$...$`, display `$$...$$`.
    - Include data tables with clear column headers and units.
    - Use numbered references `[N]` matching the paper's References section.
63. **Definition consistency check:** Ensure any revised wording remains aligned with canonical definitions; if semantics changed, request updates to `definitions/DEFINITIONS.md` and `definitions/DEFINITIONS-INDEX.md` before paper edits.
64. **Update experiment status:** Mark the experiment as "completed" in EXPERIMENTS.md.
65. **Session retrospective:** Record analysis learnings:
    - Which analysis steps produced the most insight?
    - Were any steps unnecessary for this experiment type?
    - What would improve the pipeline for next time?
    - Update `sources/SOURCE-CATALOG.md` with evidence quality ratings if applicable.

**Output:** Complete results file, updated experiment file, optional paper section draft, updated experiment status.

</process>

<analysis-method-selection>

Not every experiment needs every statistical technique. Use this decision tree to select the right methods per experiment type:

### Coverage Experiments (E6-style: "does X cover Y?")
- **Primary:** Proportion analysis, Wilson score CI, coverage-by-subgroup
- **Secondary:** Gap taxonomy (grounded theory coding), saturation check
- **Sensitivity:** Reclassification analysis, domain removal test
- **Typical finding shape:** "X% coverage (95% CI: [a, b]), N gaps clustering into K categories"

### Comparison Experiments (E2-style: "is X better than Y?")
- **Primary:** Paired comparison (Wilcoxon signed-rank for small N, t-test for larger N), effect size (Cohen's d or Cliff's delta)
- **Secondary:** Per-feature comparison, coverage delta distribution
- **Sensitivity:** Threshold sensitivity, feature removal test
- **Typical finding shape:** "X outperforms Y by Z% (effect size d=W, 95% CI: [a, b]), significant in P/Q subgroups"

### Determinism Experiments (E1-style: "is output consistent?")
- **Primary:** Agreement metrics (Fleiss' kappa, Krippendorff's alpha), edit distance
- **Secondary:** Per-run deviation analysis, convergence check
- **Sensitivity:** Temperature sensitivity, prompt perturbation
- **Typical finding shape:** "Agreement κ=X across N runs, Y% exact match, deviations cluster in Z"

### Trend Experiments (E7/E8-style: "does metric improve over time?")
- **Primary:** Time series analysis (trend detection, moving average), regression (linear or logistic)
- **Secondary:** Change point detection, convergence test (is the series approaching a limit?)
- **Sensitivity:** Window size sensitivity, outlier removal impact
- **Typical finding shape:** "Metric decreased from X to Y over N sessions (slope=Z, R²=W), converging toward target T"

### Stress Test Experiments (E9-style: "where does X break?")
- **Primary:** Failure mode analysis, edge classification distribution
- **Secondary:** Composition algebra proposal, remediation impact estimation
- **Sensitivity:** Classification boundary sensitivity, domain removal test
- **Typical finding shape:** "N/M edges work (X%), failures cluster into K patterns, K proposed extensions resolve all failures"

### Productivity Experiments (E10-style: "does X make developers faster/better?")
- **Primary:** Between-group comparison (Mann-Whitney U), task completion rates, time metrics
- **Secondary:** Qualitative coding of developer behavior, learning curve analysis
- **Sensitivity:** Participant removal, task difficulty variation
- **Typical finding shape:** "Group A completed X% more tasks in Y% less time (U=Z, p=W, effect size r=V)"

</analysis-method-selection>

<output-contract>

### Complete analysis output:

```
## Experiment EX — Analysis Report

### Step 1: Data Integrity
- Rows: actual / expected (%)
- Schema violations: N
- Protocol deviations: [list]
- Gate: PASS / BLOCKED

### Step 2: Descriptive Statistics
[Summary tables — overall, by subgroup, distributions]

### Step 3: Hypothesis Testing
| Criterion | Target | Observed | 95% CI | Effect Size | Status |
|-----------|--------|----------|--------|-------------|--------|

### Step 4: Subgroup Analysis
[Per-subgroup metrics, cross-group variance, Simpson's paradox check]

### Step 5: Gap Taxonomy
| Category | Pattern | Frequency | Severity | Remediation |
|----------|---------|-----------|----------|-------------|

### Step 6: Sensitivity Analysis
| Perturbation | Original Result | Perturbed Result | Conclusion Stable? |
|-------------|-----------------|-----------------|-------------------|

### Step 7: Triangulation
| Experiment | Finding | Relation | Convergence |
|-----------|---------|----------|-------------|

### Step 8: Validity Threats
- Internal: [threats + mitigations]
- External: [threats + mitigations]
- Construct: [threats + mitigations]
- Conclusion: [threats + mitigations]

### Step 9: Claim Adjudication
| Claim | Evidence Strength | Status | Revision Needed? |
|-------|------------------|--------|-----------------|

### Step 10: Synthesis
- Results file: results/EX-results.md
- Experiment file: updated with Results Analysis
- Paper action: [none | revise §N | add data to §N]
- Session learnings: [what improved the pipeline]
```

### Abbreviated output (for --focus runs):

Only the requested step's output plus a one-line summary of implications for adjacent steps.

</output-contract>
