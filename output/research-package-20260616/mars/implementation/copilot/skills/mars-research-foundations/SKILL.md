---
name: mars-research-foundations
description: "Build the project-level research foundations baseline before protocol design by producing domain context, methodology/theory synthesis, source catalog updates, reference-ledger updates, and library-grade inventory coverage."
argument-hint: "<project-key> [--refresh-sources] [--refresh-library] [--context-label <label>]"
agent: mars-research-scientist
allowed-tools: Read, Write, Bash, Glob, Grep, Fetch, AskQuestions
---

<objective>
Create the project-level research foundations that must exist before experiment protocol design or execution begins.

This skill produces two project-scoped baseline artifacts:

- `foundations/DOMAIN-CONTEXT.md`
- `foundations/METHODOLOGY-AND-THEORY.md`

and ensures they are backed by:

- `sources/SOURCE-CATALOG.md`
- `sources/REFERENCE-LEDGER.md`
- `inventory/INVENTORY-INDEX.md` plus library-grade inventory entries

This skill exists because experiment-scoped methodology and context bundles are too late to establish the basic research posture of a project.
</objective>

<context>
Project baseline inputs:
- `PROJECT-OVERVIEW.md`
- `claims/CLAIMS.md`
- `claims/HYPOTHESES.md`
- `definitions/DEFINITIONS.md`
- `definitions/DEFINITIONS-INDEX.md`
- `experiments/EXPERIMENT-CANDIDATES.md`
- `experiments/EXPERIMENTS.md`

Project knowledge-stack artifacts:

- `sources/SOURCE-CATALOG.md`
- `sources/REFERENCE-LEDGER.md`
- `inventory/INVENTORY-INDEX.md`
- `inventory/*.md`

Template sources:

- `implementation/mars/templates/domain-context-template.md`
- `implementation/mars/templates/methodology-theory-baseline-template.md`

This skill should use source discovery and inventory extraction patterns when authorities are missing or under-extracted.
</context>

<process>
1. Read current project scope and experiment intent.
   - Resolve the research setting, decision surface, and experiment family.
   - Identify which authorities belong in the `domain context` versus the `methodology and theory` baseline.

2. Build or refresh the authority base.
   - Ensure required authorities are present in `sources/SOURCE-CATALOG.md`.
   - Ensure protocol-level authorities are promoted into `sources/REFERENCE-LEDGER.md` with clear usage scopes.
   - If missing, use source-discovery workflow before continuing.

3. Build or refresh the reference library.
   - Ensure `inventory/INVENTORY-INDEX.md` covers the active authorities.
   - Expand inventory artifacts so they are library-grade: enough extracted content to support later protocol design without re-discovery.
   - Library-grade means preserving reusable constructs, cautions, experiment relevance, and adaptation notes, not only short snippets.

4. Write `foundations/DOMAIN-CONTEXT.md`.
   - Explain the project setting, regimes, prior-art context, and failure modes.
   - Make the external-validity frame explicit.

5. Write `foundations/METHODOLOGY-AND-THEORY.md`.
   - Explain the methodology posture, theory baseline, authority map, and implications for experiment design.
   - Record any unresolved authority split or scope ambiguity explicitly.

6. Enforce the foundations gate.
   - Protocol design should remain blocked if either foundations artifact is missing.
   - Protocol design should remain blocked if primary authorities are not source-cataloged, ledgered, and library-inventoried.

7. Return a compact foundations summary and the next recommended command.
   </process>

<quality-bar>
- The two foundations artifacts should be consultable by a later protocol author without needing to re-read the source discovery conversation.
- Inventory should behave like a reusable reference library, not a citation cache.
- Domain-context and methodology/theory synthesis must be separate; do not collapse them into one unfocused document.
- Authority ambiguities must be explicit.
</quality-bar>

<output-contract>
Return:

```markdown
## Research Foundations Summary

- Project: <project-key>
- Domain context: ready | needs-work
- Methodology/theory baseline: ready | needs-work
- Source catalog status: ready | needs-work
- Reference library status: ready | needs-work
- Protocol-design readiness: PASS | BLOCK

### Artifacts

- <path>
- <path>

### Next Command

1. <exact command>
```

</output-contract>

<authority-rule>
- This skill establishes project-level research baselines.
- It does not replace experiment-scoped `methodology.md`, `protocol.md`, or `context.md`.
- When the foundations baseline is incomplete, protocol design should not proceed.
</authority-rule>
