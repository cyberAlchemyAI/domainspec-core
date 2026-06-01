## Your task — Editor seat, Cycle 2 verification

Your family: **Meta (Llama 3.3 70B / Groq).** Cross-family rigor — you are NOT Anthropic. L-005 two-audit cycle: this is verification of Cycle 1 fixes. No silent third round.

Your Cycle 1 verdict: **REQUIRES_FIX** with 5 findings:

- E-01 (MED): Ambiguous register distinction between Funder Intel + Match DB.
- E-02 (LOW): Curation cadence not specific enough about when operator gets prompt.
- E-03 (LOW): YAML schemas not labeled as illustrative.
- E-04 (MED): Stage-5 boundary not crisp; reader pulled toward thinking commons exists today.
- E-05 (LOW): Cross-amendment composition narrative could use diagram/table.

## Cycle 2 task

Read the patched v7.0.5 amendment (provided below). For EACH Cycle 1 finding, judge:

- **CLOSED** — fix landed, finding resolved
- **PARTIALLY CLOSED** — partial fix; remaining gap (specify gap)
- **OPEN** — fix did not land or did not resolve the concern (specify why)

Then scan for any **NEW** findings introduced by the Cycle 1 fixes (e.g., new ambiguity, new contradiction, new clarity issue).

## Output format

```
## E-01 — [CLOSED | PARTIALLY CLOSED | OPEN] — short verification statement
## E-02 — ...
## E-03 — ...
## E-04 — ...
## E-05 — ...

## NEW findings (if any)
### FINDING E-NN — Title (HIGH/MED/LOW)
[same format as Cycle 1]

## Verdict — Cycle 2
[READY_TO_LOCK | REQUIRES_FIX | BLOCKING]
```

Verdict guidance:
- READY_TO_LOCK = all Cycle 1 findings CLOSED + zero new findings (or only LOW non-blocking)
- REQUIRES_FIX = any Cycle 1 finding OPEN or PARTIALLY CLOSED, OR new MED/HIGH finding
- BLOCKING = architectural defect that text-fix cannot close (rare for Cycle 2)

Budget: ≤ 800 output tokens. Be specific. Cite the new section text where the fix landed (or didn't). No vibes.

Begin.
