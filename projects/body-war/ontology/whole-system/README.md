# Body War whole-system ontology

This candidate-local package composes three views without changing their authority:

- the existing `../business/` ontology, imported by exact digest;
- a new observed `system` branch for the runtime, persistence, endpoints, tests, and deployment topology;
- a `business-system-bridge` branch that records supported, partial, and missing realizations.

`source-universe.json` accounts for every Git-tracked file below `projects/body-war` at generation time, excluding this package so the manifest cannot digest itself. Complete evidence coverage is intentionally different from making one ontology node per file.

## Generate and validate

```bash
node projects/body-war/ontology/whole-system/scripts/generate.mjs
node projects/body-war/ontology/whole-system/scripts/validate.mjs
node --test projects/body-war/ontology/whole-system/tests/whole-system-ontology.test.mjs
```

Human entry point: [`NODE-INDEX.md`](NODE-INDEX.md).

## Display in the Ontology Evidence Workbench

The `frontend/` directory is a deterministic compatibility projection of the full ontology into the retained, validated OEW prototype. It contains all 276 nodes and 301 relations, arranged into 29 clusters with six tour steps and one accessible color per exact source predicate. Rich system kinds remain visible as tags and card metadata; the projection does not rewrite the source ontology.

```bash
node projects/body-war/ontology/whole-system/scripts/generate-oew-frontend.mjs
node projects/body-war/ontology/whole-system/scripts/validate-oew-frontend.mjs
node --test projects/body-war/ontology/whole-system/tests/whole-system-oew-frontend.test.mjs
node projects/body-war/ontology/whole-system/scripts/serve-oew-frontend.mjs
# In another terminal while the server is running:
node projects/body-war/ontology/whole-system/scripts/validate-oew-frontend-browser.mjs
```

Open `http://127.0.0.1:4178/` for the focused login-to-score scene and labeled boundary portals. Open `http://127.0.0.1:4178/?oew=1` for a curated four-node exact-relation scene; use **Full index** or **Full outline** there to browse all 276 nodes and 301 relations without drawing them simultaneously. Each selected relation preserves its exact predicate color. The loopback server makes no external requests; its local read-only token is presentation bootstrap only and is not a credential.

The package has `authority_effect: none`. It does not promote the ontology, admit DomainSpec execution, prove live Strava import, supply route geometry, calculate verified score, deploy the application, or establish production readiness.
