# TSIP v0.1 — Live Cross-Family Audit Synthesis

**Date:** 2026-04-19
**Subject:** `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1.md`
**Author family:** Anthropic (Cowork / Claude authored TSIP + simulated Thesis)
**Live reviewer families:** Meta (Llama 3.3 70B / Groq), Google (Gemini 2.5 Pro), OpenAI-OSS (GPT-OSS 120B / Groq)
**Audit trail:** this directory — editor_verdict.md, judge_verdict.md, red_team_verdict.md

## Promotion recommendation

**CYCLE-2-REQUIRED.** Same pattern as the Agent SDK audit — live cross-family found substantive findings the simulated pass missed.

## Summary

| Seat | Family | Verdict | Score |
|------|--------|---------|-------|
| Editor | Meta | READY with minor fixes suggested | n/a (A3 exempt) |
| Judge | Google | PASS | 98/100 (vs simulated 95) |
| Red Team | OpenAI-OSS | REQUIRES_MINOR_FIXES | 1 HIGH + 6 MED + 3 LOW |

Judge scored HIGHER than simulated. Red Team found substantially MORE findings than simulated. The two results aren't contradictory — Judge scores on declared dimensions against cited evidence (which TSIP does well), while Red Team attacks from unspecified adversarial angles (which TSIP has real gaps against).

## Agreement with simulated debate

- **Scope clarity:** Judge 20/20 — explicit in/out.
- **Self-consistency:** Judge 20/20 — bootstrap exception is clean.
- **Discipline alignment (L-002/L-003/L-005/Da Vinci §13/Sovereignty):** Judge 20/20 — tightly cited.
- **Enforceability via process gates:** Judge 20/20 — each phase has gates.
- **Editor voice + glossary:** flagged same kinds of jargon the simulated Editor caught (spike, real-engineer validator gate, controlled dependency). Live Editor also surfaced passive-voice issues the simulated one missed.

## Live dissent — findings the simulated audit missed

### RT-NEW-01 — HIGH — Bootstrap exception as self-referential loophole

**Finding:** The bootstrap exception ("protocol authored before protocol exists → simulated Thesis + operator sign → LOCKED-internal") creates a reusable escape hatch. Any future amendment could claim "authored before the amended protocol existed" and bypass the live cross-family audit.

**Mitigation:** Hard rule enforced by Logician — bootstrap exceptions may be used exactly once (the TSIP bootstrap itself), recorded in an immutable ledger. Any subsequent claim of "bootstrap exception" is a POST-gate fail requiring fresh cross-family audit.

### RT-NEW-02 — MED — Reviewer-family assignment is gameable

**Finding:** Phase 5 says "reviewer family ≠ author family" but doesn't define the assignment process. The author could pick a cooperative reviewer from an eligible family. L-003 gets satisfied on paper without the adversarial rigor it's meant to enforce.

**Mitigation:** Independent reviewer assignment — either a Logician-driven random-from-pool mechanism, OR an operator-signed reviewer-selection log that makes the selection auditable.

### RT-NEW-03 — MED — Watchlist phone-home risk

**Finding:** Phase 1 SURVEILLANCE includes RSS and paper-feed channels. Fetching RSS / papers generates outbound network traffic. The amendment claims "operator-reviewed, not auto-scanned" — but even manually reviewing requires fetching, which means the URL owner knows the operator looked. This contradicts the sovereignty "no phone-home" claim for the surveillance layer.

**Mitigation:** Either (a) explicit carve-out — "watchlist fetches are network-visible to source publishers; operator accepts this as a surveillance cost," OR (b) require watchlist fetches to run through an operator-controlled sandbox or Tor-like relay. Preferred: (a) plus a sentence explicitly acknowledging the visibility tradeoff.

### RT-NEW-04 — MED — "One-week formal extension" can cascade into silent extension

**Finding:** Phase 4 says "no silent extension" but allows "one-week formal extension" with new exit criterion. The amendment doesn't cap the number of extensions. Operator can declare extension-after-extension-after-extension, effectively defeating the 2-week sanity cap.

**Mitigation:** Cap the extension count at 2 (total spike length: 2 weeks + 1 week + 1 week = 4 weeks maximum). Any third extension requires fresh Thesis, not extension.

### RT-NEW-05 — MED — "Zero blocking dissent" needs a deterministic gate

**Finding:** Phase 6 ADOPTION says LOCKED-sealed requires "zero blocking dissent" but the protocol doesn't specify HOW blocking dissent is detected. Human judgement alone invites edge-case oversight (a Red Team BLOCKING verdict could be misread as HIGH by the operator).

