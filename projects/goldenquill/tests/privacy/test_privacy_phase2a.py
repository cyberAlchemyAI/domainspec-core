"""Phase 2a Privacy Router tests — §9.36a-d plus adversarial coverage.

Blueprint §4 v2.3 §4.14 + §9 test vectors LOCKED 2026-04-19.
"""

from __future__ import annotations

import pytest

from pipeline.privacy import (
    PrivacyTag,
    PrivacyRouteResult,
    run_privacy_pregate,
    PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR,
    PRIVACY_FAILURE_CODE_BYPASS_ATTEMPT,
)
from pipeline.privacy._classifier import classify_payload
import pipeline.privacy._router as _router_mod
import pipeline.privacy._classifier as _classifier_mod


# ---------------------------------------------------------------------------
# §9.36a — CLOUD_ELIGIBLE contract (documented for v0.2; v0.1 stub fires first)
# ---------------------------------------------------------------------------

class TestCloudEligibleContract:
    """§9.36a: CLOUD_ELIGIBLE tag must yield routed_local=False, failure_code=None."""

    def test_cloud_eligible_produces_correct_result(self, monkeypatch):
        monkeypatch.setattr(_router_mod, "classify_payload",
                            lambda _: PrivacyTag.CLOUD_ELIGIBLE)
        result = run_privacy_pregate("grant funding for farms", "scribe", "cloud")
        assert result.tag == PrivacyTag.CLOUD_ELIGIBLE
        assert result.routed_local is False
        assert result.failure_code is None

    def test_cloud_eligible_detail_is_none(self, monkeypatch):
        monkeypatch.setattr(_router_mod, "classify_payload",
                            lambda _: PrivacyTag.CLOUD_ELIGIBLE)
        result = run_privacy_pregate("query", "judge", "cloud")
        assert result.detail is None

    def test_cloud_eligible_with_local_default_routing(self, monkeypatch):
        monkeypatch.setattr(_router_mod, "classify_payload",
                            lambda _: PrivacyTag.CLOUD_ELIGIBLE)
        result = run_privacy_pregate("query", "scribe", "local")
        assert result.routed_local is False


# ---------------------------------------------------------------------------
# §9.36b — Stub always returns CLASSIFIER_ERROR → routed_local=True (v0.1)
# ---------------------------------------------------------------------------

class TestStubAlwaysClassifierError:
    """§9.36b: v0.1 stub fires CLASSIFIER_ERROR for all payloads."""

    def test_stub_fires_for_any_payload(self):
        result = run_privacy_pregate("What grants are available?", "scribe", "cloud")
        assert result.tag == PrivacyTag.CLASSIFIER_ERROR
        assert result.routed_local is True
        assert result.failure_code == PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR

    def test_stub_fires_for_empty_payload(self):
        result = run_privacy_pregate("", "judge", "cloud")
        assert result.tag == PrivacyTag.CLASSIFIER_ERROR
        assert result.routed_local is True

    def test_stub_fires_with_local_default_routing(self):
        result = run_privacy_pregate("anything", "scribe", "local")
        assert result.tag == PrivacyTag.CLASSIFIER_ERROR
        assert result.routed_local is True

    def test_stub_fires_for_multiple_seats(self):
        for seat in ["scribe", "judge", "editor", "scout", "logician"]:
            result = run_privacy_pregate("payload", seat, "cloud")
            assert result.tag == PrivacyTag.CLASSIFIER_ERROR
            assert result.routed_local is True

    def test_stub_sub_tag_is_stub_always_fires(self):
        result = run_privacy_pregate("payload", "scribe", "cloud")
        assert result.detail is not None
        assert result.detail.get("sub_tag") == "stub_always_fires"

    def test_stub_detail_contains_seat(self):
        result = run_privacy_pregate("payload", "judge", "cloud")
        assert result.detail is not None
        assert result.detail["seat"] == "judge"

    def test_stub_detail_contains_default_routing(self):
        result = run_privacy_pregate("payload", "scribe", "cloud")
        assert result.detail is not None
        assert result.detail["default_routing"] == "cloud"


# ---------------------------------------------------------------------------
# §9.36c — LOCAL_ONLY contract (v0.2 path)
# ---------------------------------------------------------------------------

class TestLocalOnlyContract:
    """§9.36c: LOCAL_ONLY tag must yield routed_local=True with no failure_code."""

    def test_local_only_routed_local(self, monkeypatch):
        monkeypatch.setattr(_router_mod, "classify_payload",
                            lambda _: PrivacyTag.LOCAL_ONLY)
        result = run_privacy_pregate("John Smith, 123 Main St", "scribe", "cloud")
        assert result.tag == PrivacyTag.LOCAL_ONLY
        assert result.routed_local is True
        assert result.failure_code is None

    def test_local_only_no_failure_code(self, monkeypatch):
        monkeypatch.setattr(_router_mod, "classify_payload",
                            lambda _: PrivacyTag.LOCAL_ONLY)
        result = run_privacy_pregate("person data", "scribe", "cloud")
        assert result.failure_code is None

    def test_local_only_detail_has_seat_and_routing(self, monkeypatch):
        monkeypatch.setattr(_router_mod, "classify_payload",
                            lambda _: PrivacyTag.LOCAL_ONLY)
        result = run_privacy_pregate("person data", "judge", "cloud")
        assert result.detail is not None
        assert result.detail["seat"] == "judge"
        assert result.detail["default_routing"] == "cloud"


