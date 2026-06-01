---
version: alpha
name: Golden Quill
description: >
  Golden Quill is FIT Farms LLC's operator-owned grant intelligence workstation
  running Tilth: a local-first, audit-visible, agent-council workbench for
  discovery, eligibility gating, drafting, scoring, adversarial review,
  sign-off, and funding-cycle memory. The UI is infrastructure-grade, earth-toned,
  serif-led, desktop-first, and built around always-visible posture, Ed25519
  verification, and fail-closed compliance states.
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8523A"
  neutral: "#F5F1E8"
  sage: "#7A8C70"
  terracotta: "#B8523A"
  oak: "#6B5642"
  rust: "#9C3C28"
  charcoal: "#1F1E1B"
  paper: "#F5F1E8"
  bone: "#EAE3D2"
  ink: "#1A1C1E"
  surface: "#F5F1E8"
  surface-2: "#EAE3D2"
  surface-inset: "#FFFDF7"
  border: "#D8CFBC"
  border-strong: "#B8AC91"
  on-primary: "#F5F1E8"
  on-surface: "#1A1C1E"
  on-tertiary: "#F5F1E8"
  state-pass: "#4F6B45"
  state-fail: "#A5321F"
  state-warn: "#B07A2C"
  state-pending: "#7C7669"
  state-verified: "#3F5C36"
  posture-frontier: "#3F5C36"
  posture-hybrid: "#B07A2C"
  posture-local: "#1F1E1B"
  conjecture: "#7C7669"
  evidence-strong: "#3F5C36"
  evidence-acceptable: "#7A8C70"
  evidence-weak: "#B07A2C"
  evidence-unacceptable: "#A5321F"
  dark-surface: "#1A1815"
  dark-surface-2: "#252220"
  dark-surface-inset: "#302C28"
  dark-on-surface: "#F0E9D8"
typography:
  display:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: "2.5rem"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  headline-lg:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: "2rem"
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: "-0.005em"
  headline-md:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: "1.5rem"
    fontWeight: 500
    lineHeight: 1.3
  headline-sm:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.35
  body-lg:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
  body-sm:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.5
  label-lg:
    fontFamily: "Inter, -apple-system, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.005em"
  label-md:
    fontFamily: "Inter, -apple-system, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: "0.01em"
  label-sm:
    fontFamily: "Inter, -apple-system, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.06em"
  mono:
    fontFamily: "JetBrains Mono, Berkeley Mono, IBM Plex Mono, ui-monospace, monospace"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "'calt' 0, 'liga' 0"
  mono-sm:
    fontFamily: "JetBrains Mono, Berkeley Mono, IBM Plex Mono, ui-monospace, monospace"
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: 1.45
    fontFeature: "'calt' 0, 'liga' 0"
rounded:
  none: "0px"
  xs: "2px"
  sm: "4px"
  md: "6px"
  lg: "10px"
  xl: "14px"
  full: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  2xl: "32px"
  3xl: "48px"
  4xl: "64px"
  nav-rail: "220px"
  inspector: "380px"
  topbar: "56px"
