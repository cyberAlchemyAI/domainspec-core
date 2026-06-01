"""Unit tests for F-CIC-CLC-COUPLING-VIOLATION (four detection layers).

Per architecture v7.0.8 §4.1 (LOCKED 2026-05-08, Cycle-1 RT-02 fix).
"""

from __future__ import annotations

from typing import Iterable, Optional

from pipeline.logician.gates.f_cic_clc_coupling_violation import (
    GATE_ID,
    LAYER_1_FIELD_REGEX,
    PRE_GATE_ORDER,
    run,
)


# ---------------------------------------------------------------------------
# Helpers — convert lists to no-arg generators (Source Protocols)
# ---------------------------------------------------------------------------


def _src_field_names(items: list[tuple[str, Optional[int], str]]):
    def _r() -> Iterable:
        return iter(items)
    return _r


def _src_pydantic(items: list[tuple[str, Optional[int], str, str]]):
    def _r() -> Iterable:
        return iter(items)
    return _r


def _src_yaml(items: list[tuple[str, Optional[int], str, list[str]]]):
    def _r() -> Iterable:
        return iter(items)
    return _r


def _src_kp_manifest(items: list[tuple[str, str, str]]):
    def _r() -> Iterable:
        return iter(items)
    return _r


def _empty_sources():
    return {
        "field_name_source": _src_field_names([]),
        "pydantic_shape_source": _src_pydantic([]),
        "cic_keyed_yaml_value_source": _src_yaml([]),
        "knowledge_pack_manifest_source": _src_kp_manifest([]),
    }


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_gate_id() -> None:
    assert GATE_ID == "F-CIC-CLC-COUPLING-VIOLATION"


def test_pre_gate_order() -> None:
    assert PRE_GATE_ORDER == 6.5


# ---------------------------------------------------------------------------
# Empty world passes
# ---------------------------------------------------------------------------


def test_no_violations_passes() -> None:
    r = run(**_empty_sources())
    assert r.passed is True
    assert r.findings == ()


# ---------------------------------------------------------------------------
# Layer 1 — lexical regex
# ---------------------------------------------------------------------------


def test_layer1_primary_clc_field_caught() -> None:
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("orgs/foo/PROJECT_CONTEXT.md", 12, "primary_clc")]
    )
    r = run(**sources)
    assert r.passed is False
    assert any(f.layer == 1 for f in r.findings)
    assert any(f.subcode == f"{GATE_ID}.layer1_lexical" for f in r.findings)


def test_layer1_preferred_capital_logic_activations_caught() -> None:
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.yaml", 1, "preferred_capital_logic_activations")]
    )
    r = run(**sources)
    assert r.passed is False
    assert any(f.layer == 1 for f in r.findings)


def test_layer1_allowed_clc_subset_caught() -> None:
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.yaml", 1, "allowed_clc_subset")]
    )
    r = run(**sources)
    assert r.passed is False


def test_layer1_enabled_clc_caught() -> None:
    """Cycle-1 fix added 'enabled' and 'valid' prefixes to the regex."""
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.yaml", 1, "enabled_clc")]
    )
    r = run(**sources)
    assert r.passed is False


def test_layer1_valid_capital_logic_caught() -> None:
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.yaml", 1, "valid_capital_logic")]
    )
    r = run(**sources)
    assert r.passed is False


def test_layer1_innocent_field_passes() -> None:
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.yaml", 1, "funder_name")]
    )
    r = run(**sources)
    assert r.passed is True


def test_layer1_regex_directly() -> None:
    """Direct regex spec-pin against future regression."""
    assert LAYER_1_FIELD_REGEX.match("primary_clc")
    assert LAYER_1_FIELD_REGEX.match("preferred_capital_logic_activations")
    assert LAYER_1_FIELD_REGEX.match("PRIMARY_CLC")  # case-insensitive
    assert not LAYER_1_FIELD_REGEX.match("clc_primary_subset")  # NOT prefix-matching
    assert not LAYER_1_FIELD_REGEX.match("funder_name")


# ---------------------------------------------------------------------------
# Layer 2 — Pydantic shape
# ---------------------------------------------------------------------------


def test_layer2_dict_cic_to_list_clc_caught() -> None:
    """The classic forbidden shape."""
    sources = _empty_sources()
    sources["pydantic_shape_source"] = _src_pydantic(
        [
            (
                "pipeline/seats/scribe/models.py",
                42,
                "cic_to_clcs",
                "dict[CustomerIdentityCategory, list[CapitalLogicCard]]",
            ),
        ]
    )
    r = run(**sources)
    assert r.passed is False
    assert any(f.layer == 2 for f in r.findings)
    assert any(f.subcode == f"{GATE_ID}.layer2_pydantic_shape" for f in r.findings)


def test_layer2_innocuous_cic_field_passes() -> None:
    """A field of type CustomerIdentityCategory alone is not a coupling."""
    sources = _empty_sources()
    sources["pydantic_shape_source"] = _src_pydantic(
        [("any.py", 1, "cic_active", "list[CustomerIdentityCategory]")]
    )
    r = run(**sources)
    assert r.passed is True


def test_layer2_innocuous_clc_field_passes() -> None:
    """A field of type CapitalLogicCard alone is not a coupling."""
    sources = _empty_sources()
    sources["pydantic_shape_source"] = _src_pydantic(
        [("any.py", 1, "clc_assigned", "Optional[CapitalLogicCard]")]
    )
    r = run(**sources)
    assert r.passed is True


def test_layer2_mapping_cic_clc_caught_regardless_of_field_name() -> None:
    """The whole point of Layer 2 — name doesn't matter, shape does."""
    sources = _empty_sources()
    sources["pydantic_shape_source"] = _src_pydantic(
        [
            (
                "any.py",
                1,
                "innocent_looking_field",
                "Mapping[CustomerIdentityCategory, set[CapitalLogicCard]]",
            ),
        ]
    )
    r = run(**sources)
    assert r.passed is False
    assert any(f.layer == 2 for f in r.findings)


# ---------------------------------------------------------------------------
# Layer 3 — value-set check (catches creative renamings)
# ---------------------------------------------------------------------------


def test_layer3_funding_streams_caught() -> None:
    """The exact RT-02 evasion pattern: rename to evade Layer 1 regex."""
    sources = _empty_sources()
    sources["cic_keyed_yaml_value_source"] = _src_yaml(
        [
            (
                "pipeline/knowledge_packs/educator/manifest.yaml",
                10,
                "educator",  # CIC value as key
                ["public_purpose_works", "operating_capacity"],
            ),
        ]
    )
    r = run(**sources)
    assert r.passed is False
    assert any(f.layer == 3 for f in r.findings)
    assert any(
        f.subcode == f"{GATE_ID}.layer3_value_set" for f in r.findings
    )


def test_layer3_symmetric_clc_keyed_cic_subset_caught() -> None:
    """The reverse direction is also forbidden."""
    sources = _empty_sources()
    sources["cic_keyed_yaml_value_source"] = _src_yaml(
        [
            (
                "any.yaml",
                1,
                "operating_capacity",  # CLC value as key
                ["food_systems", "educator"],
            ),
        ]
    )
    r = run(**sources)
    assert r.passed is False
    assert any(f.layer == 3 for f in r.findings)


def test_layer3_non_canonical_key_passes() -> None:
    """If the key isn't a canonical CIC or CLC value, no coupling."""
    sources = _empty_sources()
    sources["cic_keyed_yaml_value_source"] = _src_yaml(
        [
            (
                "any.yaml",
                1,
                "tag",  # not a canonical CIC or CLC
                ["food_systems"],
            ),
        ]
    )
    r = run(**sources)
    assert r.passed is True


def test_layer3_empty_value_list_passes() -> None:
    sources = _empty_sources()
    sources["cic_keyed_yaml_value_source"] = _src_yaml(
        [("any.yaml", 1, "educator", [])]
    )
    r = run(**sources)
    assert r.passed is True


def test_layer3_value_list_with_non_canonical_member_passes() -> None:
    """If the value-list isn't a strict subset, not a coupling."""
    sources = _empty_sources()
    sources["cic_keyed_yaml_value_source"] = _src_yaml(
        [
            (
                "any.yaml",
                1,
                "educator",
                ["public_purpose_works", "made_up_value"],
            ),
        ]
    )
    r = run(**sources)
    assert r.passed is True


# ---------------------------------------------------------------------------
# Layer 4 — knowledge-pack manifest schema
# ---------------------------------------------------------------------------


def test_layer4_manifest_with_clc_field_caught() -> None:
    sources = _empty_sources()
    sources["knowledge_pack_manifest_source"] = _src_kp_manifest(
        [
            (
                "pipeline/knowledge_packs/farmer/manifest.py",
                "applies_to_clcs",
                "list[CapitalLogicCard]",
            ),
        ]
    )
    r = run(**sources)
    assert r.passed is False
    assert any(f.layer == 4 for f in r.findings)


def test_layer4_manifest_with_cic_field_passes() -> None:
    """Knowledge packs MAY carry CIC tags."""
    sources = _empty_sources()
    sources["knowledge_pack_manifest_source"] = _src_kp_manifest(
        [
            (
                "pipeline/knowledge_packs/farmer/manifest.py",
                "applies_to_cics",
                "list[CustomerIdentityCategory]",
            ),
        ]
    )
    r = run(**sources)
    assert r.passed is True


def test_layer4_optional_clc_annotation_caught() -> None:
    """Optional[CapitalLogicCard] still contains the type — caught."""
    sources = _empty_sources()
    sources["knowledge_pack_manifest_source"] = _src_kp_manifest(
        [("any.py", "preferred_clc", "Optional[CapitalLogicCard]")]
    )
    r = run(**sources)
    assert r.passed is False


# ---------------------------------------------------------------------------
# Multiple layers fire — all findings reported
# ---------------------------------------------------------------------------


def test_multiple_layers_fire_aggregates_findings() -> None:
    sources = {
        "field_name_source": _src_field_names(
            [("a.yaml", 1, "primary_clc")]
        ),
        "pydantic_shape_source": _src_pydantic(
            [
                (
                    "b.py",
                    2,
                    "x",
                    "dict[CustomerIdentityCategory, list[CapitalLogicCard]]",
                )
            ]
        ),
        "cic_keyed_yaml_value_source": _src_yaml(
            [("c.yaml", 3, "educator", ["operating_capacity"])]
        ),
        "knowledge_pack_manifest_source": _src_kp_manifest(
            [("d.py", "clcs", "list[CapitalLogicCard]")]
        ),
    }
    r = run(**sources)
    assert r.passed is False
    layers_caught = {f.layer for f in r.findings}
    assert layers_caught == {1, 2, 3, 4}
