# Research Transcript: Spec-Driven Completeness Moat Inventory Research

- Dispatch: `2026-07-06-spec-driven-completeness-moat-inventory-research`
- Date: 2026-07-06
- Strategy: `EXPLORE-STRATEGY.md`
- Proposal: `DISPATCH-PROPOSAL.json`
- Transcript note: explorer returns are preserved by agent section. After context compaction, three completed agents were resumed and instructed to repeat their completed final answer without adding analysis.

## Explorer: Shannon / James

- Agent id: `019f360c-4689-7a81-a952-290c407153b6`
- Role: local inventory/source coverage, evidence matrix, BP claim ladder

## Required-Source Coverage

| Source | Seen? | Most relevant evidence | Claim supported | Gap / risk |
|---|---:|---|---|---|
| `.arcanum/inventory/index.json` | Yes | 127 entries; relevant tags around `deterministic-validation`, `completeness`, `lean`, `moat`, `kodamai`, `investor-bp` | Inventory has enough indexed substrate for a BP differentiation census | Index is a read model; claims still need source/runnable backing |
| `.arcanum/inventory/index.md` | Yes | Current gaps repeatedly mark evidence-cards/EvidenceSets as candidate read models; many validators unbuilt | Strong boundary discipline for `claim <= proof` | Do not treat inventory summaries as promoted authority |
| `.arcanum/inventory/entries/` | Yes, swept by index/rg; key entries opened | Deterministic retrieval, CAV2 determinism, validation-for-all-CAV2, FOL complement, attestation MVP, machine-map/moat, Kodamai | Supports differentiated substrate story | Many entries are candidate/internal/moat-adjacent |
| Investor BP findings | Yes | Barbell: paid witnessed readiness engagements now; receipts compound into platform thesis; Tier 0 substrate includes DomainSpec v2/CAV2/Craft/Lean | BP shape and portfolio reach | Explicitly says not final investor prose and not finished platform |
| AI assurance vocabulary findings | Yes | “Governed AI work readiness package”; “receipt-backed assurance case” only scoped/intended; deterministic validation specimens, not runtime correctness | Safe public assurance vocabulary | No complete end-to-end assurance-case specimen yet |
| `COMMERCIALIZATION-SYNTHESIS.md` | Yes | Free wedge: validators/audits; paid moat: engine + governance + attestation + vertical; services first | Commercialization/moat framing | Older discovery/exploratory artifact; says most monetizable surfaces deferred/unbuilt |
| `machine-map-and-moat-synthesis.md` | Yes | Moat inversion: attestation + governance-data + vertical; provability/Lean as amplifier, not moat | Defensibility framing | Candidate only; Saturn/control loop mostly unbuilt |
| `read-trivial-via-selective-promotion-synthesis.md` | Yes | “Promote less, not write less”; authority surface small/high-signal; read is cheap, not zero | Read-trivial/selective-promotion story | Govern-importance runtime unbuilt; “trivial” overclaims |
| `kodamai-smithe-correctness-layer-synthesis.md` | Yes | Kodamai comparator: public corpus shows proof-artifact claims but no specimen/checker/soundness theorem; internal edge is runnable checker + honest scope | Comparator/demonstration-over-assertion | Cannot assert Kodamai lacks internal unpublished mechanism; no market uniqueness claim |
| `domainspec-lean-formalization/lean-engineer/` | Yes | Lean package contains verified reference-monitor core, `permguard`, confinement/egress/taint theorems, and CAV2 governs-acyclicity witness | Formal-methods discipline and bounded machine-checked witnesses | Not whole-system correctness; I did not run `lake build` in this pass |
| `implementation/domainspec/scripts/audit_richness.py` | Yes, read and sampled | Six deterministic structural checks: injectivity, faithfulness, fullness, M6 clusters, cardinality lower bound, perturbation proxy | Deterministically validates named structural obligations/gaps for compatible specs | Sample runs found under-specified/parser-blind results, so it supports gap detection more than corpus completeness |

## BP Claim / Evidence / Gap Matrix

| BP axis | Evidence found | Safe claim | Gap / stronger obligation |
|---|---|---|---|
| Deterministic validation | `projects/domainspec-v2/impl/test-derivation-engine/src/index.ts` is parse -> graph -> derive -> emit, no LLM/network; tests assert byte-stable obligation keys, deterministic δ, semantic round-trip pass-with-residue for financial settlement. `audit_richness.py` emits deterministic JSON structural audits. | DomainSpec has deterministic derivation/validation specimens for named structural obligations in current compatible corpora. | Need current test run receipts; need end-to-end typed spec -> obligations -> validator receipts -> owner decision. |
| Structural completeness / richness | Richness audit sampled `payment-processing`, `user-account`, and auth demo: reports exact concepts, typed edges, unwitnessed edges, theoretical min tests, shortfalls, collisions, M6 clusters. | The framework can deterministically census structural gaps and richness risks. | Current samples are under-specified or parser-blind; do not claim corpus is complete. |
| Formalization / Lean | `lean-engineer` is a self-contained Lean package for verified engineering artifacts; has reference-monitor proofs and CAV2 governs-cycle witness showing unary lints miss cross-rule acyclicity. | Formal-methods discipline with bounded theorem/counterexample witnesses. | Not “formally verified platform”; no current `lake build`/sorry audit performed here. |
| Commercialization / moat | Commercialization and machine-map entries converge: free wedge drives adoption; paid moat is engine/governance/attestation/vertical; attestation L1 is built/demonstrated per inventory. | Defensibility substrate is governance-data + attestation + private engine/vertical leverage. | Attestation L2, hosted services, enforcement runtime, and many paid-meter surfaces remain unbuilt. |
| Read-trivial / selective promotion | Read-trivial entry cleanly splits capture vs authority and recall-importance vs govern-importance. | Gated promotion can make authoritative reads cheaper and higher-signal. | “Trivial” is forbidden; capture completeness and runtime govern-importance are unmeasured/unbuilt. |
| Kodamai comparison | Kodamai entry supports “demonstration over assertion” as the edge: show runnable checker/specimen/soundness scope; do not claim their internal absence. | Compared to visible Kodamai corpus, DomainSpec can differentiate by runnable bounded validators and honest claim scope. | Requires current external market/Kodamai check later; no uniqueness claim. |
| Compounding POC reach | BP and AI-assurance findings converge: POCs leave receipts, gates, owner decisions, telemetry, readiness verdicts, verifier outputs. | Owned POCs compound as a receipt/residue base for later assurance cases and platform thesis. | Need one complete receipt-backed assurance-case specimen across derivation, validation, CAV2 classification, Craft/goal receipt, and attestation seal. |

