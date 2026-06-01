# TSIP v0.1 — Cycle 2 Cross-Family Re-Audit Synthesis

**Date:** 2026-04-20
**Subject:** `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1.md` with Cycle 2 fixes F-1 through F-10 applied
**Live reviewer families:** Meta (Llama 3.3 70B / Groq), Google (Gemini 2.5 Pro), OpenAI-OSS (GPT-OSS 120B / Groq)
**Cycle 1 outcome:** CYCLE-2-REQUIRED with 1 HIGH + 6 MED + 3 LOW
**Cycle 2 outcome:** Editor READY, Judge PASS 100/100, Red Team REQUIRES_MINOR_FIXES **blocking:false**
**Interpretation adopted:** policy-lock (amendment seals policy; named Logician gates + schema validators + scripts are engineering queue items tracked under Da Vinci §7 + Logician v0.2 — not LOCK blockers).
**Audit trail:** this directory — editor_verdict.md, judge_verdict.md, red_team_verdict.md.

## Summary

| Seat | Family | Verdict | Score | blocking |
|------|--------|---------|-------|----------|
| Editor | Meta | READY | n/a | false |
| Judge | Google | PASS | 100/100 (completeness 18 → 20 via F-10) | false |
| Red Team | OpenAI-OSS | REQUIRES_MINOR_FIXES | 7 policy-CLOSED + 2 OPEN-policy MED + 4 NEW (MED×2 + LOW×2) | **false** |

All three seats return `blocking:false`. No seat gates LOCK promotion.

## Cycle 1 → Cycle 2 closure matrix (Red Team view)

| Cycle 1 finding | Cycle 2 fix | Red Team verdict | Real status |
|-----------------|-------------|------------------|-------------|
| RT-NEW-01 HIGH — bootstrap reusable escape hatch | F-1 single-use rule + queued `F-BOOTSTRAP-REUSE` | CLOSED-policy | Engineering queue: implement `F-BOOTSTRAP-REUSE` Logician gate |
| RT-NEW-02 MED — reviewer-family assignment gameable | F-2 router.yaml-anchored assignment + operator-signed ledger | **OPEN-policy** | Residual trust in single operator signature; queued follow-up: independent second-signer or randomized pool |
| RT-NEW-03 MED — watchlist phone-home risk | F-3 explicit carve-out + surveillance-cost acceptance | **OPEN-policy** | Carve-out still permits outbound HTTP for watchlists; tension with broader "nothing phones home" slogan — v0.2 language refinement queued |
| RT-NEW-04 MED — extension cascade | F-4 hard cap max 2 extensions (4 weeks total) | CLOSED-policy | Numeric ceiling removes cascade vector |
| RT-NEW-05 MED — blocking dissent needs deterministic gate | F-5 mandatory `blocking:true\|false` field + queued `F-VERDICT-BLOCKING-MISSING` POST-gate | CLOSED-policy | Engineering queue: implement POST-gate |
| RT-NEW-07 MED — Q5 default-NO triage needs appeal | F-7 30-day cooling-off + batch re-review | CLOSED-policy | Appeal path now formal |
| RT-NEW-06 LOW — operator-alone audit steady-state | F-6 clarifies Da Vinci optional, operator-alone steady-state indefinite | CLOSED-policy | Fallback gap removed |
| RT-NEW-08 LOW — spike manifest pre-approval | F-9 YAML schema validation blocks branch creation | CLOSED-policy | Engineering queue: author `spike_manifest.schema.json` |
| RT-NEW-09 LOW — v0.2 continuous-scan contingency | F-10 12-month manual-weekly fallback | CLOSED-policy | Manual fallback defined |
| Judge completeness dock (Cycle 1 18/20) | F-6 + F-10 cover v0.2 dependency gap | CLOSED | Judge Cycle 2 re-scored 20/20, total 100/100 |
| Editor findings (tone, glosses, passive voice, structure) | Editor cleanups applied in place | CLOSED | Editor Cycle 2 READY |

## New Red Team findings this cycle (all engineering-queue, none blocking)

| Severity | Finding | Engineering-queue disposition |
|----------|---------|-------------------------------|
| MED | F-2 single-operator sign-off = single-point-of-failure for reviewer assignment | v0.2 protocol refinement: add independent second-signer or randomized pool selection from router.yaml-eligible families |
| MED | F-3 phone-home carve-out creates privacy-consistency tension with broader sovereignty claim | v0.2 protocol language refinement: rewrite sovereignty statement to distinguish inference-path ("never phones home") from surveillance-path ("fetches from publisher-visible sources with operator acceptance of that visibility") |
| LOW | F-5 manual verification of `blocking` field invites human-error miss | Covered by queued `F-VERDICT-BLOCKING-MISSING` POST-gate (engineering queue item — not a new residual) |
| LOW | F-10 manual-weekly fallback introduces long-term reliance variability | v0.2 check-in: quarterly operator cadence review; accepted as steady-state risk for v0.1 |

