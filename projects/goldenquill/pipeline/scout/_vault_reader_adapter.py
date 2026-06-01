"""Concrete :class:`VaultReader` adapter — the ONLY place Channel F touches
:mod:`pipeline.vault` directly.

Round 7 keeps :mod:`pipeline.scout.channel_f_websearch` stdlib-adjacent by
forbidding any direct ``pipeline.vault`` import inside the dispatcher. The
dispatcher consumes an injected :class:`VaultReader` Protocol; in production
the concrete binding is :class:`Section2VaultReader` — a thin adapter whose
``read`` method delegates to :func:`pipeline.vault.vault_query_skill.vault_read`
(or a caller-supplied callable in test paths).

Blueprint anchors:
- §4.6 Channel F — policy-file read via ``vault_read`` (A-08 closure).
- §2.5 IdentityTuple shape.

Pattern mirrors Round 6's :mod:`pipeline.scout._feedparser_adapter`: one
Protocol declared in the dispatcher module, one concrete sibling file.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


__all__ = [
    "IdentityTupleSnapshot",
    "Section2VaultReader",
]


@dataclass(frozen=True)
class IdentityTupleSnapshot:
    """Shape-compatible snapshot matching :class:`VaultReader` Protocol.

    Mirrors the duck-type declared in
    :class:`pipeline.scout.channel_f_websearch.IdentityTupleLike`. Exposes
    exactly the three attributes the post-read intent check reads.
    """

    intent: str
    session_id: str
    slug: str


_VaultReadCallable = Callable[..., "tuple[bytes, object]"]


class Section2VaultReader:
    """Adapter bridging Channel F to :mod:`pipeline.vault.vault_query_skill`.

    Lazy-imports the Section 2 module on first call so that
    :mod:`pipeline.scout` as a whole — and Round 7's channel_f_websearch.py
    in particular — does not pull the vault surface into ``sys.modules`` at
    Scout import-time.
    """

    def __init__(
        self,
        *,
        read_callable: Optional[_VaultReadCallable] = None,
    ) -> None:
        self._read_callable = read_callable

    def read(
        self,
        *,
        path: str,
        intent: str,
        session_id: str,
        slug: str,
    ) -> "tuple[bytes, IdentityTupleSnapshot]":
        if self._read_callable is None:
            # Lazy import — keeps pipeline.scout.channel_f_websearch free of
            # any pipeline.vault import at module scope.
            from pipeline.vault.vault_query_skill import (  # pragma: no cover
                vault_read as _real_vault_read,
            )

            self._read_callable = _real_vault_read

        data, identity = self._read_callable(  # type: ignore[misc]
            path=path,
            intent=intent,
            session_id=session_id,
            slug=slug,
        )
        snapshot = IdentityTupleSnapshot(
            intent=getattr(identity, "intent", ""),
            session_id=getattr(identity, "session_id", ""),
            slug=getattr(identity, "slug", ""),
        )
        return data, snapshot
