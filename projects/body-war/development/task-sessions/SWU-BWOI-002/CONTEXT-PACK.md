# Context Pack — SWU-BWOI-002

## Selected unit

- Work pack: `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/WORK-PACK.md`
- Task: `TASK-BWOI-DOMAINSPEC`
- SWU: `SWU-BWOI-002`
- Layer / wave: `L1` / `W1`
- Execution owner: `local-fallback`

## Objective

Derive the admitted `body-war.CT-2` function from the canonical
`body-war.CreateSuggestedTrack` Operation node, compare its generated result
with the current memory repository, and prove that a stronger mutated backend
result is rejected.

## Selected sources

| Role | Path | SHA-256 |
| --- | --- | --- |
| work-pack authority | `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/WORK-PACK.md` | `392480456ada3315aebf9a11fe113a2731623176c6b348786384b6eee7d3b4ce` |
| task contract | `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/work-pack/tasks/TASK-BWOI-DOMAINSPEC.md` | `aa2e700ac1aadc71fccec827d88a7cf48702b3fd402384652b5399fb77c8184a` |
| wave gate | `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/work-pack/waves/W1.md` | `c9457a00c0f1b680f40d6df26ee8af734236f067eec1eec36637f6481b340050` |
| test contract | `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/SPEC.md` | `7c759884d00c51f29f28c7279ffeae6b1fd91e318a6733a39feed237826e94f4` |
| architecture contract | `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/ARCHITECTURE.md` | `ee1928193a1f5580c022db59e6c04e91f0323a092af23d8856a9fd400e006d4a` |
| development profile | `projects/domainspec-v2/impl/spec/sfol-profile/minted-project-profile.json` | `17384f4161df05461ac193ab6df369a20f189233a3f27fb111b437845b468918` |
| logic envelope schema | `projects/domainspec-v2/impl/spec/sfol-profile/node-logic-envelope.schema.json` | `f50d9978193bfaeca0b8005750e7f08686210d809bb8823af117c6248f49a5ea` |
| generic profile example | `projects/domainspec-v2/impl/tools/tests/sfol-profile-engine.test.ts` | `26b4129a4f2f08d786bd4257afbf8e55ddcd0fd30d811e9dc0016bedc1073488` |
| compiler | `projects/domainspec-v2/impl/tools/minted-project/compiler.ts` | `6b21ac8091f564e7bcefd07637e111ea46ddc665275246d7eb051d5bd2bf9073` |
| build views | `projects/domainspec-v2/impl/tools/minted-project/views.ts` | `b411d40802ed0f94cc1cf783ae879b63f8dc0a366358a3e76c170eb3e91e9ea8` |
| memory repository | `projects/body-war/app/src/auth/memory-repository.ts` | `4f1ba3315621586640c6b8cafb03ae00715e58ad6a616745f01b21b86afb2ada` |
| repository contract | `projects/body-war/app/src/auth/body-war-repository.ts` | `3fd085deeb2fc716189d8dd1a945c21ec6aaab686b36c3ad907cadbc3f3d5815` |
| domain types | `projects/body-war/app/src/auth/types.ts` | `1ad27dcc659050682029f81e4938fcf65daf7e76711521a036cfcd1445bd29af` |

Generic DS-SFOL implementation modules under
`projects/domainspec-v2/impl/test-derivation-engine/src/sfol/` are selected as
read-only APIs. Their exact files are bound by the tool digest recorded in the
standalone proof receipt.

## Dependency boundary

`projects/body-war/development/task-sessions/SWU-BWOI-001/TASK-SESSION-RESULT.md`
at SHA-256
`0ef0597d91f7c96fb936d98f61c3d00729a26b6c9773f0a0fbb5347b1bad1e38`
is selected only as an ordering-gate receipt. Its proof inputs and outputs are
not selected. Semantic dependencies from the preceding proof lane or the
later composition lane are empty.

## Write boundary

Implementation writes are restricted to the DomainSpec subdirectory, the
consumer runner, its test, generated proof artifacts, and the standalone
receipt under:

`projects/body-war/proofs/suggested-track-ontology-domainspec/`

Task Session control and closeout evidence is restricted to:

`projects/body-war/development/task-sessions/SWU-BWOI-002/`

DomainSpec v2 and Body War app sources remain read-only.

## Claim ceiling

A passing receipt proves one experimental CT-2 seam against the current
memory adapter. It grants no release admission, production readiness,
promotion, deployment, or proof of the complete SuggestedTrack workflow.
