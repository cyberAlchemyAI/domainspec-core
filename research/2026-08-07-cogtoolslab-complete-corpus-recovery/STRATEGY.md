# CogTools Lab Complete-Corpus Recovery Strategy

Status: `closed: error; partial paper evidence preserved`
Dispatch type: `research`
Evidence contract: `exact-binding recovery`
Authority effect: `none`

## P1 Trigger Decision

Dispatch remains required. The closed run left three independently bounded evidence gaps: semantic repair of 36 modern papers, acquisition of 25 historical papers, and acquisition of the one-hop teaching corpus. Synthesis, adversarial review, exact-binding closure, writing, and audit remain downstream. Raw paper evidence would overflow the parent context, while corpus completeness and cognitive-claim boundaries require independent attacks.

This is a new recovery strategy, not a retry of the closed dispatch. The failed dispatch remains closed with `exit_reason: error`.

## Frozen Recovery Scope

The recovery will:

1. reuse the 29 exact-bound 2021–2023 rows preserved in the prior `research.md`;
2. re-fetch and semantically parse the 36 already byte-bound 2024–2026 PDFs, checking for digest drift and adding paper-read capsules plus exact selectors;
3. acquire and bind all 25 page-listed 2009–2020 papers while preserving their historical terminology;
4. audit seven course descriptions and five directly linked public course or syllabus surfaces, following exactly one hop for public readings and recording access residue;
5. reconcile 90 unique Tier-A rows partitioned `36/29/25`, deduplicate Tier-B readings, and produce an audited findings artifact.

It will not recurse through bibliographies, retain PDF bytes, claim that course inclusion proves teaching effectiveness, claim that document extraction proves comprehension, or treat formal or computational analogy as cognitive proof.

## Groups And Outputs

| Group | Native wave | Subagents | Owned result |
|---|---:|---|---|
| `paper-explorers` | 2 concurrent | **Halford, Graeme** repairs all 36 modern semantic bindings. **Bateson, Gregory** acquires all 25 historical rows. | Two exact-bound explorer receipts with drift, selectors, and residue. |
| `teaching-explorer` | 1 after paper join | **Simon, Herbert** audits the one-hop teaching corpus and research framing. | Teaching-reading, deduplication, access, and framing receipt. |
| `synthesizer` | 1 | **Beer, Stafford** combines recovered evidence with the 29 reusable middle rows. | Complete manifest, thematic and temporal maps, contradictions, crosswalk, and closure candidate. |
| `reviewers-core` | 2 concurrent | **Hacking, Ian** attacks precedent and ownership. **Popper, Karl** attacks non-vacuity and reproducibility. | Two independent attack receipts. |
| `scope-reviewer` | 1 after core join | **Quine, Willard Van Orman** attacks definitional collapse and cognitive-proof overreach. | KEEP/MERGE/RENAME/DEFER/KILL scope receipt. |
| `writer` | 1 after exact-binding closure | **Senge, Peter** writes `findings.md` only. | Source-bound findings and writer receipt. |
| `auditor` | 1 after writer | **Brandenburg, Martin** audits completeness, copyright, and claim ceilings. | ACCEPT or one bounded writer revision. |

## Dependency And Capacity Plan

```text
paper explorers (2; join all)
  -> teaching explorer (1)
  -> synthesizer (1)
  -> precedent + non-vacuity reviewers (2; join all)
  -> scope reviewer (1)
  -> exact-binding closure
  -> findings writer (1)
  -> auditor (1)
  -> parent final approval
```

No native execution wave exceeds two agents. This is a capacity repair grounded in the prior host observation that two concurrent spawns succeeded and the third failed; it is not a guarantee that a future spawn will succeed. Any rejected spawn blocks that wave with residue rather than silently shrinking the review.

One bounded synthesizer-to-explorer feedback edge may repair missing source identity, bytes, drift, or selectors. One auditor-to-writer feedback edge may repair wording or structure when the evidence already exists. The writer cannot manufacture missing paper evidence.

## Inventory Preflight

- Machine index: `.arcanum/inventory/index.json`.
- Readiness: `ready`; 301 entries, zero validation failures, 146 inherited uncontrolled-historical-tag warnings.
- Selected precedents: Craft causal-class teaching review, Interactive Ontology Learning Map, Body War novice-comprehension review, and Learning Graph exact-binding research synthesis.
- Excluded: selective-promotion comprehension, generic high-attention-model strategy, and broad dispersed-knowledge cartography because none owns this corpus.
- Gap: no Inventory entry owns CogTools Lab or the requested corpus.
- Consequences: live CogTools Lab pages own enumeration; exact source bindings own paper claims; Inventory remains a non-authority discovery read model; comprehension and formal analogy remain separate claim classes.

The complete packet, including the live page digests and recovery inputs, is `strategy-inventory-packet.json`.

## Source And Evidence Boundary

- Live preflight observed HTTP 200 for all three named pages and 90 distinct PDF links on `papers.html`.
- The teaching and research pages expose no direct PDF links; teaching-reading count therefore remains unknown until the one-hop lane runs.
- `pypdf` and `pdfminer` are locally importable. Explorers must parse transient bytes through memory and must not commit PDFs.
- Every durable paper capsule must be a concise paraphrase with an exact PDF page or named-section selector.
- Snapshot completeness is not permanent bibliographic completeness.
- Structural extraction, model behavior, cognitive effect, and human comprehension are different evidence classes.

## Gates And Current State

- Live research schema: `0.8.0`.
- Candidate sheet: `dispatch-sheet.json`; its immutable bytes remain the evidence-bound registration source.
- Registrar validation: `pass`; sheet SHA-256 `38f4b7b5f7f4fc322491725b78173a497b7a8e9947036aa98f0d6b273aac783a`; ledger mutation `none`.
- Material projection: `material-strategy.json`; material SHA-256 `ff14ad4ed7e977d5c721fa5445ea49d4a8e5ef72f8a0b580d11b520e5787e84e`.
- Dispatch Spec: `pass`; authorized route SHA-256 `6e3aa39ff5aaae890e5e8b2de872bbfca45fc55a7408fd16452985172ee113ab`; execution owner `orchestrate`; authorization `approved`.
- Check-tension: `PASS/PASS` on the exact current sheet digest.
- Human confirmation: received and recorded in `confirmation.json` under handle `confirmation-cogtoolslab-recovery-38f4b7b5-20260807`.
- Registration and closeout: appended exactly once each under schema `0.8.0`; close `exit_reason: error`.
- Research workers: two paper explorers spawned, joined, and closed; 36 modern and 24 historical PDFs gained semantic capsules and selectors, while `fan_bbs_2014` remained unclosed because the source URL returns HTTP 404.
- Gate: `g-paper-coverage` blocked; the teaching, synthesis, review, writer, and auditor waves did not run.
- Findings, publication, paper edits, promotion, release, and deployment: not performed.

## Required Next Action

The closed run cannot be silently retried. A later proposal must repair the single `fan_bbs_2014` source binding, complete the teaching lane, and then reuse the 89 semantically bound Tier-A rows for synthesis and audit.
