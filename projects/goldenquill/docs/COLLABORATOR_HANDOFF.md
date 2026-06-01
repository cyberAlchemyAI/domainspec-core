---
title: Collaborator Handoff — role clarity for the first technical contributor
filed: 2026-05-17
audience: first technical collaborator outside the operator (e.g., Paul Norton, candidate engineer, paid reviewer)
companion_docs: docs/AGENT_CONTEXT_INDEX.md · docs/LOCAL_DEVELOPMENT.md · docs/TECHNICAL_BACKLOG.md
front_door: PROJECT_STATUS.md (root)
prerequisite: docs/LOCAL_DEVELOPMENT.md (read this before your first PR)
---

# Collaborator Handoff

This document is the role-clarity doc. It does not teach the system —
`README.md` does that, and `docs/AGENT_CONTEXT_INDEX.md` is the next step.
It does not list work — `docs/TECHNICAL_BACKLOG.md` does that. It tells
you who owns what, where the shared boundary is, what you should not
touch casually, where you can move fast, and what business reality this
codebase rests on.

## Who owns what

**Josh (operator):** grant logic, sales, market, client truth, founder
vision. He has won three competitive grants in 2026 using the manual
version of the workflow Tilth systematizes; he carries the substrate of
*why this works as a product* in a way no engineer can shortcut. The
following surfaces are operator-led: the Five Laws, the maturity
classification of any subsystem, the Customer Identity Categories and the
paired Eight Capital Logic Cards, every funder-dialect decision, every
client communication, every claim that ships to a buyer, every blueprint
amendment, every LOCK ceremony, every signed asset, every classification
register entry. If you're tempted to change product copy, dialect rules,
card content, or the F-* failure-code roster, that's an operator surface
— propose, do not commit.

**Technical collaborator:** simplification, runtime hardening, deployment,
CI, repo hygiene, test discipline. The work you're being asked to do is
real engineering: make the runtime more legible, expand test coverage
where it's thin, harden CI against the cross-Python-version matrix,
straighten what's tangled. You are not being asked to invent the product
or to second-guess the Five Laws. The product hypothesis is Josh's; the
discipline that proves it ships is yours.

## The shared boundary

Two surfaces are explicitly shared and require collaboration in both
directions:

1. **Blueprint amendments.** Any new `§N` amendment file, any change to
   an existing amendment's intent, or any LOCK ceremony is a paired
   operation between you and Josh. You can identify the *need* for an
   amendment (e.g., during a refactor you discover a §4 routing decision
   that needs to be specified in writing); you cannot draft the
   amendment without operator coordination because the amendment text is
   what the Ed25519 signing chain pins. The paired-commit discipline
   (every section amendment ships with a `section_00_5_…` interface-
   index paired-commit) and the `lock_history.v1.jsonl` append are
   operator ceremonies. See the cleanup plan v1.1 Track 4 item 3 for the
   "no in-place edits to LOCKed amendment files" rule.

2. **LOCK ceremonies.** Operator-led. Seeds, signing, ledger append,
   amendment_status flips, supersession rows, all of it. Your role is to
   notice when a change you want to make requires a LOCK (e.g., adding a
   new F-* failure-code family, changing a posture rule, adding a new
   §-blueprint section) and to surface that need cleanly so the
   ceremony can be scheduled. See `docs/TECHNICAL_BACKLOG.md` for the
   "Needs architecture / LOCK process" queue.

Inside those two surfaces, runtime hardening is collaborator-led: once
the spec is LOCKed, landing the runtime that satisfies it is engineering
work, and the §4 v2.x.6 runtime companion landing on 2026-05-17 is the
template for how that goes (Code session lands the refactor against the
LOCKed amendment, all green, paired-commit row already exists from the
LOCK ceremony, no further append needed at the runtime landing).

## Specific surfaces the collaborator should NOT touch casually

These are surfaces where a casual edit can break preservation discipline
or working bootstrap chains. Touching them is not forbidden, but it
requires operator coordination first.

- **Any LOCKed amendment file.** Anywhere under `pipeline/blueprint/v0.1/`
  or `pipeline/architecture/v0.1/` with `amendment_status: LOCKED` in
  its front matter. Cosmetic edits (whitespace, header restructuring)
  are *also* prohibited — the canonical bytes are pinned by the lock-
  history row and the Ed25519 signature. See cleanup plan v1.1 Track 4
  item 3.
- **`pipeline/engineering/lock_history.v1.jsonl`.** Operator-write-only.
  Append-only in normal operation; the only reason to touch it is to
  read.
- **Signed cards.** Anywhere under `pipeline/cards/` carrying an
  embedded `_research_metadata.ed25519_signature`. The OD-C and OD-E
  ceremonies on 2026-05-17 demonstrate the supersession-re-sign
  discipline — that's operator work.
- **Classification register signatures.** Anywhere under
  `orgs/<slug>/vault/classification/register.yaml` and the
  `signed/` subtree.
- **Root wake-up files.** `SOUL.md`, `USER.md`, `MEMORY.md`, `AGENTS.md`,
  `CLAUDE.md`, plus the agent-identity files (`IDENTITY.md`, `SKELETON.md`,
  `HEARTBEAT.md`, `TOOLS.md`, `lessons.md`). Many agent bootstrap
  chains hard-code these paths. Do not relocate, rename, or restructure
  without operator coordination. Content edits to `SOUL.md` and `USER.md`
  are operator-only.
