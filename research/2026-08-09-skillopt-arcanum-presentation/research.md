# SkillOpt + Arcanum presentation research corpus

Dispatch: `2026-08-09-skillopt-arcanum-presentation-research`

The parent appends explorer returns verbatim below. These returns are evidence inputs, not final findings or authority. Paper results remain paper-reported unless a receipt explicitly establishes reproduction.

## Explorer return spawn-0001

~~~text
status: PASS
output_ref: receipts/explorer-skillopt.json
started_utc: 2026-08-09T23:28:23Z
finished_utc: 2026-08-09T23:33:04Z
mutation: none
reproduction_status: not independently reproduced; all experimental findings below are paper-reported

source_identities:
- paper: arXiv:2605.23904v2, “SkillOpt: Executive Strategy for Self-Evolving Agent Skills”
  - authors: Yifan Yang; Ziyang Gong; Weiquan Huang; Qihao Yang; Ziwei Zhou; Zisu Huang; Yan Li; Xuemei Gao; Qi Dai; Bei Liu; Kai Qiu; Yuqing Yang; Dongdong Chen; Xue Yang; Chong Luo
  - v1: 2026-05-22T17:59:50Z
  - v2/current: 2026-05-25T17:58:16Z
  - identity/history: https://arxiv.org/abs/2605.23904
  - immutable PDF: https://arxiv.org/pdf/2605.23904v2
  - locally downloaded PDF sha256: 87f7f0f323b1671e9202b3ebb1596e909e507c71ecd1b360b0075a5ee1727fe3
  - extent: 27 pages, 4 figures, 6 tables
- author-linked code: Microsoft/SkillOpt, https://github.com/microsoft/SkillOpt
  - current inspected identity: commit ba820b500f9da96685cf2780c7dc85ed4eb6563e, committed 2026-08-09T16:50:50Z
  - immutable URL: https://github.com/microsoft/SkillOpt/tree/ba820b500f9da96685cf2780c7dc85ed4eb6563e
  - repository is substantially newer than the paper and must not be used as though it were the exact experimental snapshot
- author project page: https://microsoft.github.io/SkillOpt/
  - official but mutable; use for presentation media/navigation, not load-bearing experimental proof

evidence_rows:

- row_id: SO-P01
  claim/paraphrase: SkillOpt formulates one natural-language skill document as the trainable external state of a frozen target model. For harness h, task x, skill s, execution yields trajectory and scalar reward in [0,1]; train generates candidates, selection chooses, and test reports final performance.
  source: arXiv:2605.23904v2
  selector: pp.4–5, §3.1, Equations (1)–(3)
  proof_status: paper-defined method; not reproduced
  presentation_relevance: anchor the optimization analogy without claiming model-weight training

- row_id: SO-P02
  claim/paraphrase: Optimizer state includes current skill, best validation-gated skill, cached skill hashes, an epoch-local rejected-step buffer, and optional slow/meta state; only the best accepted artifact is exported as best_skill.md.
  source: arXiv:2605.23904v2
  selector: p.5, §3.1, paragraph following Eq. (3); p.22, Algorithm 1 lines 1–3
  proof_status: paper-described implementation
  presentation_relevance: gives an exact state-machine vocabulary for a code diagram

- row_id: SO-P03
  claim/paraphrase: The frozen target model produces scored rollout batches; optimizer reflection separates failures and successes into minibatches, proposes structured edits, then hierarchically deduplicates and merges proposals with failure corrections prioritized.
  source: arXiv:2605.23904v2
  selector: p.5, §§3.2–3.3; p.4, Figure 2; p.22, Algorithm 1 lines 7–12
  proof_status: paper-described method
  presentation_relevance: supports the rollout → reflection → proposal → merge causal chain

- row_id: SO-P04
  claim/paraphrase: The edit budget Lt is a textual learning-rate analogue. Patch mode permits append, insert_after, replace, and delete; ranking clips the merged pool to at most Lt edits. Constant, linear, cosine, and autonomous schedules are supported.
  source: arXiv:2605.23904v2
  selector: p.5, §3.4; p.27, §C.3; pp.23–25, §§C.2.1–C.2.6 prompt contracts
  proof_status: paper-described mechanism
  presentation_relevance: precise meaning of “bounded edit,” avoiding the false analogy of a numeric gradient

- row_id: SO-P05
  claim/paraphrase: A candidate is accepted only when its selection score is strictly greater than the current score; ties are rejected. If it also exceeds the historical best, it becomes best_skill.md. The test split remains locked until final reporting.
  source: arXiv:2605.23904v2
  selector: p.6, §3.5; p.8, “Default optimizer hyperparameters”; p.12, “Gate strictness”; p.22, Algorithm 1 lines 14–27 and 37
  proof_status: paper-defined acceptance rule
  presentation_relevance: clean held-out gate; must not be renamed promotion, publication, or production approval

- row_id: SO-P06
  claim/paraphrase: Rejected edits and their score drops become epoch-local negative feedback. At epoch boundaries, same-task comparisons categorize improvements, regressions, persistent failures, and stable successes; protected slow guidance is itself validation-gated. Optimizer meta-skill remains optimizer-side and is not deployed.
  source: arXiv:2605.23904v2
  selector: p.6, §§3.5–3.6; pp.26–27, §§C.2.7–C.2.8; p.27, §§C.3–C.4
  proof_status: paper-described method
  presentation_relevance: distinguishes target-facing skill state from training-only optimizer memory

- row_id: SO-P07
  claim/paraphrase: Optimization is offline. Deployment uses the static best_skill.md with the target model/harness fixed; it adds zero optimizer model calls and no weight updates at inference, though the skill’s text still consumes context tokens.
  source: arXiv:2605.23904v2
  selector: pp.2–3, Introduction; p.6, §3.7; pp.13–15, §§4.3–4.4 and Table 6
  proof_status: architecture/property reported by authors
  presentation_relevance: essential offline-versus-inference distinction; “zero inference-time model calls” does not mean zero prompt-token overhead

