---
module: body-war-suggested-track-three-witness-verification
status: pass
updatedAt: 2026-07-27
docType: verification-report
---

# BWOI Verification Report

## Verdict

`TASK-BWOI-VERIFY` passes all eight declared checks. The result proves
reproducibility and claim-ceiling preservation for one experimental CT-2 seam.
It does not promote ontology, release DomainSpec, establish production parity,
or admit deployment.

## Preflight

- Selected task: `TASK-BWOI-VERIFY`
- Dependency receipts: ontology, DomainSpec, and integration Task Sessions all
  pass with joined owner receipts.
- Declared write scope: exactly this report, `RECEIPT-DIGESTS.json`,
  `RESIDUE.md`, and `TASK-SESSION-RESULT.md`.
- Proof sources and receipts: read-only in content; preflight tree digest
  `9831b688b7c10e0e19385486bc428fcaad71f3d1eb11689c74625932a36dc065`.
- CyberAlchemy ontology tree digest:
  `a09d9d54e0cc23e9c3ae4a35c1c04069fe1c83c8b8b123d700d2b968bd6ccc31`.
- DomainSpec v2 tree digest:
  `6e3dbb0c39f80a2cc4444bec9d3965db88cf00f3f4ce6aa8226e1583ae1da0f0`.
- Four future owner targets were captured before execution in
  `RECEIPT-DIGESTS.json`.

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Full proof suite run 1 | pass | 11/11 |
| Full proof suite run 2 | pass | 11/11 |
| Receipt digest equality | pass | all four file hashes identical before and after both runs |
| Fixture oracle scan | pass | no expected/oracle/verdict/acceptance/predicate/assert fields |
| Case identity | pass | all surfaces use `body-war.CT-2#return@campinas-suggested-track` |
| Claim ceilings | pass | four terminal receipts retain authority none and release not granted |
| Forbidden external trees | pass | CyberAlchemy ontology and DomainSpec v2 tree/status digests unchanged |
| Body War application | pass | 3/3 |
| Scoped diff hygiene | pass | no whitespace errors |
| Task write boundary | pass | only four declared verification artifacts created or updated |

## Reproducibility

The following file hashes were identical at preflight, after run 1, and after
run 2:

| Receipt | SHA-256 |
| --- | --- |
| ontology | `071e397041e3dfe9c0777c92dff20fa92ea63af61990b51ec1b13d2bf878dc88` |
| DomainSpec | `d1484bb6d8ee6a637e3eba4ee4b38336582b36fbf9ef901d087946415f46f756` |
| bridge admission | `c7e737627e736ac661b0e8b3f60db52d81b1612fbdad5e13c8b48a7836a62b20` |
| integration | `3f1400be86ca218a6266a89c800d1bb6845a2ca32ebcff122d8e14fb9c24993f` |

The proof-tree digest also remained exactly unchanged, demonstrating that the
test executions reproduced the receipts without content drift.

## Commands

```bash
(cd projects/domainspec-v2/impl && node --import tsx --test \
  ../../body-war/proofs/suggested-track-ontology-domainspec/tests/*.test.ts)
# executed twice

rg -n '"(expected|oracle|verdict|acceptance|predicate|assert)[^"]*"\s*:' \
  projects/body-war/proofs/suggested-track-ontology-domainspec/{ontology,domainspec,bridge}/fixtures

npm --prefix projects/body-war/app test
git diff --check -- projects/body-war
```

## Owner Closeout

Task Session execution is complete. Invoke Refresh must still join as the
separate lifecycle owner and may synchronize only the four captured planning
and Craft targets. The owner route has no successor and cannot promote,
release, publish, deploy, or accept product risk.