## BP-Safe Wording

- “Spec-driven framework for deriving and checking named structural obligations in bounded corpora.”
- “Deterministic validation specimens for spec-to-obligation/test derivation.”
- “Structural richness and completeness gap detection, not completeness proof.”
- “Governed AI work readiness packages with source-linked evidence, owner-routed decisions, readiness gates, and receipt-backed assurance-case materials.”
- “Formal-methods discipline with bounded Lean witnesses and explicit claim boundaries.”
- “Demonstration-over-assertion: runnable bounded checkers and specimens where available.”
- “Defensibility substrate: governance-data, attestation, private derivation engine, and vertical/domain receipts.”

## Forbidden Wording

- “Market unique”
- “Correctness proven”
- “Formally verified platform”
- “Complete corpus validation”
- “Certification-ready” as headline
- “Certified,” “ISO/IEC 42001 compliant,” “EU AI Act compliant,” “conformity assessed”
- “Runtime conformance guaranteed”
- “Receipts prove truth”
- “Public-ready engine”
- “Validated operating system”
- “Read is trivial” without “cheap/high-signal within stable schema epoch”

## Missing-Source Flags / Follow-Up Asks

- No missing required source found.
- Follow-up should run current build/test receipts: `vitest` for the test-derivation engine, `lake build` for `lean-engineer`, and a fuller `audit_richness.py` batch over all compatible `SPEC.md` directories.
- External comparator/market claims must be refreshed later with dated checks; this pass should not assert market uniqueness.
- Strongest next BP proof object: one complete specimen chaining typed spec -> derived obligations/tests -> deterministic validator/richness result -> CAV2 claim classification -> Craft/goal receipt -> L1 attestation seal.

## Explorer: Beer / Carson

- Agent id: `019f360c-4cb0-7f61-8888-4931776a4b3d`
- Role: portfolio map, owned projects, near-term consulting routes, exclusions

**Findings**

**1. DomainSpec v2 + CAV2 Primacy**

DomainSpec v2 and CAV2 should be treated as the primary spine for the investor-BP substrate, but at different altitudes.

DomainSpec v2 is the implementation/research home for spec-governance: typed specs, derived obligations, validation/layering/drift governance, deterministic test-derivation, and private moat boundaries. Evidence boundary: [projects/domainspec-v2/README.md](/home/vrondelli/projects/domainspec-core/projects/domainspec-v2/README.md), [projects/domainspec-v2/authority/AUTHORITY-MODEL.md](/home/vrondelli/projects/domainspec-core/projects/domainspec-v2/authority/AUTHORITY-MODEL.md), [projects/domainspec-v2/impl/test-derivation-engine/README.md](/home/vrondelli/projects/domainspec-core/projects/domainspec-v2/impl/test-derivation-engine/README.md).

CAV2 is the consolidation/governance spine: authority by owner route, evidence != authority, inventory/ontology as read models, explicit promotion ladder, public/private boundary, and governed human-machine integration language. Evidence boundary: [cyberAlchemy-v2/README.md](/home/vrondelli/projects/domainspec-core/cyberAlchemy-v2/README.md), [cyberAlchemy-v2/authority/AUTHORITY-MODEL.md](/home/vrondelli/projects/domainspec-core/cyberAlchemy-v2/authority/AUTHORITY-MODEL.md), [cyberAlchemy-v2/VALUE-AND-PHILOSOPHY-PROPOSITION.md](/home/vrondelli/projects/domainspec-core/cyberAlchemy-v2/VALUE-AND-PHILOSOPHY-PROPOSITION.md).

Claim-safe primacy statement:

DomainSpec v2 proves the operating discipline can become typed, validated, and partially implemented. CAV2 proves the broader company spine can preserve evidence, authority, ontology, implementation, validation, observability, and product boundaries without collapsing them. Together they are stronger than a single POC: they form a repeatable substrate for turning owned research, prototypes, and client/domain projects into governed offerings.

**2. Compounding POC Map**

