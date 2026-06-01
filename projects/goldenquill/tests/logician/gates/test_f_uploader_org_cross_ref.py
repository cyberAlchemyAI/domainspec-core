"""Unit tests for F-UPLOADER-ORG-CROSS-REF (PRE-36).

Per Blueprint §12.9.5 + §4 v2.7 amendment. Law 3 enforcement.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pipeline.logician.gates.f_uploader_org_cross_ref import (
    F_UPLOADER_ORG_CROSS_REF,
    check_uploader_org_cross_ref,
)
from pipeline.orchestrator.seats.uploader import (
    AttachmentRef,
    UploaderInput,
)


def _att(path: str) -> AttachmentRef:
    return AttachmentRef(
        file_path=path,
        original_file_name=path.split("/")[-1],
        content_sha3_512="0" * 128,
        uploaded_at_utc=datetime.now(timezone.utc),
        uploaded_by="josh",
        rfa_attachment_match=None,
    )


def _make_input(*, org_slug: str, attachments: tuple[AttachmentRef, ...]) -> UploaderInput:
    return UploaderInput(
        run_id="r1",
        grant_id="g1",
        org_slug=org_slug,
        submission_bundle_ref=f"orgs/{org_slug}/vault/grants/g1/submission.bin",
        section_drafts=(),
        claim_evidence_map=(),
        rfa_extracted_record=object(),
        operator_signature=None,
        attachments=attachments,
    )


def test_failure_code_constant() -> None:
    assert F_UPLOADER_ORG_CROSS_REF == "F-UPLOADER-ORG-CROSS-REF"


def test_single_org_passes() -> None:
    r = check_uploader_org_cross_ref(
        uploader_input=_make_input(
            org_slug="org_a",
            attachments=(
                _att("orgs/org_a/vault/grants/g1/attachments/a.pdf"),
                _att("orgs/org_a/vault/grants/g1/attachments/b.pdf"),
            ),
        )
    )
    assert r.success is True
    assert r.failure_code is None


def test_multi_org_attachment_path_fails() -> None:
    r = check_uploader_org_cross_ref(
        uploader_input=_make_input(
            org_slug="org_a",
            attachments=(
                _att("orgs/org_a/vault/grants/g1/attachments/a.pdf"),
                _att("orgs/org_b/vault/grants/g1/attachments/leak.pdf"),
            ),
        )
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_ORG_CROSS_REF


def test_no_attachments_passes() -> None:
    r = check_uploader_org_cross_ref(
        uploader_input=_make_input(org_slug="org_a", attachments=())
    )
    assert r.success is True
