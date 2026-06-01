---
title: GitHub Product-Truth Cleanup + Navigation Plan
filed: 2026-05-17
operator: Josh Inklovich
analyst: Claude Opus 4.7 (planning lane only — no LOCK ceremonies, no code edits, no doc rewrites in this artifact)
basis: operator's 2026-05-17 executive read + the GitHub form/function analysis at docs/github_form_and_function_analysis_2026-05-16.md
companion: pipeline/handoffs/audit_prompt_v1_1_pr4_staging_2026-05-16.md (audit playbook staging note)
posture: PLAN ONLY. This document proposes work; it does not perform it. Each track ends with a "what this plan does NOT do" line so the scope stays honest.
---

# GitHub Product-Truth Cleanup + Navigation Plan

## Frame

Two facts from the operator's 2026-05-17 read define everything that follows.

**Fact 1: PR #4 is the canonical product landing path.** It includes PR #3 verbatim, CI is green on Python 3.11/3.12 (wheel-smoke + lint + AST-lint + serial pytest), and `main` is still at `044415c` — last week's audit/CI commit, not the product state. The first move is to land PR #4 to `main`. Everything else here assumes that landing has happened or is about to.

**Fact 2: The remaining risk is narrative, not engineering.** The code, the gates, the schemas, the audit ledger, and the tests are real. The danger is *semantic overclaim* — governance language (LOCKED, signed, loaded) read as runtime-live language by a reviewer who doesn't know the difference. The cleanup work is about making the truth legible at three different reader depths: skimmer (README), collaborator (status docs), engineer (blueprint chain + lock ledger).

The plan is organized as six tracks plus a one-line "do not touch" boundary. Each track names the deliverable, the audience, the dependencies, the effort, and the explicit exclusions.

## Track boundary: what this plan does NOT do

This plan does NOT propose new LOCK ceremonies, code refactors, blueprint amendments, runtime companion code landings, ledger row writes, or any work that would interfere with the in-flight OD-A / OD-D / OD-C / OD-E ceremonies or the §4 v2.x.6 runtime companion Code session. Every recommendation below operates on documentation, navigation surface, repo metadata, or labels — never on the engineering tree, the lock_history, or the F-* gates.

---

## Track 1 — Truth cleanup on `main`

**Audience:** anyone landing on `main` cold (Paul Norton, a future engineer, a paying customer's tech reviewer).
**Trigger:** PR #4 merged to `main`.

Once PR #4 is on `main`, run a single coordinated "doc-truth sweep" against `main` (NOT the local dirty tree) that fixes the four classes of staleness:

1. **Stale row counts and test counts.** The README's "Focused v0.1 smoke suite on 2026-05-11: 339 tests passed" needs a refresh that points at the current PR #4 number (the operator's own commit body on `044415c` records `10,584 passed / 3 skipped / 1 xfailed`). The same kind of staleness lives in `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md`, `pipeline/planning/v0_1_beta_readiness_2026-05-10.md`, and any `docs/alpha_readiness_checklist.md`-style file that names a specific row total — the lock_history is now at row 262+ on disk, and any doc still naming row 216 / row 224 / row 235 / row 247 is reading as historical.
2. **PR #3 references.** Any doc that names PR #3 as the "clean baseline" or "next thing to land" is now superseded — PR #3 is absorbed by PR #4. Grep for `PR #3`, `PR/3`, `codex-pr2-cc003-cleanup`, `pull/3`.
3. **"Alpha" language.** Replace loose "Alpha" / "Alpha-ready" / "Alpha checklist" framing with **Gate 1 (internal replay with Paul)** and **Gate 2 (first paid client)** language per the operator's read. This is a global rename across `docs/alpha_readiness_checklist.md`, the README's Status paragraph, `docs/paul_norton_memory_alignment_brief_2026-05-15.md`, the website build spec, and any planning doc that uses "Alpha" as a state label.
4. **Runtime claims that exceed runtime state.** Anywhere a doc says cards are "loaded" or the system is "live" or "running in production," tighten to the precise maturity label from Track 3. The §4 v2.x.6 runtime companion has not landed; the card runtime loader is v0.2 first-wave; Brain/JIT is research-only; Reflection Packet activation truth needs care. The README *is* already careful about this (Local-Only/Sovereign is marked "performance-dependent / under validation"); extend that discipline workspace-wide.

