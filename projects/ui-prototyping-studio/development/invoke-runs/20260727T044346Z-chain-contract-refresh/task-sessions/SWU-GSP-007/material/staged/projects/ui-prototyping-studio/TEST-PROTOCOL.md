# Test Protocol — governed local loop

**Scope:** this protocol studies governance and integrity ergonomics in the
locally implemented Studio. It does not establish release readiness, broad
accessibility conformance, or polished visual-prototyping ergonomics.

Read [TESTER-BRIEF.md](TESTER-BRIEF.md), then follow the setup in
[README.md](README.md#running). Use a fresh `STUDIO_DATA` file inside a fresh
directory for every full run.

## Capture

For each task record:

- whether the result matched your expectation;
- anything confusing;
- anything that felt unsafe or outside the intended authority route; and
- the exact state/action where that happened.

## Tasks

You may operate the CLI yourself or supervise an authorized tool route. The
important boundary is that you know which route is issuing each durable
operation; the Studio does not infer human identity from the caller.

1. **Start and prompt.** Run `session open`, then `prompt submit`.
   - Can you identify the session and its next valid state?

2. **Register variants.** Register one to three HTML files with
   `variants register --from <dir>`. Annotatable elements must have stable
   `data-od-id` values.
   - Are the returned artifacts and labels understandable?

3. **Choose a baseline.** Run `baseline select`, then `baseline commit`.
   Start `studio preview <sessionId>` and open its printed loopback URL.
   - Is the current baseline primary and are other variants clearly history?

4. **Annotate a real component.** In the preview, click an element with
   `data-od-id`, check that its target is shown, choose a constrained severity,
   and submit an intent/note.
   - Is the form unavailable before a real target is selected?
   - Does the selected target match the component you clicked?

5. **Synthesize and approve.** Run `synthesize`, inspect its tasks and
   checksum, then run `batch approve`.
   - Do you understand the bounded intent before approval?

6. **Stage and inspect.** Run
   `apply <sessionId> <batchId> --candidate-from <candidate.html>`.
   Refresh the preview.
   - Does it make clear that the candidate is staged rather than head?
   - Does the before/after evidence include structural and any CSS/global or
     unattributed change?
   - At a 390px-wide viewport, do the cards stack without horizontal page
     overflow?

7. **Exercise the browser gates.** Inspect the candidate/revision identity,
   intended action, target state, and diff recap. Confirm that Accept/Revert is
   disabled before acknowledgment. Acknowledge the exact context, then choose
   Accept or Revert.
   - Does the result match the acknowledged action?
   - If another process changes the state first, does the stale action refuse?
   - You may use CLI `accept`, `discard`, or `revert` to compare the
     scriptable route, but do not treat CLI caller identity as authority.

8. **Inspect history.** Run `revisions` and `state`.
   - Does the current head match the accepted/reverted append-only record?
   - Is every durable revision one you intended through the authorized route?
   Stop and report any unexpected revision.

9. **Inspect handoff predicates.** Run
   `handoff export <sessionId> --confirm`.
   Review `missingRefs`, `exportConfirmed`, `evidenceComplete`,
   `integrationReady`, and `implementationReady`.
   - Are missing references explicit?
   - Does confirmation remain separate from the three readiness predicates?
   - Do not interpret any field as release authorization.

## Feedback form

```text
Tester:
Date:
STUDIO_DATA:
Mode or authorized route:

Tasks 1–9 (expected? confusion? authority concern?):
1:
2:
3:
4:
5:
6:
7:
8:
9:

Did current head/history stay understandable?
Did staged versus recorded stay understandable?
Did the action acknowledgment match what happened?
Did any revision appear that you did not intend?
Did handoff confirmation remain distinct from readiness?
At 390px, was the comparison inspectable without page overflow?
Biggest control-surface confusion:
One improvement:
```

Store completed forms only in the evidence location selected by a bound
human-study owner. Until such an owner and protocol are admitted, individual
forms are observations, not a project-level ergonomics verdict.