| Project / capability | Evidence residue type | Commercial / research role | Maturity | BP fit |
| --- | --- | --- | --- | --- |
| DomainSpec v2 | Gate, validator, proof residue, implementation scaffold | Core moat: spec-to-obligation discipline, private deterministic rules, evidence-governed implementation | Active implementation home; parser/rules still partly stubbed | High: technical defensibility and productizable governance engine |
| CAV2 / CyberAlchemy v2 | Authority model, promotion gates, inventory/ontology boundary, observability substrate | Company operating system: governs how knowledge becomes product safely | Project start; active local authority model; not standalone repo | Very high: investor narrative spine |
| Evidence Exchange | Proposal blueprint, receipt concept, credit/authority separation | Future product/workbench for reusable knowledge labor and provenance | Product proposal only; MVP witness not implemented | High, but only as staged opportunity |
| Craft | Canonical sigil, ledger schema, examples, row/index discipline | Durable work-state substrate for projects, delivery, blockers, decisions, receipts | Canonical Arcana sigil; portable contract exists | High: setup/training + managed delivery backbone |
| Goal spell / native skill | Receipts, staged deltas, audit gates, telemetry, approval token | Autonomous governed execution loop over Craft graphs | Registered reusable spell; validation fixtures/results present | High: services automation and internal operating leverage |
| Whisper | Review HTML, draft lifecycle, validation report, learning residue | Fundraising/product narrative and governed composition capability | Generated native runtime package; extension presets exist | Medium-high: BP, sales, investor, research packaging |
| IDE Ergonomics / Connective | Strategy specs, task candidate schemas, human indicator boundaries | Future IDE-side operator surface for governed work selection | Strategy proposal; no runtime | Medium: flagship UX thesis, not near-term revenue proof |
| UI Prototyping Studio | Prototype, CLI, Playwright e2e, mutation gates, revision manifest | Real usable prototype for governed UI iteration | Runnable backend + preview; known gaps remain | High as concrete demo of governance-as-product |
| Ontologize | Research dispatch, product/public offering, buyer-readiness findings | Consulting wedge: metric trust sprint, ontology+DAG for BI/governed agents | Candidate first product; buyer discovery/paid readiness ready, not proven sold | Very high near-term commercial route |
| Savvy Legal Studio AI | Brownfield app, Craft index, architecture principles, audit findings | Domain transfer target: legal AI workflow with traceability and evidence gaps | Real prototype, active blockers/gaps, not production SaaS | High as vertical proof candidate if instrumented |
| autoads | Refine result, design fanout, non-executed plan | Ads/creative learning vertical using Ontologize loop | Seed validated; no live network/spend | Medium-high as later vertical extension |
| Arcanum user-guide / Translate | Refinement receipts, pass-with-runtime-caveat | Training/setup route: translate before guide, concept bridging | Candidate route; runtime caveats | Medium: onboarding/training product support |
| MOGT | Runtime decision receipt schema, synthetic harness, experiments not started | Research capability for agent decision audit and objective tradeoffs | Design + dry-run only; no live evidence | Medium: research moat, not commercial claim yet |
| Lean formalization | Machine-checked witnesses, no-collapse theorem, explicit scope caveats | Formal witness layer for claim discipline and anti-scalar evaluation | Strong formal artifacts, but applied claims conditional | High for credibility, carefully bounded |
| ResonantOS economy research | Research tower, attack lanes, validation scaffold, source-claim ledger | Economy/incentive resilience and Evidence Exchange gating precedent | Active research repo; local-research-only | Medium-high for future incentive layer, not launch proof |
| maestro-trama / urdume | Real creative data, creative DNA, retrieval/labeling systems, telemetry | External/sibling evidence for creative compounding and autoads analogy | Draft but with mature app/data surfaces | Medium as analogy/source precedent, not owned scored POC unless included by BP scope |

**3. Evidence Exchange Transfer To Savvy Legal Studio AI**

The transfer is conceptually strong but must stay explicitly non-production.

Safe concept transfer:

```text
Savvy legal artifact / document set
  -> local AI workflow consumes it
  -> generated draft / discovery / tournament output
  -> ObservedUseReceipt-style record
  -> review action by lawyer / owner
  -> credit or provenance seed
  -> no authority, no legal correctness, no SaaS production claim
```

Savvy already has the right pressure points: OCR/document persistence, draft versions, delivery receipts, legal workflow stages, Craft blockers, and identified audit gaps around correlation IDs, model-used records, document-to-draft linkage, tournament persistence, and silent audit failure. Evidence Exchange can become a legal-work provenance layer: “which source documents, model route, preliminary discovery, structure candidate, and reviewer decision contributed to this draft?”

Safe claim:

Savvy is a good vertical candidate for testing Evidence Exchange-style receipts because it already needs provenance, model traceability, document linkage, review, and delivery receipts.

Forbidden claim:

Do not say Evidence Exchange is implemented in Savvy, that Savvy is production SaaS, that legal outputs are audited/compliant, or that receipts prove legal correctness.

**4. Consulting / Setup / Training Routes**

The strongest near-term company-reach route is services-first, productized over time:

1. Metric Trust / Ontologize setup  
   Sell one operating metric, one source chain, one owner-reviewed learning loop. Evidence: [projects/ontologize/PUBLIC-OFFERING.md](/home/vrondelli/projects/domainspec-core/projects/ontologize/PUBLIC-OFFERING.md), [projects/ontologize/research/2026-06-18-cyberalchemy-integration-first-sale/findings.md](/home/vrondelli/projects/domainspec-core/projects/ontologize/research/2026-06-18-cyberalchemy-integration-first-sale/findings.md).

2. Governance substrate installation  
   Install Craft ledger, authority model, promotion DAG, evidence refs, boundary register, and task-session/goal operating route for a client or internal team.

3. AI-workflow audit and hardening  
   Use Savvy-like gaps as a repeatable assessment: correlation IDs, model-used logging, document lineage, receipt persistence, error observability, owner decisions.

4. Formalization / proof-bound consulting  
   Use DomainSpec v2 + Lean as a high-end research/architecture offer: “we can separate what is formally witnessed, what is interpretive, and what is merely hoped.”

