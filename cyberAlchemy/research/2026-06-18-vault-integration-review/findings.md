# Findings: CyberAlchemy And DomainSpec Vault Integration

Dispatch: `2026-06-18-cyberalchemy-vault-integration-review`
Verdict: FIX before integration

No critical finding survives verification because this run did not mutate
canonical vault schema or promote CyberAlchemy artifacts into the vault. The
remaining issues are MAJOR integration gates: they must be resolved before
CyberAlchemy is described as integrated with `implementation/domainspec/vault/`.

## Surviving Change Requests

| Severity | Finding | Required Change |
| --- | --- | --- |
| MAJOR | Subagent authority is split between the active vault constitution and a repo-local draft replacement used operationally. | Promote/sync the repo-local constitution or mark the older vault constitution historical before citing subagent strategy as stable vault authority. |
| MAJOR | CyberAlchemy primitives do not yet have an executable adapter contract. | Create a matrix: CyberAlchemy primitive -> DomainSpec `node_type`/`status`/`layer`/edge -> authority scope -> owner route -> promotion gate -> validator command. |
| MAJOR | PromotionRecord, B3/B4, and OIL-style records can be mistaken for vault schema. | Keep them as review/evidence companion records until admitted through DomainSpec schema amendment. |
| MAJOR | Edge authority is unresolved across conventions, executable frontmatter, inverse rules, and validation. | Reconcile the 21/22 edge catalog split, the `retrofits` inverse exception, and executable `EDGE_FIELDS` before adding method edges. |
| MAJOR | CyberAlchemy labels overlap with governed vault lifecycle and confidence terms. | Keep CyberAlchemy labels method-local as `method_status` or `witness_status`; do not map them directly to vault `status`, veracidade, conviccao, or applicability. |
| MAJOR | New frontmatter/control values would require schema governance. | Route any new node type, status, edge field, lifecycle control, or confidence projection through schema amendment and migration. |
| MAJOR | Enforcement is not sufficient for an integration claim. | Add a validation path: Tier 1 frontmatter checks, Tier 2 edge-name checks, Tier 3 graph checks, and cross-system fixtures/report gates. |
| MAJOR | Current and proposed classification axes are mixed in the source material. | Use current `layer` in the adapter contract; treat `scope`, `domain`, `schema`, and `instance` as migration pressure until accepted. |
| MAJOR | Cross-system witnesses need explicit authority boundaries. | Add `authority_scope` values such as external witness, method-local evidence, vault-governed, and executable schema, with owner, use scope, contradiction path, maintenance route, and non-authority notice. |
| MAJOR | Provenance inputs can be over-promoted. | Cap sessions, telemetry, reflections, synthesis, and subagent outputs at candidate/review authority unless an owner route promotes them. |
| MINOR | Templates are missing for repeatable integration review. | Add seed templates for review output, promotion packet, retrieval packet, and maintenance/reflection packet with required selectors and verdict vocabulary. |

## Per-Artifact Verdicts

| Artifact | Verdict |
| --- | --- |
| `corpus.md` | KEEP as review corpus. It must continue to separate current authority, proposed futures, and companion evidence shapes. |
| `attacks.md` | KEEP as attack ledger. Preserve verifier demotions so later readers do not treat review gates as discovered canonical breakage. |
| `findings.md` | FIX verdict accepted. The surviving rows are the work required before integration can be claimed. |

## Dropped Or Refuted Interpretations

| Interpretation | Verdict |
| --- | --- |
| PromotionRecord is already a DomainSpec vault node type. | DROP |
| CyberAlchemy labels are already vault statuses. | DROP |
| Method-specific edges can be added before catalog reconciliation. | DROP |
| Robot-talks or dispatch outputs create a separate authority family. | DROP |
| Retrieval/session futures prove current runtime integration. | DROP |

## Next Packet

Create a bounded implementation-readiness packet before mutating the vault:

- `method-vault-adapter.seed.md`
- `authority-scope.profile.md`
- `edge-catalog-reconciliation.review.md`
- `frontmatter-schema-alignment.review.md`
- `validation-gate.plan.md`

These should remain review/design artifacts until the vault owner route accepts
the specific schema and validator changes.
