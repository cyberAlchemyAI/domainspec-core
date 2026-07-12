# Distill Validation: Operations V1 Design

## Run Profile

- Target context: backward-compatible local HTML construction surface.
- Objective/output: six-view architecture that can later become a dedicated
  implementation plan.
- Mode: `validate`.
- Budget: one Balancer-led pass and one reconciliation pass.
- Role path: labeled local Proposer/Balancer because the accepted multi-agent
  review already supplied independent attack evidence.
- Verdict: `pass`.

## Role Conversation Trace

### Proposer

The smallest coherent unit is:

```text
exact V0 revision
  -> separate derived surface
  -> immutable initial body
  -> one CAS-guarded whole-document replacement
  -> restart-stable content fetch and display
```

It proves compatibility, body authority, revision identity, operation retry,
and complete-revision display before append, rebuild, or regions.

### Balancer

| Objection category | Objection |
| --- | --- |
| Hidden glue | A derived surface is not honest unless some owner persists its body. |
| Source integrity | Current V0 revisions may no longer have retrievable exact bytes after workspace drift. |
| Premature variety | Append, replace, rebuild, navigation, and regions could become one oversized first unit. |
| Crash boundary | Blob storage plus event append can produce missing or orphan references. |
| Compatibility | Teaching the original surface about CAS would still change old behavior. |

### Reconciliation

- Accept hidden-glue objection: kernel-owned immutable blob storage is explicit.
- Accept source-integrity objection: derivation fails when the selected V0
  revision bytes are unavailable.
- Accept premature-variety objection: first unit is derive plus replace;
  append/retry hardening and rebuild/navigation are later layers; regions are
  deferred.
- Accept crash-boundary objection: blob durability precedes event append;
  orphan blobs are safe residue.
- Accept compatibility objection: new surface identity is mandatory.

No stable disagreement remains at design level.

## Technique Trace

| Technique | Hook | Outcome |
| --- | --- | --- |
| abstraction-level guard | Builder idea mixed protocol, storage, display, and region concerns. | Selected one protocol/storage/display slice, not a full editor. |
| recomposition proof | First unit omits append and rebuild. | Same CAS, blob, event, revision, and display path supports later operations. |
| evolution profile | User explicitly expects named regions later. | Preserve additive `target` boundary; defer region semantics. |
| frame-expiry note | Authority or collaboration posture may change. | Named below. |
| navigable result | Design must lead to a plan. | Start with architecture bundle; later route is Invoke plan. |
| requisite variety | Multiple operation modes exist. | Layer modes after shared derive/replace substrate. |
| boundary-object check | V0 revision crosses into a new body owner. | Exact derivation contract and lineage record added. |
| premortem | Durable body/event ordering can fail. | Blob-before-event invariant and restart validation required. |

Tournament was skipped because the accepted adversarial review already rejected
in-place promotion and selected separate identity. More competing tracks would
repeat a closed decision.

## Closure And Recomposition

The selected unit owns one responsibility: establish an independently durable,
retry-safe operations surface from exact V0 bytes. Its inputs, outputs, storage,
errors, and display behavior are explicit. Splitting it below derivation,
storage, CAS replacement, and fetch would leave a surface with no honest body or
an operation with no compatible identity.

Append reuses the same current-revision read, CAS, blob write, event append, and
notice path with a fragment transform. Rebuild changes only input admission and
lineage. Navigation consumes committed revision handles. Regions extend the
target discriminator after separate design.

## Deferred Complexity

- parser package/version and byte limits;
- garbage collection;
- navigation durability;
- declared region semantics;
- collaboration, merge, hostile HTML, and remote access.

## Premortem

Likely failure: an implementation stores only metadata and rereads a mutable
workspace file, making retry and history claims false. Guardrail: no derivation
event may commit until exact bytes exist in immutable kernel storage.

## Frame Expiry

This optimization point expires if the product chooses direct canonical
workspace mutation, multi-user collaboration, hostile agent inputs, or in-place
V0 promotion. Any of those requires a new design decision, not a larger SWU.

## Navigation Guide

Start with `ARCHITECTURE-BUNDLE.md`, confirm decisions in `DECISIONS.md`, then
use `IMPLEMENTATION-LAYERING-SEED.md` for a dedicated Operations V1 Invoke plan.
