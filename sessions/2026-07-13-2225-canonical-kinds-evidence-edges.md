---
tags: [ontology, canonical-kinds, evidence, edges, durability, schema, cyberalchemy-v2]
node_type: discovery
is_session: true
layer: ontology
nature: explanatory, technical
status: active
created: 2026-07-13
timestamp: 2026-07-13T22:25:00-03:00
expires: 2026-09-11
conversation_id: 2026-07-13-canonical-kinds-evidence-edges
decisions_made: true
contradictions_found: true
specs_updated: [cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md, cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml, cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Settles the Evidence instance contract and the first machine-readable edge schema for the four Evidence kinds, and in doing so falsifies the `durability` axis twice — the second redefinition exposes four enumeration rows that were never derived from anything and leaves `contradictions` provably underivable from it."
---

# Canonical Kinds — the Evidence contract, and durability falsified twice

## Summary

The session set out to fix the rules of `CANONICAL-KINDS.md` and became a rebuild of the
Evidence layer. Four decisions landed on the instance contract: the `bounded`/`accreting`
axis was struck as doing no work; `canonical_kind` left the frontmatter entirely and became
the filename, with `title` identifying the instance; the required `synthesis` field was
renamed `description` because "synthesis" was simultaneously the name of a field on every
artifact and the name of what a `findings` *is*, and it was given a real contract — it is the
string that gets embedded into RAG, so it must discriminate, be dense, carry no filler, and
stand alone; and `residue` was struck as a canonical kind and made an attribute, on the
owner's test that a `residue.md` full of unhomed questions would be an absurdity. `session`
was brought into the contract as the fourth Evidence kind. On edges, four were settled —
`findings derives-from research` (the synthesis rests on the aggregate), `discovery
derives-from research`, `research derives-from discovery` (optional: a research answering a
discovery's open question, or dispatched cold), and `session creates artifact` — and written
to two new YAML files, `ALLOWED-EDGES.yaml` (what is permitted; anything absent is forbidden)
and `EDGES.yaml` (what each verb means). The load-bearing failure was `durability`: it was
first redefined to govern mutation, then falsified by the owner ("I can change a discovery"),
then redefined again to answer one question only — *does this artifact claim to hold now?* —
with `contradictions` deriving from it. Four review agents across two dispatches then
established that this second definition does not rescue the axis either: `backlog` and
`ledger` carry `contradictions` values the derivation cannot produce, and `readme` and
`projection` are mislabelled under the new question — not because the definition is bad, but
because the enumeration was never derived from any test, and writing one exposed the rows.
The axis survives; the table does not.

## Contradictions

- questions `implementation/domainspec/vault/ontology-conventions.md` — three of its edges
  (`synthesized-by` :582, `corroborates` :583, `retrofits` :584) assume `research` = the
  synthesis and `findings` = raw lens output, the exact inverse of the research-first
  direction settled here. The same two filenames carry opposite roles in the two patterns.
  Owner deferred reconciliation; recorded, not resolved.
- questions `cyberAlchemy-v2/authority/decisions/2026-07-13-canonical-kind-one-label.md` — the
  decision fixes `canonical_kind` as a frontmatter field ("the field is defined and unused").
  The filename ruling abolishes that field. The decision's carrier premise is superseded and
  carries no supersession note.
- questions `cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml` — whether `refutes` carries
  force or is a bare annotation is unresolved and recorded there. If it lowers its target's
  standing, a session — which can never bear authority — demotes an artifact that can.
- questions `cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml` — `discovery -> findings` is
  forbidden while `discovery -> research` is allowed, so a discovery rests on the raw aggregate
  but not on the verdict. Recorded there as unexamined, not defended.

## Open questions

- Is `contradictions: tolerated` right for the Evidence kinds at all? Two `findings` from the
  same dispatch reaching opposite conclusions is a defect that must be resolved, not two
  harmless records of different moments. The "different moments" defence confuses when an
  artifact was *written* with what it is *about*.
- Should any edge ever be mandatory? Today none is. Nothing obliges a synthesis to point at
  what it synthesized.
- Is `implementation-plan` `ephemeral` or `perennial`? Its row says it *prescribes execution*,
  and a prescription binds now — which is `perennial`. The row says `ephemeral`. Both cannot
  stand, and which one falls is the owner's call, not a derivation.

## Next steps

- Correct the enumeration rows in `cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md`
  that the durability redefinition exposed: `backlog` and `ledger` (contradictions values the
  derivation cannot produce), `readme` and `projection` (they assert what the thing *is now*,
  so `perennial`), and strip `(regenerable)` from the durability column — it is a mutation fact
  sitting in a two-valued enum.
- Fix OQ-11's Revisable row in the same file — it reads "every `ephemeral` kind", inferring
  mutation from durability inside the section that forbids that inference.
- Fix the acyclicity self-contradiction in the same file: the Evidence-edges section states
  that instance acyclicity is unenforced, and the four-class table thirty lines later still
  states that durability enforces it. Both were written this session.

## Recommendation

Attack the enumeration rows first, ahead of the two file-internal fixes. The license is
concrete: two independent review agents, one assuming the durability definition true and one
attacking it, converged on the same rows — so the failure is in the table, not in the axis.
Until those rows are re-derived, `contradictions` is a free value wearing a derived value's
clothes, and anything that reads it is reading a column that was hand-patched twice. The two
self-contradiction fixes are real but local; the table is what everything else rests on. The
edge schema is safe to build on; the kind table is not.

## Files touched

- cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md
- cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml
- cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml
- telemetry/agents/subagents-dispatch.yaml
