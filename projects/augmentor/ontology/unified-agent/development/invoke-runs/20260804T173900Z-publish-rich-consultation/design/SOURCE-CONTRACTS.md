# Design Source Contracts

| Owner | Owned source | Consumer | Invariant |
| --- | --- | --- | --- |
| Augmentor ontology/page owner | page template, explanations, compiler, generated consumer bundle | release packager and browser | Generated output is current; only reviewed neutral fields cross. |
| ResonantOS consultation owner | query/result/loader/cache/service modules and API reference | production API container and external agents | Contract family and atomic bundle closure remain exact `1.1.0`. |
| Deployment owner | release script, Compose, Nginx | production VPS | Existing path, auth hash, topology, rollback, and homepage isolation remain intact. |
| Validation owner | producer, consumer, docs, alpha, browser, packaging, remote checks | production operator and closeout | Each claim names its evidence layer; no local-to-production promotion. |
| Production operator | SSH session and remote release state | deployment script | Credentials remain outside files and receipts; external switch is explicit. |

## Required closure

The runtime loader reads:

1. `projection.json`
2. `glossary.json`
3. `projection-manifest.json`
4. `schemas/projection.schema.json`
5. `schemas/projection-manifest.schema.json`
6. `schemas/glossary.schema.json`
7. `schemas/explanation-support.schema.json`

The deploy packager must copy and verify all seven. The current two-file copy is
an observed blocker, not an accepted compatibility mode.

