"""§4 Logician Round 5 — `dossier_verify.py` S11c + BT11."""

from __future__ import annotations

import dataclasses
import json

import pytest

from pipeline.logician import dossier_verify as dv
from pipeline.logician.dossier_verify import (
    CrossOrgVerifyResult,
    DossierCiteVerifyResult,
    DossierLiveState,
    DossierSignoffSnapshot,
    F_BT11_01,
    F_BT11_02,
    F_POST_08_FAIL_HASH,
    F_POST_08_FAIL_INODE,
    F_POST_08_FAIL_PATH,
    F_POST_08_SIGNATURE_INVALID,
    F_POST_08_SIGNOFF_EXPIRED,
    F_POST_08_SIGNOFF_MISSING,
    F_POST_09,
    F_PRE_14_DOSSIER_UNSIGNED,
    S11cVerifyResult,
    compute_dossier_body_hash,
    extract_org_slug_from_dossier_path,
    is_cross_org_dossier,
    parse_signoff_json,
    verify_cross_org_reference,
    verify_dossier_cite,
    verify_s11c_lock,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_signoff(
    *,
    canonical_path: str = "/abs/orgs/fit_farms_llc/dossier/entities/usda_amber.md",
    inode: int = 1234567,
    content_hash: str = "a" * 128,
    signed_at: str = "2026-01-19T00:00:00Z",
    expires_at: str = "2026-04-19T00:00:00Z",
    operator_id: str = "op-1",
    signature: bytes = b"\x01" * 64,
) -> DossierSignoffSnapshot:
    return DossierSignoffSnapshot(
        signed_at_utc=signed_at,
        operator_id=operator_id,
        signed_canonical_path=canonical_path,
        signed_inode=inode,
        signed_content_hash=content_hash,
        operator_signature=signature,
        expires_at_utc=expires_at,
    )


def _make_live(
    *,
    canonical_path: str = "/abs/orgs/fit_farms_llc/dossier/entities/usda_amber.md",
    inode: int = 1234567,
    content_hash: str = "a" * 128,
) -> DossierLiveState:
    return DossierLiveState(
        canonical_path=canonical_path, inode=inode, content_hash=content_hash
    )


# ---------------------------------------------------------------------------
# TestConstants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_post_08_codes_pinned(self) -> None:
        assert F_POST_08_FAIL_PATH == "F-POST-08.dossier_s11c_fail_path"
        assert F_POST_08_FAIL_INODE == "F-POST-08.dossier_s11c_fail_inode"
        assert F_POST_08_FAIL_HASH == "F-POST-08.dossier_s11c_fail_hash"
        assert F_POST_08_SIGNOFF_MISSING == "F-POST-08.dossier_s11c_signoff_missing"
        assert F_POST_08_SIGNOFF_EXPIRED == "F-POST-08.dossier_s11c_signoff_expired"
        assert (
            F_POST_08_SIGNATURE_INVALID == "F-POST-08.dossier_s11c_signature_invalid"
        )

    def test_pre_14_code_pinned(self) -> None:
        assert F_PRE_14_DOSSIER_UNSIGNED == "F-PRE-14.dossier_unsigned"

    def test_bt11_codes_pinned(self) -> None:
        assert (
            F_BT11_01
            == "F-BT11-01.cross_org_reference_created_without_audit_entry"
        )
        assert (
            F_BT11_02
            == "F-BT11-02.cross_org_reference_missing_draft_time_confirmation"
        )

    def test_post_09_pinned(self) -> None:
        assert F_POST_09 == "F-POST-09.bt11_cross_org_unconfirmed"


# ---------------------------------------------------------------------------
# TestComputeDossierBodyHash
# ---------------------------------------------------------------------------


class TestComputeDossierBodyHash:
    def test_returns_128_hex(self) -> None:
        h = compute_dossier_body_hash(b"# Dossier body\n")
        assert len(h) == 128
        int(h, 16)

    def test_deterministic(self) -> None:
        b = b"# Dossier body\n"
        assert compute_dossier_body_hash(b) == compute_dossier_body_hash(b)

    def test_rejects_non_bytes(self) -> None:
        with pytest.raises(TypeError):
            compute_dossier_body_hash("not bytes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TestParseSignoffJson
# ---------------------------------------------------------------------------


class TestParseSignoffJson:
    def _payload(self) -> dict:
        return {
            "signed_at_utc": "2026-01-19T00:00:00Z",
            "operator_id": "op-1",
            "signed_canonical_path": "/abs/orgs/fit_farms_llc/dossier/entities/usda.md",
            "signed_inode": 999,
            "signed_content_hash": "b" * 128,
            "operator_signature": (b"\x02" * 32).hex(),
            "expires_at_utc": "2026-04-19T00:00:00Z",
        }

    def test_from_dict(self) -> None:
        s = parse_signoff_json(self._payload())
        assert s.operator_id == "op-1"
        assert s.signed_inode == 999
        assert s.operator_signature == b"\x02" * 32

    def test_from_str(self) -> None:
        s = parse_signoff_json(json.dumps(self._payload()))
        assert s.operator_id == "op-1"

    def test_from_bytes(self) -> None:
        s = parse_signoff_json(json.dumps(self._payload()).encode("utf-8"))
        assert s.operator_id == "op-1"

    def test_accepts_raw_bytes_signature(self) -> None:
        payload = self._payload()
        # parser must also accept already-bytes signatures (defensive)
        s = parse_signoff_json(
            {**payload, "operator_signature": b"\x03" * 16}
        )
        assert s.operator_signature == b"\x03" * 16

    def test_malformed_raises(self) -> None:
        with pytest.raises(json.JSONDecodeError):
            parse_signoff_json("{not valid json")

    def test_missing_field_raises(self) -> None:
        bad = self._payload()
        del bad["operator_id"]
        with pytest.raises(KeyError):
            parse_signoff_json(bad)

    def test_wrong_type_raises(self) -> None:
        with pytest.raises(TypeError):
            parse_signoff_json(12345)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TestVerifyS11cLock
# ---------------------------------------------------------------------------


class TestVerifyS11cLock:
    def test_happy_path(self) -> None:
        result = verify_s11c_lock(signoff=_make_signoff(), live=_make_live())
        assert result.s11c_pass is True
        assert result.failure_code is None

    def test_signoff_missing(self) -> None:
        result = verify_s11c_lock(signoff=None, live=_make_live())
        assert result.s11c_pass is False
        assert result.failure_code == F_POST_08_SIGNOFF_MISSING

    def test_signoff_expired(self) -> None:
        result = verify_s11c_lock(
            signoff=_make_signoff(expires_at="2026-04-19T00:00:00Z"),
            live=_make_live(),
            current_utc="2026-04-20T00:00:00Z",
        )
        assert result.s11c_pass is False
        assert result.failure_code == F_POST_08_SIGNOFF_EXPIRED

    def test_signoff_not_yet_expired(self) -> None:
        result = verify_s11c_lock(
            signoff=_make_signoff(expires_at="2026-04-19T00:00:00Z"),
            live=_make_live(),
            current_utc="2026-04-18T00:00:00Z",
        )
        assert result.s11c_pass is True

    def test_signature_invalid(self) -> None:
        def bad_sig(_signoff: DossierSignoffSnapshot) -> bool:
            return False

        result = verify_s11c_lock(
            signoff=_make_signoff(),
            live=_make_live(),
            signature_verifier=bad_sig,
        )
        assert result.s11c_pass is False
        assert result.failure_code == F_POST_08_SIGNATURE_INVALID

    def test_signature_valid(self) -> None:
        def ok_sig(_signoff: DossierSignoffSnapshot) -> bool:
            return True

        result = verify_s11c_lock(
            signoff=_make_signoff(),
            live=_make_live(),
            signature_verifier=ok_sig,
        )
        assert result.s11c_pass is True

    def test_path_mismatch(self) -> None:
        result = verify_s11c_lock(
            signoff=_make_signoff(canonical_path="/orig/path.md"),
            live=_make_live(canonical_path="/swapped/path.md"),
        )
        assert result.s11c_pass is False
        assert result.failure_code == F_POST_08_FAIL_PATH

    def test_inode_mismatch(self) -> None:
        result = verify_s11c_lock(
            signoff=_make_signoff(inode=100),
            live=_make_live(inode=200),
        )
        assert result.s11c_pass is False
        assert result.failure_code == F_POST_08_FAIL_INODE

    def test_hash_mismatch(self) -> None:
        result = verify_s11c_lock(
            signoff=_make_signoff(content_hash="a" * 128),
            live=_make_live(content_hash="b" * 128),
        )
        assert result.s11c_pass is False
        assert result.failure_code == F_POST_08_FAIL_HASH

    def test_live_must_be_dataclass(self) -> None:
        with pytest.raises(TypeError):
            verify_s11c_lock(signoff=_make_signoff(), live={})  # type: ignore[arg-type]

    def test_signoff_wrong_type(self) -> None:
        with pytest.raises(TypeError):
            verify_s11c_lock(
                signoff="not-a-signoff",  # type: ignore[arg-type]
                live=_make_live(),
            )

    def test_signature_verifier_not_callable(self) -> None:
        with pytest.raises(TypeError):
            verify_s11c_lock(
                signoff=_make_signoff(),
                live=_make_live(),
                signature_verifier="nope",  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# TestExtractOrgSlugFromDossierPath
# ---------------------------------------------------------------------------


class TestExtractOrgSlugFromDossierPath:
    def test_extracts_slug(self) -> None:
        slug = extract_org_slug_from_dossier_path(
            "/abs/orgs/fit_farms_llc/dossier/entities/usda.md"
        )
        assert slug == "fit_farms_llc"

    def test_relative_path(self) -> None:
        slug = extract_org_slug_from_dossier_path(
            "orgs/mycosymbiotics_inc/dossier/entities/foo.md"
        )
        assert slug == "mycosymbiotics_inc"

    def test_returns_none_for_vault_shared(self) -> None:
        assert (
            extract_org_slug_from_dossier_path(
                "/abs/vault_shared/rubrics/usda.md"
            )
            is None
        )

    def test_returns_none_for_unrelated(self) -> None:
        assert (
            extract_org_slug_from_dossier_path("/etc/passwd") is None
        )

    def test_returns_none_for_non_dossier_org_path(self) -> None:
        assert (
            extract_org_slug_from_dossier_path(
                "/abs/orgs/fit_farms_llc/scout/run_log/abc.json"
            )
            is None
        )

    def test_rejects_non_str(self) -> None:
        with pytest.raises(TypeError):
            extract_org_slug_from_dossier_path(b"x")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TestIsCrossOrgDossier
# ---------------------------------------------------------------------------


class TestIsCrossOrgDossier:
    def test_same_org(self) -> None:
        assert (
            is_cross_org_dossier(
                dossier_canonical_path=(
                    "/abs/orgs/fit_farms_llc/dossier/entities/usda.md"
                ),
                current_org_slug="fit_farms_llc",
            )
            is False
        )

    def test_different_org(self) -> None:
        assert (
            is_cross_org_dossier(
                dossier_canonical_path=(
                    "/abs/orgs/mycosymbiotics_inc/dossier/entities/usda.md"
                ),
                current_org_slug="fit_farms_llc",
            )
            is True
        )

    def test_non_dossier_path_returns_false(self) -> None:
        assert (
            is_cross_org_dossier(
                dossier_canonical_path="/abs/vault_shared/rubrics/x.md",
                current_org_slug="fit_farms_llc",
            )
            is False
        )

    def test_current_slug_must_be_str(self) -> None:
        with pytest.raises(TypeError):
            is_cross_org_dossier(
                dossier_canonical_path=(
                    "/abs/orgs/foo/dossier/entities/x.md"
                ),
                current_org_slug=1,  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# TestVerifyCrossOrgReference
# ---------------------------------------------------------------------------


class TestVerifyCrossOrgReference:
    SAME_ORG_PATH = "/abs/orgs/fit_farms_llc/dossier/entities/usda.md"
    CROSS_ORG_PATH = "/abs/orgs/mycosymbiotics_inc/dossier/entities/usda.md"

    def test_same_org_passes(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path=self.SAME_ORG_PATH,
            current_org_slug="fit_farms_llc",
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        assert r.cross_org_pass is True
        assert r.cross_org_dossier is False
        assert r.failure_codes == ()

    def test_cross_org_with_both_flags_passes(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path=self.CROSS_ORG_PATH,
            current_org_slug="fit_farms_llc",
            draft_time_confirmation_present=True,
            audit_entry_present=True,
        )
        assert r.cross_org_pass is True
        assert r.cross_org_dossier is True
        assert r.failure_codes == ()

    def test_cross_org_missing_audit(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path=self.CROSS_ORG_PATH,
            current_org_slug="fit_farms_llc",
            draft_time_confirmation_present=True,
            audit_entry_present=False,
        )
        assert r.cross_org_pass is False
        assert r.cross_org_dossier is True
        assert F_BT11_01 in r.failure_codes
        assert F_POST_09 in r.failure_codes
        assert F_BT11_02 not in r.failure_codes

    def test_cross_org_missing_confirmation(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path=self.CROSS_ORG_PATH,
            current_org_slug="fit_farms_llc",
            draft_time_confirmation_present=False,
            audit_entry_present=True,
        )
        assert r.cross_org_pass is False
        assert F_BT11_02 in r.failure_codes
        assert F_POST_09 in r.failure_codes
        assert F_BT11_01 not in r.failure_codes

    def test_cross_org_missing_both(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path=self.CROSS_ORG_PATH,
            current_org_slug="fit_farms_llc",
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        assert r.cross_org_pass is False
        assert F_BT11_01 in r.failure_codes
        assert F_BT11_02 in r.failure_codes
        assert F_POST_09 in r.failure_codes
        assert r.failure_codes.count(F_POST_09) == 1

    def test_non_dossier_path_treated_as_same_org(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path="/abs/vault_shared/rubrics/x.md",
            current_org_slug="fit_farms_llc",
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        assert r.cross_org_pass is True
        assert r.cross_org_dossier is False


# ---------------------------------------------------------------------------
# TestVerifyDossierCite
# ---------------------------------------------------------------------------


class TestVerifyDossierCite:
    def test_same_org_happy(self) -> None:
        r = verify_dossier_cite(
            signoff=_make_signoff(),
            live=_make_live(),
            current_org_slug="fit_farms_llc",
        )
        assert r.overall_pass is True
        assert r.s11c_pass is True
        assert r.cross_org_pass is True
        assert r.cross_org_dossier is False
        assert r.failure_codes == ()

    def test_cross_org_happy_with_flags(self) -> None:
        cross_path = (
            "/abs/orgs/mycosymbiotics_inc/dossier/entities/usda_amber.md"
        )
        r = verify_dossier_cite(
            signoff=_make_signoff(canonical_path=cross_path),
            live=_make_live(canonical_path=cross_path),
            current_org_slug="fit_farms_llc",
            draft_time_confirmation_present=True,
            audit_entry_present=True,
        )
        assert r.overall_pass is True
        assert r.cross_org_dossier is True
        assert r.failure_codes == ()

    def test_s11c_fail_path_alone(self) -> None:
        r = verify_dossier_cite(
            signoff=_make_signoff(canonical_path="/orig/path.md"),
            live=_make_live(
                canonical_path=(
                    "/abs/orgs/fit_farms_llc/dossier/entities/usda_amber.md"
                )
            ),
            current_org_slug="fit_farms_llc",
        )
        assert r.overall_pass is False
        assert r.s11c_pass is False
        assert r.cross_org_pass is True  # same-org path
        assert F_POST_08_FAIL_PATH in r.failure_codes

    def test_cross_org_fail_alone(self) -> None:
        cross_path = (
            "/abs/orgs/mycosymbiotics_inc/dossier/entities/usda_amber.md"
        )
        r = verify_dossier_cite(
            signoff=_make_signoff(canonical_path=cross_path),
            live=_make_live(canonical_path=cross_path),
            current_org_slug="fit_farms_llc",
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        assert r.overall_pass is False
        assert r.s11c_pass is True  # path/inode/hash all match the signoff
        assert r.cross_org_pass is False
        assert F_BT11_01 in r.failure_codes
        assert F_BT11_02 in r.failure_codes
        assert F_POST_09 in r.failure_codes

    def test_both_fail_collects_all_codes(self) -> None:
        cross_path = (
            "/abs/orgs/mycosymbiotics_inc/dossier/entities/usda_amber.md"
        )
        r = verify_dossier_cite(
            signoff=_make_signoff(
                canonical_path=cross_path, content_hash="a" * 128
            ),
            live=_make_live(
                canonical_path=cross_path, content_hash="b" * 128
            ),
            current_org_slug="fit_farms_llc",
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        assert r.overall_pass is False
        assert F_POST_08_FAIL_HASH in r.failure_codes
        assert F_BT11_01 in r.failure_codes
        assert F_BT11_02 in r.failure_codes

    def test_signoff_missing_propagates(self) -> None:
        r = verify_dossier_cite(
            signoff=None,
            live=_make_live(),
            current_org_slug="fit_farms_llc",
        )
        assert r.overall_pass is False
        assert F_POST_08_SIGNOFF_MISSING in r.failure_codes


# ---------------------------------------------------------------------------
# TestResultShapes
# ---------------------------------------------------------------------------


class TestResultShapes:
    def test_s11c_result_frozen_kw_only(self) -> None:
        r = S11cVerifyResult(s11c_pass=True, failure_code=None, failure_detail="")
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.s11c_pass = False  # type: ignore[misc]
        with pytest.raises(TypeError):
            S11cVerifyResult(True, None, "")  # type: ignore[misc]

    def test_cross_org_result_frozen_kw_only(self) -> None:
        r = CrossOrgVerifyResult(
            cross_org_pass=True,
            cross_org_dossier=False,
            failure_codes=(),
            failure_detail="",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.cross_org_pass = False  # type: ignore[misc]

    def test_compose_result_frozen_kw_only(self) -> None:
        r = DossierCiteVerifyResult(
            s11c_pass=True,
            cross_org_pass=True,
            overall_pass=True,
            cross_org_dossier=False,
            failure_codes=(),
            failure_detail="",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.overall_pass = False  # type: ignore[misc]

    def test_signoff_snapshot_frozen_kw_only(self) -> None:
        s = _make_signoff()
        with pytest.raises(dataclasses.FrozenInstanceError):
            s.signed_inode = 0  # type: ignore[misc]

    def test_live_state_frozen_kw_only(self) -> None:
        live = _make_live()
        with pytest.raises(dataclasses.FrozenInstanceError):
            live.inode = 0  # type: ignore[misc]
