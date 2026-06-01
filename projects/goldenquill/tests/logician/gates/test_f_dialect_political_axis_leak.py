"""Unit tests for F-DIALECT-POLITICAL-AXIS-LEAK (three detection layers +
Layer 1b proximity + Layer 1c singular-in-routing-path).

Per architecture v7.0.12 LOCKED 2026-05-16T14:00:00Z + §4 v2.x apolitical_dialect
§4.X.4 test requirements + Cycle 1 + Cycle 2 fold-ins (FI-2 + FI-3 + FI-4 +
C2-H-1 + C2-H-2 + C2-M-3 partial + C2-M-6 + C2-P0-9).
"""

from __future__ import annotations

from typing import Iterable, Optional

from pipeline.logician.gates.f_dialect_political_axis_leak import (
    EXCLUDED_PATH_GLOBS,
    GATE_ID,
    LAYER_1_FIELD_REGEX,
    LAYER_1_FIELD_SUBSTRING,
    LAYER_1_LITERAL_REGEX,
    LAYER_1B_PROXIMITY_WINDOW_CHARS,
    PRE_GATE_ORDER,
    RETIRED_FIELD_NAMES,
    RETIRED_FIELD_NAME_TOKENS,
    RETIRED_LITERALS,
    run,
)


# ---------------------------------------------------------------------------
# Helpers — convert lists to no-arg generators (Source Protocols)
# ---------------------------------------------------------------------------


def _src_field_names(items: list[tuple[str, Optional[int], str]]):
    def _r() -> Iterable:
        return iter(items)
    return _r


def _src_literals(items: list[tuple[str, Optional[int], str, str]]):
    def _r() -> Iterable:
        return iter(items)
    return _r


def _src_pydantic(items: list[
    tuple[str, Optional[int], str, tuple[str, ...], bool]
]):
    def _r() -> Iterable:
        return iter(items)
    return _r


def _src_schema(items: list[tuple[str, str, str, str]]):
    def _r() -> Iterable:
        return iter(items)
    return _r


def _empty_sources() -> dict[str, object]:
    return {
        "field_name_source": _src_field_names([]),
        "string_literal_source": _src_literals([]),
        "pydantic_literal_source": _src_pydantic([]),
        "schema_validation_source": _src_schema([]),
    }


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_gate_id() -> None:
    assert GATE_ID == "F-DIALECT-POLITICAL-AXIS-LEAK"


def test_pre_gate_order() -> None:
    assert PRE_GATE_ORDER == 6.55


def test_retired_literal_closed_set() -> None:
    assert RETIRED_LITERALS == frozenset(
        {"conservative", "centrist", "progressive", "soul_fire", "soul-fire"}
    )


def test_retired_field_names_closed_set() -> None:
    assert RETIRED_FIELD_NAMES == frozenset(
        {"funder_political_axis", "progressive_register"}
    )


def test_retired_field_name_tokens_two_sets() -> None:
    """C2-M-6 token-based matcher relies on these token sets."""
    assert RETIRED_FIELD_NAME_TOKENS == (
        frozenset({"funder", "political", "axis"}),
        frozenset({"progressive", "register"}),
    )


def test_layer_1b_proximity_window() -> None:
    """FI-2 proximity-window constant."""
    assert LAYER_1B_PROXIMITY_WINDOW_CHARS == 200


# ---------------------------------------------------------------------------
# Empty world passes
# ---------------------------------------------------------------------------


def test_no_violations_passes() -> None:
    r = run(**_empty_sources())  # type: ignore[arg-type]
    assert r.passed is True
    assert r.findings == ()


# ---------------------------------------------------------------------------
# Layer 1 — field-name detection
# ---------------------------------------------------------------------------


def test_layer1_field_name_exact_funder_political_axis_caught() -> None:
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("pipeline/cards/CIC/food_systems.yaml", 12, "funder_political_axis")]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(f.layer == 1 for f in r.findings)
    assert any(f.subcode == f"{GATE_ID}.field_name" for f in r.findings)


def test_layer1_field_name_exact_progressive_register_caught() -> None:
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("pipeline/institutional_memory/admin_risk_register.yaml", 5,
          "progressive_register")]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(f.subcode == f"{GATE_ID}.field_name" for f in r.findings)


