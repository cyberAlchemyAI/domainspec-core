---
id: plan-studio-preview
project: ui-prototyping-studio
title: "Build Plan — fill the gaps + run the studio as live HTML in VSCode (see the product)"
status: proposal
node_type: implementation-plan
invoke_mode: plan
complexity: medium
source: development/cycle-close-research/findings.md (D2 / Surface C) + the live-run gaps (GAP-015, GAP-009)
updatedAt: 2026-06-17
---

# Build Plan — studio preview in VSCode

**Goal:** fill the gaps so the studio's mutation loop is clean **and** renders as **live HTML inside
VSCode** — `studio preview <sid>` boots an ephemeral local server; you open the printed
`http://localhost:PORT` in VSCode's built-in **Simple Browser** (or any browser) and *see* the variants
and the honest before/after diff as you design. This is the research's Deliverable 2 ("Surface C:
same-origin served page") made concrete, plus the two doc/run bugs the live run exposed.

Planning artifact — `[PROPOSAL]`, nothing executed; each SWU runs via a separate `task-session`.

## What exists vs the gap
- **Exists:** the full loop (register real HTML, two-gate apply/accept, honest od-id diff), the content
  port (`readHtml`/`pathForRef`), a fastify app (`backend/src/index.ts` + `interface/http-routes.ts`).
- **The gap:** you can only *open static `.html` files* via the printed `openPaths`; there is no served
  view, no rendered diff, and two documented steps error (`baseline commit`, `handoff export`).

## Standing design decision (recommended default)
Serve the preview through the **existing fastify app** (it already boots and has the content port), via a
new read-only render route + a static no-build page — not a second server. (Research Surface C: vanilla
HTML/JS, sandboxed iframes, no framework/build.) `studio preview <sid>` starts it ephemerally and prints
the URL. *If you'd rather keep the CLI server-free, the alternative is a tiny stdlib http server in the
CLI — flagged, not chosen.*

## Wave / layer map
```
L0  Fill the run gaps (clean loop)     : G1 baseline-commit idempotent · G2 handoff-export standalone
L1  SEE the variants in VSCode         : P1 `studio preview <sid>` — served page renders the session's variants (iframes) + plain state
L2  SEE the change (the irreducible)   : P2 rendered before/after diff at the apply gate (the "saw-the-diff" render)
L3  ACT on a component (defer)         : P3 click-to-annotate on the rendered component (preview --annotate, DC-1)
```
Promotion by evidence from the prior layer. L0+L1 = "I can run it and see the product in VSCode" (the ask).

## SWU manifest

| SWU | Title | Layer | Depends on | Write scope | Acceptance (one-line) |
|-----|-------|-------|-----------|-------------|-----------------------|
| **G1** | `baseline commit` idempotent | L0 | — | `application/select-or-commit-baseline.ts` + test | after `baseline select B`, `baseline commit` commits the selected label instead of erroring `BASELINE_SELECTION_REQUIRED` |
| **G2** | `handoff export` standalone | L0 | — | `application/export-design-handoff.ts` + test | `handoff export` succeeds against the lean doc set (feature-doc refs optional / point at SPEC), no `HANDOFF_REFERENCE_INCOMPLETE` |
| **P1** | `studio preview <sid>` served page | L1 | content port (done), fastify | `interface/preview-routes.ts` (new), `cli/studio.ts` (`preview`), a static `preview/` asset | a localhost page renders each variant's committed HTML in a sandboxed iframe + session state in plain words; opens in VSCode Simple Browser |
| **P2** | Rendered before/after diff at the gate | L2 | P1, MW1 (done) | preview page + a diff render route | when a candidate is staged, the page shows baseline vs candidate side-by-side + the honest od-id fragments highlighted |
| **P3** | Click-to-annotate (defer) | L3 | P2 | overlay asset + POST → CommentEvent | click a rendered component → comment with resolved `data-od-id` (DC-1); INV-2 gated |

## Per-SWU detail

### G1 — `baseline commit` idempotent  `[backend fix; GAP-SKILL-BASELINE-COMMIT-REDUNDANT-015]`
- **Now:** `baseline select B` satisfies the gate; a following `baseline commit` (no label) throws
  `BASELINE_SELECTION_REQUIRED`. The README/protocol document both → testers hit an error.
- **Fix:** in `selectOrCommitBaseline`, when no label is given AND a baseline is already selected, **commit
  the selected label** (mode selected→committed) instead of demanding a label. **Verify:** select→commit
  succeeds (gate `satisfied`, baseline mode `committed`); existing baseline tests stay green.

