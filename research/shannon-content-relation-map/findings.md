# Findings: Shannon Content Relation Map

Dispatch: `2026-06-19-shannon-content-relation-map`

This is a Shannon-centered relation map. It starts from the local Shannon tower
and asks how repository surfaces witness, analogize, constrain, or risk misusing
Shannon anchors. It is not a self-map of DomainSpec, Arcanum, Ontologize,
CyberAlchemy, or Lean.

The governing boundary is local-only: Shannon terms here are research anchors,
not promoted canonical vocabulary, runtime contracts, product language, Lean
definitions, or ontology entries. Any promotion requires a separate governed
decision. [Wiener-R1] `research/claude-shannon-secrecy-systems/DEFINITIONS.md`,
`research/claude-shannon-secrecy-systems/tracks/bridge-decisions.md`;
[Shannon-R1] `arcanum/arcana/inventory/SKILL.md`,
`arcanum/arcana/ontology-vault/SKILL.md`; [Spivak-R1]
`projects/framework-unification/CONCEPT-MAP.md:156`

## Core Finding

The strongest transfer is not "secrecy" as a broad metaphor. The useful Shannon
spine is hidden state, visible artifact, observer, prior/posterior update, and
remaining uncertainty. Repository artifacts such as generated skill mirrors,
inventory pages, telemetry rows, dispatch packets, scorecards, product pages,
and Lean prose can update an observer's belief, but they do not automatically
become authority. [Wiener-R1] `research/claude-shannon-secrecy-systems/NOTATION.md:20`;
[Shannon-R1] `.arcanum/inventory/schema.md`,
`.arcanum/observability/README.md`; [Spivak-R1]
`projects/framework-unification/layers/domainspec-language/SCHEMA-INVENTORY.md:86`;
[Bateson-R1]
`projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/SCORECARD-SPEC.md`

## Relation Map

