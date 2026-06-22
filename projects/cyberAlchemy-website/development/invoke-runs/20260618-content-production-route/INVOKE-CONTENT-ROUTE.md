# Invoke Content Production Route

Run id: `20260618-content-production-route`

Observed capability: `invoke`

Mode: `design-discovery`, with plan handoff.

Target artifact: CyberAlchemy website content package.

Target owner: `projects/cyberAlchemy-website`

Source evidence:

- `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/findings.md`
- `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/research.md`
- `projects/cyberAlchemy-website/whisper-presets/cyberalchemy-site-page.md`
- `projects/cyberAlchemy-website/strategy/2026-06-17-existing-html-source-inventory.md`
- `projects/cyberAlchemy-website/strategy/2026-06-17-pdf-source-inventory.md`
- `projects/cyberAlchemy-website/strategy/2026-06-17-explanation-methods-inventory.md`

## Objective

Transform the completed CyberAlchemy content research into actual website
content through governed page contracts, not freeform copy generation.

The research should become:

1. page contracts
2. evidence packets
3. Whisper page drafts
4. review surfaces
5. accepted website copy

## Decision

Do not start by asking Whisper to "write the site."

Start by converting each selected page into a compact page contract that fixes:

- reader job
- page role
- source anchors
- authority type
- claim type
- Built/Designed/Planned/Open labels
- allowed claims
- forbidden claims
- public-boundary notes
- explanation method
- CTA or next read

Then invoke `whisper` once per page.

## Content Architecture

### Page 1: Home

Role: `home`

Primary method: `public-offer`

Reader job: understand what CyberAlchemy helps them do and decide whether to
continue.

Core claim: CyberAlchemy is a capability-foundry method for turning vague intent
and scattered evidence into useful artifacts with evidence and limits attached.

Allowed source types:

- canonical source
- public documentation
- analogy pattern for structure only

Forbidden:

- shipped universal runtime claim
- security guarantee
- raw private/session/dispatch mechanics
- ontology-heavy first-screen explanation

Next route: draft with `whisper` using `cyberalchemy_site_page`.

### Page 2: Method

Role: `method`

Primary method: `method-doctrine`

Reader job: understand the CyberAlchemy method without needing Arcanum fluency.

Core claim: the method organizes objective, artifact, discovery, tension, route,
execution, and evidence into a governed loop.

Allowed source types:

- canonical source
- public documentation

Forbidden:

- product-completion claims
- private fusion proof claims without abstraction

Next route: draft after Home contract is accepted, or draft in parallel if the
Home source contract is stable.

### Page 3: How Claims Are Checked

Role: `trust`

Primary method: `technical-appendix`

Reader job: understand how the site decides what it is allowed to claim.

Core claim: CyberAlchemy pages preserve authority type, claim type, source
anchors, and Built/Designed/Planned/Open status.

Allowed source types:

- canonical source
- public documentation
- internal evidence only as abstract editorial rule

Forbidden:

- private strategy paths in public copy
- claim <= proof phrasing that depends only on private docs
- "Built" without owned evidence verifying implementation or operation

Next route: draft after one public-safe phrase set is selected.

### Page 4: How It Works

Role: `how-it-works`

Primary method: `beginner-tutorial`

Reader job: follow the journey from vague intent to useful artifact.

Core claim: a run discovers evidence, routes work, reviews claims, and produces
an artifact with visible limits.

Allowed source types:

- canonical source
- public documentation
- presentation artifact for structure only

Forbidden:

- dense route grammar
- internal skill catalog as first-contact copy

Next route: draft after Home and Method establish vocabulary.

### Page 5: Examples

Role: `case`

Primary method: `client-package`

Reader job: see the method in bounded practice without private project leakage.

Core claim: CyberAlchemy-style work can be shown through anonymized patterns
such as source-backed knowledge capture, layer separation, and structured
critique loops.

Allowed source types:

- internal evidence as anonymized pattern
- canonical/public examples where available

Forbidden:

- raw GoldenQuill/Ontologize/session details
- names, emails, local paths, dispatch IDs, token budgets, private critique

Next route: create anonymization decisions before drafting.

## Page Contract Template

```markdown
# Page Contract: <page name>

- Page role:
- Target public:
- Reader job:
- Primary explanation method:
- Secondary explanation method:
- One-sentence page promise:
- Source anchors:
- Authority types:
- Claim types:
- Status labels:
- Allowed claims:
- Forbidden claims:
- Public-boundary notes:
- Required body parts:
- CTA or next read:
- Review risks:
- Whisper preset: `cyberalchemy_site_page`
```

## Execution Plan

### L0: First page proof

Goal: prove the research can become one public-safe page.

SWU candidates:

- `SWU-CAW-CONTENT-001`: create Home page contract.
- `SWU-CAW-CONTENT-002`: draft Home page with `whisper`.
- `SWU-CAW-CONTENT-003`: review Home page against source, boundary, proof, and
  visitor clarity gates.

Acceptance evidence:

- Home page contract exists.
- Home draft has source anchors, authority types, claim types, and status labels.
- Review marks draft `pass`, `flag`, or `block` with reasons.

### L1: Repeatable page pipeline

Goal: repeat the same contract -> draft -> review loop for Method and How Claims
Are Checked.

SWU candidates:

- `SWU-CAW-CONTENT-004`: create Method page contract.
- `SWU-CAW-CONTENT-005`: draft Method page with `whisper`.
- `SWU-CAW-CONTENT-006`: create How Claims Are Checked contract.
- `SWU-CAW-CONTENT-007`: draft How Claims Are Checked with `whisper`.

Acceptance evidence:

- Both pages use the same contract shape.
- Both pages preserve claim <= proof and public-boundary gates.

### L2: Content system hardening

Goal: make content production auditable and reusable.

SWU candidates:

- `SWU-CAW-CONTENT-008`: create a page-index table for all selected pages.
- `SWU-CAW-CONTENT-009`: create a review checklist for page drafts.
- `SWU-CAW-CONTENT-010`: define anonymization rules for Examples.

Acceptance evidence:

- Page index shows draft state, evidence state, and review state.
- Checklist covers source anchors, authority types, claim types, status labels,
  public boundary, visitor clarity, and CTA.

### L3: Website assembly readiness

Goal: prepare accepted content for implementation.

SWU candidates:

- `SWU-CAW-CONTENT-011`: package accepted copy as page Markdown.
- `SWU-CAW-CONTENT-012`: define asset needs for diagrams, PDFs, and review HTML.
- `SWU-CAW-CONTENT-013`: write implementation handoff for the website build.

Acceptance evidence:

- Accepted pages are stored as page Markdown.
- Open content gaps are explicit.
- Implementation handoff names pages, assets, routes, and blocked claims.

## Validation Gates

Every page draft blocks if:

- a load-bearing claim lacks a source anchor
- authority type is missing or misleading
- Built/Designed/Planned/Open status is missing or too strong
- HTML/PDF or analogy material is used as factual authority without re-anchoring
- private/session/project residue appears in public copy
- homepage copy becomes architecture-first
- claim > proof

Every page draft flags if:

- the copy is correct but too internal
- the page lacks a clear reader job
- the CTA or next read is weak
- residue, route, ontology, or proof vocabulary appears before it is explained

## Recommended Next Route

Run `task-session` or a focused local authoring pass for
`SWU-CAW-CONTENT-001`: create the Home page contract.

After the Home contract is accepted, invoke `whisper` with:

- preset: `cyberalchemy_site_page`
- page role: `home`
- primary explanation method: `public-offer`
- curated evidence bundle:
  `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/findings.md`

Do not draft multiple pages before the first contract/draft/review loop proves
that the gates work.
