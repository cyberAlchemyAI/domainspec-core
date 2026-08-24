---
module: augmentor-rich-consultation-publication
version: candidate-0.1.0
status: implementation-ready-local-external-gate-pending
updatedAt: 2026-08-04
docType: work-pack
---

# Work Pack: Publish Rich Consultation

## Control fields

| Field | Value |
| --- | --- |
| Planning gate | pass |
| Design gate | `design-validator-pass` |
| Complexity | high |
| First unit | `SWU-AUGPUB-000` |
| Local mutation authority | absent from this Plan |
| Production authority | absent; exact external-effect confirmation required after 003 |
| Execution | serial, fail closed |
| Credentials | forbidden from artifacts, commands, logs, fixtures, and receipts |

## SWU manifest

| SWU | Primary behavior | Exact target | Depends on | Acceptance |
| --- | --- | --- | --- | --- |
| AUGPUB-000 | Freeze exact current inputs and prove the deployment-closure mismatch. | target inventory and byte baseline only | none | hashes current; loader requires seven files; packager copies two; no writes |
| AUGPUB-001 | Make candidate packaging complete and version-correct. | `deployment/deploy-static-vps.sh` plus focused packaging tests | 000 | all seven files copied/verified; whole-release id; `1.1.0` guided smoke; negative cases stop pre-SSH |
| AUGPUB-002 | Rebuild and validate the exact page and rich consumer bundle. | existing generators and generated outputs in DomainSpec; consumer docs/runtime in ResonantOS | 001 | no unreviewed drift; complete local suites pass under Node 22.13.0 |
| AUGPUB-003 | Assemble and prove one deployable candidate without external transport. | dry-run bundle, release manifest, rollback fixture, validation receipt | 002 | exact inventory/digests, Compose config, loader boot, rich request, and rollback rehearsal pass |
| AUGPUB-004 | Publish the admitted candidate as one production generation. | `/srv/augmentor-ontology` through owned release script | 003 + explicit authorization | upload/switch/start/check succeeds or previous generation is restored |
| AUGPUB-005 | Verify the production generation through each evidence layer. | remote containers, protected public routes, exact deployed files | 004 | hashes, health, `1.1.0` guided support, denial, restart, topology, homepage isolation pass |
| AUGPUB-006 | Close the release with a secret-free receipt and residue. | `deployment/DEPLOYMENT-RECEIPT.md` and Task Session closeout | 005 | current/previous ids, hashes, evidence layers, rollback locator, residue and successor recorded |

## Recomposition

```text
000 exact truth
 -> 001 complete release packager
 -> 002 current validated product bytes
 -> 003 admitted candidate generation
 -> 004 production switch or rollback
 -> 005 production evidence
 -> 006 durable closeout
```

## Task Session closeout sync

Every mutation-capable unit must record:

- exact target inventory and pre-mutation SHA-256;
- baseline binding to the predecessor receipt;
- admitted delta classes and forbidden files;
- exact validation commands and results;
- expected owner receipt with artifacts, status, validation, blockers, residue,
  and handoff note;
- deterministic successor or terminal rollback route.

| SWU | Admitted delta | Forbidden delta | Owner receipt | Successor |
| --- | --- | --- | --- | --- |
| 000 | evidence files in Task Session only | product, deployment, remote, Git | baseline receipt | 001 if exact; otherwise owner review |
| 001 | deploy packager and focused tests | page semantics, API logic, auth, production | packaging receipt | 002 |
| 002 | generator-owned outputs only when deterministic rebuild requires them; consumer-owned docs/runtime only if admitted drift repair is proven | deployment, secrets, unrelated user changes | candidate validation receipt | 003 |
| 003 | candidate-local release manifest and fixtures | SSH, DNS, containers, production links | candidate admission receipt | external-effect gate for 004 |
| 004 | one immutable remote release plus `current`/`previous` switch | credentials, unrelated host paths, homepage, source repos | deployment or rollback receipt | 005 on success; incident closeout on rollback |
| 005 | read-only production probes and evidence | config or data mutation except automatic rollback | production validation receipt | 006 or rollback route |
| 006 | append one dated deployment closeout and Task Session evidence | product/runtime/remote mutation | terminal closeout receipt | monitor or targeted residue route |

