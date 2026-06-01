"""F-KFR-YAML-CONSTRUCT-FORBIDDEN tests (M1 §2.4)."""

from __future__ import annotations

from pipeline.logician.gates.f_kfr_yaml_construct_forbidden import (
    F_KFR_YAML_CONSTRUCT_FORBIDDEN,
    check_kfr_yaml_construct_forbidden,
)


def test_failure_code_constant() -> None:
    assert F_KFR_YAML_CONSTRUCT_FORBIDDEN == "F-KFR-YAML-CONSTRUCT-FORBIDDEN"


def test_clean_kfr_passes() -> None:
    r = check_kfr_yaml_construct_forbidden(
        raw_bytes=b"fact_id: F1\nvalue: 100\n"
    )
    assert r.success is True
    assert r.failure_code is None
    assert r.parsed["fact_id"] == "F1"


def test_anchor_alias_pair_fails() -> None:
    r = check_kfr_yaml_construct_forbidden(
        raw_bytes=b"a: &foo bar\nb: *foo\n"
    )
    assert r.success is False
    assert r.failure_code == F_KFR_YAML_CONSTRUCT_FORBIDDEN


def test_merge_key_fails() -> None:
    r = check_kfr_yaml_construct_forbidden(
        raw_bytes=b"target:\n  <<: {x: 1}\n  z: 3\n"
    )
    assert r.success is False
    assert r.failure_code == F_KFR_YAML_CONSTRUCT_FORBIDDEN


def test_python_tag_fails() -> None:
    r = check_kfr_yaml_construct_forbidden(
        raw_bytes=b"value: !!python/object/apply:os.system ['ls']\n"
    )
    assert r.success is False
    assert r.failure_code == F_KFR_YAML_CONSTRUCT_FORBIDDEN
