"""pipeline.harness — canonical call sites for engineering-artifact gates.

The ``pipeline.harness.gates`` submodule wraps the v2.2 amendment-enforcement
gates (F-AMDT-02 / F-AMDT-03 / F-AMDT-12) at their canonical call boundaries
(committee verdict ingest, lock_history append). The wrappers are the *only*
sanctioned route — future dispatch scripts and LOCK ceremonies that bypass
them regress harness discipline and will show up as ungated activity in the
session-log audit.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_v2_2_consolidated_amendment.md``
(v2.2 LOCKED 2026-04-21, sha3_512[:16] ``1eb6610a1409fa58``).
"""

from __future__ import annotations

from pipeline.harness.gates import (
    AppendLockHistoryResult,
    BLUEPRINT_DEPS,
    GateDenied,
    LockHistoryAppendCallable,
    RecordVerdictResult,
    append_lock_history,
    record_verdict,
)

__all__ = [
    "AppendLockHistoryResult",
    "BLUEPRINT_DEPS",
    "GateDenied",
    "LockHistoryAppendCallable",
    "RecordVerdictResult",
    "append_lock_history",
    "record_verdict",
]
