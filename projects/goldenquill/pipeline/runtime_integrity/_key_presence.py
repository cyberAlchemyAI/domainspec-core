"""Key Presence preflight — §4.2.1 Row 22.

Blueprint §4 v2.5 LOCKED 2026-04-19.
Verifies each API key env var cited by router.yaml is present and non-empty
in the operator's environment. Runs once per pipeline start.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Final

BLUEPRINT_DEPS: Final[dict] = {
    "section_04_v2_4_v2_5_amendment.md": {
        "sections_implemented": ["§4.2.1 Row 22 key presence preflight"],
        "hash_source_version": "v2.5",
    },
}

F_KEY_PRESENCE_PREFLIGHT_FAIL: Final[str] = "F-KEY-PRESENCE-PREFLIGHT-FAIL"


@dataclass(frozen=True)
class KeyPresenceResult:
    """Result of the key presence preflight (§4.2.1 Row 22)."""

    all_present: bool
    failure_code: str | None
    missing_keys: tuple[str, ...] | None
    detail: dict[str, Any] | None


def check_key_presence(
    required_keys: dict[str, str],
    env: dict[str, str] | None = None,
) -> KeyPresenceResult:
    """Key Presence preflight (§4.2.1 Row 22). [LOCKED §4 v2.5]

    Parameters
    ----------
    required_keys : dict[str, str]
        Maps seat name → env var name. Caller (Section 5 orchestrator) derives
        this from router.yaml for the seats bound in the current run.
        Example: {"scribe": "ANTHROPIC_API_KEY", "judge": "GROQ_API_KEY"}.
    env : dict[str, str] | None
        Environment to check. Defaults to a snapshot of os.environ at call time.
        Injectable for testing. Note: the snapshot means env mutations between this
        preflight and the actual API call are not detected (acceptable in v0.1
        trusted-operator envelope; continuous monitoring is a v0.2 concern).

    Returns
    -------
    KeyPresenceResult
        all_present=True when all required keys are non-empty.
        failure_code set when any key is absent or empty.
    """
    environment = env if env is not None else dict(os.environ)

    absent: list[str] = []
    empty: list[str] = []

    for seat, env_var in required_keys.items():
        value = environment.get(env_var)
        if value is None:
            absent.append(env_var)
        elif value == "":
            empty.append(env_var)

    missing = absent + empty

    if missing:
        # Sub-tags per §6: .key_absent (env var not set) / .key_empty (env var set but empty).
        # Mixed case: absent takes precedence (absent is a superset failure of empty).
        sub_tag = "key_absent" if absent else "key_empty"
        return KeyPresenceResult(
            all_present=False,
            failure_code=F_KEY_PRESENCE_PREFLIGHT_FAIL,
            missing_keys=tuple(missing),
            detail={
                "sub_tag": sub_tag,
                "absent_vars": absent,
                "empty_vars": empty,
                "required_keys": required_keys,
            },
        )

    return KeyPresenceResult(
        all_present=True,
        failure_code=None,
        missing_keys=None,
        detail=None,
    )
