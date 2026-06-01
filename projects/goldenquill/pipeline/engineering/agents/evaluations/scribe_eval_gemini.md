# SCRIBE Self-Evaluation (Gemini Pro) — 2026-04-20

**Model:** google/gemini-2.5-pro
**Old:** skills/scribe-ghostwriter/SKILL.md
**New:** pipeline/engineering/agents/scribe_writer_agent_v1.md

---

## IMPROVEMENTS (what NEW does better for grant outcomes)
- **State Management and Resilience (Sections 4, 18)**: The `draft_manifest.json` with per-section state saving is a critical workhorse feature. It prevents data loss from crashes, which is vital during long drafting sessions. The explicit `Compaction Survival` protocol also makes the agent more reliable and predictable turn-over-turn.
- **Validation Self-Check (Section 16)**: The 12-point checklist before marking a draft complete is the operationalization of Rule 2 ("Test Your Own Work"). For a workhorse, this pre-flight check prevents shipping a draft with simple, unforced errors made under pressure, like forgetting to resolve `[UNSOURCED]` tags or having a budget that doesn't match the work plan.
- **Narrative Coherence Check (Section 8)**: The "Golden Thread" test transforms Scribe from a section-filler into a true grant writer. By checking that the needs statement sets up the approach, which delivers the objectives, which are funded by the budget, it automates the single most important (and most often missed) aspect of a winning proposal.

## REGRESSIONS (what OLD did better that NEW lost or weakened)
- **Simplicity and Speed**: The OLD prompt was self-contained and simple. The NEW prompt's reliance on numerous external files (`SOUL.md`, `router.yaml`, `dialect_codebook.yaml`, etc.) introduces multiple points of failure. A workhorse needs to be robust; if `dialect_codebook.yaml` is missing, the OLD prompt still functions while the NEW one is degraded.
- **Inline Checklists**: OLD had the Overlooked Expenses checklist directly in the prompt. It was less elegant, but it could not fail to load. NEW's reference to `overlooked_expenses_checklist.yaml` is cleaner architecture but more brittle in practice.
- **Program-Specific Detail (Section 14)**: The OLD prompt provided five specific, mandatory components for a VAPG grant. The NEW prompt compresses this to a two-bullet summary. For a workhorse targeting a specific grant like VAPG, losing that explicit checklist is a significant step backward.

## MISSING (gaps in both versions)
- **Deadline/Triage Mode**: A true workhorse needs to adapt to time pressure. Neither prompt defines a "fast-track" mode that could, for example, defer the full three-tag claim mapping in favor of a source-only tag to get a complete draft out faster, with full validation happening in a later pass.
- **Boilerplate Management**: Grant writing involves significant repetition (organizational history, key personnel bios). Neither prompt specifies a secure protocol for pulling pre-approved, Law 3-compliant boilerplate from a dedicated library (e.g., `orgs/<client>/boilerplate/`), forcing the agent to rewrite standard content repeatedly.

## TENSIONS (tradeoffs where reasonable people would disagree)
- **Rigorous Tagging vs. Drafting Velocity (Section 9)**: The three-tag system per claim is architecturally pure and creates a perfectly auditable draft. However, it imposes significant overhead during the creative drafting process. Under a tight deadline, many would argue for a "draft first, tag later" workflow to avoid slowing down the initial writing.

## VERDICT: UPGRADE — The structural improvements in state management and narrative coherence create a more reliable workhorse, but its dependencies make it less resilient than the original.

## TOP 3 CHANGES before deploying NEW as replacement
1.  **Introduce a `[DEADLINE_MODE]` flag**: When active, this mode simplifies the claim-tagging requirement to `[SOURCE]` tags only, deferring the full three-tag map to a post-draft validation pass. This prioritizes getting a complete draft done over perfect real-time auditing.
2.  **Add a Boilerplate Protocol**: Define a mechanism for Scribe to securely pull and insert pre-written, approved content from an `orgs/<client>/boilerplate/` directory. This increases speed and consistency, which are key for a workhorse.
3.  **Restore Program-Specific Checklists**: Re-integrate the detailed, multi-point checklists from the OLD prompt's "Program-Specific Templates" section back into Section 14, especially for high-frequency targets like VAPG.
