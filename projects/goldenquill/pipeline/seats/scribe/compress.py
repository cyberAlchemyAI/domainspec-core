"""pipeline.seats.scribe.compress — §7.10 word / character / page counters.

Blueprint §7 Scribe v1.1.1 §7.10 LOCKED 2026-04-21. Pure deterministic
counters. Zero I/O, zero LLM, zero external-package imports.

R2 ships the three count helpers + the ``is_over_limit`` predicate
consumed by :mod:`pipeline.seats.scribe.section_draft` invariants. The
actual compression / operator-ranking protocol (§7.10 steps 1-3) lands at
R3 alongside the seat subprocess entry.

Page counting at v0.1 uses a caller-supplied ``chars_per_page``; the
standard grant-template fallback is 3000 chars/page (≈ one single-spaced
page at 12pt), but the RFA template-specific value lives in the
``ProgramTemplate`` (§7.9) and is passed in by the seat. No blueprint
directive fixes a global default, so the keyword is required when a
``SectionLimit`` of ``limit_kind="pages"`` is in play.

Word counting uses Python's standard whitespace-split (``str.split()`` with
no arguments) — NFC-independent, locale-independent, and matches the
``.split()`` convention used across §7 blueprint examples. Word-count
numeric tokens (``"$12.50"``, ``"3.5%"``) count as single words; the
numeric-verbatim discipline lives in :mod:`.smart`, not here.

Character counting is ``len(text)`` — the Unicode code-point count, which
matches every RFA portal character-limit convention v0.1 has encountered
(Grants.gov character limits, state-portal textarea counts). NFC
normalization is a §7.4a canonicalization concern for conversation-anchor
hashing, NOT a character-count concern — operator-visible draft text is
not re-normalized before counting.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - imported only for type-checking
    from pipeline.seats.scribe.section_draft import SectionLimit


def count_words(text: str) -> int:
    """Return the whitespace-split word count of ``text``.

    Empty / whitespace-only strings yield 0. Mixed whitespace (tabs,
    newlines, NBSP-via-whitespace) collapses identically to
    :meth:`str.split` with no separator argument.
    """
    if not isinstance(text, str):
        raise TypeError(
            f"count_words(text) requires str; got {type(text).__name__!r}."
        )
    return len(text.split())


def count_characters(text: str) -> int:
    """Return the Unicode code-point count of ``text`` — ``len(text)``.

    Matches every v0.1 RFA portal character-limit convention. No NFC
    normalization here; draft text is counted as-displayed-to-operator.
    """
    if not isinstance(text, str):
        raise TypeError(
            f"count_characters(text) requires str; got {type(text).__name__!r}."
        )
    return len(text)


def count_pages(text: str, *, chars_per_page: int) -> int:
    """Return the ceiling-page count of ``text`` under ``chars_per_page``.

    A zero-length body yields 0 pages. A body of exactly ``chars_per_page``
    chars yields 1 page. A body of ``chars_per_page + 1`` yields 2. The
    RFA template-specific ``chars_per_page`` is supplied by the seat; no
    global default is defined at v0.1.

    Raises:
        ValueError: if ``chars_per_page`` is not a positive int.
    """
    if not isinstance(text, str):
        raise TypeError(
            f"count_pages(text, ...) requires str; got {type(text).__name__!r}."
        )
    if not isinstance(chars_per_page, int) or isinstance(chars_per_page, bool):
        raise TypeError(
            f"count_pages(chars_per_page) must be int; got "
            f"{type(chars_per_page).__name__!r}."
        )
    if chars_per_page <= 0:
        raise ValueError(
            f"count_pages(chars_per_page) must be a positive int; got "
            f"{chars_per_page!r}."
        )
    chars = len(text)
    if chars == 0:
        return 0
    # Ceiling division without math.ceil to keep imports stdlib-minimal.
    return (chars + chars_per_page - 1) // chars_per_page


def is_over_limit(
    text: str,
    limit: "SectionLimit",
    *,
    chars_per_page: int | None = None,
) -> bool:
    """Return True iff ``text`` exceeds ``limit`` under its ``limit_kind``.

    - ``limit_kind == "words"``: ``count_words(text) > limit.limit_value``.
    - ``limit_kind == "characters"``: ``count_characters(text) >
      limit.limit_value``.
    - ``limit_kind == "pages"``: ``count_pages(text,
      chars_per_page=chars_per_page) > limit.limit_value``; requires
      ``chars_per_page`` to be supplied (from the active
      :class:`ProgramTemplate`).

    Raises:
        ValueError: if ``limit.limit_kind == "pages"`` and
            ``chars_per_page`` is None.
    """
    kind = limit.limit_kind
    if kind == "words":
        return count_words(text) > limit.limit_value
    if kind == "characters":
        return count_characters(text) > limit.limit_value
    if kind == "pages":
        if chars_per_page is None:
            raise ValueError(
                "is_over_limit(..., limit.limit_kind='pages') requires a "
                "non-None chars_per_page keyword."
            )
        return (
            count_pages(text, chars_per_page=chars_per_page) > limit.limit_value
        )
    # Unreachable under LimitKind Literal closed-set; SectionLimit
    # construction already rejects any non-member value.
    raise ValueError(  # pragma: no cover - defensive
        f"is_over_limit: unrecognized limit.limit_kind={kind!r}."
    )


__all__ = [
    "count_words",
    "count_characters",
    "count_pages",
    "is_over_limit",
]
