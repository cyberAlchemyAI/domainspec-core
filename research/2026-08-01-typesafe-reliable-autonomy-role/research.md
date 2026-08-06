# TypeSafe Reliable Autonomy Role — Verbatim Research Returns

## Agent 1 — Wiener, Norbert / CAV2 Reliability Explorer

## Explorer verdict

The strongest defensible capability is not frontier-model reliability research. It is designing and testing the decision infrastructure around AI systems: bounded authority, explicit abstention/escalation, challenge handling, deterministic routing, replay, drift invalidation, and human-controlled effects.

That could serve TypeSafe’s stated interest in real-world reliability and autonomy, but only if attached to a concrete model-driven workflow and measurable failures. A role consisting mainly of governance documents would be too weak.

Proof-posture key:

- **Canonical authority:** active project-local rule or definition; not runtime proof.
- **Verified local witness:** executable bounded implementation with tests or receipts.
- **Accepted research:** reviewed synthesis; not authority or implementation.
- **Candidate design/intended behavior:** specified target without full execution evidence.
- **Absent:** no repository evidence.

## Exact-bound matrix

| Candidate capability | TypeSafe need it could serve | Exact source | Proof posture | Concrete role responsibility | First-90-day deliverable | Public-safe phrasing | Forbidden overclaim |
|---|---|---|---|---|---|---|---|
| Evidence-bounded authority and claim discipline | Keep model output, eval results, consensus, and successful executions from silently becoming production authority | `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md:23-46`, `:74-88`, `:122-133`; `authority/definitions/DEFINITIONS.md:2434-2482` (`CAV2-D38`) | **Canonical local authority.** Operational enforcement is review-first; deterministic authority-kind scanning remains pending at `AUTHORITY-MODEL.md:63-69,144-159`. | Define what may authorize a consequential workflow decision, which evidence supports it, who owns exceptions, and what wording each result permits. | For one economically valuable workflow, publish an internal claim/evidence map, decision-owner map, negative controls, and an executable admission checker whose failures route to a named human. | “I design AI-assisted workflows where claims, evidence, decisions, and owner boundaries remain explicit and testable.” | “I solved AI authority”; “production governance platform”; “formal assurance of model truth”; “compliance guaranteed.” |
| Challengeability and retained human responsibility | Make autonomous recommendations contestable and prevent confidence or agent agreement from replacing accountable judgment | `authority/definitions/DEFINITIONS.md:2559-2618` (`CAV2-D40`); `development/agent-reasoning-engine/spec/SPEC.md:241-259,274-285` | **Canonical challenge contract plus candidate engine design.** The evaluator has challenge fixtures, but there is no general empirical proof that bias is detected or reduced. | Specify material challenge lanes, defeaters, timeout behavior, blocking questions, escalation owners, and the decision retained by humans. | Add a shadow-mode challenge suite to one TypeSafe automation path: disagreement, missing evidence, timeout, conflict, and owner-unavailable cases, with measured false blocks and missed escalations. | “I build reviewable AI decision paths that expose disagreement, missing evidence, and escalation points.” | “Bias-cancelling engine”; “consensus proves correctness”; “human oversight solved”; “safe autonomous agents.” |
| Deterministic intent-to-capability routing without execution authority | Route ambiguous user or operator intent to appropriate tools/workflows while preserving uncertainty and preventing accidental action | `development/agent-reasoning-engine/intent-route-resolver/define/SPEC.md:20-42,160-200`; `implementation/.../intent-route-resolver/generated/runs/.../receipt.json:2-30`; browser receipt `:2-17` | **Verified private L0 local witness.** Fresh run: **34/34 tests passed**. Materialized receipt records 17 Node/Chromium cases with main/worker parity and `authority_effect: none`. No natural-language, host, approval, execution, or product witness. | Build the typed seam between model-produced intent projections and an owner-supplied capability catalog; return candidate, ambiguity, no-match, or invalid, never permission. | Integrate a shadow resolver into one internal workflow; freeze the catalog, test ambiguous/no-match cases, compare model projection with human labels, and prove zero execution from advisory output. | “I’ve built bounded prototypes that turn structured intent into deterministic, non-authorizing route recommendations and typed ambiguity.” | “Production intent router”; “understands natural language reliably”; “autonomous orchestration”; “portable across all runtimes.” |
| Finite semantic evaluation with abstention, defeat, escalation, and exact-effect separation | Convert evidence under a frozen rule/catalog state into inspectable outcomes while preventing weak or stale evidence from producing action | `development/agent-reasoning-engine/spec/SPEC.md:127-191,215-239`; promotion receipt `decisions/g-are-l0-promotion/PROMOTION-RECEIPT.json:20-47`; package README `implementation/.../semantic-judgment-evaluator/README.md:1-11` | **Explicitly promoted private finite L0 witness.** Fresh run: **16/16 tests passed**. Two rule families, typed counterfactuals, persisted ordering, and a test-only effect boundary. Whole engine, actor runtime, real effects, ACI conformance, and anti-bias efficacy are absent. | Own a model-agnostic decision-evaluation harness for one bounded production-relevant conclusion, including insufficient, defeated, invalid, drifted, and owner-escalation outcomes. | Build one falsifiable “model recommendation to real-work decision” specimen: frozen evidence, two independently authored rule families, counterfactual mutations, abstention criteria, exact-effect gate, and human acceptance review. | “I’ve implemented a bounded, replayable evaluator that returns typed recommendations, abstentions, defeats, invalidations, and owner escalations under frozen inputs.” | “General reasoning engine”; “AI judgment is correct”; “real effects safely automated”; “frontier-model reliability demonstrated.” |
| Replay, temporal revalidation, persistence-before-effect, and idempotent recovery | Diagnose incidents, reproduce prior decisions, distinguish historical correctness from current validity, and prevent duplicate or partially recorded effects | `implementation/.../semantic-judgment-evaluator/test/evaluator.test.mjs:246-330,332-405`; `test/store.test.mjs:12-43`; terminal receipt `generated/runs/evaluator-v1-.../TERMINAL-RECEIPT.json:8-24` | **Verified local fixtures.** Historical replay is byte-identical with zero provider/effect calls; expiry can invalidate current state; persistence failure stops before effect evaluation; repeated test delivery is idempotent. Only a test double is exercised. | Define audit/recovery semantics for model-assisted decisions: immutable inputs, replay versus revalidation, incomplete-run handling, drift invalidation, and idempotency conflicts. | Instrument one workflow with decision receipts and a replay tool; run injected expiry, revocation, persistence-failure, duplicate-delivery, and changed-content scenarios; produce an incident-review report. | “I design replayable decision workflows that preserve inputs, expose drift, fail before effects when records are incomplete, and test duplicate-delivery behavior.” | “Production incident recovery proven”; “exactly-once effects”; “distributed durability”; “real-provider fault tolerance.” |
| Bounded formal counterexamples and structural-law witnesses | Test whether a proposed reliability rule actually expresses the system property it claims to protect | `domainspec-lean-formalization/lean-engineer/cav2-governance/GovernsAcyclicity.lean:18-35,64-72,96-140`; `.../categorical-deep-learning.../witness/ParametricMapWitness.lean:5-20,34-97,136-184`; accepted research `cyberAlchemy-v2/development/research/2026-07-23-categorical-deep-learning-algebraic-architectures/findings.md:74-116,172-207` | **Machine-checked bounded witnesses plus accepted research.** The graph witness shows unary lints cannot express acyclicity. The categorical witness covers low-level reparameterization laws and finite Boolean fixtures only. No neural semantics, G.10, architecture universality, empirical benefit, or fresh Lean compilation was performed in this action. Personal/sole authorship is not established; the graph file explicitly credits a collaborator. | Work with research and infrastructure teams to turn one reliability assumption into a precise property, positive/negative fixtures, and—where proportionate—a small formal counterexample or proof. | Select one failure-prone interface contract, demonstrate a case where local checks pass but the global property fails, then add the smallest executable or formal cross-check. | “I use bounded formal witnesses and counterexamples to test specific system assumptions, alongside collaborators.” | “I formally verified neural architectures”; “proved model safety”; “all architectures”; “I authored every cited proof”; “formal methods guarantee production reliability.” |

## Strongest integrated 90-day witness

The rows compose into one credible deliverable:

1. Select one real TypeSafe model-assisted workflow with a consequential but reversible downstream decision.
2. Freeze the intent, authority/catalog state, evidence handles, and exact effect.
3. Run a shadow evaluator that can recommend, abstain, defeat, invalidate, or escalate.
4. Attach challenge cases and counterfactual mutations.
5. Persist the receipt before any effect gate.
6. Demonstrate historical replay, current-state revalidation, persistence failure, drift, and duplicate-delivery behavior.
7. Have the actual decision owner determine whether the witness reduced missed failures or merely added friction.

Success must be measured through defect discovery, reproducibility, escalation usefulness, and operational cost—not by the existence of a framework.

## Contradictions and gaps

- The private product philosophy speaks of deciding, acting, recovering, and retaining human agency, but it is explicitly a **candidate proposition**, not evidence of delivered end-to-end behavior (`VALUE-AND-PHILOSOPHY-PROPOSITION.md:3-16,99-106`).
- The reasoning-engine specification is much broader than its implementation. Only the finite evaluator slice is promoted; the actor runtime, real effect adapter, integrated journal, production durability, and whole-engine admission remain absent.
- The authority model is active local authority, but several enforcement mechanisms remain review-mode or pending. It supports disciplined system design, not a claim that governance has been automated.
- The route resolver demonstrates typed structured-input behavior and browser-runtime parity, not natural-language understanding, product integration, approval semantics, or execution.
- The categorical ML work demonstrates careful reading and a narrow Lean foothold. It supplies no frontier-model architecture, training, inference, synthetic-data, empirical safety, or trained-weight result.
- Nothing inspected establishes production-ML ownership, distributed training, GPU/kernel work, model architecture research, large-scale eval infrastructure, customer deployment, or reliability improvement on TypeSafe models.
- Repository artifacts establish team/project evidence more strongly than individual authorship. The candidate profile supplies leadership claims, but it is self-description; public claims should use “led,” “worked on,” or “with collaborators” only when separately supportable.
- TypeSafe’s public mission and openings were supplied in the frozen candidate profile but were not re-opened in this lane. Employer-specific ownership remains an inference pending the live-source explorer.
- Central non-collapse: **workflow/system reliability controls the conditions under which model output becomes work; it does not improve model weights or prove frontier-model reliability.** The credible role must interface with model researchers and evaluate behavior in real workflows, not present process governance as a substitute for model research.

## Role-name fragments

Not final titles:

- **Reliable Autonomy Systems**
- **Decision Infrastructure & Evaluation**

