# Mint improvement audit — explorer returns

These are mechanically preserved, non-authoritative research returns. They do not establish implementation, authority, promotion, publication, deployment, release, shipment, production readiness, or Inventory authority.

## Agent 1 — current state and reliability

## SUBSTANTIVE RETURN

### Plain-language finding

Mint has a substantial, evidence-backed design and template corpus, but it is not a callable or recoverable repository generator. Its current installed “runtime” is an agent instruction file plus Markdown templates. The declared L0 scaffolder is absent, authority-triage is source-only and contractually classifies/routes rather than emits, and there is no executable Mint plan/apply/check/resume path.

The strongest current bytes are the 21 templates and `EMIT-PROCEDURE.md`; two historical smoke reports say agents instantiated them successfully in scratch space. Those scratch outputs are not persisted, while the checked-in `release-approval` example contains only the older core surface and fails the expanded checks by absence.

Mint’s L2 blocker is also misclassified. Attestation L1 is built, and its checked-in seal executed `valid` against the current decision bytes. Mint has not integrated it. Thus the current block is Mint integration and owner-act wiring, not absence of the L1 capability. External actor-identity signing remains unbuilt.

All identities below use repository `HEAD ab46061bf14db23a01054c2fd3fafec60fb5eb2f` unless another immutable commit/blob is stated. Explorer return references are stable local IDs `CS-*`.

### Surface and status drift matrix

| Ref | Surface classification and current claim | Immutable source identity, path, selector | Evidence scope | Proof |
|---|---|---|---|---|
| CS-01 | **Current source contract, older authoring state.** Source `SKILL.md` describes L0/L1 as buildable, L2 blocked, future telemetry, and future task sessions. It omits the later 13 additions and universal baseline. | blob `45268fd8d005bc4599ee0dd8161492b3f6b2fa63`; `cyberAlchemy-v2/development/mint/SKILL.md` §§process, observability, origin; last changed at `5662be19ae7b054bc30a2d1d180e6013e69c8926` | Source contract only; not proof of runtime | observed |
| CS-02 | **Installed runtime/projection, newer but unsynchronized.** It carries the additions/baseline and says emit logic is built, but is byte-divergent from the source contract: SHA-256 `d2e29d…` versus `31ce21…`; diff is 116 insertions/70 deletions. No source-to-installed generation/version declaration exists. | blob `9d6b260905dc2755e5c41344046ac4e5ff0bd231`; `.claude/skills/mint/SKILL.md` `<status>`, `<process>`, `<gates>`, `<origin>`; commit `fad671aed4ebf6c1405e4264a40d14e3ee33e740` | Installed agent instructions; not executable implementation | observed |
| CS-03 | **Plans containing stale status.** SPEC calls the additions “committed, NOT yet built”; EXECUTION-PACK and IMPLEMENTATION-LAYERING say “committed-not-built.” | `HEAD:cyberAlchemy-v2/development/mint/SPEC.md#Committed additions` lines 46–67; `HEAD:.../EXECUTION-PACK.md` lines 23–30; `HEAD:.../IMPLEMENTATION-LAYERING.md` lines 22–29 | Plan/define projections | observed |
| CS-04 | **Work-pack has the later state.** It says SWU-2 and SWU-5..10 emit logic are built but non-executed, with live Mint and N=3 work still outstanding. | `HEAD:cyberAlchemy-v2/development/mint/WORK-PACK.md#Build status` lines 37–45 | Work-pack status; does not prove execution | observed |
| CS-05 | **Harness source is stale.** It says “no examples run yet — Mint is not implemented,” while installed run reports record two smoke passes. | blob `54b87bacd99f9c994930833f5ea161c1059c5797`; `cyberAlchemy-v2/development/mint/development/HARNESS.md` lines 1–4; commit `fad671ae…` | Harness projection | observed |
| CS-06 | **Installed README is stale internally.** It says templates/additions “are being built” and invoking Mint will block at spine seed, while the adjacent installed SKILL says emit logic is built. | `HEAD:.claude/skills/mint/README.md` lines 7–12 versus `HEAD:.claude/skills/mint/SKILL.md` lines 8–15 | Installed documentation | observed |
| CS-07 | **Historical smoke evidence.** Reports record one fresh-domain core/additions pass and one baseline pass. The outputs were scratch test evidence, are not in the current tree, and therefore cannot be replayed from a persisted output fixture. | `HEAD:.claude/skills/mint/development/runs/20260701T180723Z-mint-smoke-01.md` lines 14–25, 27–51; `.../20260701T182000Z-mint-smoke-02.md` lines 8–38 | Historical handoff/run reports; runner output absent | observed report; execution unverified this turn |
| CS-08 | **Frozen experiment status differs from installed “future N=3” prose.** The original kind-level N=3 criterion completed and was FALSIFIED on research Obs-A; the corrected content-autonomy criterion later SURVIVED. Neither is shipment or live-mint proof. | `HEAD:cyberAlchemy-v2/development/mint/experiment-foundry-boundary/run/findings.md` lines 14–24, 39–61; `HEAD:.../experiment-content-autonomy/run-findings.md` lines 19–27, 136–142 | Frozen experimental artifacts | observed |
| CS-09 | **Inventory is discovery only.** Its source/runtime drift lead was confirmed, but its Mint status is not treated as authority. | `strategy-inventory-packet.json#direct_live_observations` and `#non_authority_notice`, packet ID `strategy-inventory-packet-2026-08-06-mint-improvement-audit` | Non-authority Inventory | observed |
| CS-10 | **Current Git state is clean for existing Mint/dependency files.** Only the active audit folder is untracked. Current bytes therefore match the cited tracked objects. | `HEAD ab46061…`; `git status --short -- cyberAlchemy-v2/development/mint .claude/skills/mint development/authority-triage`, observed `2026-08-06T13:14:19-03:00` | Current checkout | executed |

