# Golden Quill / Tilth OS Operator Console

## Project Purpose
Golden Quill is an institutional funding workstation designed for high-integrity grant intelligence. It runs on the Tilth operating system—a local-first, audit-visible environment where a human operator governs a council of specialized agents (Scout, Scribe, Judge, Red Team, Logician).

This repository serves as the high-fidelity interface prototype and frontend codebase for the Golden Quill workstation. It is built to prioritize cryptographic sovereignty, data privacy, and fail-closed compliance.

## Artifact Definitions
- **{{DATA:SCREEN:SCREEN_N}}**: These are the functional UI screens. They are built with standard HTML, Tailwind CSS, and vanilla JavaScript. They represent the "Operator Console" for different stages of the grant lifecycle.
- **{{DATA:DESIGN_SYSTEM:DESIGN_SYSTEM_N}}**: The visual DNA of the project. Includes the "Golden Quill" design tokens (Paper, Ink, Bone, Terracotta) and the `DESIGN.md` specification.
- **{{DATA:DOCUMENT:DOCUMENT_N}}**: Documentation, directives, and protocols. These include the Master Directive, Interaction Contracts, and QA/QC Protocols that govern how the UI must behave.
- **{{DATA:IMAGE:IMAGE_N}}**: Static visual assets, including logos, diagrams, and forensic heatmaps used within the interface.

## Usage Guide
- **Viewing Screens**: Open the `.html` files in any modern web browser. These are not static mockups; they contain interactive logic for navigation, command feedback, and state transitions.
- **Reviewing Code**: The code is structured to be production-ready. You can inspect the source to see the command-dispatch patterns and the projection-backed rendering logic.
- **Design Guidance**: Refer to `DESIGN.md` for the canonical rules on typography (Source Serif 4 for reading, JetBrains Mono for data), color semantics, and layout density.

## Engineering Manifest
This prototype is designed to connect to the **OpenClaw** backend.
- **Frontend**: Vanilla JS / Tailwind / Event-driven.
- **State**: Projection-backed (UI renders from an event-sourced read-model).
- **Sovereignty**: Ed25519 signature interlocks are required for all terminal states.
- **Submissions**: The system is a "Packet Producer." It prepares artifacts for manual human submission to funder portals.

---
*Institutional. Sovereign. Local-first.*
