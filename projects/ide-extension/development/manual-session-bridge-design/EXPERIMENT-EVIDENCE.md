---
id: ide-extension-manual-session-bridge-experiment-evidence
project: ide-extension
title: "Blind Manual Poll Experiment Evidence"
status: observed
node_type: experiment-evidence
updatedAt: 2026-07-12
---

# Blind Manual Poll Experiment Evidence

## Question

Can the operator choose a skill in the local Approval Desk without revealing it
to the active Codex session, approve the proposal, and reveal the skill only
when the operator explicitly asks that session to poll?

## Setup

- Local workbench: `http://127.0.0.1:8765/demo/l0`
- State root: fresh temporary `.ide-extension`-compatible state directory.
- Agent ref: `codex.current-session`
- Requested skill: entered privately in the browser.
- Execution trigger: the operator later sent only `poll` in the Codex session.
- Approved grants: `dry-run.noop` and `preview.read`.

## Observed Binding

| Field | Observed value |
| --- | --- |
| Envelope | `env-1783825072671-71ae20` |
| Run | `run-1783825072671-dd8976` |
| Approval | `approval-1783825072671-e02a04` |
| Approval state | `consumed` |
| Approval receipt | `receipt-1783825083965-21b37a` |
| Requested skill revealed at poll | `decision-gate` |
| Receipt stage | `l0-dry-run` |
| Loaded skill SHA-256 | `699718b4276c8dc7e276e19b4f50f8d549163d581d8cb488a0ed7158d496be16` |

The live projection bound the same `requested_skill` to the envelope and
approval receipt. The session did not inspect the new state between private
entry and the explicit `poll` message.

## What The Experiment Proved

1. The browser can capture an opaque safe skill slug without a predefined skill
   menu or named allowlist.
2. The server can preserve that slug through envelope, approval artifact, and
   receipt bindings without resolving a skill path.
3. The operator can keep the selected skill out of the chat until an explicit
   poll.
4. After polling, the session can resolve the revealed slug to an installed
   skill package, read its contract, and follow its fail-closed behavior.
5. The selected `decision-gate` skill returned `BLOCK` because the approved
   task did not contain a decision target or options. That is evidence that the
   skill contract affected behavior rather than merely appearing in output.

## What The Experiment Did Not Prove

1. The local server did not invoke Codex or an agent SDK.
2. The session result was reported in chat, not posted back to the kernel.
3. The approval receipt was a dry-run receipt; it did not prove skill execution.
4. The current session had no authenticated session identity or server-issued
   claim token.
5. The server did not technically constrain the Codex tool surface or enforce
   workspace write scope.
6. Crash recovery, duplicate polling, claim timeout, and replay behavior were
   not exercised.
7. The proposal task field existed but its visible label was hidden and its
   generic default value was submitted accidentally. The experiment therefore
   did not prove that a normal user could knowingly provide the task.

## Design Requirements Derived From The Experiment

| Requirement | Evidence source |
| --- | --- |
| Keep skill resolution out of the server. | Blindness held until the session polled. |
| Make the proposal task visibly labeled, empty by default, and required. | The generic default task caused a valid skill to receive unusable input. |
| Separate approval authorization from execution completion. | Current approval immediately produced a `passed` dry-run receipt. |
| Add one atomic claim before revealing the skill. | The manual poll currently reads a general state projection with no claim ownership. |
| Return the result to the kernel under the claim and approval bindings. | Chat-only output is not durable workbench evidence. |
| Keep the first bridge read/preview-only. | Current Codex session has no technical effect sandbox controlled by the server. |
| Fail closed on missing skill, invalid task, duplicate claim, or result mismatch. | The useful signal from `decision-gate` was its refusal to invent missing input. |

## Evidence Boundary

This record is a local observed experiment note. It is not an execution receipt,
an authenticated identity claim, or proof that arbitrary skills can be safely
run. The proposed architecture must create those missing boundaries rather than
renaming the dry-run evidence.