### Executable-path map

| Ref | Stage | Current path and behavior | Immutable source identity / selector | Evidence scope | Proof |
|---|---|---|---|---|---|
| CS-11 | Operator entry | `.claude/skills/mint/SKILL.md` is an agent instruction surface. Mint source and installed trees contain **zero executable files**. No Mint CLI/script exists. | `HEAD:.claude/skills/mint/SKILL.md`; `HEAD:cyberAlchemy-v2/development/mint/templates/EMIT-PROCEDURE.md` lines 27–34 | Current installed/source bytes | executed file-mode scan |
| CS-12 | L0 scaffold | Contract calls `domainspec-new-repo … --mode plan|apply`; `command -v domainspec-new-repo` returned missing, and the contract’s named source path `implementation/domainspec/.claude/skills/domainspec-new-repo/SKILL.md` does not exist in the checkout. | `HEAD:cyberAlchemy-v2/development/mint/templates/L0-compose-contract.md` lines 19–30, 33–61 | Current PATH and checkout | executed |
| CS-13 | L1 classification | `development/authority-triage/SKILL.md` exists at version 0.1.0, but `.claude/skills/authority-triage/SKILL.md` does not. Its contract says it classifies/routes and writes nothing into authority surfaces; Mint must own emission separately. | blob `5658e76bc81bef69b83ef81537b6355cb1e87a9e`; `development/authority-triage/SKILL.md` lines 1–11, 62–73, 102–110, 125–133 | Direct dependency contract | executed existence check; observed contract |
| CS-14 | L1 emission | `EMIT-PROCEDURE.md` is prose instantiation logic over 21 Markdown templates, not a runtime tool. | blob `ba3ce8456fa344b70162600d1062956d0946acc7`; `cyberAlchemy-v2/development/mint/templates/EMIT-PROCEDURE.md` lines 27–34, 75–225 | Current source | observed |
| CS-15 | Validation | Checks 1–13 are prose/grep obligations. No parser, validator, fixture runner, or receipt emitter implements them. | same blob; `EMIT-PROCEDURE.md` lines 246–297 | Current source | observed plus executable scan |
| CS-16 | L2 attestation | `attest.py` exists. `verify` returned `valid` against the live decision whose SHA-256 equals the artifact’s recorded hash. Mint contains no call/integration. | `HEAD:cyberAlchemy-v2/development/attestation-capability/attest.py`; `.../development/2026-07-12-l1-status-refresh.md` lines 12–42; attestation JSON lines 1–12 | Direct Mint dependency, L1 only | executed |
| CS-17 | Receipt/observability | Installed harness says observability is “not yet wired.” No Mint execution receipt exists. | `HEAD:.claude/skills/mint/development/EXPERIMENT-HARNESS.md` lines 22–30 | Installed lifecycle sidecar | observed |

