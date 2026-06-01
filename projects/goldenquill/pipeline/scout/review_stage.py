"""§4.8 REVIEW stage — human-gate enqueue + operator-decision path.

Scout Round 10. Implements architecture D.1 STAGE 3 verbatim per the
LOCKED blueprint §4.8 / §6.8 / §8. Consumes Round 9's
:class:`VerificationVerdict` (``verdict == "VERIFIED_FIT"`` only) and
emits one canonical-JSON :class:`ReviewQueueItem` record per candidate
via an injected :class:`VaultWriter`. Operator decisions flow through
:func:`record_operator_decision` under a fixed-length striped lock
array (``SCOUT_REVIEW_LOCK_STRIPES = 64``) — memory is O(stripes),
not O(candidates), closing A-v3-02 / RT-v2-HIGH-02 + MED-07.

Blueprint anchors:

- §4.8 REVIEW stage — primary implementation target. Two public
  entries (:func:`enqueue_for_review`, :func:`record_operator_decision`)
  plus a Logician-facing read helper (:func:`read_review_queue`).
- §6.8 F-SCOUT-R-01..04 — the only failure codes this module emits.
- §8 numeric pin: ``SCOUT_REVIEW_LOCK_STRIPES = 64``.
- A-10 / RT-v1-MED-04 — per-(slug, candidate_id) read-check-write
  serialisation via ``threading.Lock()``.
- A-v3-02 / RT-v2-HIGH-02 + MED-07 — striped 64-slot lock array
  ``_REVIEW_DECISION_LOCK_STRIPES`` replaces the unbounded dict. Hash
  collisions across distinct keys serialise unrelated decisions, which
  is a correctness no-op (decisions are idempotent once linearised).
- A-v3-04 / RT-v2-CRIT-02 + MED-01 — NFC-normalised post-read intent
  equality check via :func:`_assert_intent_matches` on every
  ``review-queue-read`` call-site.
- Architecture D.1 STAGE 3 (human gate — Scout never auto-files) —
  :func:`record_operator_decision` is the only function that may
  write ``operator_decision``. Scout's DISCOVER / VERIFY paths cannot
  reach this function; Pipeline (§5) routes operator invocation.
- Autonomy Rule 1 — checkpoint at ``review_enqueue_start`` +
  ``review_enqueue_complete`` (success AND failure) and at
  ``operator_decision_start`` + ``operator_decision_complete`` (both).

Spec-card deviation notes (from pre-staged
``spec_cards/scout_round_10_review_and_entity_research.md`` v1):

- Spec card proposed "anything else raises ``ReviewDecisionInvalid``
  BEFORE lock acquisition". Build honours this: input validation is
  performed at call top, before any stripe dispatch, so garbage
  decisions do not contend for locks.
- Spec card proposed F-SCOUT-R-04 raises *inside* the striped lock.
  Build honours this: the read-check-write is atomic under the
  per-(slug, candidate_id) stripe.
- Spec card proposed a ``ReviewQueueReader`` Protocol wrapping vault
  read. Build lands this Protocol at module scope; production binding
  wraps Section 2 ``vault_read`` under intent
  ``"review-queue-read"`` + NFC-normalised intent check. Tests inject
  an in-memory recorder.

No module-level side effects on import — no network, no disk, no
vault calls, no keystore resolution. All persistence routes through
injected Protocols (E-017 — ninth reuse in Scout). AST-lint
R1/R3/R4/R5 clean.
"""

from __future__ import annotations

import threading
import time
import unicodedata
from dataclasses import dataclass, replace
from typing import (
    Any,
    Callable,
    Final,
    Mapping,
    Optional,
    Protocol,
    runtime_checkable,
)

from pipeline.scout._constants import (
    DECISION_ACCEPT,
    DECISION_HOLD,
    DECISION_REJECT,
    INTENT_REVIEW_QUEUE_READ,
    INTENT_REVIEW_QUEUE_WRITE,
    SCOUT_REVIEW_LOCK_STRIPES,
    VERDICT_VERIFIED_FIT,
)
from pipeline.scout._types import (
    Candidate,
    ReviewQueueItem,
    VerificationVerdict,
)
from pipeline.sovereignty import canonical_json_bytes

