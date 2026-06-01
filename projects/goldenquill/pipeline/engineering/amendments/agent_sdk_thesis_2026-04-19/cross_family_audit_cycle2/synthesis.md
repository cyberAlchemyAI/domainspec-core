# Agent SDK Thesis — Cycle 2 Cross-Family Re-Audit Synthesis

**Date:** 2026-04-20
**Subjects:** EN-001 + EN-002 with Cycle 2 fixes F-1 through F-7 applied
**Live reviewer families:** Meta (Llama 3.3 70B), Google (Gemini 2.5 Pro), OpenAI-OSS (GPT-OSS 120B)
**Cycle 1 outcome:** CYCLE-2-REQUIRED with 1 HIGH + 5 MED + 1 LOW
**Cycle 2 outcome — mixed:** Editor READY, Judge PASS 100/100, **Red Team REQUIRES_MINOR_FIXES blocking:true**

## Summary

| Seat | Family | Verdict | Score |
|------|--------|---------|-------|
| Editor | Meta | READY | n/a |
| Judge | Google | PASS | 100/100 (recovered 6 pts on reversibility) |
| Red Team | OpenAI-OSS | **REQUIRES_MINOR_FIXES — blocking:true** | 1 HIGH + 4 MED + 1 LOW remaining (all PARTIAL closures) + 5 NEW findings |

Divergence between Judge and Red Team is the substantive finding of this cycle. Judge scored the fixes on **intent** and found them complete. Red Team scored the fixes on **proof of implementation coverage** and found each fix PARTIAL.

## The interpretation question surfaced

**Does `LOCKED-sealed` represent policy lock or implementation lock?**

- **Policy-lock reading:** The amendment documents policy; referenced scripts/tests/gates are engineering queue items tracked separately. Red Team's "script doesn't exist yet" findings gate the SCRIPT's production use, not the AMENDMENT's LOCK.
- **Implementation-lock reading:** Every construct the amendment names must be executable and coverage-proven before LOCKED-sealed. Red Team's findings block LOCK.

Tilth's existing discipline (per AGENTS.md + Da Vinci §7 + Logician v0.2 queue items) reads as **policy-lock**: amendments are about policy; scripts are about engineering queue. By that reading, Red Team's PARTIAL closures aren't LOCK blockers — they're engineering-queue items that reference the amendment as their specification.

**Recommendation: adopt the policy-lock reading explicitly.** Write this into TSIP (as its own Cycle 2 follow-up) and into the handoff docs. Otherwise every amendment becomes hostage to every implementation detail.

## Cycle 1 → Cycle 2 closure matrix (Red Team view)

| Cycle 1 finding | Cycle 2 fix | Red Team verdict | Real status |
|-----------------|-------------|------------------|-------------|
| RT-NEW-01 HIGH — rollback ignores external writes | F-1 inventory + sandbox + scripts | PARTIAL — coverage proof absent | **Policy CLOSED; engineering queue: prove exhaustive coverage, author `spike_rollback.sh`, author schema-validator for manifest** |
| RT-NEW-02 MED — SDK breaking-change detection | F-2 contract check + outbound monitor | PARTIAL — doesn't catch silent logical regressions | **Policy CLOSED; engineering queue: add behavioral regression tests (parameterized spike against fixed inputs, diff outputs across SDK versions)** |
| RT-NEW-03 MED — LOCK landed ambiguity | F-3 three-check mechanical | **CLOSED** | CLOSED |
| RT-NEW-04 MED — vocabulary drift | F-5 lint rule | PARTIAL — depth of pattern matching unspecified | **Policy CLOSED; engineering queue: lint rule must cover case variations, compound names, dynamic string constructions** |
| RT-NEW-05 LOW — sovereignty under error states | F-6 4 states + outbound allowlist | PARTIAL — misses quota/streaming/tool-loop + non-HTTP channels | **Policy CLOSED; engineering queue: extend error-state matrix, add non-HTTP channel blocking (iptables/socket monitoring)** |
| RT-NEW-06 MED — L-003 precedent risk | F-4 bounded precedent | PARTIAL — no fail-closed enforcement | **Policy CLOSED; engineering queue: add Logician gate `F-SDK-PRECEDENT-REUSE` that blocks multi-seat adoption without per-seat audit evidence** |

## New findings this cycle (Red Team)

