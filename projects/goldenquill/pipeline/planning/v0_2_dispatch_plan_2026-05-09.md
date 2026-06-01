---
title: V0.2 (Reporting Vertical) Dispatch Plan — Code + Cowork workstreams
filed: 2026-05-09
operator: Josh
parent_memo: pipeline/planning/v0_2_agents_punch_list_2026-05-09.md
authority: Josh 2026-05-09 ("voice channel for data collector - yes. Telegram/whatsapp. lets generate a comprehensive plan to give to dispatch to run in code and cowork.")
purpose: Hand-dispatchable workstream packets for v0.2 reporting vertical agent build. Each packet is copy-paste-ready as a Code or Cowork session handoff. Master plan tracks decisions, sequencing, and cross-cutting threads.
---

# 1. How to use this plan

Each numbered workstream (WS-A through WS-N) is a self-contained dispatch packet. Each packet declares: session type (Code or Cowork), prerequisites, scope, handoff prompt, time estimate. The handoff prompt is the copy-paste payload that opens a fresh session — it references SESSION_BOOTSTRAP.md and this master plan by path, never re-encoding context.

**Dispatch order:** follow the sequencing graph in §3. Workstreams in the same dependency tier are parallel-eligible. Workstreams across tiers respect the listed prerequisites — opening a downstream WS before its prereqs LOCK is a planning failure, not a flexibility choice.

**Decision gates:** §2 carries the rolling decisions log. Some workstreams are blocked on a Josh-only decision (marked **Operator-decision-required-first**). Resolve those before dispatching the packet.

**Cross-cutting threads (§5):** every WS observes the same testing discipline, classification routing posture, and CIC × CLC orthogonality invariant. The threads are not their own packets; they are constraints every packet inherits.

**Status check at v0.2 production cut:** §6 is the readiness checklist. Cut v0.2 when every box is green.

# 2. Decisions log (rolling)

## Resolved 2026-05-09

