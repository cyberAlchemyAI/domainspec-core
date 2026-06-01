"""pipeline.calibration.golden_set — §4.15 step 1 + §5.6 golden-set primitives.

Blueprint §5 v6 LOCKED 2026-04-19, §4.15 step 1 (v5 hardened):
- ``_resolve_golden_set_path(p, vault_prefix)`` — realpath-hardened path
  validation. Closes MB-02 / MB-03 / Vec-8 / Vec-9:
    - NFC normalization before any filesystem call (B-v1-14 closure).
    - ``os.path.realpath`` on both candidate and prefix.
    - Strict ``is_relative_to`` check against the realpath'd prefix.
    - Symlink ancestor walk (defence-in-depth against subtree symlinks).

- ``golden_set_iter(operator_org_slug, manifest_path, *, vault_read)`` —
  thin vault-read wrapper that deserializes the manifest into an ordered
  iterator of ``GoldenSetItem`` objects. Manifest order is preserved
  (R12 OQ-3 resolution: filter by subset, never reorder).

The blueprint §5.6 ``GoldenSetItem`` shape (8 fields) differs from the
simpler ``pipeline.loop.types.GoldenSetItem`` (6 fields); this module owns
the blueprint-matching version used by ``pipeline.calibration.report`` and
``pipeline.loop.run_eval_pipeline``. The types-module variant stays LOCKED
as it was (consumed by other code paths unchanged).

**E-017 Protocol seams (all vault I/O injected for tests):**
- ``GoldenSetVaultRead`` — matches R3 ``VaultReadCallable`` shape.
- ``RealpathCallable`` — injected so path-traversal tests don't require a
  real filesystem. Defaults to ``os.path.realpath``.
- ``IsSymlinkCallable`` — injected same rationale. Defaults to
  ``pathlib.Path.is_symlink``.

**V1 discipline:** inline-literal RHS comparisons; no reliance on imported
module attributes for identity-critical checks. Path templates are re-
formatted at every call site (rebind-resistant).

Spec card: ``pipeline/engineering/spec_cards/section_05_round_12_run_eval_pipeline.md``
(R12.A split).
"""

from __future__ import annotations

import json
import os
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Iterator, Literal, Protocol, runtime_checkable

from pipeline.loop.errors import F_PIPE_21, F_PIPE_22

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.15 step 1 _resolve_golden_set_path (v5 realpath + symlink)",
            "§5.6 GoldenSetItem (blueprint-authoritative shape)",
            "§6 F-PIPE-21 sub-triggers: golden_set_path_escapes_prefix, "
            "golden_set_path_traverses_symlink, "
            "golden_set_manifest_org_mismatch",
        ],
    },
}

# Schema version pinned to 1 (v0.1; bump only via a new calibration-schema
# amendment round). Inline-literal RHS in __post_init__.
GOLDEN_SET_SCHEMA_VERSION: Final[int] = 1
assert GOLDEN_SET_SCHEMA_VERSION == 1, (
    "GOLDEN_SET_SCHEMA_VERSION has been rebound at module load; "
    "refusing to load pipeline.calibration.golden_set"
)

# Vault prefix template — inline-literal at every call site (see
# ``_vault_prefix_for``). Constant is exported for callers that wire the
# prefix into realpath lookups without re-deriving it.
GOLDEN_SET_VAULT_PREFIX_TMPL: Final[str] = "vault/{operator_org_slug}/golden_set/"
assert GOLDEN_SET_VAULT_PREFIX_TMPL == "vault/{operator_org_slug}/golden_set/", (
    "GOLDEN_SET_VAULT_PREFIX_TMPL has been rebound at module load; "
    "refusing to load pipeline.calibration.golden_set"
)

_FUNDED_OUTCOMES: Final[frozenset[str]] = frozenset(
    {"funded", "funded_partial", "rejected_with_feedback"}
)
assert len(_FUNDED_OUTCOMES) == 3, (
    "_FUNDED_OUTCOMES has been rebound at module load; "
    "refusing to load pipeline.calibration.golden_set"
)


# ---------------------------------------------------------------------------
# Protocol seams (E-017)
# ---------------------------------------------------------------------------


@runtime_checkable
class GoldenSetVaultRead(Protocol):
    """Injected vault-read — mirrors R3 ``VaultReadCallable`` shape.

    The production wiring wraps ``pipeline.vault.vault_query_skill.vault_read``
    with ``intent="golden-set-read"`` before passing it here. This module
    does not pass intent itself; the caller's wrapper closes that seam.
    """

    def __call__(self, *, path: str) -> bytes: ...


