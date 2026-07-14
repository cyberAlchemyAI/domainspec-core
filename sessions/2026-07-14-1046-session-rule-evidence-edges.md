---
tags: [ontology, canonical-kinds, edges, session-authority, inverse-edges, frontmatter, cyberalchemy-v2]
node_type: discovery
is_session: true
layer: ontology
nature: explanatory, technical
status: active
created: 2026-07-14
timestamp: 2026-07-14T10:46:03-03:00
expires: 2026-09-12
conversation_id: 2026-07-14-session-rule-evidence-edges
decisions_made: true
contradictions_found: true
specs_updated: [cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md, cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml, cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml, .claude/skills/custom/domainspec-discovery-writing.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "THE SESSION RULE — a session may only CREATE or UPDATE, because those are acts while `refutes`/`surfaces-conflict`/`opens-question`/`closes-question`/`revisits` are claims a session bears no authority to make — closes two open questions by dissolution, and then invalidates the very producer the schema names for `session`."
---

# The session rule — a session performs acts, never claims

## Summary

The session set out to report what prior sessions had settled about the Evidence-kind edges, and
became a rebuild of what a session is *allowed to say*. Four edges were carried forward and one was
reversed: `findings --derives-from--> research` was written (closing OQ-15), and `contradicts` —
first ruled a typed negative on the argument that a session already reifies any conflict — was
restored to `discovery ↔ discovery` the moment the owner struck `surfaces-conflict`, because the
argument for dropping it had depended on the verb being removed. The load-bearing decision is **the
session rule**: a session may only **create** or **update** a file, because those are *acts*, while
`refutes`, `surfaces-conflict`, `opens-question`, `closes-question` and `revisits` are *claims* — and
a session bears no authority to make one. The rule was not an invention but an enforcement: `EDGES.yaml`
already declared that *"a session records what it DID, never what is TRUE"* and then handed the session
five verbs that violated it. It closed OQ-16 and OQ-17 by **dissolution** rather than by answer. The
first inverse ruling did not survive review: the one inverse it kept (`derives`) is forbidden by the
very allow-list that governs it, and the `created-by` rationale argued against a cardinality the edge
does not have — an artifact has one creator, not five — so an inverse is a **read direction, not a
declarable edge**. `canonical_kind`
returned to frontmatter with the carrier always kept **outside** it — the filename for three kinds, the
path for `session`, the only exception — so no instance can self-declare its type. Rewiring the
`process` column to real skills falsified OQ-10: a review dispatch is *forbidden* from writing
`findings.md`, so `findings` has one producer and the `0..1` cardinality actually rests on the
single-agent (`n=1`) research case, a reason none of the three files had stated. The folder move that
preceded this session had silently broken the graph — 32 inbound references, including ones inside
CAV2-D51 and the one-label decision's own Consumers block — and all were repointed and verified
against disk. The cost of the session rule surfaced last: the producer named for `session` emits the
claim-edges the rule forbids, and the owner deferred that ruling rather than let it block the close.

## Contradictions

- questions `.claude/skills/close-session/SKILL.md` — line 35 reads *"**Contradictions** — only if a
  vault node was validated, contradicted, or questioned. One bullet per edge"*, and :98 routes
  node-naming questions into that section as `questions {node}` edges. Every one is a **claim**, which
  the session rule forbids. The schema and its own named producer now disagree, and the entire
  `sessions/` corpus — this record included — is written in the forbidden form.
- contradicts `implementation/domainspec/vault/ontology-conventions.md` — `updates` was pulled out of
  the succession class and re-minted as the session provenance verb paired with `creates`; that
  consolidated catalog **deprecates** `updates` (→ *"use `version:` frontmatter"*) and carries
  `modifies` for the equivalent role. The same word now names two different edges across two live
  catalogs — a *new* collision, created this session, on top of the standing fork.
- validates `cyberAlchemy-v2/authority/decisions/2026-07-13-canonical-kind-one-label.md` — restoring
  `canonical_kind` to frontmatter reinstates the decision's carrier premise (*"the field is defined
  and unused"*), which the previous session's filename-only ruling had abolished with no supersession
  note. The contradiction the 2026-07-13-2225 session recorded against this decision is now healed.
- questions `cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md` — whether
  `contradictions: tolerated` is right for the Evidence kinds at all. Two `findings` from the *same*
  dispatch reaching opposite conclusions is a defect to be resolved, not two harmless records of
  different moments; the "different moments" defence confuses when an artifact was *written* with what
  it is *about*. The derivation from `durability` stands on that defence.
- questions `cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml` — no edge is mandatory. The
  `1` (REQUIRED) cardinality is defined in its own header and used zero times, so the schema can be
  violated only by **commission**, never by **omission**: the empty graph conforms.

## Open questions

- Does a work-record stripped of the power to *observe* still do what a session is for? The session
  rule leaves a session unable to record even *"I noticed these two disagree"* — it may act, and it
  may narrate its acts, but it may assert nothing. That the rule follows from the principle is
  established; that a pure act-log is what a session **should be** is not.

## Next steps

- Rule OQ-19 through `decision-gate`: either rewrite `close-session` so a session narrates its acts
  and **updates** the target artifact to carry the claim, or carve an observation class into the
  session rule. Note the coupling — reading (1) cannot be *implemented* until the edge carrier exists.
- Define the edge carrier (OQ-18) in the Instance Contract: one syntax, owned by the schema, binding
  on all four kinds. Today the only statement of a carrier is `## Connections` inside a skill, so an
  operator can write a conforming `discovery.md` and nothing else.
- Resolve the `updates` name collision against `ontology-conventions.md` — it was created this
  session and should not be left to be discovered by someone else.
- Correct the enumeration rows the durability redefinition exposed (`backlog`, `ledger`, `readme`,
  `projection`) — carried from 2026-07-13-2225, owner-parked.

## Recommendation

Attack the **`close-session` contradiction** first — the first Next step, ahead of the edge carrier.

The licensing fact is verified, not inferred: `close-session:35` was read verbatim against the file,
and every session record in `sessions/` — this one included — declares the `validates` / `questions`
edges the session rule forbids. Of everything recorded above it is the only item where the schema and
a **live, named producer** actively disagree, and where the disagreement is already replicated across
the whole corpus rather than latent in one file.

It also **gates** the second Next step: what a session may write determines what the edge carrier must
be able to carry, so building the carrier first risks building it twice. And the Open question above is
the one `decision-gate` should actually put — the choice between rewriting the producer and carving an
observation class into the rule turns on it, and nothing here settles it. That reading (1) will win is
a **hunch**, not a licensed claim.

## Files touched

- cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md
- cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml
- cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml
- .claude/skills/custom/domainspec-discovery-writing.md
- cyberAlchemy-v2/authority/definitions/DEFINITIONS.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md
- cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md
- cyberAlchemy-v2/authority/decisions/2026-07-13-canonical-kind-one-label.md
- cyberAlchemy-v2/disciplines/cards/artifact-tree-admission.md
- cyberAlchemy-v2/validation/development/artifact-admission-validator/
- cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/
- cyberAlchemy-v2/authority/definitions/reviews/
- sessions/2026-07-13-1008-process-retraction-canonical-kind-ruling.md
- docs/vault/conversations/2026-07-13-1624-canonical-kinds-instance-contract.md
