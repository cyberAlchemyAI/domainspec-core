---
id: design-skill-rewrite-playwright
run_id: 20260618-skill-rewrite-playwright-plan
step_id: s2+s5+s6 (x-ray + distill + dialectic, consolidated)
capability_ref: invoke+distill (inline)
updatedAt: 2026-06-18
---

# Design — SKILL rewrite (reversibility) + Playwright closed-loop test plan

## §1 X-ray — every SKILL control statement, keep | rewrite

| Current statement | Verdict | New form under DEC-026/027 |
|---|---|---|
| "You propose. The human disposes." (posture) | **REWRITE** | "Every change is reversible. You may drive the whole loop; the human owns the one **irreversible** edge — export." |
| Loop table: 5 "human-alone disposes" gates (baseline/approve/apply/accept/export) | **REWRITE** | Only **export** is human-required. Baseline/accept are **mode-dependent**: HUMAN mode the human leads; AUTO mode you drive (reversible). |
| `studio accept` = "**NO — human gate. Never call this.**" | **REWRITE (false today)** | AUTO: you auto-accept (via `cycle`, or `accept` after stage). HUMAN: the human accepts. Either way **revertible** (`studio revert`). |
| `studio baseline select/commit` = human gate | **REWRITE** | HUMAN mode: human picks. AUTO mode: you may select to seed a direction (reversible). |
| `studio batch approve` = human gate | **SOFTEN** | A workflow step, not a safety gate; reversible downstream. AUTO bypasses it via `cycle`. |
| never-do spine: "Never approve, apply, or accept" / "never advance head" | **REWRITE** | Spine **relocates** to the irreversible edge (see §2). |
| Honest authority note (F-CRIT-1): "core can't tell you apart; spine is the only control" | **REWRITE** | Safety = **reversibility + export-confirm**, not an identity gate. You don't need the core to identify you; you need every act to be undoable + the export edge confirmed. |
| "Target gates that DO NOT EXIST YET — `preview --annotate`" | **REWRITE (now exists)** | `studio preview` + `/annotate` + click→comment now ship (CL1/P1). |
| Allowed-commands table | **EXTEND** | Add `revert`, `cycle`, `pending`, `watch`, `preview`, annotate `/comment`. |
| "claims no verb absent from surface (no preview/accept/discard)" | **REWRITE (now present)** | Those exist; the claim-only-runnable-verbs discipline stays. |
| Plain-language narration duty; no-ergonomic-claim; scope-fence honor; DC-1 comment shape | **KEEP** | Unchanged — still true and load-bearing. |

## §2 Dialectic — propose/dispose (identity gate) vs reversibility-not-gating

- **Thesis (old spine):** the agent must never run a durable gate, because the core can't tell it from the
  human and the action would be irreversible.
- **Antithesis (DEC-026/027):** control is reversibility; the agent may drive everything because `revert`
  exists and the preview makes it visible; identity is irrelevant.

**Synthesis — the spine RELOCATES, it doesn't vanish.** The old spine protected against *irreversible* agent
action when *nothing* could be undone. Now that `revert` exists, almost nothing is irreversible — so the
protection moves to the **one thing still irreversible: export** (downstream consumption), plus the duty to
**leave a revertible, honestly-diffed trail**. New never-do spine:
1. **Never `handoff export` without an explicit human `--confirm`** — the one irreversible edge.
2. **Never bypass the scope fence or forge/re-tag a `data-od-id`** (core-enforced; honor it).
3. **Always leave a revertible, honestly-diffed trail** — record provenance, surface the honest od-id diff,
   never hide or misreport what you changed. (Reversibility is only a real safety net if the trail is honest.)
4. **Never start an AUTO cycle without a human objective** (the start gate — exploit toward nothing is void).
5. **Never claim an ergonomic benefit** (unproven — charter clause 5). **Plain-language narration** stays.

**Residue:** *lost* — the absolute "human disposes every durable change" guarantee (deliberately, per DEC-026).
*kept* — the human owns the irreversible edge, honesty duties, the scope fence, no-ergonomic-claim. *gained* —
AUTO mode (hands-off cycles) is now legitimate, not a violation.

## §3 The two modes the rewritten SKILL must teach
- **HUMAN-in-the-loop:** human selects baseline, points at components (you record comments — DC-1), you
  propose + stage; the **human** accepts/reverts. You narrate state at each step.
- **AUTO (exploit/explore):** the human gives an **objective**; you run `studio cycle` — generate candidate
  HTML + a self-critique score, the core gates via the fence and **auto-accepts the top score**; you may loop
  (`watch`/`/loop`) within the human's stop dials. Every accept is revertible; you surface each change.
- **Both:** export is the one human-`--confirm` edge.

## §4 Playwright test-plan shape (the second deliverable)
e2e over the **preview HTTP surface** (the `node:http` loopback server `studio preview` starts), driven by a
CLI-seeded session. Layers (reuse the UX-EVIDENCE-REPORT L0–L4 vocabulary):
- **L0 smoke:** preview page mounts; variant iframes resolve; `/state` returns JSON.
- **Closed-loop happy path (HUMAN):** open `/annotate/variant/A` → click `cta.primary` → the parent comment
  form opens prefilled with the od-id → submit → `POST /comment` 200 → `studio pending` shows 1 → synthesize →
  `apply` stages → preview shows before/after + honest diff → `accept` → head advances.
- **AUTO path:** seed objective → `studio cycle exploit --candidate f:score` → head advances to the winner →
  preview auto-refreshes (poll on `/state`) to show it.
- **GOVERNANCE falsification (the load-bearing test):**
  - `handoff export` **without** `--confirm` → asserts **refused** (exit 3 / `HANDOFF_CONFIRMATION_REQUIRED`).
    *This test must FAIL if export ever proceeds unconfirmed.*
  - `studio revert` after an accept → asserts head HTML **equals the pre-accept HTML** (revert restores).
  - an AUTO auto-accept → asserts it is **revertible** (revert returns prior content).
- **Fixtures:** a deterministic baseline variant with `data-od-id` on `cta.primary`/`card.root`; candidate
  files (in-scope + out-of-scope) reused from the backend e2e. **Runner:** `@playwright/test`; the studio
  preview server launched per-spec on an ephemeral port with an isolated `STUDIO_DATA` dir (per-run isolation,
  the README rule). **Validator-safety** (ux-evidence-validator): user-facing locators (role/text), no
  reliance on hidden reasoning, every assertion observable in the page or CLI JSON.