| Anchor / local abstraction | Owning artifact | Evidence/witness paths | Source kind(s) | Relation type | Authority status | Useful consequence | Boundary/risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Observer prior/posterior | Shannon tower notation and operator bridge | `research/claude-shannon-secrecy-systems/NOTATION.md:20`; `.arcanum/inventory/schema.md`; `.arcanum/observability/README.md`; `projects/framework-unification/layers/domainspec-language/SCHEMA-INVENTORY.md:86` | `primary-source`; `operator-reading` | Strong operator model | Local relation only | When this Shannon lens is used, the review should name the observer, prior belief, observed artifact, posterior update, and remaining uncertainty. [Wiener-R1][Shannon-R1][Spivak-R1] | An artifact is not a cryptogram, and an update is not an authority promotion. [Shannon-R1] |
| Hidden state vs visible artifact | Local operator-reading abstraction derived from the Shannon tower | `research/claude-shannon-secrecy-systems/DISTILLED-KNOWLEDGE.md:46`; `arcanum/registry/SIGILS.md:1-5`; `.agents/skills/inventory/SKILL.md:1-7`; `.claude/skills/inventory/SKILL.md:1-7`; `.arcanum/necronomicon/capabilities.json:7-20` | `operator-reading`; `analogy` | Strong diagnostic analogy | Local relation only | Generated mirrors, registries, and capability lists should be read as visible evidence whose authority depends on canonical source refs and promotion state. [Shannon-R1] | Mirror visibility can conceal source authority, public/private boundary, and drift. Trace `canonical_source` before authority claims. [Shannon-R1] |
| Secrecy system / transformation family | Shannon tower definition; local route-selection analogy | `research/claude-shannon-secrecy-systems/DEFINITIONS.md:19`; `arcanum/formulae/dispatch-spec/SKILL.md`; `projects/framework-unification/layers/domainspec-language/README.md:24`; `projects/framework-unification/layers/domainspec-language/DOMAINSPEC-LANGUAGE-HANDOFF.md:33` | `primary-source`; `analogy` | Analogy only | Not promoted | Dispatch routes and language contracts can be viewed only as a governed route-selection analogy whose validity depends on explicit inputs, owners, receipts, and route shape. [Wiener-R1][Shannon-R1][Spivak-R1] | Local routes are non-keyed, non-reversible, non-cryptographic, and not transformations over `M,K,E,T_i`. [Lawvere-R1][Shannon-R1] |
| Perfect secrecy | Shannon tower definition; Lean preservation surfaces as warning analogy | `research/claude-shannon-secrecy-systems/DEFINITIONS.md:7`; `research/claude-shannon-secrecy-systems/tracks/bridge-decisions.md:11`; `domainspec-lean-formalization/README.md:27`; `domainspec-lean-formalization/docs/domainspec-two-layer-framework.md:145`; `domainspec-lean-formalization/GLOSSARY.md:178` | `primary-source`; `analogy` | Mostly block; warning analogy only | Blocked for general repo vocabulary | The only safe local use is as a warning: "no update" is a precise condition, not a synonym for strong governance, privacy, or security. [Wiener-R1][Lawvere-R1] | Do not equate perfect secrecy with zero-residue or full faithfulness unless a formal probability update relation over messages, keys, and cryptograms is introduced. [Lawvere-R1] |
| Equivocation | Shannon tower definition; residue and scorecard witnesses are non-synonym local analogies | `research/claude-shannon-secrecy-systems/DEFINITIONS.md:30`; `research/claude-shannon-secrecy-systems/tracks/bridge-decisions.md:12`; `domainspec-lean-formalization/lean-formalization/Residue.lean:84`; `domainspec-lean-formalization/lean-formalization/Residue.lean:229`; `projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/SCORECARD-SPEC.md:80-122` | `primary-source`; `local-inference`; `analogy` | Borrow carefully; promotion candidate only with a decision | Not promoted | Equivocation is a possible bridge for remaining uncertainty only when carrier, candidate set, observer, observation, and uncertainty measure are explicit. [Wiener-R1][Lawvere-R1][Bateson-R1][Spivak-R1] | Equivocation is not a synonym, subtype, or metric for repo `residue` until a governed decision defines it. Do not use it as decorative ambiguity. [Spivak-R1][Bateson-R1] |
| Redundancy | Shannon tower notation; generated mirrors and signal/noise formal surfaces as local witnesses | `research/claude-shannon-secrecy-systems/NOTATION.md:32`; `research/claude-shannon-secrecy-systems/tracks/paper-claim-ledger.md:13`; `domainspec-lean-formalization/lean-formalization/SignalNoiseDecomposition.lean:61`; `.agents/skills/inventory/SKILL.md:1-7`; `.claude/skills/ontology-vault/SKILL.md:1-7` | `primary-source`; `analogy`; `local-inference` | Analogy / local inference | Local relation only | Redundancy is useful for spotting duplicated generated surfaces and schema under-typing: repeated visible material can help lookup but also creates drift and false-authority risk. [Wiener-R1][Lawvere-R1][Shannon-R1] | Shannon's language redundancy `D` is not modeled for repository text, generated mirrors, or schema drift. [Lawvere-R1] |
| Unicity distance | Shannon tower formula; Ontologize scorecard thresholds as analogy witness | `research/claude-shannon-secrecy-systems/DEFINITIONS.md:43`; `research/claude-shannon-secrecy-systems/examples/worked-examples.md:32`; `research/claude-shannon-secrecy-systems/tracks/bridge-decisions.md:14`; `domainspec-lean-formalization/lean-formalization/SecondLawDiscrete.lean:119`; `projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/SCORECARD-SPEC.md:80-122`; `projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/RESULTS.md:3-14` | `primary-source`; `analogy`; `open-residue` | Analogy only | Block formula; allow governed threshold design | The repo can borrow the idea of ambiguity-collapse thresholds for scorecards, evidence grades, owner review, and promotion rules. [Wiener-R1][Lawvere-R1][Bateson-R1] | Never apply `H(K)/D` quantitatively to product validation, dispatch, Lean residue, or repo artifacts. `RESULTS.md` is only a gap witness, not threshold evidence. [Wiener-R1][Lawvere-R1] |
| Confusion / diffusion | Shannon tower definition; CyberAlchemy/Ontologize traceability witnesses | `research/claude-shannon-secrecy-systems/DEFINITIONS.md:54`; `research/claude-shannon-secrecy-systems/examples/worked-examples.md:45`; `cyberAlchemy/ontology/source-ledger.md:42-56`; `projects/ontologize/RECONCILIATION.md`; `projects/ontologize/ONTOLOGY-BRANCHES.md:19-49` | `primary-source`; `analogy`; `operator-reading` | Analogy only | Local relation only | The useful local version is traceable separation: provenance, meaning, system, run-context, and bridge material should not silently collapse into one artifact. [Wiener-R1][Bateson-R1] | Confusing documentation is not Shannon confusion, and spreading files is not Shannon diffusion. [Bateson-R1] |
| Theoretical vs practical secrecy | Shannon tower final pack; framework proof/operation boundary | `research/claude-shannon-secrecy-systems/FINAL-LEARNING-PACK.md:32`; `research/claude-shannon-secrecy-systems/tracks/paper-claim-ledger.md:11`; `projects/framework-unification/SCOPE.md:21`; `projects/framework-unification/layers/cyber-alchemy-lean-fusion/DESIGN.md:57` | `primary-source`; `local-inference` | Strong boundary distinction | Local relation only | Keep "what remains uncertain" separate from "what work remains" and keep formal proof separate from operational proof. [Wiener-R1][Spivak-R1] | Do not state that Shannon or Lean certifies an Arcanum run, product claim, or operational transformation. [Lawvere-R1][Spivak-R1] |
| Enemy knows the system / public inspection robustness | Shannon tower claim; product/public authority ladder witnesses | `research/claude-shannon-secrecy-systems/tracks/paper-claim-ledger.md:15`; `projects/ontologize/PUBLIC-OFFERING.md:46-54`; `projects/ontologize/PRODUCT.md:3-6`; `cyberAlchemy/ontology/entries/knowledge-governance-authority-ladder.md:114-126` | `primary-source`; `operator-reading` | Borrow carefully | Local relation only | Public inspection robustness: public and product claims should survive inspection through citations, confidence labels, owner routes, and clear boundaries rather than depending on hidden private scaffolding. [Wiener-R1][Bateson-R1] | This is not a full modern threat model and must not imply security guarantees. [Wiener-R1][Bateson-R1] |
| Open residue as residual uncertainty | Shannon tower residue map; framework, Arcanum, and scorecard uncertainty witnesses | `research/claude-shannon-secrecy-systems/levels/L1-residue-map.md:5`; `projects/framework-unification/SCOPE.md:61`; `projects/framework-unification/CONCEPT-MAP.md:156`; `arcanum/arcana/ontology-vault/SKILL.md`; `projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/SCORECARD-SPEC.md:80-92` | `open-residue`; `operator-reading` | Strong governance transfer | Local relation only | Residue should remain visible as open questions, contradiction, `flag`, `block`, scorecard inconclusive, or promotion blocker instead of being smoothed into narrative certainty. [Shannon-R1][Spivak-R1][Bateson-R1] | Open residue is not the same as Shannon equivocation unless candidate set, observation, observer, and remaining uncertainty are all defined. [Wiener-R1][Spivak-R1] |

