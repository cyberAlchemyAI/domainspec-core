"""pipeline.loop.config — §5 v6 constants + module-load integrity asserts.

Blueprint §5 v6 §8 LOCKED 2026-04-19 — canonical constant set for the Pipeline
Orchestrator. Every rebind-sensitive constant below ships a module-load
``assert`` with an inline-literal RHS (V1 discipline — a module-attribute
rebinding cannot bypass the check because the comparison is against a fresh
literal at import time).

Every section listed in ``BLUEPRINT_DEPS`` pins the SHA3-512[:16] prefix of the
blueprint file it implements. Drift detection is manual at Round lock time;
the pins themselves are the contract.
"""

from __future__ import annotations

from typing import Final

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§8 constants (v6 LOCKED constants table)",
            "§3.2.1 RunState schema_version + mode + eval-phase field names",
            "§3.2.6 TabEnvelope tab_ordering type literal",
            "§6 failure-code names (referenced by errors module)",
        ],
    },
    "section_05_v6_amendment.md": {
        "version": "LOCK-READY",
        "hash_sha3_512_prefix16": "52ae6b3b97b159b5",
        "sections_implemented": [
            "pointer-only: invocation-record + STR constants owned by pipeline.observability",
        ],
    },
}

# ---------------------------------------------------------------------------
# §8 v6 rebind-sensitive constants (module-load integrity-asserted)
# ---------------------------------------------------------------------------

TAB_ORDERING: Final[tuple[str, str, str]] = (
    "live_radar",
    "deep_brief",
    "council_draft",
)
assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft"), (
    "TAB_ORDERING has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)

RUNSTATE_SCHEMA_VERSION: Final[int] = 2
assert RUNSTATE_SCHEMA_VERSION == 2, (
    "RUNSTATE_SCHEMA_VERSION has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)

RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED: Final[frozenset[int]] = frozenset({1})
assert RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED == frozenset({1}), (
    "RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)

CALIBRATION_REPORT_SCHEMA_VERSION: Final[int] = 1
assert CALIBRATION_REPORT_SCHEMA_VERSION == 1, (
    "CALIBRATION_REPORT_SCHEMA_VERSION has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)

CALIBRATION_SIGNING_ALGORITHM: Final[str] = "Ed25519"
assert CALIBRATION_SIGNING_ALGORITHM == "Ed25519", (
    "CALIBRATION_SIGNING_ALGORITHM has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)

MAX_CALIBRATION_AGE_DAYS: Final[int] = 90
assert MAX_CALIBRATION_AGE_DAYS == 90, (
    "MAX_CALIBRATION_AGE_DAYS has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)

EVAL_MODE_ALLOWED_INTENTS: Final[frozenset[str]] = frozenset(
    {"golden-set-write", "state-success", "state-failure"}
)
assert EVAL_MODE_ALLOWED_INTENTS == frozenset(
    {"golden-set-write", "state-success", "state-failure"}
), (
    "EVAL_MODE_ALLOWED_INTENTS has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)

SUBMISSION_MODE_FORBIDDEN_INTENTS: Final[frozenset[str]] = frozenset(
    {"golden-set-read", "golden-set-write"}
)
assert SUBMISSION_MODE_FORBIDDEN_INTENTS == frozenset(
    {"golden-set-read", "golden-set-write"}
), (
    "SUBMISSION_MODE_FORBIDDEN_INTENTS has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)

# ---------------------------------------------------------------------------
# §8 constants — scalar / tuple (not rebind-sensitive per blueprint §8 table)
# ---------------------------------------------------------------------------

CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS: Final[tuple[int, int, int]] = (50, 200, 800)
CHECKPOINT_TOTAL_TIMEOUT_SEC: Final[int] = 10
CRON_VAULT_RETRY_WINDOW_SEC: Final[int] = 300
CRON_VAULT_RETRY_ATTEMPTS: Final[int] = 6
RATE_LIMIT_JITTER_RANGE_MS: Final[tuple[int, int]] = (0, 300)
RATE_LIMIT_LEASE_TTL_SEC: Final[int] = 30
CRON_STAMP_TTL_HOURS: Final[int] = 36
SCRIBE_SUBPROCESS_TIMEOUT_MS: Final[int] = 300_000
EDITOR_SUBPROCESS_TIMEOUT_MS: Final[int] = 180_000
JUDGE_SUBPROCESS_TIMEOUT_MS: Final[int] = 180_000
OPERATOR_INTERRUPT_POLL_INTERVAL_MS: Final[int] = 500
MAX_REVISION_ITERATIONS: Final[int] = 3

# Vault-relative path templates (§8 v4 table rows).
CALIBRATION_REPORT_PATH_TMPL: Final[str] = (
    "{org_slug}/golden_set/calibration_reports/{run_id}.json"
)
CALIBRATION_SIGNATURE_PATH_TMPL: Final[str] = (
    "{org_slug}/golden_set/calibration_reports/{run_id}.sig"
)
BYPASS_PENDING_CHECKPOINT_PATH_TMPL: Final[str] = (
    "pipeline/{run_id}/bypass_pending.json"
)

# ---------------------------------------------------------------------------
# Exhaustive F-PIPE-21 / F-PIPE-22 sub-trigger taxonomies
# ---------------------------------------------------------------------------
# §6 v6 line 1052 enumerates every F-PIPE-21 sub-trigger; §6 v6 line 1053 does
# the same for F-PIPE-22. Sub-trigger strings are compared against these sets
# at construction time by concrete failure classes in pipeline.loop.errors.

F_PIPE_21_TRIGGERS: Final[frozenset[str]] = frozenset(
    {
        "mode_change_after_start",
        "eval_mode_has_tab_envelope_hash",
        "eval_mode_invalid_intent",
        "submission_mode_calibration_intent",
        "submission_mode_has_calibration_ref",
        "submission_mode_missing_rfa_hash",
        "submission_mode_missing_project_context_hash",
        "eval_mode_missing_golden_set_ref",
        "eval_mode_has_rfa_hash",
        "eval_mode_has_project_context_hash",
        "golden_set_path_escapes_prefix",
        "golden_set_path_traverses_symlink",
        "eval_run_reached_tab_delivery",
        "calibration_signature_stale",
        "golden_set_manifest_org_mismatch",
    }
)
assert len(F_PIPE_21_TRIGGERS) == 15, (
    "F_PIPE_21_TRIGGERS has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)

F_PIPE_22_TRIGGERS: Final[frozenset[str]] = frozenset(
    {
        "runstate_schema_downgrade",
        "calibration_report_schema_mismatch",
    }
)
assert len(F_PIPE_22_TRIGGERS) == 2, (
    "F_PIPE_22_TRIGGERS has been rebound at module load; "
    "refusing to load pipeline.loop.config"
)
