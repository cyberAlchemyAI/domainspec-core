# Arcanum ↔ CyberAlchemy v2 integration findings

Dispatch: `2026-08-05-arcanum-cav2-integration-research`

Run: `cav2-integration-run-01`

Evidence revision: `synthesis-zig-zag-01`

Authority effect: none

## 1. Plain-language answer

CyberAlchemy v2 (CAV2) ties to Arcanum today as a **private, project-local documentary and import consumer** of selected **public Arcanum** sources, methods, and candidate patterns. CAV2 has real staging seams and committed plans showing where Arcanum material must be re-rooted and locally admitted. It does **not** have a proved implemented CAV2 adapter, installed generated package, callable end-to-end Arcanum runtime integration, release, deployment, or publication chain.

The boundary is deliberately asymmetric. Public Arcanum material may be referenced, staged, and adapted inside private CAV2, but its Arcanum owner remains authoritative until a distinct CAV2-local owner admits a local rule. Private CAV2 or DomainSpec material cannot move back into public Arcanum without scrub, source-owner review, an explicit public-owner decision, mutation, and verification. Inventory, ontology, research, generation, validation, execution, receipts, Craft, and Git history can supply evidence; none can perform that owner decision for itself. [Authority explorer `AUTH-001`, `AUTH-003`, `AUTH-012`, return `agent-return://2026-08-05-arcanum-cav2-integration-research/cav2-integration-run-01/spawn-0001/explorer-authority`; direct sources: `cyberAlchemy-v2/README.md:3-16,36-47,119-127`, `cyberAlchemy-v2/SOURCE-MAP.md:8-21`, `cyberAlchemy-v2/authority/boundaries.md:6-14,58-65`.]

CAV2 does declare an active local authority model, active local definitions, and an active decision surface. That does not make every CAV2 authority kind uniformly active: the Stable Repository Constitution is simultaneously labeled `candidate` and `project-local constitution`; disciplines and promotion policy are candidate; ontology is a candidate projection/request surface; Craft is coordination; and CAV2 owns an Inventory read-model boundary but has no local machine index. “Authority spine” is therefore a private architectural descriptor, not a promoted authority kind. [Authority explorer `AUTH-002`, `AUTH-005`; operational explorer `OP-018`, `OP-019`; sources: `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md:23-29,48-72,90-103`, `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md:1-10`, `cyberAlchemy-v2/disciplines/DISCIPLINES.md:3-24`, `cyberAlchemy-v2/authority/promotion-policy.md:3-6`, `cyberAlchemy-v2/inventory/README.md:3-11`.]

This report is frozen to parent commit `ab46061bf14db23a01054c2fd3fafec60fb5eb2f` and Arcanum commit `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`, while separately labeled working-tree evidence remains working-tree evidence. The evidence closure is `ready`; that admits this report only and creates no authority, implementation, promotion, publication, release, deployment, or production effect. [Evidence closure: `receipts/evidence-closure.json`; explorer snapshot limits: operational `OP-020..022`, systems `CEIL-003`.]

## 2. DomainSpec, Arcanum, Saturn, and CyberAlchemy-v2 role map

| Surface | Verified role now | Intended role | Ownership and proof ceiling |
|---|---|---|---|
| DomainSpec | Private structured-intent and modeling evidence; a source of baselines and constraints | Supply precise intent/contracts for comparison against reality | DomainSpec owners retain private implementation authority. CAV2, Craft, validation, and Arcanum cannot manufacture or publish it. Do not describe DomainSpec as shipped. [Systems explorer `SYS-002`, `EDGE-001`, `EDGE-005`; sources: `cyberAlchemy/agentic-system-deep-dive.md#domainspec`, `ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md:17-49`, `cyberAlchemy-v2/SOURCE-MAP.md#source-cohorts`.]
| Arcanum | Public reusable framework for methods, capabilities, bounded lifecycle execution, generation, and observability | Supply accepted correction/execution routes within the broader loop | Each public definition, constitution, discipline, capability, and tool keeps its narrow Arcanum owner and individual lifecycle status. Repository/docs evidence is not CAV2 runtime or live deployment proof. [Authority explorer `AUTH-003`; systems explorer `SYS-002`, `EDGE-002`; sources: `arcanum/README.md`, `arcanum/definitions/DEFINITIONS.md:340-435`, `cyberAlchemy/agentic-system-deep-dive.md#arcanum`.]
| Saturn | Intended convergence framing: observe reality, compare to intent, decide, route correction, verify, return evidence | Close the intent↔reality loop across layers | Saturn is an architecture owner, not an Arcanum alias or a CAV2 authority kind. Current documentation says the closed loop is still being assembled; no shipped regulator is proved. [Systems explorer `SYS-002`, `EDGE-003`, `FB-001`; source: `arcanum/docs/saturn.html#loop`.]
| CyberAlchemy v2 | Private source-ledgered consolidation surface with a repository-declared active local authority model | Become an owner-reviewed stable base for downstream construction | CAV2 routes only CAV2-local reliance. It does not own Arcanum, DomainSpec, or Saturn and has not been extracted, released, deployed, or published as a standalone base. [Authority explorer `AUTH-001`, `AUTH-011`; systems explorer `SYS-001`, `EDGE-010`; sources: `cyberAlchemy-v2/README.md:3-16,36-47`, `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d9-cyberalchemy-v2`.]

Two loops therefore coexist without collapsing. Saturn’s intended loop is causal system convergence. CAV2’s loop is review-oriented local admission: source → candidate/read model → named owner → accepted local artifact, with block, defer, demote, or reroute available. The first does not grant CAV2 apex authority; the second does not implement Saturn. [Systems explorer `FB-001..003`; sources: `arcanum/docs/saturn.html#loop`, `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md#core-flow`, `cyberAlchemy-v2/authority/promotion-policy.md`.]

## 3. Exact ownership, source direction, and authority matrix

### Status by authority kind

