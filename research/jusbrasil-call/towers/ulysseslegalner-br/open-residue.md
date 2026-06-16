# Open Residue — Fabrication Guard

Items NOT verified from an accessible source as of 2026-06-10. These are honest gaps. **Do not fabricate.** Most close by fetching the PDF body: https://aclanthology.org/2026.propor-1.33.pdf

| ID | Open item | Why open | How to close |
|---|---|---|---|
| O1 | Names of the 9 categories and 23 fine-grained types | Only counts are on the landing page; names live in the PDF body | Fetch PDF; extract schema table |
| O2 | Per-label F1 table (which 6 cat / 7 types > 95%; which sit 71–82%) | Aggregate stated, breakdown not | Fetch PDF results section |
| O3 | Document split across bills / case law / laws; train/dev/test sizes | Only total 560 stated | Fetch PDF corpus section |
| O4 | "Hybrid approach" composition (manual + auto? IAA scores?) | Named, not defined | Fetch PDF annotation section |
| O5 | "Unified corpus" exact semantics (full merge vs. cross-domain eval) | Term used in abstract only | Fetch PDF experiments section |
| O6 | Computational-cost numbers (train/inference time, parameters) | "computational cost" named, no figures | Fetch PDF cost section |
| O7 | License + public download URL for UlyssesLegalNER-Br corpus/models | README has no license/links; landing page has none | Fetch PDF; check GitHub releases / data statement |
| O8 | Tagging scheme (BIO/BILOU) and tokenization | Not on accessible sources | Fetch PDF method section |
| O9 | Whether UlyssesLegalNER-Br data is published in the `ulysses-camara/ulysses-ner-br` repo or elsewhere | README describes only predecessor corpora | Re-check repo branches/releases; PDF data-availability statement |
| O10 | Comparison numbers vs. LeNER-Br / CDJUR-BR on shared types | Not on landing page | Fetch PDF related-work / comparison |

**Residue count: 10.**

## Build-blocker note

The build itself was NOT blocked: S1 (landing) and S2 (README) were accessible and yielded all headline claims verbatim. The single methodological limitation is that the **PDF body was not ingested** in this standard-depth pass, which is the sole source of O1–O10. The WSL Bash filesystem was not writable from the sandbox; all files were written via the Write tool over the Windows UNC path — no impact on content integrity.
