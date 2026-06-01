---
title: Agent Context Index — what each root wake-up file is for
filed: 2026-05-17
scope: navigation only — files referenced here are not relocated by this index
status: collaborator-facing
companion: docs/COLLABORATOR_HANDOFF.md · docs/LOCAL_DEVELOPMENT.md · docs/TECHNICAL_BACKLOG.md
front_door: PROJECT_STATUS.md (root, sister doc)
---

# Agent Context Index

## Why this file exists

The repo root holds ten or so single-purpose files — `SOUL.md`, `USER.md`,
`AGENTS.md`, `CLAUDE.md`, `MEMORY.md`, `README.md`, `lessons.md`,
`IDENTITY.md`, `SKELETON.md`, `HEARTBEAT.md`, `TOOLS.md` — plus the
architecture and blueprint trees under `pipeline/`. On first read this looks
like clutter; in practice each file has a specific reader, a specific
purpose, and (for the agent-facing ones) a specific position in the
wake-up sequence defined in `AGENTS.md`.

Earlier cleanup drafts proposed grouping the root files into an `agent/`
subdirectory. That move was reversed in the v1.1 cleanup plan: too many
bootstrap chains and agent prompts hard-code the root paths, so a cosmetic
relocation would break working machinery for a navigation win. The v1.1
discipline is *leave the files where they are; add an index*. This file is
that index.

A newcomer (technical collaborator, candidate reviewer, future-Josh after a
long context-break) should be able to read this page and know, without
opening every file, which one answers which question. For the live status
view, read `PROJECT_STATUS.md` first; this index assumes you've already
done that or know to.

## The wake-up sequence (from `AGENTS.md`)

Every agent entering the workspace runs this sequence before accepting its
first task. Order is non-optional.

1. `SOUL.md` — workspace-wide operating principles
2. `USER.md` — operator identity, working style, locked decisions
3. `router.yaml` — current seat-to-model bindings
4. The last two daily logs under `daily_logs/`
5. `lessons.md` — accumulated operational lessons (mandatory pre-checks)
6. `MEMORY.md` — the memory index
7. Agent-specific overrides (under the relevant agent folder)
8. Task-specific `PROJECT_CONTEXT.md` for the targeted client org

Only after steps 1–8 does the agent respond.

## File-by-file

### `SOUL.md` — Five Laws + Four Autonomy Rules (canonical)

The workspace-wide operating principle layer. Holds the canonical text of
the Five Operating Laws (RFA-Is-Truth, No-Boundary-Drift, Org-Isolation,
Apolitical-Language-With-Admin-Risk-Scanning, Applicant-Brings-Substance)
and the Four Autonomy Rules (Save-State-Always, Test-Your-Own-Work,
Be-Explicit, Clean-Output). Also names the Sovereignty Promise and points
at `router.yaml` for model bindings.

*Read by:* every agent on wake-up (step 1). Operator updates it when a
principle changes. Collaborators reference it for the Laws; they do not
modify it casually — text changes to the Five Laws are a LOCKed-discipline
event (see the v7.0.12 apolitical_dialect amendment line for the most
recent precedent).

### `USER.md` — operator identity and decision framework

Josh's identity, working style, decision framework, and locked v0.1 scope
decisions. Tells an agent who Josh is, how he works (underspecifies
intentionally, prefers dialogue over deliverables, push-back is welcome,
he does not code), and what is closed from re-litigation (no LangGraph, no
Managed Edition, no UI layer for v0.1, no PA Ag Innovation Grant as
dogfood target, 128 GB RAM production floor, two-audit cycle).

*Read by:* every agent on wake-up (step 2). Operator-only file. Collaborators
read it to calibrate tone and to learn what *not* to propose; they do not
edit it.

### `AGENTS.md` — wake-up sequence + invocation hygiene

