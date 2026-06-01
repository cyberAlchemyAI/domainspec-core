# Spec card — Logician gate F-DEPRECATION-EXEMPTION-REUSE (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit/` — EN-003 F-1-Cycle3
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #6

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 2 (reads lock_history.v1.jsonl)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-06`

---

## Gate name and failure code

- **Gate:** `F-DEPRECATION-EXEMPTION-REUSE`
- **Failure code:** `F-AMDT-06`
- **Kind:** PRE-gate on amendment with `amendment.forced_replacement: true`

## Purpose

When a model or component is deprecated by its provider, a replacement must be selected. The deprecation event triggers the amendment but cannot pre-approve the replacement — "forced by deprecation" is not a bypass for L-005 cross-family review. This gate verifies that any forced-replacement amendment has a live, passing cross-family audit artifact before it can promote to LOCKED-sealed. Without this gate, deprecation urgency could be used to skip the review obligation entirely.

## Trigger condition

Fires as a PRE-gate on any amendment whose frontmatter contains `forced_replacement: true`. The gate validates that a proper cross-family audit was conducted for the replacement, not just for the deprecation event itself.

## Input contract

```python
@runtime_checkable
class AuditArtifactReaderCallable(Protocol):
    def __call__(self, path: str) -> dict: ...

@runtime_checkable
class FileExistsCallable(Protocol):
    def __call__(self, path: str) -> bool: ...
```

- `amendment_frontmatter: dict` — the amendment being proposed. Must contain `forced_replacement: true` (trigger), `audit_artifact_path: str`.
- `audit_artifact_reader: AuditArtifactReaderCallable` — injected callable that reads and parses the audit artifact at the specified path.
- `file_exists: FileExistsCallable` — injected callable to check artifact existence before reading.

## Pass/fail criteria (deterministic — no LLM)

1. Confirm `amendment_frontmatter["forced_replacement"]` is `True` (trigger guard).
2. Extract `audit_artifact_path` from frontmatter. If absent → FAIL.
3. Check file exists via `file_exists(audit_artifact_path)`. If not → FAIL.
4. Read artifact via `audit_artifact_reader(audit_artifact_path)`.
5. Check the artifact's final Red Team verdict:
   a. If `red_team_verdict.blocking` is `False` → PASS (audit passed cleanly).
   b. If `red_team_verdict.blocking` is `True` → check for explicit Cycle N fix section: the artifact must contain a `cycle_fixes` list where each entry addresses a blocking finding with `finding_id`, `fix_description`, and `closure_evidence` fields. All blocking findings must have corresponding fix entries. Any unaddressed blocking finding → FAIL.
6. **FAIL (`F-AMDT-06`):** any of the above checks fail.
7. **FAIL (`F-AMDT-06`):** any injected callable raises. Fail-closed.

## Failure behavior

- **DENY** the amendment promotion to LOCKED-sealed.
- Emit structured failure record to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-06"`, `gate: "F-DEPRECATION-EXEMPTION-REUSE"`, detail: which check failed (missing artifact, blocking verdict without fixes, unaddressed findings).
- Operator must commission or complete a cross-family audit for the replacement before re-submitting.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- All file access via injected Protocols (E-017 pattern). No direct `open()` or `Path.read_text()`.
- The `cycle_fixes` matching logic compares `finding_id` fields between blocking findings and fix entries. A finding is "addressed" if a fix entry with the same `finding_id` exists and has non-empty `fix_description` and `closure_evidence`.
- Lives at `pipeline/logician/gates/f_deprecation_exemption_reuse.py`.
- AST-lint R1–R5 clean at module load.

## Test criteria

### Unit tests (≥30)
- `forced_replacement: true`, audit exists, Red Team `blocking: false` → PASS.
- `forced_replacement: true`, audit exists, Red Team `blocking: true`, all findings have fixes → PASS.
- `forced_replacement: true`, audit missing → DENY.
- `forced_replacement: true`, `audit_artifact_path` absent from frontmatter → DENY.
- `forced_replacement: true`, Red Team `blocking: true`, one finding has no fix → DENY.
- `forced_replacement: true`, Red Team `blocking: true`, fix exists but `closure_evidence` empty → DENY.
- `forced_replacement: true`, Red Team `blocking: true`, fix exists but `finding_id` doesn't match any blocking finding → DENY.
- `forced_replacement: false` → no-op PASS (gate doesn't fire).
- `forced_replacement` absent → no-op PASS.
- Artifact exists but is malformed (no `red_team_verdict` key) → DENY.
- Parametrized over 1, 3, 5 blocking findings with matching/mismatching fix entries.

### Adversarial tests (≥5)
- `test_adv_file_exists_returns_true_but_reader_raises` → DENY (fail-closed on read error).
- `test_adv_audit_artifact_is_empty_dict` → DENY (missing `red_team_verdict`).
- `test_adv_cycle_fixes_has_extra_entries` → more fixes than findings → PASS (extra fixes are harmless; all findings still addressed).
- `test_adv_forced_replacement_is_string_true` → `"true"` not `True` → no-op PASS (gate doesn't fire; strict `is True`).
- `test_adv_finding_id_collision` → two different findings with same `finding_id` → both must have fix entries (fix list matched by count, not just existence).

## Dependencies

- Cross-family audit artifact schema (established by EN-001/EN-003 audit rounds — `red_team_verdict`, `cycle_fixes` structure).
- §4 v2.1 gate infrastructure (PRE-gate hook on amendment promotion).
- `FileExistsCallable` and `AuditArtifactReaderCallable` Protocols.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_deprecation_exemption_reuse.py` |
| Tests | `tests/logician/gates/test_f_deprecation_exemption_reuse.py` + `tests/logician/gates/test_adv_f_deprecation_exemption_reuse.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-DEPRECATION-EXEMPTION-REUSE"`, `failure_code: "F-AMDT-06"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-06 |
| Memory | MEMORY.md index entry |

---

*Spec card v1 — 2026-04-20 — per-gate card split from consolidated logician_v2_2_gates.md.*