- **8a Voice channel for Data Collector v0.2 — YES.** Data Collector channels at v0.2 first ship: email + SMS + voice. Full TCPA exposure accepted. Voice substrate decision (Twilio Voice / operator-pinned PSTN gateway / local-Whisper-class transcription) lands in WS-I §13.4.
- **8b Telegram + WhatsApp in Data Collector — YES (interpretation; confirm if mistaken).** Data Collector channels at v0.2 first ship now total: email + SMS + voice + Telegram + WhatsApp. Cultivator-vs-Data-Collector substrate split flagged as a sub-decision in WS-I §13.5 — both could share a Telegram MTProto bot framework but consent ledgers + target audiences are distinct (Cultivator = operator's own employees; DC = external grantees + sub-awardees).

## Remaining (deferred to in-flight WS resolution)

- **8c Foundation portal adapter scope for Uploader v0.1.** Decision required by WS-F open. Default: ship top-N adapters (Common Grant Application + Foundant + Submittable + Fluxx) plus copy-paste fallback for everything else.
- **8d Archivist pull-forward degree.** Decision required by WS-K open. Default: spec-only at v0.2; implementation deferred to v1.x; operator-driven cadence in the interim.
- **8e Sub-awardee identity verification model for Data Collector.** Decision required by WS-I open. Default: per-recipient shared-secret token at award acceptance, embedded in every outbound message; inbound responses validate the token.
- **8f State-law layering for Data Collector.** Decision required by WS-I open. Default: SN-LLC ships state-rules card (PA / CA / FL / TX / NY at v0.2 first wave); other states operator-curated until SN-LLC adds them.
- **8g CIC × CLC orthogonality preservation in v0.2 substrate.** Confirmation rather than decision — every new schema and prompt template gets audited against F-CIC-CLC-COUPLING-VIOLATION at WS-E/F/I/J/K LOCK. Default: confirmed; auditing is a Thesis Team line item per WS.
- **8h Original proposal commitments rubric extraction owner.** Decision required by WS-I or WS-J open. Default: Intake third mode (AWARD-INGEST) added in WS-E; happens at award acceptance time.
- **8i Report Generator track-binding granularity.** Decision required by WS-J open. Default: monolithic `report_mode` track + sub-section prompt templates inside.
- **8j Report period-N comparison context.** Decision required by WS-J open. Default: pull fresh from KFR + operational data; do not load prior period draft as Scribe context.

Defaults stand if Josh does not override at the WS open. Each WS packet's open-questions section explicitly enumerates the defaults so the dispatched agent works against locked-in assumptions, not silent ambiguity.

# 3. Workstream dependency graph

```
        WS-A  v7.0.6 SELF-LOCK (roster) ◄── DONE 2026-05-09 (legacy-tier session)
            │
            └──→ WS-A-Review  4.7 audit pass on WS-A ◄── verification, single session
                  │
                  ├──→ WS-B  v7.0.7 Thesis + LOCK (classification routing) ◄── parallel-eligible with C, D
                  ├──→ WS-C  v7.0.4 Thesis + LOCK (KFR + Intake module)    ◄── parallel-eligible with B, D
                  └──→ WS-D  v7.0.5 Thesis + LOCK (Funder Intel + Match DB) ◄── parallel-eligible with B, C
            
        WS-A-Review CONFIRM
            │
            └──→ WS-F  §12 Uploader blueprint round (does NOT need C/D)
        
        WS-C LOCK
            │
            └──→ WS-E  §11 Intake blueprint round (depends on C only)
        
        WS-B + WS-C + WS-D all LOCKed
            │
            ├──→ WS-G  §5 v6 spin (track registry adoption)            ◄── Code+Cowork
            ├──→ WS-H  §2 v7.2 spin (operational-data sub-kinds)       ◄── Code+Cowork; parallel with G
            └──→ WS-L  §4 Logician v2.x (new gate families)            ◄── parallel with G, H
        
        WS-G + WS-H LOCKed
            │
            ├──→ WS-I  §13 Data Collector blueprint + module scaffold  ◄── Code+Cowork
            ├──→ WS-J  §14 Report Generator blueprint + module scaffold ◄── Code+Cowork
            └──→ WS-K  §15 Archivist blueprint round (parallel; spec-only at v0.2)
        
        Each LOCK
            │
            └──→ WS-M  §0.5 v6+ Interface Index amendment (paired with each WS LOCK)
        
        All v0.2 sections LOCKed + WS-N integration tested
            │
            └──→ v0.2 production cut
```

Tier 0: WS-A (v7.0.6 SELF-LOCK) — DONE 2026-05-09 on legacy tier
Tier 0.5: WS-A-Review (4.7 best-eyes verification on WS-A) — gates Tier 1
Tier 1: WS-B + WS-C + WS-D (parallel) — gated on WS-A-Review CONFIRM
Tier 2a: WS-F (depends on WS-A-Review CONFIRM only — can run during Tier 1)
Tier 2b: WS-E (depends on C)
Tier 3: WS-G + WS-H + WS-L (parallel after B/C/D)
Tier 4: WS-I + WS-J + WS-K (parallel after G/H)
Tier 5: WS-N (integration testing)
Tier 6: v0.2 production cut
Cross-tier: WS-M (paired with every LOCK)

# 4. Workstream packets

## WS-A: v7.0.6 SELF-LOCK

**Session type:** Cowork
**Prerequisites:** v7.0.6 SCOPING DRAFT exists (it does, at `pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md`).
**Operator-decision-required-first:** None (v7.0.6 is roster-only, SELF-LOCK candidate per its own preamble).
**Estimated wall time:** 30–45 min.

**Handoff prompt:**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-A for this packet's scope.
Read pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md.

Task: SELF-LOCK v7.0.6 (council + support-agent roster).
Scope: textual roster amendment only. Zero mechanism change. Reconcile canonical seat lists with router.yaml on-disk reality (Red Team) and name new agents (Uploader, Intake) for v0.1 plus reserve v0.2 + v1.x slots.
Companion edits to land in same commit:
  - README.md Council table: 5 rows → 6 (add Red Team).
  - README.md: add new "## Support Agents" section.
  - docs/ARCHITECTURE_OVERVIEW.md: Five Seats → Six Seats; new Support Agents section.
  - CLAUDE.md: "five-seat AI council" → "six-seat AI council plus support agents."
  - pipeline/architecture/v0.1/tilth_architecture_locked.md: Section A council enumeration adds Red Team; mark v7.0.6 as source.
LOCK ceremony: lock_history.v1.jsonl row append per existing pattern. Memory file under memory/project_architecture_v7_0_6_locked.md. MEMORY.md prepended.
Done definition: amendment status = "SELF-LOCKED 2026-05-08" (filing date) updated to "SELF-LOCKED 2026-05-09" (lock date); all five companion files edited and committed; lock_history row appended; memory file written; MEMORY.md updated; daily_log appended.
```

**Internal notes:** v7.0.6 is the lightest of the four amendments — pure roster reconciliation. Should land in one session. Unblocks WS-B/C/D + WS-F.

**Status (2026-05-09):** SELF-LOCKED 2026-05-09 in a Cowork session running on a legacy model tier. Amendment status updated, 5 companion files committed, cleanup pass executed across 17 additional active canonical files, lock_history row 176 appended, memory file written, MEMORY.md prepended, daily_log appended. Best-eyes verification pass scheduled as WS-A-Review (next packet).

## WS-A-Review: 4.7 audit of WS-A SELF-LOCK + cleanup pass

**Session type:** Cowork (single-pass verification, no Thesis Team needed — verification, not new authorship)
**Model (pinned 2026-05-09):** Cowork **Opus 4.7** OR Code **4.7 max effort**. WS-A landed on a legacy-tier model; this pass is the best-eyes verification before WS-B opens and starts citing v7.0.6.
**Prerequisites:** WS-A LOCKED (it is, 2026-05-09).
**Operator-decision-required-first:** None.
**Estimated wall time:** 30–45 min single session.

**Handoff prompt:**
```
# RUN ON: Cowork Opus 4.7 OR Code 4.7 max effort. Confirm model tier BEFORE pasting this handoff. This is a best-eyes verification pass on work landed by a legacy-tier session.

Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-A and §WS-A-Review for context.
Read pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md (the SELF-LOCKED amendment).
Read memory/project_architecture_v7_0_6_locked.md (the memory file written at LOCK).
Read daily_logs/2026-05-09.md (the WS-A entries — both initial LOCK and cleanup-pass paragraphs).
Read the lock_history row appended by WS-A: tail -1 pipeline/engineering/lock_history.v1.jsonl (row 176, lock_class=architecture_amendment, module=pipeline.architecture.v0_1.architecture_v7_0_6_amendment).

Task: Verification audit on the WS-A SELF-LOCK + cleanup pass. NOT a new amendment, NOT a Thesis round. Single-pass review with three failure-class probes:

(1) MISSED CANONICAL UPDATES — search for remaining "five.seat", "Five.seat", "five seats", "Five seats" across the workspace. For every hit, classify:
    - Active canonical (operating principles, identity, blueprints, skills, current planning, customer-facing) → MUST be updated; flag as defect if not done
    - Immutable history (daily_logs from prior days, versioned architecture snapshots like *_v[4-7]_*.md, validation/audit-trail snapshots, point-in-time external-review packets, _quarantine_for_deletion) → MUST be left untouched; flag as defect if WS-A edited
    - Different concept (5-reviewer Code Thesis Committee, NOT the council) → leave alone; flag as defect if WS-A "fixed" it as a council reference
    - Quoted historical text in amendment-diff records (the v7.0.6 amendment quoting prior wording it's replacing) → MUST be left as-is; flag as defect if WS-A edited
    - Memory/daily-log records describing the WS-A edits → expected and correct
  Reference: WS-A daily_log paragraph enumerates the 17 active files updated and the categories left untouched.

(2) ACCIDENTAL HISTORY EDITS — for every file listed in WS-A daily_log under "Updated", confirm it's in the active-canonical category. For every file under "Left untouched", grep-verify the file still contains the original "five-seat" wording (i.e., we did NOT silently edit history).

(3) MATH / QUOTE DRIFT — for every active-canonical edit:
    - Check the seat enumeration in the new wording matches the v7.0.6 canonical lineup: Scout, Scribe, Editor, Judge, Red Team, Logician (six seats; LLM count is five since Logician is deterministic).
    - Check that "v7.0.6 SELF-LOCKED 2026-05-09" cite is present where appropriate (not required everywhere, but the amendment file itself + the memory file + the lock_history row + the daily_log MUST agree on the date).
    - Check that the support-agent roster, where mentioned, lists exactly: Intake (v0.1), Uploader (v0.1), Data Collector (v0.2), Report Generator (v0.2), Archivist (v1.x). Five support agents.
    - Spot-check tilth_architecture_locked.md line 1120 (the math-error fix the WS-A cleanup made — "Five-seat" → "Six-seat" while listing six seats). Confirm the current text is "Six-seat council architecture (Scout / Scribe / Editor / Judge / Red Team / Logician — per v7.0.6 SELF-LOCKED 2026-05-09)".

Output format: a structured findings report at pipeline/validation/v7_0_6_review_<date>/findings.md with three sections (Missed Canonical Updates, Accidental History Edits, Math/Quote Drift). Each finding gets severity (BLOCKING / NON-BLOCKING / INFO) + remediation (file path + exact edit needed).

If zero BLOCKING findings: append a CONFIRM row to lock_history.v1.jsonl with lock_class="amendment_review", parent_lock_row=176, model_tier="opus_4_7" (or "code_4_7_max"), verdict="CONFIRMED". Update memory/project_architecture_v7_0_6_locked.md with a "Verification" footer naming the review session date + reviewer-model + verdict. Append to daily_log.

If any BLOCKING findings: do NOT append a CONFIRM row. File the findings report; daily_log the open defects; surface to operator for triage. WS-B remains unblocked at the planning layer (v7.0.6's textual content is sound even with companion-file gaps), but operator decides whether to fix-and-re-verify before opening WS-B.

Done definition: findings report filed; if clean, CONFIRM row appended + memory + daily_log; if defects, defects logged + daily_log surfaces them. Either way, this packet closes in one session.
```

**Internal notes:** This is a verification packet, not authorship. Cheaper than a Thesis round (no cross-family cycle, no fixes-and-reaudit). The point is to catch any defect WS-A's legacy-tier model could have missed BEFORE that defect propagates into WS-B's Thesis round (which will cite v7.0.6 as parent_lock). If WS-A-Review finds something blocking, WS-B should wait. If clean, WS-A-Review's CONFIRM row is the green light.

## WS-B: v7.0.7 Thesis round + LOCK

**Session type:** Cowork (drives Thesis Team via existing dispatch pattern)
**Model (pinned 2026-05-09):** Cowork **Opus 4.7** OR Code **4.7 max effort**. Substantive amendment — three new mechanisms, cross-family rigor, load-bearing routing primitive. Do not run on a legacy or default-tier model; shallow audits ship hidden defects.
**Prerequisites:** WS-A LOCKED.
**Operator-decision-required-first:** None at v0.2 plan level. The classification-driven routing pattern is the operator directive 2026-05-08; the amendment formalizes it.
**Estimated wall time:** 2 sessions (Audit #1 driver + Audit #2 verification per L-005 two-audit cycle).

**Handoff prompt:**
```
# RUN ON: Cowork Opus 4.7 OR Code 4.7 max effort. Confirm model tier BEFORE pasting this handoff.

Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-B for this packet's scope.
Read pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md.

Task: Thesis round on v7.0.7 (Beta classification-driven routing + Classification Review stage + on-demand heavy-Judge swap + per-deployment router.yaml derivation).
Cycle structure: L-005 two-audit. Audit #1 driver = Editor + Judge + Red Team via cross-family dispatch (Editor=Llama/Groq; Judge=Gemini-2.5-Pro/Google; Red Team=GPT-OSS-120B/Groq; never share family with the architecture's Anthropic-authored draft). Audit #2 verification after author fixes.
LOCK at unanimous READY_TO_LOCK across all three reviewers.
Companion edits at LOCK: router.yaml becomes per-deployment template; CLAUDE.md adds Beta model strategy section; ARCHITECTURE_OVERVIEW.md classification-driven routing diagram; skills/scribe-ghostwriter/SKILL.md Phase 0 RFA Extraction extension; section_07_scribe.md classification-aware-split-context formalization; section_05_pipeline.md revision-loop accommodation.
Done definition: v7.0.7 LOCKED status in amendment file; lock_history row; memory file; companion files edited; daily_log + session_metrics.
```

**Internal notes:** Heaviest of the three substantive amendments. Classification register is load-bearing for every other v0.2 agent. Red Team pass on the routing structure is critical — operator directive "we need the power with the privacy" is the rubric.

## WS-C: v7.0.4 Thesis round + LOCK

**Session type:** Cowork (drives Thesis Team)
**Model (pinned 2026-05-09):** Cowork **Opus 4.7** OR Code **4.7 max effort**. KFR is the load-bearing fact-substrate for Report Generator + Data Collector cross-validation; bad-number-ships paths are P0. Best-eyes review required.
**Prerequisites:** WS-A LOCKED.
**Operator-decision-required-first:** Decision 8h (proposal commitments rubric extraction owner). Default: Intake AWARD-INGEST mode.
**Estimated wall time:** 2 sessions.

**Handoff prompt:**
```
# RUN ON: Cowork Opus 4.7 OR Code 4.7 max effort. Confirm model tier BEFORE pasting this handoff.

Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-C for this packet's scope.
Read pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md.

Task: Thesis round on v7.0.4 (KFR per-org quantitative substrate + SP0 freshness review + F-LOGICIAN-FACT-DRIFT family + Intake module spec + Benchmarks Register).
Cycle structure: L-005 two-audit, cross-family per WS-B. Red Team pass is load-bearing — the entire amendment exists to prevent bad numbers from reaching funders; any path where a wrong number can ship is a P0.
Pre-LOCK additions to draft (per default decision 8h): add AWARD-INGEST as Intake's third mode in §5; AWARD-INGEST extracts proposal_commitments.yaml from won proposals at award acceptance time; landing this in v7.0.4 keeps Intake as the ingestion-discipline owner across BULK / INCREMENTAL / AWARD-INGEST modes.
Companion edits at LOCK: section_04_logician.md F-LOGICIAN-FACT-DRIFT POST-gate + tolerance config; section_05_pipeline.md SP0 stop-point + Intake invocation contract (3 modes); skills/scribe-ghostwriter/SKILL.md Phase 1 KGIE KFR cross-check; orgs/_TEMPLATE/vault/kfr/ schema templates; vault_shared/benchmarks/ register + initial seed.
Done definition: v7.0.4 LOCKED; lock_history; memory; companion files edited; AWARD-INGEST mode formalized in Intake spec; daily_log + session_metrics.
```

**Internal notes:** KFR is the substrate Report Generator pulls from + the cross-validation surface for Data Collector inbound. Without v7.0.4 LOCK, WS-I and WS-J cannot open.

## WS-D: v7.0.5 Thesis round + LOCK

**Session type:** Cowork
**Model (pinned 2026-05-09):** Cowork **Opus 4.7** OR Code **4.7 max effort**. Match Database is the most Law-3-sensitive register in the architecture; cross-org leak paths are P0. Best-eyes review required.
**Prerequisites:** WS-A LOCKED.
**Operator-decision-required-first:** None at v0.2 plan level (consent tier defaults already set in the amendment).
**Estimated wall time:** 2 sessions.

**Handoff prompt:**
```
# RUN ON: Cowork Opus 4.7 OR Code 4.7 max effort. Confirm model tier BEFORE pasting this handoff.

Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-D for this packet's scope.
Read pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md.

Task: Thesis round on v7.0.5 (Funder Intelligence Database + Match Database + Scout channel family G + Stage-5 cooperative on-ramp + Archivist curation-slot binding).
Cycle structure: L-005 two-audit, cross-family per WS-B. Red Team pass is critical — Match Database is the most Law-3-sensitive register in the architecture; any cross-org leak path is a P0.
Companion edits at LOCK: section_03_scout.md channel family G + Match DB de-dup integration + KFR required_for_funder query; section_04_logician.md F-MATCH-DB-CROSS-ORG + F-FUNDER-CORPUS-STALE + F-FUNDER-CORPUS-INTEGRITY gates; section_05_pipeline.md Match DB lifecycle + quarterly curation cadence + Stage-5 consent tier handling; vault_shared/funder_intelligence/ register + initial seed (USDA, NSF, regional foundation 990-PFs); orgs/_TEMPLATE/match_database/ register + consent_tier defaults.
Done definition: v7.0.5 LOCKED; lock_history; memory; companion files edited; daily_log + session_metrics.
```

**Internal notes:** Archivist's curation slot is reserved here. WS-K Archivist depends on this LOCK to know what it's curating.

## WS-E: §11 Intake blueprint round

**Session type:** Cowork
**Prerequisites:** WS-A LOCKED + WS-C LOCKED.
**Operator-decision-required-first:** None — defaults from §5 punch-list memo §5.1 stand.
**Estimated wall time:** 3 sessions (2 Thesis + 1 fixup).

**Handoff prompt:**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-E for this packet's scope.
Read pipeline/planning/v0_2_agents_punch_list_2026-05-09.md §5.1 (Intake punch list).
Read pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md §5 (Intake module spec).
Reference framework: pipeline/templates/component_analysis_template.md.

Task: Author §11 Intake blueprint (claim section number §11 in §0.5 Index).
Three modes: BULK (folder drop at onboarding), INCREMENTAL (single new doc on arrival), AWARD-INGEST (extract proposal_commitments.yaml from won proposals at award acceptance — added per decision 8h default).
Substrate: FAISS or Chroma + bge-large-en-v1.5 + Pydantic AI tool composition + Mistral 7B class local LLM. Always-local routing (touches mixed-classification raw org docs).
Logician gate owned: F-EXTRACTOR-FABRICATION (PRE pre-queue — verbatim source_quote validation).
Open questions enumerated in §5.1: BULK-mode operator review UX (batch-confirm by source doc / confidence-threshold autopromote / pure manual); INCREMENTAL trigger (filesystem watcher / operator-explicit / both); migration of existing PROJECT_CONTEXT [NEEDED] fields (Intake at first operator review post-LOCK / one-shot script).
Cycle structure: L-005 two-audit. Cross-family per WS-B.
Companion edits at LOCK: §0.5 Interface Index v6 amendment claiming §11 row + Intake primitive rows; orgs/_TEMPLATE/intake/inbox/ scaffold; pipeline/orchestrator/seats/intake.py module scaffold (Code, paired commit).
Done definition: §11 Intake blueprint LOCKED; lock_history; memory; companion files edited; module scaffold passes AST-lint; daily_log + session_metrics.
```

**Internal notes:** Module scaffold (`pipeline/orchestrator/seats/intake.py`) is Code work; can split into a sub-packet if Cowork-only blueprint authorship is faster without the code. Recommendation: same packet, since the blueprint's interface contract is more concrete with the module skeleton already in place.

## WS-F: §12 Uploader blueprint round

**Session type:** Cowork
**Model (pinned 2026-05-09):** Cowork **Opus 4.7** OR Code **4.7 max effort**. Per-portal adapter design + auto-submit fail-closed gate is the operator-accountability boundary; defects ship as a federal-portal-ToS violation. Best-eyes review required.
**Prerequisites:** WS-A LOCKED.
**Operator-decision-required-first:** Decision 8c (foundation portal adapter scope). Default: top-N adapters (Common Grant Application + Foundant + Submittable + Fluxx) + copy-paste fallback.
**Estimated wall time:** 3 sessions.

**Handoff prompt:**
```
# RUN ON: Cowork Opus 4.7 OR Code 4.7 max effort. Confirm model tier BEFORE pasting this handoff.

Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-F for this packet's scope.
Read pipeline/planning/v0_2_agents_punch_list_2026-05-09.md §5.2 (Uploader punch list).
Reference framework: pipeline/templates/component_analysis_template.md.

Task: Author §12 Uploader blueprint (claim §12 in §0.5 Index).
Scope: end-of-cycle submission package assembly. Operator clicks final submit on funder portal — Uploader does NOT auto-submit (federal-portal-ToS + operator-accountability constraint, non-negotiable).
Adapter scope per decision 8c default: Grants.gov Workspace + SAM.gov + Common Grant Application + Foundant + Submittable + Fluxx + copy-paste fallback for unsupported portals.
Substrate: Pydantic AI orchestration over python-docx + pypdf + openpyxl + per-portal adapters (frozen at Golden Image per ADR-001; no marketplace).
Logician gates owned: F-UPLOADER-PACKAGE-INCOMPLETE, F-UPLOADER-FORMAT-MISMATCH, F-UPLOADER-AUTOSUBMIT-ATTEMPTED (fail-closed on any auto-submit code path), F-UPLOADER-SIGNATURE-MISSING.
Open questions enumerated in §5.2: format-conversion responsibility (Uploader owns docx-to-pdf or §6 publishes a utility); attachment provenance (where attachments live in vault — bleeds into §2 R.PF2).
Cycle structure: L-005 two-audit. Cross-family per WS-B.
Companion edits at LOCK: §0.5 v6 amendment §12 row; orgs/_TEMPLATE/uploader scaffold; pipeline/orchestrator/seats/uploader.py module scaffold + per-portal adapter modules under pipeline/orchestrator/seats/uploader_adapters/; tests/seats/uploader/ test suite.
Done definition: §12 Uploader blueprint LOCKED; module scaffold passes AST-lint; tests pass; lock_history; memory; daily_log + session_metrics.
```

**Internal notes:** Attachment vault location should be pinned here so WS-H §2 v7.2 spin can include the right sub-kind row. Coordinate WS-F LOCK with WS-H scoping.

## WS-G: §5 v6 spin (track registry adoption)

**Session type:** Code + Cowork
**Prerequisites:** WS-A + WS-B + WS-C + WS-D all LOCKED.
**Operator-decision-required-first:** None — R.PF1 architectural commitment is binding.
**Estimated wall time:** 4 sessions (2 Code refactor + 2 Cowork Thesis round).

**Handoff prompt (Code phase):**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-G for this packet's scope.
Read pipeline/architecture/v0.1/tilth_architecture_locked.md §R.PF1 (track registry pull-forward).
Read pipeline/blueprint/v0.1/section_05_pipeline.md (current LOCKED v6 — note: pre-track-registry).
Read pipeline/blueprint/v0.1/section_06_operating_envelope.md §6.1 (track-registry host schema).

Task: Refactor §5 Pipeline to consume the §6 track-registry abstraction.
Current state: §5 v6 hardcodes submission_mode and eval_mode; v0.2 needs report_mode as a registry row. R.PF1 commits §5 to a track-registry pattern such that adding a track is a router.yaml row + new prompt templates only.
Output: pipeline/orchestrator/loop.py refactored to dispatch by track-registry lookup; pipeline/blueprint/v0.1/section_05_v8_amendment.md draft (or section_05_pipeline.md v6→v7 amendment depending on extent of change).
Required §5 follow-on per architecture: registry lives in router.yaml under §6 Operating Envelope; each registry row binds (a) Scribe prompt template, (b) Judge rubric, (c) Red Team probe template, (d) vault subtree for output, (e) output schema. §5 itself becomes track-agnostic dispatcher.
Tests: existing §5 R11 capstone (8164 tests baseline) must remain green. Add new test class for track-registry dispatch with three tracks (submission, eval, report stub).
F-PIPELINE-TRACK-FROZEN PRE-gate (architecture-side dormant) activates against the §5 amendment LOCKED text at lock-time. Thesis Team audits the amendment against R.PF1 commitment.
Done definition (Code phase): refactor lands; full suite green (>=8164 + new tests); AST-lint clean; track-registry dispatch testable for three tracks.
```

**Handoff prompt (Cowork Thesis phase):**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-G Cowork phase.
Read the §5 amendment draft authored in WS-G Code phase.
Read pipeline/architecture/v0.1/tilth_architecture_locked.md §R.PF1.

Task: L-005 two-audit cycle on §5 amendment. Cross-family per WS-B. F-PIPELINE-TRACK-FROZEN architectural commitment is the audit rubric — does the amendment expose the registry such that report_mode (and content_mode and tdsl_query_mode) registers via row + prompt template only, or does the amendment hard-code a closed track set?
Done definition: §5 amendment LOCKED; lock_history; memory; companion §0.5 v6+ row updates; daily_log + session_metrics.
```

**Internal notes:** This is the highest-leverage workstream — once §5 supports the track registry, every v0.2 vertical (R.1 / R.2 / R.3) is a registry row away. WS-J Report Generator becomes much smaller because the orchestration is reused.

## WS-H: §2 v7.2 spin (operational-data sub-kinds)

**Session type:** Code + Cowork
**Prerequisites:** WS-A + WS-B + WS-C + WS-D all LOCKED.
**Operator-decision-required-first:** None — R.PF2 architectural commitment is binding.
**Estimated wall time:** 4 sessions.

**Handoff prompt (Code phase):**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-H for this packet's scope.
Read pipeline/architecture/v0.1/tilth_architecture_locked.md §R.PF2 (vault topology operational-data extensibility).
Read pipeline/blueprint/v0.1/section_02_vault_topology.md (current LOCKED v7.1).

Task: Extend §2 Vault topology with SIMPLE sub-kinds for operational data.
Sub-kinds to add: metrics, financials, photos, narrative_entries, timeline_of_activities, beneficiary_records, attachments (for Uploader per WS-F coordination).
Per sub-kind: Pydantic schema + Cedar policy gate + vault subtree path + admin-risk severity (beneficiary_records HIGH if PII present).
Output: pipeline/blueprint/v0.1/section_02_v7_2_amendment.md draft; pipeline/vault/sub_kinds/ Python modules per sub-kind; updated Cedar policies under pipeline/vault/policies/.
Tests: existing §2 R-K capstone tests must remain green. Add per-sub-kind round-trip tests (write + read + Cedar enforcement).
F-VAULT-ARTIFACT-ONLY PRE-gate (architecture-side dormant) activates against the §2 amendment LOCKED text at lock-time. Thesis Team audits.
Done definition (Code phase): sub-kinds land; full suite green; AST-lint clean; per-sub-kind round-trip tests pass; Cedar policies enforce PII discipline on beneficiary_records.
```

**Handoff prompt (Cowork Thesis phase):**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-H Cowork phase.
Read the §2 amendment draft authored in WS-H Code phase.

Task: L-005 two-audit cycle on §2 amendment. Cross-family per WS-B. F-VAULT-ARTIFACT-ONLY architectural commitment is the audit rubric — does the amendment expose the schema for operational data extensions, or does it reject extensions at the schema level?
Beneficiary records audit emphasis: PII discipline + admin-risk severity + consent-tier handling.
Done definition: §2 amendment LOCKED; lock_history; memory; §0.5 v6+ row updates; daily_log + session_metrics.
```

**Internal notes:** Beneficiary record schema is the touchiest piece — Data Collector writes them, Report Generator reads them, and they may carry PII. Cedar policy enforcement is non-negotiable.

## WS-I: §13 Data Collector blueprint + module scaffold

**Session type:** Code + Cowork (multi-pass)
**Prerequisites:** WS-G + WS-H + WS-L all LOCKED.
**Operator-decision-required-first:** Decision 8e (sub-awardee identity verification — default: shared-secret token) + Decision 8f (state-law layering — default: SN-LLC ships PA/CA/FL/TX/NY at v0.2 first wave).
**Estimated wall time:** 6 sessions (1 spec + 3 Code modules + 2 Thesis).

**Handoff prompt (Spec + Cowork phase):**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-I for this packet's scope.
Read pipeline/planning/v0_2_agents_punch_list_2026-05-09.md §5.3 (Data Collector punch list).
Reference framework: pipeline/templates/component_analysis_template.md.

Task: Author §13 Data Collector blueprint (claim §13 in §0.5 Index).
Channels (per Josh 2026-05-09): email + SMS + voice + Telegram + WhatsApp.
Sub-decision flagged: Cultivator-vs-Data-Collector substrate split. Recommendation in blueprint: shared MTProto / Telegram bot framework substrate, distinct consent ledgers, distinct target audiences (Cultivator = operator's own employees opt-in by employment; DC = external grantees + sub-awardees with formal consent capture). Surface this for operator confirmation at Audit #1.
Outreach engine: SMTP via operator BYOK (Postmark / SendGrid / Mailgun); Twilio or equivalent for SMS + voice; MTProto bot for Telegram; WhatsApp Business API for WhatsApp. All BYOK. Frozen at Golden Image build per ADR-001.
Consent ledger: per-recipient per-channel; CAN-SPAM unsubscribe links on every email; TCPA prior-express-written-consent on every SMS or voice; per-state layering (PA/CA/FL/TX/NY at v0.2 first wave per decision 8f default; SN-LLC ships state-rules card; operator opts in per state).
Sub-awardee identity verification per decision 8e default: shared-secret token at award acceptance, embedded in every outbound message; inbound responses validate the token. Token rotates per grant cycle.
Voice substrate: Twilio Voice gateway for outbound; local Whisper-class model for transcription on inbound (always-local per classification routing); voice prompts authored in classification-aware-split-context (template = Public+Shareable; per-recipient slot-fill = local).
Response intake: email-thread parser; SMS short-form parser; Twilio Studio-equivalent flows for structured prompts; voice transcription pipeline; Telegram bot inbound handlers; WhatsApp inbound handlers.
Field validation: per-collected-data-point Pydantic schema + KFR cross-check (F-DATACOLLECTOR-KFR-DRIFT advisory).
Logician gates owned: F-DATACOLLECTOR-CONSENT-MISSING, F-DATACOLLECTOR-OPT-OUT-ACTIVE, F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED, F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND, F-DATACOLLECTOR-KFR-DRIFT, F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET.
Cycle structure: L-005 two-audit. Cross-family per WS-B. Red Team pass is critical — TCPA / CAN-SPAM / state-law violations are real legal exposure for the operator.
Companion edits at LOCK: §0.5 v6+ amendment §13 row; orgs/_TEMPLATE/data_collector/ scaffold; pipeline/orchestrator/seats/data_collector/ module tree (multi-module per channel); tests/seats/data_collector/ test suite.
Done definition: §13 blueprint LOCKED; module scaffold compiles; tests pass; consent-ledger Cedar policies enforced; lock_history; memory; daily_log + session_metrics.
```

**Handoff prompt (Code phase — channel modules):**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-I Code phase.
Read pipeline/blueprint/v0.1/section_13_data_collector.md (LOCKED in spec phase).

Task: Implement Data Collector channel modules.
Modules to author:
  pipeline/orchestrator/seats/data_collector/__init__.py
  pipeline/orchestrator/seats/data_collector/email_channel.py (SMTP via BYOK provider)
  pipeline/orchestrator/seats/data_collector/sms_channel.py (Twilio)
  pipeline/orchestrator/seats/data_collector/voice_channel.py (Twilio Voice + Whisper transcription)
  pipeline/orchestrator/seats/data_collector/telegram_channel.py (MTProto bot)
  pipeline/orchestrator/seats/data_collector/whatsapp_channel.py (WhatsApp Business API)
  pipeline/orchestrator/seats/data_collector/consent_ledger.py
  pipeline/orchestrator/seats/data_collector/state_rules_card.py
  pipeline/orchestrator/seats/data_collector/inbound_parser.py
  pipeline/orchestrator/seats/data_collector/field_validator.py
Each channel module implements a common ChannelProtocol (Protocol-DI per existing pattern). consent_ledger enforces CAN-SPAM/TCPA at the gate. state_rules_card ships PA/CA/FL/TX/NY rules at v0.2 first wave.
Tests: per-channel unit tests; cross-channel integration tests; consent-violation pre-gate tests; state-rules-card per-state tests; full-suite green required.
Done definition: all modules land; AST-lint clean; per-channel + cross-channel tests pass; full suite green; daily_log + session_metrics.
```

**Internal notes:** The substrate decisions (Twilio vs Plivo, Postmark vs SendGrid) need BYOK clarity — operator's BYOK envelope at white-glove. State-rules card is the highest-maintenance piece and the most-likely-to-need-updates as state laws evolve. SN-LLC ships updates per its router-template-update commitment.

## WS-J: §14 Report Generator blueprint + module scaffold

**Session type:** Code + Cowork
**Prerequisites:** WS-G + WS-H + WS-I + WS-L all LOCKED.
**Operator-decision-required-first:** Decision 8i (track-binding granularity — default: monolithic) + Decision 8j (period-N comparison — default: pull fresh).
**Estimated wall time:** 4 sessions.

**Handoff prompt:**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-J for this packet's scope.
Read pipeline/planning/v0_2_agents_punch_list_2026-05-09.md §5.4 (Report Generator punch list).
Read pipeline/blueprint/v0.1/section_05_pipeline.md (track registry — LOCKED in WS-G).

Task: Author §14 Report Generator blueprint (claim §14 in §0.5 Index).
Architectural shape: Report Generator is a TRACK in §6 track-registry, not a brand-new agent. Same five council seats run on report_mode with different prompt templates and the original-proposal-commitments rubric in place of the funder rubric.
Per decision 8i default: monolithic report_mode track + sub-section prompt templates inside (narrative / metrics-table / financial-summary / photo-gallery / beneficiary-section).
Per decision 8j default: pull fresh from KFR + operational data; do not load prior period draft as Scribe context. Trend narrative surfaces only on operator approval.
Inputs: orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/ (Data Collector output); orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml (extracted at award time per Intake AWARD-INGEST mode); orgs/<slug>/vault/grants/<grant_id>/reporting_template.yaml; KFR; Funder Intelligence DB.
Outputs: orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/draft_<v>.md + signed claim_evidence_map.
Logician gates owned: F-REPORT-COMMITMENT-UNTRACED, F-REPORT-COMMITMENT-MISSED, F-REPORT-OUT-OF-SCOPE-DRIFT, F-REPORT-NUMERIC-DRIFT, F-REPORT-TEMPLATE-MISMATCH.
Cycle structure: L-005 two-audit. Cross-family per WS-B.
Companion edits at LOCK: §0.5 v6+ amendment §14 row; router.yaml report_mode track-registry row + Scribe report prompt template + Judge proposal-commitments rubric + Red Team report probe template; pipeline/orchestrator/tracks/report_mode.py module; tests/tracks/report_mode/ test suite.
Done definition: §14 blueprint LOCKED; track registers in §6; full suite green with new track-mode tests; lock_history; memory; daily_log + session_metrics.
```

**Internal notes:** Smaller than §13 because the orchestration is inherited from §5 v6 + §6 track registry. The work is mostly authoring the new prompt templates + the new rubric + the gate family, not re-architecting orchestration.

## WS-K: §15 Archivist blueprint round

**Session type:** Cowork (spec-only at v0.2 per decision 8d default; implementation deferred to v1.x)
**Prerequisites:** WS-G + WS-H LOCKED (need the operational-data sub-kinds + track registry to spec curation against).
**Operator-decision-required-first:** Decision 8d (Archivist pull-forward degree) — default: spec-only at v0.2.
**Estimated wall time:** 3 sessions.

**Handoff prompt:**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-K for this packet's scope.
Read pipeline/planning/v0_2_agents_punch_list_2026-05-09.md §5.5 (Archivist punch list).
Read pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md §9 (curation slot reservation).
Read pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md §6 (curation slot binding).
Reference framework: pipeline/templates/component_analysis_template.md.

Task: Author §15 Archivist blueprint (claim §15 in §0.5 Index). Spec-only at v0.2 per decision 8d default; v1.x implementation deferred. Operator-driven cadence in the interim.
Scope: long-running between-cycle preservation. Distinct from Editor (clarity-during-drafting) by time horizon and substrate.
Inputs (read-mostly): vault_shared/funder_intelligence/, orgs/<slug>/match_database/, orgs/<slug>/vault/kfr/, pipeline/institutional_memory/lessons.json, vault_shared/benchmarks/, orgs/<slug>/vault/grants/<grant_id>/reports/.
Outputs: operator-facing digests (quarterly curation digest per workspace; per-org KFR refresh digest; Match Database lessons-delta proposals; lessons.json patches as proposals).
Cadences: weekly tick (light — KFR expiry / pending-facts / Match DB delta / lessons append); quarterly review (heavy — Funder Intel promotion-or-drop / Match DB outcome rollup / Benchmarks Register freshness / lessons.json proposed diffs).
Logician gates owned: F-ARCHIVIST-CROSS-ORG-LEAK, F-ARCHIVIST-LESSON-INSTANCE-LEAK, F-ARCHIVIST-AUTO-APPLY-ATTEMPTED, F-ARCHIVIST-CADENCE-DRIFT.
Boundary discipline: Archivist proposes, never auto-applies. Operator confirms every change. Editor stays Editor. Logician stays Logician.
Cycle structure: L-005 two-audit. Cross-family per WS-B.
Companion edits at LOCK: §0.5 v6+ amendment §15 row; archivist seat skeleton at pipeline/orchestrator/seats/archivist/__init__.py with a stubbed implementation note ("v1.x; operator-driven cadence in v0.2"); operator-facing digest templates under orgs/_TEMPLATE/archivist_digests/; tests/seats/archivist/skeleton_tests.py validating the stub does not auto-apply.
Done definition: §15 spec LOCKED; stub passes AST-lint; skeleton tests confirm proposes-only discipline; lock_history; memory; daily_log + session_metrics.
```

**Internal notes:** This is the agent Josh specifically named. Spec-only at v0.2 keeps the design coherent without committing to implementation maintenance until v1.x. The skeleton tests are non-negotiable — they prevent any future contributor from quietly turning the stub into auto-apply behavior.

## WS-L: §4 Logician v2.x amendment for new gate families

**Session type:** Code + Cowork
**Prerequisites:** WS-A + WS-B + WS-C + WS-D LOCKED.
**Operator-decision-required-first:** None.
**Estimated wall time:** 3 sessions.

**Handoff prompt:**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-L for this packet's scope.
Read pipeline/blueprint/v0.1/section_04_v2_2_consolidated_amendment.md (latest §4 LOCKED amendment — format pattern).

Task: Author §4 Logician v2.x amendment registering all v0.2 gate families.
Gates to register (estimated ~25 across the v0.2 set):
  KFR family (per WS-C v7.0.4): F-LOGICIAN-FACT-DRIFT, F-FACT-DRIFT-UNTRACED, F-FACT-DRIFT-OUT-OF-TOLERANCE, F-FACT-DRIFT-EXPIRED, F-FACT-DRIFT-DERIVATION-UNAUTHORIZED, F-EXTRACTOR-FABRICATION
  Funder Intel family (per WS-D v7.0.5): F-MATCH-DB-CROSS-ORG, F-MATCH-DB-CONSENT-TIER-VIOLATION, F-FUNDER-CORPUS-STALE, F-FUNDER-CORPUS-INTEGRITY
  Uploader family (per WS-F): F-UPLOADER-PACKAGE-INCOMPLETE, F-UPLOADER-FORMAT-MISMATCH, F-UPLOADER-AUTOSUBMIT-ATTEMPTED, F-UPLOADER-SIGNATURE-MISSING
  Data Collector family (per WS-I): F-DATACOLLECTOR-CONSENT-MISSING, F-DATACOLLECTOR-OPT-OUT-ACTIVE, F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED, F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND, F-DATACOLLECTOR-KFR-DRIFT, F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET
  Report Generator family (per WS-J): F-REPORT-COMMITMENT-UNTRACED, F-REPORT-COMMITMENT-MISSED, F-REPORT-OUT-OF-SCOPE-DRIFT, F-REPORT-NUMERIC-DRIFT, F-REPORT-TEMPLATE-MISMATCH
  Archivist family (per WS-K): F-ARCHIVIST-CROSS-ORG-LEAK, F-ARCHIVIST-LESSON-INSTANCE-LEAK, F-ARCHIVIST-AUTO-APPLY-ATTEMPTED, F-ARCHIVIST-CADENCE-DRIFT
Per gate: failure code; PRE/POST sequence position; deterministic Cedar policy or Python predicate; enforcement test; documentation row.
Code phase: pipeline/logician/gates/f_*.py per gate; tests/logician/gates/test_f_*.py per gate.
Cowork phase: §4 amendment authored as section_04_v2_x_amendment.md; PRE-gate precedence table updated; existing F-AMDT-* structural enforcement gates extended for new gate registrations.
Cycle structure: L-005 two-audit. Cross-family per WS-B.
Done definition: §4 amendment LOCKED; all ~25 gates implemented + tested + documented; full suite green; lock_history; memory; daily_log + session_metrics.
```

**Internal notes:** Largest single chunk of code work in v0.2. Each gate is small but there are ~25 of them; gate test coverage discipline is the L-002 pattern from §4 v2.2 consolidated amendment.

**Post-LOCK note (2026-05-10):** WS-L §4 v2.x LOCKed at 2026-05-10T20:45:00Z (compound-LOCK rows 193/194 with §0.5 v14 amendment; ~44 failure codes; v0.1 Beta architectural gate cleared). After LOCK, the §15 Archivist external-review disposition packet (`pipeline/planning/section_15_external_review_disposition_2026-05-10.md`) surfaced one PARTIAL closure (Tilth-RT-07) that originally pointed to the WS-L handoff prompt for the `R-ARCHIVIST-NO-CANONICAL-MUTATE` AST-lint enumeration extension to cover low-level rename primitives (`os.replace` / `os.rename` / `shutil.move` / `shutil.copy*` / `os.link`). Because the WS-L LOCK ceremony had already closed, the addendum could not ride this LOCK. Dispatch coordinator filed the §2.1 addendum text as seed for a future **§4 v2.x.1 corrective amendment** in `pipeline/planning/section_04_v2_x_1_tilth_rt_07_backlog_2026-05-10.md`. The backlog packet is dispatchable as-is (~1 session, L-005 two-cycle cadence, full live cross-family rigor matching WS-L posture). Bounded by v7 A1+A4 in the interim. Disposition row in `pipeline/engineering/lock_history.v1.jsonl` row 195 (lock_class=`external_review_disposition`; verdict=DISPOSITIONED; parent_lock_row=192).

## WS-M: §0.5 v6+ Interface Index amendments (paired with each LOCK)

**Session type:** Cowork (paired-commit pattern per §6.17 Option-B)
**Prerequisites:** Each individual LOCK that requires an Interface Index row addition.
**Operator-decision-required-first:** None.
**Estimated wall time:** 30 min per paired commit.

**Handoff prompt template:**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-M for this packet's scope.
Read pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md (current §0.5 LOCK).
Read the LOCKED section authored in WS-<X>.

Task: §0.5 paired-commit row append for WS-<X>.
Section number(s) being claimed: §<NN> (and any sub-rows).
Per-row contents per §0.5.2: kind, owner section, name, signature, schema reference, dependent sections.
Update §0.5 v<N>.json (machine-readable) + section_00_5_interface_index_locked.md (human-readable).
Compound transaction with WS-<X> LOCK per §6.17 Option-B paired-commit pattern.
Done definition: §0.5 v<N+1> amendment LOCKED in same commit as WS-<X> LOCK.
```

**Internal notes:** Reserve §11 / §12 / §13 / §14 / §15 in the first §0.5 amendment after WS-A LOCK to avoid renumbering churn. Subsequent paired commits add the per-section interface rows as each blueprint LOCKs.

## WS-N: Integration testing + v0.2 production cut readiness

**Session type:** Code + Cowork
**Prerequisites:** WS-A through WS-M all LOCKED.
**Operator-decision-required-first:** None.
**Estimated wall time:** 3 sessions.

**Handoff prompt:**
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-N for this packet's scope.
Read pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §6 (production cut readiness checklist).

Task: Integration testing for v0.2 production cut.
End-to-end test scenarios:
  1. White-glove onboarding: Intake BULK ingest of seeded org corpus → KFR populated → Classification Review stage → first grant cycle eligible.
  2. Award acceptance: Intake AWARD-INGEST extracts proposal_commitments.yaml from a won proposal.
  3. Active reporting cycle: Data Collector outreach to seeded sub-awardees across all five channels (email + SMS + voice + Telegram + WhatsApp); inbound responses parsed; operational data lands in §2 sub-kinds.
  4. Report generation: Report Generator pulls operational data + KFR + proposal_commitments → drafts report → council review (Scribe / Editor / Judge / Red Team / Logician on report_mode) → signed claim_evidence_map.
  5. Submission: Uploader assembles submission package + portal-format conversion; operator clicks final submit on funder portal.
  6. Between-cycle: Archivist weekly tick + quarterly curation review (operator-driven at v0.2 per decision 8d default).
Each scenario authored as integration test under tests/integration/v0_2/. Run on real Tilth dev node (M1 8GB Mac Mini) to confirm v0.1 hardware-floor compatibility per Sovereignty Promise (if v0.2 runs on 8GB it flies on 128GB).
Test data: seeded test client under orgs/_test_v0_2_/ with fabricated-but-plausible substance (no real client data; Law 3 strict).
Done definition: all six scenarios pass on dev node; full suite green; AST-lint clean; CIC × CLC orthogonality regression tests pass (F-CIC-CLC-COUPLING-VIOLATION on every new schema/template); v0.2 production cut readiness checklist (§6) all green; daily_log + session_metrics.
```

**Internal notes:** This is the gating workstream for v0.2 cut. Failures here block the cut. Real-hardware test (M1 8GB) is the Sovereignty Promise test — if v0.2 needs more hardware than v0.1, that's a new ADR.

# 5. Cross-cutting threads (every WS observes)

## 5.1 Testing discipline (per L-005 two-audit + AST-lint + full-suite-green)

Every WS that touches code:
- Runs the full pytest suite via `.venv/bin/python3 -m pytest` (NOT system python3 — see CLAUDE.md "Running tests — PINNED INTERPRETER").
- Adds tests for new code paths (per Rule 2 "test your own work"); skipped tests are debt, not coverage.
- Passes AST-lint R1-R7 (exit 0) before any LOCK ceremony.
- Records test deltas in session_metrics (`tests_added` + `full_suite_tests_green` + `full_suite_preexisting_failures`).
- Test files follow existing pattern: tests/seats/<seat>/, tests/tracks/<track>/, tests/logician/gates/, tests/integration/v0_2/.

## 5.2 Classification routing posture (per v7.0.7)

Every new agent declares routing posture explicitly:
- Always-local: Intake, slot-fill agent, Logician, Archivist, Data Collector outbound composition (Confidential payload), Data Collector inbound storage.
- Cloud-routable when input is Public + Shareable: Scribe (grant + report), Editor, Judge, Red Team, Scout per channel.
- Per-call decision: per v7.0.7 §1, every agent call evaluates input classification and routes accordingly. No agent unilaterally decides; the classification register is load-bearing.

## 5.3 CIC × CLC orthogonality (per v7.0.8 LOCK)

Every new schema and prompt template gets audited against F-CIC-CLC-COUPLING-VIOLATION at LOCK:
- No CIC field implies a CLC subset.
- No CLC field implies a CIC subset.
- Match logic is opportunity-driven runtime, never archetype-driven design-time.
- Four detection layers (lexical regex / Pydantic AST / value-set / KP schema) all pass before LOCK.

## 5.4 Law 3 (Org Isolation) discipline

Every new register schema, agent prompt template, and operator-facing digest:
- Declares per-org or workspace-scoped.
- If per-org: Cedar policy enforcement at the read path; no cross-org reads possible without operator override + admin-risk ledger.
- If workspace-scoped: explicit invariant that the schema carries no per-org content (e.g., Funder Intelligence DB is per-funder factual; classification-register defaults are workspace; both are Law 3-safe).

## 5.5 Memory + daily_log + session_metrics (per AGENTS.md Save-On-Decide + Session Close)

Every WS session:
- Writes daily_log entry on the same day as work.
- Writes session_metrics JSONL line at session close per `pipeline/metrics/SESSION_METRICS_SPEC.md`.
- Updates memory under `memory/` for any non-obvious decision or correction; prepends MEMORY.md index entry.
- Saves on decide, not on close. Decisions don't batch.

## 5.6 Cross-family rigor (per architecture §E + AGENTS.md "Cross-family review")

Every WS that drives Thesis Team:
- Editor: Llama 3.3 70B on Groq (Meta family).
- Judge: Gemini 2.5 Pro (Google family).
- Red Team: GPT-OSS 120B on Groq (OpenAI-OSS family) with GPT-5.1 escalation.
- Author (Cowork): Claude Sonnet 4.6 / Opus 4.7 (Anthropic family).
- No reviewer shares family with the author.
- Use full provider/model-id form per AGENTS.md (`openclaw infer model run --gateway --model groq/openai/gpt-oss-120b ...`).

# 6. v0.2 production cut readiness checklist

When every box is green, v0.2 ships.

**Architecture:**
- [ ] v7.0.6 SELF-LOCKED (WS-A)
- [ ] v7.0.7 LOCKED (WS-B)
- [ ] v7.0.4 LOCKED (WS-C)
- [ ] v7.0.5 LOCKED (WS-D)

**Blueprint:**
- [ ] §11 Intake LOCKED (WS-E)
- [ ] §12 Uploader LOCKED (WS-F)
- [ ] §5 v<NN> track-registry adoption LOCKED (WS-G)
- [ ] §2 v7.2 operational-data sub-kinds LOCKED (WS-H)
- [ ] §13 Data Collector LOCKED (WS-I)
- [ ] §14 Report Generator LOCKED (WS-J)
- [ ] §15 Archivist spec LOCKED (WS-K)
- [ ] §4 Logician v2.x new gate families LOCKED (WS-L)
- [ ] §0.5 v6+ amendments paired with each LOCK (WS-M)

**Code:**
- [ ] All Logician gates implemented + tested
- [ ] Intake module scaffold + 3 modes implemented + tested
- [ ] Uploader module + portal adapters implemented + tested
- [ ] Data Collector channel modules (5 channels) + consent ledger + state-rules card implemented + tested
- [ ] Report Generator track-mode + sub-section templates + rubric implemented + tested
- [ ] Archivist skeleton (proposes-only) implemented + tested
- [ ] Track registry dispatching submission_mode + eval_mode + report_mode
- [ ] §2 sub-kinds (metrics + financials + photos + narrative_entries + timeline_of_activities + beneficiary_records + attachments) round-tripped via Cedar enforcement

**Integration:**
- [ ] WS-N six end-to-end scenarios pass on M1 8GB dev node
- [ ] CIC × CLC orthogonality regression tests pass on every new schema/template
- [ ] Full pytest suite green (>=8164 baseline + v0.2 tests)
- [ ] AST-lint R1-R7 clean across pipeline/ + tests/

**Operations:**
- [ ] Classification Review stage operator-runnable at white-glove
- [ ] State-rules card ships PA/CA/FL/TX/NY at first wave
- [ ] BYOK envelope documented for new providers (Twilio, Postmark/SendGrid, MTProto, WhatsApp Business API)
- [ ] First opted-in client identified for v0.2 R.3 reporting pilot (per architecture §R.3 — pilot client named only in their own PROJECT_CONTEXT, not in Tilth-core artifacts)

**Documentation:**
- [ ] README.md + ARCHITECTURE_OVERVIEW.md + CLAUDE.md updated for v0.2 surface
- [ ] White-glove onboarding playbook updated for Classification Review + AWARD-INGEST + Data Collector consent capture
- [ ] Operator runbook for v0.2 R.3 reporting cycle
- [ ] Open-decisions log §2 closed (every 8c-8j resolved or default-confirmed)

# 7. v8 watch list (when to escalate beyond v0.2)

The punch-list memo §9 named five v8 candidate concerns. v0.2 stays within v7.0.x amendments. Trigger v8 only if any of the following becomes blocking:

- Multi-track concurrent runtime (a client wants submission + report tracks running simultaneously, and operator-level scheduling lockout is insufficient).
- Multi-Tilth fleet operations (Stage 2 at twelve deployments) before Stage-5 commons is live.
- Cultivator integration if it strains v0.2's Data Collector substrate (the v0.2 plan keeps them separate substrates; merging is v8).
- Sandbox / parallel-compare orchestrator for multi-Card framing if a v0.2 client demands the reframer surface as a feature.
- R.1 TDSL substrate selection if a client asks for federated knowledge-base now.

If none of the above triggers, v8 waits.

# 8. Operator dispatch sequence (suggested)

Recommended order to dispatch packets for fastest critical-path completion:

1. **Today:** Dispatch WS-A (v7.0.6 SELF-LOCK) as a single Cowork session. Light load, unblocks three downstream parallels.
2. **WS-A LOCKED:** Dispatch WS-B + WS-C + WS-D + WS-F in parallel (four sessions). WS-F unblocks early because it depends on A only.
3. **WS-C LOCKED:** Dispatch WS-E.
4. **WS-B + WS-C + WS-D all LOCKED:** Dispatch WS-G + WS-H + WS-L in parallel. Heaviest tier.
5. **WS-G + WS-H LOCKED:** Dispatch WS-I + WS-J + WS-K in parallel.
6. **All blueprint sections LOCKED:** Dispatch WS-N integration.
7. **WS-N green:** v0.2 cut.

WS-M paired commits happen alongside each LOCK ceremony and don't gate dispatch.

Total estimated session count: ~38 sessions across the workstream tree (Tier 0 = 1; Tier 1 = 6; Tier 2 = 6; Tier 3 = 11; Tier 4 = 13; Tier 5 = 3; WS-M cross-tier = ~8 paired commits not counted separately). Realistic wall-clock: weeks-to-months at current cadence.

---

End of dispatch plan. Self-check + session metrics owed at session close per AGENTS.md §Session Close.
