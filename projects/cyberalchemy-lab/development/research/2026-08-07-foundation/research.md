# CyberAlchemy Lab Foundation — Verbatim Explorer Returns

This file is a parent-owned mechanical transcript of the three read-only explorer returns for dispatch `2026-08-07-cyberalchemy-lab-foundation`, run `run-001`. The enclosing labels are transcript metadata; the content inside each labelled block is preserved verbatim. A return is research evidence, not ontology authority, implementation proof, promotion, publication, or deployment evidence.

<!-- BEGIN VERBATIM RETURN: spawn-0001 corpus-explorer -->

## Corpus-cartography result

### Frozen boundary

Snapshot: 2026-08-07, repository root `/home/vrondelli/projects/domainspec-core`.

- Census command: `rg --files -uuu -g 'TOWER.md' | sort`
- Observed path occurrences: **41**
- Distinct byte digests: **33**
- Duplicate-collapsed content families: **31**
- Current-contract exact scaffold occurrences: **24**
- Current-contract nonconforming/custom occurrences: **17**
- Completeness claim: **none**. This is a frozen `TOWER.md` occurrence census, not “all research.”
- Source identity: `research/tower-system-taxonomy/Tower-System.pdf`, SHA-256 `2318a4066b8146e7073781df7aa62589938789685b6c2c64cf83737613f32f5b`.
- Residue: the strategy packet and `file(1)` report 8 PDF pages, while `pypdf` exposes 9 page objects. Bind the source by digest, not page count, until reconciled.

Inventory was used only as a discovery projection. Its live validation passed with `lookup_readiness=ready`, 0 failures, and 146 uncontrolled-tag warnings.

### Eligibility and identity rules

1. A tower candidate is the package root containing `TOWER.md`, not every Markdown file beneath it.
2. Eligibility requires a coherent target plus a navigational or contractual spine. Exact current-contract conformance is recorded separately from eligibility.
3. The generated `research-tower` v0.1 shape requires `README.md`, `TOWER.md`, `levels/L0-corpus.md`, `levels/L1-residue-map.md`, `levels/L2-closure-plan.md`, `gates/closure-gates.md`, and `residue/open-residue.md`.
4. Package identity should bind owning repository, package-root path, `TOWER.md` digest, source-snapshot identity, and declared lineage/version. Path or digest alone is insufficient.
5. Worktrees, test/output packages, and handoff copies are projections or copies unless their owner explicitly establishes a new lineage.
6. Equal bytes prove duplication, not canonical ownership. Different bytes do not prove supersession; two output snapshots differ from their source only by a final newline.
7. Closure state and package generation are orthogonal: a legacy/custom tower may contain substantial research, while a current scaffold may remain candidate or empirically open.
8. Only `arcanum/` is public. Everything else remains private/non-public unless a separate publication owner proves otherwise.

Codes below:

- Class: `A/PUB` public Arcanum nested repo; `C/PRIV` private CAV2 original; `H/PRIV` private handoff; `L/PRIV` private nested Lean repo; `P/PRIV` private project; `R/PRIV` private root research; `WP/*` worktree copy; `O/PRIV` output/test fixture.
- Generation: `G2` exact current scaffold; `G1` adapted scaffold with renamed level artifacts; `G0` legacy/custom.
- Missing: `M0` none; `M1` exact L1/L2/gates; `M2` exact levels L0/L1/L2, gates, residue; `M3` exact L1/L2; `M4` exact levels L0/L1/L2 and gates.

### Manifest

