import numpy as np
import pytest

from intent_engine.codegen.author import author
from intent_engine.codegen.compile import compile_program, render_untuned
from intent_engine.codegen.dsl import parse, unparse
from intent_engine.intent.parse import parse_intent
from intent_engine.program import RenderCtx
from intent_engine.steer.edit import apply_edit
from intent_engine.steer.revise import UnknownCritique, revise
from intent_engine.steer.session import readout, show
from intent_engine.tune.fit import fit, feats_of
from studio_core.l2_effects.objective import THETA_BOUNDS


# --- SWU-1: DSL ---
def test_dsl_roundtrip():
    src = "voice gendyn dark violin strange\nseed 0x5eed"
    p = parse(src)
    assert p.engine == "gendyn" and p.effects == ["dark", "violin", "strange"] and p.seed == 0x5EED
    assert parse(unparse(p)).effects == p.effects


def test_dsl_rejects_pattern_and_scale():
    for bad in ("pattern \"x ~ x\"", "scale strange"):
        with pytest.raises(ValueError):
            parse(f"voice gendyn dark\n{bad}")


def test_dsl_unknown_effect_in_compile():
    with pytest.raises(ValueError):
        compile_program(parse("voice gendyn wobbly\nseed 1"))


# --- SWU-2: compile + render ---
def test_render_untuned_bit_identical():
    p = parse("voice gendyn dark\nseed 7")
    assert np.array_equal(render_untuned(p), render_untuned(p))


# --- SWU-4: resolver ---
def test_parse_intent_four_targets():
    spec, unknown = parse_intent("dark violin stochastic synth, bring strangeness")
    feats = {t.feature for t in spec.targets}
    assert spec.engine == "gendyn"
    assert feats == {"spectral_centroid", "harmonicity_match", "dissonance_minor2"}
    # every target carries a concrete value (G9)
    assert all(isinstance(t.value, float) for t in spec.targets)
    # strangeness is tagged proxy (F2)
    assert any(t.feature == "dissonance_minor2" and t.status == "proxy" for t in spec.targets)
    assert unknown == []


def test_parse_intent_flags_unknown_not_guess():
    spec, unknown = parse_intent("dark velvety synth")
    assert "velvety" in unknown  # unknown adjective surfaced, not silently mapped


# --- SWU-5: author (transliteration; no invented fields, I3/G5) ---
def test_author_no_invented_fields():
    spec, _ = parse_intent("dark violin stochastic synth, bring strangeness")
    src, prog = author(spec)
    # every Program field originates in the IntentSpec
    assert prog.engine == spec.engine
    assert prog.effects == spec.effects
    assert prog.seed == spec.seed
    # re-parses to an equivalent program
    assert parse(src).effects == prog.effects


# --- SWU-3: fit (the engineering) ---
def test_feats_reproducible_frozen_ctx():
    ctx = RenderCtx()
    theta = np.array([12.0, 20.0, 0.1])
    assert feats_of(theta, 5, ctx) == feats_of(theta, 5, ctx)


def test_fit_dark_lowers_centroid_vs_baseline():
    spec, _ = parse_intent("dark stochastic synth")  # single low(centroid) target
    rng = np.random.default_rng(0)
    base = np.nanmean([
        feats_of(np.array([rng.uniform(lo, hi) for lo, hi in THETA_BOUNDS]), spec.seed, spec.ctx)["spectral_centroid"]
        for _ in range(10)
    ])
    rs = fit(spec)
    assert rs.feats["spectral_centroid"] <= base


# --- SWU-6: steer session ---
def test_session_shows_meter_and_code_honestly():
    spec, _ = parse_intent("dark stochastic synth")
    rs = fit(spec)
    _src, prog = author(spec)
    text = show(rs, prog)
    assert "voice gendyn" in text                 # the code is shown
    rep = readout(rs)
    assert "O1" in rep["spectral_centroid_note"]   # darkness labelled analyzer-independent, felt=O1 (F2)
    assert "proxy" in rep["dissonance_note"]        # strangeness labelled proxy


# --- SWU-7: revise (closed critique) ---
def test_revise_more_bite_raises_strangeness_weight():
    spec, _ = parse_intent("dark stochastic synth, bring strangeness")
    before = next(t.weight for t in spec.targets if t.feature == "dissonance_minor2")
    spec2 = revise(spec, "more bite")
    after = next(t.weight for t in spec2.targets if t.feature == "dissonance_minor2")
    assert after > before


def test_revise_unknown_asks_not_guesses():
    spec, _ = parse_intent("dark stochastic synth")
    with pytest.raises(UnknownCritique):
        revise(spec, "make it cosmic")


def test_revise_more_bite_changes_rendered_dissonance():
    """SWU-7 (Option 1 fix): 'more bite' raises the strangeness weight, sliding the trade-off so the
    re-tuned render is measurably rougher. (The deeper steering question is the open research direction.)"""
    spec, _ = parse_intent("dark stochastic synth, bring strangeness")
    rs1 = fit(spec)
    rs2 = fit(revise(spec, "more bite"))
    assert rs2.feats["dissonance_minor2"] > rs1.feats["dissonance_minor2"]


# --- SWU-7b: human hand-edit ---
def test_hand_edit_reparses_and_renders():
    prog, ispec, sig = apply_edit("voice gendyn dark violin\nseed 0x1234")
    assert prog.seed == 0x1234 and prog.effects == ["dark", "violin"]
    assert sig.shape[0] > 0
    # editing the seed changes the sound
    _p2, _i2, sig2 = apply_edit("voice gendyn dark violin\nseed 0x9999")
    assert not np.array_equal(sig, sig2)
