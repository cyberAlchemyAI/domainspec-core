<!-- MINT-ACT OUTPUT (L1) for domainspec-v2. Cast from templates/definitions.md. INTERNAL/private.
     INHERITS the three-voice card FORMAT. SKELETON: seeds 2 cards; the owner authors the rest via the
     definitions lifecycle. Obs-B: an Evidence cav2/v1 citation is provenance, never a resolution path. -->

# DomainSpec v2 Local Definition Cards

Status: active
Promotion scope: local-domainspec-v2-only
Canonical source: yes

Local definitions for this repository. They do not define the implementation contract, governance
weight, launch readiness, or external policy. Each card keeps three voices (Formal / Plain-language /
Domain-context).

> **Citation vs authority (Obs-B).** A card's `Evidence:` MAY cite a harvested v1/cav2 snapshot —
> that is provenance, not a resolution path. The normative meaning is owned **here**; removing the
> framework attachment does not change it. A `Source kind:` of method-authority points at **this
> repo's own constitution**, never at v1 or cav2.

## domainspec-v2-D1. Drift

Source kind: operator-reading; local-inference

Evidence: [impl/spec/DRIFT-CONVERGENCE.md](../impl/spec/DRIFT-CONVERGENCE.md)

Formal voice:

```text
drift =
  measurable divergence between intended DomainSpec behavior and observed system reality
  across surfaces { semantic, contract, runtime, governance, coordination }
convergence =
  evidence-backed sustained reduction of critical drift over time
```

Plain-language voice: drift is the problem signal — the spec and reality have pulled apart;
convergence is the trend of pulling them back, with receipts.

Domain-context voice: the subject of **drift governance**; measured across the 5 surfaces, acted on
(not defined) by Saturn.

Use carefully: drift is a *signal*, not a correction; one signal is not (non-)convergence.

Misuse warning: do not conflate drift (the divergence) with Saturn (the loop that acts on it), or
detecting drift with converging.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a claimed drift not
measurable across the 5 surfaces" → challenges the term; owner route = definitions-governance; gate = owner
decision; blocking question = "measurable divergence across {semantic, contract, runtime, governance,
coordination}?"; residue → definitions/reviews/.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
the 5-surface measurement is realized (BLK-DSV2-DRIFT-ENGINE) + no open contradiction; gate =
definitions-governance owner gate; status = active.

Promotion boundary: local-only (grounds drift-governance; not an external policy term)

## domainspec-v2-D2. Validation governance ⟵ *domain-originated*

Source kind: local-inference  *(may cite v1 precedent in Evidence — citation only)*

Evidence: [authority/AUTHORITY-MODEL.md](../authority/AUTHORITY-MODEL.md),
[impl/spec/TEST-PIPELINE.md](../impl/spec/TEST-PIPELINE.md)

Formal voice:

```text
validation governance =
  the authority over BUILD-TIME FIDELITY of a typed spec:
    which obligations it must derive into (TEST-PIPELINE -> engine derive)
    AND what counts as pass/fail (engine lint; audit-alignment)
  resolving to THIS repo's authority/, never to a framework
```

Plain-language voice: the authority that says "for this typed spec, these checks must hold, and here
is what passing means" — exercised by the engine `derive`/`lint`, `generate-tests`, `audit-alignment`.

Domain-context voice: one of v2's three domain-originated governances (owner route
`validation-governance`); the methods are the already-built tools, the governance is the authority
over them.

Use carefully: build-time fidelity is necessary, not sufficient — it is not runtime conformance.

Misuse warning: do not treat a passing derived test as correctness, and do not collapse it into
cav2's `gate` / SMT meta-validation (that is meta-validation of governance rules; this is object
validation of specs/impls).

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "treating build-time
fidelity as runtime correctness, or collapsing it into cav2's gate / SMT meta-validation" → challenges the
term; owner route = definitions-governance; gate = owner decision; blocking question = "is this object-level
validation of a typed spec, resolving to THIS repo's authority?"; residue → definitions/reviews/.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner ratifies the
kind (done 2026-06-29) + the L2 attestation seal (BLK-DSV2-L2-ATTESTATION); gate = definitions-governance
owner gate; status = active (RATIFIED; L2 seal pending).

Promotion boundary: RATIFIED kind (owner, 2026-06-29); L2 attestation seal pending

