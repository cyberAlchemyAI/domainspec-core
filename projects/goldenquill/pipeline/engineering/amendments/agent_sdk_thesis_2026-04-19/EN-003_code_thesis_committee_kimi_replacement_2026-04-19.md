# EN-003 — Code Thesis Committee: Replace Kimi K2 with Gemini 2.5 Pro

**Amendment ID:** EN-003
**Date:** 2026-04-19
**Type:** Architecture amendment — A2 Block 2 (Code Thesis Committee composition)
**Status:** `LOCKED-sealed` (policy-lock 2026-04-20; see "Operator Sign-off" section below)
**Authority:** lessons.md L-009 (catalog-vs-tier discipline); Groq deprecation notice 2026-03-23; OpenClaw cross-family remediation 2026-04-19

---

## Scope

Replace Kimi K2 (Moonshot family) with Gemini 2.5 Pro (Google family) in the Code Thesis Committee's five-reviewer composition defined by A2 Block 2 of `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v7 LOCKED 2026-04-19).

## Why

1. **Kimi K2 is globally deprecated by Groq as of 2026-03-23.** Groq's deprecation notice replaces `moonshotai/kimi-k2-instruct-0905` with `openai/gpt-oss-120b`. The earlier `moonshotai/kimi-k2-instruct` was already deprecated 2025-09-10. Both variants return 404 from Josh's Groq Dev tier and from any Groq tier going forward. The A2 Block 2 spec references a model that no longer exists at the only provider it was ever hosted on.
2. **Committee cannot run as spec'd.** With one of five reviewer slots unfillable, the "5 distinct families, all-pass merge" rigor defined by A2 Block 2 is structurally broken until a replacement lands.
3. **Gemini 2.5 Pro is the cleanest swap.** Google family preserves the "5 distinct families" invariant. Josh's Google plugin was enabled 2026-04-19 (same session as this amendment); Gemini 2.5 Pro tested end-to-end via OpenClaw with clean output. Strong reasoning + 1M context matches the committee's code-review-rigor requirements.

## Change

**Before (A2 Block 2, LOCKED 2026-04-18):**

> Code Thesis Committee = author (Claude Code) + 5 cross-family reviewers: Codex (OpenAI), Qwen 3 32B (Alibaba), Llama 3.3 70B (Meta), GPT-OSS 120B (OpenAI-OSS), **Kimi K2 (Moonshot)**. all_pass merge; 1 retry cap.

**After (EN-003, this amendment):**

> Code Thesis Committee = author (Claude Code) + 5 cross-family reviewers: Codex (OpenAI), Qwen 3 32B (Alibaba), Llama 3.3 70B (Meta), GPT-OSS 120B (OpenAI-OSS), **Gemini 2.5 Pro (Google)**. all_pass merge; 1 retry cap.

## Family composition analysis

| Reviewer | Family | Status after EN-003 |
|----------|--------|---------------------|
| Codex | OpenAI | unchanged |
| Qwen 3 32B | Alibaba | unchanged |
| Llama 3.3 70B | Meta | unchanged |
| GPT-OSS 120B | OpenAI-OSS | unchanged |
| ~~Kimi K2~~ → Gemini 2.5 Pro | ~~Moonshot~~ → **Google** | replaced |

Five distinct families preserved. Author (Anthropic) remains non-overlapping with every reviewer family. No reviewer family duplicates another reviewer's family.

**Family taxonomy note (per v7 A2):** the seven-family taxonomy is Anthropic, OpenAI, OpenAI-OSS, Alibaba, Meta, Moonshot, Google. EN-003 replaces the Moonshot slot with Google. The taxonomy itself (seven families total) does not change; the committee occupies five of seven slots. Moonshot becomes available-but-unused rather than committee-used.

## Voices in the back of the head (per Da Vinci §3, post-EN-003)

- *Codex (OpenAI):* unchanged
- *Qwen (Alibaba, Groq-hosted):* unchanged
- *Llama (Meta):* unchanged
- *GPT-OSS (OpenAI-OSS, Groq-hosted):* unchanged
- ~~*Kimi (Moonshot, Groq-hosted):*~~ → *Gemini 2.5 Pro (Google):* "State the invariant explicitly. In code. Not prose. Cite the cross-document contract before you claim the contract holds."

The stylistic prompt for the fifth voice is carried forward verbatim from Kimi's in Da Vinci §3 — it was the right discipline even when the model changed. Update `pipeline/engineering/da_vinci_engineer_prompt_v2.md` §3 to reflect the new backer.

## Operational changes required

1. **`pipeline/engineering/da_vinci_engineer_prompt_v2.md` §3.** Replace the Kimi voice line with Gemini 2.5 Pro.
2. **`pipeline/engineering/engineering_process_v0.1.md` §3.** Replace references to Kimi K2 reviewer with Gemini 2.5 Pro. Verify the Code Thesis Committee invocation script references `google/gemini-2.5-pro` (not `moonshotai/kimi-k2-*`).
3. **`pipeline/architecture/v0.1/tilth_architecture_locked.md` A2 Block 2.** Record EN-003 as an amendment-on-top, preserving the v7 LOCK bar (v7 A1-A12 stays sealed at 2026-04-19; EN-003 is an amendment that requires its own LOCK flow).
4. **`~/.openclaw/openclaw.json` allowlist.** Already updated to include `google/gemini-2.5-pro` (done 2026-04-19). No config action needed.
5. **`router.yaml`.** `google/gemini-2.5-pro` already installed as Judge primary; does double-duty as the Committee reviewer. No additional binding change.

