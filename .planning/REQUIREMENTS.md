# Requirements: DomainSpec Documentation and Packaging Sync

**Defined:** 2026-04-21
**Core Value:** Maintainers and adopters can trust that documented commands, templates, and install instructions match shipped assets.

## v1 Requirements

### Main README and Reference Sync

- [ ] **DOC-01**: Main framework README reflects shipped skills, pipeline behavior, and current changelog reference.
- [ ] **DOC-02**: Root mirror README content remains synchronized with canonical implementation README.

### Copilot Documentation Sync

- [ ] **DOC-03**: Copilot README command and agent tables match shipped assets.
- [ ] **DOC-04**: INSTALL guide describes installer behavior, GSD bridge dependencies, and post-install verification accurately.

### Packaging and Governance

- [ ] **PKG-01**: Bridge skills required by planner and implementer references are present in distributable copilot skills.
- [ ] **GOV-01**: Drift detection exists for docs versus shipped assets to prevent future divergence.

## v2 Requirements

### Optional Enhancements

- **GOV-02**: CI gate for documentation drift runs automatically in pull requests.

## v3 Requirements

### Harness Minimal Profile and Durable Promotion

- [ ] **HARN-01**: Harness planning and execution start with a minimal profile path that is fast, deterministic, and lower-cost to operate than durable orchestration.
- [ ] **HARN-02**: Runtime dispatch and harness orchestration remain separated through a clean adapter boundary so Temporal can be integrated later without rewriting harness foundations.
- [ ] **HARN-03**: Durable profile promotion is blocked unless at least one trigger is present: resumable long-running flows, human-in-loop pause/resume requirements, or strict crash-recovery guarantees.
- [ ] **HARN-04**: Promotion and migration criteria include traceable evidence updates in roadmap, traceability, and completeness artifacts.

## Out of Scope

| Feature                                         | Reason                                                    |
| ----------------------------------------------- | --------------------------------------------------------- |
| Domain model or taxonomy changes                | Not required to resolve documentation and packaging drift |
| Runtime behavior changes in downstream projects | This effort targets framework docs and pack integrity     |
| New product features                            | Scope is alignment, not feature expansion                 |

## Traceability

| Requirement | Phase   | Status  |
| ----------- | ------- | ------- |
| DOC-01      | Phase 1 | Pending |
| DOC-02      | Phase 1 | Pending |
| DOC-03      | Phase 1 | Pending |
| DOC-04      | Phase 1 | Pending |
| PKG-01      | Phase 1 | Pending |
| GOV-01      | Phase 1 | Pending |
| HARN-01     | Phase 2 | Pending |
| HARN-02     | Phase 2 | Pending |
| HARN-03     | Phase 2 | Pending |
| HARN-04     | Phase 2 | Pending |

**Coverage:**

- v1 + v3 requirements: 10 total
- Mapped to phases: 10
- Unmapped: 0

---

_Requirements defined: 2026-04-21_
_Last updated: 2026-04-21 after initial definition_
