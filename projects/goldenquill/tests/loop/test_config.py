"""Tests for pipeline.loop.config — §8 v6 constants + BLUEPRINT_DEPS + trigger sets.

Blueprint §5 v6 §8 LOCKED 2026-04-19.
"""

from __future__ import annotations

from pipeline.loop import config as cfg
from pipeline.loop.config import (
    BLUEPRINT_DEPS,
    BYPASS_PENDING_CHECKPOINT_PATH_TMPL,
    CALIBRATION_REPORT_PATH_TMPL,
    CALIBRATION_REPORT_SCHEMA_VERSION,
    CALIBRATION_SIGNATURE_PATH_TMPL,
    CALIBRATION_SIGNING_ALGORITHM,
    CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS,
    CHECKPOINT_TOTAL_TIMEOUT_SEC,
    CRON_STAMP_TTL_HOURS,
    CRON_VAULT_RETRY_ATTEMPTS,
    CRON_VAULT_RETRY_WINDOW_SEC,
    EDITOR_SUBPROCESS_TIMEOUT_MS,
    EVAL_MODE_ALLOWED_INTENTS,
    F_PIPE_21_TRIGGERS,
    F_PIPE_22_TRIGGERS,
    JUDGE_SUBPROCESS_TIMEOUT_MS,
    MAX_CALIBRATION_AGE_DAYS,
    MAX_REVISION_ITERATIONS,
    OPERATOR_INTERRUPT_POLL_INTERVAL_MS,
    RATE_LIMIT_JITTER_RANGE_MS,
    RATE_LIMIT_LEASE_TTL_SEC,
    RUNSTATE_SCHEMA_VERSION,
    RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED,
    SCRIBE_SUBPROCESS_TIMEOUT_MS,
    SUBMISSION_MODE_FORBIDDEN_INTENTS,
    TAB_ORDERING,
)


class TestBlueprintPins:
    def test_blueprint_deps_present(self):
        assert "section_05_pipeline.md" in BLUEPRINT_DEPS
        assert BLUEPRINT_DEPS["section_05_pipeline.md"]["version"] == "v6"
        assert (
            BLUEPRINT_DEPS["section_05_pipeline.md"]["hash_sha3_512_prefix16"]
            == "feb5928491e4dc40"
        )

    def test_blueprint_deps_amendment_pinned(self):
        assert "section_05_v6_amendment.md" in BLUEPRINT_DEPS
        assert (
            BLUEPRINT_DEPS["section_05_v6_amendment.md"]["hash_sha3_512_prefix16"]
            == "52ae6b3b97b159b5"
        )


class TestTabOrdering:
    def test_exact_value(self):
        assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft")

    def test_len(self):
        assert len(TAB_ORDERING) == 3


class TestSchemaVersion:
    def test_runstate_schema_version(self):
        assert RUNSTATE_SCHEMA_VERSION == 2

    def test_legacy_rejected(self):
        assert RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED == frozenset({1})

    def test_calibration_report_schema_version(self):
        assert CALIBRATION_REPORT_SCHEMA_VERSION == 1


class TestEd25519Algorithm:
    def test_signing_algorithm(self):
        assert CALIBRATION_SIGNING_ALGORITHM == "Ed25519"


class TestAgeWindow:
    def test_max_calibration_age_days(self):
        assert MAX_CALIBRATION_AGE_DAYS == 90


class TestIntentSets:
    def test_eval_mode_allowed_intents(self):
        assert EVAL_MODE_ALLOWED_INTENTS == frozenset(
            {"golden-set-write", "state-success", "state-failure"}
        )

    def test_submission_mode_forbidden_intents(self):
        assert SUBMISSION_MODE_FORBIDDEN_INTENTS == frozenset(
            {"golden-set-read", "golden-set-write"}
        )

    def test_eval_allowed_and_submission_forbidden_overlap(self):
        # golden-set-write appears in both: allowed under eval, forbidden
        # under submission. This is the invariant that makes mode-isolation
        # a useful predicate.
        assert "golden-set-write" in EVAL_MODE_ALLOWED_INTENTS
        assert "golden-set-write" in SUBMISSION_MODE_FORBIDDEN_INTENTS


