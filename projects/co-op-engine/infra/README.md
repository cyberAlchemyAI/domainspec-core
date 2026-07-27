# Co-Op Engine static VPS deployment

This package reuses the isolated static-site pattern proven by Body War's
Hostinger/Traefik deployment and the existing Cyberalchemize Time Capsule
site.

It deploys the Co-Op page as its own service:

- public host: `cyberalchemize.com`;
- remote directory: `/srv/co-op-engine`;
- container: `coop-engine-site`;
- Traefik router/service: `coop-engine`;
- shared edge network: `troqar_edge`.

It does not share the TROQAR or Time Capsule application directories,
containers, routers, databases, or environment files.

## Deploy

Run the fail-closed dry run first:

```sh
DRY_RUN=1 projects/co-op-engine/infra/deploy-static-vps.sh
```

Then deploy:

```sh
projects/co-op-engine/infra/deploy-static-vps.sh
```

Only public routing values are written to the remote `.env`. The page has no
application secrets, database, form submission, analytics, tracking, or
external assets.

## Safety

The script refuses the TROQAR and Time Capsule hosts, refuses an unexpected
pre-existing remote directory, rotates the immediately previous site payload,
checks the container directly, and checks the public page title over HTTPS.
