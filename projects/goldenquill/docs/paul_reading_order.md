---
title: Paul's Reading Order — the numbered tour
audience: Paul Norton (incoming Platform Engineer)
filed: 2026-05-18
status: living document — update when the tree shifts
sibling: docs/PAUL_DAY_ONE.md
---

# Paul's Reading Order

This is the master index. Read files in this order; each item has a one-line "what / why next" hook. Pure pointer doc — nothing moves, nothing changes, no LOCKed surfaces are touched. If the tree shifts, fix this file in the same PR that surfaces the gap.

The five-thing list inside `PAUL_DAY_ONE.md` is the **dense first read**; this file is the **full ordered tour**.

---

## Phase 0 — Orient yourself

1. **`docs/paul_reading_order.md`** — *you're here.* Numbered tour. Read this once end-to-end before opening anything else.
2. **`docs/PAUL_DAY_ONE.md`** — the compressed green-path. Welcome + 5-sentence project frame + first-commit warmup + three gotchas + skip-list.

## Phase 1 — What ships today

3. **`README.md`** — what the product is, what's `runtime-live` vs `spec-locked` vs `dormant`, the four required CI checks on `main`.
4. **`PROJECT_STATUS.md`** — dated one-paragraph-per-system snapshot, anchored to a `lock_history` row. Will go stale fast; trust the date stamp.
5. **`RUNTIME_MATURITY_MATRIX.md`** — the seven-state taxonomy. When any doc disagrees, this file wins. Internalize the seven labels.

## Phase 2 — Honest reads (external + internal)

