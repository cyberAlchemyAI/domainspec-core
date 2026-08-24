# Agent 2 — "No standing"

**Verdict: `ontology-vault` keeps emitting markdown reports by default, and imposes zero record keys on owner ontologies.**

## 1. The standing argument

`arcanum/arcana/ontology-vault/SKILL.md` `<default-output>` already sets the default emission to a **markdown report** (`.arcanum/ontology-vault/<mode>-<date>.md`). The sigil reads and reports; it does not format. The 1067 record-per-file objects are owner source material, not sigil output. Three clauses make imposition a spec violation:

- `<project-runtime-profile-arguments>`: profile outputs "are not promotion verdicts, source authority, spec mutations, runtime conformance verdicts, or canonical source edits unless a separate owner route explicitly permits that movement."
- Step 5 clause 41: "Do not mutate conventions unless the user explicitly approves the change." Clause 39 lists **schema conventions** as that class. A default key mutates schema convention at 16 sites with no owner's approval.
- `<anti-patterns>`: "**hardcoding one project-local runtime profile into the reusable sigil contract**"; "letting a generated projection or profile report become canonical authority by proximity."

The first names Agent 1's proposal verbatim: `owner_route` is 88% body-war, `authority_effect` 69% augmentor.

## 2. The architecture-property counter

The catalog declares its own authority: `arcanum/arcana/ontology-vault/catalogs/ontology-types.json` sets `"authority_effect": "none"`, purpose "Select the primary modeling job for an Ontology Vault invocation **before source discovery**" — it routes an invocation, touching no byte on disk. Compare `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md`: "Use authority kinds to route a candidate to the correct owner. Do not use them to decide the candidate." Routing ≠ deciding.

Binding is owner-elected. `projects/cyberalchemy-orchestrator/.../ontology/schemas/ontology.schema.json` is the *owner's* schema — own `$id`, own 0.1.0→0.2.0→0.3.0 migration tree, `"schema_version": {"const": "rwo-architecture-property-ontology/v1"}`, **15 `"additionalProperties": false` blocks**. The sigil supplied none of it. `projects/animejs/.../profile.json` voluntarily declares `"ontology_type": "knowledge-vault"`; body-war's and augmentor's declare none — the catalog is a menu, two of four decline. `additionalProperties: false` settles it mechanically: an imposed top-level key makes the orchestrator's **own validator reject its own files**.

## 3. Criterion 1 — what is forgone

A **single-pass cross-ontology authority sweep** ("every record whose authority effect is not `none`, by owner") cannot be written once; it needs a per-dialect adapter (≥3 today). The sharp cost is not the adapters but **silent under-coverage**: a new 17th ontology returns *zero rows* rather than erroring, so the sweep looks healthy while blind. Audits must ship a dialect registry and fail closed on unregistered ones — recurring maintenance I ask readers to accept. Priced honestly the sweep is worth less than it sounds: `authority_effect` is ~96% `none` (§5c), so it returns few rows. That lowers what I forgo, and equally lowers the interop prize any rival can claim.

## 4. Criterion 2 — rules relied on, guarantee forgone

Relied on, overriding none: SKILL.md `<default-output>`; the `<project-runtime-profile-arguments>` non-authority clause; Step 5 clauses 39/41; Step 1 clause 12 ("Preserve local label names as aliases only when reporting… Do not promote local labels into canonical Arcanum vocabulary"); both anti-patterns above; `catalogs/ontology-types.json` `authority_effect: none`; `cyberAlchemy-v2/ontology/projections/README.md` ("Projections are read models… They do not create authority"); `cyberAlchemy-v2/ontology/AUTHORITY-POSTURES.md` `posture.generated` blocked use "Canonical source."

**Guarantee readers lose:** no field is guaranteed to exist anywhere. No consumer may assume `schema_version`, an authority key, or an owner key is present; every consumer handles absence explicitly, and no completeness check spans owners — only each owner's own schema.

## 5. Criterion 3 — validator

`owner_declared_conformance.py` (this directory) uses a **read-side alias table** — the executable form of SKILL.md Step 1 clause 11, "Translate local labels into generic Arcanum concepts." It asks owners for nothing.

Across **5 packages / 3 dialect signatures / 386 records**: P1 (one spelling per concept per package) 4/5; P2 (dialect-id denotes one shape) 4/5; **P3 (no file carries two spellings of one concept) 5/5**, reproducing the sheet's zero-homonym finding. **Conformance across ≥3 dialects is verifiable with zero imposed keys.**

Method matters more than score: four times the validator reported failure, and four times the *reader* was wrong, not the owner —

1. `schema` (dialect id, `@` grammar) conflated with `version` (semver);
2. animejs carries authority **nested** as `{"class","effect"}`, invisible to a flat-key census;
3. augmentor's `owner` is a **SHA-256 digest**, not a governance route;
4. body-war's dot/slash split tracks **record family** (`oew.*` vs `body-war-*`), and `body-war-branch-view/v1` is a tagged union discriminated by the owner's own `branch_role`.

