# Evidence Closure — Intent Router Bootstrap and Runtime Integration

## Frozen objective

Determine whether the existing standalone intent-route resolver can:

1. be applied through Arcanum Bootstrap in Claude and Codex runtimes;
2. later integrate with `projects/cyberalchemy-orchestrator`;
3. operate as a bounded part of `cyberAlchemy-v2`;
4. work with Augmentor or another agentic runtime without taking their authority;
   and
5. advance the Agent Reasoning Engine without being overstated as the whole
   engine.

This research authorizes no public extraction, canonical acceptance, generated
runtime package, consumer adapter, promotion, release, install, deployment, or
production claim.

## Exact-binding matrix

| Question or boundary | Current evidence | Closed verdict | Lifecycle label |
|---|---|---|---|
| Is the private resolver real and working? | The standalone package exists under `cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/intent-route-resolver/`; its manifest declares no permissions or side effects. The explorer reran `node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/intent-route-resolver/test/*.test.mjs`: 34 passed, 0 failed. See `research.md:88-90`, `research.md:579-598`, and `receipts/explorer-reasoning-layer.json`. | Yes, as a tested private standalone package only. | **CURRENT / BOUNDED** |
| Can Bootstrap select it today? | Bootstrap and selective sync accept canonical Arcanum sigils or spells only. No public canonical `intent-route-resolver` exists; the private package is outside those selector roots. See `research.md:49-53` and `receipts/explorer-bootstrap-runtime.json`. | No. Direct current Bootstrap integration is killed. | **KILLED / CURRENT TOPOLOGY** |
| Can it become a Bootstrap-installed add-on later? | Bootstrap already projects one canonical source and support closure into runtime skill packages. A fresh generic, zero-authority public sigil could use that path after separate extraction and canonical-acceptance decisions. See `research.md:58-71` and `synthesis-revised.md:64-81`. | Yes in principle, but only after public extraction and canonical acceptance. Bootstrap is the installer/projector, not the semantic resolver. | **SELECTED / FUTURE** |
| Can Claude and Codex use the same integration? | The generator supports both profiles from one canonical closure, with generated metadata and the declared Claude tool-token normalization as admitted differences. No resolver package currently exists under either runtime surface. See `research.md:71-104` and `synthesis-revised.md:162-171`. | Presence parity is feasible; behavior parity is not currently witnessed. The future contract freezes five commands, 78 logical cases, schemas, numeric exits, bytes, rollback, timeout, and zero-authority counters. | **DEFERRED / FUTURE ACCEPTANCE** |
| Is the future parity contract mechanically testable? | `acceptance-contract-addendum.md` pins timeout `5000 ms`, injected delay `5001 ms`, fixture/digest fields, case and summary schemas, exact exits/output forms, commands/counts, rollback isolation, and zero-call invariants. The final non-vacuity reviewer returned GO. | Yes as implementation-ready design. It remains non-evidence until the runners, packages, fixtures, and results exist. | **GO / DESIGN ONLY** |
| Where can the orchestrator integrate it? | The inspected nested repository was clean at `7b98bf8edbfc0647934fabfa5c9158297837ea9c`. The smallest seam is a thin process-bound JSON adapter in `implementations/server/runtime/host_dispatch_hook.py:373-380`, before `_workflow_envelope()`. Existing `RuntimeService.bind_host_workflow_turn()` at `:410-427` remains the governed binding/launch owner. See `research.md:233-278` and `receipts/explorer-orchestrator-seam.json`. | Future thin pre-launch adapter selected; no current adapter, catalog owner, request owner, or consumer witness exists. | **SELECTED / FUTURE, CURRENTLY ABSENT** |
| What may cross the orchestrator seam? | The resolver returns only `candidate`, `ambiguous`, `no-match`, or `invalid`, always non-authorizing. The repaired synthesis removes any parallel `selection_id`, selection table, lifecycle, Dispatch, or ledger. Only an already confirmed canonical Dispatch/group/seat may reach the existing workflow-binding owner. See `synthesis-revised.md:173-251`. | Advice may inform a human; it cannot select, bind, authorize, schedule, execute, or prove effects. | **FAIL-CLOSED OWNER BOUNDARY** |
| How are request and disposition retained? | The future catalog is a digest-bound read-only projection of named canonical owners. ACI may reference request/disposition as content-addressed artifacts through its one existing journal; the router creates no registry, journal, or lifecycle. Exact catalog projector, normalization owner, and ACI fields are still unbound. See `synthesis-revised.md:173-251`, `:464-478`. | Reuse canonical Dispatch and ACI ownership; do not introduce competing authorities. Implementation remains blocked until owners are bound. | **DEFERRED / OWNER DECISIONS** |
| Is it part of `cyberAlchemy-v2`? | Its code and tests live in the private reasoning-engine implementation tree, but no Agent Reasoning Engine, ACI, Augmentor, ResonantOS, or orchestrator consumer installs or invokes it. See `research.md:607-614` and `receipts/explorer-reasoning-layer.json`. | Yes only in the repository/component sense: a private standalone entry-routing component. No in the runtime-integrated sense. | **CURRENT COMPONENT / INTEGRATION DEFERRED** |
| Does it advance the reasoning engine? | It deterministically reduces typed intent and a frozen catalog to traced, digest-bound, abstaining, non-authorizing dispositions. Semantic judgment, object-level inference, actor protocol, memory/replay, effects, and ACI integration are absent. See `research.md:612-643` and `synthesis-revised.md:253-271`. | It advances the reproducible pre-inference capability-routing boundary only. It is neither the semantic judgment evaluator nor the whole reasoning engine. | **NARROW ADVANCE / CLAIM CEILING** |
| How can Augmentor or another runtime work with it? | The standalone contract keeps runtime projection, approval, execution, persistence, Augmentor, and host concerns outside the L0 resolver. See `research.md:88-90`, `:178-197`, and `:648-651`. | A runtime-specific source adapter may form typed requests or consume dispositions. Augmentor remains capture/projection/interaction owner; the host remains confirmation, authorization, execution, persistence, and effect owner. | **ADAPTER COMPATIBLE / ZERO AUTHORITY TRANSFER** |

