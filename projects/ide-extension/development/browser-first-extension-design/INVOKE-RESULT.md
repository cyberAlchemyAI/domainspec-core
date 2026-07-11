---
id: ide-extension-browser-first-invoke-result
project: ide-extension
title: "Invoke Result - Browser-First Extension Design"
status: flag
node_type: invoke-result
updatedAt: 2026-07-10
invoke_mode: design
run_id: invoke-20260710T020244Z-browser-first-extension-design
---

# Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: flag
- Mode contract: `.agents/skills/invoke/design.md`
- Outputs: `projects/ide-extension/development/browser-first-extension-design/ARCHITECTURE-BUNDLE.md`, `projects/ide-extension/development/browser-first-extension-design/GLOSSARY-CONSISTENCY.md`, `projects/ide-extension/development/browser-first-extension-design/DESIGN-TRANSPORT.md`, `projects/ide-extension/development/browser-first-extension-design/IMPLEMENTATION-LAYERING-SEED.md`, `projects/ide-extension/development/browser-first-extension-design/browser-first-extension.dispatch.json`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: discovery-mode DomainSpec architecture bundle shape plus browser-first architecture companion evidence
- Dispatch techniques: `sequence`, `concrete_path_evidence`, `owner_boundary_check`, `artifact_contract_bridge`, `protected_action_mapping`, `approval_semantics_map`, `state_namespace_boundary`, `execution_receipt_handoff`, `validation_loop`, `residue_ledger`, `scu_swu_reduction`, `recomposition_proof`; dispatch validation `pass`
- Distill validation: pass; refreshed smallest coherent unit is the L0.5 offline MCP/chat adapter-admission harness; Chrome MV3 is the later L0.6 browser-first lane
- Implementation layering: `projects/ide-extension/development/browser-first-extension-design/IMPLEMENTATION-LAYERING-SEED.md`
- Work-pack: n/a
- Complexity: medium
- Per-layer planning: compact seed only; no execution tasks emitted
- Implementation detail: design-level component contracts only; task specs deferred to plan
- Smallest working units: n/a
- Refresh: n/a
- Target artifact: `ide-extension adapter admission and browser-first extension lanes`, type `architecture/design`, owner `projects/ide-extension`
- Template or recipe selection: Invoke design mode using architecture bundle template shape; no candidate template promotion
- Decisions: offline `McpChatWitnessAdapter` is the first L0.5 admission proof; Chrome MV3 extension is the later real browser-control lane; local HTML remains UI source; local kernel remains authority; VSCodium wrapper, Playwright MCP, Chrome DevTools MCP, Kernel Cloud, Yocoolab, and `claude-max-mcp` are deferred lanes/specimens
- Unresolved gaps: no standalone glossary; no MCP/chat admission harness yet; no `DesignFeedbackContextPacket` schema/fixture yet; no fake stdio MCP witness server yet; adapter descriptor registration/custody validation missing; no Chrome extension files yet; bridge token/config generation missing; browser-action receipt schema extension deferred behind `evidence_refs`; side-panel framing needs witness; Playwright MCP and VSCodium wrapper deferred
- Next route: plan
