---
tags: [authority, definitions-governance, cav2-spine, ontology, anti-bias, check-tension]
node_type: audit
is_session: true
layer: ontology
nature: explanatory, technical
status: active
created: 2026-07-13
timestamp: 2026-07-13T11:42:16-03:00
expires: 2026-09-11
conversation_id: 2026-07-13-authority-definition-critical-assessment
decisions_made: true
contradictions_found: true
specs_updated: [.claude/skills/check-tension/SKILL.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Applied literally, CAV2-D34's own admissibility rule demotes every artifact in the spine — including itself — to residue, and the session further found two active authority files asserting incompatible ID→term maps; but the arc resolved nothing, since the review dispatch was voided and the Arcanum collision parked."
---

# Is `CAV2-D34` (authority) a good enough definition to keep?

## Summary

The owner argued that a definition whose own terms are undefined is not a good definition, and asked for a critical assessment of `CAV2-D34` (authority) — delete it, demote it, or repair it. The charge proved largely true and the diagnosis wrong. D34's admissibility rule requires five fields be explicit (`scope`, `owner`, `surface`, `operation`, `effect`); four are defined in **none** of the repository's 24 definition stores — including Arcanum, which the ownership rule says v2 must defer to — while `surface` is defined three incompatible ways (`CAV2-D3` authority layer, `CAV2-D12` Craft execution surface, and D12's ledger-surface alias). The 8-field record is instantiated **zero times** across 617 `authority/` and `ontology/` files (`Owner:` appears in 48, `Scope:` in 1, the remaining six in none), so applied literally the rule demotes every artifact in the spine — including D34 itself — to residue. The agent pushed back on the owner's principle: definitional closure is impossible (every formal system bottoms out in primitives, and `CAV2-D31 primitive type` exists for exactly that), so the real test is *declared-primitive* versus *accidental-gap*, and D34's coordinates are the second. Against deletion stands the fact that the word is load-bearing — 1,411 bare uses, seven `authority X` compound terms — and the fate of `constitution`, a needed term with no card whose citations scattered, is what deletion produces. A claimed smoking gun (that five of seven in-body citers "mis-read" D34 as `constitution`) was **falsified mid-session**: a rival ID→term map (`D34`=constitution, `D35`=discipline, `D36`=decision, `D37`=spec) is used by `DEFINITION-SCHEMAS.md`'s backlog table — which asserts full record shapes for those terms — by the 2026-07-01 mint inheritance audit, and by `CAV2-D53`/`D54`, while `DEFINITIONS.md` assigns those same IDs to authority/provenance/traceability/gate; the citers were not careless, they were following a different map. Separately, Arcanum already defines `canonical artifact` (`DEF-ARC-CANONICAL-ARTIFACT`) with `authoritative artifact` and `canonical source` as aliases — the precise reading `CAV2-D51` exists to forbid — and D51 carries no provenance to it; the cause is a stale one-shot sync, since `source-clusters/arcanum.md` holds exactly the five IDs the localization route named in its first slice while Arcanum has since grown three more. A seven-agent review dispatch on D34 was shaped and cleared the `check-tension` gate on round 4 after three reproofs, the gate catching that two of three attackers were secretly running the same vacuity attack, that the predicted-disagreement sentences were questions rather than derivations, and that the verifier pair was untensioned. Both round-2 gate agents independently surfaced a contradiction between two skills — `review` assigns attackers `role: explorer` while `check-tension` reserved the `attack-vector` axis for skeptics — which the owner resolved by ruling the axis open to a review dispatch's explorer attackers; the rubric was patched in the vocabulary line and in Test 3. The dispatch was confirmed, then **voided** when a corpus re-check falsified an attacker's premise and forced a sheet revision; it re-cleared the gate and awaits a fresh confirm.

## Contradictions

- questions `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` — `CAV2-D34`'s admissibility rule demands five explicit fields, four of which (`scope`, `owner`, `operation`, `effect`) are undefined across all 24 definition stores, and its record is instantiated 0/617 times; applied literally the rule demotes every artifact in the spine, including itself, to residue.
- contradicts `cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md` — its backlog table asserts a rival ID→term map (`CAV2-D34`=constitution, `D35`=discipline, `D36`=decision, `D37`=spec) with full record shapes, incompatible with `DEFINITIONS.md`'s assignment of those IDs to authority/provenance/traceability/gate; the backlog claims `D35` asserts `Discipline = (id, name, trigger, …)` while the real `D35` card's formal voice is `Prov(x) = [(source_i, relation_i, operation_i, owner_i, posture_i)]*`.
- contradicts `arcanum/definitions/DEFINITIONS.md` — `DEF-ARC-CANONICAL-ARTIFACT` defines `canonical artifact` with `authoritative artifact` and `canonical source` as aliases, the exact sense `CAV2-D51` is built to reject, and D51 cites no provenance to it; the two are a name collision across the public/private boundary, not a supersession. Owner-parked.
- questions `cyberAlchemy-v2/authority/definitions/source-clusters/arcanum.md` — it carries representation rows for exactly the five Arcanum IDs named in the localization route's first slice while Arcanum has since grown three more (`DEVELOPMENT-ARTIFACT`, `CANONICAL-ARTIFACT`, `PROMOTION-PATCH`); the sync is a one-shot against a hardcoded list, not a live check.
- questions `cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md` — its section headings date this work `2026-07-09` while the commits landed `2026-07-12`; the file whose purpose is recording drift carries drifted dates.
- validates `.claude/skills/check-tension/SKILL.md` — the gate reproved three successive sheets and caught a genuine collapse (two attackers running one vacuity attack under different names), an untensioned verifier pair, and a cross-skill contradiction with `review`; it earned its cost rather than rubber-stamping.

## Open questions

- Is "authority" one concept or several homonyms? A document that *constitutes* meaning (a definition) and a document that *reports* an observation (a discovery) differ in whether they can be **false** — the first cannot, the second can — yet the model calls both authority, which is why an evidence artifact carries an `authority_kind` whose content reads "not an authority."
- Does a rule that nothing enforces do any work? D34 is cited seven times and violated 617/617 with no consequence, yet the word shapes the spine's vocabulary — usage and function may come apart, and which one licenses keeping a definition is undecided.

## Next steps

- Settle the rival ID→term map at `decision-gate`: either `DEFINITION-SCHEMAS.md`'s backlog is stale and must be rewritten, or `constitution`, `decision`, `spec`, and `discipline` need cards and non-colliding IDs.
- Run or abandon the gated seven-agent D34 review; the sheet cleared `check-tension` round 4 and awaits a fresh human confirm, the prior confirm having been voided by a post-confirm sheet edit.
- Correct the `2026-07-09` date stamps in `DEFINITION-DRIFT-AUDIT.md` to the actual commit date (`2026-07-12`).
- Loosen the `subagents-dispatch.yaml` append-only hook, which currently blocks read-only Bash commands naming the path, not just writes.

## Recommendation

The keystone is the **rival ID→term map**, because it is the only finding where two active authority files assert incompatible facts about the same identifiers, and every further definitions edit inherits the ambiguity. Licensing fact: verified directly on disk — `DEFINITION-SCHEMAS.md`'s backlog assigns `CAV2-D34` → constitution with a full record shape, while `DEFINITIONS.md:2171` assigns `CAV2-D34` → authority, and a third artifact (the 2026-07-01 mint inheritance audit) uses the rival map. Recommend the next session settle that at `decision-gate` **before** running the D34 review, since the review would otherwise adjudicate a card whose identifier is contested — and one of its three attack angles is premised on which map is authoritative. That the maps conflict is verified; that settling them dissolves part of the case against D34 is a hunch.

## Files touched

- .claude/skills/check-tension/SKILL.md
