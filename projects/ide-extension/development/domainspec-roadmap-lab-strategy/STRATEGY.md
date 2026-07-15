---
id: domainspec-v2-roadmap-lab-strategy
title: DomainSpec v2 Roadmap Lab Strategy
status: candidate
updated_at: 2026-07-14
scope: private-local
transport: ide-extension-interactive-section
---

# DomainSpec v2 Roadmap Lab Strategy

## Decision in one sentence

Build a dedicated **Roadmap Lab** section in `ide-extension` where a newcomer first
forms and demonstrates a correct mental model, then submits addressable improvement
proposals; the browser never edits DomainSpec authority directly.

This strategy does not authorize implementation or production release. It defines the
smallest truthful route for a Victor pilot.

## Intended outcome

A person with no DomainSpec context should be able to use one local workbench session
to:

1. understand what DomainSpec v2 is trying to prove;
2. state honestly whether the first release is authorized;
3. identify the current step and why it comes first;
4. understand the five release phases and the role of Body War;
5. inspect exact evidence without learning the whole governance vocabulary first;
6. choose one roadmap node and identify a real weakness or ambiguity;
7. submit a proposal tied to the exact node, field, source fingerprint, and owner route;
8. see that a proposal is not the same thing as an accepted source change; and
9. compare the resulting revision after an owner applies or rejects the proposal.

The target is not passive documentation consumption. The target is a safe first
contribution.

## Evidence already available

The strategy reuses working boundaries instead of creating another application:

- The DomainSpec roadmap is a generated, self-contained HTML projection with a source
  fingerprint, 16 release nodes, 5 research frontiers, and 14 Body War checks.
- The roadmap already separates human copy from exact technical detail through
  progressive disclosure.
- `ide-extension` can publish a workspace-relative HTML file into its Canvas without
  copying or mutating the source file.
- Canvas revisions are content-addressed and retain a stable surface identity.
- An iframe can send named JSON interactions to the workbench through `postMessage`.
- The workbench records those interactions append-only with the current surface and
  revision bindings.
- Interaction payloads are schema-checked and limited to 16 KiB.
- Craft and Whisper are already modeled as modules that may read, preview, draft, and
  recommend, but may not silently rewrite authority.

These capabilities are sufficient for a proposal-first pilot. They are not sufficient
for authenticated collaboration, direct repository editing, or automatic proposal
application.

## Whisper intent substrate

### Resonance core

- Felt meaning: `I am allowed to learn, question, and contribute without pretending I
  already understand the system.`
- Voice: direct, patient, specific, and non-theatrical.
- Forbidden feel: examination, governance ceremony, or a dashboard that punishes lack
  of vocabulary.

### Relevance core

- Target public: Victor first, then any authorized collaborator with no DomainSpec
  context.
- Starting state: capable technical person, unfamiliar with DomainSpec terms, sources,
  owners, and release history.
- Authority mode: learner and proposer, not release owner.
- Primary objection: `I cannot improve this until I understand the whole system.`
- Response: one node and one addressable proposal are enough for the first contribution.

### Trajectory core

`orient -> restate -> inspect -> question -> propose -> owner gate -> compare revision`

The interface should move the person through that trajectory instead of exposing every
control at once.

## Smallest coherent unit

The smallest useful unit is a **Roadmap Learning and Improvement Packet**:

```text
roadmap id + source fingerprint + node id + field id
+ plain-language explanation + exact source value
+ newcomer restatement or question
+ proposed change + reason + supporting evidence
+ affected authority layer + owner route
```

Anything smaller loses either learning evidence or change addressability. Anything
larger forces the newcomer to understand the whole release before contributing.

Sixteen packets recompose into the whole roadmap. Packet events recompose into a review
queue. Accepted packets recompose into a regenerated roadmap revision.

## Candidate approaches

### Candidate A — embed the current roadmap only

Cheap and visually useful, but Victor can only browse. Feedback would return as vague
chat such as `FPR-06 is confusing`, with no selected field, original value, fingerprint,
or requested change mode.

Verdict: reject as the improvement workflow.

### Candidate B — make the roadmap directly editable

Fast in appearance and wrong in authority. The page is a generated projection. Direct
editing would conflate human copy, graph meaning, Craft continuation state, and release
authorization. It would also make stale edits easy to apply.

Verdict: reject.

### Candidate C — guided proposal lab over the existing Canvas

