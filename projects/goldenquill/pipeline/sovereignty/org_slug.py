"""Org slug canonicalization. [§4.3 M3]

Deterministic canonicalization prevents path-level isolation evasion via
slug-case tricks or Unicode homoglyphs (Law 3 enforcement).

Public API (exported via pipeline.sovereignty.__all__):
  - canonical_slug(s)              # the 12-step canonicalization
  - ensure_slug_available(slug, repo_root)   # collision detection
  - InvalidSlug, ReservedSlug, SlugCollisionError

Blueprint references:
  §4.3 M3 — canonicalization algorithm (v2 — hardens against v1 whitespace + lossy transliteration)
  §3.6    — public interface

Futureproofing:
  §4.1 Public API — InvalidSlug / ReservedSlug / SlugCollisionError are
        stable exception types; downstream catches by these names
  §4.6 Blueprint-code drift — BLUEPRINT_DEPS declared below
  §4.9 Regression corpus — tests/corpus/org_slug/v1/ preserves inputs
        that triggered v1 → v2 hardening; v2 must still reject them
"""

from __future__ import annotations

import unicodedata
from pathlib import Path

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": ["§4.3 M3", "§3.6"],
        "hash_at_lock": None,  # populated at committee LOCK
        "hash_source_version": "v6",
    },
}

__all__ = [
    "InvalidSlug",
    "ReservedSlug",
    "SlugCollisionError",
    "canonical_slug",
    "ensure_slug_available",
]

# Reserved slug names that MUST NOT be allocable to any org.
# Per §4.3 step 12 — v2 hardening.
_RESERVED_SLUGS: frozenset[str] = frozenset({
    ".",
    "..",
    "index",
    "shared",
    "vault_shared",
    "_template",
    ".git",
    ".well_known",
})

# Maximum slug length in characters. Per §4.3 step 11.
_MAX_SLUG_LENGTH = 64


class InvalidSlug(ValueError):
    """Raised when a candidate slug fails any §4.3 step 1-11 check.

    Subclasses ValueError so downstream `except ValueError:` catches it;
    specific `except InvalidSlug:` catches are also supported.

    Attributes vary by the specific failure (`reason`), set via the
    constructor's kwargs — e.g. `InvalidSlug("transliteration_lossy",
    original=..., transliterated=...)`.
    """

    def __init__(self, reason: str, **details: str) -> None:
        super().__init__(reason)
        self.reason = reason
        self.details = details


class ReservedSlug(InvalidSlug):
    """Raised when a candidate resolves to a reserved slug per §4.3 step 12.

    Distinct subclass so `except ReservedSlug:` can handle this case
    specifically (e.g., suggest a non-reserved alternative).
    """

    def __init__(self, reserved_name: str) -> None:
        super().__init__("reserved_slug", reserved_name=reserved_name)


class SlugCollisionError(RuntimeError):
    """Raised when `ensure_slug_available` finds the slug already exists.

    Distinct from InvalidSlug because the slug itself is valid — it's
    just taken. Caller decides whether to retry with a variant or surface
    to the operator.
    """

    def __init__(self, slug: str, existing_path: Path) -> None:
        super().__init__(
            f"slug {slug!r} already present at {existing_path}"
        )
        self.slug = slug
        self.existing_path = existing_path


