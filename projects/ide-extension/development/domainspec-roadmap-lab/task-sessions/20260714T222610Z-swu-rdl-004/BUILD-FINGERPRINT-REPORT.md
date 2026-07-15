# Build Fingerprint Report: SWU-RDL-004

## Fingerprint Contract

- Version: `roadmap-build-inputs.v1`
- Current fingerprint:
  `sha256:7564ba17043fb1905afb5e0dbb8668a87d17c94eea80ea827cde32157dffd25d`
- Hash input: deterministic JSON bytes of the embedded build-input manifest.
- Excluded: timestamps, absolute paths, generated output paths, and local temp
  paths.

## Embedded Inputs

The build manifest includes SHA-256 references for:

- roadmap projection manifest;
- Craft continuation ledger;
- presentation copy file;
- accepted decision source;
- research evidence source;
- approved findings source;
- roadmap source.

The presentation-copy input currently resolves to:

```json
{
  "role": "presentation copy",
  "path": "projects/domainspec-v2/development/first-production-release/visibility/roadmap-copy.json",
  "sha256": "sha256:5da7198a078fb2c7d50caa0e8b17e9934cb5e2278e5e0b85b5cd06b872cbfcf1"
}
```

## Rendered Selectors

The embedded manifest includes:

- 16 rendered node ids;
- 5 rendered frontier ids;
- 14 critical-step ids;
- 11 status ids;
- 67 copy field ids;
- FPR-01 proposal-relevant field ids:
  - `copy.node.FPR-01.summary`
  - `copy.node.FPR-01.title`

Coverage remains:

```json
{
  "required_fields": 67,
  "provided_fields": 67,
  "missing_fields": 0,
  "unused_fields": 0
}
```

## Mutation Proof

Focused builder tests prove that the fingerprint changes when any material
input changes:

| Input mutation | Proof |
| --- | --- |
| roadmap manifest content | `test_material_input_mutations_change_fingerprint` |
| Craft ledger content | `test_material_input_mutations_change_fingerprint` |
| presentation-copy content | `test_material_input_mutations_change_fingerprint` |
| declared source file content | `test_declared_source_content_mutation_changes_fingerprint` |

## Deterministic Build Proof

Two unchanged builder runs produced byte-identical outputs:

- `roadmap-data.json`: `b77f26be55a8e1a41d580fba9da10bb4f417a8adbdedfc3c189993c013768832`
- `roadmap.html`: `e2afe8f8cd9d095393c44bc66dd11166a2ea0fde275cd77d235e4b33a30a4039`

## Validation Evidence

- `python3 -m unittest discover -s projects/domainspec-v2/development/first-production-release/visibility/tests -p 'test_build_roadmap.py'` passed 14 tests.
- `python3 -m unittest discover -s projects/domainspec-v2/development/first-production-release/visibility/tests` passed 25 tests.
- `python3 projects/domainspec-v2/development/first-production-release/visibility/tools/build-roadmap.py --check` reported synchronized outputs after regeneration.
- No `/home/vrondelli`, `/tmp/`, or temp output path was embedded in generated data or HTML.