Keep the generated roadmap canonical, add newcomer guidance and stable proposal
controls, record proposals as revision-bound canvas events, and route each proposal to
its actual owner before changing a source.

Verdict: select. It preserves comprehension, contribution, traceability, and authority
without adding a second state system.

## Product surface

Add a dedicated `Roadmap Lab` tab or route inside `ide-extension`, rather than placing
the roadmap at the bottom of the generic L0 workbench.

The generic workbench currently opens with ide-extension Craft state, proposal queues,
approval details, and the Canvas. Those are relevant to kernel operators and unrelated
to a newcomer's DomainSpec mental model. Showing them first would recreate the cognitive
load problem that Whisper just removed from the roadmap.

The Roadmap Lab should contain five visible areas:

1. **Start here** — release status, purpose, current step, and a 20–30 minute path.
2. **Guided roadmap** — the existing human-first roadmap, published through Canvas.
3. **Understand this node** — plain meaning, exact contract, evidence, and one
   restatement prompt.
4. **Improve this node** — structured question or proposal form.
5. **Proposal history** — submitted, stale, under review, accepted, rejected, or applied
   to a later roadmap revision.

The exact graph remains available, but the default experience follows the guided path.

## Newcomer path

### Moment 1 — establish the boundary

Show, before terminology:

- `Release status: not authorized`;
- `1 of 16 release steps closed`;
- `Current step: FPR-01 — establish one trusted baseline`;
- `Body War is the proof witness, not evidence of completion`.

Ask one open restatement: `In your words, why can we not start by generating code?`

### Moment 2 — teach how to read one node

Walk through FPR-01 with four tabs:

- What this means
- Why it exists
- How we prove it
- Exact source contract

The interface should reveal the source name, owner, evidence, negative controls, and
done condition only after the plain explanation is visible.

### Moment 3 — let the learner choose

Offer the five phase cards and let Victor choose one area that matches his interest:

- meaning and specification;
- architecture and composition;
- formal validation;
- generated tests and graph comparison; or
- Body War and release operation.

Do not assign a node only because it is next in the release sequence. The learning path
and execution path have different owners.

### Moment 4 — create one real contribution

On any selected field, offer:

- `I do not understand this`;
- `This wording is misleading`;
- `I think evidence is missing`;
- `I disagree with the sequence or dependency`;
- `I found a new research frontier`.

The form asks for a reason and optional evidence. It does not ask Victor to select a
governance skill or know the final owner route.

### Moment 5 — close the loop

After submission, show:

- the proposal id;
- the roadmap fingerprint and revision it refers to;
- which authority layer it may affect;
- who must review it;
- why submission did not change release state; and
- the next observable outcome.

When an owner produces a new roadmap revision, show a before/after comparison linked to
the proposal.

## Architecture

```text
DomainSpec authority
  .craft/ledger.yml + expected-node-edge-manifest.yml
                 |
                 v
        deterministic roadmap builder
                 |
                 v
     roadmap.html + source fingerprint
                 |
     existing canvas publish request
                 |
                 v
  ide-extension Roadmap Lab iframe
                 |
        named postMessage events
                 |
                 v
 append-only canvas interactions
                 |
       active session polls events
                 |
                 v
 Roadmap Learning and Improvement Packet
       /               |               \
      v                v                v
 Whisper copy     graph owner       Craft owner
      \                |                /
       +-------- approved change -------+
                         |
                         v
              regenerate and republish
```

### Reuse unchanged

- Canvas publication and content hashing
- stable surface and revision identity
- current-revision interaction admission
- append-only interaction cursor
- 16 KiB request ceiling
- live Canvas revision notification
- existing module effect vocabulary

### Add at the presentation layer

- a dedicated Roadmap Lab shell;
- stable `data-roadmap-node` and `data-roadmap-field` addresses;
- newcomer prompts and proposal forms;
- a proposal-history projection over canvas interactions; and
- a visible authority-route explanation.

### Do not add in the first slice

- a DomainSpec-specific mutation endpoint;
- direct YAML or JSON editing in the browser;
- automatic proposal application;
- authenticated user accounts;
- simultaneous multi-user sessions;
- remote hosting or public export;
- a VS Code webview dependency; or
- a second roadmap state store.

## Interaction contract

Use the existing generic canvas event envelope. Record only meaningful learning or
proposal events; do not create surveillance-style click telemetry.

