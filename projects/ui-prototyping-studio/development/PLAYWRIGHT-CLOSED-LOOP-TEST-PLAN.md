---
id: playwright-closed-loop-test-plan
project: ui-prototyping-studio
title: "Playwright e2e test plan — the closed loop (HUMAN + AUTO), with governance falsification"
status: proposal
node_type: test-plan
source: refinement-runs/20260618-skill-rewrite-playwright-plan
updatedAt: 2026-06-18
---

# Playwright e2e test plan — closed loop (HUMAN + AUTO)

Non-executed plan. Tests the **built** surface: the `studio preview` loopback HTTP server (annotate, `/comment`,
`/state`, before/after diff) + the CLI verbs. Validator-safe per the `ux-evidence-validator` discipline:
user-facing locators, every assertion observable in the page or CLI JSON, no reliance on hidden reasoning.

## 0. Wiring (not yet present — no `e2e/` dir today)
- Add `@playwright/test` as a backend devDependency; `playwright.config.ts` with `testDir: "e2e"`, a single
  chromium project, `webServer` NOT used (we launch the studio per-spec).
- Scripts: `"test:e2e": "playwright test"`.
- **Isolation (README rule):** each spec gets its own `mkdtemp` dir and sets `STUDIO_DATA=<dir>/studio.json`
  so artifacts never collide; pick an **ephemeral port** per spec (`server.listen(0)` → read the chosen port,
  or pass `--port` from a free-port helper). Tear down the preview process in `afterEach`.

## 1. Harness helpers (`e2e/helpers.ts`)
- `seedSession(dataDir)` — run the CLI (`tsx src/cli/studio.ts …` with `STUDIO_DATA`) to: `session open
  --variants 1` → `prompt submit` → `variants register --label A --file <baseline>` → `baseline select A`.
  Returns `{ sessionId }`. Baseline fixture = a div with `data-od-id="card.root"` containing
  `data-od-id="cta.primary"` ("Go").
- `startPreview(sessionId, dataDir)` — spawn `studio preview <sid> --port <free>`; wait for the printed URL;
  return `{ url, port, stop() }`.
- `cli(args, dataDir)` — run a one-shot CLI verb, return `{ stdout, json, exitCode }`.
- Fixtures (`e2e/fixtures/`): `base.html`, `continue.html` (in-scope cta change), `next.html` (in-scope),
  `badge.html` (adds a new od-id — out of exploit scope), reused from the backend e2e set.

## 2. L0 — smoke
- `smoke.spec.ts`: open the preview URL → the page has the header with the session id; each variant `<iframe>`
  resolves (`/raw/variant/A` 200, non-empty); `GET /state` returns JSON `{state, head, stagedHash}`.

## 3. Closed-loop happy path — HUMAN mode (`human-loop.spec.ts`)
1. Open preview; the **Annotate** panel shows `iframe#annot` = `/annotate/variant/A`.
2. Inside the annotate frame, **click** the element with `data-od-id="cta.primary"` (frame locator by text "Go").
3. Assert the parent comment form (`#cf`) becomes visible and `#cf-od` shows `cta.primary` (the trusted
   click→`postMessage` fired).
4. Fill `intent`="reword", `note`="say Continue"; submit. Assert `#cf-msg` shows "captured ✓".
5. CLI: `studio pending <sid>` → JSON length **1** (the click reached the core — CL2).
6. CLI: `synthesize` → `batch approve` → `apply --candidate-from continue.html`.
7. Reload preview (or let the `/state` poll refresh): the **Pending change** section renders before/after
   iframes (`/raw/baseline`, `/raw/staged`) + the honest diff line (`~1 changed` on `cta.primary`).
8. CLI: `accept <sid>` → `studio state` shows `RevisionRecorded`, head advanced.

## 4. AUTO path (`auto-cycle.spec.ts`)
1. `seedSession`; open preview.
2. CLI: `studio cycle <sid> exploit --objective "make the cta clearer" --candidate continue.html:0.9
   --candidate next.html:0.4`.
3. Assert JSON: `staged=2`, `rejected=0`, `chosen.score=0.9`; head advanced.
4. The preview `/state` poll triggers a reload; assert the head now renders "Continue" (read `/raw/baseline`,
   which resolves to head).
5. Explore divergence: `studio cycle <sid> explore --objective "try a badge" --candidate badge.html:0.8` →
   admitted (`rejected=0`); the same candidate under `exploit` asserts `rejected=1, chosen=null` (fence).

## 5. GOVERNANCE falsification (the load-bearing specs — `governance.spec.ts`)
These must FAIL if the corresponding guarantee breaks (see the run's stages/08-toygame.md).
- **export needs confirm:** `studio handoff export <sid>` (no `--confirm`) → assert `exitCode === 3` AND
  stdout JSON `.refused === "HANDOFF_CONFIRMATION_REQUIRED"`. Then `… --confirm` → assert a bundle returns.
  *(Asserted on the CLI seam — the confirm gate lives there, not in the page.)*
- **revert restores:** after §3/§4 accept, read head HTML (via `/raw/baseline`), `studio revert <sid>`, read
  head HTML again → assert it **equals the pre-accept baseline** ("Go", not "Continue").
- **auto-accept is revertible:** after §4's auto-accept, `studio revert` → assert the prior content returns and
  `studio revisions` shows **both** events (append-only, count grew — never rewound).

## 6. Sandbox boundary check (`sandbox.spec.ts`)
- Assert `/raw/variant/A` is served into a `sandbox` (no-scripts) iframe and a `<script>` inside a variant does
  NOT execute (no console errors from it / no global set), while `/annotate/variant/A` (the trusted wrapper,
  `sandbox="allow-scripts"`) DOES post a message on click. Confirms CL1's trusted-wrapper boundary.

## 7. What this plan does NOT cover (honest scope)
- The UX-constraint fitness (axe/layout scoring) — DEFERRED (SPEC L5+, OQ-5); no constraint-runner test here.
- AUTO stop-dial *enforcement* (loop_cap/plateau) — lives in the agent `/loop`, not the core; out of e2e scope.
- A11y/layout (SPEC L1/L2) acceptance — covered by the separate UX-EVIDENCE-REPORT plan, not this loop plan.

## 8. Next route
`task-session` to wire §0 + implement the specs in order: L0 smoke → governance (the falsifiers first) →
HUMAN happy path → AUTO → sandbox. Run against the real build; the governance specs are the gate.
