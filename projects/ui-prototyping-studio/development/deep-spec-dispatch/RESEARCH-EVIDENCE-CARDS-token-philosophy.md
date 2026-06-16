# RESEARCH-EVIDENCE-CARDS — Token Philosophy (s1 token-researcher)

Deep-spec: UI Prototyping Studio. Researcher lane: design-token philosophy and its composition with domainspec's controlled Visual DNA vocabulary + token refs.

Repository accessibility: ACCESSIBLE. `https://github.com/michelnavarra/resonant-os-design-tokens` was fetched successfully (README, `tokens/tokens.json`, `tokens/color-palette-v0.2.md`). Note: the repo's display name in its own README is "ROSI: Resonant OS Interface Design System" — the GitHub slug is `resonant-os-design-tokens`. All cards below are source-cited; where a claim rests on the canonical design-token literature rather than the repo, it is labelled GENERAL.

---

## Section A — Evidence cards: the ROSI / "resonant" token philosophy

### EC-T01 — "Resonant" denotes the parent project, not a token-theoretic term
- Claim: In this repo "resonant" is not a design-token methodology word; it names the parent initiative (ResonantOS). The token system (ROSI) is "extracted from the actual Browser extension UI and formalized into atomic design tokens" — a *living system* that bridges real implementation with standardized specs.
- Significance: We must NOT import "resonant" as if it were a token philosophy (e.g. "resonant scales"). The transferable philosophy here is "implementation-driven / living-system token extraction," not a novel resonance theory.
- Source: README (ROSI Project Overview), fetched from `github.com/michelnavarra/resonant-os-design-tokens` and `raw.githubusercontent.com/.../main/README.md`.

### EC-T02 — Token layer is the contract; raw values forbidden in components
- Claim verbatim: "The token layer is the contract. No raw values in components." Single source of truth: "Tokens form the contract layer; raw values never appear in components directly."
- Significance: This is the SAME invariant domainspec asserts for `UIVisualSignature` ("controlled vocab + token refs, NOT raw color/px"). Strong philosophical alignment — both treat raw values as a leak to be eliminated at the boundary.
- Source: README (Design Token Philosophy, principle 1).

### EC-T03 — Depth through tonal layering, not shadows
- Claim verbatim: "Depth through tonal layering, not shadows" and "Surfaces differentiate by lightness." Surface family uses depth terminology — `deepest`, `deep`, `raised`, `overlay` — to indicate spatial position. Rationale quotes: "One step lighter — spatial boundary without borders"; "Lifts content one layer above."
- Significance: ROSI encodes elevation as a *semantic surface role* (a named tier) rather than as a numeric shadow. This is exactly the modeling stance domainspec takes with the `Elevation`, `SurfaceTone`, and `ColorRole` Visual DNA enums — role-named, not pixel/shadow-valued.
- Source: `tokens/color-palette-v0.2.md` (Color Philosophy; Semantic Naming & Surface Layering).

### EC-T04 — Monochromatic accent discipline / functional constraint
- Claim verbatim: "A single green accent family handles all interaction. Cognitive load stays minimal." "Success IS the green." "No colors beyond green accent without functional reason." Accent is sage green `#8AB4A0`; only warning (amber) and error (red) may break the rule, "only when functionally necessary."
- Significance: ROSI's accent rule is a *constraint expressed in prose*, not enforced by the token grammar — there is nothing in the token file preventing a new raw color. This is the gap domainspec's controlled-vocabulary enums (`AccentUsage`, `ColorRole`, `ContrastIntent`) close: domainspec turns "no colors without functional reason" from a guideline into an enumerable, checkable type.
- Source: README (Philosophy, principle 3); `tokens/color-palette-v0.2.md` (Accent Usage Rules; Forbidden Practices).

### EC-T05 — Flat W3C tokens with literal values; NO token-to-token aliases
- Claim: `tokens.json` is W3C-DTCG shaped — each token is `{ "$value": ..., "$type": ..., "$description": ... }` under three-level dot-notation keys (category.group.token, e.g. `color.surface.base`, `typography.fontSize.lg`). Critically: "No token-to-token aliases detected. Tokens contain literal values only; there are no references like `{color.surface.base}`." Semantic colors reuse the literal value directly (e.g. `semantic.success` and `info` both hold `"#8AB4A0"`) rather than referencing the accent token.
- Significance: ROSI is effectively a SINGLE-TIER token set with semantic *names* but primitive *values* — the semantic/primitive split is by naming convention, not by aliasing. This is the central composition risk: domainspec's `TypedReference`/token-ref model assumes a stable referent to point at; ROSI hard-codes values, so duplicated literals can drift independently.
- Source: `tokens/tokens.json` (fetched, structure analysis); `tokens/color-palette-v0.2.md`.

