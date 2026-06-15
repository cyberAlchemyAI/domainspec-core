# TOWER.md — Juru Research Tower Map

**Lane:** `juru-legal-llm`
**Paper:** arXiv 2403.18140 (2024)
**Date checked:** 2026-06-10

## Tower shape

```
L0  Corpus           the paper itself (source record + section map)   -> L0-corpus.md
L1  Terms            glossary + governed definitions                  -> glossary.md / definitions.md
L2  Claims           source-labeled claim ledger                      -> claim-ledger.md
L3  Distillate       one-sentence model + compositional spine         -> distill.md
L4  Bridge           carry-to-Jusbrasil verdicts                      -> bridge-decisions.md
L5  Pack             closeout learning pack for the call              -> LEARNING-PACK.md
R   Residue          unverified / open items                          -> open-residue.md
```

## How the layers compose

- **L0 -> L2:** Every claim in the ledger cites a section of the corpus (or marks it open).
- **L1 <-> L2:** Definitions pin the load-bearing terms the claims depend on (continued
  pretraining, catastrophic forgetting, domain adaptation, reputable-source curation, OAB).
- **L2 -> L3:** The distillate is the smallest model that still recomposes the paper's spine:
  *reputable in-domain corpus -> continued pretraining -> measured legal gain + measured general
  forgetting*.
- **L3 -> L4:** Each spine element gets a bridge verdict (borrow-carefully / analogy-only /
  block / promotion-candidate / future-work) against the Jusbrasil foundation-model decision.
- **L4 -> L5:** The pack turns verdicts into the operator's build-vs-buy reading and the 5
  call-ready points.
- **Everything -> R:** Anything not in fetched content is residue, never invented.

## Source-kind label legend (used in claim-ledger.md)

- `primary-source` — stated in the Juru paper (abstract or HTML body).
- `related-source` — from a cited/related work, not Juru's own result.
- `local-inference` — derived by arithmetic/logic from primary-source facts.
- `analogy` — structural mapping to Jusbrasil, not a paper claim.
- `operator-reading` — judgment call for the build-vs-buy decision.
- `open-residue` — referenced but not verifiable from fetched content.

## Promotion rule

LOCAL-ONLY. Promotion candidates stay in this research lane. The `arcanum` submodule is
NEVER touched by this tower.