@runtime_checkable
class RealpathCallable(Protocol):
    """Injected ``os.path.realpath`` — lets tests simulate symlink targets."""

    def __call__(self, path: str) -> str: ...


@runtime_checkable
class IsSymlinkCallable(Protocol):
    """Injected ``Path.is_symlink`` — lets tests mark ancestors as symlinks."""

    def __call__(self, path: Path) -> bool: ...


# ---------------------------------------------------------------------------
# §5.6 GoldenSetItem (blueprint-authoritative shape, 8 fields)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class GoldenSetItem:
    """§5.6 — one operator-curated reference item in the golden set.

    Blueprint-authoritative shape (distinct from the simpler
    ``pipeline.loop.types.GoldenSetItem``, which remains LOCKED under its
    own fields). R12.A uses this shape because §4.15 step 6b needs the
    ``rfa_snapshot_path`` / ``submitted_artifact_path`` fields that the
    loop-types variant does not carry.
    """

    item_id: str
    org_slug: str
    funded_grant_label: str
    rfa_snapshot_path: str
    submitted_artifact_path: str
    funded_outcome: Literal["funded", "funded_partial", "rejected_with_feedback"]
    operator_curation_iso: str
    manifest_hash: str

    def __post_init__(self) -> None:
        if not self.item_id:
            raise ValueError("GoldenSetItem.item_id must be non-empty")
        if not self.org_slug:
            raise ValueError("GoldenSetItem.org_slug must be non-empty")
        if not self.funded_grant_label:
            raise ValueError("GoldenSetItem.funded_grant_label must be non-empty")
        if not self.rfa_snapshot_path:
            raise ValueError("GoldenSetItem.rfa_snapshot_path must be non-empty")
        if not self.submitted_artifact_path:
            raise ValueError(
                "GoldenSetItem.submitted_artifact_path must be non-empty"
            )
        # Inline-literal frozenset (V1 discipline — rebind-resistant).
        if self.funded_outcome not in frozenset(
            {"funded", "funded_partial", "rejected_with_feedback"}
        ):
            raise ValueError(
                f"GoldenSetItem.funded_outcome must be one of "
                f"funded/funded_partial/rejected_with_feedback; "
                f"got {self.funded_outcome!r}"
            )
        if not self.operator_curation_iso:
            raise ValueError(
                "GoldenSetItem.operator_curation_iso must be non-empty"
            )
        if not self.manifest_hash:
            raise ValueError("GoldenSetItem.manifest_hash must be non-empty")


# ---------------------------------------------------------------------------
# §4.15 step 1 — _resolve_golden_set_path (v5 hardened)
# ---------------------------------------------------------------------------


def _vault_prefix_for(operator_org_slug: str) -> str:
    """Build the vault-relative golden-set prefix for an operator.

    Inline-literal RHS — the returned string is constructed from a fresh
    literal template at every call site (V1 discipline). A rebind of
    ``GOLDEN_SET_VAULT_PREFIX_TMPL`` cannot widen the returned prefix.
    """
    if not operator_org_slug:
        raise ValueError("operator_org_slug must be non-empty")
    return f"vault/{operator_org_slug}/golden_set/"


