# Manual Session Bridge Protocol

## Boundary

This protocol is a loopback-only, one-shot client for the active Codex session.
It does not poll in the background, resolve skills, execute tasks, authenticate
Codex, retry, or perform operator actions.

## Human And Session Sequence

1. The operator prepares, approves, and marks one request ready in Approval Desk.
2. The operator says `poll` in the intended Codex session.
3. The session runs `ready` once and reads the opaque `request_handle`.
4. The session runs `claim` once with its caller-generated `session_ref`.
5. Only the successful claim response reveals task, skill, grants, and context.
6. The session invokes the skill within the L0 read/preview boundary.
7. The session submits one bounded `result`; if it cannot, it submits `interrupt`.
8. Only the operator may release/requeue an interrupted attempt in Approval Desk.

## Commands

```text
npm run bridge:session -- ready [--base-url http://127.0.0.1:8765]
npm run bridge:session -- claim --request-handle <id> --session-ref <id>
npm run bridge:session -- result --claim-id <id> --input <json-file|->
npm run bridge:session -- interrupt --claim-id <id> --input <json-file|->
```

`IDE_EXTENSION_BRIDGE_URL` may set the loopback origin. Non-loopback URLs,
paths, HTTPS origins, and unknown commands are rejected.

## Process Contract

- Exit `0`: one command succeeded; one JSON object is written to stdout.
- Exit `2`: invalid command, options, URL, or input JSON.
- Exit `3`: no ready request, conflict, stale handle, or not-found state.
- Exit `4`: loopback server could not be reached.
- Exit `5`: server rejected the request or returned an invalid response.
- Diagnostics are JSON on stderr. Successful claim data is never logged on an
  error path. Every invocation exits; no timer or child process remains.

Result and interrupt JSON must use the registered v2 request schemas. The
session must not report terminal success in chat unless the result command
returns the kernel-admitted result and execution receipt.