| ID | Repository-relative path | Digest | Class | Gen/missing | Duplicate or supersession relation | Research status and residue |
|---|---|---:|---|---|---|---|
| T01 | `.claude/worktrees/codex+infra-spec/arcanum/research/autobayes/TOWER.md` | D01 | WP/PUB-mirror | G2/M0 | Exact T05 mirror | Active; noncanonical worktree occurrence |
| T02 | `.claude/worktrees/codex+infra-spec/arcanum/research/monoidal-categories-multicategories/TOWER.md` | D02 | WP/PUB-mirror | G2/M0 | Exact T07 mirror | Pass; related bibliography partial |
| T03 | `.claude/worktrees/codex+infra-spec/projects/ontologize/TOWER.md` | D03 | WP/PRIV | G1/M1 | Exact T23 mirror | Dispatch pass; product validation open |
| T04 | `arcanum/research/agentic-context-management/TOWER.md` | D04 | A/PUB | G2/M0 | Unique | Closed for standard source understanding; local research only |
| T05 | `arcanum/research/autobayes/TOWER.md` | D01 | A/PUB | G2/M0 | T01 exact; T18 newline-only snapshot | Active; named source/definition/promotion residue |
| T06 | `arcanum/research/claude-shannon-secrecy-systems/TOWER.md` | D05 | A/PUB | G2/M0 | Unique | Starter understanding closed; full corpus/modern proof/cryptanalysis open |
| T07 | `arcanum/research/monoidal-categories-multicategories/TOWER.md` | D02 | A/PUB | G2/M0 | T02 exact; T19 newline-only snapshot | Pass; related bibliography partial |
| T08 | `arcanum/research/triton-top2-backward-kernel/TOWER.md` | D06 | A/PUB | G0/M2 | Exact T21/T41; canonical owner unresolved | Rich custom tower; explicit GPU/JVP blockers |
| T09 | `cyberAlchemy-v2/development/research/2026-07-22-categorical-dng-semantic-hierarchy-towers/handoffs/2026-07-23-researcher-evidence-harness/research/2026-07-22-categorical-dng-semantic-hierarchy-towers/towers/categorical-learning-system/TOWER.md` | D07 | H/PRIV | G2/M0 | Exact handoff copy of T11 | Source closure inherited; noncanonical handoff |
| T10 | `cyberAlchemy-v2/development/research/2026-07-22-categorical-dng-semantic-hierarchy-towers/handoffs/2026-07-23-researcher-evidence-harness/research/2026-07-22-categorical-dng-semantic-hierarchy-towers/towers/dynamic-neural-graph-inference/TOWER.md` | D08 | H/PRIV | G2/M0 | Exact handoff copy of T12 | Source synthesis closed; DNG validation excluded |
| T11 | `cyberAlchemy-v2/development/research/2026-07-22-categorical-dng-semantic-hierarchy-towers/towers/categorical-learning-system/TOWER.md` | D07 | C/PRIV | G2/M0 | Original candidate for T09 | L0-L2 closed; audit-status rules retained |
| T12 | `cyberAlchemy-v2/development/research/2026-07-22-categorical-dng-semantic-hierarchy-towers/towers/dynamic-neural-graph-inference/TOWER.md` | D08 | C/PRIV | G2/M0 | Original candidate for T10 | Source synthesis closed; runtime applicability unproved |
| T13 | `cyberAlchemy-v2/development/research/2026-07-23-categorical-deep-learning-algebraic-architectures/TOWER.md` | D09 | C/PRIV | G2/M0 | Unique | Research question closed; broader/Lean program incomplete |
| T14 | `domainspec-lean-formalization/research-gpt/TOWER.md` | D10 | L/PRIV | G2/M0 | Unique | Active; direct omega target closed-negative, positive completion residue promoted |
| T15 | `domainspec-lean-formalization/research/categorical-deep-learning-algebraic-architectures/TOWER.md` | D11 | L/PRIV | G1/M3 | Unique, currently untracked in nested repo | Feasibility seed closed; paper program remains open |
| T16 | `domainspec-lean-formalization/research/cyberalchemy-functor-stack-bet/TOWER.md` | D12 | L/PRIV | G2/M0 | Unique | Local-only; decisive experiment and P3 theorem residue open |
| T17 | `domainspec-lean-formalization/research/self-harness-tower/tower/TOWER.md` | D13 | L/PRIV | G0/M4 | Unique | Source-first claim ledger; no aggregate closure declared |
| T18 | `output/research-package-20260616/tests/arcanum/research/autobayes/TOWER.md` | D14 | O/PRIV | G2/M0 | T05 plus missing final newline | Test snapshot; no authority/supersession effect |
| T19 | `output/research-package-20260616/tests/arcanum/research/monoidal-categories-multicategories/TOWER.md` | D15 | O/PRIV | G2/M0 | T07 plus missing final newline | Test snapshot; no authority/supersession effect |
| T20 | `output/research-package-20260616/tests/lesswrong-rationality/TOWER.md` | D16 | O/PRIV | G2/M0 | Exact T36 copy | Test snapshot; local-only source gaps inherited |
| T21 | `output/research-package-20260616/tests/triton-top2-backward-kernel/TOWER.md` | D06 | O/PRIV | G0/M2 | Exact T08/T41 | Test fixture; no authority |
| T22 | `projects/domainspec-v2/research/alloy-tla-modeling/TOWER.md` | D17 | P/PRIV | G2/M0 | Unique | Active; Alloy/TLA syntax and tool validation excluded/open |
| T23 | `projects/ontologize/TOWER.md` | D03 | P/PRIV | G1/M1 | Exact T03 worktree copy | Dispatch pass; product validation open |
| T24 | `projects/ontologize/operational-ontology/TOWER.md` | D18 | P/PRIV | G1/M4 | Unique | No aggregate closure; promotion requires separate owners |
| T25 | `research/2026-08-04-ontology-video-voice-provider-research/performance-preserving-enhancement/TOWER.md` | D19 | R/PRIV | G2/M0 | Unique | Desk research complete; empirical audition open |
| T26 | `research/2026-08-07-cognitive-tools-reflection-tower/TOWER.md` | D20 | R/PRIV | G2/M0 | Unique; currently untracked | Candidate; evidence-harness-ready, not cognitive result |
| T27 | `research/agentic-music-studio/TOWER.md` | D21 | R/PRIV | G2/M0 | Unique | No aggregate closure declared; build plans do not prove product |
| T28 | `research/jusbrasil-call/towers/feijo-moreira-entailment-summ/TOWER.md` | D22 | R/PRIV | G0/M2 | Unique | Standard custom package; no aggregate closure declared |
| T29 | `research/jusbrasil-call/towers/jua-benchmark/TOWER.md` | D23 | R/PRIV | G0/M2 | Unique | Local-only custom package; no aggregate closure declared |
| T30 | `research/jusbrasil-call/towers/juru-legal-llm/TOWER.md` | D24 | R/PRIV | G0/M2 | Unique | Local-only; unfetched content remains residue |
| T31 | `research/jusbrasil-call/towers/magesh-hallucination-free/TOWER.md` | D25 | R/PRIV | G0/M2 | Unique | Custom learning pack; full-PDF detail remains residue |
| T32 | `research/jusbrasil-call/towers/menezes-neto-outcome-prediction/TOWER.md` | D26 | R/PRIV | G0/M2 | Unique | Built standard; source/reading separation explicit |
| T33 | `research/jusbrasil-call/towers/multi-lexsum/TOWER.md` | D27 | R/PRIV | G0/M2 | Unique | Partial: abstract/site grounded; baselines and splits open |
| T34 | `research/jusbrasil-call/towers/robertalexpt/TOWER.md` | D28 | R/PRIV | G0/M2 | Unique | Custom package; no aggregate closure declared |
| T35 | `research/jusbrasil-call/towers/ulysseslegalner-br/TOWER.md` | D29 | R/PRIV | G0/M2 | Unique | Built standard; full PDF not fetched |
| T36 | `research/lesswrong-rationality/TOWER.md` | D16 | R/PRIV | G2/M0 | T20 exact test copy | Local-only; unfetched essay gaps retained |
| T37 | `research/mtng-resonantos/TOWER.md` | D30 | R/PRIV | G2/M0 | Unique | External code/OKF assertions unverified |
| T38 | `research/smt-fol-test-derivation/TOWER.md` | D31 | R/PRIV | G0/M2 | Unique | Active starter; L2/bridges pending |
| T39 | `research/sovereign-biocentric-ai-cognitive-commons/TOWER.md` | D32 | R/PRIV | G2/M0 | Unique | Closed, local-research-only |
| T40 | `research/ternary-models/TOWER.md` | D33 | R/PRIV | G2/M0 | Unique | Active starter; L2 and learning pack partial |
| T41 | `research/triton-top2-backward-kernel/TOWER.md` | D06 | R/PRIV | G0/M2 | Exact T08/T21; owner unresolved | Rich custom tower; runtime/GPU residue remains |

Digest ledger:

```text
D01 294b624f42ae90cb313ec7163d6a7950962992afc268cb7247b9cd70110e3fcb
D02 8a7776b6f32a7f50a48b601e8b635369c35d9ba7c7fc96613343a0e51dbaa1b2
D03 32344f5b9139db854f34caf0c5ab75bbcee5ff27e6a7cc7edbd1452540f7cd33
D04 0299995e93f92fd9dda92ddb87ddc35c14e0d7aab7f7d2d713bad2a13838821a
D05 09cb155e259f09d462cb0b9011b275a2b49872fe58516f744eee243ddf5fa1e2
D06 d890ec4646e25d0f5aede568f55f66a3f290c1624cb54f8d68a2b960ae42eecb
D07 c950b109e9c2907df80146dc28047fcd14a2c33b8f25906e5c4279cb517a2aeb
D08 cf216a91ed460bea68c15afd5a6e009e924acc4df9982af3d5617539a9450f2e
D09 4f6cff2a11f4c159cd034f612bfd6fede164191f608448b94119d5f3ec8719ee
D10 18c994c3fcb71f31a9385e6eb364e735e8c349724d66e8a4bfb2611a19481cba
D11 4ccc20ea8a44e231b008e417c979aa4b7ab40fc81009104510c81a7ca55f616b
D12 95a5a9734ae0e53e5e78efdca5910aecf7f9ba717fe0a8b81e7a14e16ef26022
D13 32652ac0199b0b11dd4214ca8051ebf7a9e0a6ea2ede794c760f81611035b338
D14 ead3b94ba7ea8adfb6371a4cc4884fcf09e11d3e0741c1d7814dd05bec71a93a
D15 7e34444473007b0492786002b22a98a5000f97c888d93ab9a63bfe4c7ad3e325
D16 b4793d733f787da6dd4e3d58a952e2cc12daa6ad08bd7517088c0260731f280a
D17 3ded7940bb76e93d261c3c263f4e7ad9e1dbeb3d6fdc9266f2d854f24b22677a
D18 a6e6b13443a112b7e85022ecbdfd6b90004a562fb0e4d42f9490d2a5ea171fb1
D19 0b751c7037d03e23569a74253616f0cae714cc03e87bdbc180c3c16d236af794
D20 693377f3b78cc440e46f20b89dfd51e2dbf6ac8d60939279f2742355afcb1324
D21 105fe2ed8eab44f8260fb17090692906b5507928621130cd11962fbf17bf841c
D22 520d39dd47928e6e02fc39e351d2625bbba1cbb81737935152ced3d445a9bb69
D23 d7f0d57483226570b19733bc58485acb45582595da060d2bdaee4bbf48475895
D24 ea3a21de6630cc5d31a0d27cbf018e70f4d996770c3cd53815cdf66a7cfff78e
D25 e6fcf4409b3020760d5591b1c6bcd8ba0618737974878a2d741ec0eac4ae0558
D26 9911593174d4f4c7544bec9adc234a412129f6595e38daa9db88d22035ce8846
D27 789da0f8072e084d0515500682504db6718ed87c32299a7215707d99ef82e335
D28 b5ab1d18ccc2088288effe8ff3a484506749d0d21d86271b63ed9911605f4c2a
D29 38383c80e402b0f7c75add6c038b40a2e63d2ef81403876b3bcd609b069f25f8
D30 83ad149cc1dbcfa89933065163dd82a397620625b002f37d1c541401a4fb1118
D31 7540a8aa83b2d54848cc816b65a49739224b8a65b2433a866e4d9c57e4b07f5d
D32 d81519de92882164ef0b9373a71fc136e38349898d3b148cbc989a6f29bbb394
D33 2614c67efa60f1ccda42385c3667444c442db131205c37903a1a64a5c1a812fe
```

