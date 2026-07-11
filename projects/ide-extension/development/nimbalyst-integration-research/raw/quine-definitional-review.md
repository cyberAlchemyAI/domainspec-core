# Quine Definitional Review

Dispatch: `2026-07-11-nimbalyst-integration-research`
Identity: Quine, Willard Van Orman
Gate: `DEFINITIONAL-SOUNDNESS` only
Pinned upstream: `Nimbalyst/nimbalyst@c8ca207c6004653ba2df3d81e06133ce2e9fad3d`

## Verdict

The synthesis overcounts candidates by treating renamed local interfaces, ordinary
test techniques, and product precedents as reusable units. A candidate is
definitionally sound here only when:

1. its intension states a behavior not already owned by an inspected local surface;
2. its extension identifies implementations or artifacts that cannot be substituted
   by a generic fixture, schema validator, package smoke test, or existing local
   adapter without loss;
3. the distinction removes a named implementation obligation after adaptation,
   provenance, testing, upgrade, and abandonment costs; and
4. its name does not disguise a second authority, status model, or execution plane.

Only `NIM-C05`, `NIM-C08`, and `NIM-C12` survive as distinct candidate concepts.
They remain deferred hypotheses, not admissions. Every other candidate is a
re-skinned duplicate, an ordinary engineering technique, or an inadmissible
execution stack. `NIM-C06` contributes useful event distinctions, but those belong
inside the surviving C05/C12 definitions; it is not a separate lifecycle contract.

## Exact Dispositions

