## Precedent / owner review

Overall verdict: **FLAG**. The structural layers and owner boundaries mostly match current sources, but several “missing capability” and repair claims need tighter classification to avoid duplicating already-deployed machinery.

### Claim dispositions

| Claims | Verdict | Precedent / actual owner | Disposition and bounded repair |
|---|---|---|---|
| `SG-STACK-01..10`, `SG-VOC-02..11`, `SG-OWN-01..09`, `SG-ENF-01..08` | PASS | Definitions Governance; Constitution Governance; Discipline Governance; Sigil Development; Spellcraft; artifact-specific owners. Exact anchors include `arcanum/arcana/constitution-governance/SKILL.md:15-29,68-113,117-148`, `arcanum/arcana/discipline-governance/SKILL.md:15-28,65-74,96-110,127-150`, and `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:19-84`. | Retain. These layers do not propose duplicate constitutions, catalogs, registries, validators, or promotion gates. Keep the evidence ceiling at observed process or bounded executable check. |
| `SG-VOC-01`, `SG-CON-10`, `SG-DRIFT-14`, `SG-REC-01` | PASS | `arcanum/arcana/definitions-governance/SKILL.md`; Constitution Governance for any axiom relationship. | **build-from-owned**. Define `constitution` through Definitions Governance. Add `axiom` only after an explicit public concept decision; do not import the private axiom hierarchy. |
| `SG-CON-01..12` | PASS with qualification | Existing constitutions plus Constitution Governance. | Retain six-public-constitution catalog as a filesystem observation, not a universal completeness claim. `SG-CON-05` must state that a metadata parser is already deployed, while end-to-end selector resolution remains missing. |
| `SG-DIS-01..08`, `SG-DRIFT-04`, `SG-DRIFT-05`, `SG-DRIFT-12`, `SG-DRIFT-13`, `SG-REC-03` | PASS | Discipline Governance owns card/catalog/status lifecycle at `arcanum/arcana/discipline-governance/SKILL.md:96-110,113-150`; the existing catalog validator is `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80`. | **build-from-owned**. Extend the existing validator or narrow claims. Do not create another discipline catalog, schema, lifecycle, or promotion process. The executable validator currently checks only table shape, status, IDs, and evidence links; the skill’s card-schema and cross-capability checks remain review obligations. |
| `SG-COMP-01..04`, `SG-COMP-07..09` | PASS | Constitution Governance’s `select`/`compose` modes and Decision Gate already own selection, precedence, conflict preservation, and blocker decisions: `arcanum/arcana/constitution-governance/SKILL.md:23-29,84-113,117-132`. | **already-deployed process**, mostly prose/review-bound. Do not introduce a second composition lifecycle or conflict gate. |
| `SG-COMP-05`, `SG-COMP-06`, `SG-DRIFT-09`, residue “no constitution schema/selector registry” | FLAG | `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:106-186`; deployed parser `arcanum/tools/validate-artifact-metadata.py:15-40,183-269,282-382`; integration at `arcanum/tools/validate-artifact-constitution.sh:351-352,391-405`. | The broad absence wording hides already-deployed metadata parsing and validation. Repair to: “No general constitution catalog, selector-to-owner mapping, composition/conflict solver, or version resolver was found; an existing parser validates required metadata fields and list shape but does not resolve selector/profile identities or conflicts.” Any improvement is **build-from-owned** under Constitution Governance and Artifact Metadata Constitution, not a new engine by default. |
| `SG-LIFE-01..05`, `SG-PLAY-01..06`, `SG-REC-06`, `SG-REC-07` | PASS | Existing artifact lifecycle owners plus `DEVELOPMENT-TO-CANONICAL-PROMOTION.md`; Decision Gate already handles blocker decisions. | Retain. Transition automation, if justified, must extend each current owner. Reject a universal promotion or retirement engine. |
| `SG-BUILD-01..04` | PASS | Invoke, Task Session, Craft boundary, Dispatch Spec, and Orchestrate. Orchestrate directly implements persisted-action admission, one native spawn, bounded join, deterministic reduction, and blocked dependent gates in `.agents/skills/orchestrate/SKILL.md:59-143`. | **already-deployed coordination**. Do not add another coordinator, receipt lifecycle, scheduler, or promotion gate. |
| `SG-BUILD-05` and the diagram’s `Experiment Harness → Signal Observer → Workflow Reflect` | FLAG | The reusable maintenance composition already exists as `arcanum/spells/sigil-maintenance-loop/README.md:1-15,21-39,43-101,103-147`; Spellcraft owns the composition and Sigil Development alone owns approved mutation. | Bind this integration to the existing spell. The diagram must not imply an ad hoc or universal observability loop, nor omit Inventory lookup and the human approval gate. Classify as **already-deployed**, not proposed infrastructure. |
| `SG-DRIFT-01`, `SG-REC-04` | PASS with repair | Canonical contract: `arcanum/arcana/discipline-governance/SKILL.md:1-10`; stale generated copy: `.agents/skills/discipline-governance/SKILL.md:1-18`; targeted generation owner: `arcanum/tools/sync-generated-skill-package.sh:106-229`. | Drift is reproducible (`0.2.2` versus `0.2.1`). Use the existing targeted staged-generation/sync route. Do not create a second registry or generator. Replace “produce transform-aware parity evidence” with the bounded existing witness: preview staged package diff, apply only when authorized, then verify expected generated metadata transforms plus canonical substantive content/version. A new general parity validator is justified only by repeated failures. |
| `SG-DRIFT-02`, `SG-DRIFT-03`, `SG-REC-05`, `SG-PROOF-03..04` | PASS | Existing combined validator `arcanum/tools/validate-artifact-constitution.sh`; it resolves `git rev-parse --show-toplevel` and uses repository-relative `framework/` and `tools/` paths at lines `1-11`. | **build-from-owned**. Frozen rerun from the Arcanum repository root is correct. Root sensitivity belongs in this existing tool; document or harden its root resolution rather than adding a wrapper validator. Preserve the count disagreement until one frozen rerun. |
| `SG-DRIFT-06`, `SG-DRIFT-08` | PASS, severity understated | Metadata Constitution still calls its deployed parser checks “future” at `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:108-114,159-176`; its Schema Constitution example at lines `118-122` does not match the live header. | This is an owner-document/implementation drift, not merely one bad example. Constitution Governance should reconcile the candidate constitution with the already-deployed parser, accurately mark which checks exist, and retain missing selector/profile mapping as future. No second metadata constitution or validator. |
| `SG-DRIFT-07`, `SG-REC-02` | PASS with scope repair | Constitution Governance already defines identity, owner, authority, selectors, validation, promotion, and retirement triggers at `arcanum/arcana/constitution-governance/SKILL.md:88-113`; Artifact Metadata Constitution already proposes lifecycle status and supersession at `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:30-60`. | **build-from-owned**. Normalize through these owners. Do not create a separate constitution catalog/schema before deciding whether existing metadata plus filesystem discovery is sufficient. Version semantics are the genuine uncovered part. |
| `SG-DRIFT-10` | PASS | Discipline deprecation is already deployed at `arcanum/arcana/discipline-governance/SKILL.md:107-110`; constitution retirement is only a declared trigger at `constitution-governance/SKILL.md:88-113`. | Narrow wording: discipline has an owner-routed manual deprecation process, not “no lifecycle”; what is missing is deterministic state-machine enforcement. Constitution retirement likewise remains review-bound. |
| `SG-DRIFT-11` | FLAG | Existing targeted generator stages canonical source and uses checksum-aware `rsync` preview/apply with rollback at `arcanum/tools/sync-generated-skill-package.sh:106-229`. | Do not imply parity infrastructure is wholly absent. Structural package parity is already supported by deterministic staging/diff; semantic equivalence of permitted host transforms is unproven. Route first to the generation owner and add only a bounded semantic check if current staging cannot distinguish a real defect. |
| `SG-VERDICT-01` | PASS | Supported by the owner and enforcement boundaries above. | Retain as a candidate explanatory model only. It is not a new structural constitution and must not become one by publication alone. |

