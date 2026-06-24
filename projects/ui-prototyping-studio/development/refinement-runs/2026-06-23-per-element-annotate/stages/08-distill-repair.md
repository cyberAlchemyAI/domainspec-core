# Stage 08 — Distill Repair

- Capability: `distill` · Mode: `validate` (repair) · Technique: `toy_game`
- Status: **pass** (design repaired; blockers closed or explicitly deferred with disclosure)

## Repairs applied to the design

- **RP-1 (closes C1) — split the honest-diff fix.** DD-F5 is replaced by two distinct mechanisms:
  - **(5a) structural-unattributed row** — surface the existing `null` od-id bucket (structural elements with no od-id ancestor), **enriched** per RP-2.
  - **(5b) CSS-diff lane** — a *new* diff lane that compares authored `<style>` rules (reuse admission's rule parser) so **theme/token edits are visible**. This is the real D2 fix and is **bigger than the MVP** → see plan slice S4. **Until S4 ships, theme/global edits are NOT a supported per-component mutation** and the surface must say so ("theme/global edit — not yet an attributable change; the apply fence will reject it") rather than show a false "0 changes."
- **RP-2 (closes C2) — enrich `OdDiffFragment`.** Carry `selector` + `elementLabel` + first-differing field into unattributed/CSS fragments so a row reads "padding/color changed on `.hero h1`," not "3 changes." Touches `domain/canonicalize.ts` diff types + tests.
- **RP-3 (closes C3+C4) — DD-F1 becomes capture-only with full disclosure.** Untagged element → mint a `{selector, label, odId:null}` handle **for capture/preview only** (never an apply target, per GAP-V3-NODE-IDENTITY-008). The `CommentEvent` persists **both** the pointed-at handle **and**, if the agent rewrites onto an ancestor, the rewrite-target od-id. UI discloses at capture ("captured — won't auto-apply: no stable id") and before folding ("will apply to parent `<section>` instead — ok?"). **Never silently retarget or drop.**
- **RP-4 (closes C5) — observed props non-transferable.** `getComputedStyle` props are display-only context, explicitly flagged non-canonical; the synthesizer reads **authored** CSS, and any candidate prop sourced from computed style is rejected/flagged.
- **RP-5 (closes C6) — don't auto-fill governance fields.** Prefill only placeholders/affordances; `intent`/`note` stay human-entered. Keep an empty-payload `COMMENT_SCHEMA_INVALID` test the UI cannot satisfy automatically.
- **RP-6 (closes C7) — restore-on-load.** Add the 3-line reader that applies `?view=full&label=B` to the DOM state after the poll's `location.reload()`.
- **RP-7 (closes C8) — hover hygiene.** `mouseover` + rAF/debounce + a separate listener; "unavailable" gated per-variant (self-contained check), not per-property.

## Toy-game falsification gate (pre-registered)

**Game:** in a fresh session, recolor the `--green` token on baseline B (the exact case from this conversation), synthesize, stage.
**Pass criterion:** the pending diff shows a **CSS-lane row** naming the changed rule/token (e.g. "`--green` #1ed97a → #5fa882") — i.e. the change is **visible and attributable**, OR the surface explicitly states "theme/global edit — not an attributable per-component change; fence will reject."
**Fail (current code):** zero diff fragments, surface implies "no changes." **This gate must pass before the honest-diff claim (S4) is marked done.**

## Repaired scope boundary

- **In:** per-element **capture** (tagged + untagged-with-disclosure), hover-prefill of observed props, expand/collapse with restore, reuse of the existing comment/drain/cycle.
- **Deferred (named):** untagged-element **apply** (fence + stable-identity work, GAP-V3-NODE-IDENTITY-008); the **CSS-diff lane** S4 (the real theme-edit honesty fix); descriptor/DNA extraction (F2a); routed full view (F4b); optimistic sync (F3c).

## repair-frame → handed to s09 Plan