| ID | Exact disposition | Definitional judgment | Real implementation cost removed |
|---|---|---|---|
| `NIM-C01` | **KILL** | `{artifact_ref, content, theme, readOnly}` is a generic read-model input, while load/subscription/dirty/save concerns reintroduce Nimbalyst editor semantics. No selected local renderer requires this named host. | None. A local component prop or narrow test port must still be designed and tested. |
| `NIM-C02` | **KILL** | After C01 is removed, this is exactly an in-memory test double. Upstream `createReadOnlyHost` implements the broad `EditorHost` and even supplies mutating no-ops such as `saveContent`; pruning it produces an ordinary fixture builder. | None. Extraction and semantic pruning cost at least as much as a local fixture. |
| `NIM-C03` | **KILL** | Closed schemas, hostile invalid fixtures, unknown-field rejection, and pre-persistence validation are already the local AR-CAND-008 remedy and generic Draft 2020-12 practice. Nimbalyst's manifest vocabulary is extension-specific and does not define a new local concept. | None. The local schema, runtime enforcement, and fixtures still must be authored. |
| `NIM-C04` | **KILL** | Build, pack/dry-run, inspect files, and compile a minimal consumer is an ordinary public-package smoke check. There is no separately packaged local contract to which an upstream-derived definition applies. | None now; later use the package manager's standard checks directly. |
| `NIM-C05` | **PRESERVE, DEFER** | Distinct definition: an **evidence projection pair** is `(R, P_v)` where `R` is an immutable, ordered, redacted sequence of provider-native records preserving unknown records and correlation data, and `P_v(R)` is a versioned, deterministic, disposable canonical view. `R`, never `P_v`, is evidential source material; neither adjudicates outcome. Local artifacts/hashes do not yet state this raw-preservation/projector-replacement relation. | Avoids separately designing replay, unknown-event retention, and projector replacement once two admitted provider formats demonstrate duplicated parser work. Before that witness, none. |
| `NIM-C06` | **KILL; fold residues into C05/C12** | The six verbs are already named by the local Agent Envelope Strategy. Renaming that set `ExternalAgent` does not change its extension. `raw`, `tool_call`, and `tool_result` belong to C05 records; abort, cleanup, completion, and resume observations belong to C12. | None as a standalone contract. Local envelope-state mapping and all failure tests remain. |
| `NIM-C07` | **KILL** | A before/after evidence view and accept/discard grammar are already owned by UI Prototyping Studio; ide-extension already owns artifact references and the known missing after-state repair. Calling the same projection a Nimbalyst candidate adds no defining property. | None. Materializing and validating evidence plus building the local projection remain unchanged. |
| `NIM-C08` | **PRESERVE, DEFER** | Distinct definition: an **owner-qualified provenance join** is a disposable, read-only relation over independently canonical identifiers whose cells retain `(owner, schema/version, id)` and whose unresolved edges remain explicit. It has no status, lifecycle, launch, promotion, or write semantics. Craft/Arcanum owns tasks/routes and IDE Ergonomics owns routing surfaces, but no inspected source defines this cross-owner join. | Potentially removes repeated resolver/navigation work only after one recurring query and measured manual cost are recorded. Without that witness, none. |
| `NIM-C09` | **KILL** | `DesignFeedbackContextPacket` is already explicitly owned and defined by the MCP/chat findings and named by local architecture. Nimbalyst adds only product corroboration. | None. This is the same local packet, not a candidate reuse unit. |
| `NIM-C10` | **KILL** | The bounded stdio descriptor, fixture CWD, redacted HOME, env allowlist, single observe tool, and no-network/no-mutation/no-receipt constraints already exist verbatim in local findings. Parsing another provider's ambient MCP configuration is contrary to that definition. | None. The local descriptor parser and hostile fixtures still must be implemented. |
| `NIM-C11` | **KILL** | Typed observe/navigate/click/fill/screenshot behavior already exists as local browser-first design and concrete ResonantOS browser-first command/action machinery. Nimbalyst's browser extension supplies another implementation, not a distinct vocabulary. | None. Admission through the local adapter and approval boundary is still required. |
| `NIM-C12` | **PRESERVE, DEFER** | Distinct definition: **observed termination semantics** separates requested interruption from observed process termination, resource cleanup, resumability validation, and kernel outcome. Resume succeeds only when provider identity and opaque continuation identity match; partial side effects/evidence remain residue and cannot be promoted to success. Local `interrupt`/`inspect` names do not yet define these separations. | Avoids rediscovering a shared failure-state matrix when the first real process/provider adapter is admitted. It removes no current L0 work. |
| `NIM-C13` | **KILL** | This is a product subsystem, not one coherent candidate concept, and duplicates local grant, approval, session, artifact, audit, and receipt owners with incompatible authority. | Negative. Authority replacement and migration add work. |
| `NIM-C14` | **KILL** | Terminal, Git/worktree, backend-module lifecycle, preload IPC, and database/storage are several unrelated execution authorities grouped by source product packaging. The grouping has no local defining unity. | Negative. Each capability still needs a separately governed adapter and recovery model. |
| `NIM-C15` | **KILL** | Sync, mobile, collaboration, identity, crypto, and credential custody are distinct systems, while the cited server is absent from the MIT checkout. "Stack" is a product boundary, not a reusable local definition. | Negative or unprovable; no server implementation is available to remove local work. |
| `NIM-C16` | **KILL** | Analytics/telemetry and executable update delivery have different subjects, risks, owners, and acceptance conditions. Combining them is extension by packaging accident. Local observability already has a separate owner and no updater is admitted. | None; both would require independent implementation and governance. |

## Comparison Findings

- **Existing ide-extension:** C03, C06, C09, and C10 duplicate explicit local
  requirements. C01/C02 add host nouns without a selected renderer. C07 depends on
  the already-recorded after-artifact and schema-enforcement repairs rather than
  removing them.
- **Craft/Arcanum:** C08 survives only as a query across owner-qualified references.
  Any task status, route, workstream, launch, or promotion field makes it a duplicate
  ledger and therefore kills it.
- **UI Prototyping Studio:** its apply/validate/stage/accept-or-discard model and
  concrete artifact/diff work make C07 a duplicate. Nimbalyst may remain a cited
  product precedent, not a candidate.
