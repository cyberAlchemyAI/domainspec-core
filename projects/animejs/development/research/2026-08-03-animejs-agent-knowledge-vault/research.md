# Anime.js Agent Knowledge Vault — Explorer Transcript

Dispatch: `2026-08-03-animejs-agent-knowledge-vault`
Run: `animejs-vault-run-001`
Evidence contract: `exact-binding`
Posture: verbatim explorer returns; not synthesis, ontology admission, runtime proof, or publication.

## Agent 1 — Feynman, Richard — Official source explorer

### Explorer result — official-source coverage manifest

**Binding.** `official-source-explorer` / `research`; dispatch `2026-08-03-animejs-agent-knowledge-vault`; run `animejs-vault-run-001`; wave `explorers`; step `s1`. Read-only. Observed 2026-08-03.

**Version/source anchor.** Official repository tag **v4.5.0** resolves to commit `2c9cf8ea00329f6768c7d7902252ed977d75ce42` (also current `master` when checked). Canonical immutable code bindings use:

- `https://github.com/juliangarnier/anime/tree/2c9cf8ea00329f6768c7d7902252ed977d75ce42/src/<module>`
- `.../tests`, `.../examples`, and `.../package.json`
- v4.5.0 package exports include root plus `timer`, `animation`, `timeline`, `animatable`, `draggable`, `scope`, `engine`, `events`, `layout`, `easings` (and submodules), `utils`, `svg`, `text`, `waapi`, `adapters`, `adapters/three`.

`https://animejs.com/documentation/` is live and mutable. Its landing navigation names 16 families but does not list descendants. A same-day DOM-link extraction found **418 unique `/documentation/...` routes**; exact selector for every route below is `a[href="/documentation/<path>"]`, and the route’s `h1`/page title is the human selector. All routes are `observed: documentation-navigation`; only top-level call signatures noted below were individually content-observed. Do not infer a runtime witness from an embedded example.

| Family / canonical base | Routes | Export / return boundary | Topic disposition |
|---|---:|---|---|
| `/getting-started` | 5 | installation/import guidance | `installation`, `module-imports`, `using-with-vanilla-js`, `using-with-react` |
| `/timer` | 32 | `createTimer(parameters)` → `Timer`; root or `animejs/timer` | playback settings; callbacks; methods; properties |
| `/animation` | 70 | `animate(targets, parameters)` → `JSAnimation`; root or `animejs/animation` | targets, animatable properties, tween values/parameters, keyframes, playback, callbacks, methods, properties |
| `/timeline` | 49 | `createTimeline(parameters)` → `Timeline`; root or `animejs/timeline` | composition and playback surface |
| `/animatable` | 11 | `createAnimatable(targets, parameters)` → `Animatable`; root or `animejs/animatable` | frequent numeric / number-array property updates, settings, methods, properties |
| `/draggable` | 46 | `createDraggable(target, parameters)` → `Draggable`; root or `animejs/draggable` | axes, settings, callbacks, methods, properties |
| `/layout` | 29 | `createLayout(root, parameters)` → `AutoLayout`; root or `animejs/layout` | layout states, usage recipes, methods/properties/settings |
| `/scope` | 14 | `createScope(parameters)` → `Scope`; root or `animejs/scope` | root/media/defaults, registration/addition, batch refresh/revert |
| `/events` | 33 | `events.onScroll` / `onScroll`; root or `animejs/events` | ScrollObserver settings, threshold/mode, callbacks, methods/properties |
| `/svg` | 4 | `svg` namespace / `animejs/svg` | `morphTo`, `createDrawable`, `createMotionPath` |
| `/text` | 38 | `text` namespace / `animejs/text` | `splitText`, `scrambleText`, settings/callbacks/methods/properties |
| `/utilities` | 43 | `utils` namespace / `animejs/utils` | stagger, target/value/time/math/random utilities; chainable utilities |
| `/easings` | 7 | `easings` namespace / `animejs/easings` | built-ins, cubic bezier, linear, steps, irregular, spring |
| `/web-animation-api` | 17 | `waapi.animate(targets, parameters)` → `WAAPIAnimation`; `animejs/waapi` | native-WAAPI differences, feature/choice guidance, `convertEase` |
| `/engine` | 13 | `engine` root export | global timing engine parameters/methods/properties/defaults |
| `/adapters` | 7 | `registerAdapter`; `animejs/adapters`, side-effect `animejs/adapters/three` | custom target adaptation and built-in Three.js support |

**Complete descendant-route coverage contract.** The following route groups enumerate all descendants found in the live navigation. A vault importer may expand each compact group into one `SourceRecord` per slash-delimited route, with the exact selector rule above; topic kind is derived by the parent segment (`*-settings`, `*-callbacks`, `*-methods`, `*-properties`, `usage`, etc.), not guessed semantic behavior.

- `getting-started`: `installation`, `module-imports`, `using-with-vanilla-js`, `using-with-react`.

- `timer`: `timer-playback-settings/{alternate,autoplay,delay,duration,framerate,loop,playback-loopdelay,playbackrate,reversed}`; `timer-callbacks/{onbegin,oncomplete,onloop,onpause,onupdate,then}`; `timer-methods/{alternate,cancel,complete,pause,play,reset,restart,resume,reverse,revert,seek,stretch}`; `timer-properties`.

- `animation`: `targets/{array-of-targets,css-selector,dom-elements,javascript-objects}`; `animatable-properties/{css-properties,css-transforms,css-variables,html-attributes,javascript-object-properties,svg-attributes}`; `tween-value-types/{color-function-value,color-value,css-variable,function-based,numerical-value,relative-value,unit-conversion-value}`; `tween-parameters/{composition,delay,duration,ease,from,modifier,to}`; `keyframes/{duration-based-keyframes,percentage-based-keyframes,tween-parameters-keyframes,tween-values-keyframes}`; `animation-playback-settings/{alternate,autoplay,delay,duration,framerate,loop,persist,playback-loopdelay,playbackease,playbackrate,reversed}`; `animation-callbacks/{onbeforeupdate,onbegin,oncomplete,onloop,onpause,onrender,onupdate,then}`; `animation-methods/{alternate,cancel,complete,pause,play,refresh,reset,restart,resume,reverse,revert,seek,stretch}`; `animation-properties`.

- `timeline`: `add-timers`, `add-animations`, `sync-waapi-animations`, `sync-timelines`, `call-functions`, `time-position`; `timeline-playback-settings/{alternate,autoplay,defaults,delay,framerate,loop,playback-loopdelay,playbackease,playbackrate,reversed}`; `timeline-callbacks/{onbeforeupdate,onbegin,oncomplete,onloop,onpause,onrender,onupdate,then}`; `timeline-methods/{add,alternate,call,cancel,complete,init,label,pause,play,refresh,remove,reset,restart,resume,reverse,revert,seek,set,stretch,sync}`; `timeline-properties`.

- `animatable`: `animatable-settings/{duration,ease,modifier,unit}`; `animatable-methods/{getters,setters,revert}`; `animatable-properties`.

