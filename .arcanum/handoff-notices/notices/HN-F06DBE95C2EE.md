# Handoff Notice: Validated durable Invoke ontology package and CAV2 public-export boundary

- Code: `HN-F06DBE95C2EE`
- Status: `open`
- Type: `outgoing`
- To: domainspec-core repository owner (`owner-route`)
- From: Invoke ontology package lane (`agent-lane`)
- Project scope: `arcanum/ontology/invoke`
- Created: `2026-08-20T19:23:33Z`
- Digest: `f06dbe95c2eee1d2078d232fab4f99bc93da4192d24cbe9f7a4bdaa61bb1bc8f`
- Remote availability: `unverified`

## Why Now

The public Arcanum implementation is validated and pushed; the private parent now needs a durable locator for the exact package receipt, migration provenance, authority boundary, and remaining lifecycle decision.

## Key Points

- Arcanum commit 66888b7d48258a8c4fbc44b13864c2446d2c16bb contains the canonical Ontology Vault receipt-versus-package behavior and the Invoke package candidate.
- The Invoke package passes canonical, Codex-generated, and Claude-generated validators with material digest 094b52ac70444484ef9e46f812e7a460f619c71f4a2fa1ce40c2bf49f261ae6d.
- The public export is mechanically limited to 13 CAV2 definition contracts and 7 model contracts; private paths, source digests, proofs, source scripts, unrelated-system material, and authority claims fail closed.
- The three legacy Invoke receipts remain byte-identical and their exact private provenance is retained only in the private parent migration receipt.

## Open Calls

- [open] Invoke lifecycle owner: Should the validated Invoke ontology remain a candidate or enter a separately governed promotion and publication decision?

## Boundaries

- This notice and locator are communication evidence only and grant no authority.
- The ontology does not decide promotion, publication, runtime conformance, release admission, or canonical definition ownership.
- Do not expand the public export beyond the allowlisted definition and model contracts or expose private proofs, source scripts, paths, digests, or other-system evidence.
- Runtime realization and full relation-envelope conformance remain explicit residue rather than inferred facts.

## Next Actions

- domainspec-core repository owner: Review the pushed parent and Arcanum commits and preserve the candidate and authority status recorded by the validation receipt.
- Invoke lifecycle owner: Resolve the open lifecycle decision through a separately authorized promotion or publication route if advancement is desired.

## Source References

- `arcanum@66888b7d48258a8c4fbc44b13864c2446d2c16bb` — Pushed public Arcanum implementation commit
- `arcanum/ontology/invoke/receipts/validation-094b52ac70444484.json` — Deterministic Invoke package validation receipt
- `arcanum/arcana/ontology-vault/contracts/cav2-public-export-policy.json` — Mechanically enforced public-export boundary
- `.arcanum/ontology-vault/migrations/invoke-public-package-export.json` — Private source-rebinding and migration provenance receipt

## Suggested Next Route

- Capability: `decision-gate`
- Mode: `owner-review`
- Target: `Invoke ontology candidate lifecycle status`
- Authorization: `not-granted`

## Terminal Receipt

- `arcanum/ontology/invoke/receipts/validation-094b52ac70444484.json`

## Authority Boundary

This notice is communication evidence only. The notice and locator grant no permission, authenticate no actor, resolve no open call, select no task, and authorize no mutation, dispatch, Git publication, or external delivery.
