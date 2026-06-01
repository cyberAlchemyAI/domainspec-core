<!-- seat=editor family=meta model=groq/llama-3.3-70b-versatile dispatched_at=2026-05-10T03:52:11Z -->

### FINDING E-01 — Ambiguous Register Distinction
**Where:** §1 and §2
**Severity:** MEDIUM
**Issue:** The two-register distinction between Funder Intelligence Database and Match Database may not be immediately clear to a builder, potentially leading to confusion about which register holds what information.
**Why it matters:** This ambiguity could result in incorrect implementation or misuse of the registers, compromising the integrity of the system.
**Suggested fixes:**
(a) Provide a concise summary or table highlighting the key differences between the two registers.
(b) Use distinct naming conventions or prefixes for the registers to emphasize their differences.
(c) Include a diagram or illustration to visually represent the relationship between the two registers.

### FINDING E-02 — Unclear Curation Cadence
**Where:** §6
**Severity:** LOW
**Issue:** The amendment suggests a quarterly curation cadence for Funder Intelligence Database but does not specify when the operator receives the curation prompt.
**Why it matters:** This lack of clarity might lead to inconsistent or overlooked curation, potentially affecting the quality of the data.
**Suggested fixes:**
(a) Specify the exact timing or trigger for the curation prompt (e.g., at Tilth wake-up, on a Tilth cron).
(b) Provide a clear definition of the curation process and its frequency.
(c) Delegate the curation schedule to a companion section (§5) for further elaboration.

### FINDING E-03 — Illustrative YAML
**Where:** §1 and §2
**Severity:** LOW
**Issue:** The YAML examples provided for the Funder Intelligence Database and Match Database registers are not explicitly labeled as illustrative.
**Why it matters:** This might lead to confusion about whether the YAML is final or subject to change.
**Suggested fixes:**
(a) Clearly label the YAML examples as illustrative or provisional.
(b) Provide a note explaining that the YAML is subject to change or refinement.
(c) Include a version number or date to indicate the YAML's status.

### FINDING E-04 — Stage-5 Boundary
**Where:** §4
**Severity:** MEDIUM
**Issue:** The amendment introduces consent tiers and the concept of a Stage-5 cooperative commons, which might blur the boundary between v0.1 and Stage-5 functionality.
**Why it matters:** This blurring could lead to unrealistic expectations or confusion about the current capabilities of the system.
**Suggested fixes:**
(a) Emphasize the distinction between v0.1 and Stage-5 functionality.
(b) Provide a clear statement about what is included in v0.1 and what is deferred to Stage-5.
(c) Use separate sections or documents to discuss Stage-5 features and avoid mixing them with v0.1 details.

### FINDING E-05 — Cross-Amendment Composition
**Where:** §7
**Severity:** LOW
**Issue:** The composition narrative between v7.0.5, v7.0.4 (KFR), and v7.0.7 (classification) might benefit from additional clarity or visual aids.
**Why it matters:** This could lead to difficulties in understanding how the different components interact and relate to each other.
**Suggested fixes:**
(a) Include a diagram or table to illustrate the relationships between the components.
(b) Provide a brief summary or overview of the composition.
(c) Use clear and concise language to explain the interactions between the components.

**Verdict:** REQUIRES_FIX. While the amendment provides a solid foundation for the Funder Intelligence Database and Match Database, there are areas that require clarification and refinement to ensure the distinction between the two registers is clear, the curation cadence is well-defined, and the Stage-5 boundary is crisp. Addressing these findings will improve the overall quality and usability of the amendment.
