# Co-Op Project Showcase And Recruitment Research Strategy

Status: resolved, parent accepted

## Corrected Scope

The Co-Op Engine already exists as a 45-minute weekly meeting. This research
does not redesign it into an exchange, matching service, or workflow engine.
It investigates one browser-native project showcase that can be used both as
the live presentation and as a self-guided recruitment page.

The artifact should open with a strong portfolio-level idea, give each project
a brief but substantial and memorable opening, and progressively disclose
deeper context, current evidence, limits, trajectory, and concrete ways to
help.

## Solution-Independent Problem

A Co-Op visitor needs to understand which projects matter to them, trust what
is real, and see a concrete way to contribute without reading fourteen
mini-specifications or being sold finished products.

## P1 Trigger

All four triggers apply:

- synthesis across current external web precedents, fourteen project corpora,
  two audience types, live and self-guided use, recruitment, copy, and
  validation;
- context protection because the source and project evidence would overwhelm
  the parent context;
- isolation because competing information architectures and copy structures
  must remain discardable until attacked;
- parallelism because portfolio IA, live presentation, project truth, and
  recruitment decisions can be researched independently.

## Two-Lane Strategy

Lane Z builds and stress-tests the user's portfolio-first hypothesis:
portfolio opening -> compact project openings -> deeper project stories, with
the same artifact used live.

Lane A holds the visitor problem fixed and tests a genuinely different
decision-first route: problem, domain act, skill, or contribution first;
projects second.

The rejected decomposition was one agent per file or one agent per project.
That would duplicate the same content question fourteen times, hide the
portfolio-versus-recruitment tension, and produce summaries without an
architecture decision.

## Groups And Subagents

- `lane_z_explorers`, parallel with Robot Talks:
  - `Ahrens, Sönke`, explorer: comparative portfolio and progressive-disclosure
    patterns; output is a sourced precedent matrix and overview-to-detail
    recommendation with counterexamples.
  - `Senge, Peter`, explorer: live presentation and audience-use patterns;
    output is a live storyboard and presenter/self-guided surface contract.
- `lane_a_explorers`, parallel with Robot Talks:
  - `Alexander, Christopher`, explorer: current fourteen-project truth and
    content constraints; output is one bounded truth record per project plus a
    shared 10-second/30-second/deep-detail grammar.
  - `Christensen, Clayton`, explorer: contributor recruitment and
    jobs-to-be-done patterns; output is a decision-first alternative, CTA
    ladder, and trust/abandonment matrix.
- `synthesizer`:
  - `Simon, Herbert`: compares both lanes and produces bridge decisions, a
    recommended architecture, an alternative, fourteen opening-content maps,
    a Whisper intake substrate, and evidence plans.
- `reviewers`, parallel with Robot Talks:
  - `Popper, Karl`: precedent gate.
  - `Taleb, Nassim Nicholas`: non-vacuity gate.
  - `Quine, Willard Van Orman`: definitional-soundness gate.
- `writer`:
  - `Drucker, Peter`: writes `findings.md` only.
- `auditor`:
  - `Brandenburg, Martin`: audits `findings.md` only and recommends acceptance
    or one bounded revision.

## Dependency Flow

```text
lane_z_explorers ─┐
                  ├─> synthesizer <-> reviewers -> writer -> auditor
lane_a_explorers ─┘                               ^          |
                                                   └ feedback ┘
```

The synthesis/reviewer zig-zag is capped at two loops. Auditor-to-writer
revision is capped at one. The whole dispatch is capped at two loops.

## Strategy Inventory Packet

- Lookup status: `ready`.
- Machine index: `.arcanum/inventory/index.json`.
- Machine index generated: `2026-07-26T09:55:52Z`.
- Human-index fallback: not used.
- Query terms: Co-Op Engine, project showcase, portfolio, recruitment,
  progressive disclosure, index-to-detail, live presentation, Whisper,
  project voice, conversational AI copy, comprehension, retellability,
  browser evidence, and the fourteen project names.

