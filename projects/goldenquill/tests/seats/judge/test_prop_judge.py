"""Property tests for pipeline.seats.judge — seeded ``random.Random`` fuzz.

Property tests are hand-rolled with seeded ``random.Random`` — hypothesis is
not installed in this venv. Matches §1 Round J / Scribe R1 precedent.

Covers:
- Rubric load → re-canonicalize → re-hash round trip yields identical
  rubric_sha256 across random VAPG-shape permutations.
- compute_rubric_sha256 is 64 hex lowercase across arbitrary byte input.
- score_dimension is deterministic over fixed (draft, criterion, fake-llm,
  fixed clock).
- CriterionScore __post_init__ holds for random (score, max_points) pairs.
- RubricSubCriterion construction is invariant under random ids.
"""

from __future__ import annotations

import hashlib
import json
import random
import string
from datetime import datetime, timezone

import pytest

from pipeline.seats.judge.dimension_scorer import score_dimension
from pipeline.seats.judge.rubric_loader import compute_rubric_sha256, load_rubric
from pipeline.seats.judge.types import (
    CriterionScore,
    RubricCriterion,
    RubricSubCriterion,
)


UTC_NOW = datetime(2026, 4, 29, 12, 0, 0, tzinfo=timezone.utc)


def _random_name(rng: random.Random, max_len: int = 12) -> str:
    n = rng.randint(1, max_len)
    return "".join(rng.choices(string.ascii_letters, k=n))


def _random_payload(rng: random.Random) -> dict:
    n_crit = rng.randint(1, 4)
    criteria = []
    seen_ids: set[str] = set()
    for i in range(n_crit):
        # Deterministic ids: crit_0, crit_1 ... so duplicates can't occur.
        cid = f"crit_{i}"
        seen_ids.add(cid)
        criteria.append(
            {
                "id": cid,
                "name": _random_name(rng),
                "max_points": rng.randint(1, 20),
                "scorer": rng.choice(
                    ["review_panel", "state_office", "administrator"]
                ),
                "tiers": [
                    {
                        "points": rng.randint(0, 20),
                        "description": _random_name(rng),
                    }
                ],
            }
        )
    sum_max = sum(c["max_points"] for c in criteria)
    max_score = sum_max + rng.randint(0, 10)
    min_score = rng.randint(0, max_score)
    return {
        "meta": {
            "program": _random_name(rng),
            "funder": _random_name(rng),
            "nofo_number": _random_name(rng),
            "min_score": min_score,
            "max_score": max_score,
        },
        "scoring_criteria": criteria,
    }


# ---------------------------------------------------------------------------
# Canonical-bytes round-trip property
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("seed", range(50))
def test_canonical_round_trip_identity(tmp_path, seed):
    rng = random.Random(seed)
    payload = _random_payload(rng)

    p_natural = tmp_path / "n.json"
    p_reversed = tmp_path / "r.json"
    p_natural.write_text(
        json.dumps(payload, sort_keys=False, indent=2),
        encoding="utf-8",
    )
    payload_reversed = {
        "scoring_criteria": payload["scoring_criteria"],
        "meta": dict(reversed(list(payload["meta"].items()))),
    }
    p_reversed.write_text(
        json.dumps(payload_reversed, sort_keys=False, indent=2),
        encoding="utf-8",
    )
    a = load_rubric(p_natural, clock=lambda: UTC_NOW)
    b = load_rubric(p_reversed, clock=lambda: UTC_NOW)
    assert a.rubric_sha256 == b.rubric_sha256


# ---------------------------------------------------------------------------
# compute_rubric_sha256 format property
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("seed", range(100))
def test_compute_rubric_sha256_format(seed):
    rng = random.Random(seed)
    raw = bytes(rng.randint(0, 255) for _ in range(rng.randint(0, 256)))
    h = compute_rubric_sha256(raw)
    assert len(h) == 64
    assert h == h.lower()
    assert all(ch in "0123456789abcdef" for ch in h)
    assert h == hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------------------
# score_dimension determinism property
# ---------------------------------------------------------------------------


class _FakeDraft:
    def __init__(self, body: str):
        self.section_name = "S"
        self.section_order = 1
        self.body_text = body
        self.claim_evidence_map: tuple = ()


def _crit_max20() -> RubricCriterion:
    return RubricCriterion(
        id="b",
        name="Q",
        max_points=20,
        scorer="review_panel",
        subcriteria=(),
        must_address=("foo",),
        tiers=({"points": 5, "description": "ok"},),
    )


@pytest.mark.parametrize("seed", range(50))
def test_score_dimension_deterministic(seed):
    rng = random.Random(seed)
    score = rng.randint(0, 20)
    confidence = rng.uniform(0.0, 1.0)

    response = json.dumps(
        {
            "score": score,
            "evidence_quote": "body",
            "confidence": confidence,
            "rationale": "ok",
        }
    )

    def _llm(*, prompt: str, max_tokens: int) -> str:
        return response

    cs1 = score_dimension(
        (_FakeDraft("body"),),
        _crit_max20(),
        llm_call=_llm,
        clock=lambda: UTC_NOW,
    )
    cs2 = score_dimension(
        (_FakeDraft("body"),),
        _crit_max20(),
        llm_call=_llm,
        clock=lambda: UTC_NOW,
    )
    assert cs1 == cs2
    assert cs1.score == score
    assert abs(cs1.confidence - confidence) < 1e-9


# ---------------------------------------------------------------------------
# CriterionScore invariants under random score / confidence values
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("seed", range(100))
def test_criterion_score_invariants(seed):
    rng = random.Random(seed)
    score = rng.randint(-100, 100)
    if score < 0:
        with pytest.raises(ValueError):
            CriterionScore(
                criterion_id="b",
                score=score,
                evidence_quote="x",
                confidence=0.5,
                rationale="ok",
            )
    else:
        cs = CriterionScore(
            criterion_id="b",
            score=score,
            evidence_quote="x",
            confidence=0.5,
            rationale="ok",
        )
        assert cs.score == score


@pytest.mark.parametrize("seed", range(100))
def test_criterion_score_confidence_bounds(seed):
    rng = random.Random(seed)
    # Equal mix of in-range and out-of-range.
    if rng.random() < 0.5:
        confidence = rng.uniform(0.0, 1.0)
        cs = CriterionScore(
            criterion_id="b",
            score=5,
            evidence_quote="x",
            confidence=confidence,
            rationale="y",
        )
        assert cs.confidence == confidence
    else:
        confidence = rng.choice([rng.uniform(-100, -0.001), rng.uniform(1.001, 100)])
        with pytest.raises(ValueError, match=r"confidence must be in"):
            CriterionScore(
                criterion_id="b",
                score=5,
                evidence_quote="x",
                confidence=confidence,
                rationale="y",
            )


# ---------------------------------------------------------------------------
# Subcriterion construction property
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("seed", range(50))
def test_subcriterion_invariants(seed):
    rng = random.Random(seed)
    sub_id = "".join(rng.choices(string.ascii_lowercase + ".", k=rng.randint(1, 8)))
    sub_id = sub_id.replace(" ", "x")  # avoid empty
    if not sub_id.strip():
        sub_id = "x.i"
    sub_max = rng.randint(0, 50)
    sub = RubricSubCriterion(
        id=sub_id,
        name="N",
        max_points=sub_max,
        must_address=(),
        tiers=({"points": 0, "description": "ok"},),
    )
    assert sub.id == sub_id
    assert sub.max_points == sub_max
