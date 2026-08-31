# Pareto front — Recovery 006

## Method and ceiling

All twelve candidates passed the four hard-elimination checks. For the twelve dimensions in `scores.json`, candidate A dominates candidate B only when every A score is at least B's score and at least one is strictly higher. No weighted total, average, rank sum, or tie-break scalar was calculated.

A non-dominated position means only that no eligible authored candidate is scored at least as strong on all twelve dimensions. It does not mean best, approved, proven comprehensible, implementation-ready, or selected.

## Non-dominated set

Listed in contract order, not rank order:

| Candidate | Vector in contract dimension order | Preserved advantage | Material trade-off |
| --- | --- | --- | --- |
| `F01-product-consequence` | `[4,5,5,5,5,5,5,4,5,5,4,5]` | Direct software relevance, strongest recurring continuity, neutral choices, and no metaphor drift. | More recurring-context load and implementation coordination than lean casebook or minimal copy. |
| `F02-product-analogy` | `[5,5,5,5,5,4,5,3,5,5,3,4]` | Recurring product stakes plus precise physical memory hooks. | Three representations increase cognitive and implementation cost; analogy salience can cue later answers. |
| `F07-casebook-consequence` | `[4,5,5,5,5,5,3,5,5,5,5,5]` | Lowest burden and cost among fully developed architectures, exact local case fit, and strong guide extensibility. | Weakest continuity within the front; the repeated causal question may not replace a story spine. |
| `F08-casebook-analogy` | `[5,5,5,5,5,4,3,4,5,5,4,5]` | Strong local resonance and analogy fit with moderate load and broad lesson-by-lesson flexibility. | Domain and analogy both change between lessons, creating reorientation and editorial-drift pressure. |
| `C02-minimal-concrete` | `[3,4,4,4,4,5,4,5,5,5,5,4]` | Safest cue profile, lowest burden, lowest cost, and concrete improvement without a story system. | Lower resonance, concreteness, and trajectory; may address abstraction without satisfying the requested storytelling need. |

Dimension order is `resonance`, `beginner_relevance`, `reader_trajectory`, `concreteness`, `analogy_accuracy`, `cue_safety`, `cross_lesson_continuity`, `cognitive_load`, `binding_fidelity`, `claim_boundary`, `implementation_cost`, `guide_extensibility`.

## Pairwise trade-off witnesses inside the front

- `F01` versus `F07`: `F01` preserves recurring continuity (`5` versus `3`); `F07` preserves lower burden and cost (`5` versus `4` on both).
- `F01` versus `F02`: `F02` improves resonance (`5` versus `4`); `F01` improves cue safety, cognitive load, cost, and extensibility.
- `F02` versus `F08`: `F02` preserves recurring continuity (`5` versus `3`); `F08` improves load, cost, and extensibility (`4/4/5` versus `3/3/4`).
- `F07` versus `F08`: `F08` improves resonance (`5` versus `4`); `F07` improves cue safety, cognitive load, and implementation cost (`5` versus `4`).
- `C02` versus developed architectures: the control preserves cue safety, low burden, and low cost, while every developed front candidate supplies stronger resonance, relevance, trajectory, or concreteness. Its higher continuity than the casebook entries comes from a repeated minimal structure, not narrative evidence.

## Dominated set and domination witnesses

| Candidate | Dominated by | Strictly weaker examples |
| --- | --- | --- |
| `F03-product-dialogue` | `F02-product-analogy` | Lower analogy accuracy and cue safety with no compensating dimension. |
| `F04-community-consequence` | `F01-product-consequence` | Lower trajectory, analogy carriage, continuity, and extensibility with no compensating dimension. |
| `F05-community-analogy` | `F02-product-analogy` | Lower trajectory, continuity, and extensibility with no compensating dimension. |
| `F06-community-dialogue` | `F02-product-analogy`, `F03-product-dialogue`, `F05-community-analogy` | Dialogue adds cue/load cost without gaining a dimension over the corresponding alternatives. |
| `F09-casebook-dialogue` | `F08-casebook-analogy` | Lower analogy accuracy, cue safety, and extensibility with no compensating dimension. |
| `C01-current-abstract` | `C02-minimal-concrete`, `F07-casebook-consequence` | Minimum concrete nouns improve relevance, trajectory, concreteness, analogy carriage, continuity, and extensibility without extra load or cost. |
| `C03-overstory-stressor` | every factorial candidate | Excess retains specificity and bindings but loses cue safety, continuity, load, cost, and extensibility. |

Dominated does not mean invalid. These candidates remain useful controls and evidence about failure modes; they simply do not preserve a unique authored trade-off under the current score vectors.

## Stable disagreements for the jury

1. Is recurring product continuity worth greater lore and implementation cost than casebook autonomy?
2. Does one mapped analogy improve intended-reader retention enough to justify representation and review cost?
3. Can the repeated question **What changed, and what still has not?** supply guide continuity without recurring characters?
4. Is `C02` the smallest sufficient correction, or does it underdeliver the operator's explicit request for storytelling and analogy?
5. Are the author cue-safety penalties for analogy and dialogue severe enough, or too severe, before browser and reader evidence exists?

## Jury use

The parent must independently inspect all three route samples for every front member, recheck the score witnesses and dominance calculation, and record disagreements in `jury-review.md`. Combining attractive properties from several candidates would create an untested thirteenth candidate; the parent may recommend such a reconciliation only as a revision direction, not treat it as part of this frozen field.

The human gate remains pending. This front may teach comparative inference; it does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, transport proof, or selection.
