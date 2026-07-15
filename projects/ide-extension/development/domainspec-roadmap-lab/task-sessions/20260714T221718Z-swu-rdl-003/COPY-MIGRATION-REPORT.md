# Copy Migration Report: SWU-RDL-003

## Before

The roadmap template owned the dynamic presentation copy in JavaScript
constants:

- `NODE_COPY`: 16 node titles and 16 node summaries.
- `STATUS_COPY`: 11 rendered state labels.
- `FRONTIER_COPY`: 5 frontier titles and 5 frontier summaries.
- `STEP_COPY`: 14 critical-step labels.

The template also had permissive runtime fallbacks:

- missing node copy could fall back to source node title/id plus
  `Read the exact contract below.`;
- missing frontier copy could fall back to frontier id/condition;
- missing critical-step copy could fall back to step id;
- missing status copy could fall back to raw state.

## After

`roadmap-copy.json` owns the migrated presentation-only fields:

| Target kind | Roles | Count |
| --- | --- | ---: |
| node | title, summary | 32 |
| status | status-label | 11 |
| frontier | title, summary | 10 |
| critical-step | label | 14 |
| total |  | 67 |

The builder derives required copy from the live manifest and current node
states, rejects missing/duplicate/unknown/unused copy, and emits the validated
copy model under `roadmap-data.json#/copy`.

The template now reads `data.copy` and throws on missing migrated copy instead
of falling back to technical authority fields.

## Generated Output Diff Explanation

`roadmap-data.json` changed because it now embeds the validated `copy` model and
coverage summary. `roadmap.html` changed because the embedded data contains the
same copy model and the template consumes it instead of local constants.

Visible roadmap wording is intentionally preserved for the migrated fields:

- `copy.node.FPR-01.title` remains `Establish one trusted baseline`;
- `copy.node.FPR-01.summary` remains the current baseline explanation;
- `copy.frontier.FR-FPR-ONTOLOGY-DIRECTION.title` remains
  `Which direction does meaning flow?`;
- `copy.critical-step.CP-01-candidate-identity.label` remains
  `Identify the exact candidate`;
- `copy.status.blocked-open.status-label` remains `Open and blocking`.

## Validation Evidence

- `roadmap-copy.json` parses as JSON and contains 67 fields.
- Generated coverage: `required_fields=67`, `provided_fields=67`,
  `missing_fields=0`, `unused_fields=0`.
- `python3 -m unittest discover -s projects/domainspec-v2/development/first-production-release/visibility/tests` passed 22 tests.
- `python3 projects/domainspec-v2/development/first-production-release/visibility/tools/build-roadmap.py --check` reported synchronized outputs after regeneration.
- Scans found no `/home/vrondelli` absolute path and no migrated fallback strings
  in generated data, generated HTML, or the template.
