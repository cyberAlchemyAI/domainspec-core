---
tags: [inventory, authority-harness, ledger-spec, authority-movement, promotion-record, ontology-vault, bridge-edge, promotion-guardrail, evidence-backfill, open-question]
node_type: evidence-card
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-21
dispatch_id: 2026-06-21-authority-harness-ledger-ontology-unification
dispatch_type: research
working_folder: cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/
sources: [cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md, cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/review-quine-definitional.md, cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/review-lakatos-precedent.md, cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/review-popper-witness.md, cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/AUDIT.md]
---

# Evidence Cards - Authority-Harness / Ledger / Ontology Unification

Each card is a candidate Inventory read model from the audited
`2026-06-21-authority-harness-ledger-ontology-unification` research dispatch
(final_approver ACCEPT). These cards do not promote ontology, definitions,
constitutions, axioms, ledgers, or Context Builder authority, and do not author
a new harness object. Promotion requires the named downstream owner.

## `authority-harness-typed-hole-contract`

- ID: `authority-harness-typed-hole-contract`
- Type: concept
- Status: candidate
- Claim or candidate: The single net-new identity in the proposed
  authority-harness is the typed-hole contract: the shared rail produces a
  `promotion_record` but never sees the `verdict`; `validate_and_promote` is a
  per-kind profile callback the rail never defaults. This is forced by a real
  policy contradiction the rail cannot hold — definitions forbid competing
  authority while constitutions preserve it — so judgment stays per-owner.
- Source refs:
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:32-37`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:226-228`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:260`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/review-quine-definitional.md`,
  `arcanum/arcana/definitions-governance/SKILL.md` (single-normative-voice rule),
  `arcanum/arcana/constitution-governance/SKILL.md` (conflict-preservation rule)
- Authority level: source-backed GROUND (net-new) candidate, downstream review required
- Promotion owner: sigil-development for the contract; definitions-governance and
  constitution-governance for the per-kind judgment profiles; decision-gate for cut-line
- Trace: `2026-06-21-authority-harness-ledger-ontology-unification`; Quine identity gate marked this the only DISTINCT structural form; auditor verified GROUND verdict
- Residue: The callback signature is a design contract, not yet authored on the existing envelope; no profile validators are written.

## `authority-harness-extend-not-author`

- ID: `authority-harness-extend-not-author`
- Type: decision
- Status: candidate
- Claim or candidate: The "authority-harness rails" (C1) and "movement-envelope"
  (C6) collapse under identity to the already-authored
  `authority_artifact_lifecycle_envelope` plus the canonical `promotion_record`
  (the envelope already carries `drift_owner` and `ontology_refs`). The cycle
  closes by EXTENDING that envelope with the typed-hole contract, not by
  authoring a parallel harness/envelope object — a parallel object would itself
  be the identity-collapse failure.
- Source refs:
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:33-36`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:255-266`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/review-quine-definitional.md`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/review-lakatos-precedent.md`,
  `cyberAlchemy-v2/development/refinement-runs/20260621T043600Z-authority-artifact-lifecycle-placement/RESULT.md:54-99`
- Authority level: source-backed EXTEND-OWNED (build-from-owned) candidate
- Promotion owner: CyberAlchemy v2 authority owner; sigil-development to extend the envelope; cross-ref existing card `caol-lifecycle-envelope-contract`
- Trace: `2026-06-21-authority-harness-ledger-ontology-unification`; Lakatos precedent gate found all 7 candidates owned; Quine flagged C1/C6 as field-for-field collapse
- Residue: Requires owner acceptance that the extension target is the existing envelope; the envelope itself remains a candidate lifecycle contract, not promoted authority.

## `ledger-spec-axis-selector`

- ID: `ledger-spec-axis-selector`
- Type: concept
- Status: candidate
- Claim or candidate: The reusable "ledger spec" is a 3-value policy selector
  (`mutability` / `row_identity` / `graph`), not one unifying schema. craft
  (edit-in-place / stable-id / typed-rows+relations), register-dispatch
  (append-only / two-row / flat+json), and signals (append-only / event-append /
  flat-event) are dialects of the axis. The authority movement ledger uses the
  append-only dialect. Caveat: the claim is witnessed for only 2 of 3 dialects —
  the signals JSONL schema is UNREAD, and no in-repo schema validates the
  append-only authority-ledger dialect (it must be built).
