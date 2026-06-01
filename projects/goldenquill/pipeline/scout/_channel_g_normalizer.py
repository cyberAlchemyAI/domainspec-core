import re
from typing import Optional

from pipeline.scout._channel_g_types import (
    BoardCategoryEnum,
    CycleStatusEnum,
    DeadlineStatusEnum,
    EligibilityStatusEnum,
    NormalizedScore,
    ScoringStatusEnum,
    SourceFreshnessStatusEnum,
)

NOW_SCORE_THRESHOLD = 80.0
PARK_SCORE_THRESHOLD = 50.0

def normalize_score(
    raw_value: object | None, alias_context: str | None = None
) -> NormalizedScore:
    if raw_value is None or str(raw_value).strip() == "":
        return NormalizedScore(
            scoring_status=ScoringStatusEnum.UNAVAILABLE,
            raw_value=None,
            normalized_value=None,
            score_scale=None,
            rationale=None,
        )

    raw_str = str(raw_value).strip()
    raw_str_lower = raw_str.lower()

    # Categorical
    if raw_str_lower in {"high", "strong"}:
        return NormalizedScore(
            scoring_status=ScoringStatusEnum.SCORED,
            raw_value=raw_str,
            normalized_value=85.0,
            score_scale="categorical_high_medium_low",
            rationale=None,
        )
    elif raw_str_lower in {"medium", "med", "moderate"}:
        return NormalizedScore(
            scoring_status=ScoringStatusEnum.SCORED,
            raw_value=raw_str,
            normalized_value=50.0,
            score_scale="categorical_high_medium_low",
            rationale=None,
        )
    elif raw_str_lower in {"low", "weak"}:
        return NormalizedScore(
            scoring_status=ScoringStatusEnum.SCORED,
            raw_value=raw_str,
            normalized_value=15.0,
            score_scale="categorical_high_medium_low",
            rationale=None,
        )

    # Fractions (e.g., 4/5, 8/10, optionally with notes)
    # Matches "4/5" or "4 / 5" at the start of the string, or anywhere if it's the only numbers.
    # We want to be careful. Let's look for a fraction pattern.
    fraction_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', raw_str)
    if fraction_match:
        try:
            num = float(fraction_match.group(1))
            den = float(fraction_match.group(2))
            if den != 0:
                norm = (num / den) * 100
                rationale = raw_str if len(raw_str) > len(fraction_match.group(0)) + 2 else None
                return NormalizedScore(
                    scoring_status=ScoringStatusEnum.SCORED,
                    raw_value=raw_str,
                    normalized_value=norm,
                    score_scale=f"0-{int(den) if den.is_integer() else den}",
                    rationale=rationale,
                )
        except ValueError:
            pass

    # Percentage (e.g., 85%)
    perc_match = re.search(r'(\d+(?:\.\d+)?)\s*%', raw_str)
    if perc_match:
        try:
            val = float(perc_match.group(1))
            rationale = raw_str if len(raw_str) > len(perc_match.group(0)) + 2 else None
            return NormalizedScore(
                scoring_status=ScoringStatusEnum.SCORED,
                raw_value=raw_str,
                normalized_value=val,
                score_scale="0-100",
                rationale=rationale,
            )
        except ValueError:
            pass

    # Bare numeric
    # Check if the string is just a number (or a number followed by a dash/note)
    bare_match = re.match(r'^(\d+(?:\.\d+)?)(?:\s*-\s*(.*))?$', raw_str)
    if bare_match:
        try:
            val = float(bare_match.group(1))
            note = bare_match.group(2)
            rationale = note.strip() if note else None

            # >10 and <= 100 -> assume 0-100 scale
            if 10 < val <= 100:
                return NormalizedScore(
                    scoring_status=ScoringStatusEnum.SCORED,
                    raw_value=raw_str,
                    normalized_value=val,
                    score_scale="0-100",
                    rationale=rationale,
                )

            # <= 10 needs explicit scale in alias_context
            if val <= 10:
                ctx = (alias_context or "").lower()
                if "1-5" in ctx or "out of 5" in ctx:
                    return NormalizedScore(
                        scoring_status=ScoringStatusEnum.SCORED,
                        raw_value=raw_str,
                        normalized_value=(val / 5) * 100,
                        score_scale="1-5",
                        rationale=rationale,
                    )
                elif "1-10" in ctx or "out of 10" in ctx:
                    return NormalizedScore(
                        scoring_status=ScoringStatusEnum.SCORED,
                        raw_value=raw_str,
                        normalized_value=(val / 10) * 100,
                        score_scale="1-10",
                        rationale=rationale,
                    )
                elif "0-100" in ctx or "percent" in ctx or "percentage" in ctx:
                    return NormalizedScore(
                        scoring_status=ScoringStatusEnum.SCORED,
                        raw_value=raw_str,
                        normalized_value=val,
                        score_scale="0-100",
                        rationale=rationale,
                    )
                else:
                    msg = "Bare numeric value requires explicit scale confirmation."
                    if rationale:
                        msg = f"{msg} Original note: {rationale}"
                    return NormalizedScore(
                        scoring_status=ScoringStatusEnum.NOT_YET_SCORED,
                        raw_value=raw_str,
                        normalized_value=None,
                        score_scale=None,
                        rationale=msg,
                    )
        except ValueError:
            pass

    # Unrecognized text
    return NormalizedScore(
        scoring_status=ScoringStatusEnum.NOT_YET_SCORED,
        raw_value=raw_str,
        normalized_value=None,
        score_scale=None,
        rationale=raw_str,
    )