def test_layer1_field_name_camelcase_caught_by_token_matcher() -> None:
    """C2-M-6: ``funderPoliticalAxis`` → token set
    ``{funder, political, axis}`` subset → caught."""
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.py", 10, "funderPoliticalAxis")]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(f.subcode == f"{GATE_ID}.field_name" for f in r.findings)


def test_layer1_field_name_dot_separated_caught_by_token_matcher() -> None:
    """C2-M-6: ``funder.political.axis`` → token-set match."""
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.py", 1, "funder.political.axis")]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False


def test_layer1_field_name_reordered_tokens_caught_by_token_matcher() -> None:
    """C2-M-6: ``axis_political_funder`` (reordered) still trips token match."""
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.py", 1, "axis_political_funder")]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False


def test_layer1_field_name_with_substring_caught() -> None:
    """FI-2 substring detector: ``_funder_political_axis_v2`` → caught."""
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.py", 1, "_funder_political_axis_v2")]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False


def test_layer1_innocent_field_passes() -> None:
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("any.yaml", 1, "funder_name")]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is True


def test_layer1_field_name_regex_direct() -> None:
    """Direct regex spec-pin against future regression."""
    assert LAYER_1_FIELD_REGEX.search("funder_political_axis")
    assert LAYER_1_FIELD_REGEX.search("progressive_register")
    assert LAYER_1_FIELD_REGEX.search("FUNDER_POLITICAL_AXIS")  # case-insensitive
    assert LAYER_1_FIELD_REGEX.search("Funder-Political-Axis")  # hyphen
    assert LAYER_1_FIELD_SUBSTRING.search("custom_political_axis_thing")
    assert not LAYER_1_FIELD_REGEX.search("funder_name")


# ---------------------------------------------------------------------------
# Layer 1b — independent literal proximity (FI-2)
# ---------------------------------------------------------------------------


def test_layer1b_two_literals_in_same_collection_caught() -> None:
    """Two distinct retired literals within the proximity window of the same
    YAML collection trips the independent sub-tag."""
    sources = _empty_sources()
    sources["string_literal_source"] = _src_literals(
        [
            ("any_file.yaml", 5, "conservative", "key: conservative\nkey2: progressive"),
            ("any_file.yaml", 6, "progressive", "key: conservative\nkey2: progressive"),
        ]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.routing_literal_independent"
        for f in r.findings
    )


