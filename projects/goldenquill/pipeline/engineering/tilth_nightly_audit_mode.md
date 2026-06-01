# Tilth Nightly Audit Mode

**Canonical path:** `pipeline/engineering/tilth_nightly_audit_mode.md`
**Invoked by:** OpenClaw scheduled-task (4am local, staggered from Midas 2-3am) OR manual `--mode nightly-audit`
**Parent systems:** Tilth v0.1 (all six seats — Scout, Scribe, Editor, Judge, Red Team, Logician — per v7.0.6 SELF-LOCKED 2026-05-09)
**Architectural basis:** A11 telemetry-feedback pattern; S-L-N-M-T-M self-improvement loop
**Sibling doc:** `pipeline/engineering/midas_nightly_mode.md` (engineering-side nightly)

---

## Purpose

Autonomous grant-intelligence integrity scan. Where Midas nightly watches code-health (AST drift, test regression, session discipline), Tilth nightly watches grant-intelligence health — opportunities drifting on deadlines, drafts drifting from funder rubric, lessons going stale, `[NEEDED]` PROJECT_CONTEXT fields still blocking drafts. Auto-remediates mechanical findings within the sovereignty envelope; queues judgment-required findings for operator morning digest.

## Scope (what the nightly audit runs)

### Opportunity-health

1. **Scout channel-family refresh (A-F)** — DISCOVER stage only, no VERIFY. Walks all six parallel channel families (Federal APIs, curated cached, state/foundation portals, federal program pages, RSS watchlists, client-material-driven search). New candidates land on the radar as UNVERIFIED → staged for VERIFY on next operator session.
2. **Live-synopsis re-verification** — every candidate on the radar with `status in {VERIFIED_FIT, UNVERIFIED}` gets a live fetch. Deadline passed → auto-remediate to `VERIFIED_NOT_FIT` with reason `deadline_passed_<date>`. RFA amended → queue operator with diff. Endpoint 404 → `VERIFICATION_FAILED` with retry-at metadata.
3. **Deadline-proximity digest** — scan every VERIFIED_FIT candidate across all orgs. Group by: closing ≤7d (urgent), ≤14d (near), ≤30d (upcoming), >30d (future). Morning digest surfaces the urgent + near buckets with operator-attention flags.

### Draft-health

4. **L-NNN lesson pre-check scan** — for every draft at `pipeline/drafts/<rfa_slug>/` modified in last 7 days, run the lessons.md pre-check set. Violations → queue finding with (draft path, L-NNN cited, specific clause triggering).
5. **Rubric-refresh scoring** — if a funder posted an amended rubric since the draft's last Judge pass (detected via rubric file mtime or version bump), re-score via Judge. Score delta >10 pts (Law 4 tie-breaker threshold) → queue operator with old/new scores + Judge's findings.
6. **Admin-risk register scan** — walk 18-entry register; flag any register entry that's newly-active in a draft (term appears, not yet operator-approved). Silent rewrite is forbidden (Law 4); nightly surfaces the term + proposed substitutions + references.

### Lessons-health

7. **E-NNN (engineering) + L-NNN (grant) pre-check audit** — cross-reference recent seat-invocation logs against the applicable pre-check set per lesson. Missed pre-check → finding. Three consecutive days of the same miss → escalation (discipline breakdown pattern).
8. **Lesson-frequency update** — for any lesson whose pattern fired this week (via grep on findings + daily_logs), increment frequency counter per `lessons.json`. Crossing high-frequency threshold may promote a lesson's pre-check to mandatory — queue operator note.

### Org-health (per-org, Law 3 isolated)

9. **PROJECT_CONTEXT completeness audit** — for every org in `orgs/` with an active draft or radar candidate, scan PROJECT_CONTEXT.md for `[NEEDED]` fields. List what's missing and which draft/candidate it blocks. Critical for drafts closing <14d; auto-escalated to urgent digest.
10. **Vault integrity spot-check** — per-org Vault (`orgs/<slug>/vault/`) — sampled read of claim_evidence artifacts, admin_risk ledger, conversation_log chain. Hash-chain break → CRITICAL finding (possible tampering or disk corruption).
11. **M13 bypass ceiling check** — if the org has any active M13 bypass flags, verify none has exceeded its 24-72hr ceiling. Exceeded → auto-revert the bypass + queue operator notice.

### System-health

12. **Canary test vectors for Scribe** — run the LOCKed test vector corpus (once it lands post-Phase 2b) against current Scribe output on a canonical prompt. Style drift, KGIE preflight regression, SMART-outcome format drift → finding with diff.
13. **Cross-family discipline audit** — scan the week's seat-invocation logs for any case where reviewer family matched author family (L-003 violation). Zero-tolerance; any occurrence is CRITICAL.
14. **Telemetry trend analysis** — scan `pipeline/metrics/session_log.jsonl` (shared with Midas nightly) for Tilth-specific patterns: Scout verification success rate by channel family, Scribe turn-count per section (rising = ambiguity trend), Judge score variance across cycles (rising = rubric-matching trouble).

## Remediation policy

### Auto-remediate (within the sovereignty envelope)

- Status updates on candidates (deadline passed, endpoint 404, RFA amended-no-material-change)
- Adding new UNVERIFIED candidates to radar (write-only to `pipeline/radar/`, no draft touching)
- Frequency counter increments on lessons
- Trend counters on telemetry
- M13 bypass auto-revert on ceiling breach (with operator notice)