### Required synthesis repairs before writer gate

1. Correct `SG-CON-05`, `SG-COMP-05`, `SG-DRIFT-09`, and residue to acknowledge the deployed artifact-metadata parser and its exact limited coverage.
2. Bind `SG-BUILD-05` to the already-deployed `sigil-maintenance-loop`, including Inventory lookup and approval before Sigil Development mutation.
3. Narrow `SG-DRIFT-10`: owner-routed discipline deprecation exists; deterministic transition enforcement does not.
4. Narrow `SG-DRIFT-11`/`SG-REC-04`: deterministic staged generation and checksum diff already exist; only transform-aware semantic equivalence remains unproven.
5. Treat `SG-DRIFT-06` as constitution-to-implementation drift: the candidate document says “future” although the parser and Artifact Constitution integration exist.
6. Preserve every recommendation as **build-from-owned** or **already-deployed**. No new universal catalog, lifecycle, registry, validator, promotion engine, coordinator, or observability loop is supported by current evidence.

Unresolved evidence: no frozen rerun resolves the Artifact Constitution failure-count discrepancy; no direct execution proves selector/profile resolution, constitution versioning, transform-aware semantic parity, discipline-card schema enforcement, or cross-capability Growth Rule enforcement.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0005",
    "assigned_identity": "Russell, Bertrand",
    "role_id": "skeptic-precedent",
    "status": "complete",
    "validation": {
      "result": "flag",
      "precedent_owner_gate": "flag",
      "direct_sources_checked": "pass",
      "coordinator_implementation_checked": "pass",
      "duplicate_structures_rejected": "pass",
      "mutation": "none",
      "authority_effect": "none",
      "proof_ceiling": "read-only adversarial review of current public sources and generated runtime; no implementation, promotion, publication, deployment, release, or production claim"
    },
    "blockers": [
      "synthesis requires bounded exact-binding repairs before writer evidence closure"
    ],
    "native_return_handle": "native-return:/root/structural_precedent_reviewer",
    "residue": [
      "artifact-metadata-document-versus-deployed-parser-drift",
      "selector-and-validation-profile-resolution-unproven",
      "constitution-version-resolution-unproven",
      "discipline-card-schema-and-growth-rule-enforcement-unproven",
      "artifact-validator-failure-count-unreconciled",
      "generated-transform-semantic-parity-unproven"
    ],
    "reroute": {
      "next": "parent synthesis exact-binding repair and reviewer join",
      "authority_effect": "none"
    }
  }
}
```
