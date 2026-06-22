# Findings: CyberAlchemy Product Architecture, Wedge, Moat, And First Proof Slice

## One-Line Answer

CyberAlchemy has enough existing material to plan from a candidate corpus, but not enough to claim a runtime, a market-proven product, or an auditor-accepted moat. The right next move is to prove one concrete SDLC change workflow: `spec -> sandboxed agent implementation -> derived tests -> alignment audit -> human gate -> merge -> ledger entry`, with the internal loop `source -> inventory -> ontology candidate -> context pack -> execution -> telemetry/reflection` serving that buyer-visible workflow rather than becoming the product story by itself. [R1][R3][R4][R8][R10]

## Verdict Matrix

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
| --- | --- | --- | --- | --- | --- |
| Existing CyberAlchemy planning corpus | Internally owned corpus mapped by R1; candidate authority only. | Yes, as scattered source documents, source digests, work-layer slices, and architecture drafts. | Sound if called a candidate planning corpus, not a governed runtime substrate. | GO | Already-deployed as planning material; not runtime proof. [R1][R3][R10] |
| First SDLC readiness wedge | Internally framed in commercialization synthesis and supported by R4's buyer job. | Partially: workflow is specified, but no pilot metrics or case study yet. | Sound only when named as a concrete SDLC change workflow. | GO | Pilot hypothesis; requires measurement before market claims. [R4][R7][R9][R10] |
| Paid attestation moat | Internally proposed in R6; adjacent categories already owned by SCM, observability, and GRC incumbents in R7. | No paid witness yet: bundle, verifier, enforcement surface, auditor export, and buyer acceptance are missing. | Sound as a paid enforcement/signing/verifier/export hypothesis, not as a proven moat. | GO | Prototype candidate; claim <= signed bundle and acceptance evidence. [R6][R7][R8][R9][R10] |
| First proof-bearing implementation slice | Internally specified across R1-R3. | Not yet: proof artifacts have not been generated. | Sound if bound to the SDLC change artifact and checked for hidden authority. | GO | Next implementation plan, not proof of correctness. [R1][R2][R3][R8][R9] |

## Evidence Vocabulary

This artifact uses "evidence" in five distinct senses and should not let one sense substitute for another:

| Evidence Type | Meaning | Current State |
| --- | --- | --- |
| Source/provenance evidence | Original docs, source digests, line references, content hashes, and source roles. | Present but scattered; inventory adaptation still needed. [R1][R3] |
| Inventory and ontology evidence | Typed inventory entries, contradictions, confidence, ontology candidates, and promotion state. | Candidate-only until inventory and ontology-harness run. [R1][R2][R3][R10] |
| Execution telemetry | Route, stage, terminal outcome, child-run, signal, and reflection rows. | Existing primitives are partial; unified vocabulary and route bridge are missing. [R2][R6][R8] |
| Gate and approval receipts | Human intent decisions, route approvals, blocks, merge decisions, and ledger receipts. | Required for the wedge; not yet demonstrated in one full workflow. [R4][R6][R9] |
| Pilot outcome evidence | Review-time, escaped-intent-bug, skip-resistance, acceptance, and buyer/auditor feedback. | Missing; no market or auditor claim should rely on it yet. [R4][R7][R9] |

## Strategic Read

CyberAlchemy is best treated as a candidate planning corpus plus a first-loop substrate hypothesis, not as a completed runtime or market-proven product. [R1][R3][R10] The useful strategic move is therefore not to broaden the platform claim, but to prove one narrow loop where human intent, agent execution, source/provenance evidence, execution telemetry, gate receipts, and review-gated learning remain visible. [R1][R3][R4][R6]

The product promise should stay modest and concrete: make one AI-assisted SDLC change workflow inspectable enough to pilot, then test whether its receipts can become signed attestation inputs. [R4][R6][R9] The candidate paid moat is not "AI governance" in general, because that category is crowded and incumbents already have observability, audit logs, workflow distribution, and governance mappings. [R7][R8] The paid hypothesis is narrower: enforcement, signing, verification, and export around cross-tool evidence of how one SDLC change was specified, executed, reviewed, approved, and preserved. [R6][R7][R8][R10]