### Tower System ↔ Research Tower crosswalk

| Tower System element | Research Tower evidence | Fit |
|---|---|---|
| L1 queryable graph | Markdown artifact spine and cross-links | Partial only; no runtime-queryable graph object |
| L1 persona set | No persona artifact/schema in the generated contract | Absent; Tower System D1 remains net-new |
| L2 distill-build | Source record → L0/L1/L2 → glossary/definitions/distill/learning pack | Strong executed precedent |
| L2 human read-through | Generated contract is agent/source-driven | Absent as a defined human accrual method |
| L2 promote | Research outputs remain local; promotion requires another owner | Guardrail exists; graph promotion mechanism absent |
| L3 debate/dispatch/application | Optional governed subagents and mandatory closeout ledger | Partial transport/governance; no reusable tensioned persona operation |
| Lφ MOGT decision policy | Not part of Research Tower | Separate owned, design-stage system |
| L4 scoring/adjudication | Claim kinds, bridge statuses, closure gates, source labels | Research adjudication only; no ELO/oracle-consensus engine |
| Recursion | Decomposition, subagents, and evidence-harness handoff | Partial; no runtime sub-tower/cycle-guard contract |
| Evidence boundary | Source-first, local-only, claim≤proof | Strong alignment |

This confirms the corrected boundary in `PRECEDENT-RECHECK.md`: Research Tower construction is owned/executed; persona-as-artifact, runtime-queryable graph, and ELO/oracle-consensus remain unwitnessed.

### Non-tower research coverage gaps

Presence-only screen, not eligibility adjudication:

| Frozen container rule | Immediate roots/containers | With descendant `TOWER.md` | Without descendant `TOWER.md` |
|---|---:|---:|---:|
| `research/*/` | 41 | 10 | 31 |
| `arcanum/research/*/` | 11 | 5 | 6 |
| `cyberAlchemy-v2/development/research/*/` | 31 | 2 | 29 |
| `domainspec-lean-formalization/research/*/` | 163 | 3 | 160 |
| `projects/*/research/` containers | 13 | 1 | 12 |

Material examples include `research/tower-system-taxonomy/`, `arcanum/research/mogt-agentic-conversation/`, `arcanum/research/dispatch-composition-attack/`, 29 CAV2 research roots, and extensive Lean proof/residue folders. Their lack of `TOWER.md` is a migration/eligibility question, not evidence that they are deficient or should become towers.

### Representative witness candidates

1. **T04 Agentic Context Management** — strongest clean positive: public owner, exact G2 scaffold, source record, validation artifact, explicit closure and promotion ceiling.
2. **T11/T09 Categorical Learning System** — strongest duplicate/provenance witness: complete private G2 package plus byte-identical handoff copy, allowing deterministic canonical-versus-copy and privacy tests.
3. **T08/T21/T41 Triton Top2** — strongest stress witness: one digest across public Arcanum, private research, and output/test locations; rich custom G0 package with active blockers. It tests legacy adaptation, owner ambiguity, duplicate collapse, and refusal to infer canonicality from bytes.

## Compact receipt

```yaml
action_id: spawn-0001
dispatch_id: 2026-08-07-cyberalchemy-lab-foundation
run_id: run-001
wave_id: wave-01-explorers
role: corpus-explorer
capability_ref: research
status: pass
validation: pass
blockers: []
started_at: unavailable
finished_at: 2026-08-07T20:48:24-03:00
files_and_selectors_inspected:
  - research/tower-system-taxonomy/Tower-System.pdf@sha256:2318a4066b8146e7073781df7aa62589938789685b6c2c64cf83737613f32f5b
  - research/tower-system-taxonomy/research.md#Explorer-1..3
  - research/tower-system-taxonomy/findings.md#Verdict-Matrix,#Resolved-Answers,#Correction
  - research/tower-system-taxonomy/PRECEDENT-RECHECK.md#Re-verdict-table
  - research/tower-system-taxonomy/SYSTEM-VIEW.md#Layer-stack,#Reuse-map,#Evidence-boundary
  - .agents/skills/research-tower/SKILL.md#process,#promotion-rule,#quality-bar,#output-contract
  - .agents/skills/inventory/SKILL.md#lookup-process,#authority-rule
  - projects/cyberalchemy-lab/development/research/2026-08-07-foundation/dispatch-sheet.json#explorers[0]
  - projects/cyberalchemy-lab/development/research/2026-08-07-foundation/strategy-inventory-packet.json#direct_source_preflight,#unresolved_gaps,#non_authority_notice
  - T01..T41 exact paths above: headings, status/closure, source-kind, promotion selectors, sibling required-artifact presence
commands_checks_run:
  - sha256sum and PDF type/page extraction
  - rg --files -uuu -g TOWER.md
  - per-path sha256sum, wc, heading/status selector scan
  - required seven-artifact existence check
  - duplicate digest grouping, cmp, diff
  - git repository/remote/submodule/tracked-state inspection
  - inventory index jq lookup
  - .agents/skills/inventory/scripts/validate-index-json.sh .arcanum/inventory/index.json
  - presence-only immediate research-root gap census
residue:
  - PDF page-count discrepancy: 8 reported versus 9 pypdf page objects
  - Triton canonical owner unresolved across three exact copies
  - legacy non-tower research eligibility remains owner decision
  - 31 content families are not 31 canonical or closed towers
reroute_needs:
  - synthesizer should preserve the three residues above
  - ontology/authority owner must decide any later identity or promotion record
observer_status: not-assigned
handoff_note: Parent may normalize this return into orchestrate/run-001/receipts/wave-01-explorers/corpus-explorer.json; no file was written by this explorer.
```

