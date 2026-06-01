"""Adversarial + property tests for §7 Scribe R2 drafting primitives.

Covers the union of smart / overlooked_expenses / dialect / program_templates
modules against malformed input, pathological text, and property invariants
(determinism, closed-set membership, idempotence).

Property tests are hand-rolled with seeded ``random.Random`` — hypothesis is
not installed in this venv. Matches the §1 Round J / Scribe R1 precedent.
"""

from __future__ import annotations

import random
from datetime import datetime, timezone

import pytest

from pipeline.seats.scribe.dialect import (
    DIALECT_VOCABULARY,
    detect_dialect_drift,
    detect_dialect_induced_identity,
)
from pipeline.seats.scribe.overlooked_expenses import (
    OverlookedExpenseEntry,
    build_walk,
    is_finalizable,
)
from pipeline.seats.scribe.program_templates import (
    KNOWN_PROGRAMS,
    build_known_template,
)
from pipeline.seats.scribe.smart import (
    check_numeric_verbatim,
    extract_numeric_tokens,
)

_FIXED = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)


def _clock() -> datetime:
    return _FIXED


# ---------------------------------------------------------------------------
# Numeric extraction — property-style
# ---------------------------------------------------------------------------


class TestNumericExtractionProperties:
    @pytest.mark.parametrize("seed", list(range(15)))
    def test_random_integer_roundtrip(self, seed: int) -> None:
        rng = random.Random(seed)
        n = rng.randint(0, 999_999)
        tokens = extract_numeric_tokens(f"value is {n} units")
        assert tokens == (str(n),)

    @pytest.mark.parametrize("seed", list(range(10)))
    def test_money_strips_commas_and_dollar(self, seed: int) -> None:
        rng = random.Random(seed)
        n = rng.randint(1_000, 99_999)
        with_commas = f"${n:,}"
        tokens = extract_numeric_tokens(f"we ask for {with_commas} total")
        assert tokens == (str(n),)

    @pytest.mark.parametrize("seed", list(range(10)))
    def test_percent_canonicalizes(self, seed: int) -> None:
        rng = random.Random(seed)
        pct = rng.randint(1, 99)
        tokens = extract_numeric_tokens(f"{pct}% match required")
        assert tokens == (str(pct),)

    def test_extraction_idempotent_on_canonical(self) -> None:
        text = "We ask $12,000 for 3 years at 75% match."
        once = extract_numeric_tokens(text)
        # Applied to a canonical join of its own tokens, each token should
        # reappear in order.
        canonical_text = " ".join(once)
        twice = extract_numeric_tokens(canonical_text)
        assert twice == once

    def test_giant_document_terminates(self) -> None:
        # Synthesize 5k words of noise with 50 numbers interspersed.
        rng = random.Random(42)
        parts: list[str] = []
        for i in range(5000):
            if i % 100 == 0:
                parts.append(str(rng.randint(10, 99)))
            else:
                parts.append("word")
        text = " ".join(parts)
        tokens = extract_numeric_tokens(text)
        assert len(tokens) == 50
        # All tokens valid integers 10..99.
        for t in tokens:
            assert t.isdigit()
            assert 10 <= int(t) <= 99

    def test_verbatim_empty_when_claim_empty(self) -> None:
        for seed in range(5):
            rng = random.Random(seed)
            evidence = f"the budget is ${rng.randint(100, 9999)}"
            assert check_numeric_verbatim("", evidence) == ()

    def test_verbatim_superset_evidence_always_clears(self) -> None:
        claim_text = "We ask $1,200 over 3 years"
        evidence_text = "1200 3 75 and many more numbers 100 500 1000"
        assert check_numeric_verbatim(claim_text, evidence_text) == ()


# ---------------------------------------------------------------------------
# Dialect — property-style
# ---------------------------------------------------------------------------