__version__: Final[str] = "0.1.0-scout-r10"

__all__ = [
    "CheckpointWriter",
    "ClockFn",
    "F_SCOUT_R_01",
    "F_SCOUT_R_02",
    "F_SCOUT_R_03",
    "F_SCOUT_R_04",
    "IntentMismatch",
    "ReviewDecisionInvalid",
    "ReviewDecisionLocked",
    "ReviewEnqueueRejected",
    "ReviewQueueReader",
    "SessionLike",
    "VALID_DECISIONS",
    "VaultWriter",
    "_REVIEW_DECISION_LOCK_STRIPES",
    "_assert_intent_matches",
    "_review_lock",
    "__version__",
    "enqueue_for_review",
    "read_review_queue",
    "record_operator_decision",
]


# ---------------------------------------------------------------------------
# Failure codes (blueprint §6.8 — verbatim)
# ---------------------------------------------------------------------------

F_SCOUT_R_01: Final[str] = "F-SCOUT-R-01"  # non-VERIFIED_FIT enqueue
F_SCOUT_R_02: Final[str] = "F-SCOUT-R-02"  # path outside org root
F_SCOUT_R_03: Final[str] = "F-SCOUT-R-03"  # invalid decision value
F_SCOUT_R_04: Final[str] = "F-SCOUT-R-04"  # ACCEPT/REJECT already recorded


# ---------------------------------------------------------------------------
# Operator-decision domain (mirrors §2.4 ReviewQueueItem.operator_decision)
# ---------------------------------------------------------------------------

VALID_DECISIONS: Final[frozenset[str]] = frozenset({
    DECISION_ACCEPT,
    DECISION_REJECT,
    DECISION_HOLD,
})


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ReviewEnqueueRejected(Exception):
    """Enqueue refused by §4.8 pre-checks.

    Raised for:

    - F-SCOUT-R-01 — verdict is not ``VERIFIED_FIT`` (Law 5 compliance:
      UNVERIFIED / VERIFIED_NOT_FIT / VERIFICATION_FAILED all refused).
    - F-SCOUT-R-02 — computed queue path fails ``within_org_root``
      (defence-in-depth; Section 2 also validates).
    """


class ReviewDecisionInvalid(Exception):
    """F-SCOUT-R-03 — ``decision`` not in ``VALID_DECISIONS``.

    Raised at the top of :func:`record_operator_decision` BEFORE any
    stripe dispatch, so garbage input cannot contend for locks.
    """


class ReviewDecisionLocked(Exception):
    """F-SCOUT-R-04 — existing ACCEPT/REJECT being overwritten.

    Raised INSIDE the per-(slug, candidate_id) striped lock. Operator
    must use Section 4's admin-risk UNDO path to reverse a finalised
    decision. HOLD is not considered final — HOLD → ACCEPT / REJECT
    transitions pass through without F-SCOUT-R-04.
    """


class IntentMismatch(Exception):
    """Post-read intent-tuple drift on a ``review-queue-read`` call-site.

    Mirrors Channel B / Channel F pattern (F-SCOUT-B-05 / F-BT12-07).
    Strict-equality miss on ``(session_id, slug, intent)`` — NFC
    normalisation is tolerated with a reason-tag sub-code.
    """

    def __init__(self, *, code: str, reason_tag: str) -> None:
        self.code = code
        self.reason_tag = reason_tag
        super().__init__(f"{code}: {reason_tag}")


# ---------------------------------------------------------------------------
# Striped lock array (A-v3-02 / RT-v2-HIGH-02 + MED-07 closure)
#
# Memory is O(stripes), not O(candidates). 64 stripes give < 2% expected
# self-collision under a thousand concurrent unique keys (blueprint §4.8
# line 748). Hash collisions across distinct keys serialise unrelated
# decisions — correctness no-op because decisions are idempotent once
# linearised. ``PYTHONHASHSEED`` salts ``hash((slug, cid))`` per-process;
# we only require intra-run stability, not cross-process consistency.
# ---------------------------------------------------------------------------