- row_id: SO-P08
  claim/paraphrase: Evaluation covers six headline benchmarks—SearchQA, SpreadsheetBench, OfficeQA, DocVQA, LiveMathematicianBench, ALFWorld—seven direct-chat target models, plus GPT-5.5 in Codex and Claude Code harnesses. Baselines are no skill, human skill, one-shot LLM skill, Trace2Skill, TextGrad, GEPA, and EvoSkill where protocol-compatible.
  source: arXiv:2605.23904v2
  selector: pp.7–10, Table 1 and §4; pp.20–21, Appendix C “Benchmarks and metrics” and “Baselines”
  proof_status: paper-reported protocol
  presentation_relevance: defines the denominator and prevents “universal” benchmark claims

- row_id: SO-P09
  claim/paraphrase: SkillOpt is reported best or tied-best in all 52 evaluated model × benchmark × harness cells. On GPT-5.5, average absolute gains over no skill are +23.5 points in direct chat, +24.8 in Codex, and +19.1 in Claude Code; direct-chat SkillOpt averages 82.3 versus a 76.9 per-cell oracle over competing methods, a +5.4-point gap.
  source: arXiv:2605.23904v2
  selector: pp.7, 10–11, Table 1 and §§4.1 “Main Results”/“Headline numbers”
  proof_status: paper-reported; no independent rerun
  presentation_relevance: headline result must retain “evaluated,” the 52-cell denominator, metric units, and baseline context

- row_id: SO-P10
  claim/paraphrase: Every reported transfer row is positive over the target no-skill baseline: four genuine cross-model rows (+3.0 to +9.4), four cross-harness rows (+1.6 to +59.7), and three OlympiadBench→Omni-MATH rows (+1.3 to +3.7), all without target-side reoptimization.
  source: arXiv:2605.23904v2
  selector: p.9, Table 4; pp.12–13, §4.3
  proof_status: paper-reported transfer, not general transfer proof
  presentation_relevance: supports bounded “transfer observed in tested shifts,” not universal portability

- row_id: SO-P11
  claim/paraphrase: Component ablations associate bounded edits, rejected-buffer feedback, and slow/meta updates with performance. Removing the rejected buffer changes SearchQA/Spreadsheet/LiveMath from 87.1/77.5/61.3 to 85.5/72.9/58.9; removing both meta and slow update changes them to 86.3/55.0/59.7.
  source: arXiv:2605.23904v2
  selector: p.8, Tables 2–3; pp.11–12, §4.2
  proof_status: one-factor paper ablations; causal scope limited to tested configurations
  presentation_relevance: evidence for mechanism importance, especially the −22.5 SpreadsheetBench change

- row_id: SO-P12
  claim/paraphrase: A target-matched optimizer remains effective but trails GPT-5.5 in all four tested cells, recovering approximately 56–74% of the stronger optimizer’s gain. This argues against describing SkillOpt solely as strong-teacher distillation, but does not eliminate all optimizer-capacity confounding.
  source: arXiv:2605.23904v2
  selector: pp.13–14, §4.3 “Effect of optimizer strength,” Table 5
  proof_status: paper-reported controlled comparison
  presentation_relevance: nuanced answer to self-optimization claims; only four cells were tested

- row_id: SO-P13
  claim/paraphrase: Final artifacts in six GPT-5.5/GPT-5.5 case studies are 379–1,995 tokens and arise from 1–4 accepted bounded updates. Training cost ranges from 20.8M to 213.8M tokens and 0.6M to 46.4M tokens per absolute test-point gain.
  source: arXiv:2605.23904v2
  selector: pp.14–15, §4.4 and Table 6
  proof_status: paper-reported case-study accounting
  presentation_relevance: balances compact deployment with substantial offline compute

- row_id: SO-P14
  claim/paraphrase: Related-work positioning is narrower than general self-improving agents: unlike prompt/configuration optimization, skill-library growth, discovery, repository sharing, or weight/policy optimization, SkillOpt claims controlled training of one persistent, portable domain skill with batching, bounded edits, selection gating, rejected memory, and slow/meta updates.
  source: arXiv:2605.23904v2
  selector: pp.3–4, §2 “Prompt auto tuning and agent-configuration search” and “Skill construction and skill evolution”
  proof_status: authors’ positioning; priority claim not independently exhaustively established
  presentation_relevance: safe framing is “paper positions itself as…”; cite GEPA, SkillsBench/SoK, Trace2Skill, EvoSkill, and related skill-evolution work when comparing

reported_quantitative_results:
- 52/52 evaluated cells: percentage accuracy/hard success or exact-match, held-out test splits; paper-reported best or tied-best against measured protocol-compatible baselines.
- GPT-5.5 direct chat: mean 58.8 no skill → 82.3 SkillOpt, +23.5 percentage points across six benchmarks.
- GPT-5.5 Codex: +24.8 points mean over no skill across five evaluated benchmarks; +14.0 over EvoSkill.
- GPT-5.5 Claude Code: +19.1 points mean over no skill across five evaluated benchmarks; +3.2 over EvoSkill.
- Largest GPT-5.5 direct-chat task gains: SpreadsheetBench 41.8→80.7 (+38.9); OfficeQA 33.1→72.1 (+39.0).
- Transfer denominator: 11 genuine transfer rows in Table 4—4 cross-model, 4 cross-harness, 3 cross-benchmark—all positive in the reported experiment.
- Ablation highlight: SpreadsheetBench 77.5→55.0 (−22.5 points) without both meta skill and slow update.
- Artifact/cost denominator: six GPT-5.5/GPT-5.5 runs; 379–1,995 final tokens, 1–4 accepted updates, 20.8M–213.8M training tokens.

