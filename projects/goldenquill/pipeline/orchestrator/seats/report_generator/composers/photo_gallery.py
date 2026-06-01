"""§14.6.4 photo_gallery sub-section composer.

Reads: operational-data ``photos`` sub-kind + ``reporting_template``
``photo_gallery`` field requirements.

Per Cycle 1 RT-7a closure: photos with
``consent_tier == "internal_only"`` are excluded from the gallery
(composer rejects at compose time;
``F-REPORT-OUT-OF-SCOPE-DRIFT.photo_consent_tier_violation`` fires
defense-in-depth at the gate layer).

Per Cycle 1 RT-7b closure: per-photo ``claim_evidence_map`` entry
includes ``caption_text_sha3_512`` (hash of just the caption text,
separate from photo bytes hash) so caption substitution post-Scribe is
structurally detectable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Sequence

from .._canonical import normalize_text_for_hash
from .._schemas import ClaimEntry, SourceRef
from ._base import (
    ClockCallable,
    ComposerError,
    HashBytesCallable,
    ScribeFieldSpec,
    ScribeProtocol,
    VaultReadIntentCallable,
    compute_claim_id,
)


_SUB_SECTION: str = "photo_gallery"
_EXCLUDED_GALLERY_TIER: str = "internal_only"


@dataclass(frozen=True, kw_only=True)
class PhotoRow:
    """Pre-parsed view of one operational-data ``photos`` row."""

    photo_id: str
    source_path: str
    photo_bytes_sha3_512: str
    caption_at_capture: str
    capture_date_utc: str
    location: Optional[str] = None
    photographer: Optional[str] = None
    consent_tier: str = "internal_only"  # default conservative — most restrictive
    related_commitment_id: Optional[str] = None


@dataclass(frozen=True, kw_only=True)
class PhotoGalleryDeps:
    read_photos: VaultReadIntentCallable
    read_template_field_specs: VaultReadIntentCallable
    scribe: ScribeProtocol
    clock: ClockCallable
    hash_bytes: HashBytesCallable


@dataclass(frozen=True, kw_only=True)
class PhotoGalleryResult:
    markdown_fragment: str
    claims: tuple[ClaimEntry, ...]
    photos_included: int
    photos_excluded_for_consent: int


def compose_photo_gallery(
    *,
    deps: PhotoGalleryDeps,
    org_slug: str,
    grant_id: str,
    period_n: int,
    operational_data_root: str,
    reporting_template_path: str,
) -> PhotoGalleryResult:
    """Compose ``photo_gallery`` per §14.6.4.

    Composer-level invariants:

    1. Photos with ``consent_tier == "internal_only"`` are EXCLUDED
       from the gallery (defense-in-depth alongside Cedar policy).
    2. Every included photo has a corresponding :class:`ClaimEntry`
       with ``claim_kind == "photo_reference"``.
    3. ``caption_text_sha3_512`` is set on every photo_reference claim
       (RT-7b closure).
    4. Each claim has exactly one operational_data source with
       ``sub_kind == "photos"``.
    """
    if period_n < 1:
        raise ComposerError(f"period_n must be >= 1; got {period_n!r}")

    _field_specs_raw = deps.read_template_field_specs(
        kind="reporting_template",
        path=reporting_template_path,
        sub_section=_SUB_SECTION,
    )
    # field_specs are advisory for photo_gallery; the per-photo metadata
    # block shape is hard-coded by §14.6.4.

    photos = _coerce_photos(
        deps.read_photos(
            kind="operational_data",
            sub_kind="photos",
            path=f"{operational_data_root.rstrip('/')}/photos",
            period_n=period_n,
        )
    )
    if not photos:
        raise ComposerError(
            "photo_gallery composer: zero operational-data photo rows for "
            f"period_n={period_n}"
        )

    md_parts: list[str] = []
    claims: list[ClaimEntry] = []
    excluded = 0
    included = 0

    for idx, photo in enumerate(photos):
        if photo.consent_tier == _EXCLUDED_GALLERY_TIER:
            # RT-7a — defense-in-depth at compose time.
            excluded += 1
            continue
        included += 1

        # Scribe drafts the per-photo caption (refines / formats the
        # at-capture caption to the funder's required register).
        caption_spec = ScribeFieldSpec(
            sub_section=_SUB_SECTION,
            field_name="caption",
            kind="gallery",
        )
        drafted_caption = deps.scribe(
            spec=caption_spec,
            sources=(
                {
                    "kind": "operational_data",
                    "sub_kind": "photos",
                    "photo_id": photo.photo_id,
                    "caption_at_capture": photo.caption_at_capture,
                    "capture_date_utc": photo.capture_date_utc,
                    "location": photo.location,
                    "photographer": photo.photographer,
                    "consent_tier": photo.consent_tier,
                },
            ),
        )
        if not isinstance(drafted_caption, str):
            raise ComposerError(
                f"Scribe returned non-string for caption: "
                f"{type(drafted_caption).__name__}"
            )

        # RT-7b — caption text hash separate from photo bytes hash.
        caption_text_hash = deps.hash_bytes(
            normalize_text_for_hash(drafted_caption).encode("utf-8")
        )

        md_parts.append(
            f"![{photo.photo_id}]({photo.source_path})\n\n"
            f"*{drafted_caption}*\n\n"
            f"- capture_date_utc: {photo.capture_date_utc}\n"
            f"- location: {photo.location or ''}\n"
            f"- photographer: {photo.photographer or ''}\n"
            f"- consent_tier: {photo.consent_tier}\n"
        )

        claim_id = compute_claim_id(
            sub_section=_SUB_SECTION,
            paragraph_index=idx,
            sentence_index=0,
            claim_text=f"photo:{photo.photo_id}:{drafted_caption}",
        )
        ref = SourceRef(
            kind="operational_data",
            sub_kind="photos",
            source_path=photo.source_path,
            source_row_id=photo.photo_id,
            source_content_sha3_512=photo.photo_bytes_sha3_512,
        )
        claims.append(
            ClaimEntry(
                claim_id=claim_id,
                sub_section=_SUB_SECTION,
                claim_text=drafted_caption,
                claim_kind="photo_reference",
                sources=(ref,),
                caption_text_sha3_512=caption_text_hash,
            )
        )

    _validate_composer_invariants(claims=tuple(claims))

    return PhotoGalleryResult(
        markdown_fragment="\n\n".join(md_parts) if md_parts else "_no photos included_",
        claims=tuple(claims),
        photos_included=included,
        photos_excluded_for_consent=excluded,
    )


# ---------------------------------------------------------------------------
# Coercion helpers
# ---------------------------------------------------------------------------


def _coerce_photos(raw: object) -> tuple[PhotoRow, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"photos must be list/tuple; got {type(raw).__name__}"
        )
    rows: list[PhotoRow] = []
    for idx, r in enumerate(raw):
        if isinstance(r, PhotoRow):
            rows.append(r)
            continue
        if not isinstance(r, Mapping):
            raise ComposerError(f"photos[{idx}] not Mapping")
        try:
            rows.append(
                PhotoRow(
                    photo_id=str(r["photo_id"]),
                    source_path=str(r["source_path"]),
                    photo_bytes_sha3_512=str(r["photo_bytes_sha3_512"]),
                    caption_at_capture=str(r["caption_at_capture"]),
                    capture_date_utc=str(r["capture_date_utc"]),
                    location=str(r["location"]) if r.get("location") is not None else None,
                    photographer=(
                        str(r["photographer"]) if r.get("photographer") is not None else None
                    ),
                    consent_tier=str(r.get("consent_tier", "internal_only")),
                    related_commitment_id=(
                        str(r["related_commitment_id"])
                        if r.get("related_commitment_id") is not None
                        else None
                    ),
                )
            )
        except KeyError as exc:
            raise ComposerError(f"photos[{idx}] missing key {exc!s}") from exc
    return tuple(rows)


def _validate_composer_invariants(*, claims: tuple[ClaimEntry, ...]) -> None:
    for c in claims:
        if c.sub_section != _SUB_SECTION:
            raise ComposerError(
                f"photo_gallery claim {c.claim_id!r} sub_section={c.sub_section!r}"
            )
        if c.claim_kind != "photo_reference":
            raise ComposerError(
                f"photo_gallery claim {c.claim_id!r} claim_kind={c.claim_kind!r}; "
                f"expected 'photo_reference'"
            )
        if c.caption_text_sha3_512 is None:
            raise ComposerError(
                f"photo_gallery claim {c.claim_id!r} missing caption_text_sha3_512 "
                f"(RT-7b closure)"
            )
        if not c.sources:
            raise ComposerError(
                f"photo_gallery claim {c.claim_id!r} has no sources"
            )


__all__ = [
    "PhotoGalleryDeps",
    "PhotoGalleryResult",
    "PhotoRow",
    "compose_photo_gallery",
]
