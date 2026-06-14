# Research Result — Tilth Runtime Build (LOCAL-FIRST execution)

- Run: `2026-06-12-craft-pipeline-hydration`
- Node: `tilth-runtime-build` (Craft `CTX-TRB-ROOT`)
- Dispatch: `gq-research-strategy-tilth-runtime-build-2026-06-12`
- Strategy executed: LOCAL-FIRST ONLY. Steps r01–r06 run. External research = DEFERRED (rg03 not authorized).
- Overall verdict: **PASS (local-first baseline complete; no external research required to map the question)**

## Core question

What local-first runtime, vault, routing, ingestion, Scout, drafting, review, and audit evidence is needed for v0.1 without adding a UI layer?

## r01 — Scope (node boundary)

The node owns workbook **Workstream B — Software / Tilth Build** (`docs/features/tilth-runtime-build/.craft/ledger.yml` note line 9). Boundary-and-canon owns deprecated posture vocabulary and the v0.1-UI scoping decision, so two of this node's gaps are *links* into that node, not owned here. Node scope is cleanly separable; no cross-node drift. No question in this run requires Josh's business judgment — all four gaps are technical/governance sequencing, not founder strategy.

## r02 — Local evidence baseline (all paths verified to exist)

| Evidence class | Concrete path | Confirms |
| --- | --- | --- |
| Source contract (Workstream B rows) | `docs/golden-quill-task-role-breakdown-handoff.md` (lines 42–55) | The 14 Tilth-Build task rows: inference, routing, vault, ingestion, Scout, Mapper, drafting, ensemble+rule review, posture, sanitization, audit log, console UI, evidence capture, Golden Image |
| Node Craft ledger | `docs/features/tilth-runtime-build/.craft/ledger.yml` | 4 active gaps, scope note, artifact set |
| Linked canon ledger | `docs/strategy/development/boundary-and-canon/.craft/ledger.yml` | `DEC-BC-POSTURE-VOCAB` (blocking), `DEC-BC-UI-BOUNDARY`, `GAP-BC-UI-SCOPE` |
| Router (model bindings) | `router.yaml` (16.6K, exists) | Local inference / routing / role bindings live here, not in spreadsheet |
| Architecture (locked v0.1 + amendments) | `pipeline/architecture/v0.1/` (v7_0_10 LOCKED amendment present, plus v7_0_1…v7_0_13) | Three-posture routing, F-CLASS gates, classification register, vault paths, audit/WPFA receipts |
| Node runtime handoff | `…/2026-06-12-craft-pipeline-hydration/RUNTIME-HANDOFF.md` | Runtime stages not_run; permission-gated |
| Node Invoke-first direction | `…/INVOKE-FIRST-ARTIFACTS.md` | define/design/plan direction only |

Workbook-vs-canon delta (data_quality_accuracy): the workbook posture row (`docs/golden-quill-task-role-breakdown-handoff.md` line 50) names **"Unrestricted / Hybrid / Sanitized / Sovereign"** — this is STALE. Current canon is the three-posture set **Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign** (`CLAUDE.md` Beta Model Strategy; `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`; boundary ledger `DEF-BC-POSTURES-001`). Do not propagate the workbook wording.

## r03 — Research lane map (per gap)

| Gap | Severity | Lane selected | Why | Local source |
| --- | --- | --- | --- | --- |
| `GAP-TRB-WORK-PACKS` | block | **Local-only** | Rows → sequenced work packs is a planning/decomposition task answerable from handoff + architecture; no external input | handoff lines 42–55; `pipeline/architecture/v0.1/` |
| `GAP-TRB-POSTURE-CANON` | block | **Local-only (cross-node link)** | Resolved by translating to canon already on disk; owned by boundary-and-canon `DEC-BC-POSTURE-VOCAB` | boundary ledger; `CLAUDE.md`; v7_0_10 amendment |
| `GAP-TRB-UI-PHASE` | flag | **Local-only (decision pending)** | v0.1 no-UI boundary is locked in canon; needs phase decision `DEC-BC-UI-BOUNDARY`, not research | `CLAUDE.md` ("no UI layer for v0.1"); boundary `GAP-BC-UI-SCOPE` |
| `GAP-TRB-GOLDEN-IMAGE-HANDOFF` | flag | **Local-only + coordinate** | Image signing / packaging interface is internal handoff to Workstream A (hardware-golden-image); substrate locked (Pydantic AI + Ollama/vLLM) | handoff line 55; `CLAUDE.md` substrate lock |

All four gaps resolve inside the local workspace. None forces an external pass.

## r04 — External-research decision: DEFERRED (rg03 — not authorized)

No external lookup was performed. External research stays permission-gated and is recorded as deferred. **Named bounded requests** (each fires only on Josh's explicit approval AND a confirmed local-evidence gap):

1. **Local-model/runtime package currency** — *only if* a named implementation gap appears during the Invoke plan stage (e.g., a pinned Ollama/vLLM model checkpoint or its OpenAI-compatible endpoint behavior is undocumented locally). Bounded to package/runtime docs for the already-locked substrate. No vendor-selection scope.
2. **No cloud-vendor dependency decisions** without approval (protected-context flag). The substrate is LOCKED per ADR-001 / v7.0.3; this request is explicitly *not* opened.

Both are gap-triggered and conditional; neither is active.

## r05 — Claim-evidence validation

See `research-validation-ledger.md` (sibling file). Every claim maps to a source class + concrete path + validation question + owner-boundary check. Verdict: all claims grounded; zero unsourced claims; zero org-isolation breaches (no `orgs/` PROJECT_CONTEXT read).

## r06 — Synthesis handoff

- The local-first baseline is **sufficient** to drive the node's Refine route (`ENA-TRB-REFINE-ROUTE`) into Invoke define/design/plan without any external pass.
- Recommended next route: resolve the two blocking dependencies first — `GAP-TRB-WORK-PACKS` (decompose Workstream B rows into sequenced work packs) and `GAP-TRB-POSTURE-CANON` (adopt three-posture canon, drop "Sanitized"). UI-phase and Golden-Image are flags that can run in parallel.

## Residue

- `GAP-TRB-POSTURE-CANON` cannot be *closed* inside this node — it is owned by boundary-and-canon (`DEC-BC-POSTURE-VOCAB`, blocking). This node consumes the resolution, does not author it.
- `GAP-TRB-UI-PHASE` awaits governance decision `DEC-BC-UI-BOUNDARY` (PENDING).
- Workbook stale-vocabulary risk persists until the posture row is translated; any downstream reader of the handoff must apply the canon override noted in r02.

## Next move

Operator decision: approve local-first research **execution** (subagent reviewers + bounded route) for this node, or hold at strategy-ready. Recommended: proceed local-only into Invoke `plan` for `GAP-TRB-WORK-PACKS`; keep both external requests deferred.

## Owner boundary (rg06)

Planning evidence only. This run wrote exactly two files into the RUN_DIR (this file + `research-validation-ledger.md`). It did NOT mutate `.craft/ledger.yml`, canonical architecture, router.yaml, or any lifecycle artifact.
