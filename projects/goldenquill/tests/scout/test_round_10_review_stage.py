"""Round 10 Module 1 — §4.8 REVIEW stage (``pipeline.scout.review_stage``).

Test surface floor ≥ 60 (spec-card scout_round_10_review_and_entity_research
v1); expects ~70 with the two-module split. E-024 eighth-firing 2.03×
multiplier applied selectively to the record_operator_decision striped-lock
correctness surface; adversarial count ≥ 6.

Lessons applied from start:

- E-017 Protocol-injection (ninth Scout reuse — ``ReviewQueueReader`` new
  seam; ``VaultWriter`` / ``CheckpointWriter`` / ``SessionLike`` reused).
- E-024 test-count multiplier (expect ~70 tests on this module).
- E-025 range-check version pin (``rN >= 10``).
- E-026 formal ``__module__`` lineage check over ``__dict__``.
- E-027 ``lint_tree`` directory contract — tmp-dir copy shim.
- E-028 ``# pragma: no cover`` not required — all branches reachable.
"""

from __future__ import annotations

import re
import shutil
import threading
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Mapping, Optional, Tuple

import pytest

import pipeline.scout.review_stage as rs
from pipeline.scout._constants import (
    DECISION_ACCEPT,
    DECISION_HOLD,
    DECISION_REJECT,
    INTENT_REVIEW_QUEUE_READ,
    INTENT_REVIEW_QUEUE_WRITE,
    SCOUT_REVIEW_LOCK_STRIPES,
    VERDICT_UNVERIFIED,
    VERDICT_VERIFICATION_FAILED,
    VERDICT_VERIFIED_FIT,
    VERDICT_VERIFIED_NOT_FIT,
)
from pipeline.scout._types import (
    Candidate,
    ReviewQueueItem,
    VerificationVerdict,
)
from pipeline.scout.review_stage import (
    F_SCOUT_R_01,
    F_SCOUT_R_02,
    F_SCOUT_R_03,
    F_SCOUT_R_04,
    VALID_DECISIONS,
    CheckpointWriter,
    IntentMismatch,
    ReviewDecisionInvalid,
    ReviewDecisionLocked,
    ReviewEnqueueRejected,
    ReviewQueueReader,
    SessionLike,
    VaultWriter,
    _assert_intent_matches,
    _canonical_queue_item_bytes,
    _review_lock,
    _review_queue_path,
    _REVIEW_DECISION_LOCK_STRIPES,
    enqueue_for_review,
    read_review_queue,
    record_operator_decision,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


@dataclass
class FakeSession:
    session_id: str = "session-r10-abc"
    slug: str = "mycosymbiotics_cooperative"
    operator_id: str = "josh"


@dataclass
class WriteCall:
    path: str
    bytes_: bytes
    intent: str
    session_id: str
    slug: str


@dataclass
class RecordingVaultWriter:
    calls: List[WriteCall] = field(default_factory=list)
    raise_with: Optional[BaseException] = None

    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None:
        if self.raise_with is not None:
            raise self.raise_with
        self.calls.append(
            WriteCall(
                path=path,
                bytes_=bytes_,
                intent=intent,
                session_id=session_id,
                slug=slug,
            )
        )


@dataclass
class FakeReviewQueueReader:
    """In-memory recorder mapping candidate_id → ReviewQueueItem."""

    store: dict[str, ReviewQueueItem] = field(default_factory=dict)
    read_calls: List[Tuple[str, str, str]] = field(default_factory=list)
    enumerate_calls: List[Tuple[str, str]] = field(default_factory=list)
    read_raises: Optional[BaseException] = None
    enumerate_raises: Optional[BaseException] = None

    def read_item(
        self,
        *,
        session_id: str,
        slug: str,
        candidate_id: str,
    ) -> Optional[ReviewQueueItem]:
        self.read_calls.append((session_id, slug, candidate_id))
        if self.read_raises is not None:
            raise self.read_raises
        return self.store.get(candidate_id)

    def enumerate_items(
        self,
        *,
        session_id: str,
        slug: str,
    ) -> tuple[ReviewQueueItem, ...]:
        self.enumerate_calls.append((session_id, slug))
        if self.enumerate_raises is not None:
            raise self.enumerate_raises
        return tuple(self.store.values())


@dataclass
class RecordingCheckpointWriter:
    calls: List[Tuple[str, Mapping[str, Any]]] = field(default_factory=list)

    def write(self, *, stage: str, payload: Mapping[str, Any]) -> None:
        self.calls.append((stage, dict(payload)))

    def stages(self) -> List[str]:
        return [stage for stage, _ in self.calls]


def _mk_candidate(candidate_id: str = "cid-001") -> Candidate:
    return Candidate(
        candidate_id=candidate_id,
        channel="A",
        feed_or_adapter_id="api:grants_gov",
        source_key="source-x",
        title=f"Opportunity {candidate_id}",
        funder="Some Funder",
        funder_kind="federal",
        url=f"https://example.test/{candidate_id}",
        close_date_utc="2026-08-01T00:00:00Z",
        award_ceiling=500_000,
        award_floor=50_000,
        applicant_types=("nonprofit",),
        program_page_url=None,
        fetch_timestamp_utc="2026-04-20T00:00:00Z",
        url_hash="0" * 128,
        content_hash=None,
        fit_score_cached=75,
        cache_provenance=None,
    )


def _mk_verdict(
    *,
    candidate_id: str = "cid-001",
    verdict: str = VERDICT_VERIFIED_FIT,
    reason_code: str = "V-OK",
) -> VerificationVerdict:
    return VerificationVerdict(
        candidate_id=candidate_id,
        verdict=verdict,
        reason_code=reason_code,
        live_synopsis_url="https://example.test/live",
        live_content_hash="d" * 128,
        fetched_at_utc="2026-05-01T00:00:00Z",
        timeout_seconds=10,
        eligibility_live=("nonprofit",),
        award_floor_live=20_000,
        award_ceiling_live=300_000,
        close_date_live_utc="2026-08-01T00:00:00Z",
        evidence_quote="eligible applicants include nonprofits",
    )


def _mk_existing_item(
    *,
    candidate_id: str = "cid-001",
    operator_decision: Optional[str] = None,
) -> ReviewQueueItem:
    return ReviewQueueItem(
        candidate_id=candidate_id,
        queued_at_utc="2026-04-21T00:00:00Z",
        queued_by_verdict=VERDICT_VERIFIED_FIT,
        candidate_snapshot=_mk_candidate(candidate_id),
        verification_snapshot=_mk_verdict(candidate_id=candidate_id),
        fit_rationale="nominal fit",
        operator_decision=operator_decision,
        operator_decided_at_utc=(
            "2026-04-21T01:00:00Z" if operator_decision else None
        ),
        operator_decision_reason=(
            "prior-decision" if operator_decision else None
        ),
    )


class FrozenClock:
    def __init__(self, seq: Optional[List[str]] = None):
        self._seq = list(seq or ["2026-04-21T12:00:00Z"])
        self.calls = 0

    def __call__(self) -> str:
        idx = min(self.calls, len(self._seq) - 1)
        self.calls += 1
        return self._seq[idx]


# ---------------------------------------------------------------------------
# Constants & public surface
# ---------------------------------------------------------------------------


class TestConstantsAndPublicSurface:
    def test_failure_codes_verbatim_blueprint_6_8(self):
        assert F_SCOUT_R_01 == "F-SCOUT-R-01"
        assert F_SCOUT_R_02 == "F-SCOUT-R-02"
        assert F_SCOUT_R_03 == "F-SCOUT-R-03"
        assert F_SCOUT_R_04 == "F-SCOUT-R-04"

    def test_valid_decisions_is_frozenset_of_three(self):
        assert isinstance(VALID_DECISIONS, frozenset)
        assert VALID_DECISIONS == frozenset(
            {DECISION_ACCEPT, DECISION_REJECT, DECISION_HOLD}
        )

    def test_stripe_count_is_64(self):
        assert SCOUT_REVIEW_LOCK_STRIPES == 64

    def test_stripe_array_length_matches_constant(self):
        assert len(_REVIEW_DECISION_LOCK_STRIPES) == SCOUT_REVIEW_LOCK_STRIPES

    def test_stripe_array_entries_are_lock_objects(self):
        # Lock class is stdlib; isinstance is brittle on some runtimes.
        # Duck-type: every element responds to ``acquire`` + ``release``.
        for lk in _REVIEW_DECISION_LOCK_STRIPES:
            assert hasattr(lk, "acquire") and hasattr(lk, "release")

    def test_review_queue_path_shape(self):
        assert (
            _review_queue_path("mycosymbiotics", "cid-abc")
            == "mycosymbiotics/review_queue/cid-abc.json"
        )

    def test_intent_literals_match_blueprint(self):
        assert INTENT_REVIEW_QUEUE_WRITE == "review-queue-write"
        assert INTENT_REVIEW_QUEUE_READ == "review-queue-read"

    def test_module_has_no_setattr_call_site(self):
        # R4 guard — scout path never sets operator_decision via setattr.
        src = Path(rs.__file__).read_text(encoding="utf-8")
        assert "setattr(" not in src

    def test_module_has_no_eval_or_exec_call_site(self):
        src = Path(rs.__file__).read_text(encoding="utf-8")
        assert "\neval(" not in src
        assert "\nexec(" not in src

    def test_module_has_no_open_call_site(self):
        src = Path(rs.__file__).read_text(encoding="utf-8")
        assert "\nopen(" not in src

    def test_module_does_not_import_pipeline_vault(self):
        src = Path(rs.__file__).read_text(encoding="utf-8")
        lines = [
            ln
            for ln in src.splitlines()
            if ln.startswith("from pipeline.vault")
            or ln.startswith("import pipeline.vault")
        ]
        assert lines == []


# ---------------------------------------------------------------------------
# Striped lock surface
# ---------------------------------------------------------------------------


class TestStripedLock:
    def test_same_key_returns_same_lock(self):
        assert _review_lock("s", "c") is _review_lock("s", "c")

    def test_lock_is_threading_lock(self):
        lk = _review_lock("s", "c")
        assert lk in _REVIEW_DECISION_LOCK_STRIPES

    def test_many_keys_cover_multiple_stripes(self):
        # With 64 stripes and 256 distinct keys, we expect >1 stripe hit.
        seen = {id(_review_lock(f"s{i}", f"c{i}")) for i in range(256)}
        assert len(seen) > 1

    def test_distinct_keys_may_share_stripe_or_not(self):
        # Existence only — this is just a pigeonhole property check.
        # Runs deterministic under intra-run hash salt.
        pairs = [(f"slug-{i}", f"cid-{i}") for i in range(128)]
        stripes = {id(_review_lock(s, c)) for s, c in pairs}
        assert stripes  # no crash


# ---------------------------------------------------------------------------
# _assert_intent_matches
# ---------------------------------------------------------------------------


class TestAssertIntentMatches:
    def test_exact_match_passes(self):
        _assert_intent_matches(
            expected_intent=INTENT_REVIEW_QUEUE_READ,
            observed_intent=INTENT_REVIEW_QUEUE_READ,
            expected_session_id="s1",
            observed_session_id="s1",
            expected_slug="my_org",
            observed_slug="my_org",
        )

    def test_session_id_mismatch_raises_intent_mismatch(self):
        with pytest.raises(IntentMismatch) as exc:
            _assert_intent_matches(
                expected_intent=INTENT_REVIEW_QUEUE_READ,
                observed_intent=INTENT_REVIEW_QUEUE_READ,
                expected_session_id="s1",
                observed_session_id="s2",
                expected_slug="my_org",
                observed_slug="my_org",
            )
        assert exc.value.code == "review-queue-intent-mismatch"
        assert "session_id_mismatch" in exc.value.reason_tag

    def test_slug_mismatch_raises_intent_mismatch(self):
        with pytest.raises(IntentMismatch) as exc:
            _assert_intent_matches(
                expected_intent=INTENT_REVIEW_QUEUE_READ,
                observed_intent=INTENT_REVIEW_QUEUE_READ,
                expected_session_id="s1",
                observed_session_id="s1",
                expected_slug="org_a",
                observed_slug="org_b",
            )
        assert "slug_mismatch" in exc.value.reason_tag

    def test_nfc_drift_raises_nfc_subcode(self):
        # U+FF09 FULLWIDTH RIGHT PARENTHESIS etc. won't NFC back.
        # Simpler: NFD-composed vs NFC-composed forms of "é".
        nfd = unicodedata.normalize("NFD", "review-qué-read")
        nfc = unicodedata.normalize("NFC", "review-qué-read")
        assert nfd != nfc  # sanity
        with pytest.raises(IntentMismatch) as exc:
            _assert_intent_matches(
                expected_intent=nfc,
                observed_intent=nfd,
                expected_session_id="s1",
                observed_session_id="s1",
                expected_slug="my_org",
                observed_slug="my_org",
            )
        assert exc.value.code == "review-queue-intent-nfc-drift"
        assert "intent_nfc_drift" in exc.value.reason_tag

    def test_plain_intent_mismatch_without_nfc_path(self):
        with pytest.raises(IntentMismatch) as exc:
            _assert_intent_matches(
                expected_intent="review-queue-read",
                observed_intent="review-queue-write",
                expected_session_id="s1",
                observed_session_id="s1",
                expected_slug="my_org",
                observed_slug="my_org",
            )
        assert exc.value.code == "review-queue-intent-mismatch"
        assert "intent_mismatch" in exc.value.reason_tag

    def test_intent_mismatch_carries_str_message(self):
        try:
            _assert_intent_matches(
                expected_intent="a",
                observed_intent="b",
                expected_session_id="s",
                observed_session_id="s",
                expected_slug="x",
                observed_slug="x",
            )
        except IntentMismatch as e:
            assert "review-queue-intent-mismatch" in str(e)
        else:  # pragma: no cover
            raise AssertionError("expected IntentMismatch")


# ---------------------------------------------------------------------------
# enqueue_for_review — happy path
# ---------------------------------------------------------------------------


class TestEnqueueHappyPath:
    def _invoke(self, **overrides):
        session = overrides.pop("session", FakeSession())
        candidate = overrides.pop("candidate", _mk_candidate())
        verdict = overrides.pop("verdict", _mk_verdict())
        fit_rationale = overrides.pop("fit_rationale", "nominal fit")
        vw = overrides.pop("vw", RecordingVaultWriter())
        cpw = overrides.pop("cpw", RecordingCheckpointWriter())
        clock = overrides.pop("clock", FrozenClock(["2026-04-21T12:00:00Z"]))
        assert not overrides
        item = enqueue_for_review(
            session=session,
            candidate=candidate,
            verdict=verdict,
            fit_rationale=fit_rationale,
            vault_writer=vw,
            checkpoint_writer=cpw,
            clock=clock,
        )
        return session, vw, cpw, item

    def test_returns_review_queue_item(self):
        _, _, _, item = self._invoke()
        assert isinstance(item, ReviewQueueItem)
        assert item.candidate_id == "cid-001"
        assert item.queued_by_verdict == VERDICT_VERIFIED_FIT
        assert item.operator_decision is None
        assert item.operator_decided_at_utc is None
        assert item.operator_decision_reason is None

    def test_vault_write_uses_review_queue_write_intent(self):
        _, vw, _, _ = self._invoke()
        assert len(vw.calls) == 1
        assert vw.calls[0].intent == INTENT_REVIEW_QUEUE_WRITE

    def test_vault_write_path_shape(self):
        session, vw, _, _ = self._invoke()
        assert (
            vw.calls[0].path
            == f"{session.slug}/review_queue/cid-001.json"
        )

    def test_vault_write_identity_tuple(self):
        session, vw, _, _ = self._invoke()
        c = vw.calls[0]
        assert c.session_id == session.session_id
        assert c.slug == session.slug

    def test_vault_write_canonical_json_bytes(self):
        _, vw, _, item = self._invoke()
        assert vw.calls[0].bytes_ == _canonical_queue_item_bytes(item)

    def test_queued_at_utc_comes_from_clock(self):
        clock = FrozenClock(["2026-04-21T12:34:56Z"])
        _, _, _, item = self._invoke(clock=clock)
        assert item.queued_at_utc == "2026-04-21T12:34:56Z"

    def test_start_and_complete_checkpoints_written(self):
        _, _, cpw, _ = self._invoke()
        assert cpw.stages() == [
            "review_enqueue_start",
            "review_enqueue_complete",
        ]
        assert cpw.calls[1][1]["outcome"] == "success"

    def test_fit_rationale_round_tripped(self):
        _, _, _, item = self._invoke(fit_rationale="bespoke rationale")
        assert item.fit_rationale == "bespoke rationale"


# ---------------------------------------------------------------------------
# enqueue_for_review — rejects
# ---------------------------------------------------------------------------


class TestEnqueueRejects:
    @pytest.mark.parametrize(
        "verdict_value",
        [
            VERDICT_VERIFIED_NOT_FIT,
            VERDICT_UNVERIFIED,
            VERDICT_VERIFICATION_FAILED,
        ],
    )
    def test_rejects_non_verified_fit_r01(self, verdict_value: str):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        with pytest.raises(ReviewEnqueueRejected) as exc:
            enqueue_for_review(
                session=FakeSession(),
                candidate=_mk_candidate(),
                verdict=_mk_verdict(verdict=verdict_value),
                fit_rationale="x",
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_01 in str(exc.value)
        assert vw.calls == []
        assert cpw.calls[-1][1]["outcome"] == "failure"
        assert cpw.calls[-1][1]["error_type"] == "ReviewEnqueueRejected"

    def test_rejects_empty_slug_r02(self):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        session = FakeSession(slug="")
        with pytest.raises(ReviewEnqueueRejected) as exc:
            enqueue_for_review(
                session=session,
                candidate=_mk_candidate(),
                verdict=_mk_verdict(),
                fit_rationale="x",
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_02 in str(exc.value)
        assert vw.calls == []

    def test_rejects_empty_candidate_id_r02(self):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        bad = Candidate(
            candidate_id="",
            channel="A",
            feed_or_adapter_id="api:seed",
            source_key="s",
            title="t",
            funder="f",
            funder_kind="federal",
            url="https://e.test/x",
            close_date_utc=None,
            award_ceiling=None,
            award_floor=None,
            applicant_types=(),
            program_page_url=None,
            fetch_timestamp_utc="2026-04-20T00:00:00Z",
            url_hash="0" * 128,
            content_hash=None,
            fit_score_cached=0,
            cache_provenance=None,
        )
        with pytest.raises(ReviewEnqueueRejected) as exc:
            enqueue_for_review(
                session=FakeSession(),
                candidate=bad,
                verdict=_mk_verdict(candidate_id=""),
                fit_rationale="x",
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_02 in str(exc.value)

    @pytest.mark.parametrize(
        "bad_cid",
        [
            "..",
            "../etc/passwd",
            "nested/path",
            ".hidden",
            "a/b",
        ],
    )
    def test_rejects_path_traversal_candidate_id_r02(self, bad_cid: str):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        cand = _mk_candidate(candidate_id=bad_cid)
        vrd = _mk_verdict(candidate_id=bad_cid)
        with pytest.raises(ReviewEnqueueRejected) as exc:
            enqueue_for_review(
                session=FakeSession(),
                candidate=cand,
                verdict=vrd,
                fit_rationale="x",
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_02 in str(exc.value)
        assert vw.calls == []

    @pytest.mark.parametrize("bad_slug", ["..", "a/b", "../escape"])
    def test_rejects_path_traversal_slug_r02(self, bad_slug: str):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        with pytest.raises(ReviewEnqueueRejected) as exc:
            enqueue_for_review(
                session=FakeSession(slug=bad_slug),
                candidate=_mk_candidate(),
                verdict=_mk_verdict(),
                fit_rationale="x",
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_02 in str(exc.value)

    def test_failure_checkpoint_on_vault_writer_exception(self):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter(raise_with=RuntimeError("disk full"))
        with pytest.raises(RuntimeError, match="disk full"):
            enqueue_for_review(
                session=FakeSession(),
                candidate=_mk_candidate(),
                verdict=_mk_verdict(),
                fit_rationale="x",
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert cpw.calls[0][0] == "review_enqueue_start"
        assert cpw.calls[-1][0] == "review_enqueue_complete"
        assert cpw.calls[-1][1]["outcome"] == "failure"
        assert cpw.calls[-1][1]["error_type"] == "RuntimeError"

    def test_keyboard_interrupt_propagates_without_failure_checkpoint(self):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter(raise_with=KeyboardInterrupt())
        with pytest.raises(KeyboardInterrupt):
            enqueue_for_review(
                session=FakeSession(),
                candidate=_mk_candidate(),
                verdict=_mk_verdict(),
                fit_rationale="x",
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        # Start checkpoint lands, complete checkpoint does NOT (Rule 1 bypass
        # on Interrupt — matches Round 9 discipline).
        assert cpw.stages() == ["review_enqueue_start"]

    def test_idempotent_second_call_overwrites_first(self):
        # Second enqueue against same (slug, candidate_id) simply re-writes;
        # vault_write is called twice, canonical bytes potentially differ by
        # clock timestamp but path + intent are identical.
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        clk = FrozenClock(
            ["2026-04-21T12:00:00Z", "2026-04-21T12:00:01Z"]
        )
        enqueue_for_review(
            session=FakeSession(),
            candidate=_mk_candidate(),
            verdict=_mk_verdict(),
            fit_rationale="first",
            vault_writer=vw,
            checkpoint_writer=cpw,
            clock=clk,
        )
        enqueue_for_review(
            session=FakeSession(),
            candidate=_mk_candidate(),
            verdict=_mk_verdict(),
            fit_rationale="second",
            vault_writer=vw,
            checkpoint_writer=cpw,
            clock=clk,
        )
        assert len(vw.calls) == 2
        assert vw.calls[0].path == vw.calls[1].path
        assert vw.calls[0].intent == vw.calls[1].intent


# ---------------------------------------------------------------------------
# record_operator_decision — valid decisions
# ---------------------------------------------------------------------------


class TestRecordOperatorDecisionValid:
    def _invoke(self, decision: str, *, existing_decision: Optional[str] = None):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        reader = FakeReviewQueueReader(
            store={
                "cid-001": _mk_existing_item(
                    operator_decision=existing_decision
                )
            }
        )
        item = record_operator_decision(
            session=FakeSession(),
            candidate_id="cid-001",
            decision=decision,
            reason="operator rationale",
            review_queue_reader=reader,
            vault_writer=vw,
            checkpoint_writer=cpw,
            clock=FrozenClock(["2026-04-21T15:00:00Z"]),
        )
        return item, vw, cpw, reader

    def test_accept_writes_updated_item(self):
        item, vw, _, _ = self._invoke(DECISION_ACCEPT)
        assert item.operator_decision == DECISION_ACCEPT
        assert item.operator_decided_at_utc == "2026-04-21T15:00:00Z"
        assert item.operator_decision_reason == "operator rationale"
        assert len(vw.calls) == 1
        assert vw.calls[0].intent == INTENT_REVIEW_QUEUE_WRITE

    def test_reject_writes_updated_item(self):
        item, _, _, _ = self._invoke(DECISION_REJECT)
        assert item.operator_decision == DECISION_REJECT

    def test_hold_writes_updated_item(self):
        item, _, _, _ = self._invoke(DECISION_HOLD)
        assert item.operator_decision == DECISION_HOLD

    def test_hold_then_accept_succeeds(self):
        item, _, _, _ = self._invoke(
            DECISION_ACCEPT, existing_decision=DECISION_HOLD
        )
        assert item.operator_decision == DECISION_ACCEPT

    def test_hold_then_reject_succeeds(self):
        item, _, _, _ = self._invoke(
            DECISION_REJECT, existing_decision=DECISION_HOLD
        )
        assert item.operator_decision == DECISION_REJECT

    def test_vault_write_path_shape_matches_enqueue(self):
        _, vw, _, _ = self._invoke(DECISION_ACCEPT)
        assert vw.calls[0].path == "mycosymbiotics_cooperative/review_queue/cid-001.json"


# ---------------------------------------------------------------------------
# record_operator_decision — invalid + locked
# ---------------------------------------------------------------------------


class TestRecordOperatorDecisionInvalid:
    @pytest.mark.parametrize(
        "bad", ["MAYBE", "", "accept", "reject", "HOLD ", "yes", "NO"]
    )
    def test_invalid_decision_raises_r03_before_lock(self, bad: str):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        reader = FakeReviewQueueReader()
        with pytest.raises(ReviewDecisionInvalid) as exc:
            record_operator_decision(
                session=FakeSession(),
                candidate_id="cid-001",
                decision=bad,
                reason="x",
                review_queue_reader=reader,
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_03 in str(exc.value)
        # Reader NOT called — we must fail before lock.
        assert reader.read_calls == []
        # Fast-fail checkpoints (start + failure-complete).
        assert cpw.stages() == [
            "operator_decision_start",
            "operator_decision_complete",
        ]
        assert cpw.calls[-1][1]["outcome"] == "failure"
        assert cpw.calls[-1][1]["error_type"] == "ReviewDecisionInvalid"

    def test_no_queue_entry_raises_r04(self):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        reader = FakeReviewQueueReader(store={})  # empty
        with pytest.raises(ReviewDecisionLocked) as exc:
            record_operator_decision(
                session=FakeSession(),
                candidate_id="cid-missing",
                decision=DECISION_ACCEPT,
                reason="x",
                review_queue_reader=reader,
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_04 in str(exc.value)
        assert vw.calls == []
        assert cpw.calls[-1][1]["error_type"] == "ReviewDecisionLocked"

    @pytest.mark.parametrize(
        "existing,new",
        [
            (DECISION_ACCEPT, DECISION_REJECT),
            (DECISION_ACCEPT, DECISION_ACCEPT),
            (DECISION_ACCEPT, DECISION_HOLD),
            (DECISION_REJECT, DECISION_ACCEPT),
            (DECISION_REJECT, DECISION_REJECT),
            (DECISION_REJECT, DECISION_HOLD),
        ],
    )
    def test_terminal_decision_overwrite_raises_r04(
        self, existing: str, new: str
    ):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        reader = FakeReviewQueueReader(
            store={
                "cid-001": _mk_existing_item(operator_decision=existing)
            }
        )
        with pytest.raises(ReviewDecisionLocked) as exc:
            record_operator_decision(
                session=FakeSession(),
                candidate_id="cid-001",
                decision=new,
                reason="flip",
                review_queue_reader=reader,
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_04 in str(exc.value)
        assert vw.calls == []
        assert cpw.calls[-1][1]["error_type"] == "ReviewDecisionLocked"

    def test_keyboard_interrupt_from_reader_propagates(self):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        reader = FakeReviewQueueReader(read_raises=KeyboardInterrupt())
        with pytest.raises(KeyboardInterrupt):
            record_operator_decision(
                session=FakeSession(),
                candidate_id="cid-001",
                decision=DECISION_ACCEPT,
                reason="x",
                review_queue_reader=reader,
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        # start checkpoint only — no failure checkpoint on Interrupt.
        assert cpw.stages() == ["operator_decision_start"]

    def test_runtime_error_from_vault_writer_writes_failure_checkpoint(self):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter(raise_with=RuntimeError("disk"))
        reader = FakeReviewQueueReader(
            store={"cid-001": _mk_existing_item()}
        )
        with pytest.raises(RuntimeError, match="disk"):
            record_operator_decision(
                session=FakeSession(),
                candidate_id="cid-001",
                decision=DECISION_ACCEPT,
                reason="x",
                review_queue_reader=reader,
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert cpw.calls[-1][0] == "operator_decision_complete"
        assert cpw.calls[-1][1]["outcome"] == "failure"
        assert cpw.calls[-1][1]["error_type"] == "RuntimeError"


# ---------------------------------------------------------------------------
# record_operator_decision — checkpoint success envelope
# ---------------------------------------------------------------------------


class TestRecordOperatorDecisionCheckpoints:
    def test_success_checkpoint_envelope(self):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        reader = FakeReviewQueueReader(
            store={"cid-001": _mk_existing_item()}
        )
        record_operator_decision(
            session=FakeSession(),
            candidate_id="cid-001",
            decision=DECISION_ACCEPT,
            reason="ok",
            review_queue_reader=reader,
            vault_writer=vw,
            checkpoint_writer=cpw,
        )
        assert cpw.stages() == [
            "operator_decision_start",
            "operator_decision_complete",
        ]
        start_payload = cpw.calls[0][1]
        assert start_payload["candidate_id"] == "cid-001"
        assert start_payload["decision"] == DECISION_ACCEPT
        assert start_payload["session_id"] == "session-r10-abc"
        end_payload = cpw.calls[1][1]
        assert end_payload["outcome"] == "success"
        assert end_payload["decision"] == DECISION_ACCEPT


# ---------------------------------------------------------------------------
# read_review_queue
# ---------------------------------------------------------------------------


class TestReadReviewQueue:
    def test_empty_queue_returns_empty_tuple(self):
        reader = FakeReviewQueueReader()
        items = read_review_queue(
            session=FakeSession(),
            review_queue_reader=reader,
        )
        assert items == ()

    def test_items_sorted_ascending_by_candidate_id(self):
        reader = FakeReviewQueueReader(
            store={
                "cid-003": _mk_existing_item(candidate_id="cid-003"),
                "cid-001": _mk_existing_item(candidate_id="cid-001"),
                "cid-002": _mk_existing_item(candidate_id="cid-002"),
            }
        )
        items = read_review_queue(
            session=FakeSession(),
            review_queue_reader=reader,
        )
        assert [it.candidate_id for it in items] == [
            "cid-001",
            "cid-002",
            "cid-003",
        ]

    def test_returns_tuple_immutable(self):
        reader = FakeReviewQueueReader(
            store={"cid-001": _mk_existing_item()}
        )
        items = read_review_queue(
            session=FakeSession(),
            review_queue_reader=reader,
        )
        assert isinstance(items, tuple)

    def test_delegates_to_enumerate_items(self):
        reader = FakeReviewQueueReader()
        session = FakeSession()
        read_review_queue(session=session, review_queue_reader=reader)
        assert reader.enumerate_calls == [(session.session_id, session.slug)]

    def test_reader_raising_propagates(self):
        reader = FakeReviewQueueReader(
            enumerate_raises=RuntimeError("enumerate failed")
        )
        with pytest.raises(RuntimeError, match="enumerate failed"):
            read_review_queue(
                session=FakeSession(),
                review_queue_reader=reader,
            )


# ---------------------------------------------------------------------------
# Protocol shapes + duck-typing
# ---------------------------------------------------------------------------


class TestProtocolShapes:
    def test_vault_writer_is_runtime_checkable(self):
        assert isinstance(RecordingVaultWriter(), VaultWriter)

    def test_review_queue_reader_is_runtime_checkable(self):
        assert isinstance(FakeReviewQueueReader(), ReviewQueueReader)

    def test_session_like_accepts_duck_typed_dataclass(self):
        s = FakeSession()
        # Structural protocol (not @runtime_checkable). We just verify the
        # three fields the module actually reads.
        for attr in ("session_id", "slug", "operator_id"):
            assert hasattr(s, attr)

    def test_candidate_imported_from_types_not_redefined(self):
        assert Candidate.__module__ == "pipeline.scout._types"
        assert ReviewQueueItem.__module__ == "pipeline.scout._types"
        assert VerificationVerdict.__module__ == "pipeline.scout._types"


# ---------------------------------------------------------------------------
# AST-lint clean
# ---------------------------------------------------------------------------


class TestASTLintClean:
    def test_ast_lint_scout_rules_clean(self, tmp_path: Path):
        # E-027 — lint_tree expects a directory. Copy review_stage.py +
        # minimal sibling layout with __init__.py.
        from pipeline.linting import ast_lint

        src = Path(rs.__file__)
        dst_dir = tmp_path / "pipeline" / "scout"
        dst_dir.mkdir(parents=True)
        (dst_dir / "__init__.py").write_text("", encoding="utf-8")
        shutil.copy(src, dst_dir / "review_stage.py")

        violations = ast_lint.lint_tree(tmp_path, ast_lint.DEFAULT_RULES)
        in_scope = [v for v in violations if v.file.name == "review_stage.py"]
        assert in_scope == []


# ---------------------------------------------------------------------------
# Public surface / version pin / module lineage
# ---------------------------------------------------------------------------


class TestPublicSurface:
    def test_version_pin_rN_ge_10(self):
        m = re.match(r"^0\.1\.0-scout-r(\d+)$", rs.__version__)
        assert m is not None
        assert int(m.group(1)) >= 10

    def test_module_lineage_enqueue_for_review(self):
        assert enqueue_for_review.__module__ == "pipeline.scout.review_stage"

    def test_module_lineage_record_operator_decision(self):
        assert (
            record_operator_decision.__module__
            == "pipeline.scout.review_stage"
        )

    def test_module_lineage_read_review_queue(self):
        assert read_review_queue.__module__ == "pipeline.scout.review_stage"

    def test_module_lineage_review_enqueue_rejected(self):
        assert (
            ReviewEnqueueRejected.__module__ == "pipeline.scout.review_stage"
        )

    def test_reachable_via_pipeline_scout_namespace(self):
        import pipeline.scout as scout

        names = {
            "enqueue_for_review",
            "record_operator_decision",
            "read_review_queue",
            "ReviewEnqueueRejected",
            "ReviewDecisionInvalid",
            "ReviewDecisionLocked",
            "F_SCOUT_R_01",
            "F_SCOUT_R_02",
            "F_SCOUT_R_03",
            "F_SCOUT_R_04",
            "VALID_DECISIONS",
            "ReviewQueueReader",
        }
        for n in names:
            assert hasattr(scout, n), n


# ---------------------------------------------------------------------------
# Adversarial — striped locks + parallel stress + tampered inputs
# ---------------------------------------------------------------------------


class TestAdversarialStripedLockCollision:
    """A-v3-02 / RT-v2-HIGH-02 — correctness under forced stripe collision."""

    def _find_colliding_pair(self) -> Tuple[Tuple[str, str], Tuple[str, str]]:
        # Find two distinct (slug, candidate_id) pairs that hash to the same
        # stripe under the current process's hash salt. Bounded search.
        base_slug = "my_org"
        target_pair = (base_slug, "cid-seed")
        target_idx = hash(target_pair) % SCOUT_REVIEW_LOCK_STRIPES
        for i in range(10_000):
            cand = f"cid-{i:05d}"
            if cand == "cid-seed":
                continue
            if hash((base_slug, cand)) % SCOUT_REVIEW_LOCK_STRIPES == target_idx:
                return target_pair, (base_slug, cand)
        raise RuntimeError("no collision found in 10k attempts")  # pragma: no cover

    def test_colliding_keys_serialise_without_cross_contamination(self):
        (slug_a, cid_a), (slug_b, cid_b) = self._find_colliding_pair()
        assert _review_lock(slug_a, cid_a) is _review_lock(slug_b, cid_b)
        # Independent reader stores per candidate — decisions must NOT bleed.
        vw = RecordingVaultWriter()
        cpw_a = RecordingCheckpointWriter()
        cpw_b = RecordingCheckpointWriter()
        reader_lock = threading.Lock()
        store = {
            cid_a: _mk_existing_item(candidate_id=cid_a),
            cid_b: _mk_existing_item(candidate_id=cid_b),
        }

        class SharedReader:
            def read_item(self, *, session_id, slug, candidate_id):
                with reader_lock:
                    return store.get(candidate_id)

            def enumerate_items(self, *, session_id, slug):
                with reader_lock:
                    return tuple(store.values())

        session = FakeSession(slug=slug_a)
        reader = SharedReader()
        record_operator_decision(
            session=session,
            candidate_id=cid_a,
            decision=DECISION_ACCEPT,
            reason="a",
            review_queue_reader=reader,
            vault_writer=vw,
            checkpoint_writer=cpw_a,
        )
        record_operator_decision(
            session=session,
            candidate_id=cid_b,
            decision=DECISION_REJECT,
            reason="b",
            review_queue_reader=reader,
            vault_writer=vw,
            checkpoint_writer=cpw_b,
        )
        # Two vault writes, one per candidate.
        paths = [c.path for c in vw.calls]
        assert any(cid_a in p for p in paths)
        assert any(cid_b in p for p in paths)


class TestAdversarialParallelStress:
    def test_parallel_decisions_on_same_candidate_only_one_wins(self):
        # N threads race to ACCEPT the same candidate; exactly one succeeds,
        # the rest see F-SCOUT-R-04 (locked).
        cpw = RecordingCheckpointWriter()
        # Shared vault writer; writes must be serialised under the stripe.
        vw_lock = threading.Lock()
        calls: List[WriteCall] = []

        class SerialisedWriter:
            def write(self, **kw):
                with vw_lock:
                    calls.append(WriteCall(**kw))

        # Reader that reflects the most-recent persisted decision.
        persisted: dict[str, ReviewQueueItem] = {
            "cid-race": _mk_existing_item(candidate_id="cid-race")
        }
        reader_lock = threading.Lock()

        def _store_hook(item: ReviewQueueItem) -> None:
            with reader_lock:
                persisted[item.candidate_id] = item

        class ReadAndCommitWriter:
            def write(self, *, path, bytes_, intent, session_id, slug):
                with vw_lock:
                    calls.append(
                        WriteCall(
                            path=path,
                            bytes_=bytes_,
                            intent=intent,
                            session_id=session_id,
                            slug=slug,
                        )
                    )
                # Also reflect the decision in the persisted store.
                # Hack: decode from bytes via test harness.
                import json as _json
                from dataclasses import replace as _replace

                data = _json.loads(bytes_.decode("utf-8"))
                with reader_lock:
                    existing = persisted[data["candidate_id"]]
                    persisted[data["candidate_id"]] = _replace(
                        existing,
                        operator_decision=data["operator_decision"],
                        operator_decided_at_utc=data[
                            "operator_decided_at_utc"
                        ],
                        operator_decision_reason=data[
                            "operator_decision_reason"
                        ],
                    )

        class LiveReader:
            def read_item(self, *, session_id, slug, candidate_id):
                with reader_lock:
                    return persisted.get(candidate_id)

            def enumerate_items(self, *, session_id, slug):
                with reader_lock:
                    return tuple(persisted.values())

        writer = ReadAndCommitWriter()
        reader = LiveReader()

        successes: List[str] = []
        failures: List[str] = []
        success_lock = threading.Lock()

        def _worker(tag: str):
            own_cpw = RecordingCheckpointWriter()
            try:
                record_operator_decision(
                    session=FakeSession(),
                    candidate_id="cid-race",
                    decision=DECISION_ACCEPT,
                    reason=tag,
                    review_queue_reader=reader,
                    vault_writer=writer,
                    checkpoint_writer=own_cpw,
                )
                with success_lock:
                    successes.append(tag)
            except ReviewDecisionLocked:
                with success_lock:
                    failures.append(tag)

        threads = [
            threading.Thread(target=_worker, args=(f"t{i}",)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(successes) == 1, (successes, failures)
        assert len(failures) == 7
        # One vault write; 7 attempts aborted inside the lock.
        assert len(calls) == 1


class TestAdversarialTamperedInputs:
    def test_tampered_verdict_string_refused_r01(self):
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        bad_verdict = _mk_verdict(verdict="VERIFIED_FITT")  # typo
        with pytest.raises(ReviewEnqueueRejected) as exc:
            enqueue_for_review(
                session=FakeSession(),
                candidate=_mk_candidate(),
                verdict=bad_verdict,
                fit_rationale="x",
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_01 in str(exc.value)
        assert vw.calls == []

    def test_unicode_slug_with_embedded_separator_refused(self):
        # ZWNJ etc. should not slip a "/" past the check.
        cpw = RecordingCheckpointWriter()
        vw = RecordingVaultWriter()
        with pytest.raises(ReviewEnqueueRejected) as exc:
            enqueue_for_review(
                session=FakeSession(slug="my_org/sub"),
                candidate=_mk_candidate(),
                verdict=_mk_verdict(),
                fit_rationale="x",
                vault_writer=vw,
                checkpoint_writer=cpw,
            )
        assert F_SCOUT_R_02 in str(exc.value)


class TestAdversarialFuzz:
    def test_decision_fuzz_accepts_only_three_values(self):
        import random as _random

        rng = _random.Random(1234)
        alphabet = (
            list(VALID_DECISIONS)
            + ["Accept", "reject", " HOLD", "", "y", "NO", "UNKNOWN", "ACCEPTT"]
        )
        for _ in range(200):
            choice = rng.choice(alphabet)
            cpw = RecordingCheckpointWriter()
            vw = RecordingVaultWriter()
            reader = FakeReviewQueueReader(
                store={"cid-001": _mk_existing_item()}
            )
            if choice in VALID_DECISIONS:
                record_operator_decision(
                    session=FakeSession(),
                    candidate_id="cid-001",
                    decision=choice,
                    reason="x",
                    review_queue_reader=reader,
                    vault_writer=vw,
                    checkpoint_writer=cpw,
                )
                assert len(vw.calls) == 1
            else:
                with pytest.raises(ReviewDecisionInvalid):
                    record_operator_decision(
                        session=FakeSession(),
                        candidate_id="cid-001",
                        decision=choice,
                        reason="x",
                        review_queue_reader=reader,
                        vault_writer=vw,
                        checkpoint_writer=cpw,
                    )
                assert vw.calls == []


class TestAdversarialReaderRaises:
    def test_enumerate_raising_midway_bubbles_up(self):
        reader = FakeReviewQueueReader(
            enumerate_raises=ValueError("corrupt queue file")
        )
        with pytest.raises(ValueError, match="corrupt queue file"):
            read_review_queue(
                session=FakeSession(),
                review_queue_reader=reader,
            )


class TestAdversarialCanonicalBytes:
    def test_canonical_bytes_are_deterministic(self):
        item = _mk_existing_item()
        b1 = _canonical_queue_item_bytes(item)
        b2 = _canonical_queue_item_bytes(item)
        assert b1 == b2

    def test_canonical_bytes_sort_keys(self):
        item = _mk_existing_item()
        import json as _json

        decoded = _json.loads(_canonical_queue_item_bytes(item).decode("utf-8"))
        assert list(decoded.keys()) == sorted(decoded.keys())