def normalize_board_category_alias(raw_value: str | None) -> BoardCategoryEnum | None:
    if not raw_value:
        return None
    val = raw_value.strip().lower()
    if val in {"immediate", "high fit", "now"}:
        return BoardCategoryEnum.NOW
    elif val in {"prep", "needs work", "prepare"}:
        return BoardCategoryEnum.PREPARE
    elif val in {"watch", "later", "monitor"}:
        return BoardCategoryEnum.MONITOR
    elif val in {"partner", "consortium", "partner / consortium"}:
        return BoardCategoryEnum.PARTNER_CONSORTIUM
    elif val in {"next cycle"}:
        return BoardCategoryEnum.NEXT_CYCLE
    elif val in {"park", "low fit", "ineligible"}:
        return BoardCategoryEnum.PARK
    return None


def normalize_eligibility_status(raw_value: str | None) -> EligibilityStatusEnum:
    if not raw_value:
        return EligibilityStatusEnum.UNKNOWN
    val = raw_value.strip().lower()
    if val in {"true", "yes", "eligible", "confirmed", "confirmed true"}:
        return EligibilityStatusEnum.CONFIRMED_TRUE
    elif val in {"false", "no", "ineligible", "not eligible", "confirmed false"}:
        return EligibilityStatusEnum.CONFIRMED_FALSE
    elif val in {"needs check", "review", "check"}:
        return EligibilityStatusEnum.NEEDS_CHECK
    return EligibilityStatusEnum.UNKNOWN


def normalize_deadline_status(raw_value: str | None) -> DeadlineStatusEnum:
    if not raw_value:
        return DeadlineStatusEnum.UNKNOWN
    val = raw_value.strip().lower()
    if val in {"open", "current", "active"}:
        return DeadlineStatusEnum.OPEN
    elif val in {"closed", "past", "expired"}:
        return DeadlineStatusEnum.CLOSED
    elif val in {"rolling"}:
        return DeadlineStatusEnum.ROLLING
    return DeadlineStatusEnum.UNKNOWN


def normalize_cycle_status(raw_value: str | None) -> CycleStatusEnum:
    if not raw_value:
        return CycleStatusEnum.UNKNOWN
    val = raw_value.strip().lower()
    if val in {"current"}:
        return CycleStatusEnum.CURRENT
    elif val in {"recurring", "annual", "next cycle", "likely recurring"}:
        return CycleStatusEnum.RECURRING
    elif val in {"one time", "one-time", "nonrecurring", "non-recurring"}:
        return CycleStatusEnum.ONE_TIME
    return CycleStatusEnum.UNKNOWN


def normalize_source_freshness_status(raw_value: str | None) -> SourceFreshnessStatusEnum:
    if not raw_value:
        return SourceFreshnessStatusEnum.NOT_YET_DETERMINED
    val = raw_value.strip().lower()
    if val in {"current", "verified", "fresh"}:
        return SourceFreshnessStatusEnum.CURRENT
    elif val in {"stale", "outdated", "old"}:
        return SourceFreshnessStatusEnum.STALE
    elif val in {"pending", "pending source configuration"}:
        return SourceFreshnessStatusEnum.PENDING_SOURCE_CONFIGURATION
    elif val in {"unavailable", "not available"}:
        return SourceFreshnessStatusEnum.UNAVAILABLE
    elif val in {"unknown"}:
        return SourceFreshnessStatusEnum.UNKNOWN
    elif val in {"not yet determined", "not_yet_determined"}:
        return SourceFreshnessStatusEnum.NOT_YET_DETERMINED
    return SourceFreshnessStatusEnum.NOT_YET_DETERMINED


def normalize_bool(raw_value: str | bool | None, *, default: bool = False) -> bool:
    if raw_value is None or raw_value == "":
        return default
    if isinstance(raw_value, bool):
        return raw_value
    val = str(raw_value).strip().lower()
    if val in {"true", "yes", "y", "1", "required"}:
        return True
    if val in {"false", "no", "n", "0", "not required"}:
        return False
    return default


def allocate_board_category(
    *,
    raw_lane_category: str | None,
    eligibility_status: EligibilityStatusEnum,
    deadline_status: DeadlineStatusEnum,
    cycle_status: CycleStatusEnum,
    partner_requirement: bool,
    partner_confirmed: bool,
    has_active_hard_blocker: bool,
    source_freshness_status: SourceFreshnessStatusEnum,
    total_score: NormalizedScore,
) -> BoardCategoryEnum:

    if eligibility_status == EligibilityStatusEnum.CONFIRMED_FALSE:
        return BoardCategoryEnum.PARK

    if deadline_status == DeadlineStatusEnum.CLOSED and cycle_status != CycleStatusEnum.RECURRING:
        return BoardCategoryEnum.PARK

    if deadline_status == DeadlineStatusEnum.CLOSED and cycle_status == CycleStatusEnum.RECURRING:
        return BoardCategoryEnum.NEXT_CYCLE

    if partner_requirement and not partner_confirmed:
        return BoardCategoryEnum.PARTNER_CONSORTIUM

    norm_score = total_score.normalized_value

    if (
        norm_score is not None
        and norm_score >= NOW_SCORE_THRESHOLD
        and not has_active_hard_blocker
        and deadline_status in {DeadlineStatusEnum.OPEN, DeadlineStatusEnum.ROLLING, DeadlineStatusEnum.UNKNOWN}
        and source_freshness_status != SourceFreshnessStatusEnum.STALE
    ):
        return BoardCategoryEnum.NOW

    if norm_score is not None and norm_score >= NOW_SCORE_THRESHOLD and has_active_hard_blocker:
        return BoardCategoryEnum.PREPARE

    if norm_score is not None and norm_score < PARK_SCORE_THRESHOLD:
        return BoardCategoryEnum.PARK

    if source_freshness_status in {
        SourceFreshnessStatusEnum.UNKNOWN,
        SourceFreshnessStatusEnum.NOT_YET_DETERMINED,
        SourceFreshnessStatusEnum.PENDING_SOURCE_CONFIGURATION,
        SourceFreshnessStatusEnum.UNAVAILABLE
    }:
        return BoardCategoryEnum.MONITOR

    alias_cat = normalize_board_category_alias(raw_lane_category)
    if alias_cat is not None:
        return alias_cat

    return BoardCategoryEnum.MONITOR
