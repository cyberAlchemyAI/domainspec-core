"""§12 Uploader F-UPLOADER-ORG-CROSS-REF — submission_bundle_ref coverage.

HIGH-1e (§4 v2.7 pre-fix dispatch): the seat-side
``f_uploader_org_cross_ref`` predicate previously only checked
``attachments[*].file_path``. It now also sweeps ``submission_bundle_ref``
— a bundle ref pointing at ``orgs/other_org/...`` while ``org_slug`` is
``my_org`` is a Law-3 violation that PRE-36 must catch.
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


def _make_input(
    *,
    org_slug: str,
    submission_bundle_ref: str,
    attachments: tuple = (),
) -> UploaderInput:
    return UploaderInput(
        run_id="r1",
        grant_id="g1",
        org_slug=org_slug,
        submission_bundle_ref=submission_bundle_ref,
        section_drafts=(),
        claim_evidence_map=(),
        rfa_extracted_record=object(),
        operator_signature=None,
        attachments=attachments,
    )


def test_bundle_ref_in_other_org_fires_gate() -> None:
    """org_slug=my_org but submission_bundle_ref points at orgs/other_org/."""
    r = check_uploader_org_cross_ref(
        uploader_input=_make_input(
            org_slug="my_org",
            submission_bundle_ref=(
                "orgs/other_org/vault/grants/g1/submission.bin"
            ),
            attachments=(),
        )
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_ORG_CROSS_REF


def test_bundle_ref_matches_org_slug_passes() -> None:
    r = check_uploader_org_cross_ref(
        uploader_input=_make_input(
            org_slug="my_org",
            submission_bundle_ref="orgs/my_org/vault/grants/g1/submission.bin",
            attachments=(_att("orgs/my_org/vault/grants/g1/attachments/a.pdf"),),
        )
    )
    assert r.success is True


def test_bundle_ref_outside_orgs_tree_does_not_pollute_slugs() -> None:
    """Bundle refs that don't follow orgs/<slug>/ must not register a slug."""
    r = check_uploader_org_cross_ref(
        uploader_input=_make_input(
            org_slug="my_org",
            submission_bundle_ref="/tmp/scratch/submission.bin",
            attachments=(),
        )
    )
    assert r.success is True


def test_attachment_in_other_org_still_fires() -> None:
    """Existing attachment-path coverage is not regressed."""
    r = check_uploader_org_cross_ref(
        uploader_input=_make_input(
            org_slug="my_org",
            submission_bundle_ref="orgs/my_org/vault/grants/g1/submission.bin",
            attachments=(
                _att("orgs/other_org/vault/grants/g1/attachments/leak.pdf"),
            ),
        )
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_ORG_CROSS_REF
