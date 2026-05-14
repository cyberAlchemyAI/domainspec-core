# Cross-Task Gaps and Questions

## Resolved During Planning

| ID     | Question                           | Resolution                                                                             | Applies To |
| ------ | ---------------------------------- | -------------------------------------------------------------------------------------- | ---------- |
| GQ-001 | Should L0 include external export? | No. L0 creates local repository tasks only; GitHub/Jira export begins after POC proof. | W1, W3     |
| GQ-002 | Should L2 and L3 merge?            | No. Governance hardening and scale fit remain separate waves.                          | W3, W4     |

## Open Execution Gaps

| ID     | Gap                                                                         | Required Handling                                                                                                              | Owning Task                                                                                                          |
| ------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| GQ-003 | Concrete source tree and package names are not defined in the feature docs. | W0 must inspect target implementation workspace before source mutation and record chosen module paths in task execution notes. | [../tasks/TASK-W0-BASELINE.md](../tasks/TASK-W0-BASELINE.md)                                                         |
| GQ-004 | Sonar runtime credentials and project keys are not specified.               | Treat as adapter/config inputs; do not bake secrets into domain/application code.                                              | [../tasks/TASK-L0-POC.md](../tasks/TASK-L0-POC.md), [../tasks/TASK-L2-GOVERNANCE.md](../tasks/TASK-L2-GOVERNANCE.md) |
| GQ-005 | GitHub/Jira API configuration references are not specified.                 | L0 avoids external export; L2 must require explicit config refs before API adapter execution.                                  | [../tasks/TASK-L2-GOVERNANCE.md](../tasks/TASK-L2-GOVERNANCE.md)                                                     |
| GQ-006 | OTel exporter backend is not specified.                                     | Instrument through ports and verify telemetry shape; defer concrete backend/deploy choices.                                    | [../tasks/TASK-OTEL.md](../tasks/TASK-OTEL.md)                                                                       |

## Link Validation Obligation

Every created or updated markdown file in this work-pack must be validated one file at a time with `./tools/guard ./tools/check_markdown_links.sh <single-file>`.
