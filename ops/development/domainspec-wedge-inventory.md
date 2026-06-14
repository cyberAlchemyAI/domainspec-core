# DomainSpec → Arcanum Wedge Inventory

Dispatch: `domainspec-wedge-inventory-20260614` · Generated: 2026-06-14
Decision Q1 (recorded): **domainspec stays private; only the free wedge is exported to public arcanum.** "Going public" = export to arcanum only what arcanum will use.
Method: 3 parallel inventory subagents over disjoint partitions (knowledge/governance · sigils/tools/Craft · runtime/spec-test/Lean), grounded in `COMMERCIALIZATION-SYNTHESIS.md` + the integration README. **Evidence only — nothing moved, nothing promoted.**

---

## Headline findings (these change prior assumptions)

1. **A deterministic spec→test ENGINE exists** — `tools/test-derivation-engine/` (`src/index.ts`: *"No LLM, no network: determinism by construction"*). This **refutes the README's R1** ("spec→test is LLM-driven") *and* refutes my earlier in-session claim that no engine exists. The engine is real and deterministic → **wedge-eligible**, not moat. Seam 2 reframes from "method-only" to "method + a deterministic engine that can also export."
2. **The sigil parity diff (the biggest unknown) is resolved — and most of the wedge is already public.** Craft (`arcanum/arcana/craft`, schema-only), experiment-harness, observability-setup/signal-observer/workflow-reflect, necronomicon, and ~30 sigils/spells already live in arcanum. domainspec's `.codex/commands/arcanum-sigil-*` are **legacy install copies of already-public sigils** — reconcile, do not re-lift.
3. **Genuine NEW wedge lift candidates are narrow and concrete** (no arcanum equivalent): the **code-tag extraction tool + schema + composability/drift checkers**, and the **taxonomy/relationships/definitions vocabulary** (DS-D1/D2 wedge subset). That's essentially it.
4. **Lean is a separate submodule, not inside domainspec.** `domainspec-lean-formalization/` sits at the umbrella root (~191 project `.lean` files); mostly moat (FF-threshold/attestation/bridge-functor). A few generic concepts are wedge-candidates pending seam-3. Only Lean *inside* domainspec is `internal_tools/lean-code-validator/` (8 example files, moat).
5. **Host trees confirmed generated** — `copilot/install.sh` and `tools/bootstrap_domainspec_codex.sh` generate `.github`, `.codex`, `.agents`. Seam-4 evidence points to **regenerate via arcanum-bootstrap, not hand-migrate.**

**Net effect:** the merge is much smaller than the punch list implied. The wedge that *isn't already public* is roughly **two clusters** (code-tag tooling, taxonomy/definitions vocabulary) plus **one reframed decision** (the deterministic test engine).

---

## A. EXPORT — genuine wedge, not yet in arcanum

| Item | Path | Why wedge | Effort | Conf |
|---|---|---|---|---|
| Code-tag **extraction tool** + language adapters (js/ts/py) | `governance/tags/tools/extract-code-tags.ts`, `lib/code-tag-adapters/` | §2 "code-tag extraction"; language-agnostic, no DS-domain coupling | decouple default paths | high |
| Code-tag **schema / data model** | `governance/tags/CODE-TAG-SCHEMA.{json,md}`, `lib/code-tag-types.ts`, `code-tag-rules.ts` | The extraction method's contract; generic tag type system | clean | high |
| Code-tag **composability checker** | `governance/tags/tools/check-code-tag-composability.ts` | Zero DS coupling; generic validator (§2) | clean | high |
| Code-tag **drift comparator** | `governance/tags/tools/compare-code-tag-drift.ts` | ~1 DS ref (report path); generic audit (§2) | clean | high |
| **TAXONOMY.md** (25 meta-types) | `implementation/domainspec/TAXONOMY.md` | §2 taxonomy is wedge; arcanum has none | clean | high |
| **RELATIONSHIPS.md** (29 edges, adopted profile) | `implementation/domainspec/RELATIONSHIPS.md` | §2; DS-D2/D7/D8 wedge | clean | high |
| **TEST-PIPELINE.md** (deterministic doc→test rules) | `implementation/domainspec/TEST-PIPELINE.md` | §2 spec→test method; no engine/Lean/governance coupling | clean | high |