5. Training route  
   Teach teams to operate evidence-first workflows: Craft ledgers, owner routes, promotion gates, receipt discipline, claim <= proof, and translation/guide-style concept bridging.

**5. Exclusions**

Excluded from scored portfolio:

- glyph
- grain
- Golden Quill

Golden Quill may appear only as read-only precedent where existing Ontologize artifacts cite it. It should not be counted as an owned scored portfolio POC for this BP map. Glyph/grain appear in external assimilation/research context but should not be scored.

**6. Claim-Safe Company-Reach Thesis**

Best thesis:

CyberAlchemy/DomainSpec is not a single product bet. It is a compounding governance substrate: formal witnesses, typed specifications, ledgers, receipts, promotion gates, telemetry, ontology, and product prototypes reinforce each other. Each POC leaves residue that the next POC can reuse: schemas, gates, artifacts, route patterns, audit failures, and buyer-facing language. That creates a moat around governed AI work where the company can sell consulting first, harden repeatable setup/training packages, and later productize the strongest receipt/workbench surfaces.

Forbidden overclaims:

- Do not claim CAV2 is a standalone shipped platform.
- Do not claim DomainSpec v2 proves runtime correctness or production conformance.
- Do not claim Evidence Exchange exists as implemented software.
- Do not claim Savvy is production SaaS or legally/compliance/audit ready.
- Do not claim Ontologize is already proven cross-vertical or already sold.
- Do not claim Lean proves business metrics, KPI collapse, or product-market fit.
- Do not claim MOGT has live experimental proof.
- Do not treat credit, popularity, ontology placement, or reuse as authority.
- Do not include glyph, grain, or Golden Quill in scored portfolio value.

## Explorer: Grothendieck / Turing

- Agent id: `019f360c-492e-7a60-b369-6f55246e94be`
- Role: formal/Lean witness inventory, claim boundary, Kodamai formal comparator boundary

**Findings**

**1. Formal Asset Inventory**

| Asset | Formalizes | Status | Register |
|---|---|---:|---|
| [AgentPermissionKernel.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernel.lean:137) | `decidePolicy` agrees with relational `Satisfies`; no false allows; deny precedence; layered authority non-flattenability | Lean theorem source; no `sorry`/`admit`/declared `axiom` found; configured in `lakefile.toml`; not freshly rebuilt this turn | theorem/proof + decidable checker |
| [AgentPermissionKernelArgs.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelArgs.lean:134) | structured tool args, segment glob, path normalization, `..` traversal defense | same | theorem/proof + decidable matcher |
| [AgentPermissionKernelGlobSpec.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelGlobSpec.lean:54) | executable glob matcher iff declarative `GlobMatches` relation | same | theorem/proof |
| [AgentPermissionKernelComposition.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelComposition.lean:41) | policy append/layer composition as conjunction/intersection of authority | same | theorem/proof |
| [AgentPermissionKernelAlgebra.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelAlgebra.lean:90) | `decidePolicy` composition as meet algebra | same | theorem/proof |
| [AgentPermissionKernelConfinement.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelConfinement.lean:82) | read path confinement under canonicalized prefix grant | same | theorem/proof |
| [AgentPermissionKernelWriteConfinement.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelWriteConfinement.lean:45) | write/edit confinement variants | same | theorem/proof |
| [AgentPermissionKernelBash.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelBash.lean:53) | literal-prefix bash matcher; explicitly type-separated from path glob | same | theorem/proof + matcher |
| [AgentPermissionKernelEgress.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelEgress.lean:63) | URL scheme/host suffix egress allowlist soundness | same | theorem/proof + matcher |
| [AgentPermissionKernelTaint.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelTaint.lean:118) | monotone session taint and egress denial after secret read | same; declared trust border on labeling, sink coverage, trace fidelity | theorem/proof + monitor |
| [AgentPermissionKernelTaintTrace.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelTaintTrace.lean:124) | whole-trace “no prior secret read before allowed egress” safety | same | theorem/proof |
| [AgentPermissionKernelSession.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelSession.lean:72) | veto guards refine base policy; veto composition | same | theorem/proof |
| [AgentPermissionKernelEgressBypass.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelEgressBypass.lean:98) | negative witness: bash-routed egress bypasses current egress classifier | same | machine-checked counterexample |
| [AgentPermissionKernelRefinementFibre.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/AgentPermissionKernelRefinementFibre.lean:85) | monotone assumed-clause/capability refinement fibre; engineering exhibit, not typed-residue | same | theorem/proof sketch-to-Lean exhibit |
| [PermGuard.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/PermGuard.lean:76) | CLI parser/wiring around proved kernel | parser explicitly unverified trust border; executable configured as `permguard` | runnable specimen, not proof of parser correctness |
| [GovernsAcyclicity.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-engineer/cav2-governance/GovernsAcyclicity.lean:104) | 3-node CAV2 governs cycle where unary lints pass; acyclicity not expressible by node-data-only predicate | no `sorry` found; `#print axioms` directives present; existing `.olean` observed for this file only | theorem/proof + bounded witness |
| [FunctorialResidueStructure.lean](/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-formalization/FunctorialResidueStructure.lean:97) | residue as genuine functor; monotonicity derived, not postulated; `separation_is_functor_action` | adjacent bridge asset; no direct agent/policy bridge; source claims sorry-free | theorem/proof, wrong object for agent correctness |

`OPEN-SORRIES.md` is scoped to `lean-formalization/`, not `lean-engineer`, and lists open obligations outside the focused agentguard kernel. It explicitly warns that syntactic sorry-free is weaker than `#print axioms`.

**2. Register Distinctions**