- `draggable`: `draggable-axes-parameters/{x,y,mapto,modifier,snap}`; `draggable-settings/{container,containerfriction,containerpadding,cursor,dragspeed,dragthreshold,maxvelocity,minvelocity,releasecontainerfriction,releasedamping,releaseease,releasemass,releasestiffness,scrollspeed,scrollthreshold,trigger,velocitymultiplier}`; `draggable-callbacks/{onafterresize,ondrag,ongrab,onrelease,onresize,onsettle,onsnap,onupdate}`; `draggable-methods/{animateinview,disable,enable,refresh,reset,revert,scrollinview,setx,sety,stop}`; `draggable-properties`.

- `layout`: `common-auto-layout-gotchas`, `layout-id-attribute`, `layout-callbacks`, `layout-settings/{children,delay,duration,ease,properties}`, `states-parameters/{enterFrom,leaveTo,swapAt}`, `layout-methods/{animate,record,revert,update}`, `layout-properties`; `usage/{animate-modal-dialog,css-display-property-animation,dom-order-change-animation,enter-layout-animation,exit-layout-animation,specifying-a-root,staggered-layout-animation,swap-parent-animation}`.

- `scope`: `scope-parameters/{defaults,mediaqueries,root}`, `add-constructor-function`, `register-method-function`, `scope-methods/{add,addonce,keeptime,refresh,revert}`, `scope-properties`.

- `events`: `onscroll`; `onscroll/scrollobserver-settings/{axis,container,debug,repeat,target}`; `onscroll/scrollobserver-thresholds/{min-max,numeric-values,positions-shorthands,relative-position-values}`; `onscroll/scrollobserver-synchronisation-modes/{eased-scroll,method-names,playback-progress,smooth-scroll}`; `onscroll/scrollobserver-callbacks/{onenter,onenterbackward,onenterforward,onleave,onleavebackward,onleaveforward,onresize,onsynccomplete,onupdate}`; `onscroll/scrollobserver-methods/{link,refresh,revert}`; `onscroll/scrollobserver-properties`.

- `svg`: `morphto`, `createdrawable`, `createmotionpath`.

- `text`: `splittext`, `splittext/html-template`, `splittext/split-parameters/{class,clone,wrap}`, `splittext/textsplitter-settings/{accessible,chars,debug,includespaces,lines,words}`, `splittext/textsplitter-methods/{addeffect,refresh,revert}`, `splittext/textsplitter-properties`; `scrambletext`, `scrambletext/scrambletext-parameters/{chars,cursor,delay,duration,ease,from,override,perturbation,revealdelay,revealrate,reversed,seed,settleduration,settlerate,text}`, `scrambletext/scrambletext-callbacks/onchange`.

- `utilities`: `stagger`, `dollar-sign`, `get`, `set`, `clean-inline-styles`, `remove`, `sync`, `createtimekeeper`, `random`, `createseededrandom`, `random-pick`, `shuffle`, `round`, `clamp`, `snap`, `wrap`, `map-range`, `lerp`, `damp`, `round-pad`, `pad-start`, `pad-end`, `deg-to-rad`, `rad-to-deg`, `chain-able-utility-functions`; `stagger/{values-staggering,time-staggering,timeline-positions-staggering,stagger-value-types/{numerical-value,range-value},stagger-parameters/{stagger-ease,stagger-from,stagger-grid,stagger-grid-axis,stagger-jitter,stagger-modifier,stagger-reversed,stagger-start,stagger-total,stagger-use}}`.

- `easings`: `built-in-eases`, `cubic-bezier-easing`, `linear-easing`, `steps-easing`, `irregular-easing`, `spring`.

- `web-animation-api`: `when-to-use-waapi`, `hardware-accelerated-animations`, `waapi-convertease`; `api-differences-with-native-waapi/{direction,easing,finished,iterations}`; `improvements-to-the-web-animation-api/{default-units,function-based-values,individual-css-transforms,individual-property-parameters,multi-targets-animation,sensible-defaults,spring-and-custom-easings}`.

- `engine`: `engine-parameters/{fps,pauseondocumenthidden,precision,speed,timeunit-seconds-milliseconds}`, `engine-methods/{pause,resume,update}`, `engine-properties`, `engine-defaults`.

- `adapters`: `threejs-adapter/{materials-and-uniforms,threejs-adapter-common-gotchas,threejs-instanced-and-batched-meshes,threejs-object-property-adapter,threejs-transforms-adapter}`.

**Examples/source disposition.** The pinned repository contains examples for additive animations, grid staggering, cursor animatable, auto-layout, canvas, draggable, scope/onScroll, SVG, text, Three.js, and timelines. Bind an example as `ExampleSource`, with `evidence_status: source-observed-not-runtime-executed`; never promote it to behavioral proof. Bind source module and matching tests separately as `code-observed` / `test-present-not-executed`.

**Important distinctions and residue.**

- JS `animate()` and `waapi.animate()` are not interchangeable: the docs call WAAPI smaller and less feature-complete, and mark JS-only versus WAAPI-only features. Keep distinct API-symbol nodes, capability fields, and versioned source links.
- Top navigation omits all 402 descendant pages; the vault must crawl/link-validate descendants, not merely preserve the 16 family labels.
- Canonical page URLs redirect from no-trailing-slash requests to trailing-slash routes; normalize canonical URL with `/`.
- `Text` and `Adapters` are visibly marked “NEW”; `registerAdapter`/Three.js is explicitly part of v4.5.0 release material. Preserve `introduced_or_currently_observed`, not a guessed introduction version.
- Official v3→v4 material is the repository wiki page `https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4`; it is a migration source, not proof that every old v3 snippet is invalid without a matching mapping.
- The live docs site can drift independently of tag `v4.5.0`; every mutable-page record needs observed timestamp, content digest, canonical URL, and pinned-repository version context. Current website navigation is not itself a release-locked snapshot.
- No runtime reproduction, accessibility proof, performance proof, production integration, or learned work episode was performed. Issue #1105 remains unadmitted/unverified and excluded.

```json
{
  "action_id": "spawn-0001",
  "dispatch_id": "2026-08-03-animejs-agent-knowledge-vault",
  "run_id": "animejs-vault-run-001",
  "wave_id": "explorers",
  "step_id": "s1",
  "role": "official-source-explorer",
  "capability_ref": "research",
  "status": "pass",
  "artifacts": [
    {
      "ref": "projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/receipts/explorer-official-source.json",
      "state": "proposed-return-only",
      "content": "418-route official Anime.js documentation coverage manifest; no file written"
    },
    {
      "ref": "https://github.com/juliangarnier/anime/tree/2c9cf8ea00329f6768c7d7902252ed977d75ce42",
      "state": "observed",
      "content": "official v4.5.0 tag/current-master source anchor"
    }
  ],
  "validation": {
    "official_sources_only": "pass",
    "live_documentation_routes": 418,
    "top_level_families": 16,
    "version_anchor": "v4.5.0 -> 2c9cf8ea00329f6768c7d7902252ed977d75ce42",
    "repository_mutation": "none",
    "runtime_claims": "none"
  },
  "blockers": [
    "Live documentation is not tag-pinned; require future digest/crawl receipt for drift detection.",
    "Descendant link discovery is navigation-observed; individual semantic headings beyond sampled top-level pages remain source-addressable but not individually parsed.",
    "No executed example/test/runtime witness."
  ],
  "started_at": "2026-08-03T00:00:00-03:00",
  "finished_at": "2026-08-03T00:00:00-03:00"
}
```

