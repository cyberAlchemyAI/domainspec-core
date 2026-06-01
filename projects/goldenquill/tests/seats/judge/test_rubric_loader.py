"""Tests for pipeline.seats.judge.rubric_loader — VAPG happy path + malformed.

Covers:
- VAPG FY26 happy-path load (real rubric JSON).
- Per-criterion shape (a/a.i/a.ii/a.iii / b / c / d / e / f/f.i/f.ii / g).
- Hash reproducibility across two loads.
- Canonical-bytes hash is dict-order-independent.
- compute_rubric_sha256 over hand-canonicalized payload matches load_rubric.
- Malformed file paths: missing meta, duplicate id, bad JSON, BOM-prefixed,
  bad UTF-8, non-object top-level, missing scoring_criteria, missing meta
  keys, non-int score band, score-band inversion, max_score < sum.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.seats.judge.rubric_loader import (
    compute_rubric_sha256,
    load_rubric,
)
from pipeline.seats.judge.types import F_JUDGE_RUBRIC_MALFORMED


REPO_ROOT = Path(__file__).resolve().parents[3]
LIVE_VAPG = REPO_ROOT / "pipeline" / "rubrics" / "vapg_fy26.json"
CORPUS_VAPG = (
    REPO_ROOT
    / "tests"
    / "corpus"
    / "judge"
    / "v1"
    / "vapg_fy26_happy_path"
    / "vapg_fy26.json"
)
CORPUS_MALFORMED_DIR = REPO_ROOT / "tests" / "corpus" / "judge" / "v1" / "malformed"


def _fixed_clock():
    return datetime(2026, 4, 29, 12, 0, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Happy-path: real VAPG FY26 rubric
# ---------------------------------------------------------------------------


class TestVapgHappyPath:
    def test_live_rubric_loads(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        assert r.program_code == "Value-Added Producer Grant (VAPG)"
        assert r.funder == "USDA Rural Development"
        assert r.nofo_number == "RDBCP-VAPG-2026"
        assert r.max_score == 100
        assert r.min_score == 50

    def test_live_rubric_has_seven_criteria(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        assert len(r.criteria) == 7
        ids = [c.id for c in r.criteria]
        assert ids == ["a", "b", "c", "d", "e", "f", "g"]

    def test_corpus_copy_loads_identically(self):
        live = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        corpus = load_rubric(CORPUS_VAPG, clock=_fixed_clock)
        assert live.rubric_sha256 == corpus.rubric_sha256

    def test_criterion_a_flattens_to_three_subcriteria(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        a = next(c for c in r.criteria if c.id == "a")
        assert a.max_points == 30
        assert len(a.subcriteria) == 3
        sub_ids = [s.id for s in a.subcriteria]
        assert sub_ids == ["a.i", "a.ii", "a.iii"]
        assert sum(s.max_points for s in a.subcriteria) == 30

    def test_criterion_a_subcriteria_have_must_address(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        a = next(c for c in r.criteria if c.id == "a")
        a_i = next(s for s in a.subcriteria if s.id == "a.i")
        assert "Value-added process description" in a_i.must_address

    def test_criterion_b_has_no_subcriteria(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        b = next(c for c in r.criteria if c.id == "b")
        assert b.subcriteria == ()
        assert len(b.tiers) == 5

    def test_criterion_b_scorer(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        b = next(c for c in r.criteria if c.id == "b")
        assert b.scorer == "review_panel"

    def test_criterion_d_scorer_state_office(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        d = next(c for c in r.criteria if c.id == "d")
        assert d.scorer == "state_office"

    def test_criterion_g_scorer_administrator(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        g = next(c for c in r.criteria if c.id == "g")
        assert g.scorer == "administrator"
        assert g.max_points == 10

    def test_criterion_f_two_subcriteria(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        f = next(c for c in r.criteria if c.id == "f")
        assert f.max_points == 10
        assert len(f.subcriteria) == 2
        sub_ids = [s.id for s in f.subcriteria]
        assert sub_ids == ["f.i", "f.ii"]

    def test_sum_criterion_max_equals_max_score(self):
        # VAPG: 30 + 20 + 20 + 5 + 5 + 10 + 10 = 100.
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        assert sum(c.max_points for c in r.criteria) == r.max_score

    def test_loaded_at_utc_pinned_via_clock(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        assert r.loaded_at_utc == _fixed_clock()
        assert r.loaded_at_utc.tzinfo is not None

    def test_default_clock_is_tz_aware(self):
        r = load_rubric(LIVE_VAPG)
        assert r.loaded_at_utc.tzinfo is not None


# ---------------------------------------------------------------------------
# Hash reproducibility + canonicalization discipline
# ---------------------------------------------------------------------------


class TestHashReproducibility:
    def test_two_loads_same_hash(self):
        a = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        b = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        assert a.rubric_sha256 == b.rubric_sha256

    def test_hash_format_64_hex_lowercase(self):
        r = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        assert len(r.rubric_sha256) == 64
        assert r.rubric_sha256 == r.rubric_sha256.lower()
        assert all(ch in "0123456789abcdef" for ch in r.rubric_sha256)

    def test_dict_order_independent_hash(self, tmp_path):
        # Build two JSON files with dict keys reordered; load_rubric should
        # produce identical rubric_sha256 since canonicalization sorts keys.
        payload_natural = {
            "meta": {
                "funder": "F",
                "program": "P",
                "nofo_number": "N",
                "min_score": 0,
                "max_score": 30,
            },
            "scoring_criteria": [
                {
                    "id": "a",
                    "name": "A",
                    "max_points": 30,
                    "scorer": "review_panel",
                    "tiers": [{"points": 5, "description": "ok"}],
                }
            ],
        }
        # Reverse key order on the meta dict.
        payload_reordered = {
            "scoring_criteria": payload_natural["scoring_criteria"],
            "meta": dict(reversed(list(payload_natural["meta"].items()))),
        }
        p1 = tmp_path / "natural.json"
        p2 = tmp_path / "reordered.json"
        # Force non-canonical (preserve ordering) on disk.
        p1.write_text(
            json.dumps(payload_natural, indent=2, sort_keys=False),
            encoding="utf-8",
        )
        p2.write_text(
            json.dumps(payload_reordered, indent=2, sort_keys=False),
            encoding="utf-8",
        )
        a = load_rubric(p1, clock=_fixed_clock)
        b = load_rubric(p2, clock=_fixed_clock)
        assert a.rubric_sha256 == b.rubric_sha256

    def test_compute_rubric_sha256_canonical_input(self):
        payload = {"a": 1, "b": [1, 2, 3]}
        canonical = json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        h = compute_rubric_sha256(canonical)
        assert len(h) == 64
        # Reordered input → same canonical bytes → same hash.
        canonical2 = json.dumps(
            {"b": [1, 2, 3], "a": 1},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        assert compute_rubric_sha256(canonical2) == h

    def test_hash_changes_when_value_changes(self, tmp_path):
        original = json.loads(LIVE_VAPG.read_text())
        modified = dict(original)
        modified["meta"] = dict(original["meta"])
        modified["meta"]["nofo_number"] = "DRIFT-001"
        p = tmp_path / "drifted.json"
        p.write_text(json.dumps(modified), encoding="utf-8")
        original_rubric = load_rubric(LIVE_VAPG, clock=_fixed_clock)
        drifted_rubric = load_rubric(p, clock=_fixed_clock)
        assert original_rubric.rubric_sha256 != drifted_rubric.rubric_sha256


# ---------------------------------------------------------------------------
# Malformed-fixture corpus
# ---------------------------------------------------------------------------


class TestMalformedFixtureCorpus:
    def test_missing_meta_rejected(self):
        path = CORPUS_MALFORMED_DIR / "missing_meta.json"
        with pytest.raises(ValueError, match="meta"):
            load_rubric(path, clock=_fixed_clock)

    def test_duplicate_criterion_id_rejected(self):
        path = CORPUS_MALFORMED_DIR / "duplicate_criterion_id.json"
        with pytest.raises(ValueError, match="duplicate criterion id"):
            load_rubric(path, clock=_fixed_clock)


# ---------------------------------------------------------------------------
# Inline malformed inputs (tmp_path)
# ---------------------------------------------------------------------------


class TestMalformedInlineInputs:
    def test_missing_file_raises_filenotfound(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_rubric(tmp_path / "nope.json", clock=_fixed_clock)

    def test_bad_json_rejected(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("{ this is not json", encoding="utf-8")
        with pytest.raises(ValueError, match="not valid JSON"):
            load_rubric(p, clock=_fixed_clock)

    def test_bom_prefixed_rejected(self, tmp_path):
        p = tmp_path / "bom.json"
        p.write_bytes(b"\xef\xbb\xbf{}")
        with pytest.raises(ValueError, match="UTF-8 BOM"):
            load_rubric(p, clock=_fixed_clock)

    def test_invalid_utf8_rejected(self, tmp_path):
        p = tmp_path / "bad_utf8.json"
        # Single 0xff byte is not valid UTF-8.
        p.write_bytes(b"\xff{}")
        with pytest.raises(ValueError, match="not valid UTF-8"):
            load_rubric(p, clock=_fixed_clock)

    def test_top_level_array_rejected(self, tmp_path):
        p = tmp_path / "array.json"
        p.write_text("[]", encoding="utf-8")
        with pytest.raises(ValueError, match="top-level must be"):
            load_rubric(p, clock=_fixed_clock)

    def test_meta_not_object_rejected(self, tmp_path):
        p = tmp_path / "bad_meta.json"
        p.write_text(
            json.dumps({"meta": "not-an-object", "scoring_criteria": []}),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="meta must be a JSON object"):
            load_rubric(p, clock=_fixed_clock)

    def test_meta_missing_program_rejected(self, tmp_path):
        p = tmp_path / "no_program.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="meta.program"):
            load_rubric(p, clock=_fixed_clock)

    def test_meta_missing_funder_rejected(self, tmp_path):
        p = tmp_path / "no_funder.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="meta.funder"):
            load_rubric(p, clock=_fixed_clock)

    def test_meta_missing_nofo_number_rejected(self, tmp_path):
        p = tmp_path / "no_nofo.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="meta.nofo_number"):
            load_rubric(p, clock=_fixed_clock)

    def test_min_score_not_int_rejected(self, tmp_path):
        p = tmp_path / "bad_min.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": "fifty",
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="meta.min_score must be an int"):
            load_rubric(p, clock=_fixed_clock)

    def test_max_score_bool_rejected(self, tmp_path):
        # bool is int subclass — explicit reject for safety.
        p = tmp_path / "bool_max.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": True,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 0,
                            "scorer": "review_panel",
                            "tiers": [{"points": 0, "description": "z"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="meta.max_score must be an int"):
            load_rubric(p, clock=_fixed_clock)

    def test_min_greater_than_max_rejected(self, tmp_path):
        p = tmp_path / "inverted.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 100,
                        "max_score": 50,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match=r"min_score.*max_score"):
            load_rubric(p, clock=_fixed_clock)

    def test_negative_min_score_rejected(self, tmp_path):
        p = tmp_path / "neg_min.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": -1,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="must be >= 0"):
            load_rubric(p, clock=_fixed_clock)

    def test_scoring_criteria_missing_rejected(self, tmp_path):
        p = tmp_path / "no_scoring.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    }
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="scoring_criteria"):
            load_rubric(p, clock=_fixed_clock)

    def test_scoring_criteria_empty_rejected(self, tmp_path):
        p = tmp_path / "empty_scoring.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="scoring_criteria"):
            load_rubric(p, clock=_fixed_clock)

    def test_criterion_missing_id_rejected(self, tmp_path):
        p = tmp_path / "no_id.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="id"):
            load_rubric(p, clock=_fixed_clock)

    def test_criterion_missing_max_points_rejected(self, tmp_path):
        p = tmp_path / "no_max.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "scorer": "review_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="max_points"):
            load_rubric(p, clock=_fixed_clock)

    def test_criterion_unknown_scorer_rejected(self, tmp_path):
        p = tmp_path / "bad_scorer.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "judge_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="scorer must be one of"):
            load_rubric(p, clock=_fixed_clock)

    def test_max_score_below_sum_rejected(self, tmp_path):
        p = tmp_path / "below_sum.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 10,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="max_score .* < sum"):
            load_rubric(p, clock=_fixed_clock)

    def test_subcriteria_not_array_rejected(self, tmp_path):
        p = tmp_path / "bad_sub.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "subcriteria": "not-an-array",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="subcriteria must be"):
            load_rubric(p, clock=_fixed_clock)

    def test_criterion_negative_max_points_rejected(self, tmp_path):
        p = tmp_path / "neg_crit.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": -3,
                            "scorer": "review_panel",
                            "tiers": [{"points": 0, "description": "z"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="max_points must be >= 0"):
            load_rubric(p, clock=_fixed_clock)

    def test_subcriterion_negative_max_points_rejected(self, tmp_path):
        p = tmp_path / "neg_sub.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "subcriteria": [
                                {
                                    "id": "a.i",
                                    "name": "Sub",
                                    "max_points": -5,
                                }
                            ],
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="max_points must be >= 0"):
            load_rubric(p, clock=_fixed_clock)

    def test_must_address_not_array_rejected(self, tmp_path):
        p = tmp_path / "bad_must.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "must_address": "should-be-list",
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="must_address must be"):
            load_rubric(p, clock=_fixed_clock)

    def test_must_address_non_string_item_rejected(self, tmp_path):
        p = tmp_path / "bad_must2.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "must_address": ["ok", 42],
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="must_address.*must be a string"):
            load_rubric(p, clock=_fixed_clock)

    def test_tiers_not_array_rejected(self, tmp_path):
        p = tmp_path / "bad_tiers.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": "should-be-list",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="tiers must be"):
            load_rubric(p, clock=_fixed_clock)

    def test_tier_entry_not_object_rejected(self, tmp_path):
        p = tmp_path / "bad_tier_entry.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "tiers": ["not-an-object"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match=r"tiers\[0\] must be"):
            load_rubric(p, clock=_fixed_clock)

    def test_scoring_entry_not_object_rejected(self, tmp_path):
        p = tmp_path / "bad_entry.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": ["not-an-object"],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="scoring_criteria entry"):
            load_rubric(p, clock=_fixed_clock)

    def test_subcriteria_entry_not_object_rejected(self, tmp_path):
        p = tmp_path / "bad_sub_entry.json"
        p.write_text(
            json.dumps(
                {
                    "meta": {
                        "program": "P",
                        "funder": "F",
                        "nofo_number": "N",
                        "min_score": 0,
                        "max_score": 100,
                    },
                    "scoring_criteria": [
                        {
                            "id": "a",
                            "name": "A",
                            "max_points": 30,
                            "scorer": "review_panel",
                            "subcriteria": ["not-an-object"],
                            "tiers": [{"points": 5, "description": "ok"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="subcriteria entry"):
            load_rubric(p, clock=_fixed_clock)

    def test_failure_messages_carry_f_code(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("not json", encoding="utf-8")
        with pytest.raises(ValueError) as exc:
            load_rubric(p, clock=_fixed_clock)
        assert F_JUDGE_RUBRIC_MALFORMED in str(exc.value)
