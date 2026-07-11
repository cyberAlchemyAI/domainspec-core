# Schon, Donald - Skeptic/Verifier Return

Registered review: `2026-07-10-ide-extension-architecture-review`

Role: skeptic/verifier  
Attack vector: scope + definitional

## Verification Rule

I treated the literal implemented-L0 acceptance contract as controlling over stronger
language imported from proposed L0.5/L0.6 or deferred L1/L2. A candidate survives as
an L0 defect only where implemented behavior contradicts an L0 claim or corrupts an
L0 artifact. A proposed control may justify a promotion blocker, but not a present
implementation defect.

The key authority distinctions are:

- **approval:** L0 has a human approval gate and queue (`SPEC.md:14-16,23-24`), but
  authenticated actor/session separation and self-approval rejection are explicit
  L0.5 requirements (`SPEC.md:122-124,159-170`);
- **run:** L0's acceptance witness says approval records the no-op receipt
  (`SPEC.md:149-157`), while exactly one post-approval adapter invocation belongs to
  L0.5 (`SPEC.md:159-167`);
- **receipt:** an L0 receipt is the closed record listed at `SPEC.md:126-138`; binding
  hashes, custody descriptors, context packet digests, and adapter identity are L0.5
  requirements (`SPEC.md:140-145`);
- **source and context references:** L0 requires strings naming references, but does
  not grant authority merely because a module is visible (`SPEC.md:87-99,103-112`);
- **adapter and secret custody:** OpenRouter is an L0 descriptor shape, not a live
  provider (`SPEC.md:27`; `CRAFT.md:42-45`; `src/adapters/openrouter.mjs:1-9`).

## Candidate Verification

### AR-CAND-001 - RECLASSIFY

**Correct classification:** MAJOR implemented-L0 approval-attribution defect;
CRITICAL promotion blocker for any effectful L0.5+ lane.

**Literal evidence:** `src/server.mjs:170-190` accepts any loopback request body and
passes `body.approved_by || 'human'`. `src/envelopes/dry-run-envelope.mjs:32-55`
persists that unverified label. `public/demo/l0.html:366-371` submits the approval
through the same unauthenticated browser channel. L0 itself binds human approval into
the workbench definition (`SPEC.md:14-16`) and calls for an approval queue for actions
beyond preview/read (`SPEC.md:23-24`). The implementation therefore cannot establish
that its durable `approved_by` assertion denotes a human.

The candidate overstates the present consequence as CRITICAL. Implemented L0 is a
loopback no-op witness: it performs no browser, shell, filesystem, network, export,
commit, push, or publication action (`SPEC.md:53-61`), and self-approval rejection by
actor/session separation is expressly an L0.5 acceptance rule (`SPEC.md:122-124,170`).
The defect is still MAJOR because the L0 receipt and state claim human approval
without evidence of it. It becomes CRITICAL before any effectful adapter is admitted.

**Fix fit:** Narrow the immediate fix to honest L0 attribution: do not accept or
default a caller-supplied identity as proved human authority. Kernel-owned
actor/session capabilities, proposer comparison, and authenticated separation fit
L0.5 promotion and should not be represented as already required L0 machinery.

### AR-CAND-002 - VERIFIED

**Severity/layer:** CRITICAL L0 receipt-fidelity defect and L0.5 promotion blocker.

**Literal evidence:** `src/server.mjs:177-180` checks only that the URL approval ID
matches `current_envelope`; it checks neither queue state nor prior consumption.
`src/server.mjs:182-210` writes a fresh artifact, receipt, state update, and event for
every matching call. `src/envelopes/dry-run-envelope.mjs:32-59` accepts an already
terminal envelope. Hewitt's recorded reproduction produced two `201` responses, two
receipt IDs, and two `receipt.appended` events from one approval.

Although explicit reused-approval rejection is stated for L0.5 at `SPEC.md:167`, the
implemented L0 defect is independently literal: one pending approval is represented
as one queue item (`SPEC.md:149-157`), yet it can mint multiple L0 receipts. This
destroys the cardinality of the acceptance witness.

**Fix fit:** The proposed atomic pending-to-used transition and replay rejection fit.
Binding adapter invocation, normalized grants, actor/session, and expiry is L0.5
hardening and should be labeled accordingly.

