---
title: Welcome, Paul — Day One Green Path
audience: Paul Norton (incoming Platform Engineer)
filed: 2026-05-18
status: living document — update as project state changes
companion_docs: docs/platform_engineer_onboarding.md (full pack) · docs/COLLABORATOR_HANDOFF.md · docs/LOCAL_DEVELOPMENT.md · docs/project_audit_2026-05-18.md
---

# Welcome, Paul — Day One Green Path

Welcome aboard. You're the first Platform Engineer on Tilth / Golden Quill, the sovereign grant-intelligence appliance Josh has been building solo for a year. This doc is the **compressed first read** — the rest of the onboarding fan-out is excellent but reading it in order takes half a day. Read this once, get to a green test run, ship one small PR. Then go wide via the full numbered tour at [`docs/paul_reading_order.md`](paul_reading_order.md), which is the master index for every file you should view, in order.

## What this project is, in 5 sentences

Golden Quill is a 128 GB customer-owned desktop appliance running **Tilth**, a six-seat AI council (Scout, Scribe, Editor, Judge, Red Team, Logician) that drafts, reviews, and scores grant proposals end-to-end. Architecture is §-numbered, amendment-chained, and audited row-by-row in `pipeline/engineering/lock_history.v1.jsonl` — every load-bearing change is operator-signed Ed25519 and paired-commit-mirrored in `pipeline/blueprint/v0.1/section_00_5_*.md`. The Logician is the only non-LLM primitive: deterministic Python + Cedar policies, fail-closed by default, enforcing the Five Operating Laws as PRE/POST gates around every seat invocation. Sovereignty is the commercial wedge — BYOK, classification-driven routing across three explicit postures (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign), nothing phones home silently. Josh has already won three competitive grants in 2026 using the manual version of this workflow; your job is to turn that working substrate into something repeatable on someone else's desk.

## The five things to read, in order

| # | Doc | What you'll get out of it |
|---|-----|---------------------------|
| 1 | [`README.md`](../README.md) | What ships today, what's `runtime-live` vs `spec-locked` vs `dormant`, and the four required CI checks on `main`. Read the "Where to read next" callout — skip the rest on first pass. |
| 2 | [`docs/project_audit_2026-05-18.md`](project_audit_2026-05-18.md) | Honest outside read of the codebase at commit `65e841a`. §3 covers the onboarding friction this doc compresses; §12 ranks the risks; §13 is the prioritized recommendation list — items #2 (signature-round-trip CI), #10 (CI hardening pack), and #11 (blueprint CURRENT_HEAD render) are realistic platform-engineer warmups. |
| 3 | [`docs/CTO_HANDOFF_BRIEF.md`](CTO_HANDOFF_BRIEF.md) | Josh's CTO-level handoff. §2 names the four CTO blind spots — blind spot D (operational freeze playbook) is the one explicitly tagged for you. §4 distinguishes load-bearing from governance theater; trust it. |
| 4 | [`pipeline/engineering/lock_history.v1.jsonl`](../pipeline/engineering/lock_history.v1.jsonl) — last 20 rows | Scroll the tail (`tail -20`) to see what a ceremony actually looks like on disk: `canonical_json_sha3_512`, `ed25519_signature`, `parent_lock_row`, `predecessor_amendments_chain`. Rows 280–292 are the cards-publisher key rotation + OD-E fix-forward — a working example of the discipline catching its own miss. |
| 5 | [`lessons.md`](../lessons.md) | L-001 through L-027. Append-only institutional memory. Frequency-weighted, severity-tagged. If you hit a problem that smells like a known shape, search here first — most are five lines and one pre-check. |

Then come back to [`docs/platform_engineer_onboarding.md`](platform_engineer_onboarding.md) and [`docs/platform_engineer_quick_reference.md`](platform_engineer_quick_reference.md) when you want the full glossary and seat-by-seat runbook. They're long but built for you specifically.

## Your first commit (low-stakes warmup)

```bash
# 1. Clone, set up venv, get tests green
git clone https://github.com/FIT-Farms/GoldenQuill.git
cd GoldenQuill
/opt/homebrew/bin/python3.14 -m venv .venv
.venv/bin/pip install --upgrade pip wheel
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -m spacy download en_core_web_sm

# 2. Verify
scripts/run_tests.sh tests/orchestrator/   # expect 66 passed
scripts/run_tests.sh tests/linting/        # expect 267 passed
scripts/run_lint.sh pipeline               # exit 0
```

Full details and common failure modes are in [`docs/LOCAL_DEVELOPMENT.md`](LOCAL_DEVELOPMENT.md).

**Pick one low-stakes warmup.** Any of these lands a clean first PR:

- A `docs/LOCAL_DEVELOPMENT.md` polish where setup steps drifted from reality (cleanup-plan v1.1 safe-first-task).
- A `pip-audit` step in `.github/workflows/ci.yml` (audit §13 #10).
- A single unit test against an already-LIVE F-* gate where `tests/logician/gates/test_*.py` coverage is thin.

A separate session is authoring the **signature-round-trip CI job** (audit §13 #2) — don't start there in parallel.

**Branch naming.** `paul-<short-slug>-<YYYY-MM-DD>`. Match Josh's pattern.

**PR conventions** are in [`docs/COLLABORATOR_HANDOFF.md`](COLLABORATOR_HANDOFF.md) §"How to start" — the template names `lock_history` row(s), F-* code(s), §-section, paired-commit SHA, and `Co-Authored-By:` for AI-assisted commits. For doc-only or CI-only PRs, most are `n/a` — say so explicitly.

## How we work

**Ceremonial discipline.** Every load-bearing architectural change goes through a LOCK ceremony — Thesis cross-family review, paired-commit §0.5 sibling, append to `lock_history.v1.jsonl`. The cost feels high until you watch it catch a near-miss (rows 274–279, the OD-E example, caught a signed-but-not-on-disk claim before it shipped). Sovereignty-wedge customers care about this ledger; it's the moat. You won't fire ceremonies yet, but you'll write code against LOCKed specs — trust the §-references.

**Fail-closed by default.** `F-CLASS-ROUTING-INDETERMINATE → local`. `F-CLASS-NEW-FACT-UNCLASSIFIED → confidential`. `NotImplementedError` everywhere a runtime is pending — that's a feature. Canonical operationalizations: `pipeline/cards/loader.py`, `pipeline/orchestrator/provider_boundary.py`.

**No mocks for boundary checks.** Integration over unit at the surfaces that matter — provider boundary, classification register loading, signature verification when it lands.

**Ask before scope-expanding.** Surface adjacent fixes as follow-up issues, not bundles. Josh underspecifies intentionally; honest scope is what makes that work.

**Memory and context.** Daily logs at `daily_logs/YYYY-MM-DD.md`; lessons in `lessons.md`; `MEMORY.md` is the index. When you make a non-obvious decision, drop a line — that's how we stay coordinated across sessions and tools.

## Comms & access

- **Ping Josh** via Dispatch (the channel he names at onboarding). Email backup: see `USER.md`.
- **Branch protection** on `main`: PR-only, four required checks (`quality-gate (3.11)`, `quality-gate (3.12)`, `wheel-install-smoke (3.11)`, `wheel-install-smoke (3.12)`), admin enforcement on. No force-pushes to `main`.
- **Repo:** `https://github.com/FIT-Farms/GoldenQuill` (private, License: Proprietary). Ask Josh for collaborator access if you don't have it on day one.
- **Plugins / skills.** Josh works in Cowork (Claude desktop) with the Anthropic skills + grant-finder + grant-writer + scribe-ghostwriter set installed. You don't need these for Platform Engineer work, but seeing what Josh uses helps explain some of the operator-facing artifacts.

## The 3 things that will trip you up (so they don't)

1. **Pinned interpreter (L-013-shaped, but mainly the LOCAL_DEVELOPMENT.md callout).** macOS-default `python3` is 3.9 and *cannot collect* the codebase — `@dataclass(frozen=True, kw_only=True)` requires 3.10+ and `pyproject.toml` pins `>=3.11`. If you run `python3 -m pytest` directly you'll see 8 collection errors that look like real failures but are an interpreter mismatch. Always go through `scripts/run_tests.sh` (which checks `.venv/bin/python3 --version`) or `.venv/bin/python3 -m pytest` explicitly.
2. **L-026 — bash 3.2 heredoc-inside-`$()` parser bug.** Operator runs macOS bash 3.2.57. The sandbox runs bash 5.x. A script that passes `bash -n` in the sandbox can fail at runtime on Josh's box with `syntax error near unexpected token ')'` because bash 3.2 scans the heredoc body for `(` / `` ` `` before single-quoting takes effect. If you write a shell script meant to run on Josh's Mac, **don't** use `VAR=$(cat <<'EOF' ... EOF)`. Use the temp-file pattern: `cat > "$WORKDIR/body.md" <<'TAG' ... TAG` and consume via `--body-file`. Full pattern in `lessons.md` L-026.
3. **L-025 — ceremony preflight: write → re-read → SHA3-512 → sign.** Every `card_cartridge_supersession` row must be preceded by a script-level preflight that writes the new bytes, re-reads from disk, recomputes SHA3-512, and aborts on mismatch *before* the Ed25519 signature is emitted. The OD-E miss happened because rows 276/277/278 signed in-memory bytes that never landed on disk. If you ever touch the ceremony scripts (`pipeline/scripts/*_ceremony_*.py`), this preflight is non-negotiable. The L-025 entry in `lessons.md` has the recovery-supersession pattern if it does fire.

## What you don't need to learn yet

Explicit permission to skip on day one — come back when these intersect your work:

- **Tier 2B card augmentation drafts** (`pipeline/cards/_drafts/`) and the LARGE cards-ceremony queued behind them. Operator content-judgment work; not your surface until v0.2.
- **§17 WPFA buyer-PDF emission** and the Coefficient Registry trust mechanism. LOCKED but not active at v0.1.
- **§16 Reflection Packet first wave.** 18 of 19 F-PACKET-* predicates raise `NotImplementedError` by design. v0.2 horizon.
- **The v0.2 PRP authoring queue** (FERPA-COPPA-HIPAA, SUBCHAPTER-T, USDA-VAPG-FY26). Becomes relevant when an educator-wedge customer lands.

## Reach out when…

- A test breaks in a way the L-001..L-027 lessons don't already cover. Surface it before debugging more than ~30 minutes solo — most failure shapes Josh has seen before.
- You discover something adjacent that "should also be fixed." Surface it; don't bundle. Josh decides whether it's the same PR or a follow-up issue.
- A LOCK ceremony, a signed asset, or anything under `_private/` is in your path. Stop and ask — those are operator-only surfaces.
- A doc disagrees with `RUNTIME_MATURITY_MATRIX.md` or `PROJECT_STATUS.md`. The matrix wins; the disagreeing doc has a bug, and you can fix it.
- You're about to ask "should I do X or Y?" and both have merit. Ask. Josh underspecifies on purpose.

**Proceed when…** the task is in `docs/TECHNICAL_BACKLOG.md` under "Safe first tasks," CI is green on your branch, and the PR fills the template honestly.

---

*Authored 2026-05-18 by a Cowork session at commit `65e841a`. Living document — update in the same PR that surfaces a gap. If something here is wrong because the codebase moved, that's a doc bug worth fixing in your second PR.*
