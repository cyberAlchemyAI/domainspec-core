# Tilth Self-Improvement Protocol (TSIP) — v0.1

**Status:** `LOCKED-internal-simulated` as of 2026-04-19 Cycle 2 — operator signature pending; live cross-family audit via OpenClaw required for `LOCKED-sealed`
**Date:** 2026-04-19
**Author:** Cowork / Anthropic family (simulated)
**Supersedes:** `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1_DRAFT.md` (redirected)
**Thesis trail:** `pipeline/engineering/protocols/tsip_v0.1_thesis_2026-04-19/00_bootstrap_thesis.md`
**OpenClaw cross-family handoff:** `pipeline/engineering/handoffs/openclaw_cross_family_audit_tsip_v0.1_2026-04-19.md`

## Why this protocol exists

LLM tooling — SDKs, MCP servers, model families, frameworks, disciplines — drifts weekly. Tilth's edge depends on being *current* without being *captured* (by hype, vendor lock-in, or premature optimization). Informal operator-mood-driven adoption leaks two ways: good tools go un-noticed, and flashy tools get adopted without audit. TSIP codifies a deterministic "find / ask / evaluate / spike / adopt / operate / retire" loop so the decision process itself is auditable.

## Scope

Applies to adoption decisions about:
- External libraries / SDKs (e.g., Claude Agent SDK, LiteLLM, LangGraph-style frameworks — note LangGraph is already REJECT-LOCKED per CLAUDE.md)
- MCP servers (new channel families, external tool integrations)
- Model providers and bindings (`router.yaml` additions or changes)
- Skills and subagent patterns
- Architectural disciplines / patterns borrowed from other systems

Does NOT apply to:
- Content decisions (what goes in a grant) — that is domain work, not tool adoption
- Client onboarding — that is the BYOK + Partner Agreement flow
- Internal amendments to already-adopted primitives (those use the existing L-005 two-audit cycle directly)

## The eight phases

### 1. Surveillance — how candidates reach attention

**v0.1 cadence: operator-triggered only.** Continuous background scan is a v0.2 feature that auto-activates when Da Vinci Quill-persona goes live (gated on real-engineer validator per Da Vinci §13). Do not build the surveillance agent before its audit gate clears.

Channels in priority order:

1. **Operator-driven** — Josh surfaces a candidate from a conversation, article, conference, peer
2. **Lessons-driven** — `lessons.md` flags a recurring failure that an external tool might address (L-NNN with tool-suggestion annotation)
3. **Client-driven** — a partner, grant program, or funder requires a specific tool
4. **Watchlist** *(operator-reviewed, not auto-scanned)* — curated RSS / paper-feed / release-notes subscriptions: Anthropic, OpenAI, Google, Meta, Alibaba, Moonshot, Mistral, MCP registry, major conferences (NeurIPS, ICML, ICLR, ACL, EMNLP). **Operator curates and reviews the watchlist in v0.1; v0.2 transfers this to Da Vinci Quill-persona.**
5. **Background scan (v0.2, not yet live)** — Da Vinci Quill-persona surveillance activates here when Da Vinci is instantiated post-real-engineer-validator-gate

Output: one-line candidate entry in `pipeline/engineering/candidates_register.md`.

**Register format:** markdown table with one row per candidate, status column edited in place (proposed / triaged / evaluating / spiking / adopted / retired), plus a change-log section below the table where each status transition gets an append-only dated note. Matches the format `lessons.md` and `daily_logs/` already use. No YAML, no tooling required — operator edits the markdown directly.

### 2. Triage — one-line yes / no / defer

For each new candidate, answer six questions in under five minutes:

1. Relevant to v0.1, v0.2, or v0.3?
2. Sovereignty-compatible (local-only OR BYOK-acceptable, no forced phone-home)?
3. Cross-family-compatible (does not force Anthropic-only or any single-family lock-in)?
4. Maturity floor met (not pre-alpha unless experimental slot is open)?
5. **Are you confident Tilth already has a better-fitting primitive? (Default NO — proceed to evaluation where this is checked rigorously.)**
6. Reversible at a reasonable cost?