# ---------------------------------------------------------------------------
# §9.36d — Classifier exception is caught and fails closed
# ---------------------------------------------------------------------------

class TestClassifierExceptionFailsClosed:
    """§9.36d: Any exception from classify_payload must be caught; gate routes local."""

    def test_exception_yields_classifier_error(self, monkeypatch):
        def raise_error(_):
            raise RuntimeError("classifier crashed")
        monkeypatch.setattr(_router_mod, "classify_payload", raise_error)
        result = run_privacy_pregate("payload", "scribe", "cloud")
        assert result.tag == PrivacyTag.CLASSIFIER_ERROR
        assert result.routed_local is True
        assert result.failure_code == PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR

    def test_exception_detail_contains_sub_tag(self, monkeypatch):
        def raise_error(_):
            raise ValueError("bad classifier")
        monkeypatch.setattr(_router_mod, "classify_payload", raise_error)
        result = run_privacy_pregate("payload", "scribe", "cloud")
        assert result.detail is not None
        assert result.detail["sub_tag"] == "classifier_exception"

    def test_exception_detail_contains_exception_message(self, monkeypatch):
        def raise_error(_):
            raise ValueError("specific error message")
        monkeypatch.setattr(_router_mod, "classify_payload", raise_error)
        result = run_privacy_pregate("payload", "scribe", "cloud")
        assert "specific error message" in result.detail["exception"]

    def test_exception_on_type_error(self, monkeypatch):
        def raise_type_error(_):
            raise TypeError("type problem")
        monkeypatch.setattr(_router_mod, "classify_payload", raise_type_error)
        result = run_privacy_pregate("payload", "judge", "cloud")
        assert result.routed_local is True

    def test_exception_with_local_default_routing(self, monkeypatch):
        def raise_error(_):
            raise RuntimeError("crash")
        monkeypatch.setattr(_router_mod, "classify_payload", raise_error)
        result = run_privacy_pregate("payload", "scribe", "local")
        assert result.routed_local is True  # already local, but still fail-closed


# ---------------------------------------------------------------------------
# Invariant properties (Da Vinci §8 step 6)
# ---------------------------------------------------------------------------

class TestPrivacyRouterInvariants:
    """Invariant: routed_local is always True when tag != CLOUD_ELIGIBLE."""

    @pytest.mark.parametrize("tag,expected_local", [
        (PrivacyTag.CLOUD_ELIGIBLE, False),
        (PrivacyTag.LOCAL_ONLY, True),
        (PrivacyTag.CLASSIFIER_ERROR, True),
    ])
    def test_routed_local_invariant(self, monkeypatch, tag, expected_local):
        monkeypatch.setattr(_router_mod, "classify_payload", lambda _: tag)
        result = run_privacy_pregate("payload", "scribe", "cloud")
        assert result.routed_local is expected_local

    @pytest.mark.parametrize("tag", [
        PrivacyTag.LOCAL_ONLY,
        PrivacyTag.CLASSIFIER_ERROR,
    ])
    def test_failure_code_set_only_on_classifier_error(self, monkeypatch, tag):
        monkeypatch.setattr(_router_mod, "classify_payload", lambda _: tag)
        result = run_privacy_pregate("payload", "scribe", "cloud")
        if tag == PrivacyTag.CLASSIFIER_ERROR:
            assert result.failure_code == PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR
        else:
            assert result.failure_code is None

    def test_result_is_frozen_dataclass(self):
        result = run_privacy_pregate("payload", "scribe", "cloud")
        with pytest.raises((AttributeError, TypeError)):
            result.routed_local = False  # type: ignore[misc]

    def test_all_results_have_valid_tag(self, monkeypatch):
        for tag in PrivacyTag:
            monkeypatch.setattr(_router_mod, "classify_payload", lambda _, t=tag: t)
            result = run_privacy_pregate("payload", "scribe", "cloud")
            assert isinstance(result.tag, PrivacyTag)

    def test_failure_code_constants_are_correct(self):
        assert PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR == "F-PRIVACY-CLASSIFIER-ERROR"
        assert PRIVACY_FAILURE_CODE_BYPASS_ATTEMPT == (
            "F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED"
        )

    def test_run_always_returns_result_never_raises(self, monkeypatch):
        def extreme_raise(_):
            raise SystemError("fatal crash")
        monkeypatch.setattr(_router_mod, "classify_payload", extreme_raise)
        result = run_privacy_pregate("payload", "scribe", "cloud")
        assert result is not None
        assert result.routed_local is True


