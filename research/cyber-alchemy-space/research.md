---
tags: [cyber-alchemy-space, architecture, research, raw-returns]
node_type: research
is_session: false
layer: architecture
nature: reference
status: draft
created: 2026-06-16
dispatch_id: 2026-06-16-cyber-alchemy-space-architecture
dispatch_type: research
working_folder: research/cyber-alchemy-space/
---

# Research — Cyber-Alchemy-Space (collected returns)

Raw returns for dispatch `2026-06-16-cyber-alchemy-space-architecture`. Groups: explorers (4) →
synthesizer (1, zig-zag turn 1 + turn-2 revision) ↔ reviewers (3 skeptics) → coverage-audit. The
synthesis lives in [findings.md](findings.md); this file is the evidence trail.

---

## Explorers (Wave 1)

### E1 — Arcanum (engine/method), source-corpus axis
- Method tiers (each subdir IS a sigil): `formulae/` (deterministic: dispatch-spec, observability-setup), `transmutations/` (context-builder, feature-glossary, implementation-layering), `arcana/` (orchestration: inventory, ontology-vault, craft, constitution-governance, decision-gate, distill, residuality-spec, robot-talks, scope-interview, task-session, signal-observer, workflow-reflect, x-ray…), `spells/` (compositions).
- LAW SPINE = `framework/`: CYBERALCHEMY-METHOD.md (13-step Orient→Discover→Shape→Stabilize→Evolve), ARTIFACT-CONSTITUTION.md (4 classes Source/Durable-Evidence/Generated/Local-Runtime + 7 rules), ARTIFACT-METADATA-CONSTITUTION.md, SCHEMA-CONSTITUTION.md, MARKDOWN-LINKING-CONSTITUTION.md, QUALITY-BAR.md.
- SUBSTRATE CHAIN (owned spine): inventory (.arcanum/inventory/) → ontology-vault (branch-aware business/system) → context-builder; composed by `spells/ontology-harness`, `spells/repository-harness`.
- BUSINESS-ONTOLOGY.md = 3-layer: Business (intent) / System (realization) / Bridge (traceability) + Axioms/Constitutions/Premises/dual-signal Confidence, Via-Negativa threshold, tree-based policy resolution.
- disciplines/DISCIPLINES.md = 19 practices w/ steward + maturity; Growth Rule: evidence RECOMMENDS, cannot directly PROMOTE registry/ontology/glossary/sigil knowledge (hard boundary).
- TWO-LANE evidence: craft (.craft/ledger.yml machine + CRAFT.md human + index.json). Sigil on-disk grammar: README.md (human) + SKILL.md (executable) + templates/ + development/ (lifecycle trace).
- Arcanum-specific (NOT portable): spellcraft/sigil-development/skill-transcriptor/skill-decomposer/sigil-runtime-installer, necronomicon, arcanum-bootstrap, Codex-bound profiles.
- E1 self-flagged its engine-spine bias + 3 contested forks: capability index (Arcanum) vs project/domain catalog (domainspec sync-registry/feature-glossary) vs contested sigils (audit-alignment, code-tag-audit, test-derivation overlap domainspec).

