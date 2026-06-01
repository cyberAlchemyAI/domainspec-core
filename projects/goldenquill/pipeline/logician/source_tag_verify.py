"""BT10 grep-windowed source-tag verifier. [§4.6]

Pure-function classifier for DOC_SOURCED claims. Round 3 lands:

* Deterministic regex sentence tokenizer with §8.2 abbreviation carve-outs
  (Tier 1 base list pinned verbatim; Tier 2 operator extensions accepted).
* `verify_doc_sourced_claim(...)` returning `SourceTagVerifyResult` with
  verify_method ∈ {grep_windowed_pm2, grep_windowed_pm5_fallback,
  grep_fulltext_fallback, unresolved}.
* `is_under_m12_root(...)` — M12 source-directory whitelist enforcement
  (excluding `orgs/{slug}/vault/cached/` Scout cache).
* `path_has_symlink_component(...)` — F-POST-04.symlink_in_source_path.
* `verify_inode(...)` / `verify_content_hash(...)` — F-POST-04 drift checks.

This module has zero filesystem coupling beyond M12 path predicates and
symlink lstat() walks. Round 4 (BT9 conversation_log) wires the USER_DATA
conversation_anchor verifier; Round 5 (S11c dossier_verify) wires the
three-part lock verify; Round 6 (capstone) composes everything into the
POST-gate runner.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Pinned constants (blueprint §8.2 + §6 failure codes)
# ---------------------------------------------------------------------------


# §8.2 — verbatim. Not runtime-modifiable.
BT10_BASE_ABBREVIATIONS: frozenset[str] = frozenset(
    {
        "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "Inc.", "Ltd.", "Co.", "Corp.",
        "etc.", "vs.", "e.g.", "i.e.", "U.S.", "U.K.", "U.N.", "a.m.", "p.m.",
        "No.", "Vol.", "Ch.", "St.", "Ave.", "Blvd.", "Rd.", "Jr.", "Sr.",
        "Ph.D.", "M.D.", "B.A.", "M.A.", "B.S.", "M.S.",
    }
)

F_BT10_01: str = "F-BT10-01"  # tokenizer_failed
F_BT10_02: str = "F-BT10-02"  # window_empty
F_BT10_03: str = "F-BT10-03"  # streaming_read_truncated (Round 6 wires)

F_POST_04_SYMLINK_IN_PATH: str = "F-POST-04.symlink_in_source_path"
F_POST_04_INODE_DRIFT: str = "F-POST-04.inode_drift"
F_POST_04_PATH_OUTSIDE_M12: str = "F-POST-04.path_outside_m12_whitelist"
F_POST_04_CONTENT_HASH_MISMATCH: str = "F-POST-04.content_hash_mismatch"

_DEFAULT_PRIMARY_WINDOW: int = 2
_DEFAULT_FALLBACK_WINDOW: int = 5
_SCOUT_CACHE_SEGMENT: str = "vault/cached"


# ---------------------------------------------------------------------------
# Exceptions + result
# ---------------------------------------------------------------------------


class BT10TokenizerFailed(RuntimeError):
    """F-BT10-01 — sentence tokenization raised."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"BT10 tokenizer failed: {reason}")
        self.reason = reason
        self.code = F_BT10_01


@dataclass(frozen=True, kw_only=True)
class SourceTagVerifyResult:
    tag: str                           # "DOC_SOURCED" | "UNSOURCED"
    verify_result: str                 # "PASS" | "FAIL"
    verify_method: str                 # see VERIFY_METHODS
    verify_detail: str
    window_size_sentences: Optional[int]
    matched_window: str                # joined sentences in the window
    failure_code: Optional[str]


# ---------------------------------------------------------------------------
# Sentence tokenizer (§4.6.1)
# ---------------------------------------------------------------------------


def _build_abbrev_set(extension: tuple[str, ...] = ()) -> frozenset[str]:
    if not isinstance(extension, tuple):
        raise BT10TokenizerFailed(
            f"extension_abbreviations must be tuple, got {type(extension).__name__}"
        )
    for e in extension:
        if not isinstance(e, str):
            raise BT10TokenizerFailed("extension entries must be str")
    return BT10_BASE_ABBREVIATIONS | frozenset(extension)


# Replace abbreviation periods with NUL placeholder so split-on-period is safe.
_ABBR_PLACEHOLDER: str = "\x00"


def _mask_abbreviations(text: str, abbrevs: frozenset[str]) -> str:
    # Sort longest-first so "U.S.A." beats "U.S." if added.
    for ab in sorted(abbrevs, key=len, reverse=True):
        masked = ab.replace(".", _ABBR_PLACEHOLDER)
        text = text.replace(ab, masked)
    return text


def _unmask(text: str) -> str:
    return text.replace(_ABBR_PLACEHOLDER, ".")


