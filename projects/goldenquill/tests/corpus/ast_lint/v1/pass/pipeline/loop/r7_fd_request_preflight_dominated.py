"""Pass fixture R7 — fd_broker.request sink is CFG-dominated by a
module-scope ``typing.Final[bool]`` preflight sentinel with literal init
(the blueprint-faithful shape, B-v5-01)."""

from __future__ import annotations

from typing import Final

import fd_broker  # type: ignore[import-not-found]

PREFLIGHT_OK: Final[bool] = True


def run(host: str):
    if PREFLIGHT_OK:
        return fd_broker.request("https", host=host)