### AR-CAND-003 - RECLASSIFY

**Correct classification:** MINOR implemented-L0 typestate inconsistency; MAJOR
L0.5 promotion blocker. Drop the claim that L0 approval is falsely presented as a
separately observed successful execution.

**Literal acceptance resolution:** `SPEC.md:149-157` defines the implemented L0
acceptance sequence. Step 5 says run is blocked before approval; step 6 says
"approve records a no-op receipt." The implementation does exactly that:
`src/server.mjs:157-167` blocks before approval and otherwise only reports state;
`src/server.mjs:182-210` records the receipt during approval; and
`src/envelopes/dry-run-envelope.mjs:36-59` marks the no-op receipt and envelope
`passed`. Therefore the candidate consequence - that L0 falsely attests to a
separately observed run - is not sustained by the literal L0 acceptance contract.

There is a real but narrower inconsistency. `SPEC.md:114-120` draws
`awaiting_approval -> running -> passed` and says `running` is the post-approval no-op,
while implementation skips the named `running` state. That is a typestate/spec defect,
not evidence that an unimplemented effect was executed. For L0.5, the distinction
becomes MAJOR because acceptance explicitly requires one allowlisted adapter call
after approval (`SPEC.md:159-167`).

**Fix fit:** Do not retrofit a distinct kernel run into L0 merely to satisfy the
candidate's interpretation. Reconcile the L0 typestate prose with its acceptance
contract. Preserve a distinct authorize -> invoke -> evidence -> receipt transition
as mandatory for L0.5 promotion.

### AR-CAND-004 - RECLASSIFY

**Correct classification:** MAJOR L0 contract-validation defect; promotion blocker
for any lane where grants control effects.

**Literal evidence:** `src/envelopes/dry-run-envelope.mjs:9-11` accepts any non-empty
array as `requested_grants`. `src/server.mjs:127-145,186-210` persists those strings
and includes the envelope in the passed L0 state without validating vocabulary.
`src/kernel/grants.mjs:1-16` defines the known effectful grants and approval predicate,
but the server imports only `blockedBeforeApproval` and never applies a closed grant
policy. The reproduced `shell.exec` acceptance confirms this path.

The phrase "bypass capability policy" is too strong for implemented L0 because L0
executes no requested capability; all envelopes are the same no-op witness. The
present defect is that authority-shaped `requested_grants` in an L0 envelope are not
validated despite the envelope contract (`SPEC.md:101-112`). Actual effect-policy
bypass begins only if an adapter executes those labels.

**Fix fit:** Enforce a closed/versioned L0 grant vocabulary at preparation and receipt
boundaries. Adapter-specific allow/forbid/target scope and grant digests fit L0.5+.

### AR-CAND-005 - VERIFIED

**Severity/layer:** MAJOR implemented-L0 concurrency and state-model defect.

**Literal evidence:** `src/server.mjs:140-144` replaces `current_envelope` while
retaining every pending queue item. Approval then loads only `current_envelope` and
rejects any other approval ID at `src/server.mjs:174-180`. Thus the API can display a
pending approval that its own approval route cannot resolve.

This is not a deferred multi-user requirement. Two sequential preparations from one
local browser or process are enough to create the contradiction.

**Fix fit:** Immutable lookup by envelope/run/approval ID fits the defect. No broader
multi-user identity system is required to correct it.

### AR-CAND-006 - VERIFIED

**Severity/layer:** MAJOR implemented-L0 persistence-consistency defect.

**Literal evidence:** the approval path reads mutable state, writes before and receipt
artifacts, overwrites `workbench.json`, and appends an event at
`src/server.mjs:174-209`, with no serialization or recoverable commit boundary.
`src/kernel/artifacts.mjs:8-12` uses overwrite-capable `writeFile`, while
`src/kernel/audit.mjs:4-7` appends independently. Hewitt's reproduced race yielded
two receipt events and receipt IDs while the read model retained one receipt.

The finding is supported by demonstrated divergence, not by a cryptographic meaning
of "append-only." `SPEC.md:81-83` requires both persisted state and an append-only
local log; it does not require signatures, hashes, or generic tamper evidence.

