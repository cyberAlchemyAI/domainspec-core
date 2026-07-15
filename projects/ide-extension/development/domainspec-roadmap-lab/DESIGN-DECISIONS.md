---
id: ide-extension-domainspec-roadmap-lab-design-decisions
status: approved-for-planning
updatedAt: 2026-07-14
---

# Roadmap Lab Design Decisions

These decisions refine the accepted strategy into design constraints. They do
not authorize implementation or source mutation.

| ID | Decision | Consequence | Rejected alternative |
| --- | --- | --- | --- |
| RDL-D01 | Add a dedicated Roadmap Lab route/tab inside the existing workbench. | A newcomer sees DomainSpec roadmap context, not the ide-extension Craft frontier, as the primary frame. | Append the lab to the bottom of the generic workbench. |
| RDL-D02 | Reuse the generic Canvas publication/revision/event kernel unchanged in intent. | Roadmap-specific behavior lives in generated HTML, presentation data, validation, and event names unless evidence proves a kernel change is necessary. | Add a DomainSpec-specific mutation API. |
| RDL-D03 | Use a proposal-first interaction model. | The learner can restate and propose, but cannot directly edit roadmap authority or mark work complete. | In-browser direct editing. |
| RDL-D04 | Extract human-facing wording into a validated `roadmap-copy.json` with stable field IDs before accepting copy proposals. | Copy suggestions bind to intentional presentation fields rather than lines in a template. | Target raw HTML/template text. |
| RDL-D05 | Bind every proposal to `surface_id`, `revision_id`, roadmap `input_fingerprint`, `node_id`, `field_id`, and the observed original value. | Later review can detect stale context and preserve what the learner actually saw. | Trust only the current page or a free-text description. |
| RDL-D06 | First-slice source inspection exposes copyable repository-relative paths plus a `roadmap.source.requested` event. | The learner can ask for evidence without introducing a repository file-reading server. | Build a generic source resolver before testing comprehension. |
| RDL-D07 | Use a self-declared participant label for the local pilot. | Trial evidence can distinguish participants without claiming authentication or durable identity. | Add accounts/authentication to L0. |
| RDL-D08 | Route proposals by target class: presentation copy, graph/claim, continuation, research evidence, or unsupported protected action. | Each proposal gets an explicit owner and next route; unsupported effects fail closed. | Send every proposal to one generic inbox with implicit authority. |
| RDL-D09 | Record only semantic learning/proposal events. | The event stream can answer what was understood or proposed without click surveillance. | Record all navigation and clicks. |
| RDL-D10 | Treat the Victor trial and one accepted copy round trip as separate gates. | Comprehension/usefulness can pass even if no proposal is accepted; application evidence requires owner acceptance and regeneration. | Conflate submission, usefulness, acceptance, and application. |
| RDL-D11 | Keep runtime mutation sequential until write-scope ownership is rechecked. | Existing dirty edits in `server.mjs`, `l0.html`, schemas, tests, and package files are never overwritten by assumption. | Treat the current worktree as a clean baseline. |
| RDL-D12 | L0 proves one node (`FPR-01`) end to end before broadening coverage. | The smallest proof still exercises explanation, restatement, inspection, proposal, persistence, and review binding. | Make every roadmap node interactive before validating the learning model. |

## Non-decisions

The design intentionally does not choose authentication, remote hosting,
multi-user concurrency, a generic source browser, direct lifecycle automation,
or production authorization. Those require evidence not available from the
trusted-local newcomer proof.

