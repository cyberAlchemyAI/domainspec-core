---
title: GitHub Product-Truth Cleanup + Navigation Plan
version: v1.1
filed: 2026-05-17
supersedes: docs/github_product_truth_cleanup_plan_2026-05-17.md
operator: Josh Inklovich
analyst: Claude Opus 4.7 (planning lane only — no LOCK ceremonies, no code edits, no doc rewrites in this artifact)
basis: operator's 2026-05-17 executive read + 2026-05-17 safety-correction pass + the GitHub form/function analysis at docs/github_form_and_function_analysis_2026-05-16.md
companion: pipeline/handoffs/audit_prompt_v1_1_pr4_staging_2026-05-16.md (audit playbook staging note)
posture: PLAN ONLY. This document proposes work; it does not perform it. Each track ends with a "what this plan does NOT do" line so the scope stays honest.
guiding_principle: do not damage LOCKed or historical truth in the act of making the repo more readable. Polish never overrides preservation.
---

# GitHub Product-Truth Cleanup + Navigation Plan (v1.1)

## §0 — What changed v1 → v1.1

This revision folds the operator's 2026-05-17 safety-correction pass into the plan. Ten substantive corrections, listed in the order they appear in the body of the plan so a reader can map "what the operator flagged" to "where the plan now reflects it."

1. **Two new tracks added at the front of the sequence.** Track 0 (Merge / Branch / PR cleanup) and Track 9 (Secrets / Data / Access audit) are now the first two tracks executed. Without Track 0 the repo carries two competing "truth branches" (PR #3 + PR #4) and Track 1's "truth sweep on `main`" has no stable target. Without Track 9, granting a collaborator access (the trigger for Track 5) is unsafe regardless of how polished the docs are.

2. **One new track added at the end of the sequence.** Track 8 (Collaborator Task Queue) ships an ordered backlog — Gate 1 blockers, Gate 2 blockers, safe-first-tasks, do-not-touch surfaces, needs-Josh-decision, needs-architecture/LOCK-process. A collaborator handoff doc (Track 5) tells *what works*; the task queue tells *what to do next*. Both are required.

3. **Track 4 item 2 reversed — root wake-up files stay where they are.** v1 proposed grouping `AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, etc. into an `agent/` subdir. Too many bootstrap chains and agent prompts expect those root paths; moving them would break working machinery for a cosmetic win. Replaced with: keep the files at root, add `docs/AGENT_CONTEXT_INDEX.md` describing what each one does, link from README.

4. **Track 4 item 3 reversed — LOCKed amendment files are not edited.** v1 proposed adding a one-paragraph header to every blueprint amendment file ("This amendment is the head of §4," etc.). Even though no LOCK ceremony is required for whitespace-level edits, the discipline this repo is built on says we do not modify LOCKed artifacts. Replaced with a sidecar approach: `pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md` (markdown, human-facing) and an optional `pipeline/blueprint/v0.1/blueprint_status.yaml` (machine-readable sidecar). The amendment files themselves are untouched.

5. **Track 1 splits current-facing docs from historical docs.** v1 implied a global sweep of stale row counts and test counts. The operator's correction: a 2026-05-10 planning doc that says "339 tests passed on 2026-05-11" is legitimate historical record — adding a "this snapshot is historical" banner is correct; rewriting the count is wrong. Only docs that *present old counts as current truth* (README's status paragraph, `docs/alpha_readiness_checklist.md`-style files that read as live) get the count refresh.

6. **Maturity taxonomy goes from six states to seven — `spec-locked` inserted.** Tilth has many surfaces where the spec is LOCKed (blueprint amendment landed, lock_history row written) but the implementation is pending. Those surfaces don't fit `schema / scaffold` (the spec is more than a scaffold), and they don't fit `gate-live` (no gate fires yet). New label `spec-locked` sits between `schema / scaffold` and `gate-live`. The §4 v2.x.6 runtime companion is the canonical example.

7. **`signed asset` renamed to `asset-signed`.** Reads as a status verb-pattern, aligning with the other status labels (`runtime-live`, `gate-live`, `spec-locked`). Pure rename — semantics unchanged.

8. **"Promotion is a paired ceremony" softened.** v1 made every status change a paired ceremony, which would make routine status cleanups feel as heavy as a LOCK event. Replaced with: *promotion requires dated evidence — CI/test proof for runtime changes, and a `lock_history` row only when the promoted state changes a LOCKed, signed, or governance-bound artifact.* Lightweight status drift (matrix updates, label corrections) gets a dated entry in `PROJECT_STATUS.md`; promotions that touch governance get the lock_history row.

9. **Track 5 gains a real local setup path.** v1 mentioned "how to run tests" in one bullet. The operator's correction: that's not enough for a contributor cloning the repo from cold. New artifact `docs/LOCAL_DEVELOPMENT.md` (or `SETUP.md` at root) covers Python 3.14 pinning, venv setup, install, lint (`scripts/run_lint.sh pipeline`), test (`scripts/run_tests.sh`), expected green result, common local failures, and the gap between local Mac tests and what CI proves on Linux.

10. **Sequence and aggregate effort updated.** New sequence: Track 0 (merge/PR) → Track 9 (secrets audit) → Track 1 (claim hardening, current-facing only) → Tracks 2-7 in their original order with the corrections folded in → Track 8 (collaborator task queue). Aggregate effort revised upward to reflect the two new front-of-queue tracks and one new end-of-queue track.

The rest of the document is the v1 plan with the corrections above applied in place.

---

## Frame

Two facts from the operator's 2026-05-17 read define everything that follows.

**Fact 1: PR #4 is the canonical product landing path.** It includes PR #3 verbatim, CI is green on Python 3.11/3.12 (wheel-smoke + lint + AST-lint + serial pytest), and `main` is still at `044415c` — last week's audit/CI commit, not the product state. The first move is to land PR #4 to `main`. Everything else here assumes that landing has happened or is about to.

**Fact 2: The remaining risk is narrative, not engineering.** The code, the gates, the schemas, the audit ledger, and the tests are real. The danger is *semantic overclaim* — governance language (LOCKED, signed, loaded) read as runtime-live language by a reviewer who doesn't know the difference. The cleanup work is about making the truth legible at three different reader depths: skimmer (README), collaborator (status docs), engineer (blueprint chain + lock ledger).

The plan is organized as ten tracks (Track 0 through Track 9) plus a one-line "do not touch" boundary. Each track names the deliverable, the audience, the dependencies, the effort, and the explicit exclusions.

## Track boundary: what this plan does NOT do

This plan does NOT propose new LOCK ceremonies, code refactors, blueprint amendments, runtime companion code landings, ledger row writes, edits to LOCKed amendment files (even cosmetic ones), relocation of root wake-up files (`AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, etc.), or any work that would interfere with the in-flight OD-A / OD-D / OD-C / OD-E ceremonies or the §4 v2.x.6 runtime companion Code session. Every recommendation below operates on documentation, navigation surface, repo metadata, branch state, or labels — never on the engineering tree, the lock_history, the LOCKed amendment text, or the F-* gates.

