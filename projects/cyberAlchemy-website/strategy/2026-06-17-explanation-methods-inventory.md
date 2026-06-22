# Explanation Methods Inventory

Status: seed palette for CyberAlchemy website curation and Whisper page drafting.

The goal is to collect ways this repository already explains complex ideas. The
website should not only choose content; it should choose the right explanatory
form for each page.

## Method Palette

| Method | Best For | Evidence To Inspect | Website Use |
| --- | --- | --- | --- |
| Method doctrine | Naming how the work operates and why it exists. | `arcanum/framework/CYBERALCHEMY-METHOD.md` | Method page, principles page, "how CyberAlchemy works". |
| Beginner tutorial | Helping a new reader understand a workflow without schema-first language. | `arcanum/development/craft/CRAFT-TUTORIAL.html`; `arcanum/development/craft/CRAFT-TUTORIAL.md` | Learn page, onboarding sidebar, "start here". |
| X-ray / layered visual explanation | Showing parts, relationships, gates, and evidence/inference boundaries. | `arcanum/arcana/x-ray/examples/arcanum-method-scu.html`; `arcanum/development/user-guide/arcanum-surface-xray.html` | Visual explainer sections and interactive diagrams. |
| Presentation page | Turning a concept into a guided narrative with sections and rhythm. | `arcanum/development/cyberalchemy-ontology-lifecycle/PRESENTATION.html`; `arcanum/output/arcanum-sigil-spell-power-presentation.html` | Hero-to-proof flow, talk-style page, pitch walkthrough. |
| Printable guide / PDF | Giving a stable artifact a visitor can download or review offline. | `arcanum/development/user-guide/ARCANUM-DEVELOPMENT-USAGE-GUIDE.print.pdf`; `cyberAlchemy/agentic-system-ontology-synthesis.pdf` | Downloadable guide, long-form proof asset. |
| Article / Substack narrative | Carrying argument, voice, and reflective ending. | `arcanum/writing/substack/introducing-arcanum.html`; `arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.public.html` | Essay page, announcement, founder note. |
| Public offer page | Explaining a product value proposition without leaking internals. | `projects/ontologize/PUBLIC-OFFERING.md`; `projects/goldenquill/landing/index.html` | Home page, offer page, audience-specific landing. |
| Client package / executive brief | Layering overview, proof, appendix, and decisions. | `projects/ontologize/deliverable/`; `projects/goldenquill/docs/client-packages/.../*.html` | Downloadable buyer packet, case page. |
| Technical appendix | Preserving rigor for claims that need detail without burdening the main page. | `arcanum/docs/research/dcb-vs-multi-aggregate-append.pdf`; `projects/framework-unification/layers/cyber-alchemy-lean-fusion/DESIGN.md` | Proof/boundary page, footnotes, "for builders". |
| Operational demo / console | Showing what a system feels like in use. | `projects/goldenquill/apps/tilth_ui/index.html`; `projects/ui-prototyping-studio/provenance/open-design-reference/...` | Product demo, interface teaser, workflow page. |
| Open-questions / blocker packet | Showing honesty around what is unresolved. | `projects/goldenquill/docs/features/goldenquill-promotion-governance/team-review/open-questions-and-blockers.pdf`; `projects/framework-unification/layers/cyber-alchemy-lean-fusion/DESIGN.md#open--unresolved-blockers-vs-non-blockers` | Trust-building "what is proven / open" section. |
| Review surface | Making a draft addressable by stable blocks and comments. | `.agents/skills/whisper/templates/draft-review-base.html`; `arcanum/spells/whisper/templates/draft-review-base.html` | Internal page review, not public site content. |

## Selection Rule

Every proposed page should choose exactly one primary method and optionally one
supporting method. If more than two methods seem necessary, split the page.

## Evidence Rule

The method source can justify form, structure, rhythm, or reader journey. It
does not justify factual claims unless the source itself is the authority for
that claim.

## Whisper Handoff

The page-writing preset at `whisper-presets/cyberalchemy-site-page.md` consumes
this palette as its `transport_schema.method_palette`.
