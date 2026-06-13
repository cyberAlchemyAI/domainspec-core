# TO-VLAD — Backend Engineer / Domain Modeler

**Role:** Vault, classification, posture enforcement, audit log, rule engine, OS baseline, imaging, signing, Golden Image, domain modeling.
**Source:** [docs/strategy/development/node-on-desk-readiness/DISPATCH-VALIDATION.md](docs/strategy/development/node-on-desk-readiness/DISPATCH-VALIDATION.md) · workbook role map [docs/golden-quill-task-role-breakdown-handoff.md](docs/golden-quill-task-role-breakdown-handoff.md)

These tasks are **refine-solvable and specced** — you can start building now. Specs carry Define→Design→Plan, acceptance criteria, and first steps.

## Agent execution contract — run this first

When Vlad asks an agent to "read the artifacts" or begin this handoff, the
agent should operate the Craft nodes directly instead of treating this as a
static task list.

1. Read `pipeline/SESSION_BOOTSTRAP.md` for project orientation.
2. Read this handoff and linked artifacts by path.
3. Run `$craft state` for the ledgers in the Vlad-facing Craft scope below.
4. Use `$interrogation` only for Vlad-owned technical choices: schema shape,
   interface boundary, implementation ordering, or evidence format. Ask one
   question at a time.
5. Do not ask Vlad to resolve Josh-owned business/governance decisions. Route
   those to `TO-JOSH.md` and keep the dependent task blocked.
6. After each answer or implementation receipt, update the owning Craft ledger:
   record decision evidence, add receipt paths, advance next moves, or preserve
   residue.
7. Return a `Craft Result` naming the files touched, validation run, blockers,
   and next move.

### Vlad-facing Craft scope

| Scope | Ledger | Vlad interface |
| --- | --- | --- |
| hardware image | `docs/features/hardware-golden-image/.craft/ledger.yml` | Image verification, backup/export/recovery, manifest consumer boundary. |
| Tilth runtime | `docs/features/tilth-runtime-build/.craft/ledger.yml` | Backend work-packs, posture enforcement once Josh ratifies canon, audit log, rule engine, Golden Image assembly. |
| capital logic | `docs/features/capital-logic-library/.craft/ledger.yml` | Rule-pack and card schema implementation without CIC/CLC coupling. |
| root promotion governance | `.craft/ledger.yml` | L0 learning-loop spine, promotion-authority gate, redaction tables, KPI/event count reconciliation. |
| node readiness | `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml` | Consume parent RG gates; do not claim parent recomposition without receipts. |

### Interrogation interface for Vlad

Use `$interrogation` when a technical decision is needed, for example:

```text
$interrogation docs/features/hardware-golden-image --mode technical-interface
```

Good Vlad questions ask for one concrete choice: manifest field name, digest
format, receipt path, interface owner, task order, or validation command.
Every answer should update either the relevant `BUILD-SPEC.md`,
`INVOKE-DEVELOPMENT.md`, task artifact, or Craft ledger evidence.

## Build now (specs ready)

1. **Golden Image write + per-unit verification** — `GAP-HGI-IMAGE-VERIFY` (block)
   → [docs/features/hardware-golden-image/BUILD-SPEC.md](docs/features/hardware-golden-image/BUILD-SPEC.md)
   Build a repeatable write+verify consuming the existing Ed25519 signing chain ([router.yaml](router.yaml) L17–48). Acceptance: boot-time manifest verification + byte-flip failure case (toy-game it).

2. **Backup / customer-owned export / recovery** — `GAP-HGI-BACKUP-RECOVERY` (block)
   → same spec. Must honor the Sovereignty Promise (customer owns data + keys). Acceptance: wipe→recover round-trip digest match.

3. **Tilth runtime work-packs — backend lane** — `GAP-TRB-WORK-PACKS` (block)
   → [docs/features/tilth-runtime-build/BUILD-SPEC.md](docs/features/tilth-runtime-build/BUILD-SPEC.md)
   Your packs: vault + classification, posture enforcement, audit log, rule engine, Golden Image assembly. Critical path WP-1→WP-2→WP-6→WP-7→WP-8→WP-13→WP-14.

4. **Golden Image handoff contract (lead)** — `GAP-TRB-GOLDEN-IMAGE-HANDOFF`
   → tilth spec + hardware spec. Jointly fix the manifest/signature schema with **Koichi** before WP-14 assembly. This is the B→A interface the hardware node's verify step consumes.

5. **Capital Logic rule-pack + card schema** — `GAP-CLL-RULE-PACKS`, card schema/governance
   → [docs/features/capital-logic-library/BUILD-SPEC.md](docs/features/capital-logic-library/BUILD-SPEC.md)
   Build the schemas now (rule content + card content come from Josh). **Hard guardrail:** no `clc_binding` / `cic_binding` field anywhere — `F-CIC-CLC-COUPLING-VIOLATION` fail-closed. The anti-coupling lint test is part of acceptance.

6. **Promotion-governance build gaps** — → [.craft/artifacts/BUILD-SPEC.md](.craft/artifacts/BUILD-SPEC.md)
   - `GAP-DESIGNED-NOT-BUILT` (block) — build the L0 learning-loop spine vs. the 10 First-Slice fixtures.
   - `GAP-PROMO-ENFORCE` (block) — build the promotion-authority gate + neg/pos/signature tests.
   - `GAP-REDACTION-TABLES` — per-CIC table schema + `R-REDACTION-NO-CLC` lint.
   - `GAP-KPI-COUNT` — reconcile prose "47" → enum 44 (`domain.md:402–449` authoritative); doc-lint, no enum mutation.
   - `GAP-EVENT-COUNT` — name the two axes (9 ingestion families / 13 op-output events); strike the phantom "12".

## Decisions you propose (Josh ratifies)
→ [.craft/artifacts/BUILD-SPEC.md](.craft/artifacts/BUILD-SPEC.md) Part A
- **DEC-OQ4** (BLOCKING, P0) — three typed decision surfaces vs. one unified enum. Recommendation A (three surfaces) makes the promotion gate trivially expressible on one type. Put your proposal to Josh.
- **DEC-D2-FLIP** — operator-signed per-org Ed25519 L0→L1 mutation flip (rec A).
- **DEC-D3-SHARED-GATE** — structural no-metric rule + K≥3 orgs (Josh sets K).
- **DEC-D4-VERIFY** — Option B + named guardrail-KPI set.

## Blocked — do not start until ratified
- **Posture enforcement build** (`GAP-TRB-POSTURE-CANON`, WP-9/WP-10) — blocked on **DEC-BC-POSTURE-VOCAB** (Josh). Spec is written against the three-posture canon; build when the canon translation is ratified. **Never** implement the deprecated "Sanitized"/4-posture or opaque-slot mechanism.

## Coordinate with
- **Koichi** — Golden Image manifest/signature schema (joint lock before assembly); shared Scout + ensemble-review packs.
- **Victor** — your audit-log + posture-enforcement output is what his guardrail tests assert against.
