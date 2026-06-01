"""Concrete :class:`FeedParserFactory` — the ONLY place ``feedparser`` is imported.

Round 6 keeps the dispatcher stdlib-adjacent by forbidding any direct import of
``feedparser`` inside :mod:`pipeline.scout.channel_e_rss`. Instead the dispatcher
accepts an injected :class:`FeedParserFactory` protocol; in production the
factory is :class:`FeedparserLibFactory`, whose :meth:`parse_streaming` body
imports ``feedparser`` lazily on the first call so that pure-test paths using
fakes never trigger the real library load.

Blueprint anchors:
- §4.5 Channel E — feedparser-dependent parse path (streaming entries +
  raw-body buffering).
- B-v5-04 closure — the drain helper probes ``raw_data`` / ``reset`` via
  :func:`hasattr`; this factory exposes a concrete handle carrying a mutable
  ``raw_data`` bytearray so path (i) of the drain is always available in
  production.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from pipeline.scout.channel_e_rss import FeedEntry, FeedParseResult


__all__ = [
    "FeedparserLibFactory",
    "FeedparserLibHandle",
]


@dataclass
class FeedparserLibHandle:
    """Handle object returned by :class:`FeedparserLibFactory`.

    Carries a mutable ``raw_data`` bytearray so :func:`_drain_parser_buffer`'s
    path (i) probe finds and zeroes it successfully. Also exposes
    :meth:`reset` for belt-and-braces coverage of path (ii).
    """

    raw_data: bytearray = field(default_factory=bytearray)

    def reset(self) -> None:  # pragma: no cover - defensive path (ii)
        self.raw_data = bytearray()


def _canonicalize_entry_body(entry: Any) -> bytes:
    """Canonicalise a feedparser entry's body bytes.

    Produces a stable byte sequence across feedparser versions:
    UTF-8 encoded; line endings normalised to ``\\n``; trailing whitespace
    stripped from each line; trailing empty lines dropped.
    """
    body_src = (
        entry.get("summary")
        or entry.get("description")
        or entry.get("content", [{}])[0].get("value", "")
        if isinstance(entry.get("content"), list)
        else entry.get("content", "")
    ) or entry.get("title", "")
    if isinstance(body_src, bytes):
        text = body_src.decode("utf-8", errors="replace")
    else:
        text = str(body_src)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines).encode("utf-8")


def _entry_iterator(parsed_entries: Any) -> Iterator[FeedEntry]:
    """Yield :class:`FeedEntry` rows from a feedparser ``entries`` list.

    Lazy generator — the dispatcher counts entry-start yields BEFORE building
    a :class:`Candidate`, so the 101st yield triggers the runaway break
    before this iterator constructs a body hash for entry 101.
    """
    for entry in parsed_entries:
        guid = entry.get("id", "") or entry.get("guid", "") or ""
        link = entry.get("link", "") or ""
        title = entry.get("title", "") or ""
        published_iso = entry.get("updated", "") or entry.get("published", "") or None
        body_bytes = _canonicalize_entry_body(entry)
        yield FeedEntry(
            guid=guid,
            link=link,
            title=title,
            body_bytes=body_bytes,
            published_iso=published_iso or None,
        )


class FeedparserLibFactory:
    """Concrete :class:`FeedParserFactory` wrapping the ``feedparser`` library.

    Imports ``feedparser`` lazily inside :meth:`parse_streaming` so that:
    * :mod:`pipeline.scout.channel_e_rss` does not pull ``feedparser`` into
      ``sys.modules`` at import-time (the import-hygiene test relies on it);
    * tests that use fake factories never load the real library.
    """

    def parse_streaming(self, raw_body: bytes) -> FeedParseResult:
        import feedparser  # Lazy — see module docstring rationale.

        parsed = feedparser.parse(raw_body)
        handle = FeedparserLibHandle(raw_data=bytearray(raw_body))

        feed_modified_iso = None
        feed_obj = getattr(parsed, "feed", None)
        if feed_obj is not None:
            candidate = feed_obj.get("updated") or feed_obj.get("published")
            if candidate:
                feed_modified_iso = str(candidate)

        return FeedParseResult(
            bozo=bool(getattr(parsed, "bozo", False)),
            feed_modified_iso=feed_modified_iso,
            entries=_entry_iterator(parsed.entries),
            raw_data_buffer_handle=handle,
            streaming=False,
        )
