# Co-Op Engine static VPS deployment

This package reuses the isolated static-site pattern proven by Body War's
Hostinger/Traefik deployment and the existing Cyberalchemize Time Capsule
site.

It deploys the Co-Op page as its own service:

- public host: `cyberalchemize.com`;
- public routes: `/` for the collaboration portfolio, `/craft` for the Craft
  augmented-physics guide, `/bella` for the Direito Romano tower canvas, and
  `/agent-orchestration-guide` for the beginner guided class;
- protected route: `/domainspec/` for the private DomainSpec v2 guide;
- remote directory: `/srv/co-op-engine`;
- container: `coop-engine-site`;
- Traefik router/service: `coop-engine`;
- shared edge network: `troqar_edge`.

It does not share the TROQAR or Time Capsule application directories,
containers, routers, databases, or environment files.

## Deploy

Run the fail-closed dry run first:

```sh
DOMAINSPEC_AUTH_PASSWORD_FILE=/absolute/path/to/domainspec-password \
  DEPLOY_SCOPE=domainspec DRY_RUN=1 \
  projects/co-op-engine/infra/deploy-static-vps.sh
```

Then deploy:

```sh
DOMAINSPEC_AUTH_PASSWORD_FILE=/absolute/path/to/domainspec-password \
  DEPLOY_SCOPE=domainspec \
  projects/co-op-engine/infra/deploy-static-vps.sh
```

To release only the public agent-orchestration class, first run:

```sh
DEPLOY_SCOPE=agent-orchestration-guide DRY_RUN=1 \
  projects/co-op-engine/infra/deploy-static-vps.sh
```

Then repeat without `DRY_RUN=1`. This scope does not require the DomainSpec
password. It clones the active remote `site` generation, removes any older copy
of only `/agent-orchestration-guide`, overlays the selected local HTML, proves
every other remote file stayed byte-identical, validates Nginx against the
existing verifier, and prepares exact rollback snapshots before the swap. It
does not replace the Compose file, environment, verifier, image, Traefik router,
or TLS configuration. Override `AGENT_ORCHESTRATION_GUIDE_FILE` only to select an
equivalent reviewed source artifact.

`DEPLOY_SCOPE=domainspec` captures the four current public responses and
repackages those exact bytes, so a private-guide-only release cannot
accidentally publish unrelated local work in `/`, `/craft`, `/bella`, or
`/agent-orchestration-guide`. Omit it, or set `DEPLOY_SCOPE=full`, only when the
selected local sources for every route are intentionally being released
together.

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
name undiscoverable and is not evidence that DomainSpec itself is released or
production-ready. Because this preview shares an origin with the public pages,
it is weaker isolation than a dedicated protected host. The guide retains its
pre-release claim boundaries.
