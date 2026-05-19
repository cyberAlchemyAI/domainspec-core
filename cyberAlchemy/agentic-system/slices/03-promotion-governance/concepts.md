---
module: cyberalchemy-agentic-system
slice: 03-promotion-governance
status: candidate
updatedAt: 2026-05-19
docType: slice-concepts
---

# Concepts: Promotion Governance

Work: [README.md](README.md)

## What This Slice Compiles

This slice gathers the promotion material from:

- Necronomicon Knowledge Substrate Flow;
- Arcanum Business Ontology;
- Ontology Vault;
- Ontology Harness;
- the agentic-system deep dive;
- the ontology entry model.

Promotion governance defines how knowledge gains authority.

## Promotion Is A Change In Authority

Promotion is not "saving a note."

Promotion changes what future agents may rely on.

The system sees many candidates:

- a user correction;
- a repeated route miss;
- a useful shortcut;
- a telemetry pattern;
- a source claim;
- a contradiction;
- a premise;
- a workflow preference;
- a failure mode.

Promotion asks:

```text
should this shape future behavior?
if yes, how strongly?
inside what scope?
with what evidence?
under which owner?
with what invalidation path?
```

## Authority Ladder

Necronomicon's substrate flow gives the main ladder:

```text
raw interaction
  -> session evidence
  -> discovery baseline
  -> inventory knowledge
  -> ontology candidate
  -> reviewed premise
  -> confidence decision
  -> constitution or axiom
  -> bridge-validated operating context
```

Each state has a different authority level.

| State               | Authority          | Owner                                  | Meaning                                                      |
| ------------------- | ------------------ | -------------------------------------- | ------------------------------------------------------------ |
| Raw interaction     | Very low           | Session                                | A conversation turn, note, or rough observation.             |
| Session evidence    | Low                | Necronomicon or task session           | Captured route, checkpoint, side note, decision, or handoff. |
| Discovery baseline  | Low-medium         | Discovery or define route              | Scoped understanding with vocabulary, constraints, and gaps. |
| Inventory knowledge | Medium             | `inventory`                            | Source-backed reusable knowledge and lookup substrate.       |
| Ontology candidate  | Medium             | `ontology-vault` or ontology-harness   | Proposed governed meaning object.                            |
| Premise             | Medium, uncertain  | `ontology-vault premise-review`        | Working bet with falsification criteria.                     |
| Confidence decision | Medium-high        | `ontology-vault promote-confidence`    | Evidence and commitment reviewed separately.                 |
| Constitution        | High               | `decision-gate` and convention update  | Codified operating rule or process convention.               |
| Axiom               | Highest            | ontology governance and decision owner | Load-bearing principle used to justify downstream rules.     |
| Bridge evidence     | Alignment-specific | ontology-harness                       | Evidence that intent and implementation are connected.       |

## Ontology Ownership

The ladder is itself ontology content.

It should live as a thick Knowledge Governance Ontology entry, not only as text inside synthesis or planning documents.

Candidate entry:

- [knowledge-governance-authority-ladder.md](../../../ontology/entries/knowledge-governance-authority-ladder.md)

That entry owns the reusable rule:

```text
raw source
  -> inventory source summary
  -> typed inventory entry
  -> thick ontology candidate
  -> premise or confidence review
  -> promoted ontology entry
  -> route, capability, specification, or context update
```

Memory and telemetry can feed this ladder, but they do not skip it. The ontology entry should be retrieved whenever an agent is deciding whether a claim, pattern, lesson, or route policy is allowed to guide future work.

## Promotion States

CyberAlchemy should use explicit states:

| State                | Meaning                                                                       |
| -------------------- | ----------------------------------------------------------------------------- |
| `raw`                | Unprocessed source, note, observation, or session fragment.                   |
| `session-evidence`   | Captured in a run, checkpoint, side note, or route ledger.                    |
| `discovery-baseline` | Organized into early scope, glossary, discovery, or definition baseline.      |
| `inventory-entry`    | Source-backed reusable entry with tags, contradictions, and lookup selectors. |
| `ontology-candidate` | Thick entry draft with meaning, context, evidence, confidence, and edges.     |
| `premise`            | Reviewed working bet that remains falsifiable.                                |
| `reviewed`           | Survived review but has not become a stronger rule.                           |
| `promoted`           | Accepted as stable ontology entry for a defined scope.                        |
| `constitution`       | Codified operating rule, convention, or process constraint.                   |
| `axiom`              | Load-bearing principle.                                                       |
| `retired`            | No longer active, preserved historically.                                     |
| `contradicted`       | Evidence shows the entry is wrong, unsafe, or overgeneralized.                |