### Verified defects and reliability gaps

| Ref | Classification | Defect or gap | Immutable source identity / selector | Evidence scope | Proof |
|---|---|---|---|---|---|
| CS-18 | defect | **L0 dependency is unavailable.** A conforming Mint cannot begin its required plan phase in this checkout. | CS-12 | Current checkout | executed |
| CS-19 | defect | **No executable Mint runtime.** “Deterministic, repeatable instantiation logic” is presently agent-mediated prose; behavior, ordering, and checks are not mechanically fixed. | CS-11, CS-14, CS-15 | Current source/runtime | executed/observed |
| CS-20 | defect | **Authority-triage integration contract is conflated.** Mint says “emit via authority-triage”; triage explicitly promotes/writes nothing and only returns a routing result. It is also not installed. | CS-13 plus `EMIT-PROCEDURE.md` lines 97–115 | Direct integration seam | observed/executed |
| CS-21 | defect | **Truth surfaces disagree.** Source, installed runtime, README, SPEC, plan, layering, work-pack, and harness describe different build/run states. | CS-01–CS-08 | Status/projection layer | observed |
| CS-22 | defect | **No current expanded golden fixture.** The persisted `release-approval` tree has zero placeholders and passes the narrow no-leak grep, but contains four `PROPOSED` occurrences, no ratify file, and none of METHODS-CATALOGUE, DEFINITIONS-INDEX, DRIFT-AUDIT, baseline constitution/primitives, or project-space roles. | `HEAD:cyberAlchemy-v2/development/mint/examples/release-approval/**`; comparison to `EMIT-PROCEDURE.md` checks 6–13 | Persisted fixture | executed |
| CS-23 | hardening gap | **The no-leak check is non-discriminating for other forbidden phrasings.** Target-owned regex did not match `route to cav2 for promotion`, although the procedure expressly forbids routing to cav2. | `EMIT-PROCEDURE.md` lines 59–71, 251–259; executed negative control | Validator design | executed |
| CS-24 | defect | **Closure contract contradicts itself.** Installed quality bar says no kind remains `PROPOSED`; ratify template and check #7 allow a deferred kind to remain `PROPOSED` with a matching record. | `.claude/skills/mint/SKILL.md` lines 108–115; `decision-mint-ratify.md` lines 35–55; `EMIT-PROCEDURE.md` lines 263–265 | Contract semantics | observed |
| CS-25 | reliability gap | **No mutation recovery contract.** L0 defines dry plan and “stop” on Step-7 failure; L1 blocks before record on failed checks. There is no target-exists/conflict/overwrite rule, staging transaction, rollback, cleanup, resumability, idempotent replay, or partial-apply receipt. | `L0-compose-contract.md` lines 27–61, 77–96; `EMIT-PROCEDURE.md` lines 246–290; recovery-term search | Failure behavior | observed/executed search |
| CS-26 | lifecycle gap | **No template version or upgrade posture.** Twenty-one templates have zero `version`, `template_version`, or `schema_version` fields; there is no manifest/lock/migration/upgrade file. Generated outputs do not pin template/source commit or hashes. | `HEAD:cyberAlchemy-v2/development/mint/templates/*.md`; commit `fad671ae…`; executed inventory | Template lifecycle | executed |
| CS-27 | stale dependency status | **Attestation L1 is no longer capability-blocked.** L1 is built and verified; Mint has not integrated it. Correct current split: L1 dependency available, Mint integration missing, L2 external identity/signature unbuilt. | CS-16; `attestation-capability/SKILL.md` lines 44–61; status refresh lines 12–42 | Direct dependency | executed/observed |
| CS-28 | reproducibility gap | Attestation DEMO gives a placeholder command but does not persist the claimed decision under `specimen/`; the obvious local `decision.md` replay failed missing-file. Verification succeeds only when resolved to the live authority decision path. | `HEAD:.../specimen/DEMO.md` lines 7–20; `attestation.json`; executed commands | Dependency specimen | executed |
| CS-29 | stale fixture classification | Installed harness calls resonantos a golden fixture; source harness correctly classifies it as an Obs-B negative control and `release-approval` as the N=1 positive fixture. | `.claude/skills/mint/development/EXPERIMENT-HARNESS.md` lines 7–20 versus `cyberAlchemy-v2/development/mint/development/HARNESS.md` lines 13–26 | Harness semantics | observed |