```json
{
  "status": "pass",
  "dispatch_id": "2026-08-01-typesafe-reliable-autonomy-role-route",
  "run_id": "typesafe-role-run-001",
  "action_id": "spawn-0001",
  "started_at": "2026-08-01T04:09:30Z",
  "finished_at": "2026-08-01T04:16:00Z",
  "artifacts_actually_read": [
    "research/2026-08-01-typesafe-reliable-autonomy-role/orchestration/run-001/actions/spawn-0001.json",
    "research/2026-08-01-typesafe-reliable-autonomy-role/dispatch-sheet.json",
    "research/2026-08-01-typesafe-reliable-autonomy-role/candidate-profile.md",
    "research/2026-08-01-typesafe-reliable-autonomy-role/strategy-inventory-packet.json",
    ".arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md",
    ".arcanum/inventory/queries/2026-07-06-spec-driven-completeness-moat-inventory-research/findings.md",
    ".arcanum/inventory/entries/agent-reasoning-engine-contract-strategy-result-synthesis.md",
    ".arcanum/inventory/entries/categorical-deep-learning-cav2-lean-tower-strategy-result-synthesis.md",
    "cyberAlchemy-v2/README.md",
    "cyberAlchemy-v2/VALUE-AND-PHILOSOPHY-PROPOSITION.md",
    "cyberAlchemy-v2/authority/AUTHORITY-MODEL.md",
    "cyberAlchemy-v2/authority/promotion-policy.md",
    "cyberAlchemy-v2/authority/definitions/DEFINITIONS.md",
    "cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md",
    "cyberAlchemy-v2/validation/README.md",
    "cyberAlchemy-v2/development/agent-reasoning-engine/spec/SPEC.md",
    "cyberAlchemy-v2/development/agent-reasoning-engine/decisions/g-are-l0-promotion/PROMOTION-RECEIPT.json",
    "cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/semantic-judgment-evaluator/README.md",
    "cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/semantic-judgment-evaluator/test/evaluator.test.mjs",
    "cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/semantic-judgment-evaluator/test/store.test.mjs",
    "cyberAlchemy-v2/implementation/agent-reasoning-engine/generated/runs/evaluator-v1-20260723T-session-001/TERMINAL-RECEIPT.json",
    "cyberAlchemy-v2/development/agent-reasoning-engine/intent-route-resolver/define/SPEC.md",
    "cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/intent-route-resolver/addon-manifest.json",
    "cyberAlchemy-v2/implementation/agent-reasoning-engine/generated/runs/intent-route-resolver-v1-20260730T213000Z/receipt.json",
    "cyberAlchemy-v2/implementation/agent-reasoning-engine/generated/runs/intent-route-resolver-v1-20260730T213000Z/browser-receipt.json",
    "cyberAlchemy-v2/development/research/2026-07-23-categorical-deep-learning-algebraic-architectures/findings.md",
    "domainspec-lean-formalization/research/categorical-deep-learning-algebraic-architectures/witness/ParametricMapWitness.lean",
    "domainspec-lean-formalization/lean-engineer/cav2-governance/GovernsAcyclicity.lean",
    "cyberAlchemy-v2/development/refinement-runs/20260629-cav2-row2-solver-trust-base/NEXT-STEPS.md",
    "cyberAlchemy-v2/development/refinement-runs/20260629-cav2-row2-solver-trust-base/RESULT.md",
    "/home/vrondelli/.codex/memories/MEMORY.md"
  ],
  "validation": [
    "semantic-judgment-evaluator: node --test, 16 passed, 0 failed",
    "intent-route-resolver: node --test, 34 passed, 0 failed",
    "repository remained unmodified by this explorer",
    "Inventory used only for navigation; substantive claims rebound to live source artifacts"
  ],
  "blockers": [
    "TypeSafe live pages were not assigned to this lane and require independent current verification",
    "no production or frontier-model reliability evidence",
    "personal authorship and individual contribution are not fully attributable from repository artifacts",
    "formal witnesses were not freshly compiled in this read-only action"
  ]
}
```

## Agent 3 — Simon, Herbert / Arcanum and TypeSafe Fit Explorer

## Explorer verdict

**PASS, with a conditional role hypothesis.**

The strongest defensible role is **Member of Technical Staff, Reliable Autonomy Systems**: own the qualification layer between a promising model capability and one inspectable, repeatable, decision-ready real-world autonomy trial.

This role should not own model training, synthetic-data pipelines, customer product, inference serving, infrastructure, or developer advocacy. It owns the task contract, executable end-to-end trial, replayable trace, cross-layer failure classification, and evidence used by those owners to decide what changes next.

This is an inferred need, not a known TypeSafe roadmap gap. If TypeSafe’s Synthetic Data or Product teams already own end-to-end tool-use/autonomy qualification, the custom-role hypothesis should be **KILL or absorbed into that team**, not preserved for novelty.

## Exact internal evidence matrix

| Candidate capability | Exact evidence | Proof posture | Relevant responsibility | Claim ceiling |
|---|---|---|---|---|
| Intent → definition/design/plan/handoff | `arcanum/README.md:148-161`; `arcanum/spells/invoke/README.md:20-26,34-76,98-115` | Define, design, plan, handoff, and refresh have implemented contracts. Composite `full` and lifecycle `validate` remain deferred. | Turn an ambiguous autonomy use case into a bounded task definition, evaluation surface, work pack, and named owner handoffs. | “Built structured research and planning workflows”; not “fully automated research-to-production lifecycle.” |
| Bounded execution with validation and synchronized closeout | `arcanum/arcana/task-session/README.md:3-18,39-70,129-161,224-260` | Stable execution contract with strict context, mutation admission, acceptance-critical validation, and separate owner closeout. | Execute one qualification slice without allowing apparent task success to imply release or owner acceptance. | Repository-local execution machinery; no production-scale evidence. |
| Recent working governance-runner prototype | `arcanum/arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/WORK-PACK.md:35-101,139-146` | SWU-TSGR-001 through 007 passed exact positive/negative/schema matrices. Executor join, replay, reconciliation, interruption recovery, atomic apply, and owner-hook paths are witnessed in synthetic repositories. SWU-008 is correctly blocked by a missing external owner-readiness receipt. | Build the trial runner and prove failure behavior before connecting it to live model/product effects. | “Working synthetic prototype through seven bounded units”; not end-to-end readiness, release, or production use. |
| Capability-bound multi-agent control | `arcanum/formulae/dispatch-spec/README.md:50-62,136-172`; `arcanum/runtime/orchestrate/SKILL.md:59-68,77-141` | Dispatch Spec remains labeled a draft package, but deterministic route validation, persisted native actions, joins, identity checks, timeout recovery, and dependency withholding are implemented contracts. | Coordinate parallel investigation or evaluation lanes while retaining exact input, output, owner, and join boundaries. | Not a general autonomous-agent platform. |
| Native success/failure canary | `arcanum/formulae/dispatch-spec/development/runtime-integration/20260722T063407Z-native-host-canary/RESULT.md:1-11` | Bounded canary demonstrated failure-first withholding and later all-pass progression through a dependent Task Session worker. Explicitly limited to one native host run. | Make failed evidence prevent downstream work rather than letting partial consensus advance. | One bounded host witness, not universal runtime behavior. |
| Fail-closed autonomous work routing | `arcanum/spells/goal/README.md:10-17,82-108,144-171`; `arcanum/spells/goal/validation/results/fixture-report.md:1-36` | Registered spell; synthetic fixtures pass for read-only work, protected stops, source-authority blocks, audit veto, exact approval, ambient-approval rejection, dedupe, budgets, and telemetry. | Encode effect, approval, audit, and budget gates around an autonomy trial. | Validated local fixtures; no proof of business outcome or production autonomy. |
| Repository-local observability and learning | `arcanum/README.md:50-82`; `arcanum/spells/observed-invocation-loop/README.md:8-18,61-85`; `arcanum/spells/observed-invocation-loop/development/REMAINING-INTERROGATION.md:24-39` | Baseline-ready for the repository-local Codex command surface. Fixtures cover partial/blocked closeout, strict-vs-standard telemetry failure, identity, migration, and dedupe recovery. | Capture task-level traces and preserve the primary result when observation plumbing fails, unless strict mode is selected. | Not infrastructure observability at scale and not evidence that telemetry improves model quality. |
| Typed semantic outcomes and replay | `.arcanum/inventory/entries/agent-reasoning-engine-contract-strategy-result-synthesis.md:78-104,122-132` | Bounded L0 evaluator witness: two rule families, typed counterfactuals, byte-identical replay, persisted ordering, and a test-only effect boundary. Actor runtime, real effects, general reasoning engine, and anti-bias efficacy remain absent. | Add explicit abstain/defeat/defer/escalate outcomes to one task-level reliability experiment. | “Bounded semantic evaluator witness”; never “built a reasoning engine.” |
| Owner-preserving architecture judgment | `.arcanum/inventory/entries/arcanum-resonantos-addon-research-result-synthesis.md:77-126,128-144` | Accepted research contract and completed governed research dispatch, but proposed product integration, lifecycle witness, and browser witness remain absent. | Keep model, runtime, product, approval, and release ownership separate in the role interface. | Architecture/research evidence only; no integration claim. |
| Concrete ML-adjacent research lifecycle | `arcanum/research/triton-top2-backward-kernel/README.md:60-110`; `RIGOR-VALIDATION-MAP.md:7-29,103-108`; `W4-PO004-PO005-VALIDATION.md:88-93`; `open-residue.md:3-13` | Artifact-backed research, interrogation, Invoke authoring, repeated Task Sessions, PyTorch reference work, and bounded fixed-mask gradient validation. GPU/Triton, FP16, zero-allocation, hard-Top2 differentiation, and full-kernel claims remain unproved. | Demonstrates how an underspecified technical claim can be decomposed into formal, numerical, and systems obligations and stopped at unresolved semantics. | Not CUDA/kernel expertise or frontier-model research ownership. |

