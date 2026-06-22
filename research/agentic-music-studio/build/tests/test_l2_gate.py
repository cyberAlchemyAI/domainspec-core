from studio_core.l2_effects.gate import Binding, Registry, SensationLabel

GROUNDED = {"spectral_centroid", "dissonance", "harmonicity_match"}


def _label(name, leaves, misuse=""):
    return SensationLabel(name=name, binding=Binding(frozenset(leaves)), misuse=misuse)


def test_reject_no_binding():
    r = Registry()
    res = r.register(_label("vapor", set()), GROUNDED)
    assert res.outcome == "rejected" and "firewall" in res.reason


def test_admit_first_then_distinct():
    r = Registry()
    a = r.register(_label("darkness", {("spectral_centroid", "low")}), GROUNDED)
    assert a.outcome == "admitted" and a.label.status == "grounded"
    b = r.register(_label("dissonant_tension", {("dissonance", "high")}, misuse="not darkness"), GROUNDED)
    assert b.outcome == "admitted"
    assert b.contrastive_boundary  # non-empty set-difference


def test_merge_synonym_empty_setdifference():
    r = Registry()
    r.register(_label("darkness", {("spectral_centroid", "low")}), GROUNDED)
    res = r.register(_label("murk", {("spectral_centroid", "low")}, misuse="x"), GROUNDED)
    assert res.outcome == "merged" and res.nearest == "darkness"


def test_distinct_binding_without_misuse_rejected():
    r = Registry()
    r.register(_label("darkness", {("spectral_centroid", "low")}), GROUNDED)
    res = r.register(_label("tension", {("dissonance", "high")}), GROUNDED)  # no misuse
    assert res.outcome == "rejected" and "misuse" in res.reason


def test_proxy_tag_when_feature_not_grounded():
    r = Registry()
    res = r.register(_label("strangeness", {("violated_expectation", "high")}), GROUNDED)
    assert res.label.status == "proxy"