## Cross-Return Synthesis

All lanes converge on an evidence discipline: visible artifacts update belief,
not authority. When this Shannon lens is used, the relation map should preserve
four distinctions: Shannon source claim vs repo analogy, observed artifact vs
canonical source, uncertainty reduction vs promotion, and formal proof vs
operational decision.
[Wiener-R1][Lawvere-R1][Shannon-R1][Bateson-R1][Spivak-R1]

`Equivocation` is the highest-value vocabulary candidate and the highest-risk
one. It is only a possible bridge for residual uncertainty; it is not a synonym,
subtype, or metric for repo `residue` until a governed decision defines the
carrier, candidate set, observation, uncertainty measure, accepted source kinds,
and forbidden uses. [Wiener-R1]
`research/claude-shannon-secrecy-systems/DEFINITIONS.md:30`; [Lawvere-R1]
`domainspec-lean-formalization/lean-formalization/Residue.lean:84`;
[Spivak-R1] `projects/framework-unification/CONCEPT-MAP.md:156`

`Perfect secrecy` should mostly function as a boundary object. It teaches the
precision of "observation causes no update," but the repo should not use it as a
metaphor for good governance, public/private separation, or security.
[Wiener-R1] `research/claude-shannon-secrecy-systems/tracks/bridge-decisions.md:11`;
[Lawvere-R1] `domainspec-lean-formalization/README.md:27`

