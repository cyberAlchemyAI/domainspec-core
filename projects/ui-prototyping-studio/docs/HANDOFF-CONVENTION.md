# Prototype Gate Handoff Convention

Status: active contract

## Export Profile

Cross-project Studio handoffs use a JSON export profile. The profile tells the
core export operation which target feature docs the handoff should cite.

Example:

```json
{
  "profileId": "troqar-product-architecture",
  "storyRefs": [
    "projects/body-war/docs/features/troqar-product-architecture/SPEC.md"
  ],
  "requirementRefs": [
    "projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md#page-layout-and-profile"
  ],
  "acceptanceRefs": [
    "projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md#browser-e2e-obligations"
  ],
  "uiSpecRef": "projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md",
  "testSpecRef": "projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md",
  "sourceRefs": [
    "projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md"
  ]
}
```

## CLI Usage

```sh
STUDIO_DATA=<run-dir>/studio.json \
STUDIO_DOCS_ROOT=<repo-root> \
pnpm --dir projects/ui-prototyping-studio/backend studio handoff export <session-id> \
  --confirm \
  --profile <profile-json-path>
```

`STUDIO_DOCS_ROOT` is the base directory for relative profile paths and
relative source refs. For repo-local feature refs, set it to the repository
root.

## Bundle Fields

| Field | Meaning |
| --- | --- |
| `exportProfile` | Profile id or profile path used for the export. |
| `storyRefs` | Source feature story/spec refs. |
| `requirementRefs` | UI requirement refs that shaped the prototype. |
| `acceptanceRefs` | Test or acceptance refs that downstream implementation must satisfy. |
| `uiSpecRef` | Canonical UI spec consumed by the prototype. |
| `testSpecRef` | Canonical test spec consumed by the prototype. |
| `sourceRefs` | Additional source docs such as visual definitions or architecture notes. |
| `missingRefs` | Advisory refs not found under `STUDIO_DOCS_ROOT`; missing refs do not block export. |

## Handoff Summary

Each target project should store a readable summary beside its feature docs. The
summary should include:

- session id;
- accepted revision id;
- handoff bundle path;
- source `UI-SPEC.md` and `TEST-SPEC.md`;
- accepted prototype path;
- `data-od-id` coverage table;
- unresolved deviations or fallback selectors;
- next target-app task or SWU.

## Stability Rules

- Existing handoff exports without `--profile` keep the default
  `ui-prototyping-studio` refs.
- Profile refs are advisory. A missing ref is recorded as `missingRefs` rather
  than blocking export, because the recorded revision and baseline provenance
  are the irreversible handoff gate.
- The profile cannot bypass the `--confirm` requirement.
- Profile data never grants authority to mutate target app source.