## Agent 2 — Mac Lane, Saunders — Ontology precedent explorer

## Ontology and model precedent explorer result

**Binding:** dispatch `2026-08-03-animejs-agent-knowledge-vault`; run `animejs-vault-run-001`; wave `explorers`; step `s1`; action `spawn-0002`; role `ontology-precedent-explorer`; pooled identity `Mac Lane, Saunders`; capability `research`; mode `explore`; mutation policy `read-only`.

**Evidence posture:** I reconciled the machine Inventory packet with live repository paths, file contents, filesystem dates, Git history/status, validators, fixtures, and receipts. Inventory remained a discovery read model only. The scoped worktree was already dirty: the Unified Ontology Canvas is untracked; Augmentor visualization additions and ontology-experiment canvas modules are modified/untracked; the learning-graph Invoke package and tower review are untracked. I did not mutate or attribute those bytes.

### Recent-model manifest

| Model and classification | Exact live selector and date/evidence posture | Purpose and shapes | Reusable for Anime.js | Typed negatives / anti-patterns |
|---|---|---|---|---|
| **Candidate graph evaluator prototype — validated executable prototype, not an admitted ontology** | `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype/`; selectors `src/contracts/candidate-v1.mjs`, `src/evaluator/edge-grammar.mjs`, `src/evaluator/grounding.mjs`, `src/evaluator/policy-disposition.mjs`, `src/projection/research-lineage.mjs`, `src/evidence/run-writer.mjs`, `fixtures/`, `test/`; created 2026-07-27; private package `@cyberalchemy/ontology-candidate-graph-prototype@0.1.0`. | Closed candidate records: node kinds `session`, `discovery`, `research`, `findings`; directed evidence-bound edges; relation candidates; separate grammar, grounding, policy disposition, projection, canonical JSON, digest map, terminal receipt, write-isolation and determinism tests. Receipt bundles contain result, projection, digest map, artifact inventory, SHA-256s, run metadata, and `authority_effect:none`. | Reuse closed shapes, repository-relative selectors, exact source digests, endpoint/cardinality checks, forbidden inverse storage, explicit grounding-cycle rejection, named-policy evaluation, canonical serialization, exclusive receipt-last writes, determinism and write-isolation tests. Generalize node vocabulary rather than copying its research-lineage kinds. | A validator pass is finite prototype evidence, not ontology admission. Do not let a session become evidence, store read inverses, permit unsupported edge triples, infer grounding from reachability alone, or let projection/receipt creation promote knowledge. |
| **Augmentor Unified-Agent Ontology — validated candidate-local ontology package; visualization is a later generated view** | `projects/augmentor/ontology/unified-agent/`; selectors `profile.json`, `sources.json`, `schemas/{node,relation,view}.schema.json`, `nodes/nodes.json`, `relations/relations.json`, `views/{experience,runtime,knowledge,authority-bridge}.json`, `residue.json`, `fixtures/`, `scripts/validate.mjs`, `receipts/validation-receipt.json`; package created 2026-07-29. Receipt: pass, 21 bound sources, 18 nodes, 21 relations, 4 views, 7 residue. `ontology-visualization.html`, builder/template/tests and README update are dirty 2026-08-03 generated-view work, not a new ontology. | Source-bound model of meaning, runtime, knowledge, and authority-bridge planes. Nodes carry confidence and challenge contracts; relations are directed and owner-routed; views are interpretive branches; fixtures include valid boundaries, authority-effect violation, and value cycle; receipt binds profile/source/node/relation/residue/view digests. | Strongest package-tree precedent: profile, sources, schemas, nodes, relations, multiple task-facing views, residue, positive/negative fixtures, validator, tests, digest receipt, generated human projection. For Anime.js, adapt views to documentation topology, API/runtime semantics, recipes, evidence, and work lessons. | Do not collapse user experience, runtime execution, retrieval knowledge, or authority. A `JudgmentReceipt` is not approval/effect. Generated visualization does not become source authority. Current receipt predates dirty visualization bytes, so it cannot validate them. No routing, durable memory, reasoning, promotion, release, or production claim follows. |
| **Body War Business Ontology — validated candidate-local ontology package with populated/generated views** | `projects/body-war/ontology/business/`; selectors `profile.json`, `sources.json`, `schemas/`, `nodes/`, `relations/relations.json`, `views/business.json`, `lifecycle-policies/`, `residue.json`, `fixtures/`, `scripts/validate.mjs`, `receipts/validation-receipt.json`; created/expanded 2026-07-29 through 2026-07-30. Receipt: pass, 34 sources, 237 nodes, 231 relations, 11 lifecycle policies, 6 residue items. | Large typed business-meaning graph. Project-local `business_kind` remains separate from vault node type; branch is an interpretive view; lifecycle policies are separate from node classification and authority. Generated Markdown/HTML/SVG atlases and browser receipts are populated views over node/relation authority. Validator checks closed shapes, source digests, coverage, endpoints, transitions, value cycles, and executable-logic prohibition. | Reuse the separation of ontology records, lifecycle/version policies, generated review/query views, source-digest coverage, diagnostic codes, explicit isolates, negative controls, and owner-routed residue. Anime.js can use coverage manifests and generated topic/API/task views without making those views canonical. | Do not invent a universal “related” edge, mix lifecycle with node type, embed executable advice in ontology data, treat a branch/view as an owner or promotion route, or infer documentation truth from visual coverage. Large populated graphs require explicit required-coverage and missing-source diagnostics. |
| **Architecture Property Ontology Experiment — corrected executable experiment, not a production ontology or real-source conformance system** | `projects/domainspec-v2/development/implementation-conformance/ontology-experiment/`; selectors `ontology.json`, `domain-meta-types.projection.json`, `profiles/*.profile.json`, `examples/typescript-observed-facts.json`, `examples/typescript-evaluation.expected.json`, `validate-ontology.mjs`, `VALIDATION-REPORT.md`; corrected 2026-07-31. Git commit evidence: `2cbb0f164eb1625995e32c2c5f1e6dff6e66c7a7`, 2026-07-31. Report: ontology pass; intentionally broken sample architecture fail as expected; 12 concepts, 17 properties, 4 relation definitions, 4 operators, 3 language projections, 42 resolved constraints, 30 assertions, 8 reproduced findings. | Separates canonical meta-type projection, candidate architecture ontology, profiles/expectations, supplied observations, and evaluator findings. Concepts/properties/relations carry owner routes and forbidden-inference rules. Profiles specialize portable constraints; supplied facts and expected findings are fixtures. | Reuse the layered fact model: official Anime.js concept/source fact → version/profile expectation → observed work episode/runtime evidence → explainable finding. Reuse typed properties, generic operators, profile composition, expected-negative fixtures, explicit unsupported adapter surfaces, and drift triggers. | File shape, name, return type, example, or profile expectation does not prove semantic identity or runtime behavior. The observed facts are hand-authored; no TypeScript/Python/Rust source adapter ran. A failing negative fixture is a successful validator witness, not package failure. |
| **Unified Ontology Canvas — implemented deterministic presentation projection/view, not a distinct ontology** | Planning package: `projects/domainspec-v2/development/implementation-conformance/unified-ontology-canvas/`; exact model implementation lives in sibling experiment selectors `unified-canvas-model.mjs`, `unified-canvas-layout.mjs`, `validate-unified-canvas-{model,layout,browser}.mjs`, `architecture-ontology-view.html`. The planning folder is untracked. SWU evidence: `.../work-pack/results/SWU-UOC-004P-RESULT.md`, completed 2026-08-01T23:04:10-03:00. Validated prototype counts: 95 nodes, 147 edges, 20 explicit gaps, five bands, structural replay, zero overlaps/interior crossings, browser checks pass. | Pure unified projection across Meaning → Realization → Expectation → Observation → Explanation. It keeps constraints, facts, findings, provenance, gaps, and source-family identities distinct; visibility/focus changes presentation state, not graph identity. Browser receipt exposes counts and `prototype-unverified`; the checksum-free browser design deliberately makes no integrity claim. | Reuse one immutable projection with namespaced stable IDs, explicit source-family/role metadata, typed cross-band bridges, structured navigator parity, deterministic layout, gap nodes, profile/version focus, and no-external-request browser validation. Useful as an Anime.js consultation view over separately owned vault data. | Do not count it as another ontology, infer semantics from spatial proximity, hide unsupported nodes to imply completeness, recompute source truth in the browser, or treat structural replay as cryptographic integrity. It is local candidate static-browser evidence only; accessibility and comprehension remain separate. |
| **Learning Graph and Next-Route Guide — accepted exact-bound research proposal / regenerable learning projection, not implemented graph semantics** | `cyberAlchemy-v2/development/research/2026-08-01-learning-graph-next-route-guide/findings.md`; exact candidate records in `receipts/learning-graph-synthesis-revised.json`; evidence closure `receipts/evidence-closure.json`; audit `receipts/learning-graph-audit.json`; accepted 2026-08-01. The subsequent `invoke/` package and `LEARNING-GRAPH-PROTOTYPE.html` are untracked planning/prototype bytes, not admission. | Projection over separately owned semantic concept, profile expectation, supplied observation, evaluator result, session question, evidence gap, and non-executing route suggestion. Core query loop: orient, focus, inspect exact bindings, expose gap, revise broad question, suggest a bounded owner route. Explicit abstention protects absent current binding/native adapter/owner admission. | Direct precedent for Anime.js agent consultation: keep documentation facts, examples, recipes, work attempts/outcomes, lessons, gaps, and recommendations distinct; bind lessons to work episodes and invalidation; generate revised verification questions and non-executing repair routes; preserve exact evidence pointers and abstention. | Do not call it a knowledge brain, learning proof, or new ontology. `session-focuses-on` does not mean understanding; a finding does not prove identity; absence of a finding is not positive proof; route suggestion does not select or execute work. Human comprehension, accessibility, real-source adapter behavior, and owner admission remain unproven. |
| **Tower-to-exam learning graph seed plus accepted review — research proposal under repair, not a created package or admitted learning graph** | Seed: `/home/vrondelli/projects/direito-romano/development/refinement-runs/20260802T013629Z-tower-exam-learning-graph/REFINE-SEED-PROPOSAL.md`; review: `ops/development/2026-08-02-tower-exam-learning-graph-review/findings.md`, `REVIEW-SYNTHESIS.md`, `DISPATCH-CLOSEOUT.md`; review completed 2026-08-02 posture, folder untracked. Verdict `FIX`; evidence-routing behavior survives, doctrinal scoring blocked. | Seed proposed tower knowledge plus learner overlay. Review repairs it toward five durable families—`SourceSnapshot`, `TowerSnapshot`, typed `KnowledgeRecord`, `EvidenceAnchor`, `StudyRoute`—four typed relation families, and a separate learner-session overlay. Required shapes include logical/snapshot/content identities, two-layer provenance, exact `NextQuestion`, deterministic abstention, and projection-side IDs where source artifacts lack them. | Reuse separation of source snapshot from learner overlay; exact source/tower provenance; evidence taxonomy and verification requirements; `NextQuestion` with missing element, target artifact, page/residue, reason, and stop condition; deterministic unsupported-question abstention; content-leakage validator. | Do not treat topic labels/order as semantic edges, two-source agreement as consensus, OCR as authority, orientation-only locators as answer support, generic “study more” as a route, or DomainSpec prototype content as Anime.js knowledge. No doctrinal/task correctness scoring without exact answer evidence; no mastery/comprehension claim. |

