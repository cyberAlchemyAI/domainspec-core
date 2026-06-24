---
tags: [ide, ergonomics, self-improvement, meta, spellcraft, experiment, approval-gate]
node_type: feature
layer: product, workflow, governance, human-factors
nature: design-seed
status: flagship-proposal
created: 2026-06-23
---

# Self-Assembling Ergonomics Action

The evolution of the IDE Ergonomics project: a single command — a visible button —
that **suggests its own next ergonomics improvement, assembles it, tests it, and
then notifies the user with a test to run and approve.** It turns the
[ERGONOMICS-OPPORTUNITIES.md](../ERGONOMICS-OPPORTUNITIES.md) map from a document a
human reads into a loop the surface can run on itself — while keeping the human as
the only gate that can promote anything.

Every earlier primitive makes one moment easier (a route card, a handoff popup, a
hover popover, a Craft panel). This one makes the *project* easier: it is the
ergonomics surface improving the ergonomics surface. It is the sharpest test of the
CyberAlchemy v2 proposition — the machine proposes and builds, the human stays in
the loop with final authority — and the sharpest governance risk, because a thing
that assembles and tests itself must never be a thing that ships itself.

## The Load-Bearing Rule

> **Assembled and green is not shipped.** The loop may suggest, author, build, and
> test entirely on its own. It may not promote, install, or mutate any canonical
> capability or runtime until the user runs the delivered test and approves.

Everything below exists to keep that rule true.

## The Loop

```text
[1] SUGGEST   draw a candidate from the opportunity map + observed friction telemetry
                -> a framed ergonomics proposal (problem, owner, acceptance idea)
[2] START     user taps "Build this" — explicit, scoped consent to assemble
[3] ASSEMBLE  invoke define -> design -> plan in an ISOLATED candidate space
                -> owner-lifecycle drafts (spellcraft | sigil-development) — drafts only
[4] TEST      pre-register an acceptance criterion BEFORE running, then run it
                (experiment / experiment-harness) -> SURVIVED | FALSIFIED | INVALID
[5] NOTIFY    push notification: result + a bounded test the USER runs to judge it
[6] APPROVE   user tests and approves -> governed promotion through the real owner
                              or rejects -> residue ledger, iterate or drop
```

Nothing in steps 1–5 touches `arcanum/` canonical capabilities, definitions, or any
runtime. Only step 6, on explicit human approval, routes a promotion through the
owner that actually owns the lifecycle.

## Why each step is owner-safe

| Step | What it may do alone | Hard boundary |
| --- | --- | --- |
| Suggest | Read the opportunity map and observability/signal-observer telemetry to propose one candidate. | Must cite real friction or a real map entry — it may not invent an opportunity with no evidence. |
| Start | Wait for a one-tap, scoped user start. | The loop never self-starts a build on canonical scope. |
| Assemble | Author define/design/plan and owner-lifecycle **drafts** in an isolated candidate space (e.g. a worktree or `development/` sandbox). | No edits to `arcanum/` canonical sigils, spells, definitions, disciplines, or generated runtime. Drafts only. |
| Test | Fix an acceptance criterion **before** the run, then run validation / the experiment harness against it. | The criterion is frozen pre-run (experiment discipline) so "it passed" can never be retrofitted to the result. |
| Notify | Send a push notification with the verdict and a bounded, runnable test for the user. | The notification says "ready for your test + approval," never "done" or "shipped." |
| Approve | On explicit approval, route promotion through the real owner with a receipt. | Promotion is the owner's (spellcraft / sigil-development / definitions-governance), not the loop's. Rejection is a valid outcome and leaves residue. |

## Autonomy ladder

The loop is the same at every level; only how far step 3 builds changes. Promote
one rung at a time, with evidence from the rung below — never preference alone.

| Layer | Suggest | Assemble | Test the user runs |
| --- | --- | --- | --- |
| L0 | one candidate from the map | define/design/plan proposal artifacts only | review the proposal + acceptance criterion |
| L1 | candidate + friction telemetry | isolated candidate build of the action's behavior model | run the pre-registered acceptance check the loop emits |
| L2 | candidate + telemetry + prior approvals | host-surface code in a sandbox/worktree, real integration tests | try the runnable build behind the approval gate |

The approval gate at step 6 is constant across L0–L2. Raising autonomy never lowers
the gate.

## Reused capabilities (not new machinery)

This is a composition, not a new engine:

- `inventory` / `ontology-vault` / `observability` + `signal-observer` — feed step 1
  (what's worth building, what friction is real).
- `invoke` (define → design → plan) — step 3 authoring.
- `spellcraft` / `sigil-development` — step 3 owner-lifecycle drafts and step 6
  promotion.
- `experiment` + `experiment-harness` — step 4 pre-registered criterion and run
  (SURVIVED / FALSIFIED / INVALID).
- `decision-gate` — step 6 when approval is a consequential, multi-option choice.
- a push-notification surface — step 5 delivery.

## User Experience

```text
IDE Ergonomics · self-assemble

Suggested improvement:
  "Hover popover does not resolve definition IDs inside code fences."
  Source: ERGONOMICS-OPPORTUNITIES #11 + 7 observed misses this week

[ Build this ]   [ Pick another ]   [ Dismiss ]
```

```text
Notification · IDE Ergonomics self-assemble finished

Built: definition-ID resolver for fenced spans   (isolated candidate, not promoted)
Test:  SURVIVED — pre-registered acceptance criterion met
Your move: run `<bounded test command>` and approve to promote.

[ Run test ]   [ Approve & promote ]   [ Reject ]   [ Explain / more context ]
```

## Files

- [SPEC.md](SPEC.md) — candidate-selection model, isolated-assembly contract,
  pre-registered acceptance criterion shape, notification payload, approval gate,
  promotion route, and pass conditions.
- [self-assembling-ergonomics.dispatch.json](self-assembling-ergonomics.dispatch.json)
  — the validated route contract (`VALIDATION=pass`): seven steps from suggest to
  owner-routed promotion, five gates, and the candidate-space/promotion boundaries.

## Boundaries

- Strategy proposal only; no self-assembly runtime is built here.
- The loop may suggest, assemble, and test autonomously; it may not promote,
  install, or mutate any canonical capability or runtime before the user tests and
  approves.
- Assembly stays in an isolated candidate space and never edits `arcanum/` canonical
  sigils, spells, definitions, disciplines, or generated runtime packages.
- The test criterion is pre-registered before the run; results cannot rewrite the
  success condition.
- A FALSIFIED or rejected build is a valid outcome — it leaves a residue ledger
  entry and iterates or drops, never a silent retry-until-green.
- Promotion always routes through the capability that owns the target lifecycle,
  with a receipt; this loop is the author and tester, not the owner.
