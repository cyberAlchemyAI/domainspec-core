# Architecture: candidate-local WaveDB projection for Craft

## Architecture intent

Make the WaveDB/Craft hypothesis empirically testable while ensuring no
database state, derived artifact, package metadata, or experiment receipt can
acquire Craft authority. The first executable gate is exact package/source
provenance; the first database query is admitted only after a fresh YAML read
and complete generation verification.

## Closed scope

- System: `wcp-candidate-projection-experiment`
- Scope manifest: `DESIGN-SCOPE-MANIFEST.json`
- Manifest input digest: `9a7351c8277d4f31c5c12252db66003c017650d1d8aea430008964022339af00`
- Denominator receipt: `DESIGN-DENOMINATOR-RECEIPT.json`
- Denominator receipt digest: `25f969db6ab04949465a5ceaae09571fad9362fbc53239d5c3bd992c82dcff00`
- Selection result: `DESIGN-SELECTION-RESULT.json`
- Selection result digest: `632574d620b42e6c6b3b3cda4d217b0bad35c2ee432a798ec9257e00968293a4`
- Evidence state: `design-validator-pass`

## View 1: Context

```text
Craft owner and canonical files
  .craft/ledger.yml  <-------------------------------+
       | sole authority                              |
       v                                             | never write back
candidate experiment                                 |
  provenance gate -> fixture compiler -> adapter ----+
                           |
                           v
                   isolated WaveDB copies
                           |
                           v
              external evidence and quarantine receipts
```

The package/security owner controls native artifact admission. The adapter
owner controls the codec and stable failure behavior. The Craft owner controls
the semantic interpretation and any later adoption decision. Publication,
promotion, deployment, and real destructive tests have separate owners and are
outside this architecture.

## View 2: High-level structure

| Component | Responsibility | Authority |
| --- | --- | --- |
| Provenance gate | Bind registry package, integrity, gitHead, source commit/tree, and toolchain | Can block install; cannot approve publication |
| Workspace resolver | Resolve and authorize the filesystem scope | Controls which YAML may be read; no database lookup |
| Fixture compiler | Validate/parse YAML and produce deterministic model, keys, values, and hashes | Derived evidence only |
| Generation builder | Write one previously unserved digest generation and manifest last | Isolated candidate mutation only |
| Complete verifier | Enumerate every stored key and compare exact bytes/digests | Sole query-admission validator |
| Query facade | Execute only allowlisted row/index reads after fresh verification | Zero or complete output |
| Failure controller | Run bounded barriers and negative controls | Isolated copies only |
| Quarantine/rebuild controller | Record external quarantine and create a fresh sibling | No in-place repair |
| Evidence writer | Persist run inputs, events, outputs, and verdicts | Filesystem receipt owner; never WaveDB |

## View 3: Low-level components

### Provenance gate algorithm

1. Read exact registry metadata for the pinned package version.
2. Download without installing and verify the declared SRI and SHA-1.
3. Resolve the declared `gitHead` and the separately reviewed source commit.
4. Compare version metadata and every shipped source byte against the selected
   source tree under a declared line-ending rule.
5. Require one non-contradictory source/package identity. On any mismatch emit
   `PACKAGE_PROVENANCE_MISMATCH` and stop before dependency resolution, build,
   install scripts, or addon loading.

### Codec pipeline

```text
exact L0 bytes
 -> Craft schema validation
 -> pinned YAML parse/options
 -> normalized S0
 -> sorted rows and indexes
 -> percent-encoded generation keys
 -> exact value bytes
 -> payload digest H_P
 -> readback
 -> manifest written last
```

The manifest excludes itself from `H_P` but enumerates every other key and
value digest. Query admission separately enumerates the complete key set,
including the manifest, and rejects extra or missing keys.

### Query admission pseudocode

```text
workspace = resolveAndAuthorize(workspaceRoot)
L = readExact(workspace/.craft/ledger.yml)
validateCraft(L)
H = sha256(L)
if H != expectedLedgerDigest: zero(LEDGER_DIGEST_MISMATCH)
generation = openExact(workspaceId, H)
if not verifyEveryKeyAndValue(generation, L):
  quarantineExternal(generation)
  zero(PROJECTION_VERIFICATION_FAILED)
return completeAllowlistedQuery(generation)
```

## View 4: Workflow process

