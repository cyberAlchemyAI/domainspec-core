---
tags: [framework-unification, system-recon, meta-layers, builder-vs-product, capability-inventory, subagents-dispatch, claim-le-proof]
node_type: conceptual
is_session: true
layer: architecture
nature: explanatory, reference
status: active
created: 2026-07-03
timestamp: 2026-07-03T20:14:41-03:00
expires: 2026-09-01
conversation_id: 2026-07-03-system-recon-builder-reframe
decisions_made: true
contradictions_found: false
specs_updated: [projects/framework-unification/components/recon/INDEX.md, projects/framework-unification/components/meta-layers-map/README.md]
promoted_candidates: []
expected_importance: 5
importance_rationale: "Durable cross-repo orientation (recon INDEX + meta-layers component map) plus a reframe that reorients the unification objective; but all synthesis/argument, no new canonical artifact or proof, so orientation-grade not foundational."
---

# System recon, meta-layers component map, and the builder-vs-product reframe

## Summary

The session began by reading `projects/framework-unification/` — whose objective is to unify the CyberAlchemy engine into one coherent view and assign a single owner to every duplicated concept — and established that its furthest-along artifact is the two-axis CONCEPT-MAP (one pipeline × three vertical mechanisms). The user then widened scope to inventory every capability across repos, and a 6-scout dispatch (`2026-07-03-system-recon-census`) mapped cyberAlchemy-v2, domainspec-v2, the built engine, Arcanum, the `../domainspec` sibling, and business-philosopher into six MAP files plus a tying INDEX. The recon resolved the "how many DomainSpecs" confusion: one built engine exists in three checkouts at three commits, plus one genuine rewrite (domainspec-v2 with its own local authority spine), and it surfaced six duplicate-owner targets and four public/private boundary flags. The user pinned the objective by explicit choice — **unify to one coherent engine** (one canonical source per capability, one authority spine, one pin) — and I named the honest caution that an inventory is a means, not the objective. Asked for the concepts of a system-that-builds-systems, I gave a grounded set (representation/pipeline/capabilities/orchestration/substrate are built and in use; provenance/epistemic-gate/authority are convention-not-mechanism; Saturn's loop and mint's reproduction are unbuilt). A second dispatch (`2026-07-03-meta-layers-component-map`, extract→map→verify) took business-philosopher's meta-representations material as true and connected our components to it: the extract rendered an L0–L7 construction stack (plus a Δ compiler, a signal protocol, and an open L1.7 telemetry idea), the map connected 10 of 14 parts to built/using components (L6 enforcement strongest), and the skeptic audit found 4 forced fits, 4 holes, four orphan classes, and one hard double-count overclaim. Two decisions fell out: the feedback half (an L2.5 operational-signal producer feeding the Saturn loop) is the concrete first build target, and the theory has no rung for "building the builder." I proposed calling that missing tier "L8," and the user corrected it decisively — it is **not a layer; it is what builds the layers.** The correct frame is that L0–L7 are the anatomy of the *product* (nouns/states), while the builder is the *factory* (the verbs/transitions, plus self-extension and reproduction) — realized today, unrecognized as a whole, by Arcanum + cav2 + the subagents-dispatch substrate + mint/arcanum-bootstrap. Net: the meta-layers theory theorizes the product richly and is blind to the builder, yet the builder is the actual objective, so the unification work is entirely builder-work — and the recon's duplications are all factory problems, which is why none appeared in the layer map.

## Next steps

- Draft the **anatomy of the builder** as the counterpart to `meta-layers-map/EXTRACT-META-LAYERS.md`: the verb-classes (capabilities · orchestration · self-extension · reproduction · machinery-governance · improvement-loop), each tagged built/designed and mapped to Arcanum/cav2/dispatch/mint/Saturn. Offered; pending the user's go.
- Scope the feedback-half build target from `meta-layers-map/MAP-RESIDUE.md` hole #1/#2: what an L2.5 operational-signal producer + the Saturn `L2.5⇢L0` closer concretely require.
- Reconcile the still-open close-session skill mismatch (repo-root `.claude/skills/close-session` targets a non-existent `docs/vault/`; the umbrella uses `sessions/`) — carried from session 2026-07-03-2010, still unfixed.

## Open questions

- Is the builder best modeled as its own L0–L7 stack applied to the domain "systems," or as a structurally different object (verb-classes, not layers)? The user settled that it is not a rung; whether it has its own internal layering is undecided.
- Should the business-philosopher meta-layers theory gain an explicit account of the builder, or does the builder live entirely outside that (product-only) frame?

## Recommendation

- The keystone is the **builder anatomy** — it is the under-theorized half where the stated objective ("a system that builds systems") actually lives, and it would give the six duplicate-owner rulings a spine to hang on. This is a hunch, licensed by the recon INDEX (the orphans cluster into one coherent tier) and the user's builder-is-not-a-layer correction — not by any new result this session proved.

## Files touched

- projects/framework-unification/components/recon/MAP-cyberalchemy-v2.md
- projects/framework-unification/components/recon/MAP-domainspec-v2.md
- projects/framework-unification/components/recon/MAP-domainspec-impl.md
- projects/framework-unification/components/recon/MAP-arcanum.md
- projects/framework-unification/components/recon/MAP-domainspec-sibling.md
- projects/framework-unification/components/recon/MAP-business-philosopher.md
- projects/framework-unification/components/recon/INDEX.md
- projects/framework-unification/components/meta-layers-map/EXTRACT-META-LAYERS.md
- projects/framework-unification/components/meta-layers-map/COMPONENT-LAYER-MAP.md
- projects/framework-unification/components/meta-layers-map/MAP-RESIDUE.md
- projects/framework-unification/components/meta-layers-map/README.md
- telemetry/agents/subagents-dispatch.yaml