# ---------------------------------------------------------------------------
# Corpus tests (v1 vectors from spec card)
# ---------------------------------------------------------------------------

class TestPrivacyRouterCorpus:
    """Corpus vectors — preserved for regression across versions."""

    def test_corpus_v1_classifier_error(self):
        # v0.1 stub fires: CLASSIFIER_ERROR → routed_local=True
        result = run_privacy_pregate("What is the VAPG grant deadline?", "scribe", "cloud")
        assert result.tag == PrivacyTag.CLASSIFIER_ERROR
        assert result.routed_local is True
        assert result.failure_code == PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR

    def test_corpus_v1_local_only_contract(self, monkeypatch):
        # v0.2 contract: LOCAL_ONLY → routed_local=True, failure_code=None
        monkeypatch.setattr(_router_mod, "classify_payload",
                            lambda _: PrivacyTag.LOCAL_ONLY)
        result = run_privacy_pregate("Employee: Alice, SSN: 123-45-6789", "scribe", "cloud")
        assert result.tag == PrivacyTag.LOCAL_ONLY
        assert result.routed_local is True
        assert result.failure_code is None

    def test_corpus_v1_cloud_eligible_contract(self, monkeypatch):
        # v0.2 contract: CLOUD_ELIGIBLE → routed_local=False, failure_code=None
        monkeypatch.setattr(_router_mod, "classify_payload",
                            lambda _: PrivacyTag.CLOUD_ELIGIBLE)
        result = run_privacy_pregate("Describe the USDA VAPG program goals.", "scribe", "cloud")
        assert result.tag == PrivacyTag.CLOUD_ELIGIBLE
        assert result.routed_local is False
        assert result.failure_code is None


# ---------------------------------------------------------------------------
# Classifier module tests
# ---------------------------------------------------------------------------

class TestClassifierStub:
    """Tests for the v0.1 classifier stub."""

    def test_stub_returns_classifier_error(self):
        assert classify_payload("anything") == PrivacyTag.CLASSIFIER_ERROR

    def test_stub_returns_classifier_error_for_empty_string(self):
        assert classify_payload("") == PrivacyTag.CLASSIFIER_ERROR

    def test_privacy_tag_values(self):
        assert PrivacyTag.LOCAL_ONLY == "LOCAL_ONLY"
        assert PrivacyTag.CLOUD_ELIGIBLE == "CLOUD_ELIGIBLE"
        assert PrivacyTag.CLASSIFIER_ERROR == "CLASSIFIER_ERROR"

    def test_privacy_tag_is_str_enum(self):
        assert isinstance(PrivacyTag.LOCAL_ONLY, str)


# ---------------------------------------------------------------------------
# Adversarial: classifier returns non-PrivacyTag — review round 2026-04-19 F1
# ---------------------------------------------------------------------------

class TestClassifierNonPrivacyTagReturnFailsClosed:
    """A compromised/future classifier must not bypass the gate by returning an
    object whose __eq__ matches CLOUD_ELIGIBLE. The router must reject anything
    that is not a PrivacyTag member and fail-closed to LOCAL-ONLY. Source:
    pipeline/validation/code_reviews/phase0_through_2b_2026-04-19 GPT-OSS F1.
    """

    def test_fake_equal_object_does_not_route_cloud(self, monkeypatch):
        class FakeTag:
            def __eq__(self, other):
                return True  # claim equality with anything, including CLOUD_ELIGIBLE

            def __hash__(self):
                return 0

        monkeypatch.setattr(_router_mod, "classify_payload", lambda p: FakeTag())
        result = run_privacy_pregate("anything", "scribe", "cloud")
        assert result.tag == PrivacyTag.CLASSIFIER_ERROR
        assert result.routed_local is True
        assert result.failure_code == PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR
        assert result.detail["sub_tag"] == "classifier_returned_non_privacytag"
        assert result.detail["returned_type"] == "FakeTag"

    def test_string_cloud_eligible_does_not_bypass(self, monkeypatch):
        # Bare str equal to the enum's value must still fail the isinstance gate.
        monkeypatch.setattr(_router_mod, "classify_payload", lambda p: "CLOUD_ELIGIBLE")
        result = run_privacy_pregate("anything", "scribe", "cloud")
        assert result.tag == PrivacyTag.CLASSIFIER_ERROR
        assert result.routed_local is True
        assert result.failure_code == PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR
        assert result.detail["returned_type"] == "str"

    def test_none_return_does_not_route_cloud(self, monkeypatch):
        monkeypatch.setattr(_router_mod, "classify_payload", lambda p: None)
        result = run_privacy_pregate("anything", "scribe", "cloud")
        assert result.routed_local is True
        assert result.failure_code == PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR
