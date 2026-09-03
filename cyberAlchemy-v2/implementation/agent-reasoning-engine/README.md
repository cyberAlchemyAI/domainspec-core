# CyberAlchemy Agent Reasoning Engine

This directory is the supported product surface for the integrated ARE
stability candidate. It composes deterministic routing, request-aware Context
Envelopes, append-only reusable Reasoning State, opt-in semantic evaluation,
authenticated Codex app-server continuity, exact cache-affinity telemetry, and
the real-reasoning benchmark.

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

The default product performs no semantic evaluation or effects. Cache affinity
is an optimization, provider cache use is reported only when explicitly
observed, and session expiration never truncates the append-only ledger. This
engineering stability candidate does not itself grant acceptance, publication,
deployment, or external-effect authority.