The collapse test is simple: if the first slice cannot produce a named SDLC change artifact, derived tests, a gate decision, terminal execution telemetry, ledger receipts, and a failed/bypassed-case check, then the architecture remains planning prose rather than product substrate. [R3][R4][R6][R8][R9]

## Existing-Substrate Map

The current CyberAlchemy corpus contains a candidate definition baseline, architecture draft, implementation layering, ontology pack, inventory/ontology pipeline, first-working-slice packet, work-layer slices, and source digests. [R1] The definition baseline is the most authoritative current vocabulary source, but it is still a candidate baseline rather than a canonical ontology promotion. [R1][R3] The architecture draft is useful substrate for planning, but it should defer to the definition/glossary vocabulary until reconciled. [R1]

The ontology pack is candidate-only: it has source digests and one candidate authority-ladder entry, but source digests are provenance evidence rather than final authority. [R1][R3][R10] The work layer is the most plannable surface because it breaks the system into slices for inventory foundation, ontology entry contract, promotion rules, candidate operational lessons, memory/context, execution feedback, and the first working loop. [R1][R10]

The core operating thesis is already clear: CyberAlchemy should keep `intent <-> execution <-> evidence` connected, name drift, correct it, preserve it as evidence, and use it to improve future agent knowledge. [R1] The practical first loop is also already named: `source -> inventory -> ontology candidate -> context pack -> execution -> telemetry/reflection`. [R1][R2][R10] This loop is the proof target and the substrate-building mechanism, not evidence that the runtime is already complete. [R1][R3][R8]

Several substrate gaps remain unresolved: output roots for generated inventory/ontology artifacts, inventory install/adaptation, initial typed entries, ontology-harness validation, context-builder proof, routed execution, telemetry/reflection closeout, candidate operational-lesson schema, privacy/redaction policy, signal vocabulary, context-retrieval card mechanics, replay verification, tamper checks, and buyer-visible workflow proof. [R1][R2][R3][R8][R9][R10]

## How The Pieces Can Be Assembled

The system should be assembled as a loop of planes, not as one monolithic runner. [R2] Necronomicon can act as the control shell that loads memory, gaps, capability manifest, and route history, then routes bounded work to the owning capability while preserving no-promotion guardrails. [R2] Inventory should be the provenance substrate where raw sources stay immutable and generated summaries, indexes, tags, contradictions, and provenance become reusable planning material. [R2][R3][R10]

Ontology Harness should sit after inventory, composing inventory, ontology-vault, and context-builder so that source/provenance evidence can become reviewed ontology candidates without turning raw memory into authority. [R2][R3][R10] Context Builder should then adapt selected evidence into obligation-linked, task-sized context packs rather than dumping the whole repository into execution. [R2][R3]

The route plane should use `orchestrate` for native routing and `dispatch-spec` for route-shape validation, with the important caveat that `dispatch-spec` validates route graphs, handoffs, gates, observability, and subagent strategy but does not execute or promote knowledge. [R2] The execution plane can borrow from DomainSpec's Agent Execution Orchestrator model, which already defines route templates, stage contracts, execution runs, terminal outcomes, telemetry envelopes, retries, cancellation, and audit-oriented interfaces. [R2]

The feedback plane should use Observed Invocation Loop, Signal Observer, and Workflow Reflect to turn execution results into telemetry, reflection counters, operational lesson candidates, and maintenance proposals. [R2][R6] Promotion must remain named and gated: telemetry and memory may create candidates, but authority changes require inventory evidence, ontology review, decision gates, and privacy/policy gates when behavior, policy, architecture, or capability contracts change. [R3][R6][R10]

The main missing adapters are concrete Arcanum-route-to-AEO route mapping, a unified OIL/AEO telemetry schema bridge, inventory/ontology bootstrap, subagent lifecycle reconciliation with child run IDs and terminal outcomes, and a coverage matrix mapping each attestation event to real files or explicit gaps. [R2][R6][R9]

## Product Architecture Decomposition

The architecture is a governed agentic knowledge/execution stack whose practical purpose is to reduce residue between human intent, system schema, execution behavior, and observed facts. [R5] "Reduce residue" is not yet an outcome claim; it needs a metric, baseline, target threshold, and a witnessed mismatch where the system detects and corrects drift. [R4][R5][R7][R9]

