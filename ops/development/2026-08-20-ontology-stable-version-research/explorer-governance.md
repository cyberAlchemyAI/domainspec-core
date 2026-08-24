# explorer-governance.md — what governance permits and forbids

Agent: Banach, Stefan (explorer, governance lane) · Dispatch: `2026-08-20-ontology-stable-version-and-runtime-research`
Claim ceiling: cited synthesis only. Grants no ontology authority, authorizes no runtime
implementation, promotes nothing, lifts no gate. Residue `ontology-authority-not-granted` and
`runtime-implementation-not-authorized` stand. No design is proposed below.

---

## 1. What "stable" can mean here

**There is no authority kind and no lifecycle status named `stable`.** Three enumerations were
checked exhaustively:

- Authority kinds — nine rows, none `stable` (`cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md:25-35`;
  authoritative table at `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md#authority-kinds`).
- Workflow states — `source-evidence, import-candidate, inventory-candidate, ontology-candidate,
  review-candidate, active, drift-flagged, superseded, deprecated`
  (`cyberAlchemy-v2/ontology/LIFECYCLE-MODEL.md:26-34`). The promoted state is `active`, not stable.
- Node `candidate_status` — `candidate, reviewed-candidate, deferred, blocked, projected`
  (`cyberAlchemy-v2/ontology/NODE-MODEL.md:83-89`).
- Schema `lifecycle_status` enum — `raw, catalogedEvidence, reviewableSignal, promotionRecordDraft,
  candidate, premise, reviewed, promoted, contradicted, retired, rejected, deferred`
  (`arcanum/arcana/ontology-vault/development/schema-validation-plan/schema/branch-aware-ontology-candidate.schema.yml:44-57`,
  key path `$defs.lifecycle_status.enum`). No `stable` member.

The term that **is** defined is `CAV2-D1: Stable Repository`, `Status: active`
(`cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:18-30`): "A stable repository is a
maintainable repository surface whose authority, source evidence, promoted contracts, validation
evidence, implementation work, and operating traces can be understood without hidden conversation
context…". Its operational test is repository-scoped, not version-scoped: "The repository is not
stable merely because files exist; it is stable when its authority model, source spine, promotion
gates, and validation surfaces are navigable and reviewable" (`:34-38`). Boundary: "This term does
not mean finished product, public repository, automatic ownership of every historical CyberAlchemy
source, or implementation complete" (`:56-59`).

Two informal uses exist and neither is a status:

- `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md:155-159` — OQ-1 uses "stable enough": "write a
  deterministic check only after the authority object schema and promotion records are stable
  enough to avoid freezing the wrong shape. **Status: OPEN.**"
- `cyberAlchemy-v2/ontology/promotion-requests/2026-06-23-authority-object-schema-proposal.md:111`
  — "then **decision-gate** to declare the schema stable → OQ-1 clears → build the closure
  validator." That document is `Status: **candidate proposal** (non-executed…)` (`:3`) and states
  "**Non-executed.** This proposal does not amend NODE-MODEL" (`:109`).

**Reading permitted by the corpus:** "stable" is (a) a defined property of a *repository*
(CAV2-D1), and (b) an owner act reserved to **decision-gate** that has never been performed for any
schema or ontology version. It is not a value an artifact may carry, and nothing in the corpus lets
an ontology version self-declare it. Note also
`arcanum/arcana/ontology-vault/development/schema-validation-plan/GOVERNED-CANDIDATE-BUNDLE.md:12`
calls the bundle "one stable reference point" while its own header reads `Status: published
candidate` (`:3`) — prose, not a status claim.

## 2. Gates that must clear first, and their current status

| Gate / question | Selector | Status |
|---|---|---|
| OQ-1 — should authority kinds become validator-backed | `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md:155-159` | **OPEN** |
| OQ-2 — `invariant`/`axiom` as first-class kinds | `AUTHORITY-MODEL.md:161-165` | **OPEN** |
| NODE-MODEL instance layer (the "declare the schema stable" precondition) | `promotion-requests/2026-06-23-authority-object-schema-proposal.md:109-111` | **non-executed candidate**; ontology-route amendment not made |
| OVS-GATE-001 promotion boundary | `arcanum/…/decision-gates/OVS-GATE-001-promotion-boundary.md:3`, `:256-264` | **PASS** (bundle only) |
| OVS-GATE-002 PromotionRecord companion boundary | `…/OVS-GATE-002-promotion-record-companion-boundary.md:3`, `:245-250` | **PASS** (record-kind only) |
| OVS-GATE-003 DomainSpec handoff route | `…/GOVERNED-CANDIDATE-BUNDLE.md:154` | **pending**; no gate file exists (`decision-gates/` holds 001, 002, 004 only) |
| Template promotion gate | `GOVERNED-CANDIDATE-BUNDLE.md:155` | **pending** |
| Label governance gate (`meaning` as branch label) | `GOVERNED-CANDIDATE-BUNDLE.md:156` | **deferred** |
| OVS-GATE-004 default output declaration | `…/OVS-GATE-004-default-output-declaration.md:3`, `:157-165` | **PASS**, narrow: `json-primary-sigil-written-only` (`:100-106`) |

OVS-GATE-004 is explicit that it moved nothing else: "It touches neither gate that is still open"
(`:117-118`), and reaffirms the 001 prohibitions verbatim (`:129-135`).

