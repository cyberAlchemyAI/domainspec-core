<!-- seat=judge family=google model=google/gemini-2.5-pro dispatched_at=2026-05-10T03:52:54Z -->

## Judge Review: Tilth Architecture Amendment v7.0.5

**ORG:** goldenquill
**TRACE:** v7-0-5-thesis-cycle-1-2026-05-09
**REVIEWER_FAMILY:** Google
**REVIEW_SEAT:** Judge

---

### **Premises**

-   **P1:** Law 3 (Org Isolation) is a non-negotiable, P0 invariant; no cross-org reads are permitted. (Source: Project context, Five Operating Laws).
-   **P2:** The v7 substrate is frozen; the amendment must reuse FAISS/Chroma, bge-large-en-v1.5, and Pydantic AI. No new dependencies. (Source: Project context, Substrate per v7.0.3).
-   **P3:** New failure codes must be enforceable by the Logician agent: deterministic, fail-closed, zero-token cost. (Source: Project context, Logician fail-closed).
-   **P4:** Stage-5 cooperative features are forward-design only for v0.1. The default behavior must be `my_eyes_only` with zero data exfiltration. (Source: Project context, Cooperative sovereignty consent tiers; Amendment §4).
-   **P5:** CIC × CLC orthogonality is locked per v7.0.8; no design-time coupling is permitted between applicant identity and funder logic archetypes. (Source: Project context, Cross-cutting invariants).
-   **P6:** The amendment must align with the v7.0.6 roster, which reserves the Archivist seat for v1.x curation tasks. (Source: Amendment §6, §10).
-   **P7:** The Funder Intelligence Database and the v7.0.4 KFR are orthogonal substrates (per-funder vs. per-org). (Source: Amendment §7, §10).
-   **P8:** The amendment must compose with v7.0.7 classification, respecting data sensitivity for routing. (Source: Amendment §7, §10).
-   **P9:** The amendment's stated intent is to create compounding institutional knowledge from ephemeral Scout discoveries. (Source: Amendment, Amendment intent).
-   **P10:** The Red Team pass on the Match Database's Law 3 enforcement is considered critical. (Source: Amendment §10, Thesis-round priorities).

### **Execution Trace**

1.  **Funder Intelligence Database Substrate:** §1 correctly specifies the use of FAISS/Chroma and bge-large-en-v1.5, explicitly stating it is the "Same...substrate as KFR Intake." This satisfies **P2**.
2.  **Match Database Law-3 Enforcement:** §2 places the Match Database at a per-org path (`orgs/<slug>/match_database/`). §5 introduces the `F-MATCH-DB-CROSS-ORG` failure code, which is a deterministic path check suitable for the Logician agent. This design directly addresses the core requirement of **P1** and acknowledges its criticality per **P10**.
3.  **Scout Channel G Integration:** §3 introduces Channel G as a "parallel primary" source, consistent with the architecture of existing channels A-F. The integration of de-duplication against the per-org Match Database is a robust enhancement. This fulfills the intent of **P9** by creating a feedback loop.
4.  **Stage-5 Consent-Tier On-Ramp:** §4 explicitly defines the scope as "forward-design, not Stage-1 build" and correctly implements the `my_eyes_only` default. The schema reserves the `consent_tier` field without creating any v0.1 implementation dependency on the non-existent commons. This strictly adheres to the scope discipline required by **P4**.
5.  **Archivist Curation-Slot Binding:** §6 binds the curation lifecycle to the slot reserved for the Archivist in v7.0.6. It correctly separates the v0.1 operator-led function from the future v1.x agent-led function without requiring a schema change. This demonstrates proper composition with companion amendments per **P6**.
6.  **Composition with v7.0.4 KFR and v7.0.7 Classification:** §7 clearly articulates the orthogonal roles of KFR (per-org facts) and the Funder Intelligence Database (per-funder facts), satisfying **P7**. It also correctly applies the v7.0.7 classification model, marking Funder Intel as `public` and adding a per-entry classification field to the sensitive `match_reasoning.narrative_summary`, satisfying **P8**.
7.  **CIC × CLC Orthogonality:** The Match Database schema's `identity_match` field (§2) represents a *runtime outcome* of matching a client's CIC against an opportunity's criteria. It does not create a design-time schema coupling between specific CICs and CLCs. This design correctly respects the orthogonality invariant (**P5**).

### **Rubric**

| Dimension | Score | Justification |
| :--- | :--- | :--- |
| D1: Scope clarity | 20/20 | Excellent. The "What this amendment does not do" section (§9) is exemplary, clearly defining boundaries and managing expectations. |
| D2: Self-consistency | 20/20 | The two new registers and the Scout channel augmentation are logically interconnected and serve the stated intent (**P9**) without internal contradiction. |
| D3: Discipline alignment | 19/20 | Alignment with core invariants (**P1, P2, P3, P4, P5**) is strong. A minor concern (DC-01) is noted regarding potential data inference from structured fields. |
| D4: Enforceability | 20/20 | The new failure codes in §5 are deterministic (path check, hash check, timestamp check) and well-suited for Logician implementation, satisfying **P3**. |
| D5: Completeness | 18/20 | The amendment is largely complete, but lacks specificity on the lifecycle of a funder document after its relevance score decays to a minimum threshold (DC-02). |
| **Total** | **97/100** | |

### **Conclusion**

**REQUIRES_FIX**

The amendment is architecturally sound, well-scoped, and demonstrates rigorous alignment with core project invariants. The design for the Match Database correctly prioritizes Law-3 isolation. The identified issues are minor and can be addressed with clarifications in companion blueprints without altering the core schemas proposed here. The amendment is fit for purpose and on track for LOCK pending the resolution of two design concerns.

---
**Design Concerns:**

**DC-01 (Severity: LOW)**
*   **File:** `v7.0.5 amendment text`
*   **Cue:** §2, `match_reasoning.structured` block
*   **Concern:** The `narrative_summary` has an explicit classification field, but the `structured` block does not. A combination of `true` flags (e.g., `identity_match`, `geography_match` for a specific rural county, `sector_match` for a niche sector) could allow for the inference of confidential client strategy, even if the narrative is redacted.
*   **Fix:** In `pipeline/blueprint/v0.1/section_05_pipeline.md`, add a note specifying that the aggregate risk of the `match_reasoning.structured` block should be considered when setting the `narrative_summary_classification`. For Stage-5, this entire block should inherit the narrative's classification for commons-routing purposes.

**DC-02 (Severity: LOW)**
*   **File:** `v7.0.5 amendment text`
*   **Cue:** §1, `relevance` block
*   **Concern:** The Funder Intelligence Database schema includes a `decay_curve` but does not specify the terminal state for a document whose relevance score has fully decayed. This could lead to corpus bloat or ambiguity about whether the document is considered "archived" or merely "irrelevant".
*   **Fix:** In `pipeline/blueprint/v0.1/section_05_pipeline.md`, add a sub-section on "Funder Intelligence Corpus Lifecycle" that defines the behavior for documents with a relevance score below a configurable threshold (e.g., they are moved to an `archive/` state and excluded from Channel G queries by default).
