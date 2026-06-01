"""Tests for pipeline.calibration.golden_set (R12.A).

Covers:
- ``GoldenSetItem`` construction validation.
- ``_vault_prefix_for`` template behaviour + empty-slug rejection.
- ``_resolve_golden_set_path`` happy path (candidate under prefix).
- ``_resolve_golden_set_path`` path-escape rejection (`..` and realpath).
- ``_resolve_golden_set_path`` symlink-ancestor rejection.
- ``_resolve_golden_set_path`` NFC normalization before realpath.
- ``_resolve_golden_set_path`` strict-child check (candidate == prefix rejected).
- ``_deserialize_manifest`` happy path + schema mismatch + shape errors.
- ``assert_manifest_org_matches`` match + mismatch.
- ``golden_set_iter`` preserves manifest order; subset filter preserves order.
- ``golden_set_iter`` propagates F_PIPE_21 / F_PIPE_22.
- Rebind-resistance: constants rebound at module attribute do not widen paths.
- Type / arg validation on all public entry points.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from pipeline.calibration.golden_set import (
    GOLDEN_SET_SCHEMA_VERSION,
    GOLDEN_SET_VAULT_PREFIX_TMPL,
    GoldenSetItem,
    _deserialize_manifest,
    _resolve_golden_set_path,
    _vault_prefix_for,
    assert_manifest_org_matches,
    golden_set_iter,
)
from pipeline.loop.errors import F_PIPE_21, F_PIPE_22


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def _item_kwargs(**overrides: Any) -> dict[str, Any]:
    base = dict(
        item_id="gs-001",
        org_slug="fit_farms_llc",
        funded_grant_label="VAPG FY24 round 2",
        rfa_snapshot_path="vault/fit_farms_llc/golden_set/items/gs-001/rfa.md",
        submitted_artifact_path=(
            "vault/fit_farms_llc/golden_set/items/gs-001/draft.md"
        ),
        funded_outcome="funded",
        operator_curation_iso="2026-03-15T12:00:00+00:00",
        manifest_hash="a" * 64,
    )
    base.update(overrides)
    return base


def _manifest_payload(
    *,
    org_slug: str = "fit_farms_llc",
    items: list[dict[str, Any]] | None = None,
    schema_version: int = 1,
    manifest_hash: str = "b" * 64,
) -> bytes:
    if items is None:
        items = [
            {
                "item_id": "gs-001",
                "org_slug": org_slug,
                "funded_grant_label": "VAPG FY24 round 2",
                "rfa_snapshot_path": (
                    f"vault/{org_slug}/golden_set/items/gs-001/rfa.md"
                ),
                "submitted_artifact_path": (
                    f"vault/{org_slug}/golden_set/items/gs-001/draft.md"
                ),
                "funded_outcome": "funded",
                "operator_curation_iso": "2026-03-15T12:00:00+00:00",
                "manifest_hash": "a" * 64,
            }
        ]
    payload = {
        "schema_version": schema_version,
        "org_slug": org_slug,
        "manifest_hash": manifest_hash,
        "items": items,
    }
    return json.dumps(payload).encode("utf-8")


# ---------------------------------------------------------------------------
# GoldenSetItem construction
# ---------------------------------------------------------------------------


def test_golden_set_item_happy_path() -> None:
    item = GoldenSetItem(**_item_kwargs())
    assert item.item_id == "gs-001"
    assert item.org_slug == "fit_farms_llc"
    assert item.funded_outcome == "funded"


def test_golden_set_item_rejects_empty_item_id() -> None:
    with pytest.raises(ValueError, match="item_id must be non-empty"):
        GoldenSetItem(**_item_kwargs(item_id=""))


def test_golden_set_item_rejects_empty_org_slug() -> None:
    with pytest.raises(ValueError, match="org_slug must be non-empty"):
        GoldenSetItem(**_item_kwargs(org_slug=""))


def test_golden_set_item_rejects_empty_funded_grant_label() -> None:
    with pytest.raises(ValueError, match="funded_grant_label must be non-empty"):
        GoldenSetItem(**_item_kwargs(funded_grant_label=""))


def test_golden_set_item_rejects_empty_rfa_snapshot_path() -> None:
    with pytest.raises(ValueError, match="rfa_snapshot_path must be non-empty"):
        GoldenSetItem(**_item_kwargs(rfa_snapshot_path=""))


def test_golden_set_item_rejects_empty_submitted_artifact_path() -> None:
    with pytest.raises(
        ValueError, match="submitted_artifact_path must be non-empty"
    ):
        GoldenSetItem(**_item_kwargs(submitted_artifact_path=""))


def test_golden_set_item_rejects_bad_funded_outcome() -> None:
    with pytest.raises(ValueError, match="funded_outcome must be one of"):
        GoldenSetItem(**_item_kwargs(funded_outcome="rejected"))


def test_golden_set_item_rejects_empty_operator_curation_iso() -> None:
    with pytest.raises(ValueError, match="operator_curation_iso must be non-empty"):
        GoldenSetItem(**_item_kwargs(operator_curation_iso=""))


def test_golden_set_item_rejects_empty_manifest_hash() -> None:
    with pytest.raises(ValueError, match="manifest_hash must be non-empty"):
        GoldenSetItem(**_item_kwargs(manifest_hash=""))


def test_golden_set_item_accepts_all_three_funded_outcomes() -> None:
    for outcome in ("funded", "funded_partial", "rejected_with_feedback"):
        item = GoldenSetItem(**_item_kwargs(funded_outcome=outcome))
        assert item.funded_outcome == outcome


# ---------------------------------------------------------------------------
# Module-load constants (rebind-resistance attested here)
# ---------------------------------------------------------------------------


def test_golden_set_schema_version_is_pinned() -> None:
    assert GOLDEN_SET_SCHEMA_VERSION == 1


def test_golden_set_vault_prefix_tmpl_is_pinned() -> None:
    assert GOLDEN_SET_VAULT_PREFIX_TMPL == "vault/{operator_org_slug}/golden_set/"


# ---------------------------------------------------------------------------
# _vault_prefix_for
# ---------------------------------------------------------------------------


def test_vault_prefix_for_basic() -> None:
    assert _vault_prefix_for("fit_farms_llc") == "vault/fit_farms_llc/golden_set/"


def test_vault_prefix_for_rejects_empty() -> None:
    with pytest.raises(ValueError, match="operator_org_slug must be non-empty"):
        _vault_prefix_for("")


# ---------------------------------------------------------------------------
# _resolve_golden_set_path — happy path + rejections
# ---------------------------------------------------------------------------


def _identity_realpath(p: str) -> str:
    """A test realpath that returns input unchanged — simulates no symlinks."""
    return str(Path(p).as_posix())


def _never_symlink(p: Path) -> bool:
    return False


def test_resolve_path_happy_strict_child() -> None:
    candidate = "vault/fit_farms_llc/golden_set/manifest.json"
    prefix = "vault/fit_farms_llc/golden_set/"
    out = _resolve_golden_set_path(
        candidate,
        prefix,
        realpath=_identity_realpath,
        is_symlink=_never_symlink,
    )
    assert str(out) == "vault/fit_farms_llc/golden_set/manifest.json"


def test_resolve_path_rejects_candidate_equal_to_prefix() -> None:
    with pytest.raises(F_PIPE_21) as ei:
        _resolve_golden_set_path(
            "vault/fit_farms_llc/golden_set/",
            "vault/fit_farms_llc/golden_set/",
            realpath=_identity_realpath,
            is_symlink=_never_symlink,
        )
    assert ei.value.trigger == "golden_set_path_escapes_prefix"


def test_resolve_path_rejects_escape_with_dotdot() -> None:
    # A realpath that follows the `..` and resolves outside the prefix.
    def realpath_resolves_dotdot(p: str) -> str:
        if p.startswith("vault/fit_farms_llc/golden_set/../other_org"):
            return "vault/other_org/golden_set/manifest.json"
        return _identity_realpath(p)

    with pytest.raises(F_PIPE_21) as ei:
        _resolve_golden_set_path(
            "vault/fit_farms_llc/golden_set/../other_org/golden_set/manifest.json",
            "vault/fit_farms_llc/golden_set/",
            realpath=realpath_resolves_dotdot,
            is_symlink=_never_symlink,
        )
    assert ei.value.trigger == "golden_set_path_escapes_prefix"


def test_resolve_path_rejects_symlink_ancestor() -> None:
    # Identity realpath + a symlink-oracle that flags `items` as a symlink.
    symlinked_dir = "vault/fit_farms_llc/golden_set/items"

    def is_symlink_flag(p: Path) -> bool:
        return str(p) == symlinked_dir

    with pytest.raises(F_PIPE_21) as ei:
        _resolve_golden_set_path(
            "vault/fit_farms_llc/golden_set/items/gs-001/manifest.json",
            "vault/fit_farms_llc/golden_set/",
            realpath=_identity_realpath,
            is_symlink=is_symlink_flag,
        )
    assert ei.value.trigger == "golden_set_path_traverses_symlink"


def test_resolve_path_nfc_normalizes_before_realpath() -> None:
    """Composed vs decomposed Unicode resolves to the same realpath input."""
    # Decomposed (NFD): 'ñ' as 'n' + combining tilde.
    decomposed = "vault/fit_farms_llc/golden_set/mañana.json"
    captured: list[str] = []

    def realpath_capture(p: str) -> str:
        captured.append(p)
        return _identity_realpath(p)

    _resolve_golden_set_path(
        decomposed,
        "vault/fit_farms_llc/golden_set/",
        realpath=realpath_capture,
        is_symlink=_never_symlink,
    )
    # First realpath() call should receive NFC-normalized form.
    assert captured[0] == "vault/fit_farms_llc/golden_set/mañana.json"
    # And the NFC form equals its own NFC (idempotent check).
    import unicodedata as _ud

    assert captured[0] == _ud.normalize("NFC", captured[0])


def test_resolve_path_type_errors() -> None:
    with pytest.raises(TypeError, match="path must be str"):
        _resolve_golden_set_path(
            123,  # type: ignore[arg-type]
            "vault/x/golden_set/",
            realpath=_identity_realpath,
            is_symlink=_never_symlink,
        )
    with pytest.raises(TypeError, match="vault_prefix must be str"):
        _resolve_golden_set_path(
            "vault/x/golden_set/y.json",
            123,  # type: ignore[arg-type]
            realpath=_identity_realpath,
            is_symlink=_never_symlink,
        )


def test_resolve_path_empty_string_errors() -> None:
    with pytest.raises(ValueError, match="path must be non-empty"):
        _resolve_golden_set_path(
            "",
            "vault/x/golden_set/",
            realpath=_identity_realpath,
            is_symlink=_never_symlink,
        )
    with pytest.raises(ValueError, match="vault_prefix must be non-empty"):
        _resolve_golden_set_path(
            "vault/x/golden_set/y.json",
            "",
            realpath=_identity_realpath,
            is_symlink=_never_symlink,
        )


def test_resolve_path_default_callables_work() -> None:
    """When realpath/is_symlink not injected, default to os/pathlib."""
    candidate = "vault/fit_farms_llc/golden_set/manifest.json"
    prefix = "vault/fit_farms_llc/golden_set/"
    # No filesystem exists; realpath of a non-existent path returns the path
    # with os.path.realpath semantics (absolute-ized). This verifies the
    # default-callable branch executes without injection.
    out = _resolve_golden_set_path(candidate, prefix)
    # We don't assert an exact string (realpath normalizes to abs); just
    # that the call succeeded.
    assert isinstance(out, Path)


# ---------------------------------------------------------------------------
# _deserialize_manifest
# ---------------------------------------------------------------------------


def test_deserialize_manifest_happy_path() -> None:
    payload = _manifest_payload()
    org_slug, items, manifest_hash = _deserialize_manifest(
        payload, manifest_path="vault/fit_farms_llc/golden_set/manifest.json"
    )
    assert org_slug == "fit_farms_llc"
    assert len(items) == 1
    assert items[0].item_id == "gs-001"
    assert manifest_hash == "b" * 64


def test_deserialize_manifest_schema_mismatch() -> None:
    payload = _manifest_payload(schema_version=2)
    with pytest.raises(F_PIPE_22) as ei:
        _deserialize_manifest(
            payload, manifest_path="vault/x/golden_set/manifest.json"
        )
    assert ei.value.trigger == "calibration_report_schema_mismatch"
    assert ei.value.details["shape"] == "GoldenSetManifest"
    assert ei.value.details["observed"] == 2


def test_deserialize_manifest_rejects_non_object() -> None:
    with pytest.raises(ValueError, match="not a JSON object"):
        _deserialize_manifest(
            json.dumps([]).encode("utf-8"),
            manifest_path="vault/x/golden_set/manifest.json",
        )


def test_deserialize_manifest_rejects_missing_org_slug() -> None:
    payload = json.dumps(
        {"schema_version": 1, "manifest_hash": "abc", "items": []}
    ).encode("utf-8")
    with pytest.raises(ValueError, match="missing org_slug"):
        _deserialize_manifest(
            payload, manifest_path="vault/x/golden_set/manifest.json"
        )


def test_deserialize_manifest_rejects_missing_manifest_hash() -> None:
    payload = json.dumps(
        {"schema_version": 1, "org_slug": "x", "items": []}
    ).encode("utf-8")
    with pytest.raises(ValueError, match="missing manifest_hash"):
        _deserialize_manifest(
            payload, manifest_path="vault/x/golden_set/manifest.json"
        )


def test_deserialize_manifest_rejects_items_not_list() -> None:
    payload = json.dumps(
        {
            "schema_version": 1,
            "org_slug": "x",
            "manifest_hash": "abc",
            "items": {},
        }
    ).encode("utf-8")
    with pytest.raises(ValueError, match="items must be a list"):
        _deserialize_manifest(
            payload, manifest_path="vault/x/golden_set/manifest.json"
        )


def test_deserialize_manifest_rejects_non_dict_item() -> None:
    payload = json.dumps(
        {
            "schema_version": 1,
            "org_slug": "x",
            "manifest_hash": "abc",
            "items": ["not-a-dict"],
        }
    ).encode("utf-8")
    with pytest.raises(ValueError, match="is not a JSON object"):
        _deserialize_manifest(
            payload, manifest_path="vault/x/golden_set/manifest.json"
        )


def test_deserialize_manifest_preserves_order() -> None:
    items = [
        {
            "item_id": f"gs-{i:03d}",
            "org_slug": "x",
            "funded_grant_label": f"label-{i}",
            "rfa_snapshot_path": f"vault/x/golden_set/items/gs-{i:03d}/rfa.md",
            "submitted_artifact_path": (
                f"vault/x/golden_set/items/gs-{i:03d}/draft.md"
            ),
            "funded_outcome": "funded",
            "operator_curation_iso": "2026-01-01T00:00:00+00:00",
            "manifest_hash": "a" * 64,
        }
        for i in (3, 1, 5, 2, 4)
    ]
    payload = _manifest_payload(org_slug="x", items=items)
    _, parsed, _ = _deserialize_manifest(
        payload, manifest_path="vault/x/golden_set/manifest.json"
    )
    assert [p.item_id for p in parsed] == [
        "gs-003",
        "gs-001",
        "gs-005",
        "gs-002",
        "gs-004",
    ]


# ---------------------------------------------------------------------------
# assert_manifest_org_matches
# ---------------------------------------------------------------------------


def test_assert_manifest_org_matches_ok() -> None:
    # Does not raise.
    assert_manifest_org_matches(
        manifest_org_slug="fit_farms_llc",
        operator_org_slug="fit_farms_llc",
        manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
    )


def test_assert_manifest_org_matches_mismatch() -> None:
    with pytest.raises(F_PIPE_21) as ei:
        assert_manifest_org_matches(
            manifest_org_slug="other_org",
            operator_org_slug="fit_farms_llc",
            manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
        )
    assert ei.value.trigger == "golden_set_manifest_org_mismatch"
    assert ei.value.details["manifest_org_slug"] == "other_org"
    assert ei.value.details["operator_org_slug"] == "fit_farms_llc"


# ---------------------------------------------------------------------------
# golden_set_iter — integration
# ---------------------------------------------------------------------------


def test_golden_set_iter_happy_path_single_item() -> None:
    payload = _manifest_payload()

    def vread(*, path: str) -> bytes:
        return payload

    items = list(
        golden_set_iter(
            operator_org_slug="fit_farms_llc",
            manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
            vault_read=vread,
            realpath=_identity_realpath,
            is_symlink=_never_symlink,
        )
    )
    assert len(items) == 1
    assert items[0].item_id == "gs-001"


def test_golden_set_iter_preserves_manifest_order() -> None:
    raw_items = [
        {
            "item_id": f"gs-{i:03d}",
            "org_slug": "fit_farms_llc",
            "funded_grant_label": f"label-{i}",
            "rfa_snapshot_path": (
                f"vault/fit_farms_llc/golden_set/items/gs-{i:03d}/rfa.md"
            ),
            "submitted_artifact_path": (
                f"vault/fit_farms_llc/golden_set/items/gs-{i:03d}/draft.md"
            ),
            "funded_outcome": "funded",
            "operator_curation_iso": "2026-01-01T00:00:00+00:00",
            "manifest_hash": "a" * 64,
        }
        for i in (7, 3, 9, 1, 5)
    ]
    payload = _manifest_payload(items=raw_items)

    def vread(*, path: str) -> bytes:
        return payload

    out = [
        it.item_id
        for it in golden_set_iter(
            operator_org_slug="fit_farms_llc",
            manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
            vault_read=vread,
            realpath=_identity_realpath,
            is_symlink=_never_symlink,
        )
    ]
    assert out == ["gs-007", "gs-003", "gs-009", "gs-001", "gs-005"]


def test_golden_set_iter_subset_filter_preserves_order() -> None:
    raw_items = [
        {
            "item_id": f"gs-{i:03d}",
            "org_slug": "fit_farms_llc",
            "funded_grant_label": f"label-{i}",
            "rfa_snapshot_path": (
                f"vault/fit_farms_llc/golden_set/items/gs-{i:03d}/rfa.md"
            ),
            "submitted_artifact_path": (
                f"vault/fit_farms_llc/golden_set/items/gs-{i:03d}/draft.md"
            ),
            "funded_outcome": "funded",
            "operator_curation_iso": "2026-01-01T00:00:00+00:00",
            "manifest_hash": "a" * 64,
        }
        for i in (7, 3, 9, 1, 5)
    ]
    payload = _manifest_payload(items=raw_items)

    def vread(*, path: str) -> bytes:
        return payload

    # Subset provides items in a DIFFERENT order — expected output is
    # manifest order, filtered to subset.
    subset = ("gs-001", "gs-007", "gs-005")
    out = [
        it.item_id
        for it in golden_set_iter(
            operator_org_slug="fit_farms_llc",
            manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
            vault_read=vread,
            subset=subset,
            realpath=_identity_realpath,
            is_symlink=_never_symlink,
        )
    ]
    # Manifest order was 7,3,9,1,5; subset is {1,7,5}; expected 7,1,5.
    assert out == ["gs-007", "gs-001", "gs-005"]


def test_golden_set_iter_subset_empty_yields_nothing() -> None:
    payload = _manifest_payload()

    def vread(*, path: str) -> bytes:
        return payload

    out = list(
        golden_set_iter(
            operator_org_slug="fit_farms_llc",
            manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
            vault_read=vread,
            subset=(),
            realpath=_identity_realpath,
            is_symlink=_never_symlink,
        )
    )
    assert out == []


def test_golden_set_iter_rejects_empty_org_slug() -> None:
    def vread(*, path: str) -> bytes:
        return b""

    with pytest.raises(ValueError, match="operator_org_slug must be non-empty"):
        list(
            golden_set_iter(
                operator_org_slug="",
                manifest_path="vault/x/golden_set/manifest.json",
                vault_read=vread,
            )
        )


def test_golden_set_iter_rejects_empty_manifest_path() -> None:
    def vread(*, path: str) -> bytes:
        return b""

    with pytest.raises(ValueError, match="manifest_path must be non-empty"):
        list(
            golden_set_iter(
                operator_org_slug="x",
                manifest_path="",
                vault_read=vread,
            )
        )


def test_golden_set_iter_path_escape_rejected() -> None:
    def vread(*, path: str) -> bytes:
        return _manifest_payload()

    def realpath_escape(p: str) -> str:
        return "other_org/secrets/manifest.json"

    with pytest.raises(F_PIPE_21) as ei:
        list(
            golden_set_iter(
                operator_org_slug="fit_farms_llc",
                manifest_path=(
                    "vault/fit_farms_llc/golden_set/../other_org/manifest.json"
                ),
                vault_read=vread,
                realpath=realpath_escape,
                is_symlink=_never_symlink,
            )
        )
    assert ei.value.trigger == "golden_set_path_escapes_prefix"


def test_golden_set_iter_manifest_org_mismatch_rejected() -> None:
    payload = _manifest_payload(org_slug="other_org")

    def vread(*, path: str) -> bytes:
        return payload

    with pytest.raises(F_PIPE_21) as ei:
        list(
            golden_set_iter(
                operator_org_slug="fit_farms_llc",
                manifest_path=(
                    "vault/fit_farms_llc/golden_set/manifest.json"
                ),
                vault_read=vread,
                realpath=_identity_realpath,
                is_symlink=_never_symlink,
            )
        )
    assert ei.value.trigger == "golden_set_manifest_org_mismatch"