---

## Track 0 — Merge / Branch / PR cleanup

**Audience:** the operator; anyone landing on `main` after Track 0 completes.
**Trigger:** none — this is the first track. Runs before everything else.
**Why first:** Track 1 ("truth cleanup on `main`") cannot run while there are two competing "truth branches" — PR #3 (the clean baseline) and PR #4 (which contains PR #3 verbatim plus additions). Without consolidating to a single canonical `main`, the rest of the plan operates on a moving target.

Concrete steps, in order:

1. **Merge PR #4 to `main`.** Use the standard merge (not squash) so the paired-commit discipline and the lock_history row references in the commit bodies survive. Confirm the merge commit on `main` matches the expected SHA before announcing.
2. **Close PR #3 as superseded by PR #4.** Per the form/function analysis at `docs/github_form_and_function_analysis_2026-05-16.md`, PR #4 already contains PR #3 verbatim. Close PR #3 with a one-line comment pointing at the PR #4 merge commit so the audit trail is preserved. Do NOT delete the `codex-pr2-cc003-cleanup` branch in the same step — leave it for a separate housekeeping pass after Track 9.
3. **Confirm `main` CI green after merge.** All four required checks (`quality-gate (3.11)`, `quality-gate (3.12)`, `wheel-install-smoke (3.11)`, `wheel-install-smoke (3.12)`) must pass on the merge commit. If any flake, re-run before proceeding.
4. **Tag or note the merge commit as the Gate 1 cleanup baseline candidate.** Either a lightweight `gate-1-cleanup-baseline-candidate` tag on the commit, or a dated note in `pipeline/handoffs/` recording the SHA. This is the commit Track 1's "truth sweep" runs against.
5. **Configure GitHub branch protection on `main`** to require those four checks + at least one review. This step lands AFTER the merge so the merge itself isn't blocked by a protection rule that didn't yet exist. UI-only step.

**Deliverable:** `main` at the PR #4 merge commit with CI green, PR #3 closed, branch protection on, baseline candidate noted.

**Effort:** 30-60 minutes elapsed (the merge is push-button; the wait is CI).

**What this track does NOT do:** rewrite any commit history, force-push, delete branches, or perform any work on the engineering tree. Pure git workflow + GitHub UI.

---

## Track 9 — Secrets / Data / Access audit

**Audience:** the operator before granting any collaborator access; future-Josh debugging a security concern.
**Trigger:** after Track 0, before Track 5 (collaborator handoff) is consumed.
**Why second:** more important than polish. A clean README does not compensate for a leaked key in commit history. This audit happens before any human outside the operator gets push or review access.

Concrete checks, in order:

