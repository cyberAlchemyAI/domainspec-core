# Agent 0 — Converge

**Verdict: emit a canonical JSON record by default; markdown becomes a rendering.**
Sheet sha256 verified; counts re-derived. Parent's three corrections verified (two
deltas, §6).

## 0. The homonym

Of 971 string values, **184 are strict `\d+\.\d+\.\d+` semvers** carrying document
version and **no type identity anywhere in the file**. The other 787 carry an identity
in four delimiter styles: slash 367, dot 250, **hybrid 109**
(`arcanum.background-helper-receipt/v1`), at-sign 60, unparseable 1.

The hybrid has a dotted identity *and* a slash version, so all 787 share one
`(identity, version)` structure differing only in delimiter — mechanically resolvable.
The 184 semvers are not a third grammar: they are `record_version` values whose
`record_kind` was never written. **Splitting the field does not paper over the
homonym, it names it.**

## 1. The contract

- `record_kind` — `^[a-z0-9]+(\.[a-z0-9]+(-[a-z0-9]+)*)+$`
- `record_version` — `^v[0-9]+(\.[0-9]+)*$`
- `authority_effect` — closed enum: the 6 observed values (`none`, `owner-decision`,
  `protected-production-deployment`, `bounded-execution-intent-only`,
  `refine-planning-only`, `planning-only`)
- `owner_route`, `source_identities` (non-empty), `emitted_by`
- `visibility` — **optional and separate**. All 127 `authorityClass`/`authority_class`
  files carry `private`, and **zero** also carry `authority_effect` (verified): empty
  intersection, different concepts. Merging them would destroy a visibility fact and
  fabricate an effect claim, so the validator *rejects* the merge. Likewise
  `ownerBoundaryResult` ({pass 37, reject 1}) maps to `checks[].result`.

**Does `authority_effect` earn its place at 96% constant (351/364 `none`)?** Not as a
discriminator — conceded. It earns it as an *invariant*: the 13 non-`none` records are
what a query must find, and two are free text. Five fields discriminate; this asserts.

## 2. Criterion 1 — migration ledger

(96 further files are JSON Schema documents, out of scope.)

| directory | records | mechanical | namespace | **authorship** |
|---|---|---|---|---|
| augmentor | 909 | 332 | 8 | **530** |
| body-war | 334 | 2 | 314 | **9** |
| cav2 | 87 | 57 | 0 | **30** |
| animejs | 42 | 19 | 0 | **12** |
| orchestrator | 125 | 8 | 45 | **35** |
| **total** | **1497** | **418** | **367** | **616** |

**616 records (41%) no script can convert** — 438 with no version key, 177 bare
semvers, 1 unparseable. The identity was never written, so there is nothing to rename:
the owner must decide what each record *is*. They cluster into **255 candidate kinds
across 211 directories** — ~255 decisions, not 616, and it collapses no further. The
367 namespace records reduce to only **52 distinct strings**. **Total: ~307 human
decisions + 418 mechanical edits, by each owner — never the sigil (§3).**

## 3. Criterion 2 — owner rules

Cites are `arcanum/arcana/ontology-vault/SKILL.md` unless noted.

**Relied on.** `:356` "identify migration impact before convention changes" and `:379`
— the sigil's own bar contemplates convention change, conditioned on exactly this
ledger. `:271-273` (rule 22) and `:374` are honored: `record_kind` is **opaque**, so no
owner taxonomy reaches canonical vocabulary.
`cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:4-8` "A session bears no
authority" — `authority_effect: none` encodes that.

**Overridden, with cost.** (1) `:152-159`, the markdown default-output ladder —
`.md` readers must re-point. (2) Dot over slash: body-war's 314 and the orchestrator's
45 lose their delimiter, mitigated by `legacy_schema_version`, which retains the
original string, making the rewrite reversible. `:387` is *not* overridden — dot comes
from the sigil's own emission.

**Binding ceiling.** `:285-288` (rule 26) forbids emitting "a source mutation … or
generated projection that outranks its owner evidence." The sigil may define the shape
of what *it* writes and may never rewrite an owner's records. Convergence is thus
opt-in per directory and can stall; readers lose joins over directories that decline.

## 4. Criterion 3 — validator

`converge/validate_canonical.py` — stdlib only, read-only. Covers **five** dialects
(>3 required). Projection unit checks 6/6 PASS on real on-disk values; envelope checks
accept the conforming record and reject **7/7** mutations with named violations,
including free-text authority, `authorityClass` merged into `authority_effect`, and
`ownerBoundaryResult` used as an owner. `RESULT: ALL CHECKS PASS`. Precedent:
`.../validate-routing.mjs:19` already asserts `authority_effect` on a sigil-owned
artifact; the cav2 prototype passes 59/59.

## 5. Objections

**To Agent 1 (three-key spine).** A shared key without a closed value grammar is a
column header over incomparable cells — and `schema_version` is worse, a homonym whose
184 semver values are document versions, not identities. Agreeing on it buys zero
joins *and hides that absence*. `authority_effect` has 8 values, 2 free text, 96%
`none`; `owner_route` is 292/330 body-war while augmentor prefers `lifecycleOwner`
91:15. The spine costs nothing, which is what it delivers.

**To Agent 2 (no standing).** Settled on disk, against him. The sigil *already* emits
a JSON record bearing `schema_version` and `authority_effect: "none"`, and its own
package ships a validator asserting that key. The contract governs what the **sigil
writes**, not what owners write: `:124-128` scopes profile outputs as artifacts that
"are not … source authority, spec mutations." Rule 26 — which I keep — enforces the
non-collapse he wants. His premise that owners *chose* these shapes fails: augmentor
emits four grammars internally, and the sigil package itself two
(`catalogs/ontology-types.json:2` vs its emitted record).

## 6. Residue

- **616 records (41%) require authorship, not conversion.** The strongest argument
  against my angle; I priced it, I did not defeat it.
- **No owner route exists for cross-project ontology migration** — rule 26 blocks the
  sigil and names no successor. The largest unresolved risk here.
- Deltas from the parent's figures: **184** strict semvers (not 188) and **364**
  `authority_effect` files (not 366) over my 14-root set; totals differ from the sheet
  (1515 vs 1518) because nested `staged/` run replicas are excluded. Unreconciled.
- Whether the 438 identity-less records are *intended* as records: sampled only.
- Siblings not read (barred); §5 attacks the sheet's angles, not their arguments.