```text
unfrozen
  -> check provenance
     -> mismatch: package-gate-blocked [terminal]
     -> exact: package-gate-pass
  -> freeze fixture and independent constants
  -> build unserved payload
  -> complete readback
     -> mismatch: verification-failed -> quarantined [terminal]
     -> exact: manifest-last -> verified
  -> fresh YAML admission per query
  -> positive and negative observations
  -> bounded closeout
```

No implicit retry is legal. A repair, new package, source correction, parser
change, or fixture change starts a new run with new identities.

## View 5: Decision flow

| Decision | Pass branch | Fail branch |
| --- | --- | --- |
| Exact package/source correspondence? | permit candidate dependency resolution/build | stop before install |
| Canonical YAML valid and exact expected digest? | select matching digest generation | zero rows; no stale fallback |
| Complete key/value set and all hashes exact? | allow query | quarantine externally; zero rows |
| Negative control targets explicit isolated copy? | run control | refuse destructive operation |
| Process termination observation recovered exactly? | record bounded observation | record failure; no power-loss claim |
| All WP-0..WP-6 oracles pass? | route evidence to Craft owner | close blocked with first failure and residue |

## View 6: Dependency and interface

| Dependency/interface | Pin/binding | Allowed use | Forbidden use |
| --- | --- | --- | --- |
| Craft contract | exact local file digests in scope manifest | schema/authority interpretation | canonical mutation |
| WaveDB npm artifact | exact version, SRI, tarball hash, resolved source | isolated adapter primitives after provenance pass | unscoped install or raw canonical store |
| YAML parser | exact package/version/options and lock integrity | deterministic fixture compilation | implicit coercion drift |
| JSON serializer | UTF-8, recursive key sort, retained array order, no terminal newline | exact values/hashes | runtime-dependent formatting |
| Filesystem | authorized fixture root and explicit isolated stores | fresh YAML read and external receipts | broad deletion or real ledger damage |
| Task Session | one selected SWU and exact write/validation scope | execution and terminal receipt | batch execution hidden inside one receipt |

## Significant behavior scenarios

| Stimulus | Preconditions | Ordered response | Failure/recovery | Evidence | Owner |
| --- | --- | --- | --- | --- | --- |
| npm package provenance check | package version and reviewed commit pinned | fetch metadata; verify tarball; compare gitHead/source | contradiction blocks before install | WP-0 receipt | package/security owner |
| query frozen generation | valid fixture, complete verified generation | fresh-read YAML; verify digest; verify generation; query | any mismatch returns zero and quarantines | query receipt and byte comparison | adapter owner |
| corrupt isolated copy | complete store copy and named corruption target | mutate copy; reopen; fresh admission | any valid-prefix or wrong state still fails closed; rebuild sibling | corruption and rebuild receipts | destructive-operation/adapter owners |

## Concern-to-view trace

| Concern | Class | Disposition | Output | Primary view/extension |
| --- | --- | --- | --- | --- |
| `concern:authority` | authority | required | `architecture:authority-trust` | context, provenance and admission placement |
| `concern:security` | security | required | `architecture:security-abuse` | native artifact and corruption-control boundary |
| `concern:state-event` | state-event | required | `architecture:state-event` | workflow states and terminal rules |
| `concern:persistence` | persistence | required | `architecture:persistence-concurrency` | generation, manifest-last, single writer |
| `concern:failure` | failure | required | `architecture:failure-compensation` | zero output, quarantine, sibling rebuild |
| `concern:reliability` | reliability | required | `architecture:quality` | exact repeatable oracles |
| `concern:integration` | integration | required | `architecture:integration-versioning` | strict Craft/WaveDB adapter |
| `concern:migration` | migration | not applicable with rationale | none | v0 explicitly excludes migration/downgrade |
| `concern:rollout` | rollout | not applicable with rationale | none | no deployment/promotion/publication |
| `concern:privacy-data` | privacy-data | required | `architecture:data-lifecycle` | external receipts and retention |
| `concern:performance` | performance | recommended | `architecture:quality` | descriptive observations only |
| `concern:validation` | validation | required | `validation-contracts` | exact WP/SWU oracles |

## Planned witness contracts

| Witness | Claim | Polarity | Expected result | Phase |
| --- | --- | --- | --- | --- |
| WIT-PROV-001 | package provenance | positive/negative | exact mapping passes; any contradiction blocks before install | WP-0 |
| WIT-CODEC-001 | closed codec | positive | independent constants and every key/value digest match | WP-0/WP-1 |
| WIT-NEG-001 | zero-output admission | negative | stable failure, zero rows, unchanged YAML | WP-4 |
| WIT-ITER-001 | iterator visibility | observation | each stream matches one complete frozen manifest; no hybrid | WP-3 |