**Fix fit:** Serialization, exclusive creation, commit ordering/journaling, and
startup reconciliation fit. Cryptographic chaining must remain optional hardening.

### AR-CAND-007 - RECLASSIFY

**Correct classification:** MAJOR L0 reference-integrity defect, with the candidate's
context-binding and digest requirements reserved for L0.5.

**Literal evidence:** `src/envelopes/dry-run-envelope.mjs:18` accepts caller
`context_refs`, but receipt construction at lines 41-45 does not carry or resolve
them and defaults `evidence_refs` to a fixed founding-research path. The server writes
only a before artifact at `src/server.mjs:182-190`; `after_ref` is the symbolic string
`state:${run_id}:passed`, not a preserved artifact. `schemas/receipt.schema.json:34-55`
accepts any non-empty strings, so the schema cannot establish resolution.

L0 does require `before_ref`, `after_ref`, and `evidence_refs` in every receipt
(`SPEC.md:126-138`), and acceptance requires persistence outside browser memory
(`SPEC.md:149-157`). References that are unrelated or cannot be resolved make that
record materially misleading. But exact context snapshots, evidence digests,
adapter identity, context-packet hashes, and custody binding are explicitly L0.5
requirements (`SPEC.md:140-145`), not missing L0 implementation.

**Fix fit:** For L0, type and resolve references and persist the actual no-op before
and after artifacts. Apply the larger binding set only to L0.5 promotion.

### AR-CAND-008 - VERIFIED

**Severity/layer:** MAJOR implemented-L0 contract-enforcement defect.

**Literal evidence:** `scripts/validate-schemas.mjs:10-18` parses schema documents as
JSON and delegates manifests to `loadModuleManifests`; it never validates instances
against JSON Schema. `src/kernel/registry.mjs:23-39` is handwritten and omits declared
constraints such as `additionalProperties: false`, `source_refs.minItems`, and
`uniqueItems` from `schemas/module-manifest.schema.json:6-78`. The prepare and approve
paths at `src/server.mjs:127-153,170-210` invoke no validator for the closed envelope
and receipt schemas (`schemas/agent-envelope.schema.json:5-17` and
`schemas/receipt.schema.json:5-17`). The recorded hostile fixtures were accepted.

This is L0, not L0.5: JSON schemas are explicitly in L0 scope (`SPEC.md:18-27`), and
the module registry plus envelope/receipt records are part of the accepted witness.

**Fix fit:** One Draft 2020-12 validator at admission/emission boundaries plus hostile
fixtures fits. If parse-only behavior remains, its command/output must say so.

### AR-CAND-009 - VERIFIED

**Severity/layer:** PROMOTION BLOCKER, not a present L0 defect.

**Literal evidence:** `schemas/module-manifest.schema.json:27-37` defines
`owner_route` as a string and `source_refs` as an array of strings.
`src/kernel/registry.mjs:23-39` checks shape but resolves neither. The ResonantOS
manifest points to mutable checkout roots at
`src/modules/resonantos-browser-first.manifest.json:4-15`, while the supporting design
names specific precedent files at
`development/browser-first-extension-design/ARCHITECTURE-BUNDLE.md:43-49`.

The candidate correctly respects `SPEC.md:98-99`: listing and validation do not make
a module authoritative. Consequently unresolved ownership and provenance do not
prove current unauthorized execution. They block promotion when a capability claim
is used for admission or authority.

**Fix fit:** Canonical bases, registered owner IDs, exact files, revisions/digests,
and machine-readable verification status fit the promotion gate. Do not backcharge
them as absent L0 execution controls.

### AR-CAND-010 - VERIFIED

**Severity/layer:** PROMOTION BLOCKER for L0.5 and later precedent claims; no present
L0 defect.

**Literal evidence:**
`development/mcp-chat-extension-integration-research/research.md:129-149` relies on
mutable GitHub file URLs for concrete descriptor, setup, transport, type, hook,
mapping, and PR-tool observations. Those citations contain no inspected commit,
captured local extract, or claim-to-source map. The same research keeps the resulting
MCP/chat lane proposed rather than implemented.

**Fix fit:** A local provenance ledger with URL, inspected revision/date, bounded
evidence, adopting owner, and adaptation decision directly addresses reproducibility.
It must gate promotion, not be described as repairing implemented L0.

