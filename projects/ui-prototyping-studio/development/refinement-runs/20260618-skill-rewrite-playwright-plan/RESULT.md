---
id: result-skill-rewrite-playwright
project: ui-prototyping-studio
title: "RESULT — SKILL rewrite (reversibility) + Playwright closed-loop test plan"
status: pass
node_type: refinement-result
run_id: 20260618-skill-rewrite-playwright-plan
dispatch_id: refine-ups-skill-rewrite-playwright-20260618
capability_ref: refine
updatedAt: 2026-06-18
---

# RESULT — SKILL rewritten + Playwright plan authored

## Answer
Two coupled deliverables, both done:
1. **`.claude/skills/ui-prototyping-studio/SKILL.md` rewritten** to the reversibility model (DEC-026/027).
2. **`development/PLAYWRIGHT-CLOSED-LOOP-TEST-PLAN.md` authored** — e2e over the preview HTTP surface, both
   modes, with a governance-falsification suite as the gate.

## SKILL rewrite — what changed (the dialectic resolution)
The old spine ("You propose. The human disposes.") protected against irreversible agent action when nothing
could be undone. Now `revert` exists, so the spine **relocated** rather than vanished:
- **Posture:** "Every change is reversible — you may drive the whole loop; the human owns the one
  irreversible edge: export."
- **Two modes taught:** HUMAN (human selects/accepts) and AUTO (you run `cycle`, auto-accept the top score).
- **`studio accept` reframed:** the false "Never call this" is gone — HUMAN: human accepts; AUTO: you
  auto-accept; both revertible.
- **New never-do spine (5):** never export without human `--confirm`; never bypass the fence / forge an
  od-id; always leave a revertible, honestly-diffed trail; never start AUTO with an empty objective; never
  claim an ergonomic benefit.
- **Honest authority note rewritten:** safety = reversibility + export-confirm, NOT an identity gate (the
  core needn't know who you are). Explicitly supersedes the prior "agent must never accept".
- **Surface updated:** `revert`, `cycle`, `pending`, `watch`, `preview` (+ annotate) documented; the stale
  "preview does not exist yet" / "no accept/discard" claims removed.
- **Kept unchanged:** plain-language narration, DC-1 comment shape, scope-fence honor, no-ergonomic-claim.

## Playwright plan — shape
e2e over the `studio preview` loopback server + CLI seam, validator-safe (user-facing locators, observable
assertions). Layers: L0 smoke · HUMAN happy path (annotate click→`/comment`→pending→synthesize→stage→diff→
accept) · AUTO (`cycle` exploit/explore→auto-accept→preview refresh) · **GOVERNANCE falsification**
(export-without-confirm must FAIL with exit 3; revert restores pre-accept HTML; auto-accept is revertible) ·
sandbox boundary (raw stays no-scripts; annotate wrapper posts on click). Honest non-coverage: UX-constraint
fitness (OQ-5), stop-dial enforcement, L1/L2 a11y/layout.

## Falsification (stages/08-toygame.md)
Both toy-games pass: the governance specs FAIL under matching injected faults (unconfirmed export, no-op
revert, unrevertible auto-accept, dropped `/comment` body) while the happy path stays green; the rewritten
spine still holds a real line (export-confirm + honest trail + fence) while permitting AUTO auto-accept.

## Residue
SKILL rewrite *loses* the absolute "human disposes everything" guarantee (deliberate — DEC-026) and *keeps*
the human-owns-the-irreversible-edge + honesty duties. The Playwright plan is non-executed; wiring is a
follow-up `task-session`.

## Stage evidence
s1–s10 pass (x-ray keep/rewrite + dialectic in stages/06-design.md; two toy-games in stages/08-toygame.md;
the SKILL rewrite + the test plan are the plan-stage outputs). Research: research-if-gap — none (Playwright +
ux-evidence-validator local).

## Recommended next routes
`task-session` to wire + implement the Playwright specs (governance falsifiers first). The MAKE-MVP DOC
public-republish — now unblocked on the SKILL side (the pre-publish rewrite is done) — still pending your go.
