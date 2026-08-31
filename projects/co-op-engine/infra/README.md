# Co-Op Engine static VPS deployment

This package reuses the isolated static-site pattern proven by Body War's
Hostinger/Traefik deployment and the existing Cyberalchemize Time Capsule
site.

It deploys the Co-Op page as its own service:

- public host: `cyberalchemize.com`;
- public routes: `/` for the collaboration portfolio, `/craft` for the Craft
  augmented-physics guide, `/bella` for the Direito Romano tower canvas, and
  `/agent-orchestration` for the beginner guided class, with the original
  `/agent-orchestration-guide` route retained;
- protected routes: `/domainspec/` for the private DomainSpec v2 guide and
  `/lucifers-lights-review/` for the Chapter 1 author-review pilot;
- remote directory: `/srv/co-op-engine`;
- container: `coop-engine-site`;
- Traefik router/service: `coop-engine`;
- shared edge network: `troqar_edge`.

It does not share the TROQAR or Time Capsule application directories,
containers, routers, databases, or environment files.

## Deploy

The protected Chapter 1 review scope below must establish the review generation
and verifier before any later agent-orchestration release. The legacy `full` and
`domainspec` rebuild scopes currently fail before remote effects: their bundle
path does not yet prove that it preserves the protected review generation and
verifier. Re-enable those scopes only after that preservation is implemented
and validated; do not route around the guard.

To release only the public agent-orchestration class, first run:

```sh
DEPLOY_SCOPE=agent-orchestration-guide DRY_RUN=1 \
  projects/co-op-engine/infra/deploy-static-vps.sh
```

Then repeat without `DRY_RUN=1`. This scope does not require either plaintext
password. It requires the deployed review file, its verifier, and its Compose
mount to already exist; otherwise it fails closed. It clones the active remote
`site` generation, removes any older copy of only
`/agent-orchestration-guide`, overlays the selected local HTML, proves every
other remote file (including the review page) stayed byte-identical, validates
Nginx against both existing verifiers, and prepares exact rollback snapshots
before the swap. It does not replace the Compose file, environment, verifier,
image, Traefik router, or TLS configuration. Override
`AGENT_ORCHESTRATION_GUIDE_FILE` only to select an equivalent reviewed source
artifact.

The shorter `/agent-orchestration` route serves the same deployed file as
`/agent-orchestration-guide`; it does not create a second content copy. Slash
and `index.html` variants redirect to their corresponding clean route.

To publish only the exact reviewed Chapter 1 pilot behind its own credentials,
create a one-line password file containing at least 16 characters, then run:

```sh
LUCIFERS_LIGHTS_AUTH_PASSWORD_FILE=/absolute/path/to/review-password \
  DEPLOY_SCOPE=lucifers-lights-review DRY_RUN=1 \
  projects/co-op-engine/infra/deploy-static-vps.sh
```

Repeat without `DRY_RUN=1` only after the dry run passes. The username defaults
to `lucifers-review` and can be changed with
`LUCIFERS_LIGHTS_AUTH_USERNAME`; it must differ from the DomainSpec username.
The review password file must also be distinct from any supplied DomainSpec
password file. The script generates a salted verifier locally, uploads only the
verifier, and uses it solely for this review route.

This scope accepts only the pinned Chapter 1 review page with SHA-256
`b396c162b70e0866014350a78dda2a8e3ecba77248cb9d1c2bdd494e1ddeab7c`.
It clones the active remote site, replaces only
`/lucifers-lights-review/index.html`, proves every other site file stayed
byte-identical, validates the Nginx and Compose candidates with both independent
verifiers, snapshots the complete rollback generation, and checks the
authenticated HTTPS response against the same digest. Override
`LUCIFERS_LIGHTS_REVIEW_FILE` only to point at byte-identical reviewed content.
The page sends no network requests; review notes remain in that browser's local
storage until the reviewer downloads them.

The inactive `domainspec` and `full` implementation remains in the script as
historical deployment logic, but the early scope guard prevents it from
rebuilding the site while review-route preservation is unproven.

Only public routing values are written to the remote `.env`; the DomainSpec
password never enters it. The public pages have no application secrets,
database, form submission, analytics, tracking, or external assets. The Craft
route is packaged directly from
`arcanum/development/user-guide/craft-augmented-physics.html`, so the deployment
does not introduce a second source copy. The Bella route follows the same rule:
it packages the tested `../direito-romano/learning-graph/FAST-TOWER-GRAPH.html`
adjacent-project source directly. Set `BELLA_SITE_FILE` only when an equivalent
workspace layout is unavailable.

The DomainSpec route packages the four committed `COMPLETE-GUIDE` artifacts
directly from `projects/domainspec-v2`. The HTML is available both as the route
index and as `COMPLETE-GUIDE.html`; the Markdown, lanes manifest, and schema are
available beside it after authentication. Links into the wider private
repository intentionally remain unavailable on the deployed site.

`DOMAINSPEC_AUTH_PASSWORD_FILE` is mandatory and must contain one password line
with at least 16 characters. The username defaults to `domainspec-guide` and
can be changed with `DOMAINSPEC_AUTH_USERNAME`. The script generates the
salted `htpasswd` entry locally, uploads only that verifier, and never writes
the plaintext password to the server. Open `https://cyberalchemize.com/domainspec/`
in a browser and enter those credentials when prompted.

## Safety

The script refuses the TROQAR and Time Capsule hosts, refuses an unexpected
pre-existing remote directory, rotates the immediately previous site payload,
and restores the previous payload and routing files if startup or HTTPS
validation fails. It checks the container directly, proves the three existing
public routes still match their selected source bytes, requires anonymous
DomainSpec requests to return `401`, verifies every authenticated guide file by
SHA-256, confirms that the Nginx worker can read every deployed file and the
password verifier, and confirms that the wider private source tree is not
deployed.

Basic Auth protects content transported over HTTPS; it does not make the route
name undiscoverable. The review route additionally sends `noindex`, `noarchive`,
`no-referrer`, and private `no-store` headers, but this is still a bounded author
preview rather than manuscript acceptance or production publication. Neither
protected route is evidence that DomainSpec or the novel is released or
production-ready. Because these previews share an origin with the public pages,
they are weaker isolation than dedicated protected hosts. Their pre-release
claim boundaries remain in force.