Recommended event names:

- `roadmap.understanding.submitted`
- `roadmap.question.submitted`
- `roadmap.improvement.proposed`
- `roadmap.review.completed`

Recommended proposal payload:

```json
{
  "roadmap_id": "domainspec-v2-first-production-release",
  "input_fingerprint": "sha256:<source fingerprint>",
  "participant_label": "victor",
  "node_id": "FPR-01",
  "field_id": "human_summary",
  "issue_type": "clarity",
  "change_mode": "clarify",
  "original_value": "<value shown on the selected revision>",
  "proposal": "<suggested wording or requested investigation>",
  "reason": "<why this improves understanding or correctness>",
  "evidence_paths": []
}
```

`participant_label` is a local self-description, not authenticated identity. The Canvas
already binds the event to `surface_id` and `revision_id`; the roadmap fingerprint binds
it to the DomainSpec inputs. Both bindings are required before review.

## Authority routing

| Proposal changes | Canonical target | Review route | Browser authority |
| --- | --- | --- | --- |
| Human title, summary, prompt, or glossary | Whisper-owned roadmap copy artifact | Whisper revision | propose only |
| Node, edge, dependency, frontier, proof, or release timing | expected node-edge manifest or named evidence | FPR graph/claim owner | propose only |
| Current stage, gate, next move, gap, or artifact status | DomainSpec-v2 Craft ledger | Craft owner and mutation gate | propose only |
| Formal, architecture, test, ontology, or Body War claim | named capability and claim owners | relevant research/decision route | propose only |
| Production authorization | release authorization owner | FPR-15 gate | forbidden as a browser effect |

The proposal form may recommend a route. It must not present the route recommendation as
an accepted disposition.

## Presentation-copy boundary

The human copy is currently embedded as JavaScript mappings in the roadmap template.
Before a real improvement loop, move that copy into a separately validated
`roadmap-copy.json` presentation artifact with stable field ids.

This extraction provides:

- addressable review targets;
- independent copy revisions without editing graph authority;
- deterministic coverage checks for all nodes, frontiers, and Body War steps;
- a clear place for glossary and onboarding prompts; and
- a safe Whisper route for accepted wording improvements.

The builder should fail when an authority item lacks required human copy or when copy
references an unknown authority id.

## Source inspection boundary

Publishing the existing HTML through the Canvas content URL changes the browser base
URL. The roadmap's current relative source links will not reliably resolve to their
workspace files inside that iframe.

The pilot must not silently ship broken evidence links. Choose one bounded L0 behavior:

1. show a copyable repository-relative source path and emit
   `roadmap.source.requested`; or
2. add a separately governed, read-only workspace source resolver.

The recommended first slice is option 1. IDE-native file opening can be added only when
the later wrapper has a witnessed command and path-admission boundary.

## Improvement loop

1. Victor submits a revision-bound proposal.
2. The active session polls `/api/canvas/events` from its last cursor.
3. The session validates node id, field id, roadmap fingerprint, payload size, and source
   freshness.
4. The session creates a Roadmap Learning and Improvement Packet.
5. The target layer determines the route: Whisper, graph/claim owner, Craft, or research.
6. An owner accepts, revises, rejects, or defers the proposal with rationale.
7. Only an accepted proposal can enter a bounded implementation task.
8. The roadmap builder and its negative tests run.
9. The HTML is republished as the next revision of the same Canvas surface.
10. The Roadmap Lab shows the proposal disposition and before/after fields.

If the fingerprint changed before review, the proposal becomes `stale-review-required`.
It is never silently rebased.

## Delivery sequence

### W0 — contract and copy extraction

- Ratify proposal-first authority.
- Define the Roadmap Learning and Improvement Packet.
- Extract stable human copy into `roadmap-copy.json`.
- Add builder validation for ids, coverage, and unknown references.
- Define the four meaningful canvas event names.

Exit: every visible human field has a stable address and a named authority route.

### W1 — Roadmap Lab read witness

- Add the dedicated Roadmap Lab route/tab.
- Publish the existing roadmap through the current Canvas with repository root as the
  configured workspace root.
- Present the start-here path and FPR-01 walkthrough.
- Replace broken iframe source links with copyable paths/source-request events.

Exit: Victor can complete the guided read path without seeing unrelated kernel controls.

### W2 — proposal witness

