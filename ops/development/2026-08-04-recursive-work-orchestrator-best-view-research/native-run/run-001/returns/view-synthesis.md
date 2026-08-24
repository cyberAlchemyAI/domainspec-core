## Synthesis verdict

Recommend one primary explanatory architecture: a **typed, coordinated Work Atlas**.

Its landing surface is the **Structure** view. **Flow** and **Ownership/Proof** are synchronized lenses over the same selected identity, while one shared **Inspector** exposes exact source, owner, evidence stage, forbidden inference, and claim ceiling. This is one architecture, not four independent truths.

The frozen sources match their registered digests:

- `D` = `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/DESIGN.md`, SHA-256 `28b6fca81693a5c6bd10dbe2e74df816312d9e1955e076c950eacd49a86a9419`
- `O` = `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/ontology/ONTOLOGY.md`, SHA-256 `1c6d417c4f0cdfc73c7c42f016c05fd6f8fbccd738a35bf7454472d3cee3b920`

Both remain proposal-only candidate sources.

### Direct external-source keys

- `E1`: [C4 diagrams and zoom](https://c4model.com/diagrams), [C4 notation](https://c4model.com/diagrams/notation)
- `E2`: [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1)
- `E3`: [OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2)
- `E4`: [OpenTelemetry trace API](https://opentelemetry.io/docs/specs/otel/trace/api/), [messaging spans](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/), [Lamport’s ordering paper](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/)
- `E5`: [Shneiderman, The Eyes Have It](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf)
- `E6`: [North and Shneiderman, Snap-Together Visualization](https://www.cs.umd.edu/users/ben/papers/North2000Snapa.pdf)
- `E7`: [Tversky, Morrison and Betrancourt, Animation: Can It Facilitate?](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)
- `E8`: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [ARIA tree-view pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/)
- `E9`: [The Open Group ArchiMate overview](https://www.opengroup.org/archimate-forum/archimate-overview)
- `E10`: [Mayer’s Segmenting Principle](https://www.cambridge.org/core/books/abs/multimedia-learning/segmenting-principle/37240877DDA0362355ADB39936027982)

These sources justify notation and interaction choices only. They do not prove this view’s accessibility or comprehensibility.

## 1. Candidate comparison

| Candidate | Complete coverage | Type/authority fidelity | Causal explanation | Orientation/disclosure | Static/non-visual equivalent | Traceability and ceiling | Disposition |
|---|---|---|---|---|---|---|---|
| **Typed coordinated Work Atlas** | Covers structural, temporal, ownership, evidence, and residue dimensions | Explicit definition/run, containment/authority, event/status, bus/journal/kernel distinctions | Causal occurrence ledger handles joins, retries, delays, and duplicates | Overview → focus → inspector; stable selection | Outline, relation table, transcripts, ownership ledger | Every card retains source selector, owner, stage, ceiling | **KEEP — primary**. `[D:19-32,87-330,368-460; O:21-253,281-327; E1,E4,E5,E6,E8]` |
| Full UML/ArchiMate suite | High formal coverage | High if profiled carefully | Requires several diagram families | High novice burden | Good print/export potential | Profiles still needed for local meanings | **DEFER** as expert export. `[D:87-330; O:63-187; E2,E9]` |
| BPMN/token or guided-scenario first | Strong for branch/join/gate/repeat | Token can be mistaken for status, authority, or accepted fact | Strong finite walkthrough | Low initial cost, poor whole-model coverage | Transcript possible | Can make illustrative behavior look implemented | **MERGE** only as Flow scenarios. `[D:148-220,304-366; O:189-253; E3,E7,E10]` |
| Annotated-document first | Preserves source prose and residue | Low translation risk | Weak cross-section causality | Familiar but reader must assemble the model | Intrinsically strong | Excellent source binding | **MERGE** as outline/table/source equivalent. `[D:34-460; O:21-337; E5,E8]` |
| Single universal graph | Can contain everything nominally | Collapses structural, temporal, ownership, and evidence edges | Arrival/layout can masquerade as causality | Severe overload | Poor without a separate linear model | Layout becomes accidental meaning | **KILL** as primary. `[D:222-330; O:137-187,220-253; E4,E5,E6]` |

## 2. Primary architecture and wireframe

```text
┌ PROPOSAL ONLY · no runtime, authority, promotion, or comprehension proof ┐
│ Root: exactly one OrchestratorKernel     Breadcrumb / stable selection   │
├ Structure (primary) ─ Flow ─ Ownership/Proof ─ Source/Text               ┤
│ semantic outline │ focused Work graph / run plan │ shared Inspector     │
│                  │ definition ≠ run              │ ID · owner · source  │
│                  │ composite ≠ orchestrator      │ stage · shields      │
├ finite causal stepper + immutable transcript + reduced-motion controls  ┤
│ Ownership ledger: domain state | journal history | cursor | confirmation │
└ Residue · invariant/profile status · unsupported evidence notices       ┘
```

Responsibilities:

- **Structure:** system boundary, one root kernel, reusable `WorkDefinition` topology, selected composite body, and separate expanded run-plan projection. Recursion appears as shared type identity, definition nesting, and root-owned graph expansion—never nested authority. `[D:19-32,87-220,304-318; O:42-76,137-179; E1,E2,E9]`
- **Flow:** immutable command/event occurrences ordered by explicit causation and declared release edges. Wall time, journal acceptance order, per-run sequence, and causality remain separate. `[D:222-285,304-330,385-399; O:137-170; E3,E4]`
- **Ownership/Proof:** named owners for domain state, confirmation, accepted history, cursor, authority boundary, evidence stage, profiles, findings, and residue. `[D:70-85,287-302,368-460; O:172-327; E6,E8]`
- **Inspector:** one stable-ID card containing definition/run identity, exact local selector, source digest, properties, allowed relations, forbidden inferences, owner, freshness/reducer where applicable, evidence stage, and visible proposal-only ceiling. `[O:111-187,220-279; E6,E8]`

## 3. Named-element atlas

| Elements | Visible encoding and non-collapse rule | Binding |
|---|---|---|
| `WorkDefinition`, `WorkRun`, attempt | Solid definition frame; separate outlined run chip; attempt rows under the run. Never apply runtime state to a definition. | `[D:87-128; O:63-76,140-143; E1,E2]` |
| Leaf/composite substitutability and recursion | Same outer Work geometry with `leaf`/`composite` body badge; drill-in body plus separately flattened root plan. Containment never denotes authority. | `[D:130-146,304-318; O:69-76,144-149,163,172-180; E1,E2]` |
| Sequence, fan-out, fan-in | Typed edge with event selector and input mapping; fan-in has named `all/any/quorum(n)` policy and canonical manifest. | `[D:148-188; O:77-89,145-159; E2,E3]` |
| Gate | Gate remains ordinary decision work; attached routing diamond visualizes label matching only. Zero/multiple matches block. | `[D:189-197,374-375; O:85-86,174-184; E2,E3]` |
| Sidecar | Detached companion lane with explicit start/observe/finish/output policy; no control edge unless declared. | `[D:198-209,397-399; O:87-88,157-158,180-181; E3,E4]` |
| Bounded repetition and explicit graph | Back-edge names decision work, round bound, and exhaustion route; convenience forms expose their primitive graph compilation. | `[D:210-220,376-377; O:89-90,153-156,199-205; E2,E3]` |
| Root kernel, bus, journal, work/adapter | One root outside composite frames; bus has separate command/event rails; journal is append-only persistence; adapters alone cross executor/effect boundaries. None substitutes for another owner. | `[D:54-68,130-136,222-302; O:91-104,160-168,172-187; E4]` |
| Commands and events | Solid addressed-request arrow versus hollow accepted-fact arrow; both show message, correlation, causation, run, node, attempt, sequence, and idempotency identity. | `[D:222-285; O:91-96,119-126,160-168; E4]` |
| Cursor, domain status, confirmation | Separate owner-tagged cards: root-derived cursor; work-owned domain state; gate/work-owned confirmation. A status projection shows reducer, freshness, and lineage. | `[D:287-302; O:99-108,127-130,166-187; E4,E6]` |
| External effects | Authority-reference checkpoint at adapter boundary; no kernel-to-effect shortcut and no implication that a reference decided correctly. | `[D:104-113,378-381; O:101-104,167-168,181-185,204-205; E4]` |
| Invariants, failures, residue | `RWO-I01–I12` badges carry evidence stage and failure posture; abnormal occurrences retain their identity; `RWO-OQ-*`/`rwo:residue.*` remain visibly open. | `[D:368-460; O:189-218,235-327; E4,E8]` |

## 4. Complete section/ontology coverage

Design coverage:

- §§1–3 → thesis, bounded purpose, one-root banner, non-goal/owner matrix. `[D:34-85; E5,E6]`
- §4 → Work anatomy and definition/run inspector. `[D:87-146; E1,E2]`
- §5 → composition catalog plus primitive typed graph. `[D:148-220; E2,E3]`
- §6 → two-lane protocol and envelope inspector. `[D:222-285; E4]`
- §7 → ownership ledger. `[D:287-302; E6]`
- §8 → finite accepted-event causal trace. `[D:304-330; E4]`
- §9 → illustrative scenario selector, always labelled proposed. `[D:332-366; E7,E10]`
- §§10–11 → invariant/profile matrix and abnormal-event overlays. `[D:368-399; E4,E8]`
- §§12–14 → provenance, bounded expressiveness, and design-to-ontology bridge. `[D:401-445; E5,E6]`
- §§15–16 → unresolved residue and typed source connections. `[D:447-470; E5,E8]`

Ontology coverage:

1. Identity/boundary → claim-ceiling card `[O:21-40; E5]`
2. Thesis → one-root semantic overview `[O:42-61; E1]`
3. Types → filtered outline/graph `[O:63-109; E1,E6]`
4. Properties → subject/property/forbidden-inference table `[O:111-135; E8]`
5. Relations → directed typed-edge table `[O:137-170; E2,E9]`
6. Shields → negative-control ledger `[O:172-187; E8]`
7. Profiles → definition/runtime evidence comparison `[O:189-218; E8]`
8. Observation projections → may-observe/cannot-establish matrix `[O:220-233; E6]`
9. Finding shape → evidence-chain inspector `[O:235-253; E8]`
10. Confidence ledger → evidence versus commitment display `[O:255-267; E8]`
11. Source ledger → provenance inspector `[O:269-279; E6]`
12. Residue → fourteen open records `[O:281-305; E5]`
13. Validation → pass/unsupported/not-granted matrix `[O:307-327; E8]`
14. Connections → typed, non-promoting source links `[O:329-337; E6]`

## 5. Three finite paper traces

All traces are proposed walkthroughs, not observations. Causation links determine the explanatory order; transport or wall-clock order does not. `[D:222-330; O:137-170; E3,E4]`

### A. Sequence with gate

| Step | Occurrence | Persisted fact / cursor | Owner and effect boundary |
|---|---|---|---|
| M01 | root → A: invoke | No domain fact; A delivery recorded | A owns status; effect only after A adapter authority check |
| M02 | A → journal/root: `A.release`, caused by M01 | Accepted A release; edge A→G satisfied | A retains meaning; event is not permission |
| M03 | root → G: invoke, caused by M02 | G delivery only | G owns decision/confirmation |
| M04 | confirmation adapter → G: `confirmation-provided` | Command receipt is not confirmation | No route or effect yet |
| M05 | G → journal/root: `route.approved`, caused by M04 | Accepted gate decision; exactly one route enables B | G retains decision evidence; zero/multiple matches block |
| M06 | root → B: invoke, caused by M05 | B delivery only | B adapter rechecks authority; route label alone is insufficient |

### B. Fan-out then fan-in

| Step | Occurrence | Persisted fact / cursor | Owner and effect boundary |
|---|---|---|---|
| F01 | source emits release | Accepted source fact; two edges eligible | Source owns its status |
| F02/F03 | root invokes B1 and B2, both caused by F01 | Independent deliveries | Separate branch status and authority |
| F04/F05 | B2 then B1 emit release; neither causes the other | After F04, `all` unsatisfied; after F05, satisfied | Arrival order does not create branch causality |
| F06 | root invokes join J with multi-cause links | Canonically ordered manifest; fired once | J owns reconciliation meaning; authority checked separately |

### C. Sidecar plus one bounded retry

| Step | Occurrence | Persisted fact / cursor | Owner and effect boundary |
|---|---|---|---|
| S01/S02 | root invokes primary attempt A1 and sidecar | Separate deliveries | P and S own separate states; sidecar has no primary authority |
| S03 | sidecar emits diagnostic observation | Diagnostic fact only; no release by default | Cannot advance or stop P |
| S04 | P/A1 emits terminal failure | A1 retained; retry decision D enabled | Failure does not itself retry |
| S05/S06 | root invokes D; D emits `route.retry` | Accepted decision; round becomes 2 | D owns retry decision; P owns primary status |
| S07 | root invokes P/A2 | A1 remains history; new attempt ID | Adapter repeats authority/idempotency check |
| S08/S09 | P/A2 releases; sidecar terminates | Separate facts; successor enabled; sidecar follows declared finish policy | Sidecar cannot control successor |

Duplicates appear as hollow linked occurrences with no new cursor transition; divergent same-key bytes are quarantined; delayed events retain `occurred_at` and `accepted_at`; stale attempts remain visible but cannot release current edges; terminal never becomes universal green success. `[D:259-285,368-399; O:119-126,172-187; E4]`

## 6. Learner paths

Novice:

1. Read the proposal-only and one-root notices.
2. Learn six terms: Work, definition, run, command, event, owner.
3. Select “Who owns what?” and compare work domain state, journal history, and root cursor.
4. Step through the gated sequence.
5. Inspect gate versus route, terminal versus success, and projection versus authority.
6. Finish at invariants, unsupported evidence, and residue.

Expert:

1. Filter Structure by definitions, runs, graphs, edges, messages, journal, cursor, and authority references.
2. Inspect an edge’s selector, input mapping, cycle policy, source, and shields.
3. Trace fan-in, retry, duplicate, delayed, and stale-attempt cases.
4. Cross-check each occurrence in Ownership/Proof against profile and evidence stage.
5. Compare graph, outline, table, and transcript identities, then inspect all residue before drawing conclusions.

`[D:87-460; O:63-327; E5,E6,E7,E10]`

## 7. Semantic-source/removable-projection contract

- Semantic input is one revision-pinned, read-only snapshot of the frozen design and candidate ontology.
- Semantic records include stable IDs, types, relations, source selectors, source digests, and explicit shields.
- Layout, learner labels, breadcrumbs, focus, selection, scenario order, highlights, and navigation links are projection records only.
- Removing every learner/navigation/layout record must leave semantic bytes, digests, node IDs, relation IDs, and selectors unchanged.
- Every view selects the same full semantic or occurrence ID and feeds the same Inspector.
- No projection may write back semantics, infer authority, manufacture status/confirmation, or claim freshness without lineage.
- Because no machine semantic graph, projection schema, or compiler exists, synchronization remains a recommended contract, not an implemented property.

`[D:70-85,430-460; O:21-40,172-253; E6,E8]`

## 8. Negative controls

- **Ownership collapse:** KILL any view where removing owner labels leaves status colors unchanged or where kernel, bus, or journal appears to decide/execute.
- **Recursion misrepresentation:** KILL nested scheduler lanes or composite-to-orchestrator invocation edges.
- **Timeline spectacle:** KILL autoplay that converts arrival/wall time into causality, moves stable nodes, or advances commands into facts.
- **Graph overload:** KILL one unfiltered semantic/runtime/evidence graph as the landing view.
- **Status inflation:** KILL universal green terminal, confirmation-on-command-receipt, gate-label effect permission, or projection-authored status.
- **Finite-bound loss:** KILL any loop without decision owner, round counter, bound, and exhaustion route.

`[D:19-32,222-302,368-399; O:172-187; E4,E7,E8]`

## 9. MVP and later boundary

MVP contract:

- Pinned semantic fixture and selector coverage manifest.
- Structure landing view with graph, outline, and relation table.
- Shared stable selection and Inspector.
- Three immutable scenario transcripts with causal stepping.
- Ownership/proof matrix, claim-ceiling banner, invariants, and residue.
- Keyboard path, visible focus, reduced motion, and no-JavaScript/static equivalents.
- Projection-removal byte-identity test.

Later or deferred:

- Live journal replay, runtime ingestion, and telemetry overlays.
- Full UML/ArchiMate export.
- Large-plan graph optimization and animated transitions.
- Dynamic topology, migrations, cross-host guarantees, quorum semantics, and effect-authority details.
- Accessibility conformance claims and human-comprehension claims until independently evaluated.

## 10. Separate validation ceilings

| Validation lane | May establish | Must not claim |
|---|---|---|
| Agent/structural | Selector coverage, stable-ID consistency, projection removability, finite trace conformity, forbidden-mutant rejection | Runtime behavior or learner understanding |
| Browser | Exact rendering, links, synchronized selection, controls, transcript parity, reduced-motion operation | Accessibility conformance or comprehension |
| Accessibility | WCAG-oriented keyboard, focus, names, contrast, zoom/reflow, motion, and assistive-technology results on a built artifact | General human comprehension |
| Human comprehension | Preregistered novice/expert locate, trace, distinguish, retell, and boundary-task results | Authority, runtime conformance, or universal usability |

No lane has been executed.

## 11. Dispositions

- **MERGE:** C4 zoom discipline; selected UML/ArchiMate definition/relation distinctions; OpenTelemetry/Lamport causal links; annotated document as text/source equivalent; BPMN-like finite gateway walkthroughs; guided scenario as novice mode.
- **KILL:** universal graph as primary; token-as-status; autoplay causality; nested orchestrator glyphs; ownerless status colors; unbounded loops.
- **DEFER:** full formal-notation export, live replay, runtime observations, dynamic topology, sophisticated animation, accessibility claims, and human-comprehension claims.

## Reviewer-gate handoff

- **Precedent/ownership gate:** reused patterns are explicitly classified; no Inventory no-match is treated as novelty, and Inventory grants no authority.
- **Non-vacuity gate:** the three traces distinguish Work from pipeline-as-Work, routing from judgment, sidecar from control, retry from terminal failure, command from event, and bus/journal from executor.
- **Definitional gate:** the visual vocabulary retains every required non-collapse pair: definition/run, leaf/composite, containment/authority, command/event, transport/persistence/decision/execution, cursor/domain state, acceptance/confirmation, gate/effect permission, main/sidecar, structural edge/temporal occurrence, and semantic source/projection.

## Receipt

```json
{
  "action_id": "spawn-0004",
  "role": "view-synthesizer",
  "status": "pass",
  "validation": "pass",
  "blockers": [],
  "artifacts": [],
  "started_at": "2026-08-04T17:32:32-03:00",
  "finished_at": "2026-08-04T17:34:12-03:00"
}
```