### Failure and recovery behavior

| Ref | Situation | Current specified/observed result | Proof |
|---|---|---|---|
| CS-30 | Start L0 | Shell cannot resolve `domainspec-new-repo`; no typed Mint block/receipt is emitted. | executed |
| CS-31 | Target has no clean domain-kind enumeration | Prose says emit `blocked-default-deny` and route to owner; exact artifact path/schema and replay behavior are unspecified. | observed, unverified |
| CS-32 | Self-check 1–13 fails after files are written | Prose says block before emitting the decision record; cleanup or rollback of already-written spine bytes is unspecified. | observed, unverified |
| CS-33 | Owner defers a kind | Ratify template permits deferred `PROPOSED`; installed quality bar says none may remain. | observed conflict |
| CS-34 | Apply is interrupted or collides with existing bytes | No behavior is specified. | verified absence |
| CS-35 | Attestation step | Separate L1 verifier works, but Mint has no stage binding, artifact destination, failure propagation, or retry contract. | executed dependency; integration unverified |

### Ranked candidate fixes

| Ref | Priority/class | Candidate, owner, and acceptance boundary | Immutable evidence / scope | Proof |
|---|---|---|---|---|
| CS-36 | P0 fix | **Choose and declare the canonical Mint source**, then generate/synchronize installed SKILL/README/harness with a source commit and hash. Owner: sigil-development. Acceptance: one status vocabulary; projection check detects drift. | CS-01–CS-08, CS-21 | candidate from observed defects |
| CS-37 | P0 dependency fix | **Restore or owner-route the exact `domainspec-new-repo` plan/apply capability.** Do not reimplement it in Mint. Mint must fail preflight with a typed missing-dependency block before target mutation. | CS-12, CS-18 | candidate |
| CS-38 | P0 implementation | **Create one executable Mint plan/apply front door** that stages output, validates all checks, then commits atomically; define target-exists, overwrite denial, cleanup, resume, and replay receipts. Owner: Mint/sigil-development. | CS-19, CS-25, CS-30–CS-34 | candidate |
| CS-39 | P0 integration fix | **Separate triage from emission.** Triage returns classification/owner-route evidence; Mint alone instantiates files after ratification. Install or explicitly invoke the source contract. | CS-20 | candidate |
| CS-40 | P0 validation fix | **Turn checks 1–13 into executable validators** with persisted normal and negative fixtures, including broader resolution-edge detection, malformed tables, missing methods, dangling links, cav2-row leakage, unresolved defer, and partial apply. | CS-22, CS-23 | candidate |
| CS-41 | P0 dependency integration | **Integrate attestation L1** into the Mint owner-close stage and update stale blocker prose. Keep external actor signature explicitly deferred. | CS-27, CS-28 | candidate |
| CS-42 | P1 contract fix | **Resolve defer semantics:** either deferred kinds are typed pending rows allowed by the quality bar, or closure removes every `PROPOSED`; encode one rule and validator. | CS-24 | candidate |
| CS-43 | P1 lifecycle hardening | **Add a template manifest/version and output provenance receipt** containing Mint version, template set version, source commit/hashes, attach mode/source identity, and migration compatibility. Add explicit upgrade/migration rules before supporting existing repos. | CS-26 | candidate |
| CS-44 | P1 evidence hardening | **Persist the expanded fresh-domain output as a fixture or provide a deterministic regeneration command.** Historical scratch reports alone are insufficient for current replay. Correct resonantos negative/golden terminology. | CS-07, CS-22, CS-29 | candidate |
| CS-45 | P1 operability | **Emit structured plan/apply/block receipts and stage telemetry** with files planned/written, checks, rollback/cleanup, owner verdicts, attestation result, and residue. | CS-17, CS-25 | candidate |

### Acceptance commands

Current read-only baseline commands, already executed:

