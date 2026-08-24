# Join — Ontology Dialect Convergence

Sheet v2 `f41492e1…`. Three receipts, all returned. Tension gate: checker PASS, reviewer PASS,
one contradiction resolved by the strategist. Every load-bearing number below was re-verified by
the parent against the corpus; agent claims the parent could not confirm are marked FALSIFIED or
UNVERIFIED.

## The finding that reframes the question

**`ontology-vault` already emits a JSON record, and it is outside its own contract.**

`projects/cyberalchemy-orchestrator/.../ontology/history/canonical-0.2.0/receipts/CURRENT-STATE-2026-08-05-VALIDATION.json`

```
schema_version:  domainspec.ontology-vault.validation.v1
authority_effect: none
keys: invocation_id, validated_at, mode, repository, ontology_type,
      ontology_type_selection, branch, runtime
```

The sigil's `<default-output>` names only markdown. It emitted this anyway. So "should JSON be the
default creation pattern" is not a proposal — it is a description of undeclared existing behaviour.

The package also contradicts itself: `arcanum/arcana/ontology-vault/catalogs/ontology-types.json`
uses `catalog_version: "ontology-vault-types/v1"` (slash grammar, key `catalog_version`) while the
record it emits uses `schema_version` in dot grammar. Different key and different grammar inside one
package. The sigil exhibits the dialect problem it would be legislating about.

## Verdicts

**Agent 2 — no standing: REFUTED ON DISK.** The standing question is moot because the sigil already
emits. But its central mechanical argument SURVIVES and binds everyone:
`projects/cyberalchemy-orchestrator/.../ontology/schemas/ontology.schema.json` carries **15
`additionalProperties: false` blocks and a `const`-pinned `schema_version`** (parent-verified). Any
sigil-imposed top-level key would make that owner's own validator reject its own files. Imposition is
not merely ultra vires; it breaks working repositories.

Three of its supporting claims are FALSIFIED: augmentor does carry `schema_version` (506 files, not
"none"); `owner_route` is a string in body-war (292), orchestrator (21) and augmentor (15), not an
object; animejs nests authority in exactly 1 file, not as a systematic census undercount. Its
headline against Agent 1 does not survive. It did withdraw its "sixteen owners chose their shapes"
claim once shown `authority_effect` is 96% constant.

**Agent 1 — minimum header: LARGELY SELF-DEFEATED, CORE SURVIVES.** It opened by demolishing its own
angle, as instructed, and the demolition holds: records carrying all three concepts together number
71 of ~1500; `authority_effect` is `none` in 96% of its 366 files (parent-verified 353/366);
`schema_version` is a homonym. What survives is not a header to ratify but an emission rule — emit on
newly created records only, rewrite nothing, resolve dialects in the reader via an owner-declared
alias table where "does not carry it" is a reportable non-failing state.

**Agent 0 — converge: PRICED HONESTLY, PRICE IS HIGH, BLOCKED BY ITS OWN CITE.** Migration ledger:
1497 records → 418 mechanical, 367 namespace, **616 (41%) requiring authorship, not conversion**,
collapsing to ~255 candidate kinds ≈ 307 human decisions. It then cites the rule that stops it:
SKILL.md rule 26 forbids the sigil emitting a source mutation over owner evidence, so convergence is
opt-in per directory and **no owner route exists for cross-project ontology migration**. It named
this as its largest unresolved risk rather than eliding it.

## Where all three converge

Despite opposed angles, the three agree on the scope rule, and it is the answer:

> **The contract governs what the sigil writes. It never governs what owners write.**

- Agent 0: "The contract governs what the sigil writes, not what owners write."
- Agent 1: "emit three concepts on newly created records only; rewrite nothing."
- Agent 2: the sigil may not impose on existing owner files — and the orchestrator's closed schema
  proves imposition breaks them.

Zero rewrites is not a compromise between the three positions. It is the intersection all three
reached independently from opposed premises.

## Corrections the parent made to its own sheet

The sheet given to the agents contained three parent errors, all corrected mid-run and re-verified:

1. `authorityClass`/`authority_class` (127 files, all value `private`) is NOT a variant of
   `authority_effect` (values `none`/`owner-decision`/…). Value intersection EMPTY — a visibility
   class versus an effect. "Any authority key: 493 (32%)" over-counted by 127; correct is 366 (24%).
   The sheet's own framing committed the collapse Agent 2 argues against.
2. `schema_version` is a homonym, not a dot/slash grammar split: 479 slash and 304 dot type
   identities plus **188 bare semvers** carrying document version and no type identity. The parent's
   earlier "492 dot / 479 slash" mis-classified semvers as dot-grammar.
3. `authority_effect` is 96% the constant `none`.

An earlier sheet also declared a tilt toward the minimum header on the claim that it was "already
majority-adopted." Verification killed it: `owner_route` is 88% body-war alone, `authority_effect` is
69% augmentor alone. The tilt was removed rather than restated.

## Unresolved

- **616 records need per-record owner authorship.** No angle resolved this; Agent 0 priced it.
- **No owner route exists for cross-project ontology migration.** Rule 26 blocks the sigil and names
  no successor.
- **Denominators do not reconcile**: parent 1518 records / 16 dirs; Agent 0 1515 / 14 roots; Agent 1
  1519 / 11 JSON-bearing dirs; Agent 2 ~16030 repo-wide including `development/` and staged trees.
  Proportions agree; absolutes do not. No count in this run should be quoted without its scope.
- **The governance blocker from the prior run stands**: Template promotion gate `pending`, Label
  governance gate `deferred`, OVS-GATE-001 still disallowing canonical template promotion.

## Recommended next route

Not a schema selection. Two bounded items, in order:

1. **Fix the sigil's own inconsistency first** — one package emitting `catalog_version` in slash
   grammar and `schema_version` in dot grammar cannot coherently propose a convention. This needs no
   gate; it is internal consistency.
2. **A decision gate** continuing the OVS series, scoped to: declaring the already-occurring JSON
   emission in `<default-output>`, bounded to sigil-written artifacts, zero owner rewrites — and
   whether that declaration may proceed while the Label governance gate holds `meaning` deferred.