| ID | Surface | Current state | Narrow owner and ceiling |
|---|---|---|---|
| `STAT-01` | Authority model | Repository-declared active; deterministic closure pending; kind enforcement partly review-mode | CAV2 authority owner; no independent bootstrap-validity proof. [Authority explorer `AUTH-002`; `authority/AUTHORITY-MODEL.md:23-29,48-72`.]
| `STAT-02` | Definitions | Active local source; individual records retain their own states | CAV2 definitions governance; no Arcanum-wide authority. [Authority explorer `AUTH-004`; `authority/definitions/DEFINITIONS.md:3-16`.]
| `STAT-03` | Decisions | Active surface; outcomes are record-specific | Named decision owner; a decision is not implementation. [Authority explorer `AUTH-002`; `authority/decisions/README.md:3-8`.]
| `STAT-04` | Stable Repository Constitution | Both `candidate` and `project-local constitution` | Constitution governance/Decision Gate must adjudicate; no editorial normalization here. [Authority explorer `AUTH-005`; `authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md:1-10`.]
| `STAT-05` | Disciplines | Candidate | Discipline governance; no canonical enforcement or execution effect. [Authority explorer `AUTH-003`; `disciplines/DISCIPLINES.md:3-24`, `arcanum/arcana/discipline-governance/README.md:19-21`.]
| `STAT-06` | Promotion policy | Candidate local policy plus an active owner-routing rule | Named owners decide; the document does not prove an executed promotion ladder. [Authority explorer `AUTH-002`; `authority/promotion-policy.md:3-6,20-29`.]
| `STAT-07` | Ontology | Candidate projection/request surface | Ontology route plus source owner; no authority-writing projection. [Authority explorer `AUTH-008`; `ontology/README.md:3-31`, `ontology/projections/README.md:6-19,37-57`.]
| `STAT-08` | Craft | Committed local ledger and derived views | Craft owner; coordination/navigation only. [Operational explorer `OP-005`, `OP-018`; `.craft/ledger.yml`, `CRAFT.md`, `.craft/index.json`, last-touch commit `32ee3c2c5a8e1c9f43f34017549cf1bea4fcf539`.]
| `STAT-09` | Inventory | CAV2-owned exported read-model boundary; no CAV2 machine index | CAV2 Inventory owner; not a standalone knowledge runtime and never a decision/promotion owner. [Operational explorer `OP-007`, `OP-019`; `inventory/README.md:3-11`.]

### Stable typed-edge registry

The fields below are independent. Privacy is never changed implicitly, and “inherited” means a transition preserves the input’s classification.

| ID | Source → target / relation | Owners | Current state → legal transition | Privacy; ceiling and non-effects | Evidence binding |
|---|---|---|---|---|---|
| `REL-001` | DomainSpec intent → Saturn baseline / supplies intended baseline | DomainSpec owner → Saturn architecture owner | Intended architecture → separate regulator proof | Private; no shipping or authority transfer | Systems `EDGE-001`; `agentic-system-deep-dive.md#domainspec`, `SATURN-LAYER-MAP.md:17-49` |
| `REL-002` | Arcanum capability → Saturn correction route / bounded execution | Capability owner → Saturn architecture owner | Architectural role → select one accepted capability | Public→inherited; execution is not Saturn | Systems `EDGE-002`; `agentic-system-deep-dive.md#arcanum` |
| `REL-003` | Evidence → Saturn feedback / supplies intended feedback | Validator/observer → Saturn owner | Intended, partly documented → bind exact evidence to an implemented regulator | Inherited; evidence cannot decide | Systems `EDGE-003`, `FB-001`; `arcanum/docs/saturn.html#loop` |
| `REL-004` | Public Arcanum artifact → CAV2 import candidate / references or stages | Upstream owner → CAV2 import owner | Observed staging seam → pin source, lifecycle status, posture, and local owner | Public→private; no admission or authority transfer | Authority `AUTH-003`; systems `EDGE-004`; `SOURCE-MAP.md:14-18`, `authority/imports/constitutions/MANIFEST.md#re-scan-2026-07-01` |
| `REL-005` | CAV2 intent → Invoke package / candidate authoring | CAV2 source owner → Invoke mode owner | Authoring contract observed; examples mixed → validate and hand off | Private/inherited; no mutation or promotion | Operational `OP-003`; `arcanum/spells/invoke/README.md`, `arcanum/spells/invoke/plan.md` |
| `REL-006` | Import candidate → local candidate / classifies or plans adaptation | Import owner → exact local candidate owner | Staging observed; adaptation planned → per-item owner review | Private; no locally admitted import or adapter implementation | Authority `AUTH-006`; operational `OP-015..016`; `development/artifact-governance-import/PLAN.md:1-33`, commit `fad671aed4ebf6c1405e4264a40d14e3ee33e740` |
| `REL-007` | Definition candidate → canonical local definition / requests promotion | Candidate owner → definitions governance | Normative, record-specific route → explicit decision and canonical mutation | Private; use, ontology, or tests cannot promote | Authority `AUTH-004`; `authority/AUTHORITY-MODEL.md:48-72`, `authority/imports/definitions/MANIFEST.md:7-11,37-43` |
| `REL-008` | Constitution candidate → local constitution / requests promotion | Candidate owner → constitution governance | Unresolved `STAT-04` → owner adjudication and mutation | Private; Task Session or validator cannot decide | Authority `AUTH-005`; `STABLE-REPOSITORY-CONSTITUTION.md:177-203,501-505` |
| `REL-009` | Practice candidate → discipline state / requests maturity | Steward → discipline governance | Candidate route → explicit card/catalog mutation | Private; presence or syntax cannot mature | Authority `AUTH-002..003`; `AUTHORITY-MODEL.md:48-72`, `disciplines/DISCIPLINES.md:3-24` |
| `REL-010` | Contested question → decision record / requests resolution | Source owner → Decision Gate/named owner | Active, record-specific route → explicit named-owner decision | Private; decision is not implementation | Authority `AUTH-002`; `authority/decisions/README.md:3-8`, `AUTHORITY-MODEL.md:48-72` |
| `REL-011` | Spec candidate → canonical spec / requests promotion | Proposer → named spec owner/gate | Normative template; no specific witness → owner acceptance and mutation | Inherited; research/interface is not a spec | Authority `AUTH-002`; `AUTHORITY-MODEL.md:48-72` |
| `REL-012` | Runtime-contract candidate → canonical contract/spec/capability / requests semantic acceptance | Author → named semantic runtime-contract owner/gate | Normative template; no specific witness → semantic-owner acceptance | Inherited, no declassification; Task Session cannot own or promote meaning | Authority `AUTH-002`; `AUTHORITY-MODEL.md:48-72,90-103`; definitional reviewer repair retained in revision |
| `REL-013` | Accepted rule/spec/contract or explicit prototype scope → bounded attempt / constrains admission | Semantic/prototype owner → Task Session | Public admission contract observed; CAV2 end-to-end absent → admit one frozen attempt | Inherited; no semantic promotion, release, or deploy | Operational `OP-004`; `arcanum/arcana/task-session/SKILL.md` |
| `REL-014` | Implementation → validation receipt / checked into | Implementation owner → validator owner | Bounded examples observed → run declared checks on frozen bytes | Inherited; bounded conformance only | Operational `OP-009`; exact trace receipts in `TRACE-OP-POS-001` and `TRACE-OP-NEG-001` |
| `REL-015` | Validation result → named owner evidence / supplies evidence | Validator → semantic/lifecycle owner | Normative plus bounded historical use → named owner interprets | Inherited; pass cannot promote | Operational `OP-009`, `OP-014`; `authority/promotion-policy.md:20-29` |
| `REL-016` | Invocation result → observability signal / observed as | Capability owner → observer | Observer contract and sampled no-effect receipt → separate maintenance decision | Inherited; no mutation or maintenance authority | Operational `OP-010`; `arcanum/arcana/signal-observer/SKILL.md`; sampled Invoke receipt says `authority_effect: none` |
| `REL-017` | Source/evidence → Inventory view / discovery index | Source owner → CAV2 Inventory owner | Exported boundary; local machine index absent → rebind to direct owner | Inherited→private projection; no selection, decision, or promotion | Operational `OP-007`, `OP-019`; `inventory/README.md:3-11` |
| `REL-018` | Owner-accepted state → ontology projection / maps or projects | Source owner → ontology route | Candidate projection surface → named source-owner request | Inherited→private projection; no self-promotion or verdict | Authority `AUTH-008`; operational `OP-008`; `ontology/README.md:3-31`, `ontology/projections/README.md:6-19,37-57` |
| `REL-019` | Receipts/events → Craft ledger/views / records | Receipt owner → Craft owner | Committed ledger/views → validate references and derive views | Private; no owner substitution | Operational `OP-005`, `OP-018`; `.craft/ledger.yml`, `.craft/index.json`, `CRAFT.md` at commit `32ee3c2c5a8e1c9f43f34017549cf1bea4fcf539` |
| `REL-020` | Terminal receipt + prerequisite → joined result / routes and joins | Closeout owner → Router, prerequisite owner, Refresh owner | Contracts/negative fixtures observed; real CAV2 join absent → exact one-hop owner work and join | Private/inherited; Router does not do owner work | Operational `OP-013`, `DEF-OP-001`; `arcanum/arcana/continuation-router/SKILL.md` |
| `REL-021` | Action contract → dispatch receipt / coordinates | Dispatch Spec owner → Orchestrate owner | Current coordination route; action-ID workaround residue → confirm, uniquely identify, spawn, join, gate, close | Private operations; no task semantics or authority | Operational `OP-006`; current `dispatch-sheet.json`; `native-run/run-01/reviewer-zig-zag-loop-01.json` |
| `REL-022` | Canonical capability → generated package / transforms | Canonical owner → generator | Generator exists; drift observed → generate and diff exact package | Public→generated local; generated is not canonical | Operational `OP-011`, `OP-021..022`; `arcanum/tools/sync-generated-skill-package.sh`; frozen Arcanum commit `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295` |
| `REL-023` | Staged package → host projection / synchronizes | Generator → sync owner | Sync route exists; repair unexecuted → explicit apply, checksum, rollback | Generated local; no install/runtime | Operational `OP-011`; `arcanum/tools/sync-generated-skill-package.sh` |
| `REL-024` | Synchronized package → consumer / installs | Sync owner → install owner | Install sources exist; no exact CAV2 receipt → explicit install and identity check | Local consumer; availability only | Operational `OP-012`; `arcanum/tools/bootstrap_arcanum.sh`, `arcanum/tools/install_arcanum.sh` |
| `REL-025` | Installed capability → behavior receipt / exercises | Install owner → acceptance owner | No exact CAV2 witness → behavioral acceptance on installed identity | Local runtime; behavior is not canonicality or release | Operational `OP-012`, `DEF-OP-009`; same install sources, but no CAV2 receipt |
| `REL-026` | Accepted implementation → release / requests release | Artifact owner → release owner | Candidate policy template; no witness → decision, package, receipt | Inherited; acceptance is not release | Operational `OP-014`; `authority/promotion-policy.md:3-6,20-29` |
| `REL-027` | Release → environment / deploys | Release owner → deployment owner | No witness → deployment authorization and health evidence | Inherited, no declassification; release is not deployment | Systems `EDGE-010`, `CEIL-001..002`; `README.md#repository-objective` |
| `REL-028` | Approved extract → public owner/surface / publishes | Private/boundary owners → public owner/publisher | Normative boundary; no leakage witness → scrub, reviews, decision, mutation, verification | Private→public only after approval; naming is not publication | Authority `AUTH-012`; systems `EDGE-008`; `authority/boundaries.md:6-14,58-65`, CAV2-C5 `STABLE-REPOSITORY-CONSTITUTION.md:85-99` |
| `REL-029` | Typed residue → named owner / hands off | Gap owner → residue owner | Used as research routing → preserve gap, ceiling, and route | Inherited; no authorization or blocker inflation | Authority explorer residue; operational `RES-OP-001..012`; systems `RES-001..006` |