class TestDialectDriftProperties:
    @pytest.mark.parametrize("dialect", sorted(DIALECT_VOCABULARY.keys()))
    def test_text_of_only_declared_dialect_has_no_drift(self, dialect: str) -> None:
        text = " and ".join(sorted(DIALECT_VOCABULARY[dialect]))
        drift = detect_dialect_drift(text, dialect)  # type: ignore[arg-type]
        assert drift == ()

    @pytest.mark.parametrize("dialect", sorted(DIALECT_VOCABULARY.keys()))
    def test_other_dialect_phrases_always_drift(self, dialect: str) -> None:
        others = [d for d in DIALECT_VOCABULARY if d != dialect]
        for other in others:
            phrases = list(DIALECT_VOCABULARY[other])
            if not phrases:
                continue
            text = f"We emphasize {phrases[0]} in our program."
            drift = detect_dialect_drift(text, dialect)  # type: ignore[arg-type]
            assert phrases[0] in drift

    def test_drift_respects_case(self) -> None:
        upper = "EQUITY and Food Sovereignty guide our work."
        drift = detect_dialect_drift(upper, "conservative")
        assert "equity" in drift
        assert "food sovereignty" in drift

    def test_drift_empty_input(self) -> None:
        assert detect_dialect_drift(" ", "conservative") == ()


class TestInducedIdentityProperties:
    def test_closed_proxy_phrases_are_subset_of_table(self) -> None:
        # Construct a text containing every proxy phrase for one dialect; with
        # NO claims, the violation set must equal the table's phrase set for
        # that dialect.
        from pipeline.seats.scribe.dialect import DIALECT_IDENTITY_PROXY_TABLE
        for dialect in ("progressive", "soul_fire"):
            phrases = tuple(DIALECT_IDENTITY_PROXY_TABLE[dialect].keys())
            if not phrases:
                continue
            text = ". ".join(phrases)
            violations = detect_dialect_induced_identity(text, dialect, ())  # type: ignore[arg-type]
            assert set(violations) == set(phrases)


# ---------------------------------------------------------------------------
# Overlooked-expenses — property-style
# ---------------------------------------------------------------------------


class TestOverlookedExpensesProperties:
    @pytest.mark.parametrize("seed", list(range(10)))
    def test_needed_count_invariant(self, seed: int) -> None:
        rng = random.Random(seed)
        n = rng.randint(1, 20)
        entries = []
        for i in range(n):
            status = rng.choice(["included", "n_a", "needed"])
            rationale = "filled" if status in ("included", "n_a") else ""
            entries.append(
                OverlookedExpenseEntry(
                    item=f"item-{i}", status=status, rationale=rationale
                )
            )
        walk = build_walk(tuple(entries), rfa_indirect_costs_allowed=None, clock=_clock)
        actual_needed = sum(1 for e in entries if e.status == "needed")
        assert walk.needed_count == actual_needed
        assert is_finalizable(walk) == (actual_needed == 0)

    def test_build_walk_preserves_order(self) -> None:
        entries = [
            OverlookedExpenseEntry(item=f"i{i}", status="needed") for i in range(7)
        ]
        walk = build_walk(entries, rfa_indirect_costs_allowed=True, clock=_clock)
        assert tuple(e.item for e in walk.entries) == tuple(f"i{i}" for i in range(7))


# ---------------------------------------------------------------------------
# Program template — property-style
# ---------------------------------------------------------------------------


class TestProgramTemplateProperties:
    def test_sha_collision_free_across_registry(self) -> None:
        shas = {
            code: build_known_template(code, clock=_clock).template_content_sha3_512
            for code in KNOWN_PROGRAMS
        }
        assert len(set(shas.values())) == len(KNOWN_PROGRAMS)

    def test_every_known_template_section_overrides_frozen(self) -> None:
        import types as _types
        for code in KNOWN_PROGRAMS:
            t = build_known_template(code, clock=_clock)
            assert isinstance(t.section_overrides, _types.MappingProxyType)

    def test_unknown_codes_raise(self) -> None:
        for bogus in ("", "vapg", "  ", "UNKNOWN"):
            with pytest.raises(KeyError):
                build_known_template(bogus)
