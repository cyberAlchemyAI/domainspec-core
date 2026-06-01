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

Golden Quill is the productized surface for Tilth: a sovereign, operator-owned grant intelligence platform installed on a 128 GB-class local workstation bundle and governed by explicit operator authority. It is not a chatbot, not a blank document editor, and not a “magic grant writer.” It is an institutional funding workbench where a council of specialized agents helps the operator discover opportunities, check eligibility gates, draft against funder-specific registers, score against rubrics, attack weak claims, and authorize the final packet with a visible Ed25519 audit chain.

The product should feel like serious infrastructure: Linear-like calm minimalism, Stripe-level legibility, Vercel-like engineering discipline, and a warm FIT Farms / regenerative agriculture material palette. The UI should read as paper, ink, clay, oak, sage, and charcoal rather than generic AI blue, purple, glass, or neon. The operator should feel: “this is my machine, my data, my signing key, my cycle, my final decision.”

Every screen must answer one question: **what does the operator need to see here to make the next decision?** The UI should not explain itself like consumer software. It should surface authorized state, licensing/identity boundaries, posture, source quality, evidence tier, cost, and next action with very low ceremony. Golden Quill assumes technical literacy. Use precise labels, visible IDs, source-backed reasoning, and terse affordances. Avoid soft SaaS copy, gamification, onboarding fluff, confetti, “welcome back” panels, and generic productivity dashboard chrome.

### Applied-As Identity and Final Packet Authorization

Golden Quill implements a hard identity boundary. Every grant cycle is bound to a specific authorized applicant identity.

- **Final Packet Authorization:** The terminal surface for packet review, licensing, authorization, and export.
- **AppliedAsIndicator:** A persistent global chrome element showing the organization applying, the licensed node organization, and the active license state.
- **License Gate:** A deterministic check ensuring the applicant organization authority matches the licensed node or a verified agent authorization.

The agent council has stable visual identity. Scout owns discovery and horizon scanning. Scribe owns register-aware drafting. Judge owns rubric scoring. Red Team owns adversarial review. Logician owns deterministic eligibility and fail-closed gates. Every artifact produced by the council carries a seat badge, timestamp, posture context, and audit relationship.

### Operator defaults and open decisions

Default primary user: **operator-only**. Default submission surface: **packet-producer**, not direct submission. Golden Quill prepares export-ready packets; the operator manually submits to Grants.gov, foundation portals, etc. Default aesthetic anchor: **Linear-like calm minimalism** with earth-tone institutional warmth. Default posture: **Split-Context Hybrid**.

## Colors

The palette is built from high-trust earth tones. Use color semantically, never decoratively.

- **Primary / Ink (#1A1C1E):** main text, dense data, headers.
- **Secondary / Slate (#6C7278):** metadata, timestamps, borders.
- **Tertiary / Terracotta (#B8523A):** the single primary commit-action color: Run Scout, Open in Scribe, Authorize Packet, Approve for Export.
- **Neutral / Paper (#F5F1E8):** primary application background.
- **Bone (#EAE3D2):** inspector panels, secondary surfaces.
- **Surface-inset (#FFFDF7):** pills, cards, elevated surfaces.

Seat colors: Scout (sage), Scribe (terracotta), Judge (oak), Red Team (rust), Logician (charcoal).

State colors: Pass (deep green), Fail (hot rust), Warning (amber-oak), Pending (neutral slate), Verified (dark green). Fail-closed License gates use the state-fail rust.

## Typography

- **Source Serif 4:** primary reading-grade family. Headlines, body prose, draft text, Judge rationales.
- **Inter:** UI labels, buttons, tabs, nav rows. Uppercase and tracked for categories.
- **JetBrains Mono:** character-level inspection. Ed25519 fingerprints, hashes, cycle IDs, costs, signatures.

## Layout

Desktop-first, 1440px-class working area.

Three-zone shell:
1. **Top bar, 56px:** Persistent system state. Golden Quill mark, AppliedAsIndicator, posture badge, audit pill, signing-state chip, operator identity.
2. **Main workbench:** Left nav rail (220px), elastic center, right inspector (380px). Nav rail includes the "Applied As" context explicitly.
3. **Footer:** machine identity, signing key fingerprint, corpus freshness.

The right inspector answers "why?". In Final Packet Authorization, it is the **Authorized Entity Inspector**.

## Elevation & Depth

Depth through tonal layering and borders. Paper base, bone secondary, surface-inset card. Use hairline borders. Use border-strong for decision boundaries (License gates, Authorization commits).

Fail-closed states (Logician or License gates) use a soft pink wash, state-fail text, and a thick left bar.

## Shapes

Architectural restraint. 4px radii for controls, 6px for cards/panels, 10px for modals. Pill radius for identity/status chips. No large consumer rounded corners.

## Components

### Top Bar / Chrome

Always visible.
- **AppliedAsIndicator:** Shows Applied As organization, Licensed node organization, and License state (e.g., "internal use verified").
- **Audit Pill:** `verified · cycle_ID · lock_count`.
- **Posture Badge:** `FRONTIER`, `HYBRID`, `LOCAL`.

### Final Packet Authorization

Answers: Is this packet current, cleared, authorized to this applicant identity, signed, and ready for human submission?
- **Readiness checklist:** rollup of all council and license gates.
- **License Gate:** `LICENSE GATE — applicant authority verified` or `LICENSE GATE FAIL_CLOSED`.
- **Authorized Entity Inspector:** Context-specific detail on node/applicant relationship.
- **Authorize Packet:** Cryptographic authorization action (Ed25519).
- **Approve for Export:** Terminal state before ZIP/PDF generation.

## Do's and Don'ts

Do use "Final Packet Authorization" instead of "Sign-Off".
Do keep the "Applied As" context visible at all times.
Do make license failures blatant and fail-closed.
Do preserve packet-producer framing: manual submission to portals like Grants.gov.
Do not use blue/purple AI gradients or consumer animations.
Do not hide node identity or signing keys.
