---
module: domainspec-core
status: active
updatedAt: 2026-05-19
docType: vscode-workspace-colors
---

# VS Code Workspace Colors

This directory contains VS Code workspace launchers for the main contexts inside `domainspec-core`.

Open a `.code-workspace` file instead of opening the raw folder when you want a distinct window color and title.

## Usage

From the repository root:

```bash
code vscode-workspaces/cyberalchemy.code-workspace
code vscode-workspaces/arcanum.code-workspace
code vscode-workspaces/domainspec-implementation.code-workspace
```

If title bar colors do not appear, set this in your VS Code user settings:

```json
{
  "window.titleBarStyle": "custom"
}
```

## Workspace Palette

| Workspace                 | File                                                                                 | Color Family |
| ------------------------- | ------------------------------------------------------------------------------------ | ------------ |
| DomainSpec Core           | [domainspec-core.code-workspace](domainspec-core.code-workspace)                     | teal         |
| CyberAlchemy              | [cyberalchemy.code-workspace](cyberalchemy.code-workspace)                           | violet       |
| Arcanum                   | [arcanum.code-workspace](arcanum.code-workspace)                                     | red/gold     |
| DomainSpec Implementation | [domainspec-implementation.code-workspace](domainspec-implementation.code-workspace) | blue         |
| MARS Implementation       | [mars-implementation.code-workspace](mars-implementation.code-workspace)             | amber        |
| Research                  | [research.code-workspace](research.code-workspace)                                   | cyan         |
| Docs And Signals          | [docs-signals.code-workspace](docs-signals.code-workspace)                           | slate        |
| Sigils Library            | [sigils-library.code-workspace](sigils-library.code-workspace)                       | purple       |
| Equalizator               | [equalizator.code-workspace](equalizator.code-workspace)                             | sky          |
| POS Multilevel            | [pos-multilevel.code-workspace](pos-multilevel.code-workspace)                       | rose         |
| Sonar Loop                | [sonar-loop.code-workspace](sonar-loop.code-workspace)                               | emerald      |
| Poker Team Validation     | [poker-team-validation.code-workspace](poker-team-validation.code-workspace)         | orange       |
| Sigil Spell Sandbox       | [sigil-spell-sandbox.code-workspace](sigil-spell-sandbox.code-workspace)             | lime         |
| Ops And Tools             | [ops-tools.code-workspace](ops-tools.code-workspace)                                 | neutral gray |

## Notes

- These files do not change project code.
- Colors are workspace-local and apply only when opening the `.code-workspace` file.
- The CyberAlchemy workspace includes the original `cyberAlchemy` folder,
  `cyberAlchemy-v2`, and the standalone `resonantos-economy-research` research
  repository so economy research can continue alongside its method authority.
- The nested git repositories found during setup were root `domainspec-core`, `arcanum`, and `validation/sigil-spell-sandbox`; the other files are major working contexts.
