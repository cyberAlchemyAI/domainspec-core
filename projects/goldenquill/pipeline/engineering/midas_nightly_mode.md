# Midas Nightly Review Mode

**Canonical path:** `pipeline/engineering/midas_nightly_mode.md`
**Invoked by:** OpenClaw scheduled-task (2-3am local) OR manual `--mode nightly-review`
**Parent persona:** `king_midas_implementation_prompt_v2_1.md`

---

## Purpose

Autonomous integrity scan of the Tilth codebase. Midas runs checks that would normally happen at commit time but are worth re-running periodically against drift, forgotten lessons, and environmental change. Auto-remediates §10-qualifying findings; queues larger findings for operator morning digest.

## Scope (what the nightly scan runs)

1. **AST-lint full tree** — `scripts/run_lint.sh` (after ARCH-04 ships). Zero violations expected; any violation → finding.
2. **BLUEPRINT_DEPS drift detection** — `python scripts/check_blueprint_drift.py` walks every module's `BLUEPRINT_DEPS` declaration, recomputes current blueprint hash, compares to locked hash. Mismatch → `drift_possible` finding, re-review required before any code-lock operation on that module.
3. **Full pytest suite** — `.venv/bin/python -m pytest tests/` — diff against last-known-green baseline at `pipeline/metrics/pytest_green_baseline.txt`. New failures → finding. New passes (tests unblocked) → advisory note.
4. **Session-log scan** — `pipeline/metrics/session_log.jsonl` last 7 days. Count `self_check_failures` by failure type. Trends → finding (e.g., "5 of last 10 sessions failed pre-staging check").
5. **GPP-DET re-run** — on the active scope-close pin directory. Any FAIL → finding.
6. **Canary test vectors freshness** — verify corpus at `pipeline/rubrics/` and test vectors at `tests/corpus/` haven't aged past staleness thresholds.
7. **Router integrity** — re-verify `router.yaml` HMAC trailer (after §1 Round H lands). Mismatch → CRITICAL finding.
8. **E-NNN pre-check scan** — for every module changed in last 7 days (`git log --since="7 days ago" --name-only`), check that the `review_lessons.v1.md` E-NNN pre-checks applicable to that module's domain were honored. Miss → finding with reference to the E-NNN.
9. **Provisioning manifest consistency** — diff `provisioning_manifest_v0.1.md` §3 dependencies against `pyproject.toml` actual deps. Drift → finding.
10. **Daily log completeness** — verify every day Midas locked a module has a `daily_logs/<date>.md` entry with the lock summary.

## Remediation policy

### Auto-remediate (narrow-edit per §10)

Findings that qualify for `engineering_process_v0.1.md` §12 v0.1.x narrow-edit:
- Typos in docstrings flagged by §9 provisioning-manifest drift
- Missing `BLUEPRINT_DEPS` hash refresh after a blueprint version bump (mechanical)
- Stale `pytest_green_baseline.txt` rows for tests that correctly changed behavior
- Missing daily log entries where `lock_history.v1.jsonl` has the substantive content

Midas writes the fix, runs the red+adversarial test pair, commits, logs telemetry with `patch_type: "v0.1.x narrow-edit"` and `invocation_mode: "nightly-review"`, writes an E-NNN lesson if the finding represents a new failure mode.

### Queue for operator (morning digest)

Everything else. Morning digest lands at `daily_logs/<date>_nightly_digest.md` with:
- Summary: X findings total, Y auto-remediated, Z queued
- Queued findings sorted by severity (CRITICAL → WARNING → NOTE)
- For each: finding, evidence (file:line or test name), proposed remediation, which task board entry it maps to (or proposal to create one)
- Pre-staging: if any queued finding is self-contained and spec-derivable, spec card drafted per §14 of Midas v2.1 proactive pre-staging

## Escalation criteria

Midas does NOT proceed with auto-remediation and escalates immediately if:
- Finding crosses a Five Operating Law or Four Autonomy Rule
- Finding indicates router.yaml HMAC mismatch (CRITICAL — may indicate tampering)
- Finding involves crypto primitives or key-material paths
- Finding crosses the scope-close pin
- Finding requires operator-voice content
- Two or more findings interact in ways that require human judgment

Escalation = morning digest entry with `ESCALATION_REQUIRED` tag + no auto-remediation attempt.

## Committee involvement

Auto-remediation patches skip committee per §10 narrow-edit carve-out. Queued findings that become full tasks go through the normal committee dispatch when implemented — same 5-cross-family reviewer rule, same all-pass discipline.

**Exception:** Nightly findings that Midas judges ambiguous can optionally be dispatched to a lightweight "verdict-only" committee (Red Team + Reasoner, cross-family) for a PASS / CONCERNS / BLOCK verdict on the finding itself. Not mandatory.

## Invocation

**Scheduled (OpenClaw cron):**
```bash
openclaw agent --agent midas --mode nightly-review --at "0 3 * * *"
```

**Manual:**
```bash
openclaw agent --agent midas --mode nightly-review --scope full
# or scoped:
openclaw agent --agent midas --mode nightly-review --scope ast-lint,blueprint-drift
```

## Session discipline

Nightly mode is a Midas session. Full read order applies (per v2.1 §2). Signature block on every commit. Session metrics logged with `session_type: "nightly-review"`. Self-check runs as always — with the additional check that every finding gets either auto-remediated OR queued with escalation criteria documented.

## Sovereignty note

Nightly mode runs local on the operator's hardware. No phone-home. No external services beyond what the code already calls (provider APIs via committee dispatch, only if Midas opts to use the verdict-only committee exception above). Findings stored locally in `daily_logs/` + `pipeline/engineering/nightly_review/<date>/`. The operator owns the review log.

---

*v1 — 2026-04-20 — specification file; implementation blocked on OpenClaw scheduled-task skill integration (task #12).*