1. **Private key sweep.** Confirm no `*.pem`, `*.key`, `id_rsa`, `id_ed25519`, or equivalent committed anywhere in the tree. The cards-publisher Ed25519 keypair is operator-local; verify it is not in the repo. Confirm `.gitignore` covers the standard private-key patterns.
2. **Real client data sweep.** Confirm no actual grant proposals, client names beyond Tilth/Golden Quill internal context, real funder communications, or other live customer material is committed. PA-foundation public-record data is fine (it's published). Anything that looks like a real proposal draft from a real grower needs to be in `pipeline/handoffs/` (gitignored) or out of the tree entirely.
3. **`data/` directory discipline.** Confirm `data/` is either README-only (with a pointer to where the real data lives locally) or fully gitignored. The corpus discipline already enforces this for `pipeline/funder_corpus/`; verify the same posture for any other `data/` location.
4. **Secrets / environment file sweep.** Confirm no `.env`, `.envrc`, `secrets.yaml`, `credentials.json`, or BYOK token material is committed. Confirm CI does not echo secrets in logs.
5. **Org / vault / customer material sweep.** Confirm no internal org vaults (e.g., 1Password references with real handles), customer NDAs, or paid-engagement material is exposed.
6. **Automated secret scan.** Run `gitleaks` or `trufflehog` against the full git history (not just `HEAD`). A leaked key that was deleted in a later commit is still leaked. If either tool surfaces a finding, the finding is triaged before any access is granted.
7. **Access roster review.** Before granting collaborator access in Track 5, document who currently has what level of access (operator, CI bot, any GitHub Apps). If the answer is "just Josh + CI," that's the line — note it.

**Deliverable:** `pipeline/handoffs/secrets_data_access_audit_2026-05-XX.md` (gitignored) with the seven checks listed and the result of each. Anything red blocks Track 5.

**Effort:** 2-3 hours for the manual checks + secret scan; longer if findings need triage.

**What this track does NOT do:** rewrite git history to remove leaked material (that's a separate, careful operation — this track *finds* problems, it does not *fix* them in-flight). Does not change any access permissions; only documents the current state.

---

## Track 1 — Truth cleanup on `main` (current-facing docs only)

**Audience:** anyone landing on `main` cold (Paul Norton, a future engineer, a paying customer's tech reviewer).
**Trigger:** Track 0 complete (PR #4 merged, `main` at known SHA, CI green).

Once `main` is settled at the PR #4 merge commit, run a coordinated "doc-truth sweep" that distinguishes **current-facing claims** from **dated historical record**. The distinction is the whole game in v1.1: a 2026-05-10 planning doc that says "339 tests passed on 2026-05-11" is correct historical record and gets a banner, not a rewrite. Only docs that *present old counts as current truth* are updated.

The sweep covers four classes of staleness:

1. **Stale row counts and test counts.**
   - **Current-facing (update the count):** the README's "Focused v0.1 smoke suite on 2026-05-11: 339 tests passed" sits in a Status paragraph that reads as live truth and gets refreshed to the PR #4 number (the merge commit body records `10,584 passed / 3 skipped / 1 xfailed`). Same treatment for any `docs/alpha_readiness_checklist.md`-style file that names a specific row total in a "where are we today" voice and is still read as current. The lock_history is now at row 262+ on disk — any doc that names row 216 / row 224 / row 235 / row 247 as a *current* state gets corrected.
   - **Historical (banner, don't rewrite):** `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md`, `pipeline/planning/v0_1_beta_readiness_2026-05-10.md`, and any other dated planning artifact whose timestamp is older than two weeks at the time of the sweep. These get a one-line banner at the top: `> Historical snapshot dated YYYY-MM-DD. Counts and states reflect the repo at that moment, not current truth. See PROJECT_STATUS.md for live state.` The body text is not edited.
   - **Rule of thumb:** if the doc's title or framing implies "this is the current state," update. If the title or filename implies "this is what we knew on date X," banner.

2. **PR #3 references.** Any doc that names PR #3 as the "clean baseline" or "next thing to land" is superseded — PR #3 is absorbed by PR #4 (Track 0 closed it). Grep for `PR #3`, `PR/3`, `codex-pr2-cc003-cleanup`, `pull/3`. Same current-vs-historical split applies: a current-facing planning doc gets the reference corrected; a dated audit note keeps the PR #3 reference and gets the historical banner.

3. **"Alpha" language.** Replace loose "Alpha" / "Alpha-ready" / "Alpha checklist" framing with **Gate 1 (internal replay with Paul)** and **Gate 2 (first paid client)** language per the operator's read. This rename is current-facing-only: `docs/alpha_readiness_checklist.md`, the README's Status paragraph, `docs/paul_norton_memory_alignment_brief_2026-05-15.md`, the website build spec, and any planning doc that uses "Alpha" as a state label *in present tense*. A historical doc that records "we called this stage Alpha in 2026-04" keeps the word with a banner.

4. **Runtime claims that exceed runtime state.** Anywhere a current-facing doc says cards are "loaded" or the system is "live" or "running in production," tighten to the precise maturity label from Track 3 (now seven-state). The §4 v2.x.6 runtime companion has not landed (`spec-locked`, not `runtime-live`); the card runtime loader is v0.2 first-wave; Brain/JIT is research-only; Reflection Packet activation truth needs care. The README *is* already careful about this (Local-Only/Sovereign is marked "performance-dependent / under validation"); extend that discipline workspace-wide on the current-facing surface.

**Deliverable:** a single `pipeline/handoffs/doc_truth_sweep_2026-05-XX.md` operator-facing punch list (gitignored), and the resulting PR that lands the fixes — call it **PR #5: doc-truth sweep** (or PR #6 if PR #5 is the v1.1 audit prompt landing).

**Effort:** 3-5 hours (slightly higher than v1's 2-4 because of the current-vs-historical triage).

**What this track does NOT do:** rewrite historical planning docs to reflect current numbers; touch blueprint section files; touch lock_history; alter the engineering tree; introduce new product claims. It is a precision-edit pass on the *current-facing* human-readable surface, with banners on the historical surface.

---

## Track 2 — Navigation layer

**Audience:** collaborator (Paul, a future engineer) skimming for "where do I start."
**Trigger:** any time after Track 1.

The repo's discoverability problem is not that critical docs are missing — they exist and the README links to them — but that there is no single page that, on first read, tells a newcomer *what the system is doing today* vs. *what it was always going to do*. Three new docs plus one index solve this:

1. **`PROJECT_STATUS.md`** (root, two pages max). One paragraph per system, written as of a dated snapshot:
   - What works in `main` today.
   - What is parked.
   - What needs engineering judgment to move forward.
   - Last update timestamp + the commit SHA the status reflects.
   This is the page a new collaborator reads first. It is meant to go stale fast — that's fine, it has a date, and stale-but-dated is more honest than confident-and-undated.

2. **`pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md`** (a sidecar — does NOT modify any amendment file). A flat table:
   - Section number (§4, §11, §13, §18, etc.).
   - Canonical filename for the *current* head amendment (e.g., for §4 today that's `section_04_v2_x_6_router_dedup_amendment.md` *as the LOCKed head*, with the runtime companion noted as "spec-locked, runtime pending").
   - Amendment chain depth and the last LOCK ceremony row.
   - One-sentence "what this section is for" pointer.
   - Status column from Track 3's seven-state taxonomy.
   The blueprint directory has ~50+ amendment files now; without an index, the chain reads as archaeology. The index does NOT replace the amendment files — it points at them and tells the reader which one is the head. Amendment files themselves are not edited.

3. **`pipeline/blueprint/v0.1/blueprint_status.yaml`** (optional machine-readable sidecar). Same data as the markdown index, but in a shape a future tool can read. Two fields per section: `head_amendment_filename`, `maturity_state` (one of the seven Track 3 labels). Optional in v1.1 — the markdown index is the source of truth; the YAML is for tooling convenience.

4. **`RUNTIME_MATURITY_MATRIX.md`** (root, one page). One row per system (see Track 3 below for the seven-state taxonomy). This is the single source of truth that all other docs cite when they make claims like "cards are loaded" — the matrix says specifically *which* loading state cards are in.

5. **`docs/AGENT_CONTEXT_INDEX.md`** (the v1.1 replacement for v1's "move the root files into `agent/`" proposal). A one-page index explaining what each root wake-up file is for: `AGENTS.md` (entry point + wake-up sequence), `CLAUDE.md`, `HEARTBEAT.md`, `IDENTITY.md`, `MEMORY.md`, `SKELETON.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `lessons.md`. The files stay at root (too many agent bootstrap chains depend on those paths); the index gives a newcomer a map to the personification archive without making them open ten files to figure out the topology. Linked from the README "What to read first" block.

Also: add a **"What to read first" block** at the very top of the README pointing at `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, `pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md`, and `docs/AGENT_CONTEXT_INDEX.md` in order. Eight-to-ten-line block.

**Effort:** 5-7 hours for first drafts (slightly higher than v1's 4-6 because of the agent context index addition and the YAML sidecar); expect 2-3 iterations.

**What this track does NOT do:** generate new content. The four new docs aggregate and label what already exists in the tree; they do not introduce new architectural claims. The blueprint amendment files are not touched.

---

## Track 3 — Runtime maturity labeling

**Audience:** anyone reading a doc that uses the word "loaded," "signed," "live," or "ready."
**Trigger:** PR #4 merged (Track 0 complete). Track 3 is the prerequisite for finishing Track 1 — you can't tighten a runtime claim without a vocabulary for what tightening means.

Adopt a **seven-state taxonomy** (six in v1, plus `spec-locked` inserted between `schema / scaffold` and `gate-live`) and apply it consistently across `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, the README capability table, and every doc that makes a claim about a subsystem.

| Label | Meaning | Example |
|---|---|---|
| **runtime-live** | Code is in production paths, exercised by CI on every PR, and would fire on a real customer call today. | Provider-boundary enforcement (`enforce_outbound_boundary` wrapper), F-CLASS-* gates, AST-lint rules, the six-seat council dispatch path. |
| **gate-live** | The Logician gate exists, the F-* code is defined, the test exercises it deterministically, but the gate only fires inside the test substrate — production execution is not yet wired or not yet exercised. | Some of the F-cards-* gates landed in `a71f841` — the gate code is present and tested, but the runtime card loader that triggers them on real customer data is still v0.2 first-wave. |
| **asset-signed** *(renamed from `signed asset` for status-verb consistency)* | The asset exists, is operator-signed (Ed25519 against the cards-publisher pubkey), is in the tree, and the signature verifies — but no runtime path loads it for real customer execution yet. | Cards Wave 1 + Wave 2 YAML cards. They are signed, LOCKed, and present at `pipeline/cards/`; the runtime loader hooks them up at v0.2. |
| **spec-locked** *(new in v1.1)* | The specification has landed and is LOCKed via the blueprint amendment chain (lock_history row written, signed if applicable), but the implementation is pending. The spec is more than a scaffold and less than a gate. | The §4 v2.x.6 runtime companion: the amendment is LOCKed, the routing semantics are specified, the lock_history row exists — and the Code session that lands the runtime is still in flight. |
| **schema / scaffold** | The shape exists. The fields are named. The tests cover the shape. Implementation is partial or stubbed. No LOCK ceremony has elevated it to `spec-locked` yet. | `pipeline/funder_intelligence/` (corpus discipline is real; the curation engine is not). `pipeline/funder_corpus/` PA-foundation dataset (data + tests; the runtime Match Database query is v0.2). |
| **dormant** | Code or doc exists but is not exercised, not on a near-term roadmap, and not load-bearing. Documented so a future contributor knows not to delete it. | The deprecated Sanitized fourth-posture defense-in-depth gates (per README historical note). |
| **historical** | Captured for audit / prior-art preservation. Explicitly not the current truth. | `pipeline/validation/v7_0_5_thesis_2026-05-09/` (preserved per AGENTS.md). The deleted `state_rules_cartridge.py` (post-rename to `state_rules_card.py`). |

Two operating rules for the taxonomy:

- **One label per system per doc.** A system cannot be `asset-signed` in one place and `runtime-live` in another. The matrix is the arbiter.
- **Promotion requires dated evidence.** *Softened from v1's "paired ceremony" framing.* Moving a subsystem along the maturity axis (e.g., `spec-locked` → `gate-live` → `runtime-live`) requires dated evidence: CI/test proof for runtime changes (a green CI run on the commit that wires the runtime), and a `lock_history` row **only when the promoted state changes a LOCKed, signed, or governance-bound artifact**. Lightweight matrix corrections — fixing a mislabeled status, refining a description — get a dated entry in `PROJECT_STATUS.md` and do not need a ledger row. This prevents every status cleanup from feeling as heavy as a LOCK event while still protecting governance-bound transitions.

**Effort:** 3-4 hours to define labels (this doc starts that work — the seven-state taxonomy is now codified above), 5-7 hours to apply the labels across the docset (slightly higher than v1's 4-6 because the seven-state taxonomy needs a per-system second-pass review).

**What this track does NOT do:** define new failure codes, gate behaviors, or runtime states. It puts a vocabulary on states that already exist. The label rename (`signed asset` → `asset-signed`) is mechanical and does not change which assets are signed.

---

## Track 4 — Repo simplification

**Audience:** anyone navigating `~/Downloads/GoldenQuill` for the first time.
**Trigger:** PR #4 merged (Track 0 complete); Track 2 navigation docs drafted.

Three concrete simplifications. **v1.1 reverses two of v1's three proposed moves** in service of the "do not damage LOCKed or historical truth" principle.

1. **Move `FOUNDATION_README.md` out of root** (per the form/function analysis P2 #9; unchanged from v1). It's a 2026-04-14 artifact that describes this repo as "the clean restart" — internal context, not product narrative. Either `docs/operator/FOUNDATION_README.md` or `pipeline/handoffs/FOUNDATION_README.md` (the latter is gitignored, which may be the right call for an artifact that's no longer load-bearing). This is a single non-LOCKed file with no agent bootstrap dependency.

2. **Root wake-up files stay at root. Add `docs/AGENT_CONTEXT_INDEX.md` instead.** *Reversed from v1.* `AGENTS.md`, `CLAUDE.md`, `HEARTBEAT.md`, `IDENTITY.md`, `MEMORY.md`, `SKELETON.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `lessons.md` are correctly committed at root because the agent wake-up sequence and a number of bootstrap chains expect those exact paths. Moving them — even to a tidy `agent/` subdir — risks breaking the working machinery for a cosmetic win. The v1.1 approach: leave the files at root, and add a one-page `docs/AGENT_CONTEXT_INDEX.md` that explains what each one is for and which agents read them. Link from the README "What to read first" block (Track 2). The file-tree appearance is unchanged; the legibility is added in the index.

3. **No headers added to LOCKed amendment files. Use the sidecar index instead.** *Reversed from v1.* v1 proposed adding a one-paragraph header to every blueprint amendment file ("This amendment is the head of §4 as of lock_history row XXX," etc.). Even though no LOCK ceremony is technically required for whitespace-level edits to LOCKed text, the discipline this repo is built on says we do not modify LOCKed artifacts — and a header insertion *is* a modification. The v1.1 approach: the same information lives in `pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md` (Track 2 item 2) and the optional `pipeline/blueprint/v0.1/blueprint_status.yaml` (Track 2 item 3). Someone who lands on a single amendment via a deep link gets pointed at the index from the README and the directory README; the amendment text itself stays exactly as LOCKed.

**Effort:** 1-2 hours for item 1; item 2 and item 3 effort moves into Track 2 (the sidecars are where the work lives now). Net v1.1 effort for Track 4 standalone: 1-2 hours.

**What this track does NOT do:** delete any tracked file from the engineering tree; rewrite or modify any amendment content; relocate root wake-up files; alter the AGENTS.md wake-up sequence.

---

## Track 5 — Collaborator handoff

**Audience:** the first technical contributor outside the operator (Paul Norton, candidate engineer, or paid reviewer) who is given push or review access.
**Trigger:** before granting that access. **Track 9 (secrets audit) must be complete and green before this track ships.**

Two new docs in v1.1 (v1 had one; the local-setup-path doc is new):

### 5a. `docs/COLLABORATOR_HANDOFF.md` (or `CONTRIBUTING.md` — same content, different filename convention)

Covers, in this order:

- **What Golden Quill is, what Tilth is** — one paragraph each, pulled directly from the README so the framing is identical.
- **What works today** — pointer to `PROJECT_STATUS.md` + `RUNTIME_MATURITY_MATRIX.md`.
- **What is parked** — pointer to the dormant/historical rows of the matrix.
- **What needs engineering judgment** — the three or four open architectural questions that a contributor should know exist before they propose changes (e.g., the card runtime loader landing schedule, the §4 v2.x.6 runtime companion in flight, the Reflection Packet activation truth).
- **How to run things locally** — short pointer to `docs/LOCAL_DEVELOPMENT.md` (5b below) for the full setup; do not duplicate the content here.
- **What not to touch** — the `lock_history.v1.jsonl` is operator-write-only; blueprint amendment files have a LOCK ceremony attached and are not edited in-place (this includes cosmetic header insertions — see Track 4 item 3); F-* gate codes do not change once LOCKed without an amendment chain entry; root wake-up files (`AGENTS.md`, `SOUL.md`, etc.) are not relocated; `data/` and `pipeline/handoffs/` follow their existing gitignore discipline.
- **How to propose work** — commit message discipline (§-blueprint reference, F-* code, lock_history row, paired-commit sibling SHA), the PR template from Track 7, the task queue (Track 8) for "what should I pick up next."

### 5b. `docs/LOCAL_DEVELOPMENT.md` (or `SETUP.md` at root) — *new in v1.1*

A dedicated local-setup path so a contributor cloning cold can reach a green test run without guessing. Covers:

- **Python version pin: 3.14.** This is the operator's pinned local version; CI runs 3.11 + 3.12 in the wheel-smoke matrix, so contributors should know both that 3.14 is the local target and that CI proves a wider matrix.
- **venv setup.** Explicit `python3.14 -m venv .venv && source .venv/bin/activate` block. Note the platform difference for Windows contributors if applicable.
- **Install command.** Whatever the canonical install incantation is (`pip install -e .[dev]` or equivalent — the doc author confirms against the actual `pyproject.toml`).
- **Lint command.** `scripts/run_lint.sh pipeline` — the same script CI runs.
- **Test command.** `scripts/run_tests.sh` (or `scripts/run_tests.sh -n auto --dist=loadfile` for the parallel variant the operator uses).
- **Expected green result.** What "green" looks like: a row count near 10,584 passed, the skipped/xfailed numbers, the elapsed range a contributor should expect on modern hardware.
- **Common local failures.** A short list — venv-not-activated, wrong Python version, missing dev extras, a flaky test that's known and tracked.
- **What CI proves that local Mac tests may not.** The Linux wheel-smoke catches a class of platform-specific issues local macOS testing won't surface; the AST-lint runs in CI and may not be wired locally; the deterministic-order test (`--dist=loadfile`) is what CI uses. Contributors should know that "green on my Mac" ≠ "green on CI" by default, and that the CI matrix is canonical.

**Effort (combined 5a + 5b):** 4-6 hours (5a is 2-3, 5b is 2-3).

**What this track does NOT do:** publish or grant access. It writes the docs that get pointed at when access is granted. Track 9 gates the access grant.

---

## Track 6 — Claim hardening

**Audience:** every doc that makes a sovereignty, alpha-readiness, or paid-client-readiness claim.
**Trigger:** after Tracks 1+3, before any external visibility move (Paul review, website launch, customer pitch).

Five docs need to tell the same truth, distinguishing three readiness states:

| Doc | Today's state | Target state |
|---|---|---|
| `README.md` | Strong; one regression (deleted sentence + handle change in PR #4 — see analysis P0 #2). | Gate 1 / Gate 2 language explicit. Capability table cites seven-state taxonomy (Track 3). |
| `docs/alpha_readiness_checklist.md` | Uses "Alpha" framing. | Renamed `docs/gate_1_internal_replay_checklist.md` + companion `docs/gate_2_first_paid_client_checklist.md`. (Current-facing only — see Track 1 split.) |
| `docs/paul_norton_memory_alignment_brief_2026-05-15.md` | Internal review framing. | Aligned to Gate 1 language; explicitly named as a Gate 1 input. |
| `docs/golden_quill_website_build_spec_v1.md` | Public-facing claim surface. | Every claim labeled with a maturity tag from Track 3's seven-state taxonomy. No "loaded" or "live" without a matrix backing. |
| Onboarding docs (`docs/platform_engineer_onboarding.md`, `docs/platform_engineer_quick_reference.md`) | Operator-oriented. | Aligned to Track 5 handoff doc + Track 5b local-development doc; Gate 1 vs Gate 2 distinction inherited. |

**Three readiness states to disambiguate:**

- **Internal replay readiness** = Gate 1 = "Josh + Paul could reproduce a full grant cycle end-to-end in a controlled environment using a real client's data, with all five Laws enforced."
- **Paid-client readiness** = Gate 2 = "A paying customer's first deployment ships with the signed classification register, the runtime card loader live, and the on-demand heavy Judge swap exercised."
- **Future-stage sovereignty roadmap** = Phase Two = "Tribal sovereign configurations, multi-site consortiums, the things the README's Roadmap section parks at April 2027."

Every public-facing claim must be tagged with one of these three.

**Effort:** 4-6 hours.

**What this track does NOT do:** ship to customers; commit to dates; change any in-tree gate behavior.

---

## Track 7 — Selective test / CI confidence

**Audience:** contributor, CI maintainer, future-Josh debugging a flake.
**Trigger:** any time after Track 0.

Four small additions on top of the already-green CI:

1. **Pin the matrix in writing.** Add a `## CI` section to the README (or to `COLLABORATOR_HANDOFF.md`) that names the required checks: `quality-gate (3.11)`, `quality-gate (3.12)`, `wheel-install-smoke (3.11)`, `wheel-install-smoke (3.12)`. This closes the loop between "we have CI" and "what does merge actually require." Note: Track 0 step 5 already configures branch protection to require these four checks — Track 7 item 1 is the documentation half of that step.

2. **Confirm GitHub branch protection is in place** (set up in Track 0 step 5). If for any reason Track 0 step 5 was deferred, Track 7 is the catch-up location.

3. **Add a one-page `docs/TEST_VERIFICATION_MATRIX.md`** that names, per subsystem, which test files exercise it and which F-* gate codes the tests are guarding. A contributor changing `pipeline/orchestrator/router.py` should know they need to re-run `tests/orchestrator/test_router_classification_boundary.py` + `tests/orchestrator/test_provider_boundary.py` + the F-CLASS-* test suites. The discipline already exists in the operator's head; the doc surfaces it.

4. **PR template** (`/.github/PULL_REQUEST_TEMPLATE.md`) — five-line checklist:
   - `lock_history` row(s) this PR references: ___
   - F-* code(s) touched: ___
   - §-blueprint section: ___
   - Paired-commit sibling SHA (if applicable): ___
   - Co-Authored-By trailer included for AI-assisted commits: yes/no

**Effort:** 1-2 hours for items 1+3+4; item 2 is already done if Track 0 was executed (15 minutes catch-up if not).

**What this track does NOT do:** change which tests run, change CI infrastructure, alter the workflow file.

---

## Track 8 — Collaborator task queue *(new in v1.1)*

**Audience:** the same first technical contributor Track 5 hands off to — but answering "what do I do?" rather than "what is this?"
**Trigger:** after Track 5 (the contributor needs the handoff context before the queue is useful).

**Why this exists:** Track 5 tells a collaborator what the system is and what's safe to touch. It does not tell them what to pick up next. A collaborator without an ordered queue either waits for the operator to assign work (bottleneck) or picks something themselves that turns out to overlap with an in-flight ceremony (collision). A written queue prevents both.

### Deliverable: `docs/TECHNICAL_BACKLOG.md`

Six sections, in this order:

1. **Gate 1 blockers.** The specific work items that must complete before Gate 1 (internal replay with Paul) is reachable. Each item names: the subsystem, the F-* code or §-blueprint reference if applicable, the rough effort, and the operator's current view on priority. Examples likely to live here today: the §4 v2.x.6 runtime companion landing, the card runtime loader v0.2 wave, the Reflection Packet activation truth resolution.

2. **Gate 2 blockers.** Same shape, for the first-paid-client gate. Examples likely to live here: the signed classification register, the on-demand heavy Judge swap exercise, the production runtime card loader.

3. **Safe first tasks** (a "good-first-issue" equivalent). Work items that a new collaborator can pick up without touching LOCKed artifacts, gate code, or anything load-bearing. Examples: doc-truth sweep follow-ups from Track 1, the `TEST_VERIFICATION_MATRIX.md` first draft (Track 7 item 3), additional Track 3 maturity-matrix application, fixture cleanups, README polish items the form/function analysis flagged at P2/P3.

4. **Do-not-touch surfaces.** A redundant restatement of Track 5's "what not to touch" — but in queue form so a collaborator looking for "what should I avoid" finds it in the same document as "what should I pick up." Includes: `lock_history.v1.jsonl`, LOCKed blueprint amendment files (including cosmetic edits — see Track 4 item 3), F-* gate codes once LOCKed, root wake-up files' locations, signed asset directories.

5. **Needs Josh decision.** Work items that are *ready to pick up* but blocked on an operator decision (a roadmap choice, a priority call, a "yes we want this" gate). A collaborator pulling from this section means "I'm waiting on a decision," not "I'm working."

6. **Needs architecture / LOCK process.** Work items that require a blueprint amendment chain entry, a LOCK ceremony, or an architectural decision a contributor cannot make unilaterally. These are surfaced so a collaborator who notices "this would be useful" knows the path is "propose, don't unilaterally implement."

### Alternative form factor

If the operator enables GitHub Issues on the repo (currently off), the six sections above map cleanly to six labels (`gate-1-blocker`, `gate-2-blocker`, `safe-first-task`, `do-not-touch`, `needs-josh-decision`, `needs-arch-lock`). The markdown file and the Issues view can co-exist (the file is the canonical source the operator maintains; Issues are the contributor-facing surface) or the operator can pick one. v1.1 recommends starting with the markdown file because it's lower-overhead and survives without GitHub Issues being enabled.

**Effort:** 3-4 hours for the first draft (the categorization is the work; the writing is mechanical once items are sorted).

**What this track does NOT do:** assign work to specific people; create deadlines; replace the operator's judgment on what should be done next. It is a *queue*, not a *plan of record* — the operator can re-prioritize at any time, and the queue is the surface for that re-prioritization to be visible.

---

## Sequencing

The tracks have a strict order at the front and back, with parallel-OK in the middle.

1. **Track 0 — Merge / Branch / PR cleanup.** Runs first. Without this, the rest of the plan operates on a moving target.
2. **Track 9 — Secrets / Data / Access audit.** Runs second. Gates Track 5's access grant. More important than polish.
3. **Track 1 — Truth cleanup (current-facing only).** Depends on Track 0 (needs stable `main`). The current-vs-historical split is the v1.1 discipline.
4. **Track 3 — Maturity taxonomy (seven-state).** Produces the vocabulary Track 1 needs to finish, and feeds every subsequent track that labels a state. Can start in parallel with Track 1.
5. **Track 2 — Navigation layer.** Depends on Track 3 (the matrix needs the seven-state taxonomy).
6. **Track 4 — Repo simplification.** Independent of Tracks 2/3; can run in parallel. v1.1 reduces this track to a single file move.
7. **Track 6 — Claim hardening.** Depends on Tracks 1+3.
8. **Track 5 — Collaborator handoff (5a + 5b).** Depends on Tracks 1+2+3+9. Track 9 must be green before access is granted.
9. **Track 7 — CI confidence.** Independent; can run any time after Track 0. Some items (item 2) already complete if Track 0 step 5 was executed.
10. **Track 8 — Collaborator task queue.** Depends on Track 5 (the queue is for the collaborator the handoff hands off to). Runs last.

**Aggregate effort:** 27-42 hours across all ten tracks (revised upward from v1's 22-34 to reflect Tracks 0, 9, and 8 as new work; Track 1 slightly higher for current-vs-historical triage; Track 3 slightly higher for the seven-state taxonomy; Track 4 lower because two of v1's three items reverted into Track 2's sidecar work; Track 5 higher for the new local-development doc). Realistically a 3-4 working-week elapsed cycle if interleaved with the in-flight OD-A / OD-D / OD-C / OD-E ceremonies and the §4 v2.x.6 runtime companion landing.

**Single-day quick wins** (≤ 4 hours, no dependency on Track 0 completing): the P0 items from the form/function analysis — pyproject readme flip, README deleted-sentence-restore, README contact-handle revert, git identity configuration. None of these requires Track 3 vocabulary; all are pure form fixes. Note: these still touch `main` content, so they should land *after* Track 0 has merged PR #4 to avoid two simultaneous PRs against `main`.

## Operating principle (v1.1 restatement)

The repo does not need more content. It needs more legibility — but never at the cost of damaging what's already LOCKed or what's already historical record. Every track above either *labels* what is already there, *aggregates* it into a navigation surface, *aligns* current-facing claims across multiple docs, or *gates* the next step (Track 0 gating Track 1; Track 9 gating Track 5; Track 5 gating Track 8). The `lock_history` is the operator's truth and it stays untouched. The git tree is the engineering's truth and it stays untouched (except for the PR #4 mega-dump re-split in the form/function analysis P1). LOCKed amendment files stay exactly as LOCKed — no cosmetic headers, no in-place edits. Root wake-up files stay at root — no relocations that risk breaking working bootstrap chains. What changes is the *human-readable surface* around those preserved truths — the layer a Paul, a customer, or a future engineer actually reads first. The polish serves the preservation, not the other way around.
