# Stage 01 — Context Builder evidence baseline

- Capability: `context-builder` · Mode: `standard` · Owner receipt: parent coordinator
- Status: **pass**

## Evidence frame (what exists today)

**Annotate surface (already built).** `backend/src/cli/studio.ts` runs a no-build loopback preview server that:
- renders each variant in a sandboxed `<iframe src="/raw/variant/<L>">`;
- injects a **click → `postMessage`** handler into `/annotate/variant/<L>` (the only iframe with `sandbox="allow-scripts"`), walking up from the click target to the nearest `data-od-id` element and posting `{odId, selector, label}` to the parent;
- shows a comment form (`severity`, `intent`, `note`) that `POST`s to `/comment`;
- polls `/state` every 1.5s and reloads on `state|head|stagedHash` change;
- drives `/accept`, `/discard`, `/revert` from in-page buttons (export stays terminal-only).

**Comment model.** `captureCommentEvent` stores `target = { selector, elementLabel, odId? }` — **`odId` is already nullable**. Gate: `selectionGate === "satisfied"` (baseline committed) and the comment binds to the current `revisionHeadId`.

**Drain / cycle.** `listPendingComments` = comments on current head **not yet** folded into a batch (`generatedFromCommentIds`). Idempotent by comment id. This is the existing "retrieve comments via CLI and run the cycle" path (`studio watch` / `run-cycle`).

**Honest diff.** `domain/canonicalize.ts` (`domainspec-html-canon v1.4.0`) parses HTML to a canonical tree, **preserves `od-id`**, normalizes attrs/whitespace/void elements, and keeps `<style>`/`<script>` as raw text. Attribution is **per-`od-id` fragment** → subtrees with no `od-id` (and `<style>` theme tokens) are **not attributed to any component**.

## Observed live constraints (this session — the load-bearing evidence)

1. **Untagged elements are un-annotatable per-element.** The saturated tagline `Corra. Conecte. Conquiste.` (`.line`) has no `data-od-id`; the click handler walks up to the nearest tagged ancestor, so the comment lands on a parent, not the tagline.
2. **Theme/global edits are diff-silent.** Recoloring `--green` (a `<style>` token) changed the visuals but produced an honest diff of **0 changed components** — correct by the per-`od-id` rule, misleading as "no change."
3. **In-memory store staleness.** The preview server snapshots state at boot; CLI mutations require a server restart to surface (in-page POSTs mutate the live store and don't).
4. **Iframe clipping.** Fixed `height:340px` clips variants; there is no expand-to-full-page / back-to-grid view-state.

## Operator intent (parsed)

Iterate **per element**, Figma-style: hover any element → inline form pre-filled with the element's properties (extracted "by spec, or by …"), page **composed** from elements; comments **saved/sent to server**; **batch** many comments then **run the skill/cycle**; **expand** a candidate to full page and **back** to the grid.

## Frame handoff → Define

The MVP must reconcile *Figma-freeform per-element annotation* with the studio's *governed honest-diff / `data-od-id` / two-gate* identity, on the existing node+fastify no-build preview stack — without breaking `pnpm test` / `pnpm test:e2e`.