The entry point. Defines the wake-up sequence above, plus three big
discipline blocks: path-references-not-content-dumps (L-002), cross-family
review (reviewer's model family must differ from author's, L-003), and
the Section E single-Claude carve-out (logged-failure-only, not a
fallback). Also covers the Cowork → osascript → openclaw gateway bridge
pattern (the operating default for cross-family Thesis dispatch), caching
discipline, org-namespacing preamble, BYOK posture for client deployments,
and the mandatory session-close self-check.

*Read by:* every agent (this file *is* the entry point). Operator + agent
authors maintain it. Collaborators read it to understand how cross-family
auditing works on this codebase.

### `CLAUDE.md` — Cowork-specific supplement to AGENTS.md

A supplement, not a replacement. Repeats the wake-up reminder, then loads
Cowork-specific context that other agents don't need: the product naming
chain (Golden Quill / Tilth / Cultivator / Sovereign Node), the Six
Customer Identity Categories, the paired Eight Capital Logic Cards, the
two FIT Farms roles (Commons owner-role vs. LLC client-role), the Three-
Posture Beta routing model (Frontier-Eligible / Split-Context Hybrid /
Local-Only-Sovereign per v7.0.10 LOCKED), the seat roster, session-
efficiency rules, the test-interpreter pin (Python 3.14 via
`.venv/bin/python3` — see `docs/LOCAL_DEVELOPMENT.md` for the full setup
path), and the running What-Not-To-Do list.

*Read by:* Cowork agents specifically. The substrate of architecture
decisions a Cowork session needs to act correctly. Collaborators skim this
when context-switching from another part of the codebase — it's the
single best place to learn "what's currently true" without reading the
full architecture chain.

### `MEMORY.md` — memory layer index

Index of where institutional and agent memory lives. Four layers:
institutional (`lessons.md` + `pipeline/institutional_memory/lessons.json`),
agent-scoped (Tilth's `Sovereign_Node_Handoff/memory/`, Sentinel's
`HeartbeatQAfiles/`), session-scoped (the Cowork host's own memory at
`~/Library/...`), and daily operational log (`daily_logs/`). Also indexes
the LOCKed amendment surfaces (the Tier-1 amendment ledger, the GPP
mechanism, the engineering-persona prompt, the architecture amendment
chain).

*Read by:* every agent on wake-up (step 6). Collaborators read it as a
navigation map for "where is X recorded." Operator-maintained; do not edit
without operator coordination.

### `README.md` — public-facing front door

The first page anyone outside the operator sees. Names what Golden Quill
is, what Tilth is, the current v0.1 Beta status, what the v0.1 Beta ships
(capability table), the white-glove onboarding flow, the Phase One /
Phase Two roadmap, the Five Operating Laws (public phrasing), the six-
seat council, the three-posture deployment model, the Sovereignty
Promise, hardware tiers, the Customer Identity Categories, and the
repository structure.

*Read by:* anyone — newcomers, candidate collaborators, paying-customer
tech reviewers. Operator-curated; collaborators may propose polish via PR
(safe-first-task per `docs/TECHNICAL_BACKLOG.md`) but should not change
product claims without `docs/RUNTIME_MATURITY_MATRIX.md` backing.

> The README's "What to read first" block (Track 2 of the cleanup plan
> v1.1) is the planned front-link to this index. Once it lands in
> `README.md`, arriving here from there, you proceed next to
> `PROJECT_STATUS.md` (live state) and `RUNTIME_MATURITY_MATRIX.md`
> (what each subsystem is actually doing). Until the README polish
> lands, this index is reachable via direct link only.

### `lessons.md` — institutional lessons (canonical, human-readable)

The pre-check log. Each `L-NNN` entry names a repeat pattern Josh wants
agents to check *before* repeating the mistake. High-frequency + high-
severity entries are mandatory pre-checks on wake-up (step 5). Examples
include L-001 (Scout must hit live APIs, not cached spreadsheets), L-002
(prompt hygiene — path references, never content dumps), L-003 (cross-
family review), L-005 (two-audit cycle, not three-round silent revision),
L-006 (verify enforcement-layer existence on disk before locking around
it), L-023 (yaml-comment-only edits to LOCKed cards do NOT require
supersession).

