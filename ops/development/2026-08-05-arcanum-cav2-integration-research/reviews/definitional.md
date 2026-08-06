REVISION_REQUIRED

The synthesis preserves the four-pillar and public/private boundaries, but it fails the stricter definitional-soundness gate. The principal defect is not its overall conclusion; it is that several retained edges lack complete typed contracts, and some procedural routes are allowed to masquerade as semantic owners.

### Claim verdicts and repairs

| Claim ID | Verdict | Attack and exact repair |
|---|---|---|
| `SYS-002`, `FB-003` | PASS | The separation of DomainSpec structured intent, Arcanum bounded execution, Saturn’s intended convergence loop, and CAV2 local promotion is sound. Retain the explicit statement that neither loop subsumes the other. |
| `EDGE-001`–`EDGE-006` | CONTENT_PASS / FORM_REVISION | Direction and ceilings are generally sound, but the synthesis’s diagrams and role map omit one or more required fields per edge. Recast each retained edge with `source`, `target`, `relation`, `source_owner`, `destination_owner`, `current_state`, `legal_transition`, `evidence_ceiling`, `privacy_class`, and `non_effects`. Architectural arrows alone are insufficient. |
| `EDGE-007` | REVISION_REQUIRED | “CAV2 → its local definitions/constitutions/decisions/specs” makes CAV2 an undifferentiated actor and collapses authority kinds. Split it into candidate/evidence → named definitions owner, constitution owner, discipline owner, decision owner, spec owner, or runtime-contract owner → canonical owner artifact. A repository is the scope, not the deciding agent. |
| `AUTH-002`, `FB-002` | REVISION_REQUIRED | The authority-kind table assigns “task-session after owner gates” to runtime contracts. Task Session is an implementation admission/execution route, not the semantic owner of a runtime contract and not a promotion route. Name the canonical contract/spec/capability owner; let that owner and any required Decision Gate approve the contract; Task Session may only implement admitted work afterward. |
| `AUTH-002`, synthesis opening flow, `FB-002` | REVISION_REQUIRED | The generic chain `narrow-owner decision → implementation → validation → possible promotion` conflates distinct legal orders. For definitions, constitutions, specs, and runtime contracts, promotion normally precedes governing implementation. Pre-promotion prototypes or validation may exist only as non-governing candidate evidence. Replace the single chain with typed branches for authority promotion, implementation admission, validation, and release/deployment. |
| `AUTH-006`, `AUTH-011` adapter subclaim | REVISION_REQUIRED | “CAV2 is an adapter” is overstated as a present fact. The verified evidence establishes a need and plan for re-rooted adaptation; the concrete validator port remains unexecuted. Repair to: “CAV2 has verified adaptation seams and planned adapter work; no implemented/runtime adapter is proved.” |
| `H-CONSUMER-001` | QUALIFIED_PASS | Retain only as “documentary/import consumer of public Arcanum sources, methods, and candidates.” State explicitly that this does not prove generated-package installation, callable runtime consumption, release, or deployment. |
| `H-CONSOLIDATION-001` | PASS | Directly supported by `cyberAlchemy-v2/README.md:8-16`; preserve source ownership and no automatic authority transfer. |
| `H-SPINE-001` | QUALIFIED_REVISION | “Authority spine” is a private architectural descriptor in `SATURN-LAYER-MAP.md:139`, while CAV2’s README says “stable spine.” It is not shown as a promoted CAV2 definition or authority kind. Label it `private architectural synthesis/descriptor`, not a formally verified repository type. Its non-effects must exclude meta-authority, workspace apex authority, standalone status, and public framework status. |
| `AUTH-010` | REVISION_REQUIRED | “Authority owns state” personifies a category and risks circular authority. Repair to: “the named narrow owner decides; the canonical owner artifact records the accepted normative state; the ledger records evidence/events; ontology projects relationships.” |
| `C-01`, `CEIL-001` | REVISION_REQUIRED | The synthesis acknowledges the candidate/project-local constitution contradiction but still treats the local authority spine as simply verified. Until constitution governance reconciles status, say “repository-declared active local authority model” rather than independently proved promoted canon. The model’s own `Status: active` declaration cannot alone prove the validity of its bootstrap authority. |
| `AUTH-012`, `EDGE-008` | PASS | Public Arcanum → private CAV2 reference/adaptation is permitted with local gates; private CAV2/DomainSpec → public Arcanum remains forbidden absent scrub, source-owner review, and explicit public-owner action. |
| `H-META-001`, `H-S5-001`, `H-MOLD-001`, `H-BASE-001` | PASS | The synthesis correctly rejects meta-authority as current fact, keeps System-5 and mold as analogies/metaphors, and keeps the downloadable base as intended-only. |
| `C-14`, `CON-002` | PASS_WITH_CEILING | Correctly distinguishes current documentation bytes from proof of a live published deployment or a shipped Saturn loop. Preserve that ceiling. |