```bash
command -v domainspec-new-repo
find cyberAlchemy-v2/development/mint -type f -perm /111
find .claude/skills/mint -type f -perm /111
test -f development/authority-triage/SKILL.md
test -f .claude/skills/authority-triage/SKILL.md
sha256sum cyberAlchemy-v2/development/mint/SKILL.md .claude/skills/mint/SKILL.md
git diff --no-index --stat cyberAlchemy-v2/development/mint/SKILL.md .claude/skills/mint/SKILL.md
python3 cyberAlchemy-v2/development/attestation-capability/attest.py verify \
  cyberAlchemy-v2/development/attestation-capability/development/specimen/attestation.json \
  cyberAlchemy-v2/authority/decisions/2026-06-24-saturn-domainspec-public-disclosure.md
```

Required executable acceptance after candidate implementation; these command names are proposed contracts and are currently unverified:

```bash
mint preflight --domain tide-tables --target /absolute/sibling/path --source /absolute/framework/path
mint plan --domain tide-tables --target /absolute/sibling/path --source /absolute/framework/path --attach submodule
mint apply --plan <plan-receipt.json>
mint validate --target /absolute/sibling/path --checks 1-13
mint resume --receipt <failed-apply-receipt.json>
mint verify-provenance --target /absolute/sibling/path
mint upgrade --target /absolute/sibling/path --plan
```

Acceptance boundaries:

- `preflight` blocks before writes when the scaffolder, triage contract, owner, target policy, or attestation integration is unavailable.
- `plan` writes no target bytes and records exact source/template identities.
- `apply` either commits a fully validated tree or leaves a typed recoverable receipt with no unaccounted partial bytes.
- `validate` passes persisted positive fixtures and rejects explicit negative fixtures, including `route to cav2 for promotion`.
- stage 3 encodes one non-contradictory defer policy.
- attestation L1 returns `valid` on the exact minted close-state and `tampered` on a content mutation.
- no result implies promotion, publication, deployment, release, shipment, or production readiness.

## RECEIPT PAYLOAD

```json
{
  "status": "pass",
  "validation": "pass",
  "artifacts": [
    "cyberAlchemy-v2/development/mint/SKILL.md",
    ".claude/skills/mint/SKILL.md",
    ".claude/skills/mint/README.md",
    "cyberAlchemy-v2/development/mint/SPEC.md",
    "cyberAlchemy-v2/development/mint/EXECUTION-PACK.md",
    "cyberAlchemy-v2/development/mint/WORK-PACK.md",
    "cyberAlchemy-v2/development/mint/IMPLEMENTATION-LAYERING.md",
    "cyberAlchemy-v2/development/mint/development/HARNESS.md",
    "cyberAlchemy-v2/development/mint/templates/EMIT-PROCEDURE.md",
    "cyberAlchemy-v2/development/mint/templates/L0-compose-contract.md",
    "cyberAlchemy-v2/development/mint/templates/decision-mint-ratify.md",
    "cyberAlchemy-v2/development/mint/examples/release-approval/",
    ".claude/skills/mint/development/EXPERIMENT-HARNESS.md",
    ".claude/skills/mint/development/EXPERIMENT-PROFILE.md",
    ".claude/skills/mint/development/runs/20260701T180723Z-mint-smoke-01.md",
    ".claude/skills/mint/development/runs/20260701T182000Z-mint-smoke-02.md",
    "development/authority-triage/SKILL.md",
    "cyberAlchemy-v2/development/attestation-capability/SKILL.md",
    "cyberAlchemy-v2/development/attestation-capability/attest.py",
    "cyberAlchemy-v2/development/attestation-capability/development/2026-07-12-l1-status-refresh.md",
    "cyberAlchemy-v2/development/attestation-capability/development/specimen/DEMO.md",
    "cyberAlchemy-v2/development/attestation-capability/development/specimen/attestation.json",
    "cyberAlchemy-v2/development/mint/experiment-foundry-boundary/run/findings.md",
    "cyberAlchemy-v2/development/mint/experiment-content-autonomy/run-findings.md",
    "cyberAlchemy-v2/development/mint/development/research/2026-08-06-mint-improvement-audit/strategy-inventory-packet.json"
  ],
  "blockers": [],
  "started_at": "2026-08-06T13:07:42-03:00",
  "finished_at": "2026-08-06T13:15:25-03:00"
}
```