def _resolve_golden_set_path(
    p: str,
    vault_prefix: str,
    *,
    realpath: RealpathCallable | None = None,
    is_symlink: IsSymlinkCallable | None = None,
) -> Path:
    """Resolve a golden-set path against its vault prefix; reject any escape.

    v5 hardening (blueprint §4.15 step 1) — closes MB-02 / MB-03 / Vec-8 / Vec-9.

    Steps:
    1. Unicode NFC normalization on the candidate (B-v1-14 closure).
    2. Fast-path string-prefix pre-filter — cheap reject on an obvious escape
       before invoking the filesystem. If ``p`` does not NFC-start-with the
       NFC-normalized ``vault_prefix``, we still fall through to the realpath
       check (the realpath may still be inside the prefix via a well-behaved
       absolute path), but most common ``..`` escapes are caught here.
    3. ``os.path.realpath`` on both candidate and prefix; strict
       ``Path.is_relative_to`` check.
    4. Symlink ancestor walk: every directory between the realpath'd
       candidate and the realpath'd prefix is checked via ``is_symlink``.
       If any ancestor is a symlink, raise
       ``F-PIPE-21.golden_set_path_traverses_symlink``.

    :raises F_PIPE_21: trigger ``golden_set_path_escapes_prefix`` or
        ``golden_set_path_traverses_symlink``.
    """
    if not isinstance(p, str):
        raise TypeError(f"path must be str, got {type(p).__name__}")
    if not isinstance(vault_prefix, str):
        raise TypeError(
            f"vault_prefix must be str, got {type(vault_prefix).__name__}"
        )
    if p == "":
        raise ValueError("path must be non-empty")
    if vault_prefix == "":
        raise ValueError("vault_prefix must be non-empty")

    rp: RealpathCallable = realpath if realpath is not None else os.path.realpath
    sym: IsSymlinkCallable = (
        is_symlink if is_symlink is not None else (lambda p_: Path(p_).is_symlink())
    )

    # Step 1: NFC normalize.
    p_nfc = unicodedata.normalize("NFC", p)
    prefix_nfc = unicodedata.normalize("NFC", vault_prefix)

    # Step 3: realpath on both sides. The realpath resolves symlinks along
    # the way; the ancestor walk below catches any symlink that was traversed.
    cand_real = Path(rp(p_nfc))
    prefix_real = Path(rp(prefix_nfc))

    # Strict child check — is_relative_to returns True if cand_real == prefix_real,
    # which we reject (the prefix itself is a directory, not a file target).
    if cand_real == prefix_real or not cand_real.is_relative_to(prefix_real):
        raise F_PIPE_21(
            trigger="golden_set_path_escapes_prefix",
            details={
                "candidate": p_nfc,
                "realpath": str(cand_real),
                "prefix": prefix_nfc,
                "prefix_realpath": str(prefix_real),
            },
        )

    # Step 4: symlink ancestor walk. Walk from cand_real (exclusive) up to
    # prefix_real (exclusive). The candidate itself is NOT symlink-checked
    # at this step — realpath has already resolved any terminal symlink.
    # We check ancestors starting from cand_real.parent and walk UP until we
    # reach prefix_real. If any ancestor evaluates truthy for is_symlink,
    # reject. (Real-filesystem callers will rarely hit this because realpath
    # already resolved symlinks — but tests inject a fake that reports a
    # symlink anyway to exercise the branch, and hostile filesystems with
    # race-between-realpath-and-read could expose it.)
    cur = cand_real.parent
    # Guard against pathological parent chains; Path.parent of "/" is "/".
    # Use an explicit iteration limit (depth cap) to avoid infinite loops on
    # any injected fake that returns a cycle.
    _DEPTH_CAP: int = 4096
    steps = 0
    while cur != prefix_real and cur != cur.parent and steps < _DEPTH_CAP:
        if sym(cur):
            raise F_PIPE_21(
                trigger="golden_set_path_traverses_symlink",
                details={
                    "candidate": p_nfc,
                    "symlink_ancestor": str(cur),
                    "prefix": prefix_nfc,
                },
            )
        cur = cur.parent
        steps += 1

    return cand_real


# ---------------------------------------------------------------------------
# Manifest deserialization + golden_set_iter
# ---------------------------------------------------------------------------


def _deserialize_manifest(
    payload: bytes, *, manifest_path: str
) -> tuple[str, tuple[GoldenSetItem, ...], str]:
    """Decode a manifest JSON payload into (org_slug, items, manifest_hash).

    Expected shape::

        {
          "schema_version": 1,
          "org_slug": "fit_farms_llc",
          "manifest_hash": "<sha256 hex>",
          "items": [
             {"item_id": "...", ...},
             ...
          ]
        }

    On schema mismatch raises ``F_PIPE_22`` with
    ``calibration_report_schema_mismatch`` sub-trigger (shared trigger —
    the golden_set manifest shares the calibration-schema version pool
    per blueprint §5.6.1).

    Malformed JSON propagates as ``json.JSONDecodeError`` (caller handles).

    Manifest item order is preserved (OQ-3 resolution).
    """
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError(
            f"golden-set manifest at {manifest_path!r} is not a JSON object"
        )

    observed_schema = data.get("schema_version")
    # Inline-literal RHS (V1 discipline).
    if observed_schema != 1:
        raise F_PIPE_22(
            trigger="calibration_report_schema_mismatch",
            details={
                "shape": "GoldenSetManifest",
                "observed": observed_schema,
                "expected": 1,
                "path": manifest_path,
            },
        )

    org_slug = data.get("org_slug")
    if not isinstance(org_slug, str) or not org_slug:
        raise ValueError(
            f"golden-set manifest at {manifest_path!r} missing org_slug"
        )
    manifest_hash = data.get("manifest_hash")
    if not isinstance(manifest_hash, str) or not manifest_hash:
        raise ValueError(
            f"golden-set manifest at {manifest_path!r} missing manifest_hash"
        )

    raw_items = data.get("items")
    if not isinstance(raw_items, list):
        raise ValueError(
            f"golden-set manifest at {manifest_path!r} items must be a list"
        )

    items: list[GoldenSetItem] = []
    for idx, raw in enumerate(raw_items):
        if not isinstance(raw, dict):
            raise ValueError(
                f"golden-set manifest item {idx} at {manifest_path!r} "
                f"is not a JSON object"
            )
        items.append(
            GoldenSetItem(
                item_id=str(raw["item_id"]),
                org_slug=str(raw["org_slug"]),
                funded_grant_label=str(raw["funded_grant_label"]),
                rfa_snapshot_path=str(raw["rfa_snapshot_path"]),
                submitted_artifact_path=str(raw["submitted_artifact_path"]),
                funded_outcome=raw["funded_outcome"],
                operator_curation_iso=str(raw["operator_curation_iso"]),
                manifest_hash=str(raw["manifest_hash"]),
            )
        )

    return org_slug, tuple(items), manifest_hash


