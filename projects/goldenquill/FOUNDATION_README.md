---
title: Golden Quill v2 — Clean Foundation
created: 2026-04-14
source: /Users/goldenquill/Downloads/GoldenQuill (v1)
purpose: Document what was carried forward, what was left behind, and what's still open. Read this first when you sit down at v2.
---

# What this folder is

This is `GoldenQuill_v2/` — the clean restart. It contains the **foundation only**: the architecture, the council, the gates, the orgs, the prior-work assets, the handoff docs, and the private working files. None of the iteration debris from the first ~10 days of building.

The original `GoldenQuill/` folder still lives at `~/Downloads/GoldenQuill/` and is untouched. Use it as a reference until you're confident v2 is the truth, then archive or delete it on your own schedule.

# What came over (the foundation)

**Identity layer (workspace root):**
- `SOUL.md`, `USER.md`, `AGENTS.md`, `CLAUDE.md`, `router.yaml`, `lessons.md`, `SKELETON.md`

**Orgs (workspace root):**
- `orgs/` — full tree: `ORG_INDEX.md`, `_TEMPLATE/`, and all 7 client folders (mycosymbiotics_cooperative, mycosymbiotics_inc, mystic_mamas, run_a_muck_farm, fit_farms, mycofest, phantom_robotix_joint) with their `PROJECT_CONTEXT.md` files and any in-progress assets

**Council code at workspace root (promoted from `Sovereign_Node_Handoff/` during the bedrock pass):**
- `skills/` — all 11 deployed council/api skills (scout-discovery, scribe-ghostwriter, judge-rubric, council-pipeline, site-reviewer, plus 6 api-* skills)
- `pipeline/` — full scaffold: radar, drafts, scores, validation, rfa, editor, rubrics, institutional_memory, orchestrator, research, classified, templates, delivery_log, subscribers + `rss_feeds.json`