Selected entries:

| Entry ID | Path and selectors | Status / confidence | Tags | Obligation fit and summary | Source references |
| --- | --- | --- | --- | --- | --- |
| `co-op-engine-portfolio-research-result-synthesis` | `.arcanum/inventory/entries/co-op-engine-portfolio-research-result-synthesis.md`; `#accepted-product-substrate`, `#acceptance-evidence-boundary`, `#typed-negatives-and-residue` | verified / high | `project-portfolio`, `typed-negative`, `claim-le-proof` | Seeds the fourteen claim ceilings, audience split, copy guardrails, and audit boundaries. Its Exchange selection is rejected for this corrected goal. | `ops/development/2026-07-25-co-op-engine-portfolio-research/findings.md`, its transcript and gate artifacts |
| `entries-investor-bp-project-portfolio-strategy-result-synthesis` | `.arcanum/inventory/entries/investor-bp-project-portfolio-strategy-result-synthesis.md`; `## Accepted Result`, `## Residue` | closed / high | `commercialization`, `public-private-boundary`, `whisper` | Supplies internal project-positioning and claim-boundary leads, not a collaborator-facing hierarchy. | `.arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md` and its dispatch artifacts |
| `investor-bp-project-portfolio-research-findings` | `.arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md`; whole accepted synthesis | accepted / medium | `investor-bp`, `claim-le-proof`, `public-private-boundary` | Gives source leads across project candidates; citation roughness and investor purpose require independent re-verification. | its `research.md`, proposal, and tension receipt |
| `entries-unified-ide-ergonomics-spine-synthesis` | `.arcanum/inventory/entries/unified-ide-ergonomics-spine-synthesis.md`; `Decision spine`, `The witness`, `Open residue` | candidate / high | `ide-ergonomics`, `unified-spine`, `build-from-owned` | Supplies a project-specific decision-spine lead while preserving its draft and analogy limits. | `projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md`, `PRODUCT-VIEW.md`, and accepted findings |
| `ui-prototyping-studio-ux-ui-upgrade-research-strategy-result-synthesis` | `.arcanum/inventory/entries/ui-prototyping-studio-ux-ui-upgrade-research-strategy-result-synthesis.md`; dispatch, top-upgrade, and auditor selectors | closed / high | `ux-lessons`, `artifact-governance`, `operational-evidence` | Supplies interaction-state, mobile, reversible-action, and evidence-integrity leads for the project detail surface. | Studio UX research transcript and findings |
| `whisper-concision-reading-flow-maintenance-review-strategy-result` | `.arcanum/inventory/entries/whisper-concision-reading-flow-maintenance-review-strategy-result-synthesis.md`; `#accepted-result`, `#residue` | verified / high | `review-change-request`, `public-private-boundary`, `claim-le-proof` | Supplies reading-flow and transport-ownership constraints while keeping private project language out of public Arcanum. | maintenance findings, Whisper README, text-intent schema |
| `domainspec-v2-bte-xray-copy-readability-review-result` | `.arcanum/inventory/entries/domainspec-v2-bte-xray-copy-readability-review-result.md`; `#accepted-review-result`, `#copy-and-example-boundary` | verified / high | `human-view`, `operational-evidence`, `claim-le-proof` | Supplies cold-reader flow, mobile meaning, and future-as-future claim guidance. | copy/readability attacks and findings |
| `domainspec-v2-bte-xray-conversational-language-audit-result` | `.arcanum/inventory/entries/domainspec-v2-bte-xray-conversational-language-audit-result.md`; `#accepted-audit-result`, `#applied-whisper-consequence` | verified / high | `human-view`, `machine-view`, `claim-le-proof` | Supplies state separation and assistant-coaching removal for the chat/copy audit. | conversational-language attacks, findings, and Whisper result |
| `craft-causal-class-total-refresh-review-strategy-result-synthesis` | `.arcanum/inventory/entries/craft-causal-class-total-refresh-review-strategy-result-synthesis.md`; slide/state/Playwright and learner-trial selectors | closed / high | `audit`, `machine-view`, `public-private-boundary` | Supplies browser-observed presentation mechanics and the explicit limit that layout/mechanics do not prove learning. | Craft teaching review, replacement README, and validation report |

