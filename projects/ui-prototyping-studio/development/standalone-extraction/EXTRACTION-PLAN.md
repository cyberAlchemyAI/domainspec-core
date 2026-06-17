---
id: ui-prototyping-studio-standalone-extraction-plan
project: ui-prototyping-studio
title: "Standalone Extraction Plan — ui-prototyping-studio out of domainspec"
status: proposal
node_type: plan
updatedAt: 2026-06-16
---

# Standalone Extraction Plan

**Goal:** turn `projects/ui-prototyping-studio/` into a **self-contained, runnable project** (backend + web + e2e + docs), independent of `implementation/domainspec`, because **domainspec is being deprecated**.

**Status:** PLAN ONLY — no code has moved. Approve, then execute phase by phase. Nothing is committed.

> Scope note: the **spec docs + `.craft/` + `development/`** already live here (moved in the prior step). This plan covers extracting the **code** (backend module, frontend, e2e) and standing up an independent build/runtime.

---

## 1. Coupling assessment (verified, not assumed)

| Surface | Coupling to domainspec | Verdict |
|---|---|---|
| **Backend module** `backend/src/modules/ui-prototyping-studio/` (39→ ~30 code files) | Imports **only** `node:*` builtins + `fastify`. No framework imports, no `../../` reaching outside the module. Wired in **only** via `backend/src/server.ts` (`registerUiPrototypingStudioRoutes`). | **Clean lift.** Needs its own fastify bootstrap + package. |
| **Frontend components** `apps/web/src/components/ui-prototyping-studio/*.tsx` (7) | Presentational, **prop-driven**. Plain HTML + CSS classes (`panel`, `ups-panel`) — **no shadcn/Radix/Tailwind** (despite D-001; the real app never adopted them). | **Clean lift.** |
| **Page** `apps/web/src/layouts/StudioWorkbenchLayout.tsx` | Wires components via the hook + api client. | Move. |
| **Hook** `apps/web/src/hooks/useUiPrototypingStudio.ts` (~15KB) | Studio state/controller. | Move (studio-specific). |
| **API client** `apps/web/src/lib/api.ts` (~25KB, shared) | ~138 studio-related lines mixed with knowledge-graph funcs. | **Carve** studio funcs into the new project's api module. |
| **Styles** `apps/web/src/styles.css` (shared) | Holds `.panel` / `.ups-panel` etc. | **Carve** studio rules (or copy whole, then trim). |
| **App shell** `App.tsx`, `AppSidebar.tsx`, `lib/api.ts` | Shared, host other features — **cannot move**. | **Recreate** a minimal shell. |
| **E2E** `apps/web/e2e/ui-prototyping-studio/` (mock-api.ts + 2 specs) + `playwright.config.ts` | Uses the web app's Playwright config. | Move + adapt config. |

**Tooling baseline to mirror:** backend = ESM, `fastify@^5`, `@fastify/cors@^10`, `tsx@^4` (dev + `tsx --test` for `node:test`), `typescript@^5.6`, `tsc` build. web = `react@^18.3`, `vite@^5.4`, `@vitejs/plugin-react@^4`, `@playwright/test@^1.59`. Source repo is a **pnpm workspace**.

---

## 2. Target structure

```
projects/ui-prototyping-studio/
  README.md                         # NEW — project entry + run instructions
  package.json                      # NEW — pnpm workspace root (backend + web)
  pnpm-workspace.yaml               # NEW
  CRAFT.md  .craft/                 # exists
  docs/                             # OPTIONAL reorg — see Decision D-EXT-1 (default: leave specs at root)
  development/                      # exists (deep-spec-dispatch + this plan)
  backend/
    package.json  tsconfig.json     # NEW
    .data/                          # session store (gitignored)
    src/
      index.ts                      # NEW — fastify bootstrap (cors + registerUiPrototypingStudioRoutes + listen)
      modules/ui-prototyping-studio/**   # MOVED (unchanged internals)
  web/
    package.json  tsconfig.json  vite.config.ts  index.html   # NEW
    playwright.config.ts            # MOVED + adapted (baseURL/webServer → this web app)
    src/
      main.tsx  App.tsx             # NEW — minimal shell mounting StudioWorkbenchLayout at /ui-prototyping-studio
      styles.css                    # carved studio styles
      lib/api.ts                    # carved studio API client
      hooks/useUiPrototypingStudio.ts    # MOVED
      layouts/StudioWorkbenchLayout.tsx  # MOVED
      components/ui-prototyping-studio/** # MOVED
    e2e/ui-prototyping-studio/**    # MOVED
```

