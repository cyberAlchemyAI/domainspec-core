# Research Tower — LessWrong *Rationality: A-Z*

A reproducible, source-backed local learning tower that dissects the corpus at
<https://www.lesswrong.com/rationality> — *Rationality: From AI to Zombies* (a.k.a.
"The Sequences"), by Eliezer Yudkowsky.

- **Built:** 2026-06-16
- **Target:** <https://www.lesswrong.com/rationality> (the 6-book corpus / The Sequences)
- **Depth:** `deep` — per-book deep maps for all 6 books + cross-book synthesis
- **Lens:** dual, **clearly separated** — (1) faithful source understanding, then
  (2) a clearly-labeled **Arcanum bridge** layer on top
- **Promotion boundary:** **LOCAL-ONLY.** Nothing here promotes vocabulary or behavior into
  Inventory, Ontology, sigils, spells, runtime contracts, or canonical definitions without a
  separate governed promotion decision. Nothing is written into the public `arcanum` submodule.
- **Method:** built via a governed `dispatch_type: research` subagent dispatch under
  `.claude/skills/domainspec-subagents-strategy` (sheet → check-tension gate → human confirm →
  run → reconcile). See [levels/L2-closure-plan.md](levels/L2-closure-plan.md).

## Fastest path through the tower

1. **[LEARNING-PACK.md](LEARNING-PACK.md)** — the accelerator: source-backed claims, the
   operator model, borrow/analogy-only/block decisions, closed residue, honest cutoff.
2. **[distill.md](distill.md)** — one-sentence model + compositional spine + what to
   borrow / keep analogy-only / block.
3. **[claim-ledger.md](claim-ledger.md)** — what is *actually* a source claim vs a related-source
   claim vs local inference vs analogy vs open residue (source-kind labels).
4. **[residue/open-residue.md](residue/open-residue.md)** — what still needs the full essays
   before external citation.

## Layer spine

See [TOWER.md](TOWER.md). Source-first at the bottom (`levels/L0-corpus.md`), use-ready at the
top (`LEARNING-PACK.md`). Every layer rests on a verified layer below it; the Arcanum bridge
layer is always labeled NON-SOURCE.
