# Shoulders Of Giants For ResonantOS

**Version:** 0.1 adapted proposal  
**Date:** 2026-06-24  
**Status:** Product proposal, pre-build  
**Applies to:** ResonantOS vNext 2.0.0-alpha, browser-first product path  
**Tagline:** Quantify and reward the work your AI operating layer builds on.

---

## Vision

ResonantOS should make cumulative contribution visible.

The product already brings together the browser, Augmentor, Living Archive, add-ons, provider routing, delegated workspaces, browser jobs, wallet/DAO helpers, and audit artifacts. That makes it the right place to answer a question ordinary AI tools do not answer:

**Whose prior work made this result possible, and how should that contribution be credited?**

The proposal is to add a first-class contribution lineage layer to ResonantOS. Every approved artifact, memory page, delegated task result, add-on output, browser research trail, prompt package, runbook, persona pack, code change, and design note can carry a trace of what it used and what later reused it. That trace becomes the basis for credit, review, reputation, and eventually optional rewards.

This is not a separate platform. It is a ResonantOS product layer built out of existing ResonantOS primitives.

---

## Purpose Inside ResonantOS

ResonantOS already has the surfaces needed to observe serious work:

- **Living Archive** records sources, intake artifacts, review decisions, trusted memory, and provenance.
- **Delegation Packets** define scoped work, files in scope, verification requirements, expected artifacts, and return protocols.
- **Add-on manifests** declare capabilities, provenance, runtime type, archive requirements, and grant boundaries.
- **Provider Fabric** knows which model/runtime produced a result and under what cost and fallback policy.
- **Browser Agent Control** can preserve page evidence, controlled action traces, approvals, blocked steps, and saved reports.
- **Wallet and DAO helpers** already enforce a human-only approval boundary for sensitive action.
- **Audit logs** make host-mediated actions reviewable.

The missing piece is the shared graph that connects these outputs.

The layer should let ResonantOS:

1. **Record** what a piece of work used.
2. **Score** how much the work recombines, extends, verifies, or depends on prior work.
3. **Review** the score through human and AI-assisted adjudication.
4. **Route credit** back to contributors and source artifacts.
5. **Enable rewards later** through explicit, gated, legally reviewed adapters.

The first product should be credit and lineage. Payment is a later adapter, not the foundation.

---

## What Counts As Work

The proposal should not be limited to art, papers, or code. In ResonantOS, a rewardable or creditable work is any durable artifact that passes through a governed boundary.

Initial work classes:

- Living Archive source bundles, intake artifacts, promoted wiki pages, repair artifacts, and review decisions
- browser research trails, page summaries, screenshots, controlled action reports, and evidence bundles
- chat artifacts, prompt packages, reusable workflows, and compacted reasoning records
- delegated task workspaces, `delegation.packet.json`, `TASK.md`, `result.md`, and `verification.json`
- add-on outputs, add-on setup runbooks, skill documents, and capability-scoped reports
- code changes, architecture notes, ADRs, product plans, security reviews, and test evidence
- persona-style expert packs, if implemented as capability-scoped add-ons or Living Archive knowledge packages
- external source references that enter through approved intake

Initial edge classes:

- `cites`: work explicitly cites source material
- `uses-context`: work used a source as retrieved or attached context
- `derives-from`: work materially transforms an earlier artifact
- `invokes`: work runs a persona pack, prompt package, add-on, tool, or workflow
- `verifies`: work reviews, tests, audits, or validates another work
- `rebuts`: work challenges or corrects another work
- `maintains`: work updates, repairs, or keeps another work usable
- `packages`: work turns scattered material into a reusable unit

These edges should be typed because different kinds of contribution deserve different treatment. A source that inspired a design, a test that caught a bug, and a maintainer patch that kept an add-on working are not the same kind of shoulder.

---

## How Towers And Personas Translate

The original research vocabulary can map directly into ResonantOS without requiring a separate product.

In ResonantOS terms:

- A **tower** becomes a Living Archive knowledge package: a domain-specific, queryable, provenance-preserving body of knowledge built from approved sources and review artifacts.
- A **persona** becomes a capability-scoped expert pack: an add-on, prompt package, or memory-backed agent profile that can be invoked through ResonantOS boundaries.
- A **witness unit** becomes a governed review panel: human review plus tensioned AI reviewers, all operating through Delegation Packets, provider policy, and audit logs.
- A **consumption edge** becomes an observed invocation, context-use, or derivation event recorded by ResonantOS at the moment of use.

This matters because the hardest problem is not inventing a score. The hardest problem is observing use honestly.

If a user copies a persona pack into an unrelated external tool and runs it privately, ResonantOS cannot verify that use. If the invocation happens through ResonantOS, the system can record it with actor, artifact, capability, scope, and privacy policy intact. Therefore the first shippable version must reward only use that happens through ResonantOS-mediated surfaces.

No observable use, no honest reward graph.

---

## Mechanism

### 1. Observe At Point Of Use

Every supported surface emits a lineage event when it uses a prior artifact:

- Augmentor uses Living Archive context in a chat answer.
- Agent Control saves a page-derived evidence bundle.
- A delegated Engineer task reads scoped architecture memory and returns a patch.
- An add-on consumes a memory-provider result through an approved grant.
- A prompt package or persona pack is invoked through the provider fabric.
- A review task validates or rejects another artifact.

The event should be host-mediated where possible. Add-ons may propose lineage events, but trusted scoring must distinguish host-observed events from self-declared events.

### 2. Preserve A Conserved Lineage Graph

Each work should carry a bounded, typed ancestry graph. The graph must avoid double-counting.

A contribution edge should carry one shared contribution value that can be split across purposes such as novelty, dependency, maintenance, and verification. The system should not let every ancestor claim the full value of the same descendant.

### 3. Score As Seed, Not Verdict

The score is a decision aid, not an automatic payout machine.

Useful initial signals:

- **novelty-in:** how unusually the work combines prior sources
- **built-upon:** how much later work depends on this artifact
- **verification value:** whether this work makes other work more trustworthy
- **maintenance value:** whether this work keeps a dependency usable
- **reuse confidence:** how directly observed the use was
- **review confidence:** how strong the review/adjudication trail is

The guiding rule: **ship a judge, not a meter.**

The meter produces evidence. A review path decides what it means.

### 4. Adjudicate Through ResonantOS Review

ResonantOS should use its existing review patterns:

- Living Archive review queue for knowledge promotion
- Delegation Packet verification requirements for task outputs
- add-on capability review for external/runtime boundaries
- human approval for money, wallet, public-posting, identity, and irreversible actions
- audit trails for all privileged host-mediated actions

AI reviewers can help, but they must not silently become the authority. They should produce review artifacts, disagreement notes, confidence scores, and cited reasons that a human or configured governance rule can accept, reject, or defer.

### 5. Route Credit First, Rewards Later

The MVP should route credit, not money.

Credit can support:

- artifact-level attribution
- contributor reputation
- maintainership visibility
- reuse dashboards
- add-on quality signals
- review priority
- future marketplace or DAO reward eligibility

Monetary reward should arrive only after the product has:

- observed invocation and derivation edges
- anti-gaming controls
- identity and contributor policies
- wallet/security review
- explicit user approval flows
- a real funding source
- legal review for payments, securities, tax, and money-transmission risk

Reward adapters must not give add-ons raw wallet, signing, or payout authority.

---

## Direct Product Mapping

| ResonantOS surface | Lineage responsibility |
| --- | --- |
| Living Archive | Preserve source provenance, trusted memory promotion history, artifact ancestry, repair lineage, and review outcomes. |
| Augmentor Chat | Record which approved context, prompt packages, persona packs, and prior artifacts shaped a response or generated artifact. |
| Provider Fabric | Attach model/runtime, route, cost posture, fallback, and provider health context to produced work. |
| Delegation Fabric | Treat `delegation.packet.json`, `TASK.md`, `result.md`, and `verification.json` as signed work units with explicit source refs and verification evidence. |
| Add-on SDK | Require add-ons to declare lineage event capabilities and distinguish proposed events from host-observed events. |
| Browser Agent Control | Record page evidence, controlled action traces, saved reports, approval gates, and source URLs as lineage inputs. |
| Audit Log | Preserve privileged action receipts and scoring/review decisions. |
| Settings | Expose lineage privacy, export, retention, and reward-adapter controls. |
| Wallet/DAO helpers | Support future human-approved reward flows while keeping signing and transfer actions human-only. |