## 4. Structural instantiation and import crosswalk

| Public or external source | CAV2 treatment | Required local owner transition | Current proof and first stop |
|---|---|---|---|
| Arcanum definitions | Reference upstream IDs; define only distinct `CAV2-D*` terms locally | Per-term classify as `reference`, `local-adaptation`, or `already-owned-skip`, then use definitions-governance if a local load-bearing term is needed | The 2026-06-19 149-candidate ledger is candidate-only and stale relative to later Arcanum definition changes through `b280678e28baf1ae6abcc9ec2d7072388fa3bc85`; no current per-term map. [Authority `AUTH-004`; `authority/imports/definitions/MANIFEST.md:3-5,37-43,237-251`, `arcanum/definitions/DEFINITIONS.md:3-16`.]
| Arcanum constitutions | Stage public patterns, preserve provenance, extract the smallest CAV2-local rule | Constitution governance decides the local rule before implementation admission | Manifest appendix says the old scan is stale, tooling was unstaged, and zero old candidates were extracted; no locally admitted import witness. [Authority `AUTH-005..007`; `authority/imports/constitutions/MANIFEST.md:159-166`, CAV2-C11 `STABLE-REPOSITORY-CONSTITUTION.md:177-203`.]
| Artifact schema form | Import the canonical `.schema.yml` form rule as a candidate local rule | Constitution governance first; Task Session only after semantic admission | `arcanum/framework/SCHEMA-CONSTITUTION.md:3-10` is canonical upstream; CAV2 `PLAN.md:1-33` is committed, candidate, intended-not-shipped, and non-executed. No local constitution was found. [Authority `AUTH-006`; operational `OP-015..016`; plan commit `fad671aed4ebf6c1405e4264a40d14e3ee33e740`.]
| Artifact validator | Adapt Arcanum-root predicates into a narrowly owned CAV2 form checker; do not copy wholesale | After local rule admission, Task Session may implement and validation may report bounded conformance | Upstream `validate-artifact-constitution.sh:169-181` checks suffix form, not YAML content. Its self-test uses `.schema.json` as bad and `.schema.yml` as good (`:233-246,276-289`). CAV2’s requested “bad `.schema.yml`” has no owned discriminating rule. [Authority `AUTH-006`; operational `OP-016`, `DEF-OP-006`; precedent reviewer `PRECEDENT-004`.]
| Artifact metadata | Keep separate from Tier-1 form unless explicitly admitted | Decision Gate/metadata semantic owner before implementation | CAV2 `PLAN.md:33` defers metadata, but upstream validator hard-requires and invokes its metadata parser (`validate-artifact-constitution.sh:347-353,391-403`) while `ARTIFACT-METADATA-CONSTITUTION.md:3-5,108-114,168-176` is candidate. The planned L2 boundary is defective as written. [Authority `AUTH-006`; operational `DEF-OP-007`; precedent `PRECEDENT-005`.]
| Arcanum disciplines and governance patterns | Reference or locally instantiate a practice card without inheriting maturity | Discipline governance owns local state; the public discipline owner retains upstream semantics | Upstream artifact statuses must remain per-file: schema canonical; metadata, gitignore, and markdown-linking candidate; inspected `ARTIFACT-CONSTITUTION.md` has no top-level lifecycle declaration. Ownership does not flatten status. [Authority `AUTH-003`; operational `OP-022`; `SCHEMA-CONSTITUTION.md:3-5`, `ARTIFACT-METADATA-CONSTITUTION.md:3-5`, `GITIGNORE-CONSTITUTION.md:3-5`, `MARKDOWN-LINKING-CONSTITUTION.md:1-7`.]
| Ontology method | Use public method to map private owner-accepted state and prepare owner-facing requests | Ontology route plus the exact source owner decides any source change | CAV2 ontology remains candidate and cannot emit authority-writing projections. Current Arcanum Ontology Vault wording inspected by the explorer was dirty-current, not commit-bound. [Authority `AUTH-008`; `ontology/README.md:3-31`, `ontology/projections/README.md:6-19,37-57`, `arcanum/arcana/ontology-vault/SKILL.md:123-126,274-305`.]
| Generated host skills | Transform only accepted canonical Arcanum packages, then separately sync, install, and behavior-test | Canonical owner → generator → sync owner → install owner → acceptance owner | Drift is observed, and no exact CAV2 generate→sync→install→behavior chain exists. [Operational `OP-011..012`, `OP-021..022`; `arcanum/tools/sync-generated-skill-package.sh`, frozen Arcanum commit `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`.]