### E2 — domainspec (law/enum), source-corpus axis
- LAW: CONSTITUTION.md (executable C1–C11, each binds axiom + gate), AXIOMS.md (A1–A6, Via-Negativa), AUTHORITY-MAP.md (tie-breaker: which artifact wins; single-file vs multi-file-pack canonicalization), GOVERNANCE-ATTENUATION.md (meta-law: governance layers erode fidelity; observer≠executor / Conant-Ashby).
- SECOND law surface: `vault/constitution/` (research-, frontmatter-ownership-, edge-acyclicity-, governs-runtime-witness-, subagents-strategy-) — NOT subsumed by root CONSTITUTION.
- ONTOLOGY/TYPES: TAXONOMY.md + RELATIONSHIPS.md (29 edges) + `vault/ontology-conventions.md` v2.3.0 (THE normative node-taxonomy + confidence + forbidden-edge matrix — what the view skills resolve against). Count drift: TAXONOMY "25" vs ATTENUATION "24"; RELATIONSHIPS "29" vs "26".
- LIFECYCLE: ADLC-ALIGNMENT.md (L0–L7). View triad skills: ontology-view (typed-graph floor, forbidden-edge unconstructibility), system-view (shape, names stances decides none), engineer-view (verdict lane RESOLVED/OPEN/CRITICAL + authority verified on disk), paired-views (single-owner invariant). Pipeline: domainspec-pipeline.
- TWO-LANE doctrine (GOVERNANCE-ATTENUATION §Structural Signal Detection): artifact-level gaps → deterministic computation; behavior-level events → independent observer over telemetry. Machine = SIGNAL-SCHEMA.md + pipeline-signals.jsonl + @biz/@sys anchors; human = veracidade/convicção frontmatter. NO SCHEMA-INVENTORY.md (signal schema is de-facto machine schema).
- E2 flagged: TWO prescribed lifecycles coexist (ADLC vs discovery→view-triad; the views already emit via domainspec-emit-signals). Signal emission empirically ~30–40% of expected. C-rule gates = prescribed obligation, not witnessed. Catalog duplication outruns AUTHORITY-MAP.

### E3 — domainspec-core projects (on-disk reality), source-corpus axis
- ONTOLOGIZE: ONTOLOGY-BRANCHES.md (B1/B2/B3/B4 + bridge edges; drifts_from≠contradicts). DELIVERY-LANES.md (Lane A/B/Hybrid "←usual"; Lane B [H] HARD GAP "no native sigil" for L-reg + 5 bridges, 2 NET-NEW). view-triad-method/BRANCH-MATERIALIZATION.md (Branch Materialization Register + Branch-To-View Matrix; FORBIDS a 4th branch-view). NEWER 2026-06-15 runs reverse direction: branch-as-view (ontology IS the tree; "ontology-view should NOT be a sibling"). clients/hellbender (triad really applied; confidence in receipts NOT frontmatter; refuses promoted-belief altitude).
- GOLDENQUILL: CRAFT.md + .craft/ledger.yml two-lane in real use; BUT GAP-DESIGNED-NOT-BUILT (learning loop designed, humans edit by hand), schema candidate-local, count drift (47v44, 13v12).
- FRAMEWORK-UNIFICATION: ARTIFACTS.md (4 tiers A/B/C/D + 3 planes M2/M1/M0); CONCEPT-MAP.md (pipeline×mechanism axes, node envelope, 10 invariants tagged Enforced-today?). ALREADY red-teamed on disk: F1 CRITICAL paired-views producers are tier-D not pipeline; F2 problem-statement root doesn't exist.
- DISPATCH CHAIN: router→type-skill→form; LIVE research/review/experiment, RESERVED code/plan/suggestion; enforcement is NUDGE-NOT-GATE, fail-open; .claude/skills is a generated copy (back-port drift).
- CYBERALCHEMY/: agentic-system slices 00-07; SOURCE of B3 naming collision ("Operational Ontology" = agent-operation ≠ run-context); only 1 promoted ontology entry on disk.
- E3 through-line: the prescribed model is consistently AHEAD of what real projects run — documented on disk by the projects themselves.

### E4 — cross-cutting convention mining, methodology axis
- **CRITICAL caveat:** core EMBEDS Arcanum + domainspec as submodules → a hit under core/arcanum or core/implementation/domainspec is NOT independent evidence. Real authors = Arcanum (engine) / domainspec (constitution+enum) / core's own tree.
- Two-lane: SHARED-DISCIPLINE as principle; PAROCHIAL as the CRAFT file pairing (core projects only; Arcanum vends the schema; domainspec instantiates as TAXONOMY→DEFINITIONS).
- `development/` context dir: SHARED-DISCIPLINE (all three; WORK-PACK/CONTEXT-PACK/SOURCE-PACK/REFINE-SEED→RESULT set).
- Frontmatter: PARTIAL; authority SPLIT — metadata-shape constitution = Arcanum; node-type+confidence enum = domainspec `vault/ontology-conventions.md` v2.3.0 (Arcanum borrows it cross-repo).
- Machine indexes: telemetry/dispatch YAML+JSONL = SHARED universal; code-tags.json + ledger indexes = parochial (tooling universal, committed instances not).
- Typed-graph ontology: SHARED one lineage; METHOD home = Arcanum, CONSTITUTION home = domainspec; authority asymmetry + cross-repo dependency.
- Artifact-catalog tiers: PARTIAL; two label schemes (Arcanum Source/Durable/Generated/Local-Runtime vs core A/B/C/D), same stratify-by-lifecycle intent; core's A/B/C/D is a fresh synthesis.