_REVIEW_DECISION_LOCK_STRIPES: Final[list[threading.Lock]] = [
    threading.Lock() for _ in range(SCOUT_REVIEW_LOCK_STRIPES)
]


def _review_lock(slug: str, candidate_id: str) -> threading.Lock:
    """Return the stripe lock for a given (slug, candidate_id) pair.

    Blueprint §4.8 line 755-758 — ``hash(...) % SCOUT_REVIEW_LOCK_STRIPES``.
    The function is deliberately cheap (hash + modulo) and does not
    dereference any module-level state other than the lock array.
    """
    idx = hash((slug, candidate_id)) % SCOUT_REVIEW_LOCK_STRIPES
    return _REVIEW_DECISION_LOCK_STRIPES[idx]


# ---------------------------------------------------------------------------
# Injection Protocols (E-017 — ninth Scout firing)
# ---------------------------------------------------------------------------


class SessionLike(Protocol):
    """Duck-type shape this module needs from a sovereignty session.

    Mirrors the shape used by Round 9's :mod:`verify_stage`. The full
    Section 1 Session satisfies this Protocol without adapter code;
    tests inject a plain dataclass with the three string fields.
    """

    session_id: str
    slug: str
    operator_id: str


@runtime_checkable
class VaultWriter(Protocol):
    """Section 2 ``vault_write`` seam (E-017 reuse).

    Production binding wraps :func:`pipeline.vault.vault_write.vault_write`
    with path validation and identity tuple assembly. Tests inject a
    recorder that captures ``(path, bytes_, intent, session_id, slug)``
    tuples for assertion.

    The module never constructs filesystem bytes itself; canonical-JSON
    is computed via :func:`canonical_json_bytes` over the
    :class:`ReviewQueueItem` asdict form, then handed to
    ``vault_write``. This keeps the module AST-lint R1 clean — no
    ``open(`` / ``Path.write_text`` / ``os.write`` call-site.
    """

    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None: ...


@runtime_checkable
class ReviewQueueReader(Protocol):
    """Logician-facing ``vault_read`` seam for review queue enumeration.

    Production binding wraps Section 2 ``vault_read`` under intent
    ``"review-queue-read"`` with NFC-normalised
    :func:`_assert_intent_matches`. Tests inject an in-memory recorder
    that returns a mapping of ``candidate_id → ReviewQueueItem`` plus
    the identity-tuple triple on every read.

    ``read_item`` returns ``None`` when the candidate has no queue
    entry (used by the read-check-write path). ``enumerate_items``
    returns the full queue for Logician PRE-gate traversal.
    """

    def read_item(
        self,
        *,
        session_id: str,
        slug: str,
        candidate_id: str,
    ) -> Optional[ReviewQueueItem]: ...

    def enumerate_items(
        self,
        *,
        session_id: str,
        slug: str,
    ) -> tuple[ReviewQueueItem, ...]: ...


class CheckpointWriter(Protocol):
    """Autonomy Rule 1 — save state always.

    Production binding wraps
    :func:`pipeline.sovereignty.interrupted_state.checkpoint`. Tests
    inject an in-memory recorder that captures ``(stage, payload)``
    tuples for assertion.
    """

    def write(self, *, stage: str, payload: Mapping[str, Any]) -> None: ...


ClockFn = Callable[[], str]
"""Clock returning UTC-aware ISO-8601 string.

Production default binds to
``lambda: datetime.datetime.now(UTC).isoformat().replace("+00:00","Z")``.
Tests inject a :class:`MockClock` that returns a fixed sequence.
"""