The artifact seam is thus a **verified staged-import and planned-adaptation precedent**, not a verified adapter. The legal positive route is `REL-004 → REL-006 → exactly one named semantic owner in REL-007..012`; a found owner changes the basis to build-from-owned but does not kill legitimate adaptation work. [Authority `AUTH-006..007`; sources: CAV2-C17 `STABLE-REPOSITORY-CONSTITUTION.md:371-398`, artifact findings `development/research/2026-07-01-arcanum-artifact-governance-import/findings.md:41-86`.]

## 5. Evidence, promotion, and control flows

There is no single generic “plan → implementation → validation → promotion” flow. The legal order depends on the artifact kind:

1. **Authority promotion:** `REL-004 → REL-006 → exactly one of REL-007..012`. The named definitions, constitution, discipline, decision, spec, or runtime-contract semantic owner decides and mutates its canonical owner artifact. [Authority `AUTH-002..010`; `AUTHORITY-MODEL.md:23-29,48-72,90-103,122-133`.]
2. **Candidate prototype:** `REL-005 → explicit non-governing scope → REL-013 → REL-014 → REL-015`. The result remains candidate evidence; a pass does not promote it. [Operational `OP-003..004`, `OP-009`, `TRACE-OP-POS-001`; typed-test-recovery fast-lane receipt identified in section 9.]
3. **Governing implementation:** an already accepted `REL-007..012` artifact constrains `REL-013`, followed by `REL-014`. Task Session executes the admitted meaning; it does not own that meaning. [Operational `OP-004`, `OP-014`; `arcanum/arcana/task-session/SKILL.md`.]
4. **Runtime availability:** `REL-022 → REL-023 → REL-024 → REL-025`. Generation, synchronization, installation, and behavioral acceptance each require an exact witness. [Operational `OP-011..012`; `arcanum/tools/sync-generated-skill-package.sh`, `bootstrap_arcanum.sh`, `install_arcanum.sh`.]
5. **Availability beyond the repository:** accepted implementation may request `REL-026`; release must separately pass `REL-027` for deployment or `REL-028` for public extraction/publication. No one transition proves another. [Authority `AUTH-012`; systems `EDGE-010`, `CEIL-001..002`; `authority/boundaries.md:58-65`.]

The control rule is: the **named narrow owner decides**, the canonical owner artifact records accepted normative state, ledgers record evidence/events, ontology projects relations, Inventory supports discovery, validators report bounded conformance, observers report signals, and orchestration coordinates agents. No evidence surface is allowed to impersonate its consumer. [Authority `AUTH-010`; operational `OP-005..010`, `OP-014`; `authority/AUTHORITY-MODEL.md:122-133`, `ontology/projections/README.md:12-19`.]

## 6. Invoke, Task Session, Craft, Dispatch, Inventory, ontology, validation, observability, and runtime integration

| Surface | Verified participation | First stop / non-effect | Proof binding |
|---|---|---|---|
| Invoke | Authors and validates candidate Define/Design/Plan packages and bounded handoffs | Its receipt neither authorizes mutation nor promotes meaning | Operational `OP-003`; `arcanum/spells/invoke/README.md`, `arcanum/spells/invoke/plan.md` |
| Task Session | Admits and executes one frozen bounded unit after semantic/prototype ownership is established; critical validation and closeout remain explicit | Cannot own a runtime contract, promote authority, release, or deploy; full CAV2 Invoke→Refresh join is absent | Operational `OP-004`, `DEF-OP-001`; `arcanum/arcana/task-session/SKILL.md` |
| Craft | Maintains `.craft/ledger.yml` and derives `CRAFT.md`/`.craft/index.json` for coordination and navigation | Cannot make a plan executable, create an owner receipt, reinterpret a verdict, or synchronize deferred governance | Operational `OP-005`, `OP-018`; sampled files at commit `32ee3c2c5a8e1c9f43f34017549cf1bea4fcf539` |
| Dispatch Spec / Orchestrate | Validates a confirmed action graph and coordinates spawn, join, gates, and closeout | Coordination receipt is not task-semantic completion or authority; this run required an action-ID remap | Operational `OP-006`, `DEF-OP-008`; `dispatch-sheet.json`, `reviewer-zig-zag-loop-01.json` |
| Inventory | Parent index supports discovery; CAV2 owns a read-model boundary but has no machine index | Caller must rebind to a direct owner; Inventory cannot select or promote | Operational `OP-007`, `OP-019`; `inventory/README.md:3-11` |
| Ontology Vault / projections | Maps candidate structure and routes a proposal to the source owner | Cannot mutate canonical sources, issue promotion verdicts, or prove runtime conformance | Authority `AUTH-008..010`; operational `OP-008`; `ontology/README.md:3-31`, `ontology/projections/README.md:6-19,37-57` |
| Validation | Checks exact contracts/fixtures/bytes and emits bounded results for named owners | A pass cannot promote, release, deploy, or generalize across mixed baselines; a failed/unrun critical check stops its declared route | Operational `OP-009`, `OP-014`, `DEF-OP-006`; trace receipts in section 9 |
| Observability | Samples invocation envelopes/results and may feed later reflection | Sampled authority effect is `none`; signals cannot authorize source maintenance | Operational `OP-010`; `arcanum/arcana/signal-observer/SKILL.md` |
| Continuation Router / Refresh | Validates a one-hop prerequisite route and joins an actual owner-issued receipt | Router does not do the owner’s work; a complete real CAV2 join is absent | Operational `OP-013`, `DEF-OP-001`; `arcanum/arcana/continuation-router/SKILL.md` |
| Generated packages | Project accepted canonical capability packages into host formats | Current drift blocks parity; generated bytes are not canonical | Operational `OP-011`, `OP-021..022`; `arcanum/tools/sync-generated-skill-package.sh` |
| Bootstrap/install/runtime | Could select, install, identify, and behavior-test an accepted capability | No exact CAV2 receipt proves canonical→generate→sync→install→behavior; private tests cannot substitute for a missing public owner | Operational `OP-012`, `OP-017`, `DEF-OP-009`; `bootstrap_arcanum.sh`, `install_arcanum.sh` |