### Cross-model reusable minimum for the Anime.js vault

1. **Package boundary:** candidate-local private profile with `authority_effect:none`, `release_admission:not-granted`, explicit owners, blocked outputs, claim ceiling, and residue.
2. **Source/evidence layer:** immutable official-source identity, exact URL/path plus selector or structured pointer, version context, digest where bytes are captured, evidence class, proof status, invalidation trigger, and copyright-safe paraphrase rather than copied documentation.
3. **Semantic layer:** keep `DocumentationTopic`, `APISymbol`, `SourceFact`, `Example`, `Recipe`, `WorkEpisode`, `Attempt`, `Outcome`, `Lesson`, `Inference`, `Recommendation`, `VersionContext`, and `EvidenceGap` non-collapsing. Every relation needs endpoint types, direction, evidence refs, owner route, effect, cycle policy, and forbidden inference.
4. **Views and queries:** generate documentation-coverage, API, task-recipe, migration/version, work-lesson, and unresolved-gap views from the owned records. Views are disposable/populated projections. Queries must return evidence and abstain on missing, conflicting, stale, or merely proposed material.
5. **Validation:** closed schemas; unique stable IDs; exact endpoint resolution; source/selector/digest checks; complete declared documentation-topic disposition; version freshness; cycle and authority guards; deterministic generation; positive, negative, stale-version, conflicting-source, copied-prose, unverified-issue, missing-work-episode, and abstention fixtures; digest-bound terminal receipt.
6. **Agent-learning boundary:** a lesson requires a named work episode, attempt, observed outcome, evidence, applicability/version scope, invalidation rule, and review owner. Advice without that chain remains inference or recommendation, never “learned fact.”

### Explicit exclusions

