# JUDGE Self-Evaluation — 2026-04-20

**Model:** google/gemini-2.5-pro
**Old:** /Users/goldenquill/Downloads/GoldenQuill/skills/judge-rubric/SKILL.md
**New:** /Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/agents/judge_scoring_agent_v1.md

---

## IMPROVEMENTS (what NEW does better for grant outcomes)
- **Funder Rubric Priority (Section 7)**: This is the most critical upgrade. OLD scored against an internal rubric and tried to map it. NEW scores against the funder's OWN rubric first, which is exactly what the real reviewer does. This directly aligns the scoring process with the actual submission gate.
- **G-Eval Chain-of-Thought Protocol (Section 6)**: The `REASON -> SCORE` sequence prevents anchor bias and halo effects. By forcing articulated reasoning *before* assigning a number, it makes the score an output of logic, not an initial guess. This dramatically increases objectivity.
- **Calibration Anchors (Section 8)**: Providing concrete WEAK/ADEQUATE/STRONG examples for the highest-weighted dimensions (Significance, Objectives, Approach) creates a stable, shared standard. This reduces scoring drift between sessions and models, making the 110/120 target meaningful.
- **Structured JSON Output (Section 12)**: Replaces OLD's unstructured text with a machine-readable JSON report. This enables robust pipeline automation, delta tracking between revisions, and feeding priority fixes directly to Scribe without fragile parsing.

## REGRESSIONS (what OLD did better that NEW lost or weakened)
- **Simplicity and Directness**: OLD's prompt was a one-page cheatsheet. A human could absorb the entire protocol in 60 seconds. NEW is architecturally sound but dense, with its protocol spread across multiple sections, requiring careful reading of lineage and external file references.
- **Human-Readable Default Output**: The default output in OLD was a clean, markdown-style report. While NEW specifies a natural-language summary must accompany the JSON, the primary artifact is machine-readable, losing the immediacy of the OLD format for quick human review.

## MISSING (gaps in both versions)
- **Integration with Scribe's Claim Tags**: The NEW Scribe prompt produces a `draft_manifest.json` with detailed claim-source mapping. Neither Judge prompt specifies how it consumes this manifest. Judge is still required to manually "cross-check claims against PROJECT_CONTEXT," duplicating verification work that Scribe has already done and logged. The pipeline lacks a formal handoff of the evidence map from Scribe to Judge.
- **Mechanism for Scoring Non-Textual Elements**: RFAs often require diagrams, Gantt charts, logic models, and complex tables. Neither prompt provides a methodology for evaluating the quality and compliance of these non-prose elements.

## TENSIONS (tradeoffs where reasonable people would disagree)
- **SFR Rigor vs. Velocity**: The new SFR format (Premises/Trace/Conclusion) provides an impeccable audit trail but is heavyweight. Applying it to all 12 dimensions, even a 5-point "Writing Quality" check that scores full points, creates significant overhead for marginal benefit. The tradeoff is perfect traceability versus a faster, "good enough" feedback loop.

## VERDICT: UPGRADE — The shift to funder-first scoring, G-Eval reasoning, and calibration anchors makes the scoring process fundamentally more rigorous and relevant to winning grants.

## TOP 3 CHANGES before deploying NEW as replacement
1.  **Integrate with Scribe's Evidence Map**: Modify Judge's Read Order (Section 3) to consume Scribe's `draft_manifest.json`. The protocol should validate Scribe's `[SOURCE]` tags rather than re-discovering them, focusing Judge's effort on scoring the *quality* of the evidence, not just its existence.
2.  **Scope the SFR Mandate**: Amend the protocol (Section 9) to require the full PREMISES/TRACE/CONCLUSION format **only for dimensions that receive a score deduction**. For dimensions at max points, a simple `[EVIDENCE: "quote"]` tag is sufficient, preserving rigor for fixes while increasing velocity.
3.  **Specify "Cross-Rubric Blind Spot" Protocol**: Clarify Section 7's "Cross-check 2-3 related rubrics" directive. Define the selection criteria (e.g., "select two other rubrics from the same agency" or "select one prior-year rubric for this program") and the action to take on discovered gaps.

