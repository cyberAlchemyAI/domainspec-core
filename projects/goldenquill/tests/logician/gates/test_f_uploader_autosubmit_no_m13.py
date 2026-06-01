"""§12 Uploader F-UPLOADER-AUTOSUBMIT-ATTEMPTED — no M13 bypass.

MEDIUM-4 (§4 v2.7 pre-fix dispatch): the autosubmit gate is the only
Uploader gate without an M13 bypass. Per architecture v7.0.6, auto-submit
is *architecturally* prohibited, not policy-prohibited. An M13 bypass
would contradict the architecture; the gate is fail-closed with no
escape valve.

This test constructs a putative M13 bypass token, attempts to invoke the
gate with the token, and asserts:
  1. The gate refuses the bypass (still fails).
  2. A "no-bypass-attempted" admin-risk ledger entry is emitted.

Because the gate runner's M13 bypass surface is not yet wired (Cowork
slice), this test exercises the *contract* the runner must honor: the
gate predicate has no bypass parameter, no environment-variable hook,
no module-attribute toggle, and any attempt to plumb one in must trip
this test.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates.f_uploader_autosubmit_attempted import (
    F_UPLOADER_AUTOSUBMIT_ATTEMPTED,
    check_uploader_autosubmit_attempted,
)


@dataclass(frozen=True)
class _Output:
    submitted: bool


@dataclass(frozen=True)
class _M13Token:
    """Putative M13 bypass token. Not consumed by the gate predicate."""

    operator_signed_at: str
    rationale: str
    severity: str = "HIGH"


def test_gate_predicate_signature_has_no_bypass_parameter() -> None:
    """The gate predicate must not accept any bypass-flavored kwarg."""
    sig = inspect.signature(check_uploader_autosubmit_attempted)
    params = set(sig.parameters)
    forbidden = {
        "bypass",
        "m13_bypass",
        "m13_token",
        "operator_override",
        "force",
        "skip",
        "allow_submit",
        "override",
    }
    leaked = params & forbidden
    assert not leaked, (
        f"F-UPLOADER-AUTOSUBMIT-ATTEMPTED gained a bypass parameter "
        f"{leaked!r} — architectural prohibition compromised"
    )


def test_putative_m13_token_does_not_affect_outcome() -> None:
    """Even with an M13 token in scope, the gate refuses on submitted=True."""
    token = _M13Token(
        operator_signed_at="2026-05-09T00:00:00Z",
        rationale="emergency portal submission",
    )
    # Token is constructed but cannot be passed to the gate (no parameter).
    # This is the architectural contract — any code path that "remembers"
    # the token to skip the gate must be discoverable via static review.
    _ = token  # silence unused
    r = check_uploader_autosubmit_attempted(output=_Output(submitted=True))
    assert r.success is False
    assert r.failure_code == F_UPLOADER_AUTOSUBMIT_ATTEMPTED
    assert r.layer == "runtime_submitted_flag"


def test_admin_risk_ledger_entry_emitted_on_bypass_attempt() -> None:
    """Synthetic gate-runner contract: bypass attempt → ledger HIGH entry.

    Since the live ledger writer isn't on disk in this slice, we verify
    the contract via a synthetic runner that calls the gate and writes a
    ledger entry on every PRE-29 fire. The ledger entry must carry a
    distinguishable "no-bypass-attempted" tag.
    """
    ledger: list[dict] = []

    def _runner_with_ledger(
        *,
        output,
        m13_token: Optional[_M13Token] = None,
    ) -> dict:
        result = check_uploader_autosubmit_attempted(output=output)
        if not result.success:
            entry = {
                "code": result.failure_code,
                "severity": "HIGH",
                "tag": (
                    "no-bypass-attempted"
                    if m13_token is not None
                    else "autosubmit-attempt"
                ),
                "detail": result.detail,
            }
            ledger.append(entry)
        return {"result": result, "ledger_appended": ledger[-1:]}

    token = _M13Token(
        operator_signed_at="2026-05-09T00:00:00Z",
        rationale="emergency portal submission",
    )
    out = _runner_with_ledger(output=_Output(submitted=True), m13_token=token)
    assert out["result"].failure_code == F_UPLOADER_AUTOSUBMIT_ATTEMPTED
    assert ledger, "ledger must record the no-bypass-attempted entry"
    assert ledger[-1]["tag"] == "no-bypass-attempted"
    assert ledger[-1]["severity"] == "HIGH"
