---
title: Platform Engineer Quick Reference
audience: Paul Norton (daily-driver one-pager)
authored: 2026-05-15
companion: docs/platform_engineer_onboarding.md
status: living document
---

# Platform Engineer Quick Reference

Daily-driver. For depth on any term, see `docs/platform_engineer_onboarding.md`.

**Read first:** `docs/platform_engineer_onboarding.md` §1.5 *Rules vs Guidance — Calibration Invitation*. The architecture is dense; some of it is genuinely load-bearing and some is ceremony. If a rule reads like it should be guidance not a fail-closed gate, surface it.

## Where to look first for any new problem

1. **`pipeline/engineering/lock_history.v1.jsonl`** (tail it) — what architectural changes shipped recently?
2. **`daily_logs/YYYY-MM-DD.md`** (today + yesterday) — what operational changes shipped?
3. **`memory/MEMORY.md`** + `lessons.md` — institutional context + mandatory pre-checks
4. **Relevant seat module under `pipeline/orchestrator/seats/<seat>/`** — runtime code
5. **Logfire spans** for the failing trace + **`pipeline/logician/audit/`** for any gate FAIL

If a `F-CODE` is in the failure: open `pipeline/logician/gates/<F-CODE>.py` to read the predicate.
If a `R-RULE` is in the failure: open `pipeline/linting/r_<rule>_*.py` to read the rule body.

## The 5 commands you'll run most

```sh
# Run tests — PINNED INTERPRETER (.venv/bin/python3, Python 3.14)
scripts/run_tests.sh                          # full suite
scripts/run_tests.sh tests/logician/          # subtree
scripts/run_tests.sh tests/ -k "F-CLASS"      # by keyword

# Run AST-lint — exit 0 = clean, 1 = violations, 2 = env error
scripts/run_lint.sh pipeline
scripts/run_lint.sh pipeline tests

# Cross-family Thesis dispatch via openclaw bridge (osascript wrapper)
osascript -e 'do shell script "PATH=$HOME/.npm-global/bin:$PATH \
  openclaw infer model run --gateway --model groq/llama-3.3-70b-versatile \
  --prompt @prompt.json --json" with timeout of 600 seconds'

# Tail the architectural change ledger
tail -n 20 pipeline/engineering/lock_history.v1.jsonl | jq -r \
  '"\(.row) | \(.date) | \(.kind) | \(.verdict) | \(.topic // .summary // "-")"'

# Append a lock_history row (manually — there's no helper script yet)
# Use jq to construct + append. Example skeleton:
echo '{"row":215,"date":"2026-05-15","kind":"...","verdict":"...","topic":"..."}' \
  >> pipeline/engineering/lock_history.v1.jsonl
```

**Do NOT run** `python3 -m pytest` (system Python is 3.9, fails dataclass collection silently).

## The 3 files to bookmark