### AR-CAND-011 - VERIFIED

**Severity/layer:** PROMOTION GATE for any live provider lane; explicitly no present
implementation defect.

**Literal evidence:** `src/adapters/openrouter.mjs:1-9` returns descriptor metadata
and only checks whether `OPENROUTER_API_KEY` exists. It does not call a provider or
return the secret. `CRAFT.md:42-45` explicitly records a boundary stub with no live
key handling or streaming proof. `SPEC.md:27,53-61` keeps keys server-side and live
effectful calls outside unapproved L0 behavior.

There is therefore no implemented secret-custody failure to soften: there is no live
secret path. The item survives solely as a precondition to provider admission.

**Fix fit:** Server/process custody, env allowlisting, bounded HOME/CWD, redaction,
and negative leak tests fit a live-provider promotion gate. They should not be added
to the no-op L0 witness merely to make the descriptor appear implemented.

## Required Synthesis Edits

1. Change AR-CAND-001 from CRITICAL present-L0 to **MAJOR L0 attribution defect;
   CRITICAL effectful-lane promotion blocker**. Separate the unproved human label
   from L0.5 authenticated actor/session machinery.
2. Keep AR-CAND-002 CRITICAL, but distinguish the present one-approval/many-receipts
   failure from L0.5 expiry, actor/session, invocation, and normalized-grant binding.
3. Replace AR-CAND-003's semantic-collapse finding with **MINOR L0 typestate
   inconsistency; MAJOR L0.5 promotion blocker**. Explicitly cite `SPEC.md:149-157`:
   L0 acceptance says approval records the no-op receipt. Drop the claim that L0
   promises a separately observed execution.
4. Rename AR-CAND-004 to **Requested grants are not validated against the L0 grant
   contract**. Do not claim an executed-capability bypass in a no-op implementation.
5. Keep AR-CAND-005 and AR-CAND-006 as independent MAJOR L0 defects. Keep all
   cryptographic tamper-evidence language out of AR-CAND-006.
6. Narrow AR-CAND-007's present-L0 fix to resolvable, persisted before/after/evidence
   references. Move envelope/actor/session/adapter/context-packet/digest custody
   binding to L0.5.
7. Keep AR-CAND-008 MAJOR and say plainly that schemas are parsed while runtime
   instances are not validated against them.
8. Keep AR-CAND-009 and AR-CAND-010 only as promotion blockers. Do not describe
   unresolved references or mutable research as current authority or execution.
9. Keep AR-CAND-011 only as a promotion gate and explicitly state that no present
   secret leak or live provider custody path exists.
10. In the synthesis definitions, reserve **approval** for authorization,
    **receipt** for the kernel-written L0 record, and **run/invocation** for a distinct
    effect only where the layer contract requires one. Do not import L0.5
    `DesignFeedbackContextPacket`, adapter invocation, evidence hashes, actor/session
    separation, or custody descriptors into claims about implemented L0.

## Exact Disposition Table

| Candidate | Disposition | Correct severity / layer |
| --- | --- | --- |
| AR-CAND-001 | RECLASSIFY | MAJOR L0; CRITICAL promotion blocker for effectful lanes |
| AR-CAND-002 | VERIFIED | CRITICAL L0 receipt fidelity; L0.5 blocker |
| AR-CAND-003 | RECLASSIFY | MINOR L0 typestate inconsistency; MAJOR L0.5 blocker |
| AR-CAND-004 | RECLASSIFY | MAJOR L0 grant-contract validation; execution blocker L0.5+ |
| AR-CAND-005 | VERIFIED | MAJOR L0 concurrency/state model |
| AR-CAND-006 | VERIFIED | MAJOR L0 persistence consistency |
| AR-CAND-007 | RECLASSIFY | MAJOR L0 reference integrity; stronger binding at L0.5 |
| AR-CAND-008 | VERIFIED | MAJOR L0 contract enforcement |
| AR-CAND-009 | VERIFIED | PROMOTION BLOCKER only; not present L0 defect |
| AR-CAND-010 | VERIFIED | PROMOTION BLOCKER only; not present L0 defect |
| AR-CAND-011 | VERIFIED | PROMOTION GATE only; no present implementation defect |
