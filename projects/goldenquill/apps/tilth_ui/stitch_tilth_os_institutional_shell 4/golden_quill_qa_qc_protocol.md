# GOLDEN QUILL QA/QC PROTOCOL — High-Integrity Console Verification

Use this document to evaluate and harden every Golden Quill workstation screen. This is the adversarial benchmark for the Tilth funding operating system. Every output must be measured against these three pillars: **Compliance Sovereignty**, **Forensic Visibility**, and **Institutional Craft**.

---

## PILLAR 1: COMPLIANCE SOVEREIGNTY (THE GATES)

Golden Quill is not a helper; it is a governed boundary.

### 1.1 The Fail-Closed Check
- [ ] **Hard Block**: If a Logician gate is `UNKNOWN` or `FAIL`, is the primary "Forward" action (e.g., Drafting, Sign-Off) physically disabled or obscured?
- [ ] **Visual Volume**: Does the fail-closed state use the mandatory `rust` (#9C3C28) border, pink/rust wash, and a blunt warning banner?
- [ ] **Override Friction**: If an override exists, is it anchored by a `gold-burnished` (#B89745) indicator and a requirement for a cryptographic signature?

### 1.2 Identity & Licensing
- [ ] **Applied-As Context**: Is the `AppliedAsIndicator` visible in the top bar? Does it show both the Applicant and the Licensed Node?
- [ ] **Beneficiary Lock**: Does the screen verify that the Licensed Node receives >50% benefit? If not, is the export disabled?
- [ ] **Scrubbed Metadata**: In Authorization views, is the "Machine ID" clearly marked as scrubbed/sanitized for the final packet?

---

## PILLAR 2: FORENSIC VISIBILITY (THE PROVENANCE)

Every pixel must be accountable.

### 2.1 The Audit Trail
- [ ] **Audit Pill**: Is the `AuditPill` visible in the top bar with a current `lock_history` count?
- [ ] **Signature Chips**: Do all authorized artifacts (drafts, scores, overrides) carry a truncated Ed25519 fingerprint?
- [ ] **System Traces**: Do evaluation surfaces (Judge, Red Team) include a scrollable "System Trace" or "Log" showing the raw logic execution?

### 2.2 Truth in Labeling
- [ ] **Conjecture Tags**: Does any non-source-backed claim carry the `[CONJECTURE — Pillar-2 corpus pending]` tag in monospace?
- [ ] **Evidence Ladders**: Are scores decomposed into "Strongest," "Acceptable," "Weak," and "Unacceptable" tiers?
- [ ] **Staleness Triggers**: If a source has changed, is the affected component marked as `STALE` with a "Re-check Required" affordance?

---

## PILLAR 3: INSTITUTIONAL CRAFT (THE AESTHETIC)

The UI must feel like serious, owned infrastructure.

### 3.1 Typographic Discipline
- [ ] **Serif Reading**: Is all long-form prose (Drafts, Rubrics, Rationales) rendered in `Source Serif 4`?
- [ ] **Inter Controls**: Are all UI labels, buttons, and nav items in `Inter` (uppercase/tracked for categories)?
- [ ] **Mono Data**: Are all IDs, hashes, costs, and signatures in `JetBrains Mono`?
- [ ] **Line Length**: Is the reading column for drafts capped at ~72 characters?

### 3.2 Interaction Contracts
- [ ] **Lease Visibility**: In multi-user drafting, is the "Active Lease" chip visible, showing who holds the section lock?
- [ ] **Autosave Status**: Is there a visible "Saved just now" or "Saving..." indicator near every edit point?
- [ ] **Tonal Depth**: Does the UI use the "Paper/Bone/Ink" depth model (tonal layering) instead of consumer-grade drop shadows?

---

## ADVERSARIAL REJECTION CRITERIA

**Reject immediately if:**
- [ ] The UI looks like a chatbot (message bubbles, "AI is typing").
- [ ] There is a "Generate Entire Grant" button (Golden Quill is section-by-section).
- [ ] The color palette uses generic AI blue, purple gradients, or neon.
- [ ] Posture, Audit, or signing state is hidden inside a settings menu.
- [ ] Copy uses "soft" SaaS language (e.g., "Oops," "Let's get started!").
- [ ] The screen implies autonomous submission to Grants.gov (Golden Quill is a Packet-Producer only).

---

## QA/QC SUMMARY PROMPT FOR GENERATION
> "Apply the Golden Quill QA/QC Protocol. Ensure the shell implements the global identity boundary. Verify all Logician gates are fail-closed. Anchor all sovereign decisions in gold-burnished (#B89745). Enforce the serif-for-reading, mono-for-data rule. No chat bubbles. No autonomous submission. This is a local node console."