The overall operational verdict is therefore a collection of bounded seams, not one integrated runtime. The strongest recent positive execution evidence intentionally stops at candidate-local validation and defers lifecycle reconciliation; the strongest committed negative trace proves fail-closed behavior at a missing external owner receipt. [Operational explorer `OP-001..002`, `TRACE-OP-POS-001`, `TRACE-OP-NEG-001`; return `agent-final://cav2_operational_explorer/spawn-0002`.]

## 7. Public/private and canonical/generated boundary

| Boundary | Allowed direction | Required gates | Forbidden inference |
|---|---|---|---|
| Public Arcanum → private CAV2 | Reference, stage, or locally adapt | Pin source and lifecycle status; scrub Arcanum-specific bindings; name the CAV2 owner; admit a distinct local artifact | Proximity, copying, or a manifest row does not transfer authority. [Authority `AUTH-003..006`; `SOURCE-MAP.md:8-21`.]
| Private CAV2/DomainSpec → public Arcanum | Only an explicitly approved public-safe extract | Boundary scrub, private source-owner review, contested-disclosure decision where needed, public owner mutation, verification | Naming Saturn/DomainSpec or summarizing them does not authorize private prose/code publication. [Authority `AUTH-012`; `authority/boundaries.md:6-14,58-65`.]
| Canonical Arcanum → generated host package | Deterministic transformation of an accepted canonical package | Generate, diff, checksum, explicit synchronization authority | Generated projection is not canonical and cannot repair its own drift. [Operational `OP-011`, `OP-021..022`; `sync-generated-skill-package.sh`.]
| Generated package → installed behavior | Explicit sync, installation identity check, then behavioral acceptance | Separate receipts for sync, install, and behavior on the frozen identity | Presence or installation is availability only; behavior is not canonicality, promotion, release, or deployment. [Operational `OP-012`; `bootstrap_arcanum.sh`, `install_arcanum.sh`.]
| Source/evidence → Inventory/ontology/Craft | Derive a private discovery/projection/coordination view | Preserve source identity, owner, state, privacy, and direct-source rebind | A view cannot select, decide, promote, declassify, or substitute for an owner. [Authority `AUTH-008..010`; operational `OP-005`, `OP-007..008`.]

The report found no safe basis for calling CAV2 public, standalone, meta-authority, a shipped System-5, an exported mold, or an installed runtime adapter. It also found no safe basis for calling DomainSpec or Saturn shipped. [Systems explorer `H-BASE-001`, `H-META-001`, `H-S5-001`, `H-MOLD-001`, `CEIL-001..002`; sources: `README.md#repository-objective`, `arcanum/docs/saturn.html#loop`.]

## 8. Current versus committed, dirty, candidate, intended, deployed, and absent status

| Proof class | What is actually supported | What it does not support |
|---|---|---|
| `direct-source-observed` / current | CAV2 README, Source Map, authority model, owner surfaces, boundary rules, ontology/read-model contracts, and current Arcanum contracts were inspected | Current text alone does not prove its workflow executed, its bootstrap authority valid, or its generated consumers in parity. [Authority `AUTH-001..012`; operational `OP-020`.]
| `committed-unexecuted` | The artifact-governance Define/Design/Plan exists; latest plan-touch commit `fad671aed4ebf6c1405e4264a40d14e3ee33e740` | No local constitutions, validator port, hook wiring, promotion, or enforcement. [Operational `OP-015..016`; `PLAN.md:1-44`.]
| `historical-executed` / committed | The IOLM block receipt proves a past fail-closed route at commit `3c12cc0f39a16e95751e7be6a6d108a2fc21060a`; Craft samples are committed at `32ee3c2c5a8e1c9f43f34017549cf1bea4fcf539` | Not current upstream compiler behavior and not resolution of the blocker. [Operational `TRACE-OP-NEG-001`, `OP-018`.]
| `dirty-worktree-only` | The typed-test-recovery package and receipts report candidate-local recovery checks; current canonical/generated Arcanum and some CAV2 implementation bytes are dirty or untracked | Stored postimages do not prove current bytes; untracked receipts are not immutable history; no unattributed write is adopted. [Operational `TRACE-OP-POS-001`, `OP-020`, `DEF-OP-010`.]
| `generated` | Host projections and generation/sync routes exist; exact discipline-governance and WPRA divergence was recorded | Generated source is not canonical; parity, synchronization, installation, or behavior is not inferred. [Operational `OP-011`, `OP-021..022`; `sync-generated-skill-package.sh`.]
| `candidate` | Stable Repository Constitution status, disciplines, promotion policy, ontology projections, authority-object proposal, CAV2-C17, and multiple imports remain candidate | No uniform active authority, mandatory ontology edge, promoted constitution, or canonical enforcement. [Authority `AUTH-005..009`; direct selectors in sections 3–4.]
| `intended-not-shipped` | Saturn convergence, the artifact import implementation, CAV2 standalone base, and downstream mold are goals or plans | No shipped loop, adapter, base, or downstream cast. [Authority `AUTH-001`, `AUTH-006`, `AUTH-011`; systems `EDGE-003`, `EDGE-010`.]
| Active local declaration; promotion history not reconstructed | CAV2’s authority model and definition source declare themselves active; the decision surface is active, with record-specific outcomes | No movement receipt reconstructed their promotion, and the declaration is not uniform across authority kinds, cross-repository authority, independent bootstrap proof, or implementation. [Authority `AUTH-002`; sources in `STAT-01..03`.]
| `deployed` | None established in this research | Repository bytes, docs, generated packages, release candidates, or old tests are not deployment. [Operational proof taxonomy and `OP-012`; systems `CEIL-001..002`.]
| `absent` / `unverified` | No local machine Inventory index, implemented CAV2 artifact validator/hooks, locally admitted import witness, complete Invoke→Refresh witness, end-to-end runtime chain, release, deployment, or publication witness | Absence is an evidence ceiling and owner-routed residue, not proof that future authorized work is impossible. [Operational `OP-019`, `DEF-OP-001..009`; synthesis absence classes in section 9.]

