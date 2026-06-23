# Arcanum Journey — Decision Record

> Decision-gate output for the four scoping decisions, 2026-06-22. Source of
> truth is [`.craft/ledger.yml`](../ledger.yml); this is the reviewable human
> record. Source of each decision: operator, via `/decision-gate` ("for all,
> 1 by 1").

## DEC-AJ-HOME-001 — Deliverable home (was BLOCKING)

- **Question:** Public arcanum submodule vs private parent for the shipped journey?
- **Options:** public-arcanum-only · hybrid-public-shell-private-content · private-parent-project
- **Selected:** **public-arcanum-only**
- **Rationale:** Operator chose a public arcanum home. The premise that this required
  private data was disproven during the gate: the explainer persona is anonymizable,
  and the **Cyber Alchemy method is already published inside public arcanum**
  ([development/cyberalchemy-ontology-lifecycle/](../../../../arcanum/development/cyberalchemy-ontology-lifecycle/),
  ARCANUM-MANUAL, README).
- **Guardrail:** Teach Cyber Alchemy only at the level already public in arcanum. The
  deeper private `cyberAlchemy-v2/` specifics and its still-open public/private
  boundary, plus any engine/proprietary specifics, stay out.
- **Downstream impact:** Deliverable lives under `arcanum/` (public); authoring follows
  submodule discipline and excludes private operator data.

## DEC-AJ-PACKAGE-MODE-001 — Package mode

- **Question:** Runtime per-user tower vs pre-authored chapters vs hybrid?
- **Selected:** **hybrid-authored-chapters-plus-runtime-tower**
- **Rationale:** Each chapter ships stable authored content; the user ends by running
  research-tower + reading-learning-package to build their own personalized tower in
  their own language. Reliable lessons + the "first tower" payoff.

## DEC-AJ-ROUTING-001 — Starting-point routing

- **Question:** How does the user reach their first tool?
- **Selected:** **both-interrogate-then-let-user-pick**
- **Rationale:** `/interrogation` infers the primary goal and recommends a first tool
  (creative → Whisper; automation → Craft/goal/task-session), then shows the full map
  so the user can override or probe.

## DEC-AJ-SURFACE-001 — Surface area

- **Question:** How does a user get and run the journey?
- **Selected:** **standalone-skill-installs-repo-teach-while-install-html-surfaces**
- **Rationale:** A standalone downloadable skill installs the repo (whole or a picked
  slice), asks what to learn, and teaches while installing — **with agent-generated
  HTML pages as the explanation surfaces** (x-ray style, as the arcanum user-guide
  already does).

## Status

- Blockers remaining: **0**
- Open decisions remaining: **0**
- Active gaps (carry into `/invoke design`): sigil/spell map, preset schema, persona
  extraction, Cyber Alchemy inclusion, chapter order.
- Next step: run `/invoke` to define → design → plan as a public arcanum spell/skill.
