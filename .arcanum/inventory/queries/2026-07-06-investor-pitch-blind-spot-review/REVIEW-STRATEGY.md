---
tags: [inventory, strategy-result, dispatch, subagents, review, investor-bp, blind-spots, pitch, claim-le-proof, public-private-boundary]
node_type: review-strategy
is_session: false
layer: strategy
nature: proposal
status: candidate
created: 2026-07-06
dispatch_id: 2026-07-06-investor-pitch-blind-spot-review
dispatch_type: review
---

# Investor Pitch Blind-Spot Review Strategy

Status: proposed review dispatch. This is not a registered dispatch, not a
business plan, and not investor-facing prose. It is a pre-confirmation strategy
sheet for red-teaming the investor story and turning the blind spots into
verified change requests.

## P1 Trigger Decision

Dispatch is justified.

- **Synthesis:** the review must combine the latest user thesis, the investor
  portfolio findings, the AI assurance vocabulary findings, the spec-driven
  completeness/moat findings, the novel model-use findings, and the root-wide
  claim-boundary memory.
- **Context protection:** each source is dense enough that raw parent synthesis
  would be too large and easy to flatten.
- **Isolation:** attacks should be discardable until verified, because some
  critiques will be plausible but false.
- **Parallelism:** investor-focus, proof, definition, and falsifiability attacks
  can run independently before reconciliation.

## Target Thesis Under Review

The thesis to attack:

> With the right storytelling, the pitch can be exceptionally strong because
> the repository shows what two dedicated people produced in roughly three
> months: DomainSpec/CAV2 plus a spread of POCs, research lanes, consulting
> wedges, and future product surfaces. That reach is not random sprawl; it is
> evidence of a system that builds systems. Because the system is trustworthy,
> auditable, source-linked, and claim-boundary governed, the company can explore
> several revenue routes while preserving investor-safe proof discipline.

The review must preserve the positive thesis where it survives. The goal is not
to shrink the story. The goal is to make the compounding effect investable
without implying a finished platform, certification/compliance, public-ready
engine, autonomous governance, token-ready economy, production legal SaaS, live
ad integration, shipping IDE plugin, or broad formal correctness.

## Source Boundary

Primary sources for the review:

- `.arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md`
- `.arcanum/inventory/queries/2026-07-06-ai-assurance-certification-vocabulary-research/findings.md`
- `.arcanum/inventory/queries/2026-07-06-spec-driven-completeness-moat-inventory-research/findings.md`
- `.arcanum/inventory/queries/2026-07-06-novel-model-use-lean-formalization-research/findings.md`
- `.arcanum/inventory/entries/novel-model-use-lean-formalization-strategy-result-synthesis.md`
- `telemetry/agents/subagents-dispatch.yaml`
- The latest user thesis recorded in the live conversation.

Optional proof checks if the review needs them:

- `implementation/domainspec/development/COMMERCIALIZATION-SYNTHESIS.md`
- `.arcanum/inventory/entries/machine-map-and-moat-synthesis.md`
- `.arcanum/inventory/entries/read-trivial-via-selective-promotion-synthesis.md`
- `.arcanum/inventory/entries/kodamai-smithe-correctness-layer-synthesis.md`
- `implementation/domainspec/scripts/audit_richness.py`
- `domainspec-lean-formalization/lean-engineer/`

## Global Anti-Bias Theme

Composite axis: methodology + attack-vector + source-corpus.

The whole sheet is tensioned around one global question: does the compounding
portfolio story read as credible leverage from a governed system, or does it
read as unfocused ambition outrunning proof?

## Lanes / Groups

### Group 1: `attackers`

Purpose: red-team the full target thesis from four distinct attack lenses.

Role: explorer attackers. Runs in parallel with `robot_talks: true`.

Anti-bias axis: composite methodology + attack-vector.

Output expectation: each attacker returns material blind spots, severity, quoted
source evidence, proposed fixes, and at least one stress test for the pitch. If
an attacker finds no issue, they must state what survived and why.

Subagents:

- **Porter, Michael** (`explorer`) - wedge and focus attack. Tests whether
  breadth reads as buyer pull or investor-confusing sprawl. Expected output:
  change requests for ICP, wedge, pricing, and first-sales proof.
- **Christensen, Clayton** (`explorer`) - market-entry and adoption attack.
  Tests whether the many POC routes form a coherent beachhead or a category
  story without an adoption mechanism. Expected output: adoption risk map and
  first narrow market selection pressure.
- **Kahneman, Daniel** (`explorer`) - investor-cognition and base-rate attack.
  Tests narrative overconfidence, survivorship bias, "unbeatable pitch"
  language, and whether the two-person/three-month claim needs hard receipts.
  Expected output: diligence questions an investor will ask and evidence needed
  to answer them.
- **Quine, Willard Van Orman** (`explorer`) - definitional and collapse attack.
  Tests whether `system`, `proof`, `reach`, `trustable`, `auditable`,
  `correctness`, `compounding`, and `system that builds systems` collapse into
  slogans without source-bounded definitions. Expected output: term repairs and
  forbidden phrasing.

