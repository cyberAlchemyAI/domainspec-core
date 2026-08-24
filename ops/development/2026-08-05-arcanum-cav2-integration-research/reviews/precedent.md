VERDICT: `REVISION_REQUIRED`

The relationship model is directionally sound, but it fails the precedent gate where it collapses mixed authority states, overstates planned adaptation, and leaves several existing-owner claims without exact direct-source bindings.

### Required attacks and repairs

- `PRECEDENT-001 — CAV2 authority-state inflation`

  - Targets: Four-system role map; “CAV2 is a private authority spine”; Promotion operational row; `C-01`.
  - Evidence:
    - `authority/AUTHORITY-MODEL.md:3-4,48-69` — active local model, but deterministic enforcement remains pending.
    - `authority/definitions/DEFINITIONS.md:3-16` — active local definitions.
    - `authority/decisions/README.md:3-8` — active decision surface.
    - `disciplines/DISCIPLINES.md:3-24` — candidate disciplines.
    - `authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md:3-6` — simultaneously `candidate` and `project-local constitution`.
    - `authority/promotion-policy.md:3-6` — candidate local policy.
  - Verdict: `REVISE`. CAV2 has an active local authority model, definitions, and decisions; it does not have uniformly active constitutions, disciplines, or promotion machinery.
  - Repair: split status by authority kind. Replace “normative active promotion route” with “active owner-routing rule plus candidate promotion ladder.” Route the constitution status contradiction to constitution-governance/decision-gate; the synthesis may not settle `C-01` editorially.

- `PRECEDENT-002 — Stale definition-import coverage is not a current owner map`

  - Targets: Arcanum-definitions ownership row; structural definition crosswalk; `C-02`.
  - Evidence:
    - `authority/imports/definitions/MANIFEST.md:3-5,37-43` — scan dated 2026-06-19, 149 heterogeneous candidates, candidate-only.
    - `MANIFEST.md:237-251` — source-of-truth classification remains open.
    - `arcanum/definitions/DEFINITIONS.md:3-16` — current canonical Arcanum owner rule.
    - Current Arcanum definitions changed through commit `b280678e28baf1ae6abcc9ec2d7072388fa3bc85`, after the manifest scan.
  - Verdict: `QUALIFIED_RETAIN`. The cross-boundary reference rule is correct; the 149-row manifest is not current per-term coverage.
  - Repair: rescan against a pinned Arcanum commit and emit per-term records containing upstream ID/path, source status, exact owner, and `reference | local-adaptation | already-owned-skip`. Do not copy Arcanum semantics into CAV2 terms.

- `PRECEDENT-003 — Artifact adaptation is planned, not verified`

  - Targets: artifact-validator ownership row; artifact crosswalk; import trace; adapter hypothesis; `C-03`.
  - Evidence:
    - Constitution manifest `:159-166` explicitly says the prior scan is stale, validator tooling was unstaged, and zero candidates were extracted.
    - `development/artifact-governance-import/PLAN.md:1-12` declares candidate, intended-not-shipped, non-executed.
    - `PLAN.md:20-31` places local constitutions, validator port, and hook wiring in future layers.
  - Verdict: `REVISE`. Call this a “verified staged-import and planned-adaptation precedent,” not a verified adaptation.
  - Repair: retain the first stop before local constitution promotion. Constitution-governance owns L1; Task Session owns L2/L3 only afterward.

- `PRECEDENT-004 — Planned adversarial validator witness is underspecified`

  - Targets: artifact plan acceptance, `C-09`, import operator playbook.
  - Evidence:
    - `arcanum/framework/SCHEMA-CONSTITUTION.md:3-10` canonically requires YAML in `.schema.yml`.
    - `arcanum/tools/validate-artifact-constitution.sh:169-181` checks disallowed schema suffixes; it does not parse or validate `.schema.yml` content.
    - Its self-test at `:233-246,276-289` treats `.schema.json` as bad and `.schema.yml` as good.
    - CAV2 `PLAN.md:31` requires “author a bad `.schema.yml`; confirm block.”
  - Verdict: `REJECT_AS_WRITTEN`. The current upstream validator cannot discriminate a malformed `.schema.yml`; “bad” has no owned rule or fixture definition.
  - Repair: Constitution Governance must choose one:
    - change the witness to an actually owned form failure such as `.schema.json`; or
    - first promote a YAML-parse/content rule and implement failing fixtures.
    Then freeze the upstream commit before adapting it.

