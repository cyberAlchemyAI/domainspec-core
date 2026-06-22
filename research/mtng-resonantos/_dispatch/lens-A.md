# Lens A — Necessity / Value attack (raw return)

- **Dispatch:** `2026-06-22-mtng-v2-review` · group `review-lenses` · agent **Russell, Bertrand** (skeptic)
- **anti_bias axis:** attack-vector — necessity/KILL-DEFER side
- **Verdict:** DEFER (until value is empirically proven)
- **Status:** integrated into `../REVIEW.md` (parent synthesis). Raw, unedited below.

> Verification discipline: each finding carries what the agent checked. The parent independently
> confirmed F1/F4 against the full spec (P8 trust-but-verify); no corrections needed on this lens.

---

# Red-Team Review — MTNG v2 Post-Hoc Issue Packager
## Attack vector: NECESSITY / VALUE (reviewer persona: Russell)

The honest charge: this is a well-disciplined narrowing of an over-built design, but the narrowing reduced *scope*, not *apparatus*. The thing it must beat — a flat summary plus a markdown issue template — is never measured, and the spec's own residue map admits it.

### F1. The central value claim is untested, and the spec admits it
**Severity: blocker** · **Spec: 01 §21, §25; corroborated by L1 R-VPR, R-VAL**
The entire justification reduces to criterion #2, "more actionable than a flat summary" (§21). No baseline, no metric, no threshold, no judge. "Becomes clearer," "more actionable," "acceptable overhead" are unfalsifiable. R-VPR states it directly and its closure mechanism ("the pilot") does not yet exist.
*Verification:* §21 (all 10 criteria qualitative); L1 R-VPR/R-VAL OPEN; ledger D4/D6.
*Change request:* **Prove first.** Pre-register a falsifiable criterion with a flat-summary-plus-template baseline before Stages 1–7. No build without a frozen criterion and a head-to-head.

### F2. A disciplined engineer with a markdown template already gets most of this for free
**Severity: major** · **Spec: 01 §4, §14, §23**
§4 "separate reproduction/environment/provider/UX/docs" = an issue template's headings. §14 validators ("facts vs speculation," "expected vs actual," "steps or missing-step marker") = the standard bug-report checklist. The only marginal value over a template is *automatic decomposition* — which is the unmeasured classifier (F4). `distill.md` concedes: "without [the node contract] MTNG is just a summarizer."
*Change request:* **Reframe** V1 as "auto-section-filler for an existing issue template" and justify only the decomposition delta.

### F3. The full node/validator/contribution/OKF apparatus is unjustified for a single-developer issue packet
**Severity: major** · **Spec: 01 §1, §19, §20**
V1 emits eight artifacts for one developer turning one session into one issue. `contribution-records.yaml` attributing triage/reproduction to the single person who did all of it, `valuation: false`, is ceremony. OKF is layered on a format R-OKF flags as unverified to even exist under that name.
*Change request:* **Defer** contribution records and OKF out of the pilot. Ship only `developer-issue-packet.md` + `validator-report.md` + `audit-log.jsonl`.

### F4. The 8 binary branch triggers are not reliably distinguishable; detection accuracy unmeasured
**Severity: major** · **Spec: 01 §12, §5; L1 R-CLS**
Several triggers co-fire by construction: in the §23 registry each mode pairs exactly one artifact with one validator, so "artifact changes" and "validator changes" are not independent. ~8 triggers ≈ 2–3 real degrees of freedom. The hard upstream problem (which mode a substring excites) is R-CLS, unmeasured; renaming Tone→Routing Signature changed the label not the fragility (D5).
*Change request:* **Prove first** — build the R-CLS evidence harness; then cut triggers to the independent ones the data supports.

### F5. "Capture contribution structure" produces a file no one has a reason to read
**Severity: major** · **Spec: 01 §19; Test 4 §25**
§19 forbids the records from feeding compensation/ownership/voting/tokenization/governance/leaderboards. So `contribution-records.yaml` is write-only in V1 — generated, persisted, consumed by nothing. §10 routes ingestion to a deferred, approval-gated future.
*Change request:* **Cut** from V1 (merge with F3); keep as a documented future hook.

### F6. The graph/synthesis layer is prose, not a schema
**Severity: minor** · **Spec: 01 §17; L1 R-MRG**
Synthesis is the payoff step but §17 gives prose rules with no merge algorithm or conflict schema. If recombination is just "concatenate section files with status labels," the graph metaphor is decorative over a list of filled-in sections.
*Change request:* **Prove first** — concrete merge schema + worked conflict example; show recombined output beats concatenated template sections, else drop the graph framing.

### F7. Per-signal overhead is unestimated even for the narrowed V1
**Severity: minor** · **Spec: 01 §21 #8; L1 R-OVH**
Criterion #8 makes "acceptable overhead" a pass condition but no estimate/budget/measurement exists. You can't claim it beats a 5-minute flat summary if a run costs more.
*Change request:* **Prove first** — back-of-envelope estimate, then measured dry-run with a stated ceiling, before Stage 2.

## OVERALL VERDICT: **DEFER (until value is empirically proven).**
Not KILL: the discipline ("branch only on a named boundary; validate before synthesis; never flatten") is sound and the residue map identifies every gap honestly. Not FIX-THEN-BUILD: the load-bearing claim (R-VPR) is untested and four of eight emitted artifacts are apparatus no V1 consumer reads. Build nothing beyond a pre-registered head-to-head until the value delta is measured.
**Changes my mind:** a pre-registered, blinded comparison on a real dataset showing MTNG packets are measurably more actionable (fixed metric, independent judge) than the same inputs through a disciplined flat summary + markdown template, at bounded overhead.