def _default_clock() -> str:
    import datetime as _dt

    return _dt.datetime.now(_dt.timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# NFC-normalised intent check (A-v3-04 / RT-v2-CRIT-02 + MED-01 closure)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class _ReadIdentity:
    """Minimal identity-tuple shape for :func:`_assert_intent_matches`.

    Mirrors the shape returned by Section 2 ``vault_read`` and the
    Channel B / Channel F post-read check pattern.
    """

    session_id: str
    slug: str
    intent: str


def _assert_intent_matches(
    *,
    expected_intent: str,
    observed_intent: str,
    expected_session_id: str,
    observed_session_id: str,
    expected_slug: str,
    observed_slug: str,
) -> None:
    """Strict-equality check; NFC drift raises with a sub-code reason tag.

    Raises :class:`IntentMismatch` on any mismatch. The ``code`` field
    is ``review-queue-intent-mismatch`` for session/slug drift,
    ``review-queue-intent-nfc-drift`` for NFC-normalised drift, and
    ``review-queue-intent-mismatch`` for any other string divergence.

    Mirrors the Channel B / Channel F pattern — defence-in-depth
    against a silently buggy vault that tolerated an intent mismatch.
    """
    if observed_session_id != expected_session_id:
        raise IntentMismatch(
            code="review-queue-intent-mismatch",
            reason_tag=(
                f"session_id_mismatch:expected={expected_session_id!r} "
                f"got={observed_session_id!r}"
            ),
        )
    if observed_slug != expected_slug:
        raise IntentMismatch(
            code="review-queue-intent-mismatch",
            reason_tag=(
                f"slug_mismatch:expected={expected_slug!r} "
                f"got={observed_slug!r}"
            ),
        )
    if observed_intent == expected_intent:
        return
    normalized = unicodedata.normalize("NFC", observed_intent).strip()
    if normalized == expected_intent:
        raise IntentMismatch(
            code="review-queue-intent-nfc-drift",
            reason_tag=f"intent_nfc_drift:{observed_intent!r}",
        )
    raise IntentMismatch(
        code="review-queue-intent-mismatch",
        reason_tag=f"intent_mismatch:{observed_intent!r}",
    )


# ---------------------------------------------------------------------------
# Path computation helpers
# ---------------------------------------------------------------------------


def _review_queue_path(slug: str, candidate_id: str) -> str:
    """Blueprint §4.8 — ``{slug}/review_queue/{candidate_id}.json``.

    Path computation only; caller passes the result to
    ``vault_write``/``vault_read`` which validate org-root containment.
    The string form avoids a ``pathlib`` dependency and is Section 2's
    canonical shape for vault paths.
    """
    return f"{slug}/review_queue/{candidate_id}.json"


def _canonical_queue_item_bytes(item: ReviewQueueItem) -> bytes:
    """Canonical-JSON bytes for a :class:`ReviewQueueItem`.

    Uses :func:`canonical_json_bytes` over ``asdict(item)`` with the
    normalisation pass already applied by
    :func:`pipeline.scout._types._normalize_for_json` via the
    canonical-bytes helpers. Queue items are plain-Python structures
    (no bytes / frozensets), so direct ``asdict`` is safe.
    """
    from dataclasses import asdict

    return canonical_json_bytes(asdict(item))


# ---------------------------------------------------------------------------
# Public entry — enqueue_for_review
# ---------------------------------------------------------------------------


def enqueue_for_review(
    *,
    session: SessionLike,
    candidate: Candidate,
    verdict: VerificationVerdict,
    fit_rationale: str,
    vault_writer: VaultWriter,
    checkpoint_writer: CheckpointWriter,
    clock: ClockFn = _default_clock,
) -> ReviewQueueItem:
    """Blueprint §4.8 ``enqueue_for_review`` — human-gate enqueue.

    Pre-checks (in order, each raising
    :class:`ReviewEnqueueRejected` on failure):

    1. ``verdict.verdict == "VERIFIED_FIT"`` — Law 5 compliance;
       F-SCOUT-R-01 otherwise.
    2. Computed ``_review_queue_path`` (defensive — Section 2 also
       validates). F-SCOUT-R-02 if the path string is malformed (empty
       slug or candidate_id).

    On success, constructs a :class:`ReviewQueueItem` with
    ``operator_decision=None`` (decision path is
    :func:`record_operator_decision`) and writes canonical-JSON bytes
    via ``vault_writer`` under intent ``"review-queue-write"``.

    Autonomy Rule 1: ``review_enqueue_start`` + ``review_enqueue_complete``
    checkpoints land on every exit path including exceptions.

    :raises ReviewEnqueueRejected: F-SCOUT-R-01 / F-SCOUT-R-02.
    :raises Exception: any exception from the injected
        :class:`VaultWriter` propagates unchanged after the failure
        checkpoint has been written (Rule 1).
    """
    checkpoint_writer.write(
        stage="review_enqueue_start",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "candidate_id": candidate.candidate_id,
            "verdict": verdict.verdict,
        },
    )

    try:
        if verdict.verdict != VERDICT_VERIFIED_FIT:
            raise ReviewEnqueueRejected(
                f"{F_SCOUT_R_01}: only VERIFIED_FIT enqueues; "
                f"got verdict={verdict.verdict!r}"
            )
        if not session.slug or not candidate.candidate_id:
            raise ReviewEnqueueRejected(
                f"{F_SCOUT_R_02}: path outside org root "
                f"(empty slug={session.slug!r} or "
                f"candidate_id={candidate.candidate_id!r})"
            )
        path = _review_queue_path(session.slug, candidate.candidate_id)
        # Defence-in-depth: reject paths that escape the org root
        # via "." / ".." / absolute prefixes. Section 2 also validates,
        # but the blueprint calls the check out explicitly (§4.8 line 712).
        if (
            ".." in candidate.candidate_id
            or "/" in candidate.candidate_id
            or candidate.candidate_id.startswith(".")
            or ".." in session.slug
            or "/" in session.slug
        ):
            raise ReviewEnqueueRejected(
                f"{F_SCOUT_R_02}: path outside org root "
                f"(slug={session.slug!r} candidate_id={candidate.candidate_id!r})"
            )

        item = ReviewQueueItem(
            candidate_id=candidate.candidate_id,
            queued_at_utc=clock(),
            queued_by_verdict=VERDICT_VERIFIED_FIT,
            candidate_snapshot=candidate,
            verification_snapshot=verdict,
            fit_rationale=fit_rationale,
            operator_decision=None,
            operator_decided_at_utc=None,
            operator_decision_reason=None,
        )
        vault_writer.write(
            path=path,
            bytes_=_canonical_queue_item_bytes(item),
            intent=INTENT_REVIEW_QUEUE_WRITE,
            session_id=session.session_id,
            slug=session.slug,
        )
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as exc:
        checkpoint_writer.write(
            stage="review_enqueue_complete",
            payload={
                "session_id": session.session_id,
                "slug": session.slug,
                "candidate_id": candidate.candidate_id,
                "outcome": "failure",
                "error_type": type(exc).__name__,
            },
        )
        raise

    checkpoint_writer.write(
        stage="review_enqueue_complete",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "candidate_id": candidate.candidate_id,
            "outcome": "success",
        },
    )
    return item


