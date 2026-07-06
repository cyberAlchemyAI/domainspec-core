# IDE Ergonomics Studio Opportunity Prototypes - Review Findings

Dispatch: `2026-07-01-ide-ergonomics-studio-opportunity-prototypes`
Reviewed artifact: `synthesis.md`

## Reviewer 1 - UX Concreteness

Attack vector: whether the proposed packages show believable end-user results
instead of abstract architecture.

Findings:

1. The flagship flow still risks being rebuilt as architecture. It should be a
   fixed click-through script: chat phrase `evidence rail` -> route card titled
   `Possible workflow transition detected` -> `preview only` pill -> four route
   buttons -> modal fields -> saved rail cards.
2. The visible outputs must be explicit:
   - Candidate: `Source span`, `Owner`, `Draft meaning`, `Blocked action`.
   - Side node: `Class`, `Source`, `Summary`, `Next`.
   - Handoff: `Start prompt`, `Open call`, `Source refs`, `Boundary`.
   - Delegation: role lanes plus `User gate`.
3. Knowledge Reference Resolver needs concrete fixtures:
   - Resolved: `knowledge:inventory/evidence-rail`.
   - Ambiguous: `confidence_reference`.
   - Unresolved: `knowledge:ontology/missing-handle`.
4. Knowledge popups should show handle, source surface, freshness, snippet,
   status, confidence, authority boundary, promotion owner, residue, and safe
   actions.
5. Craft and Connective should be split. Craft should start from a scene like:
   `Pending node: transition-card workbench needs acceptance evidence`; route
   question: `Is this a prototype review, implementation handoff, or blocked
   decision?`; expected receipt: `accepted Studio revision + screenshot/id
   coverage, no ledger write`.
6. Teammate Memo Window needs a sample memo fixture:
   `To: Vlad`, `From: Codex`, `Type: start-work`, `Status: open`,
   `Why now: transition-card proof needs owner choice`,
   `Open call: 4 choices or 6?`, `Boundary: memo is not resolution`.
7. Intent Latitude and Self-Assembling should remain L0/gated but need concrete
   end-user text. Intent can use:
   `Do not edit files; make the synthesis believable as a click-through prototype.`
   Self-Assembling can use:
   `This route miss happened 3 times. Build an L0 experiment?`
8. Operability caveats should be an appendix after a reviewer-facing evidence
   table.

## Reviewer 2 - Studio Operability And Scope

Attack vector: whether the strategy fits Studio's L0-L2 harness and does not
overload variants or session boundaries.

Findings:

1. Acceptance evidence must be a per-package Studio acceptance packet, not a
   loose visual checklist:
   - isolated `STUDIO_DATA`;
   - CLI transcript through baseline/comment/synthesize/approve/apply/accept
     where applicable;
   - stable-id comment log;
   - screenshot set;
   - axe/keyboard/focus report;
   - breakpoint bounding-box report;
   - explicit `local review only` statement when `UI-SPEC.md` and
     `TEST-SPEC.md` are absent.
2. Transition Card Workbench is too large as one package. The first package
   should be the route-card shell plus receipt/evidence boundary. Candidate,
   side-node, and handoff become child sessions sharing the shell.
3. Delegated-lane preview should be a decision-preview session, not bundled into
   the first package.
4. Spell/sigil nudge should be moved out of package 1.
5. Field-level `data-od-id` coverage is overstated. Either downgrade field-level
   review to coarse modal annotation or add stable ids for:
   - candidate source/owner/blocked action;
   - handoff start prompt/open call/refs/boundary;
   - side-node class/source/next;
   - delegation role/validation fields.
6. Knowledge Reference Resolver should drop graph panel from the first pass and
   focus on popup states only.
7. Craft and Connective should be split. Craft read model first; Connective only
   after fixture-backed load/test inputs exist.
8. Self-Assembling should be downgraded to an L0 approval storyboard unless an
   actual experiment-harness receipt is attached.
9. Host Surface Wrapper should move out of recommended packages and into
   deferred host validation dependencies.

## Reviewer 3 - Owner Boundaries And Forbidden Effects

Attack vector: whether the prototypes could imply canonical mutation, agent
execution, Craft ledger mutation, authority promotion, surveillance, or hidden
decisions.

Findings:

1. "Saving creates durable artifacts" can read as canonical mutation. Results
   should be labeled `Studio draft artifact`, `not canonical`, and
   `allowed effect: save local prototype evidence`.
2. Buttons should say `Save draft to workbench`, not just `Save`.
3. Route card, modal, artifact rail, and final workbench should show:
   `Owner route`, `Required gate`, `Forbidden effects`, and `Expected receipt`.
4. Delegated-lane preview must not use an `Approve delegation` action. Use
   `Save delegation plan` and a disabled/downstream action:
   `Run delegation requires dispatch-spec confirmation`.
5. Delegation modal must include: `No agents spawned`,
   `Recommendation is not permission`, `Join policy`, `Role owner`, and
   `Receipt required`.
6. Craft panel should be labeled `Read-only Craft view`; route answers should
   say `Draft routing answer - does not update ledger, close blocker, or change
   status`.
7. Load context must be opt-in and labeled `manual/user-supplied only`; unknown
   indicators should render as `Unknown`, never inferred.
8. Self-Assembling should split visible states:
   `Friction evidence detected`, `Candidate proposed`, `Experiment draft`,
   `Run approved`, `Ready for human test`, `Promotion request`.
9. Knowledge resolver header should say `Read-only resolver`; `refresh` should
   become `Re-run lookup`; `Add-to-handoff` should become
   `Add citation to draft handoff`.
10. Memo actions should say `Draft reply`, `Propose resolution`, and
    `Defer locally`; receipts should say `draft created`, `not sent`, or
    `resolution proposed`.
11. Add a persistent `Prototype effects` strip:
    `Preview: no write`, `Apply: stages Studio candidate`,
    `Accept: advances Studio session only`,
    `Export: terminal confirmation required`.

