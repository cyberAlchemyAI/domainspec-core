"""Tests for ``pipeline.cli.tilth_migrate_beneficiary_records`` +
``pipeline.orchestrator.migrations.beneficiary_records_history``.

Per WS-J Slice 2 (2026-05-11) + §13 v1 RT-C2-06 closure. Coverage:

* Empty-history back-fill happy path.
* Already-populated → fail-closed without ``--force``.
* ``--force`` → no-op with audit log entry recording the no-op.
* Audit-log append: one JSONL row per migrated record.
* End-to-end CLI invocation against a synthetic legacy fixture.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from pipeline.cli.tilth_migrate_beneficiary_records import main as cli_main
from pipeline.orchestrator.migrations.beneficiary_records_history import (
    MigrationAlreadyApplied,
    MigrationScanError,
    STATUS_ALREADY_APPLIED,
    STATUS_BACKFILLED,
    run_beneficiary_records_history_migration,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def operator_key_files(tmp_path):
    """Generate an operator Ed25519 keypair on disk."""
    private = ed25519.Ed25519PrivateKey.generate()
    private_bytes = private.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_bytes = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    key_path = tmp_path / "op_ed25519.key"
    pub_path = tmp_path / "op_ed25519.pub"
    key_path.write_bytes(private_bytes)
    pub_path.write_bytes(public_bytes)
    return key_path, pub_path


@pytest.fixture
def synthetic_legacy_repo(tmp_path):
    """Build a synthetic orgs/<slug>/vault/operational/grants/<id>/period_*
    subtree with pre-§13 v1 beneficiary_records (no consent_tier_history).
    """
    repo = tmp_path / "repo"
    grant_root = (
        repo / "orgs" / "myorg" / "vault" / "operational" / "grants" / "G1"
    )
    period_dir = grant_root / "period_1" / "beneficiary_records"
    period_dir.mkdir(parents=True)
    for i in range(3):
        rec = {
            "record_id": f"BR-{i:03d}",
            "beneficiary_opaque_id": f"OP-{i:03d}",
            "service": "workshop",
            "outcome": "completed",
            "consent_tier": "anonymized",
            "pii_present": False,
            "pii_fields": [],
            "captured_at": f"2026-04-{15 + i:02d}T10:00:00Z",
            "created_at_utc": f"2026-04-{15 + i:02d}T10:00:00Z",
        }
        (period_dir / f"BR-{i:03d}.yaml").write_text(
            yaml.safe_dump(rec, sort_keys=True), encoding="utf-8"
        )
    return repo


def _make_signer(key_path):
    raw = key_path.read_bytes()
    private = ed25519.Ed25519PrivateKey.from_private_bytes(raw)

    def _sign(message_bytes: bytes) -> bytes:
        return private.sign(message_bytes)

    return _sign


# ---------------------------------------------------------------------------
# Orchestrator-level tests
# ---------------------------------------------------------------------------


class TestMigrationOrchestrator:
    def test_empty_history_backfill(
        self, synthetic_legacy_repo, operator_key_files
    ):
        key_path, _ = operator_key_files
        signer = _make_signer(key_path)
        result = run_beneficiary_records_history_migration(
            repo_root=synthetic_legacy_repo,
            org_slug="myorg",
            grant_id="G1",
            operator_signer=signer,
            operator_key_id="op-001",
            invoked_at_utc="2026-05-11T12:00:00Z",
            backfill_empty_history=True,
            force=False,
        )
        assert result.records_scanned == 3
        assert result.records_backfilled == 3
        assert result.records_already_applied == 0
        assert result.records_errored == 0

        # Verify each record now has consent_tier_history.
        for i in range(3):
            path = (
                synthetic_legacy_repo
                / "orgs/myorg/vault/operational/grants/G1/period_1/beneficiary_records"
                / f"BR-{i:03d}.yaml"
            )
            content = yaml.safe_load(path.read_text(encoding="utf-8"))
            assert "consent_tier_history" in content
            history = content["consent_tier_history"]
            assert isinstance(history, list)
            assert len(history) == 1
            event = history[0]
            assert event["kind"] == "initial"
            assert event["tier"] == "anonymized"
            assert "set_by_operator_signature" in event

    def test_already_populated_fail_closed_without_force(
        self, synthetic_legacy_repo, operator_key_files
    ):
        key_path, _ = operator_key_files
        signer = _make_signer(key_path)
        # First run.
        run_beneficiary_records_history_migration(
            repo_root=synthetic_legacy_repo,
            org_slug="myorg",
            grant_id="G1",
            operator_signer=signer,
            operator_key_id="op-001",
            invoked_at_utc="2026-05-11T12:00:00Z",
            backfill_empty_history=True,
            force=False,
        )
        # Second run without --force → MigrationAlreadyApplied.
        with pytest.raises(MigrationAlreadyApplied):
            run_beneficiary_records_history_migration(
                repo_root=synthetic_legacy_repo,
                org_slug="myorg",
                grant_id="G1",
                operator_signer=signer,
                operator_key_id="op-001",
                invoked_at_utc="2026-05-11T12:05:00Z",
                backfill_empty_history=True,
                force=False,
            )

    def test_force_allows_noop_rerun(
        self, synthetic_legacy_repo, operator_key_files
    ):
        key_path, _ = operator_key_files
        signer = _make_signer(key_path)
        run_beneficiary_records_history_migration(
            repo_root=synthetic_legacy_repo,
            org_slug="myorg",
            grant_id="G1",
            operator_signer=signer,
            operator_key_id="op-001",
            invoked_at_utc="2026-05-11T12:00:00Z",
            backfill_empty_history=True,
            force=False,
        )
        # Second run with --force succeeds; status reflects already_applied.
        result2 = run_beneficiary_records_history_migration(
            repo_root=synthetic_legacy_repo,
            org_slug="myorg",
            grant_id="G1",
            operator_signer=signer,
            operator_key_id="op-001",
            invoked_at_utc="2026-05-11T12:05:00Z",
            backfill_empty_history=True,
            force=True,
        )
        assert result2.records_backfilled == 0
        assert result2.records_already_applied == 3

    def test_audit_log_append(
        self, synthetic_legacy_repo, operator_key_files
    ):
        key_path, _ = operator_key_files
        signer = _make_signer(key_path)
        result = run_beneficiary_records_history_migration(
            repo_root=synthetic_legacy_repo,
            org_slug="myorg",
            grant_id="G1",
            operator_signer=signer,
            operator_key_id="op-001",
            invoked_at_utc="2026-05-11T12:00:00Z",
            backfill_empty_history=True,
            force=False,
        )
        audit_path = Path(result.audit_log_path)
        assert audit_path.is_file()
        lines = audit_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 3
        for line in lines:
            row = json.loads(line)
            assert row["org_slug"] == "myorg"
            assert row["grant_id"] == "G1"
            assert row["status"] == STATUS_BACKFILLED
            assert row["operator_key_id"] == "op-001"
            assert row["lock_class"] == "data_migration"
            assert row["migration_signature"] is not None

    def test_force_audit_log_records_already_applied(
        self, synthetic_legacy_repo, operator_key_files
    ):
        key_path, _ = operator_key_files
        signer = _make_signer(key_path)
        run_beneficiary_records_history_migration(
            repo_root=synthetic_legacy_repo,
            org_slug="myorg",
            grant_id="G1",
            operator_signer=signer,
            operator_key_id="op-001",
            invoked_at_utc="2026-05-11T12:00:00Z",
            backfill_empty_history=True,
            force=False,
        )
        run_beneficiary_records_history_migration(
            repo_root=synthetic_legacy_repo,
            org_slug="myorg",
            grant_id="G1",
            operator_signer=signer,
            operator_key_id="op-001",
            invoked_at_utc="2026-05-11T12:05:00Z",
            backfill_empty_history=True,
            force=True,
        )
        audit_path = (
            synthetic_legacy_repo
            / "orgs/myorg/vault/operational/grants/G1/migrations/lock_history.v1.jsonl"
        )
        lines = audit_path.read_text(encoding="utf-8").strip().split("\n")
        # First run wrote 3 backfill rows; second run wrote 3 already_applied rows.
        assert len(lines) == 6
        last_three = [json.loads(l) for l in lines[-3:]]
        for row in last_three:
            assert row["status"] == STATUS_ALREADY_APPLIED

    def test_scan_error_on_missing_grant_dir(
        self, tmp_path, operator_key_files
    ):
        key_path, _ = operator_key_files
        signer = _make_signer(key_path)
        with pytest.raises(MigrationScanError):
            run_beneficiary_records_history_migration(
                repo_root=tmp_path,
                org_slug="missing_org",
                grant_id="missing_grant",
                operator_signer=signer,
                operator_key_id="op-001",
                invoked_at_utc="2026-05-11T12:00:00Z",
            )


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------


class TestCLI:
    def test_cli_happy_path(
        self, synthetic_legacy_repo, operator_key_files, capsys
    ):
        key_path, _ = operator_key_files
        rc = cli_main(
            [
                "--org-slug",
                "myorg",
                "--grant-id",
                "G1",
                "--repo-root",
                str(synthetic_legacy_repo),
                "--signed-by",
                str(key_path),
                "--operator-key-id",
                "op-001",
                "--backfill-empty-history",
                "--json-output",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out.strip()
        result = json.loads(out)
        assert result["ok"] is True
        assert result["records_backfilled"] == 3

    def test_cli_fail_closed_already_applied(
        self, synthetic_legacy_repo, operator_key_files, capsys
    ):
        key_path, _ = operator_key_files
        cli_main(
            [
                "--org-slug",
                "myorg",
                "--grant-id",
                "G1",
                "--repo-root",
                str(synthetic_legacy_repo),
                "--signed-by",
                str(key_path),
                "--operator-key-id",
                "op-001",
                "--backfill-empty-history",
                "--json-output",
            ]
        )
        capsys.readouterr()  # drain first run
        rc = cli_main(
            [
                "--org-slug",
                "myorg",
                "--grant-id",
                "G1",
                "--repo-root",
                str(synthetic_legacy_repo),
                "--signed-by",
                str(key_path),
                "--operator-key-id",
                "op-001",
                "--backfill-empty-history",
                "--json-output",
            ]
        )
        assert rc == 1
        out = capsys.readouterr().out.strip()
        result = json.loads(out)
        assert result["ok"] is False
        assert result["code"] == "MIGRATION_ALREADY_APPLIED"

    def test_cli_force_succeeds_after_first_run(
        self, synthetic_legacy_repo, operator_key_files, capsys
    ):
        key_path, _ = operator_key_files
        cli_main(
            [
                "--org-slug",
                "myorg",
                "--grant-id",
                "G1",
                "--repo-root",
                str(synthetic_legacy_repo),
                "--signed-by",
                str(key_path),
                "--operator-key-id",
                "op-001",
                "--backfill-empty-history",
                "--json-output",
            ]
        )
        capsys.readouterr()
        rc = cli_main(
            [
                "--org-slug",
                "myorg",
                "--grant-id",
                "G1",
                "--repo-root",
                str(synthetic_legacy_repo),
                "--signed-by",
                str(key_path),
                "--operator-key-id",
                "op-001",
                "--backfill-empty-history",
                "--force",
                "--json-output",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out.strip()
        result = json.loads(out)
        assert result["ok"] is True
        assert result["records_already_applied"] == 3
        assert result["records_backfilled"] == 0

    def test_cli_scan_only_no_writes(
        self, synthetic_legacy_repo, operator_key_files, capsys
    ):
        key_path, _ = operator_key_files
        rc = cli_main(
            [
                "--org-slug",
                "myorg",
                "--grant-id",
                "G1",
                "--repo-root",
                str(synthetic_legacy_repo),
                "--signed-by",
                str(key_path),
                "--operator-key-id",
                "op-001",
                "--no-backfill-empty-history",
                "--json-output",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out.strip()
        result = json.loads(out)
        assert result["records_skipped_force_false"] == 3
        # Files unchanged.
        sample = (
            synthetic_legacy_repo
            / "orgs/myorg/vault/operational/grants/G1/period_1/beneficiary_records/BR-000.yaml"
        )
        content = yaml.safe_load(sample.read_text(encoding="utf-8"))
        assert "consent_tier_history" not in content