# ---------------------------------------------------------------------------
# Public entry — record_operator_decision
# ---------------------------------------------------------------------------


def record_operator_decision(
    *,
    session: SessionLike,
    candidate_id: str,
    decision: str,
    reason: str,
    review_queue_reader: ReviewQueueReader,
    vault_writer: VaultWriter,
    checkpoint_writer: CheckpointWriter,
    clock: ClockFn = _default_clock,
) -> ReviewQueueItem:
    """Blueprint §4.8 ``record_operator_decision`` — operator-gate path.

    Input validation (no lock held):

    - ``decision in VALID_DECISIONS`` — :class:`ReviewDecisionInvalid`
      (F-SCOUT-R-03) otherwise. Fast-fail to avoid lock contention on
      garbage input.

    Under the per-(slug, candidate_id) striped lock:

    1. Read existing queue item via ``review_queue_reader.read_item``.
       If the candidate has no queue entry, the caller is invoking
       the decision path out of sequence — surface this as an
       F-SCOUT-R-04 ``no_queue_entry`` reason tag inside
       :class:`ReviewDecisionLocked`.
    2. Refuse overwrite of an existing ``ACCEPT`` / ``REJECT``.
       HOLD → any is permitted (HOLD is not a terminal state).
    3. ``replace(existing, operator_decision=decision, ...)`` and
       ``vault_writer.write`` under intent ``"review-queue-write"``.

    Autonomy Rule 1: ``operator_decision_start`` +
    ``operator_decision_complete`` checkpoints land on every exit path.

    :raises ReviewDecisionInvalid: F-SCOUT-R-03 — BEFORE lock.
    :raises ReviewDecisionLocked: F-SCOUT-R-04 — INSIDE lock.
    """
    checkpoint_writer.write(
        stage="operator_decision_start",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "candidate_id": candidate_id,
            "decision": decision,
        },
    )

    if decision not in VALID_DECISIONS:
        checkpoint_writer.write(
            stage="operator_decision_complete",
            payload={
                "session_id": session.session_id,
                "slug": session.slug,
                "candidate_id": candidate_id,
                "outcome": "failure",
                "error_type": "ReviewDecisionInvalid",
            },
        )
        raise ReviewDecisionInvalid(
            f"{F_SCOUT_R_03}: decision={decision!r} not in "
            f"{sorted(VALID_DECISIONS)!r}"
        )

    lock = _review_lock(session.slug, candidate_id)
    try:
        with lock:
            existing = review_queue_reader.read_item(
                session_id=session.session_id,
                slug=session.slug,
                candidate_id=candidate_id,
            )
            if existing is None:
                raise ReviewDecisionLocked(
                    f"{F_SCOUT_R_04}: no queue entry for "
                    f"candidate_id={candidate_id!r} — enqueue first"
                )
            if existing.operator_decision in {DECISION_ACCEPT, DECISION_REJECT}:
                raise ReviewDecisionLocked(
                    f"{F_SCOUT_R_04}: decision already recorded "
                    f"(existing={existing.operator_decision!r}); "
                    f"use admin-risk UNDO path"
                )
            updated = replace(
                existing,
                operator_decision=decision,
                operator_decided_at_utc=clock(),
                operator_decision_reason=reason,
            )
            vault_writer.write(
                path=_review_queue_path(session.slug, candidate_id),
                bytes_=_canonical_queue_item_bytes(updated),
                intent=INTENT_REVIEW_QUEUE_WRITE,
                session_id=session.session_id,
                slug=session.slug,
            )
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as exc:
        checkpoint_writer.write(
            stage="operator_decision_complete",
            payload={
                "session_id": session.session_id,
                "slug": session.slug,
                "candidate_id": candidate_id,
                "outcome": "failure",
                "error_type": type(exc).__name__,
            },
        )
        raise

    checkpoint_writer.write(
        stage="operator_decision_complete",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "candidate_id": candidate_id,
            "outcome": "success",
            "decision": decision,
        },
    )
    return updated


