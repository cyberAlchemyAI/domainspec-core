# Changelog

## 1.0.0

- Stabilizes the compiler, generated-project, verification, and Lean assurance surfaces.
- Exposes all six structured CLI authoring helpers from the package root.
- Adds `--help`, `--version`, `capabilities`, and `doctor` product surfaces.
- Moves runtime library exports to `@domainspec-v2/cli/experimental/runtime`.
- Adds bounded source/request inputs and bounded external tool execution.
- Adds portable, installed-package product verification.
- Adds stable deterministic `recipe-plan`, `recipe-generate`, and
  `recipe-verify` command surfaces for the candidate, no-effect
  `aws-ecs-fargate-postgres-v1` deployment-recipe capability.
- Ships closed deployment-recipe request, manifest, and receipt schemas plus
  OCI Dockerfiles, Terraform, PostgreSQL transactional-outbox migrations,
  operational contracts, and exact packed-consumer verification.

The package version records compatibility, not publication, deployment, Product Capability adoption, or authority.
