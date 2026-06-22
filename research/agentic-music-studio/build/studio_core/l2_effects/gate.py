"""L2 — the contrastive-review gate for named effects (the O6 mechanism).

A named effect is NOT a primitive layer (Wittgenstein). It is a saved L2
expression + a label + a contrastive boundary + a governance lifecycle. register()
enforces: a binding must exist; the contrastive boundary against the nearest
neighbour is computed as the *set-difference of bindings*; the entry is tagged
grounded vs proxy(O1). The O6 question is whether any named effect's boundary is
NOT recoverable as that set-difference.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Binding:
    """The downward resolution of a label: a set of (feature, direction) leaves."""

    leaves: frozenset  # e.g. frozenset({("dissonance","high"), ("inharmonicity","high")})

    def diff(self, other: "Binding") -> frozenset:
        return self.leaves.symmetric_difference(other.leaves)


@dataclass
class SensationLabel:
    name: str
    binding: Binding
    examples: list = field(default_factory=list)
    misuse: str = ""
    status: str = "seed"  # 'grounded' | 'proxy' | 'seed' | 'contested'
    provenance: str = ""


@dataclass
class RegisterResult:
    outcome: str  # 'admitted' | 'merged' | 'rejected'
    label: SensationLabel | None
    reason: str
    contrastive_boundary: frozenset | None = None
    nearest: str | None = None


class Registry:
    def __init__(self):
        self.labels: dict[str, SensationLabel] = {}

    def _nearest(self, cand: SensationLabel):
        best, best_overlap = None, -1
        for ex in self.labels.values():
            overlap = len(cand.binding.leaves & ex.binding.leaves)
            if overlap > best_overlap:
                best, best_overlap = ex, overlap
        return best

    def register(self, cand: SensationLabel, grounded_features: set[str]) -> RegisterResult:
        # 1. firewall: a name with no binding is rejected on sight.
        if not cand.binding.leaves:
            return RegisterResult("rejected", None, "no binding (firewall)")
        # 2. grounded vs proxy (O1): grounded iff every leaf feature is source-backed.
        feats = {feat for feat, _dir in cand.binding.leaves}
        cand.status = "grounded" if feats <= grounded_features else "proxy"
        # 3. contrastive review vs nearest neighbour.
        nb = self._nearest(cand)
        if nb is not None:
            boundary = cand.binding.diff(nb.binding)
            if not boundary:
                # indistinguishable by binding -> synonym -> merge, do not admit.
                return RegisterResult("merged", nb, f"synonym of '{nb.name}' (empty set-difference)",
                                      contrastive_boundary=boundary, nearest=nb.name)
            if not cand.misuse:
                return RegisterResult("rejected", None, "distinct binding but no misuse note written",
                                      contrastive_boundary=boundary, nearest=nb.name)
            self.labels[cand.name] = cand
            return RegisterResult("admitted", cand, "admitted (distinct binding + misuse note)",
                                  contrastive_boundary=boundary, nearest=nb.name)
        self.labels[cand.name] = cand
        return RegisterResult("admitted", cand, "admitted (first entry)", contrastive_boundary=None)
