# CyberAlchemy Agent Reasoning Engine

The request-intent vertical compiles user language into immutable Intent
Contracts before model dispatch, separates construction instructions from
visible product requirements, records explicit corrections as successor
reflections, and exposes quiet, explain, inspect, and control projections.
Codex app-server integration is opt-in and defaults to no-op; the intent
benchmark lane measures these distinctions directly.

This directory is the supported product surface for the integrated ARE
stability candidate. It composes deterministic routing, request-aware Context
Envelopes, automatically evolved append-only Reasoning State, an exact-bound
opt-in definition-readiness semantic domain, authenticated restartable Codex
app-server continuity, measured cache-affinity telemetry, and the
real-reasoning benchmark.

Use Node `26.8.1` and begin with:

```sh
node bin/are.mjs doctor --json
node bin/are.mjs test
```

Start the configured app-server gateway with:

```sh
node bin/are.mjs gateway \
  --config packages/codex-app-server-wrapper/profiles/repository-v1.json \
  --repository-root /path/to/domainspec-core \
  --listen /run/user/$(id -u)/are-codex/gateway.sock
```

`node bin/are.mjs benchmark --mode core` and `node bin/are.mjs define ...`
expose the benchmark and Define integration through the same product entrypoint.

Run the fixture-only model-driven coding-agent vertical with explicit
per-action approval:

```sh
node bin/are.mjs coding-agent demo --approve --keep
```

This command uses the scripted model transport, changes only a newly created
temporary fixture, runs its tests in a separate verifier process, and returns
a bounded patch-candidate receipt. The package also exposes a Codex App Server
transport adapter for an already initialized RPC client and thread. Run the
combined live path with `npm run coding-agent:canary`; it invokes one real model
turn through the restartable gateway and applies the captured candidate only to
an ephemeral fixture after authenticated gateway recovery.

The default product performs no semantic evaluation or effects. The configured
definition-readiness domain activates only when explicitly enabled. Cache
affinity is an optimization, provider cache use is reported only from configured
provider fields, and session expiration never truncates an append-only ledger.
Restart recovery replays completed stable requests and blocks unknown crash-time
outcomes instead of redispatching them. This
engineering stability candidate does not itself grant acceptance, publication,
deployment, or external-effect authority. The coding-agent vertical is an L2
live-session candidate with one controlled gateway restart/reconnect canary;
it does not claim general live-model reliability, proxy installation, network
isolation, or a production sandbox.