These nine planes are an architecture decomposition, not nine buyer-visible product modules:

| Plane | Product Role | Boundary |
| --- | --- | --- |
| Philosophy / Intent | Defines the CyberAlchemy lens of symmetry, drift, convergence, and residue reduction. | Does not own runtime mechanics. [R5] |
| Promotion / Authority Rules | Controls ontology branches, confidence, promotion, review, decision gates, and no-automatic-promotion discipline. | Should not be described as generic governance without named mechanisms. [R3][R5][R10] |
| Inventory | Converts scattered source material into reusable source/provenance entries, tags, indexes, contradictions, and provenance. | Does not decide final meaning or route authority. [R2][R5] |
| Candidate Operational-Lesson Branch | Candidate branch for route knowledge, lessons, failures, context-retrieval cards, and maintenance proposals. | Not distinct from memory/telemetry until schema, storage, query behavior, and promotion rules are proven. [R1][R3][R5][R10] |
| Memory / Context | Preserves continuity, route history, workflow hints, and session residue. | Emits candidates only; it does not become canonical alone. [R1][R5] |
| Candidate Context-Retrieval Cards | Intended pattern for mapping task fingerprints to recommended route, evidence, pitfalls, confidence, and expiry. | Mechanics and buyer-visible routing improvement remain undefined. [R1][R2][R3][R5][R10] |
| Execution | Routes and runs bounded work through skills, sigils, spells, task-session, Necronomicon, and AEO-style contracts. | The broader orchestrator bridge is not finished. [R2][R5] |
| Observability / Learning | Converts execution into telemetry, signals, reflection, lesson candidates, and improvement proposals. | Does not mutate capabilities without review. [R2][R5][R6] |
| Research / Decision | Tests contested choices against evidence, objectives, and decision gates. | Should not become market proof without measured pilot evidence. [R4][R7][R9] |

The implementation progression should follow the existing L0-L6 sequence: define baseline, ontology shape, memory bridge, signal bridge, retrieval behavior, maintenance loop, and research validation. [R1][R5] The next bounded architecture move is L1 ontology-shape work, especially candidate operational-lesson fit, while runtime storage, automated retrieval, privacy enforcement, signal ingestion, capability mutation, and full product surface remain deferred. [R1][R3][R10]

## Free Wedge

The free wedge should be a narrow, buyer-visible service outcome: pilot one SDLC change workflow where agentic work becomes inspectable. [R4][R9][R10] The offer should not lead with Arcanum, Craft, validators, CyberAlchemy vocabulary, or a platform story. [R4] The buyer-facing job is: help a team put agents into its SDLC without multiplying intent bugs or damaging change-control and audit trust. [R4]

The first packaging should be a fixed 2-4 week AI-dev readiness sprint: map one SDLC workflow, define "done correctly," then build a Phase 1 MVP loop of `spec -> sandboxed agent implementation -> derived tests -> alignment audit -> human gate -> merge -> ledger entry`. [R4] The mandatory framing is to relocate and legibilize human intent review, not reduce or bypass it. [R4][R7]

The free surface can include validators, audits, spec-to-test derivation, extraction, taxonomies, Arcanum sigils, Necronomicon, Craft ledger schema/type/lane/blocker discipline, and intent tools. [R4][R7] These are adoption tools and trust-building proof surfaces, not the paid meter. [R4][R7][R8]

The free proof obligation is measurement, not rhetoric. [R4] The first proof should record a named workflow, a baseline metric, pilot acceptance criteria, a caught intent bug or blocked bad case, review-time observations, escaped-intent-bug observations, a reproducible demo, and a teardown essay. [R4][R9] Until then, the project should not claim reduced review burden, reduced escaped intent bugs, buyer willingness, or market proof. [R4][R7][R9]

## Paid Moat Hypothesis

The paid moat is currently a hypothesis: governed enforcement plus signed cross-tool evidence around AI-assisted SDLC changes. [R6][R7][R8][R9][R10] It becomes more defensible only if it controls or integrates with the point where human intent, route contract, execution telemetry, gate decision, terminal outcome, and ledger receipts are required for merge, export, or attestation. [R6][R8][R9]