- `PRECEDENT-005 — Tier-1 port leaks Tier-2 metadata semantics`

  - Targets: artifact-validator row and `PLAN.md` L2.
  - Evidence:
    - CAV2 `PLAN.md:33` defers Artifact Metadata to Tier-2 and a frontmatter decision gate.
    - Upstream validator `:347-353` hard-requires the metadata constitution/parser and `:391-403` invokes the parser.
    - `framework/ARTIFACT-METADATA-CONSTITUTION.md:3-5,108-114,168-176` remains candidate and has unmet promotion requirements.
  - Verdict: `REVISION_REQUIRED`.
  - Repair: define a narrow CAV2 form adapter that excludes metadata dependencies, or explicitly admit metadata through its separate owner gate. Do not port all three tools and then describe the result as form-only enforcement.

- `PRECEDENT-006 — “Arcanum governance machinery” needs artifact-level status`

  - Targets: Arcanum role map; framework-constitution ownership row.
  - Evidence:
    - `SCHEMA-CONSTITUTION.md:3-5` is canonical.
    - `ARTIFACT-METADATA-CONSTITUTION.md:3-5` is candidate.
    - `GITIGNORE-CONSTITUTION.md:3-5` is candidate.
    - `MARKDOWN-LINKING-CONSTITUTION.md:1-7` is candidate.
  - Verdict: `REVISE`. Arcanum owns all these sources, but ownership does not make every source canonical or deployed.
  - Repair: bind each imported rule/tool to its individual upstream lifecycle status and owner. Build from the owner; do not inherit candidate status as local authority.

- `PRECEDENT-007 — Inventory ownership needs narrower wording`

  - Targets: Inventory matrix row; `C-12`; residue item 7.
  - Evidence: `cyberAlchemy-v2/inventory/README.md:3-11` already establishes a CAV2-owned exported read-model boundary, while only that README exists.
  - Verdict: `QUALIFIED_RETAIN`.
  - Repair: say “CAV2 owns the exported read-model boundary but has no machine index.” The decision is whether to add a local machine index or intentionally continue consuming the parent index—not whether a CAV2 Inventory route exists at all.

- `PRECEDENT-008 — Generated/runtime and lifecycle rows lack exact current owner bindings`

  - Targets: generated-host-skills row, runtime-integration row, Invoke/Task Session/Continuation tables.
  - Verdict: `EVIDENCE_BINDING_FAILURE`, not necessarily factual contradiction.
  - Repair: replace “current contracts” and “August 5 findings cited by explorer” with exact canonical skill/spec paths, generation script, generated consumer paths, frozen commits/hashes, installation owner, and behavioral receipt. Until then keep runtime integration `unverified`.

### Retained conclusions

The following survive the precedent gate:

- Arcanum retains authority over Arcanum-wide definitions.
- CAV2 definitions are active but project-local.
- Inventory and ontology cannot promote or decide authority.
- Private DomainSpec evidence cannot be manufactured by Craft, validation, or CAV2.
- No standalone, meta-authority, System-5, mold, deployment, or integrated-runtime claim is proved.
- A found owner routes work to build-from-owned; it does not kill the work.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0005",
    "assigned_identity": "Russell, Bertrand",
    "role": "skeptic-precedent",
    "dispatch_id": "2026-08-05-arcanum-cav2-integration-research",
    "run_id": "cav2-integration-run-01",
    "status": "complete",
    "scalar_validation": "revision_required",
    "validation_details": {
      "precedent_gate_completed": true,
      "owner_sovereignty_checked": true,
      "stale_imports_checked": true,
      "semantic_copy_risk_checked": true,
      "direct_source_bindings_required": true,
      "repository_writes": 0,
      "external_web_used": false,
      "memory_used": false
    },
    "blockers": [],
    "native_return_handle": "agent-return://2026-08-05-arcanum-cav2-integration-research/cav2-integration-run-01/spawn-0005/skeptic-precedent",
    "residue": [
      "constitution candidate versus project-local authority status requires owner adjudication",
      "definition and constitution imports require current per-item rescans",
      "artifact adaptation remains planned rather than implemented",
      "the bad .schema.yml acceptance witness lacks an owned discriminating rule",
      "Tier-1 validator port is coupled to candidate Tier-2 metadata machinery",
      "generated and runtime integration claims require exact current source and consumer bindings"
    ],
    "reroute": [
      {
        "target": "constitution-governance",
        "reason": "Adjudicate Stable Repository Constitution status and clarify the schema-form acceptance rule."
      },
      {
        "target": "definitions-governance",
        "reason": "Rescan imports and classify each term as reference, local adaptation, or already-owned skip."
      },
      {
        "target": "artifact-governance-plan-owner",
        "reason": "Separate Tier-1 form enforcement from Tier-2 metadata semantics and repair fixtures."
      },
      {
        "target": "arcanum-generation-runtime-owner",
        "reason": "Provide exact canonical, generated, installed, and behavioral bindings before runtime claims."
      }
    ]
  }
}
```