The old definition and constitution scans are directly observed in the current private working tree as historical 2026-06-19 snapshots with a later stale-state appendix. They prove staleness and incompleteness, not current per-item coverage or local adoption. No later comprehensive pinned rescan was found. [Authority `AUTH-004..006`; systems `CON-003`; `authority/imports/constitutions/MANIFEST.md#re-scan-2026-07-01`.]

## 9. Finite positive and negative traces

### `TRACE-OP-POS-001` — candidate-local recovery evidence without promotion

- **Input/artifacts:** `development/ontology-evidence-workbench-typed-test-recovery/INVOKE-RECEIPT.json`, `planning/SWU-MANIFEST.json`, fast-lane receipt `planning/work-pack/session-evidence/FAST-LANE/20260803T222716Z/receipt.json`, digest `db0713d9993ef7c0cf17dcc9b3a45d582ae3355751f8f1f87c2597a515645204`, Handoff Notice `HN-7362EC2F08B7`.
- **Ordered gates:** Invoke → design fixed point → Dispatch/Distill validation → explicit candidate-local fast-lane scope → `V-OEWFR-01..13` plus 25 reported tests → consolidated receipt → Handoff Notice owner.
- **First stop:** candidate-local validation before lifecycle reconciliation.
- **Forbidden effects:** generalized build, browser acceptance, promotion, synchronized lifecycle, retry authority, release, deployment, production.
- **Proof:** private, untracked, dirty-worktree-only, candidate-local; stored postimages do not prove current bytes. [Operational explorer `TRACE-OP-POS-001`, `OP-020`; return `agent-final://cav2_operational_explorer/spawn-0002`.]

### `TRACE-OP-NEG-001` — missing external support stops execution

- **Input/artifacts:** `development/interactive-ontology-learning-map/work-pack/session-evidence/SWU-IOLM-00C-B/execution-receipt.json`, `DECISION-GATE.md`, blocker `BLK-DSV2-BTE-SWU-READINESS-CONTRADICTION-001`.
- **Ordered gates:** selected IOLM unit → DomainSpec/compiler owner → Decision Gate option 1 → regression confirms `CROSS_FEATURE_UNSUPPORTED` → missing owner-issued support receipt → Task Session block → Craft record.
- **First stop:** absent upstream support receipt plus contradictory SWU readiness.
- **Forbidden effects:** guessed capability, prototype mutation, successor execution, treating a passing blocker regression as support, any authority effect.
- **Proof:** committed historical execution at `3c12cc0f39a16e95751e7be6a6d108a2fc21060a`; not proof of current upstream behavior. [Operational explorer `TRACE-OP-NEG-001`.]

### `TRACE-AUTHOBJ-001` — authority candidate stops before ontology amendment

- **Input:** `ontology/promotion-requests/2026-06-23-authority-object-schema-proposal.md:1-18,98-111`.
- **Ordered gates:** Invoke proposal → ontology owner amendment of `NODE-MODEL.md` → Decision Gate stabilization → named semantic owner → later Task Session validator.
- **First stop:** the proposal explicitly says it does not amend `NODE-MODEL`.
- **Forbidden effects:** amendment, stabilization, mandatory edge, emitted node, validator, promotion.
- **Proof:** private, direct-current, candidate, non-executed. It is a compliant stop, **not** an attempted self-promotion rejection. [Authority explorer `AUTH-009`; return `agent-return://2026-08-05-arcanum-cav2-integration-research/cav2-integration-run-01/spawn-0001/explorer-authority`.]

### `TRACE-IMPORT-STALE-001` — stale import coverage stops admission

- **Input:** constitution-manifest 2026-06-19 snapshot.
- **Ordered gates:** freshness check → 2026-07-01 appendix declares stale → unstaged documents/tooling and zero old extracted candidates → no comprehensive pinned rescan.
- **First stop:** current-coverage gate.
- **Forbidden effects:** current coverage, per-item owner map, local admission, implementation, enforcement.
- **Proof:** current private worktree directly records a historical scan and later stale determination. [Authority `AUTH-005..006`; systems `CON-003`; `authority/imports/constitutions/MANIFEST.md:159-166`.]

### `TRACE-GEN-DRIFT-001` — generated parity stops runtime inference

- **Input:** canonical discipline-governance `0.2.2` versus generated `0.2.1`; canonical WPRA hash `4a5ce7d8…` versus generated `a013a971…`.
- **Ordered gates:** canonical acceptance → generation → parity divergence → explicit sync authority → later install and behavioral acceptance.
- **First stop:** parity/synchronization; no repair executed.
- **Forbidden effects:** canonicality, sync, install, behavior, promotion, release, deployment.
- **Proof:** finite drift only. [Operational explorer `OP-011`, `OP-021..022`; generation route `arcanum/tools/sync-generated-skill-package.sh`; Arcanum snapshot `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`.]

### Required absences and non-witness classifications

| Classification | Why it is not a finite witness / enforced ceiling |
|---|---|
| `NO_LOCALLY_ADMITTED_IMPORT_WITNESS` | Artifact seam stops before local constitution promotion, tool implementation, and hook wiring. [Authority `AUTH-006`; operational `OP-015..016`.]
| `NO_PRIVATE_TO_PUBLIC_LEAKAGE_WITNESS` | The boundary route is normative; no specific rejected-leakage input and owner refusal were bound. [Authority `AUTH-012`; `authority/boundaries.md:58-65`.]
| `NO_FROZEN_FAILED_CRITICAL_VALIDATION_WITNESS` | Reports that full validation is red disagree and lack one frozen input, exact command/result, criticality owner, and receipt. The passing IOLM regression confirms a blocker and is not a failed-critical-validation witness. [Operational `DEF-OP-006`; non-vacuity reviewer `NV-10`.]
| `NO_ONTOLOGY_SELF_PROMOTION_REJECTION_WITNESS` | `TRACE-AUTHOBJ-001` stops compliantly before amendment; it does not record an attempted self-promotion and rejection. [Authority `AUTH-009`.]
| `NO_GENERATED_PROJECTION_AUTHORITY_WITNESS` | `TRACE-GEN-DRIFT-001` proves divergence only, not an attempted authority assertion. [Operational `OP-011`.]
| `NO_END_TO_END_RUNTIME_WITNESS` | No exact canonical→generate→sync→install→behavior chain is bound for CAV2. [Operational `OP-012`, `DEF-OP-009`.]
| `NO_RELEASE_DEPLOYMENT_PUBLICATION_WITNESS` | No exact artifact crosses any of these three separate transitions. [Systems `EDGE-010`, `CEIL-001..002`.]
| `NO_INVENTORY_PROMOTION_OR_MISSING_OWNER_WITNESS` | Explorer `OP-017` summarized an untracked intent-router Inventory result, but did not preserve its exact artifact path. The proposed stop—missing canonical public owner—and forbidden generation, Bootstrap, install, adapter, release, and deployment effects are credible absence evidence, not a finitely bound trace. [Operational `OP-017`; zig-zag-2 normalization in `synthesis-revision-1.md`.]

