# Anime.js Agent Knowledge Vault Research Strategy

Status: `confirmation-readiness candidate`
Dispatch type: `research`
Evidence contract: `exact-binding`
Ontology type: `knowledge-vault` (`inferred`, high confidence)
Authority effect: `none`

## P1 Trigger Decision

Dispatch is required. The work combines at least three independent sources and
lenses: the complete live Anime.js documentation and official repository, the
recent ontology models created in this checkout, and task-centered agent lesson
and consultation semantics. Raw source volume is large, the three lanes can run
independently, and false completeness or copied/advisory material needs
adversarial review before any ontology package is written.

## Intended Result

After accepted research, the parent may build a private candidate package at:

`projects/animejs/ontology/agent-knowledge-vault/`

The package will be source-addressable rather than a verbatim documentation
mirror. It is intended to contain:

- a pinned official-source and documentation-page manifest;
- API, module, parameter, method, concept, example, version, and migration nodes;
- task recipes, prerequisites, pitfalls, diagnoses, fixes, and abstention rules;
- an append-only WorkEpisode to Lesson evidence model for future agent work;
- typed relations with endpoint, direction, evidence, invalidation, and misuse rules;
- agent query contracts and populated human-readable views;
- deterministic schema, graph, relation, coverage, and source-drift validators;
- positive, negative, stale-version, and missing-evidence fixtures;
- digest-bound validation and non-authority receipts.

It will not copy the full documentation prose, replace official docs, become a
generic RAG dump, claim that examples prove behavior, or promote inferred or
community advice into official guidance.

## Groups And Subagents

| Group | Execution | Anti-bias purpose | Agents and outputs |
| --- | --- | --- | --- |
| `explorers` | three lanes in parallel | Official documentation completeness vs recent ontology precedent vs operational agent utility | **Feynman, Richard** — exact official docs/repository coverage manifest. **Mac Lane, Saunders** — complete recent-model manifest and reusable package/validator patterns. **Ahrens, Sönke** — task recipes and evidence-bound WorkEpisode/Lesson contract. |
| `synthesizer` | after all explorers | Reconcile full coverage with a restrained typed model and explicit evidence/version boundaries | **Shannon, Claude** — candidate package tree, node/relation catalogs, queries, views, fixtures, validators, drift/update protocol, and exact-binding matrix. |
| `reviewers` | three lanes in parallel after synthesis, with one bounded zig-zag | Precedent vs non-vacuity vs definitional/evidence non-collapse | **Popper, Karl** — owner and prior-art classification. **Russell, Bertrand** — finite implementation/debugging/migration/lesson witnesses. **Quine, Willard Van Orman** — type, relation, evidence, version, and authority distinctions. |
| `writer` | after exact-binding evidence closure | Persist the research blueprint without writing the ontology | **Simon, Herbert** — `findings.md` only, including complete precedent disposition and candidate package contract. |
| `auditor` | after writer | Independent coverage, evidence, version, copyright, usability, and claim-ceiling audit | **Loregian, Fosco** — ACCEPT or one bounded writer revision. |

## Dependency Flow

```text
explorers (parallel)
  -> synthesizer
  <-> reviewers (parallel; zig-zag cap 1)
  -> exact-binding evidence closure
  -> writer
  -> auditor
  -> parent final approval
  -> parent-owned Ontology Vault candidate build
```

One synthesizer-to-explorers feedback edge may repair missing source bindings.
One auditor-to-writer feedback edge may repair already-supported wording or
structure. The writer cannot repair missing explorer evidence.

## Inventory Preflight

- Machine index: `.arcanum/inventory/index.json`
- Validation: `lookup_readiness=ready`; 281 entries; zero failures; 136
  historical-tag warnings; partial source coverage; Inventory read-model only.
- Selected evidence: learning-graph result; ontology working-prototype gap;
  created Augmentor unified-agent ontology; DomainSpec implementation-conformance
  ontology experiment; Body War business ontology relation coverage; newest
  tower exam learning-graph review.
- Excluded as direct model precedent: Akashic graph-schema research because its
  audit loop ceiling remained unresolved; Way Clear because it is an evaluation
  query rather than a documentation vault; OEW UX review because it is an audit
  protocol; UOC digest strategy because it does not prove the live canvas.
- Gaps: no Anime.js Inventory entry; no current docs snapshot/page manifest;
  no repository-local Anime.js work episodes; partial Inventory coverage of
  untracked recent ontology bytes; no publication or promotion authority.
- Design consequence: the first explorer wave explicitly reconciles Inventory,
  live filesystem/git evidence, and official sources. The new package must be
  isolated, source/version bound, paraphrased, fail-closed, and lesson-evidence
  aware.

The full packet is in `strategy-inventory-packet.json`.

## Gates And Ledger State

- Live dispatch schema: `0.8.0`.
- Candidate sheet: `dispatch-sheet.json`; it intentionally omits
  `evidence_binding` before confirmation.
- Confirmation-readiness validator: `pass`; schema `0.8.0`; ledger mutation
  `none`; sheet SHA-256
  `2f5702d5b2dc030d56d8d16e0e80467d823e79dc250e0402a142b1a2c10d56fd`.
- Dispatch Spec validation: `pass`, with no flags.
- Check-tension: `PASS/PASS`; both independent agents recomputed and judged
  the admitted sheet digest with no apontamentos.
- Human confirmation: required only after both deterministic validators and
  tension `PASS/PASS`.
- Registration: not started; the append-only dispatch ledger must not change
  before confirmation.
- Closeout: if confirmed and run, exactly one dispatch row and one close row;
  every agent joined and closed; result Inventory and observability updated.

## Boundaries

- Existing ontology packages and all unrelated dirty-worktree bytes are read-only.
- Research writes only `research.md`, `findings.md`, and bounded receipts in the
  working folder after confirmation.
- The parent may write the isolated Anime.js ontology package only after an
  accepted audit and only within the confirmed package boundary.
- Official-source coverage uses URLs, selectors, hashes, structured facts, and
  concise paraphrases; it does not reproduce the site wholesale.
- GitHub issues and examples remain classified evidence; they are not silently
  upgraded to official documentation or runtime proof.
- `authority_effect: none`; `release_admission: not-granted`; no publication,
  release, deployment, or production-readiness claim.

## Next Human Action

Reply exactly `confirmed` to authorize registration and execution of the frozen
sheet digest above, followed by the bounded parent-owned ontology build only if
the final research auditor accepts `findings.md`. Any other reply is discussion,
revision, or decline and is not confirmation.