- Inventory entries themselves: discovery pointers, not source proof or admission.
- `akashic-periodic-table-graph-schema` research: loop-ceiling research result, no approved/implemented ontology; retain only source/claim and no-derived-edge warnings.
- `ontological-way-clear` readiness model: purpose-specific evaluation-query proposal, not a documentation vault.
- Body War OEW UX/UI quality loop: UX audit protocol, not a new ontology.
- Unified Ontology Canvas browser-neutral digest strategy: strategy evidence, not proof of a completed/admitted canvas.
- Generated Augmentor/Body War HTML/SVG views as separate ontologies: they are projections of owned records.
- `architecture-ontology-view.html` as semantic authority: it is a view over candidate ontology and supplied fixtures.
- Learning Graph Invoke prototype as an admitted learning model: untracked candidate bytes; interaction precedent only.
- Tower graph seed/review as a validated implementation: accepted FIX guidance only.
- Suggested-track proof and staging/output copies under Body War development runs: earlier proof/material copies, not additional current ontology owners.
- Anime.js issue/community guidance, including issue 1105: proposal/unverified precedent unless separately admitted by an official owner.
- Any claim of publication, promotion, runtime integration, semantic truth, accessibility, performance, learning effectiveness, release, deployment, or production readiness.

### Unresolved recent-model gaps

- The declared recent scope is not globally exhaustive: Inventory coverage is partial, and a repository-wide date scan finds staging/output copies and proofs whose ownership relationship would require a separate provenance audit.
- The live Unified Ontology Canvas and several visualization/prototype additions are dirty or untracked; their current bytes are not validated by Git history, and older receipts must not be generalized across later modifications.
- No single recent package yet combines documentation topology coverage, API/version semantics, task recipes, evidence-bound work episodes, lessons, queries, views, drift handling, and safe abstention.
- No existing Anime.js source snapshot, topic/page manifest, selector contract, release/tag/commit binding, work episode, validated lesson, or copyright-handling receipt exists in the scoped evidence.
- No common cross-package contract has yet normalized source selector types, version invalidation, work-episode/lesson evidence, generated-view freshness, and query receipts.
- Human comprehension and accessibility receipts are absent or explicitly flagged across the relevant learning/view precedents.
- The tower model still needs repaired stable identity, exact provenance, page-local fixtures, and a deterministic validator before it becomes an implementation precedent.
- Current Git evidence confirms one ontology-experiment commit, but several other recent package histories are mixed with dirty/untracked bytes; filesystem dates establish recency, not authorship, admission, or canonicality.

## Proposed normalized action receipt

```json
{
  "action_id": "spawn-0002",
  "dispatch_id": "2026-08-03-animejs-agent-knowledge-vault",
  "run_id": "animejs-vault-run-001",
  "wave_id": "explorers",
  "step_id": "s1",
  "role": "ontology-precedent-explorer",
  "capability_ref": "research",
  "status": "pass",
  "artifacts": [
    {
      "ref": "projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/receipts/explorer-ontology-precedent.json",
      "posture": "proposed-output-ref-only",
      "written": false
    },
    {
      "ref": "bounded-explorer-return",
      "posture": "returned-to-parent-for-verbatim-research-md-inclusion",
      "written": false
    }
  ],
  "validation": {
    "result": "pass",
    "method": [
      "live filesystem reconciliation",
      "scoped Git status and history inspection",
      "package profile/schema/model/validator/fixture/receipt inspection",
      "research finding, evidence-closure, audit, seed, and review inspection"
    ],
    "inventory_posture": "discovery-read-model-only",
    "mutation_check": "no writes performed",
    "scoped_dirty_status_sha256": "204c18469afced81e23402c813075823ecb77204cc065ef0296c047e1a80aec5",
    "claim_ceiling": "Defensible recent local precedent manifest for the declared scope; no ontology admission, Anime.js coverage, implementation, publication, promotion, release, deployment, or production-readiness claim."
  },
  "blockers": [],
  "started_at": "2026-08-03T13:15:00-03:00",
  "finished_at": "2026-08-03T13:23:48-03:00"
}
```

## Agent 3 — Ahrens, Sönke — Agent lessons explorer

## Explorer result — task-centered vault contract

### Evidence classes and admissibility

- `DocumentationGuidance`: official documentation URL + heading/anchor; prescriptive/API guidance, not a runtime witness.
- `SourceFact`: official repository file at an immutable commit SHA + path + symbol/range; implementation/export fact only.
- `TestObserved`: named official test at immutable SHA, with command/environment/result; proves only that tested behavior.
- `ExecutedWitness`: a future local run with immutable input, version context, environment, command, output, and verifier. None exists in this exploration.
- `Inference`: explicitly linked reasoning from one or more above; never upgrades to a fact.
- `Recommendation`: project-specific choice with rationale and constraints; never represented as Anime.js guidance.
- `UnverifiedProposal`: community material, including issue #1105; retrieval-only and cannot support a recipe, Fix, or Lesson without independent admissible evidence.

