---
name: authority-triage
description: "Use when: a candidate (claim, term, principle, rule, practice, decision, artifact, or a note captured only in memory/chat) might need to become governed authority — classify whether it needs authority at all, sweep for an existing owner (build-from-owned), determine the kind, and route it through the narrowest owner's governance cycle. Promotes nothing itself."
argument-hint: "<candidate> [--home chat|memory|doc|inventory] [--dry-run]"
tier: arcana
domain: authority-governance
version: 0.1.0
status: candidate
origin: created to operationalize cav2 AUTHORITY-MODEL's Narrowest-Owner Rule + Authority Kinds table + CAV2-D49 default-deny as an executable front-door classifier/router; no existing sigil takes an arbitrary candidate and decides "does this need authority, which kind, route it". Build-from-owned on AUTHORITY-MODEL.
promotion_target: arcanum/arcana/authority-triage/ (after experiment-harness validation)
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# Sigil: Authority Triage

<objective>
Given a candidate, decide **whether it needs to acquire authority at all**, whether it is **already owned**
(build-from-owned), what **authority kind** it is, and **which owner's governance cycle** it routes to —
emitting a routing decision and a handoff. This sigil **promotes nothing**; it classifies and routes.
</objective>

<logic-type>
Arcana: authority-routing classification over the cav2 authority model. The executable front-door of the
router -> owner -> promotion chain.
</logic-type>

<source-authority>
Build-from-owned. The classification and routing logic is OWNED by:

- `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md` — the **Authority Rule** (authority moves by owner route),
  the **Authority Kinds** table (Definition/Constitution/Discipline/Decision/Spec/Runtime-contract/Projection/
  Evidence/Residue + default-deny), the **Narrowest Owner Rule** (the movement->owner table), and the
  invariant->axiom->constitution->gate derivation.
- `CAV2-D48` authority promotion lifecycle (the staged path) and `CAV2-D49` closed authority-kind enumeration
  (default-deny for unenumerated kinds).

This sigil does not redefine any of those; it executes them. On conflict, the AUTHORITY-MODEL wins.
</source-authority>

<applicability>
Use when:
- a claim/term/principle/rule/practice/decision/artifact might need to become governed authority;
- a principle is captured only in chat or Claude Code **memory** and you want to know if it should be promoted;
- you are about to assert something as a rule and are unsure whether it is already owned;
- a candidate kind is not obviously one of the enumerated authority kinds (default-deny check).
</applicability>

<non-applicability>
Do not use when:
- the candidate is a one-off task or a per-task note with no governing reach (it stays evidence/inventory);
- you want to actually PERFORM a promotion (route to the owner — definitions/constitution/discipline-governance,
  decision-gate — this sigil only classifies and hands off);
- the candidate is plainly a definition/constitution/etc. with a known owner and no ambiguity (call that owner directly).
</non-applicability>

<inputs>
- the candidate (text or artifact ref);
- its current home (chat | memory | doc | inventory | code);
- optional: the scope it would govern, and any suspected owner.
</inputs>

<chain-boundary>
Authority-triage is a **classifier/router**, not an owner.

