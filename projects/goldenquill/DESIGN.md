---
version: alpha
name: Golden Quill
description: >
  Operator-owned sovereign grant intelligence platform. Infrastructure-grade
  aesthetic for a six-seat agent council (Scout, Scribe, Editor, Judge, Red Team,
  Logician) running on an operator-owned 128 GB appliance. Earth-tone palette,
  serif reading-grade typography, mono for IDs and hashes, audit trail pinned
  always-visible, fail-closed states visually blatant.
colors:
  # Brand earth tones (semantic anchors)
  sage:        "#7A8C70"   # Scout — discovery, horizon
  terracotta:  "#B8523A"   # Scribe — drafting, warm clay
  oak:         "#6B5642"   # Judge — gravitas, weight
  rust:        "#9C3C28"   # Red Team — adversarial, oxidized
  charcoal:    "#1F1E1B"   # Logician — deterministic, fail-closed
  paper:       "#F5F1E8"   # paper-white background
  bone:        "#EAE3D2"   # subtle warm surface
  slate:       "#6C7278"   # secondary text, borders
  ink:         "#1A1C1E"   # primary text on light
  # Semantic roles (light mode defaults; dark mode overrides documented below)
  primary:     "{colors.ink}"
  secondary:   "{colors.slate}"
  tertiary:    "{colors.terracotta}"
  neutral:     "{colors.paper}"
  surface:     "{colors.paper}"
  surface-2:   "{colors.bone}"
  surface-inset:"#FFFDF7"
  on-primary:  "{colors.paper}"
  on-surface:  "{colors.ink}"
  on-tertiary: "{colors.paper}"
  border:      "#D8CFBC"
  border-strong:"#B8AC91"
  # State tokens
  state-pass:    "#4F6B45"   # Logician gate PASS (deep muted green)
  state-fail:    "#A5321F"   # Logician gate FAIL (loud rust-red)
  state-warn:    "#B07A2C"   # admin-risk WARN (amber-oak)
  state-pending: "#7C7669"   # awaiting verification
  state-verified:"#3F5C36"   # Ed25519 signature verified
  # Posture indicators
  posture-frontier: "#3F5C36" # Frontier-Eligible (open)
  posture-hybrid:   "#B07A2C" # Split-Context Hybrid (mixed)
  posture-local:    "#1F1E1B" # Local-Only-Sovereign (locked)
  # Conjecture / evidence-tier badges
  conjecture:    "#7C7669"   # [CONJECTURE — Pillar-2 corpus pending]
  evidence-strong:    "#3F5C36"
  evidence-acceptable:"#7A8C70"
  evidence-weak:      "#B07A2C"
  evidence-unacceptable:"#A5321F"
typography:
  display:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: 2.5rem
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  h1:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: 2rem
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: "-0.005em"
  h2:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: 1.5rem
    fontWeight: 500
    lineHeight: 1.3
  h3:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: 1.25rem
    fontWeight: 600
    lineHeight: 1.35
  body-lg:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: 1.0625rem
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.55
  body-sm:
    fontFamily: "Source Serif 4, Tiempos Text, Iowan Old Style, Georgia, serif"
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.5
  ui:
    fontFamily: "Inter, -apple-system, Helvetica Neue, Arial, sans-serif"
    fontSize: 0.9375rem
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.005em"
  ui-sm:
    fontFamily: "Inter, -apple-system, Helvetica Neue, Arial, sans-serif"
    fontSize: 0.8125rem
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: "0.01em"
  label:
    fontFamily: "Inter, -apple-system, Helvetica Neue, Arial, sans-serif"
    fontSize: 0.75rem
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.06em"
    textTransform: "uppercase"
  mono:
    fontFamily: "JetBrains Mono, Berkeley Mono, IBM Plex Mono, ui-monospace, monospace"
    fontSize: 0.8125rem
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "'calt' 0, 'liga' 0"
  mono-sm:
    fontFamily: "JetBrains Mono, Berkeley Mono, IBM Plex Mono, ui-monospace, monospace"
    fontSize: 0.75rem
    fontWeight: 400
    lineHeight: 1.45
rounded:
  none: 0px
  xs:   2px
  sm:   4px
  md:   6px
  lg:   10px
  pill: 999px
spacing:
  xs:  4px
  sm:  8px
  md:  12px
  lg:  16px
  xl:  24px
  2xl: 32px
  3xl: 48px
  4xl: 64px
