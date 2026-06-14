# Research Validation Ledger — Tilth Runtime Build

- Dispatch: `gq-research-strategy-tilth-runtime-build-2026-06-12`
- Gate owner: `interrogation` (rg05 claim-evidence) + `dispatch-spec` (rg06 owner-boundary)
- Source classes: **PROJECT** = Golden Quill project evidence (handoff, ledgers, router, architecture, canon). No `orgs/` client evidence read (rg04 / Law 3 clean).

## Claim → source → validation table

| # | Claim | Source class | Concrete path / handle | Validation question | State |
| --- | --- | --- | --- | --- | --- |
| C1 | Node owns Workstream B (Software / Tilth Build) | PROJECT | `docs/features/tilth-runtime-build/.craft/ledger.yml` line 9 | Does the ledger name the workstream the node owns? | VERIFIED |
| C2 | Workstream B has 14 task rows (inference…Golden Image) | PROJECT | `docs/golden-quill-task-role-breakdown-handoff.md` lines 42–55 | Do the rows enumerate the runtime surfaces in the core question? | VERIFIED |
| C3 | Workbook posture row uses stale vocabulary "Unrestricted/Hybrid/Sanitized/Sovereign" | PROJECT | handoff line 50 | Does the row literally carry retired posture names? | VERIFIED |
| C4 | Current canon is three postures: Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign | PROJECT | `CLAUDE.md` Beta Model Strategy; `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`; boundary `DEF-BC-POSTURES-001` | Is three-posture the locked canon that overrides the workbook? | VERIFIED |
| C5 | Posture-canon gap is owned by boundary-and-canon, not this node | PROJECT | boundary ledger `DEC-BC-POSTURE-VOCAB` (blocking:true), `BLK-BC-POSTURE-VOCAB` | Is the decision owned outside this node? | VERIFIED |
| C6 | v0.1 has a locked no-UI boundary | PROJECT | `CLAUDE.md` ("Do not propose a Next.js UI or any UI layer for v0.1 — headless only"); boundary `GAP-BC-UI-SCOPE` | Is no-UI a locked v0.1 boundary? | VERIFIED |
| C7 | UI-phase resolution awaits governance decision DEC-BC-UI-BOUNDARY (PENDING) | PROJECT | boundary ledger `DEC-BC-UI-BOUNDARY` (selected: PENDING) | Is the phase decision still open? | VERIFIED |
| C8 | Substrate is LOCKED (Pydantic AI + Logfire + Ollama/vLLM + DSPy/GEPA + Logician) | PROJECT | `CLAUDE.md` "What NOT to Do" substrate lock (ADR-001, v7.0.3) | Is the runtime substrate frozen, removing it from research scope? | VERIFIED |
| C9 | Router/model bindings live in router.yaml, not the workbook | PROJECT | `router.yaml` (exists, 16.6K) | Does router.yaml exist as the binding source? | VERIFIED |
| C10 | Architecture amendments (incl. v7.0.10 LOCKED) present locally for routing/vault/audit | PROJECT | `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md` (+ v7_0_1…v7_0_13) | Do the architecture files exist to ground routing/vault/audit evidence? | VERIFIED |
| C11 | All four node gaps resolve via local-only lanes | PROJECT | `.craft/ledger.yml` gaps[0-3]; r03 lane map | Does each gap have a local source sufficient to map it? | VERIFIED |
| C12 | No external research executed; both bounded requests are gap-triggered + deferred | PROCESS | RESEARCH-RESULT.md r04; dispatch `route_menu.selected_item_id` = gap_triggered_external | Is external research blocked pending approval? | VERIFIED (DEFERRED) |
| C13 | Golden Image assembly is an internal handoff to Workstream A, not external research | PROJECT | handoff line 55; `.craft` `GAP-TRB-GOLDEN-IMAGE-HANDOFF` (treatment: coordinate) | Is the dependency internal/coordinate, not external? | VERIFIED |
| C14 | No client `orgs/` PROJECT_CONTEXT was read | PROCESS | this run's read set (handoff, two ledgers, router, architecture listing only) | Was org isolation preserved? | VERIFIED (rg04 clean) |
| C15 | This run mutated no canonical/lifecycle artifact; wrote only two RUN_DIR files | PROCESS | RESULT + this ledger; `.craft/ledger.yml` untouched | Was the owner boundary (rg06) respected? | VERIFIED |

## Gate results

| Gate | Condition | Result |
| --- | --- | --- |
| rg01 dispatch-valid | techniques reflected in steps r01–r06 | PASS |
| rg02 local-first | local evidence reviewed before external classes | PASS |
| rg03 external-approval | external requires named gap + Josh approval | DEFERRED (not invoked; correctly blocked) |
| rg04 org-isolation | Golden Quill project evidence only | PASS |
| rg05 claim-evidence | every claim → source class + path + validation question | PASS (15/15) |
| rg06 owner-boundary | route evidence only; no canonical mutation | PASS |

## Overall verdict

**PASS.** All 15 claims are grounded in PROJECT or PROCESS evidence with concrete paths/handles. Zero unsourced claims. Zero org-isolation breaches. External research correctly deferred behind the approval gate. The local-first baseline fully covers the core question; no external comparison is required to map the node's runtime/vault/routing/ingestion/Scout/drafting/review/audit evidence for v0.1.
