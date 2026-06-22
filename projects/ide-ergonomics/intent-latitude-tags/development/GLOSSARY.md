---
module: intent-latitude-tags
featureCode: ILT
version: current
status: draft
updatedAt: 2026-06-18
docType: glossary
---

# Glossary: Intent-Latitude Tags

Glossary linking status per term: `linked` (to a primary source), `partial`, or
`no-match`. Promotion of any term to a canonical registry is **not** automatic.

| Term | Definition | Link status |
| --- | --- | --- |
| **Interpretation latitude** | How much freedom the model has over a span — from "reproduce exactly" to "achieve this outcome however". The axis these tags mark; orthogonal to content-type. | linked → IFID (force vs content), Searle & Vanderveken 1985 |
| **Literal span** (`[literal]`) | A span that must be reproduced/preserved exactly; latitude zero. Enforced by verbatim diff-check. | linked → ../SPEC.md#3 |
| **Goal span** (`[goal]`) | A span describing the outcome to achieve; wording/method free; latitude high. Excluded from verbatim checks, routed to a goal oracle. | linked → ../SPEC.md#3; relates to [target-state](../../../domainspec-v2/research/target-state/SEED.md) |
| **Constraint span** (`[constraint]`) | A boundary that must not be violated; paraphrase allowed, violation not; latitude bounded. | linked → ../SPEC.md#3 |
| **Grounding** | Fixing a tag's meaning by an external mechanism (validator/parser/fine-tune) rather than by the model re-inferring the bracketed word. The whole hypothesis. | linked → ../FINDINGS.md |
| **Verbatim check** | Mechanical contiguous-substring match of a normalized literal span against normalized output. STRONG grounding. | linked → ../SPEC.md#4.1 |
| **Oracle / LLM-judge** | A separate check that decides whether a goal/constraint is satisfied. Drift-prone; FLAG-grade until fixture-validated. WEAK grounding. | linked → ../SPEC.md#4.2 |
| **Unenforced span** | A tagged span with no available oracle. Must be reported as unenforced, never as passed. | linked → ../SPEC.md#4.4 |
| **IFID (Illocutionary Force Indicating Device)** | Searle & Vanderveken (1985): an explicit marker fixing the intended force of a span. The concept this feature is "an inline IFID for prompts" — cite, don't claim novel. | linked → glossary.sil.org / SEP speech-acts |
| **Tautology-kill** | The verdict that an ungrounded tag adds nothing over a prose header of the same word; the kill banked against the naive form. | linked → ../FINDINGS.md |
| **Intent drift** | The model reading a span too literally, or in a totally different role than meant. The problem; named "Intent Misalignment" in arXiv 2509.14404. | linked → ../FINDINGS.md |

## Naming hazards (must disclaim downstream)

- **"Intent Tagging" (Gmeiner et al., CHI 2025)** — same term, `[label:value]` format,
  but content-bearing tags on a 2D canvas. This feature is **not** that; disclaim by
  name when published.
- **Anthropic XML tags / POML** — same bracket *delimiter* shape but the **content-type**
  axis, not latitude. Do not imply equivalence.