## domainspec-v2-D3. Edge-Law Admissibility ⟵ *build-from-owned (CAV2-D22/D29/D16)*

Source kind: local-inference  *(cites cav2 CAV2-D22/D29/D16 in Evidence — citation only)*

Evidence: [development/reformulate-batch1/DESIGN.md](../development/reformulate-batch1/DESIGN.md) (R3),
[research/2026-07-01-composability-edges-taxonomy-synthesis.md](../research/2026-07-01-composability-edges-taxonomy-synthesis.md);
provenance: cav2 CAV2-D22 (orthogonal classification), CAV2-D29 (axis orthogonality), CAV2-D16 (typed coupling)

Formal voice:

```text
edge-law admissibility =
  an edge TYPE is admissible IFF it composes into different code
  (adds a non-redundant distinction over the axes
   {concept-type, relation-kind, composition-shape, feature-boundary})
corollary =
  widen a SOURCE endpoint (same target, same semantics) = clean
  change the TARGET type = overload -> reject
```

Plain-language voice: an edge deserves its own name only if it makes the code compose differently; else
widen an existing edge or add a flag. Widening *who* uses an edge is fine; changing *what it points at* is not.

Domain-context voice: governs R3 (RELATIONSHIPS reformulation). Rulings: keep `enforces`≠`applies`; collapse
`enforces`/`enforces-cross`; reject `queries` for Calc→Policy; widen `applies`→Policy→{Op,Calc} and
`queries`→Behavioral→Entity. See DEC-DSV2-EDGE-ADMISSIBILITY.

Use carefully: this is classification/governance orthogonality (CAV2-D22/D29), NOT Lean/Hilbert projector
orthogonality (excluded from cav2 authority).

Misuse warning: do not overload an edge's target type to reuse a name; do not conflate with the
linear-algebra orthogonality.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "an edge type that does
NOT compose into different code yet claims its own type (or a target-type overload)" → challenges the term;
owner route = definitions-governance; gate = owner decision (cites CAV2-D22/D29/D16); blocking question =
"does the edge add a non-redundant distinction over {concept-type, relation-kind, composition-shape,
feature-boundary}?"; residue → definitions/reviews/.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
the R3 rulings applied to RELATIONSHIPS.md + no open contradiction; gate = definitions-governance owner gate;
status = active.

Promotion boundary: local-only (governs the v2 edge-law; cites cav2, transfers no cav2 authority)

## domainspec-v2-D4. Executable Typed Graph

Source kind: local-inference; synthesis

Evidence: [research/2026-07-01-composability-edges-taxonomy-synthesis.md](../research/2026-07-01-composability-edges-taxonomy-synthesis.md)

Formal voice:

```text
executable typed graph =
  the spec surface as ONE graph:
    nodes   = TAXONOMY meta-types (each -> one code pattern)
    edges   = RELATIONSHIPS typed edge-law
    realize = composability (how connected patterns reference each other in code)
  governed on 3 axes: layering (structure) / validation (derivation) / drift (alignment)
```

Plain-language voice: the spec is a typed graph you can build code from — the things (nodes), how they
connect (edges), and how each connection turns into code (composability).

Domain-context voice: thesis of the composability/edges/taxonomy synthesis; the substrate the spec-ontology
toy tested (verdict SURVIVED-narrow). Two enforcement arms: engine derivation (validation) + code-tag
composability (drift).

Use carefully: "executable" = derivable/checkable, not that the spec runs.

Misuse warning: do not collapse the three axes; engine derivation (moat) ≠ the composability check.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "collapsing the three
axes, or equating engine derivation with the composability check" → challenges the term; owner route =
definitions-governance; gate = owner decision; blocking question = "are nodes / edges / composability + the
three axes all distinct here?"; residue → definitions/reviews/.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
the composability/edges/taxonomy synthesis evidence holds + no open contradiction; gate =
definitions-governance owner gate; status = active.

Promotion boundary: local-only

## domainspec-v2-D5. Two-Plane Boundary

Source kind: local-inference (resolves the spec-as-ontology research)

Evidence: [research/2026-07-01-spec-as-ontology/findings.md](../research/2026-07-01-spec-as-ontology/findings.md)

Formal voice:

```text
two-plane boundary =
  ontology framing governs the AUTHORING plane (writing/editing/organizing the spec)
  derivation governs the CONTRACT plane (the crisp, total, engine-facing spec)
  authority flows contract -> authoring, never reverse
```

Plain-language voice: use ontology tooling while you write the spec, but the strict engine-facing spec stays
the source of truth — help flows one way only.

Domain-context voice: interim stance while DEC-DSV2-LANE-ZA (fuse vs generate) is deferred to an agent-cost
experiment.

Use carefully: authoring-plane metadata (confidence/premises) is non-authoritative over the crisp docs until
an owner route ratifies a consumer.

Misuse warning: do not let authoring-plane ontology labels leak into the engine-facing contract docs.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "authoring-plane labels
leaking into the engine-facing contract, or authority flowing authoring → contract" → challenges the term;
owner route = definitions-governance; gate = owner decision; blocking question = "does authority flow
contract → authoring only?"; residue → definitions/reviews/.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
DEC-DSV2-LANE-ZA resolved (or the interim two-plane stance holds) + no open contradiction; gate =
definitions-governance owner gate; status = active (interim).

Promotion boundary: local-only

## domainspec-v2-D6. meta-type

Source kind: method-vocabulary; local-inference

Evidence: [meta-types/meta-types.md](./meta-types/meta-types.md) (the DS-D1 meta-type system) ·
[impl/spec/TAXONOMY.md](../impl/spec/TAXONOMY.md)

Formal voice:

```text
meta-type =
  one of the 25 fixed DomainSpec concept types (the node alphabet of an aspect file).
  every concept declares exactly one meta-type; it fixes the concept's well-formedness
  criterion, its edge participation, and the code pattern it maps to.
```

Plain-language voice: one of the 25 fixed concept types a DomainSpec aspect file is built from — the node
alphabet, like parts of speech for a domain spec. Entity, Rule, Event, …; every concept declares exactly one.

Domain-context voice: the node vocabulary the content validator checks against; the 25 are carded as
`DS-D1.1..25` in [meta-types/](./meta-types/meta-types.md) (backend 1–14 formalized; UI 15–25 deferred).

Use carefully: a meta-type is a **node kind**; the relationships between them are **edge verbs** (`DS-D2`), a
separate vocabulary.

Misuse warning: do not conflate a meta-type (the kind) with a **concept** (an instance of a kind) or with a
**category** (the grouping of kinds).

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a concept that fits no
meta-type, or needs two" → challenges the 25-type closure; owner route = definitions-governance; gate = owner
decision; blocking question = "does every concept map to exactly one of the 25?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
the 25-type set is exercised on ≥1 real aspect + no open contradiction; gate = definitions-governance owner
gate; status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2); names the node alphabet, not an external policy term.

## domainspec-v2-D7. category

Source kind: method-vocabulary; local-inference

Evidence: [impl/spec/TAXONOMY.md](../impl/spec/TAXONOMY.md) · [meta-types/](./meta-types/meta-types.md) (the `<category>/` layout)

Formal voice:

```text
category =
  the top-level grouping of meta-types: Structural | Behavioral | Connective | Lifecycle | UI.
  each meta-type belongs to exactly one category; categories mirror the meta-types/<category>/ layout.
```

Plain-language voice: the family a meta-type belongs to, grouped by what it does: structural (things),
behavioral (actions), connective (bridges), lifecycle (evolution), UI.

Domain-context voice: organizes the 25 meta-types and the schema folders
(`impl/spec/meta-types/<category>/`); the authoring walkthrough proceeds category by category.

Use carefully: a category groups **kinds** (meta-types), not concepts.

Misuse warning: don't conflate a category (Structural) with a meta-type (Entity) or a concept
(PaymentTransaction).

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a meta-type that fits
no category, or two" → challenges the five-family closure; owner route = definitions-governance; gate = owner
decision; blocking question = "does each meta-type belong to exactly one family?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
all 25 types assigned to exactly one category + no open contradiction; gate = definitions-governance owner
gate; status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2).

## domainspec-v2-D8. formal criterion

Source kind: method-vocabulary; local-inference

