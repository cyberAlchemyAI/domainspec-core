---
node_type: research
is_session: false
status: candidate
created: 2026-08-07
updated: 2026-08-07
promotion_boundary: local research only
---

# Notation Bridge

This notation keeps representation design, tower construction, and experiment results separate.

## Objects

- `c_n`: a bounded claim or concrete case expressed at explanatory layer `L_n`.
- `H_n(c_n) = {h_1, …, h_k}`: horizontal representations of `c_n` at the same layer.
- `I(c_n)`: invariants every `h_i` must preserve: claim label, evidential ceiling, interpretation limits, governance, and authority.
- `P`: a fixed comprehension task.
- `R_n(P, H_n)`: typed residue observed when a participant uses the expression set.
- `mu_n`: the part of the residue that local repair cannot name or close.
- `L_(n+1)`: a richer explanatory layer seeded by `mu_n`.
- `rho_(n+1->n)`: the required return from the richer layer to the lower-level concrete case.

## Horizontal preservation

```text
for every h_i in H_n(c_n): I(h_i) = I(c_n)
```

This is a design obligation until tested. It says what the instrument must preserve, not that readers actually preserve it.

## Vertical promotion

```text
if local_repair(R_n) fails because vocabulary is missing:
    L_(n+1) := extend(L_n, Carrier(mu_n))
```

`Carrier(mu_n)` is formal vocabulary in the Lean construction. Treating an observed human stall as that Carrier is analogy only unless a separate operational bridge is established.

## Round-trip criterion

```text
round_trip(P, c_n) passes only if rho_(n+1->n) preserves I(c_n)
and reconstructs the relevant concrete distinctions.
```

The experiment must define preservation as observable scoring rules. Candidate measures are claim-ceiling retention, authority-boundary accuracy, causal-overclaim detection, transfer accuracy, stall class, and confidence calibration.

## Non-equivalences

- `h_i != L_i`: a horizontal view is not automatically a tower level.
- formal faithful functor `!=` empirically faithful comprehension.
- agent structural pretest `!=` human cognition evidence.
- completed review `!=` repaired implementation or supported claim.

