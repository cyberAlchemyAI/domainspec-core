---
tags: [research, strategy-result, dispatch, subagents, investor-bp, domainspec-v2, cav2, deterministic-validation, completeness, formalization, lean, moat, commercialization, kodamai, claim-le-proof]
node_type: explore-strategy
is_session: false
layer: strategy
nature: proposal
status: proposed
created: 2026-07-06
dispatch_id: 2026-07-06-spec-driven-completeness-moat-inventory-research
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-07-06-spec-driven-completeness-moat-inventory-research/
sources: [.arcanum/inventory/index.json, .arcanum/inventory/index.md, .arcanum/inventory/entries/, .arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md, .arcanum/inventory/queries/2026-07-06-ai-assurance-certification-vocabulary-research/findings.md, implementation/domainspec/development/COMMERCIALIZATION-SYNTHESIS.md, .arcanum/inventory/entries/machine-map-and-moat-synthesis.md, .arcanum/inventory/entries/read-trivial-via-selective-promotion-synthesis.md, .arcanum/inventory/entries/kodamai-smithe-correctness-layer-synthesis.md, domainspec-lean-formalization/lean-engineer/, implementation/domainspec/scripts/audit_richness.py]
---

# Explore Strategy - Spec-Driven Completeness Moat Inventory Research

## P1 Trigger Decision

This is a dispatch proposal.

All four Principle-1 triggers hold:

- **Synthesis:** the run must combine full Inventory, two prior BP-adjacent
  research runs, commercialization synthesis, moat/machine-map synthesis,
  selective-promotion/read-trivial synthesis, Kodamai correctness comparison,
  Lean/formalization assets, deterministic audit tooling, product portfolio
  surfaces, and current market comparators.
- **Context protection:** the source set is too large for the parent session to
  carry without losing evidence granularity.
- **Isolation:** investor-facing differentiation language must be attacked
  before it influences the business plan.
- **Parallelism:** inventory evidence, deterministic validators, Lean/formal
  witnesses, compounding company reach, and market/comparator checks can be
  explored independently before synthesis.

The dispatch is **not yet registered or run**. The current gate state is double
PASS after revisions. Human confirmation is still required before registration
and execution.

## Goal

Sweep full Inventory plus named missed artifacts to produce an investor-BP
differentiation substrate. The run should verify or narrow the candidate claim
that DomainSpec is a spec-driven framework that can derive checks and
deterministically validate named structural obligations for the current corpus,
map what stronger completeness/correctness claims would require, show how owned
POCs compound into company reach, compare against checked market alternatives
and Kodamai as a closest located comparator only if checked evidence supports
that, and preserve `claim <= proof`.

This is not final BP copy. It is the research substrate and claim ladder that a
later BP should build from.

## Source Boundary

### Required Local Sources

Every required source must receive a cited row in the findings evidence
checklist:

- `.arcanum/inventory/index.json`
- `.arcanum/inventory/index.md`
- `.arcanum/inventory/entries/`
- `.arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md`
- `.arcanum/inventory/queries/2026-07-06-ai-assurance-certification-vocabulary-research/findings.md`
- `implementation/domainspec/development/COMMERCIALIZATION-SYNTHESIS.md`
- `.arcanum/inventory/entries/machine-map-and-moat-synthesis.md`
- `.arcanum/inventory/entries/read-trivial-via-selective-promotion-synthesis.md`
- `.arcanum/inventory/entries/kodamai-smithe-correctness-layer-synthesis.md`
- `domainspec-lean-formalization/lean-engineer/`
- `implementation/domainspec/scripts/audit_richness.py`

### Required Portfolio Sources

- `projects/domainspec-v2/`
- `cyberAlchemy-v2/`
- `cyberAlchemy-v2/development/research/2026-06-24-knowledge-market-product-idea/proposal-blueprint.md`
- `arcanum/arcana/craft/`
- `arcanum/spells/goal/`
- `.agents/skills/goal/SKILL.md`
- `.agents/skills/whisper/SKILL.md`
- `projects/ide-ergonomics/`
- `projects/ui-prototyping-studio/`
- `projects/ontologize/`
- `projects/savvy_legal-studio-ai/`
- `projects/autoads/`
- `arcanum/development/user-guide/`
- `research/tower-system-taxonomy/`
- `arcanum/research/mogt-agentic-conversation/`
- `domainspec-lean-formalization/`
- `../resonantos-economy-research/`
- `../maestro-trama/`

