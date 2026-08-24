## Definitional reviewer verdict

**REVISION REQUIRED — not PASS.**

The synthesis preserves most named distinctions, but two gates fail:

1. No persistent, explicit legend is included in the wireframe or MVP.
2. The “one semantic source” contract collapses the frozen proposal design and its candidate ontology into an undifferentiated source. `DESIGN.md` is the primary proposal source; `ONTOLOGY.md` is a non-promoting structured mapping derived from it. Conflicts must remain visible residue.

### Non-collapse tests

| Pair | Verdict | Required repair |
|---|---|---|
| `WorkDefinition` / `WorkRun` | PASS | Keep solid definition frame, outlined run card, and attempt rows. Never use generic `Work` as a semantic node label. |
| Leaf / composite substitutability | PASS | Same outer definition geometry is valid only with explicit `leaf`/`composite` body labels and the warning “same contract, different body.” |
| Recursive composition / orchestration authority | PASS | Keep drill-in definition nesting separate from the flattened one-root run plan. |
| Command / event | CONDITIONAL | Each occurrence needs textual `COMMAND` or `EVENT`; lane, fill, or arrow style cannot carry meaning alone. |
| Transport / persistence / decision / execution | CONDITIONAL | Label protocol, journal, gate/work, and executor adapter with distinct responsibilities and owners. |
| Routing cursor / domain status | PASS | Keep separate owner-tagged cards; cursor must show reducer and lineage. |
| Journal acceptance / confirmation | FAIL | Add an explicit “journal acceptance disposition” state. Rename “accepted fact/decision” to “journal-accepted event record”; it must never resemble work-owned confirmation. |
| Gate decision / external-effect permission | CONDITIONAL | Split route decision, authority-reference presence, adapter admission outcome, and external-effect occurrence. A checkpoint glyph alone is insufficient. |
| Primary / sidecar | PASS | Keep a detached, labelled sidecar lane and explicit lifecycle policy; no implicit control edge. |
| Structural edge / temporal occurrence | CONDITIONAL | The legend must distinguish definition-time trigger edges from occurrence-time causation, delivery, persistence, and cursor-fold relations. |
| Source semantics / learner projection | FAIL | Declare source precedence: proposal `DESIGN.md` → candidate ontology mapping → removable learner projection. No projection writeback or semantic invention. |

### Vocabulary decisions

**KEEP**

- Structure, Flow, Ownership/Proof, and shared Inspector.
- `WorkDefinition`, `WorkRun`, `Attempt`, root kernel, protocol, journal, adapter, cursor, domain state, confirmation, projection, invariant, and residue entities.
- Owner-tagged lanes and states.
- Stable-ID selection, drill-in, source jumps, static transcript, keyboard path, and reduced-motion stepping.
- Persistent proposal-only claim ceiling and contextual misuse warnings.

**MERGE**

- Merge `Source/Text` into the shared Inspector plus co-primary outline/relation-table equivalent; it is not a fourth semantic truth.
- Merge generic status coloring into labelled owner/state cards.
- Keep the routing diamond attached to an ordinary gate work entity; it represents label matching only.

**RENAME**

- Generic semantic node `Work` → exact `WorkDefinition` or `WorkRun`; “Work Atlas” may remain only as the interface title.
- “Playback/replay” → “illustrative paper-trace stepper” until runtime evidence exists.
- “Accepted fact/decision” → “journal-accepted event record.”
- “Authority checkpoint” → separate “authority reference present” and “adapter admission outcome.”

**DEFER**

- Semantic color palette; color may initially provide redundant focus/highlight only.
- Nonessential animation, live replay, telemetry overlays, formal UML/ArchiMate export, and runtime-derived status.
- Rare ontology relations to the relation table/Inspector rather than expanding the primary visual grammar.

**KILL**

- Color-only, fill-only, shape-only, or motion-only semantics.
- Universal green terminal/success and red-only quarantine.
- Autoplay causality, moving structural nodes, command-to-state animation, nested orchestrator glyphs, ownerless status, unbounded loops, and projection writeback.
- Any visual implication that the bus decides, the journal executes, an authority reference authorizes, confirmation receipt equals confirmation, or a learner projection is source truth.

### Smallest acceptable repaired legend

The persistent legend must define:

- entities: definition, run/attempt, owner/boundary, derived projection, evidence/residue;
- relations: structural definition edge, temporal causation, transport/delivery, journal acceptance, projection derivation, ownership, and authority requirement;
- lanes: root/cursor, command protocol, work/adapter, event protocol, journal, and scenario-specific gate/effect/sidecar lanes;
- states: journal acceptance, domain status, confirmation, cursor state, adapter admission, attempt freshness, and finding status;
- claim ceiling and the principal forbidden inference for every visually similar pair.

With those bounded repairs, the three-lens atlas remains understandable without adding new semantic primitives.

```json
{
  "action_id": "spawn-0007",
  "role": "definitional-reviewer",
  "status": "revision_required",
  "validation": "fail: persistent legend absent; journal acceptance versus confirmation lacks an explicit state vocabulary; source-design, candidate-ontology, and learner-projection precedence is collapsed; several visual distinctions still depend too heavily on shape, lane, or implied context",
  "blockers": [
    "Add the persistent minimal legend to the wireframe and MVP contract.",
    "Add an explicit journal-acceptance disposition distinct from work-owned confirmation.",
    "Declare DESIGN.md as primary proposal source, ONTOLOGY.md as its candidate non-promoting mapping, and learner records as removable projections.",
    "Require text labels and owner labels in addition to shape, lane, color, and motion."
  ],
  "artifacts": [],
  "started_at": "2026-08-04T17:38:30-03:00",
  "finished_at": "2026-08-04T17:48:30-03:00"
}
```