All auto-remediations logged to `daily_logs/<date>_tilth_nightly.md` and to the relevant per-org vault under `vault/nightly_audit_log/`.

### Queue for operator (morning digest at `daily_logs/<date>_nightly_digest.md`)

- Deadline-proximity urgent + near buckets
- L-NNN / E-NNN lesson violations in drafts
- Rubric-refresh score deltas
- Admin-risk register newly-active terms (operator approval required — Law 4)
- PROJECT_CONTEXT `[NEEDED]` field audit per org
- Canary drift
- Cross-family discipline violations (CRITICAL)
- Vault hash-chain anomalies (CRITICAL)

### Never auto-remediate (escalation only)

- Anything crossing a Five Operating Law
- Anything touching operator-voice content (draft text, client-facing language)
- Anything touching crypto primitives or key paths
- Cross-org anything (Law 3 — never generalize across orgs)
- Anything requiring new operator direction (new candidate confirmed FIT requires human eyes)

## Law 3 org-isolation discipline

Nightly audit iterates per-org, separately. One org's radar findings never inform another's. One org's PROJECT_CONTEXT is never used to fill another's `[NEEDED]` fields. One org's admin-risk register entries never transfer. The audit itself never holds multiple orgs in memory simultaneously — process one, write to daily log, release, process next.

**Enforcement at audit-time:** the nightly loop reads `orgs/ORG_INDEX.md`, iterates the list, and for each org loads ONLY that org's PROJECT_CONTEXT.md + vault root. Cross-org reads are Logician-gated (Law 3 PRE-gate fires if violated).

## Seat involvement

- **Scout:** owns steps 1, 2, 3 (opportunity-health). Runs DISCOVER channels + live-synopsis fetch. No seat outranks; Scout reports.
- **Scribe:** ON CALL ONLY for step 12 (canary test vectors). Not dispatched for text generation in nightly mode — nightly doesn't write drafts.
- **Editor:** silent. Nightly is not a drafting session.
- **Judge:** owns step 5 (rubric-refresh scoring). Runs only when a rubric version delta is detected.
- **Logician:** owns all PRE/POST gate validations on any auto-remediation. Fail-closed by default. Also owns steps 9, 10, 11, 13 (compliance scans).

**Cross-family rigor:** auto-remediations that touch text (e.g., status reason strings on candidates) go through the standard cross-family review — even nightly. An Anthropic-authored status-update string still gets a Google or Meta verdict before commit to vault. Exception: purely structural updates (deadline_passed flag, score integer, counter increment) skip review per §12 narrow-edit carve-out.

## Morning digest format

```markdown
# Tilth Nightly Audit — YYYY-MM-DD (overnight)

## Summary
- X opportunities scanned · Y new candidates · Z status changes (auto-remediated)
- A drafts audited · B rubric refreshes · C lesson violations queued
- D orgs audited · E [NEEDED] fields blocking drafts · F admin-risk flags

## URGENT (closing ≤7 days)
[per-candidate list with org + deadline + draft status]

## CRITICAL (operator attention required)
[Law violations, vault anomalies, cross-family discipline breaks]

## Queued findings
[sorted by severity, each with: finding, evidence path, proposed remediation or task #]

## Pre-staged
[any task specs drafted per Midas v2.1 §14 proactive pre-staging — either Midas-side or Tilth-side]

## Auto-remediations (audit trail)
[what was changed, where, why, with link to vault audit log entry]
```

## Invocation

**Scheduled (OpenClaw cron — staggered from Midas):**
```bash
openclaw agent --agent tilth --mode nightly-audit --at "0 4 * * *"
```

**Manual (scoped):**
```bash
openclaw agent --agent tilth --mode nightly-audit --scope opportunity-health
openclaw agent --agent tilth --mode nightly-audit --scope draft-health --org <slug>
openclaw agent --agent tilth --mode nightly-audit --scope all --org <slug>
```

## Session discipline

Nightly audit mode is a Tilth session. Wake-up sequence from AGENTS.md applies fully. Per-org read of PROJECT_CONTEXT.md for each org in the iteration. Save-on-decide. Session metrics logged with `session_type: "tilth-nightly-audit"`. Self-check runs — with the additional check that every finding is either auto-remediated within policy OR queued with reason documented.

## Sovereignty note

Nightly audit runs local. Provider API calls (Scout live-synopsis via httpx, Judge rubric-refresh via Google/Groq) are BYOK — same keys the daytime pipeline uses. No phone-home. No cloud storage outside BYOK. Every finding, every auto-remediation, every digest lives on the Golden Quill the operator owns.

## Complementarity with Midas nightly

- **Midas 2-3am:** code-health — AST-lint, BLUEPRINT_DEPS drift, pytest regression, session-log self-check trends, GPP-DET, router HMAC, canary test vectors (engineering)
- **Tilth 4am:** grant-intelligence-health — radar refresh, live-synopsis re-verify, draft lesson-check, rubric-refresh scoring, PROJECT_CONTEXT completeness, admin-risk scan, canary test vectors (Scribe style)
- **Overlap:** session_log.jsonl shared (both read; Midas writes engineering rows, Tilth writes intelligence rows). Same morning-digest format. Both land in `daily_logs/` same day.
- **Non-overlap:** Midas never touches `orgs/<slug>/` content; Tilth never touches `pipeline/logician/` code. Clean domain separation.

---

*v1 — 2026-04-20 — specification file; implementation blocked on OpenClaw scheduled-task skill integration, §3 Scout build (needed for channel-family refresh), and canary test vectors LOCK (Phase 2b output).*