Decidable checks: `decidePolicy`, path/glob/bash/fetch matchers, taint/egress guards, `PermGuard` runtime.

Theorems/proofs: `decidePolicy_allow_iff`, `decidePolicy_sound`, `deny_precedence`, confinement, glob equivalence, trace safety, `governs_acyclicity_witness`, `acyclicity_not_unary`, `separation_is_functor_action`.

Runnable Lean specimen: `PermGuard.lean` plus `permguard-examples/*.json`, but the JSON-to-structure parser is outside the proof surface.

Proof sketches/prose claims: README staging notes, Kodamai synthesis, machine-map/moat entries, FOL complement entries.

Prose claim only: any “formal proof of completeness,” “agent correctness,” “behavioral verifier,” or “at scale” correctness language. No local theorem currently proves that.

**3. Investor-BP Language Now vs Future/Internal**

Supportable now:
“DomainSpec has machine-checked Lean witnesses for bounded policy-decision soundness, layered authority composition, confinement, taint/egress trace guards, and a CAV2 cross-rule acyclicity counterexample showing why local linting is insufficient.”

Supportable with care:
“Runnable verifier specimen exists for a narrow encoded tool-call policy surface.” The trust border must be named: parser fidelity, path canonicalization assumptions, sink coverage, trace fidelity, host-label fidelity.

Internal/future-only:
“agent |= spec,” “formal proof of agent correctness,” “formal completeness,” “behavioral/concurrency verifier,” “correctness at scale,” “CAV2 fully Lean-verified,” or “provability is the moat.” Current inventory says provability is an amplifier, while attestation/governance data/vertical fit are the present moat.

**4. Bridge Needed for `agent |= spec`**

The missing bridge is one object that is simultaneously:
a categorical denotation of an agent `[[A]]`,
a behavioral property/spec `φ`,
a satisfaction judgment `[[A]] |= φ`,
and a soundness theorem tying that judgment to the denotation, not merely to the existing `decidePolicy`.

Collapse test: if the bridge reduces to `decidePolicy` over a flat encoded predicate, the categorical layer adds no proof work. That would be only `action/request satisfies encoded invariant`, not `agent correct`.

**5. Kodamai Boundary**

Local artifacts demonstrate more checkable substance on the narrow permission/reference-monitor slice than the public Kodamai/Smithe corpus shows: source-level Lean theorems, bounded witnesses, and a runnable kernel wrapper.

The local Kodamai synthesis says the public Kodamai/Smithe materials assert or imply stronger “correctness layer” language, but the verifier itself is unpublished/unwitnessed publicly: no public specimen proof, runnable checker, proof system, or soundness theorem for categorical `agent |= spec`. It also explicitly says unpublished does not mean absent internally.

**6. Forbidden Overclaims**

Do not say:
“formal proof of completeness,”
“formal proof of agent correctness,”
“DomainSpec proves agents satisfy specs,”
“CAV2 is Lean-verified,”
“the verifier exists at scale,”
“PermGuard proves security,”
“GovernsAcyclicity proves full CAV2 acyclicity,”
“FunctorialResidueStructure denotes agents,”
“Kodamai lacks the verifier internally.”

Say instead:
“bounded Lean witnesses,”
“machine-checked narrow policy-decision soundness,”
“runnable specimen over encoded tool-call policies,”
“CAV2 acyclicity counterexample/witness,”
“bridge not yet built.”

## Explorer: Turing / Aquinas

- Agent id: `019f360c-4764-73f1-a7f7-9a10ee3c21f9`
- Role: deterministic richness auditor and derivation/completeness claim ladder

**1. What `audit_richness.py` Deterministically Checks**

`implementation/domainspec/scripts/audit_richness.py` is a deterministic L1 structural richness auditor. Given a spec directory, it parses `SPEC.md` plus aspect docs such as `domain.md`, `operations.md`, `states.md`, `interfaces.md`, `events.md`, `queries.md`, `workflows.md`, `mappings.md`, and `governance.md`.

It deterministically checks:

1. **Object injectivity:** flags concepts with identical derivation signatures: meta-type, counts of rules/postconditions/error states/transitions/fields/invariants, and typed incoming/outgoing edge-type multisets.
2. **Edge faithfulness:** checks whether meta-types have required structural witnesses, e.g. `Operation` needs incoming `performs`, `Rule` needs outgoing `enforces`, `Query` needs outgoing `queries`.
3. **Fullness:** checks whether concepts appear to have test rows in `TEST-SPEC.md` using its expected `T-...` ID convention and some transitive/entity heuristics.
4. **M6 / residue-bait clusters:** detects unrelated source concepts converging on the same non-Entity target through the same edge type.
5. **Cardinality lower bound:** computes a theoretical minimum test count from structural counts: rules x2, postconditions, error states, transitions, invariants, queries x3, workflows x4, events x2.
6. **Perturbation proxy:** detects redundant same-type incoming edges where deleting one may not change obligations.

It does **not** execute implementation code, prove semantic correctness, inspect runtime behavior, or formally prove completeness. It validates whether the authored corpus has named structural material sufficient for low-residue derivation.

**2. What “Derive Checks” Can Truthfully Mean**

Current evidence supports this meaning:

DomainSpec can deterministically derive named obligation records from canonical Markdown feature docs, using a no-LLM/no-network TypeScript engine in `projects/domainspec-v2/impl/test-derivation-engine`.

The concrete engine path is:

`parse(feature docs) -> typed ConceptGraph G -> derive(G) -> obligation_key -> emit spec/tests`

