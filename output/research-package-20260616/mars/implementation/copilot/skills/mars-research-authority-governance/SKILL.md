---
name: mars-research-authority-governance
description: "Govern authoritative references for research projects: enforce immutable pins, waiver lifecycle, ledger consistency, and inventory linkage before G2/G3-sensitive execution."
argument-hint: "<project-key> [--audit|--normalize|--waivers|--promote]"
agent: mars-research-sourcer
allowed-tools: Read, Write, Bash, Glob, Grep, Fetch
---

<objective>
Keep authority references auditable and execution-safe.

This skill standardizes reference governance across research projects by enforcing:
- pin quality,
- authority status consistency,
- waiver controls,
- inventory linkage for primary authorities.
</objective>

<context>
Target project contracts:
- `research/projects/<project-key>/sources/SOURCE-CATALOG.md`
- `research/projects/<project-key>/sources/REFERENCE-LEDGER.md`
- `research/projects/<project-key>/sources/REFERENCE-WAIVERS.md` (if present)
- `research/projects/<project-key>/inventory/INVENTORY-INDEX.md`
- `research/projects/<project-key>/experiments/*/sources.md`

Policy references:
- `implementation/mars/definitions/RESEARCH-KNOWLEDGE-STACK-CONTRACT.md`
- `implementation/mars/definitions/MARS-PIPELINE.md`
</context>

<process>
1. Resolve target project and read source contracts first.
2. Build authority matrix by combining ledger, source catalog, and per-experiment source selections.
3. Validate pin quality.
   - Allowed immutable patterns (examples): `sha256-*`, `commit-*`, `release-*`, `tag-*`, `isbn-*`, `doi-*`, `archive-*`.
   - Flag mutable or ambiguous pins (examples: `pending`, `tbd`, `snapshot-*`, `docs-current`).
4. Validate status coherence.
   - `operationalized`: source + pin + required linkage present.
   - `waived`: explicit waiver entry, reason, and expiry trigger present.
   - `pending normalization`: temporary state requiring remediation.
5. Validate inventory linkage for primary authorities.
   - Primary references used by protocols must map to inventory entries or approved waiver policy.
6. Normalize artifacts.
   - Update ledger status rows.
   - Add or update waiver records when temporary exceptions are unavoidable.
   - Emit remediation queue for unresolved pin/linkage defects.
7. Return governance verdict for gate readiness implications:
   - `ready` when authority set satisfies G2/G3 expectations.
   - `needs-revision` when non-blocking metadata drift exists.
   - `blocked` when primary authorities are unpinned or unlinked.
</process>

<quality-bar>
- No primary authority may be `operationalized` without pin + linkage evidence.
- Waivers must include explicit reason, scope, and expiry trigger.
- Status vocabulary must be consistent across ledger and waivers.
- Remediation output must cite exact source IDs and files.
</quality-bar>

<output-contract>
Return:

```markdown
## Authority Governance Summary
- Project: <project-key>
- References audited: <n>
- Operationalized: <n>
- Waived: <n>
- Pending normalization: <n>
- Gate readiness: ready | needs-revision | blocked

### Blocking Items
1. <source-id / reference-id + reason>

### Remediation Actions
1. <action>
2. <action>
```
</output-contract>