These are the findings the fixes themselves introduced. None are policy-level (they're all about implementation surfaces the fixes create):

1. **Rollback-script attack surface.** `spike_rollback.sh` + JSONL ledger are new code paths. If compromised, could trigger unauthorized rollbacks. Engineering queue: add signature verification for rollback scripts + ledger integrity check.
2. **Sandbox scope ambiguity.** "Transactional sandbox" at `spike-scratch/<id>/` claims pre/post snapshots but doesn't confirm indirect writes (library-level, OS temp files) are redirected. Engineering queue: sandbox implementation must use syscall-level interception (fsevents on macOS) OR explicit mount-namespace equivalent.
3. **Escalation path unspecified.** F-1 mentions escalation without concrete mechanism. Engineering queue: define escalation — alert to which channel, who approves the escalation, what's the max-time before escalation itself times out.
4. **Lint-exception abuse.** `# SDK interop:` comment could be inserted without genuine justification. Engineering queue: exception comments require PR reviewer sign-off + quarterly audit of exception count and justifications.
5. **Outbound-HTTP monitor bypass.** F-6's monitor checks HTTP. SDK could use raw TCP, gRPC, IPC. Engineering queue: extend to full-network monitoring (lsof + network namespace); note that full coverage may require privileged operation.

## Promotion recommendation

**Conditional LOCKED-sealed, with policy-lock interpretation adopted explicitly.**

If Josh accepts the policy-lock reading:
- EN-001: LOCKED-sealed pending operator signature. Engineering queue absorbs the 11 concrete implementation items above.
- EN-002: LOCKED-sealed pending operator signature.

If Josh prefers implementation-lock reading:
- EN-001: stays LOCKED-internal until implementation proofs land. Opens Cycle 3.
- EN-002: lint rule must be authored + tested before LOCK-sealed.

## For the white paper

This audit round is itself valuable evidence: three cross-family reviewers under the same discipline produced three distinct truth-tellings about the same artifact. Editor said READY (stylistic reading). Judge said PASS 100/100 (intent reading). Red Team said REQUIRES_MINOR_FIXES blocking:true (proof reading). None is wrong; each is answering a different question. The architecture correctly routes the question to the right reviewer.

**Meta-finding:** Tilth's discipline surfaces that LOCK status needs two separate fields — `policy_lock: sealed|internal` and `implementation_lock: sealed|internal|pending`. Treating them as one field is what produced the interpretation ambiguity this audit exposed.

## Engineering queue additions from this audit

All eleven items below reference EN-001 or EN-002 as their policy source. They land in Da Vinci §7 engineering queue:

1. Author `scripts/spike_rollback.sh` with dry-run/apply/verify subcommands.
2. Author `tilth/tests/sdk_contract_check.sh` with interface snapshot + outbound-traffic allowlist enforcement.
3. Author `pipeline/engineering/schemas/spike_manifest.schema.json` for manifest pre-check.
4. Author `scripts/lint_sdk_vocabulary_drift.sh` with pattern-matching depth specified (case-insensitive, compound-aware, dynamic-string-aware).
5. Extend F-6 sovereignty test to cover quota exhaustion, streaming interruption, tool-loop error.
6. Extend F-6 to block non-HTTP outbound channels (raw sockets, gRPC, IPC).
7. Add Logician gate `F-SDK-PRECEDENT-REUSE` (blocks multi-seat SDK adoption without per-seat audit evidence).
8. Add Logician gate `F-ROLLBACK-SCRIPT-INTEGRITY` (verifies signature on rollback script before execution).
9. Define escalation mechanism for failed rollback (channel, approver, timeout).
10. Quarterly audit of lint-exception comments + justifications.
11. Sandbox implementation plan for full external-write capture (syscall-level or namespace-level).

## Next steps

1. Operator decision on policy-lock vs implementation-lock reading (see "Promotion recommendation" above).
2. If policy-lock: EN-001 + EN-002 promote to LOCKED-sealed with operator signature. Engineering queue absorbs the 11 items.
3. If implementation-lock: Cycle 3 triggered; engineering builds the concrete artifacts; re-audit.
4. Parallel: run TSIP Cycle 2 re-audit using same pattern. Likely to surface similar policy-vs-implementation divergence.
5. Parallel: run EN-003 Cycle 2 re-audit with Qwen as Judge (per F-4 mandate, not Gemini which was Cycle 1 self-reference).
