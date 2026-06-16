# L0 — Source Record (corpus)

The faithful record of **what exists, where, and what was fetched**. Everything above this
layer must trace back to an entry here. `primary-source` only; accessibility gaps are marked.

## Source record

| Field | Value |
|---|---|
| Title | *Rationality: From AI to Zombies* ("Rationality: A-Z" / "The Sequences") |
| Author | Eliezer Yudkowsky |
| Canonical URL | <https://www.lesswrong.com/rationality> |
| Original publication | blog posts on Overcoming Bias / LessWrong, 2006–2009; compiled as the ebook 2015 |
| Version checked | Web (lesswrong.com) landing + book/sequence pages |
| Date checked | 2026-06-16 |
| Access | Public, free to read on lesswrong.com; ebook also distributed by MIRI |
| Source boundary | The 6-book corpus linked from `/rationality`. Related works (HPMOR, Inadequate Equilibria, CFAR material, Kahneman/Tversky source literature) are **`related-source`**, not in-corpus. |

## Corpus map — the 6 books (`primary-source`: titles per the landing page, 2026-06-16)

| # | Book | Stated focus (to be verified/expanded per-book) |
|---|---|---|
| 1 | **Map and Territory** | how beliefs function; what makes a belief effective; belief↔reality correspondence |
| 2 | **How to Actually Change Your Mind** | motivated reasoning, confirmation bias, the discipline of updating |
| 3 | **The Machine in the Ghost** | evolutionary biology, optimization, cognitive architecture, goal-directed systems |
| 4 | **Mere Reality** | physics, mind, reductionism, scientific understanding of the world |
| 5 | **Mere Goodness** | value theory, moral reasoning, terminal vs instrumental values |
| 6 | **Becoming Stronger** | applied/practical rationality and community development |

Additional named sequences cited on the landing page (subsets within the books): *Predictably
Wrong, Fake Beliefs, Noticing Confusion, Politics and Rationality, Against Rationalization,
Death Spirals*, and others.

## Named concepts surfaced at L0 (`primary-source` pointers; meaning deferred to claim-ledger)

semantic stopsigns · mysterious answers to mysterious questions · affective death spirals ·
terminal vs instrumental values · the map/territory distinction · "beliefs should pay rent (in
anticipated experience)" · Bayesian updating.

> These are **pointers**, not yet defined claims. Each must be opened and labeled in
> [../claim-ledger.md](../claim-ledger.md) before it carries reasoning load upstream.

## Accessibility note (2026-06-16)

- The landing page enumerates the 6 books and sequence names; **individual essay text was not
  yet deep-fetched at scaffold time** — that is the job of the book-reader dispatch lane.
- WebFetch returns lesswrong pages as markdown; long essays may be truncated → keystone essays
  must be fetched individually and any truncation flagged as `open-residue`.

## What the dispatch must fetch (deep lane assignments)

Each book-reader lane (one per book) must fetch the book's landing/contents page **plus 2–4
keystone essays**, and record for its book: core thesis, the sequences inside it, named
vocabulary, and the load-bearing claims — every line labeled with a source kind. Truncation,
paywalls, or unread keystone essays are logged to [../residue/open-residue.md](../residue/open-residue.md).