- `definitions-governance` owns terms/definitions (and axiom candidates' definitions).
- `constitution-governance` owns enforceable rules/constitutions (and adding a new authority kind).
- `discipline-governance` owns recurring cross-capability practices.
- `decision-gate` owns contested promotion/scope/naming/public-private choices and is co-owner of any new-kind admission.
- `inventory` / `ontology-vault` own candidate read-models and ontology candidates.
- the VALUE/philosophy surface owns value/proposition statements (per the HMI precedent + condense-knowledge).

This sigil routes to exactly one narrowest owner and writes nothing into their authority surface.
</chain-boundary>

<process>
1. **Intake.** State the candidate and its current home. If it lives only in chat/memory, note that **memory is a
   low-authority capture surface, not authority** — promotion (if any) is a separate owner act.

2. **Precedent sweep (build-from-owned — do this BEFORE any "create new" verdict).** Sweep for an existing owner:
   `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` + `DEFINITIONS-INDEX.md`, `authority/constitutions/`,
   `disciplines/`, `authority/decisions/`, the skill surfaces, and `.arcanum/inventory/`. A **found owner is a
   POSITIVE result, never a kill**: emit `build-from-owned` — route to the existing owner (cite it), and if the
   candidate merely restates the owner, emit `already-authority` (no new work). The lone exception is owned **and
   already enacted** -> `already-authority`.

3. **Needs-authority test.** Ask: would this candidate **change what the project is allowed to rely on, or govern
   future work**? (AUTHORITY-MODEL Authority Rule.)
   - NO -> emit `not-authority`: it is **evidence / a note**; keep it in inventory/memory/side-note; STOP.
   - YES -> continue.

4. **Classify the kind** (Authority Kinds + Narrowest-Owner Rule):
   | The candidate is... | Kind | Owner route |
   |---|---|---|
   | a term becoming load-bearing | Definition | definitions-governance |
   | a load-bearing principle (why governance is constrained) | Axiom-candidate (via Definition; highest bar) | definitions-governance + decision-gate |
   | a rule that should constrain future artifacts | Constitution | constitution-governance |
   | a recurring cross-capability practice | Discipline | discipline-governance |
   | a contested promotion/scope/naming/public-private choice | Decision | decision-gate |
   | a value/philosophy proposition (constrains but is not a method) | Proposition (NOT a definition) | VALUE doc + decision-gate |
   | a spec / runtime-contract / projection / evidence / residue | that kind | its owner |

5. **D49 default-deny check.** If the classified kind is **not a row** in the Authority Kinds table -> **BLOCK**:
   the kind defaults to denied; route to **decision-gate + constitution-governance to ADD the kind first** (with its
   D48 lifecycle), before the candidate can acquire authority.

6. **Consolidation check (Via Negativa).** If `build-from-owned` but the rule is **diffuse** (scattered across
   definitions/skills/docs), recommend a **consolidation** route (constitution-governance, deriving from the owner)
   rather than net-new authority — fewer, sharper rules, not more.

7. **Emit** the verdict + a one-line handoff to the narrowest owner. Promote nothing; record residue.
</process>

<authority-rule>
This sigil promotes nothing and creates no authority. Every verdict cites the AUTHORITY-MODEL row it rests on.
A found owner is build-from-owned, never a kill. An unenumerated kind is default-deny (CAV2-D49). Memory/chat
capture is not authority.
</authority-rule>

<observability>
When `.arcanum/observability/` exists, record: candidate, home, precedent-sweep result (owner found or clean),
needs-authority verdict, classified kind, owner route, default-deny block (if any), consolidation recommendation,
residue.
</observability>

<quality-bar>
A successful run must:
- sweep for an existing owner BEFORE any "create new" verdict (build-from-owned first);
- distinguish `not-authority` (evidence/note) from authority candidates — do not over-promote;
- classify the kind against the enumerated Authority Kinds table and cite the row;
- apply CAV2-D49 default-deny to unenumerated kinds;
- route to exactly one narrowest owner; write nothing into an authority surface;
- prefer consolidation over net-new when an owner already exists but is diffuse;
- return a clear verdict + handoff + residue.
</quality-bar>

<anti-patterns>
Avoid:
- emitting `new-authority` without a precedent sweep (the build-from-owned violation);
- promoting a candidate (this sigil only routes);
- treating a memory/chat note as authority;
- inventing a new authority kind without the decision-gate + constitution-governance default-deny route;
- classifying a value/philosophy proposition as a Definition (route it to the VALUE doc);
- over-promoting a one-off note that governs nothing.
</anti-patterns>

<output-contract>
Return:

```markdown
## Authority Triage Result
- Candidate: <text/ref> (home: chat|memory|doc|inventory|code)
- Precedent sweep: owner found <id+cite> | clean
- Verdict: already-authority | build-from-owned | not-authority | new-authority | blocked-default-deny
- Kind: <Definition|Constitution|Discipline|Decision|Axiom-candidate|Proposition|Spec|...|none>
- Owner route: <definitions-governance|constitution-governance|discipline-governance|decision-gate|VALUE doc|none>
- Consolidation: <recommended (route) | not needed>
- Handoff: <one-line ask to the owner>
- Residue: <what remains / why not promoted>
```
</output-contract>

<worked-example>
**Candidate:** "build-from-owned — before any KILL/net-new verdict, sweep for an owner; a found owner is
build-from-owned" (home: **Claude Code memory**).

1. Intake: lives in memory (a low-authority capture surface).
2. Precedent sweep: **OWNER FOUND** — `CAV2-D48` (its canonical definition *is* "the **build-from-owned**
   generalization of D43/D46/Growth-Rule"), and the research skill's precedent gate enforces it
   (`.claude/skills/research/SKILL.md`: "a found owner relabels the candidate build-from-owned ... never a kill").
3. Needs-authority test: YES, it governs work — but it is **already authority**.
4-5. Kind: Constitution-rule (already instantiated via D48 + the promotion ladder). Not unenumerated.
6. Consolidation: the crisp cross-capability rule is **diffuse** (D48 definition + research skill) -> **recommend**
   consolidating it into one constitution rule **deriving from D48** via constitution-governance.

```markdown
## Authority Triage Result
- Candidate: build-from-owned / precedent-sweep-before-kill (home: memory)
- Precedent sweep: owner found — CAV2-D48 + research-skill precedent gate
- Verdict: build-from-owned (already-authority)
- Kind: Constitution-rule (instantiated via CAV2-D48)
- Owner route: constitution-governance (consolidation only)
- Consolidation: recommended — one named rule deriving from CAV2-D48 (Via Negativa, not net-new)
- Handoff: "constitution-governance: consolidate the diffuse build-from-owned rule into one enforceable
  constitution rule deriving from CAV2-D48; cite the research-skill precedent gate as existing enforcement."
- Residue: the memory note is a personal restatement, not authority; do NOT create new authority.
```
</worked-example>
