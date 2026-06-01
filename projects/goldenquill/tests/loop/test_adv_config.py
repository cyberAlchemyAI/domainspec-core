"""Adversarial tests — V1-discipline module-load integrity for pipeline.loop.config.

Blueprint §5 v6 §8 LOCKED 2026-04-19. V1 closure + MA-07/MB-05/MA-11/MB-06.

Each test spawns a child Python process with a preloaded shim that rebinds a
rebind-sensitive constant, then attempts to import pipeline.loop.config. The
module-load assertion must fire, causing import to fail with AssertionError.
This proves that a compromised environment cannot silently substitute the
canonical value.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _run_child(script: str) -> subprocess.CompletedProcess[str]:
    """Run `script` in a fresh child Python process.

    The child inherits the repo root on sys.path so it can import
    pipeline.loop.config. It does NOT share module-cache state with the
    parent, so each scenario is a clean import attempt.
    """
    return subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        cwd=str(_REPO_ROOT),
    )


def _assert_import_blocked(script: str, expected_substring: str) -> None:
    """Assert the child's import attempt failed with AssertionError matching `expected_substring`."""
    r = _run_child(script)
    combined = r.stdout + r.stderr
    assert r.returncode != 0, (
        f"Expected child to fail but it exited 0.\nstdout={r.stdout}\nstderr={r.stderr}"
    )
    assert "AssertionError" in combined, (
        f"Expected AssertionError in child output.\nstdout={r.stdout}\nstderr={r.stderr}"
    )
    assert expected_substring in combined, (
        f"Expected substring {expected_substring!r} in child output.\n"
        f"stdout={r.stdout}\nstderr={r.stderr}"
    )


# ---------------------------------------------------------------------------
# Helpers: templates that load the module normally (baseline) or attempt a
# patched import (adversarial).
# ---------------------------------------------------------------------------


def _patch_template(attr: str, new_literal_repr: str) -> str:
    """Build a subprocess script that rebinds `attr` right before its assert.

    Strategy: read the config module source, find the module-load assert
    that guards `attr` (either ``assert {attr} ==`` for direct-form or
    ``assert len({attr})`` for frozenset-length form), and inject a rebind
    immediately before the assert. The assert then fires against the
    adversarial binding, proving the inline-literal RHS is rebind-resistant
    at import time. This works uniformly for single-line and multi-line
    literals because the injection happens after the definition completes,
    not in the middle of a literal.
    """
    return textwrap.dedent(
        f"""
        import sys, pathlib
        sys.path.insert(0, {str(_REPO_ROOT)!r})
        src = pathlib.Path({str(_REPO_ROOT / 'pipeline' / 'loop' / 'config.py')!r}).read_text()
        candidates = ['assert {attr} ==', 'assert len({attr})']
        idx = -1
        for cand in candidates:
            pos = src.find(cand)
            if pos >= 0:
                idx = pos
                break
        assert idx >= 0, 'no assert for {attr} found in config.py'
        patched = src[:idx] + '{attr} = {new_literal_repr}' + chr(10) + src[idx:]
        ns = {{'__name__': 'pipeline.loop.config_patched'}}
        exec(compile(patched, 'config_patched.py', 'exec'), ns)
        """
    ).strip()


