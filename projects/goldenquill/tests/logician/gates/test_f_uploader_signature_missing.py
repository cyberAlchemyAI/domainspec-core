"""Unit tests for F-UPLOADER-SIGNATURE-MISSING (PRE-31).

Per Blueprint §12.9.4 + §4 v2.7 amendment. PRE-31 surface emits MISSING
only; MISMATCH is the responsibility of PRE-32 (separate file/test).
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from pipeline.logician.gates.f_uploader_signature_missing import (
    F_UPLOADER_SIGNATURE_MISSING,
    check_uploader_signature_missing,
)
from pipeline.orchestrator.seats.uploader import (
    OperatorSignature,
    UploaderInput,
)


def _make_input(
    *,
    bundle_bytes: bytes,
    signature: OperatorSignature | None,
) -> UploaderInput:
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
    assert F_UPLOADER_SIGNATURE_MISSING == "F-UPLOADER-SIGNATURE-MISSING"


def test_signature_present_and_matches_passes() -> None:
    bundle = b"hello bundle"
    h = hashlib.sha3_512(bundle).hexdigest()
    sig = OperatorSignature(
        signed_at_utc=datetime.now(timezone.utc),
        signer_id="josh",
        bundle_content_hash=h,
    )
    r = check_uploader_signature_missing(
        uploader_input=_make_input(bundle_bytes=bundle, signature=sig),
        submission_bundle_bytes=bundle,
    )
    assert r.success is True
    assert r.failure_code is None


def test_signature_absent_fails() -> None:
    r = check_uploader_signature_missing(
        uploader_input=_make_input(bundle_bytes=b"x", signature=None),
        submission_bundle_bytes=b"x",
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_SIGNATURE_MISSING


def test_signature_mismatch_passes_on_this_surface() -> None:
    """MISMATCH is the SIGNATURE-MISMATCH surface's responsibility."""
    bundle = b"original"
    sig = OperatorSignature(
        signed_at_utc=datetime.now(timezone.utc),
        signer_id="josh",
        bundle_content_hash=hashlib.sha3_512(b"different").hexdigest(),
    )
    r = check_uploader_signature_missing(
        uploader_input=_make_input(bundle_bytes=bundle, signature=sig),
        submission_bundle_bytes=bundle,
    )
    assert r.success is True
    assert r.failure_code is None
