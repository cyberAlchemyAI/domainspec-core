# Simple Ontology Presentation Corpus

Dispatch: `2026-06-22-simple-ontology-presentation-corpus`
Status: accepted with auditor repairs
Owner route: domainspec-subagents-strategy -> research -> Whisper

## Dispatch Summary

This dispatch prepares a Whisper-ready presentation brief for explaining
ontology in plain language while staying bounded to the selected project corpus.

The presentation should explain ontology as a governed map of meaning with
receipts: it tracks what important project things are, how they relate, where
they came from, how mature or trustworthy they are, and what they may be used
for. It must avoid presenting ontology as automatic truth, total authority, a
memory dump, or a generated index.

Auditor note: the draft was repaired to avoid implying that ontology itself
grants authority. The final wording says ontology can show what may be assumed
from a meaning map, while authority still moves through owner routes.

## Selected Corpus

1. `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:873-967`
   - Canonical definition D19.
   - Supports the core definition of ontology as structured meaning with
     authority boundaries.

2. `cyberAlchemy-v2/ontology/README.md:1-27`
   - Defines the v2 ontology role and boundary.
   - Supports claims about what ontology is responsible for and what it is not.

3. `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md:31-44,304-320`
   - Separates inventory from ontology.
   - Supports the promotion ladder: receipts, candidates, governed promotion,
     authority.

4. `cyberAlchemy/agentic-system-ontology-synthesis.md:253-385`
   - Provides narrative explanation and the business/system/bridge framing.
   - Supports claims about business intent, system evidence, drift,
     contradiction, and residue.

5. `arcanum/BUSINESS-ONTOLOGY.md:5-55`
   - Provides business-facing language.
   - Supports accessible framing for non-technical audiences.

6. `projects/ontology/ARCHITECTURE.md`
   - Describes the materialization ladder and components.
   - Supports claims about how ontology becomes usable through structured
     artifacts and components.

7. `implementation/domainspec/vault/ontology-conventions.md`
   - Defines typed roles, status, confidence, and edges.
   - Supports claims about typed context, maturity, confidence, relations, and
     use rules.

## Presentation Thesis

Ontology is a governed map of meaning with receipts.

It does not merely define words. It helps a project understand what important
things are, how they relate, where their evidence comes from, how confident we
are in them, what status they have, and what agents or humans may safely assume
from them.

Inventory helps the agent find receipts. Ontology helps the agent understand
what the receipts mean and whether they can be used.

In CAV2, definitions, constitutions, specs, runtime contracts, and public claims
remain authoritative only through their own owner routes. Ontology may model
or prepare promotion, but it cannot promote them by itself.

## Five-Slide Spine

### 1. What It Is

Ontology is a map of important project meanings.

It tracks what things are, how they relate, where they came from, how much we
trust them, and what may be safely assumed from them.

Plain phrase:

> A map of meaning with receipts.

### 2. What It Is Not

Ontology is not a glossary, folder tree, transcript, memory dump, generated
index, or truth machine.

It does not automatically make anything authoritative.

Plain phrase:

> The map is not the government.

### 3. Why Relations Matter

Systems fail in the gaps between nouns.

Ontology tracks relationships: business promise to system behavior, rule to
test, runtime signal to expectation, evidence to confidence.

Plain phrase:

> A glossary tells what a word means; ontology tells what the thing means in
> context, how it relates, and what may be assumed from it.

### 4. How It Becomes Usable

Inventory finds receipts. Ontology interprets them.

Candidates propose meaning. Promotion records govern whether something can
become relied-upon authority.

Plain phrase:

> Inventory helps the agent find receipts. Ontology helps the agent understand
> what the receipts mean and whether they can be used.

### 5. How Agents Use It

Agents can receive ontology-derived typed context: kind, scope, evidence,
relations, maturity, confidence, contradictions, drift, and retrieval guidance.

They also receive warnings about what cannot be assumed.

Plain phrase:

> Nodes + edges + receipts + confidence + promotion state + use rules.

## Plain-Language Script Seeds

Ontology is not just a list of terms. A glossary can tell you what a word means,
but ontology tells you what the thing is, how it connects to other things, where
that understanding came from, and what may be safely assumed from it.

Inventory is the receipt drawer. It helps us find the evidence. Ontology is the
interpretation layer. It helps us understand what the evidence means and whether
it is mature enough to rely on.

The map is not the government. Ontology can show meaning, evidence, confidence,
and promotion state, but it does not automatically make something authoritative.

Systems fail in the gaps between nouns. The hard problems often happen between
business intent and system behavior, between a rule and a test, or between a
runtime signal and an expectation. Ontology gives those relationships a place
to live.