# ---------------------------------------------------------------------------
# Public entry — read_review_queue (Logician-facing)
# ---------------------------------------------------------------------------


def read_review_queue(
    *,
    session: SessionLike,
    review_queue_reader: ReviewQueueReader,
) -> tuple[ReviewQueueItem, ...]:
    """Blueprint §4.8 / §3.5 — Logician-facing review-queue enumeration.

    Returns the full queue as a tuple sorted ascending by
    ``candidate_id`` for determinism. Logician's PRE-gate consumes the
    returned tuple to enforce the "no Scribe draft unless review queue
    item is ACCEPT" invariant (blueprint §4.8 line 790).

    The underlying ``vault_read`` is wrapped by the injected
    :class:`ReviewQueueReader`, which runs the NFC-normalised
    :func:`_assert_intent_matches` check post-read. An intent drift
    bubbles up as :class:`IntentMismatch` — the caller aborts.
    """
    items = review_queue_reader.enumerate_items(
        session_id=session.session_id,
        slug=session.slug,
    )
    return tuple(sorted(items, key=lambda it: it.candidate_id))


# ---------------------------------------------------------------------------
# Side-effect-free import invariant
# ---------------------------------------------------------------------------


# Retain module-level reference to ``time`` so linters do not strip the
# import; the module uses monotonic time via injected Protocols rather
# than direct call-sites, so the import is logically reserved for
# test-injected clock shims (mirrors Round 9 pattern).
_ = time  # noqa: F841
