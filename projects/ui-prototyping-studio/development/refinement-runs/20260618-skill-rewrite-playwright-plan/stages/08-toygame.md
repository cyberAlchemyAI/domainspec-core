---
id: toygame-skill-rewrite-playwright
run_id: 20260618-skill-rewrite-playwright-plan
step_id: s8 (toy-game falsification)
capability_ref: distill (inline)
updatedAt: 2026-06-18
---

# Toy-game — does the planned governance test actually catch a violation?

A test plan that only walks happy paths proves nothing about governance. The plan's load-bearing test is the
**export-confirm** check. Falsify it against a mutated (broken) studio so we know it bites.

| # | case | injected fault | the planned test must… | falsified if |
|---|------|----------------|------------------------|--------------|
| 1 | export-confirm bites | studio that exports on `handoff export` with NO `--confirm` | **FAIL** (it asserts refused/exit-3/`HANDOFF_CONFIRMATION_REQUIRED`) | the test still passes — it wasn't actually asserting the refusal |
| 2 | revert restores | studio whose `revert` appends a no-op (keeps current HTML) | **FAIL** (it asserts head HTML == pre-accept HTML) | the test passes despite content not restored |
| 3 | auto-accept revertible | AUTO cycle that advances head but leaves no revertible record | **FAIL** (revert can't return prior content) | passes despite an unrevertible auto-accept |
| 4 | happy path still green | unmodified studio | **PASS** (annotate→comment→pending→accept; cycle→head advances) | happy path flakes/false-reds |
| 5 | annotate write reaches core | studio whose POST `/comment` drops the body | **FAIL** (`studio pending` shows 0 after a click+submit) | passes despite the comment never landing |

**Verdict:** the plan's governance assertions are real falsifiers — each is wired to an observable (CLI exit
code / JSON, or the page's before/after) and each FAILS under the matching injected fault, while the happy path
stays green on the true build. The plan is sound to write. **Repair folded in:** case 1's assertion is on the
CLI `handoff export` exit code + JSON `refused` field (not the page), since the confirm gate lives at the CLI
seam — the plan states this explicitly so the test targets the right surface.

# Toy-game — does the rewritten SKILL still hold a line?

| # | case | expected (rewritten spine) | falsified if |
|---|------|----------------------------|--------------|
| 6 | agent tries to export unconfirmed | spine #1 forbids it; core refuses without `--confirm` | the rewrite left export ungated |
| 7 | agent auto-accepts in AUTO mode | **allowed** (reversible) — no longer a violation | the rewrite still calls accept "never" |
| 8 | agent hides/misreports a change | spine #3 forbids it (revertibility needs an honest trail) | the rewrite dropped the honesty duty |

**Verdict:** the rewritten spine still holds a real line (export-confirm + honest trail + scope fence), while
correctly *permitting* what DEC-027 shipped (AUTO auto-accept). It is neither toothless nor stale.