- **`data/` and `orgs/`.** Per `.gitignore` these hold per-client data
  and operator-private context. Law 3 (Org Isolation) applies. The
  `_TEMPLATE/` subtree under `orgs/` is the one exception — that's the
  shape a new client folder copies from.

## Surfaces where the collaborator can move fast

These are surfaces where you should expect to commit freely (subject to
CI green and the PR template):

- **`pipeline/orchestrator/`** — runtime orchestration. Routers,
  dispatchers, the provider boundary, the classification context shape.
  The §4 v2.x.6 landing on 2026-05-17 is a recent example of how this
  surface accepts engineering refactors.
- **`pipeline/seats/`** — provider implementations for four council
  seats: Scribe, Editor, Judge, Red Team. (Scout's orchestrator-seat
  module lives at `pipeline/orchestrator/seats/scout.py`; Logician is
  its own top-level package at `pipeline/logician/`.) Watch the
  capstone-hash pins inside each seat's `__init__`; those are operator-
  signed surfaces that should be moved with care (see the §4 v2.x.6
  daily-log note for the pre-existing capstone-hash drift the runtime
  landing flagged).
- **`pipeline/orchestrator/seats/`** — the orchestrator-seat layer:
  Scout (`scout.py`), Intake (`intake.py`), Uploader (`uploader.py`),
  plus orchestrator-side modules for Editor / Judge / Red Team. Runtime
  glue around the provider implementations under `pipeline/seats/`.
- **`tests/`** — suite expansion is welcome. The cleanup plan v1.1 calls
  out test-coverage on dormant gate families and a forthcoming
  `docs/TEST_VERIFICATION_MATRIX.md` as safe-first-tasks.
- **`scripts/`** — shell helpers, including `run_tests.sh` and
  `run_lint.sh`. Improvements that preserve the interpreter pin
  discipline are welcome.
- **`pipeline/cli/`** — operator CLIs (e.g., `tilth posture select`).
- **`.github/workflows/`** — CI hardening (matrix expansion,
  dependency caching, additional smoke jobs).
- **`docs/`** — ongoing documentation. This file, the collaborator
  index, the local-development doc, the technical backlog are all in
  this category. PROJECT_STATUS.md is operator-leaning but you can
  propose edits via PR.

## The business hope layer — evidence, not hype

You should not read this codebase as a speculative bet. The product
hypothesis rests on operator-verified evidence:

- **Josh has already won grants using this workflow.** Three competitive
  grants in 2026 with the manual / Claude-skills-driven version of the
  pipeline that Tilth systematizes. The product is not a "could this
  work" — it's "this works manually; can we make it repeatable on
  customer-owned hardware."
- **The grant-writing workflow exists today.** Six-seat council, KGIE
  preflight, SMART outcomes, overlooked-expenses checklist, funder-
  dialect matching, two-audit cycle — every primitive that Tilth
  systematizes is something Josh runs by hand or by Claude skills now.
  Tilth is the productization, not the invention.
- **The sovereignty wedge is real market demand.** BYOK, local-first,
  customer-owned hardware (128 GB desktop), classification-aware
  routing — these are not philosophical talking points. They are the
  requirements that paying customers in sensitive funding domains (food
  systems, public agencies, cooperatives, tribal sovereign
  configurations on the Phase Two horizon) actually ask for. The
  competitive landscape is cloud-tenant grant-writing tools that hold
  customer data hostage; Golden Quill is the no-hostage alternative.
- **The architecture has discipline.** LOCKed amendment chain, signed
  registers, Ed25519 publisher key, paired-commit interface index, F-*
  failure-code families, deterministic Logician gates, two-audit Thesis
  cycles, cross-family adversarial review. None of that is
  decoration — every piece exists to keep the product honest as it
  scales past the operator's head. The discipline is the moat.

In the operator's own framing: *this is intense, but it is real. The
founder understands the market and grant logic. The architecture has
discipline. The mess is bounded. The collaborator's job is to help turn
this into a prosperous product.* You are not being asked to invent
demand; you are being asked to harden the substrate so the demand can be
served.

## How to start

1. Read `docs/LOCAL_DEVELOPMENT.md`. Get the venv up, get tests green.
2. Read `PROJECT_STATUS.md` (root) for the current state.
3. Read `RUNTIME_MATURITY_MATRIX.md` (root) for what's `runtime-live` vs.
   `spec-locked` vs. `dormant`.
4. Read `docs/TECHNICAL_BACKLOG.md` for the work queue. Pick from "Safe
   first tasks" before pulling from the Gate 1 / Gate 2 sections.
5. When you commit, follow the PR template:
   - `lock_history` row(s) this PR references (if any)
   - F-* code(s) touched
   - §-blueprint section
   - Paired-commit sibling SHA (if the PR pairs with a LOCK)
   - Co-Authored-By trailer for AI-assisted commits

For project orientation in any new session, the rule is path-reference,
not content-dump: read `pipeline/SESSION_BOOTSTRAP.md`. For institutional
memory, read `lessons.md`. For the Five Laws and Sovereignty Promise,
read `SOUL.md`. The wake-up sequence in `AGENTS.md` is the canonical
order.

The codebase names its debt openly — that's a feature, not a bug. When
you find something that's wrong, name it the same way: in a daily log,
in a handoff doc, in a backlog entry. The mess is bounded because it is
written down.