These absences are research residue and proof ceilings, not execution blockers and not permission to fill the gaps without their named owners.

## 10. Conflicts, duplication, stale imports, bugs, and missing links

1. **Mixed authority states:** CAV2’s active authority model does not make candidate constitutions, disciplines, policy, or ontology active canon. `STAT-04` remains an owner decision. [Authority `AUTH-002`, `AUTH-005`; sources in section 3.]
2. **Stale import coverage:** definition and constitution ledgers are old, heterogeneous, and candidate-only; Arcanum definitions changed after the scan. Current per-item ownership/adoption cannot be claimed. [Authority `AUTH-004..006`; commit `b280678e28baf1ae6abcc9ec2d7072388fa3bc85`.]
3. **Duplicate-owner risk:** importing an already-owned promotion, hygiene, definition, constitution, or discipline rule would create parallel authority. Build-from-owned requires reference or scoped adaptation, not re-promotion. [Authority `AUTH-007`; CAV2-C17 `STABLE-REPOSITORY-CONSTITUTION.md:371-398`.]
4. **Artifact witness defect:** the planned “bad `.schema.yml`” case is non-discriminating because the upstream validator checks suffix, not YAML content. Constitution Governance must either test an owned extension failure such as `.schema.json`, or first promote content semantics and fixtures. [Authority `AUTH-006`; operational `DEF-OP-006`; `validate-artifact-constitution.sh:169-181,233-246,276-289`.]
5. **Form/metadata layer leak:** planned Tier-1 form enforcement invokes candidate Tier-2 metadata machinery. The adapter must exclude that dependency or separately admit metadata first. [Operational `DEF-OP-007`; `PLAN.md:33`, validator `:347-353,391-403`, metadata constitution `:3-5,108-114,168-176`.]
6. **Runtime semantic-owner wording:** Task Session is an execution route, not the owner or promoter of a runtime contract. A named semantic owner and any required Decision Gate must precede it. [Authority `AUTH-002`; operational `OP-004`; `AUTHORITY-MODEL.md:48-72,90-103`.]
7. **No complete positive lifecycle witness:** no exact Invoke output is bound through selection, context, admission, execution, critical validation, real Refresh-owner join, synchronized result, and continuity cursor. [Operational `DEF-OP-001..002`.]
8. **Canonical/generated drift:** current canonical and generated Arcanum surfaces diverge, so source inspection cannot establish consumer runtime behavior. [Operational `DEF-OP-003`, `OP-021..022`.]
9. **Inventory gap:** CAV2 owns an exported read-model boundary, but `inventory/README.md` is its only local Inventory file; there is no machine index. [Operational `OP-019`; direct executed diagnostic recorded in the explorer return.]
10. **Dirty postimages:** user-owned modified/untracked CAV2 and Arcanum bytes cannot be attributed, adopted, promoted, or generalized from older receipts. [Operational `OP-020`, `DEF-OP-010`; systems `CON-004`.]
11. **Orchestration residue `ORCH-RES-001`:** the stock reducer reused reviewer action IDs `spawn-0002..0004`; before spawn, the run applied a semantic-neutral remap to `spawn-0005..0007`. Prompts and verdicts did not change. This is a run-local workaround, not a canonical allocator repair. [Operational `OP-006`, `DEF-OP-008`; `native-run/run-01/reviewer-zig-zag-loop-01.json`.]
12. **History residue:** broader history traversal was limited by malformed `refs/codex/turn-diffs/...`; no stronger history claim is warranted until the Git-maintenance owner repairs it. [Systems explorer `CEIL-003`, `RES-006`; observed Arcanum HEAD `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`.]
13. **Stale documentation claim:** a prior layer map said deployed Arcanum docs did not mention Saturn/DomainSpec, while current source bytes do; those bytes still describe Saturn as under construction and do not prove live publication or a closed loop. [Systems `CON-002`; `arcanum/docs/index.html:489-506`, `arcanum/docs/saturn.html`.]

## 11. Owner-routed operator playbooks

### Admit one Arcanum pattern into CAV2

1. CAV2 import owner pins the exact Arcanum path, commit, upstream lifecycle status, privacy posture, and intended local owner.
2. Definitions or Constitution Governance classifies it as `reference`, `local-adaptation`, or `already-owned-skip`; stale manifests are rescanned first.
3. The narrow semantic owner strips Arcanum-root bindings and proposes the smallest local artifact with provenance, scope, examples, non-examples, and validation mode.
4. Decision Gate resolves contested content or disclosure; the owner mutates the canonical local artifact only after acceptance.
5. Task Session may then implement a bounded adapter; validation uses an owned discriminating fixture on frozen bytes.
6. Results return as evidence only. Promotion, generation, sync, install, release, deploy, and publication remain separate owner transitions. [Authority `AUTH-003..007`; operational `OP-015..016`; `SOURCE-MAP.md:8-21`, CAV2-C11 `STABLE-REPOSITORY-CONSTITUTION.md:177-203`.]

For the current artifact plan, Constitution Governance must first resolve schema form and the `STAT-04` status, replace the malformed-`.schema.yml` witness with an owned extension failure or first admit YAML-content semantics, and keep metadata out of Tier 1 unless separately accepted. Only then may Task Session own the planned validator/hook implementation. [Authority `AUTH-006`; operational `DEF-OP-005..007`; validator selectors in section 10.]

### Move a CAV2 authority candidate toward implementation

1. Invoke may author a candidate but records `authority_effect: none`.
2. Route the candidate to exactly one semantic owner: definitions, constitution, discipline, decision, spec, runtime contract, or source-owned ontology change.
3. If accepted, mutate the canonical owner artifact and preserve an immutable decision/movement record.
4. Only then admit governing implementation through Task Session; or explicitly label a pre-promotion prototype as non-governing candidate evidence.
5. Run bounded validation; the named owner interprets the result. Craft records references, ontology projects accepted state, and Inventory supports later discovery without changing the verdict. [Authority `AUTH-002`, `AUTH-008..010`; operational `OP-003..005`, `OP-007..009`, `OP-014`.]

For the authority-object proposal, the next owner is the ontology route for `NODE-MODEL.md`, then Decision Gate for stabilization, then Task Session for a validator. The current proposal must not be described as an amendment, emitted node, mandatory edge, or rejection witness. [Authority `AUTH-009`; proposal `:1-18,98-111`.]

