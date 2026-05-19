---
id: digest.arcanum_observed_invocation_reflection
sourceArea: arcanum
sourcePaths:
  - arcanum/spells/observed-invocation-loop/README.md
  - arcanum/arcana/workflow-reflect/README.md
  - arcanum/spells/sigil-maintenance-loop/README.md
status: candidate-digest
updatedAt: 2026-05-19
branches:
  - feedback
  - operational
  - capability
---

# Source Digest: Arcanum Observed Invocation And Reflection

Sources:

- [Observed Invocation Loop](../../../arcanum/spells/observed-invocation-loop/README.md)
- [Workflow Reflect](../../../arcanum/arcana/workflow-reflect/README.md)
- [Sigil Maintenance Loop](../../../arcanum/spells/sigil-maintenance-loop/README.md)

Ledger: [../source-ledger.md](../source-ledger.md)

## Why This Source Matters

These sources define how Arcanum-managed capability execution becomes telemetry, how repeated signals become reflection, and how approved reflection can route to capability maintenance.

They are the feedback spine for Operational Ontology.

## Compiled Concepts

### Observed Invocation Loop

Observed Invocation Loop wraps managed skill, sigil, and spell invocations with a post-run observability handoff.

It should:

- create an invocation envelope;
- append exactly one telemetry signal;
- update reflection counters;
- route to reflection when thresholds are met.

Important principle:

```text
telemetry should be hook-first or wrapper-enforced when possible
agent-authored closeout is evidence, but should not be the only mechanism
```

### Invocation Envelope

The envelope should include:

- capability id;
- capability kind;
- mode;
- execution status;
- outputs;
- changed files;
- validation;
- observer evidence;
- telemetry append status;
- reflection trigger;
- next route.

### Workflow Reflect

Workflow Reflect reads accumulated telemetry and identifies:

- recurring workflow gaps;
- quality failures;
- anti-pattern hits;
- output drift;
- useful patterns;
- trend changes.

It produces reflection reports with:

- signal summary;
- triggered thresholds;
- repeated patterns;
- gap analysis;
- proposed iterations;
- rejected changes;
- contract preservation notes;
- recommended lifecycle step.

### Maintenance Boundary

Reflection does not mutate capability contracts by itself.

It recommends:

- no change;
- targeted update;
- major revision;
- retirement;
- next lifecycle route.

Approved mutation should route through the owning lifecycle authority, such as sigil-development or spellcraft.

## CyberAlchemy Adaptation

Operational Ontology should treat observed invocation and reflection as candidate-producing loops:

```text
managed invocation
  -> telemetry envelope
  -> signal observer
  -> workflow reflection
  -> operational lesson candidate
  -> promotion gate
  -> capability update or context solution
```

## Candidate Ontology Claims

| Claim                                                         | Branch               | Candidate Entry                              |
| ------------------------------------------------------------- | -------------------- | -------------------------------------------- |
| Managed invocations should emit telemetry.                    | feedback             | `rule-managed-invocation-telemetry`          |
| Reflection proposes; lifecycle authority mutates.             | knowledge-governance | `rule-reflection-non-mutating`               |
| Repeated output drift can trigger sigil maintenance.          | operational          | `maintenance-trigger-output-drift`           |
| Telemetry rows can support operational lessons.               | operational          | `edge-telemetry-supports-operational-lesson` |
| Observed invocation should be part of future execution proof. | feedback             | `feedback-loop-observed-invocation`          |

## Tensions And Promotion Gaps

- Strict telemetry may conflict with privacy or low-friction execution.
- Manual closeout is weaker than hook-enforced telemetry.
- Reflection threshold rules need calibration to avoid noisy maintenance.

## Agent Payload

After a managed run, check:

```text
was telemetry recorded?
was validation captured?
did a reflection threshold trigger?
is this a one-off event or a repeated pattern?
does it create an operational lesson candidate?
does a capability owner need to review it?
```