<!-- END VERBATIM RETURN: spawn-0001 corpus-explorer -->

<!-- BEGIN VERBATIM RETURN: spawn-0002 workbench-explorer -->

## Workbench-integration reality

Verdict: the existing IDE workbench supplies a usable local presentation substrate, event-derived state, approval/receipt separation, and evidence inspection. It does not supply a Tower Navigator, tower identity/provenance schema, hostile-HTML containment, tower-specific interaction policy, or ontology authority. A one-tower candidate witness is feasible, but “read-only” must mean no mutation of tower/source/ontology bytes: current Canvas publication still appends local projection/audit state.

The two development paths in the prompt resolve under `projects/ide-extension/development/`.

### Evidence status

| Classification | Current finding |
|---|---|
| Documented and implemented | Loopback server; schema-validated module manifests; ID-addressed envelopes/approvals; event-derived state; manual bridge; V0 Canvas publication, revision binding, interactions, and evidence routes. See `projects/ide-extension/src/server.mjs:499-565,620-633,1106-1264,1839-1990`; `src/kernel/projector.mjs:12-29,728-895,1514-1537`. |
| Implemented projection/UI | Pure `RunView` maps envelope typestate to stage, legal actions, claim, result, and evidence handles. See `src/ui/run-view.mjs:1-133`; UI consumption in `public/demo/l0.html:2101-2179,2239-2418`. |
| Test coverage present | Static test sources cover approval replay, schema admission, evidence binding, Canvas publication, path containment, stale revisions, cursor replay, RunView, browser Canvas, and Inspector. These tests were inspected, not executed in this action. |
| Historical validation | `development/workbench-ui-v1/task-sessions/20260720T173722Z-swu-wui-011/MACHINE-VALIDATION-REPORT.md:3-21` records a 2026-07-20 machine pass. It is historical evidence, not a current rerun. |
| Planned/unpromoted | Workbench UI V1 remains blocked on a human usefulness verdict, despite historical machine evidence: the same report at lines 43-49 and `development/workbench-ui-v1/README.md`. |
| Deferred | Hostile HTML containment, authenticated per-session Canvas routing, historical V0 snapshots, remote access, provider execution, browser control, and an IDE wrapper. `SPEC.md:272-278`; `README.md:41-49`. |
| Contradicted/stale prose | `SPEC.md:124-129` describes a legacy `running` state, but legacy approval transitions directly to `passed` in `src/envelopes/dry-run-envelope.mjs:76-113`; the acceptance sequence separately calls this a no-op receipt. The 2026-07-10 review is not current implementation truth: replay, singleton, schema, evidence, and persistence defects have current repairs, while unresolved module source ownership remains. |
| Not implemented | `projects/cyberalchemy-lab/` currently contains only the foundation research/dispatch package. No Tower Navigator module, schema, route, fixture, compiler, or UI exists. |

Current key-byte bindings include:

- `src/server.mjs`: `e69bdb17fb9a7b517d5089963c294c1d18f7656a3a2ac3c525b518404e5a16f7`
- `src/kernel/projector.mjs`: `3ff4a94492f064548513517efc1e0c018e15ed2b474fcb9cf97055e91ecb09f6`
- `src/kernel/canvas.mjs`: `53e6b522b52f6c47eede5cc1fe758863e7c4b5f564b0122dc42f74a3dcb5a47d`
- `public/demo/l0.html`: `e5f5ed5d82e8984eb4b663c74a23cc6ad2ddc8f4bd12c12cd1c96df218cadea7`
- `schemas/canvas-interaction-request.schema.json`: `249f508d57e115a11f2872f415bcee7a0ce8e8e5cb52be7bfbbeac8c0e044de`

## Interface map

| Interface | Current contract | Tower consequence |
|---|---|---|
| Modules | Manifest fields are `module_id`, `display_name`, `owner_route`, `source_refs`, capabilities/effects/gates/receipts (`schemas/module-manifest.schema.json`). Registry validates shape and loads sorted JSON (`src/kernel/registry.mjs:1-24`). | Add a CyberAlchemy Lab module, but do not treat its string `source_refs` as resolved provenance. Current registry records no digest, selector, revision, privacy class, or verification status. |
| Envelopes | Legacy and bridge envelopes bind envelope/run/agent/task/context/grants/skill/approval/state/receipts (`schemas/agent-envelope.schema.json`). | Suitable only for a later protected execution request. Merely opening/navigating a tower should not manufacture an execution envelope. |
| Run state | Event-derived maps for envelopes, approvals, receipts, bridge claims/results; `RunView` exposes typestate, stage, legal actions, claim/result/evidence. | A Tower Navigator needs separate selection/projection state. Tower nodes must not be masqueraded as runs. |
| Approval | Browser may approve/reject pending work; bridge authorization and execution remain distinct. `src/server.mjs:1914-2245`; `public/demo/l0.html:2598-2678`. | No approval is necessary for source-local read/navigation. Any later write, promotion, export, provider, browser-act, or publication remains behind its owning gate. |
| Receipts | Legacy, `authorization.receipt`, and `skill.execution` are a closed union (`schemas/receipt.schema.json`). Evidence endpoints resolve bound artifacts (`src/server.mjs:1839-1912`). | A Canvas publication or navigation event is not one of these receipts. Tower validation may have a separate validation report, but must not be labeled protected-effect execution. |
| Evidence inspection | Proposal detail joins envelope, approval, receipts, claims, result; Inspector renders IDs and evidence endpoints (`src/server.mjs:291-343`; `public/demo/l0.html:2239-2418`). | Reusable for provenance display if tower evidence remains separately typed: source anchor, digest, selector, claim status, residue. |
| Canvas publication | `POST /api/canvas/publish` reads one contained `.html`, hashes it, assigns path-stable surface identity, and appends `canvas.surface_published`; duplicate same-path/same-hash is idempotent (`src/kernel/canvas.mjs:24-145`; `src/server.mjs:1170-1227`). | Can host a trusted Tower shell as `kind: generic`. This writes only local Canvas projection/audit state, not tower source or ontology. |
| Canvas content | Content is reread from canonical workspace path. Digest mismatch returns `409 revision_changed`; missing/escaped source becomes unavailable (`src/server.mjs:1230-1264`). | Good final-HTML freshness guard, but insufficient for the tower inputs from which the HTML/projection was generated. |
| Named interactions | Any syntactically valid name is admitted with JSON payload and current surface/revision binding; 16 KiB boundary (`schemas/canvas-interaction-request.schema.json`; `src/server.mjs:1106-1168`). Examples are `decision.selected` and `craft.action_requested`. | Tower events require a semantic allowlist and payload schemas. Current generic contract does not know “unsupported interaction.” |
| Source retention | V0 stores path/digest/length/timestamps, not HTML bytes. Operations V1 separately stores digest-addressed blobs and can prune historical revisions (`src/kernel/canvas-blobs.mjs:75-226`; `src/kernel/canvas-retention.mjs:9-56,120-205`). | Keep tower files canonical. A witness should retain exact source locks and projection metadata, not copy source authority into Canvas blobs. |