components:
  topbar:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    height: 56px
    padding: "0 {spacing.lg}"
  topbar-audit-pill:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.state-verified}"
    rounded: "{rounded.pill}"
    padding: "6px 12px"
    typography: "{typography.mono-sm}"
  posture-badge-frontier:
    backgroundColor: "{colors.posture-frontier}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
    typography: "{typography.label}"
  posture-badge-hybrid:
    backgroundColor: "{colors.posture-hybrid}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
    typography: "{typography.label}"
  posture-badge-local:
    backgroundColor: "{colors.posture-local}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
    typography: "{typography.label}"
  seat-badge-scout:
    backgroundColor: "{colors.sage}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label}"
  seat-badge-scribe:
    backgroundColor: "{colors.terracotta}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label}"
  seat-badge-judge:
    backgroundColor: "{colors.oak}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label}"
  seat-badge-redteam:
    backgroundColor: "{colors.rust}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label}"
  seat-badge-logician:
    backgroundColor: "{colors.charcoal}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "2px 8px"
    typography: "{typography.label}"
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "10px 16px"
    typography: "{typography.ui}"
  button-primary-hover:
    backgroundColor: "{colors.terracotta}"
    textColor: "{colors.paper}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "10px 16px"
    typography: "{typography.ui}"
  button-destructive:
    backgroundColor: "{colors.state-fail}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "10px 16px"
    typography: "{typography.ui}"
  card:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  card-elevated:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "{spacing.xl}"
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
    rounded: "{rounded.pill}"
    padding: "2px 8px"
    typography: "{typography.label}"
  evidence-acceptable:
    backgroundColor: "{colors.evidence-acceptable}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
    typography: "{typography.label}"
  evidence-weak:
    backgroundColor: "{colors.evidence-weak}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
    typography: "{typography.label}"
  evidence-unacceptable:
    backgroundColor: "{colors.evidence-unacceptable}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
    typography: "{typography.label}"
  signature-chip:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.state-verified}"
    rounded: "{rounded.sm}"
    padding: "4px 8px"
    typography: "{typography.mono-sm}"
  inspector:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    width: 380px
    padding: "{spacing.xl}"
  nav-rail:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    width: 220px
    padding: "{spacing.lg}"
---

## Overview

Golden Quill is the productized hardware-plus-software shape of Tilth — a sovereign, operator-owned grant intelligence platform. It is **not a chatbot**. It is a six-seat agent council (Scout, Scribe, Editor, Judge, Red Team, Logician) that runs on an operator-owned 128 GB appliance, signed Ed25519 end-to-end, with an always-visible audit trail. The visual language is **infrastructure-grade**, drawing from Linear, Stripe, and Vercel for restraint, paired with an earth-tone palette that anchors the regenerative-agriculture origin (FIT Farms) without resorting to literal botanical imagery.

The product surface answers a single question on every screen: *what does the operator need to see right here to make the next decision?* The operator is technically literate, terse, and decisive (one human, one machine). The UI does not condescend, does not autoplay, does not nudge. It surfaces signed state, fail-closed gates, evidence tiers, and posture, and gets out of the way.

Three sensory anchors define the feel: **paper-white surfaces** (warm, library-grade, never pure white), **serif body and headlines** (reading-grade — proposals are read at length, not skimmed), and **monospace IDs everywhere identity matters** (signatures, hashes, cycle IDs, lock-history rows). When the visual language has to choose between "approachable" and "credible," it chooses credible. This is a tool that signs artifacts; the chrome has to earn that authority.

The product runs in three deployment postures (Frontier-Eligible, Split-Context Hybrid, Local-Only-Sovereign). Posture is **always visible** in the top bar. The posture badge is the second-loudest thing on screen after fail-closed gate displays. Color, contrast, and label change posture-by-posture so the operator never has to ask "where am I sending data right now?"

The product is **desktop-first**. The full operator surface (discovery, eligibility gates, drafting, scoring, sign-off, audit) is desktop-resolution. Mobile is a **review-and-approve companion**: read drafts, approve gate outcomes, sign artifacts. Mobile is not a place to author. The split is intentional and matches the operator's actual workflow.

## Colors