components:
  app-shell:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.none}"
    padding: "0px"
  topbar:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    height: "{spacing.topbar}"
    padding: "0px 16px"
    typography: "{typography.label-md}"
  nav-rail:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    width: "{spacing.nav-rail}"
    padding: "{spacing.lg}"
    typography: "{typography.label-md}"
  inspector:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    width: "{spacing.inspector}"
    padding: "{spacing.xl}"
    typography: "{typography.body-sm}"
  card:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
    typography: "{typography.body-md}"
  card-elevated:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "{spacing.xl}"
    typography: "{typography.body-md}"
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.sm}"
    padding: "10px 16px"
    typography: "{typography.label-lg}"
  button-secondary:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "10px 16px"
    typography: "{typography.label-lg}"
  button-destructive:
    backgroundColor: "{colors.state-fail}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "10px 16px"
    typography: "{typography.label-lg}"
  audit-pill:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.state-verified}"
    rounded: "{rounded.full}"
    padding: "6px 12px"
    typography: "{typography.mono-sm}"
  posture-frontier:
    backgroundColor: "{colors.posture-frontier}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
    typography: "{typography.label-sm}"
  posture-hybrid:
    backgroundColor: "{colors.posture-hybrid}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
    typography: "{typography.label-sm}"
  posture-local:
    backgroundColor: "{colors.posture-local}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
    typography: "{typography.label-sm}"
  seat-scout:
    backgroundColor: "{colors.sage}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  seat-scribe:
    backgroundColor: "{colors.terracotta}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  seat-editor:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  seat-judge:
    backgroundColor: "{colors.oak}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  seat-red-team:
    backgroundColor: "{colors.rust}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  seat-logician:
    backgroundColor: "{colors.charcoal}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  gate-pass:
    backgroundColor: "#EAF0E5"
    textColor: "{colors.state-pass}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
    typography: "{typography.body-sm}"
  gate-fail:
    backgroundColor: "#F4E1DA"
    textColor: "{colors.state-fail}"
    rounded: "{rounded.sm}"
    padding: "{spacing.lg}"
    typography: "{typography.body-md}"
  conjecture-tag:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.conjecture}"
    rounded: "{rounded.xs}"
    padding: "1px 6px"
    typography: "{typography.mono-sm}"
  evidence-strong:
    backgroundColor: "{colors.evidence-strong}"
    textColor: "{colors.paper}"
    rounded: "{rounded.full}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  evidence-acceptable:
    backgroundColor: "{colors.evidence-acceptable}"
    textColor: "{colors.paper}"
    rounded: "{rounded.full}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  evidence-weak:
    backgroundColor: "{colors.evidence-weak}"
    textColor: "{colors.paper}"
    rounded: "{rounded.full}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  evidence-unacceptable:
    backgroundColor: "{colors.evidence-unacceptable}"
    textColor: "{colors.paper}"
    rounded: "{rounded.full}"
    padding: "2px 8px"
    typography: "{typography.label-sm}"
  signature-chip:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.state-verified}"
    rounded: "{rounded.sm}"
    padding: "4px 8px"
    typography: "{typography.mono-sm}"
---

# Golden Quill DESIGN.md

## Overview

Golden Quill is the productized surface for Tilth: a sovereign, operator-owned grant intelligence platform installed on a 128 GB-class local workstation bundle and governed by explicit operator authority. It is not a chatbot, not a blank document editor, and not a “magic grant writer.” It is an institutional funding workbench where a council of specialized agents helps the operator discover opportunities, check eligibility gates, draft against funder-specific registers, score against rubrics, attack weak claims, and sign the final packet with a visible Ed25519 audit chain.

The product should feel like serious infrastructure: Linear-like calm minimalism, Stripe-level legibility, Vercel-like engineering discipline, and a warm FIT Farms / regenerative agriculture material palette. The UI should read as paper, ink, clay, oak, sage, and charcoal rather than generic AI blue, purple, glass, or neon. The operator should feel: “this is my machine, my data, my signing key, my cycle, my final decision.”

Every screen must answer one question: **what does the operator need to see here to make the next decision?** The UI should not explain itself like consumer software. It should surface signed state, eligibility state, posture, source quality, evidence tier, cost, and next action with very low ceremony. Golden Quill assumes technical literacy. Use precise labels, visible IDs, source-backed reasoning, and terse affordances. Avoid soft SaaS copy, gamification, onboarding fluff, confetti, “welcome back” panels, and generic productivity dashboard chrome.