contradictions_or_version_drift:
- arXiv is v2, not v1: v1 was 22 May; current v2 is 25 May 2026. Cite v2 explicitly.
- The PDF contains a minor internal typo: §4.3 says “Tables 4–4,” evidently referring to Table 4’s three panels.
- Appendix C names SealQA among benchmark descriptions, while the six headline Table 1 benchmarks use SearchQA and do not include SealQA. Do not silently expand the headline suite to seven.
- Main repository HEAD is commit ba820b5 from 2026-08-09 and contains substantial post-paper functionality, including SkillOpt-Sleep. It is not the immutable code snapshot for May’s experiments.
- Project-page summaries simplify transfer: one current card says cross-harness +31.8, whereas paper Table 4 reports direction/task-specific gains of +1.6, +12.8, +59.7, and +43.6. Prefer Table 4.
- Paper prose calls slow/meta removal evidence strong, but the ablation combines removal of two components in one row; do not attribute the −22.5 solely to either component.

limitations:
- Requires scored trajectories and a reliable selection signal; subjective/open-ended tasks may need human or model judges.
- Offline training requires additional rollouts and optimizer calls; costs may not amortize for one-off tasks.
- Optimizes one skill, potentially inadequate for heterogeneous domains needing disjoint procedures or libraries.
- Training-distribution heuristics can fail under larger model, harness, or domain shifts; transfer needs fresh held-out evaluation.
- Selection gating reduces harmful accepted edits but is not a safety, semantic-correctness, governance, or production-approval guarantee.
- Main results are author-reported preprint evidence, not peer-reviewed or independently reproduced here.
- Baseline coverage is not uniform: EvoSkill is harness-side where matched runs exist; TextGrad/GEPA are direct-chat comparisons; incompatible entries are omitted.
- “Best on 52/52” is bounded to tested cells, baselines, scorers, and splits.
- The stronger-optimizer claim has only four matched cells.
- Compactness and procedurality are supported by six case studies, not proof against all forms of overfitting.

citation_duties:
- Cite arXiv:2605.23904v2 with all authors or accepted abbreviated bibliography; label every number “paper-reported.”
- For 52/52, cite Table 1 and preserve “evaluated cells,” “best or tied-best,” metric, splits, and baseline set.
- For transfer, cite Table 4 and specify source→target direction, task, model, and no-skill denominator.
- For mechanism claims, cite §§3.1–3.6 plus Algorithm 1; distinguish analogy from mathematical gradient optimization.
- For related-work comparisons, cite the original works named by SkillOpt rather than relying on SkillOpt alone when a comparison becomes load-bearing.
- Cite repository code with commit ba820b500f9da96685cf2780c7dc85ed4eb6563e and state that current HEAD postdates the experiments.
- Never equate SkillOpt acceptance with human promotion, publication, deployment authorization, or production proof.

blockers:
- No exact author-declared commit/tag corresponding to the v2 experimental snapshot was established from the paper or current repository surface.
- No experiments were rerun; code/results reproducibility remains unverified.
- Exhaustive independent priority/novelty verification across all cited related work was outside this explorer’s bounded task; “first” remains an author-qualified claim.
~~~

## Explorer return spawn-0002

~~~text
status: PASS
target_output_ref: receipts/explorer-arcanum.json
dispatch_id: 2026-08-09-skillopt-arcanum-presentation-research
run_id: 20260809T232823Z-skillopt-arcanum-presentation-001
action_id: spawn-0002
role: arcanum-current-state-explorer
mutation: none
claim_ceiling: Public-source inspection proves repository contracts, registered surfaces, and documented local evidence only. It does not prove deployment, production use, broad release quality, or an integrated optimizer.

selector_bound_evidence:
- row_id: ARC-E01
  claim: Arcanum defines a twelve-stage sigil lifecycle from candidate capture through promotion, observation/reflection, and maintenance.
  evidence: arcanum/framework/SIGIL-DEVELOPMENT-WORKFLOW.md:7-22, unique heading "Workflow Overview"
  proof_status: direct
  state_classification: implemented as canonical workflow contract
  presentation_relevance: Use as the lifecycle spine; distinguish contract implementation from execution of every stage.

- row_id: ARC-E02
  claim: Promotion requires structure, validation, and a realistic trial; promotion means usable for learning, not final.
  evidence: arcanum/framework/SIGIL-DEVELOPMENT-WORKFLOW.md:182-193, unique heading "Stage 10 - Promotion"
  proof_status: direct
  state_classification: implemented governance contract
  presentation_relevance: Prevents equating validation or registry presence with finality or deployment.

- row_id: ARC-E03
  claim: Registry release is blocked until validation passes, with manual review allowed only when automation is impractical and explicitly recorded.
  evidence: arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md:51-68, unique heading "Standard Procedure"
  proof_status: direct
  state_classification: implemented governance contract
  presentation_relevance: The release gate is evidence-based but still accommodates named human review.

- row_id: ARC-E04
  claim: Schema validity alone is not execution evidence, promotion evidence, or authority transfer.
  evidence: arcanum/definitions/DEFINITIONS.md:77-114, unique heading "DEF-ARC-SCHEMA: Schema"
  proof_status: direct normative authority
  state_classification: implemented canonical definition
  presentation_relevance: Essential boundary for benchmark types and receipts.