Evidence: [meta-types/](./meta-types/meta-types.md) (each card's Formal voice) ·
[impl/spec/meta-types/](../impl/spec/meta-types/) (the `.schema.yml` criteria)

Formal voice:

```text
formal criterion =
  a decidable predicate over a concept's structure: concept C is a well-formed T iff criterion_T(C).
  authored in <type>.schema.yml (structural rule kinds); checkable WITHOUT running the engine.
```

Plain-language voice: the machine-checkable rule per meta-type (in its `.schema.yml`) — the exact structural
conditions a concept must meet to count as that type.

Domain-context voice: the checkable core of each DS-D1 card; the content validator applies it. Distinct from
TAXONOMY's descriptive prose (which says what a type is *like*, not *exactly when* a concept qualifies).

Use carefully: a formal criterion checks **shape**, not meaning; a check that needs the engine to decide is a
boundary flag, not a criterion.

Misuse warning: do not equate the formal criterion (public shape check) with the engine's δ-derivation
(private — the moat).

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a criterion decidable
only by running derivation" → challenges its public-checkability; owner route = definitions-governance; gate =
owner decision; blocking question = "can it be checked structurally, without the engine?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
the criterion runs in the validator (pos/neg fixtures discriminate) + no open contradiction; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2); a public shape check, never the engine
δ-derivation (moat).

## domainspec-v2-D9. edge-participation signature

Source kind: method-vocabulary; local-inference  *(aliased `DS-D8` in the schemas)*

Evidence: [impl/spec/RELATIONSHIPS.md](../impl/spec/RELATIONSHIPS.md) · [meta-types/](./meta-types/meta-types.md) (each card's edge-participation slice)

Formal voice:

```text
edge-participation signature (DS-D8) =
  the endpoint typing of an edge verb:  verb : source.type -> target.type.
  a declared edge is admissible iff its endpoints' meta-types match the signature.
```

Plain-language voice: the who-may-connect-to-whom rule — for each edge verb, the allowed source and target
meta-types; a declared edge with wrong endpoints is rejected.

Domain-context voice: the DS-D8 slice each meta-type card lists (SOURCE of / TARGET of); the 29 signatures
land at MT3b / R3. Distinct from the edge verbs themselves (`DS-D2`).

Use carefully: the signature types the **endpoints**; *which* edges earn a type is edge-law admissibility
(`domainspec-v2-D3`), a separate question.

Misuse warning: do not conflate the signature (endpoint typing) with the edge **verb** (`DS-D2`, the
relationship name) or with **admissibility** (`domainspec-v2-D3`).

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a declared edge whose
endpoints violate the signature yet is claimed valid" → challenges the signature; owner route =
definitions-governance; gate = owner decision; blocking question = "do both endpoints' meta-types match the
verb's signature?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
the 29 signatures land (MT3b, after R3) + the validator checks endpoints + no open contradiction; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2); the signatures depend on R3's reformulated
RELATIONSHIPS.

## domainspec-v2-D10. content validator

Source kind: method-vocabulary; local-inference

Evidence: [impl/tools/validate-content.ts](../impl/tools/validate-content.ts) · [impl/spec/meta-types/](../impl/spec/meta-types/)

Formal voice:

```text
content validator =
  validate-content(aspect_file): for each concept C with declared type T, run criterion_T(C);
  for each declared edge E(a --verb--> b), check the DS-D8 signature against type(a), type(b).
  returns { valid, violations[] }. a build-time fidelity check; no δ-rule import.
```

Plain-language voice: a linter for the spec's content — not just that types are declared, but that each
concept is well-formed and each edge is admissible.

Domain-context voice: the validation-governance method (`impl/tools/validate-content.ts`); extends
`validate-relationships` with per-type content checks; distinct from `engine lint` and engine `derive`.

Use carefully: it checks build-time **shape** fidelity, not runtime correctness.

Misuse warning: do not collapse it into the engine (`derive` / δ-rules) — it is the public contract, kept
consistent with the engine but not importing its algorithm.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a validity claim that
requires running derivation" → challenges its public-check boundary; owner route = definitions-governance;
gate = owner decision; blocking question = "does it decide validity by structure, without the engine?";
residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
validate-content runs on a real feature (a seeded violation flips it) + wired into `npm run validate` + no
open contradiction; gate = definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2); a public validation-governance method, never the
engine δ-derivation (moat).

## domainspec-v2-D11. instance

Source kind: method-vocabulary; local-inference

Evidence: [impl/tools/instances.ts](../impl/tools/instances.ts) · [meta-types/meta-types.yml](./meta-types/meta-types.yml) (the machine registry pattern)