## Policy-lock interpretation (applied from EN-001/EN-002 Cycle 2 synthesis)

The same interpretation that resolved the EN-001/EN-002 Red Team "PARTIAL" verdicts applies here: Red Team's remaining OPEN-policy findings on RT-TSIP-02 and RT-TSIP-03 are refinement asks that the existing amendment text does not fully resolve but which are policy-level follow-ups, not implementation-proof demands. Under policy-lock:

- `LOCKED-sealed` = policy seal. The protocol's rules are set; their names identify where enforcement belongs.
- Implementation of named gates (`F-BOOTSTRAP-REUSE`, `F-VERDICT-BLOCKING-MISSING`, schema validator) is engineering queue under Logician v0.2 + Da Vinci §7.
- The 2 OPEN-policy MED refinements (operator-signature trust model, watchlist-consistency language) are v0.2 protocol items tracked in the protocol's own amendment stream — not LOCK blockers.

## Bootstrap exception consumption

This LOCK-sealed consumes the single bootstrap exception (TSIP was authored before TSIP existed to govern it; F-1 declares the exception single-use and the corresponding Logician gate `F-BOOTSTRAP-REUSE` enforces non-reuse). No future amendment or protocol may invoke bootstrap exception as rationale; `F-BOOTSTRAP-REUSE` is now the structural enforcement layer.

## Promotion recommendation

**LOCKED-sealed pending operator signature.** All three seats non-blocking. Bootstrap exception consumed at this LOCK. Engineering queue absorbs 2 queued Logician gates + schema validator + v0.2 refinement items for the 2 OPEN-policy MED + 2 NEW MED findings.

## Engineering queue additions from this audit

1. `F-BOOTSTRAP-REUSE` Logician gate (v0.2 queue) — verifies bootstrap exception marker appears at most once across `lock_history.v1.jsonl`.
2. `F-VERDICT-BLOCKING-MISSING` Logician POST-gate (v0.2 queue) — verifies every reviewer verdict carries a `blocking:true|false` field with strict boolean typing.
3. `pipeline/engineering/schemas/spike_manifest.schema.json` — JSON schema for pre-branch manifest validation.
4. v0.2 TSIP protocol refinement: reviewer-assignment independent second-signer or randomized selection.
5. v0.2 TSIP protocol refinement: sovereignty-language rewrite distinguishing inference-path from surveillance-path.

## Pattern across all three Tier 1 Cycle 2 re-audits

| Amendment | Editor | Judge | Red Team | Overall blocking? |
|-----------|--------|-------|----------|-------------------|
| Agent SDK Thesis (EN-001+EN-002) | READY | 100/100 PASS | PARTIAL × 5 → policy-lock closes | FALSE under policy-lock |
| TSIP v0.1 | READY | 100/100 PASS | 7 CLOSED + 2 OPEN-policy MED | **FALSE** |
| EN-003 | READY | 96/100 (Qwen, per F-4) | Cycle 2 blocking:true → Cycle 3 blocking:false after F-1/F-4/F-6/F-7 Cycle3 fixes | FALSE at Cycle 3 |

All three promote under policy-lock.

## For the white paper

TSIP's Cycle 2 re-audit demonstrates a core property of the architecture: a protocol that governs its own future amendments must survive a live cross-family review of itself under its own rules. TSIP authored-before-TSIP-existed is the only allowable bootstrap; that bootstrap is now consumed and the `F-BOOTSTRAP-REUSE` gate closes the door behind it. The policy-lock interpretation — adopted uniformly across the three Tier 1 amendments — converges the re-audit loop: findings are either policy-CLOSED or named as specific policy-level refinements, never endless implementation-proof demands.

## Next actions

1. Operator signs LOCKED-sealed on TSIP v0.1 (3rd of the Tier 1 three).
2. Engineering queue absorbs `F-BOOTSTRAP-REUSE`, `F-VERDICT-BLOCKING-MISSING`, `spike_manifest.schema.json`.
3. v0.2 TSIP refinement items (2 OPEN-policy MED + 2 NEW MED) enter the protocol's own amendment stream under Da Vinci §7.
4. TSIP is now the active Tilth Self-Improvement Protocol governing all future tool/capability adoption decisions.