`Unicity distance`, `confusion`, and `diffusion` are useful only as
analogy-level prompts. They can inspire operational threshold design and
traceable separation, but the Shannon formulas and cryptographic mechanisms
must not be imported into repo claims. [Wiener-R1]
`research/claude-shannon-secrecy-systems/DEFINITIONS.md:43`,
`research/claude-shannon-secrecy-systems/DEFINITIONS.md:54`; [Bateson-R1]
`projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/SCORECARD-SPEC.md`;
[Spivak-R1] `arcanum/TO-VLAD/DISPATCH-COMPOSITION-MODEL.md:42`

## Open Residue

- Shannon's 1945 report, MTC, and modern cryptography crosswalk remain out of
  scope for this map and should not be implied by it. [Wiener-R1]
  `research/claude-shannon-secrecy-systems/levels/L1-residue-map.md:9`
- The repo has no formal Shannon secrecy system: no message space, key source,
  cryptogram, reversible key-indexed transformation family, posterior update
  calculus, conditional entropy theorem, redundancy-rate model, or
  unicity-distance derivation. [Lawvere-R1]
  `domainspec-lean-formalization/lean-formalization/Residue.lean`,
  `domainspec-lean-formalization/lean-formalization/KLDivergence.lean`
- The `equivocation` bridge needs a promotion decision before any canonical use.
  The decision must specify whether it is a synonym, subtype, metric, glossary
  entry, or blocked term relative to existing residue language.
  [Wiener-R1][Lawvere-R1][Spivak-R1]
- Public-facing Ontologize and CyberAlchemy material still needs claim-by-claim
  review before Shannon-inspired framing is used externally. [Bateson-R1]
  `projects/ontologize/PUBLIC-OFFERING.md`, `projects/ontologize/PRODUCT.md`,
  `cyberAlchemy/README.md`
- Generated skill mirrors, telemetry rows, and inventory surfaces need explicit
  authority tracing when used as witnesses in future relation maps. [Shannon-R1]
  `.agents/skills/inventory/SKILL.md`, `.claude/skills/inventory/SKILL.md`,
  `.arcanum/observability/README.md`

## Suggested Next Governed Decisions

1. Decide whether to create a local-only Shannon relation vocabulary note that
   remains under `research/` and explicitly blocks promotion.
   [Wiener-R1][Shannon-R1]
2. Decide whether `equivocation` should become a governed promotion candidate,
   and if so require a definition card with candidate set, observer,
   observation, uncertainty measure, anti-misuse guidance, and relation to
   `residue`. [Wiener-R1][Lawvere-R1][Spivak-R1]
3. Decide whether product scorecards may use Shannon-inspired language at all.
   If yes, constrain it to uncertainty-reduction phrasing and ban secrecy or
   security language. [Bateson-R1]
4. Decide whether framework-unification should add an epistemic field model
   using `hidden_state`, `visible_artifact`, `observer`, `evidence_state`, and
   `residue`, while keeping Shannon terms out of syntax-layer vocabulary.
   [Spivak-R1]
5. Decide whether future Lean work needs a true Shannon formalization lane, or
   whether the present map should permanently mark Lean connections as
   analogy/operator-reading only. [Lawvere-R1]

## Local Boundary

This findings draft preserves the dispatch boundary: Shannon anchors are
relation anchors for local research only. They do not promote any canonical
DomainSpec, Arcanum, Ontologize, CyberAlchemy, product, runtime, inventory,
ontology, or Lean vocabulary. [Wiener-R1][Shannon-R1][Spivak-R1]
