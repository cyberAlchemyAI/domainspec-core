---
id: plan-fixes-ups-ux-interaction
project: ui-prototyping-studio
title: "Plan — all review findings (Fs): close the change-requests, gate the build"
node_type: implementation-plan
invoke_mode: plan
run_id: 20260616-ui-ux-interaction-skill
status: proposal
complexity: medium
updatedAt: 2026-06-16
---

# Plan — all Fs (review dispatch 2026-06-16-ups-skill-design-review)

Closes every verified finding from the review and sequences what they gate. The **doc-fix Fs are already
APPLIED** by the refresh (see `REFRESH-REPORT.md`); this plan records them as closed-with-verification and
isolates the **two real pieces of forward work**: the **F2 core identity-gate decision** (pre-build), and
the **build the corrected SKILL + design now unblock**. Planning artifact — `[PROPOSAL]`, nothing executed;
each open unit runs via a separate `task-session`.

## Finding → unit → status

| F | Sev | Unit | Status | Verification |
|---|---|---|---|---|
| F1 | CRITICAL | FX-DOC (design step-7 + §5.1 honest rewrite) | **APPLIED** | grep the design for "refused server-side if it tries" → absent; step-7 cell states scope≠identity |
| F4 | MAJOR | FX-DOC (s2 forward-correction banner) | **APPLIED** | s2 §1.2 + step-7 carry the F4 correction pointing at RESULT §3.1 |
| F3 | MAJOR | FX-DOC (SKILL authorship rule) | **APPLIED** | SKILL spine has the authorship bullets + must-NOT line; "offer" defined; "on the human's behalf" scoped |
| F5 | MINOR | FX-DOC (RESULT §3.1 grammar) | **APPLIED** | web-ui default scoped to apply route |
| F6 | MINOR | FX-DOC (step-9/10 lead single-gate) | **APPLIED** | step-9/10 cells lead with runnable single-gate, two-gate as target |
| F7 | MINOR | FX-DOC (ergonomic superlatives → hypothesis) | **APPLIED** | no asserted ergonomic gain remains in design §3 cells |
| F8 | MINOR | FX-DOC (one gate-count convention) | **APPLIED** | SKILL loop section states 5 gates, baseline = 2 commands at 1 gate |
| **F2** | **build-blocking ROUTE** | **SWU-F2a decision + SWU-F2b core impl** | **OPEN — pre-build gate** | see below |

**FX-DOC is closed.** The only way it regresses is a future edit re-introducing the overclaim; the C-1-style
guard is a one-line grep check added to the build's pre-flight (below).

---

## SWU manifest (open units)

| SWU | Title | Depends on | Write scope | Acceptance (one-line) |
|-----|-------|-----------|-------------|-----------------------|
| **F2a** | Decide the human-vs-agent identity gate (R-S7-1 / P-c3) | FX-DOC | decision record only | `decision-gate` resolves: identity-gate design (token vs actor-allowlist vs OS-user) + whether it blocks build or ships interim |
| **F2b** | Implement the core identity gate (if F2a says "before build") | F2a, backend M-layer | `backend/.../application/{approve,apply}-*.ts`, route actor parsing, tests | a non-human actor is refused at `approve`+`apply` server-side; unit tests; AC for INV-3 identity |
| **S1** | Install the corrected SKILL (interim, honest) | FX-DOC, F2a | project `SKILL.md` | `06-SKILL-draft.md` (post-F1/F3/F8) promoted to live `SKILL.md`; teaches only runnable verbs; authorship rule present |
| **B-PRE** | Build pre-flight guard | FX-DOC | `e2e/` or a check script | grep guard: no "refused server-side if it tries" in design/SKILL; SKILL command table == `studio.ts` verbs |
| → | **then the existing build waves** | S1, F2(a/b) | per `WORK-PACK.md` | the corrected SKILL/design feed `WORK-PACK.md` W7 (SWU-P preview), M2-wire (two-gate accept-diff), U1/U2 |

## F2 — the one consequential decision (decision-gate input)

- **Question:** does the core get a real human-vs-agent identity gate at the 5 durable gates **before** the
  SKILL/page ship, or does an honest-interim ship first (spine = sole control, disclosed) with the gate as a
  fast-follow?
- **Options (for `decision-gate`):**
  1. **Per-session human-only token** — the served page shows a secret the agent cannot read; the core
     requires it at `approve`/`apply`/`accept`. Strongest; needs the page (W7) first.
  2. **Actor allowlist / deny the agent actor** — extend the `system:auto` denylist to refuse the known
     agent actor(s); cheap, weak (agent can set `STUDIO_ACTOR`).
  3. **OS-user / out-of-band identity** — bind the gate to a credential the CLI agent process lacks.
  4. **Honest interim** — ship with the spine as the disclosed sole control; gate as fast-follow (the
     current corpus already discloses this honestly post-F1).
- **Recommendation to surface:** option 1 as the target, option 4 as the interim — but this is the owner's
  call; route via `decision-gate`, do not auto-decide.

## Implementation-layering (value/cost)

- **L0 — FX-DOC (done):** honesty floor; promotion evidence = the grep guard + the review's resolved close.
- **L1 — F2a decision:** unblocks everything identity-related; promotion = a recorded `decision-gate`.
- **L2 — S1 SKILL install + B-PRE guard:** makes the corrected contract live + regression-guarded.
- **L3 — F2b core gate (if before-build):** the real control; promotion = server-side refusal tests.
- Then the existing `WORK-PACK.md` build layers (P/M2-wire/U1/U2) consume the corrected docs.

## Validation strategy (per slice)

- FX-DOC → the grep guard (B-PRE) + the resolved review close.
- F2a → a persisted decision record (`decision-gate`).
- F2b → server-side identity-refusal unit tests + an INV-3 identity AC.
- S1 → the SKILL command table matches `studio.ts`; authorship rule present; no overclaim (B-PRE).

## Next route

`decision-gate` for **F2a** (the only blocker), then `task-session`: **S1** (install corrected SKILL) +
**B-PRE** (guard), then F2b if F2a says before-build, then the existing `WORK-PACK.md` build waves. The
doc-fix Fs need no further work — they are applied and guarded.