## Via Negativa In Promotion

Business Ontology recommends formalizing rules only when the absence of the rule has caused measurable harm.

In CyberAlchemy, promotion should be more likely when the missing rule causes:

- repeated route misses;
- repeated misunderstanding;
- repeated validation gaps;
- implementation drift;
- telemetry noise that hides an obligation;
- user workflow friction;
- unsafe memory behavior;
- capability contract confusion.

This keeps the ontology from becoming ornamental.

## Promotion Gates

Promotion gates make authority changes inspectable.

| Gate                   | Question                                | Pass Condition                                                                  |
| ---------------------- | --------------------------------------- | ------------------------------------------------------------------------------- |
| Source coverage        | Is the source material identified?      | Source path, session id, telemetry id, or inference label exists.               |
| Inventory completeness | Is the evidence reusable?               | Summary, claim, source refs, tags, contradictions, lookup selector.             |
| Branch classification  | Where does this belong?                 | Branch, type, scope, and owner are clear.                                       |
| Thick entry            | Is this more than a pointer?            | Content, context, payload, edges, evidence, confidence, promotion, maintenance. |
| Premise                | Is this a working bet?                  | Falsification criteria and counterevidence are named.                           |
| Confidence             | How supported and how committed are we? | Evidence confidence and commitment confidence are set and justified.            |
| Decision               | Does this change behavior or policy?    | Consequential tradeoff has explicit approval.                                   |
| Bridge                 | Does this assert alignment?             | Intent side, system side, and connecting evidence are visible.                  |
| Context proof          | Can future tasks use this compactly?    | Context Builder can select it with relevant evidence and exclude noise.         |
| Maintenance            | When should it change?                  | Review trigger, expiry, contradiction path, and owner route are named.          |

## Confidence Model

Promotion keeps evidence confidence and commitment confidence separate.

| Evidence | Commitment | Meaning                                            | Action                                            |
| -------- | ---------- | -------------------------------------------------- | ------------------------------------------------- |
| Low      | Low        | Exploratory idea.                                  | Keep as candidate or research seed.               |
| High     | Low        | Well-supported but not strategically load-bearing. | Keep as reference or low-commitment entry.        |
| Low      | High       | Risky bet.                                         | Require decision gate and falsification path.     |
| High     | High       | Strong promotion candidate.                        | Promote within scope and add maintenance trigger. |

The system should be able to say:

```text
we believe this is probably true
but we are not ready to build around it
```

or:

```text
we are choosing to rely on this before evidence is strong
so the risk must be explicit
```

## Decision Matrix

| Candidate                  | Promote To                                     | Required Evidence                                                         |
| -------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------- |
| One-off memory observation | Session evidence                               | Context and source turn.                                                  |
| Repeated memory pattern    | Inventory entry or memory ontology candidate   | Repetition or explicit user decision.                                     |
| Source-backed concept      | Ontology candidate                             | Source summary, claims, contradictions, branch classification.            |
| Operational lesson         | Operational Ontology entry                     | Route evidence, scope, avoided failure, expiry.                           |
| Context solution           | Context Solution Catalog                       | Trigger fingerprint, evidence selectors, observed use.                    |
| Route policy               | Capability Ontology entry or capability update | Repeated route evidence and owner review.                                 |
| Privacy or workflow rule   | Constitution                                   | Explicit decision, scope, affected behavior, rollback path.               |
| Load-bearing principle     | Axiom                                          | Strong evidence, repeated use, contradiction review, explicit commitment. |
| Alignment claim            | Bridge entry                                   | Intent evidence, system evidence, observed or tested link.                |

## Non-Promotion Rules

The system should refuse unsafe promotion.

- Do not promote directly from raw memory to ontology authority.
- Do not promote pointer-only entries.
- Do not promote without source refs or explicit inference status.
- Do not promote a local trick into a general rule without reuse evidence.
- Do not promote user workflow observations without privacy scope.
- Do not promote route policy without failure modes and expiry.
- Do not promote bridge claims without both sides of the bridge.
- Do not overwrite contradictions.
- Do not call a discipline a rule unless there is enforcement or review.

## Promotion Record

Every promotion decision should leave a record with:

- candidate id;
- from state;
- to state;
- branch;
- owner;
- evidence confidence;
- commitment confidence;
- decision;
- scope;
- source refs;
- counterevidence;
- gates passed or failed;
- affected entries;
- affected capabilities;
- review trigger;
- rollback path.

Promotion output can be:

- promote;
- defer;
- reject;
- retire;
- contradict;
- split;
- demote;
- request evidence;
- request human decision.

Promotion is valuable because it can say no.