**Mitigation:** Logician POST-gate verifying each reviewer's signed verdict. Explicit field `blocking: true|false` in every verdict. Any `blocking: true` → automatic LOCK block until resolved.

### RT-NEW-06 — LOW — Operating audit has no fallback if Da Vinci never goes live

**Finding:** Phase 7 says "audit owner v0.1: operator alone; Da Vinci joins when live." If Da Vinci never reaches live (real-engineer validator gate never clears), Operating quarterly audit stays operator-only forever. The protocol doesn't note this as acceptable steady-state vs. temporary bootstrap.

**Mitigation:** Add a clarifying note — operator-alone audits are acceptable steady-state indefinitely; Da Vinci addition is optional enhancement not required steady-state.

### RT-NEW-07 — MED — Triage default-NO lacks appeal

**Finding:** Triage Q5 default-NO helps avoid early dismissal, but if operator does answer "confident YES" during fatigue, the candidate is rejected with no re-evaluation mechanism.

**Mitigation:** Add an "escalation" flag — any candidate rejected on Q5 gets a cooling-off period (e.g., 30 days) and a second-look trigger. Prevents operator-fatigue-one-shot-rejection.

### RT-NEW-08 — LOW — Spike manifest has no pre-approval

**Finding:** Phase 4 says manifest is "written before spike opens" but doesn't require the manifest to pass a check before the branch is created. Manifest could be incomplete or technically invalid.

**Mitigation:** Logician-approved manifest checklist as a pre-spike gate. Manifest must validate against a JSON schema before branch creation.

### RT-NEW-09 — LOW — v0.2 continuous-scan gating has no contingency

**Finding:** Phase 1's "Background scan (v0.2, not yet live)" depends on Da Vinci. If Da Vinci is permanently blocked, v0.2 continuous scan never materializes, and Tilth has no automated discovery forever.

**Mitigation:** Define a fallback — if Da Vinci doesn't reach live within 12 months, operator activates manual weekly watchlist review as minimum-viable continuous scan.

### JUDGE COMPLETENESS DOCK — v0.2 dependency lacks fallback

**Finding:** Judge docked Completeness 2/20 for the same v0.2-Da-Vinci dependency as RT-NEW-06 and RT-NEW-09. Consistent signal across reviewers.

### EDITOR READY — minor fixes suggested

Editor verdict: READY. Minor cleanup on tone consistency (present vs past tense), glossary additions (real-engineer validator gate), passive vs active voice, structural signposting for non-technical operators.

## Cycle 2 action items

1. **[HIGH]** RT-NEW-01 — hard-code bootstrap exception as single-use, Logician-recorded.
2. **[MED]** RT-NEW-02 — define reviewer-assignment mechanism (random pool OR operator-signed log).
3. **[MED]** RT-NEW-03 — sovereignty carve-out for watchlist fetches, or sandbox.
4. **[MED]** RT-NEW-04 — cap extensions at 2; third requires fresh Thesis.
5. **[MED]** RT-NEW-05 — Logician POST-gate on `blocking: true|false` verdict field.
6. **[MED]** RT-NEW-07 — cooling-off + second-look on triage Q5 rejection.
7. **[LOW]** RT-NEW-06 — clarify operator-alone audit is steady-state-acceptable.
8. **[LOW]** RT-NEW-08 — Logician manifest pre-check schema.
9. **[LOW]** RT-NEW-09 — fallback if Da Vinci doesn't reach live within 12 months.
10. **[DOCUMENTATION]** Editor tone/glossary/voice/structure cleanup.

## Meta-finding (cross-audit pattern)

Both the Agent SDK audit and this TSIP audit show the same pattern: simulated single-family Thesis declares READY; live cross-family finds 1 HIGH + 4-6 MED + 1-3 LOW findings of real substance. This is not anomalous — it's the expected shape of cross-family value. Every amendment authored by a single family voice should be treated as LOCKED-internal-simulated at best until a live cross-family pass clears it.

**Infrastructure validated:** The remediation work this session (allowlist fix, Gemini plugin enable, Judge swap to Gemini, router.yaml updates, AGENTS.md CLI shape correction) has produced a working live-cross-family audit path. That path is now the canonical L-003 enforcement layer, not ceremony.

## Post-fix re-audit path

Once Cycle 2 fixes land on TSIP v0.1:
1. Re-run this same cross-family audit via OpenClaw.
2. If all three seats READY + zero blocking: promote `LOCKED-internal-simulated` → `LOCKED-sealed`.
3. Operator signature required for LOCK-sealed.

Until then, TSIP v0.1 stays at `LOCKED-internal-simulated`.
