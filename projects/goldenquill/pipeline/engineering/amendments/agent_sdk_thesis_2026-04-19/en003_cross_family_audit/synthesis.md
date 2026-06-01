# EN-003 — Live Cross-Family Audit Synthesis

**Date:** 2026-04-19
**Subject:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-003_code_thesis_committee_kimi_replacement_2026-04-19.md`
**Audit trail:** this directory — editor_verdict.md, judge_verdict.md, red_team_verdict.md
**Author family:** Anthropic (Cowork / Claude)
**Live reviewer families:** Meta (Llama 3.3 70B), Google (Gemini 2.5 Pro — SELF-REFERENCE), OpenAI-OSS (GPT-OSS 120B)

## Promotion recommendation

**CYCLE-2-REQUIRED — promote to REQUIRES_FIX level.** Red Team raised two HIGH findings; self-reference concern is structurally unresolved. This is the strongest dissent of the three audits run today.

## Summary

| Seat | Family | Verdict | Score |
|------|--------|---------|-------|
| Editor | Meta | READY / minor | n/a |
| Judge | Google (**SELF-REFERENCE**) | PASS | 100/100 (flagged as biased — see below) |
| Red Team | OpenAI-OSS | REQUIRES_FIX | 2 HIGH + 4 MED |

## The self-reference problem — Judge's 100/100 is unreliable

Gemini 2.5 Pro (Judge) scored EN-003 at 100/100 while acknowledging the self-reference (Gemini reviewing an amendment that adds Gemini to the Committee). Gemini's self-assessment of "bias is assessed as low; fallback to Qwen not required" is exactly the kind of self-serving conclusion a biased judge would produce.

**Structural bias stands regardless of Gemini's self-report.** Red Team's RT-NEW-03 explicitly flags this: "P6 acknowledges the conflict but only flags a fallback to Qwen; it does not implement the fallback or enforce a conflict-of-interest block."

**Action required:** re-run Judge verdict through Qwen 3 32B (the documented fallback) before promoting EN-003 to LOCKED-sealed. Gemini's score should NOT be used as the primary Judge verdict for this amendment.

## Live Red Team findings (the substantive dissent)

### RT-NEW-01 — HIGH — "Forced by deprecation" bypasses full review

**Finding:** EN-003 uses "Kimi deprecated → must replace" to skip the full L-003 architectural review. No independent risk analysis beyond the deprecation citation.

**Mitigation:** Deprecation does not automatically grant exemption from full review. Add a separate impact-assessment step; require a Logician gate validating that "forced-by-deprecation" framing is used only for exact-replacement swaps, not for scope expansion or capability shifts.

### RT-NEW-05 — HIGH — Schema incompatibility never verified

**Finding:** EN-003 never confirms that Gemini 2.5 Pro's request/response schema handles the Code Thesis Committee's code-review prompt format. The five reviewers produce verdicts the Committee orchestrator must parse; if Gemini's output shape differs from Kimi's (different JSON structure, different tool-use format, different reasoning tokens), the pipeline breaks.

**Mitigation:** Before EN-003 promotes to LOCKED-sealed, run Gemini 2.5 Pro against the actual Code Thesis Committee prompt suite (archived from past Committee runs) and verify:
- Verdict output parses into the expected structure
- SFR three-block format is produced correctly
- Citation mechanism works for code references
- Token/latency envelope is compatible with Committee's budget

### RT-NEW-02 — MED — Kimi's ROLE contract not replaced, only its seat

**Finding:** Da Vinci v2 §3 describes Kimi's voice as "state the invariant explicitly, in code, not prose." EN-003 replaces the seat but doesn't verify Gemini performs the same ROLE. Different models have different tendencies — Gemini might prefer prose explanations even when instructed otherwise.

**Mitigation:** Add a role-fidelity test to the schema verification from RT-NEW-05. Verify Gemini's outputs match the ROLE contract (explicit invariants, code-over-prose), not just the family-taxonomy requirement.

### RT-NEW-03 — MED — Self-reference flagged-not-enforced

**Finding:** EN-003 acknowledges the Gemini-Judge-reviewing-Gemini-addition conflict but only documents the fallback to Qwen — doesn't enforce it. The simulated Thesis didn't catch this; live Red Team did.

**Mitigation:** Hard rule: any amendment that adds a model X to a committee MUST use a non-X-family Judge. Enforced as a Logician PRE-gate. For EN-003 specifically, re-run Judge verdict through Qwen.

### RT-NEW-04 — MED — Vendor lock-in shifted, not mitigated

**Finding:** The swap merely moves dependency from Moonshot (via Groq) to Google. If Google changes terms, API pricing, or deprecates Gemini 2.5 Pro, we're in the same position as Kimi 2026-03-23.

**Mitigation:** Add a lock-in risk register entry. Pre-author a contingency plan naming the NEXT replacement candidate (e.g., DeepSeek via Bedrock once AWS creds land). The plan sits in the lessons.md as a pre-positioned mitigation, not reactive.

### RT-NEW-06 — MED — Future Gemini deprecation risk

**Finding:** No contingency for the scenario where Google deprecates Gemini 2.5 Pro. The amendment repeats the same pattern (deprecation-forced swap) it claims to solve.

**Mitigation:** Embed a "future-deprecation watch" in the quarterly audit for every Committee reviewer model. Pre-author the fallback slot. Standing rule: every amendment that introduces a new model dependency must include the NEXT-replacement plan.

## Editor notes

READY with minor fixes suggested. No substantial blockers.

## Cycle 2 action items

1. **[HIGH-BLOCKING]** Re-run Judge verdict through Qwen 3 32B (non-self-referencing). Gemini's 100/100 discarded.
2. **[HIGH]** RT-NEW-05 — schema/role compatibility verification against archived Committee prompts BEFORE LOCK-sealed.
3. **[HIGH]** RT-NEW-01 — add "deprecation does not grant review exemption" rule.
4. **[MED]** RT-NEW-02 — role-fidelity test in the verification suite.
5. **[MED]** RT-NEW-03 — enforce self-reference block as Logician PRE-gate for all future amendments.
6. **[MED]** RT-NEW-04 — lock-in register + next-replacement pre-plan.
7. **[MED]** RT-NEW-06 — future-deprecation watch in quarterly audit.

## Meta observation

EN-003 drew the strongest live dissent of any audit this session. The self-reference pattern (Gemini reviewing a change that adds Gemini) cleanly exposes why L-003 needs enforcement, not just declaration. The simulated Thesis saw EN-003 as "narrow, forced-by-deprecation, clean swap." Live cross-family with GPT-OSS 120B surfaced six substantive findings including a schema-compatibility gap that could break the Code Thesis Committee entirely if we'd shipped.

Infrastructure again validated — the live cross-family path is doing the work it was designed for.

## Post-fix path

1. Address Cycle 2 items above.
2. Re-run full three-seat audit — with Judge swapped to Qwen 3 32B for THIS amendment specifically (recorded as an exception to the normal router.yaml Judge binding).
3. All three seats READY + zero HIGH findings + operator sign → LOCKED-sealed.

Until then, EN-003 stays at `LOCKED-internal-simulated`.