## Current versus required Tower Navigator fields

| Concern | Available now | Required candidate fields |
|---|---|---|
| Projection identity | Canvas `surface_id`, `revision_id`, final HTML SHA-256 | `projection_id`, `projection_schema_version`, `projection_sha256`, generator/version, `generated_at`, ordered input-lock digest |
| Tower identity | None | `tower_id`, canonical root, package generation/version, owner/source class, status, privacy/publication class, aliases, duplicate/supersession relation |
| Source snapshot | Generic path and final HTML digest | Per-source `source_id`, normalized repo path, SHA-256, byte length, inspected revision/date, privacy class, availability |
| Evidence anchor | Generic `evidence_refs` strings | `anchor_id`, `source_id`, selector/line locator, selector digest where feasible, claim/evidence role, verification status |
| Knowledge view | Canvas title/kind only | Typed nodes for tower level, source, claim, residue, gate, definition, bridge decision; stable IDs and source anchors |
| Relations | None | Relation ID/type/from/to, admitted endpoint kinds, direction, evidence anchor, candidate status; no authority inference |
| Claim boundary | Receipt status and result summary | Claim status/support kind/allowed wording/ceiling; explicit blocked, refuted, open, or unsupported disposition |
| Residue | Generic evidence strings | Typed residue ID, category, severity, affected nodes/anchors, owner, closure state |
| Completeness | None | Included/excluded artifacts, eligibility rule, missing required artifacts, unknown count; no “all research” claim |
| Authority | Manifest owner string | `authority_effect: none`, owner route, promotion state, and explicit non-authoritative projection label |
| Navigation | Arbitrary Canvas event name/payload | Allowlisted `tower.node_selected`, `tower.evidence_selected`, and `tower.residue_selected` with exact payloads; all other names rejected |
| Freshness | Final HTML SHA-256 | Reverify every locked tower/source digest before projection return and before Canvas publication |

## Required failure behavior

| Case | Current behavior | Required Tower behavior |
|---|---|---|
| Stale revision | Interaction gets `409 stale_canvas_revision`; content gets `409 revision_changed`. Tests: `session-content-workbench-interactions.test.mjs:104-130`, `...publish.test.mjs:73-95`. | Preserve last verified view; return typed stale-projection/source error; accept no event against old projection. |
| Duplicate identity | Same path/hash is idempotent; same path/new hash is a revision. Projector rejects path-to-new-surface and duplicate hash within one surface (`projector.mjs:808-831`). Different paths with the same bytes remain distinct. | Reject duplicate `tower_id`; classify same-content/different-path candidates as duplicate/alias/supersession before display. |
| Hostile HTML | Not contained. `l0.html:1833-1869` creates a same-origin iframe with no `sandbox`; server emits no CSP headers (`server.mjs:471-484`). `SPEC.md:277` explicitly defers containment. | Never render source-supplied HTML. Use a fixed trusted shell and `textContent`/safe DOM construction. Malicious labels remain inert. Do not claim general Canvas containment. |
| Missing source | Canvas target returns `canvas_file_not_found`; evidence validation rejects missing refs. | Fail/abstain before projection publication when a load-bearing source or selector is missing; list optional missing artifacts as residue. |
| Changed digest | Final Canvas HTML is guarded; underlying tower inputs are not. | Compare every source lock; return expected/actual digest and invalidate the projection. |
| Unsupported interaction | Any name matching the generic regex is accepted. | Reject outside the three Tower navigation events without append. Reject wrong node kind/payload/binding. |
| Forbidden mutation | Canvas event names do not execute effects, but names such as `craft.action_requested` are accepted as audit events. Operations mutation routes also exist independently. | Tower route exposes GET plus navigation-only events. Reject write/promote/approve/export/provider/browser-act/operations requests; no implicit handoff to Craft or ontology. |

## Smallest one-tower witness

A mechanically suitable provisional fixture is `research/2026-08-07-cognitive-tools-reflection-tower/`. It is not selected as project authority or claimed representative; the corpus explorer may replace it. Useful exact locks are:

- `TOWER.md`: `693377f3b78cc440e46f20b89dfd51e2dbf6ac8d60939279f2742355afcb1324`
- `sources/source-record.md`: `a0a35f78f9ad923e5d92dd304c094260d762a1f26be9333e5e15a0fbb85a8b37`
- `claims/claim-ledger.md`: `117b0bd1c084713047f08df1c68522000f5885953115f155e5716758db842350`
- `residue/open-residue.md`: `f9ecf4817873f0c1e5d5e1d4f0d8ce8151462ba8d5c4eed95573178d474a7c4c`
- `VALIDATION.md`: `bbeadbc0ea5774c46ba4feb5d4c1e4d308295bb00c3682cf9a4b353b74db2b24`

The witness should show only:

1. Tower identity/status/claim ceiling.
2. L0-L3 level nodes from `TOWER.md:38-45`.
3. Source records S1-S14 from `sources/source-record.md:14-29`.
4. Claim dispositions C1-C14 from `claims/claim-ledger.md:12-27`.
5. Residue and exact source/digest/selector evidence.
6. Local node/evidence/residue selection; no domain mutation.

Later implementation would need these exact surfaces:

- New: `projects/ide-extension/src/modules/cyberalchemy-lab.manifest.json`
- New: `projects/ide-extension/schemas/tower-navigator-projection.schema.json`
- New: `projects/ide-extension/schemas/tower-navigator-interaction.schema.json`
- New: `projects/ide-extension/src/kernel/tower-navigator.mjs`
- New: `projects/ide-extension/public/canvas/tower-navigator.html`
- New candidate-local locks/projection under `projects/cyberalchemy-lab/witnesses/cognitive-tools-reflection/`
- Modify: `projects/ide-extension/src/kernel/schema-validation.mjs`
- Modify: `projects/ide-extension/src/server.mjs` for a GET-only projection endpoint and optional allowlisted navigation event endpoint
- Modify: `projects/ide-extension/public/demo/l0.html` only to expose the owned Tower shell safely
- Modify: `projects/ide-extension/package.json` for scoped tests

Required tests:

- `tests/tower-navigator-contracts.test.mjs`: schema, identities, source locks, selectors, allowed events.
- `tests/tower-navigator-read-only.test.mjs`: unchanged source digests and no tower/ontology writes.
- `tests/tower-navigator-failures.test.mjs`: stale, duplicate, missing, changed, hostile label, unsupported interaction, forbidden mutation.
- `tests/e2e/tower-navigator.spec.mjs`: one trusted shell, exact evidence inspection, last-good-view preservation, desktop/mobile reachability.

If strict “no local writes at all” is required, current Canvas publication is the wrong route because it appends an audit event and projection state. A direct GET-rendered witness would be required instead.

