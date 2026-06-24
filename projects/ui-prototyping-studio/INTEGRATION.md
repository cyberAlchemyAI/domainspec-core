# Studio Integration Contract (B3)

How another app drives the UI Prototyping Studio. The **studio CLI is the integration surface** (`DEC-CLI-NOT-MCP-012`: CLI, not MCP). A host app shells out to the CLI, parses JSON from stdout, and checks the exit code. No source dependency, no shared process.

> Status: contract for the **live L0 CLI backend** (62/62 unit/slice green). Additive — the `UIIdentityIndex` registry (A1) lands later without breaking this surface.

## Invocation

```bash
# Clean JSON (no pnpm preamble): invoke the CLI entrypoint directly.
STUDIO_DATA=<run-dir>/studio.json \
STUDIO_DOCS_ROOT=<docs-root> \
  npx tsx backend/src/cli/studio.ts <verb> [args...]
# (or, built:  node backend/dist/cli/studio.js <verb> ...)
```

- **`STUDIO_DATA`** — path to the data **file inside a fresh per-run directory**. Session state AND artifacts (`<dir>/artifacts/`) live under that dir, so each run is fully isolated and reset together. A new dir = a clean slate; `rm -rf "$(dirname "$STUDIO_DATA")"` resets in place.
- **`STUDIO_DOCS_ROOT`** — docs root used by `handoff export`.

## Output contract

- **stdout** — the verb's result as pretty-printed JSON (`JSON.stringify(value, null, 2)`). Parse stdout as JSON.
- **stderr** — on error, a structured payload `{ "code": "<ERR_CODE>", "message": "...", "details": {...} }`. This is the authoritative error signal.
- **exit code** — `0` success; non-zero failure. Observed: `2` validation/usage/domain error (stderr carries the structured payload), `1` unknown verb / preview-server failure, `3` a verb-specific soft-fail. Treat `0` vs non-zero as the primary branch; read the stderr `code` for specifics.

## Verb catalog

| Verb | Args | Result (stdout JSON) |
| --- | --- | --- |
| `session open` | — | session snapshot `{ sessionId, prompt, variantCount, variantLabels, baseline, revisionHeadId, selectionGate, applyGate, integration, state }` |
| `prompt submit <sid> "<text>"` | session id, prompt | session snapshot (`state: PromptCaptured`) |
| `variants register <sid> --from <dir>` | dir of `a.html/b.html/c.html` (`<label>.html`, lowercase) | `{ variants:[{variantLabel, htmlArtifactRef, status,...}], openPaths:[...] }` |
| `variants register <sid> --label A --file a.html ...` | explicit label/file pairs | same |
| `baseline select <sid> <A\|B\|C>` | label | session snapshot |
| `baseline commit <sid>` | — | session snapshot (`selectionGate: satisfied`) |
| `comment add <sid> --selector <s> --label <l> --od-id <id> --intent <i> --note <n>` | annotation; `--od-id` may be omitted for untagged (`odId:null`) | `{ commentId, sessionId, revisionId, target:{selector,elementLabel,odId}, severity, intent, note, ... }` |
| `synthesize <sid>` | — | `{ batch:{ batchId, sourceRevisionId, status:'draft', generatedFromCommentIds, tasks:[...], approval, checksum } }` |
| `batch approve <sid> <bid>` | — | batch (`approval.approvedBy` set) |
| `apply <sid> <bid> --candidate-from <file>` | agent-proposed candidate HTML | `{ session(state:RevisionApplied), stagedRef, candidateHtmlHash, diff:{fragments,added,changed,removed}, openPath }` — **stages; head does NOT advance** |
| `accept <sid>` | — | session (`state: RevisionRecorded`) — **head advances by one** |
| `discard <sid>` / `revert <sid>` | — | session — reversible |
| `state <sid>` | — | current session snapshot |
| `revisions <sid>` | — | append-only revision manifest |
| `preview <sid> [--port N]` | — | starts a loopback HTTP preview server; prints `{ preview: "http://127.0.0.1:<port>/preview/<sid>", hint }` |
| `handoff export <sid> --confirm` | **terminal-only, irreversible** | export bundle ref |

## The loop (what a host app sequences)

```
session open → prompt submit → variants register → baseline select → baseline commit
→ comment add (×N)        # or drain externally-captured comments
→ synthesize → batch approve
→ apply --candidate-from <candidate.html>   # GATE 1: stage (RevisionApplied, head fixed)
→ accept                                     # GATE 2: human disposes → RevisionRecorded, head++
→ revisions / handoff export --confirm
```

## Invariants a host MUST respect

- **Two-gate apply.** `apply` only stages; only `accept` advances head. The host surfaces the staged `diff` to a human before `accept` (governance is a feature).
- **Export is the one irreversible edge.** `handoff export` requires `--confirm`; it is terminal-only (never wired to a button). Everything else (`discard`/`revert`) is reversible.
- **Gates.** `comment add` requires `selectionGate: satisfied` (baseline committed). Read `selectionGate`/`applyGate`/`state` from snapshots to drive the host UI.
- **Isolation.** One `STUDIO_DATA` dir per session/run; never share a bare `/tmp` file across runs.

## Readiness signals

The session snapshot carries an `integration` block — `{ uiPhaseBridgeReady, generateTestsUiReady, uiImplementReady }` — a host can poll to gate downstream phases.

## Regression surface

Drive the contract against the checked-in corpus `backend/e2e/fixtures/corpus/` (`CORPUS.md`): the TROQAR variants + the `--green` honest-diff toy-game. A host integration test = run the loop above against `troqar-login/` (a/b/c.html) and assert the snapshot states + `diff` shape.

## Versioning

This contract describes L0. Additions (the `UIIdentityIndex` registry, a CSS-diff lane) extend the JSON shapes additively; verbs and the two-gate sequence are stable.