| File | What it tells you |
|------|-------------------|
| `pipeline/engineering/lock_history.v1.jsonl` | Architectural changes (LOCKs). Append-only. Tail for "what shape is the system today." |
| `daily_logs/YYYY-MM-DD.md` (today's) | Operational changes today. What shipped, what broke, what's pre-staged. |
| `memory/MEMORY.md` | Institutional context, locked decisions, operator preferences. Loaded into every new session. |

Honorable mentions: `pipeline/SESSION_BOOTSTRAP.md` (new-session orientation), `router.yaml` (SOLE seat→model bindings).

## Do not touch without operator (Josh) approval

| Surface | Why |
|---------|-----|
| Any LOCKED amendment text in `pipeline/architecture/v0.1/` or `pipeline/blueprint/v0.1/` | LOCKs are immutable. Changes = new amendment, not in-place edit. |
| `pipeline/engineering/lock_history.v1.jsonl` rows (deletion or modification) | Append-only ledger. Hash-chain-friendly. |
| `vault_shared/wpfa/coefficient_registry/active.yaml` | Signed asset. Coefficient changes require signed publisher release + verify against pinned pubkey. |
| Any `orgs/<slug>/vault/classification/register.yaml` | Operator-signed Ed25519. Editing breaks the signature. Re-classify through the wrapper at `pipeline/cli/tilth_review_classify.py`. |
| `router.yaml` model bindings | SOLE source of truth. Changes ripple to derived `pipeline/orchestrator/routing.yaml`. |
| Cedar policies under `pipeline/vault/policies/` | Authoritative authorization layer. Test changes through Cedar evaluator first. |
| Any `F-CODE` predicate that other code dispatches on (search `F-<NAME>` before edit) | Gate semantics are part of the contract. |
| Operator BYOK keystore (wherever it lives on the deployment box) | Customer-owned keys. Never log, never copy, never inspect contents. |
| `SOUL.md` / `USER.md` / `AGENTS.md` / `CLAUDE.md` / `lessons.md` | Operating constitution. Read-only for engineering changes; operator-owned. |

## Emergency stop / rollback

### Stop a running cycle
1. Kill the orchestrator process (Logfire spans will capture the abort).
2. Tail `pipeline/logician/audit/` for the last gate state.
3. Operator decides: re-run from last-good seat output or re-cycle from Scout.

### A gate is fail-closing legitimate work (false positive)
1. Read the gate predicate at `pipeline/logician/gates/<F-CODE>.py` — understand what it asserts.
2. Confirm with operator that the input is actually correct (the gate is usually right).
3. If override is necessary: **M13 audited bypass** — operator signs Ed25519 attestation captured in the audit log. Single-use. Logged.
4. After the cycle, file a spec card on the false-positive class. Do not loosen the gate without a Thesis round.

### A Logician gate has a bug (predicate is wrong)
1. Patch the predicate body — gates live at `pipeline/logician/gates/<F-CODE>.py`.
2. Add a regression test under `tests/logician/gates/`.
3. Run `scripts/run_tests.sh tests/logician/gates/`.
4. File the fix in `daily_logs/` + propose a §4 narrow-corrective amendment if the predicate's contract is changing (not just the implementation).

### Cross-family dispatch (openclaw) is down
1. Check the dashboard at `http://127.0.0.1:18789` for daemon health.
2. Check `~/.openclaw/` config + LaunchAgent status.
3. Confirm provider keys are loaded (Anthropic + Groq + Google + OpenAI BYOK).
4. **Do not silently fall through to single-Claude.** Section E carve-out requires a *logged dispatch failure* in the audit trail. Restore the bridge.

### Local LLM (Ollama / vLLM) unreachable
1. Posture-dependent severity: HIGH on Split-Context Hybrid + Local-Only-Sovereign; LOW on Frontier-Eligible.
2. Check daemon + model load status.
3. If model load is failing on memory: this is the 8 GB dev-node limit — that's expected for very-large models. Fall back to a smaller local model or note the test as Pro-tier-only.

### Logfire bootstrap fails at process start
1. CRITICAL — gate audit log will be incomplete until restart.
2. Confirm `pipeline/observability/` config + Logfire credentials.
3. Restart process. Verify spans flowing.

### Signed asset signature fails (router-template / Coefficient Registry / classification register)
1. **Stay on prior pinned version** — the appliance does that automatically.
2. Investigate the signing path. Did the publisher pubkey rotate? Was the wrong asset version pulled?
3. Do **not** disable signature verification "temporarily" — that's a structural integrity violation.
4. Restore from prior signed version; investigate; operator-signed re-publish.

### A file mentioned in a memory entry no longer exists
1. Treat memory as time-stamped — it may have been renamed or removed.
2. `git log --all --full-history -- '<old path>'` to find the rename / removal commit.
3. Update the memory file (don't delete; correct).

---

## Vocabulary quick-flip

| You see | It means |
|---------|----------|
| LOCKED | Spec promoted to immutable. Changes only via new amendment. |
| F-CODE (`F-CLASS-*`, `F-INTAKE-*`, etc.) | Logician gate. Predicate body at `pipeline/logician/gates/<code>.py`. |
| R-RULE (`R-UPLOADER-NO-SUBMIT`, etc.) | AST-lint structural prohibition. Body at `pipeline/linting/r_*.py`. |
| §NN | Blueprint section. File at `pipeline/blueprint/v0.1/section_NN_*.md`. |
| §0.5 | Interface Index. Spreadsheet-style row ledger of all module/type/schema interfaces. |
| KFR | Key Facts Register. Per-org structured fact store with provenance. `orgs/<slug>/vault/kfr/`. |
| SP0 | Session Preflight 0 — per-cycle context-freshness check. |
| classification register | Per-org file tagging facts public/shareable/confidential/operator_flagged. Drives routing. |
| Cedar | AWS Cedar policy language. Authorization layer. Policies at `pipeline/vault/policies/*.cedar`. |
| Thesis round | Cross-family review cycle (Editor/Judge/Red Team on different model families). |
| osascript→openclaw bridge | Cross-family dispatch mechanism. Cowork → local openclaw gateway → Groq/Google/Anthropic. |
| paired-commit | Section LOCK + §0.5 amendment in the same row pair. Atomic. |
| compound LOCK | 3+ rows in one cascade (e.g., §17 WPFA quadruple LOCK rows 205-208). |
| BYOK | Bring Your Own Key. Customer-owned API keys. Never held by FIT Farms. |
| M13 | The audited bypass. Operator-signed Ed25519. Single-use. Fire-extinguisher. |
| A1, A4, A12 | Architectural assumptions (single-client, operator-trusted, Decimal mandate). |
| bounded-by-A1+A4 | Not-defended-against-yet but acceptable scope. Catalogued for v2 multi-tenant. |
| ADR-001 | The substrate-freeze decision. Pydantic AI + Logfire + Ollama/vLLM + Cedar. |
| Golden Image | Frozen substrate that ships at appliance build. No package-manager access post-build. |
| CIC × CLC | Customer Identity Card × Capital Logic Card. Orthogonal axes. Never hardcode mappings. |
| WPFA | Watts Per Funding Action. Cycle-close accounting. Buyer-facing PDF sales lever. |
| three-posture routing | Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign. Per-deployment choice. |

---

**See full glossary + per-seat runbook + LOCK ceremony + Thesis dispatch in `docs/platform_engineer_onboarding.md`.**
