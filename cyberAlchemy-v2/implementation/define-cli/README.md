# CyberAlchemy Define CLI

This package is the candidate conversational terminal realization of `CA2-CAP-DEFINE-SHARED-MEANING`.
It is ready for local testing, but it is not accepted, published, deployed, or installed globally.

The primary command performs one bounded in-memory lifecycle:

```text
broad domain / subject / context / project opening
  -> persistent ARE gateway
  -> shared app-server RPC client
  -> conversational discovery through the Codex app-server wrapper
  -> explicit scope review and confirmation
  -> candidate meaning options
  -> one-option-at-a-time review
  -> verified ARE route and frozen inline Context Envelope
  -> candidate Definition Pack
```

The agent may reflect, summarize, and propose. It may not silently confirm its own inference.
The exact scope requires a human confirmation, and every option requires an explicit accept,
edit, discuss, or defer action.

## Conversational run

Use the repository-supported Node binary:

```bash
NODE=/home/vrondelli/.nvm/versions/node/v26.8.1/bin/node
$NODE cyberAlchemy-v2/implementation/define-cli/bin/define.mjs
```

You can also supply the broad opening immediately:

```bash
$NODE cyberAlchemy-v2/implementation/define-cli/bin/define.mjs \
  "We are building a knowledge system for clinical research teams and the language is becoming inconsistent"
```

The conversational path connects to the persistent ARE gateway at
`$XDG_RUNTIME_DIR/are-codex/gateway.sock` (or `/run/user/<uid>/are-codex/gateway.sock`) and
creates an ephemeral read-only Codex thread on the `codex:human-chat` interaction lane. The
gateway preserves its consumer runtime across transport reconnects; Define itself does not
create durable conversation storage. Use `--gateway-socket <path>` for a different gateway.

`--direct` is an explicit diagnostic fallback that spawns the strict app-server wrapper for
this process. It does not permit protocol drift and is not the normal conversational path.
Use `--output <path>` to atomically retain the final pack, and `--json` to print the complete
result instead of the compact human summary.

## Advanced scripted run

`define run` retains the deterministic exact-input interface for automation:

```bash
$NODE cyberAlchemy-v2/implementation/define-cli/bin/define.mjs run \
  --goal "Define a release channel" \
  --intent "Remove ambiguity for a local consumer" \
  --context "A release channel names how candidate output reaches a consumer." \
  --consumer local-test \
  --input cyberAlchemy-v2/implementation/define-cli/fixtures/smoke-input.json \
  --json
```

Scripted input has this shape:

```json
{
  "concepts": [{"concept_id":"concept:term","term":"term","question":"What does term mean?","owner_route":"Definitions Governance owner"}],
  "responses": [{"concept_id":"concept:term","action":"propose","payload":{"definition":"Candidate meaning."}}]
}
```

The advanced path supports `reuse`, `specialize`, `propose`, `open`, `defer`, and `refuse`.
Open dispositions cause exit code `4`; they never invent an answer.

Exit codes: `0` complete candidate pack, `2` CLI/input error, `3` context or structural
block, and `4` valid pack with open meaning. All outputs retain `authority_effect: none`.

## Test

```bash
NODE=/home/vrondelli/.nvm/versions/node/v26.8.1/bin/node
cd cyberAlchemy-v2/implementation/define-cli
$NODE --test test/*.test.mjs
```

The candidate intentionally excludes durable sessions, cross-client chat/CLI continuity, canonical definition
promotion, automatic consumer execution, publication, deployment, and global installation.