The derivation rules cover named structures including valid/invalid transitions, invariants, rule validations, calculations, postconditions, contracts, events, workflow steps, queries, mappings, error states, domain fields, enums, and policy decisions. Obligation keys are content-addressed from `source_anchor`, `rule_type`, and canonical params.

Strongest current witness in the corpus: `validation/poker-team/docs/features/financial-settlement/TEST-SPEC.engine.md` records engine provenance and **79 engine-derived obligations**: 24 `derivable-pure`, 54 `derivable-needs-harness`, and 1 `needs-formal`.

So “derive checks” is safe if it means: derive deterministic, source-linked obligation/check specifications from canonical spec artifacts. It should not mean all checks are executable assertions or all obligations are semantically validated.

**3. What “Validate Completeness” Can Truthfully Mean**

Safe meaning:

DomainSpec can deterministically validate **structural completeness/richness** against named obligations and corpus conventions.

That includes:

- whether concepts are registered;
- whether typed edge obligations are witnessed;
- whether structural categories imply missing test obligations;
- whether authored tests/spec rows meet expected conventions;
- whether the engine-derived obligation set covers or exceeds a committed semantic catalogue, where the roundtrip comparator is available.

Unsafe meaning:

- Not full semantic completeness.
- Not runtime correctness.
- Not implementation conformance.
- Not formal proof of all obligations.
- Not assurance/certification/compliance.
- Not universal CAV2 validation. The inventory entries explicitly mark CAV2-wide deterministic validators, SMT/FOL/Cedar layers, and categorical correctness as intended/candidate or future, not shipped.

Important live audit result: running `audit_richness.py` on `validation/poker-team/docs/features/financial-settlement` returned **10 concepts, 3 typed edges, 2 untyped refs, theoretical min 28, actual test rows 0, shortfall 28, verdict UNDER-SPECIFIED**. That `0` is because the auditor’s test parser expects `T-...` row IDs, while the live `TEST-SPEC.md` uses IDs like `RV-1`, `CT-1`, `WF-1`. So the auditor proves dialect-sensitive structural validation, not absolute test absence.

**4. Claim Ladder**

Safe now:

- “DomainSpec deterministically validates named structural obligations for the current corpus.”
- “DomainSpec derives source-linked obligation records from canonical spec documents.”
- “DomainSpec distinguishes derivable-pure obligations, obligations needing a harness, and needs-formal gaps.”
- “DomainSpec supports claim-boundary governance: what is derived, what is skipped, and what remains unresolved.”

Internal moat:

- The private v2 derivation rules under `projects/domainspec-v2/impl/test-derivation-engine/src/rules/`.
- Engine-derived `TEST-SPEC.engine.md` with provenance, hashes, and deterministic engine region.
- Roundtrip and negative-control design in the derivation engine, though I could not execute it in this environment because PNPM/Corepack failed before package code started.

Next witness:

- A runnable read-only demo command that produces or checks `financial-settlement` end to end:
  `parse -> derive 79 obligations -> compare committed catalogue -> negative-control passes -> emit hybrid tests/report`.
- A small fixture showing one intentional missing obligation fails the comparator.
- A generated report that joins `audit_richness.py` structural verdict with engine-derived obligation coverage.

Future ambition:

- SMT/FOL/Cedar cross-rule validators for CAV2.
- Formal proof of selected governance invariants.
- Categorical `agent ⊨ spec` correctness layer.
- Assurance-case or verifier product language only after a complete specimen exists.

**5. Minimum Runnable Witness To Strengthen The BP Claim**

Minimum investor-safe witness:

1. Use `financial-settlement` as the bounded corpus.
2. Run the derivation engine read-only.
3. Show:
   - exact input docs and hashes;
   - exact derived obligation count;
   - obligation tiers: pure / needs harness / needs formal;
   - roundtrip verdict against committed `TEST-SPEC.md`;
   - negative-control pass proving the comparator can fail;
   - one emitted test/spec artifact with coverage gaps explicitly labeled.

Current blocker: I attempted `pnpm run test`, `pnpm exec tsx src/cli.ts roundtrip financial-settlement`, and `pnpm exec tsx src/cli.ts self-check financial-settlement`; all failed at Corepack PNPM signature verification before running project code. There is also no local `node_modules/.bin` in the package, so I could not execute the TypeScript witness without installing dependencies.

**6. Forbidden Overclaims**

Do not claim:

- “proves correctness”
- “validates runtime behavior”
- “complete correctness layer”
- “formal proof of completeness”
- “certification-ready”
- “audit-ready”
- “ISO/EU AI Act compliant”
- “universal CAV2 deterministic validators shipped”
- “agent behavior correctness”
- “semantic completeness”
- “all checks are executable”
- “the auditor proves test coverage”
- “the platform is finished”

Best default public phrase remains:

“DomainSpec deterministically validates named structural obligations for the current corpus.”

Slightly stronger, if paired with the `TEST-SPEC.engine.md` witness:

“DomainSpec derives source-linked obligation records from canonical specs and deterministically validates named structural coverage boundaries for the current corpus.”

## Explorer: Porter / Volta

- Agent id: `019f360e-11e9-71f0-8f2f-7ed92d487100`
- Role: external comparator map, buyer wedge, defensibility and standards boundaries

**Findings: Porter Comparator Map, 2026-07-06**

