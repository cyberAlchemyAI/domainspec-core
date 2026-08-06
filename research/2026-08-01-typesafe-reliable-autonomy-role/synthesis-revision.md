# TypeSafe Custom Role — Reviewer-Reconciled Synthesis

## 1. Selected title and aliases

**Selected title:** Member of Technical Staff, Agent Task Qualification

**Aliases:**

1. Research Engineer, Agent Evals & Environments
2. Autonomy Task Qualification Engineer

“Agent Task Qualification” preserves the task/workflow boundary; “Agent Evals & Environments” supplies the conventional frontier-lab search language. “Member of Technical Staff” is the application target, not an independently evidenced claim about current seniority.

## 2. Organizational posture

**Embedded, not standalone.**

The function should sit within or directly beside Synthetic Data, serving a bounded cross-functional pilot with Product and Platform. It is **BUILD-FROM-OWNED**:

- Synthetic Data retains model evaluation, datasets, grading methodology, and training-intervention authority.
- Product retains task selection, user value, shipped behavior, and release authority.
- Platform/Infrastructure retain runtime reliability, telemetry, root-cause determination, and remediation.
- Agent Task Qualification owns the runnable task environment, task-level evidence, replay, provisional failure routing, and a non-authorizing recommendation.

## 3. Repaired mandate

Build and maintain candidate-authored evaluation environments for one real, recurring, reversible tool-using task, producing replayable and non-authorizing task evidence that helps named Product, Synthetic Data, and Platform owners decide invest, hold, or stop without claiming model-level reliability or exact cross-layer root cause.

## 4. Five technical responsibilities and boundaries

1. **Encode the real task and economic baseline.**  
   Implement its environment, inputs, tool permissions, grading contract, terminal states, and reversible effects. Product owns task value and acceptance semantics; Synthetic Data approves any model-evaluation interpretation.

2. **Write and operate the task runner.**  
   Connect to the actual TypeSafe model and tool interfaces, persist versioned run inputs and outputs, and make incomplete runs distinguishable from failures. Platform owns interface availability and production runtime behavior.

3. **Precommit the experiment.**  
   Before results, record sample size, repetitions, primary task metric, economic threshold, critical failure conditions, and maintenance-cost ceiling with the relevant owners. Synthetic Data owns statistical and model-comparison validity.

4. **Exercise failure and replay paths.**  
   Inject stale input, partial completion, denied tool use, missing telemetry, interrupted execution, and changed-result replay. Classify the likely owning layer with uncertainty retained; the functional owner determines actual cause.

5. **Produce a decision package and conditional regression gate.**  
   Report measured task outcomes, economic signal, review burden, failure evidence, uncertainty, and upkeep. The named owner makes the invest/hold/stop decision. A reusable gate lands only if its measured decision value exceeds its maintenance cost.

Non-scope includes model training, general model evaluation, causal claims about training interventions, production release, customer-product ownership, serving reliability, cluster operations, safety assurance, compliance, and claims of general AI reliability.

## 5. Precise 30/60/90 economic witness

### First 30 days — freeze a real baseline

- Product selects one recurring, economically meaningful, reversible task and names the invest/hold/stop owner.
- The candidate implements a thin runner against the actual model and tool interfaces.
- Product defines the accepted outcome and the economic unit. Precommit:

  `net task value = accepted-output value - inference/tool cost - human review/rework cost - expected failure loss`

- Synthetic Data and the decision owner freeze:

  - baseline window;
  - sample size `N` and repetition policy;
  - primary task metric and threshold `T`;
  - critical effect-boundary failures that force hold;
  - maximum review burden;
  - monthly maintenance ceiling `M`.

- Deliverable: running baseline, versioned task/environment definition, precommitted experiment record, and initial cost measurement—not merely a contract or taxonomy.

### By 60 days — produce falsifiable task evidence

- Run the fixed sample against the agreed baseline and available candidate configuration.
- Exercise at least six failure cases: stale input, partial completion, denied tool use, interrupted execution, missing trace, and nondeterministic retry.
- Measure:

  - accepted completion rate;
  - net task value per attempt;
  - human-review minutes per accepted outcome;
  - false-pass and false-block counts;
  - replay completeness;
  - model/tool/runtime cost;
  - candidate engineering time and projected upkeep.

- Return provisional failure routing with an explicit unknown category. Do not assert exact model, data, product, or infrastructure cause.

### By 90 days — enable one economic decision

- Repeat the task on a time-separated or otherwise precommitted evaluation slice.
- Deliver candidate-authored running code, inspectable traces, failure-injection results, economic comparison, uncertainty, and maintenance estimate.
- The named owner records **invest**, **hold**, or **stop**.
- A reusable gate lands only if all precommitted conditions pass:

  1. primary task metric clears `T`;
  2. no critical effect-boundary failure occurred;
  3. replay completeness clears its threshold;
  4. net decision value is positive under the agreed calculation;
  5. projected upkeep remains at or below `M`.