```yaml
receipt:
  action_id: spawn-0002
  dispatch_id: 2026-08-07-cyberalchemy-lab-foundation
  run_id: run-001
  wave_id: wave-01-explorers
  role: workbench-explorer
  capability_ref: research
  status: pass
  validation: pass
  blockers: []
  started_at: unavailable
  finished_at: 2026-08-07T20:48:00-03:00
  inspected:
    documents:
      - projects/ide-extension/README.md
      - projects/ide-extension/SPEC.md
      - projects/ide-extension/ARCHITECTURE.md
      - projects/ide-extension/development/session-content-workbench-plan/README.md
      - projects/ide-extension/development/workbench-ui-v1/README.md
      - projects/ide-extension/development/architecture-review-2026-07-10/findings.md
      - projects/ide-extension/development/architecture-review-2026-07-10/audit.md
    selectors:
      - projects/ide-extension/src/server.mjs:createServer, proposalDetail, projectReceiptForUi, /api/state, /api/canvas/*, /api/proposals/*, /api/receipts/*/evidence/*, /api/envelopes/*, /api/approvals/*
      - projects/ide-extension/src/kernel/projector.mjs:createInitialWorkbench, withCanvasState, applyCanvasPublished, applyCanvasInteraction, reduceEvents
      - projects/ide-extension/src/kernel/canvas.mjs:normalizeCanvasPath, readWorkspaceHtml, prepareCanvasPublication, projectCurrentCanvas
      - projects/ide-extension/src/kernel/registry.mjs:loadModuleManifests
      - projects/ide-extension/src/kernel/schema-validation.mjs:SCHEMA_FILES, createSchemaValidators
      - projects/ide-extension/src/ui/run-view.mjs:projectRunView
      - projects/ide-extension/src/ui/run-actions.mjs:resolveRunActions
      - projects/ide-extension/public/demo/l0.html:performCanvasLoad, canvasInteractionRequest, currentRunView, evidence renderer
    schemas:
      - projects/ide-extension/schemas/module-manifest.schema.json
      - projects/ide-extension/schemas/agent-envelope.schema.json
      - projects/ide-extension/schemas/approval-record.schema.json
      - projects/ide-extension/schemas/receipt.schema.json
      - projects/ide-extension/schemas/canvas-publish-request.schema.json
      - projects/ide-extension/schemas/canvas-interaction-request.schema.json
      - projects/ide-extension/schemas/operations-interaction-request.schema.json
    tests:
      - projects/ide-extension/tests/l0-lifecycle.test.mjs
      - projects/ide-extension/tests/l0-runtime-schema-enforcement.test.mjs
      - projects/ide-extension/tests/l0-artifact-evidence.test.mjs
      - projects/ide-extension/tests/session-content-workbench-{contracts,path-admission,publish,interactions,replay}.test.mjs
      - projects/ide-extension/tests/workbench-ui-v1-{run-view,run-actions}.test.mjs
      - projects/ide-extension/tests/e2e/workbench-ui-v1-{canvas,evidence-inspector,actions}.spec.mjs
      - projects/ide-extension/tests/e2e/session-content-workbench-matrix.spec.mjs
  commands_checks:
    - rg/rg --files, wc, sed, nl for bounded read-only inspection
    - sha256sum for current source/schema/test and provisional tower locks
    - node --check on server.mjs, projector.mjs, canvas.mjs, run-view.mjs: pass
    - no Node or Playwright test suite executed because those fixtures write temporary/local state
  residue:
    - Tower Navigator unimplemented
    - tower corpus selection provisional
    - module source refs unresolved to digests/selectors
    - hostile Canvas HTML containment deferred
    - Canvas interactions unauthenticated and globally scoped
    - Workbench UI V1 human usefulness verdict pending
    - no current runtime/browser test execution in this action
  reroute_needs:
    - corpus explorer for final witness tower identity
    - ontology explorer for candidate record/relation semantics
    - later implementation owner for ide-extension adapter
    - human gate before any Workbench UI promotion
  observer_status: not_run
  handoff_note: >
    Synthesize the current IDE substrate as build-from-owned presentation and
    evidence machinery only. Preserve Tower/source/ontology authority outside
    Canvas, define read-only as no domain-source mutation, and retain all named
    negative cases as implementation acceptance tests.
```

<!-- END VERBATIM RETURN: spawn-0002 workbench-explorer -->

<!-- BEGIN VERBATIM RETURN: spawn-0003 ontology-explorer -->

## Candidate ontology-governance result

Verdict: use an authority-record model with regenerable projections. Do not make a graph, Inventory, Ontology Vault, or the workbench the authority substrate.

This is an `authority-governance` map, inferred with high confidence. It defines a candidate contract only; no schema, compiler, ontology, fixture, query graph, or workbench adapter was created or proven.

Classification:

- `BFO` — build from repository-owned concepts.
- `NEW` — net-new candidate specialization for CyberAlchemy Lab.
- `ANALOGY` — external standard constrains the design but does not own local meaning.
- `BLOCKED` — requires another owner or evidence lane.
- `FUTURE` — unnecessary for the first witness.

### Governing separation

```text
immutable source/tower snapshots
  -> selector-bound evidence
  -> candidate knowledge and claims
  -> external owner decision / PromotionRecord
  -> scoped authority artifact, if approved

candidate records
  -> disposable graph/read-model projection
  -> read-only workbench projection
```

Inventory remains discovery and evidence lookup. Ontology records candidate meaning. Validation reports shape or execution evidence. Promotion decisions remain external owner acts. This follows `.arcanum/inventory/entries/ontology-population-from-inventory-synthesis.md#Direct Answer`, `projects/ontology/ARCHITECTURE.md#Artifact Classes`, and `arcanum/development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md#PromotionRecord Boundary`.

## Candidate record families