6. **`docs/project_audit_2026-05-18.md`** — outside read at commit `65e841a`. §3 (onboarding friction this file compresses), §12 (risks ranked), §13 (the prioritized recommendation queue you'll pull from).
7. **`docs/CTO_HANDOFF_BRIEF.md`** — Josh's CTO-level handoff. §2 names the four CTO blind spots; blind spot D (operational freeze playbook) is yours. §4 distinguishes load-bearing from governance theater.
8. **`lessons.md`** — L-001..L-027. Append-only institutional memory. If a problem smells like a known shape, search here first.

## Phase 3 — Setup + role clarity

9. **`docs/LOCAL_DEVELOPMENT.md`** — the venv setup that gets you to a green test run. Python 3.14 local pin; macOS-default 3.9 is rejected. Read before your first PR.
10. **`docs/COLLABORATOR_HANDOFF.md`** — who owns what, the shared boundaries, do-not-touch surfaces, surfaces you can move fast on, the PR template.
11. **`docs/AGENT_CONTEXT_INDEX.md`** — map of every root personification file (`SOUL.md`, `USER.md`, `AGENTS.md`, `CLAUDE.md`, `MEMORY.md`, etc.) — what each is for and who reads it.
12. **`docs/TECHNICAL_BACKLOG.md`** — ordered work queue. Gate 1 blockers, Gate 2 blockers, safe first tasks, do-not-touch surfaces, needs-Josh-decision. Pull from "Safe first tasks" for your first PR.

## Phase 4 — Platform-engineer pack (full pack + daily-driver)

13. **`docs/platform_engineer_onboarding.md`** — the full operations-register handoff written for you specifically. Glossary, deployment topology, observability stack, test playbook, seat-by-seat runbook.
14. **`docs/platform_engineer_quick_reference.md`** — the 1-page daily driver. Bookmark.

## Phase 5 — How the architecture is shaped

15. **`docs/ARCHITECTURE_OVERVIEW.md`** — rendered architecture overview, ASCII flowchart, cross-cutting summary.
16. **`docs/decisions/ADR-001.md`** — the substrate decision: Pydantic AI + Logfire + Ollama/vLLM + DSPy/GEPA + Logician. Frozen at Golden Image build.
17. **`pipeline/architecture/v0.1/tilth_architecture_locked.md`** — v7 LOCKED 2026-04-19, A1–A12. The "WHAT." Do not edit in place; amendments only.
18. **`pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md`** — per-section current-head amendment + lock_history row + one-sentence purpose + maturity label. The blueprint directory reads as archaeology without this index.

## Phase 6 — Audit ledger + agent identity

19. **`pipeline/engineering/lock_history.v1.jsonl`** — the append-only architectural-change ledger. Don't read end-to-end; sample with `tail -20`. Rows 280–292 are the cards-publisher key rotation + OD-E fix-forward. See the shape, not the content.
20. **`AGENTS.md`** — the canonical wake-up sequence for any agent session. Memorize the order: SOUL → USER → router.yaml → daily_logs → lessons → MEMORY → agent overrides → PROJECT_CONTEXT.
21. **`SOUL.md`** — the Five Operating Laws (non-negotiable) + Sovereignty Promise. Operator-only edit surface; you read but do not modify.
22. **`USER.md`** — operator context: who Josh is, his register, what he's already won, what underspecification means.
23. **`CLAUDE.md`** — Cowork-specific supplement. Lots of project naming, taxonomy, locked decisions. Dense; skim once, return when a term in another doc isn't in `docs/AGENT_CONTEXT_INDEX.md`.
24. **`MEMORY.md`** + **`IDENTITY.md`** + **`HEARTBEAT.md`** + **`SKELETON.md`** + **`TOOLS.md`** — the rest of the root wake-up set. Each is short. Skim, bookmark, don't memorize. Per `COLLABORATOR_HANDOFF.md`, these stay at root; do not relocate.

## Phase 7 — Tooling + CI

25. **`pyproject.toml`** — dependency declaration with inline comments per dep. Python `>=3.11` floor.
26. **`router.yaml`** — model bindings per seat. Provider tier changes update this file only — never hardcode model names in identity, plan, or memory docs.
27. **`scripts/run_tests.sh`** — pinned-interpreter test runner. Refuses to use system Python. Always go through this.
28. **`scripts/run_lint.sh`** — AST-lint runner. Exit 0 on `pipeline` = green.
29. **`.github/workflows/ci.yml`** — CI shape. Four required checks (`quality-gate (3.11)`, `quality-gate (3.12)`, `wheel-install-smoke (3.11)`, `wheel-install-smoke (3.12)`). Tag-pinned actions (audit §10.5 P2-C).
30. **`pipeline/SESSION_BOOTSTRAP.md`** — project universe for new sessions. Path-reference in handoffs; never content-dump (L-002).

## Phase 8 — Runtime code (open these when you touch them)

These are surfaces, not files. Open by need; don't read end-to-end.

31. **`pipeline/orchestrator/`** — runtime orchestration. Routers, dispatchers, the provider boundary, classification context. `provider_boundary.py:736` (the sole egress wrapper) and `router.py:944` (`_dispatch_with_classification_boundary`) are the load-bearing pair.
32. **`pipeline/logician/`** — deterministic Python + Cedar policy gates. `gates/f_*.py` is the F-* family. Many raise `NotImplementedError` by design (fail-closed-pending); some are LIVE.
33. **`pipeline/cards/`** — CIC + CLC YAML + `loader.py`. Signed-loaded-governance at v0.1; runtime injection lands v0.2 first-wave.
34. **`pipeline/seats/`** — provider implementations for Scribe / Editor / Judge / Red Team. Capstone-hash pins inside each `__init__`; move with care.
35. **`pipeline/orchestrator/seats/`** — orchestrator-side seat modules (Scout, Intake, Uploader, + orchestrator glue for the council seats).
36. **`pipeline/sovereignty/`** — boot, isolation, audit, admin_risk, project_context_envelope, rfa_envelope, router_integrity, session, topology.
37. **`pipeline/program_rule_packs/`** — PRP scaffolding (live infrastructure per CTO blind spot A). Three of six PRPs are DRAFT bodies; loader top-level `load_active_prps()` raises `NotImplementedError`.
38. **`tests/`** — mirrors `pipeline/`. 365 files, ~10k+ passing. `tests/orchestrator/` and `tests/linting/` are the canonical "is my setup green" smokes (66 + 267 passed at last calibration).

## Phase 9 — Customer-facing + signed-asset surfaces

39. **`docs/white_glove_v0_1_beta.md`** — single-track white-glove onboarding playbook (Intake BULK_INGEST → Classification Review → first-cycle dispatch). Customer-and-operator register; not platform-engineer register. Read for context; don't author against.
40. **`vault_shared/`** — public-by-design pubkeys (cards-publisher, FID, operator-attestation stub, reflection-packet placeholder, SN-LLC). **Read-only for you.** Key rotation policy at `vault_shared/key_rotation_policy.md`.

## Surfaces NOT in this repo (gitignored — ask Josh)

- **`daily_logs/`** — operator's narrative thread. Most recent two are the canonical "what's going on right now" read; you'll need them on day one. Ask Josh to share.
- **`pipeline/handoffs/`** — workstream dispatch packets (the `<50-line + bootstrap reference` discipline). Ask Josh when you start a workstream that's already been pre-staged.
- **`orgs/`** — per-client data. Law 3 (Org Isolation) applies. The `_TEMPLATE/` subtree shape is documented; client folders are operator-private.
- **`_private/`** — operator-local Ed25519 seeds. **Operator-only.** Never touch.

## When you finish this list

You've covered the v0.1 reading surface. The next read is whatever's blocking your current PR — pull from `docs/TECHNICAL_BACKLOG.md` "Safe first tasks," open the surface, ship.

---

*Authored 2026-05-18 at commit `65e841a`. Living document — if the tree shifts and this index goes stale, fix it in the same PR that surfaces the gap. The discipline that matters: when you discover an out-of-order file, surface it; don't bundle.*