- row_id: ARC-E05
  claim: Development evidence remains non-authoritative until an owning route applies a reviewed change to canonical source.
  evidence: arcanum/definitions/DEFINITIONS.md:280-323, unique heading "DEF-ARC-DEVELOPMENT-ARTIFACT: Development Artifact"
  proof_status: direct normative authority
  state_classification: implemented canonical definition
  presentation_relevance: Separates experiment/reflection output from accepted capability behavior.

- row_id: ARC-E06
  claim: A promotion patch must name source evidence, owner route, selected content, validation, and approval/rejection state.
  evidence: arcanum/definitions/DEFINITIONS.md:396-437, unique heading "DEF-ARC-PROMOTION-PATCH: Promotion Patch"
  proof_status: direct normative authority
  state_classification: implemented canonical definition
  presentation_relevance: Shows that optimization output cannot silently become canonical.

- row_id: ARC-E07
  claim: The public README declares repository-local observability and an experiment harness implemented, while describing their distinct roles: real-use evidence versus controlled validation.
  evidence: arcanum/README.md:50-82, unique headings "Observability Layer" and "Experiment Harness"
  proof_status: direct repository claim, corroborated by architecture/contracts
  state_classification: implemented locally; not deployment proof
  presentation_relevance: Establishes that Arcanum already has evidence capture and repeatable validation surfaces.

- row_id: ARC-E08
  claim: The observability pipeline appends canonical invocation events, indexes them, updates reflection counters, and routes accumulated signals to reflection reports and lifecycle owners.
  evidence: arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md:9-75, unique headings "Current Architecture In One Sentence" and "Component Chart"
  proof_status: direct architecture description
  state_classification: mixed: core pipeline implemented; L4 continuation edge explicitly planned
  presentation_relevance: Visual witness for the current evidence-to-reflection route.

- row_id: ARC-E09
  claim: Direct native skill invocation lacks the deterministic envelope/hook bridge available to legacy slash-command paths.
  evidence: arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md:123-170, unique heading "Direct Skill Path"
  proof_status: direct stated gap
  state_classification: absent
  presentation_relevance: Prevents claiming universal automatic observability for every skill run.

- row_id: ARC-E10
  claim: Continuation-feedback attribution is an L4 future path, not current implemented behavior.
  evidence: arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md:63-68 and 172-181, labels "L4 planned" and "Continuation Feedback Path"
  proof_status: direct
  state_classification: planned/candidate
  presentation_relevance: Useful example of explicit implemented-versus-planned notation.

- row_id: ARC-E11
  claim: Signal Observer derives categorical behavior signals and threshold triggers; it does not compute a scalar quality/reward score.
  evidence: arcanum/arcana/signal-observer/SKILL.md:53-90, unique tags "<process>" and "<authority-rule>"
  proof_status: direct
  state_classification: implemented capability contract
  presentation_relevance: Shows the current telemetry vocabulary: quality pass/gap, anti-pattern, drift, workflow gap, rework, useful pattern, and trigger categories.

- row_id: ARC-E12
  claim: Workflow Reflect groups categorical evidence, evaluates counters/thresholds, and writes improvement proposals without directly mutating the observed sigil.
  evidence: arcanum/arcana/workflow-reflect/SKILL.md:60-130, unique headings "Step 2 - Group Evidence" through "authority-rule"
  proof_status: direct
  state_classification: implemented capability contract
  presentation_relevance: Demonstrates a real improvement proposal loop, but not score-driven edit acceptance.

- row_id: ARC-E13
  claim: Sigil Maintenance Loop is registered as reusable and composes Inventory, Signal Observer, Workflow Reflect, and Sigil Development.
  evidence: arcanum/registry/SPELLS.md:7-22, row "Sigil Maintenance Loop"; arcanum/spells/sigil-maintenance-loop/README.md:1-35
  proof_status: direct
  state_classification: implemented/registered reusable composition
  presentation_relevance: Replaces TO-VLAD3’s older framing of only disconnected primitive machinery with an explicit composed maintenance route.

- row_id: ARC-E14
  claim: The maintenance loop requires explicit user approval before targeted mutation and keeps Inventory and reflection proposal-only.
  evidence: arcanum/spells/sigil-maintenance-loop/README.md:78-110 and 129-152, unique headings "Authority Boundaries", "Execution Phases", and "Gates"
  proof_status: direct
  state_classification: implemented governance contract
  presentation_relevance: Identifies the human-owned change gate.

- row_id: ARC-E15
  claim: Behavior-changing maintenance is not promotion-ready without live runtime evidence; deterministic fixture/contract checks establish structural validity only.
  evidence: arcanum/spells/sigil-maintenance-loop/README.md:179-193, unique heading "Experiment Harness"
  proof_status: direct
  state_classification: implemented gate; evidence for any particular revision remains run-specific
  presentation_relevance: Blocks “validated equals improved/released” overclaims.

- row_id: ARC-E16
  claim: Benchmark schemas support numeric oracle metrics and numeric-or-boolean score components.
  evidence: arcanum/benchmark/src/schemas.ts:57-78, symbols OracleEvidence and ScoreResult
  proof_status: direct code
  state_classification: implemented type surface
  presentation_relevance: Proves score-shaped infrastructure exists, but not one canonical scalar objective.

- row_id: ARC-E17
  claim: The benchmark architecture evaluates coding-agent candidate patches/source changes against upstream oracles; its agent and scoring interfaces are not sigil-maintenance interfaces.
  evidence: arcanum/benchmark/ARCHITECTURE.md:127-177 and 224-234, unique headings "Context View", "Low-Level Components View", and "Dependency Interface View"
  proof_status: direct architecture
  state_classification: mixed: run kernel and SWE-bench Lite bridge documented implemented; broader SmellBench, PerfCodeBench, cloud, and dashboard layers planned
  presentation_relevance: Establishes adjacency, not integration, between benchmark scoring and sigil improvement.