| Family | Class | Minimum candidate shape and invariant |
|---|---|---|
| `SourceSnapshot` | `BFO` | `logical_source_id`, immutable `snapshot_id`, repo-relative path, media type, byte digest, byte size, capture activity/time, source owner, privacy class, source status, revision/supersession refs. A mutable path is not identity. Based on `ops/development/2026-08-02-tower-exam-learning-graph-review/findings.md#Artifact: provenance and evidence contract`; PROV mapping is `ANALOGY`. |
| `TowerPackageSnapshot` | `NEW` over owned Research Tower packaging | Stable tower logical ID, immutable package snapshot ID, root, ordered artifact manifest with per-file digests, package generation, source cohort/owner, research status, privacy/publication class, missing required artifacts, duplicate/supersession refs, residue. Exact eligibility and tower identity remain `BLOCKED` on the corpus lane. The package contract comes from `dispatch-sheet.json`, writer prompt and `.arcanum/inventory/entries/cyberalchemy-lab-foundation-research-strategy-result-synthesis.md#Research Tower Artifact Contract`. |
| `KnowledgeRecord` | `BFO` | Logical ID, snapshot ID, record kind, owning tower snapshot, owner-supplied local ID or registered sidecar ID, payload, evidence ceiling, status, provenance, anchors, privacy, invalidation conditions. Allowed kinds should initially be only those actually witnessed in the selected tower, such as claim, definition, example, residue, gate, or route—not inferred “topics.” Source: `ops/.../tower-exam-learning-graph-review/findings.md#Artifact: Refine seed and candidate graph model`. |
| `EvidenceAnchor` | `BFO` | Anchor ID, exact `SourceSnapshot`, selector kind/value, closed range where applicable, extraction mode, artifact digest, evidence taxonomy, verification requirement, supported/challenged claim IDs, expiry/invalidation condition. It must fail closed if its selector no longer resolves under the bound digest. Source: tower-exam findings CR-02, CR-06, and CR-08; `.arcanum/inventory/schema.md#Evidence Cards`. |
| `ClaimCandidate` | `BFO` | One explicit statement, claim type, scope/branch hypothesis, evidence anchors, evidence and commitment confidence separately, review owner, candidate status, contradiction/falsification path, expiry, permitted candidate uses, and proposed PromotionRecord. It is the Lab specialization of `OntologyCandidate`, not an already promoted ontology node. Source: `projects/ontology/ARCHITECTURE.md#Node Eligibility` and CAOL `#PromotionRecord Schema`. |
| `DefinitionReference` | `BFO` | Term/reference ID, canonical owner source plus selector and digest, authority scope, referenced version, local usage context, candidate alias if any, and drift status. It references normative definitions; it must not copy or redefine them. Public Arcanum and private CyberAlchemy-v2 definition authorities remain separate. Source: `arcanum/definitions/DEFINITIONS.md#Authority Rule`; `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#Authority Rule`. |
| `BridgeDecisionRecord` | `BFO` | Subject claim/relation, evidence from both required sides, outcome `aligned|partial|drift|insufficient|contradicted`, scope, confidence split, contradiction path, owner, rationale, rejected alternatives, source decision reference, and promotion impact. Until an owner decides, the Lab record is a pending assessment with `authority_effect: none`. Source: `PROMOTION-LIFECYCLE.md#Bridge Validation` and `ONTOLOGY-ARCHITECTURE.md#Review Owner Matrix`. |
| `ResidueRecord` | `BFO` | Subject, residue type, evidence refs, observed/missing state, severity, blocking effect, owner route, privacy, resolution conditions, and terminal resolution reference. Residue is not automatically a defect. Source: `.arcanum/inventory/schema.md#Entry Fields` and `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md#Candidate Kinds`. |
| `ValidationRecord` | `BFO`; SHACL `ANALOGY` | Immutable input digests, profile/shape and validator identity/version, executed command/environment, result, violations, affected subjects, scope, timestamps, and `authority_effect: none`. Conformance is shape evidence, never promotion or implementation proof. Arcanum’s canonical schema boundary states this explicitly in `arcanum/definitions/DEFINITIONS.md#DEF-ARC-SCHEMA`. |
| `WorkbenchProjection` | `NEW` | Projection logical ID and immutable revision ID, generator contract digest, source record/snapshot set, filters, projected nodes/relations, graph digest, read-only flag, privacy filter, session/revision binding supplied by the IDE lane, validation refs, stale/invalidated state, and `authority_effect: none`. It may expose evidence but cannot become its source. |
| `PromotionRecord` plus owner-decision ref | `BFO` | One primary claim only; source inputs, provenance, branch target, status, confidence split, review owner, gate result, use scope, contradiction path, rollback/retirement, route impact, bridge validation, expiry, and external decision reference. Default first-fixture result is `block`. Source: CAOL `#PromotionRecord Schema` and `#PromotionRecord Boundary`; `cyberAlchemy-v2/authority/promotion-policy.md#Promotion Ladder`. |

## Relation invariants

| Relation | Class | Invariant |
|---|---|---|
| `snapshot_of` | `BFO` | Snapshot → logical source/package/record. Many immutable snapshots may specialize one logical identity; path equality does not establish identity. |
| `revision_of` / `supersedes` | `BFO`, PROV `ANALOGY` | Newer snapshot → prior snapshot; owner-asserted and acyclic. Same bytes at two paths are duplicate candidates, not automatically revisions. |
| `package_contains` | `NEW` | Tower package snapshot → knowledge-record snapshot. Both endpoints are frozen; membership never points to mutable “latest.” |
| `anchored_by` | `BFO` | Knowledge/claim → EvidenceAnchor → exactly one SourceSnapshot. The selector must resolve against that snapshot digest. |
| `supports` / `challenges` | `BFO` | EvidenceAnchor → ClaimCandidate. These relations may alter evidence confidence or create residue; they cannot change commitment or promotion state. |
| `references_definition` | `BFO` | Candidate record → DefinitionReference. It cannot imply `defines`, `sameAs`, or semantic equivalence. |
| `derived_from` | `BFO` | Projection/validation → immutable input records and generation activity. Every derived result must be reproducible or explicitly marked non-reproducible residue. |
| `bridge_assessed_by` | `BFO` | Claim/relation → BridgeDecisionRecord. Alignment requires evidence from both sides; `insufficient` and `contradicted` block dependent promotion. |
| `blocked_by` | `BFO` | PromotionRecord → open residue, contradiction, failed validation, privacy gate, or owner gate. It only blocks; it never confers approval. |
| `approved_by` / `promotes_to` | `BFO` | Candidate → owner decision → scoped authority artifact. Only the named owner route may create this edge. |
| `projected_as` | `NEW` | Candidate/snapshot → WorkbenchProjection node. There is no inverse mutation edge from the projection. |
| `invalidated_by` | `BFO`, PROV `ANALOGY` | Snapshot/projection/current-use assertion → identified change or expiry activity. Historical evidence remains preserved; active reliance is withdrawn or revalidated. |

All edge kinds require declared source/target types, cardinality, provenance, and cycle policy. Deterministic edge IDs should hash the predicate, ordered endpoint snapshot IDs, and provenance-anchor IDs. For symmetric `contradicts`, sort endpoints and forbid self-loops. Inverses are computed, not independently authored. These constraints follow `projects/ontologize/DAG-AND-METRICS.md#Edge catalog` and the accepted tower-review CR-03.

## Identity, version, and invalidation

1. `BFO` Logical identity and snapshot identity stay separate.

   - `source_snapshot_id = H(logical_source_id, content_digest)`.
   - `tower_snapshot_id = H(tower_logical_id, canonical ordered artifact manifest)`.
   - `knowledge_snapshot_id = H(record_logical_id, tower_snapshot_id, record-content digest)`.
   - Projection revision = `H(input snapshot set, projection rules, generator contract)`.

2. `BFO` Digest equality does not prove semantic identity. It may indicate a copy; the corpus owner decides duplicate, alternate, revision, or independent package status.

3. `BFO` Where a tower supplies a durable local claim/definition/residue ID, preserve it. Otherwise use an explicit sidecar registry. Do not derive logical identity solely from heading text or list order.

4. `BFO` A changed source creates a new snapshot. The old anchor remains historically accurate but becomes stale for “current” use. Dependent claims are challenged, PromotionRecords become blocked pending review, and active projections are regenerated or invalidated. Do not rewrite history. This matches `projects/ontology/research/2026-06-18-inventory-evolution-efficiency/findings.md#One Update`, `#One Invalidation`, and `#One Projection`.

5. `BFO` Validation records are immutable witnesses. Changing input, validator, shape/profile, or environment makes the prior result stale for the new target; it does not mutate the old result.

6. `BLOCKED` Append-only promotion-event storage is an owner-scoped precedent, not a proven global ontology axiom. The Lab may require it later, but this lane cannot impose it.