## Cross-family rigor check (L-003)

- Author family for Code Thesis Committee: **Anthropic** (Claude Code is the code author).
- Five reviewer families post-EN-003: OpenAI, Alibaba, Meta, OpenAI-OSS, Google.
- Reviewer ≠ author family: **all five satisfy**.
- Reviewer ≠ each other: **all five satisfy** (no duplicate families among reviewers).
- L-003 cross-family rigor: **preserved.**

## Thesis path

This amendment modifies LOCKED architecture (A2 Block 2). Per L-005, requires:

1. **Cycle 1 simulated + Cycle 2 simulated** Thesis (this document is the artifact; operator signs off on the simulated pass).
2. **Live cross-family re-audit via OpenClaw** per the post-remediation CLI shape. Use the existing handoff template (`pipeline/engineering/handoffs/openclaw_cross_family_audit_agent_sdk_2026-04-19.md`) with input files being (a) this EN-003 amendment file, (b) the lessons.md L-009 entry, (c) the Groq deprecation notice excerpt.
3. **Operator sign-off** to promote `LOCKED-internal-simulated` → `LOCKED-sealed`.

**Reviewers for live audit:**
- Editor: `groq/llama-3.3-70b-versatile` (Meta family — distinct from this amendment's author)
- Judge: `google/gemini-2.5-pro` (Google family — **NOTE: Gemini reviewing Gemini inclusion is a mild self-reference; acceptable for this narrow swap since the decision is operationally forced by Kimi deprecation, not aesthetic**). If self-reference concern arises, delegate Judge to `groq/qwen/qwen3-32b` (fallback, Alibaba family).
- Red Team: `groq/openai/gpt-oss-120b` (OpenAI-OSS family — distinct)

## Rejected alternatives

- **Leave the slot empty.** Committee runs with 4 reviewers instead of 5. Rejected: violates A2 Block 2's "5 distinct families" rigor.
- **DeepSeek R1 Distill (Groq) as the Moonshot substitute.** Not available on Josh's tier; schema-rejected in OpenClaw's Groq plugin. Also DeepSeek is an 8th family outside the seven-family taxonomy — adopting it would require taxonomy amendment.
- **Add Bedrock + pull DeepSeek R1 from there.** Requires AWS credentials which Josh doesn't have in `.env`. Out of scope.
- **Revisit Moonshot via a different provider (Moonshot API direct).** Requires a new provider integration, new API key, new BYOK discipline. Expensive for a single-reviewer slot.

## Rollback

If EN-003 proves problematic:
1. Revert `router.yaml` Judge primary to `groq/qwen/qwen3-32b` (the pre-EN-003 working state — hardened prompt template still applies).
2. Revert engineering-process + Da Vinci v2 §3 references.
3. Remove Gemini 2.5 Pro from `openclaw.json` allowlist (Python patch).
4. File a new amendment naming the replacement for the Moonshot slot.

Rollback does NOT restore Kimi — Kimi is gone from Groq globally.

## Sign-off

- Cycle 1 simulated verdict: PASS — the change is forced by external deprecation, not discretionary; trade-offs are documented; rollback is clean.
- Cycle 2 simulated verdict: READY.
- Operator signature required for `LOCKED-internal`.
- Live cross-family audit via OpenClaw required for `LOCKED-sealed`.

---

## Cycle 2 Fixes — Applied 2026-04-20 (addresses live cross-family audit findings)

The live cross-family audit at `en003_cross_family_audit/` surfaced 2 HIGH + 4 MED + 1 self-reference-bias concern. Fixes F-1 through F-7 below resolve each finding inline within this amendment.

### F-1 — Forced-replacement rigor note (addresses RT-NEW-01 HIGH)

**Adds to the "Why" section:** *Forced-replacement rule — deprecation is sufficient cause for substitution of a provider slot, but does NOT exempt the replacement from full L-005 cross-family Thesis review. The live cross-family audit at `en003_cross_family_audit/` constitutes that review. The deprecation event triggered the amendment; it did not pre-approve the replacement. This rule generalizes: every future "forced by deprecation" amendment carries the same obligation.*

### F-2 — Schema verification gate (addresses RT-NEW-05 HIGH)

**Adds to the "Operational changes required" list as item (6):** *Schema compatibility verification — before the first live Code Thesis Committee run that includes Gemini 2.5 Pro, Gemini must receive a representative code-review prompt from the Committee's archived suite and return a response that parses cleanly into the expected SFR three-block + verdict structure. Result logged at `pipeline/engineering/en003_gemini_schema_check_<date>.md`. Gate: schema check PASS is a precondition for LOCKED-sealed promotion to production use. Schema FAIL triggers an engineering follow-up, not a bypass.*

### F-3 — Voice-line scope (addresses RT-NEW-02 MED)

**Adds to the "Operational changes required" item (1):** *Kimi's Moonshot voice contract ("state the invariant explicitly, in code, not prose") is NOT assumed to transfer to Gemini. The Gemini voice line in Da Vinci v2 §3 receives a neutral Committee-reviewer characterization. If a code-invariant-specialist voice is needed, that is a separate amendment — not this one.*

### F-4 — Mandatory Qwen fallback for self-reference audits (addresses RT-NEW-03 MED + Judge self-reference bias)

**Replaces the self-reference note with:** *Self-reference mandatory fallback rule — any amendment that adds the active Judge's model family to a governed committee requires automatic reassignment of the Judge seat to the non-self-referencing fallback (`groq/qwen/qwen3-32b` per router.yaml) for that specific amendment's audit. This is not optional. For EN-003 LOCKED-sealed promotion, Qwen 3 32B must independently re-score the amendment. The initial Gemini Judge verdict of 100/100 (self-assessed as low-bias) is retained as a data point but is NOT the sole scoring authority for this amendment.*

### F-5 — Vendor lock-in register (addresses RT-NEW-04 MED)

**Adds to the "Operational changes required" list as item (7):** *adopted_tools_register.md entry — Gemini 2.5 Pro is logged as a Google-family dependency with vendor-lock-in risk tier MEDIUM (single Google-family dependency). Mitigation: quarterly audit checkpoint for Google API stability + pre-authorized fallback reviewer slot (Qwen 3 32B already in Committee serves as the same-slot fallback if Google deprecates Gemini 2.5 Pro).*

### F-6 — Future-deprecation contingency (addresses RT-NEW-06 MED)

**Adds to the "Rollback" section:** *Future deprecation contingency — if Google deprecates Gemini 2.5 Pro, this amendment triggers a new replacement Thesis under TSIP Phase 1 (SURVEILLANCE) and Phase 5 (Thesis). Pre-authorized fallback reviewer slot: Qwen 3 32B (already present as Judge fallback). No architectural gap during transition — the Committee degrades to 4-family all-pass review until the replacement Thesis completes, rather than pausing all code work.*

### F-7 — Editor copy edits

Tone normalized to present-tense declarative throughout; passive voice eliminated in the family-composition section; "Josh's Google plugin" → "the Google plugin" for voice consistency.

## Cycle 2 status

All 2 HIGH findings CLOSED with procedural additions (F-1 adds rule; F-2 adds gate).
All 4 MED findings CLOSED (F-3, F-4, F-5, F-6).
Judge self-reference CLOSED via F-4 (Qwen rescore required).
Editor findings CLOSED via F-7 (applied in place).

**EN-003 Cycle 2 status: REQUIRES_QWEN_RESCORE** before `LOCKED-sealed`. Once Qwen 3 32B independently re-scores this amended version, and the schema verification gate (F-2) passes, the amendment is ready for operator signature → `LOCKED-sealed`.

---

## Cycle 3 Fixes — Applied 2026-04-20 (close remaining policy-level gaps from Cycle 2 Red Team)

Cycle 2 Qwen Judge (non-self-referencing per F-4) returned 96/100 REQUIRES_MINOR_FIXES blocking:false. Cycle 2 Red Team returned REQUIRES_MINOR_FIXES **blocking:true** on 3 OPEN-policy findings. F-1-Cycle3, F-4-Cycle3, F-6-Cycle3 below close the three blockers.

### F-1-Cycle3 — Name the enforcement gate for the forced-replacement rigor rule (closes RT-NEW-01 HIGH OPEN)

**Replaces F-1:** *Forced-replacement rule with named enforcement gate. Deprecation is sufficient cause for provider-slot substitution but does NOT exempt the replacement from full L-005 cross-family Thesis review. Enforced by Logician PRE-gate `F-DEPRECATION-EXEMPTION-REUSE` (queued for v0.2, gate spec: verifies two fields on any amendment that sets `amendment.forced_replacement: true` — (a) the live cross-family audit artifact exists at a canonical path, (b) the audit artifact's final Red Team verdict is blocking:false OR carries an explicit Cycle N fix addressing each blocking finding). Amendments missing either field fail the gate and cannot promote to LOCKED-sealed. The rule generalizes: every future "forced by deprecation" amendment carries this obligation.*

### F-4-Cycle3 — Define trigger criteria for self-reference Judge fallback (closes RT-NEW-03 MED OPEN)

**Extends F-4:** *Self-reference Judge-fallback trigger criteria — the mandatory Qwen reassignment fires when an amendment satisfies all three conditions: (a) MODIFIES the Code Thesis Committee composition (adds, removes, or swaps a reviewer slot); AND (b) the added or swapped-in model's family matches the current Judge primary's family per router.yaml; AND (c) the amendment author is not already Judge's family. Trigger detection is Logician PRE-gate `F-AMENDMENT-SELF-REFERENCE-DETECT` (queued for v0.2, gate spec: reads the amendment metadata for a `modifies_committee: true` flag + compares added-reviewer family against router.yaml Judge primary family). False-negatives (amendments with subtle wording that evade detection) are tracked in lessons.md as recurring-pattern candidates for gate refinement. The gate fail-closes on ambiguity.*

### F-6-Cycle3 — Max-duration on 4-family Committee degradation (closes RT-NEW-06 MED OPEN)

**Extends F-6:** *Degradation time bound — the temporary 4-family Committee degradation during a deprecation-triggered replacement Thesis is capped at 30 calendar days from LOCKED-sealed of the deprecation amendment. If the replacement Thesis has not completed within 30 days, the Committee enters SUSPENDED state: no code-review LOCKs may promote, engineering queue backs up, operator escalation mandatory. Max suspended period: 30 additional days (60 calendar days total from original LOCK). At 60 days without replacement LOCK-sealed, operator triggers fresh architectural Thesis rather than continue piecemeal. Tracked via Logician PRE-gate `F-COMMITTEE-DEGRADATION-TIMEOUT` (queued for v0.2, gate spec: reads `deprecation_amendment.locked_at_iso8601` + current time; emits warning at 14 days, blocks new code LOCKs at 30 days, escalates mandatory at 60 days).*

### F-7-Cycle3 — LOW severity single-fallback defense-in-depth (closes Red Team NEW finding)

**Adds to the "Operational changes required" list as item (8):** *Fallback defense-in-depth — the Qwen 3 32B self-reference fallback is the primary non-Google independent scorer. Pre-authorize a secondary fallback (Llama 3.3 70B when not already serving the Editor seat in the same round) so that loss of Qwen access does not leave the self-reference rule un-enforceable. Secondary-fallback activation criteria + routing added to router.yaml with a dated commentary note.*

## Cycle 3 status

All three Cycle 2 Red Team OPEN-policy findings CLOSED with named Logician gates + concrete policy logic:
- RT-NEW-01 HIGH: CLOSED via F-1-Cycle3 + `F-DEPRECATION-EXEMPTION-REUSE`.
- RT-NEW-03 MED: CLOSED via F-4-Cycle3 + `F-AMENDMENT-SELF-REFERENCE-DETECT`.
- RT-NEW-06 MED: CLOSED via F-6-Cycle3 + `F-COMMITTEE-DEGRADATION-TIMEOUT`.
- LOW new-finding: CLOSED via F-7-Cycle3 (secondary fallback pre-authorized).

Three additional Logician v0.2 gates added to the engineering queue:
- `F-DEPRECATION-EXEMPTION-REUSE`
- `F-AMENDMENT-SELF-REFERENCE-DETECT`
- `F-COMMITTEE-DEGRADATION-TIMEOUT`

**EN-003 Cycle 3 status: READY for final Red Team re-audit.** Editor + Qwen Judge already READY in Cycle 2. Only a Red Team pass is needed to confirm the three blockers close. If Red Team returns blocking:false, EN-003 promotes `LOCKED-internal-simulated` → `LOCKED-sealed` pending operator signature.

---

## Cycle 3 Red Team Re-Audit Result — 2026-04-20

**Verdict:** REQUIRES_MINOR_FIXES, **blocking: false.** All three Cycle 2 OPEN-policy blockers CLOSED (RT-NEW-01 HIGH via F-1-Cycle3 + `F-DEPRECATION-EXEMPTION-REUSE`; RT-NEW-03 MED via F-4-Cycle3 + `F-AMENDMENT-SELF-REFERENCE-DETECT`; RT-NEW-06 MED via F-6-Cycle3 + `F-COMMITTEE-DEGRADATION-TIMEOUT`). Three new MED findings surfaced (marker-field evasion risk, router.yaml integrity dependency, escalation-authority underspecified) + 1 LOW (fallback-chain self-reference risk). All four are policy-consistency refinements tracked as engineering-queue items — none block LOCK.
**Audit trail:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit_cycle3/red_team_verdict.md`

## Operator Sign-off — LOCKED-sealed 2026-04-20

**Status:** `LOCKED-sealed`
**Interpretation adopted:** policy-lock.
**Cycle 2 + Cycle 3 re-audit outcomes:** Editor READY (Cycle 2), Qwen Judge 96/100 REQUIRES_MINOR_FIXES blocking:false (Cycle 2, non-self-referencing per F-4), Red Team blocking:false (Cycle 3 after F-1/F-4/F-6/F-7 Cycle3 fixes named enforcement gates).
**F-4 vindication:** Gemini's Cycle 1 self-score of 100/100 replaced by Qwen's 96/100 independent score. Qwen caught a rollback-gap refinement Gemini missed. Self-reference protection worked as architecturally specified.
**Audit trail:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit_cycle2/` + `/en003_cross_family_audit_cycle3/`
**Operator authorization token:** Josh Inklovich, session authorization 2026-04-20.
**Cryptographic seal (Ed25519):** pending v2.2 gates #5/#10 infrastructure; hash-bound record at `pipeline/engineering/operator_authorization_ledger.v1.jsonl`. `LOCKED-sealed` reflects policy-lock, not cryptographic seal.
**Engineering-queue items absorbed:** `F-DEPRECATION-EXEMPTION-REUSE`, `F-AMENDMENT-SELF-REFERENCE-DETECT`, `F-COMMITTEE-DEGRADATION-TIMEOUT` (Logician v0.2 queue, assigned to Code session).
**Effective:** LOCKED-sealed 2026-04-20. Code Thesis Committee fifth reviewer slot is now Gemini 2.5 Pro (Google family). Kimi K2 slot is retired. Five distinct families preserved (Anthropic author + 5 reviewers: OpenAI/Alibaba/Meta/OpenAI-OSS/Google).

---

## Cycle 4 Fixes — Applied 2026-04-20 (in-amendment closure of Cycle 3 RT engineering-queue findings)

**Scope note.** EN-003 remains LOCKED-sealed 2026-04-20 under policy-lock. Cycle 4 does NOT reopen the LOCK; it folds the four non-blocking findings surfaced by the Cycle 3 Red Team re-audit (marker-field evasion risk, router.yaml integrity dependency, escalation-authority underspecified, fallback-chain self-reference risk) from engineering-queue-only closure into text-level policy closure inside this amendment. The Logician v2.2 spec-cards at `pipeline/engineering/spec_cards/logician_v2_2_*.md` carry the structural enforcement. Cycle 4 adds the policy contract those gates enforce.

### F-1-Cycle4 — Mandatory `amendment.forced_replacement` schema enforcement (closes Cycle 3 RT new-finding MED: marker-field evasion risk)

**Extends F-1-Cycle3:** *Marker-field evasion is closed at two layers, not one.*

**Layer 1 (structural schema).** Every amendment file under `pipeline/engineering/amendments/**` carries a YAML frontmatter block with a mandatory `amendment.forced_replacement: true|false` field. Amendments lacking the field fail closed at Logician PRE-gate `F-DEPRECATION-EXEMPTION-REUSE` schema validation, BEFORE policy evaluation. No `forced_replacement` key → DENY with `F-AMDT-06-SCHEMA-MISSING`. The spec card at `pipeline/engineering/spec_cards/logician_v2_2_f_deprecation_exemption_reuse.md` is updated to add a schema pre-check as gate step 0.

**Layer 2 (semantic cross-reference).** An amendment that sets `amendment.forced_replacement: false` but whose diff touches a provider slot listed in the deprecation register at `pipeline/engineering/deprecation_register.jsonl` is treated as if `forced_replacement: true` — the gate re-enters the full Cycle N evidence chain check. This closes the "author forgets or omits" evasion path the Cycle 3 RT identified. The deprecation register is appended whenever a provider publishes a deprecation notice that affects a slot Tilth references (Groq Kimi K2 removal 2026-03-23 is the seed entry).

### F-4-Cycle4 — Router.yaml integrity cross-reference (closes Cycle 3 RT new-finding MED: router.yaml integrity dependency)

**Extends F-4-Cycle3:** *`F-AMENDMENT-SELF-REFERENCE-DETECT` does not trust `router.yaml` contents without an integrity check.*

**Mechanism.** Before the gate reads the `judge_primary_family` field, it calls `router_integrity.verify(router_yaml_path)` (module queued at `pipeline/linting/router_integrity.py` — Round H of the Logician v2.2 wave, tracked as a new spec-card dependency `logician_v2_2_router_integrity.md`). The verifier computes a SHA3-512 digest of `router.yaml` and compares against the pinned digest in `pipeline/engineering/router_integrity.pinned.json`, which is rotated whenever an authorized router edit lands (ritual: edit `router.yaml` → re-pin digest in the same commit → commit message references both files). Integrity mismatch → DENY with `F-AMDT-07-ROUTER-INTEGRITY-MISMATCH`. Missing pin file → DENY with `F-AMDT-07-ROUTER-INTEGRITY-MISSING`. `F-COMMITTEE-DEGRADATION-TIMEOUT` gate #8 adopts the same verify call for its `locked_at_iso8601` read path. Cross-reference added to both spec cards.

**Trust boundary.** The pinned-digest file itself lives under the sovereignty envelope (§1 Vault). The pin rotation is operator-acknowledged, not silent; a pin rotation that happens without an accompanying `router.yaml` content change fails the envelope's pair-commit rule and is rejected at the source-control layer (convention-level this round; AST-lint R8 `ROUTER_PIN_PAIR_COMMIT` tracked as future ARCH round).

### F-6-Cycle4 — Escalation-authority definition (closes Cycle 3 RT new-finding MED: escalation-authority underspecified)

**Extends F-6-Cycle3:** *"Mandatory operator escalation" is defined — who acts, how, on what channel, and the consequence of inaction.*

**Notification channel.** At the 30-day SUSPEND threshold, `F-COMMITTEE-DEGRADATION-TIMEOUT` gate #8 writes `event: "F-AMDT-08-SUSPEND"` to `pipeline/metrics/session_log.jsonl` AND appends a mandatory acknowledgment stanza to `daily_logs/YYYY-MM-DD.md` with the literal header `## F-AMDT-08-SUSPEND — Committee degradation 30-day threshold`. The Cowork session prompt surface renders the stanza as a blocking banner on next orientation until the operator writes a response entry beneath it.

**Required sign-off.** Operator response must contain one of three literal strings (exact byte match, gate re-reads the log on every run): (a) `TARGET_DATE: YYYY-MM-DD` committing to a replacement Thesis completion date ≤ 60 days from original LOCK; (b) `IMMEDIATE_DISPATCH` with an accompanying Midas handoff path pointing to a new replacement-Thesis spec card; (c) `FRESH_ARCHITECTURAL_THESIS` triggering the full L-005 flow. Any other response string is ignored; the banner stays.

**Cannot be silently extended.** The 60-day total ceiling is hard. No operator response string extends beyond 60 days. At day 60, `F-AMDT-08-ESCALATE` fires regardless of prior `TARGET_DATE` commitments; a missed target-date is itself a separate escalation event logged `event: "F-AMDT-08-TARGET-DATE-MISSED"`. Any amendment proposing to extend the 60-day ceiling is itself subject to full L-005 cross-family Thesis and cannot carry `forced_replacement: true` (closes the recursive-bypass path).

**Inaction consequence.** Seven calendar days after `F-AMDT-08-ESCALATE` fires without a valid operator response, the pipeline enters READ-ONLY mode: no new LOCKs of any kind may promote (not EN-series, not TSIP, not §4/§5 build rounds, not narrow-edit). Read-only is enforced by `F-AMDT-08-READONLY` as a global PRE-gate on every LOCK path. Exit from READ-ONLY requires a fresh architectural Thesis sign-off — not a narrow-edit.

### F-7-Cycle4 — Secondary-fallback collision check (closes Cycle 3 RT new-finding LOW: fallback-chain self-reference risk)

**Extends F-7-Cycle3:** *The self-reference fallback chain is three layers deep, never two, and carries an anti-collision invariant.*

**Tertiary fallback authorized.** When an amendment triggers `F-AMENDMENT-SELF-REFERENCE-DETECT` AND the current Qwen 3 32B primary fallback matches the amendment's added-reviewer family (Alibaba), AND the current Llama 3.3 70B secondary fallback matches the added-reviewer family (Meta), the tertiary fallback is **Codex (OpenAI direct, `openai/gpt-4o` per router.yaml `code_reviewer_1.fallback`)**. Tertiary activation writes `event: "F-AMDT-07-TERTIARY-FALLBACK-ACTIVATED"` with the family-collision reason to `pipeline/metrics/session_log.jsonl`.

**Anti-collision invariant.** No two layers of the self-reference fallback chain (primary fallback / secondary fallback / tertiary fallback) may share a model family. Enforced at `F-AMENDMENT-SELF-REFERENCE-DETECT` PRE-gate time by walking the chain from router.yaml at gate invocation (not at amendment commit time — catches drift). Chain-collision → DENY with `F-AMDT-07-FALLBACK-CHAIN-COLLISION`; the amendment cannot promote until router.yaml is updated to restore family distinctness across the chain.

**Quarterly audit checkpoint.** On the first of every calendar quarter (2026-04-01, 2026-07-01, 2026-10-01, 2027-01-01, …), the Logician emits `event: "F-AMDT-07-FALLBACK-CHAIN-AUDIT"` summarizing the current three-layer chain families and any near-collision risks (e.g., two layers hosted on the same provider but in different families — Groq-Alibaba vs Groq-Meta is a provider-single-point-of-failure risk that does not collide on family but bears recording). The audit entry is operator-read at next session orientation, not a blocking gate.

### Cycle 4 status

All four Cycle 3 RT engineering-queue findings CLOSED at text-level policy inside this amendment:
- Cycle 3 RT MED (marker-field evasion): CLOSED via F-1-Cycle4 (two-layer schema + deprecation-register cross-ref).
- Cycle 3 RT MED (router.yaml integrity dependency): CLOSED via F-4-Cycle4 (`router_integrity.verify` call + pinned-digest rotation ritual).
- Cycle 3 RT MED (escalation-authority underspecified): CLOSED via F-6-Cycle4 (notification channel, sign-off strings, 60-day hard ceiling, READ-ONLY inaction consequence).
- Cycle 3 RT LOW (fallback-chain self-reference risk): CLOSED via F-7-Cycle4 (Codex tertiary, anti-collision invariant, quarterly audit checkpoint).

Three new Logician v2.2 spec-card dependencies added to the engineering queue (do not block this amendment; block v2.2 milestone LOCK):
- `logician_v2_2_router_integrity.md` (Round H prerequisite — `router_integrity.verify` module)
- Update to `logician_v2_2_f_deprecation_exemption_reuse.md` (schema-pre-check step 0 + deprecation-register read)
- Update to `logician_v2_2_f_amendment_self_reference_detect.md` (router-integrity call + three-layer chain walk + anti-collision invariant)

**EN-003 Cycle 4 status:** READY for Red Team re-audit to confirm closure. No blocking verdict expected; audit confirms the text-level closures cover the policy surface the Cycle 3 RT flagged. LOCKED-sealed status does not change regardless of Cycle 4 verdict (this is a tightening pass); a blocking Cycle 4 verdict would surface a gap the Cycle 3 closure missed, which would then trigger a Cycle 5 text-only fix — not a LOCK reopen.

---

## Cycle 4 Red Team Re-Audit Result — 2026-04-20

**Verdict:** `REQUIRES_MINOR_FIXES`, **blocking: true** (on the evolved form of RT-NEW-01).
**Model:** `groq/openai/gpt-oss-120b` (OpenAI-OSS family, cross-family vs Anthropic author / Google Judge / Meta Editor / Alibaba reviewer pool).
**Dispatched:** 2026-04-20T22:21:39Z.
**Audit trail:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit_cycle4/red_team_verdict.md`.

**Closure summary per Cycle 3 RT finding:**

| Cycle 3 RT finding | Cycle 4 closure claim | Cycle 4 RT status | New surface (MED) |
|---------------------|------------------------|----------------------|---------------------|
| RT-NEW-01 HIGH — marker-field evasion | F-1-Cycle4 two-layer (schema + semantic) | OPEN-policy (partial) | **C4-NEW-01** Deprecation-register lag window: if `deprecation_register.jsonl` is not atomically updated with upstream provider deprecation notices, an author can set `forced_replacement:false` on a freshly-deprecated slot and evade Layer 2. |
| RT-NEW-02 MED — router.yaml integrity | F-4-Cycle4 SHA3-512 pinned-digest | OPEN-policy (partial) | **C4-NEW-02** Same-commit pair tampering: attacker with write to both `router.yaml` and `router_integrity.pinned.json` in one commit satisfies pair rule with evil content. |
| RT-NEW-03 MED — escalation authority | F-6-Cycle4 sign-off strings + 60-day ceiling + READ-ONLY | OPEN-policy (partial) | **C4-NEW-03** (a) Precedence ambiguity when operator writes both `TARGET_DATE:` and `FRESH_ARCHITECTURAL_THESIS`; (b) READ-ONLY deadlock — exit requires fresh architectural Thesis, which requires a LOCK, which READ-ONLY blocks. |
| RT-NEW-04 LOW — fallback-chain self-reference | F-7-Cycle4 tertiary Codex + anti-collision | CLOSED-policy (layers), OPEN on author | **C4-NEW-04** Author-family omitted from anti-collision invariant: if amendment author is OpenAI-direct, tertiary Codex collides with author without gate firing. |

**Per-finding engineering rationale (why C4 blocks despite LOCK-sealed status):**

- **C4-NEW-01** is an evolution, not a closure, of RT-NEW-01 HIGH. The Red Team's judgment is correct: the Layer-2 semantic check is only as strong as the register's freshness, and "register is stale for 48 hours after a Groq deprecation" is a realistic failure mode given Groq's 2026-03-23 Kimi K2 deprecation was the seed event — the register currently has one entry for that event but no ingest automation. Cycle 5 must close this loop.
- **C4-NEW-02** is a real trust-boundary gap: the pair-commit rule treats the two files as mutually-authenticating but they share the same write authority. Cycle 5 needs an external integrity anchor (signed append-only audit log with a key outside the workspace, or a two-operator sign-off for pin rotation).
- **C4-NEW-03** is two separate issues in one finding. Precedence ambiguity is solvable via explicit ordering (`FRESH_ARCHITECTURAL_THESIS` always wins when both present). The deadlock is architecturally more serious: READ-ONLY mode is supposed to be the terminal safety floor, but it cannot self-exit. Cycle 5 must carve a narrow READ-ONLY exit lane: the fresh architectural Thesis LOCK is exempt from the global PRE-gate via a named bootstrap exemption analogous to TSIP F-1, logged at `event: "F-AMDT-08-READONLY-EXIT-BOOTSTRAP"` and capped at ONE firing per READ-ONLY entry.
- **C4-NEW-04** is a straightforward extension: the anti-collision invariant must also check `amendment.author_family` against all three fallback layers, not just the three layers against each other.

**Does Cycle 4 reopen LOCKED-sealed status?** No. Per the Cycle 4 scope note, LOCKED-sealed stands regardless of this verdict — the amendment's fifth-reviewer substitution (Kimi K2 → Gemini 2.5 Pro) is unaffected by these policy-surface findings. The Cycle 3 RT engineering-queue findings are now Cycle 4 RT engineering-queue findings at the next fidelity level; the policy work continues in a Cycle 5 text-fix pass OR via the Logician v2.2 spec-card queue.

**Cycle 4 status:** BLOCKING at policy-fix level; NOT BLOCKING at LOCK-sealed level. Operator decision required before Cycle 5 dispatches:

1. **Cycle 5 text-fix pass.** Close the 4 C4-NEW findings inline in this amendment (analogous to Cycle 3 → Cycle 4). Re-dispatch Red Team. Risk: evolution spiral — each closure risks surfacing a sub-finding, and we're past the L-005 two-audit ceiling (though the LOCK is sealed, so L-005's "escalate at ceiling" fires as a tripwire, not a gate).
2. **Park to Logician v2.2 queue.** Transfer the 4 C4-NEW findings to the spec-cards at `pipeline/engineering/spec_cards/logician_v2_2_*.md` (new sub-card for deprecation-register ingest automation, update to router-integrity for external anchor, update to gate #8 for READ-ONLY exit bootstrap, update to gate #7 for author-family invariant). Accept that the text-level closure hit a ceiling and the remaining work is structural, not textual.
3. **Escalate to fresh architectural Thesis round.** The READ-ONLY deadlock in particular is architecturally load-bearing; the Red Team's catch is real and may deserve a full L-005 round with Editor + Judge re-reviewing alongside Red Team, not just a Red Team re-audit.

Recommended: **Option 2 (park to v2.2 queue).** The four findings are implementation-layer, not policy-layer — the text-level policy has now reached the resolution ceiling, and the gates are where the structural defense lives. This is the same pattern as the Cycle 3 → LOCKED-sealed transition: Red Team finds a gap, engineering queue absorbs it, LOCK stands.

---

## Cycle 4 Disposition — 2026-04-20

**Operator decision:** Option 2 selected. Four C4-NEW findings absorbed into the Logician v2.2 spec-card queue. EN-003 LOCK-sealed status stands; no Cycle 5 text-fix pass; no fresh architectural Thesis round.

**Rationale:** Cycle 3 → Cycle 4 each generated sub-findings, confirming that text-level closure has hit the L-005 resolution ceiling. Remaining work is mechanical enforcement (gate code), not prose refinement. Option 3 (fresh architectural Thesis) was considered for C4-NEW-03's READ-ONLY deadlock, which has architectural flavor, but the deadlock resolves cleanly in gate code by distinguishing `lock_class: "architectural_thesis"` from `lock_class: "code"` in the carve-out logic of gate #11 — no fresh Thesis needed.

**Finding → spec-card mapping:**

| Cycle 4 finding | Absorbing spec card | Gate # | Failure code | Kind |
|---|---|---|---|---|
| C4-NEW-01 deprecation-register lag | `logician_v2_2_f_deprecation_register_staleness.md` | #9 | `F-AMDT-09-STALE` / `F-AMDT-09-MISSING` | New gate |
| C4-NEW-02 router pair same-commit tamper | `logician_v2_2_f_router_integrity_multi_source.md` | #10 | `F-AMDT-10-PAIR` / `-EXTERNAL` / `-SIGNATURE` / `-CHAIN-BREAK` | New gate |
| C4-NEW-03 stanza precedence + READ-ONLY deadlock | `logician_v2_2_f_degradation_stanza_precedence.md` | #11 | `F-AMDT-11-PRECEDENCE` / `-DEADLOCK-CARVEOUT-VIOLATION` | New gate (sibling to #8) |
| C4-NEW-04 author-family anti-collision gap | `logician_v2_2_f_amendment_self_reference_detect.md` v1.1 extension | #7 | `F-AMDT-07-AUTHOR-COLLISION` | Extension of existing gate |

**Master queue update:** `pipeline/engineering/spec_cards/logician_v2_2_gates.md` updated to v1.2 (count: 11 gates + #7 v1.1 extension; Cycle-4 additions section; Wave 3 expanded).

**READ-ONLY deadlock resolution (C4-NEW-03 tooth b):** gate #11 F-DEGRADATION-STANZA-PRECEDENCE introduces an explicit `lock_class` field on `lock_history.v1.jsonl` rows. Architectural-Thesis LOCKs (`lock_class: "architectural_thesis"`, operator-Ed25519-signed, targeting an architecture-file path) are exempt from code-LOCK READ-ONLY. Code-LOCKs (`lock_class: "code"` or unset) remain subject to READ-ONLY. Schema extension + backfill of existing rows (default `lock_class: "code"`) lands with gate #11 implementation. Deadlock broken in gate code; the amendment text is not modified to carve out exceptions because the exception is architectural, not prose.

**L-005 ceiling status:** Cycles 2, 3, 4 are a three-audit sequence on EN-003. L-005 caps silent revision loops at two audits. The LOCK-sealed status through Cycles 3 and 4 means L-005 fires as a *tripwire* (surface to operator for disposition) rather than a *gate* (halt). Operator disposition here — park the findings, stop cycling — is the L-005-prescribed response. A hypothetical Cycle 5 would violate L-005 without a fresh architectural round; Option 2 respects the ceiling.

**Lesson candidate (pending):** "When Red Team Cycle N generates a finding set whose complement of Cycle N-1 closures has increasing structural content (gates rather than prose), the next move is engineering queue, not Cycle N+1 text-fix." Track as a potential lessons.md entry after the v2.2 gates are implemented and the pattern proves durable across more than one amendment.

**Amendment status unchanged:** LOCKED-sealed 2026-04-20. Policy-lock semantics preserved. Kimi K2 → Gemini 2.5 Pro substitution stands. v2.2 queue now carries 11 gates covering both the Tier 1 policy surface (gates #1–#8) and the Cycle 4 structural residue (gates #9–#11 + #7 v1.1 extension).

*Cycle 4 disposition recorded 2026-04-20 by Josh Inklovich per LOCKED-sealed operator authority.*