### EC-T06 — Dark-only, system-first typography, bounded scales
- Claim: "Dark-only aesthetic — no light theme variant." Typography is "system-ui first" with Inter for display only. v0.2 = 60 tokens / 12 categories: Surfaces(5), Borders(3), Text(4), Accent(4), Semantic(6), Chrome(4), Typography(9), Spacing(8: 2px–64px), Radius(4: 4/8/12/16px), Elevation(4), Motion(4), Z-Index(7). Hard rules: "No rounded corners > 12px except circles"; "No shadows except overlaying panels and dropdowns."
- Significance: ROSI's bounded, enumerated scales (4 radii, 8 spacings, 4 elevations) are the closest structural cousin to domainspec's controlled enums (`CornerProfile`, `SpacingPattern`, `Elevation`, `Density`). Both reject the infinite-value space. ROSI does it per-system with prose rules; domainspec does it per-vocabulary with typed enums.
- Source: README (Philosophy; Token Structure & Categories); `tokens/color-palette-v0.2.md` (Rules).

### EC-T07 — Naming convention: hierarchical role prefixes, W3C-compliant
- Claim: CSS custom properties use hierarchical role prefixes, e.g. `--rosi-color-surface-raised`, `--rosi-color-border-default`. Names "communicate functional role rather than arbitrary identifiers." Stated as W3C Design Tokens spec compliant.
- Significance: ROSI token names are themselves a controlled role vocabulary (surface/border/text/accent/semantic × role). domainspec's `TypedReference` token refs can target exactly these role-named tokens — the naming layer is the interop seam.
- Source: README (Theming Model & Naming).

### EC-T08 (GENERAL) — Canonical three-tier philosophy ROSI partially implements
- Claim: The mainstream token philosophy is three-tier: Tier-1 Primitive (raw values, e.g. `colors.white`), Tier-2 Semantic/Theme (e.g. `theme.bg.surface`, references primitives — "if you want dark mode... identical semantic layers that point to different aliases"), Tier-3 Component (e.g. `card.background`, references semantic). Aliasing creates the single source of truth: "Changing just the theme token's value would cascade through the entire system." W3C-DTCG defines an alias: "A design token's value can be a reference to another token," via `{group.token}` syntax that "always resolves to the `$value` property of the target token."
- Significance: This is the *reference model* domainspec's "token refs" presupposes. ROSI implements the NAMING of Tier-2 but not the ALIASING of Tier-2 — which is why ROSI is dark-only (no second theme to swap). domainspec can adopt the three-tier reference grammar as the contract its `TypedReference` resolves against.
- Source (GENERAL): designtokens.org/tr/drafts/format (W3C-DTCG); goodpractices.design; tasteprofile.io; penpot.app; Material Design 3 (m3.material.io/foundations/design-tokens). Labelled GENERAL — not the ROSI repo.

---

## Section B — Composition analysis: ROSI/token philosophy × domainspec controlled Visual DNA + token refs

domainspec invariant (restated from the type vocabulary): `UIVisualSignature` carries 24 controlled visual-DNA fields backed by enums (`ColorRole`, `SurfaceTone`, `ContrastIntent`, `AccentUsage`, `Elevation`, `CornerProfile`, `SpacingPattern`, `Density`, ...); values are controlled-vocabulary tokens + `TypedReference` token refs, NEVER raw color/px. Generated identity/DNA suggestions become durable only after a human runs `ConfirmUIDecisionEvidence` (producing a `UIDecisionRecord`, `UIDecisionType=preserve|constrain|...`).

There are two complementary planes that must NOT be conflated:
- domainspec Visual DNA enums = the controlled QUALITATIVE vocabulary ("this element is `SurfaceTone=raised`, `AccentUsage=primary`, `Elevation=overlay`"). Selection, not measurement.
- A token system like ROSI = the QUANTITATIVE referent that a qualitative choice resolves to ("`raised` -> `--rosi-color-surface-raised` -> `#252A2E`"). The `TypedReference` in `UIVisualSignature` is the pointer from the qualitative field to the token.

