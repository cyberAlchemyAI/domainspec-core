"""§9 R2 — E-026 ``__module__`` lineage assertion that
:class:`pipeline.seats.judge.types.SectionDraftLike` is satisfied by the
concrete :class:`pipeline.seats.scribe.section_draft.SectionDraft`.

E-026 (per ``pipeline/engineering/review_lessons.v1.md``): use
``__module__`` lineage inspection rather than ``is`` identity for
shared-Protocol provenance, because ``importlib.reload`` /
``sys.modules.pop`` elsewhere in the suite produces a new class object
that passes ``isinstance`` but fails ``is``. The Round-7 aftermath of
Scout's shared-Protocol lineage tests showed this cascade; the same
discipline applies to Judge R2's binding of ``SectionDraftLike`` to
Scribe R2's concrete ``SectionDraft``.

Tests here verify:

- ``SectionDraft.__module__`` is exactly the canonical Scribe module
  path (lineage assertion, stable across reload).
- A real ``SectionDraft`` instance satisfies the
  :class:`SectionDraftLike` ``runtime_checkable`` Protocol.
- The four fields Judge reads from the Protocol —
  ``section_name`` / ``section_order`` / ``body_text`` /
  ``claim_evidence_map`` — are all populated on the concrete shape with
  the documented types.
- ``ClaimEvidence`` lineage assertion (the concrete Scribe shape lives
  at the documented module path) PLUS structural conformance under the
  R3-amended ``ClaimEvidenceLike`` Protocol. R3 reconciled the original
  R1-vs-Scribe-shape divergence via §7.a option (b) — the Judge
  Protocol now carries ``evidence_kind`` + ``source_pointer`` (Scribe's
  actual field names), so a real ``ClaimEvidence`` instance now
  satisfies ``isinstance(ce, ClaimEvidenceLike)`` directly.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pipeline.seats.judge.types import (
    ClaimEvidenceLike,
    SectionDraftLike,
)
from pipeline.seats.scribe.section_draft import (
    ClaimEvidence,
    SectionDraft,
)


UTC = timezone.utc
DRAFT_AT = datetime(2026, 4, 29, 12, 0, 0, tzinfo=UTC)


# ---------------------------------------------------------------------------
# Helpers — build a real concrete SectionDraft instance.
# ---------------------------------------------------------------------------


def _build_real_section_draft() -> SectionDraft:
    body = "Real body text from Scribe."
    from pipeline.seats.scribe.compress import (
        count_characters,
        count_words,
    )

    return SectionDraft(
        section_name="Project Narrative",
        section_order=1,
        body_text=body,
        word_count=count_words(body),
        character_count=count_characters(body),
        rfa_section_limit=None,
        over_limit_flag=False,
        claim_evidence_map=(),
        eligible_activity_map=(),
        admin_risk_flags=(),
        scope_check_comments=(),
        draft_dialect="centrist",
        drafted_at_utc=DRAFT_AT,
    )


def _build_real_claim_evidence() -> ClaimEvidence:
    return ClaimEvidence(
        claim_text="The cooperative serves 12 farms.",
        evidence_kind="PROJECT_CONTEXT",
        source_pointer="org_profile.cooperative_membership.count",
    )


# ---------------------------------------------------------------------------
# Lineage assertions (E-026)
# ---------------------------------------------------------------------------


class TestSectionDraftLikeLineage:
    def test_concrete_section_draft_module_is_canonical(self):
        # E-026: assert __module__ rather than `is` identity.
        assert SectionDraft.__module__ == (
            "pipeline.seats.scribe.section_draft"
        )

    def test_concrete_section_draft_qualname_is_canonical(self):
        assert SectionDraft.__qualname__ == "SectionDraft"

    def test_real_instance_passes_runtime_protocol_check(self):
        draft = _build_real_section_draft()
        assert isinstance(draft, SectionDraftLike)

    def test_protocol_fields_populated_on_real_instance(self):
        draft = _build_real_section_draft()
        # The four fields Judge reads from the Protocol.
        assert isinstance(draft.section_name, str) and draft.section_name
        assert isinstance(draft.section_order, int) and draft.section_order >= 1
        assert isinstance(draft.body_text, str)
        assert isinstance(draft.claim_evidence_map, tuple)

    def test_protocol_field_set_matches_documented_surface(self):
        # Per types.SectionDraftLike docstring, Judge reads exactly:
        #   section_name, section_order, body_text, claim_evidence_map.
        # Verify each via attribute access on the concrete instance.
        draft = _build_real_section_draft()
        for fname in (
            "section_name",
            "section_order",
            "body_text",
            "claim_evidence_map",
        ):
            assert hasattr(draft, fname), (
                f"concrete SectionDraft missing protocol field {fname!r}"
            )

    def test_concrete_section_draft_satisfies_protocol_under_lineage(self):
        # Combined: lineage AND structural conformance — the lineage
        # assertion above proves origin; this one proves the runtime
        # check still works (E-026's "passes isinstance even after
        # reload" property).
        draft = _build_real_section_draft()
        assert SectionDraft.__module__ == (
            "pipeline.seats.scribe.section_draft"
        )
        assert isinstance(draft, SectionDraftLike)


# ---------------------------------------------------------------------------
# ClaimEvidence parallel
# ---------------------------------------------------------------------------


class TestClaimEvidenceLineage:
    """E-026 lineage for :class:`ClaimEvidence` — the Scribe concrete
    type lives at its canonical module path AND, after the R3
    Protocol amendment, structurally satisfies the Judge
    ``ClaimEvidenceLike`` Protocol.
    """

    def test_concrete_claim_evidence_module_is_canonical(self):
        assert ClaimEvidence.__module__ == (
            "pipeline.seats.scribe.section_draft"
        )

    def test_concrete_claim_evidence_qualname_is_canonical(self):
        assert ClaimEvidence.__qualname__ == "ClaimEvidence"

    def test_concrete_shape_matches_amended_protocol_field_names(self):
        # R3 §7.a option (b): Protocol now declares
        # claim_text + evidence_kind + source_pointer (Scribe's actual
        # fields). The original R1 fields evidence_text + source_field
        # are gone from the Protocol.
        ce = _build_real_claim_evidence()
        assert hasattr(ce, "claim_text")
        assert hasattr(ce, "evidence_kind")
        assert hasattr(ce, "source_pointer")
        assert not hasattr(ce, "evidence_text")
        assert not hasattr(ce, "source_field")
        assert isinstance(ce, ClaimEvidenceLike)


# ---------------------------------------------------------------------------
# Negative case — non-conforming object fails the runtime check.
# ---------------------------------------------------------------------------


class TestProtocolNegativeCase:
    def test_random_object_does_not_satisfy_protocol(self):
        class _NotADraft:
            pass

        assert not isinstance(_NotADraft(), SectionDraftLike)

    def test_partial_object_does_not_satisfy_protocol(self):
        class _PartialDraft:
            section_name = "X"
            section_order = 1
            # Missing body_text + claim_evidence_map.

        assert not isinstance(_PartialDraft(), SectionDraftLike)