The minimum prototype artifact is a signed `AttestationBundle` over run IDs, route template IDs, stage run IDs, route contract version, Craft ledger path, `ledger_sha256`, artifact references, telemetry references, terminal guard references, transcript excerpt references, decision snapshots, governance signal references, approving human/governance decision IDs, git/content hashes where available, signer identity, timestamp, and verification policy. [R6] This is a signed cross-tool evidence bundle prototype until verifier output, auditor export, buyer/auditor acceptance, and paid pilot evidence exist. [R6][R7][R9][R10]

The existing primitives cover pieces of this, but not the paid product: source ledgers, Craft ledger/index hashes, observability JSONL rows, AEO-style delegation telemetry, context provenance, and terminal evidence rows. [R6] The missing paid primitives are the signature bundle, verifier, enforcement surface, auditor export, cross-tool receipt model, privacy/redaction policy, and a coverage matrix marking actual schema/file examples versus missing pieces. [R6][R8][R9]

External pressure creates a plausible demand hypothesis, not buyer willingness. [R7][R9] AI governance, secure SDLC, agentic-AI security guidance, SOC 2/ITGC/SOX-style control evidence, ISO 42001, NIST AI RMF, and EU AI Act pressure all support demand for better evidence, logging, human oversight, cybersecurity, traceability, and accountability. [R7] None of those sources should be overstated as requiring cryptographic attestation for all AI-generated code, proving product safety, or showing willingness to pay. [R7][R8][R9]

The moat weakens if it depends on generic AI governance mappings, prompt discipline, local YAML ledgers, observability dashboards, schema-only validators, or the public CyberAlchemy method itself. [R7][R8] The moat hypothesis strengthens if it stays anchored to the SDLC change artifact itself: what changed, what intent governed it, what tests derived from that intent, which agents or humans acted, who approved, what immutable evidence survived, and whether bypass attempts fail. [R7][R8][R9]

## First Proof-Bearing Slice

The first proof-bearing slice should implement only the existing internal loop, but it must wrap the buyer-visible SDLC change artifact rather than proving an internal ontology/context pipeline in isolation. [R1][R2][R3][R4][R8] The combined target is:

`source/provenance -> inventory entry -> ontology candidate -> context pack -> SDLC route -> sandboxed execution -> derived tests -> alignment audit -> human gate -> merge/blocked decision -> telemetry/reflection`

It should not attempt full repository ingest, canonical ontology promotion, automated retrieval, runtime storage, complete Operational Ontology, automatic signal ingestion, durable user model, dashboards, automatic personalization, capability mutation, or auditor-grade claims. [R3][R7][R8][R10]

A practical slice sequence is:

1. Freeze one commercial workflow boundary and keep the public/private seam fixed: public method and wedge in `arcanum`, private runtime/moat candidates in `implementation/domainspec`. [R3][R7][R8]
2. Decide provisional output roots for inventory and ontology, or run `decision-gate` if ownership between `cyberAlchemy/ontology/` and `.arcanum/ontology/` blocks work. [R2][R3]
3. Install or adapt `.arcanum/inventory/`, create the CyberAlchemy source manifest, and ingest only the first cohort rather than the whole corpus. [R2][R3]
4. Create typed inventory entries with provenance, contradictions, branch hypotheses, source roles, and indexes before treating ontology candidates as usable. [R3][R10]
5. Run ontology-harness over the source digests and first entries, keeping ontology entries thick, evidence-backed, confidence-bearing, and promotion-aware. [R2][R3]
6. Run context-builder for one concrete task: prepare context for the SDLC readiness workflow, including the alignment-audit and human-gate obligations. [R2][R3][R4]
7. Validate a route through `orchestrate` plus `dispatch-spec`, then execute one bounded task through a native parent skill or `task-session`. [R2]
8. Capture OIL telemetry, signal rows, reflection status, decision receipts, and promotion candidates without promoting them automatically. [R2][R3][R6]
9. Run a skip-resistance test: a run lacking required route, gate, terminal evidence, or ledger receipt must fail merge, attestation, or export. [R6][R9]
10. Run a hidden-authority audit, replay verifier, tamper test, and one blocked/bad-evidence case. [R2][R3][R6][R9]

