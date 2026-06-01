"""Unit tests for F-CLASS-* outbound-boundary sub-codes.

Per architecture v7.0.7 §1 + §4.1 + §5.1.
"""

from __future__ import annotations

from pipeline.logician.gates.f_class_outbound_boundary import (
    CLASS_CONFIDENTIAL,
    CLASS_OPERATOR_FLAGGED,
    CLASS_PUBLIC,
    CLASS_SHAREABLE,
    ClassifiedValue,
    F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
    F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED,
    F_CLASS_HIGH_STAKES_FLAG_LEAK,
    F_CLASS_SLOT_ID_NON_OPAQUE,
    SlotPosition,
    check_class_cloud_received_confidential,
    check_class_cloud_received_opaque_slot_filled,
    check_class_high_stakes_flag_leak,
    check_class_slot_id_non_opaque,
)


# ---------------------------------------------------------------------------
# F-CLASS-SLOT-ID-NON-OPAQUE
# ---------------------------------------------------------------------------


def test_slot_id_non_opaque_constant() -> None:
    assert F_CLASS_SLOT_ID_NON_OPAQUE == "F-CLASS-SLOT-ID-NON-OPAQUE"


def test_opaque_numeric_slot_passes() -> None:
    prompt = "Annual revenue: [SLOT_001]. Acres: [SLOT_42]."
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=prompt)
    assert r.success is True
    assert r.matched_count == 0


def test_no_slots_at_all_passes() -> None:
    r = check_class_slot_id_non_opaque(
        cloud_routed_prompt="No placeholders here at all."
    )
    assert r.success is True


def test_semantic_slot_name_fails() -> None:
    prompt = "Annual revenue: [SLOT_ANNUAL_REVENUE]."
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=prompt)
    assert r.success is False
    assert r.failure_code == F_CLASS_SLOT_ID_NON_OPAQUE
    assert "[SLOT_ANNUAL_REVENUE]" in r.detail


def test_alphanumeric_payload_fails() -> None:
    prompt = "[SLOT_001A]"
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=prompt)
    assert r.success is False
    assert r.failure_code == F_CLASS_SLOT_ID_NON_OPAQUE


def test_empty_slot_id_payload_fails() -> None:
    prompt = "[SLOT_]"
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=prompt)
    assert r.success is False


def test_multiple_non_opaque_collected() -> None:
    prompt = "[SLOT_EIN] [SLOT_REVENUE] [SLOT_001]"
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=prompt)
    assert r.success is False
    # Two non-opaque, one opaque.
    assert r.matched_count == 2


def test_non_string_prompt_fails() -> None:
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=None)  # type: ignore[arg-type]
    assert r.success is False
    assert r.failure_code == F_CLASS_SLOT_ID_NON_OPAQUE


def test_rt12_unicode_devanagari_digit_rejected() -> None:
    # RT-12 closure (Cycle 1, 2026-05-10): Unicode-confusable digit
    # bypass — Python's default \d matches Devanagari १ (U+0967).
    # The opaque-ID regex must use re.ASCII so that `[SLOT_१]` is
    # treated as non-opaque (caught by _ANY_SLOT_LIKE_RE) rather than
    # silently admitted as opaque (passed by _OPAQUE_SLOT_RE).
    prompt = "Confidential: [SLOT_१]"  # Devanagari digit ONE
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=prompt)
    assert r.success is False
    assert r.failure_code == F_CLASS_SLOT_ID_NON_OPAQUE


def test_rt12_unicode_arabic_indic_digit_rejected() -> None:
    # RT-12 closure: Arabic-Indic digit ١ (U+0661) similarly excluded.
    prompt = "[SLOT_١]"
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=prompt)
    assert r.success is False
    assert r.failure_code == F_CLASS_SLOT_ID_NON_OPAQUE


def test_rt12_ascii_digits_still_pass() -> None:
    # RT-12 closure: regression check — ASCII-digit opaque slots
    # still pass under the re.ASCII flag.
    prompt = "Annual: [SLOT_001234567890]"
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=prompt)
    assert r.success is True