- row_id: ARC-E18
  claim: The benchmark document itself remains status draft despite documenting an implemented official SWE-bench Lite smoke.
  evidence: arcanum/benchmark/ARCHITECTURE.md:1-5 and 66-70
  proof_status: direct
  state_classification: candidate architecture document with bounded implemented witness
  presentation_relevance: Avoid presenting the whole benchmark roadmap as shipped.

implemented_planned_absent_deployed_map:
- implemented:
  - Canonical sigil lifecycle, validation protocol, registry gates, and promotion semantics.
  - Repository-local observability data model and deterministic command/harness observation paths.
  - Signal Observer and Workflow Reflect contracts.
  - Registered Sigil Maintenance Loop with evidence, approval, validation, and residue gates.
  - Experiment-harness support described as implemented for fixture/output/report/observation workflows.
  - Benchmark TypeScript schemas for task, oracle evidence, score components, and telemetry.
  - Benchmark run kernel and one documented official SWE-bench Lite unresolved smoke as bounded plumbing evidence.
- planned_or_candidate:
  - L4 continuation-feedback attribution and active-run pointer.
  - First-class deterministic observation of native `$skill-name` invocations.
  - Broader SmellBench and PerfCodeBench integrations, cloud workers, and dashboard breadth.
  - Any SkillOpt-style offline optimizer, held-out sigil reward surface, or strict score-improvement edit gate.
- absent:
  - A wired path from benchmark ScoreResult to workflow-reflect, sigil-development, or sigil-maintenance-loop.
  - A canonical single scalar reward for sigil quality.
  - A held-out comparison that automatically accepts/rejects sigil edits.
  - A grader-independence field or validator rule in the inspected current sources.
  - A prohibition in the benchmark schema against task/grader self-authorship.
  - Universal deterministic observability across direct native skill selection.
- deployed_or_projected:
  - No inspected source proves external deployment or production operation.
  - `.agents/skills` and `.arcanum/observability` are repository-local discovery/runtime projections, not deployment proof.
  - Registry presence means reusable library availability under governance, not production deployment.

scalar_grader_verdict:
  verdict: NOT WIRED TO SIGIL IMPROVEMENT
  detail: `OracleEvidence.metrics` and `ScoreResult.components` provide numeric score-shaped fields, but the inspected schema does not define one canonical scalar objective. Workflow Reflect and Signal Observer consume categorical statuses, counters, gaps, corrections, and drift. No inspected import, interface, phase, or handoff connects benchmark ScoreResult to reflection, maintenance, edit acceptance, or promotion. TO-VLAD3’s narrow “disconnected” conclusion remains correct, but “a real scalar oracle” should now be phrased more carefully as “numeric component and oracle infrastructure”; the selected live schema alone does not prove one universal scalar reward.

self_authored_grader_verdict:
  verdict: NOT PREVENTED BY CURRENT INSPECTED CONTRACTS
  detail: The benchmark task schema accepts an oracle command and metadata, while ScoreResult accepts arbitrary named numeric/boolean components. No provenance, author identity, held-out-set binding, grader-independence field, or no-self-loop validator appears in the inspected schema or maintenance contracts. Benchmark architecture does protect candidate paths from gold/reference outputs and treats upstream runners/results as grading authority where available, but that is benchmark leakage control, not a general rule that a sigil cannot author its grading surface. Therefore graders can be repository/task authored at the schema level; whether a particular grader is legitimately external is a separate evidence obligation.

promotion_authority:
- Reflection authority: `workflow-reflect` may write proposals/reports and update reflection state, but cannot edit the target sigil.
- Observation authority: `signal-observer` may append telemetry and counters, but cannot prescribe or apply mutation.
- Mutation authority: `sigil-development` may apply only an explicitly user-approved bounded change scope.
- Reusable spell lifecycle owner: `spellcraft`.
- Registry promotion: requires passing validation evidence and lifecycle approval.
- Canonical mutation: must follow the owning route via a reviewed promotion patch.
- Human-owned gates remaining: approval of bounded mutation scope; any explicitly manual validation review; lifecycle approval for registry promotion; acceptance of a promotion patch. No numeric score supersedes these gates.

proposed_demo_witness_and_limits:
- witness: A public-safe split-screen trace using `arcanum/benchmark/src/schemas.ts` symbols `OracleEvidence` and `ScoreResult` beside the registered `arcanum/spells/sigil-maintenance-loop/README.md` phases/gates. The audience can see numeric score-shaped evidence on one side and categorical evidence -> reflection proposal -> human approval -> validation on the other. The absence of a connecting interface is the demonstrable fact.
- supported validation command:
  `find arcanum -path arcanum/.git -prune -o -name "*.md" -print0 | xargs -0 -n1 ./tools/check_markdown_links.sh`
  Source: arcanum/framework/SIGIL-DEVELOPMENT-WORKFLOW.md:158-165.
- optional source-specific neutrality scan pattern:
  `rg -n -i "<project-specific-term>|<source-specific-term>|<legacy-label>" arcanum --glob '!/.git/**'`
  Source: same span; placeholders must be replaced for the presentation context.
- limits:
  - This witness is a source/code trace, not a running optimizer demo.
  - It proves schemas and governance contracts, not end-to-end benchmark execution.
  - Do not claim live optimization, automatic edit acceptance, production telemetry coverage, or deployed self-improvement.
  - The architecture document supplies `python -m swebench.harness.run_evaluation` as an upstream entrypoint, but selected evidence does not supply a complete safe local invocation with all required fixtures, Docker state, and pinned arguments; do not improvise one for the talk.

to_vlad3_drift:
- still_current:
  - Benchmark scoring and sigil improvement remain unwired.
  - Current sigil reflection is categorical/threshold-based and proposal-oriented.
  - Promotion remains human- and multi-criteria-gated.
  - A general grader-independence check remains absent.