### B.1 — WHAT TO ADOPT

1. ROSI/W3C token names as the `TypedReference` target namespace (EC-T07, EC-T08).
   The role-named tokens (`color.surface.raised`, `color.border.default`, `color.accent.*`, `radius.*`, `spacing.*`) are a ready-made, W3C-shaped referent layer. domainspec's `UIVisualSignature` enum value should map to a token ref, e.g. `SurfaceTone=raised` -> `{color.surface.raised}`. Adopt the W3C `{group.token}` reference syntax as the canonical form of a domainspec `TypedReference` to a visual token. This keeps "controlled vocab + token refs" literal: the enum is the vocab, the `{...}` ref is the token ref.

2. The "token layer is the contract, no raw values" invariant (EC-T02).
   This is a direct philosophical match and should be cited as external precedent for domainspec's "NOT raw color/px" rule. Adopt it as a `ProofObligation` / `EvaluateProofGate` check: a `PrototypeVariant`'s `UIVisualSignature` is `ProofStatus=block` if any field resolves to a literal value instead of an enum + token ref.

3. Bounded, enumerated scales philosophy (EC-T03, EC-T06).
   ROSI's "depth = named tier, not shadow" and its 4-radius / 8-spacing / 4-elevation closed sets validate domainspec's choice to model `Elevation`, `CornerProfile`, `SpacingPattern`, `Density` as enums. Adopt the principle: a token system feeding domainspec SHOULD expose a small, closed scale per visual dimension so each enum value has exactly one referent.

4. Constraint-as-discipline, promoted to type (EC-T04).
   ROSI's prose accent rule ("no colors beyond green without functional reason") is the use case for domainspec's `AccentUsage` enum + `RulePromotionRequest`/`PromoteEvolutionRule`. Adopt ROSI's accent discipline as a seed `EvolutionCycle` rule candidate, but encoded as a checkable enum constraint rather than a guideline.

### B.2 — HOW IT COMPOSES (concrete binding)

- A `StudioSession` can register a token source (ROSI `tokens.json`) as the resolution backend. `GenerateVariants` produces `PrototypeVariant`s whose `UIVisualSignature` fields are populated as enum + `TypedReference` pairs only.
- Resolution table (qualitative -> token ref -> ROSI literal), e.g.:
  - `SurfaceTone=raised` -> `{color.surface.raised}` -> `#252A2E`
  - `ColorRole=accent` + `AccentUsage=primary` -> `{color.accent.default}` -> `#8AB4A0`
  - `CornerProfile=rounded-soft` -> `{radius.md}` -> `8px`
  - `Elevation=overlay` -> `{color.surface.overlay}` (ROSI models elevation as a surface tone, EC-T03) — note the binding choice this forces (see conflict C3).
