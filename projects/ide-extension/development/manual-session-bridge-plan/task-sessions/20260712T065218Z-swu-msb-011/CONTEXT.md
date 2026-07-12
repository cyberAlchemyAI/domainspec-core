# Context Pack: SWU-MSB-011

- Task/SWU: `TASK-VALIDATION-WITNESS / SWU-MSB-011`
- Dependency: automated and Chromium gates complete
- Sources: real witness procedure, session bridge protocol, fresh loopback
  workbench, active conversation session
- Runtime: manual human plus active Codex session

## Boundaries And Decisions

- The human privately chooses the read/preview-safe installed skill and concrete
  task; neither is written into this context pack.
- Codex must receive only `poll` after the request is authorized and ready.
- The session may learn task and skill only from a successful atomic claim.
- A chat-only outcome is insufficient; the session must submit a kernel-admitted
  result or interruption.
- This witness proves only the bounded unattested L0 route.

## Preflight

- Fresh event count, envelopes, receipts, ready target: `0 / 0 / 0 / null`.
- Workbench: `http://127.0.0.1:8765/demo/l0`.
- Runtime holder: detached local `tmux` session `ide-extension-msb-011`.
- Temporary state: `/tmp/ide-extension-msb-011-Vrb4AH`.
- Repository HEAD: `996ac595815034043f5717f24db54e1cb70774d8`.
- Runtime source aggregate SHA-256: `f992eef885f15d796ba1d42da94359766ccb0ecafb6f036b2f88982bdfd45a81`.
- Server readiness: pass.
- Human private preparation/authorization/target: pending.
- Gate verdict: BLOCK pending the intended human-only action.

## Postflight

- The human sent only `poll`; no skill or task appeared in the chat trigger.
- Ready inspection exposed only opaque handle
  `env-f5916fc9-1d78-4732-bea0-a6fa0ca43293`.
- Atomic claim was the first session response to disclose skill `invoke` and its
  task, under exact grants `preview.read` and `skill.invoke`.
- The kernel admitted terminal result `flagged`, consumed authorization, and
  minted a bound `skill.execution` receipt beside the authorization receipt.
- All seven receipt evidence routes resolved with HTTP 200.
- Postflight gate verdict: PASS for the bounded blind witness; the result's
  named artifact-status residue is synchronized by the approved follow-up.