Formal voice:

```text
instance =
  a concept normalized to structured YAML conforming to its meta-type schema (<concept>.instance.yml):
    a declared meta_type + fields / values / attributes as data.
  the machine-readable form; validated against the SAME criterion as the authored markdown.
```

Plain-language voice: the machine-readable twin of an authored concept — the same concept expressed as data
(fields, attributes) a tool can consume, not prose.

Domain-context voice: the MT-INST surface (`impl/tools/instances.ts generate`, DEF-D3 = source B); generated
example instances live under `impl/spec/__generated__/` (gitignored).

Use carefully: an instance is a machine **form** of a concept, not a new concept; it conforms to — does not
redefine — its meta-type schema.

Misuse warning: do not confuse an instance (data conforming to a schema) with the **schema** itself (the
criterion) or with the concept's markdown card.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "an instance that claims
conformance but violates its schema criterion" → challenges the instance; owner route = definitions-governance;
gate = owner decision; blocking question = "does the instance satisfy its meta-type criterion?"; residue →
`definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
generated instances validate round-trip (ok passes, mutated rejected) + no open contradiction; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2); a public shape artifact, never the engine
δ-derivation (moat).

## domainspec-v2-D12. instance validator

Source kind: method-vocabulary; local-inference

Evidence: [impl/tools/instances.ts](../impl/tools/instances.ts) · [impl/tools/tests/instances.test.ts](../impl/tools/tests/instances.test.ts)

Formal voice:

```text
instance validator =
  instances validate: for each <concept>.instance.yml, load its meta-type schema and apply the same
  criterion rules to the instance's structured data (fields / values / attributes).
  returns pass | violations. shape only; no δ-rule import.
```

Plain-language voice: the `instances validate` mode — load each `<concept>.instance.yml`, apply its schema
criterion, accept conforming / reject malformed.

Domain-context voice: `impl/tools/instances.ts` (validate mode); the machine-side counterpart of the content
validator; proven by `tools/tests/instances.test.ts` (generate → validate; mutated → reject).

Use carefully: it checks the generated instance's **shape** against the schema, not meaning.

Misuse warning: do not conflate it with the content validator (markdown) or the engine (`derive`) — it is the
instance-side public shape check.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "an instance passing the
validator but violating the schema criterion" → challenges the validator; owner route = definitions-governance;
gate = owner decision; blocking question = "does it apply the same criterion the schema declares?"; residue →
`definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
the round-trip test is green (generate → validate passes; mutated → rejected) + no open contradiction; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2); a public shape check, never the engine
δ-derivation (moat).

## domainspec-v2-D13. aspect file

Source kind: method-vocabulary; local-inference

Evidence: [impl/spec/features/sample/SPEC.md](../impl/spec/features/sample/SPEC.md) · [impl/spec/__fixtures__/mt/](../impl/spec/__fixtures__/mt/) (minimal aspect files)

Formal voice:

```text
aspect file =
  a markdown spec document for a feature: a Concept Registry (concept -> meta-type) + per-concept tables
  (fields / attributes) + declared edges. the human-authored unit the content validator reads.
```

Plain-language voice: a spec doc that declares concepts and their meta-types + fields/edges — the
human-authored source the content validator checks.

Domain-context voice: e.g. `impl/spec/features/<feature>/SPEC.md`; the `__fixtures__/mt/*.md` are minimal
aspect files; its granularity is the content validator's input.

Use carefully: "aspect" = a facet of a feature's spec; the validator's input granularity is the aspect file.

Misuse warning: do not confuse the aspect file (human markdown) with an **instance** (machine YAML) — both
are validated, but they are different forms.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a spec doc with concepts
but no registry/tables the validator can read" → challenges the aspect-file shape; owner route =
definitions-governance; gate = owner decision; blocking question = "does it carry a Concept Registry +
per-concept tables?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
a real feature aspect file validates + no open contradiction; gate = definitions-governance owner gate;
status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2).

## domainspec-v2-D14. Concept Registry

Source kind: method-vocabulary; local-inference

Evidence: [impl/tools/validate-content.ts](../impl/tools/validate-content.ts) (reads it first) · [impl/spec/__fixtures__/mt/](../impl/spec/__fixtures__/mt/)

Formal voice:

