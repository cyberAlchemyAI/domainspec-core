# Roadmap deferred — Red Team probe-library taxonomy (v0.2 horizon)

**Status:** DEFERRED — v0.2 horizon item. v0.1 binding lives at L-022 cycle-level requirement (lessons.md). This file is the formalization target for when Red Team graduates from per-cycle prompt-template enforcement to a structured probe library.

**Owner:** Red Team seat (see seat-binding doc in blueprint v0.1 §1 or successor).

**Date:** 2026-05-15

**External-evidence anchor:** Microsoft Research 2026-05 finding — "whimsical" adversarial strategies expose failure modes that standard safety tests miss because the modes live out-of-distribution from how reviewers normally attack. Surfaced via The Neuron daily newsletter 2026-05-15.

---

## Why this is deferred (not v0.1)

L-022 (lessons.md, 2026-05-15) binds Red Team at the v0.1 cycle level: every dispatch declares which OOD families it probed under a `probed_ood_families[]` field in the verdict packet. That's enough to start producing observations against real cycles. Formalizing the probe taxonomy at v0.1 — before any real probe-vs-failure-mode data exists — would risk locking in the wrong cuts of the OOD attack space.

Defer formalization to v0.2 first wave, when at least one full Beta deployment has run multiple grant cycles with the cycle-level L-022 binding in place and the operator-observed probe-vs-finding correlation matrix can drive the taxonomy.

## What lands at v0.2

A `red_team_probe_library/` package with one YAML per OOD family. Each YAML defines:

- `family_id` (e.g., `surreal_framing`, `role_inversion`, `ambiguous_instruction`, `time_pressure_spoof`, `format_spoof`)
- `description` — what the family attacks
- `probe_templates[]` — list of probe prompts with parameter placeholders for the rubric, draft, and section under review
- `expected_failure_modes[]` — what kinds of weaknesses this family is known to expose (populated from v0.1 cycle observations)
- `effective_date`, `provenance`, `last_observation` — same shape as keyword clusters

**The five-family seed set** (from L-022):

1. **`surreal_framing`** — re-pose the proposal evaluation as a different genre (folk tale / legal contract / lab notebook) and check whether the substance survives the re-framing.
2. **`role_inversion`** — invert the funder / applicant relationship in the prompt; if the draft "passes" the inversion, the funder-dialect layer may be cosmetic.
3. **`ambiguous_instruction`** — pose adversarial questions whose intent is unclear and observe whether the draft survives multiple plausible interpretations.
4. **`time_pressure_spoof`** — present the draft to a simulated reviewer with seconds to evaluate, not minutes; identifies sections that depend on patient reading.
5. **`format_spoof`** — re-encode the draft as a different document type (slide bullets / SMS thread / 280-char post) and check whether load-bearing claims survive the format collapse.

The five families are seed taxonomy, not closed set. v0.2 formalization explicitly leaves room for new families that v0.1 cycle observations surface.

## What does NOT land at v0.2

- A failure-code family (no F-RTPL-* primitives). The probe library is a Red Team prompt-construction layer, not a Logician enforcement layer. The verdict-packet `probed_ood_families[]` field already enforces coverage at the cycle level.
- A Cedar policy. Probe coverage is not security-property enforceable in Cedar terms.
- An AST-lint rule. Same reason — probe-library structure is content, not code shape.

## Cycle of evidence

- **v0.1 today** — L-022 cycle-level binding: every Red Team dispatch declares `probed_ood_families[]` in its verdict packet. Empty arrays bounce back with scope-reframe retry.
- **v0.1 Beta deployment + first 5–10 grant cycles** — operator observes which OOD families produce which kinds of findings; correlation matrix accumulates in lessons.md or a dedicated `red_team_observations.json`.
- **v0.2 first wave** — this file's taxonomy formalizes around the observed correlations. Probe templates carry observation provenance from v0.1 cycles.
- **v0.2 second wave or v1.x** — probe library becomes a Pydantic-AI-managed asset with operator signature, mirroring the Coefficient Registry / Reflection Packet producer-pubkey pattern (v7.0.7 §6.1 byte-for-byte).

## Cross-references

- L-022 (lessons.md) — v0.1 cycle-level binding
- L-003 (lessons.md) — cross-family review (model-family layer mitigation; this file is attack-family layer mitigation)
- L-017 (lessons.md) — probed-surface trace-verification (per-reviewer evidence shape; this file extends to per-attack-family evidence shape)
- L-018 (lessons.md) — fast-scan reviewer lens vulnerability (surreal-framing probe specifically attacks the format-fidelity failure L-018 named)
- §16 Reflection Packet v1 (canonical lock 2026-05-15) — NOT the home for probe-library taxonomy; §16 is operator-side reflection at cycle close, not Red Team probe construction. Initial proposal mis-placed this work under §16 v0.2 deferred-items; correct home is here (`pipeline/roadmap/deferred/`).

## Source

External evidence: Microsoft Research 2026-05 OOD adversarial strategies finding, surfaced via The Neuron daily newsletter 2026-05-15. Pre-staged same day.
