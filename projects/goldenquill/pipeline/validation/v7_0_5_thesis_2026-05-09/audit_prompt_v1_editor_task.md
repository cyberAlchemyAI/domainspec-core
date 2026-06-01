## Your task — Editor seat

Your family: **Meta (Llama 3.3 70B / Groq).** You are NOT Anthropic. Read with different eyes.

Editor's lens (per architecture §E):

1. **Clarity of the two-register distinction.** v7.0.5 introduces two registers — Funder Intelligence Database (workspace-shared, per-funder factual) and Match Database (per-org, per-client matching reasoning). Are these distinguishable on a single read-through? Could a builder confuse which register holds what? Are the lifecycle differences (Funder Intel = additive corpus growth + quarterly curation; Match DB = per-cycle proposal-to-outcome trail) clearly separated?
2. **Operator usability of curation cadence.** §6 binds Funder Intel curation to the Archivist v1.x slot but says v0.1 is operator-owned with "quarterly suggested cadence." Is that operationally specific enough? When does the operator get the curation prompt — at Tilth wake-up? On a Tilth cron? Does the amendment need to specify this or is it explicitly punted to companion §5?
3. **Schema readability.** §1 (Funder Intelligence Database register.yaml) and §2 (Match Database register.yaml) are illustrative YAML. Are they labeled as illustrative or are they implied final? Are field names consistent with v7.0.4 KFR conventions (e.g., `populated_at`, `populated_by`, `audit_chain`)?
4. **Stage-5 framing.** §4 introduces consent tiers and explicitly defers commons-side architecture. Is the v0.1-vs-Stage-5 boundary crisp, or does a reader feel pulled toward thinking commons exists today?
5. **Cross-amendment composition.** v7.0.5 composes against v7.0.4 (KFR) and v7.0.7 (classification). Is the composition narrative in §7 readable — does a builder know where KFR ends and Funder Intel begins?

## Output format

Per the existing pattern (see `pipeline/validation/section_1_amendment_m7_wire_2026-04-17/audit_v1_editor.md`):

- 4-8 findings as `### FINDING E-NN — Title` blocks.
- Per finding: **Where** (§N.M / line cue), **Severity** (HIGH / MEDIUM / LOW), **Issue** (what's wrong), **Why it matters** (impact on builder/operator), **Suggested fixes** ((a) / (b) / (c) ranked options).
- Final paragraph: **Verdict** — one of READY_TO_LOCK / REQUIRES_FIX / BLOCKING. State briefly why.

Budget: ≤ 1000 output tokens. Be specific — cite section numbers and the exact phrase you flagged. No vibes.

Begin.
