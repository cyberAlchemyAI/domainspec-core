# Scout — Dev Path vs Production Path

**For:** The engineer who picks up the Tilth v0.1 Section 5 wire-up.
**From:** Josh (operator) + Claude (session 2026-05-23).
**Status:** Dev path is shipping today. Production path stays LOCKED until you arrive.

## The two-copies architecture

Tilth's Scout seat has two parallel entrypoints. They share the **reasoning contract** (prompts, output schema, validation) but diverge on **transport**.

| | **Production path** | **Dev path** |
|---|---|---|
| **Entrypoint** | `pipeline/orchestrator/seats/scout.py` ( `run(context_path, candidates_path, out_path)`) | `pipeline/deprecated/operator_glue/tilth_scout_ui.py` (CLI bridge for apps/tilth_ui) |
| **Capstone** | `pipeline/scout/run.py` `run_scout_discover_verify_review(...)` — six-channel parallel fan-out → live VERIFY → REVIEW queue | None — Channel A only, no VERIFY round-trip |
| **Routing** | `router.call_seat("scout", ...)` → `router.yaml#tilth.scout` → `routing.yaml` → posture-aware provider boundary | Direct HTTP to provider API, env-var swappable |
| **Default model** | `ollama/mistral:7b` (8GB tier) / `mixtral:8x22b` (128GB tier) per `routing.yaml` | `gemini-2.5-flash` (Google AI Studio free tier) |
| **Classification ceremony** | Required (Frontier-Eligible posture) | Bypassed |
| **Outbound boundary** | `enforce_outbound_boundary(stdlib_urlopen_caller, …)` wrapper with F-CLASS PRE/POST chain | Bare `urllib.request.urlopen` |
| **Sovereignty session boot** | Required (vault commit hook, HMAC keys, FDBroker, NonceRegistry) | None — stateless |
| **Vault writes** | Checkpoint + degradation ledger + Channel A SAM/USAspending snapshots | None |
| **Audit trail** | Full per Five Laws + Logician PRE/POST gates | Just the UI's event log |
| **Customer deployments** | YES — this is the canonical path for Beta / V1 / V1.x customer Tilth nodes | **NO** — dev face only |
| **Hardware target** | 128GB Mac Studio (Stage 2+); 8GB only via `routing.yaml` `tier_8gb` rows | Operator's 8GB Mac Mini |
| **Touched by** | An engineer under Thesis Team audit discipline per `pipeline/engineering/engineering_process_v0.1.md` §3 | Josh + Claude, freely, no LOCK ceremony |

## Why the split exists

The operator's daily-driver workflow (RESCAN button in `apps/tilth_ui_react/src/routes/Scout.tsx` → see federal opportunities → start writing) cannot tolerate weeks of provider-boundary debugging and Section 5 plumbing before it produces value. The dev path skips the ceremony so RESCAN works today. The production path keeps the ceremony so customer deployments are audit-clean tomorrow.

The shared reasoning contract — `SYSTEM_PROMPT + build_user_prompt + extract_json + validate` imported from `pipeline.orchestrator.seats.scout` into the bridge — means Scout's *behavior* is identical across both paths. Only the *transport* differs.

## What the dev path explicitly bypasses (and why)

1. **`pipeline.orchestrator.router.call_seat`** — would require:
   - Posture loaded from a signed classification register (`vault_shared/classification/register.yaml` + `orgs/<slug>/vault/classification/register.yaml`) — not set up for the dev org yet.
   - `classification_context` parameter on every call (`{"inputs": [{"field_path": "prompt", "class_name": "public"}]}`) — would need to be threaded through `pipeline/orchestrator/seats/scout.py`.
   - The outbound boundary wrapper, which has a real bug (see next item).

2. **`pipeline.orchestrator.provider_boundary.stdlib_urlopen_caller`** at line ~368 unconditionally refuses non-https URLs (DC-CYCLE2-02 fold-in). This was intended as defense-in-depth against misconfigured *cloud* endpoints, but it fires on every call — including legitimate local ollama at `http://localhost:11434/v1/chat/completions` per `routing.yaml`. The `_local_provider_caller` shim sets `_INSIDE_WRAPPER.active` to skip the cloud F-CLASS gates, but the https check is in the shared canonical caller and fires regardless. **Result:** the orchestrator router cannot reach the configured local Scout model at all today.

3. **Section 5 Pipeline orchestrator** — the function that wires `run_scout_discover_verify_review` to all 15 production dependency bindings (sovereignty session boot, `make_default_health_signer`, production FDBroker/NonceRegistry/HTTPClient/VaultWriter/SynopsisFetcher/ApplicantProfileProvider) — is not in the tree. The pieces all exist (`pipeline/sovereignty/interrupted_state.checkpoint`, `degradation_log.record_degradation`, `make_default_health_signer`, etc.) but no caller assembles them.