Failure to meet those conditions is still a valid 90-day witness if it supports a documented hold or stop decision.

## 6. Public-safe capability paragraph

I build bounded, inspectable workflows for AI-assisted tasks: turning ambiguous requirements into runnable checks, preserving the evidence behind outcomes, testing failure and replay behavior, and keeping unresolved decisions visible. At TypeSafe, I would apply that practice to one recurring tool-using task by writing the evaluation environment and runner, measuring its operational and economic behavior, and giving the existing model, product, and platform owners a clear basis for an invest, hold, or stop decision. My focus is task qualification around model use, not frontier-model training, production reliability, or safety assurance.

## 7. Kill and absorb conditions

**Absorb into Synthetic Data or Product if:**

- either team already owns the complete path from environment/grading contract through traces, failure routing, economic decision, and regression gate;
- task specification and traceability are ordinary supporting work inside its existing evaluation stack;
- the only distinct contribution is coordination or documentation.

**Kill the pilot or role hypothesis if:**

- no real recurring reversible task, economic baseline, or actual model/tool interface is available;
- the candidate is not expected to author and maintain running code;
- sample size, thresholds, failure conditions, maintenance ceiling, or decision owner cannot be precommitted;
- the output is only contracts, diagrams, taxonomies, or governance prose;
- the regression gate costs more to maintain than the decisions it improves;
- the role requires frontier-model training, exact causal attribution, production-autonomy ownership, safety assurance, or general reliability claims;
- the application presents Staff seniority as proven without separate professional evidence.

The exact TypeSafe interview question is:

> Who owns the full multi-step tool-use path from environment/grading contract through replayable traces and failure attribution to regression gate, and which parts are outside Synthetic Data/Product?

## 8. Reviewer-concern dispositions

| Reviewer concern | Disposition |
|---|---|
| Rank 1 was not precedent-clean | **Accepted.** Reclassified as BUILD-FROM-OWNED and embedded. |
| Prefer conventional frontier-lab language | **Repaired.** “Agent Task Qualification” is selected; “Agent Evals & Environments” is retained as a conventional alias. |
| Product, Synthetic Data, and Platform ownership was blurred | **Repaired.** Functional authority and non-scope are explicit in every responsibility. |
| Exact ownership question needed | **Accepted verbatim** in the kill/absorb gate. |
| Rank 2 largely duplicates evaluation tooling | **Absorbed.** “Task Specification and Traceability” becomes a supporting responsibility, not a role. |
| Rank 3 resembles TPM/program management | **Killed.** No coordination-led custom role remains. |
| A real recurring reversible TypeSafe task was missing | **Repaired** as the first admission condition. |
| Economic baseline was absent | **Repaired** with a precommitted net-task-value definition and decision threshold. |
| Actual model/tool integration was optional | **Repaired.** The witness requires the real interface. |
| Candidate-authored running code was not mandatory | **Repaired.** Code ownership is a 30-day and 90-day gate. |
| Sample size and thresholds were not precommitted | **Repaired.** `N`, `T`, critical failures, replay threshold, and `M` are frozen before results. |
| Failure injection was underspecified | **Repaired** with six minimum injected conditions. |
| Maintenance cost was ignored | **Repaired.** The gate lands only when decision value exceeds upkeep. |
| Decision authority was vague | **Repaired.** A named Product/leadership owner records invest, hold, or stop. |
| Contracts or taxonomies could masquerade as value | **Killed.** Documentation without running evidence fails admission. |
| “Reliable Autonomy Systems” overstated evidence | **Removed.** Neither “reliable” nor “systems” appears in the selected title. |
| Recommendation could become authorizing | **Repaired.** The output is explicitly non-authorizing. |
| Cross-layer failure classification implied exact cause | **Repaired.** Routing is provisional, preserves unknown, and leaves cause to the owning team. |
| Production autonomy, safety, or general reliability could leak into claims | **Killed** as public claims and placed in non-scope. |
| Public language leaked private names, paths, counts, or maturity | **Repaired.** The public paragraph uses generic capability language only. |
| Staff seniority was not independently proved | **Preserved as a gap.** It is an application target, not biography. |
| Homepage/board hashes were over-broad | **Repaired below.** A capture binds only its exact extracted selector, not roadmap, culture, or unadvertised ownership. |

## 9. Updated exact-binding rows