Planned witnesses are contracts only; they are not execution evidence.

## Selected extensions

### Authority and trust

Authority is enforced before WaveDB access. Craft YAML is the only source of
truth; the provenance gate may block native execution; the complete verifier is
the only query-admission owner; no component can promote the result.

### Security and abuse

Threats include a mislabeled native tarball, install-script execution before
review, workspace escape, prefix traversal, oversized/unlisted payloads,
crafted IDs, stale generation fallback, valid-prefix corruption, and receipt
injection. Controls are exact integrity/source binding, normalized relative
paths, closed key manifests, isolated stores, zero-output verification, and
external-only receipts. Dependency license/SBOM and encryption lifecycle remain
HOLD.

### State and events

Only the states in View 4 are legal. Manifest write is the last build action;
verified is required before query admission; blocked, failed, quarantined, and
closed are terminal for a run/generation. Events are observation evidence, not
Craft domain events.

### Persistence and concurrency

The adapter admits one writer. Concurrent A/B is an observation, not a supported
interface. There is no active pointer, CAS, lease, dual write, prefix deletion,
or database-to-YAML transaction. Batch preflight rejection is not mid-apply
atomicity proof.

### Failure and compensation

No retry or in-place recovery occurs. Failure returns zero rows, records exact
external evidence, quarantines the suspect generation, and may rebuild a fresh
sibling from YAML. Process termination is bounded crash observation only.

### Integration and versioning

The adapter surface is smaller than WaveDB's native API and excludes Graph,
GraphQL, vector, derived ingestion, and raw mutation. Any package, Craft schema,
adapter schema, parser, or serializer change creates a new input identity and
invalidates prior generations.

### Data lifecycle

Fixture data are synthetic. Package metadata, toolchain identities, hashes,
events, and receipts remain in this candidate-local package. No receipt body,
reference, digest, or verdict is written into WaveDB. Cleanup applies only to
an exact isolated temporary path and is not deletion semantics evidence.

### Quality and validation

Correctness requires exact bytes, hashes, counts, keys, stable failure codes,
and unchanged YAML. Latency/size may be recorded with environment details but
never gates correctness. Each WP is one or more atomic SWUs with independent
acceptance evidence and a terminal receipt.

## Dependency rules

| Rule | Enforcement |
| --- | --- |
| No install before provenance pass | WP-0 Task Session stops before package manager mutation |
| No query before complete verification | adapter returns stable zero-output failure |
| No non-manifest unlisted key | complete key enumeration and manifest comparison |
| No owner receipt in WaveDB | key-family allowlist plus full enumeration |
| No canonical mutation | pre/post YAML digest plus write-scope audit |
| No destructive target outside isolated root | realpath/root check and explicit target receipt |

## Decision log

| ID | Status | Decision | Rejected alternatives | Evidence/revisit |
| --- | --- | --- | --- | --- |
| D-WCP-001 | accepted | YAML remains sole authority | WaveDB canonical store; dual write | Craft contract; separate authority-change route required |
| D-WCP-002 | accepted | direct digest generation selection, no active pointer | mutable activation alias | findings corrected v0 architecture |
| D-WCP-003 | accepted | complete readback then manifest-last | partial/prefix trust | findings codec proposal |
| D-WCP-004 | accepted | package contradiction blocks before install | infer correspondence from normalized similarity | package/security owner gate |
| D-WCP-005 | accepted | quarantine and sibling rebuild | in-place recovery | corruption research and KILL residue |
| D-WCP-006 | accepted | process-crash observation only | power-loss/durability claim | HOLD residue |

## Risks

| Risk | Mitigation | Owner |
| --- | --- | --- |
| npm metadata points at source version `0.15.7` while tarball is `0.15.8` | block WP-0; obtain corrected provenance or explicitly select a new source-build route | package/security owner |
| native addon may not build on Node 22/WSL2 | observe only after provenance pass; pin complete toolchain | package/security owner |
| parser normalization may change Craft meaning | pin version/options and compare exact semantic/model hashes | adapter + Craft owners |
| corruption may yield a valid prefix | never serve prefix; enumerate and hash every key/value | adapter owner |
| false success from limited crash testing | preserve process/power claim boundary | validation owner |

## Gate result

- Status: `pass`
- Evidence: scope extraction pass; selection result `design-validator-pass`;
  pass-one and pass-two digests equal; diagnostics empty.
- Execution caveat: Design pass does not override the current WP-0 package
  provenance blocker.
