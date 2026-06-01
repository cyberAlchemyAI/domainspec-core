"""Unit tests for F-UPLOADER-SIGNATURE-MISMATCH (PRE-32).

Per Blueprint §12.9.5 + §4 v2.7 amendment. PRE-32 surface emits MISMATCH
only; MISSING (signature absent) is owned by PRE-31's separate surface.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from pipeline.logician.gates.f_uploader_signature_mismatch import (
    F_UPLOADER_SIGNATURE_MISMATCH,
    check_uploader_signature_mismatch,
)
from pipeline.orchestrator.seats.uploader import (
    OperatorSignature,
    UploaderInput,
)


def _make_input(signature: OperatorSignature | None) -> UploaderInput:
    return UploaderInput(
        run_id="r1",
        grant_id="g1",
        org_slug="org_a",
        submission_bundle_ref="orgs/org_a/vault/grants/g1/submission.bin",
        section_drafts=(),
        claim_evidence_map=(),
        rfa_extracted_record=object(),
        operator_signature=signature,
    )


def test_failure_code_constant() -> None:
    assert F_UPLOADER_SIGNATURE_MISMATCH == "F-UPLOADER-SIGNATURE-MISMATCH"


def test_matching_hash_passes() -> None:
    bundle = b"hello bundle"
    h = hashlib.sha3_512(bundle).hexdigest()
    sig = OperatorSignature(
        signed_at_utc=datetime.now(timezone.utc),
        signer_id="josh",
        bundle_content_hash=h,
    )
    r = check_uploader_signature_mismatch(
        uploader_input=_make_input(sig),
        submission_bundle_bytes=bundle,
    )
    assert r.success is True
    assert r.failure_code is None


def test_mismatched_hash_fails() -> None:
    bundle = b"original"
    sig = OperatorSignature(
        signed_at_utc=datetime.now(timezone.utc),
        signer_id="josh",
        bundle_content_hash=hashlib.sha3_512(b"tampered").hexdigest(),
    )
    r = check_uploader_signature_mismatch(
        uploader_input=_make_input(sig),
        submission_bundle_bytes=bundle,
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_SIGNATURE_MISMATCH


def test_missing_signature_passes_on_this_surface() -> None:
    """MISSING is the SIGNATURE-MISSING surface's responsibility."""
    r = check_uploader_signature_mismatch(
        uploader_input=_make_input(None),
        submission_bundle_bytes=b"x",
    )
    assert r.success is True
    assert r.failure_code is None
