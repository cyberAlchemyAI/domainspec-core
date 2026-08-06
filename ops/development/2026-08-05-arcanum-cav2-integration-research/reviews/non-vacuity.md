REVISION_REQUIRED

The synthesis preserves proof ceilings, but fails the non-vacuity gate. Mandatory cases are mostly distributed invariants or future routes rather than finite, discriminating witnesses.

| ID | Gate result | Attack and required repair |
|---|---|---|
| `NV-01` | **FAIL** | No public Arcanum structural pattern is shown both imported **and locally admitted** by CAV2. The artifact trace stops before local constitution promotion, validator implementation, and hooks ([synthesis.md:168](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:168)). Either supply an exact upstream pattern, manifest entry, promoted CAV2 artifact, owner decision/receipt, and subsequent stop—or record `NO_LOCALLY_ADMITTED_IMPORT_WITNESS`. Until then, narrow “adapter verified” ([synthesis.md:213](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:213)) to planned/candidate adaptation. |
| `NV-02` | **PARTIAL** | The authority-object proposal correctly stops before implementation, but is only a crosswalk row ([synthesis.md:66](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:66)). Convert `AUTH-009` into a finite trace: exact proposal input → ontology owner → decision gate → Task Session; artifacts; first stop before `NODE-MODEL` amendment; forbidden amendment/stabilization/validator effects; `direct-current + candidate + non-executed`. |
| `NV-03` | **PARTIAL** | The recovery trace demonstrates Invoke/validation evidence without promotion, but omits explicit ordered owners/gates and exact artifact identities ([synthesis.md:135](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:135)). Port the complete `TRACE-OP-POS-001` field block from [research.md:553](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/research.md:553). Preserve its status as untracked, dirty-worktree-only candidate evidence whose stored postimages are not current proof. |
| `NV-04` | **FAIL** | Ontology self-promotion is prohibited normatively ([synthesis.md:110](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:110)), but no finite negative case binds a specific candidate/projection to an owner refusal or absent mutation. Reuse the authority-object proposal as input and show the exact stop before canonical mutation. |
| `NV-05` | **FAIL** | Inventory promotion is described as impossible, but lacks a finite trace. Use `OP-017`: Inventory result → direct-source rebind → missing canonical Arcanum owner → Bootstrap selection killed → no generated package/install/deployment. Bind its dirty, untracked, non-authority proof status from [research.md:699](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/research.md:699). |
| `NV-06` | **FAIL** | Generated-projection authority is denied, while only drift is reported ([synthesis.md:58](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:58)). Add an exact canonical input → generator → named divergent projection → parity gate stop trace. Forbid canonical authority, installation, runtime parity, and promotion. If no exact artifact/result exists, record the witness as absent. |
| `NV-07` | **FAIL** | Private-to-public leakage has a policy route but no discriminating case ([synthesis.md:221](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:221)). Name a representative private input, scrub/review gates, first missing approval, and prove no public mutation. Otherwise classify this as a normative prohibition, not an executed negative witness. |
| `NV-08` | **PARTIAL** | Stale imports are identified ([synthesis.md:187](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:187)), but not traced. Add old manifest snapshot → freshness/rescan gate → absent current rescan → stop; forbid current-coverage, admission, implementation, and enforcement claims. |
| `NV-09` | **PARTIAL** | Missing-owner evidence exists for intent-router ([synthesis.md:203](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:203)), but is not presented as a complete trace. Expand `OP-017` with exact input/artifact, ordered owner gates, killed Bootstrap selection, forbidden downstream effects, and historical/dirty proof class. |
| `NV-10` | **FAIL** | “Full validation is red” ([synthesis.md:195](/home/vrondelli/projects/domainspec-core/ops/development/2026-08-05-arcanum-cav2-integration-research/synthesis.md:195)) lacks the exact frozen inputs, command/result or receipt, criticality owner, and downstream stop. The IOLM regression passed while confirming a blocker; it is not a failed-critical-validation witness. Bind the precise failed Artifact Constitution validation or explicitly record this witness as absent. |

The two existing operational traces remain valid but bounded:

- Recovery: candidate-local, untracked, dirty-worktree-only; evidence without promotion.
- External support stop: committed historical fail-closed behavior; not proof of current upstream behavior.

Research absences are revision residue, not execution blockers.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0006",
    "assigned_identity": "Popper, Karl",
    "role": "skeptic-non-vacuity",
    "dispatch_id": "2026-08-05-arcanum-cav2-integration-research",
    "run_id": "cav2-integration-run-01",
    "status": "complete",
    "scalar_validation": "fail",
    "verdict": "REVISION_REQUIRED",
    "blockers": [],
    "native_return_handle": "agent-return://2026-08-05-arcanum-cav2-integration-research/cav2-integration-run-01/spawn-0006/skeptic-non-vacuity",
    "residue": [
      "no verified public-Arcanum-pattern to locally-admitted-CAV2-rule witness",
      "authority proposal and operational evidence traces need complete field blocks",
      "ontology self-promotion negative witness is absent",
      "Inventory promotion negative witness is not assembled",
      "generated-projection authority negative witness is absent",
      "private-to-public leakage negative witness is absent",
      "stale-import and missing-owner evidence are not assembled as finite traces",
      "failed-critical-validation lacks exact input command result receipt and downstream stop"
    ],
    "reroute": [
      {
        "target": "synthesizer",
        "reason": "Add the required finite witness matrix and narrow adapter or integration claims that lack local admission evidence."
      },
      {
        "target": "operational-explorer",
        "reason": "Supply exact generated-projection and failed-critical-validation artifacts if they exist; otherwise return explicit absence classifications."
      },
      {
        "target": "writer",
        "reason": "Publish only after every retained trace contains inputs, ordered owners and gates, artifacts, first stop, forbidden effects, and proof status."
      }
    ]
  }
}
```