- changed_since_2026-06-02:
  - Live public Arcanum now has a registered reusable `sigil-maintenance-loop`, explicitly composing Inventory lookup, observation, reflection, approved update, and validation. TO-VLAD3’s “machinery exists but they do not touch” remains true specifically for scalar benchmark-to-improvement wiring, but it understates the now-explicit non-scalar maintenance composition.
  - Current observability architecture documents concrete implemented command/harness paths and explicitly labels direct-native-skill observation and continuation feedback as gaps/planned work.
  - Benchmark architecture now documents a bounded implemented official SWE-bench Lite smoke and evidence bridge, while retaining draft status and substantial planned integrations.
  - Canonical definitions now sharpen development-versus-canonical evidence and approval/promotion boundaries.
- correction_to_dated_wording:
  - Replace “Arcanum already owns a scalar grading oracle” with “Arcanum contains numeric benchmark oracle/score-component infrastructure.” The inspected `ScoreResult` is a component map plus categorical status, not necessarily one scalar optimization objective.
  - Keep “no scalar wired to sigil improvement.”
  - Keep grader independence as a proposal/residue, not an implemented property.
  - Do not say the optimizer is merely a cheap downstream addition: current sources still lack held-out sigil distributions, reward provenance, edit-generation/acceptance machinery, and integration validation.

blockers:
- No blocker to the current-state audit.
- Presentation/demo blocker: no current source proves an end-to-end scalar sigil optimizer or strict held-out improvement loop.
- Claim blocker: no deployment or production evidence was in the allowed corpus.
- Coverage blocker: direct native skill observability is not deterministic in the documented current architecture.
- Grader-governance blocker: no general grader-independence/provenance contract or validator exists in the inspected sources.
- Evidence blocker for a runnable benchmark demo: the allowed source set does not provide a complete pinned local fixture/runtime command suitable for honest reproduction.
~~~

## Explorer return spawn-0003

~~~text
status: PASS

target_output_ref: receipts/explorer-presentation.json

audience_format_contract:
  language: Portuguese, retaining English technical terms where translation would collapse distinctions
  audience: Advanced practitioners building agents, LLM automations, developer workflows, internal AI platforms, or multi-agent systems
  format: Slides plus code
  duration: 35 minutes maximum
  public_delivery: Recording and slide publication authorized
  evidence_boundary: Presentation research only. No final slides, demo execution, optimizer integration, audience-comprehension proof, promotion, or deployment is established.
  selectors:
    - arcanum/writing/cfp-tdc-arcanum-skillopt.md:19-19
    - arcanum/writing/cfp-tdc-arcanum-skillopt.md:29-47
    - arcanum/writing/cfp-tdc-arcanum-skillopt.md:49-55

thesis_candidates:
  - id: T1
    thesis: "O salto de prompt para infraestrutura acontece quando um comportamento ganha nome, contrato, fixture, evidência operacional e uma autoridade explícita para aceitar mudanças."
    strength: Directly demonstrable with current Arcanum concepts and lifecycle boundaries.
    risk: SkillOpt can become decorative unless its optimizer mechanism is independently source-verified.
  - id: T2
    thesis: "SkillOpt e Arcanum não são equivalentes: SkillOpt investiga como propor e selecionar alterações em estado textual; Arcanum fornece superfícies adjacentes para nomear, testar, observar e governar capacidades."
    strength: Best protection against category collapse and optimizer overclaim.
    risk: Exact SkillOpt wording remains paper-verification-dependent.
  - id: T3
    thesis: "Uma skill que se modifica não é ainda uma capacidade que melhora: melhoria exige um circuito causal observável, fixtures independentes, rejeição de regressões e decisão humana sobre a mutação."
    strength: Strongest practical lesson and demo arc.
    risk: “Fixtures independentes” and the SkillOpt comparison need precise paper evidence before publication.
  recommended: T2, closed with T3
  recommended_wording: "SkillOpt explora a otimização do estado textual de uma skill; Arcanum explora o sistema operacional de engenharia ao redor de capacidades reutilizáveis. A ponte útil não é identidade, mas composição: proposta, teste, observação, reflexão e aprovação continuam sendo responsabilidades distintas."

relationship_map:
  equivalence:
    safe_claim: Both can discuss text that influences an agent’s reusable behavior.
    ceiling: Do not equate a SkillOpt skill state with an Arcanum sigil, spell, capability, registry entry, or promoted artifact.
    proof_status: SkillOpt side unverified in this receipt; Arcanum capability shape locally documented.
  adjacency:
    safe_claim: SkillOpt’s reported edit/evaluation loop is conceptually adjacent to Arcanum’s fixture, validation, observability, and reflection surfaces.
    ceiling: Adjacency does not prove integration or shared implementation.
  complement:
    safe_claim: A verified optimizer could propose candidate edits while Arcanum-owned capabilities preserve evidence, approval, validation, and lifecycle routing.
    proof_status: Proposed architecture, not implemented integration.
  gap:
    safe_claim: No evidence in the permitted corpus proves a SkillOpt-style scalar optimizer, edit policy, rejection buffer, or held-out acceptance loop wired into Arcanum.
    additional_gap: Native Codex skill invocations are not deterministically observed without compatibility routing or manual closeout.
    selector: arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md:164-170,343-357