Selected evidence-card IDs:

- `entries-evidence-cards-2026-06-24-unified-ide-ergonomics-spine-cards`:
  selector-level lead for the IDE Ergonomics project card; it remains
  candidate Inventory evidence and must be followed to current sources.

Selected EvidenceSet IDs: none. No indexed set fits the corrected
showcase/recruitment obligations closely enough to justify passing one to all
lanes.

Excluded evidence:

- the prior Co-Op Experiment Exchange mechanism, admission state machine,
  appointment lifecycle, SLA, expiry, and receipt flow because they answer a
  different product question;
- investor portfolio prioritization as the public page hierarchy because an
  investor decision is not a collaborator's decision;
- Nimbalyst integration and other IDE-specific implementation findings because
  they do not decide cross-project portfolio IA;
- raw simple-ontology-presentation returns where accepted findings supersede
  wording.

Gaps and residue:

- Inventory contains no current external precedent survey for this corrected
  showcase/recruitment question. This is `no_inventory_match`, not
  `precedent-clean`.
- No source-backed comparison yet establishes whether project-first,
  contribution-first, problem-first, or a hybrid entry route works best.
- The fourteen projects do not share a currently owner-admitted public content
  schema, and several names/roots/statuses remain unresolved.
- Browser behavior cannot establish understanding or recruitment intent;
  human retellability and decision evidence remain separate.
- Inventory is a non-authority discovery read model and does not authorize
  public copy, implementation, or promotion.

Design consequences:

- external source research focuses on portfolio/navigation, live-use, and
  recruitment patterns rather than meeting-mechanism design;
- the existing fourteen claim ceilings seed the local explorer but must be
  re-verified from current canonical sources;
- the final substrate must compare project-first and decision-first routes;
- Whisper receives structured, proof-bounded opening/detail inputs, not
  generic marketing copy;
- acceptance remains three distinct lanes: black-box browser behavior;
  conversational-AI/chat terminology and copy; and ease/coherence with human
  retellability and contribution-decision evidence.

## Gate And Ledger State

- Frozen sheet: `dispatch-sheet.json`.
- Confirmation readiness: `PASS`, schema `0.7.0`, ledger mutation `none`.
- Frozen sheet SHA-256:
  `af87013f928a664640923ad3e23087251341df900a4fd4c36722d8e0802555a6`.
- Check-tension:
  `tension-checker-2026-07-26-co-op-showcase-1 = PASS` and
  `tension-reviewer-2026-07-26-co-op-showcase-2 = PASS`.
- Human confirmation:
  `confirmation-2026-07-26-co-op-showcase-1`, bound to the frozen digest.
- Registration: appended once through the deterministic registrar.
- Research: completed with ten registered agents and two bounded loops.
- Reviewer outcome: precedent, research-plan non-vacuity, and definitional
  soundness all `PASS`.
- Dedicated auditor: `RECOMMEND_ACCEPT`.
- Parent final approval: `ACCEPT`; see `PARENT-VALIDATION.md`.
- Closeout: `resolved`; exactly one close row is appended after parent
  acceptance.

## Accepted Boundary And Next Route

The accepted result is the research substrate in `findings.md`, not a chosen
entrance, final copy, implemented page, deployment, or outcome proof. Owner
binding comes first; then Whisper may compose both candidate openings, Invoke
Design may specify the fixed specimen, and browser, copy, and human evidence
must be collected in separate lanes.