---

## V1 → V2 RESOLUTION (2026-04-20, post-Opus re-evaluation)

A second evaluation pass (`judge_eval_prompt_opus.md`) produced an expanded TOP 3 plus a MISSING-in-both-versions gap list. Before any deployment, v1 was amended in place to v2 at `pipeline/engineering/agents/judge_scoring_agent_v1.md` (filename retained for call-site stability; internal `version: 2` is authoritative).

**Opus Top-3 applied:**
1.  **Calibration anchors extended** — §8 now carries three-level WEAK / ADEQUATE / STRONG anchors for dims 4, 5, 6, 7, 9, 11. Calibrated surface area grew from 45/120 pts (v1) to 79/120 pts (v2). Innovation, Qualifications, and Evaluation Plan were the most variance-prone unanchored dimensions in prior scoring runs.
2.  **Responsiveness Map + missing cue restoration** — §5 table regained "no typos" (Dim 1) and "no missing categories" (Dim 10). §3 added a mandatory responsiveness-map build step (RFA numbered question → draft section). §13 added five funder-specific validation items (responsiveness map, match credibility, budget narrative reconciliation, LOS specificity, funder-required compliance plans on Dim 11). §12 JSON schema extended with `responsiveness_map`, `unmapped_questions_count`, `funder_rubric_gate_met`, and `insufficient_dims` fields.
3.  **Externalization + hard-constraint fold-in** — §14 anti-pattern table moved to `pipeline/engineering/agents/judge_anti_patterns.md` with expanded evidence-discipline, funder-specific, and predicted-failure-mode entries. §16 "What Judge Never Does" folded into §1 Identity as a single paragraph. HARD CONSTRAINTS from `pipeline/engineering/templates/judge_prompt_template.md` folded into §10, including `INSUFFICIENT` promoted to a first-class scoring output (per Qwen-hardening precedent).

**First-Gemini-Eval Top-3 also applied (from original `judge_eval.md` above):**

1.  **Scribe manifest handoff** — §3 read order now consumes `draft_manifest.json` with explicit validation responsibilities (kgie / coherence / source_tag spot-check) rather than re-computing. If `unresolved_tags > 0`, Judge halts and returns to Scribe.
2.  **Scoped SFR** — preserved from v1 §9 (full SFR on deductions, simple evidence on max-score).
3.  **Cross-rubric selection criteria** — preserved from v1 §7 (prior-year same program → same agency different program → cognate different agency).

**MISSING-in-both gaps closed in v2:**

- Match/cost-share credibility check (Dim 10 cue + §13 validation item)
- Letters of support specificity (Dim 9 cue + Dim 9 STRONG anchor example + anti-pattern)
- Prior-award track record and close-out history (Dim 9 cue + STRONG anchor)
- Responsiveness map (§3 build step + §13 validation item)
- Budget narrative ↔ budget form total reconciliation (Dim 10 cue + §13 item)
- Funder-required compliance plans (Dim 11 cue + §13 item + STRONG anchor)
- Plain-language / equity / theory-of-change clarified as funder-driven (§7) — folded into Dim 4 / Dim 1 / Dim 7 when the funder doesn't publish them

**Intentionally not addressed in v2:** Non-prose element scoring (Gantt charts, logic-model diagrams, tables) remains gapped — assessed as lower-ROI than the six closed gaps and potentially better handled by Editor or a future visual-review seat. Flag for v2.1.

**Status:** v2 ready for pre-deploy Thesis Team round (Editor / Judge-self / Red Team cross-family audit) before LOCK. No LOCK declared here — two-audit-cycle discipline (L-005) requires Audit #2 on v2 before sealing.