slide_spine:
  - time: "00:00-02:30 (2.5m)"
    seed: "A resposta boa desaparece; o método reutilizável é o ativo."
    job: Establish the engineering problem with one prompt-before/after contrast.
  - time: "02:30-05:30 (3m)"
    seed: "Do prompt à capacidade: nome, fronteira, contrato e próximo dono."
    job: Define prompt versus reusable capability without introducing optimizer claims.
  - time: "05:30-09:00 (3.5m)"
    seed: "Vocabulário que não pode colapsar."
    job: Separate skill state, sigil, spell, fixture, observation, reflection, acceptance, promotion.
  - time: "09:00-13:00 (4m)"
    seed: "SkillOpt: mecanismo reportado e limite da nossa evidência."
    job: Present only claims independently verified by the SkillOpt explorer; label results paper-reported, not reproduced.
  - time: "13:00-17:00 (4m)"
    seed: "Arcanum hoje: contrato, harness e observabilidade."
    job: Show public local architecture and the current direct-skill observation gap.
  - time: "17:00-20:00 (3m)"
    seed: "Equivalência, adjacência, complemento e gap."
    job: Use a four-column comparison, with “integração” explicitly absent.
  - time: "20:00-28:00 (8m)"
    seed: "Demo mínima: prompt → capability → fixture → observation → controlled improvement."
    job: Run or transparently simulate the bounded witness below.
  - time: "28:00-31:00 (3m)"
    seed: "Onde a máquina para."
    job: Show reflection proposal, human approval gate, validation, and promotion ceiling.
  - time: "31:00-33:00 (2m)"
    seed: "Teach-back: você consegue recontar a cadeia?"
    job: Ask the three audience questions below.
  - time: "33:00-35:00 (2m)"
    seed: "Takeaway e convite."
    job: End on composition, not self-evolution.
  total: 35m

source_to_slide_rows:
  - slide_seed: "Audience and delivery contract"
    claim: "The accepted proposal targets an advanced Portuguese 35-minute slides-and-code talk."
    selector: arcanum/writing/cfp-tdc-arcanum-skillopt.md:29-47
    proof_status: locally_observed_contract
  - slide_seed: "Prompt is not infrastructure"
    claim: "An Arcanum capability states use, non-use, reasoning, failure, outputs, observation, and lifecycle ownership."
    selector: arcanum/writing/substack/introducing-arcanum.md:16-30
    proof_status: public_draft_framing
  - slide_seed: "Capability lifecycle"
    claim: "The public framing separates definition, design, implementation, validation, observation, reflection, and revision."
    selector: arcanum/writing/substack/introducing-arcanum.md:91-110
    proof_status: public_draft_framing
  - slide_seed: "Sigil versus spell"
    claim: "Sigils are tiered reusable capabilities; spells compose capabilities and own ordering, shared state, artifacts, gates, and overall observation."
    selector: arcanum/README.md:125-146
    proof_status: locally_observed_public_source
  - slide_seed: "Implemented Arcanum surfaces"
    claim: "The repository declares implemented observability and experiment-harness support."
    selector: arcanum/README.md:50-82
    proof_status: implementation_claim_in_public_source_not_executed_here
  - slide_seed: "Fixture is evidence, not prose"
    claim: "Validation requires realistic positive and negative fixtures, expected outputs, execution method, gates, observability, and verdict."
    selector: arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md:18-49
    proof_status: locally_observed_contract
  - slide_seed: "Reproducibility and simulation"
    claim: "A dry run must bind fixture inputs, expected outputs, outcome, command, captured result, and execution mode; contract simulation must be labeled."
    selector: arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md:70-98
    proof_status: locally_observed_contract
  - slide_seed: "Harness causal chain"
    claim: "Experiment Harness selects one prompt, captures output, validates contract evidence, reports, and can append an observability signal."
    selector: arcanum/arcana/experiment-harness/SKILL.md:47-68
    proof_status: locally_observed_capability_contract_not_executed
  - slide_seed: "Harness semantic limit"
    claim: "The first implementation uses structured-section and keyword checks; semantic judging is future-layer language."
    selector: arcanum/arcana/experiment-harness/SKILL.md:62-68
    proof_status: locally_observed_limitation
  - slide_seed: "Observation boundary"
    claim: "Observability records and routes evidence; it does not decide capability meaning or mutate capabilities."
    selector: arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md:215-240
    proof_status: locally_observed_architecture
  - slide_seed: "Direct-skill gap"
    claim: "The documented direct Codex skill path lacks a deterministic hook bridge equivalent to the command hook."
    selector: arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md:164-170
    proof_status: locally_observed_documented_gap
  - slide_seed: "Controlled improvement"
    claim: "Observation records evidence, reflection proposes, and sigil-development mutates only within approved scope."
    selector: arcanum/spells/sigil-maintenance-loop/README.md:80-110
    proof_status: locally_observed_spell_contract_not_executed
  - slide_seed: "Human gate"
    claim: "A bounded user-approved mutation scope is required; absence of approval blocks mutation."
    selector: arcanum/spells/sigil-maintenance-loop/README.md:130-150
    proof_status: locally_observed_gate
  - slide_seed: "Promotion ceiling"
    claim: "Fixture checks can show structural validity, but behavior-changing revisions need live runtime evidence before being called promotion-ready."
    selector: arcanum/spells/sigil-maintenance-loop/README.md:191-193
    proof_status: locally_observed_claim_ceiling
  - slide_seed: "SkillOpt bridge"
    claim: "SkillOpt reportedly treats a skill as external textual state and proposes controlled edits without changing model weights."
    selector: arcanum/writing/cfp-tdc-arcanum-skillopt.md:17-19
    proof_status: proposal_claim_pending_primary_paper_verification

