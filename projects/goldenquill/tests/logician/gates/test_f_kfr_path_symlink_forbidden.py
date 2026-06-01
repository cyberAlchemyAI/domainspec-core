"""F-KFR-PATH-SYMLINK-FORBIDDEN tests (M1 §4.2.2)."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from pipeline.logician.gates.f_kfr_path_symlink_forbidden import (
    F_KFR_PATH_SYMLINK_FORBIDDEN,
    check_kfr_path_symlink_forbidden,
)


def test_failure_code_constant() -> None:
    assert F_KFR_PATH_SYMLINK_FORBIDDEN == "F-KFR-PATH-SYMLINK-FORBIDDEN"


def test_real_files_pass(tmp_path: Path) -> None:
    kfr = tmp_path / "kfr.yaml"
    kfr.write_text("fact_id: F1\n")
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_text("")
    r = check_kfr_path_symlink_forbidden(
        kfr_path=kfr, ledger_path=ledger
    )
    assert r.success is True


def test_kfr_symlink_fails(tmp_path: Path) -> None:
    real = tmp_path / "real.yaml"
    real.write_text("fact_id: F1\n")
    sym = tmp_path / "kfr.yaml"
    os.symlink(real, sym)
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_text("")
    r = check_kfr_path_symlink_forbidden(
        kfr_path=sym, ledger_path=ledger
    )
    assert r.success is False
    assert r.failure_code == F_KFR_PATH_SYMLINK_FORBIDDEN
    assert "kfr_path" in r.detail


def test_ledger_symlink_fails(tmp_path: Path) -> None:
    kfr = tmp_path / "kfr.yaml"
    kfr.write_text("fact_id: F1\n")
    real = tmp_path / "real.jsonl"
    real.write_text("")
    sym = tmp_path / "ledger.jsonl"
    os.symlink(real, sym)
    r = check_kfr_path_symlink_forbidden(
        kfr_path=kfr, ledger_path=sym
    )
    assert r.success is False
    assert r.failure_code == F_KFR_PATH_SYMLINK_FORBIDDEN
    assert "ledger_path" in r.detail