---

## Reviewers (zig-zag turn 1)

### S1 — precedent gate
- Block 1 SPACE MODEL → build-from-owned, SURVIVES.
- Block 2 PER-CONTEXT → branch substrate (B1–B4) + view-triad-method = build-from-owned; **five-view branch-as-view reframing = novel-attempt** (RESULT.md: "Runtime-backed refine stages have not run"; it proposes FOUR views meaning/engineer/run/residue, not five; BRANCH-MATERIALIZATION forbids a standalone branch-view; hellbender uses the prior triad).
- Block 3 TWO-LANE → build-from-owned, SURVIVES.
- Block 4 2-D CATALOG → **novel-attempt** (no on-disk owner for the cross-product).
- Block 5 GOVERNANCE → build-from-owned, SURVIVES.
- Block 6 AUTHORITY RULE → single-owner principle build-from-owned; the path/git/VERSION resolution **algorithm is novel-attempt — NOT in AUTHORITY-MAP** (grep returned no matches).

### S2 — non-vacuity gate (hellbender witness)
- 3/5 views map by rename/move (B1→meaning-view rename, B2 system-view, B2-verdict engineer-view). SUMMARY/RESEARCH-STRATEGY = source corpus; README = index (not views).
- **B3 run-view = HARD NEGATIVE:** hellbender has 0 code, 0 pilot (engineer-view D4/D6 CRITICAL, D2/D3/D5/D7 OPEN). Only run-trace = the research fanout (run-context of producing the doc, not the subject system); filling run-view from it commits a forbidden edge. No producer skill.
- **B4 residue-view = SOFT gap:** residue exists embedded in ontology-view (R1–R4) + engineer-view (R1–R6); standalone file conflicts with single-owner.
- Two-lane largely UNMET: only `dispatch.json` is machine-only; views ship mermaid/prose, no paired machine artifact.
- **2-D catalog does NOT partition:** `receipts.md` dual-classed (Source+Runtime); `dispatch.json` triple-classed (Source+Durable+Runtime).

### S3 — definitional-soundness gate
- (a) "cyber-alchemy-space" → RE-SKIN of "the private umbrella parent repo" unless branch-as-view lands.
- (b) "branch-as-view" → RE-SKIN of the triad + ontology-folder; rename ontology-view→meaning-view strands the skill's forbidden-edge differentiator; bijection ≈ Business/System/Bridge relabeled; **run-view is a legit NET-NEW gap-name but not yet an object (carry as OQ).**
- (c) 2-D catalog → RE-SKIN (inert grid; no new validator check).
- (d) "spec feeds system-view⇄engineer-view" → DODGE; **inverts the built pipeline order** (views precede spec). Honest answer: **spec ≠ system-view**; spec ≈ engineer-view's schemas.
- (e) "orthogonal lifecycles" → RE-SKIN/post-hoc; the 5-verb loop appears NOWHERE; the real thesis is **recursive self-application (I9)**; loops are COUPLED (shared signal stream), not orthogonal.

---

## Synthesizer (zig-zag turn 2 — accepted all corrections)

The writer revised to accept every skeptic objection: fixed the 4-vs-5 view miscount; demoted branch-as-view to an UNRUN proposal / OPEN owner-decision (OD-1); answered spec ≠ system-view (OD-6); reframed run-view as a gap (OD-2); residue embedded-vs-extracted as a choice (OD-3); 2-D catalog as two independent axes needing a primary-class rule (OD-4, novel); authority algorithm as a PROPOSED extension not in AUTHORITY-MAP (OD-5); dropped "orthogonal lifecycles" for I9 + tier-A/tier-B. Convergence reached (no remaining dissent). Final architecture in [findings.md](findings.md).