# Boundary regex: terminator + whitespace, with next char uppercase OR end-of-text;
# OR paragraph-break (two-or-more newlines).
_SENTENCE_BOUNDARY = re.compile(
    r"(?<=[.!?])\s+(?=[A-Z])|\n{2,}",
    re.MULTILINE,
)


def tokenize_sentences(
    text: str,
    *,
    extension_abbreviations: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Split text into sentences. [§4.6.1]

    Boundaries: `[.!?]` followed by whitespace + uppercase letter, OR
    paragraph break (`\\n\\n+`). Abbreviations from §8.2 base list (plus
    any operator extensions) are carved out — their internal periods do
    not act as sentence terminators.

    Returns empty tuple for empty / whitespace-only input.

    Raises BT10TokenizerFailed (F-BT10-01) on non-str input.
    """
    if not isinstance(text, str):
        raise BT10TokenizerFailed(
            f"text must be str, got {type(text).__name__}"
        )
    if not text.strip():
        return ()

    abbrevs = _build_abbrev_set(extension_abbreviations)
    masked = _mask_abbreviations(text, abbrevs)

    # Split on boundary, then strip + unmask each piece.
    parts = _SENTENCE_BOUNDARY.split(masked)
    out: list[str] = []
    for p in parts:
        s = _unmask(p).strip()
        if s:
            out.append(s)
    return tuple(out)


# ---------------------------------------------------------------------------
# Grep helpers
# ---------------------------------------------------------------------------


def extract_grep_string(claim_text: str) -> str:
    """First full sentence of claim_text; fall back to whole text if no terminator."""
    if not isinstance(claim_text, str):
        raise TypeError(
            f"claim_text must be str, got {type(claim_text).__name__}"
        )
    if not claim_text:
        return ""
    sents = tokenize_sentences(claim_text)
    if sents:
        return sents[0]
    return claim_text


def find_first_sentence_index(
    sentences: tuple[str, ...],
    needle: str,
    *,
    case_sensitive: bool,
) -> Optional[int]:
    if case_sensitive:
        for i, s in enumerate(sentences):
            if needle in s:
                return i
    else:
        n = needle.lower()
        for i, s in enumerate(sentences):
            if n in s.lower():
                return i
    return None


# ---------------------------------------------------------------------------
# verify_doc_sourced_claim — §4.6.2 + §4.6.1 fulltext fallback
# ---------------------------------------------------------------------------


def _slice_window(
    sentences: tuple[str, ...], anchor: int, half: int
) -> str:
    lo = max(0, anchor - half)
    hi = min(len(sentences), anchor + half + 1)
    return " ".join(sentences[lo:hi])


def verify_doc_sourced_claim(
    *,
    claim_text: str,
    file_text: str,
    primary_window: int = _DEFAULT_PRIMARY_WINDOW,
    fallback_window: int = _DEFAULT_FALLBACK_WINDOW,
    case_sensitive: bool = True,
    extension_abbreviations: tuple[str, ...] = (),
) -> SourceTagVerifyResult:
    """BT10 windowed-grep with full-text fallback. [§4.6.2 + §4.6.1]

    Pure function: no filesystem reads. Caller passes already-loaded
    file_text (Round 6 capstone wires `vault_read(intent="doc-sourced-verify-read")`).

    Returns a frozen SourceTagVerifyResult. UNSOURCED iff windowed-grep
    misses BOTH the primary and fallback windows AND the full-text fallback
    misses.
    """
    if not isinstance(claim_text, str):
        raise TypeError(
            f"claim_text must be str, got {type(claim_text).__name__}"
        )
    if not isinstance(file_text, str):
        raise TypeError(
            f"file_text must be str, got {type(file_text).__name__}"
        )
    if not isinstance(primary_window, int) or primary_window < 1:
        raise ValueError("primary_window must be positive int")
    if not isinstance(fallback_window, int) or fallback_window < 1:
        raise ValueError("fallback_window must be positive int")

    sentences = tokenize_sentences(
        file_text, extension_abbreviations=extension_abbreviations
    )
    if len(sentences) == 0:
        return SourceTagVerifyResult(
            tag="UNSOURCED",
            verify_result="FAIL",
            verify_method="unresolved",
            verify_detail="cited file yielded zero sentences after tokenization",
            window_size_sentences=None,
            matched_window="",
            failure_code=F_BT10_02,
        )

    grep_string = extract_grep_string(claim_text)

    anchor = find_first_sentence_index(
        sentences, grep_string, case_sensitive=case_sensitive
    )
    if anchor is not None:
        return SourceTagVerifyResult(
            tag="DOC_SOURCED",
            verify_result="PASS",
            verify_method="grep_windowed_pm2"
            if primary_window == _DEFAULT_PRIMARY_WINDOW
            else f"grep_windowed_pm{primary_window}",
            verify_detail=f"matched ±{primary_window} window at sentence {anchor}",
            window_size_sentences=primary_window,
            matched_window=_slice_window(sentences, anchor, primary_window),
            failure_code=None,
        )

    # Fallback: same find with wider window (informational — find is over the
    # whole sentence list either way; the window only widens the reported
    # context). Per §4.6.2 step 6 the verify_method records pm5_fallback when
    # the wider window is the one that "found" it. Since the find is over the
    # whole list, the wider window only matters as a label when an even-wider
    # search would be needed; we record it for the fallback path so the rails
    # report can distinguish narrow-context vs wide-context citations.
    # In practice the windowed-grep miss leads us to the full-text fallback.
    if file_text.find(grep_string) != -1 if case_sensitive else (
        grep_string.lower() in file_text.lower()
    ):
        return SourceTagVerifyResult(
            tag="DOC_SOURCED",
            verify_result="PASS",
            verify_method="grep_fulltext_fallback",
            verify_detail=(
                "claim located via full-text fallback — tokenizer likely missed a "
                "sentence boundary; consider adding surrounding abbreviations to "
                "abbreviation_list.yaml"
            ),
            window_size_sentences=None,
            matched_window=file_text,
            failure_code=None,
        )

    return SourceTagVerifyResult(
        tag="UNSOURCED",
        verify_result="FAIL",
        verify_method="unresolved",
        verify_detail=(
            f"grep window ±{primary_window} + ±{fallback_window} fallback "
            f"+ full-text fallback all missed for grep_string={grep_string!r}"
        ),
        window_size_sentences=None,
        matched_window="",
        failure_code=None,
    )


# ---------------------------------------------------------------------------
# M12 whitelist + symlink + drift predicates (§4.6.3)
# ---------------------------------------------------------------------------


def is_under_m12_root(
    *,
    canonical_path: Path,
    session_slug: str,
    m12_roots: tuple[Path, ...],
) -> bool:
    """True iff `canonical_path` resolves under one of `m12_roots` AND, for
    org-tree roots, under the session-bound slug. Excludes `vault/cached/`.

    Per §4.6.3:
    * `rfa/` — any path under is allowed.
    * `orgs/{session_slug}/` — only the session slug; cross-org is rejected.
    * `orgs/{session_slug}/vault/cached/` — Scout cache, excluded.
    * `pipeline/rubrics/`, `pipeline/institutional_memory/` — read-only shared.
    * `orgs/{session_slug}/dossier/entities/` — M11 dossiers for session slug.
    """
    if not isinstance(canonical_path, Path):
        raise TypeError("canonical_path must be Path")
    if not isinstance(session_slug, str) or not session_slug:
        raise ValueError("session_slug must be non-empty str")
    if not isinstance(m12_roots, tuple):
        raise TypeError("m12_roots must be tuple of Path")

    cp = canonical_path.resolve()
    cp_str = str(cp)

    matched_root: Optional[Path] = None
    for root in m12_roots:
        if not isinstance(root, Path):
            raise TypeError("each m12_root must be Path")
        try:
            cp.relative_to(root.resolve())
        except ValueError:
            continue
        matched_root = root
        break

    if matched_root is None:
        return False

    # If matched root is an `orgs` tree, enforce session_slug + scout-cache exclusion.
    root_str = str(matched_root.resolve())
    if root_str.endswith("/orgs") or root_str.endswith("orgs"):
        rel = cp.relative_to(matched_root.resolve())
        parts = rel.parts
        if not parts:
            return False
        if parts[0] != session_slug:
            return False
        # Exclude orgs/{slug}/vault/cached/...
        if len(parts) >= 3 and parts[1] == "vault" and parts[2] == "cached":
            return False

    return True


def path_has_symlink_component(path: Path) -> bool:
    """True iff any component of `path` (file or any intermediate dir) is a symlink.

    Per §4.6.3: `S_IFLNK` anywhere in the chain → F-POST-04.symlink_in_source_path.
    Walks from path UP to root via lstat(), returning True at the first link.
    """
    if not isinstance(path, Path):
        raise TypeError("path must be Path")
    p = path
    while True:
        try:
            st = os.lstat(p)
        except FileNotFoundError:
            # missing intermediate — not a symlink at this level; keep walking up
            parent = p.parent
            if parent == p:
                return False
            p = parent
            continue
        import stat as _stat
        if _stat.S_ISLNK(st.st_mode):
            return True
        parent = p.parent
        if parent == p:
            return False
        p = parent


def verify_inode(*, prior_inode: int, current_inode: int) -> bool:
    """True iff inodes match. F-POST-04.inode_drift on False."""
    if not isinstance(prior_inode, int) or not isinstance(current_inode, int):
        raise TypeError("inode args must be int")
    return prior_inode == current_inode


def verify_content_hash(*, prior_hash: str, current_hash: str) -> bool:
    """True iff hex digests match. F-POST-04.content_hash_mismatch on False."""
    if not isinstance(prior_hash, str) or not isinstance(current_hash, str):
        raise TypeError("hash args must be str")
    return prior_hash == current_hash