Business intent says what should be true. System evidence says what is
happening. The bridge shows match, drift, contradiction, and residue.

As a secondary metaphor, ontology can feel like a traceability layer between
intention, evidence, and action. It gives agents ontology-derived typed context
instead of loose memory: what kind of thing this is, what scope it belongs to,
what evidence supports it, what relations matter, how confident we are, and
what not to assume.

## Source-Bounded Claim Table

| Claim | Source Boundary | Safe Use |
| --- | --- | --- |
| Ontology is a governed map of project meaning. | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:873-967`; `cyberAlchemy-v2/ontology/README.md:1-27` | Use as the central presentation definition. |
| Ontology includes evidence, relations, confidence, status, and use boundaries. | `implementation/domainspec/vault/ontology-conventions.md`; `projects/ontology/ARCHITECTURE.md` | Use when explaining ontology-derived typed context. |
| Inventory and ontology have different jobs. | `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md:31-44,304-320` | Say inventory finds receipts; ontology interprets meaning and usability. |
| Ontology does not automatically create authority. | `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md:304-320`; `cyberAlchemy-v2/ontology/README.md:1-27` | Use "the map is not the government." |
| Promotion governs whether something can become relied-upon authority. | `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md:304-320` | Use when explaining candidates, promotion records, and authority. |
| Relations matter because they connect intent, evidence, tests, signals, and confidence. | `cyberAlchemy/agentic-system-ontology-synthesis.md:253-385`; `implementation/domainspec/vault/ontology-conventions.md` | Use in the "Why Relations Matter" slide. |
| Business intent, system evidence, and bridge framing help explain match, drift, contradiction, and residue. | `cyberAlchemy/agentic-system-ontology-synthesis.md:253-385`; `arcanum/BUSINESS-ONTOLOGY.md:5-55` | Use for business-facing explanation. |
| Agents can use ontology-derived typed context with warnings and retrieval guidance. | `implementation/domainspec/vault/ontology-conventions.md`; `projects/ontology/ARCHITECTURE.md` | Use in the final slide, avoiding claims of autonomous truth. |

## Forbidden Overclaims

Do not say ontology is the source of truth for everything.

Do not say ontology automatically makes something authoritative.

Do not call ontology a truth machine.

Do not reduce ontology to a glossary, folder tree, generated index, transcript,
or memory dump.

Do not describe pointer-only nodes as sufficient.

Do not erase uncertainty, contradiction, drift, residue, confidence level,
maturity state, or promotion status.

Do not imply that evidence alone creates authority without governed promotion.

Do not imply agents can assume everything retrieved from ontology is safe to act
on.

In CAV2, ontology may classify, relate, trace, condense, and prepare promotion
requests. It cannot bless itself. Definitions, constitutions, decisions, specs,
runtime contracts, public claims, and owner routes still govern what actually
counts.

## Whisper Intake Substrate

### Intent

Create a clear, plain-language presentation explaining ontology to an audience
that may not know the technical architecture.

### Audience

Mixed business, product, and technical listeners who need to understand why
ontology matters and how agents use it.

### Tone

Plain, confident, grounded, and careful.

Avoid mystical or absolute language. Prefer practical metaphors with
boundaries.

### Core Metaphors

- A map of meaning with receipts.
- The map is not the government.
- A traceability layer between intent, evidence, and action.
- Systems fail in the gaps between nouns.

### Must Preserve

- Ontology is governed meaning, not automatic truth.
- Inventory and ontology are different.
- Promotion matters.
- Relations matter.
- Evidence, confidence, maturity, and use rules matter.
- Agents need warnings about what cannot be assumed.

### Must Avoid

- "Source of truth for everything."
- "Truth machine."
- "Just a glossary."
- "Just memory."
- "Automatically authoritative."
- "Generated index."
- Certainty where the source corpus preserves uncertainty.

## Auditor Repair Record

The auditor required four fixes:

- replace the original glossary comparison with a phrase about contextual
  meaning, relations, and what may be assumed;
- tighten the broad body-metaphor phrasing into a traceability-layer phrase;
- qualify the agent-context claim as ontology-derived context rather than a
  guaranteed runtime behavior;
- add the explicit CAV2 authority sentence that ontology may model or prepare
  promotion but cannot promote authority by itself.

All four repairs are incorporated above.

## Next Route

Send this brief to Whisper as presentation intake.

Recommended next route:

1. Use this `findings.md` content as the source-bounded intake.
2. Ask Whisper to produce a five-slide presentation draft.
3. Preserve the five-slide spine unless there is an explicit reason to revise
   it.
4. Keep speaker notes plain-language and source-bounded.
5. Run a final overclaim pass before publishing or sharing.
