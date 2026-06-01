"""F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED — PRE-write gate.

NEW per Cycle-2 RT-C2-02 closure (§13.16.6.2). The 8th gate in the §13 v1
LOCK roster.

Per §13.5.3 cross-channel opt-out propagation discipline: STOP/UNSUBSCRIBE
signal on ANY channel triggers an atomic write across ALL ledger entries
for that ``recipient_id``. The atomic update uses all-or-nothing
copy-on-write semantics:

  1. acquire ``fcntl.flock(LOCK_EX)`` on a workspace-level coordinator file
  2. snapshot the five ledger files' pre-state to a temp directory
  3. write new state to all five ledger files
  4. if ANY write fails, restore the temp snapshot back to canonical paths
     via ``os.rename`` (atomic per filesystem)
  5. release the coordinator lock

This gate fires when the propagation either fully fails (no rollback
attempted, partial state on disk) OR succeeds at rollback (consistent state
restored, but the propagation itself did not complete — operator must
re-issue the opt-out signal).

Sub-tags:

* ``.partial_propagation_no_rollback`` — propagation failed mid-flight AND
  rollback also failed; ledger files are in inconsistent state. CRITICAL —
  blocks ALL Data Collector cycles for this org until operator manually
  reconciles.
* ``.partial_propagation_rolled_back`` — propagation failed but rollback
  succeeded; ledger restored to pre-propagation state. Operator must
  re-issue the opt-out (the original STOP signal was effectively dropped).
* ``.coordinator_lock_acquisition_failed`` — could not acquire the
  workspace-level coordinator lock within timeout; propagation skipped to
  avoid corrupting state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional, Sequence

F_DATACOLLECTOR_OPT_OUT_PROPAGATION_FAILED: Final[str] = (
    "F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED"
)

SUB_TAG_PARTIAL_PROPAGATION_NO_ROLLBACK: Final[str] = (
    ".partial_propagation_no_rollback"
)
SUB_TAG_PARTIAL_PROPAGATION_ROLLED_BACK: Final[str] = (
    ".partial_propagation_rolled_back"
)
SUB_TAG_COORDINATOR_LOCK_ACQUISITION_FAILED: Final[str] = (
    ".coordinator_lock_acquisition_failed"
)


@dataclass(frozen=True, kw_only=True)
class OptOutPropagationResult:
    """Result of F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED check."""

    success: bool
    failure_code: Optional[str]
    sub_tag: Optional[str]
    detail: str
    recipient_id: Optional[str] = None
    failed_channels: tuple[str, ...] = ()
    rolled_back: bool = False


def check_opt_out_propagation_failed(
    *,
    recipient_id: str,
    coordinator_lock_acquired: bool,
    per_channel_write_results: Sequence[tuple[str, bool]],
    rollback_succeeded: Optional[bool] = None,
) -> OptOutPropagationResult:
    """PRE-write check on cross-channel opt-out propagation outcome.

    Parameters
    ----------
    recipient_id
        Per-recipient opaque identifier.
    coordinator_lock_acquired
        Whether the workspace-level coordinator ``fcntl.flock(LOCK_EX)`` was
        acquired within timeout.
    per_channel_write_results
        Sequence of ``(channel_name, success_bool)`` tuples — one per
        channel attempted in the propagation batch (typically all five).
    rollback_succeeded
        ``None`` if rollback not attempted (all writes succeeded);
        ``True`` if rollback restored pre-state; ``False`` if rollback
        itself failed (ledger files in inconsistent state).
    """
    if not coordinator_lock_acquired:
        return OptOutPropagationResult(
            success=False,
            failure_code=F_DATACOLLECTOR_OPT_OUT_PROPAGATION_FAILED,
            sub_tag=SUB_TAG_COORDINATOR_LOCK_ACQUISITION_FAILED,
            detail=(
                f"coordinator lock acquisition failed for "
                f"recipient={recipient_id!r}; propagation skipped to avoid "
                "corrupting ledger state — operator must re-issue opt-out"
            ),
            recipient_id=recipient_id,
        )
    failed = tuple(ch for ch, ok in per_channel_write_results if not ok)
    if not failed:
        return OptOutPropagationResult(
            success=True,
            failure_code=None,
            sub_tag=None,
            detail=(
                f"cross-channel opt-out propagation succeeded across all "
                f"{len(per_channel_write_results)} channels for "
                f"recipient={recipient_id!r}"
            ),
            recipient_id=recipient_id,
        )
    # Partial propagation occurred. Check rollback outcome.
    if rollback_succeeded is True:
        return OptOutPropagationResult(
            success=False,
            failure_code=F_DATACOLLECTOR_OPT_OUT_PROPAGATION_FAILED,
            sub_tag=SUB_TAG_PARTIAL_PROPAGATION_ROLLED_BACK,
            detail=(
                f"propagation failed on channels {list(failed)} for "
                f"recipient={recipient_id!r}; rollback succeeded — operator "
                "must re-issue opt-out signal"
            ),
            recipient_id=recipient_id,
            failed_channels=failed,
            rolled_back=True,
        )
    return OptOutPropagationResult(
        success=False,
        failure_code=F_DATACOLLECTOR_OPT_OUT_PROPAGATION_FAILED,
        sub_tag=SUB_TAG_PARTIAL_PROPAGATION_NO_ROLLBACK,
        detail=(
            f"propagation failed on channels {list(failed)} for "
            f"recipient={recipient_id!r}; rollback failed/not-attempted — "
            "ledger files in inconsistent state; admin-risk CRITICAL; "
            "blocks all DC cycles for this org until operator reconciles"
        ),
        recipient_id=recipient_id,
        failed_channels=failed,
        rolled_back=False,
    )


__all__ = [
    "F_DATACOLLECTOR_OPT_OUT_PROPAGATION_FAILED",
    "OptOutPropagationResult",
    "SUB_TAG_COORDINATOR_LOCK_ACQUISITION_FAILED",
    "SUB_TAG_PARTIAL_PROPAGATION_NO_ROLLBACK",
    "SUB_TAG_PARTIAL_PROPAGATION_ROLLED_BACK",
    "check_opt_out_propagation_failed",
]