The agent council has stable visual identity. Scout owns discovery and horizon scanning. Scribe owns register-aware drafting. Editor may appear as a refinement/support badge when polishing is explicitly separated from Scribe, but Editor does not need a separate primary workflow in this v0.1 design. Judge owns rubric scoring. Red Team owns adversarial downgrade probes. Logician owns deterministic eligibility, policy, and fail-closed gates. Every artifact produced by the council carries a seat badge, timestamp, posture context, model/source context where applicable, and audit relationship to the current cycle.

### Operator defaults and open decisions

Default primary user: **operator-only**. Role-restricted reviewer/co-author views may exist later, but v0.1 should treat Josh / FIT Farms as the canonical single-operator authority model. Default submission surface: **packet-producer**, not direct submission. Golden Quill prepares export-ready packets; the operator manually submits to Grants.gov, foundation portals, municipal systems, or email. Default aesthetic anchor: **Linear-like calm minimalism** with earth-tone institutional warmth. Default posture for mixed work: **Split-Context Hybrid**, with Local-Only-Sovereign available and visually unmistakable. These defaults should be visible in the design language, not buried in settings.

## Colors

The palette is built from high-trust earth tones. It should feel like a field notebook, legal packet, machine room, and grant archive at once. The background is warm paper, the type is ink, action is terracotta, logic is charcoal, review is oak, discovery is sage, and adversarial review is oxidized rust. Use color semantically, never decoratively.