### Exclusions

`glyph/`, `grain/`, and Golden Quill are excluded from the scored portfolio
except as explicit excluded-source notes. Generated/worktree mirrors are
excluded unless explicitly named or needed for installed-runtime evidence.

## Required Output Shape

The confirmed run should produce:

- `research.md`: verbatim explorer returns only, appended by the strategist.
- `findings.md`: writer-authored and auditor-checked synthesis.

`findings.md` must include:

- required-source coverage table;
- evidence checklist table;
- split claim ladder for deterministic runnable validators/audits, Lean
  machine-checked witnesses, formal proof status, market differentiation, and
  future ambition;
- BP-safe claim ladder and forbidden language;
- comparator/market map with dated current external public/primary sources;
- compounding POC reach map;
- next witness queue.

Every load-bearing claim must cite `research.md` and source evidence. The
auditor must fail missing required-source rows, missing index/entry
reconciliation, missing dated external checks, unbounded "unique" / "no one"
language, broad formal-proof/completeness language, or investor/public phrasing
that exceeds the evidence map.

## Lanes / Groups

| Group | Purpose | Role | Anti-bias axis | Dependency |
| --- | --- | --- | --- | --- |
| `evidence-explorers` | Inventory, deterministic validation, and formal witness evidence. | 3 parallel explorers with robot-talks. | composite `source-corpus + methodology + temporal-prior` | Starts first. |
| `business-market-explorers` | Company reach, commercialization, and current comparator map. | 2 parallel explorers with robot-talks. | composite `source-corpus + methodology + temporal-prior` | Starts first. |
| `synthesizer` | Reconcile explorer evidence into candidate thesis, claim ladder, and BP substrate. | 1 synthesizer. | n/a | After both explorer groups. |
| `reviewers` | Attack the candidate thesis. | 3 parallel skeptics with robot-talks. | `attack-vector` | Zig-zag from synthesizer. |
| `writer` | Persist `findings.md` only. | 1 writer. | n/a | After reviewer convergence. |
| `auditor` | Final approval over `findings.md`. | 1 dedicated auditor and final approver. | n/a | After writer. |

## Subagents

| Agent | Role | Angle | Expected output |
| --- | --- | --- | --- |
| Shannon, Claude | explorer | Inventory-wide evidence census. | Required-source coverage table; claim/evidence/gap matrix; BP-safe wording; missing-source flags. |
| Turing, Alan | explorer | Deterministic derivation/completeness validator audit. | Exact meaning and limits of deterministic validation, including structural completeness/richness versus semantic/runtime correctness. |
| Grothendieck, Alexander | explorer | Lean/formal witness audit. | What is machine-checked; theorem/proof/specimen status; what cannot be called formal proof of completeness. |
| Beer, Stafford | explorer | Company-reach / compounding POC map. | DomainSpec v2 and CAV2 primacy; compounding reach across owned POCs, receipts, gates, proof residue, and reusable operating system; explicit exclusions. |
| Porter, Michael | explorer | Commercialization and external market/comparator map. | Dated Kodamai/Kelvingrove and adjacent-market checks; comparator map; buyer wedge; defensibility; safe uniqueness phrasing. |
| Simon, Herbert | synthesizer | Bounded-rationality synthesis. | Candidate thesis, differentiation map, claim ladder, public/internal/current/future split, and dogfood/internal/future/external-offer split. |
| Popper, Karl | skeptic | Precedent gate. | Narrow or demote "only", "no one", "Kodamai-only", and market-uniqueness claims. Precedent never auto-kills. |
| Taleb, Nassim Nicholas | skeptic | Non-vacuity gate. | Kill or downgrade claims without runnable witness, dated source, cited artifact, buyer signal, or falsifiable next test. |
| Quine, Willard Van Orman | skeptic | Definitional-soundness gate. | Definitions and collapse tests for spec-driven, derive, validate completeness, deterministic completeness, formal proof, correctness, market uniqueness, comparator, and company reach. |
| Drucker, Peter | writer | Findings author. | `findings.md` only: BP differentiation substrate, evidence checklist, claim ladder, market map, compounding reach map, forbidden language, and next witness queue. |
| Brandenburg, Martin | auditor | Final approver. | Accept/reject `findings.md`; fail missing evidence rows, overclaims, missing external checks, or public language beyond proof. |

## Predicted Disagreement Design

### Evidence Explorers

