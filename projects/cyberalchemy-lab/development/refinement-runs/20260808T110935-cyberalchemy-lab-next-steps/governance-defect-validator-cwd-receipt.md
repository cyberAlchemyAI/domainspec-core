# Governance Defect Receipt: Validator CWD Path Mismatch

- Classification: governance-only, pre-execution Dispatch Spec validation defect
- Status: affected edge remains stopped; diagnosis and repair proposal only

## Root cause

`generate-refine-dispatch.py` writes `--output` using the caller-supplied `Path`, retains that same relative path as `dispatch_path`, and then starts the canonical validator with `cwd` set to the Arcanum root. For this run, the repository-relative argument `projects/cyberalchemy-lab/.../REFINE-DISPATCH.json` was therefore reinterpreted relative to `arcanum/`, even though the file had been written relative to the repository root. The validator opens its dispatch argument directly and performs no path rebasing. It consequently raised `FileNotFoundError` before route-shape validation and the generator correctly returned nonzero.

Evidence: `arcanum/arcana/refine/scripts/generate-refine-dispatch.py:230-244`; `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py:183-185,1080-1091`.

## Affected invariant

The `--validate` path must cause Dispatch Spec to validate the exact file just materialized, independent of the generator caller's working directory. Until that succeeds, the Refine contract requires a block before strategy preview, runtime-backed stages, subagents, or synthesis. The present failure proves neither route validity nor invalidity; validation never loaded the dispatch.

## Minimal current-run repair

Do not regenerate or edit `REFINE-DISPATCH.json`. Bind the retry to its current SHA-256, `c77ec1aa276b78966f53d7f7d93fe56b14329e03f2c97dfd2c9005eac10a8914`, then invoke the canonical validator directly with the dispatch's absolute path:

```text
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py /home/vrondelli/projects/domainspec-core/projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/REFINE-DISPATCH.json
```

This receipt does not execute that command. If the validator reports `pass` or `flag` with exit 0, the parent may prepare the required strategy preview. If it reports `block` or exits nonzero, keep the run stopped and preserve the diagnostic.

## Changed-byte inventory

- Added only this run-local receipt: `projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/governance-defect-validator-cwd-receipt.md`.
- No canonical or generated skill, generator, validator, dispatch, product, source-research, ontology, Inventory, telemetry, Git, or external-system bytes were changed by this sidecar.
- `REFINE-DISPATCH.json` existed before this sidecar and was read only; its observed size is 23,606 bytes and its observed SHA-256 is the digest above.

## Required revalidation

1. Recompute the dispatch SHA-256 and require an exact match with the bound digest before retrying.
2. Run the canonical Dispatch Spec validator against the absolute path and preserve its stdout, stderr, and exit status as one validation result; a later successful command must not mask failure.
3. Require exit 0 with `VALIDATION=pass` or `VALIDATION=flag` before treating the route as validation-complete. Treat `VALIDATION=block`, an exception, or nonzero exit as stopped.
4. Confirm that no runtime stage, delegated subagent, external research, implementation, or product mutation occurred before presenting the validated strategy.

## User confirmation

No renewed confirmation is required merely to retry this mechanical validation against unchanged bytes. The ordinary Refine confirmation is still outstanding: after successful validation, the parent must show the strategy preview and obtain explicit user permission before any runtime-backed stage runs. If any acceptance-bound dispatch byte changes, treat it as a new candidate and request confirmation against the new validated strategy.

## Permanent workflow regression fix

In a separately authorized change, normalize the written dispatch path to an absolute path before passing it to the validator, or preserve a single consistent path frame for both write and validation. Add a regression test that invokes the generator from the repository root with a repository-relative, newly created output outside `arcanum/`; the test must prove that the validator loads the exact emitted bytes, that validator stdout/stderr are retained, and that the generator propagates validator failure status unchanged. Include an untracked/create target so this gap fails before a future confirmation request.

## Authority ceiling

This receipt is diagnostic collaboration evidence only. It does not validate or approve the dispatch, authorize strategy execution, grant subagent or research permission, implement the CyberAlchemy Lab plan, change ontology or Inventory authority, promote or publish anything, or prove release, deployment, or production readiness.