```text
Concept Registry =
  a table in an aspect file: Concept | Type (a meta-type), optionally an ID.
  it declares each concept's meta-type; the content validator reads it to dispatch the right criterion.
```

Plain-language voice: the concept-to-meta-type map for a feature — it says "PaymentTransaction is an Entity,"
so the validator knows to run the Entity criterion.

Domain-context voice: the first thing the content validator parses; definitions-governance (M2-C1) aggregates
per-feature registries into a project-level typed registry.

Use carefully: the registry declares the **type**; the concept's structure (fields / attributes) is in its
own table below.

Misuse warning: a concept absent from the registry is untyped — the validator can't check it; do not rely on
headings alone.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a concept used but not
registered with a meta-type" → challenges the registry's completeness; owner route = definitions-governance;
gate = owner decision; blocking question = "is every concept declared with a meta-type here?"; residue →
`definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
a real aspect file's registry drives validation + no open contradiction; gate = definitions-governance owner
gate; status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2).

## domainspec-v2-D15. declared-attributes convention

Source kind: method-vocabulary; local-inference (owner decision 2026-07-02)

Evidence: [meta-types/](./meta-types/meta-types.md) (behavioral/connective/lifecycle cards) · [impl/spec/meta-types/](../impl/spec/meta-types/) (the `attribute-*` rule kinds)

Formal voice:

```text
declared-attributes convention =
  behavioral / connective / lifecycle concepts declare their discriminators in an Attribute | Value table;
  the validator reads the declared value (attribute-equals / attribute-present) instead of parsing the
  Formal cell. shape-only; keeps the semantic parse behind the engine moat.
```

Plain-language voice: declare-don't-infer — instead of the validator guessing a concept's kind from its body,
the concept states its discriminating attributes (`state_change`, `formal_return_type`, `scope`, …) in a table.

Domain-context voice: the owner decision (2026-07-02) powering the MT2/MT3 discriminators (`state_change`,
`formal_return_type`, `scope`, `temporal`, `direction`, `interface_kind`, `has_transitions`).

Use carefully: it trades some rigor (author self-declaration) for moat-safety — a declared value is checked,
not proven.

Misuse warning: do not infer the discriminator by parsing the Formal cell — that crosses into the engine moat
(a DEFINE-FALSIFIED boundary).

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a discriminator
decidable only by parsing the body, not declarable" → challenges the convention's coverage; owner route =
definitions-governance; gate = owner decision; blocking question = "can the discriminator be a declared value,
or does it need a semantic parse?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
the declared attributes discriminate all behavioral/connective/lifecycle pairs (tests green) + no open
contradiction; gate = definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local method vocabulary (DomainSpec v2); declared-value checks, never the engine semantic
parse (moat).

## DS-D1 — Meta-Type System

The **DomainSpec domain-vocabulary** scheme (`DS-D*`) — the node/edge alphabet — is maintained **separately**
from this file's governance/method scheme (`domainspec-v2-D*`), and linked here:

- **meta-type** = one of the 25 DomainSpec concept types (the node alphabet of an aspect file).
- Human cards (per type, 3-voice): [meta-types/meta-types.md](./meta-types/meta-types.md)
- Machine view (registry): [meta-types/meta-types.yml](./meta-types/meta-types.yml)
- Criterion (per type, machine-checkable): `impl/spec/meta-types/<category>/<type>.schema.yml`

Status: `DS-D1.1..14` (backend) authored as candidate cards (1-by-1, owner-reviewed voices; each with a
challenge + confirm contract). `DS-D1.15..25` (UI) deferred (MT5); edge verbs (`DS-D2`) + the edge signature
(`DS-D8`) follow after batch-1 R3.

<!-- SKELETON note: D1-D2 mint-seeded; D3-D5 consolidated 2026-07-01 into this canonical home (was the
     separate governance surface DSV2-D1/2/3, now removed). Companions backfilled 2026-07-01 to the current
     mint baseline: DEFINITIONS-INDEX + DEFINITION-DRIFT-AUDIT + DEFINITION-LOCALIZATION-ROUTE + reviews/.
     Still owed: layering-governance + drift-governance kind cards (tracked as owed in the drift audit).
     DS-D1 meta-type system lives in meta-types/ (human meta-types.md + machine meta-types.yml), linked above. -->