The slice is successful when it produces proof artifacts plus correctness checks: an inventory manifest, first typed entries, ontology-harness output, task-sized context pack, validated route, execution receipt, telemetry/reflection rows, explicit promotion candidates, coverage matrix, replay verifier output, tamper check, skip-resistance result, and a blocked-case receipt. [R2][R3][R6][R9] The slice is not successful merely because the architecture is coherent or because the wedge narrative is compelling. [R1][R4][R8]

## Roadmap Phases

Phase 0 is boundary selection: choose one SDLC change workflow, define "done correctly," fix public/private seams, and decide whether output-root uncertainty requires `decision-gate`. [R3][R4][R7]

Phase 1 is substrate installation: stand up `.arcanum/inventory/`, create the source manifest, backfill the first cohort, and produce typed evidence entries with provenance before ontology work is treated as operational. [R2][R3]

Phase 2 is ontology shape: validate the candidate operational-lesson branch shape, convert first entries into thick ontology candidates, and keep candidate-vs-authority status explicit. [R1][R3][R5][R10]

Phase 3 is context and route proof: generate one obligation-linked context pack, validate one route graph, and execute one bounded SDLC change task without claiming that the broader AEO bridge is complete. [R2][R3][R4]

Phase 4 is feedback and correctness proof: capture telemetry, reflection, signal rows, promotion candidates, skip-resistance result, replay verification, tamper check, hidden-authority audit, and one blocked-case receipt. [R2][R3][R6][R9]

Phase 5 is signed evidence prototype: bind source, intent, route, gate, execution, telemetry, terminal outcome, and approval evidence into a signed `AttestationBundle`, verifier output, and coverage matrix. [R6][R9]

Phase 6 is acceptance testing: map one control objective, produce an auditor-review rubric and sample export, then record explicit accepted/rejected/not-reviewed status. [R6][R7][R9]

Phase 7 is pilot packaging: run the 2-4 week readiness sprint with measured review-time and escaped-intent-bug observations, then decide whether a vertical attestation offer has enough proof to sell. [R4][R7][R9]

## Decision Gates

Gate 1: Authority boundary. Decide which artifacts are source/provenance evidence, inventory entries, ontology candidates, promoted ontology, context packs, execution telemetry, approval receipts, signed attestation inputs, or pilot outcome evidence before using them in implementation planning. [R1][R3][R10]

Gate 2: Workflow boundary. Select one SDLC change workflow and define "done correctly" before building a generalized product surface. [R3][R4][R8]

Gate 3: Public/private seam. Keep public method, schemas, and adoption aids separate from private runtime, metering, signing, enforcement, auditor export, vertical deployment, and formal proof. [R3][R7][R8]

Gate 4: Output roots. Decide where generated inventory and ontology maps live before producing artifacts that future agents may treat as authority. [R2][R3]

Gate 5: Candidate operational-lesson branch. Validate schema, storage, query behavior, promotion rules, and routing use before treating it as an execution-routing substrate. [R1][R3][R5][R10]

Gate 6: Privacy and redaction. Define how user workflow memory, route history, transcript excerpts, and evidence references are redacted before treating telemetry as reusable product data. [R3][R6][R8]

Gate 7: Route/execution adapter. Do not claim integrated runtime until Arcanum route artifacts, AEO-style stage contracts, telemetry envelopes, terminal outcomes, and subagent child runs are bridged. [R2]

Gate 8: Signal vocabulary. Unify OIL, Signal Observer, Craft, and AEO-style telemetry vocabulary before signed cross-ledger evidence depends on it. [R2][R6][R8]

Gate 9: Attestation claim. Do not claim auditor-grade or auditor-acceptable attestation until a signed bundle, verifier output, route/gate/execution/ledger hashes, terminal evidence, approval identities, auditor rubric, sample export, and acceptance status exist. [R6][R7][R8][R9][R10]

Gate 10: Bypass and correctness. Do not claim chokepoint control until skip-resistance, replay, tamper, hidden-authority, and blocked-case checks pass. [R2][R3][R6][R9]

Gate 11: Market proof. Do not claim reduced review burden, fewer escaped intent bugs, buyer willingness, or compliance necessity until pilots measure those outcomes and the claims stay inside what the evidence supports. [R4][R7][R9]