- Shannon vs Turing, axis `source-corpus + methodology`: Shannon runs
  inventory/semantic evidence and can over-trust recorded language; Turing runs
  executable validators and exposes that bias by demoting any phrase not backed
  by runnable deterministic checks. Shannon exposes Turing's too-narrow tool
  bias by surfacing cited evidence from inventory/query findings that a
  script-only audit would miss.
- Shannon vs Grothendieck, axis `source-corpus + methodology`: Shannon runs
  proof/moat inventory entries and can treat claims as evidence; Grothendieck
  runs Lean/formal witness status and exposes that bias by separating
  machine-checked witness, theorem, open sorry, and prose claim. Shannon
  exposes Grothendieck's formal-isolation bias by showing where formal artifacts
  matter only through surrounding commercialization/evidence context.
- Turing vs Grothendieck, axis `methodology`: Turing runs deterministic
  validators/audits and can collapse structural checks into proof language;
  Grothendieck runs formal semantics/proof status and exposes that bias by
  requiring exact proof-obligation labels. Turing exposes Grothendieck's
  proof-purity bias by identifying runnable deterministic witness value that is
  commercially useful before a full theorem.

### Business / Market Explorers

- Beer vs Porter, axis `source-corpus + methodology + temporal-prior`: Beer
  runs internal viable-system/compounding POC evidence and can over-read
  coherent platform leverage; Porter runs current external market/comparator
  and buyer evidence and exposes that bias by identifying commodity categories,
  competitors, and unfocused portfolio risk. Beer exposes Porter's
  market-category bias by showing the receipt/gate/proof-residue operating
  system that makes the portfolio more than adjacent products.

### Reviewers

- Popper vs Taleb, axis `attack-vector`: Popper runs precedent and can
  over-demote by market similarity; Taleb runs witness/non-vacuity and exposes
  that bias by preserving differentiated claims with concrete witnesses.
  Popper exposes Taleb's witness-only bias by showing where current market
  precedent narrows even a witnessed claim.
- Popper vs Quine, axis `attack-vector`: Popper runs market/precedent labels
  and can import vague category language; Quine runs definitions and exposes
  that bias by requiring each category to preserve distinct meaning. Popper
  exposes Quine's definition-local bias by testing whether terms survive
  outside repo-internal vocabulary.
- Taleb vs Quine, axis `attack-vector`: Taleb runs non-vacuity and can reduce
  claims to artifact-counting; Quine runs definitional-soundness and exposes
  that bias by checking whether the artifact proves the defined claim. Taleb
  exposes Quine's wording-only bias by requiring a runnable/cited witness for
  each refined definition.

## Dependency Flow

```text
evidence-explorers ---------\
                             +--> synthesizer -> reviewers -> writer -> auditor
business-market-explorers --/
                                      ^             ^                  |
                                      |             |                  |
                     conditional feedback     zig-zag loop 1     feedback loop 1
```

Connections:

- `evidence-explorers -> synthesizer`: sequential.
- `business-market-explorers -> synthesizer`: sequential.
- `synthesizer -> reviewers`: zig-zag, `loop_cap: 1`.
- `synthesizer -> evidence-explorers`: feedback, `loop_cap: 1`, only if
  required evidence rows are missing.
- `synthesizer -> business-market-explorers`: feedback, `loop_cap: 1`, only if
  portfolio/comparator coverage is missing.
- `reviewers -> writer`: sequential.
- `writer -> auditor`: sequential.
- `auditor -> writer`: feedback, `loop_cap: 1`.

## Gate / Ledger State

- Check-tension gate: current double PASS after revisions and active mirror
  sync.
- Current PASS agents:
  - `019f3603-b949-79e0-9c99-76c2bea69f8e` (Mencius)
  - `019f3603-b9f6-7050-9020-7f7cc83077c2` (Lorentz)
- Gate artifact: [CHECK-TENSION.md](CHECK-TENSION.md).
- Dispatch proposal JSON: [DISPATCH-PROPOSAL.json](DISPATCH-PROPOSAL.json).
- Registration state: unregistered.
- Ledger state: no dispatch row and no close row appended.
- Closeout expectation after confirmation/run: append dispatch row before
  launch; append close row after auditor acceptance or failure; inventory the
  final `research.md` and `findings.md`.

## Next Human Action

Reply `confirmed` to freeze, register, and run this strategy. Otherwise revise
the sheet or decline the dispatch.