*Read by:* every agent on wake-up. Lessons are append-mostly; the
machine-readable mirror at `pipeline/institutional_memory/lessons.json`
stays in sync. Collaborators reading this page get a fast read of "what
has gone wrong before on this codebase and how it was fixed." This is the
canonical `/lessons.md` at the repo root — not the older
`pipeline/lessons.md` (if any reference points there, it's stale).

### `pipeline/SESSION_BOOTSTRAP.md` — session orientation

The bootstrap file referenced from every handoff prompt. Compresses the
project universe — identity, file locations, locked decisions, active
constraints — so handoffs can say "Read `pipeline/SESSION_BOOTSTRAP.md`
for project orientation" instead of pasting the full context. Per L-002,
this is how cross-session handoffs stay cheap.

*Read by:* any agent receiving a handoff prompt. Updated when the project
universe changes (new locked decision, file relocation, posture shift).
Collaborators read it once and reference it forever after.

### `pipeline/architecture/v0.1/` — architecture trail

The "what" of the system. `tilth_architecture_locked.md` is the canonical
v7 architecture LOCKED 2026-04-19 (A1–A12); the v7.0.x amendment line
walks the corrections forward through `_v7_0_1_amendment.md` (Section E.P
Governance Plan Preflight) up through `_v7_0_12_apolitical_dialect_amendment.md`
(retires the four-axis political enum, registers F-DIALECT-*). Earlier
historical snapshots (`tilth_architecture_locked_v4_…`, `_v5_r8_…`,
`_v6_r2_…`, `_v7_a1_a6_…`) are preserved for prior-art and audit.

*Read by:* engineers and collaborators reasoning about subsystem
boundaries, failure-code families, posture rules, or substrate choice.
The architecture trail is LOCKed; amendment files are not edited in place.

### `pipeline/blueprint/v0.1/` — blueprint chain

The "how" of the system — one canonical file per section (§0.5 interface
index, §1 sovereignty envelope, §2 vault topology, §3 Scout, §4 Logician,
§5 pipeline, §6 operating envelope, §7 Scribe, §10 Red Team, §11 Intake,
§12 Uploader, §13 Data Collector, §14 Report Generator, §15 Archivist,
§16 Reflection Packet, §17 WPFA, §18 Cards), each carrying its amendment
chain. The §0.5 paired-commit discipline keeps the interface index
synchronized with every section amendment (LOCK ceremonies write paired
rows; the most recent monotonic position was v32 at OD-E on 2026-05-17).
LOCKed amendment files are not edited in place — see Track 4 of the
cleanup plan v1.1 for the discipline. The forthcoming
`pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md` (sister doc, Track 2
item 2) names the current head amendment for each section.

*Read by:* engineers landing runtime changes; collaborators tracing why a
behavior exists. Operator-led LOCK ceremonies extend the chain.

## Where to go next

- For the live state of every subsystem: `PROJECT_STATUS.md` (root,
  sister doc; "what works today" / "what's parked" / "what needs
  engineering judgment").
- For maturity labels on each subsystem (the seven-state vocabulary —
  `runtime-live` / `gate-live` / `asset-signed` / `spec-locked` /
  `schema-scaffold` / `dormant` / `historical`):
  `RUNTIME_MATURITY_MATRIX.md` (repo root, not `docs/`).
- For the local setup path (Python ≥ 3.11 venv, install, lint, test):
  `docs/LOCAL_DEVELOPMENT.md`.
- For role clarity (who owns what, what the collaborator should and
  should not touch): `docs/COLLABORATOR_HANDOFF.md`.
- For the ordered work queue: `docs/TECHNICAL_BACKLOG.md`.

This file will front-link from the README's "What to read first" block
once Track 2 of the cleanup plan v1.1 lands that block in `README.md`.
As of 2026-05-17 the README does not yet carry the block; this index is
reachable via direct link until the README polish lands.