def canonical_slug(s: str) -> str:
    """Canonicalize an org slug deterministically. [§4.3 M3, v2 algorithm]

    Applies the blueprint's 12-step sequence in exact order. Each step's
    rationale is documented inline. The order matters — reversing whitespace
    strip and the reserved-name check (v1 bug) silently admitted `" .git "`.

    :param s: raw slug candidate
    :returns: canonicalized slug (lowercase, `[a-z0-9-]`, non-empty, len ≤ 64)
    :raises InvalidSlug: for rules 1-11 failures (empty, lossy transliteration,
                         all-non-alphanum, length)
    :raises ReservedSlug: for rule 12 (the 8 reserved names)
    :raises TypeError: if s is not a str

    Examples:
      "MycoSymbiotics Cooperative"  → "mycosymbiotics-cooperative"
      "FIT Farms, Inc."             → "fit-farms-inc"
      "Run-a-Muck!"                 → "run-a-muck"
      "mycosymbiotics_cooperative"  → "mycosymbiotics-cooperative"

    Rejects:
      " .git "                      → ReservedSlug (v2 fix — v1 accepted this)
      "café"                        → InvalidSlug("transliteration_lossy")
      ""                            → InvalidSlug("empty")
      "!!!"                         → InvalidSlug("all_non_alphanum")
      "a" * 65                      → InvalidSlug("too_long")
    """
    # Step 1: reject non-string input with TypeError (defensive).
    if not isinstance(s, str):
        raise TypeError(
            f"canonical_slug requires str; got {type(s).__name__}"
        )

    # Step 2: strip surrounding whitespace BEFORE any other check.
    # v2 FIX — v1 omitted this, allowing " .git " to bypass step 12's
    # reserved-name table.
    s_stripped = s.strip()

    # Step 3: reject empty after strip.
    if not s_stripped:
        raise InvalidSlug("empty")

    # Step 4: NFC normalize.
    s_nfc = unicodedata.normalize("NFC", s_stripped)

    # Step 5: NFKD decompose + ASCII encode (ignore non-ASCII).
    # This transliterates combining-mark compositions; "café" (é as e + ◌́)
    # → "cafe" because the combining acute is non-ASCII and gets ignored.
    s_after_nfkd = unicodedata.normalize("NFKD", s_nfc)
    s_ascii_raw = s_after_nfkd.encode("ascii", "ignore").decode("ascii")

    # Step 6: v2 FIX — lossy-transliteration rejection.
    # Round-A Committee finding RT-v1-H-01 (GPT-OSS-120B 2026-04-19):
    # the earlier "post-NFKD non-ASCII + shrink" formulation failed on
    # Unicode codepoints that NFKD-decompose directly to pure ASCII
    # without a combining-mark residue — e.g. `Å` (U+212B ANGSTROM SIGN)
    # → NFKD → `A`. Such inputs collapse to the same slug as the pure-
    # ASCII `A`, violating Law 3 distinctness.
    #
    # v3 rule (tightened): reject if the NFC form of the input contains
    # ANY non-ASCII codepoint at all. Strictly stronger than the
    # blueprint §4.3 step 6 formula; preserves the blueprint's stated
    # design intent ("prevents distinct org names collapsing to the
    # same slug"). Operators who want a transliterated slug must
    # explicitly Latinize their input before passing it in.
    #
    # Drift notes:
    #   - D-06 (blueprint formula vs example mismatch on `café`) —
    #     example-wins resolution; blueprint prose v6.1 backfill pending.
    #   - D-07 (Round-A HIGH finding Unicode-homoglyph bypass) — v3 rule
    #     is strictly stronger than D-06 resolution; see drift_log.
    if any(ord(ch) > 127 for ch in s_nfc):
        raise InvalidSlug(
            "transliteration_lossy",
            original=s,
            transliterated=s_ascii_raw,
        )

    # Step 7: lowercase.
    s_lower = s_ascii_raw.lower()

    # Step 8: collapse runs of non-[a-z0-9] to a single dash.
    collapsed_chars: list[str] = []
    prev_was_dash = False
    for ch in s_lower:
        if ("a" <= ch <= "z") or ("0" <= ch <= "9"):
            collapsed_chars.append(ch)
            prev_was_dash = False
        else:
            if not prev_was_dash:
                collapsed_chars.append("-")
                prev_was_dash = True
    s_collapsed = "".join(collapsed_chars)

    # Step 9: strip leading / trailing dashes.
    s_trimmed = s_collapsed.strip("-")

    # Step 10: reject empty result.
    if not s_trimmed:
        raise InvalidSlug("all_non_alphanum", original=s)

    # Step 11: reject length > 64.
    if len(s_trimmed) > _MAX_SLUG_LENGTH:
        raise InvalidSlug(
            "too_long",
            original=s,
            length=str(len(s_trimmed)),
            max_length=str(_MAX_SLUG_LENGTH),
        )

    # Step 12: reject reserved names.
    # Per v2 — applied AFTER strip + normalize, so whitespace-padded
    # variants of reserved names still hit.
    if s_trimmed in _RESERVED_SLUGS:
        raise ReservedSlug(s_trimmed)

    # Also reject reserved names if they appear in the pre-strip/normalize
    # form (e.g., if input was "./" or "..").
    # The post-normalize result `s_trimmed` already catches these, but we
    # also check the stripped-only form in case normalization changed it.
    stripped_lower = s_stripped.lower()
    if stripped_lower in _RESERVED_SLUGS:
        raise ReservedSlug(stripped_lower)

    return s_trimmed


def ensure_slug_available(slug: str, repo_root: Path) -> None:
    """Verify `slug` is not already allocated under `repo_root/orgs/`. [§4.3]

    Used at org-init time, NOT at session start. Session start binds to an
    existing slug; ensure_slug_available is for creating a NEW slug.

    :param slug: a pre-canonicalized slug (caller should run canonical_slug first)
    :param repo_root: the repository root directory (contains `orgs/`)
    :raises SlugCollisionError: if `repo_root/orgs/<slug>` exists
    :raises TypeError: if arguments are wrong types
    """
    if not isinstance(slug, str):
        raise TypeError(
            f"ensure_slug_available: slug must be str; got "
            f"{type(slug).__name__}"
        )
    if not isinstance(repo_root, Path):
        raise TypeError(
            f"ensure_slug_available: repo_root must be Path; got "
            f"{type(repo_root).__name__}"
        )
    candidate = repo_root / "orgs" / slug
    if candidate.exists():
        raise SlugCollisionError(slug=slug, existing_path=candidate)