class TestModuleLoadIntegrityAttacks:
    """Each test patches a rebind-sensitive constant and asserts import fails."""

    def test_tab_ordering_reorder_blocked(self):
        script = _patch_template(
            "TAB_ORDERING",
            '("deep_brief", "live_radar", "council_draft")',
        )
        _assert_import_blocked(script, "TAB_ORDERING has been rebound")

    def test_tab_ordering_rename_blocked(self):
        script = _patch_template(
            "TAB_ORDERING",
            '("live_radar", "deep_brief", "bogus")',
        )
        _assert_import_blocked(script, "TAB_ORDERING has been rebound")

    def test_runstate_schema_version_downgrade_blocked(self):
        script = _patch_template("RUNSTATE_SCHEMA_VERSION", "1")
        _assert_import_blocked(script, "RUNSTATE_SCHEMA_VERSION has been rebound")

    def test_runstate_schema_version_upgrade_blocked(self):
        script = _patch_template("RUNSTATE_SCHEMA_VERSION", "3")
        _assert_import_blocked(script, "RUNSTATE_SCHEMA_VERSION has been rebound")

    def test_calibration_signing_algorithm_change_blocked(self):
        script = _patch_template("CALIBRATION_SIGNING_ALGORITHM", '"MD5"')
        _assert_import_blocked(
            script, "CALIBRATION_SIGNING_ALGORITHM has been rebound"
        )

    def test_max_calibration_age_days_extended_blocked(self):
        script = _patch_template("MAX_CALIBRATION_AGE_DAYS", "99999")
        _assert_import_blocked(
            script, "MAX_CALIBRATION_AGE_DAYS has been rebound"
        )

    def test_max_calibration_age_days_zero_blocked(self):
        script = _patch_template("MAX_CALIBRATION_AGE_DAYS", "0")
        _assert_import_blocked(
            script, "MAX_CALIBRATION_AGE_DAYS has been rebound"
        )

    def test_eval_mode_allowed_intents_rebind_blocked(self):
        script = _patch_template(
            "EVAL_MODE_ALLOWED_INTENTS",
            'frozenset({"golden-set-read", "golden-set-write", "state-success", "state-failure"})',
        )
        _assert_import_blocked(
            script, "EVAL_MODE_ALLOWED_INTENTS has been rebound"
        )

    def test_submission_mode_forbidden_intents_rebind_blocked(self):
        script = _patch_template(
            "SUBMISSION_MODE_FORBIDDEN_INTENTS",
            'frozenset()',
        )
        _assert_import_blocked(
            script, "SUBMISSION_MODE_FORBIDDEN_INTENTS has been rebound"
        )

    def test_legacy_rejected_tampered_blocked(self):
        script = _patch_template(
            "RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED",
            "frozenset()",
        )
        _assert_import_blocked(
            script,
            "RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED has been rebound",
        )

    def test_calibration_report_schema_version_blocked(self):
        script = _patch_template("CALIBRATION_REPORT_SCHEMA_VERSION", "2")
        _assert_import_blocked(
            script, "CALIBRATION_REPORT_SCHEMA_VERSION has been rebound"
        )


class TestTriggerSetIntegrity:
    """F_PIPE_21_TRIGGERS + F_PIPE_22_TRIGGERS length asserts fire on rebind."""

    def test_f_pipe_21_triggers_added_blocked(self):
        # Rebind F_PIPE_21_TRIGGERS to a 16-element frozenset (rogue trigger
        # slipped in). The inline-literal ``len(...) == 15`` assert must fire.
        sixteen = (
            'frozenset({"mode_change_after_start", "eval_mode_has_tab_envelope_hash", '
            '"eval_mode_invalid_intent", "submission_mode_calibration_intent", '
            '"submission_mode_has_calibration_ref", "submission_mode_missing_rfa_hash", '
            '"submission_mode_missing_project_context_hash", "eval_mode_missing_golden_set_ref", '
            '"eval_mode_has_rfa_hash", "eval_mode_has_project_context_hash", '
            '"golden_set_path_escapes_prefix", "golden_set_path_traverses_symlink", '
            '"eval_run_reached_tab_delivery", "calibration_signature_stale", '
            '"golden_set_manifest_org_mismatch", "rogue_extra_trigger"})'
        )
        script = _patch_template("F_PIPE_21_TRIGGERS", sixteen)
        _assert_import_blocked(script, "F_PIPE_21_TRIGGERS has been rebound")

    def test_f_pipe_22_triggers_removed_blocked(self):
        # Rebind F_PIPE_22_TRIGGERS to a 1-element frozenset. The inline-literal
        # ``len(...) == 2`` assert must fire.
        script = _patch_template(
            "F_PIPE_22_TRIGGERS",
            'frozenset({"runstate_schema_downgrade"})',
        )
        _assert_import_blocked(script, "F_PIPE_22_TRIGGERS has been rebound")