Unactioned review change-requests that bear on any stability claim
(`cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:219-240`):

- CR-1 **[CRITICAL]**, still live — route 3 must point at `authority/AUTHORITY-MODEL.md`, not
  `ontology/AUTHORITY-KINDS.md`. Verified unfixed: `CLAUDE.md:67`, `AGENTS.md:176`.
- CR-2 **[CRITICAL]**, still live — no definition card exists for `authority kind` or `canonical
  kind`. Verified: 56 `CAV2-D` cards, no `Term: authority kind` / `Term: canonical kind` line.
- CR-3 **[MAJOR]** — delete `ontology/AUTHORITY-KINDS.md`; file still present, `Status: candidate`
  (`AUTHORITY-KINDS.md:3`).
- CR-4 **[MAJOR]** — `canonical_kind`/`authority_kind` carry no `enum` in the admission schema;
  "CAV2-D49's 'closed, default-deny' exists in exactly one place: review prose" (`findings.md:96`).
- CR-9 **[DISPATCH DEFECT]** — three fabricated quotes propagated through `attacks.md`; that file
  "**must not be cited as independent confirmation**" (`findings.md:238-240`).

`CANONICAL-KINDS.md:6-9` carries its own warning: "**Uncited by construction.** … Do not read an
unattributed claim here as ratified."

## 3. What a runtime may and may not decide

May: emit read models. "Projections are read models… They do not create authority"
(`ontology/projections/README.md:8-10`); allowed kinds and their blocked uses at `:39-45`; emission
rule at `:47-50` — "A projection may emit owner-approved state only when the owner decision permits
the use scope. Blocked, deferred, or unknown candidates may appear only as such." Relation
`emits_projection_when_allowed` is permitted with effect `projection` (`RELATION-MODEL.md:55`).

May not: fill the verdict. "Ontology may represent the rail and projection. It must not fill the
verdict hole" (`LIFECYCLE-MODEL.md:48-49`); "The package models authority. It does not decide
authority" (`PACKAGE-MODEL.md:14`); "Ontology can model authority, but it cannot decide authority"
(`AUTHORITY-MODEL.md:125`). Generated output is posture `posture.generated`, blocked use
"Canonical source" (`AUTHORITY-POSTURES.md:30`). `kind.runtime_contract` is owned by "task-session
after owner gates", forbidden collapse "Not generated mirror output" (`AUTHORITY-KINDS.md:32`).
Identity is local, not global: `concept_id` / `relation_id` are "Local stable identifier"
(`NODE-MODEL.md:18`; `RELATION-MODEL.md:15`).

Ingest rule 5 binds any runtime projection: "Generated runtime projections must point back to
canonical sources before they influence capability contracts" (`SOURCE-MAP.md:32-33`).

## 4. Currently FORBIDDEN (quoted, with selectors)

- `PACKAGE-MODEL.md:46-54` out of scope: "live vault `node_type` creation · vault `## Connections`
  edge creation · schema amendment · movement-edge creation · **runtime contract definition** ·
  generated mirror authority · promotion verdicts · public/private release decisions".
- `RELATION-MODEL.md:62-71` — not allowed as live relations: `witnesses_authority_movement`,
  `promotion_movement_edge`, `ledger_row_as_subgraph`, `promotion_event_as_node`, `movement_as_node`;
  "They require schema governance, edge law, and authority-ledger validation before any executable
  or vault effect."
- `RELATION-MODEL.md:40-43` — value-constraining + cycle-permitted relations are "blocked until
  schema governance records a contextuality-obstruction review and an explicit exception. Unknown
  values are typed residue, not permission." Constitution source: `CAV2-C13`
  (`STABLE-REPOSITORY-CONSTITUTION.md:247-264`).
- `OVS-GATE-001…:240-247` still disallowed: "promoting canonical Ontology Vault templates; requiring
  Inventory to emit ontology fields; mutating structured-action-schema; **treating the JSON Schema
  candidate as final canonical schema**; mutating DomainSpec or CyberAlchemy source packages;
  requiring future systems to adopt the fields."
- `OVS-GATE-004…:129-135` still disallowed: the 001 items unchanged, plus "Importing `meaning` or
  any other label under deferred governance; Requiring any consuming repository to emit, adopt, or
  migrate to these keys; Rewriting records held by owners."
- `GOVERNED-CANDIDATE-BUNDLE.md:87-96` disallowed use, including "treat this bundle as final
  canonical Ontology Vault schema".
- `CAV2-D49` (`DEFINITIONS.md:3247-3261`): an artifact whose kind is not in the closed enumeration
  "may not acquire or exercise authority — it defaults to **blocked** pending an owner decision".
- `CAV2-C2` (`STABLE-REPOSITORY-CONSTITUTION.md:34-51`) non-examples: "Letting an ontology candidate
  redefine a project term. Letting observability signals become design authority without review."
- `promotion-requests/README.md:8-10` — "A request is not a verdict, not a PromotionRecord-compatible
  decision, and not an authority artifact."

## Residue

- No owner route exists for cross-project ontology migration (`OVS-GATE-004…:142-144`).
- Authority-ledger validator missing (`LIFECYCLE-MODEL.md:58-62`).
- Two CRITICAL review change-requests (CR-1, CR-2) remain unactioned as of this read.
