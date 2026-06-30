---
run_id: 20260629T0700Z-inventory-js-updater
target: deterministic simple inventory updater (JavaScript)
status: pass
preset: compact
research_mode: no-research
final_verdict: build-ready non-executed plan
---

# Refine Result — deterministic inventory updater (JS)

## One-sentence synthesis
A ~150-line dependency-free Node.js tool, `inventory-update.js`, that **deterministically** appends one
inventory record to `index.json` (updating every index map by one normalized convention) and syncs the
matching `index.md` row — so the LLM never hand-edits the machine index again.

## What it is (Define)
- A module + thin CLI: `node inventory-update.js add <record.json> --timestamp <iso8601> [--index <dir>]`,
  and an exported `addRecord(indexObj, record, timestamp) -> newIndexObj`.
- Owns the **mechanical** surface: `index.json` (core) + the `index.md` table row. **Does NOT** write
  `log.md` (human judgment prose) — scope decision **(b)**, the smallest viable mechanical owner.

## Input record contract
One object matching the schema entry shape:
`{ id, path, kind, type, title, summary, tags[], sources[], updated, status, confidence, selectors[],
evidence_card_ids[], evidence_set_ids[], residue[] }`. The tool fills nothing it isn't given (no inference).

## The determinism contract (the load-bearing design)
1. **Timestamp is an INPUT, never wall-clock.** `Date.now()`/`new Date()` would make output non-reproducible
   → `generated_at` is set from the `--timestamp` arg. Same (index + record + timestamp) → byte-identical output.
2. **Append-only map updates — no key reordering.** Existing keys/arrays are never reordered; the record's id
   is appended to `by_type[type]`, `by_status[status]`, each `by_tag[t]`, each `by_source[s]`,
   `by_evidence_card[c]`, `by_evidence_set[setId]` (keys created if absent); `by_id[id] = path` (string).
   Within a key array, **dedup** (no double-append).
3. **Idempotent on existing id.** If `record.id` already in `by_id`: default = **no-op** (exit 0, "already present");
   `--replace` = in-place update (same array positions). Never a duplicate `entries[]` push.
4. **Canonical serialization.** `JSON.stringify(out, null, 2) + "\n"`. (One-time residue — see below.)

## Index-map update rules + the `by_evidence_set` normalization
- Normalize **`by_evidence_set` to key by SET-id** (schema-correct: set-id → [bundle entry-ids], mirroring
  `by_evidence_card`). The existing 13 entries key by *bundle-entry-id* — a **one-shot migration** (SWU-3)
  rewrites them; the updater then only ever writes the normalized form. (Surfaced, not silently mixed.)
- `index.md` row: ~~pick the table by `kind`~~ **CORRECTED at build (SWU-2):** route by **path prefix**, not
  `kind`. The data falsified the kind-router — `kind: page` spans `wiki/`, `entries/` (12 synthesis pages),
  and `../`; there are no `Entries[evidence-card]`/`Entries[evidence-set]` subtables. Real map:
  `entries/`→`## Entries`, `wiki/`→`## Wiki Pages`, `queries/`→`## Query Files`, `lint/`→`## Lint Files`;
  any other prefix → warn + skip (human-placed). Append `| [path](path) | type | \`tags\` | summary |` at the
  table's end (before the next `## ` header); escape `|`/newlines in cells.

## Validation (run after each update — the tool self-checks)
- `JSON.parse` round-trips (the jq-parse guarantee); `entries[]` has no duplicate `id`; every `tag` ∈ the
  controlled set parsed from `tags.md` (else warn — surfaced, not blocked); `generated_at` updated;
  `entries.length` increased by exactly 1 (or 0 on idempotent no-op).

## Build plan (3 SWUs; SWU-1 + SWU-2 BUILT via task-session)
- **SWU-1 (core, MVP) — DONE:** `addRecord(indexObj, record, ts)` + the 7-map update + the determinism
  contract + the CLI `add`. Built as `tools/inventory-update.cjs`; toy_game suite (6 groups) passes.
- **SWU-2 — DONE:** the `index.md` row sync (**path-prefix** router + row append). Same file; suite
  `tools/test/test-index-md.cjs` (7 groups) passes; coupled CLI write verified end-to-end.
- **SWU-3 (one-shot) — DEFERRED:** the `by_evidence_set` migration (rewrite the 13 existing string-form
  keys to the normalized array form) + re-validate. Write scope: `index.json` (data migration), run once.

## Validation strategy / toy_game (the determinism falsification)
A fixture test (`development/<run>/stages/` or a `test/` dir): take a frozen `index.fixture.json` + a known
record + a fixed timestamp → assert the output **equals** a checked-in `index.expected.json` (byte-identical);
apply the **same** record twice → assert the second is a **no-op** (entries length unchanged, maps unchanged).
A FAILING determinism test = the tool isn't deterministic; that is the load-bearing acceptance gate.

## Residue / risks (named)
- **Python→JS formatting delta.** ~~The first run may reformat the whole file once.~~ **MEASURED at build
  (SWU-1, 2026-06-29):** reserializing the current real `index.json` through the tool with no record change
  differs by exactly **one byte** — the real file has no trailing newline, the tool adds one. Key order,
  separators, and unicode all match Python's `json.dump(indent=2)`. The "reformat the whole file" worry was
  overstated; the one-time delta is a single `\n`, byte-stable thereafter. Decision: accept it (documented in
  `tools/README.md`).
- `by_evidence_set` migration touches existing data — run SWU-3 once, re-validate.
- Tag-validation against `tags.md` is a **warn**, not a block (new tags are sometimes legitimately added).

## Recommended next routes (NOT part of refine)
- **`task-session`** → build SWU-1 (the MVP core + toy_game test), then SWU-2/SWU-3.
- Optional later: an `inventory sync`/`lint` mode that calls this updater's validation on the whole index.