Each time the owner had a coherent local scheme my cross-owner expectation had not learned — the empirical case for no standing, not a rhetorical one. Two residual failures I decline to tune away (animejs's profile-vs-record spelling; the branch-view union) are real, owner-fixable locally, and need no cross-repo key.

### Parent evidence corrections, verified independently

**(a) `authorityClass`/`authority_class` is not a spelling of `authority_effect`.** Class values are dominated by `private`/`public` (visibility); effect values run `none`, `bounded-execution-only`, `blocked`, `owner-decision`. Dominant value sets are **disjoint**. This is the collapse I argue against, already realized — in the *analysis*, not the corpus. Imposing one canonical `authority_effect` spelling would have folded augmentor's visibility class into an effect field, destroying a distinction its owner draws. Finding 2 corroborates it independently: animejs stores `authority = {"class": "private", "effect": "none"}` — one owner modelling **both** concepts at once, with exactly those value domains. Owners distinguish what a flat census merges. The errors run opposite ways: "any authority key" **over**counted by folding class in; `authority_effect` **under**counts nested carriers.

**(b) `schema_version` is a homonym over three concepts** — slash and dot *type identities*, plus bare semvers (`1.0.0`) carrying *document version*. Deciding which a record means is authorship about what the record **is**; no format default can answer it. It also bounds my validator, and I state the limit rather than hide it: P2 dispatches on the full dialect-id string, which works for type identities and **cannot** work for bare semvers — `1.0.0` identifies nothing. Those need an owner-context fallback I did not write.

**(c) `authority_effect` is ~96% the constant `none`.** This cuts against me. My angle says sixteen owners *chose* their shapes; for this field that is thin, since a 96%-constant key is not evidence of active governance expression. What survives is narrower and still sufficient: the demonstrated choice sits at the **dialect** layer, not this field's value — three dialect signatures, different dialect-id spellings (`schema_version` vs `schema`), three value grammars, nested vs flat carriers, a tagged union. Standing rests on who may decide, not on expressive use. But "sixteen owners chose their shapes" overstates the per-field evidence, and I withdraw it in that form.

## 6. What my position costs

- **Adapter maintenance is permanent** and grows per ontology. Bounded, but unending.
- **Silent blindness is the real hazard** (§3); nothing forces consumers to fail closed. The strongest argument against me.
- **My validator needed four corrections**, and (b) exposes a fifth I have not closed. A read-side table is harder to get right than a mandated key, and its errors are quiet — mine produced confident FAILs against innocent owners.
- **I resolve nothing today.** Sixteen owners keep sixteen shapes.
- **My rhetoric was looser than my evidence** (§5c).
- `cyberAlchemy-v2/ontology` has **zero** JSON outside `development/` — markdown, so Criterion 1's named cav2 dialect has no record files to change. That helps me, but the "16 directories" framing is looser than the sheet implies, weakening everyone's evidence base including mine.

## 7. Objections

**Agent 0 (canonical contract):** migration is owner-schema-*breaking*, not merely costly. Fifteen `additionalProperties: false` blocks and a `const`-pinned `schema_version` mean the orchestrator's validator rejects any canonical rewrite until its owner re-authors the schema, three migration generations, and the `history/canonical-*` trees. Name who may edit `urn:cyberalchemy-orchestrator:...:3` — not the sigil; clause 41 forbids it unasked. Correction (b) adds a prior question: the contract must first decide, per record, whether `schema_version` means type identity or document version. Authorship, not format.

**Agent 1 (three-key spine):** the keys are **homonyms, not shared vocabulary**. `owner_route` resolves to four incompatible referent kinds: `body-war.product-ontology-owner` (dotted local name); `rwo:owner.definition` (an ID into that file's *in-file* `owner_routes` table); augmentor's `task-session`/`invoke` (Arcanum capability names, not project owners); and orchestrator's `ownerRoute`, an **object** where body-war's is a **string**. The sheet rejected `schema_version` because "a shared key whose values disagree buys no cross-ontology tooling"; that defeat applies to `owner_route` too, and (b) shows `schema_version` is worse than the sheet said — three concepts, not two grammars. Augmentor's profile has **no `schema_version`**; it uses `schema`, so the largest directory (909 files) fails key one of three at its own profile. (c) compounds it: mandating a 96%-constant field buys near-zero information for a write obligation on every owner — and mandating its canonical *spelling* would commit exactly the class/effect collapse the sheet's own framing fell into.

## 8. Residue

- Flat cross-owner key censuses both over- and under-count (§5a). Count-based proposals should be re-run **path-aware and value-aware** before they are trusted.
- Real convergence exists at the **profile** layer, not the record layer: `package_id` and `claim_ceiling` appear in all four owner profiles, unimposed — evidence imposition is unnecessary. I deliberately do **not** propose promoting them; that would be my own anti-pattern.
- Unclosed: bare-semver `schema_version` records cannot be dispatched on value (§5b).
- Owner-owned: whether `authority.effect` (profile) and `authority_effect` (record) are one concept at two layers. Only animejs's owner can say.
- Untested: whether consumers fail closed on unknown dialects. If they fail *open*, §6's hazard is live today.
