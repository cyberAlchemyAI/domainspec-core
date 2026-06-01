"""R-UPLOADER-NO-SUBMIT — aliased httpx.post call (must fire).

The classic regex-blocklist bypass: ``from httpx import post as p``
followed by ``p(url, ...)``. The shared _AliasResolver collapses ``p``
to ``attr:httpx.post``, which is not on the allow-list, so the rule
fires.
"""

from __future__ import annotations

from httpx import post as p


def submit(url: str, payload: bytes) -> None:
    p(url, content=payload)
