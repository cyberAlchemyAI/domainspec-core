# CyberAlchemy Visual Identity Assets

This folder contains reusable visual identity assets for CyberAlchemy.

## Mark

Primary mark: [cyberalchemy-mark.svg](cyberalchemy-mark.svg)

The mark was derived from the agentic-system synthesis page and promoted into a reusable asset because it expresses the CyberAlchemy system model cleanly:

- outer circle: Saturn convergence loop and continuous alignment;
- triangle: alchemical transformation and structured ascent;
- curved arc: cybernetic feedback between intent and reality;
- central dot: preserved meaning, the kernel the system keeps translating;
- red-to-orange gradient: philosopher-stone red moving into cybernetic signal.

Use this mark for CyberAlchemy identity surfaces, shareable articles, docs covers, system diagrams, and lightweight navigation headers.

Do not use it to replace project-specific marks when a page already needs a specialized product identity. It is the shared CyberAlchemy system mark.

## Color System

Reusable color tokens live in [cyberalchemy-identity.css](cyberalchemy-identity.css).

The palette follows the existing CyberAlchemy pages:

| Token                     | Light     | Dark      | Role                                      |
| ------------------------- | --------- | --------- | ----------------------------------------- |
| `--cyberalchemy-bg`       | `#fdfaf3` | `#000000` | editorial page background                 |
| `--cyberalchemy-surface`  | `#f6f2e6` | `#111111` | panels and cards                          |
| `--cyberalchemy-text`     | `#1a1a1a` | `#ededed` | primary text                              |
| `--cyberalchemy-muted`    | `#62625b` | `#9a9a9a` | secondary text                            |
| `--cyberalchemy-red`      | `#e60023` | `#e60023` | primary CyberAlchemy accent               |
| `--cyberalchemy-red-deep` | `#cc0000` | `#ff4d4d` | gradient and emphasis accent              |
| `--cyberalchemy-orange`   | `#ea580c` | `#fb923c` | signal, feedback, and transition accent   |
| `--cyberalchemy-teal`     | `#0f766e` | `#2dd4bf` | system/operational knowledge accent       |
| `--cyberalchemy-blue`     | `#2563eb` | `#60a5fa` | bridge, traceability, and evidence accent |
| `--cyberalchemy-violet`   | `#7c3aed` | `#a78bfa` | operational ontology and agent work       |
| `--cyberalchemy-green`    | `#15803d` | `#4ade80` | governance and promoted knowledge         |

## HTML Usage

```html
<link rel="stylesheet" href="assets/cyberalchemy-identity.css" />
<img
  class="cyberalchemy-mark"
  src="assets/cyberalchemy-mark.svg"
  alt="CyberAlchemy mark"
/>
```

For standalone share files, inline the SVG from [cyberalchemy-mark.svg](cyberalchemy-mark.svg) so the document remains self-contained.