### G2 — `handoff export` standalone  `[backend fix; GAP-HANDOFF-DOC-REFS-009]`
- **Now:** `exportDesignHandoff` requires `STORIES.md`/`UI-SPEC.md`/`TEST-SPEC.md` under the docs root →
  `HANDOFF_REFERENCE_INCOMPLETE` in the lean project.
- **Fix (decide one):** (a) make those refs **optional** (export what exists; emit a `missingRefs` note), or
  (b) point the required set at the lean `SPEC.md` + aspect docs. Recommend (a). **Verify:** `handoff
  export` returns a bundle for a session with only the lean docs; the slice test (currently the accepted-red
  one) flips to green or is re-scoped.

### P1 — `studio preview <sid>`  `[server + static page; the "see it in VSCode" core]`
- **Steps:** add `interface/preview-routes.ts` — a read-only `GET /preview/:sid` returning a no-build HTML
  page, and `GET /preview/:sid/variant/:label` (and `/staged`) returning the committed/staged HTML via the
  content port (`readHtml`). The page lists the session's variants in **sandboxed iframes** (one per
  label), shows session **state in plain sentences** (what happened, what's next, why a control is
  disabled), and the durable gates as labeled (non-interactive in L1 — disposition stays in the CLI).
  CLI: `studio preview <sid> [--port N]` boots the fastify app on an ephemeral port, prints
  `http://localhost:PORT/preview/<sid>`, runs until Ctrl-C.
- **VSCode:** open the URL via Command Palette → **"Simple Browser: Show"** (built in; renders in an editor
  tab), or the Live Preview extension, or any browser. No custom extension.
- **Edge/failure:** a variant whose `htmlArtifactRef` is unresolvable (stub-generated) → iframe shows an
  honest "no rendered HTML (register real HTML)" placeholder. Bind localhost only (loopback) — never
  expose. **Verify:** `curl localhost:PORT/preview/<sid>/variant/B` returns the variant HTML; manual: the
  page renders all variants in VSCode Simple Browser.

### P2 — rendered before/after diff at the gate  `[the irreducible render]`
- **Steps:** when `getStagedCandidate(sid)` exists, the preview page shows **baseline (current head HTML)
  vs candidate** side-by-side iframes + the honest `DiffSummaryHonest` fragments (per-od-id added/changed/
  removed) listed/highlighted. This makes "saw-the-diff" real before the human accepts.
- **Verify:** stage an in-scope candidate → the page shows both renders + the changed od-id; a human can
  see exactly what changes before running `accept` in the CLI.

### P3 — click-to-annotate (deferred)
- Inject a click-to-annotate overlay; clicking a rendered component POSTs a `CommentEvent` with its
  resolved `data-od-id` (DC-1, INV-2 gated). Closes the last visual-ergonomics gap; not needed to *see* the product.

## Implementation-layering (value/cost + promotion)
- **L0 (G1/G2):** clean loop — promotion = the two fixes' tests green + the README steps no longer error.
- **L1 (P1):** **the ask** — see the variants live in VSCode. Promotion = the served page renders variants
  in Simple Browser.
- **L2 (P2):** see the change — promotion = before/after + honest diff visible at a staged gate.
- **L3 (P3):** act on a component — deferred.

## Validation strategy (per slice)
G1/G2 → unit tests (select→commit; handoff with lean docs). P1 → route test (`curl` returns variant HTML)
+ manual VSCode Simple Browser render. P2 → staged-session render shows before/after + diff. Existing
backend suite (42/42) stays green throughout (`pnpm test`).

## Use it with the open-design references (the payoff)
Once L1 lands, the design loop is: Claude Code authors variant HTML **grounded in the published
open-design refs** (e.g. a brand's tokens from `provenance/open-design-reference/voltagent-design-md/<brand>/DESIGN.md`,
or the `nexu-io/open-design` web-prototype skill) → `variants register` → **you open `studio preview` in
VSCode and see them** → comment → Claude proposes a mutation → **you see the before/after diff (P2)** →
`accept`. That is "UI designed with it," visible in your editor.

## Decisions / blockers
- **Serve via existing fastify (recommended) vs standalone CLI server** — default fastify; non-blocking.
- **G2 handoff approach (optional refs vs point-at-SPEC)** — recommend optional refs; resolve in the G2 task-session.
- No human-gate blocker; this is additive build. (Public docs that ship these commands get refreshed after L1/L2.)

## Next route
`task-session`: **G1 → G2** (clean the loop, fast) → **P1** (see variants in VSCode — the core ask) → **P2**
(see the diff). P3 deferred. After L1/L2, refresh the public README/TEST-PROTOCOL to document `studio preview`.
