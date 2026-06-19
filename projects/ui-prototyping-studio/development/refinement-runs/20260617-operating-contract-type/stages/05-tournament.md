---
id: tournament-operating-contract-type
run_id: 20260617-operating-contract-type
step_id: s5-distill-tournament
capability_ref: distill
updatedAt: 2026-06-17
---

# s5 — Tournament of candidate homes (+ x-ray placement)

## X-ray: the three type registries (which one even owns "artifact kind"?)

| Registry | Types *what* | Does it own "artifact kind"? | Placement of the operating-contract |
|---|---|---|---|
| Capability taxonomy (formulae/transmutation/arcana; sigil/spell) | capabilities | no | **fails** — not a sigil, not a spell (composes app verbs, not sigils) |
| `artifact_type` enum (ARTIFACT-METADATA-CONSTITUTION, `candidate`, no validator) | **artifact kinds** | **yes** — "validation selected from declared intent + type, not path" | near-neighbor `skill-contract`; distinct on 3 axes (project-local / named-engine-binding / CLI-seam+gates) |
| Craft ledger type system (`arcana/craft/`) | **ledger conditions** (blocker/gate/enabler + lane) + `typed_items` | no (types entries, not artifact kinds) | **wrong registry for kind**; right place to *track governance* as a context-specific typed_item |

**Structural finding:** only the `artifact_type` enum is the registry whose job is "what kind of file is this." Craft is categorically not about artifact kind (it types conditions); it can *track* the artifact, not *classify its kind*.

## Advocate returns (condensed; full reasoning in agent receipts)

- **A — define new `operating-contract` artifact_type.** By elimination it's the only registry for "kind"; genuinely doesn't fit `skill-contract` (which is product-neutral + tier-classified; this is product-bound + binds a runtime agent); cost is one enum row + a sentence in an already-`candidate` constitution; gives a future `validation_profile` hook (e.g. check the honesty clause — F-CRIT-1). **Confidence A-should-win-NOW: LOW** — "right home, wrong time": prior bar (≥2 instances) not met, single *unreviewed* instance, no validator → buys no enforcement now.
- **B — reuse an existing slot.** b1: classify as `skill-contract` + carry project-local-ness as a `scope`/`owner` field (the constitution already rides cross-cutting attributes as fields, not new types); b2: track governance as a Craft context-specific typed_item (no enum amendment). Cheapest; advances the registry instead of forking it; honors the prior. **Confidence: MEDIUM.** Counter: collapses a distinction the `validation_profile` selector must eventually tell apart (portable capability vs product-bound runtime-binding) — a field that *changes which validator runs* is functionally a type. Offered trip-wire.
- **D — defer; define no new type now.** n=1 is premature generalization (the session's recurring anti-pattern); a type with no validator is "classification theater, not enforcement"; the artifact is already handled as `node_type: skill-draft`; Craft's own philosophy is condition-typing + "prune verbosity, wait for examples." **Confidence: MEDIUM, leaning hold.** Counter (the pivotal one): deferral leaves it **unclassified**, so every future reader re-runs the "sigil? spell?" confusion — and that cost is **per-reader, not per-instance**, so the ≥2-instance trigger never fires for it. **D's own admission:** the confusion is a *naming/denotation* need, not a *typing/enforcement* need — best fixed by a one-line note, not a framework type.

## Pareto judgment (parent)

The advocates **converge**, not split. A: right home, wrong time. B: cheapest interim, but a field that flips the validator is a latent type. D: defer the type, but the real pain is naming, not typing.

The dominating move separates **two axes the binary conflated**:
- **Typing (enforcement):** does the framework need a new `artifact_type`? → **No, not now.** No validator exists (constitution is `candidate`, every rule `future`); n=1 and unreviewed; minting now is theater (A-LOW, D, and B all agree the enforcement payoff is ~0 today).
- **Naming (denotation):** does the recurring "is it a sigil/spell?" confusion need ending? → **Yes, cheaply, now** — a one-line disambiguation co-located with the artifact, costing nothing and firing per-reader.

**Selected: a third option neither single home owned** — *defer the framework type (A's home, behind the prior's trip-wire) + solve the naming need now with a denotational note (D's own escape hatch) + use B's reuse as the interim classification.* Rejected alternatives recorded: A-now (premature, no enforcement), pure-D (leaves naming cost unpaid), B-as-permanent-home (latent validator-selection collapse).