---

## 3. Phased execution

Each phase ends with a **verification gate**; do not proceed on red.

### P1 — Backend standalone (clean lift)
1. `mkdir backend`; move `implementation/domainspec/backend/src/modules/ui-prototyping-studio/` → `backend/src/modules/ui-prototyping-studio/`.
2. Write `backend/src/index.ts`: create fastify app, register `@fastify/cors`, call `registerUiPrototypingStudioRoutes(app, { uiPrototypingStudio: {...} })`, `listen` on a configurable port; ensure `.data/` session-store dir.
3. Write `backend/package.json` (`@ui-prototyping-studio/backend`, type module, deps `fastify@^5` + `@fastify/cors@^10`, dev `tsx`/`typescript`/`@types/node`; scripts build/dev/start/test mirroring source) and `tsconfig.json`.
4. Add `.gitignore` (`dist/`, `.data/`, `node_modules/`).
- **Verify:** `pnpm --filter backend build` (tsc clean) · `pnpm --filter backend test` (the existing `ui-prototyping-studio.slice.test.ts` passes) · `pnpm --filter backend dev` then `curl` the studio routes.

### P1.5 — `studio` CLI + operating skill (Claude Code seam) — NEW
Decided: `DEC-INTERFACE-MODEL-009` (human workbench + embedded assistant), `DEC-GENERATOR-PORT-010` (add the seam now), `DEC-RUNTIME-CLAUDE-CODE-011` (**Claude Code-native runtime**), `DEC-CLI-NOT-MCP-012` (**CLI, not MCP server**). The embedded assistant *is* Claude Code; no MCP server, no `@anthropic-ai/sdk`, no API key, no agent loop.
1. Build a `studio` CLI (node/tsx in the backend package) wrapping the orchestration module. Commands: `session open`, `prompt submit`, `variants register --from <dir>` (and `--fake`), `state`, `baseline select|commit`, `comment add`, `synthesize`, `batch approve`, `batch apply`, `revisions`, `handoff export`, `preview` (opens HTML in a browser).
2. Generation seam: Claude Code generates HTML and calls `studio variants register`; a deterministic `--fake`/fixture drives e2e. Synthesis stays deterministic; generation/mutation are the only agentic actions. **The operating skill requires the generator to stamp annotatable elements with a stable `data-od-id`** (minimal component-role convention) so annotation targets survive regeneration (`DEC-ATOMIC-IDS-014`); full atomic-design taxonomy is L4.
3. Gate enforcement lives in the orchestration module **behind** the CLI: `batch apply` refuses non-approved / `system:auto` / stale applies (INV-3/4/5/8) regardless of CLI flags.
4. **Operating skill** (`SKILL.md`) — discipline for Claude Code: generate on request, `variants register`, never self-approve/apply, hand the gates to the human via the CLI.

> **Status update (2026-06-16):** decision-gate PASS — scope confirmed **L0→L2** (`DEC-ONE-SHOT-SCOPE-002`); no open/blocking decisions. The **C-1 spike SURVIVED** (`DEC-C1-SPIKE-SURVIVED-016`, parent-verified): the whole-tree od-id V3 fence is **buildable** on the closed set. Two items moved to **separated research tracks** (off the L0→L2 critical path): (1) UX/ergonomics (OQ-1 trust meter + `GAP-ERGONOMICS-UNPROVEN-001`); (2) CSS-attribution/node-identity spike (`DEC-R2-CSS-ATTRIBUTION-017` + `GAP-V3-NODE-IDENTITY-008`).