---

## Proposed Local Data Model

The first implementation can be local-first.

Suggested root:

```text
ResonantOS_User/
  Lineage/
    events.jsonl
    works/
      {work_id}.json
    edges/
      {edge_id}.json
    reviews/
      {review_id}.json
    exports/
```

Minimum `work` fields:

```json
{
  "id": "work_...",
  "kind": "living_archive_artifact",
  "title": "Example artifact",
  "createdAt": "2026-06-24T00:00:00Z",
  "createdBy": {
    "actorKind": "human|augmentor|engineer|addon|external",
    "actorId": "..."
  },
  "artifactRefs": [],
  "privacy": "private|shareable|public",
  "trustStatus": "draft|reviewed|promoted|revoked",
  "sourceRefs": [],
  "auditRefs": []
}
```

Minimum `edge` fields:

```json
{
  "id": "edge_...",
  "fromWorkId": "work_source",
  "toWorkId": "work_descendant",
  "edgeKind": "cites|uses-context|derives-from|invokes|verifies|rebuts|maintains|packages",
  "observedBy": "host|addon|human|imported",
  "confidence": 0.0,
  "conservedWeight": 0.0,
  "evidenceRefs": [],
  "createdAt": "2026-06-24T00:00:00Z"
}
```

Minimum `review` fields:

```json
{
  "id": "review_...",
  "targetWorkId": "work_...",
  "reviewKind": "lineage|novelty|verification|reward-eligibility",
  "decision": "accept|revise|reject|defer",
  "scoreSeed": {},
  "reasons": [],
  "reviewerRefs": [],
  "auditRefs": []
}
```

The exact schema should be refined before implementation, but the product should keep these invariants:

- every rewardable work has a stable id
- every lineage claim has typed evidence
- observed and self-declared edges are different
- scoring is reproducible from stored evidence
- review decisions are auditable
- private source content is not exported by accident

---

## UI Shape

The feature should not become a giant analytics dashboard first. It should appear where users already work.

Initial user surfaces:

- **Artifact detail panel:** "Built on" and "Used by" sections for any saved artifact.
- **Living Archive review view:** lineage preview before promotion.
- **Delegation Monitor:** source refs, produced artifacts, and downstream reuse.
- **Add-on detail view:** contribution graph, emitted event types, and trust posture.
- **Settings -> Lineage:** privacy, retention, export, scoring policy, and reward adapters.
- **Optional contributor view:** accumulated credit by artifact, review, maintenance, and reuse.

The first satisfying moment should be simple: open a saved artifact and see the real shoulders under it.

---

## Why This Belongs In ResonantOS

- **It fits the operating layer.** ResonantOS sits where sources, memory, model calls, delegated work, browser evidence, and add-ons meet.
- **It makes memory economically meaningful.** Living Archive stops being only recall and becomes the substrate for durable contribution.
- **It strengthens add-on governance.** Add-ons that produce reusable value can earn credit without becoming trusted core.
- **It improves review discipline.** Verification, maintenance, and challenge work become visible instead of disappearing behind the final artifact.
- **It differentiates the product.** Most AI products produce outputs. ResonantOS can preserve the contribution graph behind outputs.
- **It supports future marketplace/DAO paths without rushing money.** Credit and reputation can ship before payment.

---

## Honest Status

This is a proposal, not a shipped feature.

What is true today:

- ResonantOS has working or documented foundations for Living Archive, provider routing, add-on manifests, delegated workspaces, browser jobs, wallet/DAO helpers, and audit boundaries.
- ResonantOS does not yet have a contribution lineage index.
- There is no shipped scoring model for novelty, reuse, maintenance, verification, or reward eligibility.
- There is no durable reward pool, marketplace-fee stream, or payout adapter.
- Add-ons do not yet have a formal lineage event contract.
- The browser-first product still needs release hardening before this layer should compete with core stabilization.

