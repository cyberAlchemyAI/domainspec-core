# Revised synthesis — Typed Coordinated Work Atlas

## Status and claim ceiling

The recommendation remains one primary explanatory architecture: a **typed coordinated Work Atlas**.

Its landing surface is **Structure**. **Flow** and **Ownership/Proof** are synchronized lenses over the same selected identity, while one shared **Inspector** exposes source, owner, evidence stage, forbidden inference, and claim ceiling. `Source/Text` is an outline/table equivalent feeding that Inspector, not a fourth semantic truth.

This is a research recommendation over frozen proposal-only sources. It is not an implementation, runtime observation, browser result, accessibility result, human-comprehension result, publication, promotion, authority grant, or production claim.

## Repair matrix

| Required repair | Revised location | Exact binding |
|---|---|---|
| Persistent learner-facing Work answer | §4 “Persistent Work card”; wireframe | `DESIGN.md:87-220`; `ONTOLOGY.md:63-90`; C4-inspired decomposition source `E1` |
| Retry exhaustion counterfactual | §8 scenario C, steps C-X1/C-X2 | `DESIGN.md:210-215,376-377,385-399`; `ONTOLOGY.md:87-90,125-126,201-205`; BPMN visualization precedent `E3` |
| Persistent minimal legend | §3 wireframe and legend; §12 MVP | `DESIGN.md:19-32,87-330`; `ONTOLOGY.md:63-187`; `E1,E4,E8` |
| Explicit journal-acceptance disposition | §3 legend; §7 element atlas; all scenario traces | `DESIGN.md:222-330,385-399`; `ONTOLOGY.md:91-100,123-126,160-166,172-187`; `E4` as visualization precedent only |
| Source precedence without collapse | §2 source contract; §11 removable-projection contract | `DESIGN.md:19-32,430-460`; `ONTOLOGY.md:21-40,269-327`; coordinated-view precedent `E6` |
| Textual kind/owner labels; split effect boundary | §3 legend; §7 atlas; §8 traces | `DESIGN.md:70-85,222-302,368-381`; `ONTOLOGY.md:101-108,127-130,167-187`; `E8` |
| External-pattern wording guard | §1 source keys; §5 comparison; §14 dispositions | `DESIGN.md:87-330`; `ONTOLOGY.md:63-187`; `E1,E3,E4` |

## 1. Frozen source and external evidence keys

- `D` = `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/DESIGN.md`, SHA-256 `28b6fca81693a5c6bd10dbe2e74df816312d9e1955e076c950eacd49a86a9419`
- `O` = `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/ontology/ONTOLOGY.md`, SHA-256 `1c6d417c4f0cdfc73c7c42f016c05fd6f8fbccd738a35bf7454472d3cee3b920`

Direct external sources:

- `E1`: [C4 notation](https://c4model.com/diagrams/notation) — decomposition, explicit labels, legends, and zoom discipline only; no RWO semantics or interactive-zoom claim.
- `E2`: [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1) — definition/instance and interaction notation precedent only.
- `E3`: [OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2) — gateway/branch/join/repetition visualization precedent only; no BPMN conformance or imported token semantics.
- `E4`: [OpenTelemetry trace API](https://opentelemetry.io/docs/specs/otel/trace/api/), [messaging spans](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/), and [Lamport’s ordering paper](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/) — occurrence-link and partial-order visualization precedents only; they neither define RWO causation nor prove delivery, replay, or runtime behavior.
- `E5`: [Shneiderman, The Eyes Have It](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf)
- `E6`: [North and Shneiderman, Snap-Together Visualization](https://www.cs.umd.edu/users/ben/papers/North2000Snapa.pdf)
- `E7`: [Tversky, Morrison and Betrancourt, Animation: Can It Facilitate?](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)
- `E8`: [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [ARIA tree-view pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/)
- `E9`: [The Open Group ArchiMate overview](https://www.opengroup.org/archimate-forum/archimate-overview)
- `E10`: [Mayer’s Segmenting Principle](https://www.cambridge.org/core/books/abs/multimedia-learning/segmenting-principle/37240877DDA0362355ADB39936027982)

External evidence informs the proposed notation and interaction grammar. It does not transfer implementation, accessibility, comprehension, conformance, or authority evidence.

## 2. Source precedence without semantic collapse

The view contract has a strict three-level source chain:

1. **`DESIGN.md` is the primary proposal source.** It owns the proposed architecture meanings, distinctions, invariants, and open questions.
2. **`ONTOLOGY.md` is the candidate, non-promoting structured mapping derived from the design.** It supplies local IDs, typed properties, relations, shields, profiles, findings, and residue, but cannot silently override or promote the design.
3. **Learner, navigation, scenario, layout, focus, and highlight records are removable projections.** They may explain or navigate source meaning but cannot create or change it.

If design and ontology conflict, the view displays both selectors and records the conflict as open residue. It does not silently choose the ontology, merge the meanings, or manufacture a repaired semantic record.

`[D:19-32,430-460; O:21-40,172-187,255-327; E6]`

## 3. Primary architecture, wireframe, and persistent legend

```text
┌ PROPOSAL ONLY · no runtime, authority, promotion, or comprehension proof ┐
│ WORK CARD: uniform typed executable boundary; pipeline is also Work      │
│ Root authority: exactly one OrchestratorKernel                          │
├ Structure (primary) ─ Flow ─ Ownership/Proof ─ Source outline/table     ┤
│ semantic outline │ focused definition graph/run plan │ shared Inspector │
│ KIND + OWNER text │ stable source/occurrence IDs       │ source · stage  │
├ Illustrative paper-trace stepper + immutable transcript                 ┤
├ Persistent legend ──────────────────────────────────────────────────────┤
│ ENTITIES │ RELATIONS │ LANES │ STATES │ CLAIM CEILING │ FORBIDDEN       │
└ Invariants · source conflicts · unsupported evidence · open residue     ┘
```

The legend is always available in every lens and in static exports.

### Persistent minimal legend

| Class | Required textual vocabulary |
|---|---|
| Entities | `KIND: WorkDefinition`; `KIND: WorkRun`; `KIND: Attempt`; owner/boundary; derived projection; evidence finding; residue. “Work Atlas” is an interface title, never a generic semantic-node type. |
| Relations | `RELATION: STRUCTURAL TRIGGER`; `TEMPORAL CAUSATION`; `TRANSPORT/DELIVERY`; `JOURNAL ACCEPTANCE`; `PROJECTION DERIVATION`; `OWNED BY`; `REQUIRES AUTHORITY`. |
| Lanes | `OWNER: ROOT/CURSOR`; `COMMAND PROTOCOL`; `WORK/ADAPTER`; `EVENT PROTOCOL`; `JOURNAL`; and scenario-specific `GATE`, `EXTERNAL EFFECT`, and `SIDECAR`. |
| Distinct states | `JOURNAL ACCEPTANCE DISPOSITION`; work-owned `DOMAIN STATUS`; work/gate-owned `CONFIRMATION`; root-owned `CURSOR STATE`; `ADAPTER ADMISSION`; `ATTEMPT FRESHNESS`; `FINDING STATUS`. |
| Journal disposition | `journal-accepted/new event record`; `journal-accepted/duplicate event record—no new cursor transition`; `quarantined/divergent`; `rejected/not recorded`. This is persistence disposition, never confirmation. |
| Effect boundary | Three separate fields: `AUTHORITY REFERENCE: present/absent/unsupported`; `ADAPTER ADMISSION: admitted/rejected/not observed`; `EXTERNAL EFFECT OCCURRENCE: observed/not observed/unsupported`. No field implies another. |
| Claim ceiling | Persistent `PROPOSAL ONLY` text, source layer, evidence stage, and cannot-establish statement. |
| Principal forbidden inferences | Same outer contract ≠ same body; composition/containment ≠ orchestrator authority or inherited authority; command ≠ journal-accepted event record; journal acceptance ≠ confirmation; terminal ≠ success/approval/effect permission; protocol/journal ≠ decision/execution; authority-reference presence ≠ adapter admission ≠ effect occurrence; projection ≠ domain state or authority. |

Shape, position, lane, color, fill, arrow style, or motion may reinforce these labels but can never replace textual `KIND`, `RELATION`, `OWNER`, or state labels.

`[D:19-32,70-146,222-302,368-399; O:63-187,220-253; E1,E4,E8]`

## 4. Persistent learner-facing Work card

```text
WHAT IS WORK?

Work is the uniform typed executable boundary.

Its immutable, versioned WorkDefinition declares:
input/output schemas · command/event contracts · authority requirements · limits
and exactly one body kind:
  LEAF      → executor binding
  COMPOSITE → WorkGraph

WorkRun is one invocation of one WorkDefinition.
Attempts belong to a WorkRun and do not change its definition or authority basis.

Every composition operator returns the same outer Work contract.
Therefore a pipeline is also Work and can be nested where a leaf can be used.
It does not become an orchestrator: one root OrchestratorKernel expands and schedules it.

Same outer contract; different body. Structural recursion; shallow authority.
```

The card remains reachable from every lens. Semantic nodes remain exactly `WorkDefinition`, `WorkRun`, or `Attempt`; generic `Work` is the explanatory contract name, not an ambiguous node type.

`[D:87-220,304-318; O:42-90,140-163,172-180; E1,E2]`

## 5. Candidate comparison

| Candidate | Coverage | Type/authority fidelity | Causal execution | Orientation and disclosure | Static/non-visual equivalence | Traceability/ceiling | Disposition |
|---|---|---|---|---|---|---|---|
| **Typed coordinated Work Atlas** | Covers structure, time, ownership, evidence, and residue | Preserves all named non-collapse pairs | Causal occurrence ledger handles joins, retries, delays, duplicates, and exhaustion | Work card → overview → focus → inspect → trace → bound | Outline, table, legend, ownership ledger, transcript | Every record retains exact selector, owner, stage, and proposal ceiling | **KEEP — primary** `[D:19-460; O:21-337; E1,E4-E8]` |
| Full UML/ArchiMate suite | High formal coverage | High only with local profiles and warnings | Requires several diagram families | High novice cost | Good expert export | Risks imported semantics and false conformance | **DEFER** `[D:87-330; O:63-187; E2,E9]` |
| BPMN/guided scenario first | Strong branch/join/gate/repeat account | Token may collapse routing, domain status, or authority | Strong finite walkthrough | Low initial cost; weak ontology/residue coverage | Transcript possible | Illustrative behavior can appear implemented | **MERGE** only into Flow; BPMN is a visualization precedent `[D:148-220,304-366; O:189-253; E3,E7,E10]` |
| Annotated document first | Preserves every source section | Lowest translation risk | Weak cross-section causality | Familiar but assembly burden remains | Strongest text equivalent | Excellent source traceability | **MERGE** as outline/table/Inspector source path `[D:34-460; O:21-337; E5,E8]` |
| Universal graph | Nominally includes everything | Mixes definition, occurrence, ownership, evidence, and layout relations | Arrival/layout can masquerade as causality | Severe overload | Poor linear equivalence | Layout becomes accidental meaning | **KILL** as primary `[D:222-330; O:137-253; E4-E6]` |

## 6. Synchronized-lens responsibilities

- **Structure:** one-root overview, reusable `WorkDefinition` topology, selected composite body, and a separate flattened run-plan projection. Recursion appears as shared contract, definition nesting, and root-owned graph expansion—never nested authority. Uses **C4-inspired decomposition/zoom discipline**, not C4 semantics. `[D:19-32,87-220,304-318; O:42-90,137-180; E1,E2,E9]`
- **Flow:** immutable, text-labelled `COMMAND` and `EVENT` occurrence cards ordered by explicit causation and declared release edges. Wall time, journal order, per-run sequence, transport, journal acceptance, and causality remain separate. OpenTelemetry and BPMN are visualization precedents only. `[D:222-330,385-399; O:137-170; E3,E4]`
- **Ownership/Proof:** named owners and distinct state rows for domain status, confirmation, journal acceptance, cursor, authority-reference presence, adapter admission, external-effect occurrence, evidence stage, profile, finding, and residue. `[D:70-85,287-302,368-460; O:172-327; E6,E8]`
- **Inspector:** exact semantic or occurrence ID, `KIND`, `OWNER`, source precedence layer, source selector/digest, properties, relations, shields, journal disposition, reducer/freshness where relevant, evidence stage, and claim ceiling. `[O:111-187,220-279; E6,E8]`

## 7. Complete named-element and section atlas

| Elements | Visible encoding and non-collapse rule | Binding |
|---|---|---|
| `WorkDefinition`, `WorkRun`, `Attempt` | Text-labelled definition card, separate run card, and attempt rows. No runtime state on a definition. | `[D:87-128; O:63-76,140-143; E1,E2]` |
| Leaf/composite substitutability | Same outer definition frame with explicit `BODY: LEAF` or `BODY: COMPOSITE`; persistent “same contract, different body” warning. | `[D:130-146; O:65-72,144-149; E1,E2]` |
| Sequence, fan-out, fan-in | Text-labelled structural edges carrying selector and input mapping; fan-in names policy and canonical manifest. | `[D:148-188; O:77-89,145-159; E2,E3]` |
| Gate | Ordinary decision-work entity plus `RELATION: ROUTE LABEL MATCH`; zero/multiple matches block. Work-owned confirmation remains separate from journal acceptance. | `[D:189-197,374-375; O:85-86,174-184; E2,E3]` |
| Sidecar | `KIND: SIDECAR WORK`, owner, lifecycle policy, and detached lane; no control without an explicit edge. | `[D:198-209,397-399; O:87-88,157-158,180-181; E3,E4]` |
| Bounded repetition | Back-edge labels decision work, round/max, and named exhaustion edge. No hidden/unbounded loop. | `[D:210-215,376-377; O:89-90,125-126,201-205; E3]` |
| Explicit graph composition | Operator and primitive graph are separately inspectable; compilation does not imply execution. | `[D:216-220; O:90,153-156,225-228; E2]` |
| Root, protocol, journal, adapters | Distinct `KIND` and `OWNER` labels: one root schedules; protocol transports; journal records; adapter executes/translates. | `[D:54-68,130-136,222-302; O:91-104,160-187; E4]` |
| Commands/events | Every occurrence says `KIND: COMMAND` or `KIND: EVENT`; visual lane/style is redundant only. | `[D:222-285; O:91-96,119-126,160-168; E4]` |
| Journal acceptance | Separate labelled disposition attached to the event record; never styled or named as confirmation. | `[D:227-232,259-271,304-322,385-390; O:96-100,123-126,164-166,182-185; E4]` |
| Cursor/domain status/confirmation | Three separately owned cards; confirmation is gate/work-owned even when its event record is journal-accepted. | `[D:287-302; O:99-108,127-130,166-187; E4,E6]` |
| External effects | Separate textual fields for authority-reference presence, adapter admission, and effect occurrence. | `[D:104-113,378-381; O:101-104,167-168,181-185,204-205; E4]` |
| Invariants/failure/residue | `RWO-I01–I12` with evidence stage/failure posture; abnormal records retain identity; all residue remains open. | `[D:368-460; O:189-218,235-327; E4,E8]` |

Design-section coverage:

- §§1–3 → purpose/thesis/non-goal overview and owner matrix `[D:34-85; E5,E6]`
- §4 → Work card, definition/run anatomy `[D:87-146; E1,E2]`
- §5 → composition catalog and primitive graph `[D:148-220; E2,E3]`
- §6 → command/event rails, envelope, journal disposition `[D:222-285; E4]`
- §7 → ownership ledger `[D:287-302; E6]`
- §8 → illustrative paper-trace stepper `[D:304-330; E4]`
- §9 → proposed scenario selector `[D:332-366; E7,E10]`
- §§10–11 → invariant/profile matrix and abnormal-event overlays `[D:368-399; E4,E8]`
- §§12–14 → provenance, bounded claim, design→ontology handoff `[D:401-445; E5,E6]`
- §§15–16 → residue and typed connections `[D:447-470; E5,E8]`

Ontology coverage:

1. identity/boundary → source-precedence and ceiling card `[O:21-40; E5]`
2. thesis → one-root overview `[O:42-61; E1]`
3. types → filtered outline/graph `[O:63-109; E1,E6]`
4. properties → property/inference table `[O:111-135; E8]`
5. relations → typed relation table `[O:137-170; E2,E9]`
6. shields → negative-control ledger `[O:172-187; E8]`
7. profiles → definition/runtime evidence comparison `[O:189-218; E8]`
8. observations → may-observe/cannot-establish matrix `[O:220-233; E6]`
9. findings → evidence-chain Inspector `[O:235-253; E8]`
10. confidence → evidence/commitment display `[O:255-267; E8]`
11. sources → precedence-aware provenance `[O:269-279; E6]`
12. residue → all fourteen unresolved records `[O:281-305; E5]`
13. validation → pass/unsupported/not-granted matrix `[O:307-327; E8]`
14. connections → typed, non-promoting links `[O:329-337; E6]`

## 8. Three finite illustrative paper traces

Every occurrence card includes textual `KIND`, `PRODUCER`, `CONSUMER`, `CAUSE`, and `OWNER` fields. For effectful boundaries, it separately reports authority-reference presence, adapter admission, and effect occurrence. No runtime outcome is inferred.

### A. Sequence with gate

| Step | Occurrence | Journal disposition / cursor | Ownership and effect boundary |
|---|---|---|---|
| M01 | `COMMAND`, root → A: invoke | No event record; cursor records proposed delivery | A owns status. Authority reference required; adapter admission not observed; effect occurrence unsupported. |
| M02 | `EVENT`, A → protocol/journal: `A.release`, caused by M01 | `journal-accepted/new event record`; cursor satisfies A→G | A retains domain meaning. Event record is not confirmation or effect permission. |
| M03 | `COMMAND`, root → G: invoke, caused by M02 | No event record; cursor records proposed delivery | G owns decision and confirmation. |
| M04 | `COMMAND`, confirmation adapter → G: `confirmation-provided` | No journal-accepted gate event record yet; cursor unchanged | Command receipt is not work-owned confirmation. |
| M05 | `EVENT`, G → journal/root: `route.approved`, caused by M04 | `journal-accepted/new route-event record`; one route becomes eligible | G separately owns its decision/confirmation. Journal acceptance does not create either. |
| M06 | `COMMAND`, root → B: invoke, caused by M05 | No result event record | Authority reference required; adapter admission not observed; external-effect occurrence unsupported. Route label implies none of these outcomes. |

### B. Fan-out followed by fan-in

| Step | Occurrence | Journal disposition / cursor | Ownership and effect boundary |
|---|---|---|---|
| F01 | `EVENT`, source emits release | `journal-accepted/new event record`; two declared edges eligible | Source owns domain status. |
| F02/F03 | `COMMAND`, root invokes B1 and B2, both caused by F01 | Separate delivery entries; no shared event record | Separate owners and independent authority-reference/admission/effect fields. |
| F04/F05 | `EVENT`, B2 then B1 release; neither causes the other | Two `journal-accepted/new event records`; `all` false after F04, true after F05 | Arrival order creates no sibling causality or shared status. |
| F06 | `COMMAND`, root invokes J with two explicit causes | Canonical input manifest; fan-in fires once | J owns reconciliation. Authority reference, admission, and effect occurrence remain separate/unsupported. |

### C. Primary, non-controlling sidecar, one retry, and exhaustion

| Step | Occurrence | Journal disposition / cursor | Ownership and effect boundary |
|---|---|---|---|
| S01/S02 | `COMMAND`, root invokes P/A1 and sidecar S | Separate deliveries; no shared event record | P and S own separate states; S has no primary authority. |
| S03 | `EVENT`, S emits diagnostic observation | `journal-accepted/new diagnostic event record`; no release by default | S cannot advance or stop P. |
| S04 | `EVENT`, P/A1 emits terminal failure | `journal-accepted/new event record`; retry-decision work D becomes eligible | P owns failure meaning; terminal event record does not itself retry. |
| S05/S06 | `COMMAND` root→D; then `EVENT` D emits `route.retry` | Route event is `journal-accepted/new`; round becomes 2 and A2 becomes eligible | D owns retry decision; journal acceptance is not D’s confirmation state. |
| S07 | `COMMAND`, root invokes P/A2 | A1 remains history; new attempt ID | Authority-reference presence, adapter admission, and effect occurrence remain distinct. |
| S08-success | `EVENT`, P/A2 emits release | `journal-accepted/new event record`; primary successor eligible | P owns outcome meaning. |
| S09-success | `EVENT`, sidecar terminates | Separate journal disposition; finish policy applies | Sidecar still cannot control the primary successor. |
| **C-X1 exhaustion counterfactual** | After the one permitted retry, P/A2 instead emits terminal failure | `journal-accepted/new event record`; cursor observes `round=2=maxRounds` | Failure cannot enable another retry attempt. |
| **C-X2 exhaustion counterfactual** | The declared, text-labelled `RELATION: EXHAUSTION EDGE` fires to its named exhaustion target | Cursor records exhaustion route; **no A3 may be created** | Exhaustion target owns any subsequent domain meaning; root only routes the declared edge. |

Identical duplicates receive `journal-accepted/duplicate event record—no new cursor transition`; divergent same-key bytes are `quarantined/divergent`; delayed records retain occurrence and journal times; stale-attempt records remain visible but cannot release current edges. None is encoded by color alone.

`[D:148-215,222-330,368-399; O:77-100,119-187,189-205; E3,E4]`

## 9. Learner paths and finite acceptance tasks

Novice path:

1. Read the proposal ceiling and persistent Work card.
2. Distinguish `WorkDefinition`, `WorkRun`, attempt, and one-root kernel.
3. Use Ownership/Proof to compare work domain state, journal acceptance, cursor, and confirmation.
4. Step through the gated sequence with the persistent legend.
5. Trace sidecar/retry through the exhaustion counterfactual and deny A3.
6. Finish at unsupported evidence and residue.

Expert path:

1. Filter definitions, runs, graphs, edges, messages, journal, cursor, adapters, and authority references.
2. Inspect one edge’s selector, mapping, source precedence, cycle policy, and shields.
3. Compare causation, delivery, journal acceptance, and cursor fold in Flow.
4. Inspect authority-reference presence, adapter admission, and effect occurrence independently.
5. Cross-check profiles/invariants and inspect every conflict/residue before treating a conclusion as settled.

Required but unexecuted acceptance tasks include:

- Select Work and state the uniform contract, definition/run distinction, leaf-or-graph body, pipeline closure, and one-root rule.
- Walk M01–M06 and distinguish command, journal-accepted event record, gate-owned confirmation, routing, and effect admission.
- Walk F01–F06 and identify concurrent siblings, `all` readiness, multi-cause join, and canonical manifest.
- Walk S01–S09 plus C-X1/C-X2 and deny sidecar control and A3 creation.
- Assign domain state, journal acceptance, cursor, confirmation, adapter admission, and effect occurrence to the correct owner/boundary.
- Reject every mutant in §12.

No task has been human-tested. `[D:87-399; O:63-253; E5-E8,E10]`

## 10. Semantic-source and removable-projection contract

- Pin `DESIGN.md` and `ONTOLOGY.md` independently, retaining their separate identities, digests, roles, and precedence.
- Semantic records use exact design claims plus candidate ontology IDs, relations, selectors, shields, and explicit conflict/residue records.
- Learner routes, Work-card wording, layout coordinates, focus, selection, breadcrumbs, scenario ordering, highlights, and navigation links are removable projection records.
- Deleting all projections must leave design bytes, ontology bytes, digests, semantic IDs, relation IDs, selectors, and source-conflict records unchanged.
- Every view selects the same full source or occurrence identity and feeds the same Inspector.
- No projection may write back, resolve a design/ontology conflict, create authority, manufacture domain status or confirmation, or claim freshness without lineage.
- No machine semantic graph, stable-ID policy, projection compiler, or synchronized UI exists; the contract remains proposed.

`[D:19-32,430-460; O:21-40,172-187,220-327; E6,E8]`

## 11. Negative controls

- **Ownership collapse:** KILL removal of Ownership/Proof or any ownerless status.
- **Recursion collapse:** KILL a kernel inside a composite or any containment-to-authority inference.
- **Command/event collapse:** KILL merged rails or occurrences lacking textual `COMMAND`/`EVENT`.
- **Journal/confirmation collapse:** KILL “accepted fact/decision” wording or any journal disposition styled as confirmation.
- **Effect-boundary collapse:** KILL any single checkpoint that merges authority-reference presence, adapter admission, and effect occurrence.
- **Timeline spectacle:** KILL autoplay causality, moving structural nodes, or ordering by arrival/wall time.
- **Graph overload:** KILL the universal graph as the landing surface.
- **Status inflation:** KILL universal green terminal/success, projection-authored state, or terminal-as-permission.
- **Finite-bound loss:** KILL a loop without decision owner, bound, exhaustion edge, and explicit no-next-attempt result.
- **Source collapse:** KILL ontology-overrides-design behavior or projection writeback.

`[D:19-32,70-85,210-215,222-302,368-399; O:172-187; E4,E7,E8]`

## 12. MVP versus later capability

MVP contract:

- Pinned, precedence-aware design and ontology fixture.
- Persistent proposal ceiling.
- Persistent Work card.
- Persistent text-first legend covering entities, relations, lanes, distinct states, claim ceiling, and principal forbidden inferences.
- Structure landing view with graph, outline, and relation table.
- Textual `KIND`, `RELATION`, and `OWNER` labels throughout.
- Shared stable selection and Inspector.
- Three immutable paper-trace transcripts, including exhaustion/no-A3.
- Explicit journal-acceptance dispositions.
- Separate authority-reference, adapter-admission, and effect-occurrence fields.
- Ownership/Proof matrix, invariants, source conflicts, and residue.
- Keyboard path, visible focus, reduced-motion stepping, and static/no-JavaScript equivalents.
- Projection-removal byte-identity and complete-section-coverage tests.

Later/deferred:

- Live journal replay, telemetry ingestion, runtime-derived state, and observed effect records.
- Formal UML/ArchiMate export.
- Semantic color palette beyond redundant focus/highlight.
- Nonessential animation and large-plan optimization.
- Dynamic topology, migrations, cross-host delivery guarantees, quorum semantics, and authority-reference details.
- Accessibility-conformance and human-comprehension claims until independently evaluated.

## 13. Separate validation ceilings

| Lane | May establish | Must not claim |
|---|---|---|
| Agent/structural | Source precedence, selector coverage, stable-ID consistency, projection removability, finite trace conformity, legend completeness, mutant rejection | Runtime behavior or learner understanding |
| Browser | Rendering, links, synchronized selection, persistent legend/card, controls, transcript parity, reduced-motion behavior | Accessibility conformance or comprehension |
| Accessibility | Keyboard, focus, names, contrast, zoom/reflow, motion, reading order, and assistive-technology results on a built artifact | General comprehension |
| Human comprehension | Preregistered novice/expert locate, trace, distinguish, retell, and boundary-task results | Runtime conformance, authority, or universal usability |

None has been executed.

## 14. Dispositions

- **MERGE:** C4-inspired decomposition/zoom discipline; selected UML/ArchiMate relation distinctions; annotated document as the outline/table/Inspector source path; guided scenarios and BPMN-like glyphs within Flow; OpenTelemetry-style occurrence links within the paper-trace renderer.
- **KILL:** universal graph as primary; token-as-status; generic semantic `Work` nodes; merged command/event rails; “accepted fact/decision” wording; nested orchestrator glyphs; ownerless/color-only states; single effect checkpoint; projection writeback; autoplay causality; unbounded loops.
- **DEFER:** full UML/ArchiMate export, live replay, telemetry overlays, runtime status, semantic color palette, nonessential animation, accessibility claims, and human-comprehension claims.

C4, OpenTelemetry, and BPMN remain visualization precedents only. They do not supply RWO semantics or runtime evidence.

## Reviewer-gate handoff

- **Precedent gate:** local meanings remain source-owned; external notations are explicitly bounded precedents; Inventory remains discovery only.
- **Non-vacuity gate:** the persistent Work card answers what Work is and why a pipeline is Work without becoming an orchestrator; C-X1/C-X2 visibly terminate bounded retry through exhaustion with no A3.
- **Definitional gate:** the persistent legend, journal disposition, source precedence, textual kind/owner labels, and three-stage effect boundary repair every conditional or failed non-collapse test while retaining the smallest vocabulary.

## Receipt

```json
{
  "action_id": "spawn-0004",
  "role": "view-synthesizer",
  "status": "pass",
  "validation": "pass",
  "blockers": [],
  "artifacts": [],
  "started_at": "2026-08-04T17:51:19-03:00",
  "finished_at": "2026-08-04T17:51:48-03:00"
}
```