def test_rt12_fullwidth_ascii_digit_rejected() -> None:
    # RT-12 follow-on (2026-05-11): fullwidth-ASCII digits U+FF11..U+FF19
    # also satisfy Python's default .isdigit() == True. The procedural
    # `payload.isascii() and payload.isdigit()` classifier rejects them
    # because .isascii() is False for U+FF1x — this regression-locks the
    # fullwidth-confusable bypass surface alongside Devanagari + Arabic.
    prompt = "Confidential revenue: [SLOT_１２３]"  # U+FF11 U+FF12 U+FF13
    r = check_class_slot_id_non_opaque(cloud_routed_prompt=prompt)
    assert r.success is False
    assert r.failure_code == F_CLASS_SLOT_ID_NON_OPAQUE


# ---------------------------------------------------------------------------
# F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL
# ---------------------------------------------------------------------------


def test_cloud_received_confidential_constant() -> None:
    assert F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL == (
        "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL"
    )


def test_cloud_payload_no_confidential_passes() -> None:
    r = check_class_cloud_received_confidential(
        cloud_routed_payload="Public mission statement appears here.",
        classified_values=[
            ClassifiedValue(
                value="$1,234,567",
                class_name=CLASS_CONFIDENTIAL,
                field_path="org.annual_revenue",
            ),
        ],
    )
    assert r.success is True
    assert r.matched_count == 0


