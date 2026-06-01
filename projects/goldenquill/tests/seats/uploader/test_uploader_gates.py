"""§12 Uploader — Logician gate tests.

Spec card: ``pipeline/blueprint/v0.1/section_12_uploader.md`` (§12 v1).

Coverage targets:
- F-UPLOADER-SIGNATURE-MISSING: no signature → FAIL
- F-UPLOADER-SIGNATURE-MISMATCH: wrong hash → FAIL
- F-UPLOADER-SIGNATURE valid: correct hash → PASS
- F-UPLOADER-ORG-CROSS-REF: multi-org input → FAIL
- F-UPLOADER-ORG-CROSS-REF single org: single org → PASS
- F-UPLOADER-AUTOSUBMIT-ATTEMPTED: submitted=True → AssertionError
- UploaderOutput submitted=False: no error
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

import pytest

from pipeline.orchestrator.seats.uploader import (
    AttachmentRef,
    GateResult,
    OperatorSignature,
    PortalConfig,
    UploaderInput,
    UploaderOutput,
    UploaderState,
    ManifestEntry,
    ReadinessChecklist,
    ChecklistItem,
    SubmissionManifest,
    f_uploader_signature_missing,
    f_uploader_org_cross_ref,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_NOW = datetime(2026, 5, 9, 12, 0, 0, tzinfo=timezone.utc)
_BUNDLE_BYTES = b"fake-submission-bundle-bytes-for-testing"
_BUNDLE_HASH = hashlib.sha3_512(_BUNDLE_BYTES).hexdigest()


def _make_signature(*, hash_override: str | None = None) -> OperatorSignature:
    return OperatorSignature(
        signed_at_utc=_NOW,
        signer_id="josh",
        bundle_content_hash=hash_override or _BUNDLE_HASH,
    )


def _make_input(
    *,
    signature: OperatorSignature | None = None,
    attachments: tuple[AttachmentRef, ...] = (),
    org_slug: str = "test_org",
) -> UploaderInput:
    return UploaderInput(
        run_id="run-001",
        grant_id="grant-001",
        org_slug=org_slug,
        submission_bundle_ref=f"orgs/{org_slug}/vault/grants/grant-001/bundle.yaml",
        section_drafts=(),
        claim_evidence_map=(),
        rfa_extracted_record=None,
        operator_signature=signature,
        attachments=attachments,
        target_portal="copy_paste",
        portal_config=None,
        prepared_at_utc=_NOW,
    )


def _make_manifest(*, entries: tuple[ManifestEntry, ...] = ()) -> SubmissionManifest:
    return SubmissionManifest(
        entries=entries,
        assembled_at_utc=_NOW,
        adapter_id="copy_paste",
        run_id="run-001",
    )


def _make_checklist(*, status: str = "ready") -> ReadinessChecklist:
    return ReadinessChecklist(
        overall_status=status,
        items=(),
        fail_count=0,
        warn_count=0,
        pass_count=0,
        checked_at_utc=_NOW,
    )


# ---------------------------------------------------------------------------
# F-UPLOADER-SIGNATURE-MISSING / MISMATCH tests
# ---------------------------------------------------------------------------

class TestSignatureGate:
    def test_signature_missing_none(self) -> None:
        inp = _make_input(signature=None)
        result = f_uploader_signature_missing(inp, _BUNDLE_BYTES)
        assert not result.passed
        assert result.code == "F-UPLOADER-SIGNATURE-MISSING"

    def test_signature_hash_mismatch(self) -> None:
        bad_sig = _make_signature(hash_override="0000" * 32)
        inp = _make_input(signature=bad_sig)
        result = f_uploader_signature_missing(inp, _BUNDLE_BYTES)
        assert not result.passed
        assert result.code == "F-UPLOADER-SIGNATURE-MISMATCH"

    def test_signature_valid(self) -> None:
        good_sig = _make_signature()
        inp = _make_input(signature=good_sig)
        result = f_uploader_signature_missing(inp, _BUNDLE_BYTES)
        assert result.passed
        assert result.code is None


# ---------------------------------------------------------------------------
# F-UPLOADER-ORG-CROSS-REF tests
# ---------------------------------------------------------------------------

class TestOrgCrossRefGate:
    def test_single_org_passes(self) -> None:
        inp = _make_input(org_slug="my_org")
        result = f_uploader_org_cross_ref(inp)
        assert result.passed

    def test_multi_org_fails(self) -> None:
        att = AttachmentRef(
            file_path="orgs/other_org/vault/grants/g1/attachments/resume.pdf",
            original_file_name="resume.pdf",
            content_sha3_512="abc123",
            uploaded_at_utc=_NOW,
            uploaded_by="josh",
            rfa_attachment_match=None,
        )
        inp = _make_input(org_slug="my_org", attachments=(att,))
        result = f_uploader_org_cross_ref(inp)
        assert not result.passed
        assert result.code == "F-UPLOADER-ORG-CROSS-REF"

    def test_same_org_attachment_passes(self) -> None:
        att = AttachmentRef(
            file_path="orgs/my_org/vault/grants/g1/attachments/resume.pdf",
            original_file_name="resume.pdf",
            content_sha3_512="abc123",
            uploaded_at_utc=_NOW,
            uploaded_by="josh",
            rfa_attachment_match=None,
        )
        inp = _make_input(org_slug="my_org", attachments=(att,))
        result = f_uploader_org_cross_ref(inp)
        assert result.passed


# ---------------------------------------------------------------------------
# F-UPLOADER-AUTOSUBMIT-ATTEMPTED tests
# ---------------------------------------------------------------------------

class TestAutosubmitGate:
    def test_submitted_false_ok(self) -> None:
        output = UploaderOutput(
            run_id="run-001",
            manifest=_make_manifest(),
            readiness_checklist=_make_checklist(),
            output_dir="/tmp/test",
            submitted=False,
        )
        assert output.submitted is False

    def test_submitted_true_raises(self) -> None:
        # The runtime layer of F-UPLOADER-AUTOSUBMIT-ATTEMPTED uses ``raise``
        # not ``assert`` (per §4 v2.7 HIGH-1 — assert is stripped by ``python
        # -O``). The exception is RuntimeError, not AssertionError.
        with pytest.raises(RuntimeError, match="F-UPLOADER-AUTOSUBMIT-ATTEMPTED"):
            UploaderOutput(
                run_id="run-001",
                manifest=_make_manifest(),
                readiness_checklist=_make_checklist(),
                output_dir="/tmp/test",
                submitted=True,
            )


# ---------------------------------------------------------------------------
# Type invariant tests
# ---------------------------------------------------------------------------

class TestTypeInvariants:
    def test_uploader_input_frozen(self) -> None:
        inp = _make_input(signature=_make_signature())
        with pytest.raises(AttributeError):
            inp.run_id = "changed"  # type: ignore[misc]

    def test_operator_signature_frozen(self) -> None:
        sig = _make_signature()
        with pytest.raises(AttributeError):
            sig.signer_id = "someone_else"  # type: ignore[misc]

    def test_attachment_ref_frozen(self) -> None:
        att = AttachmentRef(
            file_path="orgs/test/vault/grants/g1/attachments/f.pdf",
            original_file_name="f.pdf",
            content_sha3_512="abc",
            uploaded_at_utc=_NOW,
            uploaded_by="josh",
            rfa_attachment_match=None,
        )
        with pytest.raises(AttributeError):
            att.file_path = "changed"  # type: ignore[misc]

    def test_gate_result_pass(self) -> None:
        r = GateResult.PASS()
        assert r.passed is True
        assert r.code is None

    def test_gate_result_fail(self) -> None:
        r = GateResult.FAIL(code="TEST", detail="test detail")
        assert r.passed is False
        assert r.code == "TEST"
        assert r.detail == "test detail"

    def test_uploader_state_frozen(self) -> None:
        state = UploaderState(
            run_id="run-001",
            grant_id="g1",
            org_slug="test",
            adapter_id="copy_paste",
            assembly_attempted_at_utc=_NOW,
            assembly_succeeded=True,
            sections_assembled=("narrative",),
            sections_failed=(),
            attachments_staged=2,
            readiness_status="ready",
        )
        with pytest.raises(AttributeError):
            state.run_id = "changed"  # type: ignore[misc]