## The work to merge the two paths

When you're ready to collapse the dev/prod split:

### Phase 1 — fix the outbound boundary (~5 LOC, Thesis-audited)
1. Move the `if not url.startswith("https://")` check from `provider_boundary.stdlib_urlopen_caller` (line ~368) into the PRE chain of `enforce_outbound_boundary` so it only fires for cloud-egress wrapped calls.
2. Add an explicit allowlist or accept-http path for local providers (or rely on the fact that `_local_provider_caller` doesn't go through the wrapper post-fix, so the check naturally won't fire for local).
3. Add regression test: `_local_provider_caller(url="http://localhost:11434/...", ...)` returns 200 without raising `F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY`.
4. LOCK the change as a §4 v2.x.y amendment per `pipeline/engineering/engineering_process_v0.1.md` §3.

### Phase 2 — pass classification_context through orchestrator/seats/scout.py
1. Add `classification_context: ClassificationContext | dict | None` kwarg to `run(...)` and `call_seat(...)` invocation site (line ~223).
2. For Scout's inputs (RFA candidates + PROJECT_CONTEXT): default to `PUBLIC` classification (federal grant data + applicant context are both PUBLIC by Three-Layer Defaults).
3. Wire from the deployment posture: if `local_only_sovereign`, no classification needed; if `frontier_eligible` or `split_context_hybrid`, the `inputs` array drives routing.

### Phase 3 — wire Section 5 production bindings (this is the real work)
1. Build production `HTTPClient` (wrap `urllib`/`httpx` with the retry ladder).
2. Build production `FDBroker` + `NonceRegistry` (look for the protocol contracts in `pipeline/scout/channel_a_federal_apis.py`).
3. Build production `SynopsisFetcher` (live RFA synopsis fetch for VERIFY stage).
4. Build production `ApplicantProfileProvider` (reads `orgs/<slug>/PROJECT_CONTEXT.md` + classification register).
5. Build production `VaultWriter` (writes channel A snapshots, REVIEW queue items, checkpoints to `orgs/<slug>/vault/scout/`).
6. Assemble + call `run_scout_discover_verify_review` in a new `pipeline/orchestrator/section_5_scout_cycle.py` (or similar).
7. Wire that into `pipeline/orchestrator/tracks/submission.py` so the dispatcher per `router.yaml#tracks.submission` actually runs it.

### Phase 4 — collapse the dev path
1. Add an env-var or CLI flag to `pipeline/deprecated/operator_glue/tilth_scout_ui.py` that flips it from direct-HTTP transport to `run_scout_seat(ctx_file, cand_file, out_file)` (one-line swap — the bridge's `_call_provider_with_fallback` becomes a thin wrapper around the production seat).
2. Keep the dev path as the fast-feedback shell for prompt iteration. Customer cycles route through the production path.

## What NOT to do

- Don't delete `pipeline/deprecated/operator_glue/tilth_scout_ui.py` when Phase 4 lands. The dev path stays as a fast-iteration shell; collapsing it kills operator velocity.
- Don't propagate the dev path's transport shortcuts (direct HTTP, env-var key resolution, no classification) anywhere into `pipeline/orchestrator/`, `pipeline/scout/`, or `pipeline/sovereignty/`. Those are LOCKED for a reason.
- Don't add a v0.1 amendment to "officially" support the dev path. It's a development tool, not a production primitive.

## Files to read first

- `CLAUDE.md` — workspace orientation, Five Laws, deployment postures
- `router.yaml` — seat-to-model bindings
- `pipeline/orchestrator/router.py` — `call_seat` + posture-aware dispatch
- `pipeline/orchestrator/provider_boundary.py` — the wrapper + the canonical caller with the boundary bug
- `pipeline/orchestrator/seats/scout.py` — the production seat (currently can't reach local ollama because of the boundary bug)
- `pipeline/scout/run.py` — the §4.11 capstone (the function you'll eventually invoke from Section 5)
- `pipeline/scout/discover.py` — Round 8 capstone (channels A–F fan-out)
- `pipeline/scout/verify_stage.py` — Round 9 VERIFY
- `pipeline/scout/review_stage.py` — Round 10 REVIEW queue

- `pipeline/engineering/engineering_process_v0.1.md` §3 — Thesis Team audit discipline

## Open architectural memory

`memory/project_v01_outbound_boundary_ollama_gap.md` carries the boundary-bug analysis. Read that first before opening `provider_boundary.py`.