- Source refs:
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:193-208`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:263`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/review-popper-witness.md`,
  `.claude/skills/craft/templates/ledger.schema.yml:5-8`,
  `.claude/skills/register-dispatch/SKILL.md:8-13`
- Authority level: source-backed EXTEND-OWNED + BUILD candidate, partial witness
- Promotion owner: sigil-development / register-dispatch owner for the validator; ledger-spec authoring owner
- Trace: `2026-06-21-authority-harness-ledger-ontology-unification`; Popper non-vacuity gate witnessed the row writability but flagged the missing validator (W1)
- Residue: signals JSONL schema unread (mandatory pre-build read); append-only authority-ledger validator does not exist; the "reusable spec over all three" is a 2-point claim until both close.

## `ledger-ontology-bridge-edge-kill-until-amendment`

- ID: `ledger-ontology-bridge-edge-kill-until-amendment`
- Type: question
- Status: open-question
- Claim or candidate: "ledger = ontology subgraph" is killed as an identity (it
  is the shipped vault↔`ontology_events` event-sourcing split, kept as a typed
  projection). The node→promotion-record forward-only movement/bridge edge that
  would close the ontology tie CANNOT be hand-built today: the ontology
  constitution has exactly two forward-only carve-outs (keyed on
  `is_session: true` or a target under `.claude/skills|agents/**`), the skip list
  is explicitly closed at those two, and a promotion edge matches neither
  (OQ-C open); no `node_type` value exists that lets the record be a vault node
  carrying a lawful inverse. The ontology-tie cycle therefore has exactly one
  open link. It is fixable via the schema-evolution gate: (A) a third
  forward-only carve-out keyed on the movement-event logical type, or (B) a
  `promotion-event` node_type with a lawful catalog inverse.
- Source refs:
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:40-65`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:236-237`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/review-popper-witness.md`,
  `implementation/domainspec/vault/ontology-conventions.md:301-320`,
  `implementation/domainspec/vault/ontology-conventions.md:312`,
  `implementation/domainspec/vault/ontology-conventions.md:56`
- Authority level: KILL-until-amendment / open-question evidence
- Promotion owner: ontology-vault and constitution-governance via the schema-evolution gate; decision-gate to choose option A vs B
- Trace: `2026-06-21-authority-harness-ledger-ontology-unification`; Popper no-witness KILL on the bridge edge; auditor confirmed the open-link honesty requirement is met
- Residue: No chosen amendment; the full premise→axiom promotion atomicity (OQ-6) is itself still Open, so identity-collapse of ledger into ontology would assert atomicity the repo lacks.

## `authority-workflow-vs-maturity-status-placement`

- ID: `authority-workflow-vs-maturity-status-placement`
- Type: dependency-rule
- Status: candidate
- Claim or candidate: Workflow status and maturity status are orthogonal axes on
  different objects: `current_status` (the 9-value workflow ladder) lives on the
  ledger/movement record; maturity `status` (the 5-rung draft→evergreen ladder)
  lives on the ontology node; the orthogonality rule forbids merging them into
  one field. Popper witnessed this as the cleanest part of the loop (confidence
  mapping to `veracidade`/`convicção`).
- Source refs:
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:213-217`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md:255-266`,
  `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/review-popper-witness.md`,
  `implementation/domainspec/vault/ontology-conventions.md:332-345`,
  `.claude/skills/craft/templates/ledger.schema.yml:111-121`
- Authority level: source-backed GROUND (ruling) candidate, conventions-amendment scope
- Promotion owner: ontology-vault conventions owner and definitions/constitution-governance for the placement amendment
- Trace: `2026-06-21-authority-harness-ledger-ontology-unification`; Quine marked DISTINCT (placement ruling new), Popper witnessed, auditor verified GROUND
- Residue: The placement is a ruling, not yet written into ontology-conventions or the envelope schema.