def test_confidential_literal_in_payload_fails() -> None:
    r = check_class_cloud_received_confidential(
        cloud_routed_payload="The annual revenue is $1,234,567 audited.",
        classified_values=[
            ClassifiedValue(
                value="$1,234,567",
                class_name=CLASS_CONFIDENTIAL,
                field_path="org.annual_revenue",
            ),
        ],
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL
    assert "annual_revenue" in r.detail


def test_operator_flagged_literal_in_payload_fails() -> None:
    r = check_class_cloud_received_confidential(
        cloud_routed_payload="Recipe: combine flour with water and yeast.",
        classified_values=[
            ClassifiedValue(
                value="combine flour with water and yeast",
                class_name=CLASS_OPERATOR_FLAGGED,
                field_path="org.recipe_ip",
            ),
        ],
    )
    assert r.success is False


def test_public_and_shareable_literals_ignored() -> None:
    r = check_class_cloud_received_confidential(
        cloud_routed_payload="The org name is Mystic Mamas LLC at 123 Main St.",
        classified_values=[
            ClassifiedValue(
                value="Mystic Mamas LLC",
                class_name=CLASS_PUBLIC,
                field_path="org.name",
            ),
            ClassifiedValue(
                value="123 Main St",
                class_name=CLASS_SHAREABLE,
                field_path="org.address",
            ),
        ],
    )
    assert r.success is True


def test_empty_value_skipped() -> None:
    r = check_class_cloud_received_confidential(
        cloud_routed_payload="anything goes",
        classified_values=[
            ClassifiedValue(
                value="",
                class_name=CLASS_CONFIDENTIAL,
                field_path="org.x",
            ),
        ],
    )
    assert r.success is True


def test_multiple_confidential_matches() -> None:
    r = check_class_cloud_received_confidential(
        cloud_routed_payload="A=alpha B=beta C=gamma",
        classified_values=[
            ClassifiedValue(
                value="alpha",
                class_name=CLASS_CONFIDENTIAL,
                field_path="x.a",
            ),
            ClassifiedValue(
                value="beta",
                class_name=CLASS_CONFIDENTIAL,
                field_path="x.b",
            ),
            ClassifiedValue(
                value="gamma",
                class_name=CLASS_CONFIDENTIAL,
                field_path="x.c",
            ),
        ],
    )
    assert r.success is False
    assert r.matched_count == 3


def test_non_string_payload_fails() -> None:
    r = check_class_cloud_received_confidential(
        cloud_routed_payload=None,  # type: ignore[arg-type]
        classified_values=[],
    )
    assert r.success is False


# ---------------------------------------------------------------------------
# F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED
# ---------------------------------------------------------------------------


def test_opaque_slot_filled_constant() -> None:
    assert F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED == (
        "F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED"
    )


def test_opaque_token_preserved_passes() -> None:
    payload = "Annual revenue: [SLOT_001]. Acres: [SLOT_002]."
    r = check_class_cloud_received_opaque_slot_filled(
        cloud_routed_payload=payload,
        slot_positions=[
            SlotPosition(slot_id="001"),
            SlotPosition(slot_id="002"),
        ],
    )
    assert r.success is True


def test_slot_synthesized_with_literal_fails() -> None:
    payload = "Annual revenue: $1,234,567. Acres: [SLOT_002]."
    r = check_class_cloud_received_opaque_slot_filled(
        cloud_routed_payload=payload,
        slot_positions=[
            SlotPosition(slot_id="001"),
            SlotPosition(slot_id="002"),
        ],
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED
    assert "001" in r.detail


def test_slot_with_pre_post_marker_passes() -> None:
    payload = 'Total: ">>[SLOT_007]<<" units.'
    r = check_class_cloud_received_opaque_slot_filled(
        cloud_routed_payload=payload,
        slot_positions=[
            SlotPosition(slot_id="007", pre_marker='>>', post_marker='<<'),
        ],
    )
    assert r.success is True


def test_slot_with_marker_synthesized_fails() -> None:
    payload = 'Total: ">>42<<" units.'
    r = check_class_cloud_received_opaque_slot_filled(
        cloud_routed_payload=payload,
        slot_positions=[
            SlotPosition(slot_id="007", pre_marker='>>', post_marker='<<'),
        ],
    )
    assert r.success is False


def test_malformed_slot_id_fails() -> None:
    r = check_class_cloud_received_opaque_slot_filled(
        cloud_routed_payload="payload",
        slot_positions=[SlotPosition(slot_id="REVENUE")],
    )
    assert r.success is False
    assert "malformed" in r.detail


def test_no_slot_positions_passes() -> None:
    r = check_class_cloud_received_opaque_slot_filled(
        cloud_routed_payload="anything",
        slot_positions=[],
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# F-CLASS-HIGH-STAKES-FLAG-LEAK
# ---------------------------------------------------------------------------


def test_high_stakes_leak_constant() -> None:
    assert F_CLASS_HIGH_STAKES_FLAG_LEAK == "F-CLASS-HIGH-STAKES-FLAG-LEAK"


def test_no_high_stakes_token_passes() -> None:
    r = check_class_high_stakes_flag_leak(
        cloud_routed_payload="Routine grant cycle review for next month.",
    )
    assert r.success is True


def test_high_stakes_underscored_fails() -> None:
    r = check_class_high_stakes_flag_leak(
        cloud_routed_payload='{"high_stakes": true}'
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_HIGH_STAKES_FLAG_LEAK


def test_high_stakes_hyphenated_fails() -> None:
    r = check_class_high_stakes_flag_leak(
        cloud_routed_payload="This is a high-stakes review of the grant.",
    )
    assert r.success is False


def test_high_stakes_concatenated_fails() -> None:
    r = check_class_high_stakes_flag_leak(
        cloud_routed_payload="Tagged HighStakes today.",
    )
    assert r.success is False


def test_high_stakes_case_insensitive() -> None:
    r = check_class_high_stakes_flag_leak(
        cloud_routed_payload="HIGH_STAKES",
    )
    assert r.success is False


def test_tagged_grant_id_value_fails() -> None:
    grant_id = "rfa_hash_abcdef"
    r = check_class_high_stakes_flag_leak(
        cloud_routed_payload=f"Tagged grant {grant_id} appears.",
        high_stakes_flag_values=[grant_id],
    )
    assert r.success is False
    assert grant_id in r.detail


def test_tagged_value_not_present_passes() -> None:
    r = check_class_high_stakes_flag_leak(
        cloud_routed_payload="Routine grant review.",
        high_stakes_flag_values=["rfa_hash_xyz"],
    )
    assert r.success is True


def test_non_string_payload_fails() -> None:
    r = check_class_high_stakes_flag_leak(
        cloud_routed_payload=None,  # type: ignore[arg-type]
    )
    assert r.success is False
