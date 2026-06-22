# Whisper Preset: CyberAlchemy Site Page

Preset id: `cyberalchemy_site_page`.

Use with: `whisper`.

Purpose: create or revise one CyberAlchemy website page from curated evidence
without flattening source proof, public/private boundaries, or explanation form.

## Inputs

Required:

- page objective
- target public
- selected page role
- selected primary explanation method
- curated evidence bundle from
  `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/findings.md`
- source anchors for every load-bearing claim
- authority type for every load-bearing claim:
  `canonical source`, `public documentation`, `internal evidence`,
  `presentation artifact`, or `analogy pattern`
- claim type for every load-bearing claim
- status label for every load-bearing claim:
  `Built`, `Designed`, `Planned`, or `Open`

Recommended:

- secondary explanation method
- selected examples from:
  - `strategy/2026-06-17-existing-html-source-inventory.md`
  - `strategy/2026-06-17-pdf-source-inventory.md`
  - `strategy/2026-06-17-explanation-methods-inventory.md`
- public-boundary notes
- forbidden claims or phrases
- desired CTA policy

## Transport Schema

Transport id: `cyberalchemy_site_page`.

Allowed page roles:

- `home`
- `method`
- `how-it-works`
- `proof-boundary`
- `trust`
- `case`
- `learn`
- `article`
- `downloadable-guide`
- `builder-appendix`

Required body parts:

1. `opening`: name the page's reader job in one plain sentence.
2. `orientation`: explain what CyberAlchemy is in the smallest relevant frame.
3. `evidence-backed body`: 2-5 sections, each with source anchors.
4. `boundary`: authority type plus what is Built, Designed, Planned, or Open.
5. `next action`: one clear action, link, or continuation route.

Optional body parts:

- `visual map`
- `example walkthrough`
- `download asset`
- `technical appendix link`
- `open questions`
- `review notes`

CTA policy:

- Home or offer pages may invite contact, reading, or a demo.
- Proof/boundary pages should invite deeper reading, not conversion pressure.
- Learn pages should route to the next concept.
- No page should promise shipped capability without source evidence.
- Home pages are offer pages only: problem, transformation, who it helps, proof
  hint, and CTA.
- Architecture belongs after offer, method, and trust.

## SCU Defaults

### Resonance Core

Tone: precise, inviting, quietly rigorous.

Voice: collaborative expert, not manifesto, not hype.

Value signal: "this system helps people turn intent into durable artifacts while
keeping evidence, loss, and decisions visible."

Forbidden feels:

- mystical alchemy without operational grounding
- novelty inflation
- "AI magic" claims
- internal workshop residue
- dense schema-first onboarding

### Relevance Core

Target publics:

- curious builder
- technical founder
- research collaborator
- buyer/adopter evaluating trust
- returning operator who needs orientation

Authority mode:

- source-backed and boundary-honest
- concept-level public language
- private details translated, not exposed
- HTML/PDF artifacts can shape structure, but they do not authorize factual
  claims unless audited and re-anchored

Reader state:

- interested but not yet fluent in Arcanum/DomainSpec vocabulary
- willing to follow a clear idea if jargon is staged carefully

Objections to answer:

- "Is this just prompt engineering?"
- "What is actually built?"
- "What is formal versus aspirational?"
- "Why should I trust the method?"
- "Where do I start?"
- "Which claims are built, designed, planned, or open?"

### Trajectory Core

Movement:

1. Start from the reader's problem or curiosity.
2. Name the CyberAlchemy frame.
3. Show the mechanism or example.
4. State evidence and limits.
5. Route the reader to the next step.

Length:

- Short page: 500-900 words.
- Standard page: 900-1400 words.
- Deep page: 1400-2200 words with appendix links.

## Explanation Method Menu

Choose one primary method from
`strategy/2026-06-17-explanation-methods-inventory.md`:

- `method-doctrine`
- `beginner-tutorial`
- `xray-layered-visual`
- `presentation-page`
- `printable-guide`
- `article-narrative`
- `public-offer`
- `client-package`
- `technical-appendix`
- `operational-demo`
- `open-questions`
- `review-surface`

Method fit checks:

- If the reader needs orientation, prefer `beginner-tutorial` or `method-doctrine`.
- If the reader needs trust, prefer `technical-appendix`, `method-doctrine`, or
  `open-questions`, and consider a public page title such as `How Claims Are
  Checked`.
- If the reader needs desire, prefer `public-offer` with strict proof language.
- If the reader needs to understand a mechanism, prefer `xray-layered-visual` or
  `presentation-page`.
- If the text is mainly for internal revision, use `review-surface`, not a public
  page.

## Composition Plan Template

```markdown
## Page Plan

- Page role:
- Target public:
- Primary explanation method:
- Secondary explanation method:
- Reader job:
- One-sentence page promise:
- Evidence anchors:
- Authority types:
- Claim types:
- Status labels:
- Claims allowed:
- Claims forbidden:
- Body parts:
- CTA:
- Review risks:
```

## Draft Gate

A draft passes only if:

- every load-bearing claim has a source anchor
- every load-bearing claim has an authority type
- every load-bearing claim has a claim type
- every load-bearing claim has a Built, Designed, Planned, or Open label
- every planned/open capability is marked as planned/open
- no private path, owner handoff, private submodule detail, or workspace-only
  residue appears in public copy
- the chosen explanation method is visible in the structure
- the page can be understood without prior Arcanum vocabulary
- the CTA matches the page role
- `Built` is used only when owned source evidence verifies implementation or
  operation; documentation alone is not enough
- private/session/project material is abstracted, anonymized, and re-anchored
  before it appears in public copy

Flag if:

- the copy is true but too internal
- the page mixes more than two explanation methods
- HTML/PDF examples drive claims instead of structure
- the page needs a diagram or appendix to avoid overloading prose
- architecture appears before the page has established visitor value and trust

Block if:

- public/private boundary is unclear
- a core claim cannot be anchored
- built/planned/open status is ambiguous
- authority type is missing or misleading
- HTML/PDF or analogy material is used as factual authority without re-anchoring
- the page depends on source material the content inventory has not approved

## Review HTML

When a draft is ready for detailed review, render it with Whisper's review HTML
contract using `.agents/skills/whisper/templates/draft-review-base.html` or the
canonical `arcanum/spells/whisper/templates/draft-review-base.html`.

Review payloads should tag comments by part:

- `opening`
- `orientation`
- `body`
- `boundary`
- `cta`
- `evidence`
- `voice`

## Output Contract

Return:

```markdown
## Whisper Result

- Spell: whisper
- Preset: cyberalchemy_site_page
- Page role:
- Objective:
- Target public:
- Explanation method:
- SCU cores:
- Composition plan:
- Draft status: pass | flag | block
- Validation:
- Learning residue:
- Next route:
```
