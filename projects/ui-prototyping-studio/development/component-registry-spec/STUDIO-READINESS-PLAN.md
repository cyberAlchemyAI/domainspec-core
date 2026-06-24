# Invoke · Plan — Studio Test/Use/Integration Readiness

- Mode: `plan` · Owner: `invoke` (parent-coordinator receipt under the `goal` loop)
- Goal: **Goal B** — make the studio ready to test and use, so integration with other apps can begin.
- Frontier nodes routed: `GAP-CONTRACT-DRIFT-004`, `BLK-FIXTURE-CORPUS-001`, `GAP-DOCS-CODE-SPLIT-005`, `DEC-CLI-NOT-MCP-012` (the integration interface).
- Status: **non-executed plan** (route staged; nothing built/committed here).

## What "ready to test and use" means here

The studio CLI loop already runs end-to-end (we drove generate→annotate→synthesize→apply→accept→preview live). "Ready" = the loop is **correct, repeatably testable, and exposes a stable contract another app can drive.**

## Slices

### B1 — Correctness: close `GAP-CONTRACT-DRIFT-004`  *(test-blocking bug)*
- `mock-api` emits `RevisionRecorded` but never a distinct `RevisionApplied`, while `models.ts` declares both. The two-gate apply (stage→accept) needs both events distinct for honest state.
- **Done:** the apply path emits `RevisionApplied` (head advances) vs `RevisionRecorded` (manifest append) distinctly; `slice.test.ts`/`server.test.ts` assert both. Route: `task-session`.

### B2 — Repeatable tests: close `BLK-FIXTURE-CORPUS-001`  *(fixtures)*
- No fixture corpus → no deterministic regression surface. Add a small variant/comment/candidate fixture set the e2e + unit suites run against (the TROQAR login variants are a natural seed).
- **Done:** `pnpm test` + `pnpm test:e2e` run green against a checked-in fixture corpus; the `--green` theme-edit toy-game (from the per-element run) is one fixture. Route: `task-session`.

### B3 — Integration interface: formalize the CLI contract (`DEC-CLI-NOT-MCP-012`)  *(the integration surface)*
- Other apps integrate by **driving the `studio` CLI** (decided: CLI, not MCP). Make that a *contract*: documented verbs, stable JSON output shapes (`sessionId`, `state`, `diff`, `openPath`, `stagedRef`), exit codes, and `STUDIO_DATA`/`STUDIO_DOCS_ROOT` env as the isolation boundary.
- **Done:** an `INTEGRATION.md` + a JSON-schema for each verb's output; a host app can open a session, register variants, drain comments, run the cycle, and read the diff **without reading the source**. Route: `invoke design` → `task-session`.

### B4 — Reconcile the docs/code split: `GAP-DOCS-CODE-SPLIT-005`  *(operator decision)*
- 8 domainspec files hold stale `docs/features/ui-prototyping-studio/` handoff paths; **do not** repoint them at `projects/...` (would make the submodule depend on a parent path). Decide where the handoff bundle references the spec now.
- **Done:** a `decision-gate` record fixing the handoff reference target; then reconcile. Route: `decision-gate` → `task-session`. **Operator-owned.**

## Sequencing

B1 (correctness) → B2 (fixtures, depends on B1 events) → B3 (interface, depends on a green loop) → B4 (operator decision, parallel). B3 is the one that *enables integration with other apps*; B1+B2 make it trustworthy first.

## Relation to Goal A

Goal A (`UIIdentityIndex`) is **architecture convergence**; Goal B is **operational readiness**. They are independent: B3 can expose the current L0 loop as an integration surface now, while A1's registry lands in the L4 design. A host app can integrate against B3 today and gain the component registry later without an interface break (the CLI contract is additive).

## Deferred / gated

- Full L4 identity/DNA build (Goal A's A2) — not required for B-readiness.
- MCP surface — explicitly out (`DEC-CLI-NOT-MCP-012`); revisit only if a host needs it.

## Non-executed — staged route for operator approval.