## Unit details

### SWU-AUGPUB-000 — baseline and blocker proof

- Recompute every Design manifest digest.
- Capture scoped `git status` in both repositories without adopting unrelated
  changes.
- Compare current deployed receipt hashes to local page, runtime, and bundle.
- Prove the loader reads seven files and the packager copies only two.
- Stop on any competing production route, missing previous generation, or
  changed source not attributed to the rich implementation.

### SWU-AUGPUB-001 — release closure repair

- Require and copy projection, glossary, manifest, and four schemas.
- Generate a candidate file manifest and derive the release id from the entire
  candidate rather than page bytes alone.
- Update internal smoke to query `augmentor.consultation.query@1.1.0` with
  `explanation.profile=guided`.
- Assert returned contract family, expected bundle digest, at least one whole
  explanation pack, 2-5 glossary terms when returned, `qualify|answer`,
  `followRetrievedInstructions=false`, and `authorityEffect=none`.
- Add negative packaging cases for absent glossary, absent schema, wrong schema
  digest, mixed family, and missing consumer module.

### SWU-AUGPUB-002 — exact candidate validation

- Rebuild generators in check mode first; block on unexplained output drift.
- Run the exact producer, consumer, docs, alpha, page, browser, ownership, and
  leakage commands in `IMPLEMENTATION-PLAN.md`.
- Recompute page, bundle, glossary, manifest, runtime-module, Compose, Nginx,
  and packager hashes.

### SWU-AUGPUB-003 — no-transport deployment rehearsal

- Run the packager in dry-run/package-verification mode with the exact consumer
  root.
- Inspect the candidate inventory and run the API container entrypoint against
  the staged seven-file bundle.
- Send the five questions across brief/guided/deep as the local acceptance
  matrix.
- Inject one acceptance failure in an isolated fixture and prove the rollback
  target is selected without touching production.
- Emit the candidate admission receipt naming exact external target and prior
  rollback release.

### SWU-AUGPUB-004 — production switch

- Require an explicit authorization that names the AUGPUB-003 candidate receipt,
  production host/path, current generation, and rollback generation.
- Use the verified SSH host key and existing operator session. Do not pass
  `AUTH_PASSWORD`; preserve the existing hash from `current`.
- Upload, validate, rename the immutable release, switch links, recreate the two
  containers, and run the script's acceptance loop.
- On failure, restore `previous`, recreate with `--remove-orphans`, verify
  health, and emit rollback rather than completion.

### SWU-AUGPUB-005 — production validation

- Compare deployed and candidate hashes for every release artifact.
- Verify API has no public host port and only Nginx joins the edge network.
- Run internal trusted-proxy `1.1.0` guided and deep consultations, including
  “How does the Augmentor reasoning engine work?” and assert current-state
  qualification plus the expected bundle digest.
- Restart both containers and repeat health and rich query.
- Verify anonymous and wrong-password page/API denial, unrelated path `404`,
  TLS route, CSP, and unchanged root homepage.
- If the human operator chooses to replay the authenticated public form, record
  only result metadata. Never request, log, or store the password.

### SWU-AUGPUB-006 — closeout

- Append a dated receipt section with candidate/current/previous release ids,
  exact hashes, validations, rollback state, and evidence-layer distinctions.
- Record public authenticated browser replay as passed or explicit residue.
- Bind failure residue to rollback/incident handling; bind success residue to a
  monitoring or human-replay route.

## Stop conditions

- Any credential becomes visible or would be written to an artifact.
- Exact baseline drift cannot be attributed and admitted.
- Bundle closure, digest, contract family, or local validation fails.
- The candidate would mix page, runtime, or bundle generations.
- The external authorization does not name the exact candidate and rollback.
- Remote path ownership marker, host key, edge network, current/previous links,
  or existing homepage differs from the admitted baseline.
- Rich response changes truth, authority, or instruction-following boundary.
- Rollback cannot restore a healthy prior generation.

## Readiness verdict

Implementation-ready for local units 000-003 after Task Session admission.
Production unit 004 is deliberately gated by a later exact external-effect
authorization. That stop is a safety boundary, not a planning gap.

