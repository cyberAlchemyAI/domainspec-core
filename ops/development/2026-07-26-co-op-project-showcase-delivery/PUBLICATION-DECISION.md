# Publication Decision — Co-Op Project Showcase

Status: approved for public review deployment

## Direct owner instruction

The user explicitly requested deployment through the Body War VPS pattern and
identified `cyberalchemize.com` as the available owned domain.

## Selected boundary

- Publish the existing single-source Co-Op page at
  `https://cyberalchemize.com/`.
- Reuse the proven secret-blind static Nginx/Traefik shape.
- Create an isolated `/srv/co-op-engine` directory, `coop-engine-site`
  container, and `coop-engine` router/service.
- Do not change TROQAR, `time-capsule.cyberalchemize.com`, their containers,
  databases, routers, application directories, or environment files.

## Claim boundary

The deployment changes reachability, not evidentiary status. The page remains
a public review prototype. It does not establish comprehension, delight,
recruitment effectiveness, current project-owner welcome, production product
readiness, or completion of any project it describes.

## Preconditions

- The apex resolves to the existing VPS and returns HTTP 404 before deploy.
- The Time Capsule subdomain returns HTTP 200 before deploy.
- The TROQAR host returns HTTP 200 before deploy.
- The Co-Op deployment package passes a dry run.
