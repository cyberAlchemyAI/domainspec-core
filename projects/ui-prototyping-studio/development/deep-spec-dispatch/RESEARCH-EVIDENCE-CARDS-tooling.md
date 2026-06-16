# Research Evidence Cards — Tooling Survey (s1: web-tool-researcher)

Scope: current tooling for the UI Prototyping Studio. Each card has tool, what it does, reuse-vs-build verdict for this studio, trade-offs, and integration risk. Studio constraints assumed throughout: HTML-first MVP (D-002), shadcn/Radix/Tailwind studio surfaces only (D-001), deterministic mutation synthesis, manual governance.

Research date: 2026-06-15. All verdicts are scoped to *this* studio, not general merit.

---

## A. AI/LLM UI Prototyping Studios & Variant Generation

### Card A1 — Vercel v0
- **What it does:** Natural-language to UI generator. Outputs React components with shadcn/ui + Tailwind *exclusively* — no HTML or alternate-framework export. Output deploys directly to Vercel. Also publishes a shadcn registry namespace (`@v0`).
- **Reuse-vs-build verdict:** DO NOT REUSE as a runtime dependency; STUDY as prior art. v0's output target (React+shadcn) is exactly our studio surface (D-001), which validates the surface choice. But v0 is React-first, not HTML-first (conflicts with D-002), is stochastic/LLM-driven (conflicts with deterministic mutation synthesis), and is a hosted product with platform lock-in to Vercel.
- **Trade-offs:** Strong proof that "shadcn-shaped output" is the industry lingua franca; weak fit because generation is non-deterministic and the editable artifact is React, not HTML.
- **Integration risk:** HIGH if used as engine (lock-in, non-determinism, opaque generation). LOW as a reference/benchmark.