### Required structural repair

Add a stable claim/edge registry. The synthesis currently relies on imported explorer IDs, conflict IDs, headings, and unnumbered diagrams; therefore not every retained synthesis claim has an exact ID.

At minimum, split the opening relationship into these distinct edges:

1. Public Arcanum canonical source → CAV2 import candidate: reference/staging only; public → private; no authority transfer.
2. Import candidate → local definition/constitution/spec candidate: classification or adaptation by the appropriate local owner; still candidate.
3. Local candidate → local canonical authority: explicit owner decision plus canonical owner mutation.
4. Promoted rule/spec/runtime contract → implementation admission: Task Session may execute but cannot promote.
5. Execution result → validation evidence: validation owner reports bounded conformance; no semantic promotion.
6. Canonical capability → generation → synchronization → installation → behavioral acceptance: separate witnessed runtime transitions.
7. Accepted artifact → release → deployment → publication: three separate transitions with separate owners, privacy review, and proof ceilings.

The registry must also give dedicated rows to source, import candidate, Inventory, ontology, definition, constitution, discipline, decision, spec, runtime contract, projection, evidence, residue, implementation, validation, deployment, and publication. Their appearance in prose or a folder/status table is not enough to prove non-collapse.

Research negatives—no System-5 edge, no standalone extraction, absent runtime adapter, missing end-to-end witness—remain residue/evidence ceilings. They are not execution blockers. The blockers below concern only passing this synthesis through the definitional review gate.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0007",
    "assigned_identity": "Quine, Willard Van Orman",
    "role": "skeptic-definitional",
    "dispatch_id": "2026-08-05-arcanum-cav2-integration-research",
    "run_id": "cav2-integration-run-01",
    "status": "complete",
    "scalar_validation": "revision_required",
    "validation_details": {
      "four_system_non_collapse": "pass",
      "public_private_non_collapse": "pass",
      "artifact_kind_non_collapse": "revision_required",
      "every_retained_edge_fully_typed": false,
      "circular_authority_excluded": false,
      "analogies_kept_out_of_repository_fact": "partial",
      "repository_writes": 0,
      "external_web_used": false,
      "memory_used": false
    },
    "blockers": [
      "runtime contract ownership is conflated with the Task Session execution route",
      "the generic promotion and implementation flow does not encode type-specific legal ordering",
      "retained edges lack complete owner, state, transition, ceiling, privacy, and non-effect fields",
      "adapter and authority-spine claims require corrected current-state and source-status labels",
      "the synthesis lacks stable IDs for all retained claims and edges"
    ],
    "native_return_handle": "agent-final://cav2_definitional_reviewer/spawn-0007",
    "residue": [
      "constitution candidate versus project-local status awaits constitution-governance adjudication",
      "implemented CAV2 adapter remains unproved",
      "standalone extraction, release, deployment, meta-authority, System-5 operation, and downstream mold remain unproved",
      "research negatives remain evidence ceilings rather than execution blockers"
    ],
    "reroute": [
      {
        "target": "synthesizer",
        "reason": "Normalize every retained claim and edge, split authority promotion from implementation and runtime transitions, and correct owner/category labels."
      },
      {
        "target": "constitution-governance reviewer",
        "reason": "Resolve candidate versus project-local constitution status before stronger canonical-authority wording."
      },
      {
        "target": "runtime-contract owner",
        "reason": "Name the semantic owner that precedes Task Session implementation admission."
      }
    ]
  }
}
```