Predicted disagreements:

- Porter vs Christensen: Porter will prefer narrowing to the easiest paid wedge;
  Christensen will pressure whether the selected wedge creates an adoption path
  to the bigger system rather than a consulting dead end.
- Porter vs Kahneman: Porter will optimize investor salience and buyer urgency;
  Kahneman will challenge whether salience is masking missing base-rate and
  conversion evidence.
- Porter vs Quine: Porter will tolerate commercial shorthand if it sells the
  wedge; Quine will reject shorthand that makes `proof` or `system` ambiguous.
- Christensen vs Kahneman: Christensen will look for disruption/adoption
  theory; Kahneman will test whether the theory is post-hoc narrative from a
  small sample.
- Christensen vs Quine: Christensen will allow strategic category framing;
  Quine will force definitions so category language does not smuggle platform
  readiness.
- Kahneman vs Quine: Kahneman will attack investor perception and bias; Quine
  will attack semantic collapse. Bias in either should be exposed by the other.

### Group 2: `synthesizer`

Purpose: dedupe attacks into a cited change-request draft.

Role: writer synthesizer. Runs after `attackers`.

Subagent:

- **Simon, Herbert** (`writer`) - bounded-rationality synthesis. Expected
  output: `attacks.md` from collected returns and draft `findings.md` with
  severity-ranked blind spots, evidence, proposed fixes, and a pitch repair
  ladder.

### Group 3: `verifiers`

Purpose: refute false positives and force each surviving finding back to a
source boundary.

Role: skeptic verifiers. Runs after `synthesizer` and zig-zags once if needed.

Anti-bias axis: attack-vector.

Output expectation: each verifier returns ACCEPT/DROP/REVISE per finding.
Refuted findings are dropped, not softened.

Subagents:

- **Lakatos, Imre** (`skeptic`) - precedent and research-program verifier.
  Tests whether "only", "unique", "no one", and Kodamai/comparator framing are
  overstated; verifies the story as a progressive research program rather than
  a loose pile of work.
- **Taleb, Nassim Nicholas** (`skeptic`) - non-vacuity and fragility verifier.
  Tests whether the three-month/two-person proof, compounding residue, and
  multiple-revenue-routes story survives stressors and negative controls.
- **Popper, Karl** (`skeptic`) - falsifiability and next-witness verifier.
  Tests whether each pitch claim names a falsifier, next proof object, or
  demotion condition.

Predicted disagreements:

- Lakatos vs Taleb: Lakatos will preserve a coherent research-program story if
  the sequence is progressive; Taleb will reject it unless the proof survives
  adverse-selection, fragility, and optionality stress.
- Lakatos vs Popper: Lakatos will ask whether the work forms a program; Popper
  will ask what observation would falsify each claim.
- Taleb vs Popper: Taleb will focus on hidden fragility and narrative risk;
  Popper will translate those risks into explicit falsifiers and next tests.

### Group 4: `auditor`

Purpose: coverage and final approval.

Role: auditor. Runs after `verifiers`.

Subagent:

- **Brandenburg, Martin** (`auditor`) - coverage auditor and final approver.
  Expected output: check that every target source and attack lens was covered,
  every surviving finding is cited, zero-finding red flags were handled, and
  the final `findings.md` preserves claim <= proof.

## Dependency Flow

- `attackers -> synthesizer` is sequential.
- `synthesizer -> verifiers` is zig-zag with `loop_cap: 1`.
- `verifiers -> auditor` is sequential.
- `auditor -> synthesizer` is conditional feedback with `loop_cap: 1`.
- `final_approver` is `Brandenburg, Martin`.

## Required Outputs

The review must write:

- `attacks.md` - collected attacker returns, robot-talks positions, verifier
  responses, and any dropped/refuted findings.
- `findings.md` - verified blind spots and change requests.

`findings.md` must include:

- blind-spot severity table;
- affected pitch claim;
- source evidence;
- proposed repair;
- whether the repair is a wording fix, proof-object gap, market/wedge gap,
  source-boundary gap, or investor-diligence gap;
- a "compounding story that survives" section;
- a "claims to demote or forbid" section;
- next witness queue ordered by investor leverage.

## Gate / Ledger State

Current state: proposed, pre-confirmation.

- Check-tension: pending until the two gate agents pass this sheet.
- Ledger: unregistered. No dispatch row may be appended before human
  confirmation.
- Runtime: not run. No review agents have been launched for the review itself.
- Closeout expectation after a confirmed run: append one dispatch row and one
  close row; close `resolved` only when Brandenburg accepts the verified
  change-request list, even if some verdicts are FIX.

## Next Human Action

If the check-tension gate passes, reply:

`confirmed`

That will freeze this sheet for registration and runtime execution. Any
strategist edit after confirmation must re-enter check-tension before running.