- **Primary — Ink (#1A1C1E):** Deep near-black for body text, headlines, primary buttons, and emphasized rows. Used on paper-white surfaces. Reads as printer-ink on cotton.
- **Secondary — Slate (#6C7278):** Captions, borders, metadata, timestamps, "pending" states. The voice of the secondary layer; never the loudest element.
- **Tertiary — Terracotta (#B8523A):** The single primary-action color. Used for "Run Cycle," "Sign Artifact," "Open Drawer," and other commit-shaped interactions. Also Scribe's seat color. Used **sparingly** — one terracotta element per screen ideally, never more than three.
- **Neutral — Paper (#F5F1E8):** Warm paper-white base. Every light-mode surface starts here. Subtle yellow-cream cast under D65, never antiseptic.
- **Surface-2 — Bone (#EAE3D2):** Inspector panel, secondary card, hover-elevated row. One warmth-step deeper than paper.
- **Surface-inset — #FFFDF7:** Cards on the top bar (audit pill, signature chip). One step *lighter* than paper, almost-white but warm.

### Seat identity colors (used on badges, lane headers, and inspector rails)

- **Sage (#7A8C70) — Scout** — muted moss green. Discovery, horizon-scanning. Daemon mode pulses sage at 0.4 Hz to signal a live channel.
- **Terracotta (#B8523A) — Scribe** — warm clay. Drafting, register-matched composition. Shares hue with the tertiary action color, by design (Scribe's work is the operator's primary deliverable).
- **Oak (#6B5642) — Judge** — warm brown. Gravitas. Used on rubric panels and predicted-score displays.
- **Rust (#9C3C28) — Red Team** — oxidized red. Adversarial, friction-by-design. Visually distinct from state-fail rust (#A5321F is hotter, more saturated; Red Team is a step muted).
- **Charcoal (#1F1E1B) — Logician** — near-black. Deterministic gate authority. When Logician fails closed, the gate display uses **state-fail rust on a soft pink wash**, not charcoal — charcoal is the *seat*, state-fail is the *verdict*.

### State tokens

- **state-pass (#4F6B45)** — gate PASS, signature verified, evidence sufficient.
- **state-fail (#A5321F)** — gate FAIL, fail-closed lock, evidence-unacceptable.
- **state-warn (#B07A2C)** — admin-risk register WARN, evidence-weak.
- **state-pending (#7C7669)** — awaiting verification, unverified Scout candidate, signature awaiting paste-back.
- **state-verified (#3F5C36)** — Ed25519 verified — used only on the top-bar audit pill and lock-history rows.

### Posture indicator colors

- **posture-frontier (#3F5C36)** — Frontier-Eligible. Open posture, dark verified-green badge.
- **posture-hybrid (#B07A2C)** — Split-Context Hybrid. Amber-oak. Active reminder: substance stays local, scaffolding routes out.
- **posture-local (#1F1E1B)** — Local-Only-Sovereign. Charcoal, near-black. Locked posture badge.

### Conjecture and evidence-tier palette

Pre-corpus content (claims sitting on Pillar-2-pending data) carries the **conjecture** color (slate-gray) and a `[CONJECTURE — Pillar-2 corpus pending]` mono tag. This is a permanent, non-stylistic class — operators are looking for it.

Evidence ladders use a four-step palette: **strong (deep green) → acceptable (sage) → weak (amber) → unacceptable (rust)**. Each tier is a pill badge in the Judge panel, the Red Team checklist, and the Scribe inline-annotation layer.

### Dark mode

Dark mode inverts the surface stack: surface becomes `#1A1815` (warm near-black, not pure black), surface-2 `#252220`, surface-inset `#302C28`, ink-on-dark `#F0E9D8`. The earth-tone seat palette stays — sage, terracotta, oak, rust, charcoal — but each gets a +10% lightness shift to maintain WCAG AA on dark surface. Verified-green and fail-rust remain the same; they pop on both surfaces by design.

## Typography

Golden Quill is a reading product. Operators read 8-30 page draft proposals at length, then drill into evidence and score panels. Typography is reading-grade serif for prose and Inter for UI affordances, with monospace for any identifier the operator might paste, sign, or grep.

- **Display & Headlines — Source Serif 4** (with Tiempos Text and Iowan Old Style as fallbacks). Serif with sharp, modern terminals; reads as institutional without slipping into legal-document stiffness. H1 at 2rem / 500 weight, tracked tight (-0.005em). Used on cycle headers, FID charter titles, and the operator dashboard.
- **Body — Source Serif 4 at 16-17px**, line-height 1.55-1.6. Proposal text, charter narrative, FID summaries, rubric rationales. Body type sets the entire reading rhythm; everything else negotiates around it.
- **UI Labels — Inter** at 13-15px, medium weight, very slightly tracked. Buttons, nav items, tab labels, inspector field headers. Inter is the load-bearing sans — it is invisible by design, ceding visual weight to the serif body.
- **All-caps labels — Inter at 12px, 600 weight, 0.06em tracked, uppercase.** Used on seat badges (SCOUT, SCRIBE, JUDGE), gate names (E-101, F-CLASS-COVERAGE-INCOMPLETE), evidence-tier pills (STRONG, WEAK), and posture badges (FRONTIER, HYBRID, LOCAL).
- **Monospace — JetBrains Mono** (with Berkeley Mono and IBM Plex Mono as fallbacks). Ligatures **off** (`'calt' 0, 'liga' 0`) — operators are reading hashes and IDs, not code, and ligatures obscure character-level inspection. Used for: Ed25519 fingerprints, lock-history rows, cycle IDs (`cycle_2026-05-20T14:32Z`), org slugs, F-CLASS codes, hash prefixes, machine identity, signing key fingerprint.

Maximum two font weights per screen (per spec): regular and medium for serif, medium and semibold for sans. Never three weights of the same family on the same surface.

Line length on prose surfaces is capped at **72ch** (~640px). Wider than that, body reading rhythm collapses.

## Layout

- **Fluid Grid for desktop, max-width 1440px** on the primary cycle dashboard. Inspector pinned to the right at 380px. Nav rail pinned to the left at 220px. Main surface is the elastic middle.
- **Strict 4px / 8px spacing scale** (xs 4 / sm 8 / md 12 / lg 16 / xl 24 / 2xl 32 / 3xl 48 / 4xl 64). The 4px micro-step exists for inline icon adjustments only — every layout-meaningful gap is 8px or a multiple.
- **Three-zone shell** (top bar / main / footer). Audit pill, posture badge, machine identity sit in the top bar. Footer carries the operator's signing-key fingerprint (truncated, hoverable for full hash), the active org slug, and the FID corpus freshness indicator.
- **Inspector panel** (right side, 380px, surface-2) is context-aware: when an opportunity row is selected, it shows funder envelope + evidence tiers + verification state. When a gate row is selected, it shows source-backed evidence + fail-closed reason + how to resolve. When a draft section is selected, it shows applied register + suspicious terms + admin-risk-register hits.
- **Nav rail** (left, 220px) holds the eleven primary surfaces (Discovery, Eligibility, Drafting, Scoring, Red Team, Sign-Off, Audit Trail, Posture, BYOK, Cards, FIDs). Each row is a serif label + small mono cycle-count chip showing pending work in that surface.
- **Mobile** collapses to a single-column shell, hides the inspector behind a slide-up sheet, and surfaces only the **review surfaces**: Sign-Off, Audit Trail, and a read-only Drafting viewer.

## Elevation & Depth

Depth through **tonal layers**, not shadows. The surface stack (paper → bone → surface-inset) does the work that drop shadows do in consumer UI. The only place a soft shadow appears is the inspector panel's left edge (a 1px hairline at border + a 4px soft inset shadow at 0.04 alpha) and the slide-up mobile sheet.

Hover states use a single +4% lightness step on background, no shadow, no transform. Active/pressed states drop a 1px translateY and darken background by 6%. Focus rings are 2px terracotta with a 1px paper offset; visible on every interactive element, always.

Fail-closed gate displays break the elevation rule: the gate-fail card carries a **2px solid state-fail border**, a soft pink (#F4E1DA) wash, and a left-edge 6px state-fail bar. This is the loudest visual the UI ever produces — and it is deliberate. The operator must not miss it.

## Shapes

Architectural sharpness. **4px base radius** (rounded.sm) on buttons, cards, badges, and form fields. **6px** (rounded.md) on cards-elevated and the inspector panel. **10px** (rounded.lg) reserved for modals and slide-up sheets. **Pill (999px)** reserved for evidence-tier pills, audit pills, and verification chips — anywhere identity-class status is signaled.

No mixed corners on a single component. No fully square (0px) outside of dividing rules. The aesthetic is "modern with restraint" — Linear's geometry, not Apple's.

## Components

The component inventory is documented in the YAML front matter; this section names the patterns operators will recognize across surfaces.

- **Top bar** (height 56px) — left: Golden Quill mark + active org slug (mono); center: search; right: posture badge → audit pill → signing-key fingerprint pill → operator avatar.
- **Audit pill** — pinned in the top bar. Format: `✓ verified · cycle_2026-05-20T14:32Z · 12/12 lock_history`. Click opens the Audit Trail surface drilled to the current cycle's rows. The pill turns state-fail rust if any signature fails verification mid-cycle.
- **Posture badge** — pinned in the top bar, left of the audit pill. Three states, three colors, mono label: `FRONTIER` / `HYBRID` / `LOCAL`. Click opens the posture-change drawer (requires explicit operator confirmation, see Interactions).
- **Seat badges** — small all-caps pills in the seat color: `SCOUT` / `SCRIBE` / `JUDGE` / `RED TEAM` / `LOGICIAN` / `EDITOR`. Appear inline next to any artifact attributed to a seat (drafts, scores, probe results, gate verdicts).
- **Gate display (pass)** — soft sage wash, deep-green text, gate code in mono, evidence link in serif. Compact: `✓ E-101 hard_eligibility_gates · entity_eligible_status: PASS · source: RFA §4.2`.
- **Gate display (fail)** — loud rust border, soft pink wash, state-fail icon, large display: `✗ E-104 hard_eligibility_gates · DO NOT DRAFT until applicant_uei is registered in SAM.gov · source: RFA §4.2; SAM.gov live check`. Always carries a "Resolve" action.
- **Opportunity card** — Scout-discovered opportunities. Mono opportunity ID + serif funder name + serif title + deadline chip + confidence ribbon (5-step: 0.95+ / 0.85+ / 0.70+ / 0.50+ / unverified) + fit rationale (3-line max) + source-backing tier badge.
- **Score panel** — Judge's predicted score against the funder's rubric. Per-criterion bars (criterion name in serif + numeric score in mono + weight + cumulative). Each criterion expands to show the evidence-ladder chain.
- **Evidence ladder** — vertical list of evidence claims with tier pills: strong / acceptable / weak / unacceptable. Each row shows the source ID, the quoted text in serif italic, and the confidence rationale.
- **Red Team probe list** — checklist with verdict per probe (`fake-fit signal: clean` / `missing financial evidence: HIT` / `common downgrade pattern: HIT`). HIT rows expand to show the attack vector and Scribe's required response.
- **Conjecture tag** — inline mono pill `[CONJECTURE — Pillar-2 pending]` adjacent to any claim sitting on incomplete corpus.
- **Lock-history row** — mono table row: `lock_id | cycle_id | seat | artifact_hash | operator_sig | timestamp`. Hover reveals full hashes and the paired-commit ceremony state. Click drills into the artifact preview.
- **Signature chip** — mono pill on any artifact: `Ed25519 · 4a3f…b2c8 · verified`. Click reveals the full signature panel.
- **Posture-change drawer** — slides up from the bottom, charcoal background, paper-white text, requires the operator to type the target posture name (`type "LOCAL-ONLY-SOVEREIGN" to confirm`) and paste a fresh Ed25519 signature. No accidental posture changes.
- **Card matrix (CIC × CLC)** — 6×8 grid (48 cells, some Option-A dual-track marked with a small split icon). Each cell is a serif-titled card with the CIC + CLC charter excerpt and a "Configure" action. Selected cells highlight terracotta.
- **FID browser** — list view of 14+ funder/program charters (expanding with Pillar-2 corpus + 117 net-new candidates). Each row: funder name (serif) + program code (mono) + verification status pill + corpus freshness indicator (`fresh` / `stale @ 2026-05-08` / `pending`).
- **BYOK cost dashboard** — per-cycle, per-seat, per-charter cost breakdown. Mini-bar chart per seat (Scout / Scribe / Judge / Red Team) + cache-hit rate + posture-aware cost projection.

## Do's and Don'ts

- **Do** keep the audit pill, posture badge, and signing-key fingerprint visible at all times on desktop. Hiding any of these is a Law-3-shaped failure.
- **Do** use terracotta for the **single most commit-shaped action** on a screen — "Run Cycle," "Sign Artifact," "Approve Gate." Never more than one terracotta-primary action per surface.
- **Do** display fail-closed Logician gates with the rust border + pink wash + left bar — louder than any other element on the screen. The operator must not be able to scroll past one.
- **Do** mark every pre-corpus claim with the `[CONJECTURE — Pillar-2 pending]` mono tag in conjecture-slate color. This tag is non-negotiable until corpus lands.
- **Do** show seat attribution via the colored seat badge on every artifact the council produces.
- **Do** use serif for all reading-length prose. Drafts, charters, FID summaries, rationale text — serif.
- **Do** use mono with ligatures **off** for IDs, hashes, fingerprints, F-CLASS codes, cycle IDs, org slugs.
- **Do** maintain WCAG AA contrast (4.5:1 normal text, 3:1 UI components) on both light paper and dark warm-black surfaces.

- **Don't** build a chat input. Golden Quill is not a chatbot. There is no message thread, no chat avatar, no "typing…" indicator. Council seats communicate through structured artifacts (drafts, scores, probe results, gate verdicts), not chat.
- **Don't** auto-submit to grants.gov or any funder portal. The submission surface is **packet-producer-only** (default). Direct submission is an explicit, gated, operator-confirmed action — and may not exist in v0.1 at all.
- **Don't** silently rewrite suspicious terms or admin-risk-register hits. The operator approves each substitution explicitly. Inline annotations show the original term, the suggested replacement, the severity tier, and an explicit "Apply / Keep" choice.
- **Don't** hide posture state or push posture changes through implicit toggles. Posture is changed only through the posture-change drawer with explicit operator typing + signature.
- **Don't** use blue or purple as primary accent. The palette is earth-tone — sage, terracotta, oak, rust, charcoal. Generic SaaS-blue is off-brand.
- **Don't** mix rounded scales on a single component. Pick the radius and stay.
- **Don't** stack more than two font weights of the same family on a single screen.
- **Don't** put consumer-grade chrome anywhere — no gradients, no glassmorphism, no animated illustrations. The product is infrastructure-grade. Restraint is the point.
- **Don't** show progress bars for cycle work without a numeric mono percentage and an estimated-completion timestamp. "Spinning…" is not enough; operators are watching cost.

---

## Product overview & positioning

Golden Quill is the **128 GB operator-owned appliance**. The hardware is fixed (Apple M3 Ultra Mac Studio, AMD GX-10, or NVIDIA Spark class, depending on supply). The software running on it is **Tilth** — the six-seat agent council, the Logician deterministic gate layer, the Five Operating Laws, the classification register, the FID corpus, and the audit/signing chain. One Golden Quill per client. One Tilth per Golden Quill.

Positioning line: *"Golden Quill — regenerative grant intelligence."* The UI must reflect the sovereignty promise: operator owns the hardware, operator owns the keys, operator's data stays local by default, every artifact is signed, the system runs offline.

## Primary user & role model

**Default: operator-only.** v0.1 ships as a single-operator surface. Josh (sole operator at FIT Farms) is the canonical user. Technical literate, project-management-experienced, decisive, terse. The UI assumes the operator knows what a gate, a posture, an Ed25519 signature, and a charter are.

**Open question (operator decision):** Multi-user / role-restricted views in v1.x or later. Possible roles: operator (full), reviewer (read + sign-off only), co-author (draft-section editing). v0.1 default is operator-only.

## Core workflows

Each workflow below describes a primary surface in the desktop shell. Mobile surfaces a subset (Sign-Off, Audit Trail, Draft viewer read-only).

### 1. Discovery (Scout)

Operator opens Discovery. Top of surface: applicant context selector — CIC dropdown (6 options: Food Systems, Educator, Public Agency, Arts & Culture, Cooperative, Ecosystem Intermediary), CLC dropdown (8 options: Public Purpose & Works, Catalytic Change, Operating Capacity, Research & Evidence, Market Access, Credit & Underwriting, Sponsorship & Corporate Support, Shared Assets), funder envelope field (optional).

Scout returns a ranked list of opportunities. Each opportunity card carries: funder name (serif), program code (mono), title (serif), submission deadline (mono, with relative chip "in 14 days"), confidence ribbon (5-step), fit rationale (3 lines max), source-backing tier (`VERIFIED_FIT` / `VERIFIED_NOT_FIT` / `UNVERIFIED` / `VERIFICATION_FAILED`).

Daemon mode toggle (top-right of surface) — when on, a sage pulse indicator appears in the top bar and the channel-family roster (A federal APIs / B curated cached datasets / C seeded portals / D federal program pages / E RSS / F client-material-driven web search) shows per-channel last-checked timestamps. One-shot mode runs on operator-triggered queries only.

### 2. Eligibility gate check (Logician)

After Scout returns and the operator picks an opportunity, the surface transitions to the Eligibility view. This is the load-bearing UX moment.

Logician runs the gate cascade (hard_eligibility_gates from Pass 1 taxonomy). The surface shows a vertical list of gate cards. Each card: gate code (mono, e.g. `E-101`), gate name, verdict (PASS / FAIL / PENDING), source-backed evidence (RFA section quoted in serif italic), and resolution action if fail.

If any gate fails closed, the surface locks the "Open in Scribe" action and displays a rust-bordered banner: `DO NOT DRAFT — 1 gate failed closed. Resolve E-104 before continuing.` The banner cannot be dismissed; it can only be cleared by resolving the gate.

### 3. Drafting (Scribe)

Once eligibility clears, the operator opens the draft surface. Two-pane layout: left is the editable draft (serif, 72ch column), right is the inspector (380px, surface-2).

Top-of-pane chip: funder-specific register being applied (`Register: USDA-RD — mechanism-aware`, or `Register: SARE — outcomes-first`, or `Register: Heinz — narrative-first`). Section headers enforce the funder's charter ordering. Pre-corpus claims carry the `[CONJECTURE — Pillar-2 pending]` mono tag inline.

The inspector shows: voice (the funder dialect — conservative / centrist / progressive / soul-fire from Law 4), suspicious terms hits (from the admin-risk register), evidence-tier rating of the current paragraph, and the seat badge for whatever council seat last touched this section.

Inline edits: any term flagged by Law 4 shows as a wavy underline with a hover popover offering 2-3 replacement options. The operator chooses "Apply suggestion" or "Keep original" — never auto-applied.

### 4. Scoring (Judge)

The Scoring surface runs the draft against the funder's published rubric. Top card: predicted-score numeric (`82 / 100`) in display serif, with the funder's published threshold (`pass ≥ 75`) shown for context. Below: per-criterion bar list — each criterion in serif, score in mono, weight + cumulative. Each criterion expands into the evidence-ladder for that score.

Cross-family rigor indicators: Judge's model identity (mono, e.g. `google/gemini-2.5-pro`) and Scribe's model identity displayed side-by-side. If they share provider family, a rust warning chip appears: `Cross-family rigor violated — Judge and Scribe share provider family.` Operator decides whether to proceed or re-route.

### 5. Red Team probes

The Red Team surface runs the adversarial probe set against the draft. Probes display as a checklist: probe name (serif), verdict (clean / HIT), expanded HIT rows show the attack vector (e.g. `fake-fit signal: applicant claims partnership with X, no source evidence`) and the required response (`Scribe must remove or substantiate`).

If Judge's score and Red Team's verdict diverge by ≥10 points, a council-split banner appears: `Judge: 82 / Red Team: 68 — split exceeds threshold. Operator decides.` The banner pins on the cycle until the operator records a tie-break decision.

### 6. Operator sign-off

The Sign-Off surface is the final commit surface. Top-card: the final draft preview (PDF render or in-pane). Below: every signed artifact in the cycle as a list — draft, Scribe attestation, Judge score, Red Team verdict, Logician gate cascade, classification register reference, posture attestation. Each row shows artifact hash, seat, and current signature state.

Bottom: the **lock_history row preview** — mono table row showing exactly what will be committed. The operator pastes their Ed25519 signature into the signature input (mono, monospace, no autocorrect). On valid signature, the lock_history row commits atomically and the cycle moves to `committed` state.

Paired-commit ceremony events (when applicable — e.g. dual-LOCK rows like the §16 / §17 v1 reflection-packet / WPFA pair) display as a separate panel showing both artifacts side-by-side, both require operator sign-off in the same drawer.

### 7. Audit trail viewer

Always accessible from the audit pill in the top bar. Surface: a vertical timeline of lock_history rows, paired-commit ceremony events, signing chain events, and gate cascade traces. Each row in mono. Filter by cycle, org, seat, F-CLASS code, posture. Drill-down into any row reveals: the full artifact, the Ed25519 signature panel, the signing chain (router-template signature → operator signature → ceremony signature), and verification status.

If any signature fails verification (mid-cycle key rotation, corrupted artifact), the audit pill in the top bar turns state-fail rust and the affected rows are pinned to the top of the viewer.

### 8. Posture toggle

Surface accessed by clicking the posture badge. Slide-up drawer (charcoal background) with three options: Frontier-Eligible, Split-Context Hybrid, Local-Only-Sovereign. Each option carries a short serif explainer.

Posture change requires: (a) the operator to type the target posture name in full, (b) paste a fresh Ed25519 signature, (c) confirm the deployment manifest update. Mid-cycle posture changes fail closed per `F-CLASS-POSTURE-MID-CYCLE-CHANGE` — the drawer blocks the change and surfaces the active cycle ID.

### 9. BYOK cost dashboard

Per-cycle cost breakdown: total cycle cost (mono), per-seat cost (Scout / Scribe / Judge / Red Team), per-charter cost (which FID this work was billed against), cache-hit rate (mono percentage), posture-aware projection (`At current posture, monthly projected cost: $X. At Local-Only, projected: $Y`).

Cost data sources are the operator's own provider invoices (BYOK). No metered billing surface — Golden Quill never bills the operator.

### 10. Card selection matrix

The 6×8 CIC × CLC grid. Each cell carries the relevant charter excerpt for the (CIC × CLC) pair. Some cells are Option-A dual-track (marked with a split icon). Selecting a cell activates the charter and configures Tilth's search vocabulary, evidence schema, language register, reporting rhythm, and capital-logic activation per the canonical taxonomy.

### 11. FID browser

Funder Intelligence Database. List view of 14+ active charters + 117 net-new candidates (Pillar-2 corpus expansion). Per-charter: funder name, program code, verification status, corpus freshness, last cycle this charter was used. Drill into any charter shows the full charter document, mechanism details, rubric, evidence requirements, admin-risk hits, and dialect markers.

## Visual language reference

See the YAML front matter for token values. The visual language summary: paper-white surfaces, ink and slate text, terracotta for the single commit-action, earth-tone seat palette (sage / terracotta / oak / rust / charcoal), serif body + Inter labels + JetBrains Mono for IDs (ligatures off), 8px spacing scale, 4-6px corner radius, tonal-layer elevation (not shadows), fail-closed gates loud (rust border + pink wash + left bar), audit pill pinned, posture badge pinned, signing-key fingerprint in footer.

## Interactions & state

- **Loading.** Mono percentage + estimated-completion timestamp. No abstract spinners on cycle work. For instant local actions, a 1-frame paper-white fade is acceptable.
- **Fail-closed.** Rust border + pink wash + left state-fail bar + a resolution action. Operator cannot proceed past a fail-closed gate without resolving.
- **Conjecture-tagged.** Mono pill `[CONJECTURE — Pillar-2 pending]` in conjecture-slate color. Persistent until corpus lands.
- **Signed.** Mono signature chip with truncated Ed25519 fingerprint + `verified` state-verified color. Hover reveals full signature panel.
- **Verifying.** Mono signature chip in state-pending slate with a 0.6 Hz subtle pulse. Resolves to verified-green or state-fail rust within 200ms typically; longer signatures show a numeric progress.
- **Council-split.** Banner pinned at the cycle level with both Judge and Red Team verdicts visible until operator records a tie-break.

## Accessibility & responsive

- **WCAG AA minimum** on every token pair. The linter's contrast-ratio rule is enforced at component definition time.
- **Focus rings always visible** — 2px terracotta with 1px paper offset on every interactive element.
- **Keyboard navigation** — every surface reachable. Top-bar audit pill, posture badge, and signing-key fingerprint reachable via keyboard. Sign-off signature paste-back works without mouse.
- **Screen reader semantics** — gate verdicts announced as PASS / FAIL with the gate code; conjecture tags announced inline; seat badges announced before the artifact they attribute.
- **Reduced motion** — daemon-mode sage pulse and signature-verifying pulse both honor `prefers-reduced-motion: reduce` and become static color states.
- **Dark mode** — `prefers-color-scheme: dark` flips the surface stack (see Colors). Token references survive.
- **Mobile** — review surfaces only. Sign-Off, Audit Trail, read-only Draft viewer. Inspector behind a slide-up sheet. Posture changes desktop-only.

## What this UI is NOT

- **Not a chatbot.** No chat input, no thread, no message bubbles, no avatar typing indicator. Council seats produce artifacts; the operator reads and signs.
- **Not autonomous-submission.** Default is packet-producer; the operator manually submits to the funder portal. Direct submission, if it ever ships, requires explicit operator gating per cycle.
- **Not consumer-grade chrome.** No gradients, glassmorphism, animated illustrations, marketing copy, or onboarding overlays. The operator already bought the appliance.
- **Not a generic SaaS dashboard.** No blue-purple gradient, no "Welcome back, Josh!" greeting, no streak counters, no gamification.
- **Not a CRM.** Golden Quill is not for tracking funders as relationships; it is for shaping submission packets that win.

## Open questions for operator

1. **Primary user shape — operator-only vs role-restricted views.** Default in this DESIGN.md is operator-only. v1.x may add reviewer / co-author roles. Operator decides.
2. **Submission surface — packet-producer vs direct submission.** Default is packet-producer. Direct submission (grants.gov / funder portal integration) requires explicit go-ahead and may stay out of v0.1 entirely.
3. **Aesthetic anchor — Linear-like calm minimalism vs alternative.** Default is Linear-like (terse, monochrome-leaning, monospace IDs, restraint). Alternatives the operator could specify: more Stripe-like (more whitespace, softer borders), more Vercel-like (denser, blacker), or a custom anchor.
4. **Mobile parity.** Default is review-and-approve only (Sign-Off, Audit Trail, Draft viewer). Operator may want fuller mobile parity for traveling work.
5. **Daemon-mode default.** Default off (one-shot Scout). Operator may want daemon-on as the deployment-default for FIT Farms.
6. **Posture default.** v0.1 ships with **Split-Context Hybrid** as the recommended default for Confidential-bearing grants. Operator may set deployment-default to Local-Only-Sovereign for higher-custody posture.
7. **Council-split threshold.** Default is ≥10 points between Judge and Red Team. Operator may want tighter or looser.
8. **Footer signing-key fingerprint display.** Default: truncated mono fingerprint with hover for full hash. Operator may prefer it permanently expanded.
9. **Cost dashboard granularity.** Default is per-cycle, per-seat, per-charter. Operator may want per-call (more detail) or per-week (less detail).
10. **Dark-mode default.** Default is `prefers-color-scheme` driven. Operator may want dark-always or light-always.

## Notes for the AI UI generator

This DESIGN.md is the source of truth for any Golden Quill UI surface. When generating UI:

- Use the canonical 8-section structure (Overview / Colors / Typography / Layout / Elevation / Shapes / Components / Do's & Don'ts) as primary constraint.
- Treat the seat palette (sage / terracotta / oak / rust / charcoal) as load-bearing — every council artifact must carry its seat badge.
- Treat the audit pill, posture badge, and signing-key fingerprint as **non-removable chrome** on desktop. The operator must always be able to see them.
- Treat fail-closed gate displays as the loudest visual the system produces. They must not be styled into compliance with surrounding chrome.
- Treat the conjecture tag and evidence-tier pills as functional UI, not decoration. Their presence/absence is information.
- Default to serif for prose, Inter for UI affordances, JetBrains Mono (ligatures off) for IDs.
- Default to packet-producer submission, operator-only user shape, and Split-Context Hybrid posture unless the operator overrides.

When in doubt: pick the more restrained, more sovereign-signaling option. This is infrastructure for an operator who signs every artifact with their own key. The chrome has to earn that signature.