### Establish a real CAV2 runtime integration

1. Arcanum canonical owner accepts the exact capability at a pinned clean commit.
2. Generator produces the host package; sync owner diffs, checksums, applies, and preserves rollback.
3. Install owner installs the exact identity into the intended CAV2 consumer.
4. Acceptance owner runs behavioral tests against that installed identity.
5. Only separate release, deployment, or publication owners may cross those later boundaries. A missing step yields residue, never inferred parity. [Operational `OP-011..013`, `DEF-OP-003`, `DEF-OP-009`; `sync-generated-skill-package.sh`, `bootstrap_arcanum.sh`, `install_arcanum.sh`.]

### Close the operational and indexing gaps

- Task Session/Refresh owners: freeze one exact positive Invoke→selection→admission→execution→critical-validation→owner-join→synchronized-result witness.
- Handoff Notice owner: reconcile `HN-7362EC2F08B7` without retroactively promoting candidate-local evidence.
- Inventory owner: decide whether CAV2 will build a local machine index or explicitly continue consuming the parent read model.
- Generation/runtime owners: restore or reject parity, then produce exact install and behavior receipts.
- Dispatch/Orchestrate maintainer: repair action-ID allocation and exact-input/correlation evidence.
- Git-maintenance owner: repair the malformed ref before extending history-sensitive claims. [Operational `RES-OP-001..008`; systems `RES-004..006`.]

## 12. Verdict, hypothesis dispositions, residue, and next owners

### Verdict

**Qualified integration only.** CAV2 is a verified private consolidation surface and documentary/import consumer of public Arcanum. It has verified adaptation seams, owner routes, committed plans, bounded candidate execution evidence, and fail-closed precedents. It is not proved to have a locally admitted Arcanum import, implemented CAV2 adapter, installed generated package, end-to-end runtime integration, synchronized full lifecycle, release, deployment, publication chain, standalone base, System-5 controller, or downstream mold.

This verdict passed the revised precedent, non-vacuity, and definitional-soundness gates under `synthesis-zig-zag-01`. Passing the research gate means the claims are correctly bounded; it does not erase the explicit non-witnesses or create any authority effect. [Review loop: `native-run/run-01/reviewer-zig-zag-loop-01.json`; reviewer-owned passes: `reviews/precedent-revision-1.md`, `reviews/non-vacuity-revision-1.md`, `reviews/definitional-revision-1.md`; closure: `receipts/evidence-closure.json`.]

### Hypothesis dispositions

| ID | Disposition | Boundary |
|---|---|---|
| `H-CONSUMER-001` | **Qualified verified** | Documentary/import consumption of sources, methods, and candidates only; no installed/runtime consumption proved. [Authority `AUTH-011`; operational `OP-001..002`; `README.md:8-16`, `SOURCE-MAP.md:10-21`.]
| Adapter description | **Planned, not implemented** | Verified seams require re-rooted adaptation; no CAV2 adapter implementation/runtime receipt. [Authority `AUTH-006`; operational `OP-015..016`; plan commit `fad671aed4ebf6c1405e4264a40d14e3ee33e740`.]
| `H-CONSOLIDATION-001` | **Verified** | CAV2 consolidates source-ledgered evidence without absorbing source ownership. [Authority `AUTH-001`, `AUTH-011`; systems `SYS-001`; `README.md:8-16`.]
| `H-SPINE-001` | **Bounded architectural descriptor** | Private CAV2-local routing arrangement, not a promoted authority kind, workspace apex, standalone status, or public framework. [Authority `AUTH-002`, `AUTH-011`; systems `SYS-001`; `AUTHORITY-MODEL.md:23-29,122-133`.]
| `H-BASE-001` | **Intended only** | Repository objective requires later owner-reviewed extraction; no executed transition. [Authority `AUTH-001`; systems `EDGE-010`; `README.md:36-47`.]
| `H-META-001` | **Contradicted as current fact** | CAV2 authority is local and cannot automatically govern Arcanum, DomainSpec, or Saturn. [Systems `SYS-001`, `H-META-001`; `AUTHORITY-MODEL.md#non-collapse-rules`.]
| `H-S5-001` | **Analogy only** | No owner-routed edge makes CAV2 a shipped System-5 controller of the system-work recursion. [Systems `H-S5-001`, `FB-003`.]
| `H-MOLD-001` | **Method metaphor/intention only** | No exported enforced mold or downstream casts are proved. [Authority `AUTH-011`; systems `H-MOLD-001`; `README.md#repository-objective`.]

### Residue and next owners

| Residue | Next owner | Required evidence before stronger claim |
|---|---|---|
| Resolve `STAT-04` and whether CAV2-C17 becomes deterministic | Constitution Governance + Decision Gate | Owner decision, canonical mutation, validation record |
| Refresh definition and constitution import coverage | Definitions Governance + Constitution Governance/import owner | Pinned Arcanum commit; per-item source/status/owner/posture records |
| Repair artifact form/content/metadata boundaries | Constitution Governance, metadata semantic owner, then Task Session | Owned rule and discriminating fixture; separately admitted metadata if used |
| Correct runtime-contract ownership language | Named runtime-contract/spec/capability semantic owner | Accepted canonical contract before Task Session admission |
| Complete one clean lifecycle witness | Invoke, Task Session, prerequisite owner, Refresh/closeout owner | Frozen exact chain through synchronized result and continuity cursor |
| Reconcile candidate-local recovery | Handoff Notice `HN-7362EC2F08B7` owner | Current-byte baseline and explicit lifecycle receipt without retroactive promotion |
| Decide CAV2 Inventory indexing | CAV2 Inventory owner | Local machine-index contract and validation, or explicit parent-index dependency decision |
| Restore generated parity and runtime proof | Arcanum canonical owner, generator, sync, install, acceptance owners | Exact generate/diff/sync/install/behavior receipts |
| Repair dispatch allocator/correlation | Dispatch Spec/Orchestrate maintainer | Canonical allocator fix and regression witness; run-local remap is insufficient |
| Repair malformed Git reference | Repository Git-maintenance owner | Clean history traversal before broader history claims |
| Decide any standalone/public extraction | Private source/boundary owners, Decision Gate, public owner/publisher | Scrub, approvals, public mutation, verification; no leakage witness currently exists |
| Keep ontology and Inventory non-authoritative | Ontology route + every projected source owner | Consequential projections preserve source owner/state/privacy and prove no write effect |

Final residue is deliberate: no meta-authority, uniform active authority, System-5 controller, standalone extraction, implemented adapter, locally admitted import, complete runtime chain, release, deployment, publication, or downstream mold is proved. Those are proof ceilings and owner-routed next questions—not hidden completions, automatic blockers, or authorization for further mutation.