The portfolio Inventory lead correctly characterizes Craft/goal as ledgered execution and continuation, while naming a live non-synthetic run as its next falsifier: `.arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md:213-228`. It supports the proof ceiling, not a stronger capability claim.

## Live TypeSafe need and overlap map

Current evidence was re-opened on **2026-08-01**.

The live Ashby board returned nine listed openings: Synthetic Data, Senior Backend/Platform Engineer, Developer Advocate, Product Engineer, Member of Staff, Infrastructure/Kubernetes, Founding Recruiter, GPU Kernel Engineer, and Founding Marketer. The custom opening is currently titled **Member of Staff**, department **Create your own role**, published 2026-07-25. [Live TypeSafe Ashby board API](https://api.ashbyhq.com/posting-api/job-board/typesafe-ai)

TypeSafe publicly describes its mission as lowering the cost of intelligence and building systems that “actually get things done”; its job pages describe the company as a frontier-model lab pursuing real-world reliability, decision-making, and production autonomy. [TypeSafe homepage](https://typesafe.ai/), [Member of Staff](https://jobs.ashbyhq.com/typesafe-ai/cbc0b60a-1613-4b0d-b38a-04fc5558152c)

| Published owner | Explicit current scope | Boundary for the proposed role |
|---|---|---|
| [MTS, Synthetic Data](https://jobs.ashbyhq.com/typesafe-ai/df3dbf1b-9a47-4d8a-88a8-d28c8b8a2ef0) | Datasets, internal evaluation/debugging/data-inspection tooling, evaluation frameworks across model iterations, and experiments connecting data/training interventions to behavior. | Biggest overlap. Proposed role must not own training data, general model evaluation, or causal analysis of training interventions. It owns one end-to-end task trial spanning model output, tools, effects, and owner decisions. |
| [Product Engineer](https://jobs.ashbyhq.com/typesafe-ai/f21f0f84-b0c9-4b63-9f61-3aad6ab0eca4) | Customer-facing features from prototype to production; product instrumentation, quality, reliability, and performance. | Product owns the shipped experience. Proposed role provides a qualification contract and failure evidence; it does not own the UI roadmap or customer feature. |
| [Senior Backend/Platform Engineer](https://jobs.ashbyhq.com/typesafe-ai/d15fb33c-0679-4822-be50-2afb75320e4b) | Inference APIs, resilient multi-cloud serving, storage abstractions, uptime, backward compatibility, and on-call quality. | Platform owns serving reliability and APIs. Proposed role consumes stable interfaces and reports task-level runtime failures. |
| [Infrastructure Engineer](https://jobs.ashbyhq.com/typesafe-ai/4da613b6-6d56-4e8d-8cc4-fad8ca57e4ce) | Kubernetes, networking, GPU infrastructure, monitoring, alerting, tracing, logging, SLO and incident-response concerns. | Infrastructure owns operational telemetry and availability. Proposed role consumes selected traces but does not run clusters or observability infrastructure. |
| [GPU Kernel Engineer](https://jobs.ashbyhq.com/typesafe-ai/382181f5-4ef4-4cba-85ca-efd79b13284e) | CUDA/CuTe kernels, training/inference performance, profiling, and real LLM-training experience. | No overlap should be claimed. Repository ML research explicitly stops short of this expertise. |
| [Developer Advocate](https://jobs.ashbyhq.com/typesafe-ai/4537eb37-94a3-4d6-9760-6f41c125aba4) | Developer voice, documentation, SDK/API references, community feedback, early access, red-teaming, bug bounties, demos, and education. | DevRel owns external feedback and communication. Proposed role’s artifacts are internal qualification evidence, not community programming or public documentation. |

The current team page lists public biographies spanning AI research/software, production AI, backend/API, developer tooling, MLOps, infrastructure/observability, product, design, and DevRel. That makes the interface discipline especially important, but biographies do not reveal private ownership or prove the proposed gap exists. [TypeSafe team](https://typesafe.ai/#team)

**Inferred unsolved problem:** TypeSafe may need an owner for the point where model-level evaluation stops and a real, multi-step, tool-using task must be qualified as understandable, replayable, failure-visible, and safe to advance. No public page establishes whether that point is currently unowned.

## Role-interface map

- **Model research:** supplies model checkpoints and hypotheses; receives task-level failure evidence. Retains architecture, training, and model-quality authority.
- **Synthetic Data/evals:** owns datasets, model-evaluation frameworks, and training-intervention analysis. Co-designs representative task fixtures; does not inherit task/runtime failure ownership.
- **Reliable Autonomy Systems:** owns one end-to-end task contract, runnable qualification harness, trace schema, effect boundaries, failure taxonomy, replay, and decision-ready terminal report.
- **Product:** selects economically valuable workflows and owns shipped behavior.
- **Backend/platform:** supplies stable inference/runtime interfaces and owns API/SLO incidents.
- **Infrastructure:** supplies operational telemetry and owns cluster/network/GPU remediation.
- **DevRel:** translates released evidence into public developer material only after the owning teams approve it.
- **Leadership/human owners:** choose the trial, accept risk, and make go/hold/kill or release decisions.

## First 30/60/90-day outcomes

**First 30 days**

- Select exactly one economically valuable, multi-step model-backed task with research, product, and platform owners.
- Freeze a task contract: inputs, environment, tool/effect permissions, success criteria, abstention/escalation behavior, failure taxonomy, and owner map.
- Baseline the current model/system path using existing TypeSafe instrumentation.
- Deliver a runnable thin-slice fixture and a report that distinguishes model, task-specification, product, runtime, and infrastructure failures.

**By 60 days**

- Build an internal qualification harness that runs the frozen task against available versioned model candidates.
- Capture model calls, tool/effect attempts, environment state, interventions, terminal outcome, and incomplete/invalid evidence.
- Add adversarial fixtures for stale input, partial completion, unauthorized effect, ambiguous ownership, nondeterministic replay, and missing telemetry.
- Demonstrate that a failed or incomplete trace cannot silently become a passing qualification result.

**By 90 days**

- Run one bounded cross-functional pilot, ideally across two model iterations if TypeSafe can expose them.
- Reproduce the principal failure classes and route each to its actual owner.
- Evaluate at least one bounded intervention without claiming causal model improvement unless the experiment supports it.
- Produce a go/hold/kill decision package and land one reusable regression gate in the owning team’s workflow.
- Success witness: TypeSafe can inspect why the task passed or failed, replay the controlled evidence, and decide whether the next change belongs to model research, data/evals, product, platform, or infrastructure.

## Missing qualifications and questions

- Does the candidate satisfy the Member of Staff requirement for 5+ years of professional expertise in high-performing teams? The supplied profile does not establish this.
- Is five-day in-person San Francisco work feasible? Visa sponsorship is advertised, but relocation and authorization details are unknown.
- What production software, customer, or on-call experience exists beyond repository-local work?
- What hands-on Python, TypeScript, LLM implementation, statistics, and experiment-design depth can be demonstrated?
- Can the candidate produce a public portfolio from Arcanum without exposing private DomainSpec, Saturn, or CyberAlchemy-v2 material?
- Does TypeSafe already assign end-to-end tool-use/autonomy qualification to Synthetic Data, Product, or an unadvertised research owner?
- What real tasks, model interfaces, checkpoints, and traces would be available in the first 90 days?
- Would TypeSafe value a separate task-level qualification owner, or prefer this capability inside Synthetic Data/Product Engineering?
- No current web evidence supports a culture-fit claim; only work arrangements and self-described values are public.

## Public-safe phrasing

- “I build repeatable, inspectable workflows that turn ambiguous AI-assisted work into explicit task contracts, executable checks, and evidence-backed handoffs.”
- “My public work includes repository-local systems for bounded multi-agent execution, deterministic validation, failure-first gating, replay, and observability.”
- “I use formal methods to constrain claims and test small interfaces; I do not treat them as proof of model behavior.”
- “My focus is system and workflow reliability around AI use, not frontier-model training or production infrastructure ownership.”
- “At TypeSafe, I would propose owning the qualification path from one promising model capability to one falsifiable real-world autonomy trial.”

Suggested short pitch:

> I would like to own the path from a promising model behavior to a decision-ready autonomy trial. That means choosing one economically valuable task with the relevant owners, making its assumptions and effect boundaries explicit, building a runnable evaluation harness around the complete model-and-tool loop, and returning replayable evidence that tells research, product, and platform teams what failed and what decision is justified. My public work demonstrates bounded execution, deterministic validation, multi-agent coordination, failure-first gates, and evidence-backed continuation. I am not claiming frontier-model training or production-infrastructure ownership; the value of the role is making those owners’ work meet in an inspectable end-to-end test.

## Forbidden overclaims

- “Frontier-model reliability expert.”
- “Built or operated autonomous AI in production.”
- “Built a general reasoning engine.”
- “Formal verification proves model or AI correctness.”
- “Owned synthetic-data or frontier-model evaluation.”
- “Built a zero-allocation Triton kernel” or “exact backward through hard Top2.”
- “Production-grade multi-agent orchestration platform.”
- “Arcanum proves productivity, reliability, or business impact.”
- “Repository receipts prove deployment, release, customer value, or production readiness.”
- “TypeSafe lacks this role” or “TypeSafe needs me to own this.”
- Any culture-fit claim inferred from recruiting copy.
- Any public disclosure of private repository paths, private authority prose, or descriptions of DomainSpec/Saturn as shipped products.

## Ranked role candidates

1. **Member of Technical Staff, Reliable Autonomy Systems**  
   Distinctiveness: high. Usefulness: high if TypeSafe lacks an end-to-end task-qualification owner. Best interface clarity and strongest 90-day witness.

2. **Research Engineer, Task-Level AI Reliability**  
   Distinctiveness: medium. Usefulness: high. More conventional title, but serious overlap risk with Synthetic Data’s published evaluation ownership.

3. **Member of Staff, Research-to-Production Qualification**  
   Distinctiveness: high. Usefulness: medium. Risks collapsing into program management, governance, or process overhead; viable only with hands-on code ownership and the concrete pilot above.

```json
{
  "status": "pass",
  "dispatch_id": "2026-08-01-typesafe-reliable-autonomy-role-route",
  "run_id": "typesafe-role-run-001",
  "action_id": "spawn-0003",
  "role": "arcanum-typesafe-fit-explorer",
  "started_at": "2026-08-01T04:09:21Z",
  "finished_at": "2026-08-01T04:19:39Z",
  "artifacts_read": [
    "research/2026-08-01-typesafe-reliable-autonomy-role/orchestration/run-001/actions/spawn-0003.json",
    "research/2026-08-01-typesafe-reliable-autonomy-role/dispatch-sheet.json",
    "research/2026-08-01-typesafe-reliable-autonomy-role/candidate-profile.md",
    "research/2026-08-01-typesafe-reliable-autonomy-role/strategy-inventory-packet.json#selected[arcanum-resonantos-addon-research-result-synthesis,agent-reasoning-engine-contract-strategy-result-synthesis,investor-bp-project-portfolio-research-findings]",
    ".arcanum/inventory/entries/arcanum-resonantos-addon-research-result-synthesis.md",
    ".arcanum/inventory/entries/agent-reasoning-engine-contract-strategy-result-synthesis.md",
    ".arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md",
    "arcanum/README.md",
    "arcanum/spells/invoke/README.md",
    "arcanum/arcana/task-session/README.md",
    "arcanum/arcana/craft/README.md",
    "arcanum/spells/goal/README.md",
    "arcanum/spells/goal/validation/results/fixture-report.md",
    "arcanum/formulae/dispatch-spec/README.md",
    "arcanum/runtime/orchestrate/SKILL.md",
    "arcanum/formulae/dispatch-spec/development/runtime-integration/20260722T063407Z-native-host-canary/RESULT.md",
    "arcanum/spells/observed-invocation-loop/README.md",
    "arcanum/spells/observed-invocation-loop/development/REMAINING-INTERROGATION.md",
    "arcanum/framework/observability/OBSERVED-RUNS.md",
    "arcanum/framework/observability/HOOK-OPERATIONS-LEDGER.md",
    "arcanum/arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/INVOKE-REPORT.md",
    "arcanum/arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/WORK-PACK.md",
    "arcanum/arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/work-pack/results/SWU-TSGR-001-RESULT.json through SWU-TSGR-007-RESULT.json",
    "arcanum/research/triton-top2-backward-kernel/README.md",
    "arcanum/research/triton-top2-backward-kernel/RIGOR-VALIDATION-MAP.md",
    "arcanum/research/triton-top2-backward-kernel/W4-PO004-PO005-VALIDATION.md",
    "arcanum/research/triton-top2-backward-kernel/open-residue.md"
  ],
  "urls": [
    "https://typesafe.ai/",
    "https://api.ashbyhq.com/posting-api/job-board/typesafe-ai",
    "https://jobs.ashbyhq.com/typesafe-ai/cbc0b60a-1613-4b0d-b38a-04fc5558152c",
    "https://jobs.ashbyhq.com/typesafe-ai/df3dbf1b-9a47-4d8a-88a8-d28c8b8a2ef0",
    "https://jobs.ashbyhq.com/typesafe-ai/d15fb33c-0679-4822-be50-2afb75320e4b",
    "https://jobs.ashbyhq.com/typesafe-ai/4537eb37-94a3-4d6-9760-6f41c125aba4",
    "https://jobs.ashbyhq.com/typesafe-ai/f21f0f84-b0c9-4b63-9f61-3aad6ab0eca4",
    "https://jobs.ashbyhq.com/typesafe-ai/4da613b6-6d56-4e8d-8cc4-fad8ca57e4ce",
    "https://jobs.ashbyhq.com/typesafe-ai/382181f5-4ef4-4cba-85ca-efd79b13284e"
  ],
  "validation": [
    "read-only action and zero-write scope confirmed",
    "only the three named Inventory leads were used as discovery inputs",
    "load-bearing internal claims were resolved to source files and exact line selectors",
    "current TypeSafe employer claims were checked only against the TypeSafe homepage and employer-controlled Ashby pages/API on 2026-08-01",
    "current open-role overlap was separated from inferred private roadmap",
    "no repository files were edited and no external contact or application action occurred"
  ],
  "blockers": [
    "TypeSafe internal ownership and roadmap are unknown",
    "candidate production experience, professional-years evidence, language depth, onsite feasibility, and work authorization are not established",
    "the custom role is killed or absorbed if Synthetic Data or Product already owns end-to-end autonomy qualification"
  ]
}
```

## Agent 2 — Spivak, David / DomainSpec Traceability Explorer

The repository supports a strong, bounded hypothesis: the candidate could own the bridge from ambiguous automation intent to typed, traceable, falsifiable workflow evidence. It does not establish frontier-model training, model architecture, GPU, synthetic-data, or model-level reliability expertise. Personal leadership is self-described; repository evidence proves the system’s artifacts and results, not exclusive individual authorship.

## Exact-bound evidence matrix

| Capability | Observed artifact/result | Exact source | Proof posture | Reliability/automation problem it could serve | Concrete responsibility | First-90-day deliverable | Public-safe phrasing | Forbidden overclaim |
|---|---|---|---|---|---|---|---|---|
| Turn ambiguous architecture into a typed implementation contract | A refinement separated factory, consumer authority, source files, generated graph, manifest, and human view; its toy compared three layouts with byte-identical graphs, ten negative controls, and an owner-gated plan. A later Task Session validated two independent corpora and 26 degraded cases, while explicitly withholding release admission. | `projects/domainspec-v2/development/refinement-runs/20260714-minted-project-node-package-toy-game/RESULT.md:L7-L49,L69-L80`; `.../task-sessions/20260715-swu-mnp-006/TASK-SESSION-RESULT.md:L3-L13`; `.../conformance-receipt.json` selectors `$.fixtures`, `$.case_results`, `$.release_admission` | Implemented, deterministic, private, bounded conformance evidence; not released or production-admitted. | Requirements and representations drift before an automation system reaches executable evaluation. | Own problem framing, typed artifact contracts, source/generated boundaries, and the smallest falsifiable pilot. | Convert one real lab workflow into canonical sources, a typed graph, generated views, negative controls, and a digest-bound conformance receipt. | “I turn ambiguous requirements into typed, inspectable contracts and executable failure cases.” | “I built a production autonomous platform”; “formally complete”; “the repository proves my exclusive authorship.” |
| Derive executable checks from source-linked specifications | The engine implements `parse → typed graph → pure derivation → content-addressed key → spec/tests`; normalized parsing explicitly excludes behavioral inference from prose. Live run: 29 test files and 240/240 tests passed. | `projects/domainspec-v2/impl/test-derivation-engine/README.md:L3-L50`; live command `npm --prefix projects/domainspec-v2/impl run engine:test`, 2026-08-01 | Current executable implementation; structural/check derivation, not semantic satisfiability, application generation, or model evaluation. Private rules remain private. | Automation evaluations can be incomplete, unstable, or detached from the requirement that motivated them. | Build deterministic specification-to-check tooling and maintain source anchors, stable identities, and negative controls. | Produce a two-corpus check-generation pilot with replayable outputs, mutation controls, and explicit uncovered obligations. | “I build deterministic pipelines that derive source-linked checks and make missing coverage visible.” | “The checks prove runtime correctness”; “model reliability is solved”; “all obligations are executable.” |
| Preserve traceability without coercing unresolved concepts | The UI-profile specimen has 17 source nodes, 20 endpoint-admitted edges, all 11 required concept representations, zero orphans, and five typed owner-decision residues. Tests ensure unresolved edges remain absent and five named endpoint mutants fail. | `projects/domainspec-v2/impl/tools/tests/ui-profile-graph-source.test.ts:L59-L178`; `projects/domainspec-v2/development/ui-profile-implementation/runs/SWU-UIP-007/TASK-SESSION-RESULT.md:L10-L31`; generated receipt selector `impl/spec/features/ui-profile-create-player/generated/build-receipt.json:$` | Implemented and mechanically validated, but canonically inactive, release-unadmitted, independently unreplicated, and empirically provisional. | A reliable automation chain needs to explain which source, type, relationship, projection, and unresolved decision produced each output. | Own traceability contracts joining source intent, generated artifacts, checks, residue, and decision owners. | Instrument one automation workflow end-to-end with stable source handles, typed transformations, output digests, and an unresolved-residue queue. | “I make automation artifacts traceable back to their sources, transformations, checks, and decision owners.” | “End-to-end model interpretability”; “production provenance guarantee”; “all semantics are captured.” |
| Convert ambiguous failure semantics into an explicit decision map | A blocker gate presented two admissible semantics for a known failing case, including benefit, risk, downstream effect, and reversibility. Direct human selection authorized an expected-red meta-verifier while preserving the raw red. | `projects/domainspec-v2/development/financial-settlement-executable-test-generation/session-evidence/SWU-FSTG-004/20260723T193928Z-emitter-verification-decision/DECISION-GATE.md:L10-L58`; `option-admissibility-receipt.json:L2-L18`; `decision-receipt.json:$` | Closed owner decision with exact provenance; local/private. It governs verifier semantics, not model behavior. | Teams need to decide whether a known failure blocks closure, becomes an expected-red invariant, or demands source repair. | Design decision gates for evaluation semantics, exceptions, and escalation boundaries. | Deliver a decision protocol and receipt schema for one recurring reliability ambiguity, with explicit options, falsifiers, and owner selection. | “I turn ambiguous failures into explicit, reversible decisions with inspectable consequences.” | “Automated judgment replaces human responsibility”; “a green wrapper removes the failure.” |
| Stop, resume, and continue bounded automation without losing state | The first chain stopped intentionally after two passes when SWU-004 hit a semantic blocker; no implementation mutation occurred. After the owner decision, the resumed chain completed SWU-004 and VERIFY. The historical blocker remained intact, and an earlier continuation artifact identified—but did not auto-dispatch—the next owner route. | `.../task-session-until-blocker/20260723T191821Z-fstg-frontier/CHAIN-RESULT.md:L1-L14`; `.../20260723T213902Z-fstg-resumed-frontier/CHAIN-RESULT.md:L1-L18`; `.../SWU-FSTG-001/20260723T174139Z-declared-subset-mode/CONTINUATION-ROUTE-RESULT.md:L1-L20`; `.../TASK-SESSION-CLOSEOUT-REPORT.md:L1-L15` | Closed local workflow evidence; runtime recorded as local fallback, not production orchestration. | Long-running automation must fail closed, preserve why it stopped, and resume only after the correct authority acts. | Own bounded run-state, blocker fingerprints, continuation packets, and authorization-aware resumption. | Pilot one lab workflow that can stop on a typed blocker, emit a continuation packet, accept an owner decision, and replay the completed evidence chain. | “I design automation that stops honestly, preserves state, and resumes through an explicit owner route.” | “Fully autonomous research operator”; “self-healing production agent”; “human approval is unnecessary.” |
| Design experiments that distinguish support, collapse, and missing evidence | The Form experiment defined exactly three outcomes, fixed positive-equivalence and 2/2/2 evidence gates, evaluated three alternatives over six dimensions, and found 0/3 complete coverage. It then blocked rather than inventing corpus B, independent authorship, or a second style. | `projects/domainspec-v2/development/ui-candidate-formalization-experiments/DEFINE.md:L21-L47`; `EXPERIMENT-CONTRACTS.md:L15-L55`; `runs/SWU-UCFE-003/receipt.json:L26-L45`; `runs/SWU-UCFE-005/BLOCKER.md:L3-L20` | Candidate/experimental and incomplete. Historic local receipt passed; current rerun is 30/33 because pinned registry digest and status assumptions have drifted. | Reliability claims often survive because missing evidence is mistaken for novelty or success. | Preregister capability hypotheses, alternatives, negative controls, independence requirements, and typed defer conditions. | Run one two-corpus, two-style, two-reviewer reliability experiment and report supported, covered-existing, or defer-missing without threshold tailoring. | “I build experiments that separate supported capability from existing explanations and insufficient evidence.” | “The candidate type is validated”; “independent replication exists”; “structural fixtures substitute for real evidence.” |
| Reconcile inconsistent evidence without manufacturing authority | A governed triage reconciled 35 unique relationship keys: 24 evidence-ready, six staged-review, three deferred, and two rejected/superseded. Seven agents joined and closed; missing cards were not invented, contradictions and generated/deferred states remained visible, and a next definitions owner was named. | `projects/domainspec-v2/development/r3-closeout-plan/task-sessions/2026-07-12-swu-r3c-006/TASK-SESSION-RESULT.md:L13-L50,L65-L115`; supporting findings `.../research/2026-07-12-relationship-card-triage/findings.md:L102-L126` | Closed non-authority staging result. Historic 69/69 tool receipt is valid for that session, not the current aggregate checkout. | Complex automation programs accumulate conflicting schemas, legacy evidence, generated views, and unresolved ownership. | Own evidence reconciliation, typed dispositions, contradiction retention, and downstream owner routing. | Produce a reconciled evidence matrix for one reliability surface, including rejected/deferred states and a named next-action owner. | “I reconcile conflicting technical evidence without turning absence, repetition, or generated output into authority.” | “The ontology is complete”; “the dispatch proves correctness”; “receipts prove truth.” |

## Current validation and claim ceiling

- `engine:test`: PASS — 29 files, 240/240 tests.
- Root `typecheck`: PASS.
- Financial Settlement expected-red verifier: PASS — 52 generated, 51 passing, exactly one declared red; zero todo/skip. Its behavioral ledger remains 79 obligations: 12 assertions, one property, 67 coverage gaps.
- `tools:test`: FAIL — 170/172. Both failures come from the retired-reference guard finding seven newer unclassified implementation-conformance files.
- UI-candidate experiment tests: FAIL — 30/33. The old preregistration digest and status assumptions no longer match current meta-type authority.
- Validation produced no tracked DomainSpec-v2 diff. The checkout already contained untracked implementation-conformance work.

Therefore the strongest claim is workflow/system-level reliability engineering around AI-enabled automation: specification, traceability, evaluators, negative controls, decision gates, evidence receipts, and bounded continuation. It is not proof of frontier-model reliability or model-training expertise.

Maturity boundaries:

- **Reformulation:** the implementation home is still described as migrating and reformulating earlier material.
- **Candidate:** UI candidate types and their empirical formalization process remain non-active.
- **Partial:** typed graphs and deterministic checks cover bounded structural/behavioral slices, not whole-system semantics.
- **Private:** the implementation corpus and derivation rules are private; public application prose must use generic capability language only.
- **Unimplemented/unproved:** broad semantic satisfiability, cross-feature completeness, independent replication for the UI experiment, production orchestration, release admission, and model-level reliability.

Role-name fragments only:

- **Specification-to-Reliability**
- **Traceable Autonomy**

```yaml
receipt:
  status: pass
  action_id: spawn-0002
  dispatch_id: 2026-08-01-typesafe-reliable-autonomy-role-route
  run_id: typesafe-role-run-001
  started_at_utc: 2026-08-01T04:12:54Z
  finished_at_utc: 2026-08-01T04:18:58Z
  artifacts_actually_read:
    dispatch:
      - research/2026-08-01-typesafe-reliable-autonomy-role/orchestration/run-001/actions/spawn-0002.json
      - research/2026-08-01-typesafe-reliable-autonomy-role/dispatch-sheet.json
      - research/2026-08-01-typesafe-reliable-autonomy-role/candidate-profile.md
      - research/2026-08-01-typesafe-reliable-autonomy-role/strategy-inventory-packet.json
    inventory_leads:
      - .arcanum/inventory/entries/domainspec-v2-r3c-relationship-card-triage-dispatch-closeout-synthesis.md
      - .arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md
      - .arcanum/inventory/queries/2026-07-06-spec-driven-completeness-moat-inventory-research/findings.md
    primary_evidence:
      - projects/domainspec-v2/README.md
      - projects/domainspec-v2/authority/AUTHORITY-MODEL.md
      - projects/domainspec-v2/impl/test-derivation-engine/README.md
      - projects/domainspec-v2/impl/tools/tests/ui-profile-graph-source.test.ts
      - projects/domainspec-v2/development/ui-profile-implementation/runs/SWU-UIP-007/TASK-SESSION-RESULT.md
      - projects/domainspec-v2/development/refinement-runs/20260714-minted-project-node-package-toy-game/RESULT.md
      - projects/domainspec-v2/authority/decisions/2026-07-14-minted-project-node-package.md
      - projects/domainspec-v2/development/refinement-runs/20260714-minted-project-node-package-toy-game/task-sessions/20260715-swu-mnp-006/TASK-SESSION-RESULT.md
      - projects/domainspec-v2/development/financial-settlement-executable-test-generation/session-evidence/
      - projects/domainspec-v2/development/ui-candidate-formalization-experiments/
      - projects/domainspec-v2/development/r3-closeout-plan/research/2026-07-12-relationship-card-triage/findings.md
      - projects/domainspec-v2/development/r3-closeout-plan/task-sessions/2026-07-12-swu-r3c-006/TASK-SESSION-RESULT.md
  validation:
    engine_test: "pass 240/240"
    typecheck: pass
    financial_settlement_verifier: "pass 52 generated, 51 pass, 1 expected red"
    tools_test: "fail 170/172; seven unclassified current-checkout files"
    ui_candidate_experiment: "fail 30/33; stale digest/status pins"
    tracked_diff: none
  blockers: []
```
