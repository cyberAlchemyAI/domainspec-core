# Claim Ledger

Every load-bearing claim about the corpus, separated by source kind. **No claim flows upstream
without a label here.** (Taxonomy: see [TOWER.md](TOWER.md).) Built from the dispatch lens
returns + synthesizer, with reviewer S1's faithfulness corrections applied.

> **Fetch caveat:** ~60% of direct essay URLs 404'd; title-level concepts are `[open-residue]`
> in [residue/open-residue.md](residue/open-residue.md), not asserted here.

## Direct source claims (`primary-source`)

| id | claim | book | rests on | collapse-test (the fact that would zero it) |
|---|---|---|---|---|
| P1 | Evidence = an event causally **entangled** with the target of inquiry; rational belief must be so entangled, else it is blind faith | B1 | lens-E2 | show a belief tracking reality with no causal channel to it |
| P2 | Beliefs should **pay rent in anticipated experiences**; a belief yielding identical predictions whether true or false carries zero information | B1 | lens-E1 | exhibit a belief the author calls genuine that constrains no anticipation |
| P3 | **The bottom line**: the algorithm that produced the conclusion — not the post-hoc arguments — is what counts | B2 | lens-E1 | show the author crediting arguments written after the conclusion |
| P4 | **Conservation of Expected Evidence**: each anticipated support must be balanced by equal-and-opposite anticipated counter-evidence | B2 | lens-E1 | a test the author endorses that expects net confidence gain pre-evidence |
| P5 | Organisms are **adaptation-executors, not fitness-maximizers** (phrase per Tooby & Cosmides; *corroborated by external literature, `[related-source]`*) | B3 | lens-E1, lens-E2 | show the corpus claiming organisms compute current fitness |
| P6 | **No Universally Compelling Arguments**; "morality" names a specific human computation with relative truth-values *(via mirror/summary, not a canonical fetched body — S1)* | B5 | lens-E2 | a canonical body contradicting the relative-computation framing |
| P7 | The **Twelve Virtues of Rationality** describe rationalist character; **taboo your words** to dissolve definition disputes | B6 | lens-E1 | — |
| P8 | The corpus **asserts** Many-Worlds "wins outright"; collapse is "phlogiston-like" (this is the corpus's claim, not an endorsed fact) | B4 | lens-E2 | — (see R7 for the external check) |

> *S1 minor fix applied:* E2's judgment that P1 is "the strongest, hardest-to-attack part of the
> corpus" is **`[local-inference, per lens-E2]`**, not part of the primary-source line.

## Related-source claims (`related-source`) — external literature (per lens-E2 / E3)

| id | claim | external source |
|---|---|---|
| R1 | "Pay rent" ≈ positivist verification principle, largely abandoned as self-refuting | Ayer/Carnap; Quine |
| R2 | Solomonoff prior is **uncomputable** and UTM-dependent (constant factor unbounded) | Li & Vitányi; Sterkenburg |
| R3 | Core K&T biases replicate; adjacent priming/ego-depletion did **not** (replication crisis) | Tversky & Kahneman 1974; Hagger et al. ego-depletion RRR |
| R4 | Ecological-rationality program contests "biases-as-defects" | Gigerenzer ("Homo Heuristicus") |
| R5 | Bayesian conditionalization has warrant but is **not** the unique standard | Mayo (error statistics); de Finetti; Joyce |
| R6 | Foresightless evolution / adaptation-executors strongly backed | Williams; Tooby & Cosmides; Dawkins |
| R7 | Physicists are **not** near MWI consensus (2025 survey: MWI ~15%, Copenhagen 36%) | physicist interpretation survey 2025 |
| R8 | Hard problem of consciousness is not "dissolved" by calling it confused | Chalmers; Jackson ("Mary") |
| R9 | Evolutionary debunking is unengaged and cuts against CEV authority | Street |
| R10 | Debiasing transfers poorly across domain/time | Lilienfeld; Kahneman & Klein |
| R11 | Map/territory **originates with Korzybski (1931)**, not Yudkowsky | Korzybski, *Science and Sanity* |

## Local inference (`local-inference`)

| id | inference | rests on |
|---|---|---|
| L1 | The 6 books form one progressive map-quality argument | lens-E1 |
| L2 | **B1 ↔ B4 internal contradiction**: rent-criterion vs. choosing empirically-equivalent MWI on simplicity | lens-E2 |
| L3 | "Optimization process" is **analogy, not theorem** (reductive overreach across evolution/markets/minds) | lens-E2 |
| L4 | "Morality as fixed computation with truth-values" borrows realist confidence on anti-realist metaphysics | lens-E2 |
| L5 | Claimed trainability of rationality outruns the transfer evidence | lens-E2 |

## Open residue (`open-residue`) — see [residue/open-residue.md](residue/open-residue.md)

| id | unverified | rests on |
|---|---|---|
| O1 | Map/Territory title essay; An Alien God; Godshatter; Value is Fragile nuances; Something to Protect; Terminal/Instrumental **origin essay**; Mind Projection Fallacy body; 37 Ways That Words Can Be Wrong body; sanity-waterline body; "mental paintbrush handles" phrasing | lens-E1, lens-E3 (URLs 404'd) |

## Bridge layer (NON-SOURCE) — pointer only

Arcanum readings are **not** corpus claims and live in [bridge-decisions.md](bridge-decisions.md)
(`analogy` / `operator-reading`). S1 confirmed none leaked into the source layer above.
