# Stage 09 — Invoke Plan (non-executed)

- Capability: `invoke` · Mode: `plan`
- Status: **pass** · This is a plan, not an execution.

## MVP slices (ordered by value ÷ safety; each independently shippable & demoable)

### S1 — Per-element capture with disclosure  *(foundation; ~free, invariant-safe)*
- Extend `annotateClickScript` in `studio.ts`: on click, tagged → existing od-id path; untagged → mint `{selector(nth-child path), label(text), odId:null}` **for capture only**.
- Reuse `POST /comment` (already accepts `odId:null`) + `listPendingComments` drain (RP-3, DD-F3).
- UI disclosure: untagged capture shows "captured — won't auto-apply (no stable id)."
- **Cost:** ~25–40 LOC, one file, no deps. **Touches no invariant.**
- **Done:** click any element → comment persists → appears in `listPendingComments`; untagged ones flagged.

### S2 — Hover-prefill of Observed properties  *(the "Figma feel"; the headline ask)*
- `mouseover` + rAF/debounce, **separate** listener in the allow-scripts wrapper; read ~6 `getComputedStyle` props; `postMessage` out; render a **read-only "Observed properties"** panel (RP-4, RP-7).
- Props labelled *observed / non-canonical*; "unavailable" gated per self-contained variant.
- Form prefill = **placeholders only**; `intent`/`note` stay human-entered (RP-5).
- **Cost:** ~30–50 LOC, one file, no deps. **Risk:** event-flood — mitigated by mouseover+rAF.
- **Done:** hovering an element shows its real font/color/spacing; clicking still captures.

### S3 — Expand / collapse candidate ↔ grid  *(readability; the "expand the page and go back")*
- In-page CSS view-state; one enlarged iframe, grid hidden; state in URL `?view=full&label=B`; **restore-on-load** reader so the 1.5s poll-reload doesn't snap back (RP-6, DD-F4).
- **Cost:** ~15–25 LOC + CSS, one file, no deps, no new route.
- **Done:** expand B to full page, trigger a state change (poll reloads), still full-page; collapse returns to grid.

### S4 — Honest-diff truth for unattributed & theme edits  *(the real D2 engineering; biggest)*
- **S4a:** enrich `OdDiffFragment` with `selector`/`elementLabel`/first-differing-field; render the structural `null` bucket as a named "⚠ unattributed change" row (RP-2).
- **S4b:** add a **CSS-diff lane** comparing authored `<style>` rules (reuse admission's rule parser); render theme/token changes as attributable rows (RP-1).
- Until S4b lands, the surface states "theme/global edit — not yet an attributable change; the apply fence will reject it" (no false "0 changes").
- **Cost:** medium — touches `domain/canonicalize.ts` diff types + tests + `studio.ts` render. **Not one-file.**
- **Gate:** the **toy-game** (recolor `--green` → visible CSS-lane row) must pass (s08).
- **Done:** the exact `--green` case from this session shows an attributable diff row.

## Sequencing & dependencies

- S1 → S2 → S3 are independent, single-file, dep-free, invariant-safe; ship in that order for fastest demo of the operator's loop.
- S4 is the gating quality work for D2; it is **separable** and can follow once S1–S3 prove the UX. The honest-diff claim is only *true* after S4b.

## Validation surface (must stay green)

- `pnpm test` (node:test unit/slice) and `pnpm test:e2e` (Playwright). **Click stays the capture trigger** so existing e2e specs keep passing (hover is additive, read-only).
- New tests: S1 untagged-capture persists with `odId:null`; S4 toy-game (recolor → CSS-lane row); S2 prefill-does-not-satisfy-`COMMENT_SCHEMA_INVALID`.

## Explicitly deferred (named, not silent)

Untagged-element **apply** (stable-identity / fence work — GAP-V3-NODE-IDENTITY-008); descriptor/DNA extraction (F2a); routed `/full/<label>` (F4b); optimistic-local sync (F3c).

## Non-executed

No studio code is modified by this refine run. These slices are a recommended build order for a future `task-session`.
