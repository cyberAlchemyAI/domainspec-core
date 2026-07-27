# UI Prototyping Studio

Accountable UI exploration: generate 1–3 bounded variants → intentionally
select a baseline → annotate with canonical comments → synthesize a
deterministic mutation draft → explicit approval → validate and stage →
acknowledge Accept or Revert → append-only revision manifest → confirmed
handoff. Governance is a feature, not friction.

This is a **standalone project** (extracted from the now-deprecated `domainspec` monorepo). It is deliberately scoped to what is real and buildable today.

## What's here

| Path | What it is |
|------|-----------|
| [SPEC.md](SPEC.md) | Receipt-backed contract for the current bounded implementation floor and its explicit evidence gaps. |
| [CRAFT.md](CRAFT.md) · [.craft/](.craft/) | Craft ledger — live project state (contexts, decisions, blockers, gaps). Source of truth = `.craft/ledger.yml`. |
| [ide-ergonomics-experience-prototype.html](ide-ergonomics-experience-prototype.html) | Interactive click-through prototype for the IDE Ergonomics presentation: highlighted chat phrase → route card → candidate/side-node/handoff/delegation previews → durable workbench outputs. |
| [development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md](development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md) | Current implementation contract. Joined Task Session and Invoke closeout receipts under the sibling `20260727T044346Z-chain-contract-refresh/` run own completion evidence. |
| [development/deep-spec-dispatch/](development/deep-spec-dispatch/) | Dated June deep-spec exploration and proposal evidence. Useful design history, not current execution or release authority. |
| [development/standalone-extraction/](development/standalone-extraction/) | The plan to bring the code over and make this project runnable. |
| `provenance/` | Archive, not spine: the 19-doc full-vision DomainSpec spec (`legacy-domainspec-spec/`) and a vendored design-skills reference tree (`open-design-reference/`). Mine for detail; do not treat as current. |

## Proven implementation scope

The 2026-07-27 governed-state implementation is locally reproducible across
the working L0 loop and selected trust/layout properties:

- current persisted head drives preview and annotation;
- CSS/global/unattributed changes cannot disappear behind zero structural
  counts;
- browser Accept/Revert requires an actor-neutral, live action-context
  acknowledgment;
- annotation remains disabled until a real target is selected;
- the 390px before/after comparison stacks without horizontal overflow;
- export confirmation, evidence completeness, integration readiness, and
  implementation readiness are separate facts.

This does not establish the full L1 accessibility suite, human ergonomics, or
release authorization. Those remain explicit evidence/authority gaps.

## Status

- Spec spine + Craft ledger: in place; `.craft/ledger.yml` is state authority.
- Backend and no-build loopback preview: implemented and locally reproducible.
- Current completion audit: TypeScript no-emit pass, unit/slice **72/72**,
  Playwright **21/21**, including the independent-process freshness and 390px
  layout witnesses.
- Publication/release: **not authorized**. “Implemented” here is not “shipped.”

## Running

> ⚠️ **Before you test, read [TESTER-BRIEF.md](TESTER-BRIEF.md)** (a one-page safety/consent note) and follow [TEST-PROTOCOL.md](TEST-PROTOCOL.md) for a guided run.

Requires Node ≥ 20 and pnpm. The CLI lives in `backend/`:

```bash
cd backend
pnpm install
pnpm test            # node:test suite (unit + slice)
pnpm test:e2e        # Playwright over the local preview/CLI seams

# Drive the studio. STUDIO_DATA is the data FILE inside a fresh per-run DIR, so the session
# state AND the artifacts (under <dir>/artifacts) are fully isolated and reset together.
# STUDIO_DOCS_ROOT points at a docs root for the handoff export.
export STUDIO_DATA=/tmp/ups-run-1/studio.json      # fresh DIR per run, not a bare /tmp file
export STUDIO_DOCS_ROOT="$(pwd)/.."

pnpm studio session open                         # -> { sessionId: ups-session-0001, ... }
pnpm studio prompt submit ups-session-0001 "a sign-up card"
# register real variant HTML (each <label>.html must stamp data-od-id on annotatable components):
pnpm studio variants register ups-session-0001 --from ./my-variants     # dir of a.html/b.html/c.html
#   (or)  pnpm studio variants register ups-session-0001 --label A --file a.html --label B --file b.html
pnpm studio baseline select ups-session-0001 B
pnpm studio baseline commit ups-session-0001
pnpm studio comment add ups-session-0001 --selector "[data-od-id=cta.primary]" --label "Primary button" --od-id cta.primary --intent reword --note "say Continue"
pnpm studio synthesize ups-session-0001          # -> { batch: { batchId: ups-batch-00001, ... } }
pnpm studio batch approve ups-session-0001 ups-batch-00001
# two-gate apply: stage an agent-proposed candidate (head does NOT advance), then accept:
pnpm studio apply ups-session-0001 ups-batch-00001 --candidate-from ./candidate.html   # -> openPath to view the staged diff
pnpm studio accept ups-session-0001              # -> head advances by one; openPath to the committed HTML
pnpm studio revisions ups-session-0001
pnpm studio handoff export ups-session-0001 --confirm
```

For the exact receipt commands:

```bash
cd backend
./node_modules/.bin/tsc -p tsconfig.json --noEmit
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test --reporter=list
```

**Seeing the result in a browser:** run `studio preview <sid>` and open the
printed loopback URL. It renders the current head, labeled historical
variants, staged before/after evidence, and click-to-annotate. Browser
Accept/Revert shows candidate/revision identity, target state, and diff recap;
the caller must acknowledge that exact context before the request is posted,
and the server rejects absent or stale context. This acknowledgment records
inspection intent—it does not grant authority. Export remains terminal-only.

**Reset:** point `STUDIO_DATA` at a file inside a fresh **directory** per run (e.g. `/tmp/ups-run-2/studio.json`) — both the session state and the artifacts live under that directory, so a new dir is a clean slate. To reset in place: `rm -rf "$(dirname "$STUDIO_DATA")"`.