> All code-tag tools are wired into the parent `drift-check.yml` via `pnpm run check:code-tags` and default to DS paths — **decouple default paths + DS waiver/registry binding before lift** (residue #6).

## B. PRIVATE — moat (stays in domainspec / lean submodule)

| Item | Path | Why private |
|---|---|---|
| CyberAlchemy governance-attenuation thesis | `GOVERNANCE-ATTENUATION.md`, `ADLC-ALIGNMENT.md`, `TUNING-LOOP.md` | §3 lead paid asset (promotion DAG + KPI taxonomy) |
| DEFINITIONS.md **moat cluster** | DS-C3, DS-D9, DS-COR-1, DS-F1, DS-F5, DS-F6, DS-M13 | CyberAlchemy material (Part C) |
| Craft automation/metering strategy | `development/refinement-runs/2026-06-08-craft-*` | §3/§4 the paid meter + enforcement runtime |
| `validate-governance-chain.ts`, signal/tuning validators, telemetry/observer tools | `tools/` | DS-F1 chain + tuning loop muscle; CI-wired runtime |
| Lean **attestation half** (FF-threshold, faithful-not-full, bridge functor) | `domainspec-lean-formalization/` (BridgeFFRegimeAnalysis.lean, LEAN-PR-BRIDGE-FUNCTOR.md) | §3/§9 g05 — the formal-proof moat |
| Lean **refuted claims** (C_ω_absorption_refuted, Lawvere-impossibility) | `domainspec-lean-formalization/NOVEL-MAPPINGS.md` T7/R4 | do-not-lift refuted-as-settled |
| `lean-code-validator` (spec-richness checker) | `implementation/domainspec/internal_tools/lean-code-validator/` | formal-proof half |
| Product runtime | `backend/`, `apps/`, `internal_tools/`, `infra/`, `implementation/`, `scripts/`, `templates/`, `starter/`, `Codex/` | §RUNTIME — product/infra |
| GOVERNANCE-ATTENUATION-EXECUTION-BOARD, AUTHORITY-MAP, AGENTS, TOBANOV, PHASED-PLAN, INFRA-SETUP | root docs | DS-internal program/build/navigation |
| Project vault content | `vault/discovery,sessions,premise,bets,amendments,…` | private knowledge graph (only the *grammar* is wedge) |

## C. ALREADY IN ARCANUM — reconcile, do NOT re-lift (parity)

| Item | domainspec location | public home |
|---|---|---|
| Craft (schema-only, no automation) | (promoted already) | `arcanum/arcana/craft` |
| ~30 sigils/spells as Codex adapters | `.codex/commands/arcanum-sigil-*`, `arcanum-spell-*` | `arcanum/arcana/*`, `arcanum/spells/*` |
| experiment-harness | `development/arcanum-integration/arcana/experiment-harness` (may have diverged) | `arcanum/arcana/experiment-harness` |
| Observability method | `framework/observability/`, `.arcanum/observability/` (instance state) | `arcanum/formulae/observability-setup`, `spells/observed-invocation-loop` |
| Necronomicon | `.arcanum/necronomicon/` (instance state) | `arcanum/spells/necronomicon` |

## D. NEEDS-DECISION — seams the data narrowed but did not close

| Seam | Decision needed | What the data now says |
|---|---|---|
| **seam-2-spectest** | Export the **deterministic test-derivation-engine** itself, or only TEST-PIPELINE.md? | Engine is deterministic (not LLM, not Lean) → wedge-eligible. R1's "LLM engine" premise is refuted. Lean toward export. |
| **defs-split** | Split DEFINITIONS.md at wedge/moat seam; classify ambiguous DS-D4/D5/D6 | Wedge subset clean; D6 trends governance. Lift wedge subset **by reference**, not copy (avoid 3rd source of truth). |
| **canonical-home** | One public home for taxonomy | DS has 2 sources (TAXONOMY.md + DS-D1), arcanum 0. Recommend DS-D1/D2 canonical, prose as example layer. |
| **seam-5-constitution** | CONSTITUTION.md / AXIOMS.md / vault constitutions | Table shape + A1-A6 vocab = wedge; populated C-rules name hardcoded CI validators = regenerate-via-template. Sanitize "ZefraHub"/Portuguese terms first. |
| **seam-3-lean** | Which Lean concepts are generic wedge vs attestation mechanism | Wedge-candidates: typed residue, declared-scope stopping (C7), subset rule, regimes-of-residue. Moat: FF-threshold/bridge-functor. Refuted: do-not-lift. |
| **seam-4-hosttrees** | Regenerate vs migrate | Generators confirmed (`copilot/install.sh`, `bootstrap_domainspec_codex.sh`) → **regenerate**. |
| **vault parity** | Re-lift vault conventions/constitutions, or treat arcanum ontology-vault/constitution-governance as the home? | Equivalent skills already public; likely reconcile not re-lift. Edge-vocab may collide. |
| **`validate-code-tags.ts`** | Split generic validation from DS-registry cross-checks | 15 DS refs; the generic half is wedge, registry binding is runtime. |

## Collisions to guard on lift
`schema` (arcanum `DEF-ARC-SCHEMA` vs Lean/Spivak `schema`), `contract` (`DEF-ARC-CONTRACT`), `constitution`/node_type vocab, and every `craft` / `experiment-harness` / `arcanum-sigil-*` name (already public). Mint new IDs; add boundary notes.

## Do-not-lift flags
- The proposed **~38-edge / 7-category** taxonomy extension (DS-D2 marks it *proposed, not adopted*).
- Lean **refuted claims** (NOVEL-MAPPINGS T7 `refuted-positive`, R4, Lawvere-impossibility).
- Stale project strings (`ZefraHub`) and Portuguese confidence terms (`veracidade`/`convicção`) — sanitize first.

---

## Gate results
- **g-classification-evidence:** PASS — every row carries reason + confidence.
- **g-moat-protection:** PASS — no moat/runtime item marked export.
- **g-no-promotion:** PASS — evidence only; nothing moved.

---

# Capability-Delta Harvest (agents/skills bodies, not name-parity)

Second pass: 3 agents read the actual `SKILL.md` bodies of domainspec-native skills (+ `ontology-view`, the test engine) and compared **capability**, not names. `gsd-*` excluded by scope. This answers "what does DS *do* that arcanum can't — to improve a sigil or make a new one?"

## NEW capabilities arcanum lacks (wedge — strongest harvest)

| Capability | Source | Why new / wedge | Effort | Conf |
|---|---|---|---|---|
| **Deterministic test-derivation engine** | `tools/test-derivation-engine/` | No-LLM spec→test compiler: typed graph → pure δ rule fn with exact cardinalities → `sha1` obligation keys → byte-stable TEST-SPEC + round-trip oracle. Arcanum has nothing. | decouple (vocab/rules → profile) | high |
| **Code-tag traceability toolchain** | `governance/tags/tools/*.ts` (44KB) | Deterministic code↔spec drift linter (extract→validate→drift→composability, BLOCK on critical). §2 audits = commodity wedge. | decouple paths | high |
| **doc→metrics derivation rules (O1–O16)** | `OBSERVABILITY.md` | Each behavior clause → typed observable obligation + 3-layer fidelity/health/effectiveness model. Runtime stays private; the *rule method* is generic. New sigil. | decouple | high |
| **brownfield-translation** | `domainspec-brownfield-translation` | Reverse code+docs → as-is spec; observed/stated/hypothesized labels; placeholder-satisfies-gate-but-needs-human-promotion. Arcanum cannot reverse impl→spec. | M | high |
| **audit-alignment** | `domainspec-audit-alignment` | Spec-vs-impl fidelity audit: compliant/partial/missing/extra + remediation. Governance-free. | decouple | high |
| **ontology-view** | `ontology-view` | Forbidden edges **unconstructible-by-type** + reflexive predicate guards + live-edge count w/ mismatch surfacing. Vault only asserts in prose. | decouple (strip telemetry) | high |
| **sync-user-stories** | `domainspec-sync-user-stories` | spec→story with mandatory slice taxonomy + concept-coverage matrix flagging unmapped concepts. | decouple | med |
| **delegation-adapter** (phase-bridge pattern) | `domainspec-*-phase-bridge` | Wrap an external orchestrator, normalize its output back to your concept IDs, apply authority-precedence ladder, own the verdict. dispatch-spec validates route shape; this normalizes *results*. | M | med |

## IMPROVE existing arcanum sigils (wedge)

| Arcanum sigil | Harvest from DS | The delta |
|---|---|---|
| **interrogation** ⭐ | `domainspec-interview-kits` | arcanum's interrogation ships an *empty* mode contract; DS has a 4-mode registry + auto-select + Robot-Talks 3-perspective tension synthesis (impact×reversibility×uncertainty, "surfaced not averaged"). Fills a hollow sigil. |
| **dispatch-spec** ⭐ | `domainspec-subagents-strategy` | R29 anti-bias pairwise-tension validator (reject false-consensus) + parametrized dispatch-shape schema + role-ordering invariant. |
| **workflow-reflect** | `domainspec-reflect` | Named cross-run thresholds TH1–TH8 + report-over-report trend comparison + pruning-candidate detection. |
| **context-builder** | `domainspec-context-builder` | Numeric relevance scoring formula + `noiseRatio ≤ 0.15` gate. |
| **definitions-governance** | `domainspec-sync-registry` | Concept-graph-edge + meta-type registry aggregation from per-feature spec tables. |
| **orchestrate** | `domainspec-orchestrate` | Planner-first fail-closed mutation gate + subagent-per-stage capture-before-advance + terminal-resilience (stuck-recovery) policy. |
| **implementation-layering** | `domainspec-audit-layering` | Adds the missing *drift-audit* counterpart (forward layering + drift audit = closed loop). |
| **observed-invocation-loop** | `domainspec-emit-signals` | Per-session epilogue contract + completeness invariants (if step-verdict → exactly one overhead signal). |

## INVERSE finding — do NOT harvest (arcanum already the superset)
For **feature-glossary, definitions-governance, decision-gate, scope-interview**, arcanum is already the *more general* sigil (richer taxonomies, output-contracts, anti-patterns); the DS surplus is pure moat (planner gates, WORK-PACK backfill, pilot checklists, hardcoded paths). Harvest would flow arcanum→DS, not DS→arcanum. **Don't re-lift these.**

## KEEP PRIVATE (moat / product runtime)
`instrument-otel`, `infra-architecture`, `ui-architecture`, `ui-pipeline`, `domainspec-pipeline` (whole — it *is* the product runtime), `pilot-readiness`. Harvest only thin patterns where noted (flag-propagation + binding-gate from pipeline; profile-escalation from readiness-gate).

## Design decision (recorded 2026-06-14): spec-write via DomainSpec template
**Added to build set by operator.** invoke's `define` mode adopts the **DomainSpec SPEC + aspect-doc template** (`implementation/domainspec/templates/SPEC.md` + `operations/queries/interfaces/states/events/mappings.md`), **substituting the Module Formulae** family (`arcanum/spells/invoke/templates/module-formulae/`). Plus the harvested discovery-existence soft gate (with `--skip-discovery` waiver writeback).
- **Rationale:** the DomainSpec template is the shared input the rest of the wedge consumes (test-derivation, doc→metrics O1–O16, sync-registry, sync-user-stories all read aspect docs / Concept Registry; Module Formulae feeds none). It's the keystone, not a cosmetic rename.
- **Nature:** format *replacement* (different decomposition), not a rename. "DomainSpec" becomes the template/brand name in public arcanum.
- **Coupling:** light — "Module Formulae" only in dev/craft docs + invoke SKILL/`define.md` text + runtime logs; no validator keys off it. Touches `templates/` + invoke contract text.
- **Branding implication (confirm):** DomainSpec becomes the public methodology name in arcanum; repo + CyberAlchemy stay private.
- **Pre-lift sanitization:** check the SPEC/aspect templates for DS-private paths/agent-ids before they become the public invoke default.
- **Scope decision (resolved 2026-06-14): FULL REPLACEMENT.** Remove `module-formulae/`; the DomainSpec SPEC + aspect-doc template becomes invoke's only `define` baseline. All define runs emit DomainSpec-format specs. Module Formulae's record/value-type/enum modeling is intentionally dropped. Migration note: update invoke SKILL.md + `define.md` contract text that names "Module Formulae baseline."

## Caveats flagged by agents
- The test-derivation engine is an **L0 skeleton** — `keys/roundtrip/emit/ir` implemented + tested, but `derive()`/grammar parser/`parseCommittedSpec` are stubs. You'd lift the architecture + determinism primitives, not a finished compiler.
- ontology-view's two strongest mechanisms (version+path constitution resolution, live-edge count) are **transfer-asserted, not yet witnessed on disk** (the one GoldenQuill example is a counter-example).
- DS interview `readiness-gate`/`audit-gap` modes are **registry-only stubs** (no MODES/ file).
- The LLM-orchestrated DS skills delegate real logic to `agent:`-referenced agent bodies that were **not read** — capability-class calls are sound, internals are not fully verified.