## Standards constraints

- `ANALOGY` [W3C PROV-O](https://www.w3.org/TR/prov-o/) supports separating general entities from time/context-specific specializations, representing derivation/revision, and recording generation and invalidation activities. Use these mappings for interchange, but retain local digest, privacy, owner, and promotion gates.
- `ANALOGY` [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) supports stable IRI identity and optional named-graph projections. Blank-node identifiers are local and non-portable, so they must not identify tower records across snapshots. A named graph’s name does not inherently denote its graph; a manifest must say what each graph IRI represents.
- `FUTURE` [SHACL](https://www.w3.org/TR/shacl/) is suitable for structural checks and validation reports. `sh:conforms` means conformance to the supplied shapes, not truth, promotion, runtime behavior, or owner approval.
- `FUTURE` [OWL 2](https://www.w3.org/TR/owl2-syntax/) is warranted only if the project later needs formal class/property axioms, entailment, imports, or interoperable ontology/version IRIs. OWL version IRIs must not be substituted for tower-package versions. OWL is unnecessary for the first fixture.

## Graph-substrate decision

Use JSON/Markdown authority records, indexes, typed sets, forward/reverse adjacency, and a bounded disposable graph projection first. This is `BFO`, not an implemented runtime.

Adopt a primary graph store only after at least one becomes routine and bounded projections are demonstrably inadequate:

- ad hoc multi-hop queries across many relation kinds;
- large transitive invalidation or supersession closure;
- contradiction blocking across many towers or branches;
- dynamic bridge-coverage projections;
- promotion-impact traversal;
- graph analytics such as clustering, motifs, or centrality.

This threshold is owned by `projects/ontology/research/2026-06-18-inventory-evolution-efficiency/findings.md#Graph-First Threshold`. The current strategy explicitly reports that no Lab ontology schema, compiler, query graph, or workbench integration exists.

## Prohibited write edges

All are `BLOCKED`:

- Inventory row/EvidenceSet → ontology node or promotion state.
- Evidence, validation, telemetry, session, or Canvas event → authority or owner decision.
- Ontology candidate → canonical definition, constitution, spec, code, or public Arcanum.
- Workbench projection → source snapshot, candidate record, promotion gate, Git, or external transport.
- Validation success → `approved_by` or `promotes_to`.
- Label, order, path, or digest similarity → `sameAs`, semantic link, consensus, or duplicate resolution.
- One-sided evidence → bridge alignment.
- Private evidence → public Arcanum without boundary scrub and owner review.
- Source change → destructive rewrite of old snapshots or decision history.
- Candidate graph → automatic bulk ingestion, scoring, persona behavior, publication, or deployment.

## One-tower candidate fixture

`NEW`, unimplemented, `authority_effect: none`:

```yaml
fixture_id: cxl-one-tower-001
status: candidate
selected_tower:
  logical_id: BLOCKED_CORPUS_LANE
  snapshot_id: BLOCKED_CORPUS_LANE
  package_manifest_digest: BLOCKED_CORPUS_LANE

records:
  source_snapshots: [at_least_one_digest_bound_source]
  tower_package_snapshots: [exactly_one]
  knowledge_records:
    - one source-backed claim
    - one definition reference
    - one explicit residue or missing-evidence record
  evidence_anchors: [at_least_one_per_claim_or_definition]
  claim_candidates: [exactly_one]
  bridge_decisions:
    - status: insufficient
      reason: "No owner-reviewed cross-surface decision in this fixture."
  validations:
    - schema_conformance: NOT_RUN
    - selector_resolution: NOT_RUN
    - privacy_filter: NOT_RUN
    - relation_integrity: NOT_RUN
  workbench_projections:
    - mode: read-only
      status: candidate
      authority_effect: none
      adapter_binding: BLOCKED_IDE_LANE
  promotion_records:
    - gateResult: block
      reviewOwner: ontology-owner
      useScope: fixture-review-only

required_relations:
  - tower_snapshot package_contains knowledge_record_snapshot
  - knowledge_record anchored_by evidence_anchor
  - evidence_anchor supports claim_candidate
  - claim_candidate references_definition definition_reference
  - projection derived_from all_projected_snapshot_ids
  - promotion_record blocked_by open_residue
```

Required negative cases: changed source digest, missing selector, duplicate path/same content, dangling relation, unsupported record kind, private-source exposure, stale projection revision, validation without bound inputs, and projection-attempted promotion must all fail deterministically.

The corpus lane must supply the exact tower and manifest. The IDE lane must supply the actual read-only adapter/session/revision binding. Until those join, the fixture is concrete in shape but intentionally uninstantiated.

## Compact receipt

```yaml
action_id: spawn-0003
dispatch_id: 2026-08-07-cyberalchemy-lab-foundation
run_id: run-001
wave_id: wave-01-explorers
role: ontology-explorer
capability_ref: research
status: pass
validation: pass
validation_scope: research-source binding and internal boundary consistency only
blockers:
  - exact tower identity and manifest await corpus explorer
  - exact workbench adapter/session/revision fields await IDE explorer
  - owner bridge and promotion decisions remain external
started_at: unavailable
finished_at: 2026-08-07T23:48:11Z
residue:
  - candidate ontology schema/compiler/query graph unbuilt
  - fixture uninstantiated and validation NOT_RUN
  - primary graph substrate unwarranted
  - SHACL and OWL remain future decisions
  - authority_effect_none
reroute_needs:
  - synthesizer join with corpus and IDE receipts
  - later owner decision before implementation or promotion
observer_status: not_emitted_read_only_scope
handoff_note: Reconcile this candidate contract with the exact corpus manifest and current IDE interface; keep PromotionRecord blocked until both bindings and an owner decision exist.
```

Inspected repository evidence:

- `.agents/skills/ontology-vault/SKILL.md`; `catalogs/ontology-types.json`.
- CyberAlchemy Lab `dispatch-sheet.json` and `strategy-inventory-packet.json`; dispatch SHA-256 `94372866…fda64`, packet SHA-256 `969160b8…cfa7`.
- `.arcanum/inventory/entries/ontology-population-from-inventory-synthesis.md` and both named EvidenceSets plus their selected evidence cards.
- `.arcanum/inventory/schema.md`; both `.arcanum/ontology-vault/map-*` files.
- `projects/ontology/ARCHITECTURE.md` and the two materialization/substrate findings.
- `ops/development/2026-08-02-tower-exam-learning-graph-review/findings.md`.
- CAOL `ONTOLOGY-ARCHITECTURE.md` and `PROMOTION-LIFECYCLE.md`.
- `projects/ontologize/DAG-AND-METRICS.md`.
- Arcanum and CyberAlchemy-v2 definition/authority owner files, `SOURCE-MAP.md`, `AUTHORITY-KINDS.md`, and `promotion-policy.md`.
- Official primary URLs: PROV-O, RDF 1.1 Concepts, SHACL, and OWL 2 linked above.

Checks run: bounded `rg` discovery/selectors, line-numbered source inspection, JSON `jq -e` binding checks, and SHA-256 verification. No files were mutated.

<!-- END VERBATIM RETURN: spawn-0003 ontology-explorer -->
