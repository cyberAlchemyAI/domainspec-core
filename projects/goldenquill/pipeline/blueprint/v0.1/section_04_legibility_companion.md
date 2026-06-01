# Section 4 Legibility Companion — Huyen Vocabulary Map

**Status:** Companion document. Does NOT modify Section 4 LOCKED v2. Read alongside `section_04_logician.md`.
**Date:** 2026-04-18
**Purpose:** External-reader legibility. Map Section 4's locked vocabulary onto the public vocabulary of Chip Huyen's *AI Engineering* (O'Reilly, 2024–2025) so reviewers who know the book's vocabulary recognize the pattern instead of treating Tilth as novel ceremony.
**Motivation:** 2026-04-18 external critique of Tilth characterized the architecture as "psychotically over-engineered." Part of the reason is that the vocabulary is internal. This companion document is the cheapest mitigation: same mechanisms, public vocabulary.

---

## 1. Scope and non-scope

**This document:**
- Is a glossary cross-reference, not a re-specification.
- Does not alter any Section 4 mechanism, gate, failure code, Cedar allowlist row, or rubric dimension.
- Is non-authoritative. If this document and Section 4 disagree, Section 4 wins.
- Versions independently of Section 4. Lock bar: Editor pass + Judge ≥ 85, no Red Team (zero new attack surface).

**This document is NOT:**
- An endorsement of any particular book, framework, or methodology as binding.
- A replacement for Section 4, Section 5 Judge rubric, or the admin-risk register.
- A claim that Tilth was built *from* Huyen's book — the book is a post-hoc legibility peg.

---

## 2. Why map to Huyen specifically

*AI Engineering* is the most widely-read practitioner text on LLM system design as of 2026. Reviewers with engineering backgrounds read it. If we describe Logician in Huyen's chapter-3-chapter-4 evaluation vocabulary, a reviewer's internal reaction is "I know this pattern" instead of "what is this custom thing." That reaction gap is where bus-factor anxiety lives. Closing it is cheap.

---

## 3. Vocabulary cross-reference

| Huyen term (*AI Engineering*) | Tilth / Section 4 term | Where in Section 4 | Notes |
|-------------------------------|------------------------|-------------------|-------|
| **AI-as-Judge** | Judge seat (see Section 5 rubric; Logician enforces rubric outputs at POST-gate) | §4.4 POST-gate; §4.7 (rubric-dimension threshold enforcement) | Huyen: Ch. 3. Tilth specifies the evaluator must not share model family with the drafter (cross-family rigor); Huyen mentions but does not mandate family separation. |
| **Golden Set** | Rubric-library seeded exemplars per grant family | `pipeline/rubrics/` read-only shared; §4.4.1 #7 | Huyen: Ch. 3. Tilth uses funder's own rubric first, then cross-checks related rubrics from the library. |
| **Pairwise Comparison** | Cross-family Judge vs. Scribe output comparison | Section 5 (Judge seat); referenced in §4.4.1 #7 | Huyen: Ch. 3. Tilth's implementation is single-judge-against-rubric, not pairwise; this is a v0.2 upgrade candidate. |
| **Rubric** | Per-funder rubric library (e.g., `pipeline/rubrics/vapg_fy26.json`) | §4.4.1 #7 calls into Section 5 rubric | Huyen: Ch. 3. Tilth matches on this term directly. |
| **Context Adherence** | Claim-evidence map (BT7) + DOC_SOURCED grep window (BT10) | §4.5, §4.6 | Huyen: Ch. 4 (grounding). Tilth's version is token-granular and deterministic, not probabilistic; stronger than typical Galileo-style scoring. |
| **Grounding** | Law 1 (RFA is the source of truth) + BT7 + BT10 | §4.4 PRE-gate Law 1 check; §4.5; §4.6 | Huyen: Ch. 4. Tilth's grounding is multi-source-required, not retrieval-quality-scored. |
| **Hallucination (closed-domain)** | `F-POST-05.unsourced_claim`; `F-POST-06.claim_evidence_mismatch` | §6.1 failure codes | Huyen: Ch. 4. Tilth treats closed-domain hallucination as hard-fail at POST-gate, not as a score. |
| **Hallucination (open-domain)** | Out-of-scope at v0.1 per Law 1 | §10 (open questions); referenced in §1.4 threat model | Tilth-specific: RFA + applicant-provided dossier are the only grounding sources by design. |
| **Evaluation Pipeline** | PRE-gate + POST-gate + revision loop | §4.3 gate topology; §4.4 gate contents | Huyen: Ch. 3. Tilth's evaluation pipeline is deterministic-first (Logician) with AI-scored dimensions (Judge) inside a fail-closed envelope. |
| **Eval Harness** | Section 9 property-based tests; `pipeline/validation/` | §9 test vectors | Huyen: Ch. 3. Tilth has a per-section audit harness (Thesis Team seats) plus property tests per blueprint section. |
| **Safety Guardrail** | Admin-risk register (18 flagged terms); Cedar policy allowlist | `logician/registers/admin_risk_register.json`; §4.10.4 allowlist | Huyen: Ch. 7. Tilth's safety guardrails are grant-domain-specific, not general-purpose. |
| **Instruction Adherence** | Five Operating Laws enforcement at PRE/POST gates | §4.4 gate contents; §6.1 `F-PRE-*` / `F-POST-*` codes | Huyen: Ch. 5. Tilth's implementation is deterministic Cedar + Python, not AI-scored. |
| **Tool-Use Evaluation** | Scout verifier (VERIFIED / VERIFICATION_FAILED / UNVERIFIED) | Section 3 Scout; Section 4 §4.6.3 verify-method tag | Huyen: Ch. 6. Tilth's tool-use eval is source-availability-bound (can we re-fetch?) rather than LLM-inferred. |
| **Observability** | Append-only signed conversation log (BT9); rails report (BT13); admin-risk ledger (M8) | §4.7 BT9; §4.8 BT13; §4.7.3 M8 | Huyen: Ch. 9. Tilth's observability is on-disk signed append-only, not remote telemetry — required by Sovereignty Promise. |
| **Checkpointing** | AR-1 save-state-always | §4.4 gate contracts include checkpoint-on-both-success-and-failure | Huyen: Ch. 8. Tilth elevates this to an operating rule (AR-1), not a best practice. |
| **Metric as Code** | Each failure code `F-PRE-*` / `F-POST-*` is a named, versioned, testable predicate | §6.1 failure-code schema; §9 tests | Huyen: Ch. 3. Tilth matches this pattern by construction; could be made more explicit in Section 4 v3 by a one-sentence methodology note. |
| **Cost / Latency Budgeting** | Three-iteration revision cap (Section J of architecture); per-seat provider cascade | Section 5 (revision loop); referenced in §1.3 non-ownership | Huyen: Ch. 8. Tilth caps by iterations (quality proxy) rather than tokens / dollars (cost proxy); v0.2 candidate to add a dollar-budget cap. |

---

## 4. Patterns present in Tilth but not common in *AI Engineering*

These are genuinely Tilth-specific and do not have a Huyen-book equivalent. They should be flagged in external descriptions as novel, not hidden behind borrowed vocabulary.

1. **Cross-family rigor as a hard rule, not a preference.** Judge must not share model family with Scribe. Huyen discusses the benefit of independent evaluators; Tilth mandates it at the allowlist level. (Section 4 §4.9 + Section 5 rubric.)
2. **Admin-risk register as a domain-specific terminology guardrail.** Huyen's safety chapter talks about toxicity and PII; he does not cover regulatory-dialect term risk. This is a grant-writing-specific guardrail with no generic analogue.
3. **Fail-closed envelope across six seats** (per v7.0.6 SELF-LOCKED 2026-05-09). Huyen discusses eval pipelines; Tilth runs the eval pipeline inside a deterministic envelope where any gate failure can be hard-blocking. This is architecturally stricter than common LLM-app patterns.
4. **Operator final-review gate as the last step.** Huyen treats human-in-the-loop as optional. Tilth's Law 5 + L-001 make it mandatory at sign-off. (Section 4 §4.4 final-review gate.)
5. **Cedar policy + write-intent enum as the authorization substrate.** Huyen's book pre-dates common Cedar usage for LLM authorization and does not cover this pattern. (Section 4 §4.10; Section 2 v7 §4.10.4.)

---

## 5. When to cite this companion

Use in:
- External technical reviews (offer the vocabulary map up front so the reviewer recognizes the pattern).
- Grant-infrastructure proposals (foundation/VC/B-corp audience).
- Hiring for blueprint-maintenance cover (candidate reads this first, then Section 4).
- Section 0.5 interface-index doc preamble (when authored after Section 5 locks).

Do NOT use in:
- Tilth internal blueprint authoring (the locked blueprints are authoritative; this is translation, not source).
- Cedar policy authoring (Cedar files cite `§` numbers in Section 4, not book chapters).
- Failure-code definitions (the `F-` codes are canonical; Huyen's terms are explanatory only).

---

## 6. Audit trail

- 2026-04-18: initial companion authored alongside Galileo taxonomy cross-check (`pipeline/validation/logician_taxonomy_crosscheck_2026-04-18/galileo_crosscheck.md`).
- Triggered by 2026-04-18 external critique citing "psychotically over-engineered."
- Related memory: `project_bus_factor_interface_index.md`.
- Lock bar (this doc only): Editor pass + Judge ≥ 85. No Red Team round (zero new attack surface introduced by a glossary).