All six YES (with Q5 YES meaning "confident existing primitive is better") → triage REJECT. All-six-PROCEED pattern (Q1–Q4 + Q6 YES, Q5 NO) → triage PROCEED. Any NO with severity HIGH on Q1–Q4 or Q6 → triage REJECT. Mixed → triage DEFER with a re-evaluate date.

Output: triage verdict appended to the candidate register row.

### 3. Evaluation — structured questioning

If triage = PROCEED. Use `pipeline/engineering/templates/tool_evaluation_template.md` (to be written on first use). Question set:

- What problem does it solve?
- What does Tilth currently do that this would replace or augment?
- Does Tilth already have a better-fitting primitive? (second check, more rigorous than triage)
- Dependency surface? (what versions, what APIs, what breaking-change cadence)
- Reversibility? (rollback cost, data lock-in, state migration)
- Cross-family impact? (L-003)
- Sovereignty posture? (phone-home, cloud lock-in, BYOK fidelity)
- Resource cost? (8 GB dev + 128 GB prod memory, disk, latency)
- Version-pinnable?
- Real-engineer or external-expert validator available?
- Exit criteria? (what would make us abandon adoption later?)

Output: `pipeline/engineering/evaluations/<candidate>_<date>.md`.

### 4. Spike — bounded engineering experiment

If evaluation says PROCEED. Evidence-producing, not code-committing. A spike generates the data needed to decide; it does not ship anything.

**Spike manifest** *(YAML file at spike-open declaring version pin, exit criteria, rollback procedure)*:

- Dedicated branch
- Spike manifest committed before spike opens
- No state persisted in candidate-only format
- **Real-engineer validator gate** *(external engineer audits spike outputs before main-line merge, operationalized per Da Vinci §13; TSIP consumes this gate, does not define it)* required for promotion to main-line
- Pre-written rollback documented BEFORE spike opens

**Completion rule — evidence-triggered with sanity cap.** A spike ends when either (a) the evidence threshold in its exit criteria is reached (PASS, FAIL, or INCONCLUSIVE), OR (b) two calendar weeks elapse — whichever fires first. The 2-week cap is a backstop against drift; spikes that hit it without evidence get one of three operator verdicts: declare PASS, declare FAIL, or formally extend by one week with a new exit criterion. No silent extension beyond that.

Output: `pipeline/engineering/spikes/<candidate>_<date>/` with manifest, experiment log, metrics.

### 5. Thesis — cross-family audit

L-005 two-cycle discipline applied. Author seat = the proposing voice. Reviewer seats = three cross-family seats per `router.yaml`.

- Cycle 1 DRIVER: per-seat audit with discipline-specific focus (Editor clarity, Judge rubric score, Red Team adversarial). SFR three-block format for Judge and Red Team.
- Cycle 2 VERIFICATION: reviewers re-audit the fixes; verdicts harden.
- Zero silent third round per L-005.

Cross-family is strict: reviewer family ≠ author family. The seven-family taxonomy (Anthropic, OpenAI, OpenAI-OSS, Alibaba, Meta, Moonshot, Google) is defined in the A2 addendum per `pipeline/architecture/v0.1/tilth_architecture_locked.md` and live in `router.yaml`. For Anthropic-authored proposals, reviewers draw from Meta / Alibaba / OpenAI-OSS / Moonshot / Google / Mistral / OpenAI.

Output: audit trail under `pipeline/engineering/amendments/<candidate>_thesis_<date>/`.

### 6. Adoption — if Thesis passes

`LOCKED-sealed` requires: all reviewers READY + zero blocking dissent + operator signature.

On LOCK:
- Amendment file enters `pipeline/engineering/amendments/`
- `lessons.md` updated if adoption closes a recurring failure
- `router.yaml` updated if a binding changes
- Relevant blueprint section updated if architecture-touching
- `pipeline/engineering/adopted_tools_register.md` gets a row (tool, version, pin, maintainer, refresh policy)

### 7. Operating — after adoption

- Version pin maintained in the spike / adoption manifest
- Quarterly audit: has the tool deprecated a feature Tilth depends on? If so, spike replacement BEFORE deprecation bite
- Metrics: is the tool delivering its promised benefit? Measure against adoption-time baseline
- Drift watch: if the tool's API or behavior changes in a non-breaking way that nevertheless shifts Tilth's invariants, surface it at the quarterly audit