### Card A2 — Lovable
- **What it does:** Full-app generator from natural language; outputs shadcn/ui React with Supabase backend integration, GitHub connection for self-hosting. Targets ship-without-coding teams.
- **Reuse-vs-build verdict:** DO NOT REUSE. It is an app builder, not a prototyping/variant primitive. Scope far exceeds the studio (backend, auth, DB) and is wholly LLM-driven.
- **Trade-offs:** Good "professional defaults" reference (loading states, error boundaries, responsive layouts the studio's mutations should preserve); over-scoped and non-deterministic.
- **Integration risk:** HIGH (over-scoped, hosted, non-deterministic). Reference value only.

### Card A3 — Bolt.new (StackBlitz WebContainer)
- **What it does:** Full-stack app generation running entirely in-browser via WebContainer. Frontend+backend+DB from text.
- **Reuse-vs-build verdict:** PARTIAL REUSE of one idea only — the **in-browser sandbox execution model** (WebContainer) is a candidate pattern if the studio later needs to render/preview generated HTML/React without a server. The generation engine itself is out of scope.
- **Trade-offs:** WebContainer is a compelling preview substrate; the rest (full-stack generation) is irrelevant to an HTML-first prototyping studio.
- **Integration risk:** MEDIUM for the preview-sandbox idea (WebContainer licensing/commercial terms; heavy runtime). Defer past MVP.

### Card A4 — Google Stitch / Komposo (multi-format exporters)
- **What it does:** AI UI generators that export multiple formats. Stitch: HTML/CSS, Tailwind, React/JSX, plus Figma round-trip. Komposo: React, HTML/CSS, or Tailwind with self-host download.
- **Reuse-vs-build verdict:** DO NOT REUSE; VALIDATE positioning. Their multi-format export (HTML *and* React from one source) mirrors our HTML-first-then-componentize thesis (D-002 -> later component). They demonstrate market demand for HTML-first output, but they are stochastic hosted tools.
- **Trade-offs:** Confirms HTML-first export is a real, shipped pattern in 2026; does not give us deterministic mutation.
- **Integration risk:** LOW as evidence; HIGH as dependency.

### Card A5 — Deterministic / mutation-based variant generation (prior art, not a product)
- **What it does:** Body of patents + research on automated UI variation: genetic-algorithm site variation, deterministic A/B variant assignment via hash functions, multivariate element-combination testing, and "UI mutation" defined literally as modifying variables in a UI version (e.g., font 13pt->14pt, margin 3px->4px). 2024 LLM-iteration research (arXiv 2412.20071) frames modern tools on a "stochastic-inputs / deterministic-output" spectrum and generates multiple prototypes varying layout/theme while holding semantic consistency.
- **Reuse-vs-build verdict:** BUILD (this is the studio's differentiating core). No off-the-shelf product does *deterministic* mutation synthesis over shadcn/Tailwind surfaces. The literature gives us the vocabulary: mutate token/variable values and structural props deterministically while preserving semantic consistency.
- **Trade-offs:** Building gives full control of determinism (required) and governance (manual, required); cost is we author the mutation grammar ourselves.
- **Integration risk:** LOW — building is the intended path. Main risk is scope creep toward stochastic generation; the "deterministic-output" framing is the guardrail.

---

## B. Design-Token Pipelines

### Card B1 — Style Dictionary (v4 stable / v5 in progress)
- **What it does:** Token compiler. Reads token JSON, transforms/distributes to CSS custom properties, SCSS, JS, **Tailwind config**, Swift, Android XML, etc. v4 added first-class DTCG-format support and conversion tools. v5 (in progress) targets the DTCG 2025.10 spec.
- **Reuse-vs-build verdict:** REUSE. This is the canonical, framework-agnostic token build step. It outputs Tailwind config and CSS variables — exactly the studio surface (D-001). Deterministic by design (pure transform of JSON input), which fits deterministic mutation synthesis: the studio can mutate token JSON and re-run the build to produce variant themes.
- **Trade-offs:** Mature and deterministic; but spec is in flux — default export is now DTCG JSON, and **support for legacy/older export formats ends early September 2026**. Pin a version and a spec revision.
- **Integration risk:** MEDIUM (spec churn v4->v5 / DTCG 2025.10 not yet fully supported in v5). Mitigate by pinning Style Dictionary version + DTCG revision and isolating the build behind a studio adapter.

### Card B2 — DTCG / W3C Design Tokens Format Module (2025.10)
- **What it does:** Standard JSON format for exchanging design tokens cross-tool/cross-platform. Reached its **first stable version Oct 2025** via the W3C Community Group. Core/semantic/component token tiering is the conventional structure.
- **Reuse-vs-build verdict:** ADOPT as the studio's token data contract. Using DTCG (not a proprietary shape) future-proofs the token layer and keeps Style Dictionary, Tokens Studio, and any agent interoperable.
- **Trade-offs:** First stable but still evolving; tooling support (incl. Style Dictionary v5) lags the 2025.10 revision.
- **Integration risk:** MEDIUM (spec young, tooling catching up). Pin to a specific revision; treat as the mutation target schema for deterministic theme variants.

### Card B3 — Tokens Studio (Figma plugin + tokens manager)
- **What it does:** No-code token authoring in Figma; two-way Git sync (GitHub/GitLab/URL) of token JSON; multi-theme/mode support. Tokens manager upgraded to Style Dictionary v5 + DTCG 2025.10.
- **Reuse-vs-build verdict:** DEFER / OPTIONAL. Studio is HTML-first and code-first (D-001/D-002), not Figma-authored — so the Figma plugin is out of the MVP critical path. The *Git-as-source-of-truth + JSON sync* pattern is worth borrowing conceptually, but the studio can author/mutate token JSON directly without the plugin.
- **Trade-offs:** Great for design-team authoring; unnecessary coupling to Figma for a code-first deterministic studio. Manual governance (our constraint) is easier with plain Git-tracked JSON than with a plugin-driven two-way sync.
- **Integration risk:** LOW if skipped; MEDIUM if adopted (Figma dependency, sync conflicts complicate manual governance).

---

## C. Evidence-Backed UX / Accessibility Automation

### Card C1 — axe-core (Deque)
- **What it does:** Deterministic, rules-based accessibility engine. Catches missing alt/labels, static-text color contrast, invalid ARIA roles, missing titles. Free, open source.
- **Reuse-vs-build verdict:** REUSE as the hard, deterministic a11y gate. Its determinism aligns with the studio's deterministic ethos and with manual governance (rules are inspectable, results reproducible). Industry-standard 2026 pattern: layer axe-core as a free deterministic CI gate.
- **Trade-offs:** Deterministic and authoritative for what it covers; **coverage is partial** — WebAIM ~30% of real WCAG failures auto-detectable; W3C/WAI ~20–30% of success criteria fully automatable; Deque's own real-world analysis ~57% of known violations detected. So a 40–70% gap remains.
- **Integration risk:** LOW. Stable API, deterministic, no lock-in. Risk is *over-trusting* the green check.

### Card C2 — @axe-core/playwright (axe + Playwright)
- **What it does:** Runs axe-core inside Playwright browser sessions, enabling a11y checks against rendered, interactive DOM (hover/focus/dark-mode states, dynamic content). Also `axe-playwright` (abhinaba-ghosh) for custom commands.
- **Reuse-vs-build verdict:** REUSE. This is the recommended 2026 stack and is exactly how the studio should evidence a11y on generated prototype variants — render each HTML/component variant, run axe, capture violations as evidence. Deterministic per run; produces structured violation data the studio can attach to each variant as an evidence card.
- **Trade-offs:** Catches interaction-state issues axe-alone misses; still bounded by axe's rule coverage. Pairs naturally with the studio's variant loop (one Playwright run per mutation).
- **Integration risk:** LOW–MEDIUM. Playwright browser binaries + CI runtime cost; otherwise stable, open, deterministic.

### Card C3 — Manual / assistive-tech review layer (NVDA, JAWS, VoiceOver) + targeted Playwright behavior tests
- **What it does:** Human + screen-reader review for what automation cannot judge: contextual link ambiguity ("Read more"), dynamic aria-state on toggles, alt-text *quality*, modal focus-trapping, keyboard nav, Escape-to-close, form error clarity, skip-link UX, hover/focus-only contrast.
- **Reuse-vs-build verdict:** BUILD a lightweight manual-review checklist into the studio's manual governance step; REUSE Playwright for the scriptable interaction subset (focus trap, keyboard, Escape). Do not attempt to fully automate the judgment-based items.
- **Trade-offs:** Aligns directly with the studio's "manual governance" constraint — these gaps are precisely where a human gate adds value; cost is reviewer time per variant. 2026 consensus: AI/automation made specialist expertise *scalable*, not obsolete.
- **Integration risk:** LOW (process, not dependency). Risk is gate fatigue if every variant triggers full manual review — scope manual review to promoted variants only.

### Card C4 — Lighthouse (context note, not a primary pick)
- **What it does:** Broader page-quality audit incl. an a11y category.
- **Reuse-vs-build verdict:** OPTIONAL/SKIP for the a11y gate. axe-core (via Playwright) is the more precise, deterministic, lower-noise choice for per-variant a11y evidence. Lighthouse adds perf/SEO signals but its a11y subset overlaps axe with less determinism for our needs.
- **Trade-offs:** Useful breadth (perf), redundant for a11y.
- **Integration risk:** LOW. Only adds value if the studio later wants perf evidence cards.

---

## D. HTML-First Prototype-to-Component Workflows

### Card D1 — shadcn/ui (copy-in component model)
- **What it does:** Accessible Radix+Tailwind components distributed as *source you copy into your project* (not an npm dependency). The de facto 2026 standard and the output target of every major AI generator. You own and edit the code.
- **Reuse-vs-build verdict:** REUSE as the studio's component surface (already mandated by D-001). The copy-in/own-the-source model is ideal for deterministic mutation: the studio mutates source it controls, with no opaque dependency. Radix underneath gives a11y primitives that strengthen Card C outcomes.
- **Trade-offs:** Full control + a11y defaults; the cost (vendored source needs maintenance) is acceptable and intended for a studio that mutates source.
- **Integration risk:** LOW. It is source code, no runtime lock-in.

### Card D2 — shadcn CLI v4 + Registry (registry:base, namespaces, presets) [March 2026]
- **What it does:** CLI v4 can distribute an **entire design system as one `registry:base` payload** (components, deps, CSS vars, fonts, config). Namespaces (`@internal`, `@acme`) organize private registries. `--preset` packages a whole design-system config (colors, theme, icon library, fonts, radius) into a shareable string. Agent-oriented flags `--dry-run`, `--diff`, `--view`, plus `shadcn info`/`docs` and `shadcn/skills`.
- **Reuse-vs-build verdict:** REUSE — this is the strongest single tooling find for the studio. A **private registry namespace + `--preset`** is a near-perfect deterministic distribution mechanism for the studio's theme/component variants: each deterministic mutation can emit a preset string or a registry payload, inspectable before write via `--dry-run`/`--diff` (which directly supports *manual governance* — the human reviews the diff before anything is written).
- **Trade-offs:** Gives us deterministic, inspectable, git-trackable variant distribution with no bespoke packaging code. Cost: ties variant packaging to shadcn's registry schema and CLI versioning.
- **Integration risk:** LOW–MEDIUM. New in March 2026 so the API surface may still move; pin the CLI version. The `--dry-run/--diff/--view` review-before-write flow is exactly the manual-governance hook we want.
- **Note:** `registry:base` lets variant generation operate at design-system granularity (a variant = a different base payload), and presets let token-driven theme variants ship as compact strings — both deterministic given fixed input.

### Card D3 — HTML-first -> shadcn componentization workflow (community pattern)
- **What it does:** 2026 consensus workflow: prototype in Tailwind HTML, then promote into shadcn/ui React components (copy/paste/customize), scaffolding a themeable, publishable component library (shadcn + Vite + Tailwind).
- **Reuse-vs-build verdict:** ADOPT as the studio's lifecycle (HTML-first MVP per D-002 -> later componentize into shadcn per D-001). This is a documented, mainstream path, not a bespoke invention — de-risks the D-002->component progression.
- **Trade-offs:** Well-trodden and low-risk; the HTML->React promotion step is currently manual/agent-assisted (fits manual governance) — no fully deterministic HTML-to-shadcn transpiler exists off the shelf, so that promotion step is a future BUILD candidate.
- **Integration risk:** LOW for MVP (HTML-first only). The componentization transpiler is an open build item, not an MVP dependency.

---

## Consolidated Reuse-vs-Build Matrix

| Tool / Pattern | Verdict | MVP? |
|---|---|---|
| Style Dictionary (B1) | REUSE | Yes |
| DTCG 2025.10 format (B2) | ADOPT (data contract) | Yes |
| Tokens Studio (B3) | DEFER (Figma, optional) | No |
| axe-core (C1) | REUSE (deterministic gate) | Yes |
| @axe-core/playwright (C2) | REUSE (per-variant evidence) | Yes |
| Manual + AT review checklist (C3) | BUILD (into manual governance) | Yes (promoted variants) |
| Lighthouse (C4) | SKIP for a11y | No |
| shadcn/ui (D1) | REUSE (surface, per D-001) | Yes |
| shadcn CLI v4 registry/preset (D2) | REUSE (variant distribution) | Yes — highest-leverage find |
| HTML-first -> componentize (D3) | ADOPT (lifecycle) | Yes (HTML side) |
| Deterministic mutation engine (A5) | BUILD (the differentiator) | Yes |
| v0 / Lovable / Bolt / Stitch / Komposo (A1-A4) | DO NOT REUSE (study only) | No |

**Core thesis from the survey:** REUSE the deterministic transform-and-distribute layer (Style Dictionary + DTCG + shadcn CLI v4 registry/presets) and the deterministic a11y gate (axe-core via Playwright); BUILD only the deterministic mutation synthesis engine — which no shipped product provides — and the manual-governance review checklist. Every shipped AI prototyping studio (v0/Lovable/Bolt) is stochastic and hosted, confirming the studio's deterministic + manual-governance position is a genuine gap, not a reinvention.

---

## Sources
- AI UI generators / variant generation: https://www.komposo.ai/blog/best-ai-ui-generators-2026 ; https://muz.li/blog/best-ai-design-tools-for-ui-ux-designers-in-2026/ ; https://www.banani.co/blog/11-best-vercel-v0-alternatives ; https://www.builder.io/blog/lovable-alternatives ; https://getmocha.com/blog/best-ai-app-builder-2026 ; https://www.shadcn.io/
- Deterministic / mutation variant prior art: https://arxiv.org/pdf/2412.20071 ; https://www.uxtools.co/blog/stochastic-vs-deterministic-design ; https://www.nngroup.com/articles/multivariate-testing/ ; USPTO 10503804 / 11030272 / 11243785
- Design tokens: https://styledictionary.com/info/dtcg/ ; https://styledictionary.com/versions/v4/migration/ ; https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/ ; https://www.designtokens.org/tr/drafts/format/ ; https://help.zeroheight.com/hc/en-us/articles/48049028236187-Migrating-to-Style-Dictionary-v5-in-tokens-automation ; https://docs.tokens.studio/fundamentals/design-tokens/ ; https://tokens.studio/
- Accessibility automation: https://www.davidmello.com/software-testing/test-automation/playwright-accessibility-testing-axe-lighthouse-limitations ; https://github.com/abhinaba-ghosh/axe-playwright ; https://blog.doubleslash.de/en/software-technologien/software-quality-management/automated-a11y-tests-with-playwright-and-axe/ ; https://qaskills.sh/blog/ai-accessibility-testing-tools-2026 ; https://testdino.com/blog/playwright-accessibility
- HTML-first / shadcn workflow: https://ui.shadcn.com/docs/changelog/2026-03-cli-v4 ; https://ui.shadcn.com/docs/registry/namespace ; https://ui.shadcn.com/docs/registry/getting-started ; https://www.untitledui.com/blog/react-component-libraries ; https://dev.to/_d7eb1c1703182e3ce1782/best-tailwind-css-tools-and-resources-for-developers-in-2026-3ida