| Claim ID | Immutable source identity | Exact selector | Source/reference | Evidence scope and proof | Public posture | State |
|---|---|---|---|---|---|---|
| ROLE-01 | Revised synthesis must be persisted and hashed by parent | Sections 1–3 | Reviewer zig-zag loop 1 | Candidate role hypothesis, not a TypeSafe fact | “Proposed role” only | **deferred** until persisted |
| ROLE-02 | Same revised-synthesis identity | Section 2 ownership table | PRECEDENT verdict | BUILD-FROM-OWNED organizational posture | Do not claim TypeSafe accepted this structure | **bound as recommendation** |
| OWN-SD-01 | Exact captured Synthetic Data page/API body hash required | Responsibilities covering datasets, eval/debug tools, evaluation frameworks, and training interventions | TypeSafe Synthetic Data posting; PRECEDENT | Published ownership only; private ownership remains unknown | Public dated fact | **deferred** pending selector-bound capture |
| OWN-PROD-01 | Exact captured Product Engineer page/API body hash required | Responsibilities covering prototype-to-production features, quality, reliability, performance, and instrumentation | TypeSafe Product posting; PRECEDENT | Published ownership only | Public dated fact | **deferred** pending selector-bound capture |
| OWN-PLAT-01 | Exact captured Backend/Platform page/API body hash required | Responsibilities covering inference APIs, serving resilience, uptime, and compatibility | TypeSafe Backend/Platform posting; PRECEDENT | Published runtime ownership only | Public dated fact | **deferred** pending selector-bound capture |
| OWN-UNKNOWN-01 | No public source can bind an absence | Exact interview question in Section 7 | All reviewers | Whether the task-qualification seam is unowned | Must remain a question | **killed as factual claim** |
| CAND-RUN-01 | `sha256:c22dc903041bbc8191624f2458845aa66c56238c4555a3b90b5172eca09d9efd` | Governance-runner `WORK-PACK.md:35-101,139-146` | Prior synthesis ARC-02; explorer 3 | Candidate evidence for bounded running prototypes in synthetic repositories | Generic capability only; omit project name/counts | **bound** |
| CAND-FAIL-01 | `sha256:2390b23c2b1cf726e613629708b9a32fddde12f5abf8d783d7f3c3f5111e7f66` | Fixture report `:1-36` | Prior synthesis ARC-04; explorer 3 | Local failure-first fixtures | Do not imply production behavior | **bound** |
| CAND-REPLAY-01 | `sha256:5f622b2a70ef549f9ae545c0152371032cad1a6a5021a3a74ceae96c0d0da6a9` | Terminal receipt `:8-24` and cited test selectors | Prior synthesis CAV2-02; explorer 1 | Private finite replay/evaluator witness with test-only effects | Generic capability only; omit private name/path/counts | **bound internally** |
| CAND-SPEC-01 | `sha256:03284fe696d2bf982156a8892300438f0a44fa06cc032265773a73682162b26e` | Test-derivation README `:3-50` | Prior synthesis DS-01; explorer 2 | Deterministic source-linked check derivation | Generic capability only; no completeness claim | **bound internally** |
| PUB-CAP-01 | Requires parent claim map binding each sentence to CAND-RUN-01, CAND-FAIL-01, CAND-REPLAY-01, or CAND-SPEC-01 | Section 6, sentence by sentence | CLAIM BOUNDARY verdict | Public capability paragraph | No private names, paths, counts, authority vocabulary, or maturity labels | **deferred** pending claim map |
| WIT-30-01 | Revised synthesis identity after persistence | Section 5, first 30 days | NON-VACUITY verdict | Proposed future experiment, not past accomplishment | Future conditional language only | **bound as proposal** |
| WIT-60-01 | Same | Section 5, by 60 days | NON-VACUITY verdict | Proposed measurements and injections | No reliability or causal-result claim | **bound as proposal** |
| WIT-90-01 | Same | Section 5, by 90 days | NON-VACUITY verdict | Proposed invest/hold/stop witness and upkeep gate | No promise that thresholds will pass | **bound as proposal** |
| ECON-01 | No TypeSafe task evidence yet | `N`, `T`, replay threshold, net-task-value inputs, and `M` | NON-VACUITY verdict | Values must be supplied and frozen with TypeSafe owners | Do not invent numbers in application | **deferred to pilot** |
| SENIORITY-01 | Candidate profile remains self-description; independent source absent | Member-of-Staff experience criterion versus candidate record | CLAIM BOUNDARY and explorer gaps | Seniority is an application target only | No affirmative years/high-performing-team claim | **killed unless independently evidenced** |
| CLAIM-KILL-01 | Prior `research.md` identity `sha256:84068783ce6f81452e48d1ada784b35fbe941a383bc4d706ede9b03e919b091f` | Explorer claim ceilings plus reviewer repairs | All three reviewers | Model reliability, production autonomy, safety, exact root cause, and frontier-training expertise are unsupported | Forbidden public claims | **killed** |
| WEB-SCOPE-01 | Each captured homepage/job-board body hash | Only the exact text selectors extracted from that capture | CLAIM BOUNDARY verdict | Dated public text | Cannot establish culture, private roadmap, absence of an owner, or broader page content | **bound only per selector** |
