# Agent 1 — "Minimum header" — receipt

Counts are my own (11 JSON-bearing ontology dirs, 1519 records). Validator `spine-check.py`,
output `spine-check.out`.

## 1. The strongest case against my own angle

My census makes my position worse than the sheet's.

**(a) The spine is 4.7% adopted.** Records carrying all three concepts *together*: **71 of
1519**; 293 (19.3%) carry none. There is no consensus to ratify.

**(b) `authority_effect` is near-constant.** 353 of its 366 values are `none` (96%). It
does not discriminate; it decorates. This is the worst single fact for my angle.

**(c) The sheet's "variants" are not variants — which cuts against me.** `authorityClass`
(91) + `authority_class` (36) hold exactly **one** value across all 127 files: `private`.
`authority_effect` holds `{none, owner-decision, blocked, …}`. **Intersection: empty** — a
*visibility* class versus an *effect*. Likewise `ownerBoundaryResult` ∈ {pass, reject} is a
check result, not an owner. So "any authority key: 493" over-counts by 127; the real figure
is **366 (24%)**. My key is rarer than advertised.

**(d) The grammar split is worse than dot-vs-slash — it is an *arity* split.**
`body-war-business-node/v1` is 2-segment (no namespace); `rwo.current-state-evidence.v1` is
3-segment. Worse, **319 records put a bare semver (`1.0.0`) under `schema_version`** — a
version with no type identity. Not variance but a **homonym**: one key, two concepts,
unfixable by regex.

**(e) The governing anti-pattern is aimed at me.**
`arcanum/arcana/ontology-vault/SKILL.md:388` forbids "hardcoding one project-local runtime
profile into the reusable sigil contract." `owner_route` is 292/329 body-war,
`authority_effect` 251/366 augmentor. Promoting them is exactly that.

## 2. What survives

The three-key spine *as a header to be adopted* is dead; I do not defend it. What survives:
**emit three concepts on newly created records only; rewrite nothing; resolve dialects in
the reader, not the record.**

- `schema_version` — required, type-identifying, normal form `(namespace?, name, version)`.
  Bare semver rejected *for new records*: 319 existing ones prove the key is ambiguous
  without that constraint.
- `authority_effect` — emitted only when non-`none`; at 96% `none` a default is noise.
- `owner_route` — emitted; no value grammar imposed.

**On dot/slash I pick neither.** One normalizer with two arities reads both: **835 of 1147
typed values (73%) across 5 dialects normalize under a single function**. The residue is the
312 homonyms, which no grammar choice fixes.

## 3. Criterion 1 — dialect fit (costing)

**Files changed: zero** in augmentor, body-war, cav2, orchestrator.

**Alias resolved:** `authorityClass` does **not** satisfy `authority_effect`, and augmentor
must **not** rename — not because renaming is costly but because they are
different concepts (empty value intersection, §1c). Renaming would destroy the `private`
visibility fact and fabricate an effect claim. Augmentor keeps `authorityClass` and is
recorded as **not declaring** `authority_effect`. **Cost:** its authority coverage reads
251/909 permanently; my spine can never claim augmentor conformance.

**Interoperability forgone:** (i) no cross-ontology join on authority effect — 1153 records
have none; (ii) the 319 bare-semver records stay unresolvable to a schema; (iii) 350 scanned
records carry no type id, invisible to type-indexed queries. A reader gets a **census, not a
join**. Performed by the sigil's emit path only, under Rule 41.

## 4. Criterion 2 — owner non-collapse (costing)

Relied on, not overridden (all `arcanum/arcana/ontology-vault/SKILL.md`): **Rule 41 (:311)**
no convention mutation without approval — zero-rewrite honors it. **Rule 39 (:310)** demands
migration impact / affected files / rollback: affected files = 0, rollback = delete the
default. **Rule 22 (:273)** no profile labels into canonical vocabulary. **Rule 26 (:283)**
blocks source mutation; emit-on-new is not one.

**Overridden: the anti-pattern at :388.** Promoting `owner_route` / `authority_effect` —
each one directory's convention — into the reusable contract *is* hardcoding a
project-local profile. **Cost:** body-war's and augmentor's vocabulary becomes the default
for every future repo with no stake in either. I cannot pay this down, only bound it to
three concepts, two satisfiable by omission.

**Guarantee readers do not get:** absence of `authority_effect` can never be read as
"checked and none" rather than "never modeled." At a 4.7% baseline absence is the norm: the
spine supports **counting, not inference**.

## 5. Criterion 3 — executable check

`spine-check.py` runs over 5 dialects (body-war, augmentor, cav2, orchestrator, animejs),
1497 records, zero rewrites.

It avoids collapsing owner authority because **the alias table is owner-declared**: each
owner registers which local key carries each concept, and `None` — "does not carry it" — is
a reportable, non-failing state (cav2 and animejs both hit it). The sigil owns three
*concepts*; owners own *spellings* and *value spaces*. Adding a dialect is one table row.
It proves conformance **computable**, not **useful**.

## 6. Objections

**Agent 0 (canonical contract):** your migration touches ≥1067 records, but **319 carry a
bare semver under `schema_version`**. No script can derive a type identity from `1.0.0` —
the information is not in the file. Those are not renames but 319 acts of *authorship*:
the owner must decide what each record is. Price them as human decisions or the cost
accounting is fiction.

**Agent 2 (no standing):** right that the sigil may not *impose* on existing owner files —
conceded, I rewrite zero. But you over-reach on emission. SKILL.md:31 grants
`convention-update` explicit standing to *propose* schema conventions, and Rule 39 presumes
a proposal has "affected files" and a "rollback path" — clauses a sigil with no format
standing would never need. Standing to propose under approval is not standing to impose.

## 7. Residue

- The 319 bare-semver homonyms need per-record owner authorship; no angle here resolves them.
- `authority_effect` at 96% `none` may be a dead key. Nobody tested whether any consumer
  reads it; that test should precede adoption.
- Census covers JSON objects only — not the 5 carrier docs or 541 markdown files.
- I found 11 JSON-bearing ontology dirs / 1519 records vs the sheet's 16 / 1518. Records
  reconcile; the directory count does not.
- `ontology-candidate-graph-prototype` `npm test`: 59/59 pass; spine check not wired in.