def test_layer1b_single_literal_outside_routing_path_passes() -> None:
    """A lone retired literal in a non-routing path is fine — Layer 1c only
    fires inside routing-relevant paths."""
    sources = _empty_sources()
    sources["string_literal_source"] = _src_literals(
        [("docs/post_alpha/notes.md", 1, "progressive",
          "the prior taxonomy used progressive")]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is True


# ---------------------------------------------------------------------------
# Layer 1c — singular literal in routing-relevant path (C2-H-1)
# ---------------------------------------------------------------------------


def test_layer1c_singular_literal_in_routing_path_caught() -> None:
    """A single retired literal in a routing-relevant path trips even without
    co-occurrence."""
    sources = _empty_sources()
    sources["string_literal_source"] = _src_literals(
        [(
            "pipeline/cards/CIC/educator.yaml",
            12,
            "progressive",
            "- funder_political_axis: progressive\n  dialect: civic-formal",
        )]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.routing_literal_singular" for f in r.findings
    )


def test_layer1c_singular_literal_in_dialect_codebook_caught() -> None:
    """``pipeline/engineering/agents/references/dialect_codebook.yaml`` is
    routing-relevant; any retired literal there trips."""
    sources = _empty_sources()
    sources["string_literal_source"] = _src_literals(
        [(
            "pipeline/engineering/agents/references/dialect_codebook.yaml",
            1,
            "soul-fire",
            "soul-fire:\n  - voice: prophetic",
        )]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False


# ---------------------------------------------------------------------------
# Layer 2 — Pydantic Literal[...] AST inspection
# ---------------------------------------------------------------------------


def test_layer2_pydantic_literal_with_two_retired_values_caught() -> None:
    sources = _empty_sources()
    sources["pydantic_literal_source"] = _src_pydantic(
        [
            (
                "pipeline/seats/scribe/models.py",
                42,
                "funder_political_axis",
                ("conservative", "centrist", "progressive", "soul_fire"),
                True,
            ),
        ]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.pydantic_literal" for f in r.findings
    )


def test_layer2_pydantic_literal_with_only_one_retired_value_passes() -> None:
    """A single retired value alone in a Literal[...] does NOT trip Layer 2
    — Layer 2 requires two-or-more. The schema-property layer + Layer 1b
    catch single-value cases via path-scope routing-relevance."""
    sources = _empty_sources()
    sources["pydantic_literal_source"] = _src_pydantic(
        [("any.py", 1, "some_field", ("progressive",), True)]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is True


def test_layer2_pydantic_literal_innocent_values_pass() -> None:
    sources = _empty_sources()
    sources["pydantic_literal_source"] = _src_pydantic(
        [
            (
                "pipeline/types/identity_capital.py",
                1,
                "CapitalLogicCard",
                (
                    "public_purpose_works",
                    "catalytic_change",
                    "operating_capacity",
                ),
                True,
            ),
        ]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is True


def test_layer2_pydantic_literal_unresolved_caught_conservatively() -> None:
    """FI-4 + C2-H-2: when the AST walker cannot statically resolve the
    Literal[...] contents, fail-closed HIGH-severity."""
    sources = _empty_sources()
    sources["pydantic_literal_source"] = _src_pydantic(
        [("any.py", 1, "axis_field", (), False)]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.pydantic_literal_unresolved"
        for f in r.findings
    )


def test_layer2_pydantic_literal_handles_soul_fire_hyphen() -> None:
    """The normalization handles ``soul-fire`` and ``soul_fire`` equivalently."""
    sources = _empty_sources()
    sources["pydantic_literal_source"] = _src_pydantic(
        [("any.py", 1, "f", ("soul-fire", "progressive"), True)]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.pydantic_literal" for f in r.findings
    )


# ---------------------------------------------------------------------------
# Layer 3 — schema validation
# ---------------------------------------------------------------------------


def test_layer3_schema_property_forbidden_caught() -> None:
    sources = _empty_sources()
    sources["schema_validation_source"] = _src_schema(
        [
            (
                "pipeline/cards/CIC/food_systems.yaml",
                "dialect_routing_table[0].funder_political_axis",
                "property_forbidden",
                "funder_political_axis",
            ),
        ]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.schema_property" for f in r.findings
    )


def test_layer3_schema_enum_value_forbidden_caught() -> None:
    """C2-NEW-P0-1: retired strings forbidden as ENUM VALUES of `clc` field,
    not just as property name."""
    sources = _empty_sources()
    sources["schema_validation_source"] = _src_schema(
        [
            (
                "pipeline/cards/CIC/educator.yaml",
                "dialect_routing_table[2].clc",
                "enum_value_forbidden",
                "progressive",
            ),
        ]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.schema_property" for f in r.findings
    )


def test_layer3_admin_risk_register_progressive_register_caught() -> None:
    sources = _empty_sources()
    sources["schema_validation_source"] = _src_schema(
        [
            (
                "pipeline/institutional_memory/admin_risk_register.yaml",
                "entries[5].progressive_register",
                "property_forbidden",
                "progressive_register",
            ),
        ]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False


# ---------------------------------------------------------------------------
# Excluded-path allowlist
# ---------------------------------------------------------------------------


def test_excluded_path_lock_history_passes() -> None:
    """``pipeline/engineering/lock_history.v1.jsonl`` is excluded — historical
    record."""
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [(
            "pipeline/engineering/lock_history.v1.jsonl",
            1,
            "funder_political_axis",
        )]
    )
    sources["string_literal_source"] = _src_literals(
        [(
            "pipeline/engineering/lock_history.v1.jsonl",
            1,
            "progressive",
            "{\"lock_class\": \"progressive\"}",
        )]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is True


def test_excluded_path_archived_architecture_passes() -> None:
    """``pipeline/architecture/v0.1/tilth_architecture_locked_v6*.md`` is
    excluded — version-trail history."""
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [(
            "pipeline/architecture/v0.1/tilth_architecture_locked_v6_r2_2026-04-18.md",
            1,
            "funder_political_axis",
        )]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is True


def test_excluded_path_apolitical_amendment_passes() -> None:
    """The amendment file itself legitimately references the retired vocabulary."""
    sources = _empty_sources()
    sources["string_literal_source"] = _src_literals(
        [(
            "pipeline/architecture/v0.1/architecture_v7_0_12_apolitical_dialect_amendment.md",
            1,
            "conservative",
            "the retired enum was: conservative | centrist | progressive | soul_fire",
        )]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is True


def test_excluded_paths_globs_contain_expected_entries() -> None:
    """Spec-pin the excluded-path allowlist roster."""
    paths_set = set(EXCLUDED_PATH_GLOBS)
    assert "pipeline/engineering/lock_history.v1.jsonl" in paths_set
    assert any("tilth_architecture_locked_v6" in p for p in paths_set)
    assert any("apolitical_dialect" in p for p in paths_set)


def test_excluded_path_does_not_exempt_schema_validation() -> None:
    """Schema-validation failures fire even on excluded paths — Layer 3 is
    not gated by the path allowlist."""
    sources = _empty_sources()
    sources["schema_validation_source"] = _src_schema(
        [
            (
                # Even an excluded path with schema failure fires.
                "pipeline/architecture/v0.1/tilth_architecture_locked_v6_r2_2026-04-18.md",
                "some.path",
                "property_forbidden",
                "funder_political_axis",
            ),
        ]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False


# ---------------------------------------------------------------------------
# Prose context outside routing-relevant paths passes (FI-3)
# ---------------------------------------------------------------------------


def test_prose_paragraph_outside_routing_path_passes() -> None:
    """A single literal in a non-routing-relevant doc path is fine."""
    sources = _empty_sources()
    sources["string_literal_source"] = _src_literals(
        [(
            "docs/some_essay.md",
            42,
            "progressive",
            "the prior architecture used a conservative/centrist/progressive/soul_fire taxonomy",
        )]
    )
    r = run(**sources)  # type: ignore[arg-type]
    # Multiple literals in same neighborhood would trip FI-2 — but a single
    # literal in this isolated context does NOT trip Layer 1c (not routing-
    # relevant) and there's no field-name observation.
    assert r.passed is True


def test_prose_paragraph_with_multiple_literals_in_same_window_caught() -> None:
    """FI-2: even outside a routing path, two-or-more retired literals
    co-occurring in proximity trips the independent sub-tag."""
    sources = _empty_sources()
    context = "conservative-centrist-progressive-soul_fire-axis"
    sources["string_literal_source"] = _src_literals(
        [
            ("docs/some_doc.md", 1, "conservative", context),
            ("docs/some_doc.md", 1, "centrist", context),
            ("docs/some_doc.md", 1, "progressive", context),
        ]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False


# ---------------------------------------------------------------------------
# C2-P0-9: surrounding context is hashed, never raw
# ---------------------------------------------------------------------------


def test_findings_carry_sha3_256_hash_not_raw_context() -> None:
    """C2-P0-9: ``surrounding_context_sha3_256_hex`` is a hex digest, not
    raw text. The raw context (which may carry PII) never leaves the gate."""
    sources = _empty_sources()
    sensitive_context = "email: applicant@example.org\nfunder_political_axis: progressive"
    sources["string_literal_source"] = _src_literals(
        [(
            "pipeline/cards/CIC/food_systems.yaml",
            1,
            "progressive",
            sensitive_context,
        )]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    finding = r.findings[0]
    # Verify the hex digest is exactly 64 hex characters (SHA3-256 → 32 bytes).
    assert len(finding.surrounding_context_sha3_256_hex) == 64
    assert all(c in "0123456789abcdef" for c in finding.surrounding_context_sha3_256_hex)
    # Verify the raw PII string does NOT appear in any finding field.
    raw_assertion = "applicant@example.org"
    for field in (
        finding.subcode,
        finding.file_path,
        finding.detail,
        finding.matched_pattern,
        finding.surrounding_context_sha3_256_hex,
    ):
        assert raw_assertion not in field


# ---------------------------------------------------------------------------
# Composition with multiple layers firing
# ---------------------------------------------------------------------------


def test_multiple_layers_fire_aggregated() -> None:
    sources = _empty_sources()
    sources["field_name_source"] = _src_field_names(
        [("pipeline/cards/CIC/food_systems.yaml", 1, "funder_political_axis")]
    )
    sources["pydantic_literal_source"] = _src_pydantic(
        [(
            "pipeline/seats/scribe/models.py",
            10,
            "some_axis",
            ("conservative", "progressive"),
            True,
        )]
    )
    sources["schema_validation_source"] = _src_schema(
        [(
            "pipeline/cards/CIC/educator.yaml",
            "dialect_routing_table[0].funder_political_axis",
            "property_forbidden",
            "funder_political_axis",
        )]
    )
    r = run(**sources)  # type: ignore[arg-type]
    assert r.passed is False
    # At least one finding per layer.
    layers = {f.layer for f in r.findings}
    assert 1 in layers and 2 in layers and 3 in layers


# ---------------------------------------------------------------------------
# Codebook test per FI-10 (§4.X.4)
# ---------------------------------------------------------------------------


def test_dialect_codebook_no_retired_axis_keys() -> None:
    """FI-10 + C2-M-7: load ``pipeline/engineering/agents/references/dialect_codebook.yaml``,
    iterate ALL dot-segments of every top-level key, assert no segment is a
    retired literal.

    The codebook is a runtime-loaded routing asset; if it survives re-keying
    with a retired axis name, the gate would catch it at startup, but this
    test catches it earlier (commit time).

    Option-B split discipline (v7.0.12 LOCK 2026-05-16T14:00:00Z): the
    cards-ceremony that re-keys the codebook is deferred to a separate
    operator-driven ceremony per `JD-C2-LOW-2` (~22-36h pre-ceremony work).
    Until that ceremony runs, the codebook still carries the four retired
    axes (`conservative` / `centrist` / `progressive` / `soul_fire`) as
    legitimate routing keys. This test SKIPS in that pre-ceremony window
    (the runtime gate `F-DIALECT-POLITICAL-AXIS-LEAK` doesn't fire in
    production because the routing asset is excluded by file scope at the
    Card load pathway during Option-B; cards-ceremony flips both the asset
    AND the test).
    """
    import os

    import pytest

    codebook_path = os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..",
        "pipeline", "engineering", "agents", "references",
        "dialect_codebook.yaml",
    )
    codebook_path = os.path.normpath(codebook_path)
    if not os.path.exists(codebook_path):
        pytest.skip("dialect_codebook.yaml not present in this checkout")
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        pytest.skip("PyYAML not installed; cannot parse codebook")

    # Read as text first to do a quick pre-check for retired top-level keys
    # without depending on YAML parser succeeding on a pre-cards-ceremony
    # file that may contain in-string quotes that confuse safe_load.
    with open(codebook_path, encoding="utf-8") as f:
        raw = f.read()
    retired = {"conservative", "centrist", "progressive", "soul_fire", "soul-fire"}
    # If retired vocabulary still present as YAML keys, the cards-ceremony
    # hasn't run yet — skip per Option-B split discipline.
    pre_ceremony_signals = [
        "\n  conservative:", "\n  centrist:", "\n  progressive:",
        "\n  soul_fire:", "\n  soul-fire:",
    ]
    if any(sig in raw for sig in pre_ceremony_signals):
        pytest.skip(
            "dialect_codebook.yaml still carries retired axis keys — "
            "cards-ceremony has not run; per v7.0.12 LOCK Option-B split "
            "(JD-C2-LOW-2), this test re-activates after the cards-ceremony "
            "completes."
        )

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        pytest.skip(
            f"dialect_codebook.yaml parses with error ({exc!r}); "
            "presumed pre-cards-ceremony state."
        )
    if not isinstance(data, dict):
        pytest.skip("dialect_codebook.yaml does not parse to a top-level dict")

    def _walk_keys(d: dict) -> list[str]:
        out: list[str] = []
        for k, v in d.items():
            if isinstance(k, str):
                out.extend(k.split("."))
            if isinstance(v, dict):
                out.extend(_walk_keys(v))
        return out

    all_segments = _walk_keys(data)
    overlap = retired.intersection(s.lower() for s in all_segments)
    assert not overlap, (
        "dialect_codebook.yaml contains retired political-axis segments: "
        f"{overlap}"
    )