- `ExportDesignHandoff` becomes a token-bound export: it emits the `UIVisualSignature` enums together with their resolved ROSI token refs, giving engineering a W3C-DTCG-shaped artifact (the `DiffSummary` and `IntegrationReadiness` can be computed against the ROSI token file's categories).
- Durability path is preserved: a generated suggestion (e.g. "use `AccentUsage=primary` here") is a candidate until `ConfirmUIDecisionEvidence` writes a `UIDecisionRecord` (`UIDecisionType=preserve` or `constrain`), which can then feed `RulePromotionRequest` to fix the binding system-wide.

### B.3 — CONFLICTS

- C1 (PRIMARY) — ROSI has no aliases; domainspec token refs need a stable referent (EC-T05).
  ROSI stores literal values and even *duplicates* them across semantic tokens (`success`/`info` both `#8AB4A0`) instead of aliasing the accent. domainspec's `TypedReference` assumes pointing at a referent is meaningful; if it points at a leaf literal that was hand-duplicated, the "single source of truth" guarantee is only nominal — two refs can drift. Mitigation: domainspec should require its target token layer to use W3C aliases (Tier-2 references Tier-1, EC-T08); when consuming ROSI as-is, treat each ROSI token as Tier-1 and synthesize a domainspec-owned Tier-2 semantic alias layer over it so the enum->ref binding is the single source of truth, not ROSI's duplicated literals.

- C2 — Theming model mismatch: ROSI is dark-only / single-theme (EC-T06); domainspec enums are theme-neutral.
  domainspec's qualitative vocab (`ContrastIntent`, `SurfaceTone`, `ColorRole`) is designed to be theme-portable (a value should resolve under multiple themes). ROSI deliberately has exactly one theme and no swap mechanism. Adopting ROSI tokens directly bakes dark-only into the referent layer; domainspec's promise that an enum value resolves per-theme cannot be met from ROSI alone. Mitigation: scope ROSI as one `BaselineProvenance` theme context; do not present its single-theme literals as the universal referent for `ContrastIntent`/light variants.

- C3 — Cross-axis collapse: ROSI folds elevation INTO surface tone (EC-T03).
  domainspec keeps `Elevation` and `SurfaceTone` as two independent enums. ROSI expresses elevation via lighter surface tokens ("depth through tonal layering, not shadows") and forbids shadows except overlays. So a domainspec `(SurfaceTone, Elevation)` pair has no clean orthogonal mapping into ROSI — both axes resolve to the same surface-token family. Mitigation: document a binding rule that, for ROSI-backed sessions, `Elevation` is realized through `SurfaceTone` token selection (and `Elevation=floating/shadowed` is unsupported), captured as a `ProofObligation` rather than silently mapped.

- C4 — Granularity gap: 24 Visual DNA fields vs ROSI's 12 categories.
  domainspec's vocabulary spans typography role/weight/scale/transform/numeric, motion intent, interaction/state/feedback, composition/layout — several axes ROSI either lacks (`NumericStyle`, `InteractionPattern`, `StateModel`, `FeedbackStyle`, `MotionIntent` beyond 4 duration tokens) or covers only thinly. Many `UIVisualSignature` fields will have NO ROSI token ref to resolve to. Mitigation: allow `TypedReference` to be unresolved/pending for fields with no backing token (surface as `GateState=pending` in `EvaluateProofGate`); never fabricate a raw value to fill the gap.

- C5 — Naming-as-semantics is a soft contract.
  W3C-DTCG explicitly warns groups are "arbitrary" and tools "SHOULD NOT use them to infer the type or purpose of design tokens" (EC-T08 source). ROSI's semantics live in token *names*, which the spec says are not load-bearing for type inference. domainspec must not rely on ROSI's name strings to infer enum membership; the enum<->token mapping must be an explicit, human-confirmed binding (`ConfirmUIDecisionEvidence`), not a string-match heuristic.

### B.4 — RESIDUE (unresolved / open)

- R1: Could not read `tokens.css` or `tokens.json` byte-for-byte (WebFetch summarized via a small model). The "no aliases" finding (C1) is high-confidence from two independent fetches but should be confirmed by a raw byte read of `tokens.json` before being treated as a hard spec input.
- R2: ROSI `components/` (Phase 1) and `dashboard/` (Phase 2) are "coming soon" / empty. If/when component-tier tokens land, they could change the composition picture (component tier would be the natural target for several `UIVisualSignature` interaction/state fields). Re-check before freezing the binding.
- R3: The exact ROSI radius/spacing leaf values are partially inferred (radius 4/8/12/16px; spacing 2–64px) from README category descriptions, not a verbatim token dump. Treat the resolution-table literals in B.2 as illustrative, not authoritative, until a raw read confirms them.
- R4: No evidence in ROSI of any `TypedReference`-like indirection or theming swap, so the "synthesize a domainspec-owned Tier-2 alias layer" mitigation (C1) is a domainspec design obligation, not something ROSI provides — it needs its own design card downstream.

---

## Sources
- ROSI repo: https://github.com/michelnavarra/resonant-os-design-tokens (README), https://raw.githubusercontent.com/michelnavarra/resonant-os-design-tokens/main/README.md
- https://raw.githubusercontent.com/michelnavarra/resonant-os-design-tokens/main/tokens/tokens.json
- https://raw.githubusercontent.com/michelnavarra/resonant-os-design-tokens/main/tokens/color-palette-v0.2.md
- W3C Design Tokens Format Module: https://www.designtokens.org/tr/drafts/format/
- https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
- https://goodpractices.design/articles/design-tokens
- https://tasteprofile.io/blog/w3c-dtcg-design-tokens-practical-guide
- https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/
- Material Design 3 — Design tokens: https://m3.material.io/foundations/design-tokens
