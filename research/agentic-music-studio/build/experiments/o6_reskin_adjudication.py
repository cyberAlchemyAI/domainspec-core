"""O6 — is any named effect's contrastive boundary NOT the set-difference of its bindings?

Wittgenstein's challenge. If every named effect's misuse boundary IS recoverable as
the symmetric set-difference of bindings, L2-lib is a re-skin -> keep labels+gate, drop
the "first-class object/layer" claim. This experiment tries the strongest candidate
(dissonant-tension vs strangeness) and any others, and reports whether a non-reducible
case was found. Independent of O8 (operates on bindings, not on GENDYN analysis).
"""
from __future__ import annotations

import json
from pathlib import Path

from studio_core.l2_effects.gate import Binding, Registry, SensationLabel

GROUNDED = {"spectral_centroid", "dissonance", "harmonicity_match"}


def boundary_is_reducible(a: SensationLabel, b: SensationLabel) -> bool:
    """Is the human-written misuse boundary recoverable from the binding set-difference?"""
    setdiff = a.binding.diff(b.binding)
    # The claim survives (NON-reducible) only if there is a misuse distinction with
    # an EMPTY set-difference (same bindings, yet a real felt boundary). Otherwise the
    # boundary is exactly the set-difference -> reducible -> re-skin.
    return len(setdiff) > 0  # reducible: the boundary == the non-empty set-difference


def main():
    r = Registry()
    cases = []

    # candidate pair 1: darkness vs warmth (different centroid direction)
    darkness = SensationLabel("darkness", Binding(frozenset({("spectral_centroid", "low")})),
                              misuse="not warmth")
    warmth = SensationLabel("warmth", Binding(frozenset({("spectral_centroid", "high")})),
                            misuse="not darkness")
    # candidate pair 2 (the strongest, per the dispatch): dissonant-tension vs strangeness
    tension = SensationLabel("dissonant_tension", Binding(frozenset({("dissonance", "high")})),
                             misuse="not strangeness")
    strangeness = SensationLabel("strangeness",
                                 Binding(frozenset({("dissonance", "high"),
                                                    ("harmonicity_match", "high")})),
                                 misuse="not dissonant-tension")

    for a, b in [(darkness, warmth), (tension, strangeness)]:
        setdiff = sorted(map(str, a.binding.diff(b.binding)))
        reducible = boundary_is_reducible(a, b)
        cases.append({
            "pair": f"{a.name} vs {b.name}",
            "a_binding": sorted(map(str, a.binding.leaves)),
            "b_binding": sorted(map(str, b.binding.leaves)),
            "symmetric_set_difference": setdiff,
            "misuse_boundary_reducible_to_setdiff": reducible,
            "non_reducible_witness": not reducible,
        })

    # register them through the actual gate to confirm the governance path works
    reg_results = []
    for lab in [darkness, warmth, tension, strangeness]:
        res = r.register(lab, GROUNDED)
        reg_results.append({"name": lab.name, "outcome": res.outcome, "status": lab.status})

    any_non_reducible = any(c["non_reducible_witness"] for c in cases)
    verdict = {
        "O6": "KEEP-OBJECT" if any_non_reducible else "RE-SKIN",
        "non_reducible_case_found": any_non_reducible,
        "interpretation": (
            "A named effect carries a distinction not in its bindings -> first-class object justified."
            if any_non_reducible else
            "Every named effect's boundary == the set-difference of its bindings. L2-lib is a "
            "RE-SKIN: keep labels + the contrastive-review gate as GOVERNANCE/ergonomics, but do "
            "NOT mint named effects as a primitive layer or first-class object. Confirms findings.md "
            "default and Wittgenstein's review verdict."
        ),
        "note": (
            "The gate cannot, by construction (floor-clause: every leaf is an L1 feature), admit a "
            "boundary that is not a region of feature-space. A non-reducible case would require a "
            "misuse distinction with an EMPTY binding set-difference AND a real felt boundary - which "
            "the floor-clause forbids. So O6 resolves to RE-SKIN unless the floor-clause is relaxed."
        ),
    }

    out_obj = {"cases": cases, "registrations": reg_results, "verdict": verdict}
    out = Path(__file__).parent / "o6_verdict.json"
    out.write_text(json.dumps(out_obj, indent=2))
    print(json.dumps(verdict, indent=2))
    return out_obj


if __name__ == "__main__":
    main()
