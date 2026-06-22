# CyberAlchemy Website Content Inventory and Curation Strategy

Status: registered, run, auditor accepted, closed as `resolved`.

Dispatch type: `research`.

Reason for dispatch:

- Synthesis: the material spans public Arcanum docs, private framework maps,
  session summaries, prior dispatch rows, product-facing examples, and existing
  built HTML/PDF explanation artifacts.
- Context protection: raw collection will be much larger than what the parent
  session should carry.
- Isolation: candidate website content should be discovered and rejected without
  prematurely writing public copy.
- Parallelism: source-corpus sweeps and curation attacks are independent enough
  to run concurrently inside their groups.

## Goal

Inventory dispersed CyberAlchemy-related material and curate it into a
website-ready selection map: what to publish, what to adapt, what to keep
internal, and what to defer until stronger proof exists.

## Working Folder

`projects/cyberAlchemy-website/research/2026-06-17-content-inventory/`

Outputs:

- `research.md`: collected returns from content explorers, curation skeptics,
  and coverage auditor.
- `findings.md`: cited synthesis with candidate website sections, inclusion
  verdicts, rejected material, private-boundary notes, and a first sitemap.

Output paths:

- `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/research.md`
- `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/findings.md`

Auditor verdict: `ACCEPT`.

## Source Buckets

The agents should start with, but not be limited to:

- `arcanum/framework/CYBERALCHEMY-METHOD.md`
- public-safe Arcanum docs under `arcanum/`
- `projects/framework-unification/layers/cyber-alchemy-lean-fusion/`
- `projects/framework-unification/research/RESEARCH.md`
- built CyberAlchemy HTML pages under `cyberAlchemy/*.html`
- development-package HTML and built presentation pages listed in
  `strategy/2026-06-17-existing-html-source-inventory.md`
- PDFs listed in `strategy/2026-06-17-pdf-source-inventory.md`
- explanation methods listed in
  `strategy/2026-06-17-explanation-methods-inventory.md`
- relevant `sessions/` summaries for CyberAlchemy, capability foundry, framework
  unification, and public/private boundary decisions
- relevant rows in `telemetry/agents/subagents-dispatch.yaml`
- product-facing comparison material such as `projects/ontologize/PUBLIC-OFFERING.md`

HTML artifacts are evidence for content, page structure, visual treatment, and
prior audience framing. They are not source truth by themselves: agents must
trace any website claim back to an owned source or mark it as an inferred
presentation pattern.

PDFs and other explanation artifacts are evidence for how hard concepts have
already been explained: tutorial, X-ray, presentation, printable guide, article,
offer page, case packet, review surface, and reference appendix. The dispatch
should extract explanation methods as reusable writing choices, not only content.

## Inclusion Criteria

A content unit belongs on the website only if it passes all gates:

- Audience value: a visitor can tell what it helps them understand or do.
- Evidence anchor: the claim cites an owned source or is clearly marked as an
  interpretation.
- Public boundary: no private paths, private handoffs, internal-only names, or
  workspace-specific operational residue.
- Proof discipline: claim <= proof, with built, designed, planned, and open
  states kept distinct.
- Website role: it naturally fits home, method, product, case, proof/boundary,
  or learn-more pages.
- Transformation need: raw notes are classified as publish now, adapt, internal
  only, or defer.

## Proposed Groups

### content-explorers

Four explorers run in parallel over different source corpora and methods.

Anti-bias: `declared composite(source-corpus + methodology)`.

- `Shannon, Claude`: public Arcanum and CyberAlchemy method corpus, looking for
  already-public language and stable method anchors.
- `Tarski, Alfred`: private fusion/framework corpus, looking for the exact
  architecture concepts and proof-status boundaries.
- `Baars, Bernard`: session-history corpus, looking for user intent, recurring
  language, decisions, and narrative through-lines.
- `Acemoglu, Daron`: product and website analogy corpus, looking for what can
  become an external offer or page structure, including already-built HTML
  prototypes, PDFs, and presentation methods.

Predicted disagreements:

- Shannon runs public-method anchoring, Tarski runs private-architecture mining
  on the source-corpus axis; a bias in Shannon toward already-polished language
  would be exposed by Tarski's private proof-status map.
- Shannon runs public-method anchoring, Baars runs session-history recovery on
  the source-corpus axis; a bias in Shannon toward stable docs would be exposed
  by Baars preserving decisions and intent that never reached formal docs.
- Shannon runs public-method anchoring, Acemoglu runs product-site translation
  on the methodology axis; a bias in Shannon toward method fidelity would be
  exposed by Acemoglu's demand for visitor-facing structure.
- Tarski runs private-architecture mining, Baars runs session-history recovery
  on the source-corpus axis; a bias in Tarski toward clean architecture would be
  exposed by Baars's chronology and unresolved-decision trace.
- Tarski runs private-architecture mining, Acemoglu runs product-site
  translation on the methodology axis; a bias in Tarski toward conceptual
  completeness would be exposed by Acemoglu narrowing to audience-useful offers.
- Baars runs session-history recovery, Acemoglu runs product-site translation on
  the methodology axis; a bias in Baars toward preserving nuance would be
  exposed by Acemoglu's compression into navigable site sections.

### site-synthesizer

One writer turns the explorer returns into a candidate website map. It must keep
source evidence separate from proposed website copy and select one or more
explanation methods for each proposed page.

### curation-reviewers

Three skeptics attack the synthesis before acceptance.

Anti-bias: `attack-vector`.

- `Kahneman, Daniel`: public-boundary gate. Rejects leakage, private residue,
  internal-only paths, and owner-specific context.
- `Russell, Bertrand`: claim-proof gate. Rejects novelty inflation, proof drift,
  and built-vs-planned ambiguity.
- `Rittel, Horst`: visitor-clarity gate. Rejects material that is true but not
  useful or navigable for a website visitor.

Predicted disagreements:

- Kahneman runs public-boundary attack, Russell runs claim-proof attack on the
  attack-vector axis; a bias in Kahneman toward safe wording would be exposed by
  Russell catching public-safe but unsupported claims.
- Kahneman runs public-boundary attack, Rittel runs visitor-clarity attack on the
  attack-vector axis; a bias in Kahneman toward safety-through-vagueness would
  be exposed by Rittel demanding concrete visitor value.
- Russell runs claim-proof attack, Rittel runs visitor-clarity attack on the
  attack-vector axis; a bias in Russell toward dense evidence language would be
  exposed by Rittel demanding usable website structure without overclaiming.

### coverage-auditor

One auditor checks that every included candidate has a source anchor, public
boundary status, proof status, website role, explanation method, and inclusion
verdict.

## Proposed Connections

- `content-explorers -> site-synthesizer`: sequential.
- `site-synthesizer -> curation-reviewers`: zig-zag, loop cap 2.
- `site-synthesizer -> content-explorers`: feedback, loop cap 1, only if the
  reviewers expose missing evidence.
- `curation-reviewers -> coverage-auditor`: sequential.

## Run Rule

Human confirmation was received as `approve and run`. The dispatch was appended
with the deterministic appender, run by dependency, reviewed by the curation
gates, accepted by the coverage auditor, and closed with an append-only close
row.

When the dispatch closes, use `whisper-presets/cyberalchemy-site-page.md` as the
page-writing preset for any selected page. The preset consumes the curated
findings, HTML/PDF inventories, and explanation-method inventory.
