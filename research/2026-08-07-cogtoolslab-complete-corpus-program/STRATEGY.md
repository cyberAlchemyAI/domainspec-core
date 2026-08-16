# CogTools Lab Complete-Corpus Research Strategy

Status: `closed: error; partial explorer evidence preserved`
Dispatch type: `research`
Evidence contract: `exact-binding`
Authority effect: `none`

## P1 Trigger Decision

Dispatch is required. The target contains 90 directly linked papers, one-hop teaching surfaces whose reading count is not yet known, and a separate research-framing surface. Corpus partitions can run independently, raw paper extraction would overwhelm the parent context, and completeness plus interpretation need independent checks.

## Research Program

The program freezes three source tiers:

1. **Tier A:** all 90 PDFs directly listed by `papers.html` in the run snapshot.
2. **Tier B:** papers explicitly named in the five one-hop public teaching or syllabus surfaces, deduplicated against Tier A.
3. **Tier C:** the lab's research framing, which contains no additional paper links.

It does not recursively crawl every bibliography or cited-by graph. It stores stable citations, access receipts, byte digests, selectors, short paraphrased evidence capsules, and open residue. It does not commit or republish PDF bytes.

## Groups And Subagents

| Group | Execution | Anti-bias purpose | Subagents and outputs |
|---|---|---|---|
| `explorers` | four parallel lanes | Temporal and source-corpus disagreement | **Halford, Graeme** — all 36 papers from 2024–2026. **Saxe, Andrew** — all 29 papers from 2021–2023, with benchmark-shift reconstruction and developmental-method transitions. **Bateson, Gregory** — all 25 papers from 2009–2020. **Simon, Herbert** — seven courses, five one-hop teaching surfaces, deduplicated readings, and research framing. |
| `synthesizer` | after all explorers | Reconcile rows without turning a corpus into one theory | **Beer, Stafford** — 90-row closure, Tier-B deduplication, temporal/thematic map, contradictions, and cognitive-tools crosswalk. |
| `reviewers` | three parallel attacks after synthesis | Precedent, non-vacuity, and definitional/scope separation | **Hacking, Ian** — source and theoretical ownership. **Popper, Karl** — counts, hashes, rereads, deduplication, and failure mutants. **Quine, Willard Van Orman** — paper/corpus/cognition/formal-analogy boundaries. |
| `writer` | after exact-binding evidence closure | Persist the complete source-bound result | **Senge, Peter** — `findings.md` only. |
| `auditor` | after writer | Independent completeness, copyright, and claim-ceiling audit | **Brandenburg, Martin** — ACCEPT or one bounded writer revision. |

## Dependency Flow

```text
explorers (parallel)
  -> synthesizer
  <-> reviewers (parallel; zig-zag cap 1)
  -> exact-binding evidence closure
  -> findings writer
  -> auditor
  -> parent final approval
```

One bounded synthesizer-to-explorers feedback edge may repair missing source identity, PDF access, digest, or selector evidence. One bounded auditor-to-writer edge may repair wording or structure when evidence already exists. The writer cannot manufacture missing paper evidence.

## Inventory Preflight

- Machine index: `.arcanum/inventory/index.json`.
- Validation: `lookup_readiness=ready`, 301 entries, zero failures, 146 historical-tag warnings, partial source coverage, Inventory-read-model boundary only.
- Selected: Craft teaching review, Interactive Ontology Learning Map, Body War novice-comprehension review, and the exact-binding learning-graph research result.
- Excluded: selective-promotion comprehension, high-attention model research, and broad dispersed-knowledge cartography because they do not own this corpus.
- Gap: no Inventory entry names CogTools Lab or this new corpus.
- Design consequence: live pages own enumeration; exact bindings own paper evidence; comprehension and formal analogy remain separate claim classes.

The full non-authority packet is in `strategy-inventory-packet.json`.

## Boundaries

- The complete claim is snapshot-bound: `papers.html` as observed during the run, not all lab output forever.
- Inaccessible or mutable teaching surfaces remain explicit residue.
- Availability, hashing, extraction, and browser access do not establish learning or human comprehension.
- Formal or computational analogy does not prove cognitive mechanisms.
- Paper summaries are paraphrased and source-bound; full texts are not reproduced.
- No deployed paper, public Arcanum artifact, ontology, definitions, Inventory authority, Git state, publication, promotion, release, or deployment is changed.

## Gate And Ledger State

- Live research schema: `0.8.0`.
- Candidate sheet: `dispatch-sheet.json`; it intentionally omits `evidence_binding` before confirmation.
- Registrar validation: `pass`; current sheet SHA-256 is `40057058d95e90515ce04d43a508b05e1e860cefaa8069faf98314cca33dd988`; ledger mutation `none`.
- Material projection: `material-strategy.json`; material SHA-256 is `203623ea0fd112718bacffb81d9ad4dccceb3a47d59e3ab60db5e6c0e0727a21`.
- Dispatch Spec: `pass`; capability-bound execution owner is `orchestrate` and authorization remains `requires_user_permission`.
- Check-tension: `PASS/PASS` on the current digest. The superseded Test-2 rejection and exact repair are preserved in `CHECK-TENSION.md`.
- Human confirmation: received for the unchanged material strategy; handle `confirmation-cogtoolslab-40057058-20260807` is bound to the current sheet digest.
- Registration: appended exactly once under schema `0.8.0`.
- Execution: Orchestrate run 1 closed fail-closed in the explorer wave. Two explorers spawned, joined, and closed; the third spawn was rejected by the native agent-thread limit; the fourth was not attempted.
- Evidence closure: `blocked`. The middle-period lane closed all 29 rows; the modern lane established enumeration and byte identities for 36 rows but left every semantic capsule and exact selector unclosed. The historical and teaching lanes did not run.
- Dispatch close: one append-only close row records `exit_reason: error`, two spawned explorers, zero feedback loops, and no downstream agents.
- Post-result Inventory: the complete non-authority strategy-result candidate is preserved at `.arcanum/inventory/queries/2026-08-07-cogtoolslab-complete-corpus-research-strategy-result.md`. The deterministic updater blocked before write because its isolated candidate copy cannot resolve existing repository-external source paths, so the human-index link remains pending; the live machine and human indexes remained byte-identical and the baseline remains lookup-ready.
- Closeout expectation if confirmed: exactly one dispatch row and one close row; every spawned agent must be joined and closed; durable findings and closeout evidence return to Inventory and observability afterward.

## Next Human Action

The next governed action, if the program is to continue, is a fresh replay-safe recovery strategy that preserves the same claim boundary, admits an available PDF extractor such as `pypdf`, and executes under a host context with capacity for every declared explorer. This closed dispatch cannot be silently retried.