class TestScalarConstants:
    def test_checkpoint_backoff_schedule(self):
        assert CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS == (50, 200, 800)

    def test_checkpoint_total_timeout(self):
        assert CHECKPOINT_TOTAL_TIMEOUT_SEC == 10

    def test_cron_retry_window(self):
        assert CRON_VAULT_RETRY_WINDOW_SEC == 300

    def test_cron_retry_attempts(self):
        assert CRON_VAULT_RETRY_ATTEMPTS == 6

    def test_rate_limit_jitter_range(self):
        assert RATE_LIMIT_JITTER_RANGE_MS == (0, 300)

    def test_rate_limit_lease_ttl(self):
        assert RATE_LIMIT_LEASE_TTL_SEC == 30

    def test_cron_stamp_ttl_hours(self):
        assert CRON_STAMP_TTL_HOURS == 36

    def test_seat_timeouts(self):
        assert SCRIBE_SUBPROCESS_TIMEOUT_MS == 300_000
        assert EDITOR_SUBPROCESS_TIMEOUT_MS == 180_000
        assert JUDGE_SUBPROCESS_TIMEOUT_MS == 180_000

    def test_operator_interrupt_poll_interval(self):
        assert OPERATOR_INTERRUPT_POLL_INTERVAL_MS == 500

    def test_max_revision_iterations(self):
        assert MAX_REVISION_ITERATIONS == 3


class TestPathTemplates:
    def test_calibration_report_path_tmpl(self):
        assert CALIBRATION_REPORT_PATH_TMPL == (
            "{org_slug}/golden_set/calibration_reports/{run_id}.json"
        )

    def test_calibration_signature_path_tmpl(self):
        assert CALIBRATION_SIGNATURE_PATH_TMPL == (
            "{org_slug}/golden_set/calibration_reports/{run_id}.sig"
        )

    def test_bypass_pending_path_tmpl(self):
        assert BYPASS_PENDING_CHECKPOINT_PATH_TMPL == (
            "pipeline/{run_id}/bypass_pending.json"
        )

    def test_path_tmpls_format_correctly(self):
        # A round-trip: format with known substitutions → compare substring.
        assert CALIBRATION_REPORT_PATH_TMPL.format(
            org_slug="mycosymbiotics_cooperative", run_id="abc"
        ) == "mycosymbiotics_cooperative/golden_set/calibration_reports/abc.json"


class TestFPipeTriggers:
    def test_f_pipe_21_trigger_count(self):
        # v6 line 1052 enumerates exactly 15 sub-triggers.
        assert len(F_PIPE_21_TRIGGERS) == 15

    def test_f_pipe_21_trigger_canonical_values(self):
        # Exhaustive list from blueprint §6 v6 line 1052. This locks the set
        # so a silent addition/removal is a test failure.
        assert F_PIPE_21_TRIGGERS == frozenset(
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

    def test_f_pipe_22_trigger_count(self):
        assert len(F_PIPE_22_TRIGGERS) == 2

    def test_f_pipe_22_trigger_canonical_values(self):
        assert F_PIPE_22_TRIGGERS == frozenset(
            {
                "runstate_schema_downgrade",
                "calibration_report_schema_mismatch",
            }
        )


class TestModuleAttrSurface:
    def test_module_is_importable_and_public_names_present(self):
        # Sanity: every constant documented in the spec card is importable
        # at module top-level.
        for name in [
            "TAB_ORDERING",
            "RUNSTATE_SCHEMA_VERSION",
            "RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED",
            "CALIBRATION_REPORT_SCHEMA_VERSION",
            "CALIBRATION_SIGNING_ALGORITHM",
            "MAX_CALIBRATION_AGE_DAYS",
            "EVAL_MODE_ALLOWED_INTENTS",
            "SUBMISSION_MODE_FORBIDDEN_INTENTS",
            "CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS",
            "CHECKPOINT_TOTAL_TIMEOUT_SEC",
            "CRON_VAULT_RETRY_WINDOW_SEC",
            "CRON_VAULT_RETRY_ATTEMPTS",
            "RATE_LIMIT_JITTER_RANGE_MS",
            "RATE_LIMIT_LEASE_TTL_SEC",
            "CRON_STAMP_TTL_HOURS",
            "SCRIBE_SUBPROCESS_TIMEOUT_MS",
            "EDITOR_SUBPROCESS_TIMEOUT_MS",
            "JUDGE_SUBPROCESS_TIMEOUT_MS",
            "OPERATOR_INTERRUPT_POLL_INTERVAL_MS",
            "MAX_REVISION_ITERATIONS",
            "CALIBRATION_REPORT_PATH_TMPL",
            "CALIBRATION_SIGNATURE_PATH_TMPL",
            "BYPASS_PENDING_CHECKPOINT_PATH_TMPL",
            "F_PIPE_21_TRIGGERS",
            "F_PIPE_22_TRIGGERS",
            "BLUEPRINT_DEPS",
        ]:
            assert hasattr(cfg, name), f"pipeline.loop.config missing {name}"