- Add question, restatement, and improvement forms.
- Emit revision- and fingerprint-bound canvas interactions.
- Project a read-only proposal history from the interaction cursor.
- Reject malformed, oversized, stale-revision, and unknown-field proposals.

Exit: one proposal survives restart and can be polled as an exact packet.

### W3 — governed handoff witness

- Route presentation copy to Whisper.
- Route graph/state changes to their distinct owners.
- Use the existing approval/envelope boundary for any protected write task.
- Preserve accepted/rejected rationale and resulting artifact refs.

Exit: a proposal can reach an owner without granting the browser source-write authority.

### W4 — revision round trip

- Apply one accepted low-risk copy improvement.
- Regenerate and validate the roadmap.
- Republish the same Canvas surface as a new revision.
- Show the exact before/after field and proposal disposition.

Exit: proposal -> review -> change -> proof -> new revision is demonstrated end to end.

### W5 — Victor comprehension and usefulness trial

- Run the newcomer path without coaching.
- Capture Victor's answers and one real proposal.
- Record confusion, time, abandoned steps, and whether the proposal was actionable.
- Revise the transport from observed use.

Exit: the human gate below is answered with evidence, not browser behavior alone.

## Human validation gate

After no more than 30 minutes, Victor should be able to answer without prompting:

1. Is DomainSpec v2 authorized for its first release?
2. What is the current step, and why does it come before code generation?
3. What are the five broad phases?
4. What does Body War prove, and what does it not prove?
5. Which information is presentation copy, graph authority, and continuation state?

He should then submit one proposal that an owner can adjudicate in under five minutes
because it contains a node, field, original value, fingerprint, reason, and suggested
change or investigation.

Browser tests cannot satisfy this gate.

## Mechanical validation

The implementation plan should require:

- deterministic roadmap generation;
- human-copy coverage for every authority id;
- unknown-id and missing-copy failures;
- Canvas publish and revision identity tests;
- interaction schema, 16 KiB, stale-revision, and restart tests;
- stale roadmap fingerprint rejection;
- source-path handling inside the iframe;
- proposal routing tests for copy, graph, Craft, research, and forbidden authorization;
- desktop and mobile Roadmap Lab checks;
- keyboard-only submission;
- zero direct repository writes from browser events; and
- visible private/local and production-unauthorized boundaries.

## Premortem

| Likely failure | Why it happens | Guardrail |
| --- | --- | --- |
| Victor browses but cannot contribute | Embed-only design | Require one addressable proposal as the product witness |
| Victor feels examined | Comprehension becomes a quiz | Use open restatements and let him choose an interest area |
| Suggestions overwrite authority | Direct-edit convenience | Proposal-only browser; owner-routed protected writes |
| Proposals cannot be applied | Human copy has no stable fields | Extract `roadmap-copy.json` before proposal UI |
| Evidence links break in Canvas | Relative paths resolve against the Canvas API URL | Copyable path/source-request witness first |
| A stale suggestion is applied | Roadmap changed after submission | Require revision id and input fingerprint; never silent rebase |
| ide-extension Craft state is mistaken for DomainSpec state | Both appear in one generic workbench | Dedicated Roadmap Lab and explicit authority labels |
| The pilot is described as multi-user collaboration | V0 has one global Canvas and no authenticated sessions | Name it a single-participant local pilot |
| DomainSpec content leaks publicly | Reuse drifts into public Arcanum surfaces | Keep the route private/local and outside `arcanum/` |

## Deferred complexity

- Authentication and verified person identity
- Concurrent proposals from multiple users
- Rich inline code diffing
- IDE-native file opening
- Remote access
- Automatic proposal application
- Generic roadmap support for other projects
- Analytics beyond the explicit comprehension trial

These features have no first-pilot failure that requires them.

## Frame-expiry conditions

Revisit this strategy if:

- the Canvas becomes authenticated and multi-session;
- DomainSpec's graph or Craft authority model changes;
- the roadmap stops being a generated projection;
- Victor needs protected source editing rather than proposal contribution; or
- the human trial shows that node-level packets are too small to preserve meaning.

## Recommended next route

Use `invoke plan` to convert W0–W5 into a bounded work pack after the owner accepts the
proposal-first boundary. Do not begin by editing the current dirty workbench surface.
Start with the isolated copy schema and generated roadmap contract, then integrate the
Canvas against the live ide-extension state.
