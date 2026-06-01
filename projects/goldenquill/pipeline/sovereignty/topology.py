"""DOC_SOURCED whitelist + path canonicalization. [§1 row 7, §3.11d, §7.5 BT2, §6.7]"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from pipeline.sovereignty.org_slug import canonical_slug

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": ["§1 row 7", "§3.11d (path topology surface)", "§7.5 BT2"],
        "hash_at_lock": None,  # populated at committee LOCK
        "hash_source_version": "v6",
    },
}

__all__ = [
    "DocSourcedRoot",
    "DOC_SOURCED_ROOTS",
    "PathEscapedRoot",
    "SymlinkRejected",
    "is_doc_sourced_path",
    "canonicalize_vault_path",
]


class PathEscapedRoot(RuntimeError):
    """Path resolves outside claimed root. [§6.7 F-ISO-*]"""

    def __init__(self, path: Path, repo_root: Path, reason: str = "canonical_outside_root") -> None:
        super().__init__(f"path {path!s} escapes repo_root {repo_root!s} ({reason})")
        self.path = path
        self.repo_root = repo_root
        self.reason = reason


class SymlinkRejected(RuntimeError):
    """Symlink component points outside claimed root. [§6.7 F-ISO-02]"""

    def __init__(self, path: Path, offending_component: Path, target: Path) -> None:
        super().__init__(
            f"symlink escape at {offending_component!s} -> {target!s} while resolving {path!s}"
        )
        self.path = path
        self.offending_component = offending_component
        self.target = target


@dataclass(frozen=True, kw_only=True)
class DocSourcedRoot:
    """One whitelisted root. [§1 row 7] E-002: label is lowercase ascii."""

    label: str
    path_template: str
    slug_parameterized: bool


# Five whitelisted roots, in blueprint §1 row 7 order. Order is stable —
# new entries append only. Reordering is a Section 1 revision.
DOC_SOURCED_ROOTS: tuple[DocSourcedRoot, ...] = (
    DocSourcedRoot(
        label="rfa",
        path_template="rfa/",
        slug_parameterized=False,
    ),
    DocSourcedRoot(
        label="org",
        path_template="orgs/{slug}/",
        slug_parameterized=True,
    ),
    DocSourcedRoot(
        label="dossier",
        path_template="orgs/{slug}/dossier/entities/",
        slug_parameterized=True,
    ),
    DocSourcedRoot(
        label="rubrics",
        path_template="pipeline/rubrics/",
        slug_parameterized=False,
    ),
    DocSourcedRoot(
        label="institutional_memory",
        path_template="pipeline/institutional_memory/",
        slug_parameterized=False,
    ),
)


def _validate_entry_args(path: Path, bound_slug: str, repo_root: Path) -> None:
    """E-001 type gate + defensive canonical-slug assertion. [§1 row 7]

    :raises TypeError: wrong arg types.
    :raises ValueError: bound_slug not canonical (propagates InvalidSlug /
                        ReservedSlug from canonical_slug, both ValueError).
    """
    if not isinstance(path, Path):
        raise TypeError(
            f"topology: path must be pathlib.Path; got {type(path).__name__}"
        )
    if not isinstance(bound_slug, str):
        raise TypeError(
            f"topology: bound_slug must be str; got {type(bound_slug).__name__}"
        )
    if not isinstance(repo_root, Path):
        raise TypeError(
            f"topology: repo_root must be pathlib.Path; got {type(repo_root).__name__}"
        )
    # Propagates InvalidSlug/ReservedSlug for truly invalid slugs; both are
    # ValueError subclasses so `except ValueError:` catches them.
    canon = canonical_slug(bound_slug)
    if canon != bound_slug:
        raise ValueError(
            f"topology: bound_slug {bound_slug!r} is not canonical "
            f"(canonical form is {canon!r}); caller must pre-canonicalize "
            f"via pipeline.sovereignty.canonical_slug before passing in"
        )


def _walk_for_symlink_escape(target: Path, repo_root_resolved: Path) -> None:
    """Raise SymlinkRejected if any component from repo_root to target is a
    symlink pointing outside repo_root. [§7.5 BT2 symlink-escape discipline]"""
    # Walk parents from target down to (but not including) repo_root_resolved.
    # Sorted from repo_root-near to target-near so the earliest escape is the
    # first one surfaced.
    ancestors: list[Path] = []
    p = target
    while True:
        if p == repo_root_resolved:
            break
        ancestors.append(p)
        parent = p.parent
        if parent == p:  # reached filesystem root without hitting repo_root
            # target is not under repo_root — caller's prefix check should
            # have caught this; defensive raise.
            raise PathEscapedRoot(
                target, repo_root_resolved, reason="target_not_under_repo_root"
            )
        p = parent
    ancestors.reverse()  # now repo_root-near → target-near

    for component in ancestors:
        if not component.exists() and not component.is_symlink():
            # Nonexistent tail is fine — the caller may be asking about a
            # path that will be created. We only care about existing
            # symlinks escaping.
            continue
        if component.is_symlink():
            # Readlink is a single-step target; may itself be a symlink,
            # but resolve() of the component would recurse and land
            # somewhere. We use resolve(strict=False) to get the final
            # destination.
            try:
                resolved_component = component.resolve(strict=False)
            except (OSError, RuntimeError) as e:  # symlink loop, etc.
                raise SymlinkRejected(
                    path=target,
                    offending_component=component,
                    target=component,
                ) from e
            # Defence: also read the raw symlink target for the exception
            # payload (what the attacker planted) — useful diagnostics.
            try:
                raw_target = Path(os.readlink(component))
            except OSError:
                raw_target = component
            try:
                resolved_component.relative_to(repo_root_resolved)
            except ValueError:
                raise SymlinkRejected(
                    path=target,
                    offending_component=component,
                    target=raw_target,
                )


def is_doc_sourced_path(
    path: Path,
    *,
    bound_slug: str,
    repo_root: Path,
) -> bool:
    """True iff `path` is under one of the five DOC_SOURCED roots. [§7.5]

    Slug mismatch yields False (wrong-org not doc-sourced under bound_slug).
    Symlink-escape raises SymlinkRejected (fail-loud). Path outside repo_root
    returns False (benign probe).

    :raises TypeError / ValueError / SymlinkRejected / PathEscapedRoot.
    """
    _validate_entry_args(path, bound_slug, repo_root)

    try:
        repo_root_resolved = repo_root.resolve(strict=True)
    except (OSError, RuntimeError) as e:
        raise PathEscapedRoot(path, repo_root, reason="repo_root_not_resolvable") from e
    if not repo_root_resolved.is_dir():
        raise PathEscapedRoot(path, repo_root, reason="repo_root_not_a_directory")

    # Resolve the target. Use strict=False so callers can probe paths that
    # don't yet exist (e.g. "will this be a doc-sourced path once created?").
    try:
        path_resolved = path.resolve(strict=False)
    except (OSError, RuntimeError):
        # Resolution can fail on certain malformed inputs; treat as non-doc-
        # sourced rather than raising.
        return False

    # First cheap filter: must be under repo_root.
    try:
        path_resolved.relative_to(repo_root_resolved)
    except ValueError:
        return False

    for root in DOC_SOURCED_ROOTS:
        template = root.path_template
        if root.slug_parameterized:
            template = template.replace("{slug}", bound_slug)
        # Normalize trailing slash on template for directory prefix
        # semantics: paths under `rfa/` must have `rfa/` as a parent
        # directory, not share a prefix with `rfaish/`.
        if not template.endswith("/"):
            template = template + "/"
        expected_prefix = (repo_root_resolved / template.rstrip("/")).resolve(strict=False)
        try:
            path_resolved.relative_to(expected_prefix)
        except ValueError:
            continue
        # Inside the prefix — now check symlink components for escape.
        # Any symlink-escape in the walk raises SymlinkRejected.
        _walk_for_symlink_escape(path_resolved, repo_root_resolved)
        return True

    return False


def canonicalize_vault_path(path: Path, *, repo_root: Path) -> Path:
    """Resolve `path` (strict=True); reject escape + symlink-escape. [§3.11d, §7.5 BT2]

    :raises TypeError / PathEscapedRoot / SymlinkRejected / FileNotFoundError.
    """
    if not isinstance(path, Path):
        raise TypeError(
            f"canonicalize_vault_path: path must be pathlib.Path; got {type(path).__name__}"
        )
    if not isinstance(repo_root, Path):
        raise TypeError(
            f"canonicalize_vault_path: repo_root must be pathlib.Path; got "
            f"{type(repo_root).__name__}"
        )
    try:
        repo_root_resolved = repo_root.resolve(strict=True)
    except (OSError, RuntimeError) as e:
        raise PathEscapedRoot(path, repo_root, reason="repo_root_not_resolvable") from e
    if not repo_root_resolved.is_dir():
        raise PathEscapedRoot(path, repo_root, reason="repo_root_not_a_directory")

    # strict=True — path must exist.
    path_resolved = path.resolve(strict=True)

    # Membership check: resolved path must be under repo_root.
    try:
        path_resolved.relative_to(repo_root_resolved)
    except ValueError:
        raise PathEscapedRoot(path, repo_root, reason="canonical_outside_root")

    # Symlink-escape walk. Any symlink whose target escapes repo_root is
    # rejected even if the final resolved path happens to stay inside.
    _walk_for_symlink_escape(path_resolved, repo_root_resolved)
    return path_resolved
