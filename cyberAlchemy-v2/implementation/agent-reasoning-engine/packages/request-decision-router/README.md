# Request Decision Router

Private candidate runtime for fast CyberAlchemy-v2 request routing and
configurable continuation gating.

The package performs two pure decisions after one startup verification:

```text
RequestContext + verified DecisionProfile
  -> direct capability | decision gate | block

Completion + proposed continuations + verified DecisionProfile
  -> complete | direct | decision gate | block
```

Goal is a normal route candidate. It matches only goal-specific objective
evidence and is never a fallback for Define, Understand, Validate, or another
capability.

After each completed operation, the host calls `evaluateContinuation`. It may
follow a `direct` result only when exactly one structurally admissible option is
non-consequential and reversible. Multiple choices, unknown effects,
irreversibility, protected hazards, or a named owner gate return `gate`. Zero
admissible options return `block`; no required continuation returns `complete`.

`advanceUntilGate` evaluates an already supplied sequence. It does not execute
tools or effects. A host may use the same rule after each real completion, but
the host remains responsible for execution, persistence, and owner interaction.

## Performance boundary

`loadVerifiedDecisionProfile` reads and hashes provenance once. The hot-path
functions receive the admitted frozen profile and perform no filesystem,
network, model, discovery, persistence, or tool calls. Run the local benchmark:

```text
toolchains/node-typescript/bin/node-env run \
  --project projects/domainspec-v2/impl -- \
  node cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/request-decision-router/scripts/benchmark.mjs
```

Timing is evidence for the current machine and bytes, not a universal latency
guarantee.

## Authority boundary

Every result has `authority_effect: none`. `direct` is routing evidence, not
consent or execution. `gate` identifies an owner decision boundary but cannot
satisfy it. The configured profile is candidate runtime policy, not an adopted
Governance rule, Constitution, permission, or exact-effect gate.
