"""Tests for §14.6.4 photo_gallery sub-section composer."""

from __future__ import annotations

import pytest

from pipeline.orchestrator.seats.report_generator.composers._base import ComposerError
from pipeline.orchestrator.seats.report_generator.composers.photo_gallery import (
    PhotoGalleryDeps,
    compose_photo_gallery,
)


def _registry(*, include_internal: bool = True):
    rows = [
        {
            "photo_id": "PHOTO-001",
            "source_path": "orgs/myorg/vault/operational/grants/G1/period_1/photos/PHOTO-001.jpg",
            "photo_bytes_sha3_512": "a" * 128,
            "caption_at_capture": "Workshop in PA — week 1.",
            "capture_date_utc": "2026-04-15T10:00:00Z",
            "location": "Philadelphia, PA",
            "photographer": "Daniel",
            "consent_tier": "narrative-text-only",
        }
    ]
    if include_internal:
        rows.append(
            {
                "photo_id": "PHOTO-002",
                "source_path": "x",
                "photo_bytes_sha3_512": "b" * 128,
                "caption_at_capture": "Internal staff training.",
                "capture_date_utc": "2026-04-16T10:00:00Z",
                "location": "Office",
                "photographer": "Daniel",
                "consent_tier": "internal_only",  # MUST be excluded
            }
        )
    return {
        ("operational_data", "photos"): rows,
        ("reporting_template", None): [{"field_name": "photo_gallery"}],
    }


def _make_deps(*, fixed_clock, hash_bytes, make_read_intent, make_scribe, include_internal=True):
    reg = _registry(include_internal=include_internal)
    return PhotoGalleryDeps(
        read_photos=make_read_intent(reg),
        read_template_field_specs=make_read_intent(reg),
        scribe=make_scribe(),
        clock=fixed_clock,
        hash_bytes=hash_bytes,
    )


class TestComposePhotoGallery:
    def test_internal_only_excluded(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
        )
        r = compose_photo_gallery(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="orgs/myorg/vault/operational/grants/G1/period_1",
            reporting_template_path="x",
        )
        assert r.photos_included == 1
        assert r.photos_excluded_for_consent == 1
        for c in r.claims:
            assert c.sub_section == "photo_gallery"
            assert c.claim_kind == "photo_reference"
            assert c.caption_text_sha3_512 is not None  # RT-7b
            assert len(c.caption_text_sha3_512) == 128

    def test_caption_hash_is_text_only(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        """RT-7b: caption_text_sha3_512 must differ from photo bytes hash."""
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
            include_internal=False,
        )
        r = compose_photo_gallery(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="x",
            reporting_template_path="y",
        )
        c = r.claims[0]
        # Both hashes are SHA3-512 128-hex but should be different inputs.
        assert c.caption_text_sha3_512 != c.sources[0].source_content_sha3_512

    def test_empty_photos_raises(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        reg = {("operational_data", "photos"): [], ("reporting_template", None): []}
        deps = PhotoGalleryDeps(
            read_photos=make_read_intent(reg),
            read_template_field_specs=make_read_intent(reg),
            scribe=make_scribe(),
            clock=fixed_clock,
            hash_bytes=hash_bytes,
        )
        with pytest.raises(ComposerError):
            compose_photo_gallery(
                deps=deps,
                org_slug="myorg",
                grant_id="G1",
                period_n=1,
                operational_data_root="x",
                reporting_template_path="y",
            )
