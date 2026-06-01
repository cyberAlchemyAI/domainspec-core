## Your task — Red Team seat, Cycle 2 verification

Your family: **OpenAI-OSS (GPT-OSS 120B / Groq).** Triple cross-family rigor preserved. L-005 two-audit cycle: this is verification of Cycle 1 fixes. No silent third round.

Your Cycle 1 verdict: **ESCALATE / blocking:true** with 9 findings:

- **RT-01 (HIGH):** Cross-org Match DB read via indirect Logician path — failure code named but no concrete pre-check enforcement specified.
- **RT-02 (HIGH):** Vector index workspace-shared without per-org namespace partition for Match DB content.
- **RT-03 (HIGH):** Funder corpus integrity check at ingestion only — no per-read hash verification.
- **RT-04 (MED):** Pydantic-AI vector tool lacks org_filter argument validation.
- **RT-05 (MED):** consent_tier mutation lacks operator signature audit trail.
- **RT-06 (MED):** Channel G cross-reference sanitization unspecified — funder docs may embed cross-org match_id refs.
- **RT-07 (LOW):** Staleness threshold undefined — operator can disable protection by setting absurd values.
- **RT-08 (LOW):** Archivist slot transition leaves stale `curated_by: operator` audit chain entries.
- **RT-09 (LOW):** Channel G assumes Funder Intel always public; some funder docs may be confidential.

Your Cycle 1 framing: "ESCALATE" because HIGH findings required runtime enforcement guarantees you said "go beyond text-level fixes." **Author disposition:** disagrees — Logician PRE-check semantics are an existing v7 architectural primitive; specifying those semantics IS a text-level fix. Test your Cycle 1 framing against the patched amendment.

## Cycle 2 task — A3 SFR three-block

**Premises.** Re-cite Cycle 1 premises by ID. Add new premises if Cycle 1 fixes introduced new architectural commitments.

**Execution trace.** For EACH Cycle 1 finding (RT-01..RT-09):

- **Disposition:** [CLOSED | PARTIALLY CLOSED | OPEN]
- **Closure verification:** cite the patched §N + the specific phrase that addresses the finding. Quote the enforcement-specific text where applicable (e.g., the new §5.1 enforcement spec for F-MATCH-DB-CROSS-ORG).
- **Adversarial probe of the closure:** if you say CLOSED, briefly state why the closure does NOT introduce a new evasion surface. If you say PARTIALLY CLOSED or OPEN, specify the remaining attack vector.

Then run **fresh adversarial probes** against the elaborated §5 (six failure codes with enforcement specs) AND the new §3 sanitization pre-pass AND the new §1 lifecycle terminal state. Find new attack surfaces if any exist.

**Conclusion.** State `blocking: true|false`. Verdict:

- **PASS** — all HIGH closed; zero new HIGH; LOCK-ready
- **REQUIRES_MINOR_FIXES** — Cycle 1 LOW remain OPEN, no new HIGH, no Cycle 1 HIGH OPEN
- **REQUIRES_FIXES** — any Cycle 1 HIGH OPEN, OR new HIGH from Cycle 2 probes
- **ESCALATE** — architectural defect not closeable by amendment edit; surface to operator

Budget: ≤ 2000 output tokens. Be adversarial — if a Cycle 1 fix opens a new evasion surface, name it. If your Cycle 1 escalation framing was overcautious, say so explicitly. Honesty over face-saving.

Begin.