- **Primary / Ink (#1A1C1E):** main text, dense data, headers, and default button text on light surfaces. It should behave like printed ink, not digital black.
- **Secondary / Slate (#6C7278):** metadata, timestamps, borders, inactive nav labels, source-quality captions, pending verification, and low-emphasis secondary text.
- **Tertiary / Terracotta (#B8523A):** the single primary commit-action color. Use it for one major action per surface: Run Scout, Open in Scribe, Sign Artifact, Approve Gate, Export Packet. Terracotta is also Scribe’s seat color, which reinforces that drafting is the primary production act.
- **Neutral / Paper (#F5F1E8):** the primary application background. Never use pure white as the base surface.
- **Bone (#EAE3D2):** inspector panels, secondary surface wells, drawer backgrounds, and hover planes.
- **Surface-inset (#FFFDF7):** topbar pills, cards, audit chips, and small elevated surfaces that need to sit forward without shadow.

Seat colors are load-bearing. Scout is sage (#7A8C70), Scribe is terracotta (#B8523A), Editor is slate (#6C7278), Judge is oak (#6B5642), Red Team is rust (#9C3C28), and Logician is charcoal (#1F1E1B). Do not recolor agent badges per screen. The operator must learn the council at a glance.

State colors override seat colors when a decision matters. Pass is deep green (#4F6B45). Fail is hot rust (#A5321F). Warning is amber-oak (#B07A2C). Pending is neutral slate (#7C7669). Verified is dark green (#3F5C36). Fail-closed Logician gates always use the fail state, not Logician charcoal, because the verdict is more important than the seat identity.

Posture indicators are global: Frontier-Eligible is verified green, Split-Context Hybrid is amber-oak, and Local-Only-Sovereign is charcoal. The posture badge is always visible in the top bar. It should never be subtle. It tells the operator what kind of data boundary the current cycle is operating under.

Evidence ladders use four levels: strongest / acceptable / weak / unacceptable. Use green, sage, amber, and fail-rust respectively. Conjecture content uses slate-gray and the exact inline mono tag `[CONJECTURE — Pillar-2 corpus pending]`. This tag is functional compliance UI, not editorial decoration.

Dark mode uses warm near-black surfaces, not blue-black. `dark-surface` is #1A1815, `dark-surface-2` is #252220, `dark-surface-inset` is #302C28, and `dark-on-surface` is #F0E9D8. Seat colors remain recognizable and may be lightened slightly for WCAG AA contrast. Do not create a separate cyberpunk identity for dark mode.

## Typography

Golden Quill is a reading product. Operators will read opportunity rationales, RFA excerpts, proposal drafts, score explanations, Red Team attacks, lock-history rows, signatures, and funder charters for long stretches. Typography must make long-form review possible without reducing the UI to a legal document.

Use **Source Serif 4** as the primary reading-grade family, with Tiempos Text, Iowan Old Style, Georgia, and serif as fallbacks. Use it for headlines, body prose, draft text, FID summaries, Judge rationales, Red Team explanations, gate evidence excerpts, and charter excerpts. The serif should make the system feel authored, institutional, and legible at length.

Use **Inter** for UI labels, buttons, tabs, nav rows, form labels, and compact status controls. Inter should be quiet and utilitarian. It should never compete with the serif reading surfaces. Labels use uppercase, 0.06em tracking, and semibold weight when they behave as system categories: SCOUT, LOCAL, VERIFIED, STRONG, E-104, or DO NOT DRAFT.

Use **JetBrains Mono** for anything the operator might paste, verify, grep, compare, or sign: Ed25519 fingerprints, lock IDs, cycle IDs, FID codes, F-CLASS codes, model IDs, artifact hashes, org slugs, timestamps, row previews, cache-hit percentages, and cost values. Disable ligatures and contextual alternates. Character-level inspection matters more than typographic prettiness.

Proposal prose line length should cap at roughly 72 characters. Drafting surfaces should use a focused reading column, not a full-width text block. Dense inspector content may be smaller, but do not compress source-backed rationale into unreadable dashboard text. The product’s credibility depends on being able to read the reasoning, not merely see a badge.

Use no more than two weights of a type family per surface. Avoid bold soup. Hierarchy should come from spacing, sectioning, color, and consistent token use rather than random type size escalation.

## Layout

The product is desktop-first. The full operator surface assumes a 1440px-class working area with persistent system chrome. Mobile is a companion for review, audit, and sign-off, not the primary authoring environment.

Use a three-zone shell:

1. **Top bar, 56px:** persistent system state. It includes the Golden Quill mark, active organization slug, posture badge, audit pill, signing-state chip, current cycle ID, and operator identity. The posture badge and audit pill are non-removable.
2. **Main workbench:** left nav rail, elastic central surface, right inspector. The left rail is 220px and lists the primary surfaces: Discovery, Eligibility, Drafting, Scoring, Red Team, Sign-Off, Audit Trail, Posture, BYOK Cost, Cards, and FIDs. The center changes by workflow. The inspector is 380px and context-sensitive.
3. **Footer / node identity strip:** active machine identity, truncated signing-key fingerprint, FID corpus freshness, current deployment posture, and local node status.

The right inspector is essential. It answers “why?” for the selected object. When the operator selects an opportunity, it shows fit rationale, source-backing tier, deadline risk, and funder envelope. When the operator selects a gate, it shows source evidence, rule ID, fail reason, and resolution path. When the operator selects a draft paragraph, it shows register, suspicious terms, evidence tier, and conjecture status. When the operator selects a score, it shows rubric evidence and downgrade risk.

Use an 8px spacing rhythm with a 4px micro-step only for icon alignment and inline chips. Cards use 16px or 24px internal padding. Panels should feel dense but not cramped. This is not a consumer dashboard with huge empty hero blocks. Density is acceptable because the operator is doing serious work, but every dense surface must retain a clear next-action affordance.

Mobile collapses to one column. It exposes Sign-Off, Audit Trail, and read-only Draft Viewer by default. Inspector content becomes a bottom sheet. Posture changes should remain desktop-only unless explicitly designed as a high-friction signed flow.

## Elevation & Depth

Depth is conveyed through tonal layering, borders, and pinned structure rather than shadows. Paper is the base, bone is the secondary plane, and surface-inset is the forward card plane. This gives the product a calm archival feel and avoids consumer-app gloss.

Use hairline borders for table rows, lock-history entries, cards, and inspectors. Use border-strong only when a region represents a decision boundary: eligibility gates, posture changes, signature paste-back, export confirmation, or council split.

Hover states should be restrained: a small background tonal shift is enough. Avoid lift animations. Avoid bouncy cards. The operator is not browsing marketing content; they are managing compliance-critical work.

Fail-closed states break the quiet system intentionally. A failed Logician gate gets a soft pink wash, state-fail text, a solid fail-rust border, and a thick left bar. The banner text must say exactly what is blocked and what must resolve before continuing: `DO NOT DRAFT — E-104 failed closed. Resolve applicant_uei before Scribe can open.` The operator must not be able to scroll past a fail-closed gate without seeing it.

Verification states may pulse subtly only while actively checking signatures or daemon freshness. Respect reduced-motion settings. Do not pulse generic loading states.

## Shapes

Use architectural restraint. Buttons, chips, input fields, cards, and gate rows use small radii: 4px for most controls, 6px for cards and panels, 10px for modals and drawers, and pill radius only for identity/status chips such as evidence tiers, posture badges, audit pills, and signature chips.

Do not mix sharp and rounded corners inside a single component family. Do not use large rounded consumer cards. The shape language should feel engineered and durable, not friendly in a startup-dashboard way.

Modals and drawers are reserved for high-friction actions: posture change, signature paste-back, packet export, resolving fail-closed gates, or committing lock-history. Routine inspector detail should stay in-panel, not modalized.

## Components

### Persistent system chrome

The **top bar** is the global truth surface. It always shows posture, audit verification, signing state, active cycle, and operator identity. The audit pill format should resemble: `verified · cycle_2026-05-20T14:32Z · 12/12 lock_history`. If any signature fails, the pill turns state-fail and links directly to the affected rows.

The **posture badge** has three states: `FRONTIER`, `HYBRID`, and `LOCAL`. Changing posture requires explicit operator action, a confirmation drawer, and an audit event. Mid-cycle posture changes should fail closed unless the workflow explicitly permits a signed new cycle boundary.

The **signing-key chip** shows truncated Ed25519 fingerprint by default and full fingerprint on hover or click. The footer may also show machine identity to remind the operator that this is their instance, not a rented SaaS tenant.

### Workflow surfaces

**Discovery / Scout** answers: what should we pursue, why, and how fresh is the signal? The surface starts with applicant context selection: CIC, CLC, and optional funder envelope. Scout returns opportunity cards ranked by confidence, fit, deadline risk, and source-backing tier. Daemon mode shows continuous-fresh state with channel-family freshness; one-shot mode runs only on operator-triggered queries. Opportunity cards include funder name, program code, title, deadline, confidence ribbon, fit rationale, and source tier.

**Eligibility / Logician** answers: are we allowed to draft? Before Scribe opens, Logician runs `hard_eligibility_gates` from the Pass 1 taxonomy. Gate cards show code, name, pass/fail/pending verdict, source-backed evidence, and resolution path. Any fail-closed gate disables drafting and displays a loud `DO NOT DRAFT` banner. This is the most important safety UX in the product.

**Drafting / Scribe** answers: what section are we writing, under which funder register, with which evidence? The drafting canvas is serif, capped at readable line length, and ordered by the funder’s charter. The inspector shows register (`USDA-RD`, `SARE`, `Heinz`, etc.), voice constraints, suspicious terms, evidence tier, and pre-corpus claims. Pre-corpus claims carry `[CONJECTURE — Pillar-2 corpus pending]`. Suspicious terms are never silently replaced; the operator applies or keeps each suggestion.

**Scoring / Judge** answers: how would this score, and which claim changes the score? Show predicted score against the funder rubric, criterion weights, evidence ladders, and drill-down traces. Each criterion expands into claim-level evidence: strongest, acceptable, weak, unacceptable. Judge output should be forensic, not decorative.

**Red Team** answers: how would a hostile reviewer downgrade this? Display probes as a checklist with verdicts. HIT rows expand into attack vector and required response. Probe categories include fake-fit signals, unsupported partnership claims, missing evidence, budget mismatch, admin-risk language, overclaimed impact, and common downgrade patterns. If Judge score and Red Team verdict diverge beyond threshold, pin a council-split banner until the operator records a tie-break.

**Operator Sign-Off** answers: what exactly am I signing? Show the final packet preview, all signed artifacts in the cycle, artifact hashes, seat attribution, posture attestation, and lock-history row preview. The Ed25519 paste-back field uses monospace, disables autocorrect, and validates before commit. Final state progression is Draft → Reviewed → Signed → Locked. No artifact becomes final without operator action.

**Audit Trail Viewer** answers: can I prove what happened? It shows lock-history rows, paired-commit ceremony events, signing chain status, seat contributions, timestamps, model/source context where relevant, and artifact previews. Filter by cycle, seat, posture, FID, F-CLASS code, and verification state.

**BYOK Cost Dashboard** answers: what did this cycle cost and why? Show per-cycle, per-seat, per-charter cost; cache-hit rate; posture-aware projection; and provider-source context. This is a cost observability panel, not a Golden Quill billing screen.

**Card Matrix** answers: which identity and capital lens are active? Render a 6 CIC × 8 CLC grid. Each cell exposes charter excerpt, active rules, search vocabulary, language register, evidence expectations, and reporting rhythm. Selection drives Scout, Scribe, Judge, and Logician behavior.

**FID Browser** answers: what funder/program charter are we operating under, and how verified is it? Show 14+ active charters plus expanding Pillar-2 candidates. Each FID row has funder name, program code, verification status, corpus freshness, last used cycle, and drill-down details.

### Functional components

Use gate cards, opportunity cards, evidence ladders, score panels, Red Team probe rows, conjecture tags, seat badges, signature chips, lock-history rows, posture drawers, cost stacks, FID rows, and card-matrix cells as the core component vocabulary. These components should reuse the same typography, badge, and state logic across every surface.

## Do's and Don'ts

Do keep audit status, posture, active cycle, and signing identity visible at all times on desktop. These are not optional widgets.

Do use the canonical DESIGN.md structure: YAML front matter, followed by markdown sections in this order. Tokens are normative. Prose explains why and how to apply them.

Do use terracotta for the single most commit-shaped action per surface. Do not create competing primary actions.

Do make failed Logician gates visually blatant. The operator must know drafting is blocked.

Do mark every pre-corpus claim with `[CONJECTURE — Pillar-2 corpus pending]` until the corpus state changes.

Do show agent seat attribution on council-produced artifacts.

Do use serif for draft/prose reading, Inter for controls, and JetBrains Mono for hashes, IDs, codes, costs, and signatures.

Do preserve packet-producer framing. Golden Quill prepares, audits, signs, and exports packets; it does not autonomously submit applications.

Do maintain WCAG AA contrast on light and dark modes. Focus rings must be visible.

Do make mobile a review/sign-off companion unless the operator explicitly chooses fuller parity.

Do not build a chat UI. No message bubbles, no chat input, no “typing…” indicator, no agent avatars pretending to converse. Council seats produce structured artifacts.

Do not hide posture, cost, audit, or signing state in settings.

Do not silently rewrite admin-risk terms or suspicious phrases. Show the original, suggested replacement, severity, and Apply / Keep choice.

Do not use blue/purple AI gradients, glassmorphism, neon, confetti, or consumer animation.

Do not imply award guarantees, legal certification, or autonomous compliance authority. The system supports operator judgment; it does not replace it.

Do not mention MyCel or Loom in this UI spec. They are separate workstreams.

Do not present direct submission as default. If direct portal integration ever exists, it must be signed, gated, and operator-triggered.

Do not create a CRM, generic SaaS dashboard, or marketing homepage. Golden Quill is a governed funding-cycle workbench with signed artifacts.