- **IDE Ergonomics:** route surfaces already point to owner capabilities without
  acquiring authority. This constrains C08 but does not itself implement the
  cross-owner provenance join.
- **ResonantOS browser-first:** concrete command parsing, tab observation, typed page
  actions, permission checks, session storage, and action controllers make C11 a
  re-skinned duplicate.
- **Generic local fixtures:** C02, C03, and C04 are test-fixture, schema-validation,
  and package-smoke shapes. None has a Nimbalyst-specific extension that survives
  clean-room local expression.

## Required Synthesis Revisions

1. Replace the candidate-count summary with: **3 preserved/deferred, 13 killed**.
2. Remove `adapt locally`, `adopt local vocabulary`, `build-from-owned`, and
   `precedent` as candidate dispositions. A precedent may be cited in rationale, but
   is not itself an integration candidate.
3. Delete C01-C04, C06-C07, C09-C11, and C13-C16 from the shared-ready candidate
   list. Retain their evidence only in a killed-candidates appendix.
4. Replace C05's definition with the exact evidence projection pair above. State the
   two-provider duplication witness as a necessary condition, not merely timing
   advice. Fold provider record tags from C06 into C05.
5. Replace C08's definition with the owner-qualified provenance join above. Require
   one named recurring query, baseline navigation cost, and resolver ownership before
   admission. Delete all unqualified `task_ref`/`artifact_ref` language.
6. Replace C12's definition with observed termination semantics above. Fold C06's
   abort/cleanup/complete/resume distinctions into it and keep provider completion
   separate from kernel outcome.
7. Remove claims that C01 avoids editor-host naming, C02 avoids fixture invention,
   C03 avoids hostile-case design, C04 avoids package-check design, C06 avoids
   lifecycle rediscovery, C07 avoids interaction research, C09 avoids packet design,
   C10 avoids parser design, or C11 avoids browser-tool naming. The inspected local
   and generic surfaces already supply those forms; no net implementation saving is
   demonstrated.
8. Split every product-stack row into either a killed source precedent or a future
   separately governed program. Do not call C13-C16 reusable units.
9. Revise the final position: no immediate Nimbalyst-derived implementation unit is
   admitted by definitional soundness. The next possible units are C05 after a second
   provider, C08 after a measured recurring query, and C12 with the first real
   process/provider adapter.

## Source Accounting

Reviewed inputs were `synthesis.md`, `research.md`, and all four existing raw explorer
files. Local comparison included the cited ide-extension architecture, specification,
schemas, kernel/envelope implementations, smoke fixture, architecture review, MCP/chat
findings, UI Prototyping Studio interfaces and implementation/test surfaces, IDE
Ergonomics route constraints, Craft's task/query authority, and ResonantOS
browser-first command, action, permission, session, and controller surfaces.

The pinned upstream SHA was verified. The review inspected every file or bounded
directory named by C01-C16: extension SDK editor/lifecycle/read-only-host types and
tests; manifest validation, package checks, dev-kit/examples; transcript runtime,
projectors, parsers, accumulator, and transcript UI; agent protocol/host and provider
implementations/tests; feature/planning/tracker documentation and tracker/session UI
evidence; MCP configuration/OAuth/IPC; browser extension/client/tools/session service
and handlers; permission/provider/session runtime; terminal, Git/worktree, backend,
preload, database/storage; collaboration protocol, runtime sync, mobile/client
boundaries, README/licensing; and telemetry/updater source and package/release
surfaces. The collaboration server was not present and therefore cannot support an
implementation-saving claim.

## Gate Result

`DEFINITIONAL-SOUNDNESS`: **FAIL AS SYNTHESIZED; PASS AFTER THE REQUIRED REVISIONS**.

No canonical definition is promoted by this review. C05, C08, and C12 are precise
research candidates whose admission remains contingent on their stated witnesses.