**Deliverable:** a single `pipeline/handoffs/doc_truth_sweep_2026-05-XX.md` operator-facing punch list (gitignored), and the resulting PR that lands the fixes — call it **PR #5: doc-truth sweep** (or PR #6 if PR #5 is the v1.1 audit prompt landing).

**Effort:** 2-4 hours.

**What this track does NOT do:** rewrite blueprint section files, touch lock_history, alter the engineering tree, or introduce new product claims. It is a precision-edit pass on the human-readable surface.

---

## Track 2 — Navigation layer

**Audience:** collaborator (Paul, a future engineer) skimming for "where do I start."
**Trigger:** any time after Track 1.

The repo's discoverability problem is not that critical docs are missing — they exist and the README links to them — but that there is no single page that, on first read, tells a newcomer *what the system is doing today* vs. *what it was always going to do*. Three new docs solve this:

1. **`PROJECT_STATUS.md`** (root, two pages max). One paragraph per system, written as of a dated snapshot:
   - What works in `main` today.
   - What is parked.
   - What needs engineering judgment to move forward.
   - Last update timestamp + the commit SHA the status reflects.
   This is the page a new collaborator reads first. It is meant to go stale fast — that's fine, it has a date, and stale-but-dated is more honest than confident-and-undated.

2. **`ACTIVE_BLUEPRINT_INDEX.md`** (under `pipeline/blueprint/v0.1/` or at root, linked from README). A flat table:
   - Section number (§4, §11, §13, §18, etc.).
   - Canonical filename for the *current* head amendment (e.g., for §4 today that's `section_04_v2_x_6_router_dedup_amendment.md` *as the LOCKed head*, with the runtime companion noted as "not yet landed").
   - Amendment chain depth and the last LOCK ceremony row.
   - One-sentence "what this section is for" pointer.
   The blueprint directory has ~50+ amendment files now; without an index, the chain reads as archaeology. The index does NOT replace the amendment files — it points at them and tells the reader which one is the head.

3. **`RUNTIME_MATURITY_MATRIX.md`** (root, one page). One row per system (see Track 3 below for the six-state taxonomy). This is the single source of truth that all other docs cite when they make claims like "cards are loaded" — the matrix says specifically *which* loading state cards are in.

Also: add a **"What to read first" block** at the very top of the README pointing at these three pages in order. Eight-line block, no more.

**Effort:** 4-6 hours for first drafts; expect 2-3 iterations.

**What this track does NOT do:** generate new content. The three docs aggregate and label what already exists in the tree; they do not introduce new architectural claims.

---

## Track 3 — Runtime maturity labeling

**Audience:** anyone reading a doc that uses the word "loaded," "signed," "live," or "ready."
**Trigger:** PR #4 merged. Track 3 is the prerequisite for finishing Track 1 — you can't tighten a runtime claim without a vocabulary for what tightening means.

Adopt a six-state taxonomy and apply it consistently across `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, the README capability table, and every doc that makes a claim about a subsystem.

| Label | Meaning | Example |
|---|---|---|
| **runtime-live** | Code is in production paths, exercised by CI on every PR, and would fire on a real customer call today. | Provider-boundary enforcement (`enforce_outbound_boundary` wrapper), F-CLASS-* gates, AST-lint rules, the six-seat council dispatch path. |
| **gate-live** | The Logician gate exists, the F-* code is defined, the test exercises it deterministically, but the gate only fires inside the test substrate — production execution is not yet wired or not yet exercised. | Some of the F-cards-* gates landed in `a71f841` — the gate code is present and tested, but the runtime card loader that triggers them on real customer data is still v0.2 first-wave. |
| **signed asset** | The asset exists, is operator-signed (Ed25519 against the cards-publisher pubkey), is in the tree, and the signature verifies — but no runtime path loads it for real customer execution yet. | Cards Wave 1 + Wave 2 YAML cards. They are signed, LOCKed, and present at `pipeline/cards/`; the runtime loader hooks them up at v0.2. |
| **schema / scaffold** | The shape exists. The fields are named. The tests cover the shape. Implementation is partial or stubbed. | `pipeline/funder_intelligence/` (corpus discipline is real; the curation engine is not). `pipeline/funder_corpus/` PA-foundation dataset (data + tests; the runtime Match Database query is v0.2). |
| **dormant** | Code or doc exists but is not exercised, not on a near-term roadmap, and not load-bearing. Documented so a future contributor knows not to delete it. | The deprecated Sanitized fourth-posture defense-in-depth gates (per README historical note). |
| **historical** | Captured for audit / prior-art preservation. Explicitly not the current truth. | `pipeline/validation/v7_0_5_thesis_2026-05-09/` (preserved per AGENTS.md). The deleted `state_rules_cartridge.py` (post-rename to `state_rules_card.py`). |

Two operating rules for the taxonomy:

- **One label per system per doc.** A system cannot be "signed asset" in one place and "loaded" in another. The matrix is the arbiter.
- **Promotion is a paired ceremony.** Moving a subsystem from `signed asset` → `gate-live` → `runtime-live` is a status change that requires a lock_history row (or at minimum a dated entry in `PROJECT_STATUS.md`) — same discipline as the blueprint amendment chain. This prevents quiet upgrades from making the matrix lie.

**Effort:** 2-3 hours to define labels (this doc starts that work), 4-6 hours to apply the labels across the docset.

**What this track does NOT do:** define new failure codes, gate behaviors, or runtime states. It puts a vocabulary on states that already exist.

---

## Track 4 — Repo simplification

**Audience:** anyone navigating `~/Downloads/GoldenQuill` for the first time.
**Trigger:** PR #4 merged; Track 2 navigation docs drafted.

Three concrete simplifications:

1. **Move `FOUNDATION_README.md` out of root** (per the form/function analysis P2 #9). It's a 2026-04-14 artifact that describes this repo as "the clean restart" — internal context, not product narrative. Either `docs/operator/FOUNDATION_README.md` or `pipeline/handoffs/FOUNDATION_README.md` (the latter is gitignored, which may be the right call for an artifact that's no longer load-bearing).

2. **Group the operator-orientation files.** `AGENTS.md`, `CLAUDE.md`, `HEARTBEAT.md`, `IDENTITY.md`, `MEMORY.md`, `SKELETON.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `lessons.md` all serve the agent wake-up sequence and are correctly committed. The root listing would benefit from either a small `agent/` (or `_agent/`) subdir that holds them, with `AGENTS.md` remaining at root as the entry point that links to the rest. This is a polish move, not a content move — the sequence in `AGENTS.md` still drives discovery; the file tree just stops looking like a personification archive.

3. **Add a one-paragraph header to every blueprint amendment file** (existing ones, not new ones — no LOCK ceremony required because amendment text is NOT being changed). The header is a single block above the existing frontmatter that says: "This amendment is the head of §4 as of lock_history row XXX," OR "This amendment is superseded by section_04_v2_x_7_amendment.md (row XXX)," OR "This amendment is dormant." Track 2's `ACTIVE_BLUEPRINT_INDEX.md` is the authoritative version of this; the per-file headers are the courtesy version for someone who landed on a single amendment via a deep link.

**Effort:** 1-2 hours for items 1+2; 3-4 hours for item 3 (~50 amendment files × 5-minute header).

**What this track does NOT do:** delete any tracked file from the engineering tree; rewrite or modify any amendment content; alter the AGENTS.md wake-up sequence.

---

## Track 5 — Collaborator handoff

**Audience:** the first technical contributor outside the operator (Paul Norton, candidate engineer, or paid reviewer) who is given push or review access.
**Trigger:** before granting that access.

One new doc: **`docs/COLLABORATOR_HANDOFF.md`** (or `CONTRIBUTING.md` — same content, different filename convention). Covers, in this order:

- **What Golden Quill is, what Tilth is** — one paragraph each, pulled directly from the README so the framing is identical.
- **What works today** — pointer to `PROJECT_STATUS.md` + `RUNTIME_MATURITY_MATRIX.md`.
- **What is parked** — pointer to the dormant/historical rows of the matrix.
- **What needs engineering judgment** — the three or four open architectural questions that a contributor should know exist before they propose changes (e.g., the card runtime loader landing schedule, the §4 v2.x.6 runtime companion in flight, the Reflection Packet activation truth).
- **How to run tests** — `scripts/run_tests.sh -n auto --dist=loadfile` locally; the CI matrix on PR #4 is canonical.
- **What not to touch** — the lock_history.v1.jsonl is operator-write-only; blueprint amendment files have a LOCK ceremony attached and are not edited in-place; F-* gate codes do not change once LOCKed without an amendment chain entry.
- **How to propose work** — commit message discipline (§-blueprint reference, F-* code, lock_history row, paired-commit sibling SHA), the PR template from Track 7.

**Effort:** 2-3 hours.

**What this track does NOT do:** publish or grant access. It writes the doc that gets pointed at when access is granted.

---

## Track 6 — Claim hardening

**Audience:** every doc that makes a sovereignty, alpha-readiness, or paid-client-readiness claim.
**Trigger:** after Tracks 1+3, before any external visibility move (Paul review, website launch, customer pitch).

Five docs need to tell the same truth, distinguishing three readiness states:

| Doc | Today's state | Target state |
|---|---|---|
| `README.md` | Strong; one regression (deleted sentence + handle change in PR #4 — see analysis P0 #2). | Gate 1 / Gate 2 language explicit. |
| `docs/alpha_readiness_checklist.md` | Uses "Alpha" framing. | Renamed `docs/gate_1_internal_replay_checklist.md` + companion `docs/gate_2_first_paid_client_checklist.md`. |
| `docs/paul_norton_memory_alignment_brief_2026-05-15.md` | Internal review framing. | Aligned to Gate 1 language; explicitly named as a Gate 1 input. |
| `docs/golden_quill_website_build_spec_v1.md` | Public-facing claim surface. | Every claim labeled with a maturity tag from Track 3. No "loaded" or "live" without a matrix backing. |
| Onboarding docs (`docs/platform_engineer_onboarding.md`, `docs/platform_engineer_quick_reference.md`) | Operator-oriented. | Aligned to Track 5 handoff doc; Gate 1 vs Gate 2 distinction inherited. |

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
**Trigger:** any time after PR #4 lands.

Three small additions on top of the already-green CI:

1. **Pin the matrix in writing.** Add a `## CI` section to the README (or to `COLLABORATOR_HANDOFF.md`) that names the required checks: `quality-gate (3.11)`, `quality-gate (3.12)`, `wheel-install-smoke (3.11)`, `wheel-install-smoke (3.12)`. This closes the loop between "we have CI" and "what does merge actually require."

2. **Configure GitHub branch protection on `main`** to require those four checks + at least one review (operator self-review counts today). UI-only step; cannot be done from a sandbox.

3. **Add a one-page `docs/TEST_VERIFICATION_MATRIX.md`** that names, per subsystem, which test files exercise it and which F-* gate codes the tests are guarding. A contributor changing `pipeline/orchestrator/router.py` should know they need to re-run `tests/orchestrator/test_router_classification_boundary.py` + `tests/orchestrator/test_provider_boundary.py` + the F-CLASS-* test suites. The discipline already exists in the operator's head; the doc surfaces it.

4. **PR template** (`/.github/PULL_REQUEST_TEMPLATE.md`) — five-line checklist:
   - lock_history row(s) this PR references: ___
   - F-* code(s) touched: ___
   - §-blueprint section: ___
   - Paired-commit sibling SHA (if applicable): ___
   - Co-Authored-By trailer included for AI-assisted commits: yes/no

**Effort:** 1-2 hours for items 1+3+4; 15 minutes for item 2 (UI).

**What this track does NOT do:** change which tests run, change CI infrastructure, alter the workflow file.

---

## Sequencing

The tracks have a soft order:

1. Merge PR #4 to `main` (operator decision).
2. Track 1 (truth cleanup) — depends on PR #4 merge.
3. Track 3 (maturity taxonomy) — produces the vocabulary Track 1 needs to finish.
4. Track 2 (navigation layer) — depends on Track 3.
5. Track 4 (repo simplification) — independent; can run in parallel with Track 2.
6. Track 6 (claim hardening) — depends on Tracks 1+3.
7. Track 5 (collaborator handoff) — depends on Tracks 1+2+3.
8. Track 7 (CI confidence) — independent; can run any time after PR #4.

**Aggregate effort:** 22-34 hours across all seven tracks. Realistically a 2-3 working-week elapsed cycle if interleaved with the in-flight OD-A / OD-D / OD-C / OD-E ceremonies and the §4 v2.x.6 runtime companion landing.

**Single-day quick wins** (≤ 4 hours, no dependency on PR #4 merge): the P0 items from the form/function analysis — pyproject readme flip, README deleted-sentence-restore, README contact-handle revert, git identity configuration. None of these requires Track 3 vocabulary; all are pure form fixes.

## Operating principle

The repo does not need more content. It needs more legibility. Every track above either *labels* what is already there, *aggregates* it into a navigation surface, or *aligns* claims across multiple docs that already exist. The lock_history is the operator's truth and it stays untouched; the git tree is the engineering's truth and it stays untouched (except for the PR #4 mega-dump re-split in the form/function analysis P1). What changes is the *human-readable surface* around those two truths — the layer a Paul, a customer, or a future engineer actually reads first.