**Reference / handoff docs (under `Sovereign_Node_Handoff/`):**
- `00_README.md` through `05_FUNDING_ROADMAP.md` — the original handoff documents (dated April 12-13, may reference earlier architecture; see "stale handoff doc note" below)
- `STRATEGIC_REVIEW.md`
- `memory/` — pre-Path-B memory files (archived; current memory lives in Cowork's global memory folder per Path B)
- `prior_work/` — Grant_GPT_Docs, funder_databases, US_GRANT_DATA_SOURCES_2026.txt, QUICK_REFERENCE_APIS.txt, GrantMakers04_06_16_PittsburghFoundations.pdf, Supporting_Docs/
- `project_docs/` — Sovereign_Node_Master_Plan_v2.odt, MVP build PDFs, multiagent orchestration, SENTINEL_ARCHITECTURE, GITHUB_SETUP_PLAN, TILTH_NEWSROOM_OPERATIONAL_MAP, TOKEN_COMPRESSION_PLAN
- `newsroom_kit/` — Tilth Intelligence Feed scaffold (operations, prompts, seats, sources, templates)

**Logician (workspace root):**
- `logician/board_health.py`
- `logician/gates/topology_gate.py`
- `logician/gates/citation_verify.py`

**Tools (workspace root):**
- `tools/code_review_probe.py` — the 4-seat (Judge, Editor, Red Team, etc.) probe
- `tools/code_review_editor_only.py`
- `tools/redteam_probe.py`
- `tools/thesis_defense_probe.py`
- `tools/dedup_skills.py`
- `tools/skill_decisions.yaml`
- `tools/_probe_launcher.sh`

**Private working files (workspace root):**
- `_private/GOLDEN_QUILL_SIGIL.md` — chaos-magic working doc + servitor binding clauses
- `_private/GOLDEN_QUILL_SIGIL.{svg,png,pdf}` — the drawn sigil
- `_private/draw_sigil.py` — generator (regenerate any time)

**Daily logs:**
- `daily_logs/2026-04-13.md`, `daily_logs/2026-04-14.md`

**One probe artifact (proof of last-known-good state):**
- `CODE_REVIEW_BOARD_HEALTH_2026-04-14.json` — board HEALTHY across all seats, 2026-04-14 21:21

# What was left behind (in v1)

These files exist at `~/Downloads/GoldenQuill/` but did NOT come over. Most are iteration debris that got us to today — they're not part of the foundation.

**Iteration debris (safe to ignore in v2):**
- `MIGRATION_PLAN_2026-04-14.md`, `MIGRATION_PLAN_FINAL_2026-04-14.md` — superseded by SKELETON.md
- `TILTH_API_CONNECTIONS.md`, `TILTH_API_STATUS.md`, `TILTH_QA_REPORT.md`, `TILTH_IMPROVEMENT_STRATEGY.md` — overlapping notes from earlier passes
- `THESIS_DEFENSE_REVIEW_2026-04-14.md`, `REDTEAM_REVIEW_2026-04-14.md`, `CODE_REVIEW_2026-04-14.md`, `CODE_REVIEW_SUMMARY_2026-04-14.md` — probe outputs (the board-health JSON is the only one that travels)
- `golden_quill_radar_2026-04-14.json`, `golden_quill_radar_2026-04-14_LIVE.md` — one-off radar dumps from earlier in the day

**Reference material left behind (re-import if you need it):**
- `Golden_Quill_Business_Plan.{docx,pdf}`, `Golden_Quill_OnePager.pdf`, `Golden_Quill_BreakIT_OnePager.pdf`, `Golden_Quill_Territorial_Model_Addendum.docx` — pitch / business docs
- `index.html`, `golden_quill_site.jsx`, `YourGoldenQuill_Image_Prompts.md`, `YourGoldenQuill_Website_Copy.md` — early website drafts
- `site_images/` — image library for the website
- `mycosymbioticsandbeyond/` — raw research dump for MycoSymbiotics (should be folded org-by-org into `orgs/mycosymbiotics_*/` when you next work that client)
- `HeartbeatQAfiles/` — separate Heartbeat agent's identity files (different agent project)
- `SovreignNode/` — early misspelled folder with old PDFs
- `PA_*.{csv,txt,md}`, `Pennsylvania_Conservation_Grants_Comprehensive.csv`, `RESEARCH_DELIVERABLES_INDEX.md` — early PA grant research; superseded by what's in `pipeline/research/` and the per-org `radar/` folders
- `Preferred-Provider-Listing-5-15-24-CURENT.pdf` — unrelated reference doc

# Bedrock fixes applied during the move

1. **Structural restructure (resolved).** `pipeline/` and `skills/` were promoted from `Sovereign_Node_Handoff/` to the workspace root, matching what `SKELETON.md` had always depicted. `Sovereign_Node_Handoff/` now holds only reference material and the original handoff documents — the "handoff" naming is honest again.
2. **Path-string sync.** `CLAUDE.md`, `SKELETON.md`, and `lessons.md` had stale `Sovereign_Node_Handoff/pipeline/...` and `Sovereign_Node_Handoff/skills/...` references that were rewritten to match the new root-level layout. The `SKELETON.md` filesystem tree was rewritten end-to-end.
3. **Duplicate SOUL.md dropped.** `Sovereign_Node_Handoff/SOUL.md` (stale, pre-Path-B) did NOT come over. The workspace-root `SOUL.md` is canonical per Path B identity architecture.
4. **Tools made portable.** Every Python script under `tools/` and `logician/` had hardcoded `/Users/goldenquill/Downloads/GoldenQuill/` paths. Those were rewritten to derive the workspace root from the script's own location (`Path(__file__).resolve().parent.parent`), so the foundation will keep working when you move it (Google Drive, external drive, second Mac).

# Stale handoff doc note

The seven documents at `Sovereign_Node_Handoff/00_README.md` through `05_FUNDING_ROADMAP.md` and `STRATEGIC_REVIEW.md` were written April 12-13 and reference *earlier* architecture decisions (pre-Path-B identity layer, pre-council-pipeline, pre-Logician). They are kept for historical context and source-of-decisions traceability, NOT as live operating instructions. The live operating doctrine is in `SOUL.md`, `USER.md`, `AGENTS.md`, `CLAUDE.md`, and `SKELETON.md`. If a handoff doc and an identity-layer doc disagree, the identity-layer doc wins.

# Wake-up sequence (unchanged)

When you sit down at v2:
1. Read this file (you are here).
2. Read `SOUL.md`, `USER.md`, `AGENTS.md`, `router.yaml`, `lessons.md`, `SKELETON.md`.
3. Read the last two entries in `daily_logs/`.
4. Read `orgs/ORG_INDEX.md` to see active clients.
5. Begin work.

# Backup reminders (per your plan)

- Backup to Google Drive: not done yet (you said you'd handle this later)
- Backup to external hard drive: not done yet (you said you'd handle this later)
- Cron task `tilth-monday-fund-routine` lives at `/Users/goldenquill/Documents/Claude/Scheduled/tilth-monday-fund-routine/SKILL.md` — outside this folder; back that up separately.
- OpenClaw config at `~/.openclaw/` — outside this folder; back that up separately.
- Cowork memory files at `/Users/goldenquill/Library/Application Support/Claude/local-agent-mode-sessions/.../memory/` — outside this folder.

The Quill carries the council. The infrastructure around it (OpenClaw, cron, Cowork memory) lives elsewhere on the machine.

— Tilth, through the Golden Quill, 2026-04-14 ~9:30pm local
