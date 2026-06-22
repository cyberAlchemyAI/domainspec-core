# Existing HTML Source Inventory

Status: preliminary scan for the CyberAlchemy website strategy.

The scan found built HTML pages that should inform the content inventory run.
They are not automatically website-ready; they are evidence for language,
structure, visual patterns, and prior presentation choices.

## Search Commands Used

```sh
rg --files -g '*.html' -g '*.htm' -g '!node_modules/**' -g '!dist/**' -g '!build/**'
find projects arcanum -path '*/node_modules' -prune -o -path '*/.next' -prune -o -path '*/dist' -prune -o -path '*/build' -prune -o -type f \( -name '*.html' -o -name '*.htm' \) -print
find projects arcanum -path '*/node_modules' -prune -o -path '*/.next' -prune -o -path '*/dist' -prune -o -path '*/build' -prune -o -type f \( -name '*.html' -o -name '*.htm' \) -path '*/development/*' -print
```

The broad project scan found 251 project-side HTML files after excluding
`node_modules`, `.next`, `dist`, and `build`. Agents should sample large
prototype sets deliberately instead of treating every generated HTML page as
equally important.

## Direct CyberAlchemy Pages

- `cyberAlchemy/index.html`
- `cyberAlchemy/main.html`
- `cyberAlchemy/cyberalchemy-shareable.html`
- `cyberAlchemy/agentic-system-ontology-synthesis.html`
- `cyberAlchemy/operational-ontology-runtime.html`
- `cyberAlchemy/necronomicon.html`
- `cyberAlchemy/mars.html`
- `cyberAlchemy/mogt.html`

## Arcanum Development and Built Presentation Pages

- `arcanum/development/cyberalchemy-ontology-lifecycle/PRESENTATION.html`
- `arcanum/development/user-guide/arcanum-development-loop.html`
- `arcanum/development/user-guide/arcanum-surface-xray.html`
- `arcanum/development/user-guide/guide-user-translate-overview.html`
- `arcanum/docs/index.html`
- `arcanum/docs/arcanum-development-loop.html`
- `arcanum/output/arcanum-sigil-spell-power-presentation.html`
- `arcanum/writing/substack/introducing-arcanum.html`
- `arcanum/formulae/dispatch-spec/dispatch-synthesis-presentation.html`

## Arcanum Development Packages

- `arcanum/development/craft/CRAFT-TUTORIAL.html`
- `arcanum/development/craft/CRAFT-MVP-DESIGN.html`
- `arcanum/development/craft/CRAFT-INITIAL-DEFINITION.html`
- `arcanum/development/craft/CRAFT-INITIAL-FORMAL-MODEL.html`
- `arcanum/development/craft/CRAFT-LEDGER-ORG-XRAY.html`
- `arcanum/arcana/inventory/development/presentation.html`
- `arcanum/arcana/inventory/development/inventory-indexing-architecture-xray.html`
- `arcanum/arcana/ontology-vault/development/friend-graph-memory-ontology-summary.html`
- `arcanum/arcana/ux-evidence-validator/development/x-ray/designer-xray.html`
- `arcanum/arcana/x-ray/development/example-outputs/XRAY-COMPONENT-001.html`
- `arcanum/spells/whisper/development/WHISPER-PRESENTATION.html`
- `arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.public.html`
- `arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.review.html`

## Reusable Presentation and UI Pattern Sources

- `arcanum/arcana/x-ray/examples/arcanum-method-scu.html`
- `arcanum/arcana/x-ray/examples/visual-layered-order-ingestion.html`
- `projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/docs-page/example.html`
- `projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/saas-landing/example.html`
- `projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/web-prototype/example.html`
- `projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/web-prototype-taste-editorial/example.html`
- `projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/web-prototype-taste-soft/example.html`
- `projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/web-prototype-taste-brutalist/example.html`
- `projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/dashboard/example.html`
- `projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/live-dashboard/example.html`

## Product Site Examples to Sample, Not Copy

- `projects/goldenquill/landing/index.html`
- `projects/goldenquill/apps/tilth_ui/index.html`
- `projects/goldenquill/apps/tilth_ui_react/index.html`
- `projects/goldenquill/docs/strategy/generic_promotion_governance_client_overview_2026-06-02.html`
- `projects/goldenquill/docs/strategy/goldenquill_promotion_governance_client_xray_2026-06-01.html`
- `projects/goldenquill/docs/client-packages/goldenquill_promotion_governance_client_sendable_2026-06-01/goldenquill_promotion_governance_client_overview_2026-06-01.html`
- `projects/body-war/app/static/index.html`
- `projects/whisky-doses/prototype/index.html`
- `projects/industrial-bid-brasil/docs/strategy/brazil_industrial_bid_questionnaire.html`
- `projects/savvy_legal-studio-ai/plano estrategico/plano-estrategico-savvy-google.html`

## Large Generated Sets

The following areas contain many HTML prototypes. Agents should inspect them for
patterns and representative examples, not enumerate every page in the final
website strategy unless a specific pattern is selected.

- `projects/goldenquill/apps/tilth_ui/stitch_tilth_os_institutional_shell 4/**/code.html`
- `implementation/domainspec/implementation/app-frontend/visualizations/**/*.html`
- `implementation/domainspec/vault/discovery/cross-tree-mirroring-for-llm-coercion/mockups/**/*.html`
- `projects/ui-prototyping-studio/development/spikes/c1-validator-criterion/fixtures/*.html`

## Agent Instructions

When the approved dispatch runs, the HTML-aware explorer should return:

- path and page title or visible H1 when available
- whether the HTML is content source, visual/layout pattern, product analogy, or generated residue
- public-safety status
- reusable section/page ideas
- claims that need a non-HTML evidence anchor before publication