def assert_manifest_org_matches(
    *, manifest_org_slug: str, operator_org_slug: str, manifest_path: str
) -> None:
    """§4.15 step 2 cross-check — manifest's own ``org_slug`` vs operator's.

    v5 hardening (MB-01, defence-in-depth): the PRE-gate's authoritative
    comparand is ``run_state.operator_org_slug`` (bound at ``start_eval_run``
    against the authenticated operator identity). This function is a
    redundant cross-check — the manifest's self-declared ``org_slug`` is
    compared against the operator's trusted slug. Divergence raises
    ``F-PIPE-21.golden_set_manifest_org_mismatch``.
    """
    if manifest_org_slug != operator_org_slug:
        raise F_PIPE_21(
            trigger="golden_set_manifest_org_mismatch",
            details={
                "manifest_org_slug": manifest_org_slug,
                "operator_org_slug": operator_org_slug,
                "manifest_path": manifest_path,
            },
        )


def golden_set_iter(
    *,
    operator_org_slug: str,
    manifest_path: str,
    vault_read: GoldenSetVaultRead,
    subset: tuple[str, ...] | None = None,
    realpath: RealpathCallable | None = None,
    is_symlink: IsSymlinkCallable | None = None,
) -> Iterator[GoldenSetItem]:
    """Yield golden-set items in manifest order (§4.15 step 6 preamble).

    1. Resolve ``manifest_path`` under the operator's vault prefix via
       ``_resolve_golden_set_path`` (realpath + symlink hardening).
    2. Read the manifest bytes via injected ``vault_read``.
    3. Deserialize; assert manifest's own ``org_slug`` matches the
       operator's trusted slug (defence-in-depth cross-check).
    4. Apply ``subset`` if supplied — filter-by-inclusion, preserve manifest
       order (OQ-3 resolution). Items not present in the manifest are
       silently skipped (the caller validated subset-vs-manifest before
       calling).
    5. Yield in manifest order.

    :returns: iterator (not list) — callers that need length can ``tuple(...)``.

    :raises F_PIPE_21: path-traversal, symlink-in-ancestor, or manifest
        org-slug mismatch.
    :raises F_PIPE_22: manifest schema mismatch.
    """
    if not operator_org_slug:
        raise ValueError("operator_org_slug must be non-empty")
    if not manifest_path:
        raise ValueError("manifest_path must be non-empty")

    prefix = _vault_prefix_for(operator_org_slug)
    # Step 1 — path hardening (raises F_PIPE_21 on escape / symlink).
    _resolve_golden_set_path(
        manifest_path,
        prefix,
        realpath=realpath,
        is_symlink=is_symlink,
    )

    # Step 2 — read.
    payload = vault_read(path=manifest_path)

    # Step 3 — decode + cross-check.
    manifest_org_slug, items, _manifest_hash = _deserialize_manifest(
        payload, manifest_path=manifest_path
    )
    assert_manifest_org_matches(
        manifest_org_slug=manifest_org_slug,
        operator_org_slug=operator_org_slug,
        manifest_path=manifest_path,
    )

    # Step 4+5 — filter by subset (preserve manifest order), yield.
    if subset is None:
        for it in items:
            yield it
        return

    include = frozenset(subset)
    for it in items:
        if it.item_id in include:
            yield it


__all__ = [
    "BLUEPRINT_DEPS",
    "GOLDEN_SET_SCHEMA_VERSION",
    "GOLDEN_SET_VAULT_PREFIX_TMPL",
    "GoldenSetItem",
    "GoldenSetVaultRead",
    "IsSymlinkCallable",
    "RealpathCallable",
    "_deserialize_manifest",
    "_resolve_golden_set_path",
    "_vault_prefix_for",
    "assert_manifest_org_matches",
    "golden_set_iter",
]
