# Stage 06 — Invoke Redefine / Design

- Capability: `invoke` · Mode: `design`
- Status: **pass** (forks resolved; gated for operator confirm at g05)

## Design decisions (the five forks)

- **DD-F1 — Element addressing: hybrid, MVP-scoped.**
  Capture a comment on **any** element. For a `data-od-id` element, target = that od-id (unchanged). For an **untagged** element, mint a **structural handle** (`odId:null`, `selector` = stable nth-child/path, `elementLabel` = trimmed text) — the data model already allows this. **Apply path stays governed:** an untagged comment is *capturable and previewable* in the MVP, but a candidate can only **apply** when its change lands on an in-scope `data-od-id` (the synthesizer rewrites the intent onto the nearest in-scope od-id ancestor, surfaced to the user). **Full untagged-apply (minted handle survives the M1 fence) is deferred.**

- **DD-F2 — Property extraction: `getComputedStyle`, labelled *observed*.**
  Extend the existing injected handler in `/annotate/variant/<L>` (already `allow-scripts`, same-origin, self-contained) to read ~6 props (font, font-size/weight, color, background, padding, border) via `getComputedStyle` and `postMessage` them with the existing `{odId, selector, label}`. The form shows them as **Observed properties** (read-only context), never as canonical/manifest truth. **Guard:** if the variant references external CSS/fonts (not self-contained), mark props "unavailable (external resources)" rather than show wrong values.

- **DD-F3 — Persistence: reuse immediate `/comment` + `listPendingComments`.**
  No new persistence layer. The existing `POST /comment` persists on head; `listPendingComments` is the drain. "Batch many then run the cycle" is *already* the model (pending = on-head-not-yet-batched). MVP adds only client UX for accumulating multiple comments before the user triggers the cycle.

- **DD-F4 — View-state: in-page CSS expand/collapse, URL-encoded.**
  A candidate/variant card can **expand** to full-page (single enlarged iframe, grid hidden) and **collapse** back. View-state lives in the URL query (`?view=full&label=B`) so the 1.5s `/state` poll-reload **does not snap back**. No new route.

- **DD-F5 — Honest-diff reconciliation: surface the existing `null` bucket.**
  `diffByOdId` already buckets unattributable changes under `null`. Render that bucket in the pending-diff as an explicit **"⚠ visual-only / unattributed change"** row with a count. This keeps D2 honest (the diff never reports "0 changes" when pixels moved) **without** a new change-class and **without** suppressing the change. Theme-token edits (the `--green` case) now show up here.

## Trigger & schema (from s03 convergence)

- **Click stays the capture trigger** (protects the Playwright e2e). **Hover only pre-fills** the form's Observed-properties preview.
- **Required `intent`/`note`:** the inline form pre-fills `intent` from the picked property when obvious (e.g. recolor/resize/reword) and seeds `note` with the observed value, so a "one-save" flow never 400s on `COMMENT_SCHEMA_INVALID`.

## Surface shape (x-ray)

```
preview page
├─ grid (variants/candidate)            ← expand/collapse (DD-F4)
│   └─ each card → sandboxed iframe
├─ /annotate/variant/<L>  (allow-scripts wrapper)
│   ├─ hover  → getComputedStyle → postMessage(observed props)   (DD-F2)
│   └─ click  → postMessage({odId|null, selector, label})        (DD-F1 capture)
├─ inline form  → POST /comment  (prefilled, observed shown)     (DD-F3)
├─ CLI: studio watch / run-cycle → listPendingComments → synthesize → stage
└─ pending diff  → per-od-id rows + "⚠ visual-only" null-bucket row (DD-F5)
```

## Preserved invariants

D1 two-gate apply — unchanged (apply still stages; human accepts). D2 honest diff — *strengthened* (null bucket surfaced). D3 append-only — unchanged. D4 sandbox — unchanged (props read in the existing allow-scripts wrapper only). D5 ergonomics — hover-prefill + expand + one-save.

## Open for s07 attack

1. Does "untagged capturable but not appliable" confuse users (a comment that can never become a change)?
2. Is the `null`-bucket row enough, or does it hide *which* element changed?
3. Does URL view-state interact badly with the poll-reload or the postMessage origin checks?
4. Does prefilling `intent`/`note` mask the COMMENT_SCHEMA_INVALID contract in a way that hurts later?
