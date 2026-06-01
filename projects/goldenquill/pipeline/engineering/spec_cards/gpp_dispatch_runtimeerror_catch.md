# Spec card — pipeline.validation.integration_scope_close_2026-04-19.gpp.gpp_council_dispatch (RuntimeError stub fallback)

**STATUS:** PRE-STAGED 2026-05-10
**Round:** Dispatch fallback regression closure — surfaced by 2026-05-10 review (finding #10), confirmed by failing test in `./scripts/run_tests.sh`.
**Canonical home:** `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_council_dispatch.py`

**Framework:** per `pipeline/templates/component_analysis_template.md`.

---

## 1. Blueprint anchors

- `pipeline/blueprint/v0.1/section_05_v6_amendment.md` — F-PIPE-06 cascade discipline (seat dispatch failure must fall through to stub, not abort the round).
- `pipeline/engineering/engineering_process_v0.1.md` §10 — committee dispatch fallback contract.
- `pipeline/validation/integration_scope_close_2026-04-19/gpp/` — Tier-2 GPP council dispatch is the consumer.

**Spec-card version:** v1

---

## 2. Current state (drift / defect)

`pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_council_dispatch.py`:

**`_call_model` (line 447):** raises `RuntimeError` on missing API key (lines 453, 459, 465, 471) and on unknown model prefix (line 473).

**`_dispatch_one_seat` (line 689):** catches `(urllib.error.URLError, OSError, ValueError, KeyError)` — **`RuntimeError` is NOT in the tuple**.

**Effect:** When a provider key is missing (the common dev path on Josh's M1 dev node), `_call_model` raises `RuntimeError("GROQ_API_KEY missing")`, that escapes `_dispatch_one_seat`'s except block, and the documented stub-mode fallback (line 695-698, `dispatch_mode="stub_dispatch_failed"`) never fires. Tier-2 council dispatch aborts the whole round instead of degrading to stub findings.

Confirmed by `./scripts/run_tests.sh`: the no-key fallback test for `_dispatch_one_seat` fails for exactly this reason.

---

## 3. Scope

### 3.1 In scope

- Add `RuntimeError` to the except tuple at `gpp_council_dispatch.py:689`:
  ```python
  except (urllib.error.URLError, OSError, ValueError, KeyError, RuntimeError) as exc:
  ```
- Preserve the existing log shape (`"  {seat} dispatch via {model_str} failed: {last_err}"`); `RuntimeError("GROQ_API_KEY missing")` formats cleanly.
- Verify the stub-fallback path (line 694-698) executes when every primary + fallback model in the seat's cascade raises `RuntimeError`.
- Audit `_call_model` to confirm `RuntimeError` is the *only* exception class raised that the dispatch loop should catch. (`urllib.error.HTTPError` is already caught separately at line 680; that's correct — HTTP errors carry status codes worth distinct logging.)
- If `_call_model` also raises bare `Exception` anywhere indirectly (e.g., JSON decode in `_dispatch_via_*` helpers), trace and bring those under the same fallback umbrella OR document the carve-out.

### 3.2 Out of scope

- Restructuring `_call_model` to return `(text, error)` tuples instead of raising. Larger refactor; not justified for v0.1 GPP test harness.
- Adding new failure codes. The existing `dispatch_mode="stub_dispatch_failed"` enum value is sufficient.
- Telemetry/metrics on dispatch-failure rates. Separate observability card.

---

## 4. Failure codes touched

- None new.
- Existing `dispatch_mode` enum behavior is *restored* — no semantic change to the contract; the bug was that one path was unreachable.

---

## 5. Test surface

### 5.1 Failure-mode tests
- **No-key path (the regression):** with `env={}` (no `GROQ_API_KEY`, no `GOOGLE_API_KEY`, no `OPENAI_API_KEY`, no `ANTHROPIC_API_KEY`), `_dispatch_one_seat` returns `(stub_findings, "stub_dispatch_failed", "")`. Each stub finding carries `dispatch_error` containing the missing-key message.
- **Unknown-model path:** with a router config containing `primary: "made-up/nonexistent-1"`, `_dispatch_one_seat` returns stub mode with `dispatch_error` containing `"No live dispatch handler for model: made-up/nonexistent-1"`.
- **Primary missing key, fallback present:** primary raises `RuntimeError`, fallback succeeds → returns live findings from fallback. Dispatch mode is `"live"`, not stub.
- **Both missing key:** both primary and fallback raise `RuntimeError` → stub mode, error message from fallback (last_err).

### 5.2 Regression coverage
- Confirm the existing `HTTP 429` / `URLError` / `OSError` paths still produce stub mode unchanged.
- Confirm the live-success path is untouched (no behavioral diff on the happy path).

### 5.3 Smoke
- Manual run: `python -m pipeline.validation.integration_scope_close_2026-04-19.gpp.gpp_council_dispatch --dry-run` succeeds; no RuntimeError escapes.

---

## 6. Done definition

- `pytest pipeline/validation/integration_scope_close_2026-04-19/gpp/` green, including the no-key fallback test that was failing.
- Full suite (`./scripts/run_tests.sh`) green — except environment-gated sovereignty tests.
- No `RuntimeError` escapes `_dispatch_one_seat` under any tested input.
- One-line diff explained in commit message; reference this spec card.

---

## 7. Risks / open questions

- **Q1.** Is `gpp_council_dispatch.py` considered an integration-scope-close fixture (frozen audit artifact) or a live module? Path includes `validation/integration_scope_close_2026-04-19/`, which is dated like a frozen audit dir, but tests still exercise it. If frozen, this fix needs to land alongside an audit-trail note (lock_history row). If live, just patch and ship.
- **Q2.** Are there sibling dispatch modules under `pipeline/validation/*` or `pipeline/engineering/*` with the same bug shape? Worth a grep for `except (urllib.error.URLError, OSError, ValueError, KeyError)` to see if the same fix applies elsewhere. If so, expand scope OR file additional cards.

---

## 8. Suggested executor

Codex (Claude Code) — single-session fix. One-line change in the except clause + four new failure-mode tests. Cross-family review optional given the tiny diff; recommend Editor + Red Team only (skip Judge — no rubric reasoning needed).