**Comparator Map**
Kodamai/Kelvingrove is the closest located comparator for “formal governance/provable agent correctness” positioning. Its April 2026 launch claims Kelvingrove provides a formal governance layer using category theory, type theory, and neuro-symbolic AI; the release says it can prove agent correctness and is compatible with any LLM/enterprise platform. Checked public evidence did not surface a specimen proof, public checker, named proof assistant, soundness theorem, or runnable verifier. That supports “closest located comparator in checked sources,” not “they lack it internally.” ([businesswire.com](https://www.businesswire.com/news/home/20260413955417/en/Kodamai-Solves-Enterprise-AIs-Hardest-Problem-Making-Autonomous-Agents-Provably-Correct-at-Scale)) Kodamai’s public research page points to Bayesian lenses / compositional active inference work, and Smithe’s arXiv corpus supports a category-theoretic research lineage, not by itself a published enterprise `agent satisfies spec` verifier. ([kodamai.com](https://www.kodamai.com/foundational-research?utm_source=openai)) ([arxiv.org](https://arxiv.org/a/smithe_t_1.html?utm_source=openai))

Spec-driven development is now a live category, not a white space. Kiro uses structured specs to turn ideas into requirements, design docs, and tasks; GitHub Spec Kit puts specifications at the center of AI-assisted development; OpenSpec provides repo-local proposal/spec/design/task workflow across many coding assistants. ([kiro.dev](https://kiro.dev/docs/specs/)) ([github.github.com](https://github.github.com/spec-kit/)) ([openspec.pro](https://openspec.pro/)) The external market has already converged on “specs before code”; DomainSpec cannot claim novelty there.

Requirements/model-based testing and traceability are mature adjacent incumbents. Jama, Siemens Polarion, IBM DOORS Next, MathWorks Requirements Toolbox, Keysight Eggplant, and SmartBear cover requirements capture, traceability, test generation/management, model-based testing, and quality systems for regulated engineering. ([jamasoftware.com](https://www.jamasoftware.com/blog/ai-requirements-management/?utm_source=openai)) ([siemens.com](https://www.siemens.com/en-us/products/polarion/industrial-ai/?utm_source=openai)) ([ibm.com](https://www.ibm.com/products/requirements-management?utm_source=openai)) ([mathworks.com](https://www.mathworks.com/products/requirements-toolbox.html?utm_source=openai)) ([keysight.com](https://www.keysight.com/us/en/cmp/2025/ai-software-testing.html)) ([smartbear.com](https://smartbear.com/blog/smartbear-software-testing-tool-comparison/)) DomainSpec differentiation must be narrower: repo-native authority/receipts/governed AI work, not generic traceability.

Formal methods/proof tools are also mature infrastructure. Lean publicly positions itself as an open-source proof assistant with a minimal trusted kernel and real-world verification use cases including Cedar. Proof logging research shows the classic pattern: claims need proof artifacts plus checkers, and proof generation/checking overhead is a central adoption issue. ([lean-lang.org](https://lean-lang.org/)) ([drops.dagstuhl.de](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2024.11)) DomainSpec’s Lean/formal witnesses are an amplifier only when attached to scoped claims.

AI governance/compliance platforms are crowded. Credo AI offers policy packs for EU AI Act, NIST AI RMF, ISO 42001, and contextual governance knowledge graphs. ISO/IEC 42001 is an AI management-system standard; NIST AI RMF is voluntary risk-management guidance; the EU AI Act is a risk-based legal framework with staged obligations. ([credo.ai](https://www.credo.ai/)) ([iso.org](https://www.iso.org/standard/81230.html)) ([nist.gov](https://www.nist.gov/itl/ai-risk-management-framework)) ([digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)) DomainSpec should not lead with “AI governance platform”; lead with governed AI work readiness packages and receipts.

Developer-assurance/audit tooling is emerging fast. Northflank frames enterprise AI coding deployment as requiring SSO, SIEM audit logs, PR gates, sandbox isolation, data residency, and incident response. Proofpoint sells agent integrity with intent alignment, reconstructed workflows, and defensible audit trails. TrueFoundry frames AI code security as governing gateways, MCP access, audit logs, and VPC deployment, not just code scanning. ([northflank.com](https://northflank.com/blog/enterprise-ai-coding-agent-deployment)) ([proofpoint.com](https://www.proofpoint.com/us/products/agentic-ai-security)) ([truefoundry.com](https://www.truefoundry.com/blog/best-ai-code-security)) This validates buyer pain, but also means “audit trail for agents” alone is not distinctive.

**Safe Differentiation If Evidence Holds**
Safest claim: “DomainSpec/CyberAlchemy produces governed AI work readiness packages: source-linked evidence, owner-routed decisions, readiness gates, and receipt-backed assurance-case materials for bounded AI workflows.” This matches local assurance vocabulary and avoids certification claims. [findings.md](/home/vrondelli/projects/domainspec-core/.arcanum/inventory/queries/2026-07-06-ai-assurance-certification-vocabulary-research/findings.md:21)

Against spec-driven tools, the differentiator is not “spec-first.” It is spec-to-obligation/test derivation plus owner authority, claim-boundary governance, receipts, and attestation packaging. Local evidence frames DomainSpec v2 as a private implementation/research surface, not public-ready platform infrastructure. [findings.md](/home/vrondelli/projects/domainspec-core/.arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md:176)

Against Kodamai/Kelvingrove, the safe phrase is: “closest located comparator in checked sources markets formal/provable agent correctness; DomainSpec’s defensible edge, if demonstrated, is runnable specimen + explicit checker + claim-scope labeling rather than assertion-level proof language.” Local Kodamai synthesis already says the edge is demonstration versus assertion, while warning unpublished does not mean absent internally. [kodamai-smithe-correctness-layer-synthesis.md](/home/vrondelli/projects/domainspec-core/.arcanum/inventory/entries/kodamai-smithe-correctness-layer-synthesis.md:64)

Against AI governance platforms, the wedge is not policy-pack breadth. It is work-product-level readiness: a bounded workflow leaves receipts, source chains, decisions, gates, and optional attestations. Local BP research says repeated receipts test a platform thesis, not that a finished platform exists. [findings.md](/home/vrondelli/projects/domainspec-core/.arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md:38)

Against developer security/audit platforms, the differentiator is semantic/governance custody over intent and authority, not infrastructure controls. Northflank/Proofpoint/TrueFoundry cover execution, identity, behavioral security, audit logs, and gateways; DomainSpec should position beside them as “what was intended, who owns the claim, what evidence supports it, what does not follow,” not as a replacement.

**Buyer Wedge / WTP Thesis**
Free wedge: spec/test derivation, validators, extraction, intent tools, and ledger discipline drive adoption. Paid wedge: trust/readiness/attestation/services. The local commercialization synthesis is explicit: give away the wedge, sell governed, legible, auditor-acceptable attestation and readiness. [COMMERCIALIZATION-SYNTHESIS.md](/home/vrondelli/projects/domainspec-core/implementation/domainspec/development/COMMERCIALIZATION-SYNTHESIS.md:33)

Initial buyer: CTO/product/engineering leaders using AI agents whose work cannot be safely reviewed; BI/ops leaders with distrusted metrics; confidential-workflow teams needing custody/readiness; regulated or enterprise-selling teams worried about change-control evidence. Local BP research recommends narrow paid witnessed trust/readiness engagements now, not product claims. [findings.md](/home/vrondelli/projects/domainspec-core/.arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md:20)

Offer shape: 2-4 week AI-dev readiness or metric trust sprint producing source chain, denominator/confound notes, owner decision, privacy/reuse boundary, readiness scorecard, and receipt bundle. This fits current external pressure around AI agent audit logging, governance controls, and AI risk frameworks while avoiding compliance guarantees.

**Defensibility Stack**
Governance data: repeated engagements produce structured receipts, owner decisions, gates, trace links, and non-claims. This is the compounding asset, not a one-off consulting memo.

Receipts and attestation: local L1 attestation has a built valid/tampered discriminator; L2 external signature remains intended-not-shipped. Claim as integrity specimen, not external assurance. [attestation-capability-moat-mvp-synthesis.md](/home/vrondelli/projects/domainspec-core/.arcanum/inventory/entries/attestation-capability-moat-mvp-synthesis.md:28)

Switching cost: once a client’s definitions, evidence chains, owner decisions, readiness gates, and audit narratives live in the governed corpus, replacement cost rises because the artifact is not just docs; it is operating memory plus claim boundaries.

Verticalization: strongest paid path is services into specific workflows first, then repeated receipts across similar buyer contexts. Generic platform-first is weaker because Credo/Trustible/Vanta-style governance and Northflank/Proofpoint/TrueFoundry-style infrastructure already own broad platforms.

Formal witnesses: Lean/formalization amplifies scoped claims when there is a theorem/checker/specimen attached. It is not the core moat today; local machine-map synthesis says the moat is attestation + governance data + vertical, with provability a conjectural amplifier. [machine-map-and-moat-synthesis.md](/home/vrondelli/projects/domainspec-core/.arcanum/inventory/entries/machine-map-and-moat-synthesis.md:24)

**Forbidden Investor/Public Claims**
Do not claim: certified, certification-ready headline, ISO/IEC 42001 compliant, EU AI Act compliant, conformity assessed, third-party audit-ready, auditor-approved, formally verified platform, provably correct agents, public verifier available, external-signature attestation complete, regulatory compliance achieved, or receipts prove truth. Local assurance findings forbid the same set. [findings.md](/home/vrondelli/projects/domainspec-core/.arcanum/inventory/queries/2026-07-06-ai-assurance-certification-vocabulary-research/findings.md:228)

Do not claim market uniqueness: “no one,” “only competitor,” “Kodamai-only,” “first,” or “only platform” should be avoided. Checked sources show multiple adjacent live categories: SDD tools, requirements/traceability incumbents, AI governance platforms, formal methods, and AI agent security/audit systems.

Do not claim completed autonomous governance platform, public-ready DomainSpec v2/CAV2, whole-system correctness, or at-scale assurance. The local dispatch strategy explicitly leaves strong market language gated on dated external checks and strong correctness language gated on runnable/formal witnesses. [spec-driven-completeness-moat-inventory-strategy-result-synthesis.md](/home/vrondelli/projects/domainspec-core/.arcanum/inventory/entries/spec-driven-completeness-moat-inventory-strategy-result-synthesis.md:108)

**Next External Validation Queue**
1. Kodamai/Kelvingrove: archive current homepage/security/research pages with screenshots; look for any public proof artifact, checker, proof assistant, API docs, patent, or technical whitepaper.
2. Buyer interviews: 10-15 CTO/compliance/security leaders on whether “AI work readiness package” maps to an urgent budget, and which artifact closes procurement friction.
3. Comparator teardown: Kiro, Spec Kit, OpenSpec, Jama, Polarion, Credo AI, Proofpoint, TrueFoundry, Northflank: compare artifact model, authority owner, traceability depth, audit export, evidence tamper-resistance, and integration surface.
4. Standards crosswalk: produce a non-certifying NIST AI RMF / ISO 42001 / EU AI Act vocabulary map with explicit “not compliant” boundaries.
5. Public specimen: one bounded assurance-case demo with derived obligations/tests, owner decision, receipt, L1 attestation, positive/negative mutation, and “what this does not prove.”
6. Pricing validation: test paid service packages before product tiers: Metric Trust Sprint, AI Work Readiness Diagnostic, Confidential AI Workflow Readiness, Guided Governance Onboarding.