## Selected target topology

```text
source-specific intent capture (Augmentor, Claude, Codex, or another host)
    -> typed intent-route.request@1
    -> digest-bound read-only route-catalog projection
    -> generic zero-authority intent-route resolver
    -> candidate | ambiguous | no-match | invalid
    -> human clarification or confirmation
    -> existing canonical Dispatch/group/seat
    -> existing host binding, authorization, execution, persistence, effects
```

The generic resolver may eventually be public Arcanum source. Private
`cyberAlchemy-v2` and orchestrator adapters may depend on that public contract,
but private CAV2, DomainSpec, Saturn, ACI, Augmentor, ResonantOS, or
reasoning-engine prose and authority must not be copied into public Arcanum.

## Ordered project path and gates

1. **Extraction decision:** approve the public/private boundary, name, API,
   license, and compatibility commitment.
2. **Owner binding:** name the canonical capability and confirmed-Dispatch
   sources, route-catalog projector owner/path, request-normalization owner, and
   ACI artifact-reference fields.
3. **Canonical candidate:** write a fresh project-agnostic, candidate-only
   Arcanum contract and prove the private-boundary scan.
4. **Canonical acceptance:** separately accept it as Arcanum source; this is not
   implied by extraction.
5. **Core witness:** implement the public runner and synthetic fixtures.
6. **Runtime projections:** generate disposable Claude and Codex packages from
   the same closure.
7. **Parity and lifecycle witness:** run the frozen future contract for presence,
   behavior, negatives, disable, provenance, timeout, and durable rollback.
8. **Promotion and release:** separately promote generated packages and publish
   a pinned release.
9. **Disposable consumer install:** prove local installation before touching
   the orchestrator.
10. **Orchestrator adapter:** implement the thin JSON process adapter and ACI
    artifact references, first in advisory shadow mode.
11. **Authority proof:** prove that only a confirmed canonical
    Dispatch/group/seat crosses the seam and that selection, binding,
    authorization, attempt, effect, and receipt cannot substitute for one
    another.
12. **Private reasoning integration:** add an ACI-subordinate
    `cyberAlchemy-v2` entry-routing witness and a distinct handoff to semantic
    evaluation.

Every transition involving extraction, canonical authority, promotion, public
release, consumer installation, deployment, or movement from advisory to
gating remains a separate human decision.

## Review closure

| Reviewer | Final status | Closed scope |
|---|---|---|
| Precedent and ownership | GO | No duplicate selection, Dispatch, route registry, or ACI lifecycle owner. |
| Definitional boundary | GO | Support evidence, disposition integrity, lifecycle receipts, authority evidence, and authority transitions are non-substitutable. |
| Non-vacuity and parity | GO | Future commands, schemas, scalar values, failure mappings, timeout, digests, rollback, and counters are mechanically closed. |

The synthesis is ready for findings writing under this evidence ceiling.