minimum_code_demo_witness:
  demo_status: PROPOSED_AND_UNEXECUTED
  target_capability: experiment-harness
  input_prompt_exact: "Analise este plano de implementação e devolva exatamente: Objetivo, Riscos, Gate de execução e Próximo dono. Se não houver critério de aceite, retorne BLOCK em Gate de execução."
  fixture_proposed:
    id: tdc-missing-acceptance-001
    input_state: C0_BASELINE_CONTRACT
    fixture_body: "Plano: adicionar cache ao agente. Etapas: implementar e publicar."
    expected_output_fields:
      - "Objetivo: adicionar cache ao agente"
      - "Riscos: publicação sem critério verificável"
      - "Gate de execução: BLOCK — critério de aceite ausente"
      - "Próximo dono: autor do plano"
    expected_validation_state: V0_EXPECTED_BLOCK
  live_sequence:
    - state: D0_PROPOSED
      action: Place the exact prompt and fixture in an artifact-local development harness.
      status: proposed
    - state: D1_RUN
      action: Run exactly one selected example through the native capability surface.
      expected_observation: A real artifact body is captured; empty or save-summary output blocks.
      selector: arcanum/arcana/experiment-harness/SKILL.md:47-59,101-118
      status: proposed_not_executed
    - state: D2_VALIDATE
      action: Validate required fields, Quality Bar status, anti-pattern hits, and workflow gaps.
      expected_machine_labels:
        QUALITY_BAR_STATUS: partial_or_fail
        ANTI_PATTERN_HITS_JSON: '["missing_acceptance_criterion"]'
        WORKFLOW_GAPS_JSON: '["gate_reason_not_explicit"]'
      caveat: These exact values are presentation fixtures, not current observed output.
      status: proposed_not_executed
    - state: D3_OBSERVE
      action: Convert the report into one observer-compatible signal.
      expected_state: OBSERVED_GAP
      status: proposed_not_executed
    - state: D4_REFLECT
      action: workflow-reflect proposes adding an explicit missing-acceptance rule.
      expected_state: TARGETED_UPDATE_PROPOSED
      status: proposed_not_executed
    - state: D5_HUMAN_GATE
      action: Presenter displays APPROVE or REJECT; no file changes occur without bounded approval.
      expected_state: AWAITING_APPROVAL
      status: demonstrable_as_control_flow; no repository mutation authorized
    - state: D6_RERUN
      action: If separately approved and implemented, rerun the same positive and negative fixtures and reject regression.
      expected_state: ACCEPTED_CANDIDATE or REJECTED_CANDIDATE
      status: proposed_not_implemented
  fallback_demo:
    trigger: Live model call, hook, or observability path fails.
    method: Use a pre-captured, public-safe terminal transcript only if generated and verified before the talk; otherwise perform a contract dry-run and visibly label it SIMULAÇÃO DE CONTRATO.
    witness: Walk the exact fixture, expected result, gate table, and proposed state transition without claiming runtime execution.
    selector: arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md:51-68,70-98
    safety: Never substitute invented terminal output for captured execution.

teach_back_questions:
  - "Qual é a diferença entre a skill textual que um otimizador edita e o sigil que possui contrato e ciclo de vida?"
  - "Qual artefato prova comportamento: o contrato, a fixture, o relatório de validação ou a telemetria? O que cada um não prova?"
  - "Depois que a reflexão propõe uma mudança, quem pode autorizar a mutação e que evidência ainda falta para promoção?"

likely_misconceptions:
  - "Arcanum implementa SkillOpt." Correction: no integration evidence in the permitted corpus.
  - "Sigil é apenas outro nome para prompt." Correction: the contract includes boundaries, outputs, failure, observation, and lifecycle ownership.
  - "Telemetry is a grader." Correction: it records/routes evidence; it does not own semantic judgment or mutation.
  - "Fixture pass means production-ready." Correction: fixture evidence is bounded; live evidence and lifecycle approval remain distinct.
  - "Reflection automatically edits." Correction: reflection proposes; approved sigil-development owns bounded mutation.
  - "Implemented observability means every native skill run is observed." Correction: the direct-skill hook gap is explicitly documented.
  - "Paper-reported results were reproduced locally." Correction: they were not reproduced by this action.

cuts:
  - Cut the complete Cyber Alchemy Method anchor taxonomy if timing slips; retain only Objective, Evidence, Gate, Next owner.
  - Cut tier taxonomy beyond the one-line sigil/spell distinction.
  - Cut registry and installation walkthroughs.
  - Cut benchmark architecture unless the primary synthesis finds it essential to a verified SkillOpt comparison.
  - Cut all paper result tables except one verified mechanism figure and one verified limitation.
  - Never cut the four-way relationship map, demo state labels, human approval gate, or direct-skill observation gap.

public_private_safety:
  - Use only public Arcanum paths and freshly authored neutral examples.
  - The CFP’s section explicitly labeled “Mensagem privada” is audience/intent evidence, not slide-ready prose; do not quote or publish it without owner review.
  - Do not copy content from the private Inventory presentation precedent; reuse only its abstract structure of timed retell, witness, and claim ceiling.
  - Do not expose `.arcanum/observability/` real payloads, prompts, paths, identities, or repository-local telemetry in slides. Use synthetic fixtures and redacted schema-shaped examples.
  - Do not describe DomainSpec, Saturn, private ontology, or private authority artifacts.
  - Describe Arcanum as public experimental infrastructure; do not imply optimizer integration, autonomous self-improvement, promotion, deployment, or production proof.

blockers:
  - Primary SkillOpt paper evidence, exact selectors, results, limitations, and related-work positioning are outside this action’s verified corpus and must come from the dedicated primary-source explorer.
  - No minimum demo fixture, captured run, report, or observability event has been executed for this talk.
  - No evidence proves the proposed exact machine labels are emitted by a current runner; they are presentation fixture expectations.
  - No rehearsal proves the demo fits eight minutes or that the full talk achieves audience comprehension.
  - Before final slides, the owner must choose whether the demo is live, pre-captured, or contract-simulated and label it accordingly.
~~~
