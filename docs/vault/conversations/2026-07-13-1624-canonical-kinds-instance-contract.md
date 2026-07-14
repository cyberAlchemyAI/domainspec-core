---
tags: [cyberalchemy-v2, ontology, canonical-kinds, instance-contract, authority-layer, frontmatter-contract]
node_type: discovery
is_session: true
layer: ontology
nature: [reference, technical]
status: active
created: 2026-07-13
timestamp: 2026-07-13T16:24:41-03:00
expires: 2026-09-11
conversation_id: 2026-07-13-canonical-kinds-instance-contract
decisions_made: true
contradictions_found: true
specs_updated: [cyberAlchemy-v2/ontology/CANONICAL-KINDS.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Writes the first instance contract the canonical-kind system has had — fixing the type/instance split, making the kind the filename rather than a forgeable field, and adding a new kind (findings) — but leaves two named contradictions as carried debt and opens four questions rather than closing the design."
---

# Canonical-kind instance contract, and `findings` as a kind

## Summary

The session set out to design the frontmatter of a `discovery` and ended by writing the first
instance contract the canonical-kind system has ever had. The user's proposed "what is this
evidence for" field was traced to an existing owner rather than minted: `authority layer` is
already defined as `CAV2-D3` (active), so the field reuses promoted vocabulary — but the `layer:`
field live in 40 session records means subject/altitude, not authority-surface, and the two cannot
share a name. Two standing contradictions surfaced and the owner directed both be carried as debt:
`CAV2-D3` enumerates five authority layers while `CAV2-C2` enumerates ten and refutes itself by
listing `observability` against its own non-example; and `CAV2-C18` already requires canonical
artifacts to *declare* `authority_kind`, `process_origin`, `durability`, and `authority_state`,
which is precisely the pattern the new contract forbids. The type/instance split was fixed:
nothing type-level is written into an instance, because every such fact is a function of the kind.
The kind, in turn, is not a field at all — it is the **filename** (`research.md` *is* a `research`),
so an instance says nothing about its own type and there is nothing to forge; `title` is what
distinguishes one instance of a kind from another. That rule is scoped rather than repo-wide, and
says so: it already fails for `sessions/`, `authority/decisions/`, and `DEFINITIONS.md`, which
carry their kind in the path, in a slug, or nowhere. `durability` was kept as the axis and given a
second job — it governs mutation, where `ephemeral` means closed when written and superseded rather
than edited, so state belongs to the file and the file carries a bounded `synthesis`; `status` and
`authority_state` were struck from Evidence frontmatter as derivable or as edges. `findings` was
added as a canonical kind on three verified facts: a one-agent research dispatch emits
`findings.md` alone, review dispatches emit it too, and it is the file that gets cited while no
`research.md` ever is. Four questions were opened — `review` emits no `review.md` (OQ-9), `findings`
is the first kind with two producers (OQ-10), `perennial` covers three incompatible mutation
regimes (OQ-11), and filename-as-kind versus path-as-kind (OQ-12) — and the owner ordered all
changelog prose stripped from the file, including six pre-existing paragraphs.

## Contradictions

> Three of the four targets below live under `cyberAlchemy-v2/**` and carry **no `node_type`** —
> the CAV2 authority spine uses its own `Status:`/`Owner:` scheme, not the vault's. Appendix C's
> target classes are defined over vault node types, and `ontology-conventions.md` explicitly
> defers non-vault paths (its own OQ-C). These verbs are therefore used **descriptively**, pending
> that resolution; they are not claims of catalog conformance. This gap predates the session.

- surfaces-conflict `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md` —
  `CAV2-C18` requires a canonical artifact to declare its `canonical_kind`, `authority_kind`,
  `process_origin`, `durability`, and `authority_state`. The new Instance Contract forbids exactly
  that: type-level facts are looked up from the kind, the kind is read off the filename, and
  `authority_state` is struck from Evidence entirely. `C18` guards the same forgery risk with
  prose; the contract guards it by making the forgery inexpressible. Carried as debt by owner
  direction, not resolved.
- surfaces-conflict `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` — `CAV2-D3` enumerates
  five authority layers; `CAV2-C2` enumerates ten, and is self-inconsistent, listing
  `observability` as an authority layer while its own non-example forbids observability from
  becoming design authority. The `authority_layer` enum follows `D3`. Unresolved.
- surfaces-conflict `implementation/domainspec/vault/ontology-conventions.md` — the new
  `authority_layer` field and the existing `layer:` field (owned by this catalog; valued
  `ontology`, `architecture`, `domain`, `market`, `governance`, `authority`) share the word
  *layer*, and `ontology` is an admissible value of both. Whether the subject-axis `layer`
  survives alongside the authority-surface `authority_layer`, is renamed, or is retired, is
  undecided.
- cites `cyberAlchemy-v2/authority/decisions/2026-07-13-canonical-kind-one-label.md` — the
  one-label ruling (what an artifact *did* is expressed as edges leaving it, never as a second
  type label) is the precedent that forced "what is this evidence for" to be reframed as a
  forward declaration typed on authority layers, rather than as a second type label on the
  artifact.

## Open questions

- **Is a kind identified by its filename, by its path, or by declaration?** Rule 2 makes it the
  filename, and concedes in its own text that this already fails for `sessions/`,
  `authority/decisions/`, and `DEFINITIONS.md` — which carry the kind in the path, in a slug, or
  nowhere. (OQ-12.)
- **Are `review` and `audit` file kinds at all?** A review dispatch emits no `review.md` — only
  `findings.md`, sometimes with an unenumerated `attacks.md`. And `audit`, which has no producing
  process, drafted identically to `review`. (OQ-9.)
- **Is a set-valued `process` admissible, or does a kind with two producers mean the kind is
  under-specified?** `findings` is the first row naming more than one. (OQ-10.)
- **Does `perennial` need a finer axis?** It covers three incompatible mutation regimes:
  `definition` is revised in place, `ledger` is appended to, `decision` is never touched and is
  only superseded. (OQ-11.)
- **Should a single entry point author every canonical artifact** — and if so, is it subordinate
  to the owner routes that already produce `definition`, `constitution`, `decision`, and `spec`,
  or does it supersede them? A single actor holding every pen collapses the authority-layer
  separation; a subordinate one owning only *form* does not. Deferred by the owner.

## Next steps

- Close the cross-system edge gap in `implementation/domainspec/vault/ontology-conventions.md`
  (its OQ-C): either extend Appendix C's target classes to `cyberAlchemy-v2/**`, or rule that
  vault sessions may not carry typed edges into the CAV2 spine at all. Every edge in this node
  but one sits in that gap.
- Extend the instance contract to the deferred kinds, beginning with `session` — 40 live records
  already carry a de-facto contract that was left untouched.

## Recommendation

Attack OQ-12 first; it is the keystone, and OQ-9 is the same doubt wearing a different hat. Rule 2
makes the kind the filename, and the rule's own text concedes that this already fails for three
live surfaces — `sessions/`, `authority/decisions/`, and `DEFINITIONS.md` (many definitions, one
file) — which carry their kind in the path, in a slug, or nowhere. That concession is written into
the file, not conjectured. OQ-9 then reduces to the same question: a review dispatch emits no
`review.md`, only `findings.md` and sometimes an unenumerated `attacks.md`, which is exactly what
filename-as-kind cannot account for. Settle how a kind is identified — filename, path, or declared
— and both close together. Everything else written this session rests on that rule, so it should
not be extended to a fourth kind until it holds for the three.

## Files touched

- `cyberAlchemy-v2/ontology/CANONICAL-KINDS.md`
