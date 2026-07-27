# Design Decision Log

| ID | Decision | Evidence | Consequence | Revisit trigger |
| --- | --- | --- | --- | --- |
| DD-001 | Use one React + TypeScript + Vite application. | D-006 selects a dedicated browser app; local repository has established Vite browser patterns. | shared routing, components, fixtures, and build; exact versions deferred to Plan | target ceases to be a browser application |
| DD-002 | Compile owner-reviewed project records; do not embed facts in components. | one-truth/two-projection invariant and project-owner veto | source correction is reviewable and deterministic | a governed runtime authoring service is approved |
| DD-003 | Project visibility before view-model creation. | D-004 deny-by-default policy | forbidden fields cannot be hidden only at presentation layer | none without reopening privacy policy |
| DD-004 | Separate card state from collaboration state. | freshness policy and reciprocal workflow are independent | stale/overdue cannot be confused with interest/appointment status | Define changes the product mechanism |
| DD-005 | Use URL/history only for non-sensitive navigation. | direct-link and recovery obligations plus privacy matrix | mode/project/step are reconstructible; private values stay out of URL | a privacy-reviewed encrypted route contract is approved |
| DD-006 | Use session memory for unsubmitted private drafts. | bounded first proof and data minimization | refresh warns before loss; durable submission is an explicit external effect | offline/durable drafts become a product requirement |
| DD-007 | Put durable submission and receipts behind a versioned gateway. | reciprocity, idempotency, failure, and history obligations | L0/L1 can proceed without selecting backend technology | Plan reaches L2 |
| DD-008 | Treat presenter notes as a separate authenticated projection. | notes must be absent from audience surfaces | no notes in audience DOM, bundle projection, export, or screenshot | facilitator decides notes are unnecessary |
| DD-009 | Keep Veritasium lineage inside editorial review metadata only. | approved public/private and non-endorsement boundary | public copy cannot name or imitate the precedent | D-005 owner explicitly approves a bounded citation |
| DD-010 | Model the offer composer as structured conversation, not AI chat. | no implemented AI matcher; user requested chat-term audit | UI names offer, recipient, visibility, consent, and next state precisely | an actual conversational AI capability receives its own Define/Design |
| DD-011 | Gate public access after restricted production validation. | D-006 and D-005 | deployment can be tested without implying public readiness | all audit and publication receipts pass |

None of these decisions authorizes implementation or changes approved Define
artifacts.