Primary open risks:

- **Observation:** use outside ResonantOS cannot be verified.
- **Privacy:** lineage exports must not leak private sources, prompts, page content, wallet context, or personal memory.
- **Gaming:** self-declared lineage, collusive review, synthetic novelty, and spam artifacts can all inflate credit.
- **Double-counting:** ancestor chains can overclaim unless value is conserved across edges.
- **Review capture:** AI review panels can drift, agree too easily, or overfit to the author unless tension and audit are designed in.
- **Funding:** money is vacuous until a real funding source exists.
- **Law:** payouts, tokenized reward, public attribution, cross-border payments, and DAO flows need legal review.
- **Product timing:** the core browser-first alpha should stabilize before a reward economy becomes user-facing.

None of these risks kill the idea. They sequence it.

---

## Implementation Sequence

### 0. Credit-only MVP

Ship no money. Ship lineage visibility.

Acceptance:

- a saved artifact can show "built on" and "used by"
- private source content is redacted from exported lineage
- self-declared edges are visibly lower-trust than host-observed edges

### 1. Lineage event schema and local store

Define `work`, `edge`, `event`, and `review` schemas. Store JSONL events plus indexed work/edge records under the user data root.

Acceptance:

- deterministic schema validation
- append-only event log
- import/export without private-content leakage by default

### 2. Living Archive instrumentation

Record lineage when source files become intake artifacts, review artifacts become trusted memory, and trusted memory is used as context.

Acceptance:

- intake artifact points back to source version
- promoted memory points back to review evidence
- Augmentor context use can create a host-observed `uses-context` edge

### 3. Delegation Packet instrumentation

Add `sourceWorkRefs`, `producedWorkRefs`, and `lineagePolicy` to delegated workspaces.

Acceptance:

- `result.md` and `verification.json` can become work records
- source refs survive task dispatch and return
- failed or unverified results cannot receive trusted credit silently

### 4. Add-on SDK event contract

Let add-ons propose lineage events through a host API. Require manifests to declare which event kinds they emit.

Acceptance:

- add-on events are scoped by grants
- host distinguishes proposed edges from observed edges
- add-ons cannot assign their own final score or payout eligibility

### 5. Artifact UI

Add "Built on" and "Used by" sections to artifact details, review views, and delegated task results.

Acceptance:

- user can inspect evidence refs
- user can reject or correct a lineage edge
- corrections are logged as review events, not silent rewrites

### 6. Score seed

Implement a conservative scoring seed for observed use, review value, and maintenance value.

Acceptance:

- score is reproducible from stored events
- score is labeled as evidence, not final reward
- no payout or public claim is made from score alone

### 7. Review and challenge path

Add review actions for accepted, revised, rejected, and deferred lineage claims. Later, add challenge bounties only after anti-gaming controls exist.

Acceptance:

- challenge and correction preserve old evidence
- reviewer rationale is stored
- review confidence is separate from model confidence

### 8. Reward adapter gate

Only after the graph works, add an optional reward adapter design behind wallet/security/legal review.

Acceptance:

- no automatic transfer
- no add-on wallet authority
- human approval required for any payout
- funding source is explicit
- legal and tax status is documented before public release

---

## Initial Non-goals

- no automatic wallet payout
- no public token claim
- no universal cross-app tracking
- no raw prompt or private memory export by default
- no add-on self-certification
- no attempt to score every chat message
- no reward eligibility for unreviewed spam artifacts
- no replacement for Living Archive review or existing security boundaries

---

## One-line Summary

The shoulders layer for ResonantOS is a local-first contribution lineage system: observe use through ResonantOS surfaces, preserve a typed graph of what work built on what, score that graph only as review evidence, route credit before money, and postpone rewards until identity, funding, wallet security, anti-gaming, and legal gates are real.

---

*Provenance: adapted from the governed shoulders-of-giants research packet into a ResonantOS-native product proposal. Claims about current product surfaces are grounded in the ResonantOS 2.0.0-alpha docs and should be rechecked before implementation planning.*