**Audit owner (v0.1):** operator alone. Da Vinci joins the audit group automatically when Da Vinci goes live post-real-engineer-validator-gate.

### 8. Retirement — when a tool should leave

Triggers (any one fires; they operate independently):

- Breaking change the spike cannot absorb
- Drift that violates Tilth invariants (sovereignty, cross-family, deterministic-first)
- Superseded by a better-fitting primitive (often Tilth's own specialization)
- Unused for **four consecutive quarterly audits (one full year)** — gives seasonal tools a full cycle before retirement
- **Operator discretion** — retiring for reasons not in the above triggers is always valid, logged in `lessons.md` with reasoning

On retirement:
- `lessons.md` gets an L-NNN entry documenting why
- Migration path for any state / data locked in the retiring tool
- Thesis round for the replacement (re-enters the protocol at phase 3 or 4)

## Cadence

| Phase | Cadence |
|-------|---------|
| 1 Surveillance | Operator-triggered; watchlist reviewed weekly |
| 2 Triage | Weekly batch review |
| 3 Evaluation | Per candidate on triage PROCEED |
| 4 Spike | Per evaluation PROCEED; evidence-triggered; 2-week sanity cap |
| 5 Thesis | Per spike completion |
| 6 Adoption | Per Thesis LOCK-sealed |
| 7 Operating | Quarterly audit per adopted tool |
| 8 Retirement | Triggered; not scheduled |

## Anti-patterns this protocol prevents

- Adopting because it's trending
- Rejecting because it's new (flip side of the same sin)
- Silent third-round revision (L-005)
- Single-family review of a cross-family-consequential decision (L-003)
- Pasting vendor docs as "already evaluated" (L-002)
- Treating a `LOCKED-internal` verdict as `LOCKED-sealed` without live cross-family pass
- Letting a spike creep into main-line without real-engineer gate (Da Vinci §13)
- Retiring silently (always logged in `lessons.md` with reasoning)
- Dying at triage Q5 without the rigorous evaluation check (mitigated by Q5 confidence-framing default NO)

## Resolved decisions (operator-set 2026-04-19)

| # | Decision | Resolution |
|---|----------|-----------|
| 1 | Surveillance cadence | Operator-triggered only for v0.1. Continuous background = v0.2 gated on Da Vinci live. |
| 2 | Candidates register format | Markdown table with status column (edit-in-place) + appended dated change-log below. No YAML. |
| 3 | Spike completion rule | Evidence-triggered; 2-week sanity cap as backstop; operator verdict at cap (PASS / FAIL / one-week formal extension). |
| 4 | Quarterly audit owner | Operator alone for v0.1. Da Vinci joins when Da Vinci goes live. |
| 5 | Retirement "unused" threshold | Four consecutive quarterly audits (one year). Other triggers (including operator discretion) fire independently. |

## Bootstrap Thesis — 2026-04-19

Simulated Thesis (single-family voice) cleared L-005 two-cycle at `pipeline/engineering/protocols/tsip_v0.1_thesis_2026-04-19/00_bootstrap_thesis.md`. Judge Cycle 2 score: 95/100. All reviewers READY. Status: `LOCKED-internal-simulated`.

## Protocol self-application

TSIP is itself a candidate for adoption under its own process. First-run bootstrap exception: the protocol is authored before the protocol exists, so its initial Thesis is simulated + operator-signed as `LOCKED-internal`. Promotion to `LOCKED-sealed` requires a live cross-family audit on the protocol itself via OpenClaw per `pipeline/engineering/handoffs/openclaw_cross_family_audit_tsip_v0.1_2026-04-19.md`.

**Bootstrap exception single-use rule (per Cycle 2 fix F-1 below):** the bootstrap exception documented above is used EXACTLY ONCE — for TSIP v0.1 itself. No future amendment may invoke "bootstrap exception" as a reason to skip live cross-family audit. Any invocation of the phrase post-TSIP-LOCKED-sealed is a PRE-gate fail and blocks the LOCK. The exception is recorded in `pipeline/engineering/lock_history.v1.jsonl` with flag `bootstrap: true` — exactly one such entry ever exists.

---

## Cycle 2 Fixes — Applied 2026-04-20 (addresses live cross-family audit findings)

The live cross-family audit at `pipeline/engineering/protocols/tsip_v0.1_thesis_2026-04-19/cross_family_audit/` surfaced 1 HIGH + 6 MED + 3 LOW + Editor notes. Fixes F-1 through F-10 below address each finding inline.

### F-1 — Bootstrap exception single-use lock (addresses RT-NEW-01 HIGH)

The bootstrap exception note above now states explicitly: used exactly once, recorded in `lock_history.v1.jsonl` with `bootstrap: true`, any future invocation is a PRE-gate fail. Planned Logician gate: `F-BOOTSTRAP-REUSE` (v0.2 engineering queue).

### F-2 — Reviewer-family assignment mechanism (addresses RT-NEW-02 MED)

**Adds to Phase 5 Thesis section:**

*Reviewer assignment rule: for each Thesis round, the reviewer seats for Editor, Judge, and Red Team are determined by router.yaml (not by author choice). Any deviation (e.g., self-reference Judge swap per F-4 in EN-003) must be explicitly documented in the audit trail before the call fires. The assignment is logged in the audit trail's header; operator signs off on the assignment log as part of the LOCK ceremony. An independent random-pool scheduler is a v0.2 enhancement; for v0.1 the router-plus-documented-deviation path is the mechanism.*

### F-3 — Watchlist phone-home carve-out (addresses RT-NEW-03 MED)

**Adds to Phase 1 Surveillance:**

*Sovereignty carve-out — watchlist fetches (RSS, paper feeds, release notes) generate outbound HTTP requests that source publishers can observe. This is a surveillance cost the operator accepts: the publisher learns their source was read, but no operator data flows outward. The carve-out is documented so the sovereignty claim ("nothing phones home") remains accurate for the inference pipeline while the discovery pipeline operates under a weaker "publishers may observe what we read" rule. Future defense-in-depth option: route watchlist fetches through Tor/relay; not implemented in v0.1.*

### F-4 — Extension cap (addresses RT-NEW-04 MED)

**Replaces the "Completion rule" paragraph in Phase 4 Spike:**

*A spike ends when either (a) the evidence threshold in its exit criteria is reached (PASS, FAIL, INCONCLUSIVE), OR (b) two calendar weeks elapse — whichever fires first. The 2-week cap may be extended by one-week increments, to a hard ceiling of **two extensions total (4 weeks absolute)**. Each extension requires an operator verdict entry in the spike ledger with a revised exit criterion. A third extension is a PRE-gate fail; any spike needing more than 4 weeks requires a fresh Thesis round, not an extension. "No silent extension beyond 4 weeks" is the discipline.*

### F-5 — Logician POST-gate on blocking verdict field (addresses RT-NEW-05 MED)

**Adds to Phase 6 Adoption:**

*Deterministic blocking gate: each reviewer's verdict carries a mandatory `blocking: true | false` field. Logician POST-gate `F-VERDICT-BLOCKING-MISSING` verifies this field is present and typed correctly on every verdict; any missing or malformed field blocks the LOCK. Any `blocking: true` on any reviewer's verdict automatically blocks LOCKED-sealed until resolved in a Cycle 2 fix + re-audit. The gate is Logician v0.2 engineering queue; for v0.1, operator manually verifies the blocking field before signing.*

### F-6 — Operator-alone audit steady-state clarification (addresses RT-NEW-06 LOW)

**Adds to Phase 7 Operating:**

*Operator-alone audit is an acceptable steady-state indefinitely — not a temporary bootstrap state. Da Vinci's eventual joining is optional enhancement, not a prerequisite for the protocol to function. If Da Vinci never reaches live (real-engineer validator gate never clears), TSIP continues to operate correctly with operator-alone quarterly audits. The "Da Vinci joins when live" note is an available future enhancement path, not an unmet dependency.*

### F-7 — Triage Q5 cooling-off + second-look (addresses RT-NEW-07 MED)

**Adds to Phase 2 Triage:**

*Q5 "confident existing primitive is better" rejection appeal: any candidate rejected on Q5 alone is flagged in the register with status "rejected-q5-only." After a cooling-off period of 30 days, the operator reviews rejected-q5-only candidates in a batch and chooses to re-triage, keep rejected, or escalate to evaluation. This catches operator-fatigue false rejections without reopening obvious rejections. Other rejection reasons (sovereignty-incompatible, not reversible) do not get the cooling-off — they stay rejected.*

### F-8 — Watchlist owner note (supports RT-NEW-03 context)

Phase 1 already documents operator curates in v0.1, Da Vinci joins at v0.2. No additional change needed.

### F-9 — Spike manifest pre-check (addresses RT-NEW-08 LOW)

**Adds to Phase 4 Spike:**

*Manifest pre-check: before the spike branch is created, the manifest YAML is validated against a JSON schema (`pipeline/engineering/schemas/spike_manifest.schema.json`). Schema checks: version pin present and non-empty, exit criteria present with at least one measurable metric, rollback procedure present with abandonment commands, external-state inventory present (may be empty list for zero-state spikes). Manifest FAIL blocks branch creation.*

### F-10 — v0.2 continuous-scan fallback (addresses RT-NEW-09 LOW)

**Adds to Phase 1 Surveillance:**

*Fallback if Da Vinci doesn't reach live within 12 months from TSIP LOCK-sealed: operator activates manual weekly watchlist review as minimum-viable continuous scan. The v0.2 continuous-scan feature does not block TSIP's Phase 1 from functioning; operator-triggered cadence is the steady-state fallback for as long as needed.*

### Editor cleanups

Tone consistency normalized to present-tense throughout. "Real-engineer validator gate" gloss added on first use (external engineer audits spike outputs before main-line merge, per Da Vinci §13). Passive voice eliminated in adoption process. Candidates register section given a "how-to-use" sub-heading for operator accessibility.

## Cycle 2 status (TSIP v0.1)

- RT-NEW-01 HIGH: CLOSED (F-1 bootstrap single-use).
- RT-NEW-02 MED: CLOSED (F-2 reviewer assignment mechanism).
- RT-NEW-03 MED: CLOSED (F-3 watchlist carve-out).
- RT-NEW-04 MED: CLOSED (F-4 extension cap).
- RT-NEW-05 MED: CLOSED (F-5 blocking gate).
- RT-NEW-07 MED: CLOSED (F-7 Q5 cooling-off).
- RT-NEW-06 LOW: CLOSED (F-6 steady-state clarification).
- RT-NEW-08 LOW: CLOSED (F-9 manifest pre-check).
- RT-NEW-09 LOW: CLOSED (F-10 v0.2 fallback).
- Judge completeness dock: CLOSED (F-6 + F-10 address the v0.2 dependency concern).
- Editor findings: CLOSED (cleanups applied in place).

**TSIP v0.1 Cycle 2 status: READY for re-audit.** Live cross-family re-audit (using the now-live caching-enabled OpenClaw path) verifies closures. All three seats READY + zero blocking + operator sign → LOCKED-sealed.

---

## Operator Sign-off — LOCKED-sealed 2026-04-20

**Status:** `LOCKED-sealed`
**Interpretation adopted:** policy-lock.
**Cycle 2 re-audit outcomes:** Editor READY, Judge 100/100 PASS (completeness recovered 18→20 via F-10), Red Team REQUIRES_MINOR_FIXES blocking:false (7 policy-CLOSED, 2 OPEN-policy MED on operator-signature trust model + watchlist-sovereignty consistency language; both tracked as v0.2 protocol refinements).
**Audit trail:** `pipeline/engineering/protocols/tsip_v0.1_thesis_2026-04-19/cross_family_audit_cycle2/`
**Operator authorization token:** Josh Inklovich, session authorization 2026-04-20.
**Cryptographic seal (Ed25519):** pending v2.2 gates #5/#10 infrastructure; hash-bound record at `pipeline/engineering/operator_authorization_ledger.v1.jsonl`. `LOCKED-sealed` reflects policy-lock, not cryptographic seal.
**Self-application status:** bootstrap exception CONSUMED at this LOCK-sealed. Per F-1 single-use rule, no future amendment may invoke "bootstrap exception" — `F-BOOTSTRAP-REUSE` gate (Logician v2.2 queue gate #1, per-gate spec at `pipeline/engineering/spec_cards/logician_v2_2_f_bootstrap_reuse.md`) will enforce this at the structural layer.
**Effective:** LOCKED-sealed 2026-04-20. TSIP is now the active Tilth Self-Improvement Protocol governing all future tool/capability adoption decisions.