**Apply is the produce→validate→stage→accept→record machine** (not a one-shot "apply"). Generation is non-deterministic behind the CLI seam (Claude Code proposer); determinism is recovered at the *admission* boundary in the pure core: `propose` → `validate` (pure clock-free verdict) → stage candidate at a temp ref (`RevisionApplied`, NOT head) → human **accept-diff** the exact staged hash → atomic **record** (seen == recorded). The full build is the refine's 7-layer sub-plan `[PROPOSAL]` (`development/refinement-runs/20260615-mutation-execution-mechanics/`, RESULT §8):
- **L0 substrate** — schema migrations (`odId` + `MutationChangeType` union, `DiffSummaryHonest`/`OdDiffFragment`, `ExecutionProvenance`) + the artifact content port (`readHtml`/`stageHtml`/`commitHtml`/`discardStagedHtml`) + the shared canonicalizer. **Unblocks everything.**
- **L1 (MWU)** — pure validator suite V1–V9b + composite fail-closed verdict + whole-tree V3 fence; toy-game falsifiers land as regression fixtures. **C-1 spike SURVIVED** — the fence is buildable (port `run_spike.py` logic); carry `GAP-V3-NODE-IDENTITY-008` (reordering-robust node identity + real CSS cascade/specificity for production, beyond the spike's conservative version).
- **L2** — two-gate state machine + `RevisionApplied` staged-preview lifecycle + accept-time staleness re-check.
- **L3** — recorder atomicity: all-or-nothing commit + compensating rollback + `removeRevision`.
- **L4 (RESEARCH-TRACK-GATED)** — *C-1 V3-fence dimension already SURVIVED.* Remaining: the **CSS-attribution/node-identity spike** (research track 2) calibrates `S`/`B`/`k`/`c` and decides V2-vs-CSS (R2-a/R2-b, `DEC-R2-CSS-ATTRIBUTION-017`); wire C→A / C→B config levers. Runs off the critical path; gates L4+, not L0–L3.
- **L5** — `studio apply`/accept CLI + Claude Code proposer adapter; toy-game-style e2e with a **scripted** proposer (no live LLM in CI).
- **L6** — governance closeout + D4 checksum migration.

**THREE BLOCK-LOCAL fixes must land early** (each blocks the lane it sits in): **A1** — the artifact content port (substrate; today HTML is read/written through a port that does not exist, so lanes 3/4 have no input); **B1** — the whole-tree V3 fence (od-id-blind detection admits/hides adversarial un-anchored markup); **C1** — the `RevisionApplied` staged-preview lifecycle (the real saw-the-diff gate).

**RESIDUE-B — partially cleared.** The V3-fence dimension **SURVIVED** the C-1 spike (the fence is buildable). Remaining in RESIDUE-B: decide R2-a vs R2-b and commit+report `S`/`B`/`k`/`c` on real comment workloads — now **research track 2**, gating L4+ only. **L0–L3 build now** without it.
- **Verify:** existing slice/e2e pass against the fake (contract unchanged) · a Claude Code session drives generate→`variants register`→propose→validate→stage→(human accept-diff gate)→record over a smoke prompt · `batch apply` rejects non-approved/auto/stale.

### P2 — `studio preview` + in-prototype annotation overlay — MVP (no React SPA)
Reframed by `DEC-CLI-NOT-MCP-012` (no SPA) and `DEC-INPROTO-ANNOTATION-013` (annotate on the components):
1. `studio preview [--annotate]` serves the variant/revision HTML from an **ephemeral local server** and opens it in the browser.
2. With `--annotate` (default once a baseline exists), inject a small **click-to-annotate overlay**: click a rendered element → capture its `data-od-id` (stable component id; selector as fallback) + label → `{severity,intent,note}` → POST back → `CaptureCommentEvent` (gated by INV-2). No hand-typed selectors; no React SPA. `studio comment add` stays the headless path — identical `CommentEvent` contract.
3. The existing selector-typing `AnnotationPanel`/React components are **superseded** (kept in old code only as reference).
- **Verify:** open `preview --annotate`, click an element, confirm a `CommentEvent` with the captured selector lands and is identical in shape to a `comment add` event; annotation is rejected before a baseline exists.

### P2b — (only if/when the annotation UI is built) Frontend move mechanics
1. `mkdir -p web/src`; move components, `layouts/StudioWorkbenchLayout.tsx`, `hooks/useUiPrototypingStudio.ts`.
2. **Carve** `lib/api.ts`: copy only the studio API functions (init/submit/generate/select/confirm/comment/synthesize/approve/apply/list/handoff) into `web/src/lib/api.ts`; point base URL at the P1 backend.
3. **Carve** `styles.css`: copy `.panel`, `.ups-panel`, and studio-scoped rules into `web/src/styles.css` (start by copying whole, then trim non-studio).
4. Write `web/src/main.tsx`, `App.tsx` (minimal: render `StudioWorkbenchLayout` at `/ui-prototyping-studio`; no AppSidebar/knowledge-graph), `index.html`, `vite.config.ts`, `web/package.json`, `tsconfig.json`.
- **Verify:** `pnpm --filter web build` (vite build clean) · `pnpm --filter web dev` renders the studio against the running backend; smoke the full loop (prompt → variants → baseline → comment → approve → apply → handoff).

### P3 — E2E
1. Move `e2e/ui-prototyping-studio/` (mock-api.ts + wp01 + wp02wp03 specs) → `web/e2e/ui-prototyping-studio/`.
2. Move + adapt `playwright.config.ts`: `webServer` launches the new `web` dev server; `baseURL` → its port.
- **Verify:** `pnpm --filter web exec playwright test` (the wp01 / wp02wp03 specs pass against the mock + the new shell).

### P4 — De-register from domainspec (gated; domainspec is deprecating)
- `backend/src/server.ts`: remove the import + `registerUiPrototypingStudioRoutes` call (lines ~9–29).
- `backend/src/server.test.ts`: drop the studio handoff assertions.
- `apps/web/src/App.tsx`: remove the studio route + `StudioWorkbenchLayout` import.
- `apps/web/src/components/layout/AppSidebar.tsx`: remove the `/ui-prototyping-studio` nav entry.
- `apps/web/src/lib/api.ts`: remove now-dead studio functions (optional).
- Delete the moved component/hook files from `apps/web` (optional).
- **Decision D-EXT-2:** do we keep domainspec building green, or accept breakage since it's being deprecated? (Default: do the minimal de-registration so domainspec still builds, skip cosmetic cleanup.) This **supersedes `GAP-DOCS-CODE-SPLIT-005`** — the dangling doc-path refs (`export-design-handoff.ts`, `mock-api.ts`, tests, `PRODUCT-COMPONENTS-IDEA.md`, tag reports) move into the new project with the code, so they resolve naturally.

### P5 — Project meta + ledger recompose
1. Root `package.json` + `pnpm-workspace.yaml` (`backend`, `web`); root scripts (`dev`, `build`, `test`, `test:e2e`).
2. `README.md`: what the project is, how to run (backend + web + e2e), link to `CRAFT.md` and the deep-spec.
3. Update `.craft/ledger.yml`: close `CTX-UPS-EXTRACTION`, recompose into `CTX-UPS-ROOT`, mark `GAP-DOCS-CODE-SPLIT-005` resolved.
- **Verify:** fresh clone-style `pnpm install && pnpm build && pnpm test && pnpm test:e2e` all green from `projects/ui-prototyping-studio/`.

---

## 4. Open decisions to resolve at execution

- **D-EXT-1 — docs layout:** leave the 249 spec docs at the project root (current), or reorganize under `docs/`? Reorg re-breaks the `.craft` path refs (fixable) and the deep-spec internal links. *Default: leave at root.*
- **D-EXT-2 — domainspec build:** minimal de-registration to keep it green, vs. accept breakage (deprecating). *Default: minimal de-registration.*
- **D-EXT-3 — package layout:** pnpm workspace (backend + web) vs. two independent packages with no root. *Default: pnpm workspace.*
- **D-EXT-4 — git history:** plain move (history stays in domainspec git; new files in parent) vs. `git filter-repo` to carry history across the submodule boundary. *Default: plain move; note history lives in domainspec.*
- **D-EXT-5 — node version / package manager:** confirm pnpm + Node version to pin in `engines`.

## 5. Risks

- Carving `lib/api.ts` / `styles.css` by hand can miss a studio dependency → caught by P2 verify (build + smoke).
- The backend `.data` file store path is relative; the new bootstrap must set it explicitly.
- Removing the module from domainspec breaks its `server.ts`/`App.tsx` build until P4 de-registration lands — sequence P4 right after P1/P2 if anyone still builds domainspec.
- Submodule discipline: P1–P3 deletions happen **inside** the domainspec submodule; committing is submodule-first (commit+push domainspec, then add the parent `projects/` files and bump the gitlink).

## 6. Effort estimate

P1 small · P2 medium (carve + shell) · P3 small · P4 small · P5 small. Roughly one focused session to a green `pnpm build && pnpm test && pnpm test:e2e`.
