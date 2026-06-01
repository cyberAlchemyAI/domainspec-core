# SCOUT Self-Evaluation — 2026-04-20

**Model:** google/gemini-2.5-flash
**Old:** /Users/goldenquill/Downloads/GoldenQuill/skills/scout-discovery/SKILL.md
**New:** /Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/agents/scout_discovery_agent_v1.md

---

## IMPROVEMENTS (what NEW does better for grant outcomes)
-   **Mandatory Verification Protocol (Section 5.2)**: NEW introduces a critical `VERIFY` stage, demanding live synopsis fetches from primary sources (e.g., Grants.gov `fetchOpportunity`). This directly addresses the `EPA NEETP-26` precedent, preventing wasted effort on stale or ineligible data and significantly improving **grant outcome accuracy**.
-   **Architectural Integration & Read Order (Sections 2, 3, 4)**: NEW correctly references `/SOUL.md` for canonical operating laws and outlines a comprehensive "Read Order" (Section 3) and "Compaction Survival" (Section 4) protocols. This tighter integration with the broader Tilth architecture ensures Scout operates consistently and securely, directly contributing to **systemic reliability and reduced compliance risk**.
-   **Defensive Robustness (Sections 11, 12, 13)**: The new "Validation Self-Check" (Section 11), comprehensive "Anti-Patterns" (Section 12), and "Anti-Injection" (Section 13) directives provide robust internal safeguards. This greatly improves Scout's **reliability and resilience** against data quality issues and prompt manipulation, directly impacting grant outcome accuracy.
-   **Clearer Role Definition and Escalation (Sections 14, 15)**: NEW significantly expands "What Scout Does NOT Do" (Section 14) and includes specific "Escalation" guidance (Section 15). This explicitly defines Scout's function, reducing **operator ambiguity and preventing scope creep**.
-   **Parallel Channel Discovery (Section 5.1)**: The "Wide-net harvest across ALL six channel families" (Section 5.1) is a more comprehensive and resilient discovery approach than OLD's implicit tier-based search, ensuring **broader and more consistent opportunity capture**.

## REGRESSIONS (what OLD did better that NEW lost or weakened)
-   **Discovery Tier Interaction Clarity (Section 5.1 vs. Section 6)**: OLD (Section "Discovery Tiers," line ~25) unambiguously stated "Search in this order, always." NEW’s `STAGE 1: DISCOVER` (Section 5.1) instructs "Query all six channels... All six are parallel primary," then re-lists the tiers in Section 6 without clarifying their interaction. This ambiguity risks **inconsistent or suboptimal search execution** if the intended hierarchical prioritization of sources is lost.

## MISSING (gaps in both versions)
-   **Dynamic Channel Health Response**: While NEW (Section 5.1, Protocol 4) emits per-channel health (`OK|DEGRADED|FAILED`), neither version defines Scout's autonomous actions for `DEGRADED|FAILED` statuses (e.g., automatic retry limits, temporary exclusion, or dynamic strategy adjustments beyond the `3+ channels` rule in Section 15). This leaves a **gap in resilient operation when a single channel degrades**, potentially impacting discovery completeness.

## TENSIONS (tradeoffs where reasonable people would disagree)
-   **Inline Operating Laws vs. Referenced**: OLD embeds "Operating Laws" directly inline (line ~18), offering immediate context. NEW references `/SOUL.md` (Section 2), enforcing a single, canonical source of truth. This trades local, immediate rule visibility for **architectural consistency and centralized governance**, reducing drift risk.

## VERDICT: UPGRADE — The new prompt significantly enhances Scout's rigor, architectural alignment, and defensive capabilities, providing a much more reliable and auditable foundation for grant discovery.

## TOP 3 CHANGES before deploying NEW as replacement
1.  **Clarify Discovery Tier Search Logic**: Explicitly define how the sequential "Discovery Tiers" (Section 6) interact with the "Query all six channels" (Section 5.1) directive, ensuring a clear and unambiguous search order within the parallel channel framework.
2.  **Define Channel Health Reaction Protocol**: Add explicit instructions for Scout's autonomous response to `DEGRADED|FAILED` channel health statuses (e.g., retry limits, temporary exclusion, or specific escalation procedures), ensuring resilient operation.
3.  **Implement Operator Feedback Capture**: Create a mechanism within the "REVIEW" stage (Section 5.3) for Scout to systematically record operator decisions (e.g., "pursue" or "skip" for each candidate) to refine future discovery heuristics and improve outcome relevance.
