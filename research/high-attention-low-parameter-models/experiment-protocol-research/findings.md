# Findings: high-attention experiment protocol research

Dispatch: `2026-07-18-high-attention-experiment-protocol-research`

## Answer and status

**Research is sufficient as decision-ready input to author a later experiment specification. Execution is blocked.** There is no materialized generator/data split, tested renderer/scorer, admitted checkpoint set, frozen runtime, KV-capacity witness, sample allocation, or numeric decision rule; therefore this artifact is not a specification, preregistration, executable protocol, benchmark implementation, capacity proof, or experiment run. [Platform evidence](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18) and [internal-validity requirements](research.md#gerd-gigerenzer--internal-validity-and-inference) support those distinctions.

## Evidence and claim boundary

Labels used below:

- **Source-backed fact** — stated or supported by cited external evidence preserved in the explorer transcript.
- **Synthesis** — a bounded combination of explorer findings; not itself an external fact.
- **Recommendation** — a proposed design rule for the later specification.
- **Project choice (unfrozen)** — a candidate default that has not been authorized or frozen.
- **Unresolved gate** — an obligation that must close before execution or a named claim.

**Source-backed facts.** Long-context performance varies by task complexity, length, and evidence position; benchmark conclusions also vary with experimental choices, so a single aggregate or needle result cannot establish generic usable context. Comparative systems work should report quality beside resource measures and must declare its energy/cost boundary. [Workload evidence](research.md#shannon--workloadcontent-matrix-research), [inference evidence](research.md#gerd-gigerenzer--internal-validity-and-inference), [budget evidence](research.md#simon--herbert--budgeted-comparison-matrix-research)

As checked on 2026-07-18, vLLM 0.25.1 listed the relevant Llama and Phi architecture classes, but architecture support and advertised 128K context do not prove exact checkpoint/template/backend compatibility, resident KV capacity, or successful information use. [Platform evidence](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18)

**Claim boundary.** Synthetic fixtures can isolate fixture-level behavior, not an internal attention mechanism. Dense resident KV is an implementation condition, not evidence of effective use. The Llama 1B/3B pair is a within-family checkpoint comparison, not parameter causality; Phi is an external-family comparator, not a replicate. A causal parameter claim would require matched training pipelines and independent training replicates. [Internal-validity evidence](research.md#gerd-gigerenzer--internal-validity-and-inference), [platform candidates](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18)

T0 means project-generated, not automatically license-clean. Generator, filler, template, tokenizer, runtime dependency, upstream data, and redistributed artifacts still require manifested provenance and licenses. [Workload evidence](research.md#shannon--workloadcontent-matrix-research)

## Four ownership surfaces

| Surface | Owns for the later specification | Must not silently decide |
|---|---|---|
| Workload/content | Fixture semantics, task coverage, evidence/decoy placement, rendering, output grammar, data provenance, and deterministic scoring. [Workload explorer](research.md#shannon--workloadcontent-matrix-research) | Runtime/backend, inferential thresholds, resource frontier policy. |
| Execution-platform | Immutable checkpoint/tokenizer/template/runtime identities; KV policy and capacity admission; warmup, cache, hardware, and systems telemetry. [Platform explorer](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18) | Task meaning, sample size, acceptance margins, or causal interpretation. |
| Internal-validity/inference | Experimental unit, pairing/blocking/randomization, controls, uncertainty, multiplicity, scorer validation, and claim/falsification language. [Inference explorer](research.md#gerd-gigerenzer--internal-validity-and-inference) | Workload content, platform compatibility, or deployment constraint. |
| Budgeted comparison | Fixed-cell fairness, actual-work accounting, feasibility outcomes, Pareto axes, phased pruning, and value-of-information termination. [Budget explorer](research.md#simon--herbert--budgeted-comparison-matrix-research) | Content coverage, inferential thresholds, or a single composite winner score. |

## Repaired constructs and estimands

| Construct/estimand | Required meaning and boundary |
|---|---|
| Present tokens | Exact post-template token sequence/count supplied; says nothing about retention or use. [Workload explorer](research.md#shannon--workloadcontent-matrix-research) |
| KV-retained tokens | Frozen runtime plus capacity witness establishes resident KV; says nothing about effective attention/use. [Platform explorer](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18) |
| Retrieval-selected tokens | Exact tokenized documents in a recorded retrieval receipt; not equivalent to raw visibility. [Inference explorer](research.md#gerd-gigerenzer--internal-validity-and-inference) |
| Successful information use | Correct answer and separately correct evidence provenance where evidence is required; fixture-level outcome, not a general mechanism claim. [Workload](research.md#shannon--workloadcontent-matrix-research), [inference](research.md#gerd-gigerenzer--internal-validity-and-inference) |
| Full-context retention | `S_full - S_compact`, where compact contains identical answer evidence; test non-inferiority `>= -epsilon` or a frozen ratio `>= rho`. Full context need not beat compact context. **Project choice:** scale and margin remain unfrozen. [Strict-control rationale](research.md#gerd-gigerenzer--internal-validity-and-inference) |
| Added-evidence behavior | Paired evidence-present support and evidence-absent abstention; do not subtract raw scores whose correct-output semantics differ. [Negative-control rationale](research.md#gerd-gigerenzer--internal-validity-and-inference) |
| Direct checkpoint contrast | Paired `S_3B - S_1B`; difference-in-retention is mandatory for any claim that one checkpoint *uses long context better* rather than performs better generally. [Inference explorer](research.md#gerd-gigerenzer--internal-validity-and-inference) |
| Middle loss | `S_middle - mean(S_early, S_late)` on rotations of the same instance; tolerance remains unfrozen. [Position evidence](research.md#gerd-gigerenzer--internal-validity-and-inference) |
| False support | Erroneous support assertions divided by eligible evidence-absent or contradiction controls; report separately. [Negative controls](research.md#gerd-gigerenzer--internal-validity-and-inference) |
| Answer/evidence outcomes | Report separately; any product/joint score is diagnostic unless a binary joint-success outcome is frozen in advance. [Workload metrics](research.md#shannon--workloadcontent-matrix-research) |
| Resource frontier | Name measured axes; weak dominance means no worse on every named axis and better on at least one; show uncertainty and infeasible cells. Do not collapse capability, latency, energy, cost, and parameters into one primary score. [Budget explorer](research.md#simon--herbert--budgeted-comparison-matrix-research) |

## Smallest coherent specification target

**Recommendation/synthesis:** specify a paired Llama 1B/3B checkpoint comparison on procedural literal-retrieval, two-hop-tracing, and contradiction fixtures. Rotate identical evidence and decoys through early/middle/late positions. Include compact evidence-complete, full evidence-complete, evidence-absent/added-evidence, no-answer, oracle-selection, and retrieved-selection arms; the later spec may defer oracle/retrieved arms unless it states the decision each can change. Report answer, evidence, false support, feasibility, prefill, decode, and GPU-energy fields separately. Use paired instance-level inference for full-context non-inferiority, direct checkpoint contrast, and added-evidence behavior. Start, if admitted, on one dedicated single-H100 stack and state that the result is stack-specific. [Workload matrix](research.md#shannon--workloadcontent-matrix-research), [minimal comparative design](research.md#gerd-gigerenzer--internal-validity-and-inference), [platform matrix](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18)

**Project choices (all unfrozen):** 4K/64K initial lengths; one interference level; BF16 weights and full-retention KV; greedy decoding; GPU-only pilot energy; exact task/output budgets; and gate ordering. A 128K cell is inadmissible without an exact post-template fit and per-model resident-KV witness. Raw-versus-RAG must distinguish frozen receipts (selection-only comparison) from live retrieval whose indexing, retrieval, reranking, retries, and prompt construction are charged. [Platform admission conditions](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18), [budget fairness rules](research.md#simon--herbert--budgeted-comparison-matrix-research)

## Mandatory closure before any run

- [ ] Versioned generator; filler/data provenance and license manifest; frozen family-level splits; semantic plans and fixture hashes. [Workload requirements](research.md#shannon--workloadcontent-matrix-research)
- [ ] Versioned renderer and tested deterministic scorer; output grammar; rendered-byte/token-ID hashes; tokenizer/template hashes. [Workload requirements](research.md#shannon--workloadcontent-matrix-research)
- [ ] Authorized immutable checkpoint snapshots with complete inventories/hashes and checkpoint/template/backend smoke tests. [Platform requirements](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18)
- [ ] Runtime image digest; backend, chunk, driver, CUDA, package, hardware, cache, precision, and KV-policy manifest. [Platform requirements](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18)
- [ ] Per-model/length resident-KV capacity witness proving no truncation, offload, preemption, fallback, recomputation, or OOM recovery. [128K admission conditions](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18)
- [ ] Frozen experimental unit, `N`, allocation, repetitions, master seed, exclusions/failure codes, precision and power rationale, and paired/clustered analysis. [Inference requirements](research.md#gerd-gigerenzer--internal-validity-and-inference)
- [ ] Numeric `epsilon`/`rho`, direct-checkpoint margin, middle tolerance, false-support ceiling, scorer threshold, primary outcome family, and multiplicity rule. [Inference requirements](research.md#gerd-gigerenzer--internal-validity-and-inference)
- [ ] Retrieval role/accounting, energy and cost boundary, deployment constraint, frontier axes, trial schema, raw-output retention, and manifest validator. [Budget requirements](research.md#simon--herbert--budgeted-comparison-matrix-research)

Every applicable box is an **unresolved gate**. No run should start while one remains open.

## Staged escalation

| Stage | Decision target | Escalate only if |
|---|---|---|
| A — measurement pilot | Harness comparability and short/long systems behavior for one candidate plus shared comparator | Instrumentation validates and at least one arm is feasible at the long bin. |
| B — decision pilot | Whether any arm reaches the capability/resource frontier; add size comparator and one alternative mechanism | A non-dominated arm appears or normalization views reverse the apparent ranking. |
| C — focused study | Where frontier mechanisms fail across position, interference, and reasoning; add full-SUT energy and dated cost | The distinction can change a design/deployment decision. |
| D — confirmation | Portability on an independent hardware/runtime setting | The intended claim extends beyond the measured stack. |

This is a sequential recommendation, not a frozen matrix. Before each queued run, name the decision it could change; stop an arm when no remaining cell can change feasibility, Pareto membership, a normalization-rank reversal, or a mechanism-specific explanation. Never prune the shared comparator, first long-bin feasibility test, prefill/decode split, raw capability, or manifest/measurement-boundary ledger. [Phased budget and termination](research.md#simon--herbert--budgeted-comparison-matrix-research)

## Unresolved human decisions

The specification owner must choose: target claim and scope (family-specific or generalized); retention scale and `epsilon`/`rho`; direct checkpoint contrast and margin; middle tolerance; false-support ceiling; primary family/multiplicity; `N`, power, repetitions, and budget; initial tasks, lengths, interference, and output limits; oracle/retrieved-arm purpose; retrieval implementation/accounting; Phi phase; backend/chunk/incompatibility policy; energy/system and cost boundary; frontier axes and binding deployment constraint; QASPER versus HotpotQA and packaging/license treatment; filler provenance and contamination controls; and any qualitative-scorer validation protocol. [Workload unresolved choices](research.md#shannon--workloadcontent-matrix-research), [platform unresolved choices](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18), [inference unresolved choices](research.md#gerd-gigerenzer--internal-validity-and-inference), [budget unresolved choices](research.md#simon--herbert--budgeted-comparison-matrix-research)

## Verdict matrix

| Gate/claim | Verdict | Consequence |
|---|---|---|
| Precedent | **CONDITIONAL PASS** | A later spec may proceed only while external precedent, dated platform fact, project choice, and admission gate remain separately typed. |
| Runnable witness | **KILL** | No executable experiment exists; missing artifacts, admission evidence, allocation, and thresholds are blockers. |
| Prior positive full-minus-compact “usable context” formulation | **KILL** | It must not return. Use retention/non-inferiority, added-evidence behavior, direct checkpoint contrast, middle loss, and false-support estimands. |
| Decision-ready research/specification input | **SURVIVES** | The repaired candidate is sufficient to author and review a later specification, not to execute. |

## Explicit reviewer carry-forwards

- Keep T0 provenance/license obligations, comparator-only Llama language, external-family Phi language, architecture-support versus compatibility, all negative/selection controls, and the fixture-level—not mechanism-level—claim boundary.
- Preserve the runnable-witness KILL until generator/data, renderer/scorer, checkpoint admission, runtime/backend, KV witness, `N`/repetitions, and numeric thresholds exist.
- Compute retention separately for named answer and evidence scales, or freeze a binary joint-success outcome.
- Require difference-in-retention for any “uses long context better” checkpoint claim.
- Define added-evidence behavior as paired evidence-present support plus evidence-absent abstention, not a raw subtraction across different correct-output semantics.
- In the later spec, justify oracle and retrieved arms as decision-bearing secondary contrasts or defer them.

These are synthesis carry-forwards grounded in the [workload](research.md#shannon--workloadcontent-matrix-research), [platform](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18), [inference](research.md#gerd-gigerenzer--internal-validity-and-inference), and [budget](research.md#simon--herbert--budgeted-comparison-matrix-research) returns.

## Execution note and closeout

The dispatch owner reports that four explorers were capacity-launched `3+1`; all four completed before synthesis. The evidence boundary contains the four completed returns: [Shannon](research.md#shannon--workloadcontent-matrix-research), [Hewitt](research.md#explorer-2-hewitt-carl--execution-platform-matrix-2026-07-18), [Gigerenzer](research.md#gerd-gigerenzer--internal-validity-and-inference), and [Simon](research.md#simon--herbert--budgeted-comparison-matrix-research).

```yaml
exit_reason: resolved
audit: approved
agents_spawned:
  planned: 10
  actual:
    total: 10
    tree:
      explorer: 4
      synthesizer: 1
      skeptic: 3
      writer: 1
      auditor: 1
      helpers: 0
    loops_used: 1
```

The auditor approved the findings, and the dispatch resolves as decision-ready research; execution remains blocked.
