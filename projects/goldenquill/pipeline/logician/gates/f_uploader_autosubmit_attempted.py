"""F-UPLOADER-AUTOSUBMIT-ATTEMPTED — PRE-gate. NO M13 BYPASS.

Per Blueprint §12.9.3 + §4 v2.7 amendment. Architecturally prohibited mode
per architecture v7.0.6 (Uploader = "prepare-and-stage discipline only —
operator clicks final submit on funder portal"). An M13 bypass would
contradict the architecture; gate is fail-closed with no escape valve.

Three-layer defense
-------------------
1. **AST-lint R-UPLOADER-NO-SUBMIT** (CI + LOCK ceremony) — static analysis
   of `pipeline/orchestrator/seats/uploader.py` and all files under
   `pipeline/orchestrator/seats/uploader_adapters/` rejects any
   `requests.post`, `requests.put`, `httpx.post`, `httpx.put`,
   `urllib.request.urlopen` with method POST/PUT, or function calls to
   names matching `submit|send|post_to_portal|upload_to_portal`.
2. **Cedar policy** `uploader_no_submit.cedar` — denies any Vault write
   intent containing `submission_api_call` in metadata.
3. **Runtime assertion** — `UploaderOutput.__post_init__` asserts
   `self.submitted is False`. The `submitted` field is structurally always
   False; any code path that flips it triggers AssertionError before the
   output is persisted.

This gate predicate exposes layer-2 / layer-3 surface checks that the
gate runner invokes per Uploader output emission. AST-lint is a separate
CI surface and is not invoked from this predicate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable


F_UPLOADER_AUTOSUBMIT_ATTEMPTED: str = "F-UPLOADER-AUTOSUBMIT-ATTEMPTED"


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class AutosubmitAttemptedResult:
    """Result of F-UPLOADER-AUTOSUBMIT-ATTEMPTED check."""

    success: bool
    failure_code: Optional[str]
    layer: Optional[str]  # "runtime_submitted_flag" | "cedar_intent" | None
    detail: str


# ---------------------------------------------------------------------------
# Injected protocols
# ---------------------------------------------------------------------------


@runtime_checkable
class _UploaderOutput(Protocol):
    submitted: bool


@runtime_checkable
class _CedarIntentReader(Protocol):
    """Returns metadata-key set for any Vault write intent in this run."""

    def __call__(self) -> set[str]: ...


# ---------------------------------------------------------------------------
# Gate predicate
# ---------------------------------------------------------------------------


_FORBIDDEN_INTENT_KEY: str = "submission_api_call"


def check_uploader_autosubmit_attempted(
    *,
    output: _UploaderOutput,
    cedar_intent_reader: Optional[_CedarIntentReader] = None,
) -> AutosubmitAttemptedResult:
    """PRE-gate: Uploader output must never carry submitted=True; no Cedar intent."""
    # Layer 3 — runtime assertion equivalent. Use ``is True`` (clearer than
    # ``is not False``); ``submitted`` is annotated ``bool`` so the only
    # other value is False, but explicit positive identity reads better.
    if output.submitted is True:
        return AutosubmitAttemptedResult(
            success=False,
            failure_code=F_UPLOADER_AUTOSUBMIT_ATTEMPTED,
            layer="runtime_submitted_flag",
            detail=(
                "UploaderOutput.submitted is True — auto-submit "
                "is architecturally prohibited (no M13 bypass)."
            ),
        )
    # Layer 2 — Cedar intent metadata sweep (only when reader supplied)
    if cedar_intent_reader is not None:
        try:
            intent_keys = cedar_intent_reader()
        except Exception as exc:  # fail-closed on reader failure
            return AutosubmitAttemptedResult(
                success=False,
                failure_code=F_UPLOADER_AUTOSUBMIT_ATTEMPTED,
                layer="cedar_intent",
                detail=f"cedar_intent_reader raised: {exc!r}",
            )
        if _FORBIDDEN_INTENT_KEY in intent_keys:
            return AutosubmitAttemptedResult(
                success=False,
                failure_code=F_UPLOADER_AUTOSUBMIT_ATTEMPTED,
                layer="cedar_intent",
                detail=(
                    f"Vault write intent contains forbidden key "
                    f"{_FORBIDDEN_INTENT_KEY!r}; auto-submit "
                    "architecturally prohibited (no M13 bypass)."
                ),
            )
    return AutosubmitAttemptedResult(
        success=True,
        failure_code=None,
        layer=None,
        detail="no auto-submit code path detected",
    )