Every fact-like record needs `source_kind`, canonical URI, selector/path, `captured_at`, `version_context`, content digest, and status (`documented|source-derived|test-observed|executed|inferred|unverified`). Current live source evidence establishes package version `4.5.0` and its subpath export map, but the vault must pin a commit SHA before admitting source or test records. [Official package manifest](https://raw.githubusercontent.com/juliangarnier/anime/master/package.json)

### Exact official bindings and recipes

| Task | Consult in order | Bounded recipe / abstention |
|---|---|---|
| Setup/imports | [`Getting started`](https://animejs.com/documentation/getting-started/) → [repository README](https://github.com/juliangarnier/anime#usage) → manifest `exports` | Record installed package lock/version; select `animejs` or an exported subpath; named `animate` import is documented. Do not infer a project’s bundler, CDN, or installed version. |
| Basic animation | [`Animation`](https://animejs.com/documentation/animation/) heading “Animation” / “Parameters” | Use `animate(targets, parameters)`; returned type is documented as `JSAnimation`. For the smaller WAAPI implementation, route to the WAAPI recipe rather than assuming parity. |
| Timelines | [`Timeline`](https://animejs.com/documentation/timeline/) heading “Timeline” / “Methods” | `createTimeline(parameters)` then choose `add`, `sync`, `call`, or `label` according to the documented composition need. Record exact time-position syntax consulted; no claim that a composition works until a witness exists. |
| Scope/framework cleanup | [`Scope`](https://animejs.com/documentation/scope/) heading “Scope”; [`Utilities`](https://animejs.com/documentation/utilities/) `cleanInlineStyles()` | Consult Scope for custom root/media-query/batch-revert lifecycle and Utilities for cleanup. A framework-specific unmount fix requires a local witness; do not promote the scope example to framework proof. |
| Draggable/layout | [`Draggable`](https://animejs.com/documentation/draggable/) heading “Draggable”; [`Layout`](https://animejs.com/documentation/layout/) “Creating a layout”, “Animating a layout”, “Common gotchas” | Use `createDraggable(target, parameters)` for DOM targets. For layout, create layout and use `update(cb)` or record/animate around the DOM change. Keep layout behavior separate from performance claims. |
| Events | [`Events`](https://animejs.com/documentation/events/) heading “Events” / `onScroll` | Retrieve `events.onScroll` or direct/subpath import binding. Do not infer scroll accessibility, event teardown, or browser support without the relevant official subsection/source/test. |
| SVG/text | [`SVG`](https://animejs.com/documentation/svg/) headings `morphTo`, `createDrawable`, `createMotionPath`; [`Text`](https://animejs.com/documentation/text/) headings `splitText`, `scrambleText` | Select helper by task (morph, line drawing, motion path, split/scramble text). Text DOM/accessibility effects are evidence gaps unless a test/witness covers them. |
| Utilities/easings | [`Utilities`](https://animejs.com/documentation/utilities/) individual method heading; [`Easings`](https://animejs.com/documentation/easings/) relevant family/selector | Store utility/ease selection as documentation guidance. `stagger`, selection/get/set, cleanup, numeric helpers, and easing functions must retain their specific selector, not a generic “utilities” citation. |
| JS versus WAAPI | [`Animation`](https://animejs.com/documentation/animation/) “WAAPI powered animations”; [`Web Animation API`](https://animejs.com/documentation/web-animation-api/) “When to use”, “API differences”, `convertEase()` | Decision: use `animate` when required features are JS-only; consider `waapi.animate` only after checking documented differences/pitfalls. Docs identify 10KB JS vs 3KB WAAPI and reduced WAAPI feature coverage; neither is a measured project-performance result. |
| Engine/adapters | [`Engine`](https://animejs.com/documentation/engine/) “Execution order”; [`Adapters`](https://animejs.com/documentation/adapters/) “Built-in adapters” / “Custom adapters” | Engine priority governs documented engine ordering. Three.js adapter is a side-effect import; custom adapters use `registerAdapter`, target adapters or property resolvers. Pin source/types before recording implementation details. |
| Debugging | Target recipe → current package version → [v3→v4 guide](https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4) | Form a `Symptom`, capture attempted version/import/API spelling, then diagnose only from evidence. No known failure is created by this research. |
| Performance | WAAPI guide “Hardware-acceleration” and “When to use”; target API docs | Retrieval may expose documented considerations. Abstain on “faster”, dropped frames, bundle impact, or layout cost until a project-controlled performance witness exists. |
| Accessibility/reduced motion | [`Scope`](https://animejs.com/documentation/scope/) example media query `reduceMotion` | The official example includes `(prefers-reduced-motion)` and varies duration. This supports a documentation-guidance record only; accessibility conformance, user outcome, and product policy require separate evidence. |
| v3 migration | [official migration wiki](https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4) headings “Animation”, “Targets”, parameter headings | Version-gate before applying: global `anime` → named `animate`, targets move to first argument, `easing` → `ease`, `value` → `to`, `direction` → `reversed`/`alternate`, and loop semantics change. Do not mass-rewrite without a version-local scan and witness. |

The root documentation index is the coverage gate for Timer, Animation, Timeline, Animatable, Draggable, Layout, Scope, Events, SVG, Text, Utilities, Easings, WAAPI, Engine, and Adapters; each recipe must retain its descendant heading, not merely the index. [Official documentation index](https://animejs.com/documentation/)

### Work-episode model

`WorkEpisode` is the append-only envelope for one bounded implementation/debugging effort; it is not a lesson and not proof that production behavior changed.

- `WorkEpisode(id, task_id, version_context_id, started_at, closed_at?, scope, status)`
- `Task(id, intent, target_kind, acceptance_criterion?, constraints)`
- `Attempt(id, episode_id, ordinal, change_description, evidence_ids[])`
- `Symptom(id, observed_statement, witness_id?)`
- `Diagnosis(id, claim, confidence, evidence_ids[])`
- `Fix(id, proposed_change, evidence_ids[])`
- `Outcome(id, status: succeeded|failed|inconclusive|not-run, witness_ids[])`
- `Lesson(id, conditional_guidance, confidence, status: candidate|verified|invalidated|superseded, evidence_ids[])`
- `Evidence(id, class, source_identity, selector, digest, captured_at, assertion_scope)`
- `VersionContext(id, anime_package_version, immutable_commit?, lockfile_digest?, runtime/browser?, framework?, OS?)`

Typed relations:

- `WorkEpisode --addresses--> Task`
- `WorkEpisode --usesVersion--> VersionContext`
- `WorkEpisode --contains--> Attempt`
- `Attempt --observes--> Symptom`
- `Attempt --supports|contradicts--> Diagnosis`
- `Diagnosis --proposes--> Fix`
- `Attempt --applies--> Fix`
- `Attempt --yields--> Outcome`
- `Lesson --generalizesFrom--> WorkEpisode` (minimum one closed episode)
- `Lesson --supportedBy--> Evidence` (minimum one admissible record)
- `Lesson --boundedBy--> VersionContext`
- `Evidence --documents|derivesFrom|observes|witnesses|proposes--> subject`
- `NewEvidence|VersionContext --invalidates|supersedes--> Lesson`

Rules:

1. Append raw episode/attempt/evidence records; corrections are new records linked by `supersedes` or `invalidates`, never edits that erase provenance.
2. A `verified` Lesson needs a closed episode, a stated outcome, compatible version context, and at least one `ExecutedWitness` or `TestObserved` evidence record. Documentation alone may create a `candidate` guidance record, not an operational lesson.
3. A `failed` or `inconclusive` outcome may be retained only as episode evidence; it must not prescribe a Fix.
4. Any mismatch in package major/minor, lock digest, API selector, or environmental precondition sets a lesson to `stale-pending-review`; incompatible evidence cannot be silently reused.
5. Conflicting docs/source/test records retain all records and force abstention until scoped by version or resolved with a higher-quality witness.
6. Queries return evidence class, version match, confidence, and absences alongside recommendations; a query without admissible support returns `ABSTAIN_UNSUPPORTED`.

### Safe consultation/update protocol

1. Resolve `Task` and `VersionContext` first. If the project version is unknown, return only version-independent documentation navigation.
2. Retrieve topic bindings, then filter by version compatibility and evidence class. Prefer official documentation for API intent, pinned source for exports/implementation questions, tests or local witnesses for behavior.
3. Produce a recipe with preconditions, cited action, validation required, and explicit unknowns.
4. On completion, append the episode, attempts, commands/outputs and outcome. Promote a Lesson only when the rule above is satisfied; otherwise append a candidate, failed, or abstention record.
5. On package update or changed source digest, mark dependent Lessons stale and require revalidation; never silently “refresh” their confidence.

### Required fixtures

- Positive: A local v4.x episode imports `animate`, runs a stated command against a captured target, and produces a bounded witness matching its criterion. The resulting Lesson says only that the action worked under that exact `VersionContext`.
- Failed: An attempt has a captured `Symptom`, diagnosis evidence, proposed Fix, and `Outcome=failed`; it remains a failure record, with no reusable lesson.
- Stale-version: An episode uses v3 global `anime`/`targets` object syntax; migration bindings classify the mismatch. Any v3 lesson is stale for v4 until re-executed because the documented API changes include imports, target placement, and parameter/loop semantics.
- Abstention: “Will `createLayout` meet our frame budget and accessibility policy?” returns `ABSTAIN_UNSUPPORTED`: the official docs establish API usage but this explorer found no local benchmark, assistive-technology witness, or project policy evidence.
- Proposal quarantine: issue #1105 is an open user-authored proposal for an LLM guide, explicitly not maintainer-approved API authority. It may be indexed as `UnverifiedProposal`; none of its installation, performance, or workflow claims may become a recipe/lesson without independent official evidence. [Issue #1105](https://github.com/juliangarnier/anime/issues/1105)

### Evidence gaps / next admissible work

- Pin the Anime.js repository SHA, retrieve exact source/type/test paths and selectors, and bind them to the observed `4.5.0` package manifest; current branch URLs are mutable.
- Crawl every descendant docs page/heading, including Timer, Animatable, Easings and all recipe-linked subsection anchors, before claiming coverage complete.
- Add no performance, accessibility, framework-cleanup, browser-support, or migration-success lessons until test-observed or executed local witnesses exist.
- Capture project package lock, runtime/browser/framework and acceptance criterion before first WorkEpisode; without them, create only documentation/source records and abstentions.

Proposed normalized action receipt:

```json
{
  "action_id": "spawn-0003",
  "dispatch_id": "2026-08-03-animejs-agent-knowledge-vault",
  "run_id": "animejs-vault-run-001",
  "wave_id": "explorers",
  "step_id": "s1",
  "role": "agent-lessons-explorer",
  "capability_ref": "research",
  "status": "completed",
  "artifacts": [
    {
      "ref": "projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/receipts/explorer-agent-lessons.json",
      "exists_claimed": false,
      "content_returned_to_parent": true
    }
  ],
  "validation": {
    "mode": "read-only",
    "official_documentation_topology_verified": true,
    "official_repository_manifest_verified": true,
    "community_issue_1105_quarantined_as_unverified_proposal": true,
    "no_local_execution_or_product_integration_claimed": true,
    "no_mutation_performed": true
  },
  "blockers": [
    "No immutable repository commit was captured; source/type/test claims must remain pending SHA pinning.",
    "No executed local witnesses exist for performance, accessibility, framework cleanup, or operational lessons."
  ],
  "started_at": "2026-08-03T13:23:28-03:00",
  "finished_at": "2026-08-03T13:23:28-03:00"
}
```

## Agent 1 feedback traversal 1 of 1 — Official source repair

+Both feedback gaps are `ready`. The repair provides digest-bound, machine-expandable manifests without repository mutation or runtime claims.

## AKV-FB-001 — `ready`

Official live source: [Anime.js documentation](https://animejs.com/documentation/).

Observed snapshot:

```json
{
  "observed_at": "2026-08-03T16:36:51.838Z",
  "seed_url": "https://animejs.com/documentation/",
  "seed_raw_sha256": "6f9912f716849789b9468b4916e88398f0028775e8b054c5d4604ef1afb78f28",
  "route_count": 418,
  "successful_rows": 418,
  "failed_rows": 0,
  "raw_page_set_sha256": "63125e931350f5dbf8552a289ac80d687bb1867e7c94c1e2d6e33904f16befcd",
  "semantic_jsonl_sha256": "681f004e04a91ab1a3462e882edff24d09454297f34a41863e81df06e20066fb"
}
```

Every route returned HTTP 200 after redirect normalization to a trailing-slash canonical path.

### Lossless extraction contract

The official `/documentation/` HTML is the route-set artifact. Discover routes with:

```regex
href="(\/documentation(?:\/[^"?# ]*)?)"
```

Exclude `/documentation`, deduplicate, and sort lexicographically. For each path, request `https://animejs.com<path>/` with redirects enabled.

Extract only from:

```css
article#docs-info
```

For every route emit this ordered JSON object:

```json
{
  "canonical_path": "<final redirected URL pathname>",
  "title": "<decoded title text>",
  "h1": "<decoded article#docs-info h1 text>",
  "heading_selectors": ["#<id>", "..."],
  "headings": ["<article h1-h6 text>", "..."],
  "topic_kind": "<classification below>",
  "parameters": "present|absent",
  "returns": "present|absent",
  "related_topics": {
    "disposition": "present|absent",
    "targets": [
      {"path": "<normalized documentation path with trailing slash>", "label": "<decoded anchor text>"}
    ]
  },
  "examples": "present-source-only|absent",
  "version_notes": {
    "disposition": "present|absent",
    "notes": ["<.docs-breadcrumb-version text>"]
  },
  "badges": {"js": false, "waapi": false, "new": false},
  "status": "semantic-observed",
  "http_status": 200,
  "raw_sha256": "<SHA-256 of response HTML bytes>"
}
```

Normalization and disposition rules:

- Decode tags/whitespace plus `&nbsp;`, `&amp;`, `&#39;`, `&apos;`, and `&quot;`.
- `heading_selectors`: ordered IDs of `article#docs-info h1` through `h6`.
- `parameters=present` iff an article heading normalizes case-insensitively to `Parameters`, `Parameter`, or `Accepts`.
- `returns=present` iff an article heading normalizes to `Return` or `Returns`.
- `related_topics.targets`: all distinct internal `/documentation/...` anchors in the article except the current canonical path, preserving first occurrence.
- `examples=present-source-only` iff the article contains `section.code-preview`. It is not execution evidence.
- `version_notes`: ordered `.docs-breadcrumb-version` text, generally `Since <version>`.
- Badges are article-local: literal `(JS)`, `(WAAPI)`, or `NEW` in the H1.
- Topic-kind precedence: top-level family; callback; method; property; parameter-or-setting; recipe; pitfall-guide; target-kind; keyframe-guide; easing-topic; otherwise guide-or-api-topic.
- Sort rows by `canonical_path`.
- Serialize each object with `JSON.stringify(row) + "\n"`.
- `semantic_jsonl_sha256` is SHA-256 of the concatenated rows.
- `raw_page_set_sha256` is SHA-256 of sorted `canonical_path + "\t" + raw_sha256 + "\n"` records.

Snapshot dispositions:

```json
{
  "parameters": {"present": 260, "absent": 158},
  "returns": {"present": 123, "absent": 295},
  "related_topics": {"present": 418, "absent": 0},
  "examples": {"present-source-only": 353, "absent": 65},
  "version_notes": {"present": 388, "absent": 30}
}
```

Representative exact row:

```json
{
  "canonical_path": "/documentation/animation/tween-parameters/duration/",
  "title": "duration | Tween parameters | Animation | Documentation | Anime.js | JavaScript Animation Engine",
  "h1": "duration",
  "heading_selectors": ["#accepts", "#default"],
  "headings": ["duration", "Accepts", "Default"],
  "topic_kind": "parameter-or-setting",
  "parameters": "present",
  "returns": "absent",
  "related_topics": {
    "disposition": "present",
    "targets": [
      {"path": "/documentation/animation/", "label": "Animation"},
      {"path": "/documentation/animation/tween-parameters/", "label": "Tween parameters"},
      {"path": "/documentation/animation/tween-value-types/function-based/", "label": "Function based value"},
      {"path": "/documentation/animation/tween-parameters/delay/", "label": "delay"},
      {"path": "/documentation/animation/tween-parameters/ease/", "label": "ease"}
    ]
  },
  "examples": "present-source-only",
  "version_notes": {"disposition": "present", "notes": ["Since 1.0.0"]},
  "badges": {"js": false, "waapi": false, "new": false},
  "status": "semantic-observed",
  "http_status": 200,
  "raw_sha256": "81383b6835e550ddd35e7e9c2d6b6d83862e0bc057a61c2fe8273aff701d4a0b"
}
```

Residue: no official sitemap, robots manifest, or repository-owned documentation-generation input was found at the obvious official endpoints. The digest binds this crawl but does not make the mutable website immutable. Re-crawls must compare both digests and retain changed rows as versioned observations.

The HTML references site CSS/JS assets with `?v=4.4.1`; that is a cache/version marker, not proof that documentation semantics are package v4.4.1.

## AKV-FB-002 — `ready`

Official immutable anchors: [v4.5.0 commit](https://github.com/juliangarnier/anime/tree/2c9cf8ea00329f6768c7d7902252ed977d75ce42), [v4.5.0 release](https://github.com/juliangarnier/anime/releases/tag/v4.5.0).

```json
{
  "version": "4.5.0",
  "commit_sha": "2c9cf8ea00329f6768c7d7902252ed977d75ce42",
  "commit_tree_sha1": "1511dce2d3e54de4c9c9cbfdb1d1dff2248d2c98",
  "tree_api": "https://api.github.com/repos/juliangarnier/anime/git/trees/1511dce2d3e54de4c9c9cbfdb1d1dff2248d2c98?recursive=1",
  "tree_truncated": false,
  "manifest_rows": 348,
  "manifest_jsonl_sha256": "f4026dec178de523262aca34dcddc5e419681b3494f37f496d9da8553d3ebcc0",
  "counts": {
    "source": 70,
    "type": 70,
    "test": 125,
    "example": 81,
    "package_documentation": 2
  }
}
```

### Machine expansion contract

Read the immutable recursive Git tree and retain blobs matching:

```text
README.md
package.json
src/**
dist/modules/**/*.d.ts
tests/**
examples/**
```

Sort by `path`. Emit:

```json
{
  "path": "<repository path>",
  "blob_sha1": "<Git blob identity>",
  "size": 0,
  "kind": "source|type|test|example|package-documentation",
  "structured_pointer": "git:2c9cf8ea00329f6768c7d7902252ed977d75ce42:<path>",
  "evidence_status": "source-observed|type-present|test-present-not-executed|example-source-present-not-executed"
}
```

Serialize as ordered JSONL. The resulting digest must equal `f4026dec...3ebcc0`.

Package-documentation anchors:

```json
[
  {
    "path": "README.md",
    "blob_sha1": "11e8d61143d56f82c5940267d990425bc6de5482",
    "size": 5192
  },
  {
    "path": "package.json",
    "blob_sha1": "7ebe3997b3620aeb7757c1d24b568d461ceb967d",
    "size": 8344
  }
]
```

### Documentation-family joins

| Documentation family | Package/module source |
|---|---|
| Getting started | `README.md`; `package.json#exports` |
| Timer | `animejs/timer`; `src/timer/`; `dist/modules/timer/` |
| Animation | `animejs/animation`; `src/animation/`; shared `src/core/`; matching declarations |
| Timeline | `animejs/timeline`; `src/timeline/`; matching declarations |
| Animatable | `animejs/animatable`; `src/animatable/`; matching declarations |
| Draggable | `animejs/draggable`; `src/draggable/`; matching declarations |
| Layout | `animejs/layout`; `src/layout/`; matching declarations |
| Scope | `animejs/scope`; `src/scope/`; matching declarations |
| Events | `animejs/events`; `src/events/`; matching declarations |
| SVG | `animejs/svg`; `src/svg/`; matching declarations |
| Text | `animejs/text`; `src/text/`; matching declarations |
| Utilities | `animejs/utils`; `src/utils/`; matching declarations |
| Easings | `animejs/easings` and its six published easing subpaths; `src/easings/` |
| WAAPI | `animejs/waapi`; `src/waapi/`; matching declarations |
| Engine | `animejs/engine`; `src/engine/`; matching declarations |
| Adapters | `animejs/adapters`; side-effect `animejs/adapters/three`; `src/adapters/` |

Root `src/index.js` re-exports every principal module and namespace except adapters; adapters remain explicit package subpaths. Structured symbol pointers may therefore use `path#export:<symbol>` after following `export *` edges from each module `index.js`.

Source-level observed direct exports include:

- SVG: `morphTo`, `createDrawable`, `createMotionPath`.
- Adapters: `registerAdapter`.
- Three.js adapter: `threeAdapter`, `getInstances`, `commitChanges`, plus side-effect resolver registrations.
- Root namespaces: `easings`, `utils`, `svg`, `text`; root also exports `globals`.

### Explicit residues

- `getting-started` has repository package/README evidence but no same-named source, test, or example directory.
- No directly named repository example was found for Timer, Engine, or WAAPI. Documentation code previews remain separate `present-source-only` examples.
- Tests and examples whose filenames do not identify one family must remain `shared-or-unmatched`; do not infer ownership from plausible behavior.
- Unmatched support material consists of 29 blobs: example assets/configuration and additive/canvas examples; test assets/configuration/runners plus generic build, leak, Node, seconds, and types suites.
- Test and example presence does not establish execution, passing behavior, performance, accessibility, or production readiness.
- The official [v3-to-v4 migration guide](https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4) is mutable wiki evidence and is not part of the pinned commit tree.

## Proposed continuation receipt

```json
{
  "action_id": "spawn-0001",
  "dispatch_id": "2026-08-03-animejs-agent-knowledge-vault-route",
  "run_id": "animejs-vault-run-001",
  "wave_id": "explorers",
  "step_id": "s1",
  "role": "official-source-explorer",
  "capability_ref": "research",
  "status": "pass",
  "artifacts": [
    {
      "ref": "urn:animejs-doc-semantic-manifest:sha256:681f004e04a91ab1a3462e882edff24d09454297f34a41863e81df06e20066fb",
      "state": "returned-not-written",
      "rows": 418
    },
    {
      "ref": "urn:animejs-v4.5.0-source-manifest:sha256:f4026dec178de523262aca34dcddc5e419681b3494f37f496d9da8553d3ebcc0",
      "state": "returned-not-written",
      "rows": 348
    }
  ],
  "validation": {
    "feedback_traversal": "1/1",
    "AKV-FB-001": "ready",
    "AKV-FB-002": "ready",
    "documentation_rows": "418/418",
    "documentation_fetch_failures": 0,
    "repository_tree_truncated": false,
    "test_execution": "not-performed",
    "example_execution": "not-performed",
    "workspace_mutation_during_feedback": "none",
    "git_mutation": "none"
  },
  "blockers": [],
  "started_at": "2026-08-03T16:28:00Z",
  "finished_at": "2026-08-03T16:37:00Z"
}
```

Hygiene residue from the earlier traversal: `/tmp/animejs-doc-urls` was created during the initial diagnostic, outside the repository, and a host safety guard rejected its attempted removal. This feedback traversal made no filesystem writes; the parent should account for that temporary-file residue when normalizing the overall action receipt.
